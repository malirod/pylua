# -*- coding: utf-8 -*-

import asyncio
from threading import Thread
from pylua.timer import Timer
from lupa import LuaRuntime


def assert_expr(expr):
    assert expr


class TestTimerLua(object):  # pylint: disable=too-few-public-methods

    def __init__(self):
        pass

    @staticmethod
    def test_start_timer_lua():
        def worker():
            lua_runtime = LuaRuntime()
            lua_runtime.globals()['Timer'] = Timer
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            lua_runtime.globals()['event_loop'] = loop
            lua_runtime.globals()['assert_expr'] = assert_expr
            lua_code = '''\
                local shot_counter = 0
                local function timer_task()
                    shot_counter = shot_counter + 1
                    event_loop.stop()
                end
                local timer = Timer(timer_task, 30)
                timer.start()
                event_loop.run_forever()
                assert_expr(shot_counter == 3)
                '''
            lua_runtime.execute(lua_code)
        thread = Thread(target=worker)
        thread.start()
        thread.join()
