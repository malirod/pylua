import lua
import load_lua

script = load_lua.open_script("1.lua")

print('=======START EXECUTION==============\n')

lua.execute(script)

print('\n=======FINISH EXECUTION=============')
