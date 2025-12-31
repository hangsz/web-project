#!/usr/bin/env python
# coding: utf-8


from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.infra.telemetry import logger


def health(request: Request):
    logger.info("health")
    return JSONResponse({"code": 0, "message": "OK"})


routes = [
    Route("/health", health, methods=["GET"]),
]
