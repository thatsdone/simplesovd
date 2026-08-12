#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# simplesovd: A simple implementation of SOVD (ISO 17973)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/09 v0.2 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
from fastapi import APIRouter, Request
#
from app.core.config import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get('')
async def get_root(request: Request):
    logger.debug("get_status() called.")
    conf = request.state.conf.predefined_config
    base_uri = conf['config']['base_uri']
    res = {'items': ['status','command']}
    return res

@router.get('/status')
async def get_status(request: Request):
    logger.debug("get_status() called.")
    conf = request.state.conf.predefined_config
    base_uri = conf['config']['base_uri']
    vendor_prefix = conf['config']['vendor_prefix']
    version = conf['config']['version']
    res = {
        'version': '1.1',
        'base_uri': base_uri,
        'vendor_info': {
            'name': 'simplesovd',
            'version': version
        },
        'status': 'UP'
    }
    return res

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('/command', methods=methods)
@router.api_route('/command/{subpath:path}', methods=methods)
async def handle_command(request: Request, subpath: str = ''):
    logger.debug("handle_command() called. subpath: %s" % (subpath))
    #TODO: implement commands
    return {'command': subpath}
