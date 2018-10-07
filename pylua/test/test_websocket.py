# -*- coding: utf-8 -*-

import asyncio
from pylua.network import send, run_websocket_server
from pylua.test.mixin import EventLoopMixin, LuaRuntimeMixin


SERVER_ADDRESS = '127.0.0.1'


def send_get_echo_message(message, address='ws://{}:8087'.format(SERVER_ADDRESS)):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(send(message, address))
    return result


def prepare_server(address, port):
    server_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(server_event_loop)
    run_websocket_server(address, port)
    return server_event_loop


class TestWebSocket(EventLoopMixin, LuaRuntimeMixin):

    def setup(self):
        EventLoopMixin.setup(self)
        LuaRuntimeMixin.setup(self)
        self.lua_runtime.globals()['run_server'] = prepare_server
        self.lua_runtime.globals()['send_message'] = send_get_echo_message

    def teardown(self):
        LuaRuntimeMixin.teardown()
        EventLoopMixin.teardown(self)

    def test_send_one_message_server(self):
        server_event_loop = prepare_server(SERVER_ADDRESS, 8087)
        assert send_get_echo_message("test1") == "test1"
        server_event_loop.close()
        self.loop.close()

    def test_send_two_messages_server(self):
        server_event_loop = prepare_server(SERVER_ADDRESS, 8081)
        assert send_get_echo_message(
            "test2", 'ws://{}:8081'.format(SERVER_ADDRESS)) == "test2"
        assert send_get_echo_message(
            "test22", 'ws://{}:8081'.format(SERVER_ADDRESS)) == "test22"
        server_event_loop.close()
        self.loop.close()

    def test_send_message_from_lua(self):
        lua_code = '''
        server_event_loop = run_server('{0}', 8082)
        text = send_message('test3', 'ws://{0}:8082')
        assert(text == "test3", "Wrong response message")
        server_event_loop.close()
        '''.format(SERVER_ADDRESS)
        self._lua_runtime.execute(lua_code)
