
import subprocess
import os
import time
from quest_frame import *
import pika

# MQ stuff
mq_user = 'broker'
mq_pass = 'CHANGEME'
host_name = 'localhost'

# Test stuff
poll_interval = 100  # How often to poll the DB to check how many inserts
time_out = 60


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
        count = get_count()
        start_index = count.find('\n') + 1
        response = count[start_index:count.find('\n', start_index)].strip()

        if response == str(poll_state.num_tests):
            stop_test(response,poll_state)
            return

        if response == last_response:
            dura = time.time()-st
            if dura >= time_out:
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


#def send_msg(msg: str, exchange='lts_exchange', queue: str = 'ltsreader_logical_msg_queue') -> str: 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host_name))
    #channel = connection.channel()
    #channel.queue_declare(queue=queue)
    #channel.basic_publish(exchange, routing_key=queue, body=msg)
    #connection.close()
