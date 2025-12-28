#!/usr/bin/env python
# coding: utf-8


from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


def health(request: Request):
    return JSONResponse({"code": 0, "message": "OK"})


routes = [
    Route("/api/v1/health", health, methods=["GET"]),
]
