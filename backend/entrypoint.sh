#!/bin/bash
# filepath: /home/quentin/Projects/IA/ia-pau-data-battle-mars-2025/backend/entrypoint.sh

python3 -m ai.src.create_embeddings

# Create tables
echo "Creating database tables..."
python3 create_tables.py

# Start the backend
echo "Starting the backend..."
exec fastapi run --port 8000