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
from fastapi import APIRouter, Request, HTTPException, status
import asyncio
import json

from routers import common_router

router = APIRouter()

#methods = ['GET', 'DELETE', 'POST', 'PUT']
methods = ['GET']
#
@router.api_route('', methods=methods)
@router.api_route('/', methods=methods)
def handle_components(request: Request):

    resp = common_router.handle_entities(request, None)
    return resp


@router.api_route('/{subpath:path}', methods=methods)
def handle_component_one(request: Request, subpath: str):

    entity_collection = request.url.path.split('/')[3]
    #
    # work: built-in CDA
    #
    canid = -1
    path_elements = subpath.split('/')
    if path_elements[-1] == 'faults':
        entity = (path_elements[-2])
        if entity in request.state.config['topology'][entity_collection].keys():
            if 'canid' in request.state.config['topology'][entity_collection][entity].keys():
                #
                # TODO: To be split to another file.
                #
                canid = request.state.config['topology'][entity_collection][entity]['canid']
                import obdonuds
                import isotp
                socket = isotp.socket()
                tx_id = canid
                rx_id = canid + 0x8
                socket.bind(request.state.config['config']['can_interface'],
                            isotp.Address(rxid=rx_id, txid=tx_id))
                data = obdonuds.send_get_all_dtcs(socket)

                dtc_mask_bits = {
                    'testFailed': 0x01,
                    'testFailedThisOperationCycle': 0x02,
                    'pendingDTC': 0x04,
                    'confirmedDTC': 0x08,
                    'testNotCompletedSinceLastClear': 0x10,
                    'testFailedSinceLastClear': 0x20,
                    'testNotCompletedThisOperationCycle': 0x40,
                    'warningIndicatorRequested': 0x80
                }

                resp_body = dict()
                resp_body['items'] = list()
                if not data:
                    return resp_body

                for dtc in data:
                    item = dict()
                    item['code'] = '%06X' % dtc
                    item['scope'] = 'Default'
                    #item['display_code'] = ''
                    #item['fault_name'] = ''
                    #item['fault_translation_id'] = ''
                    #item['severity'] = ''
                    item['status'] = dict()
                    for status_bit in dtc_mask_bits.keys():
                        if dtc_mask_bits[status_bit] & (dtc & 0xff):
                            item['status'][status_bit] = '1'
                        else:
                            item['status'][status_bit] = '0'
                    resp_body['items'].append(item)
                return resp_body

            else:
                # TODO
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'faults for {canid} not found'
                )
    #
    base_uri = request.state.config['config']['base_uri']
    resp = dict()
    resp['items'] = []
    entity = subpath.split('/')[0]
    if entity in request.state.config['topology'][entity_collection].keys():
        resp_body = dict()
        resp_body['id'] = entity
        resp_body['name'] = entity
        # see Table 53 of ISO 17973-3
        for feature in request.state.config['sovd']['features']:
            resp_body[feature] = '%s/%s' % (request.url, feature)
        resp['items'].append(resp_body)
    return resp
