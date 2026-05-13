#!/bin/sh
# Healthcheck script for Django application

# Check if Django is responding on health endpoint
curl -sf http://localhost:3000/health/ > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Django application is healthy"
    exit 0
else
    echo "Django application health check failed"
    exit 1
fi
