# -*- coding: utf-8 -*-

import asyncio
from pylua.network import send, run_websocket_server
from pylua.test.mixin import EventLoopMixin, LuaRuntimeMixin


def send_get_echo_message(message, address='ws://localhost:8087'):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(send(message, address))
    return result


def prepare_server(address, port):
    asyncio.set_event_loop(asyncio.new_event_loop())
    run_websocket_server(address, port)


class TestWebSocket(EventLoopMixin, LuaRuntimeMixin):

    def __init__(self):
        super().__init__()

    def setup(self):
        super().setup()
        self.lua_runtime.globals()['run_server'] = prepare_server
        self.lua_runtime.globals()['send_message'] = send_get_echo_message

    def teardown(self):
        super().teardown()

    def test_send_one_message_server(self):
        prepare_server('localhost', 8087)
        assert send_get_echo_message("test1") == "test1"
        self.loop.close()

    def test_send_two_messages_server(self):
        prepare_server('localhost', 8081)
        assert send_get_echo_message("test2", 'ws://localhost:8081') == "test2"
        assert send_get_echo_message("test22", 'ws://localhost:8081') == "test22"
        self.loop.close()

    def test_send_message_from_lua(self):
        lua_code = '''\
        run_server('localhost', 8082)
        text = send_message('test3', 'ws://localhost:8082')
        assert(text == "test3", "Wrong response message")
        '''
        self._lua_runtime.execute(lua_code)
