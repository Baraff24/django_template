#!/usr/bin/env bash

# Function to handle termination signals
function shutdown() {
    echo "Shutting down Celery worker and Beat..."
    pkill -TERM -P $$
    exit 0
}

# Trap termination signals
trap shutdown SIGTERM SIGINT

# Start Celery worker in the background
echo "Starting Celery worker..."
celery -A config worker -l info -E &

# Start Celery Beat in the background
echo "Starting Celery Beat..."
celery -A config beat -l info &

# Wait for any process to exit
wait -n

# Exit with status of the process that exited first
exit $?
