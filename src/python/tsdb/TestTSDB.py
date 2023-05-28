from IoTaDecoder import *
import json
import time

## UNIT TESTS

#test receiving messages::::
def test_receive_valid_one_ts_msg():
    msg = """
    {
      "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
      "p_uid": 301,
      "l_uid": 276,
      "timestamp": "2023-01-30T06:21:56Z",
      "timeseries": [
        {
          "name": "battery (v)",
          "value": 4.16008997
        }
      ]
    }
    """
    #parse message
    syms, cols, timestamp = parse_json_msg(json.loads(msg))
    assert syms == {'l_uid': '276', 'p_uid': '301'}
    assert cols == {'battery v': 4.16008997}
    assert timestamp.isoformat() == '2023-01-30T06:21:56+00:00'


def test_receive_valid_multi_ts_msg():
    msg = """
    {
        "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
        "p_uid": 31,
        "l_uid": 2111,
        "timestamp": "2023-01-30T06:21:56Z",
        "timeseries": [
        {
            "name": "battery (v)",
            "value": 4.16008997
        },
        {
            "name": "pulse_count",
            "value": 1
        },
        {
            "name": "1_Temperature",
            "value": 21.60000038
        }
        ]
    }
    """
    #parse msg
    syms, cols, timestamp = parse_json_msg(json.loads(msg))
    assert syms == {'l_uid': '2111', 'p_uid': '31'}
    assert cols == {'1_Temperature': 21.60000038, 'battery v': 4.16008997, 'pulse_count': 1}
    assert timestamp.isoformat() == '2023-01-30T06:21:56+00:00'


def test_receive_invalid_fmt_msg():
    msg = """
    {
        "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
        "p_uid": 31,
        "l_uid": 2111,
        "timestamp": "2023-01-30T06:21:56Z",
        "timeseries": [
        {
            "name": "battery (v)",
            "value": 4.16008997
        },
        {
            "name": "pulse_count",
            "value": 1
        },
        {
            "name": "1_Temperature",
            "value": 21.60000038
        }
        ]
    }
    """
    #pass it valid string formatting instead
    syms, cols, timestamp = parse_json_msg(msg)
    assert syms == {'l_uid': '2111', 'p_uid': '31'}
    assert cols == {'1_Temperature': 21.60000038, 'battery v': 4.16008997, 'pulse_count': 1}
    assert timestamp.isoformat() == '2023-01-30T06:21:56+00:00'


def test_receive_invalid_fmtd_msg():
    msg = """
    {
        "timeseries":
        },
        ]
    }
    """
    #pass it invalid string formatting instead
    syms, cols, timestamp = parse_json_msg(msg)
    assert(syms == None)
    assert(cols == None)
    assert(timestamp == None)


def test_receive_missing_puid_msg():
    msg = """
    {
      "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
      "l_uid": 276,
      "timestamp": "2023-01-30T06:21:56Z",
      "timeseries": [
        {
          "name": "battery (v)",
          "value": 4.16008997
        }
      ]
    }
    """
    #parse message missing puid
    syms, cols, timestamp = parse_json_msg(json.loads(msg))
    assert(syms == None)
    assert(cols == None)
    assert(timestamp == None)


def test_receive_missing_luid_msg():
    msg = """
    {
      "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
      "p_uid": 31,
      "timestamp": "2023-01-30T06:21:56Z",
      "timeseries": [
        {
          "name": "battery (v)",
          "value": 4.16008997
        }
      ]
    }
    """
    #parse message missing puid
    syms, cols, timestamp = parse_json_msg(json.loads(msg))
    assert(syms == None)
    assert(cols == None)
    assert(timestamp == None)


def test_receive_missing_ts_msg():
    msg = """
    {
      "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
      "p_uid": 301,
      "l_uid": 276,
      "timestamp": "2023-01-30T06:21:56Z",
      "timeseries": [
        {
        }
      ]
    }
    """
    #parse message
    syms, cols, timestamp = parse_json_msg(json.loads(msg))
    assert(syms == None)
    assert(cols == None)
    assert(timestamp == None)


#tests for cleaning names for db
def test_invalid_db_names():
    assert(clean_names("test\"") == "test")
    assert(clean_names("test\n") == "test")
    assert(clean_names("test\r") == "test")
    assert(clean_names("test.") == "test")
    assert(clean_names("test?") == "test")
    assert(clean_names("test*") == "test")
    assert(clean_names("test~") == "test")
    assert(clean_names("test%") == "test")
    assert(clean_names("test'") == "test")
    assert(clean_names("test\\") == "test")
    assert(clean_names("test/") == "test")
    assert(clean_names("test(") == "test")
    assert(clean_names("test)") == "test")
    assert(clean_names("test-") == "test")

import sys
#tests to confirm insert into db
def test_db_insert():
    hostname = "localhost"
    insert_port = 9009
    receive_port = 9000
    bucket_name = "testingtests"
    msg = """
    {
      "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
      "p_uid": 301,
      "l_uid": 276,
      "timestamp": "2023-01-30T06:21:56Z",
      "timeseries": [
        {
          "name": "battery (v)",
          "value": 4.16008997
        }
      ]
    }
    """
    #parse message
    syms, cols, timestamp = parse_json_msg(json.loads(msg))
    #insert into db
    insert_line_protocol(syms, cols, timestamp, hostname, insert_port, bucket_name)
    #sleep
    time.sleep(1)
    last_insert = requests.get(
        f'http://{hostname}:{receive_port}/exp',
        {
            'query':f'SELECT * FROM {bucket_name} LIMIT -1'
        }).text
    assert(last_insert == '"p_uid","l_uid","battery v","timestamp"\r\n"301","276",4.16008997,"2023-01-30T06:21:56.000000Z"\r\n')

