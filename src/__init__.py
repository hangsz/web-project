#!/usr/bin/env python
# coding: utf-8

import sys

# config init
try:
    from . import config

    config.init()
except Exception as e:
    sys.exit(repr(e))


# infra init

try:
    from src.infra import db

    db.init()
except Exception as e:
    sys.exit(repr(e))
