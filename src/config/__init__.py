#!/usr/bin/env python
# coding: utf-8


import os
import tomllib

ENV = os.getenv("APP_ENV", "LOCAL")
CONF = None


def init():
    print(f"env: {ENV}")

    global CONF
    if CONF:
        return

    print("config init start")

    match ENV:
        case "LOCAL":
            filename = "local.toml"
        case "DEV":
            filename = "dev.toml"
        case "PROD":
            filename = "prod.toml"
        case _:
            raise ValueError(f"unknown ENV: {ENV}")

    with open(os.path.join(os.path.dirname(__file__), filename), "rb") as f:
        CONF = tomllib.load(f)

    print("config init end")
