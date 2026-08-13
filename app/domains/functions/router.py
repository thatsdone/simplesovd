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
from fastapi import APIRouter, Request, Depends
#
import logging
from app.core.dependencies import EntityDiscovery, get_entity_collection
from app.core.config import SOVDConfig, get_conf

logger = logging.getLogger(__name__)

router = APIRouter()

get_current_app = EntityDiscovery(collection_name = 'functions')

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('', methods=methods)
async def get_functions(request: Request,
                        functions_list: dict = Depends(get_entity_collection),
                        conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_functions() called.")
    return functions_list

@router.api_route('/{entity_id}', methods=methods)
async def get_function_by_id(request: Request,
                             function_data: dict = Depends(get_current_app),
                             conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_function_by_id() called.")

    return function_data

from  app.services.can_services import can_query
@router.api_route('/{entity_id}/{subpath:path}', methods=methods)
async def get_function_with_subpath(request: Request,
                                    function_data: dict = Depends(get_current_app),
                                    subpath: str = '',
                                    conf: SOVDConfig = Depends(get_conf)):
    logger.debug('get_function_with_subpath() called: %s ', subpath)

    # DEBUG for built-in CDA(WIP)
    if request.url.path.split('/')[4] == 'UDSGateway' and subpath == 'data/vin':
        response = await can_query(bytes([0x22, 0xF1, 0x90]), request)
        logger.debug('VIN(hex isotp response): ' + ' '.join('%02X' % response[idx]for idx in range(0, len(response))))
        logger.debug('VIN(str): ' + response[3:].decode('utf-8'))
        function_data['vin'] = response[3:].decode('utf-8')

    return function_data
