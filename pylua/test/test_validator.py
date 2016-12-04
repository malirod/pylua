# -*- coding: utf-8 -*-

from pylua.validator import Validator
from pylua.test.mixin import LuaRuntimeMixin

class TestValidator(LuaRuntimeMixin):

    _xml_schema = '''\
        <root>
            <function name="update" id="update" type="request">
                <param name="some_list" minsize="1" maxsize="100" array="true" mandatory="false">
                </param>
                <param name="some_bool_param" type="Boolean" mandatory="true">
                </param>
            </function>
            <function name="put" id="put" type="request">
                <param name="some_string" type="String" mandatory="true">
                </param>
            </function>
            <function name="get" id="get" type="request">
            </function>
        </root>
        '''

    def __init__(self):
        super().__init__()
        self._validator = None

    def setup(self):
        super().setup()
        self._validator = Validator()
        loaded = self._validator.load_schema_from_string(self._xml_schema)
        self.lua_runtime.globals()['Validator'] = self._validator
        assert loaded

    def teardown(self):
        super().teardown()

    def test_load_invalid_xml(self):
        invalid_xml = '<root><sub-root></sub-root>'
        loaded = self._validator.load_schema_from_string(invalid_xml)
        assert not loaded

    def test_load_invalid_xml_lua(self):
        lua_code = '''\
            local invalid_xml = '<root><sub-root></sub-root>'
            local loaded = Validator.load_schema_from_string(invalid_xml)
            assert(not loaded, "Expected to fail on invalid xml")
            '''
        self._lua_runtime.execute(lua_code)

    def test_not_found(self):
        code, error = self._validator.validate('get', 'response')
        assert code == 1
        assert error == 'Function not found'

    def test_not_found_lua(self):
        lua_code = '''\
            local code, error = Validator.validate('get', 'response')
            assert(code == 1)
            assert(error == 'Function not found')
            '''
        self._lua_runtime.execute(lua_code)

    def test_ok_no_params(self):
        code, error = self._validator.validate('get', 'request')
        assert code == 0
        assert error == 'Ok'

    def test_ok_no_params_lua(self):
        lua_code = '''\
            local code, error = Validator.validate('get', 'request')
            assert(code == 0)
            assert(error == 'Ok')
            '''
        self._lua_runtime.execute(lua_code)

    def test_ok_params(self):
        code, error = self._validator.validate('put', 'request', '{"some_string": "string_value"}')
        assert code == 0
        assert error == 'Ok'

    def test_ok_params_lua(self):
        lua_code = '''\
            local code, error = Validator.validate('put', 'request', '{"some_string": "string_value"}')
            assert(code == 0)
            assert(error == 'Ok')
            '''
        self._lua_runtime.execute(lua_code)

    def test_error_params_wrong_name(self):
        code, error = self._validator.validate(
            'put', 'request', '{"some_another_string": "string_value"}')
        assert code == 2
        assert error == 'Validation error'

    def test_error_params_wrong_name_lua(self):
        lua_code = '''\
            local code, error = Validator.validate('put', 'request', '{"some_another_string": "string_value"}')
            assert(code == 2)
            assert(error == 'Validation error')
            '''
        self._lua_runtime.execute(lua_code)

    def test_error_wrong_function(self):
        code, error = self._validator.validate('delete', 'request')
        assert code == 1
        assert error == 'Function not found'

    def test_error_wrong_function_lua(self):
        lua_code = '''\
            local code, error = Validator.validate('delete', 'request')
            assert(code == 1)
            assert(error == 'Function not found')
            '''
        self._lua_runtime.execute(lua_code)
