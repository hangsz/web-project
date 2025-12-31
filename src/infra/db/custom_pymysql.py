#!/usr/bin/env python
# coding: utf-8

from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql


class CustomPymysql(MySQLDialect_pymysql):
    def __init__(self, **kwargs):
        super(CustomPymysql, self).__init__(**kwargs)

    def _get_server_version_info(self, connection):
        return (5, 8, 0)


CustomPymysql.supports_statement_cache = True
