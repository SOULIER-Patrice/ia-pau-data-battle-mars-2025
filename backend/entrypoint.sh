#!/bin/bash

# Create tables
echo "Creating database tables..."
python3 initialization.py

# Start the backend
echo "Starting the backend..."
exec fastapi run --port 8000