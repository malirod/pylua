# -*- coding: utf-8 -*-

import asyncio
from gc import collect
from pylua.network import send_get_echo_message
from pylua.network import run_websocket_server
from lupa import LuaRuntime

class TestWebSocket(object):
    def __init__(self):
        self._lua_runtime = None
        self._loop = None
        self._old_loop = None

    def setup(self):
        self._lua_runtime = LuaRuntime()
        self._loop = asyncio.new_event_loop()
        self._old_loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self._loop)
        self._lua_runtime.globals()['run_server'] = self._prepare_server
        self._lua_runtime.globals()['send_message'] = send_get_echo_message

    def teardown(self):
        asyncio.set_event_loop(self._old_loop)
        self._lua_runtime = None
        self._loop = None
        self._old_loop = None
        collect()

    def _prepare_server(self, address, port): #pylint: disable=no-self-use
        asyncio.set_event_loop(asyncio.new_event_loop())
        run_websocket_server(address, port)

    def test_send_one_message_server(self):
        self._prepare_server('localhost', 8087)
        assert send_get_echo_message("test1") == "test1"
        asyncio.get_event_loop().close()

    def test_send_two_messages_server(self):
        self._prepare_server('localhost', 8081)
        assert send_get_echo_message("test2", 'ws://localhost:8081') == "test2"
        assert send_get_echo_message("test22", 'ws://localhost:8081') == "test22"
        asyncio.get_event_loop().close()

    def test_send_message_from_lua(self):
        lua_code = '''\
        run_server('localhost', 8082)
        text = send_message('test3', 'ws://localhost:8082')
        assert(text == "test3", "Wrong response message")
        '''
        self._lua_runtime.execute(lua_code)
