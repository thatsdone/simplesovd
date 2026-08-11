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
from app.core.dependencies import EntityDiscovery, get_entity_collection
logger = get_logger(__name__)

router = APIRouter()

get_current_app = EntityDiscovery(collection_name = 'apps')

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('', methods=methods)
async def get_apps(request: Request,
                   apps_list: dict = Depends(get_entity_collection)):
    logger.debug("get_apps() called.")
    return apps_list

@router.api_route('/{entity_id}', methods=methods)
async def get_app_by_id(request: Request,
                        app_data: dict = Depends(get_current_app)):
    logger.debug("get_app_by_id() called.")

    return app_data

@router.api_route('/{entity_id}/{subpath:path}', methods=methods)
async def get_app_with_subpath(request: Request,
                                app_data: dict = Depends(get_current_app),
                                subpath: str = ''):
    logger.debug('get_app_with_subpath() called: %s ', subpath)

    return app_data
