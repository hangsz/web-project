#!/usr/bin/env python
# coding: utf-8

from sqlalchemy.dialects.mysql.aiomysql import MySQLDialect_aiomysql


class CustomAiomysql(MySQLDialect_aiomysql):
    def __init__(self, **kwargs):
        super(CustomAiomysql, self).__init__(**kwargs)

    def _get_server_version_info(self, connection):
        return (5, 8, 0)


CustomAiomysql.supports_statement_cache = True
