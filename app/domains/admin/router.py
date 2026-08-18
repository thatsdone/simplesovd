#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# simplesovd: A simple implementation of SOVD (ISO 17978)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/09 v0.2 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
from fastapi import APIRouter, Request, Depends
#
import logging
#
from app.core.config import SOVDConfig, get_conf

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get('')
async def get_root(request: Request,
                   conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_status() called.")
    base_uri = conf.static_conf['config']['base_uri']
    res = {'items': ['status','command']}
    return res

@router.get('/status')
async def get_status(request: Request,
                     conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_status() called.")
    base_uri = conf.static_conf['config']['base_uri']
    vendor_prefix = conf.static_conf['config']['vendor_prefix']
    version = conf.static_conf['config']['version']
    res = {
        'version': '1.1',
        'base_uri': base_uri,
        'vendor_info': {
            'name': 'simplesovd',
            'version': version
        },
        'status': 'UP'
    }
    # list configured entity/resource paths
    res['paths'] = list()
    for route in request.app.routes:
        res['paths'].append(
            {
                'path':  route.path,
                'methods': route.methods
            })
    return res

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('/command', methods=methods)
@router.api_route('/command/{subpath:path}', methods=methods)
async def handle_command(request: Request, subpath: str = '',
                     conf: SOVDConfig = Depends(get_conf)):
    logger.debug("handle_command() called. subpath: %s" % (subpath))
    #TODO: implement commands
    return {'command': subpath}
