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
from fastapi import APIRouter, Request
import asyncio
import json

def handle_entities(request: Request, subpath: str):

    entity_collection = request.url.path.split('/')[3]
    resp = dict()
    resp['items'] = []
    base_uri = request.state.config['config']['base_uri']
    for elm in request.state.config['topology'][entity_collection]:
        resp['items'].append({'id': elm,
                              'name': elm,
                              'href': '%s/%s/%s' % (base_uri,
                                                    entity_collection,
                                                    elm)
                              })
    return resp

