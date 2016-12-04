# -*- coding: utf-8 -*-

"""Module stores all global default settings. To customize setting put
   local_settings.py near by and set custom values."""

LOG_CONFIG = 'log.config'

# Load custom\local settings if exists
try:
    # pylint: disable=wrong-import-position, wildcard-import
    from local_settings import * # NOQA
except ImportError:
    pass
