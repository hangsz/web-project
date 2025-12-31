#!/usr/bin/env python
# coding: utf-8

import requests

HOST = "http://127.0.0.1:8000"


def test_admin_get():
    url = HOST + "/api/v1"
    resp = requests.get(url)

    assert resp.status_code == 200


def test_admin_create():
    url = HOST + "/api/v1"
    headers = {"Content-Type": "application/json"}

    params = {"method": "admin.request_create", "async": "no"}
    resp = requests.post(url, headers=headers, mparams=params, data={})

    assert resp.status_code == 200
