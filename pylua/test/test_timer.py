# -*- coding: utf-8 -*-

"""
Module implements tests for testing of
timer module
"""

import timeit
import threading
from pylua.timer import Timer, msec_to_sec

class TestPyTimer(object):

    def _timer_task(self):
        self._task_is_run = True
        self._event.set()

    def __init__(self):
        self._interval = 50  # interval in milliseconds
        self._task_is_run = False
        self._event = threading.Event()
        self._shot_counter = 0

    def _wait_event(self, timeout=None):
        if timeout is not None:
            timeout = msec_to_sec(timeout)
        self._event.wait(timeout)

    def _run_timer(self):
        timer = Timer(self._timer_task, self._interval)
        self._task_is_run = False
        started = timeit.default_timer()
        self._event.clear()
        timer.start()
        self._wait_event()
        assert self._task_is_run is True, "Task wasn't run"
        assert (timeit.default_timer() - started) > (
            msec_to_sec(self._interval)), "Timer doesn't work correctly"

    def test_start_timer(self):
        self._run_timer()

    def test_start_timer_periodicaly(self):
        for _ in range(0, 5):
            self._run_timer()

    def test_stop_timer(self):
        self._task_is_run = False
        timer = Timer(self._timer_task, self._interval)
        wait_time = 100  # wait_time in milliseconds
        self._event.clear()
        timer.start()
        timer.stop()
        self._wait_event(wait_time)
        assert self._task_is_run is False, "Timer was not stoped"

    def test_reset_timer(self):
        self._task_is_run = False
        interval = 600  # interval in milliseconds
        timer = Timer(self._timer_task, interval)
        wait_time = 100  # wait_time in milliseconds
        self._event.clear()
        timer.start()
        self._wait_event(wait_time)
        reseted = timeit.default_timer()
        self._event.clear()
        timer.reset()
        wait_time = 700
        self._wait_event()
        assert self._task_is_run is True, "Reset doesn't work"
        assert (timeit.default_timer() - reseted) > (
            msec_to_sec(interval)), "Timer doesn't work correctly"

    def _multishot_task(self):
        self._shot_counter = self._shot_counter + 1
        if self._shot_counter >= 3:
            self._event.set()

    def test_multishot_timer(self):
        timer = Timer(self._multishot_task, interval=30, multishot=True)
        timer.start()
        self._wait_event()
        timer.stop()
        assert self._shot_counter == 3

    def test_autostart_multishot_timer(self):
        timer = Timer(self._multishot_task,
                      interval=30, multishot=True, autostart=True)
        self._wait_event()
        timer.stop()
        assert self._shot_counter == 3
