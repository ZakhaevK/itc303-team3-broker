# Use an Ubuntu-based TimescaleDB image
FROM timescale/timescaledb-ha:pg15-latest

# Switch to root user
USER root

# Update package list and install wget
RUN apt-get update && \
    apt-get install -y wget

# Download and install WAL-G
RUN wget https://github.com/wal-g/wal-g/releases/download/v2.0.1/wal-g-pg-ubuntu-20.04-amd64 -O wal-g && \
    chmod +x wal-g && \
    mv wal-g /usr/local/bin/

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions and ownership for the backup directory
RUN mkdir -p /var/lib/wal-g && \
    chown -R postgres:postgres /var/lib/wal-g && \
    chmod -R 770 /var/lib/wal-g
    
# Switch back to postgres user
USER postgres
