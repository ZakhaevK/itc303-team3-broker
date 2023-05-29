"""
This program receives logical device timeseries messages and decodes message 
into time series data and inserts into QuestDB time series database

skeleton is based off LTSReader.py
"""
import asyncio, json, logging, signal, sys

from pika.exchange_type import ExchangeType
import api.client.RabbitMQ as mq
import BrokerConstants
import util.LoggingUtil as lu
import api.client.DAO as dao

from questdb.ingress import Sender, IngressError
from dateutil import parser

#TODO: move these to .env file
bucket_name = "dpi"
tsdb_host_name = "quest"
tsdb_port = 9009

#TODO: move these to main end check it doesn't break anything
rx_channel = None
mq_client = None
finish = False


def sigterm_handler(sig_no, stack_frame) -> None:
    """
    Handle SIGTERM from docker by closing the mq and db connections and setting a
    flag to tell the main loop to exit.
    """
    global finish, mq_client

    logging.info(f'Caught signal {signal.strsignal(sig_no)}, setting finish to True')
    finish = True
    mq_client.stop()
    dao.stop()


async def main():
    """
    Initiate the connection to RabbitMQ and then idle until asked to stop.

    Because the messages from RabbitMQ arrive via async processing this function
    has nothing to do after starting connection.
    """
    global mq_client, rx_channel, finish

    logging.info('===============================================================')
    logging.info('               STARTING IoTaDecoder (TSDB ENCODER)             ')
    logging.info('===============================================================')

    # The routing key is ignored by fanout exchanges so it does not need to be a constant.
    # Change the queue name. This code should change to use a server generated queue name.
    rx_channel = mq.RxChannel(
        BrokerConstants.LOGICAL_TIMESERIES_EXCHANGE_NAME, exchange_type=ExchangeType.fanout, 
        queue_name='ltsreader_logical_msg_queue', on_message=on_message, routing_key='logical_timeseries'
    )
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


    """
    dao.get_current_device_mapping(luid..)
    ==
    pd=PhysicalDevice(
        uid=1, source_name='ttn', name='Test Sensor 1', location=Location(lat=-34.3372, long=508.6245),
        last_seen=None, source_ids={'app_id': 'ttn-app-id-1', 'dev_id': 'ttn-device-id-1', 'dev_eui': 'ttn-dev-eui-1'},
        properties={'description': 'Sample Test Device Properties'})
    ld=LogicalDevice(
        uid=1, name='Test Sensor 1', location=Location(lat=-34.3372, long=508.6245),
        last_seen=None, properties={'description': 'Sample Test Device Properties'})
        start_time=datetime.datetime(2023, 5, 29, 13, 49, 33, 240101,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=36000)))
        end_time=None
    """

    global rx_channel, finish

    delivery_tag = method.delivery_tag

    # If the finish flag is set, reject the message so RabbitMQ will re-queue it
    # and return early.
    if finish:
        rx_channel._channel.basic_reject(delivery_tag)
        return

    try:
        msg = json.loads(body)
        lu.cid_logger.info(f'Received Message: {msg}', extra=msg)

        #TODO:add checks and create uid for puid + luid
        #logging.info(dao.get_current_device_mapping(msg['l_uid']))

        syms, cols, timestamp = parse_json_msg(msg)
        if syms is not None:
            insert_line_protocol(syms, cols, timestamp)
            rx_channel._channel.basic_ack(delivery_tag)
            return
    except Exception as e:
        lu.cid_logger.error(f'Unable to process LTS message: {e}')
        rx_channel.channel.basic_reject(delivery_tag)
        return

    # This tells RabbitMQ the message is handled and can be deleted from the queue
    #rx_channel._channel.basic_ack(delivery_tag)
    rx_channel.channel.basic_reject(delivery_tag)

def parse_json_msg(msg: str) -> str:
    """
    This function is the main message parser, 
    it will convert IoTa format to something TSDB can insert
    """

    #try convert to json object if it is not
    if not isinstance(msg, dict):
        try:
            msg = json.loads(msg)
        except Exception as e:
            sys.stderr.write(f'error: wrong format {e}\n')
            return None, None, None

    try:
        syms = {"p_uid" : f'{msg["p_uid"]}', "l_uid" : f'{msg["l_uid"]}'}
        cols = {clean_names(item['name']):item['value'] for item in msg['timeseries']}
        timestamp = parser.parse(msg['timestamp'])
        return syms, cols, timestamp
    except Exception as e:
        sys.stderr.write(f'error: unable to parse {e}\n')
        return None, None, None


def insert_line_protocol(syms: str, cols: str, timestamp: str, 
                         hostname=tsdb_host_name, port=tsdb_port, 
                         bucket=bucket_name
                         ) -> int:
    """
    This function will insert a message via line protocol to questdb
    """
    try:
        with Sender(hostname,port) as sender:
            sender.row(
                bucket,
                symbols=syms,
                columns=cols,
                at=timestamp
            )
            sender.flush()
        return 200
    except IngressError as e:
        sys.stderr.write(f'error: {e}\n')
        return 400


def clean_names(msg: str) -> str:
    """
    Table and column names must not contain any of the forbidden characters: 
    \n \r ? , : " ' \\ / \0 ) ( + * ~ %

    Additionally, table name must not start or end with the . character. 
    Column name must not contain . -
    """
    translation_table = str.maketrans("", "", "\n\r?,:\"'\\/).(+*~%.-")
    return msg.translate(translation_table)


if __name__ == '__main__':
    # Docker sends SIGTERM to tell the process the container is stopping so set
    # a handler to catch the signal and initiate an orderly shutdown.
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Ctrl-C sends SIGINT, handle it the same way.
    signal.signal(signal.SIGINT, sigterm_handler)

    # Does not return until SIGTERM is received.
    asyncio.run(main())
    logging.info('Exiting.')
