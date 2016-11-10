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

    def __init__(self, task, interval):
        self._task = task
        self._interfal = msec_to_sec(interval)
        self._timer = threading.Timer(self._interfal, self._task)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.cancel()

    def reset(self):
        self._timer.cancel()
        self._timer = threading.Timer(self._interfal, self._task)
        self._timer.start()
