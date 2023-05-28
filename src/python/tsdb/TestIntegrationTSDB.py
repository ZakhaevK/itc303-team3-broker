from asyncio import queues
import subprocess
import time
import requests
#
# integration tests for confirming it is working inside docker compose stack
# should only be run in test env as it will add data to lts_exchange
#

#set a bunch of probably to never change prerequsites
exchange='lts_exchange'
queue='ltsreader_logical_msg_queue'
mq_user='broker'
mq_pass='CHANGEME'
hostname="localhost"
receive_port=9000
bucket_name="dpi"


#helper, easier to just send via cmdline
def send_msg(msg: str):
    command = [
        'docker', 'exec', 'test-mq-1', 'rabbitmqadmin',
        'publish', '-u', mq_user, '-p', mq_pass,
        f'exchange={exchange}', f'routing_key={queue}',
        f'payload={msg}', 'properties={}'
    ]
    return subprocess.run(command, capture_output=True, text=True)


#another helper
def get_last_insert():
    return requests.get(
    f'http://{hostname}:{receive_port}/exp',
    {
        'query':f'SELECT * FROM {bucket_name} LIMIT -1'
    }).text


def test_send_valid_msg():
    msg = """
    {
        "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
        "p_uid": 999,
        "l_uid": 666,
        "timestamp": "2023-01-30T06:21:56Z",
        "timeseries": [
        {
            "name": "battery (v)",
            "value": 6.66
        }
        ]
    }
    """
    result = send_msg(msg)
    time.sleep(1)
    last_insert = get_last_insert()
    assert(result.stdout == "Message published\n")
    assert(last_insert == '"p_uid","l_uid","battery v","timestamp"\r\n"999","666",6.66,"2023-01-30T06:21:56.000000Z"\r\n')


def test_send_invalid_msg():
    msg = """
    {
        "l_uid": 777,
        "timestamp": "2023-01-30T06:21:56Z",
        "timeseries": [
        {
        }
        ]
    }
    """
    result = send_msg(msg)
    #should still be last insert!
    last_insert = get_last_insert()
    assert(result.stdout == "Message published\n")
    assert(last_insert == '"p_uid","l_uid","battery v","timestamp"\r\n"999","666",6.66,"2023-01-30T06:21:56.000000Z"\r\n')


#check we can still send a message after a bad one
def test_send_valid_msg2():
    msg = """
    {
        "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
        "p_uid": 123,
        "l_uid": 456,
        "timestamp": "2023-01-30T06:22:56Z",
        "timeseries": [
        {
            "name": "battery (v)",
            "value": 9.99
        }
        ]
    }
    """
    result = send_msg(msg)
    time.sleep(1)
    last_insert = get_last_insert()
    assert(result.stdout == "Message published\n")
    assert(last_insert == '"p_uid","l_uid","battery v","timestamp"\r\n"123","456",9.99,"2023-01-30T06:22:56.000000Z"\r\n')
