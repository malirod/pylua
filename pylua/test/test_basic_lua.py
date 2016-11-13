# -*- coding: utf-8 -*-

from gc import collect
from lupa import LuaRuntime


class TestLuaBasic(object):

    def __init__(self):
        self._lua = None

    def setup(self):
        self._lua = LuaRuntime()

    def teardown(self):
        self._lua = None
        collect()

    def test_eval(self):
        assert self._lua.eval('1+1') == 2

    def test_factorial(self):
        fac = self._lua.execute('''\
            function fac(i)
                if i <= 1
                    then return 1
                    else return i * fac(i-1)
                end
            end
            return fac
            ''')
        assert fac is not None
        assert fac(3) == 6
        assert fac(10) == 3628800
