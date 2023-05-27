from questdb.ingress import Sender, IngressError
import requests
import json
import sys
from dateutil import parser

bucket_name = "dpi"
tsdb_host_name = "quest"
tsdb_port = 9009

def parse_json_msg(msg: str) -> None:
    """
    This function is the main message parser, it will convert IoTa format to something TSDB can insert
    """
    #syms = {"p_uid" : f'{msg["p_uid"]}', "l_uid" : f'{msg["l_uid"]}'}
    syms = {}
    cols = {clean(item['name']):item['value'] for item in msg['timeseries']}
    cols['p_uid'] = msg['p_uid']
    cols['l_uid'] = msg['l_uid']
    timestamp = parser.parse(msg['timestamp'])
    insert_line_protocol(syms, cols, timestamp)


def insert_line_protocol(syms: str, cols: str, timestamp: str) -> None:
    """
    This function will insert a message via line protocol to questdb
    """
    try:
        with Sender(tsdb_host_name,tsdb_port) as sender:
            sender.row(
                bucket_name,
                symbols=syms,
                columns=cols,
                at=timestamp
            )
            sender.flush()
    except IngressError as e:
        sys.stderr.write(f'error: {e}\n')


def clean(msg: str) -> str:
    return msg.replace('(','').replace(')','').replace('/','')


def get_all_inserts() -> str:
    """
    This function is helper, to simply return all data in db
    REMOVE ME AFTER TESTING
    """

    return requests.get(
        f'http://{tsdb_host_name}:{tsdb_port}/exec',
        {
            'query':f'{bucket_name} ORDER BY l_uid;'
        }
    ).text

