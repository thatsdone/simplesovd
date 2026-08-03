#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# simplesovd: A simple implementation of SOVD (ISO 17973)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/02 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * many
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from routers import commands, areas, components, apps, functions, common
from contextlib import asynccontextmanager
#import asyncio
import httpx

import os
import sys
import logging
import urllib
import yaml
#
conf_data = dict()
debug = False
#async_loop = None
#
simplesovd_debug = os.getenv("SIMPLESOVD_DEBUG")
if simplesovd_debug and int(simplesovd_debug) != 0:
    debug = True

logger = logging.getLogger('simplesovd')
#
log_level = "DEBUG" if debug else "INFO"
logger.setLevel(log_level)
formatter = logging.Formatter(
    fmt = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting...')

    #global async_loop
    global debug

    #async_loop = asyncio.get_running_loop()

    with open('config.yaml', 'rt') as fp:
        predefined_config = yaml.load(fp, Loader=yaml.SafeLoader)
    if not predefined_config:
        sys.exit()

    if debug:
        import pprint
        pprint.pprint(predefined_config)

    conf_data = predefined_config
    yield {"config": conf_data}

    logger.info('Shutting down...')

app = FastAPI(
    title="A simple SOVD Server",
    lifespan=lifespan)
#
app.include_router(commands.router, prefix='/commands', tags=['Proxy Commands'])
# SOVD top level entities. a.k.a. entity-collection
vendor_prefix = 'simplesovd/v1'
app.include_router(areas.router, prefix=f'/{vendor_prefix}/areas', tags=['areas'])
app.include_router(components.router, prefix=f'/{vendor_prefix}/components', tags=['components'])
app.include_router(apps.router, prefix=f'/{vendor_prefix}/apps', tags=['apps'])
app.include_router(functions.router, prefix=f'/{vendor_prefix}/functions', tags=['functions'])
app.include_router(common.router, prefix=f'/{vendor_prefix}', tags=['common'])
