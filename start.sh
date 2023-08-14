#!/bin/bash
echo 'Starting bot service'
cd /home/MTS_chatbot
source mts/bin/activate
uvicorn entrypoints.http_server:app --host 0.0.0.0 --port 8000
echo 'Started'
