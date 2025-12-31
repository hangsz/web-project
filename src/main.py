#!/usr/bin/env python
# coding: utf-8

import os
import sys

import uvicorn

from src.api import app


def main() -> int:
    passwd = "test"
    command = f"redis-server --requirepass '{passwd}' --daemonize yes"
    os.system(command)

    os.environ["APP_ENV"] = "LOCAL"
    print(f"env: {os.getenv('APP_ENV')}")

    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=False, reload_dirs=["src"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
