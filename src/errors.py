#!/usr/bin/env python
# coding: utf-8

import enum


class Errors(enum.Enum):
    ParamMethodRequired = {"code": 1001, "message": "param method required"}
    ParamMethodUnknown = {"code": 1002, "message": "param method unknown"}
    ParamAsyncInvalied = {"code": 1003, "message": "param async should be yes/no"}

    @classmethod
    def get_code(cls, err: str):
        if not err:
            return 0

        try:
            return cls[err].value["code"]
        except KeyError:
            return 1

    @classmethod
    def get_message(cls, err: str):
        if not err:
            return None
        try:
            return cls[err].value["message"]
        except KeyError:
            return err
