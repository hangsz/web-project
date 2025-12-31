#!/usr/bin/env python
# coding: utf-8


from src.domain.admin.request import Request


def admin_request_get(params: dict) -> tuple[dict | None, str | None]:
    return Request().get(params["uid"])
