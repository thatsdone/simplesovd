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
from app.core.config import sovd_config, get_logger
from app.api.v1 import api_v1_router, admin_base_router

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info('Starting...')

    yield {'config': sovd_config.predefined_config}

    logger.info('Shutting down...')

app = FastAPI(
    title="A simple SOVD Server",
    lifespan=lifespan)

#
app.include_router(api_v1_router)
app.include_router(admin_base_router)
