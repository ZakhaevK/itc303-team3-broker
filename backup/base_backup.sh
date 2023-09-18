#!/bin/bash

# Find the container name containing "timescaledb-1"
DB_CONTAINER_NAME=$(docker ps --format '{{.Names}}' | grep "timescaledb-1")

if [ -z "$DB_CONTAINER_NAME" ]; then
    echo "Error: Container containing 'timescale-1' not found."
    exit 1
fi

docker exec -e PGUSER=postgres -e PGPASSWORD=admin -it "$DB_CONTAINER_NAME" wal-g backup-push /home/postgres/pgdata/data

