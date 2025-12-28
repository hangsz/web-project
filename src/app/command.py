#!/usr/bin/env python
# coding: utf-8


import asyncio
import os
import socket
import traceback
from concurrent.futures import ThreadPoolExecutor

from opentelemetry import context

from src.config import CONF, ENV
from src.errors import Errors
from src.infra.telemetry import get_trace_id, logger, new_meter_provider, observe

from . import service

HOSTNAME = socket.gethostname()
meter = new_meter_provider().get_meter("app.command")
COUNTER = meter.create_counter(f"{CONF['app_name']}_api_command_count")
POOL_LENGTH = meter.create_gauge(f"{CONF['app_name']}_api_background_tasks")


pool = ThreadPoolExecutor(thread_name_prefix="background", max_workers=os.cpu_count() + 1)

commands = {
    "admin.request.create": service.admin_request_create,
    "admin.request.update": service.admin_request_update,
    "admin.request.delete": service.admin_request_delete,
}


@observe
async def command(params: dict, data: dict | list) -> tuple[dict | list, str | None]:
    method = params["method"]
    fn = commands.get(method)
    if not fn:
        return None, Errors.ParamMethodUnknown.name

    req = {
        "method": params["method"],
        "params": params,
        "body": data,
        "code": 0,
        "message": None,
        "trace_id": get_trace_id(),
        "status": "RUNNING",
        "hostname": HOSTNAME,
        "env": ENV,
    }

    _reqid, err = service.admin_request_create(req)
    if err:
        return None, err
    params["_reqid"] = _reqid

    try:
        if params["async"] == "yes":
            return background_command(params)
        else:
            return await _command(fn, params, data)
    except Exception as e:
        logger.exception(traceback.format_exc())
        COUNTER.add(1, {"method": params["method"], "code": 1, "hostname": HOSTNAME, "env": ENV})
        return None, repr(e)


@observe
async def _command(fn, params: dict, data: dict | list) -> tuple[dict | list, str | None]:
    try:
        if not asyncio.iscoroutinefunction(fn):
            result = observe(fn)(params, data)
        else:
            result = await observe(fn)(params, data)
        if not isinstance(result, tuple):
            result = None, result
    except Exception as e:
        logger.exception(traceback.format_exc())
        result = None, repr(e)

    err = result[-1]
    code = Errors.get_code(err)
    message = Errors.get_message(err)
    service.admin_request_update(
        {{"uuid": params["_reqid"]}, {"code": code, "message": message, "status": "COMPLETED"}}
    )

    COUNTER.add(1, attributes={"method": params["method"], "code": code, "hostname": HOSTNAME, "env": ENV})

    return result


@observe
async def background_command(fn, params: dict, data: dict | list) -> tuple[dict | list, str | None]:
    ctx = context.get_current()

    global pool
    pool.submit(background_execute, ctx, fn, params, data)
    POOL_LENGTH.set(pool._work_queue.qsize(), {"max_worksers": pool._max_workers, "env": ENV})

    result = {"path": f"/api/v1?method=admin.request.get&uuid={params['_reqid']}"}, None

    return result


@observe
async def background_execute(ctx, fn, params: dict, data: dict | list) -> tuple[dict | list, str | None]:
    try:
        ctx and context.attach(ctx)
    except Exception as e:
        logger.warning(repr(e))

    try:
        result = observe(fn)(params, data)
        if not isinstance(result, tuple):
            result = None, result
    except Exception as e:
        logger.exception(traceback.format_exc())
        result = None, repr(e)

    err = result[-1]
    code = Errors.get_code(err)
    message = Errors.get_message(err)
    service.admin_request_update(
        {{"uuid": params["_reqid"]}, {"code": code, "message": message, "status": "COMPLETED"}}
    )

    COUNTER.add(1, attributes={"method": params["method"], "code": code, "hostname": HOSTNAME, "env": ENV})

    return result
