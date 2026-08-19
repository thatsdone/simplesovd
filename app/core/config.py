#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import os
import sys
import logging
import yaml
import pprint
#
from fastapi import Request
#
class SOVDConfig:
    def __init__(self):
        self.debug: bool = True if os.environ.get('SIMPLESOVD_DEBUG') in ('true', '1') else False
        self.simplesovd_config: str = os.environ.get('SIMPLESOVD_CONFIG', 'config.yaml')
        #
        self.log_level = logging.DEBUG if self.debug else logging.INFO

        fmt = '%(asctime)s.%(msecs)03d %(levelname)s: %(funcName)s: %(message)s'
        datefmt='%Y/%m/%d %H:%M:%S'
        logging.basicConfig(
            level = self.log_level,
            format = fmt,
            datefmt = datefmt,
            handlers = [
                logging.StreamHandler(sys.stdout)
            ]
        )

        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('httpcore').setLevel(logging.WARNING)

        self.logger = logging.getLogger(__name__)
        #
        if not os.path.exists(self.simplesovd_config):
            return {}
        #
        self.static_conf = None
        with open(self.simplesovd_config, 'rt') as fp:
            self.static_conf = yaml.load(fp, Loader=yaml.SafeLoader)
            if not self.static_conf:
                sys.exit()
        self.logger.debug(pprint.pformat(self.static_conf))

def get_conf(request: Request) -> SOVDConfig:
    return request.state.conf
