#!/usr/bin/env python
# coding: utf-8


import socket
import time
import traceback
import typing as t

from src import app
from src.errors import Errors
from src.infra.telemetry import get_trace_id, logger

HOSTNAME = socket.gethostname()

async def query(query_params: t.Mapping) -> dict:
    start = time.perf_counter()
    result, err = None, None
    try:
        params, err = build_params(query_params)
        if not err:
            result, err = await app.query(params)
    except Exception as e:
        logger.exception(traceback.format_exc())
        err = repr(e)

    return {
        "code": Errors.get_code(err),
        "message": Errors.get_message(err),
        "data": result,
        "hostname": HOSTNAME,
        "duration": time.perf_counter() - start,
        "trace_id": get_trace_id(),
    }


async def command(query_params: t.Mapping, data: dict | list) -> dict:
    start = time.perf_counter()
    result, err = None, None
    try:
        params, err = build_params(query_params)
        if not err:
            result, err = await app.command(params, data)
    except Exception as e:
        logger.exception(traceback.format_exc())
        err = repr(e)

    return {
        "code": Errors.get_code(err),
        "message": Errors.get_message(err),
        "data": result,
        "hostname": HOSTNAME,
        "duration": time.perf_counter() - start,
        "trace_id": get_trace_id(),
    }


def build_params(query_params: t.Mapping) -> tuple[dict, str]:
    params = {}
    for k, v in query_params._list:
        if k in params:
            if not isinstance(params[k], list):
                params[k] = [params[k]]
            params[k].append(v)
        else:
            params[k] = v

    if "method" not in params:
        return None, Errors.ParamMethodRequired.name
    if "async" not in params:
        params["async"] = "no"
    if params["async"] not in ("yes", "no"):
        return None, Errors.ParamAsyncInvalied.name

    return params, None
