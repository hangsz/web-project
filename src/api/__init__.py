#!/usr/bin/env python
# coding: utf-8

import json

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from . import apiv1, health
from .middleware import TelemetryMiddleware

JSONResponse.render = lambda self, content: json.dumps(content, default=str).encode("utf-8")

app = Starlette(debug=True, routes=apiv1.routes + health.routes)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

app.add_middleware(TelemetryMiddleware)
