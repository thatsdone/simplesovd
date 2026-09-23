#!/usr/bin/env python3
#
# simplesovd: A simple implementation of SOVD (ISO 17978)
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2026/08/09 v0.2 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * many
import logging

from fastapi.routing import APIRoute, _IncludedRouter

logger = logging.getLogger(__name__)

def get_all_routes(routes, prefix=''):
    all_routes = []
    for route in routes:
        if isinstance(route, _IncludedRouter):
            orig_router = getattr(route, 'original_router', None)
            include_ctx = getattr(route, 'include_context', None)
            route_prefix = getattr(include_ctx, 'prefix', '') if include_ctx else ''
            if orig_router and hasattr(orig_router, 'routes'):
                all_routes.extend(get_all_routes(orig_router.routes, prefix=prefix + route_prefix))

        elif isinstance(route, APIRoute):
            all_routes.append((prefix + route.path, route.methods, route.endpoint))
    return all_routes
