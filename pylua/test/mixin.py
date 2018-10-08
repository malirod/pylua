# -*- coding: utf-8 -*-

import asyncio
from gc import collect
from lupa import LuaRuntime


class EventLoopMixin:

    def setup(self):
        self._loop = asyncio.new_event_loop()
        self._old_loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self._loop)

    def teardown(self):
        asyncio.set_event_loop(self._old_loop)

    @property
    def loop(self):
        return self._loop


class LuaRuntimeMixin:

    def setup(self):
        self._lua_runtime = LuaRuntime(unpack_returned_tuples=True)

    @staticmethod
    def teardown():
        collect()

    @property
    def lua_runtime(self):
        return self._lua_runtime
