import psycopg2
import sys
import json
import random
from datetime import datetime
from dateutil import parser

username = "postgres"
password = "admin"
host = "localhost"
port = 5433     # Not 5432 since postgres already exists in stack
dbname = "postgres"
table_name = "timeseries"
CONNECTION = f"postgres://{username}:{password}@{host}:{port}/{dbname}"

def create_test_table(connection: str = CONNECTION, table: str = table_name):
    query_create_table = f"""CREATE TABLE {table} (
                                        broker_id VARCHAR,
                                        l_uid VARCHAR,
                                        p_uid VARCHAR,
                                        timestamp TIMESTAMPTZ NOT NULL,
                                        name VARCHAR,
                                        value VARCHAR
                                    );
                                    """
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    try:
        cursor.execute(query_create_table)
        # Creates a hypertable for time-based partitioning
        cursor.execute(f"SELECT create_hypertable('{table}', 'timestamp');")
        # commit changes to the database to make changes persistent
        conn.commit()
    except psycopg2.errors.DuplicateTable as e:
        sys.stderr.write(f'error: {e}\n')
    cursor.close()

    # Produce the test temperature data that is inserted.
def generate_test_message():
    json_example = []
    for i in range(2):
        rand_cor_id = random.randint(100000, 999999)
        rand_value = random.randint(0, 45)
        rand_id = random.randint(140, 200)
        json_item = f'{{"broker_correlation_id": "{rand_cor_id}" "l_uid": "{rand_id}", "p_uid": "{rand_id + 1}", "name": "temperature", "value": "{rand_value}"}}'
        json_example.append(json_item)
        return json_example

# def insert_lines(json_entries: list = generate_test_message(), connection: str = CONNECTION,):
#     conn = psycopg2.connect(connection)
#     cursor = conn.cursor()
#     try:
#         for json_data in json_entries:
#         # Parse the JSON message and extract the relevant data fields
#             data = json.loads(json_data)
#             l_uid = data['l_uid']
#             p_uid = data['p_uid']
#             name = data['name']
#             value = data['value']

#             cursor.execute("INSERT INTO test_table (l_uid, p_uid, timestamp, name, value) VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s);",
#                            (l_uid, p_uid, name, value))
#     except (Exception, psycopg2.Error) as error:
#         print(error)
#     conn.commit()

def insert_lines(parsed_data: list, connection: str = CONNECTION, table: str = table_name):
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    try:
        for entry in parsed_data:
            broker_id, l_uid, p_uid, timestamp, name, value = entry
            cursor.execute(
                f"INSERT INTO {table} (broker_id, l_uid, p_uid, timestamp, name, value) VALUES (%s, %s, %s, %s, %s, %s);",
                (broker_id, l_uid, p_uid, timestamp, name, value))
    except (Exception, psycopg2.Error) as error:
        print(error)
    conn.commit()
    

def query_all_data(connection: str = CONNECTION, table: str = table_name):
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table};"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    json_data = []
    for row in rows:
        # Convert datetime object to string before loading as JSON
        timestamp_str = row[3].isoformat()
        json_obj = {
            "broker_id": row[0],
            "l_uid": row[1],
            "p_uid": row[2],
            "timestamp": timestamp_str,
            "name": row[4],
            "value": row[5]
        }
        json_data.append(json_obj)
    return json_data

def query_avg_value(interval_hrs: int = 24, connection: str = CONNECTION, table: str = table_name ):
    query_avg = f"""SELECT AVG(value) FROM {table}
                            WHERE timestamp > NOW() - INTERVAL '{interval_hrs} hours';
                            """
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    try:
        cursor.execute(query_avg)
        conn.commit()
        result = cursor.fetchone()
    except psycopg2.errors as e:
        sys.stderr.write(f'error: {e}\n')
    cursor.close()
    return result

#     # Old file method, format specific.
# def insert_data_json_file(filename: str, connection: str = CONNECTION, table_name: str = "test_table"):
#     # Open the JSON file and load its contents
#     with open(filename, 'r') as f:
#         data = json.load(f)

