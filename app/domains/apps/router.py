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
from app.core.dependencies import EntityDiscovery, get_entity_collection
from app.core.config import SOVDConfig, get_conf

logger = logging.getLogger(__name__)

router = APIRouter()

get_current_app = EntityDiscovery(collection_name = 'apps')

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
@router.api_route('', methods=methods)
async def get_apps(request: Request,
                   apps_list: dict = Depends(get_entity_collection),
                   conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_apps() called.")
    return apps_list

@router.api_route('/{entity_id}', methods=methods)
async def get_app_by_id(request: Request,
                        app_data: dict = Depends(get_current_app),
                        conf: SOVDConfig = Depends(get_conf)):
    logger.debug("get_app_by_id() called.")

    return app_data

@router.api_route('/{entity_id}/{subpath:path}', methods=methods)
async def get_app_with_subpath(request: Request,
                                app_data: dict = Depends(get_current_app),
                                conf: SOVDConfig = Depends(get_conf),
                                subpath: str = ''):
    logger.debug('get_app_with_subpath() called: %s ', subpath)

    return app_data
