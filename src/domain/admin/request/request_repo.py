#!/usr/bin/env python
# coding: utf-8


import traceback

import sqlalchemy as sa

from src.config import CONF
from src.infra import db
from src.infra.telemetry import logger, observe

Table = sa.Table(
    CONF["app_name"] + "_request",
    sa.MetaData(),
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("gmt_created", sa.DateTime, nullable=False),
    sa.Column("gmt_modified", sa.DateTime, nullable=False),
    sa.Column("uuid", sa.String(128), nullable=False, unique=True),
    sa.Column("method", sa.String(128), nullable=False),
    sa.Column("params", sa.Text, nullable=False),
    sa.Column("body", sa.Text, nullable=True),
    sa.Column("code", sa.Integer, nullable=False),
    sa.Column("message", sa.Text, nullable=True),
    sa.Column("data", sa.Text, nullable=True),
    sa.Column("status", sa.String(32), nullable=False),
    sa.Column("trace_id", sa.String(128), nullable=True, unique=True),
    sa.Column("hostname", sa.String(64), nullable=True),
    sa.Column("env", sa.String(16), nullable=True),
)


class RequestRepo(object):
    def __init__(self):
        pass

    def get_from_db(self, uid: str) -> tuple[dict, str | None]:
        try:
            with db.pool.begin() as conn:
                query = sa.select(Table).where(Table.c.uuid == uid).limit(1)
                data = conn.execute(query).first()

        except Exception as e:
            logger.exception(traceback.format_exc())
            return None, repr(e)

        # best practice: return error if get empty
        if not data:
            return None, f"data empty. uuid={uid}"

        return data._asdict(), None

    def create_to_db(self, data: dict) -> str | None:
        try:
            with db.pool.begin() as conn:
                query = sa.insert(Table).values(data)
                conn.execute(query)

        except Exception as e:
            logger.exception(traceback.format_exc())

            return repr(e)

        return None

    def update_to_db(self, uid: str, data: dict) -> str | None:
        try:
            with db.pool.begin() as conn:
                query = sa.update(Table).where(Table.c.uuid == uid).values(data)
                conn.execute(query)
        except Exception as e:
            logger.exception(traceback.format_exc())

            return repr(e)

        return None
