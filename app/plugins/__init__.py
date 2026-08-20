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
import importlib
import pkgutil
import logging

from fastapi import APIRouter
from app.core.config import get_conf

logger = logging.getLogger(__name__)

def load_plugins(parent_router: APIRouter):
    """
    Scan app/plugins and load plugins there on startup.
    """

    logger.debug('called.')

    package_prefix = __name__ + '.'

    for _, module_name, is_pkg in pkgutil.iter_modules(__path__):
        if not is_pkg:
            logger.debug(f'Ignore {module_name}')
            continue
        full_module_name = package_prefix + module_name
        logger.debug(f'full_module_name: {full_module_name}')
        try:
            plugin_module = importlib.import_module(full_module_name)
            if hasattr(plugin_module, 'router'):
                entity_path = f'{module_name}'
                if hasattr(plugin_module, 'entity_collection'):
                    entity_path = f'/{plugin_module.entity_collection}/{module_name}'
                # TODO: what if no 'entity_collection' attribute case?
                parent_router.include_router(plugin_module.router,
                                             prefix = entity_path)
                logger.info(f'Loaded plugin: {module_name}')
            else:
                logger.info(f'Ignored plugin: {module_name}')

        except Exception as e:
            logger.error(f'Faiied to load plugin: {module_name}', exc_info=True)
