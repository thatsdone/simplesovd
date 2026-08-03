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
from fastapi import APIRouter, Request
import asyncio
import json

from routers import common_router

router = APIRouter()

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
#
@router.api_route('', methods=methods)
@router.api_route('/', methods=methods)
def handle_components(request: Request):

    resp = common_router.handle_entities(request)
    return resp
    

@router.api_route('/{subpath:path}', methods=methods)
def handle_component_one(request: Request, subpath: str):

    entity_collection = request.url.path.split('/')[3]
    base_uri = request.state.config['config']['base_uri']
    resp = dict()
    resp['items'] = []
    entity = subpath.split('/')[0]
    if entity in request.state.config['topology'][entity_collection].keys():
        resp_body = dict()
        resp_body['id'] = entity
        resp_body['name'] = entity
        # see Table 53 of ISO 17973-3
        for feature in request.state.config['sovd']['features']:
            resp_body[feature] = '%s/%s' % (request.url, feature)
        resp['items'].append(resp_body)
    return resp
