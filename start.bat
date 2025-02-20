@echo off
echo Starting mockPIE, hold your breath....

uvicorn app.mock:app --host 0.0.0.0 --port 3030 --reload