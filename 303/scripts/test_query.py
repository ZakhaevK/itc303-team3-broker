import time
import sys
from test_frame import *


def run_query_test(test_file_name, iterations: int):
    with open(test_file_name, "r") as file:
        queries = file.read()
        
    query_list = [query.strip() for query in queries.split('\n\n') if query.strip()]
    
    #print("Queries in the file:")
    #for idx, query in enumerate(query_list):
    #    print(f"Query {idx + 1}:\n{query}")
    
    poll_state = PollState()
    poll_state.num_tests = len(query_list)

    print(f"\nTotal Queries: {poll_state.num_tests}")
    print(f"Total Iterations: {iterations}")

    poll_state.start_time = time.time()

    for msg in query_list:
        for i in range(iterations+1):
            try:
                query_db(msg)
            except Exception as e:
                print(f"Error executing query: {e}")

    taken = time.time() - poll_state.start_time
    print(f'Time Taken: {taken}')
    print(f'Per Query: {taken / (poll_state.num_tests)}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("requires arg: test_file_name iterations")
        sys.exit(1)

    try:
        #clean_up_db()
        run_query_test(sys.argv[1], int(sys.argv[2]))
        #clean_up_db()
    except KeyboardInterrupt:
        #clean_up_db()
        sys.exit(0)
