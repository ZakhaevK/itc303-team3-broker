import json
import time
import time
from dateutil import parser

def parse_msg(msg):
    line = []
    if not isinstance(msg, dict):
        try:
            msg = json.loads(msg)
        except Exception as e:
            logging.info(f'error: wrong format {e}\n')
            return None

    l_uid = msg['l_uid']
    p_uid = msg['p_uid']
    timestamp = int(time.mktime(parser.parse(msg['timestamp']).timetuple()))
    measurements = msg['timeseries']

    for measurement in measurements:
        measurement_name = clean_names(measurement['name'])
        measurement_value = measurement['value']

        #TODO: fix me
        if measurement_value == "NaN" or measurement_name == "Device":
            continue
 
        line = f"{measurement_name},l_uid={l_uid},p_uid={p_uid} {measurement_name}={measurement_value} {timestamp}"
        return line
    return None


def clean_names(msg: str) -> str:
    """
    Table and column names must not contain any of the forbidden characters: 
    \n \r ? , : " ' \\ / \0 ) ( + * ~ %
    Additionally, table name must not start or end with the . character. 
    Column name must not contain . -
    """
    translation_table = str.maketrans("", "", "\n\r?,:\"'\\/).(+*~%.-")
    return msg.translate(translation_table)
