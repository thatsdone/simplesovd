#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# simplesovd: A simple implementation of SOVD (ISO 17973)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/02 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * many
from fastapi import APIRouter, Request, Response
#import asyncio
#import json
#import httpx
import requests

from routers import common_router

router = APIRouter()

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
#
@router.api_route('', methods=methods)
@router.api_route('/', methods=methods)
def handle_apps(request: Request):
    resp = common_router.handle_entities(request, None)
    return resp

@router.api_route('/{subpath:path}', methods=methods)
def handle_one(request: Request, subpath: str):
    path_elements = request.url.path.split('/')
    entity_collection = path_elements[3]
    entity = path_elements[4]

    backward_resp = None
    forward_path = None
    if len(path_elements) >= 5:
        forward_path = '/'.join(p for p in subpath.split('/')[1:])
    topology = request.state.config['topology']
    if entity in topology[entity_collection].keys():
        if 'href' in topology[entity_collection][entity].keys():
            url = '%s' % (topology[entity_collection][entity]['href'])
            if forward_path:
                url += ('/' + forward_path)
            try:
                backend_resp = requests.get(url,
                                            headers=request.headers,
                                            timeout=5.0)
            except Exception as e:
                print('ERROR: requests.get() failed', e)
                return Response(status_code = 503)

            return Response(status_code = backend_resp.status_code,
                            headers = backend_resp.headers,
                            content = backend_resp.text)

    # built-in processing
    resp = common_router.handle_entities(request, subpath)
    return resp
