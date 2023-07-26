import subprocess
import time
import time
from influxdb_client import InfluxDBClient
#
# integration tests for confirming it is working inside docker compose stack
# should only be run in test env as it will add data to lts_exchange
#
def get_token():
    command = [
        'docker', 'exec', 'test-lts-1', 'cat', '../../../shared/token'
    ]
    return subprocess.run(command, capture_output=True, text=True).stdout.strip()

#set a bunch of probably to never change prerequsites
exchange='lts_exchange'
queue='ltsreader_logical_msg_queue'
mq_user='broker'
mq_pass='CHANGEME'
hostname="localhost"
receive_port=8086
bucket_name="DPI"
org = "ITC303"
url = "http://localhost:8086"
token = get_token()
print(token)


client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()


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
    with client:
        query =f'''
            from(bucket: "{bucket_name}")
            |> range(start: 0)
            |> last()
        '''
    result = query_api.query(query=query)
    records = result[0].records[0]
    #this does not get all of the info we submit, just enough to confirm it was accepted into DB
    return str(f'p_uid:{records["p_uid"]},l_uid:{records["l_uid"]},{records["_field"]}:{records["_value"]}')



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
   assert(last_insert == "p_uid:999,l_uid:666,battery_(v):6.66")


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
    time.sleep(1)
    last_insert = get_last_insert()
    assert(result.stdout == "Message published\n")
    assert(last_insert == "p_uid:999,l_uid:666,battery_(v):6.66")


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
    assert(last_insert == 'p_uid:123,l_uid:456,battery_(v):9.99')
