#!/bin/sh
# Healthcheck script for PostgreSQL

# Use POSTGRES_USER if set, otherwise default to 'postgres'
USER=${POSTGRES_USER:-postgres}

# Check if PostgreSQL is accepting connections
pg_isready -h localhost -p 5432 -U "$USER" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "PostgreSQL is healthy"
    exit 0
else
    echo "PostgreSQL health check failed"
    exit 1
fi
