from result import Result, Ok, Err
from instruction import *

inp = input("> ")
while inp.upper() != "X":
    inst = Instruction.from_string(inp)
    match inst:
        case Ok(value):
            print(value)
        case Err(e):
            print(e)
    inp = input("> ")
