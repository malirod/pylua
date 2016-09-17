#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os
from fabric.api import local, task
from pylua.settings import LOG_CONFIG

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = 'pylua'
TESTS_DIR = os.path.join(SRC_DIR, 'test')
LOG_CONFIG_PATH = os.path.join(ROOT_DIR, SRC_DIR, LOG_CONFIG)


@task
def test_all():
    local('nosetests -vv --with-timer {} --log-config={}'.format(
        TESTS_DIR, LOG_CONFIG_PATH))


@task
def run_test(name=None):
    if name is None:
        print 'Usage: fab run_test:name=<file>:<Test_Case>.<test_method>'
        print ('Sample: fab run_test:name={}/test_json.py:TestJson.'
               'test_int_param_py'.format(TESTS_DIR))
        return
    local('nosetests -vv -s --with-timer --log-config={} {}'.format(
        LOG_CONFIG_PATH, name))
