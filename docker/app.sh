#!/bin/bash

aerich upgrade

gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000