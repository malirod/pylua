#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Module implements wrapper of python
timer. Wrapper allows to use timer with milliseconds
"""

import threading


def msec_to_sec(milliseconds):
    milliseconds_in_second = 1000.0
    assert milliseconds is not None
    return milliseconds/milliseconds_in_second


def sec_to_msec(seconds):
    milliseconds_in_second = 1000.0
    assert seconds is not None
    return seconds*milliseconds_in_second



class PyTimer(object):

    def __init__(self, task, interval, multishot=False, autostart=False):
        self._multishot = multishot
        self._task = task
        self._interfal = msec_to_sec(interval)
        self._is_runnning = False
        self._timer = None
        if autostart:
            self.start()

    def _run_task(self):
        if self._multishot:
            self._is_runnning = False
        self.start()
        self._task()

    def _run_timer(self):
        self._timer = threading.Timer(self._interfal, self._run_task)
        self._timer.start()
        self._is_runnning = True

    def start(self):
        if not self._is_runnning:
            self._run_timer()

    def stop(self):
        self._is_runnning = False
        self._timer.cancel()

    def reset(self):
        self._timer.cancel()
        self._run_timer()
