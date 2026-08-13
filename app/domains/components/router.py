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
import logging
from app.core.dependencies import EntityDiscovery, get_entity_collection

logger = logging.getLogger(__name__)

router = APIRouter()

get_current_app = EntityDiscovery(collection_name = 'components')

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('', methods=methods)
async def get_components(components_list: dict = Depends(get_entity_collection)):
    logger.debug("get_components() called.")
    return components_list

@router.api_route('/{entity_id}', methods=methods)
async def get_component_by_id(component_data: dict = Depends(get_current_app)):
    logger.debug("DEBUG: get_component_by_id() called.")
    return component_data

@router.api_route('/{entity_id}/{subpath:path}', methods=methods)
async def get_component_with_subpath(request: Request,
                                     component_data: dict = Depends(get_current_app),
                                      subpath: str = ''):
    logger.debug('get_component_with_subpath() called: %s ', subpath)

    return component_data
