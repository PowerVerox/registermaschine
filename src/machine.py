from __future__ import annotations
from program import *
from typing import Callable

def nbool_to_int(boolean: bool):
        if boolean:
            return 0
        else:
            return 1
        
class MachineRuntimeError(Exception):
    pass

class Machine:
    def __init__(self):
        self.instruction_set: dict[Operator, Callable[[Machine, int], Machine]] = {}
        self.instruction_set[Operator.NONE] = lambda m, v: m
        self.instruction_set[Operator.END] = lambda m, v: m.end()
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
    
    def set_pc(self, value: int) -> Machine:
        if value < 0:
            raise MachineRuntimeError('Programcounter is non-negative')
        self.programcounter = value
        return self
    
    def inc_pc(self, value: int) -> Machine:
        self.programcounter += value
        return self
    
    def out(self, value: int) -> Machine:
        print(f'Out: {value}')
        return self
    
    def run_program(self, program: Program) -> Machine:
        self.program = program
        # Maschine kann extern beendet werden oder durch einen internen Befehl
        while self.should_continue and self.programcounter < self.program.size():
            # Aktuellen Befehl erhalten
            instruction = self.program[self.programcounter]
            # Zugehoeriges Lambda ausfuehren
            try:
                self.instruction_set[instruction.operator](self, instruction.operand)
            except KeyError:
                raise MachineRuntimeError(f'Instruction {instruction.operator} is undefined')
            # TODO: Die Lambdas koennen Fehler erzeugen (invalider Speicherzugriff u.a)
            # Befehlszaehler inkrementieren
            self.programcounter += 1
        return self
    
    def run_file(self, path: str = 'prog.ram') -> Machine:
        return self.run_program(Program.from_file(path))

    def run_code(self, code: str) -> Machine:
        return self.run_program(Program.from_string(code))

    def add_math(self) -> Machine:
        self.add_fn(Operator.LOAD, fn = (lambda m, i: m.set(0, m.get(i))))
        self.add_fn(Operator.STORE, fn = (lambda m, i: m.set(i, m.get(0))))
        self.add_fn(Operator.ADD, fn = (lambda m, i: m.set(0, m.get(0) + m.get(i))))
        self.add_fn(Operator.SUB, fn = (lambda m, i: m.set(0, m.get(0) - m.get(i))))
        self.add_fn(Operator.MULT, fn = (lambda m, i: m.set(0, m.get(0) * m.get(i))))
        self.add_fn(Operator.DIV, fn = (lambda m, i: m.set(0, m.get(0) / m.get(i))))
        return self
    
    def add_jumps(self) -> Machine:
        self.add_fn(Operator.GOTO, fn = (lambda m, i: m.set_pc(i-1)))
        self.add_fn(Operator.IF_EQ, fn = (lambda m, i: m.inc_pc(nbool_to_int(m.get(0) == i))))
        self.add_fn(Operator.IF_NE, fn = (lambda m, i: m.inc_pc(nbool_to_int(m.get(0) != i))))
        self.add_fn(Operator.IF_LT, fn = (lambda m, i: m.inc_pc(nbool_to_int(m.get(0) < i))))
        self.add_fn(Operator.IF_LE, fn = (lambda m, i: m.inc_pc(nbool_to_int(m.get(0) <= i))))
        self.add_fn(Operator.IF_GT, fn = (lambda m, i: m.inc_pc(nbool_to_int(m.get(0) > i))))
        self.add_fn(Operator.IF_GE, fn = (lambda m, i: m.inc_pc(nbool_to_int(m.get(0) >= i))))
        return self
    
    def add_constants(self) -> Machine:
        self.add_fn(Operator.CLOAD, fn = (lambda m, i: m.set(0, i)))
        self.add_fn(Operator.CADD, fn = (lambda m, i: m.set(0, m.get(0) + i)))
        self.add_fn(Operator.CSUB, fn = (lambda m, i: m.set(0, m.get(0) - i)))
        self.add_fn(Operator.CMULT, fn = (lambda m, i: m.set(0, m.get(0) * i)))
        self.add_fn(Operator.CDIV, fn = (lambda m, i: m.set(0, m.get(0) / i)))
        return self
    
    def add_indirections(self) -> Machine:
        self.add_fn(Operator.INDLOAD, fn = (lambda m, i: m.set(0, m.get(m.get(i)))))
        self.add_fn(Operator.INDSTORE, fn = (lambda m, i: m.set(m.get(i), m.get(0))))
        self.add_fn(Operator.INDADD, fn = (lambda m, i: m.set(0, m.get(0) + m.get(m.get(i)))))
        self.add_fn(Operator.INDSUB, fn = (lambda m, i: m.set(0, m.get(0) - m.get(m.get(i)))))
        self.add_fn(Operator.INDMULT, fn = (lambda m, i: m.set(0, m.get(0) * m.get(m.get(i)))))
        self.add_fn(Operator.INDDIV, fn = (lambda m, i: m.set(0, m.get(0) / m.get(m.get(i)))))
        return self
    
    def add_standard_instructions(self) -> Machine:
        return self.add_math().add_jumps().add_constants().add_indirections()
    
    def print(self) -> Machine:
        print(self)
        return self
    
