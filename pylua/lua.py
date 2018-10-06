# -*- coding: utf-8 -*-

import sys
import os

LUA_RUNTIME = None


def get_lua_runtime():
    from lupa import LuaRuntime
    global LUA_RUNTIME  # pylint: disable=global-statement
    if LUA_RUNTIME is None:
        LUA_RUNTIME = LuaRuntime()
    return LUA_RUNTIME


def load_lua_script(lua_script_name):
    python_path = sys.path
    lua_script_full_name = lua_script_name + '.lua'
    lua_script_full_path = None
    for path_item in python_path:
        for root, _, files in os.walk(path_item):
            for file in files:
                if lua_script_full_name == file:
                    lua_script_full_path = os.path.join(root, file)
    with open(lua_script_full_path) as lua_script_file:
        content = lua_script_file.read()
    return content


def eval_lua_script(lua_script):
    lua_runtime = get_lua_runtime()
    return lua_runtime.eval(lua_script)


def exec_lua_script(lua_script):
    lua_runtime = get_lua_runtime()
    return lua_runtime.execute(lua_script)
