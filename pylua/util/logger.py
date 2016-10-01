#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pylua.settings import LOG_CONFIG


def init_logging():
    from logging.config import fileConfig

    fileConfig(LOG_CONFIG)
