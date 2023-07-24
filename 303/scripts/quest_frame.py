#db specific stuff goes here i guess
import requests

# DB stuff
hostname = "localhost"  # Will need to be changed if running from inside Docker
receive_port = 9000  # Port to send stuff to
bucket_name = "dpi"  # Bucket/TABLE


def get_count() -> str:
    return requests.get(
        f'http://{hostname}:{receive_port}/exp',
        {
            'query':f'SELECT COUNT(*) FROM {bucket_name}'
        }).text


def clean_up_db():
    requests.get(
        f'http://{hostname}:{receive_port}/exp',
        {
            'query':f'TRUNCATE TABLE {bucket_name}'
        }).text


def query_db(msg: str):
    return requests.get(
        f'http://{hostname}:{receive_port}/exp',
        {
            'query':f'{msg}'
        }).text


def create_table() -> int:
    query = 'CREATE TABLE dpi(p_uid symbol CAPACITY 128, l_uid symbol CAPACITY 128, ts TIMESTAMP)'\
            'timestamp(ts)'\
            'PARTITION BY month WITH maxUncommittedRows=250000'
    result = requests.get("http://localhost:9000/exec?query=" + query)
    if result.status_code == 200:
        #print("table created")
        return result.status_code

    elif result.status_code == 400:
        return result.status_code
        #print("table exists")
    else:
        print(f"error creating table : {result}")
    return result.status_code

