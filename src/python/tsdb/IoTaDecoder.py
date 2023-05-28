from questdb.ingress import Sender, IngressError
import requests
import sys
from dateutil import parser
import json

bucket_name = "dpi"
tsdb_host_name = "quest"
tsdb_port = 9009

def parse_json_msg(msg: str) -> None:
    """
    This function is the main message parser, it will convert IoTa format to something TSDB can insert
    """

    #try convert to json object if it is not
    if not isinstance(msg, dict):
        try:
            msg = json.loads(msg)
        except Exception as e:
            sys.stderr.write(f'error: wrong format {e}\n')
            return None, None, None

    try:
        syms = {"p_uid" : f'{msg["p_uid"]}', "l_uid" : f'{msg["l_uid"]}'}
        cols = {clean_names(item['name']):item['value'] for item in msg['timeseries']}
        timestamp = parser.parse(msg['timestamp'])
        return syms, cols, timestamp
    except Exception as e:
        sys.stderr.write(f'error: unable to parse {e}\n')
        return None, None, None


def insert_line_protocol(syms: str, cols: str, timestamp: str, hostname=tsdb_host_name, port=tsdb_port, bucket=bucket_name) -> None:
    """
    This function will insert a message via line protocol to questdb
    """
    try:
        with Sender(hostname,port) as sender:
            sender.row(
                bucket,
                symbols=syms,
                columns=cols,
                at=timestamp
            )
            sender.flush()
    except IngressError as e:
        sys.stderr.write(f'error: {e}\n')


def clean_names(msg: str) -> str:
    """
    Table and column names must not contain any of the forbidden characters: 
    \n \r ? , : " ' \\ / \0 ) ( + * ~ %

    Additionally, table name must not start or end with the . character. 
    Column name must not contain . -
    """
    translation_table = str.maketrans("", "", "\n\r?,:\"'\\/).(+*~%.-")
    return msg.translate(translation_table)
