#!/bin/bash

set +e
cd /home/admin/app
. .venv/bin/activate
gunicorn -w 9 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 600 --reuse-port src.main:app

exit 0