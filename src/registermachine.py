from __future__ import annotations
from program import *
from typing import Callable

class Registermachine:
    def __init__(self):
        self.instruction_set: dict[Operator, Callable[[Registermachine, int]]] = {}
        self.program = Program()
        self.programcounter: int = 0
        self.memory = bytearray(16) # 1 Byte je Register, 16 Register insgesamt
        self.should_continue = True

    def __str__(self) -> str:
        return f'Program: {self.program}\nBefehlszähler: {self.programcounter}\nSpeicher: {self.memory}\n'

    def register(self, operator: Operator, func: Callable[[Registermachine, int]]) -> Registermachine:
        self.instruction_set[operator] = func
        return self
    
    def clear_memory(self) -> Registermachine:
        self.memory.clear()
        return self
    
    def run(self, program: Program) -> Registermachine:
        # Maschine kann extern beendet werden oder durch einen internen Befehl
        while self.should_continue:
            # Aktuellen Befehl erhalten
            instruction = self.program[self.programcounter]
            # Zugehoeriges Lambda ausfuehren
            self.instruction_set[instruction.operator](self, instruction.operand)
            # Befehlszaehler inkrementieren
            self.programcounter += 1
        return self
