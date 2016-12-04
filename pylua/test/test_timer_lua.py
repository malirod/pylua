# -*- coding: utf-8 -*-

import timeit
from pylua.timer import Timer, msec_to_sec
from pylua.test.mixin import EventLoopMixin, LuaRuntimeMixin

class TestTimer(EventLoopMixin, LuaRuntimeMixin):

    def __init__(self):
        super().__init__()

    def setup(self):
        super().setup()
        self.lua_runtime.globals()['Timer'] = Timer
        self.lua_runtime.globals()['event_loop'] = self.loop
        self.lua_runtime.globals()['now'] = timeit.default_timer
        self.lua_runtime.globals()['msec_to_sec'] = msec_to_sec

    def teardown(self):
        super().teardown()

    def test_start_timer(self):
        lua_code = '''\
            local shot_counter = 0
            local interval_ms = 30
            local started = now()
            local function timer_task()
                delay = now() - started
                assert(delay >=
                    msec_to_sec(interval_ms), "Timer doesn't work correctly")
                shot_counter = shot_counter + 1
                event_loop.stop()
            end
            local timer = Timer(timer_task, interval_ms)
            timer.start()
            event_loop.run_forever()
            assert(shot_counter == 1, "Wrong number of tasks fired")
            '''
        self.lua_runtime.execute(lua_code)


    def test_start_multiple_timers(self):
        lua_code = '''\
            local timers_count = 5
            local shot_counter = 0
            local interval_ms = 30
            local started = now()
            function timer_task()
                delay = now() - started
                assert(delay >=
                    msec_to_sec(interval_ms), "Timer doesn't work correctly")
                shot_counter = shot_counter + 1
                if shot_counter == timers_count then
                    event_loop.stop()
                end
            end
            local timers = {}
            for i = 1, timers_count do
                local timer = Timer(timer_task, interval_ms)
                table.insert(timers, timer)
                timer.start()
            end
            event_loop.run_forever()
            assert(shot_counter == timers_count, "Wrong number of tasks fired")
            '''
        self.lua_runtime.execute(lua_code)

    def test_multishot_timer(self):
        lua_code = '''\
            local shots_count = 3
            local shot_counter = 0
            local interval_ms = 30
            local started = now()
            function timer_task()
                delay = now() - started
                assert(delay >=
                    msec_to_sec(interval_ms), "Timer doesn't work correctly")
                shot_counter = shot_counter + 1
                started = now()
                if shot_counter >= shots_count then
                    event_loop.stop()
                end
            end
            local timer = Timer(timer_task, interval_ms, true)
            timer.start()
            event_loop.run_forever()
            assert(shot_counter == shots_count, "Wrong number of tasks fired")
            '''
        self.lua_runtime.execute(lua_code)
