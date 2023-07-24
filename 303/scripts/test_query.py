import time
import sys
from test_bulk_insert import GROUP_SIZE
from test_frame import *


BATCH_SIZE=100
GROUP_SIZE=100
ITERATIONS=1


def run_query_test(test_file_name):
    msg_gen = get_test_msgs(test_file_name, BATCH_SIZE)
    poll_state = PollState()
    poll_state.num_tests = count_lines(test_file_name)

    #print("QUERY_TESTS:")
    print(f"Total Queries: {poll_state.num_tests}")
    print(f"Total Iterations: {ITERATIONS}")

    poll_state.start_time = time.time()

    for msgs in msg_gen:
        for msg in msgs:
            for i in range(ITERATIONS+1):
                query_db(msg)

    taken = time.time() - poll_state.start_time
    print(f'Time Taken: {taken}')
    print(f'Per Query: {taken / (poll_state.num_tests+ITERATIONS)}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("requires arg: test_file_name")
        sys.exit(1)

    try:
        #clean_up_db()
        run_query_test(sys.argv[1])
        #clean_up_db()
    except KeyboardInterrupt:
        #clean_up_db()
        sys.exit(0)
