# -*- coding: utf-8 -*-

from gc import collect
from lupa import LuaRuntime
from pylua.lua import eval_lua_script, exec_lua_script, load_lua_script


def create_data_producer(data):
    result = DataProducer(data)
    return result


class DataProducer(object):

    def __init__(self, initial_data):
        self._data = initial_data

    def add_to_data(self, addition):
        self._data += addition

    def get_data(self):
        return self._data

class TestLuaBasic(object):

    def __init__(self):
        self._lua_runtime = None

    def setup(self):
        self._lua_runtime = LuaRuntime()

    def teardown(self):
        self._lua_runtime = None
        collect()

    def test_eval_local(self):
        assert self._lua_runtime.eval('1+1') == 2

    @staticmethod
    def test_eval_global():
        assert eval_lua_script('1+1') == 2

    def test_factorial_local(self):
        fac = self._lua_runtime.execute('''\
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

    @staticmethod
    def test_factorial_global():
        lua_func = exec_lua_script('''\
            function fac(i)
                if i <= 1
                    then return 1
                    else return i * fac(i-1)
                end
            end
            return fac
            ''')
        assert lua_func is not None
        assert lua_func(3) == 6
        assert lua_func(10) == 3628800

    @staticmethod
    def test_load_lua_from_file():
        lua_code = '''\
            function (initial_value, count)
                local result = initial_value
                for i=1, count do
                result = result + 1
                end
                return result
            end
            '''
        lua_func_local = eval_lua_script(lua_code)
        assert lua_func_local(5, 10) == 15
        lua_func_loaded = eval_lua_script(load_lua_script('basic'))
        assert lua_func_loaded(6, 10) == 16

    def test_feed_python_object_to_lua(self):
        data_producer = create_data_producer('aaa')
        data_producer.add_to_data('bbb')
        assert data_producer.get_data() == 'aaabbb'
        self._lua_runtime.globals()['create_data_producer'] = create_data_producer
        lua_code = '''\
            function test()
                local data_producer = create_data_producer('nnn')
                data_producer.add_to_data('zzz')
                return data_producer.get_data()
            end
            return test()
            '''
        result = self._lua_runtime.execute(lua_code)
        assert result == 'nnnzzz'
