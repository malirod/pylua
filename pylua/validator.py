# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
from json import JSONDecoder

class Validator(object):

    _errors = [(0, 'Ok'), (1, "Function not found"), (2, "Validation error")]
    _error_indx_ok = 0
    _error_indx_not_found = 1
    _error_indx_error = 2

    def __init__(self):
        self._schema = None

    def load_schema_from_string(self, xml_string):
        assert xml_string is not None
        try:
            self._schema = etree.fromstring(xml_string)
        except etree.ParseError:
            return False
        return True

    @staticmethod
    def _validate_param(schema_param_name, schema_param_is_mandatory,
                        schema_param_type, params):
        assert schema_param_name is not None
        assert schema_param_is_mandatory is not None
        assert schema_param_type is not None
        params_obj = JSONDecoder().decode(params)
        if params_obj.get(schema_param_name) is None:
            return False
        return True

    def _validate(self, function_item, params):
        # This is very simple validation, will work only with test data
        schema_params = function_item.findall('param')
        is_schema_params_empty = len(schema_params) == 0
        if not is_schema_params_empty and params is None:
            return self._errors[self._error_indx_error]
        if is_schema_params_empty and params is None:
            return self._errors[self._error_indx_ok]
        for param in schema_params:
            validated = self._validate_param(
                param.get('name'),
                param.get('mandatory'),
                param.get('type'),
                params)
            if not validated:
                return self._errors[self._error_indx_error]

        return self._errors[self._error_indx_ok]

    def validate(self, function_id, function_type, params=None):
        assert function_id is not None
        assert function_type is not None
        assert self._schema is not None
        for function_item in self._schema.findall('function'):
            if (function_id == function_item.get('id')
                    and function_type == function_item.get('type')):
                return self._validate(function_item, params)
        return self._errors[self._error_indx_not_found]
