#!/bin/bash

# Find the container name containing "timescaledb-1"
DB_CONTAINER_NAME=$(docker ps --format '{{.Names}}' | grep "timescaledb-1")

# Check if the container is running
if [ -z "$DB_CONTAINER_NAME" ]; then
    echo "Error: Container containing 'timescaledb-1' not found."
    exit 1
fi

# Run the SQL command to delete all data from the timeseries table
docker exec -it "$DB_CONTAINER_NAME" psql -U postgres -d postgres -c "DELETE FROM timeseries;"

echo "All data from the timeseries table has been deleted."

