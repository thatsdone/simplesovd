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
# TODO:
#   * many
from fastapi import FastAPI
from contextlib import asynccontextmanager
#
from app.core.config import SOVDConfig, get_logger
from app.api.v1 import api_v1_router, admin_base_router

logger = get_logger(__name__)
global sovd_config
sovd_config = None

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info('Starting...')
    yield {'conf': sovd_config}

    logger.info('Shutting down...')

app = FastAPI(
    title="A simple SOVD Server",
    lifespan=lifespan)
#
#
sovd_config = SOVDConfig()
vendor_prefix = sovd_config.predefined_config['config']['vendor_prefix']
#
app.include_router(api_v1_router, prefix=vendor_prefix)
app.include_router(admin_base_router)
