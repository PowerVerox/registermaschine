from __future__ import annotations
from program import *
from typing import Callable

class Machine:
    def __init__(self):
        self.instruction_set: dict[Operator, Callable[[Machine, int], Machine]] = {}
        self.program = Program()
        self.programcounter: int = 0
        self.memory = [0] * 16 # 4 Byte je Register, 16 Register insgesamt
        self.should_continue = True

    def __str__(self) -> str:
        return f'Program: {self.program}\nBefehlszähler: {self.programcounter}\nSpeicher: {self.memory}\n'

    def add_fn(self, operator: Operator, fn: Callable[[Machine, int], Machine]) -> Machine:
        self.instruction_set[operator] = fn
        return self
    
    def clear_memory(self) -> Machine:
        self.memory.clear()
        return self
    
    def set(self, index: int, value: int) -> Machine:
        self.memory[index] = value
        return self
    
    def get(self, index: int) -> int:
        return self.memory[index]
    
    def end(self) -> Machine:
        self.should_continue = False
        return self
    
    def run(self, program: Program) -> Machine:
        self.program = program
        # Maschine kann extern beendet werden oder durch einen internen Befehl
        while self.should_continue and self.programcounter < self.program.size():
            # Aktuellen Befehl erhalten
            instruction = self.program[self.programcounter]
            # Zugehoeriges Lambda ausfuehren
            self.instruction_set[instruction.operator](self, instruction.operand)
            # Befehlszaehler inkrementieren
            self.programcounter += 1
        return self
