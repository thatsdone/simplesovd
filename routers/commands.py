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

commands = ['status', 'restart']
    
methods = ['GET', 'DELETE', 'POST', 'PUT']
#methods = ['GET']
@router.api_route('', methods=methods)
@router.api_route('/', methods=methods)
def command_list_handler(request: Request):
    base_uri = request.state.config['config']['base_uri']
    resp = dict()
    resp['items'] = []
    for cmd in commands:
        resp_body = dict()
        resp_body['command'] = cmd
        resp_body['href'] = '%s/%s' % (request.url, cmd)
        
        resp['items'].append(resp_body)
    return resp

@router.api_route('/{subpath:path}', methods=methods)
def command_handler(request: Request, subpath: str):
    return {'command': '%s' % (subpath)}
