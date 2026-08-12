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
from fastapi import APIRouter, Depends, Request
#
from app.core.config import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get('/version-info')
async def get_version_info(request: Request):
    logger.debug("get_version_info() called.")
    conf = request.state.conf.predefined_config
    base_uri = conf['config']['base_uri']
    vendor_prefix = conf['config']['vendor_prefix']
    version = conf['config']['version']
    res = {
        'version': '1.1',
        'base_uri': vendor_prefix,
        'vendor_info': {
            'name': 'simplesovd',
            'version': version
        }
    }
    return res

@router.get('/docs')
async def get_root_docs():
    logger.debug('get_root_docs() called.')
    res = {
        'doc': 'foobar'
    }
    return res

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('/updates', methods=methods)
@router.api_route('/updates/{subpath:path}', methods=methods)
async def handle_updates(request: Request, subpath: str = ''):
    logger.debug("handle_updates() called. subpath: %s" % (subpath))
    #TODO: implement /updates
    return {'item': []}
