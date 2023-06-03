import json
import time
import time
from dateutil import parser
import sys

def parse_msg(msg):
    #line = []
    if not isinstance(msg, dict):
        try:
            msg = json.loads(msg)
        except Exception as e:
            #logging.info(f'error: wrong format {e}\n')
            return None
    try:
        broker_correlation_id = msg['broker_correlation_id']
        l_uid = msg['l_uid']
        p_uid = msg['p_uid']
        timestamp = int(time.mktime(parser.parse(msg['timestamp']).timetuple()))
        measurements = msg['timeseries']

        measures = ""
        for measurement in measurements:
            measurement_name = clean_names(measurement['name'])
            measurement_value = measurement['value']

            #TODO: fix me
            if measurement_value == "NaN" or measurement_name == "Device":
                continue
 
            #append measurements for line
            measures += f"{measurement_name}={measurement_value},"
        return f"{broker_correlation_id},l_uid={l_uid},p_uid={p_uid} " + measures[0:-1] + f" {timestamp}"
    except Exception as e:
        sys.stderr.write(f'Error message: {e}\n')
        #logging.info(f'error: missing information {e}\n')
        return None


def clean_names(msg: str) -> str:
    """
    Table and column names must not contain any of the forbidden characters: 
    \n \r ? , : " ' \\ / \0 ) ( + * ~ %
    Additionally, table name must not start or end with the . character. 
    Column name must not contain . -
    """
    msg = msg.replace(" ", "_")
    translation_table = str.maketrans("", "", "\n\r?,:\"'\\/.+*~%.-")
    return msg.translate(translation_table)
