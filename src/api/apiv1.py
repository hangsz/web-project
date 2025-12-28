#!/usr/bin/env python
# coding: utf-8

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from . import adaptor


async def query(request: Request):
    result = await adaptor.query(request.query_params)
    return JSONResponse(result)


async def command(request: Request):
    result = await adaptor.command(request.path_params, await request.json())
    return JSONResponse(result)


routes = [
    Route("/api/v1", query, methods=["GET"]),
    Route("/api/v1", command, methods=["POST"]),
]
