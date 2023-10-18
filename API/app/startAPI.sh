#!/bin/bash
# start the fastAPI application with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
