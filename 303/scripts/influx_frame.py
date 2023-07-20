#db specific stuff goes here i guess
import os
import requests
import subprocess
import re
from influxdb_client import InfluxDBClient, Query

def get_token():
    command = [
        'docker', 'exec', 'test-lts-1', 'cat', '../../../shared/token'
    ]
    return subprocess.run(command, capture_output=True, text=True).stdout.strip()

# DB stuff
receive_port=8086
bucket_name="DPI"
org = "ITC303"
url = "http://localhost:8086"
token = get_token()
print(token)

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()


def get_token():
    command = [
        'docker', 'exec', 'test-lts-1', 'cat', '../../../shared/token'
    ]
    return subprocess.run(command, capture_output=True, text=True).stdout.strip()


#TODO: IMPLEMENT THIS
def get_count() -> str:
    with client:
        query=f'''
            from(bucket: "{bucket_name}")
            |> range(start: -1y)
            |> count()
            '''
    result = query_api.query(query=query)
    count = 0
    results = []
    for table in result:
        for record in table.records:
            count+=1
            results.append((record.get_field(), record.get_value()))
    #print(count)

    #records = result[0].records[0]
    #print(result[0])
    return str(count)


#TODO: implement this
def clean_up_db():
    return "0"
#   requests.get(
#       f'http://{hostname}:{receive_port}/exp',
#       {
#           'query':f'DROP TABLE {bucket_name}'
#       }).text

#TODO: IMPLEMENT THIS
def query_db(msg: str):
    response = requests.get(f'http://localhost:8086/exp',
    {
        'query':f'{msg}'
        }).text
    print(response)
    return response
       
   
