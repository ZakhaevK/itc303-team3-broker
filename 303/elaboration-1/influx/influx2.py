#! /usr/bin/python3

from datetime import datetime
import time
from dateutil import parser
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import math

#variables for connecting to the db
token = os.environ.get("INFLUXDB_TOKEN")
org = "ITC303"
url = "http://localhost:8086"

#connect to the db
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

#create bucket for data storage
bucket="DPI"

#create a writeAPI client
write_api = client.write_api(write_options=SYNCHRONOUS)

"""
def parse_input_file() -> None:
  f = open("../../docs/sample_messages", "r")
  l = f.readlines()
  for line in l:
    return msg_parser(json.loads(line))

def msg_parser(msg: str) -> None:
    ret = f'DPI,p_uid={msg["p_uid"]},l_uid={msg["l_uid"]} '
    ret += ",".join([f"{i['name']}={i['value']}" for i in msg["timeseries"]])
    ret += " " + str(time.mktime(parser.parse(msg['timestamp']).timetuple()))
    return ret
"""

#define a function to parse json message and convert to influxdb line protocol
def json_to_line_protocol(json_msg):
  parsed_msg = json.loads(json_msg)
  l_uid = parsed_msg['l_uid']
  p_uid = parsed_msg['p_uid']
  timestamp = int(time.mktime(parser.parse(parsed_msg['timestamp']).timetuple())*1000)
  #ts_datetime = datetime.fromisoformat(timestamp)
  #ts_unix = int(ts_datetime.timestamp()*1000)
  measurements = parsed_msg['timeseries']
  lines = []
  for measurement in measurements:
    measurement_name = measurement['name']
    measurement_value = measurement['value']
    if measurement_value == "NaN":
        continue
    line = f"{measurement_name},l_uid={l_uid},p_uid={p_uid} value={measurement_value} {timestamp}"
    lines.append(line)
  return "\n".join(lines)


#open json file
with open("../../docs/sample_messages", "r") as f:
  json_msgs = f.readlines()
  lines = [json_to_line_protocol(msg) for msg in json_msgs]
#lines = parse_input_file()
print(lines)
#write lines
write_api = client.write_api(write_options=WriteOptions(batch_size=100, flush_interval=5000, jitter_interval=400, retry_interval = 2500))
write_api.write(bucket=bucket, org=org, record=lines, write_precision="ns")

#example json msg
#
#{
# "broker_correlation_id": "83d04e6f-db16-4280-53f11b2335c6",
# "p_uid": 301,
# "l_uid": 276,
# "timestamp": "2023-01-30T06:21:56Z",
# "timeseries": [
#   {
#   "name": "battery (v)",
#   "value": 4.16008997
#   },
#   {
#   "name": "pulse_count",
#   "value": 1
#   },
#   {"name": "1_Temperature",
#   "value": 21.60000038
#   }
# ]
#}

query_api = client.query_api()

query = """from(bucket: "DPI")
  |> range(start: 0, stop: now())"""
tables = query_api.query(query, org="ITC303")

for table in tables:
  for record in table.records:
    print(record)


