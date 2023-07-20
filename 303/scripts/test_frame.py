import subprocess
import os
import time
from influx_frame import *

# MQ stuff
mq_user = 'broker'
mq_pass = 'CHANGEME'
host_name = 'localhost'

# Test stuff
poll_interval = 100  # How often to poll the DB to check how many inserts


class PollState:
    def __init__(self):
        #self.should_poll = True
        self.start_time = 0.0
        self.num_tests = 0


def count_lines(test_file_name):
    """
    Counts lines in ./${test_file_name} file to determine how many tests we're running.
    """
    file_path = os.path.join(os.path.dirname(__file__), test_file_name)
    return sum(1 for _ in open(file_path))

def count_measurements(test_file_name, word):
    """
    mainly for influx, counts the measurements in a file (ie how many "names" there are)
    """
    count = -1
    file_path = os.path.join(os.path.dirname(__file__), test_file_name)
    with open(file_path, 'r') as file:
        for line in file:
            count += line.lower().count(word.lower())
    return count


def get_test_msgs(test_file_name, n):
    """
    Returns an array of all the messages in the ./${test_file_name} file.
    """
    file_path = os.path.join(os.path.dirname(__file__), test_file_name)
    with open(file_path, 'r') as file:
        while True:
            batch = [line.strip() for _, line in zip(range(n), file)]
            if not batch:
                break
            yield batch


def poll_db(poll_state):
    st = time.time()
    last_response = None
    dura = 0
    while True:
        response = get_count()

        if response == str(poll_state.num_tests):
            stop_test(response,poll_state)
            return

        if response == last_response:
            dura = time.time()-st
            if dura >= 10:
                print("timed out")
                stop_test(response,poll_state)
                return
        else:
            st = time.time()
            dura = 0.0
            last_response = response

        time.sleep(poll_interval / 1000)


def stop_test(msg: str, poll_state):
    taken = time.time() - poll_state.start_time
    print(f'Time Taken: {taken}')
    print(f'Per Test: {taken / poll_state.num_tests}')



def send_msg(msg: str, exchange='lts_exchange', queue='ltsreader_logical_msg_queue'):
    command = [
        'docker', 'exec', 'test-mq-1', 'rabbitmqadmin',
        'publish', '-u', mq_user, '-p', mq_pass,
        f'routing_key={queue}',
        f'payload={msg}', 'properties={}'
    ]
    return subprocess.run(command, capture_output=True, text=True)


def append_lines_by_fixed_size(lines, group_size):
    num_lines = len(lines)
    grouped_lines = []

    for i in range(0, num_lines, group_size):
        group = ','.join(lines[i:i+group_size])
        grouped_lines.append('{"data":['+group+']}')

    return grouped_lines


def append_lines_by_block_size(lines, block_size):
    grouped_lines = []
    current_group = []
    current_size = 0

    for line in lines:
        line_size = len(line.encode('utf-8'))
        if current_size + line_size <= block_size:
            current_group.append(line)
            current_size += line_size
        else:
            grouped_lines.append('{"data":[' + ','.join(current_group) + ']}')
            current_group = [line]
            current_size = line_size

    if current_group:
        grouped_lines.append('{"data":[' + ','.join(current_group) + ']}')

    return grouped_lines
