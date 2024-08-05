from instruction import *
from machine import *

prompt = "> "

m = Machine()
m.add_fn(Operator.LOAD, fn = (lambda m, v: m.set(0, v)))
m.add_fn(Operator.END, fn = (lambda m, v: m.end()))

print(m)
m.run(Program.from_string("LOAD 42\nEND"))
print(m)

#while (inp := input(prompt)).upper() != "X":
#    inst = Instruction.from_string(inp)
#    match inst:
#        case Ok(value):
#            print(value)
#        case Err(e):
#            print(e)
