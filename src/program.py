from __future__ import annotations
from instruction import *

class Program:
    def __init__(self, instructions = None):
        if instructions is None:
            self.instructions: list[Instruction] = []
        else:
            self.instructions = instructions

    def __str__(self) -> str:
        strings = []
        for e in self.instructions:
            strings.append(e.__str__())
        return '['+ ', '.join(strings) + ']'

    @staticmethod
    def from_string(source: str) -> Program:
        lines = source.lower().replace("go to", "goto").splitlines()
        instructions: list[Instruction] = []
        for l in lines:
            instructions.append(Instruction.from_string(l))
        return Program(instructions)

    @staticmethod
    def from_file(path: str = 'prog.ram') -> Program:
        with open(path, "r") as program_file:
            return Program.from_string(program_file.read())
        
    # Mit Indexoperator kann direkt auf den n. Befehl zugegriffen werden
    def __getitem__(self, key) -> Instruction:
        return self.instructions[key]
    
    def size(self) -> int:
        return len(self.instructions)

    
