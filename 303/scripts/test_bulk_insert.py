import time
import sys
from test_frame import *

BATCH_SIZE=10000
BLOCK_SIZE=64*1024 #questdb auto flushes at 64kb, so probably most efficient
GROUP_SIZE=200

def run_bulk_test(test_file_name):
    msg_gen = get_test_msgs(test_file_name, BATCH_SIZE)
    poll_state = PollState()
    poll_state.num_tests = count_lines(test_file_name)

    #print("BULKY_INSERTS:")
    print(f"\nTotal Messages: {poll_state.num_tests}")

    poll_state.start_time = time.time()

    for msgs in msg_gen:
        grouped_msgs = append_lines_by_block_size(msgs, BLOCK_SIZE)
        #grouped_msgs = append_lines_in_groups(msgs, GROUP_SIZE)
        for msg in grouped_msgs:
            send_msg(msg, "TEST_BULK", "bulky_ts_queue")

    poll_db(poll_state)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("requires arg: test_file_name")
        sys.exit(1)

    try:
        create_table()
        clean_up_db()
        run_bulk_test(sys.argv[1])
        #clean_up_db()
    except KeyboardInterrupt:
       #clean_up_db()
        sys.exit(0)
