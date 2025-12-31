#!/usr/bin/env python
# coding: utf-8

from opentelemetry import context, trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from src.infra.telemetry import tracer


class TelemetryMiddleware(object):
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        headers = dict(scope.get("headers", {}))
        if "traceparent" in headers:
            carrier = {"traceparent": headers["traceparent"]}
            ctx = TraceContextTextMapPropagator().extract(carrier)
            token = context.attach(ctx)
            try:
                await self.app(scope, receive, send)
            finally:
                context.detach(token)
        else:
            name = "query" if scope["method"] == "GET" else "command"
            span = tracer.start_span(name)
            span.set_attribute("http.method", scope["method"])
            ctx = trace.set_span_in_context(span)
            token = context.attach(ctx)

        await self.app(scope, receive, send)
