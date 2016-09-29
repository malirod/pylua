

package.loadlib("libpython2.7.so", "*")
require('lua-python')

python.execute("import mymodule")

pg = python.globals()

print('Hello from Lua!')

s = pg.mymodule.python_method()

print(s)
