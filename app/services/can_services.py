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
from fastapi import HTTPException, status
import asyncio

import can
import isotp
import logging
from fastapi import Request

can_lock = asyncio.Lock()

logger = logging.getLogger(__name__)

# TODO: make it as configurable
can_timeout = 2.0

# Note: dependency injection does not work here.
def _blocking_isotp_worker(payload: bytes, request: Request):

    conf = request.state.conf.static_conf
    can_interface = conf.get('config', {}).get('can_interface', None)
    if not can_interface:
        logger.error('can_interface not found in config.')
        return
    socket = isotp.socket()

    # TODO:
    # * refer somewhere or allow multiple isotp sockets handling
    # * allow functional address (0x7DF) handling
    tx_id = 0x7E0 # EngineECU
    rx_id = tx_id + 0x8 # respnonse from EngineECU
    try:
        logger.debug('Sending a CAN msg: if:%s tx:%03X rx:%03X' % (can_interface, tx_id, rx_id))
        socket.bind(can_interface, isotp.Address(txid=tx_id, rxid=rx_id))
        socket.settimeout(can_timeout)
        socket.send(payload)
        response = socket.recv()
        return response

    except Exception as e:
        logger.error(f'Exception: {e}')
        raise
    finally:
        socket.close()

async def can_query(payload: bytes, request: Request) -> bytes:

    logger.debug('can_query() called.')

    async with can_lock:
        try:
            response = await asyncio.to_thread(_blocking_isotp_worker,
                                               payload, request)
            return response
        except Exception as e:
            logger.error(f'Failed CAN transaction: {e}')
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f'Service unavailable'
            )
