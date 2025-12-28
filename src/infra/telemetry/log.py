#!/usr/bin/env python
# coding: utf-8

import logging

from opentelemetry import trace

from src.config import CONF

conf = CONF["telemetry"]["log"]


match conf["level"].lower():
    case "debug":
        level = logging.DEBUG
    case "info":
        level = logging.INFO
    case "warning":
        level = logging.WARNING
    case "error":
        level = logging.ERROR
    case "critical":
        level = logging.CRITICAL
    case _:
        level = logging.INFO

logging.basicConfig(level=level)

handler = logging.FileHandler(conf["filename"])
handler.setLevel(level)


class TraceFormatter(logging.Formatter):
    def format(self, record):
        ctx = trace.get_current_span().get_span_context()
        record.trace_id = trace.format_trace_id(ctx.trace_id)
        record.span_id = trace.format_span_id(ctx.span_id)
        return super().format(record)


FORMAT = "%(asctime)s %(levelname)s [%(filename)s %(lineno)d] [%(trace_id)s %(span_id)s] %(message)s"
handler.setFormatter(TraceFormatter(FORMAT))

logger = logging.getLogger(conf["app_name"])
logger.addHandler(handler)
logger.propagate = False
