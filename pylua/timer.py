# -*- coding: utf-8 -*-

import asyncio


def msec_to_sec(milliseconds):
    milliseconds_in_second = 1000.0
    assert milliseconds is not None
    return milliseconds/milliseconds_in_second


def sec_to_msec(seconds):
    milliseconds_in_second = 1000.0
    assert seconds is not None
    return seconds*milliseconds_in_second


class Timer(object):

    def __init__(self, task, interval, multishot=False, loop=None):
        self._multishot = multishot
        self._task = task
        self._interval = msec_to_sec(interval)
        self._handler = None
        self._loop = loop
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

    def _run_task(self):
        if self._multishot:
            self.start()
        self._task()

    def _run(self):
        self._handler = self._loop.call_later(self._interval, self._run_task)

    def start(self):
        if self._handler is not None:
            self.stop()
        self._run()

    def stop(self):
        if self._handler is not None:
            self._handler.cancel()
            self._handler = None

    def reset(self):
        self.stop()
        self.start()
