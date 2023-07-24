import pytest
import subprocess
import random
import requests
import json
import time
from datetime import datetime

# helper
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

#helper

def generate_message():
    corr_id = random.randint(100000, 9999999)
    p_uid = random.randint(1, 200)
    l_uid = random.randint(1, 400)
    value = str(random.randint(0, 30))

    msg = "{\"broker_correlation_id\": " + str(corr_id) + \
    ", \"p_uid\": " + str(p_uid) + \
    ", \"l_uid\": " + str (l_uid) + \
    ", \"timestamp\": \"2023-01-30T06:21:56Z\", " +  \
    "\"timeseries\": [{\"name\": \"battery (v)\"," + \
    "\"value\": " + str(value) + "}]}"

    return msg, value

def extract_value(message):
    json_dict = json.loads(message)
    return json_dict["timeseries"][0]["value"]


def get_db_response(query):
    host = "localhost"
    port = "9090"    
    response = requests.get("http://" + host + ":" + port + "/api/v1/query",
        params= {"query" : query }).text
    response = json.loads(response)
    #print(response)
    return response    

def get_db_response_range(query, start, end):
    host = "localhost"
    port = "9090"    
    response = requests.get("http://" + host + ":" + port + "/api/v1/query_range",
        params= {"query" : query , "start": start, "end" : end, "step" : "300ms"}).text
    response = json.loads(response)
    #print(response)
    return response 

def single_insert_time_test():
    msg = ""
    # print(msg)
    with open("single_1", "r") as msg_file:
        msg = msg_file.readline()
    start_time = time.time()
    send_message(msg)
    while True:
        response = get_db_response()
        test_val = response["data"]["result"][0]["value"][1]
        if val == (test_val):
            break 
    end_time = time.time()
    total_time = end_time - start_time
    print("Time for single insert: " + str(total_time))

def multi_insert_time_test():
    time.sleep(2)
    messages = []
    with open("bulk_1000", "r") as msg_file:
        for index, line in enumerate(msg_file):
            messages.append(line)
            if index == 999:
                break

    start_time = time.time()
    for i in range(1000):
        # msg, val = generate_message()
        msg = messages[i]
        val = extract_value(msg)
        send_message(msg)      
        # time.sleep(0.3)  
        # print("progressing!")
        while True:
            response = get_db_response()
            test_val = response["data"]["result"][0]["value"][1]
            # print(str(i) + ", " + str(val) + ", " + str(test_val))
            # time.sleep(1)
            if (val) == eval(test_val):
                break               
    end_time = time.time()
    total_time = end_time - start_time
    print("Time for multi (1000) insert: " + str(total_time))

def query_time_test():
    start_time = time.time()
    print(get_db_response("count(sensor_value)"))    
    print(get_db_response("sensor_value"))    
    print(get_db_response_range("sensor_value", "2023-01-05T05:00:00.000000Z", datetime.now().isoformat()))
    print(get_db_response_range("sensor_value", "2023-01-04T00:00:00.000000Z", "2023-01-05T00:00:00.000000Z"))
    print(get_db_response_range("count(sensor_value)", "2023-01-04T00:00:00.000000Z", "2023-01-05T00:00:00.000000Z"))    
    print(get_db_response_range("sensor_value{name=\"gnss\"} and sensor_value > 20", "2023-01-04T00:00:00.000000Z", "2023-01-05T00:00:00.000000Z"))
    print(get_db_response_range("count(sensor_value{name=\"gnss\"} and sensor_value > 20)", "2023-01-04T00:00:00.000000Z", "2023-01-05T00:00:00.000000Z"))
    print(get_db_response_range("count(sensor_value{name=\"gnss\"} and sensor_value > 20 and sensor_value < 25)", "2023-01-04T00:00:00.000000Z", "2023-01-05T00:00:00.000000Z"))
    print(get_db_response_range("sensor_value{name=\"gnss\"} and sensor_value > 20 and sensor_value < 25", "2023-01-04T00:00:00.000000Z", "2023-01-05T00:00:00.000000Z"))
    end_time = time.time()
    print("Time for a single query: " + str(end_time - start_time))

if __name__ == "__main__":
    single_insert_time_test()
    query_time_test()
    multi_insert_time_test()    