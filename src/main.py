from result import Result, Ok, Err
from instruction import *

prompt = "> "


while (inp := input(prompt)).upper() != "X":
    inst = Instruction.from_string(inp)
    match inst:
        case Ok(value):
            print(value)
        case Err(e):
            print(e)
