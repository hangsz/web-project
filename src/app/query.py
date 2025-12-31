#!/usr/bin/env python
# coding: utf-8


import asyncio
import copy
import socket
import traceback

from src.config import CONF, ENV
from src.errors import Errors
from src.infra.telemetry import get_trace_id, logger, new_meter_provider, observe

from . import service

HOSTNAME = socket.gethostname()
COUNTER = new_meter_provider().get_meter("app.query").create_counter(f"{CONF['app_name']}_query_count")


queries = {
    "admin.request.get": service.admin_request_get,
}


@observe
async def query(params: dict) -> tuple[dict | list, str | None]:
    method = params["method"]
    fn = queries.get(method)
    if not fn:
        return None, Errors.ParamMethodUnknown.name

    try:
        return await _query(params)
    except Exception as e:
        logger.exception(traceback.format_exc())
        COUNTER.add(1, {"method": params["method"], "code": 1})
        return None, repr(e)


@observe
async def _query(fn, params: dict) -> tuple[dict | list, str | None]:
    try:
        if not asyncio.iscoroutinefunction(fn):
            result = observe(fn)(copy.deepcopy(params))
        else:
            result = await observe(fn)(copy.deepcopy(params))
        if not isinstance(result, tuple):
            result = None, result
    except Exception as e:
        logger.exception(traceback.format_exc())
        result = None, repr(e)

    err = result[-1]
    code = 1 if err else 0
    if code:
        req = {
            "method": params["method"],
            "params": params,
            "body": {},
            "code": code,
            "message": err,
            "trace_id": get_trace_id(),
            "status": "COMPLETED",
            "hostname": HOSTNAME,
            "env": ENV,
        }

        service.admin_request_create(req)

        COUNTER.add(1, attributes={"method": params["method"], "code": code})

    return result
