import pytest
import subprocess
import requests
import json
import time

# helper function
def send_message(msg: str):
    mq_user="broker"
    mq_pass="CHANGEME"
    
    exchange = "lts_exchange"
    queue="ltsreader_logical_message_queue"


    command = [
        'docker', 'exec', 'test-mq-1', 'rabbitmqadmin',
        'publish', '-u', mq_user, '-p', mq_pass,
        f'exchange={exchange}', f'routing_key={queue}',
        f'payload={msg}', 'properties={}'
    ]
    return subprocess.run(command, capture_output=True, text=True)

#another helper
def get_db_response():
    host = "localhost"
    port = "9090"    
    response = requests.get("http://" + host + ":" + port + "/api/v1/query",
        params= {"query" : "sensor_value"}).text
    response = json.loads(response)
    print(response)
    return response

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
    result = send_message(msg)
    time.sleep(1)
    response = get_db_response()    
    assert(result.stdout == "Message published\n")
    assert(response["data"]["result"][0]["value"][1] == "6.66")


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
    time.sleep(2)
    result = send_message(msg)
    time.sleep(1)
    response = get_db_response()    
    assert(result.stdout == "Message published\n")
    assert(len(response["data"]["result"]) == 0)


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
    time.sleep(4)
    result = send_message(msg)
    time.sleep(1)
    response = get_db_response()
    assert(result.stdout == "Message published\n")    
    assert(response["data"]["result"][0]["value"][1] == "9.99")

