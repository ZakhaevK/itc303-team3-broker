from TestFunctions import *
import json
import time
import requests

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
    parsed = parse_msg(msg)
    assert(parsed=="battery v,l_uid=276,p_uid=301 battery v=4.16008997 1675023716")
    
def test_receive_valid_multi_ts_msg():
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
    #parse message
    parsed = parse_msg(msg)
    assert(parsed=="")
    
def test_receive_invalid_format_msg():
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
    #pass message (valid format)
    parsed = parse_msg(json.loads(msg))
    assert(parsed == "battery v,l_uid=276,p_uid=301 battery v=4.16008997 1675023716")
    
def test_receive_invalid_formatted_msg():
    msg = """
    {

      "timeseries": [
        {

        }
      ]
    }
    """
    #pass message (invalid format)
    parsed = parse_msg(msg)
    assert(parsed == "")
