# -*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger(__name__)


class TestJson(object):

    _JSON_STRING = '''{
        "IntParam": 10,
        "StrParam": "TestString",
        "ArrayParam": [1,2,3],
        "ObjParam": {"ObjIntParam": 11, "ObjStrParam": "ObjTestString"}
        }'''

    _json_obj = None

    def __init__(self):
        pass

    def setup(self):
        logger.debug('Setup')
        self._json_obj = json.loads(self._JSON_STRING)
        assert self._json_obj is not None
        assert isinstance(self._json_obj, dict)

    @classmethod
    def teardown(cls):
        logger.debug('Teardown')

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_int_param_py(self):
        assert 'IntParam' in self._json_obj
        value = self._json_obj['IntParam']
        assert isinstance(value, int)
        assert value == 10

    def test_int_param_lua(self):
        pass

    def test_string_param_py(self):
        assert 'StrParam' in self._json_obj
        value = self._json_obj['StrParam']
        assert isinstance(value, str)
        assert value == 'TestString'

    def test_string_param_lua(self):
        pass

    def test_array_param_py(self):
        assert 'ArrayParam' in self._json_obj
        value = self._json_obj['ArrayParam']
        assert isinstance(value, list)
        assert len(value) == 3
        index = 1
        for item in value:
            assert index == item
            index += 1
        assert index == 4

    def test_array_param_lua(self):
        pass

    def test_obj_param_py(self):
        assert 'ObjParam' in self._json_obj
        value = self._json_obj['ObjParam']
        assert isinstance(value, dict)
        assert 'ObjIntParam' in value
        param = value['ObjIntParam']
        assert isinstance(param, int)
        assert param == 11
        assert 'ObjStrParam' in value
        param = value['ObjStrParam']
        assert isinstance(param, str)
        assert param == 'ObjTestString'

    def test_obj_param_lua(self):
        pass
