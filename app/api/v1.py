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

from fastapi import APIRouter
from app.core.config import sovd_config
from app.domains.areas.router import router as areas_router
from app.domains.components.router import router as components_router
from app.domains.apps.router import router as apps_router
from app.domains.functions.router import router as functions_router
from app.domains.system.router import router as system_router
#
from app.domains.admin.router import router as admin_router

default_vendor_prefix = '/simplesovd/v1'
vendor_prefix = sovd_config.predefined_config['config'].get('vendor_prefix', None)
if not vendor_prefix:
    vendor_prefix = default_vendor_prefix

api_v1_router = APIRouter(prefix=vendor_prefix)

# SOVD top level entities. a.k.a. entity-collection
api_v1_router.include_router(areas_router,
#                             prefix=f'/{vendor_prefix}/areas',
                             prefix=f'/areas',
                             tags=['SOVD entity-collection: areas'])
api_v1_router.include_router(components_router,
#                             prefix=f'/{vendor_prefix}/components',
                             prefix=f'/components',
                             tags=['SOVD entity-collection: components'])
api_v1_router.include_router(apps_router,
                             prefix=f'/apps',
                             tags=['SOVD entity-collection: apps'])
api_v1_router.include_router(functions_router,
                             prefix=f'/functions',
                             tags=['SOVD functions'])
# SOVD other top level path
api_v1_router.include_router(system_router, #),
#                             prefix=f'/{vendor_prefix}',
                             tags=['SOVD Other elements'])

# for the SOVD server administration
admin_base_router = APIRouter()#prefix='/admin')
admin_base_router.include_router(admin_router,
                            prefix='/admin',
                            tags=['Non-SOVD System administration'])
