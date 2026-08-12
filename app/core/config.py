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
import os
import sys
import logging
import yaml
import pprint
#
class SOVDConfig:
    def __init__(self):
        self.debug: bool = True if os.environ.get('SIMPLESOVD_DEBUG') in ('true', '1') else False
        self.simplesovd_config: str = os.environ.get('SIMPLESOVD_CONFIG', 'config.yaml')
        #
        self.log_level = logging.DEBUG if self.debug else logging.INFO

        fmt = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s'
        datefmt='%Y/%m/%d %H:%M:%S'
        logging.basicConfig(
            level = self.log_level,
            format = fmt,
            datefmt = datefmt,
            handlers = [
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        #
        if not os.path.exists(self.simplesovd_config):
            return {}
        #
        self.predefined_config = None
        with open(self.simplesovd_config, 'rt') as fp:
            self.predefined_config = yaml.load(fp, Loader=yaml.SafeLoader)
            if not self.predefined_config:
                sys.exit()
        self.logger.debug(pprint.pformat(self.predefined_config))


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

