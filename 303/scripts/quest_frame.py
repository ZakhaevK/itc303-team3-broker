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
            'query':f'DROP TABLE {bucket_name}'
        }).text


def query_db(msg: str):
    return requests.get(
        f'http://{hostname}:{receive_port}/exp',
        {
            'query':f'{msg}'
        }).text


