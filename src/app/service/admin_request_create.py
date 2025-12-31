#!/usr/bin/env python
# coding: utf-8

from src.domain.admin.request import Request


def admin_request_create(params: dict, data: dict) -> tuple[str | None, str | None]:
    return Request().create(data)