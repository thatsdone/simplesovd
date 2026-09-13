#!/usr/bin/env python3
#
# simplesovd: A simple implementation of SOVD (ISO 17978)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/09 v0.2 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
from fastapi import APIRouter, Depends, Request
from fastapi.openapi.utils import get_openapi
#
import copy
import logging

from app.core.config import SOVDConfig, get_conf

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get('/version-info')
async def get_version_info(request: Request,
                           conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_version_info() called.")
    base_uri = conf.static_conf['config']['base_uri']
    vendor_prefix = conf.static_conf['config']['vendor_prefix']
    version = conf.static_conf['config']['version']
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
async def get_root_docs(request: Request):
    logger.debug('get_root_docs() called.')
    full_spec = copy.deepcopy(get_openapi(title='Service Oriented Vehicle Diagnostics (SOVD) API',
                                          version='1.1.0',
                                          routes=request.app.routes))
    filtered_paths = {}
    vendor_prefix = request.state.conf.static_conf['config']['vendor_prefix']
    for path, action in full_spec.get('paths', {}).items():
        if path.startswith(vendor_prefix):
            filtered_paths[path] = action
    full_spec['paths'] = filtered_paths

    return full_spec

@router.get('/{anypath:path}/docs')
async def get_docs(request: Request, anypath: str):
    logger.debug(f'get_docs() called. {anypath}')
    full_spec = copy.deepcopy(get_openapi(title='Service Oriented Vehicle Diagnostics (SOVD) API',
                                          version='1.1.0',
                                          routes=request.app.routes))
    # TODO: Implement per entity online capability processing.
    return full_spec

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('/updates', methods=methods)
@router.api_route('/updates/{subpath:path}', methods=methods)
async def handle_updates(request: Request, subpath: str = '',
                         conf: SOVDConfig = Depends(get_conf)):
    logger.debug("handle_updates() called. subpath: %s" % (subpath))
    #TODO: implement /updates
    return {'item': []}
