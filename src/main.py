from instruction import *
from machine import *

prompt = "> "

def bool_to_int(boolean: bool):
    if boolean:
        return 1
    else:
        return 0

m = Machine()
m.add_fn(Operator.STORE, fn = (lambda m, v: m.set(v, m.get(0))))
m.add_fn(Operator.LOAD, fn = (lambda m, v: m.set(0, v)))
m.add_fn(Operator.END, fn = (lambda m, v: m.end()))
m.add_fn(Operator.GO_TO, fn = (lambda m, v: m.set_pc(v)))
m.add_fn(Operator.IF_EQ, fn = (lambda m, v: m.inc_pc(bool_to_int(m.get(0) != v))))


print(m)
code = """LOAD 42
IF = 42 GO TO 4
LOAD 420
LOAD 69
"""
m.run(Program.from_string(code))
print(m)