#     # Extract the ID, timestamp, and timeseries data from the JSON data
#     l_uid = data['l_uid']
#     p_uid = data['p_uid']
#     timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
#     timeseries = data['timeseries']

#     conn = psycopg2.connect(connection)
#     cur = conn.cursor()

#     # Extract the timeseries data and insert it into the database
#     for tsd in timeseries:
#         name = tsd['name']
#         value = tsd['value']
#         insert_query = f"INSERT INTO {table_name} (l_uid, p_uid, timestamp, name, value) VALUES (%s, %s, %s, %s, %s)"
#         cur.execute(insert_query, (l_uid, p_uid, timestamp, name, value))

#     conn.commit()
#     conn.close()

def parse_json(json_obj: dict) -> list:
    parsed_data = []
    
    try:
        broker_id = json_obj['broker_correlation_id']
        l_uid = json_obj['l_uid']
        p_uid = json_obj['p_uid']
        timestamp = parser.parse(json_obj['timestamp'])
        timeseries = json_obj['timeseries']

        for tsd in timeseries:
            name = tsd['name']
            value = tsd['value']
            parsed_data.append((broker_id, l_uid, p_uid, timestamp, name, value))
    except KeyError:
        pass
    
    return parsed_data


def parse_json_string(json_string: str) -> list:
    parsed_data = []
    json_str = ""

    for line in json_string.split('\n'):
        json_str += line.strip()
        try:
            json_data = json.loads(json_str)
            broker_id = json_data['broker_correlation_id']
            l_uid = json_data['l_uid']
            p_uid = json_data['p_uid']
            timestamp = parser.parse(json_data['timestamp'])
            timeseries = json_data['timeseries']

            for tsd in timeseries:
                name = tsd['name']
                value = tsd['value']
                parsed_data.append((broker_id, l_uid, p_uid, timestamp, name, value))

            json_str = ""
        except json.decoder.JSONDecodeError:
            pass

    return parsed_data


def parse_json_file(filename: str) -> list:
    parsed_data = []

    with open(filename, 'r') as f:
        json_str = ""
        for line in f:
            json_str += line.strip()
            try:
                json_data = json.loads(json_str)
                broker_id = json_data['broker_correlation_id']
                l_uid = json_data['l_uid']
                p_uid = json_data['p_uid']
                timestamp = parser.parse(json_data['timestamp'])
                timeseries = json_data['timeseries']

                for tsd in timeseries:
                    name = tsd['name']
                    value = tsd['value']
                    parsed_data.append((broker_id, l_uid, p_uid, timestamp, name, value))

                json_str = ""
            except json.decoder.JSONDecodeError:
                pass

    return parsed_data


def insert_data_to_db(filename: str, connection: str = CONNECTION, table_name: str = table_name):
    # Parse the JSON file
    parsed_data = parse_json_file(filename)

    conn = psycopg2.connect(connection)
    cur = conn.cursor()

    # Insert parsed data into the database
    for data in parsed_data:
        broker_id, l_uid, p_uid, timestamp, name, value = data
        insert_query = f"INSERT INTO {table_name} (broker_id, l_uid, p_uid, timestamp, name, value) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(insert_query, (broker_id, l_uid, p_uid, timestamp, name, value))

    conn.commit()
    conn.close()

test_message = """{
  "broker_correlation_id": "83d04e6f-db16-4280-8337-53f11b2335c6",
  "p_uid": 301,
  "l_uid": 276,
  "timestamp": "2023-01-30T06:21:56Z",
  "timeseries": [
    {
      "name": "battery (v)",
      "value": 4.16008997
    },
    {
      "name": "pulse_count",
      "value": 1
    },
    {
      "name": "1_Temperature",
      "value": 21.60000038
    }
  ]
}
"""

if __name__ == "__main__":
    create_test_table()
    #lol = parse_json_string(test_message)
    #print(lol)
    #insert_lines(lol)
    #insert_data_to_db("JSON_message")
    #insert_data_to_db("sample_messages")
    print(query_all_data())