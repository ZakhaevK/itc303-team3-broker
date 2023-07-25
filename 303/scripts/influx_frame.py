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
#print(token)

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
    command = [
        'docker', 'exec', 'test-influxdb-1', 'influx',
        'delete', '--bucket', 'DPI', '--start', '1970-01-01T00:00:00Z',
        '--stop','2024-01-01T00:00:00Z'
    ]
    return subprocess.run(command, capture_output=True, text=True)

#TODO: IMPLEMENT THIS
def query_db(query: str):
    try:
        tables = query_api.query(query)
        
        results = []
        for table in tables:
            for record in table.records:
                #print(query)
                #print(record)
                results.append(record.values)     
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

   
