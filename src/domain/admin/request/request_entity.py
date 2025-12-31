#!/usr/bin/env python
# coding: utf-8


import json

from uuid_extensions import uuid7

from src.infra.telemetry import logger, observe

from .request_repo import RequestRepo


class Request(object):
    def __init__(self):
        self._repo = RequestRepo()

    def get(self, uid: str) -> tuple[dict, str | None]:
        data, err = self._repo.get_from_db(uid)

        if err:
            return None, err

        # best practice: load needed keys
        data["params"] = json.loads(data.get("params", "null"))

        return data, None

    def create(self, data: dict) -> str | None:
        uid = uuid7().hex
        data["uuid"] = uid
        data["params"] = json.dumps(data["params"])
        data["body"] = json.dumps(data["body"])

        err = self._repo.create_to_db(data)
        if err:
            return None, err

        return uid, str

    def update(self, uid: str, data: dict) -> str | None:
        return self._repo.update_to_db(uid, data)
