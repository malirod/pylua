#!/usr/bin/env python2
# -*- coding: utf-8 -*-

LOG_CONFIG = 'log.config'

# Load custom\local settings if exists
try:
    from local_settings import *  # NOQA
except ImportError:
    pass
