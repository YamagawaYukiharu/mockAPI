#!/bin/bash

echo "Starting mockPIE server, hold your breath..."

uvicorn app.mock:app --host 0.0.0.0 --port 3030 --reload