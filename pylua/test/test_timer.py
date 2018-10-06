# -*- coding: utf-8 -*-

import timeit
from pylua.timer import Timer, msec_to_sec
from pylua.test.mixin import EventLoopMixin


class TestTimer(EventLoopMixin):

    def __init__(self):
        super().__init__()
        self._interval_ms = 30
        self._timer = None

    def setup(self):
        EventLoopMixin.setup(self)

    def teardown(self):
        EventLoopMixin.teardown(self)

    def test_start_timer(self):
        started = timeit.default_timer()
        shot_counter = 0

        def task():
            nonlocal shot_counter
            nonlocal started
            delay = timeit.default_timer() - started
            assert delay >= msec_to_sec(
                self._interval_ms), "Timer doesn't work correctly"
            shot_counter += 1
            self.loop.stop()
        self._timer = Timer(task, self._interval_ms, loop=self.loop)
        self._timer.start()
        self.loop.run_forever()
        assert shot_counter == 1, "Wrong number of tasks fired"

    def test_start_multiple_timers(self):
        timers_count = 5
        started = timeit.default_timer()
        shot_counter = 0

        def task():
            nonlocal shot_counter
            delay = timeit.default_timer() - started
            assert delay >= msec_to_sec(
                self._interval_ms), "Timer doesn't work correctly"
            shot_counter += 1
            if shot_counter == timers_count:
                self.loop.stop()
        timers = [Timer(task, self._interval_ms, loop=self.loop)
                  for _ in range(timers_count)]
        for timer in timers:
            timer.start()
        self.loop.run_forever()
        assert shot_counter == timers_count, "Wrong number of tasks fired"

    def test_stop_timer(self):
        timers_count = 3
        shot_counter = 0

        def task():
            nonlocal shot_counter
            shot_counter += 1
            if shot_counter == timers_count - 1:
                self.loop.stop()
        timers = [Timer(task, self._interval_ms, loop=self.loop)
                  for _ in range(timers_count)]
        for timer in timers:
            timer.start()
        timers[0].stop()
        self.loop.run_forever()
        assert shot_counter == timers_count - 1, "Wrong number of tasks fired"

    def test_multishot_timer(self):
        shots_count = 3
        shot_counter = 0
        started = timeit.default_timer()

        def task():
            nonlocal shot_counter
            nonlocal started
            delay = timeit.default_timer() - started
            assert delay >= msec_to_sec(
                self._interval_ms), "Timer doesn't work correctly"
            shot_counter += 1
            started = timeit.default_timer()
            if shot_counter >= shots_count:
                self.loop.stop()
        self._timer = Timer(task, self._interval_ms,
                            multishot=True, loop=self.loop)
        self._timer.start()
        self.loop.run_forever()
        assert shot_counter == shots_count, "Wrong number of tasks fired"

    def test_reset_timer(self):
        shot_counter = 0

        def task():
            nonlocal shot_counter
            shot_counter += 1
            self._timer.reset()
            if shot_counter >= 3:
                self.loop.stop()
        self._timer = Timer(task, self._interval_ms,
                            multishot=False, loop=self.loop)
        self._timer.start()
        self.loop.run_forever()
        assert shot_counter == 3, "Wrong number of tasks fired"
