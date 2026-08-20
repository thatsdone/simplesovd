#!/usr/bin/env python3
#
# simplesovd: A simple implementation of SOVD (ISO 17978)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/17 v0.3 Plugin support
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
import logging
from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.core.config import SOVDConfig, get_conf
from app.core.dependencies import EntityDiscovery, get_entity_collection
from  app.services.can_services import can_query

logger = logging.getLogger(__name__)

router = APIRouter(tags=['UDSGateway'])

get_current_app = EntityDiscovery(collection_name = 'functions')

#entity_collection = 'functions'

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.get('')
async def get_udsgateway(request: Request,
                   conf: SOVDConfig = Depends(get_conf)):
    logger.debug(f'Called. {request}')
    return {'items': []}


@router.api_route('/{subpath:path}', methods=methods)
async def get_udsgateway_with_subpath(request: Request,
                                      # this causes inconsistency in FastAPI
                                      #function_data: dict = Depends(get_current_app),
                                      subpath: str = '',
                                      entity_id: str | None = None,
                                      conf: SOVDConfig = Depends(get_conf)):

    logger.debug('called: %s ', subpath)

    # GET /.../functions/SOVDGateway/vin
    if subpath == 'vin':
        response = await can_query(bytes([0x22, 0xF1, 0x90]), request)
        logger.debug('VIN(hex isotp response): ' + ' '.join('%02X' % response[idx]for idx in range(0, len(response))))
        logger.debug('VIN(str): ' + response[3:].decode('utf-8'))
        #function_data['vin'] = response[3:].decode('utf-8')
        #return function_data
        return {
            'items': [
                {
                    'vin': response[3:].decode('utf-8')}
            ]
        }
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'/UDSGateway/{subpath} not found'
        )
