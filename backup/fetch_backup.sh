#!/bin/bash

# Find the existing TimescaleDB container
existing_container=$(docker ps --format '{{.Names}}' | grep "timescaledb-1")
if [ -z "$existing_container" ]; then
  echo "Error: Container containing 'timescaledb-1' not found."
  exit 1
fi

echo "Stopping container: $existing_container"
docker stop $existing_container

# Empty the data directory (Be very careful with this step!)
docker exec -it $existing_container rm -rf /home/postgres/pgdata/data/*

# Start the container back up
docker start $existing_container

# Wait for the container to be ready
sleep 10  # Adjust the sleep time as needed

# Fetch the base backup
docker exec -it $existing_container wal-g backup-fetch /home/postgres/pgdata/data LATEST

# Prepare for WAL replay
docker exec -it $existing_container touch /home/postgres/pgdata/data/recovery.signal

# Restart the TimescaleDB container
docker stop $existing_container
docker start $existing_container

echo "Restore process completed. Please verify the restore manually."

