#!/usr/bin/env python
# coding: utf-8


import os
import urllib

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import CONF

pool = None
async_pool = None


def init():
    sync_init()


def sync_init():
    global pool

    if pool:
        return

    print("db init start")

    match CONF["sql_driver"]:
        case "sqlite":
            conf = CONF["sqlite"]
            url = f"sqlite://{conf['db']}"

        case "pymyql":
            conf = CONF["mysql"]
            name = "custome_pymysql"
            sa.dialects.registry.register(name=name, module="src.infra.db.custome_pymysql", objname="CustomPymysql")
            username = urllib.parse.quote(conf["user"])
            password = ""

            url = f"{name}://{username}:{password}@{conf['host']}:{conf['port']}/{conf['db']}?charset={conf['charset']}"
        case _:
            raise ValueError(f"unkown sql driver {CONF['sql_driver']}")

    pool = sa.create_engine(
        url,
        echo=True if CONF["debug"] else False,
        echo_pool=False,
        pool_size=min(32, (os.cpu_count() or 1) + 4),
        max_overflow=8,
        pool_recycle=300,
        pool_use_lifo=True,
    )

    print("db init end")


def async_init():
    global async_pool

    if async_pool:
        return

    print("db async init start")

    match CONF["sql_driver"]:
        case "sqlite":
            conf = CONF["sqlite"]
            url = f"sqlite://{conf['db']}"

        case "aiomyql":
            conf = CONF["mysql"]
            name = "custome_aiomysql"
            sa.dialects.registry.register(name=name, module="src.infra.db.custome_aiomysql", objname="CustomAiomysql")
            username = urllib.parse.quote(conf["user"])
            password = ""

            url = f"{name}://{username}:{password}@{conf['host']}:{conf['port']}/{conf['db']}?charset={conf['charset']}"
        case _:
            raise ValueError(f"unkown sql driver {CONF['sql_driver']}")

    async_pool = create_async_engine(
        url,
        echo=True if CONF["debug"] else False,
        echo_pool=False,
        pool_size=min(32, (os.cpu_count() or 1) + 4),
        max_overflow=8,
        pool_recycle=300,
        pool_use_lifo=True,
    )

    print("db async init end")
