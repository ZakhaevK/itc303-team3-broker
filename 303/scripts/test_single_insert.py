import time
import sys
from test_frame import *

BATCH_SIZE=10000
BLOCK_SIZE=64*1024 #questdb auto flushes at 64kb, so probably most efficient
GROUP_SIZE=200

def run_single_test(test_file_name):
    msg_gen = get_test_msgs(test_file_name, BATCH_SIZE)
    poll_state = PollState()
    poll_state.num_tests = count_measurements(test_file_name, "name")

    print("SINGLE_INSERT:")
    print(f"Total Messages: {count_lines(test_file_name)}")
    print(f"Total Measurements: {poll_state.num_tests}")

    poll_state.start_time = time.time()

    for msgs in msg_gen:
        for msg in msgs:
            send_msg(msg)

    poll_db(poll_state)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("requires arg: test_file_name")
        sys.exit(1)

    try:
        clean_up_db()
        run_single_test(sys.argv[1])
        clean_up_db()
    except KeyboardInterrupt:
        clean_up_db()
        sys.exit(0)
