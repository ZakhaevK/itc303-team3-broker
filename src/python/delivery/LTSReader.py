"""
This program receives logical device timeseries messages and logs
them as a test of having multiple queues attached to the logical_timeseries exchange.

It can be used as a template for any program that wants to read from the logical
timeseries exchange. To do that, change the queue name to something unique.
"""

import asyncio, json, logging, signal

from pika.exchange_type import ExchangeType
import api.client.RabbitMQ as mq
import BrokerConstants
import util.LoggingUtil as lu

rx_channel = None
mq_client = None
finish = False

from datetime import datetime
import time
from dateutil import parser
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import math
import os

#variables for connecting to the db
##lu.cid_logger.info(f"USING TOKEN: {token}")





def sigterm_handler(sig_no, stack_frame) -> None:
    """
    Handle SIGTERM from docker by closing the mq and db connections and setting a
    flag to tell the main loop to exit.
    """
    global finish, mq_client

    logging.info(f'Caught signal {signal.strsignal(sig_no)}, setting finish to True')
    finish = True
    mq_client.stop()


async def main():
    """
    Initiate the connection to RabbitMQ and then idle until asked to stop.

    Because the messages from RabbitMQ arrive via async processing this function
    has nothing to do after starting connection.
    """
    global mq_client, rx_channel, finish

    logging.info('===============================================================')
    logging.info('               STARTING LOGICAL_TIMESERIES TEST READER')
    logging.info('===============================================================')

    # The routing key is ignored by fanout exchanges so it does not need to be a constant.
    # Change the queue name. This code should change to use a server generated queue name.
    rx_channel = mq.RxChannel(BrokerConstants.LOGICAL_TIMESERIES_EXCHANGE_NAME, exchange_type=ExchangeType.fanout, queue_name='ltsreader_logical_msg_queue', on_message=on_message, routing_key='logical_timeseries')
    mq_client = mq.RabbitMQConnection(channels=[rx_channel])
    asyncio.create_task(mq_client.connect())

    while not rx_channel.is_open:
        await asyncio.sleep(0)

    while not finish:
        await asyncio.sleep(2)

    while not mq_client.stopped:
        await asyncio.sleep(1)


def on_message(channel, method, properties, body):
    """
    This function is called when a message arrives from RabbitMQ.
    """

    global rx_channel, finish

    delivery_tag = method.delivery_tag

    # If the finish flag is set, reject the message so RabbitMQ will re-queue it
    # and return early.
    if finish:
        rx_channel._channel.basic_reject(delivery_tag)
        return

    #for now it will go hear as manually setting token, should be outside at start up
    token = "UNABLE TO FIND TOKEN"
    with open("../../../shared/token", 'r') as file:
        token = file.readline().strip()
    org = "ITC303"
    url = "http://influx:8086"
    bucket="DPI"

#connect to the db
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    try:
        logging.info(f'USING TOKEN = {token}\n')
        msg = json.loads(body)
        logging.info(f'Accepted message {msg}\n', extra=msg)
        line=[]
        line.append(json_to_line_protocol(msg))
        
        logging.info(f'LINE={line}\n')
        write_api.write(bucket=bucket, org=org, record=line, write_precision="s")
    except Exception as e:
        logging.info(f'Error processing message: {e}\n')
    #
    # Message processing goes here
    #

    # This tells RabbitMQ the message is handled and can be deleted from the queue.    
    rx_channel._channel.basic_ack(delivery_tag)


def json_to_line_protocol(parsed_msg):
    l_uid = parsed_msg['l_uid']
    p_uid = parsed_msg['p_uid']
    timestamp = int(time.mktime(parser.parse(parsed_msg['timestamp']).timetuple()))
    measurements = parsed_msg['timeseries']

    for measurement in measurements:
        measurement_name = measurement['name']
        measurement_value = measurement['value']

        if measurement_value == "NaN" or measurement_name == "Device":
            continue
 
        line = f"{measurement_name},l_uid={l_uid},p_uid={p_uid} {measurement_name}={measurement_value} {timestamp}"
        return line
    return None


if __name__ == '__main__':
    # Docker sends SIGTERM to tell the process the container is stopping so set
    # a handler to catch the signal and initiate an orderly shutdown.
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Ctrl-C sends SIGINT, handle it the same way.
    signal.signal(signal.SIGINT, sigterm_handler)

    # Does not return until SIGTERM is received.
    asyncio.run(main())
    logging.info('Exiting.')
