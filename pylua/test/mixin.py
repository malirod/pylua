# -*- coding: utf-8 -*-

import asyncio
from gc import collect
from lupa import LuaRuntime

class BaseFixture(object):
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def teardown(self):
        pass

class EventLoopMixin(BaseFixture):

    def __init__(self):
        super().__init__()
        self._loop = None
        self._old_loop = None

    def setup(self):
        super().setup()
        self._loop = asyncio.new_event_loop()
        self._old_loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self._loop)

    def teardown(self):
        super().teardown()
        asyncio.set_event_loop(self._old_loop)
        self._loop = None
        self._old_loop = None

    @property
    def loop(self):
        return self._loop

class LuaRuntimeMixin(BaseFixture):

    def __init__(self):
        super().__init__()
        self._lua_runtime = None

    def setup(self):
        super().setup()
        self._lua_runtime = LuaRuntime(unpack_returned_tuples=True)

    def teardown(self):
        super().teardown()
        self._lua_runtime = None
        collect()

    @property
    def lua_runtime(self):
        return self._lua_runtime
