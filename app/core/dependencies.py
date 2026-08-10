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
from fastapi import HTTPException, Path, Request, Response, status
import httpx
#
from app.core.config import get_logger
logger = get_logger(__name__)

def get_entity_collection(request: Request) -> dict:
    logger.debug('get_entity_collection(): %s' % (request.url))
    entity_collection = request.url.path.split('/')[3]

    sovd_config = request.state.config
    res = {'items': []}
    for item in sovd_config.get('topology', {}).get(entity_collection, {}):
        elm = sovd_config.get('topology', {}).get(entity_collection, {}).get(item, None)
        entity = dict()
        entity['id'] = item
        entity['name'] = item
        entity['tags'] = []
        if elm:
            for tag in elm.get('tags', []):
                entity['tags'].append(tag)
        res['items'].append(entity)
    return res


class EntityDiscovery:

    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    async def __call__(self, request: Request,
                       entity_id: str = Path(...)) -> dict:
        sovd_config = request.state.config
        #
        topology = sovd_config.get('topology', {})
        collection = topology.get(self.collection_name, {})
        if entity_id not in collection:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail=f'{self.collection_name} {entity_id} not found in the current topology'
            )
        res = dict()
        res['id'] = entity_id
        res['name'] = entity_id
        entity_collection = request.url.path.split('/')[3]
        entity_ref = sovd_config.get('topology', {}).get(entity_collection, {}).get(entity_id, {})
        if entity_ref and entity_ref.get('tags', None):
            res['tags'] = []
            for tag in entity_ref['tags']:
                res['tags'].append(tag)
        if entity_ref and entity_ref.get('area', None):
            res['area'] = entity_ref['area']

        # works for both below:
        # /{entity-collection}/{entity}/{feature}
        # /{entity-collection}/{entity}
        #
        # backend SOVD entity server case.
        # 'href' in config.yaml
        #
        if entity_ref and entity_ref.get('href', None):
            href = entity_ref.get('href')

            client = httpx.AsyncClient() #base_url=href)

            try:
                backend_resp = await client.request(
                    method=request.method,
                    url = href + '/' + '/'.join(request.url.path.split('/')[5:]),
                    params=request.query_params,
                    headers=request.headers,
                    #TODO: handle Request body (and response...)
                    #content=request.body(),
                    timeout=5.0
                )
                return Response(
                    content=backend_resp.content,
                    status_code=backend_resp.status_code,
                    headers=dict(backend_resp.headers)
                )
            except Exception as e:
                logger.error(f'Exception: {e}' )
                raise HTTPException(
                    status_code = status. HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f'Service unavailable'
                )

        elif entity_ref and entity_ref.get('type', None) and entity_ref.get('canid', {}):
            print('DEBUG: entity_id: %s %s %03X' % (entity_id,
                                              entity_ref.get('type'),
                                              entity_ref.get('canid')
                                              ))

        return res
