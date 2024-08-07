#!/bin/sh
python3 -m uvicorn wsgi:app --reload --port 9052 --host 0.0.0.0