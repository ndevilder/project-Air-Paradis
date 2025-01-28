#!/bin/bash

if [ "$APP_MODE" = "test" ]; then
  pytest --cov=. --cov-report=xml
else
  uvicorn main:app --host 0.0.0.0 --port 80
fi
