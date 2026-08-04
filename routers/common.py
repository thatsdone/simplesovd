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

methods = ['GET']
@router.api_route('', methods=methods)
@router.api_route('/', methods=methods)
@router.api_route('/{subpath:path}', methods=methods)
def handler(request: Request, subpath: str):
    if subpath == 'version-info':
        resp = {
            'version': '1.1',
            'base_uri': request.state.config['config']['base_uri'],
            'vendor_info': {
                'name': 'simplesovd',
                'version': '0.0.1'
            }
        }
    elif subpath == 'updates':
        return {'items': []}
    else:
        resp = {}
    return resp
