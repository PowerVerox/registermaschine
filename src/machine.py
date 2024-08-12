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
        self.instruction_set[Operator.NONE] = lambda m, i: m
        self.instruction_set[Operator.END] = lambda m, i: m.end()
        self.program = Program()
        self.programcounter: int = 0
        self.memory = [0] * 16 # 4 Byte je Register, 16 Register insgesamt
        self.should_continue = True

    def end(self) -> Machine:
        self.should_continue = False
        return self

    def __str__(self) -> str:
        return f'Program: {self.program}\nBefehlszähler: {self.programcounter}\nSpeicher: {self.memory}\n'
    
    def clear_memory(self) -> Machine:
        self.memory.clear()
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
    
    def instruction(self):
        def decorator(function: Callable[[Machine, int], Machine]):
            try:
                operator = Operator.from_string(function.__name__)
            except ValueError as e:
                print(f'Error trying to register instruction {function.__name__}: {e}')
                return function
            
            self.instruction_set[operator] = function
            return function
        
        return decorator
    
    def add_math(self) -> Machine:
        @self.instruction()
        def load(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[i]
            return m
    
        @self.instruction()
        def store(m: Machine, i: int) -> Machine:
            m.memory[i] = m.memory[0]
            return m
    
        @self.instruction()
        def add(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] + m.memory[i]
            return m
    
        @self.instruction()
        def sub(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] - m.memory[i]
            return m
    
        @self.instruction()
        def mult(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] * m.memory[i]
            return m
    
        @self.instruction()
        def div(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] / m.memory[i]
            return m
        
        return self
    
    def add_constants(self) -> Machine:
        @self.instruction()
        def cload(m: Machine, i: int) -> Machine:
            m.memory[0] = i
            return m
    
        @self.instruction()
        def cadd(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] + i
            return m
    
        @self.instruction()
        def csub(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] - i
            return m
    
        @self.instruction()
        def cmult(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] * i
            return m
    
        @self.instruction()
        def cdiv(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] / i
            return m
        
        return self
    
    def add_indirections(self) -> Machine:
        @self.instruction()
        def indload(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[m.memory[i]]
            return m
    
        @self.instruction()
        def indstore(m: Machine, i: int) -> Machine:
            m.memory[m.memory[i]] = m.memory[0]
            return m
    
        @self.instruction()
        def indadd(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] + m.memory[m.memory[i]]
            return m
    
        @self.instruction()
        def indsub(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] - m.memory[m.memory[i]]
            return m
    
        @self.instruction()
        def indmult(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] * m.memory[m.memory[i]]
            return m
    
        @self.instruction()
        def inddiv(m: Machine, i: int) -> Machine:
            m.memory[0] = m.memory[0] / m.memory[m.memory[i]]
            return m
        
        return self
    
    def add_jumps(self) -> Machine:
        @self.instruction()
        def goto(m: Machine, i: int) -> Machine:
            m.programcounter = i - 1
            return m
        
        @self.instruction()
        def if_eq(m: Machine, i: int) -> Machine:
            if not m.memory[0] == i:
                m.programcounter += 1
            return m
        
        @self.instruction()
        def if_ne(m: Machine, i: int) -> Machine:
            if not m.memory[0] != i:
                m.programcounter += 1
            return m
        
        @self.instruction()
        def if_lt(m: Machine, i: int) -> Machine:
            if not m.memory[0] < i:
                m.programcounter += 1
            return m
        
        @self.instruction()
        def if_le(m: Machine, i: int) -> Machine:
            if not m.memory[0] <= i:
                m.programcounter += 1
            return m
        
        @self.instruction()
        def if_gt(m: Machine, i: int) -> Machine:
            if not m.memory[0] > i:
                m.programcounter += 1
            return m
        
        @self.instruction()
        def if_ge(m: Machine, i: int) -> Machine:
            if not m.memory[0] >= i:
                m.programcounter += 1
            return m
        
        return self
    
    def add_standard_instructions(self) -> Machine:
        return self.add_math().add_jumps().add_constants().add_indirections()
    
    def print(self) -> Machine:
        print(self)
        return self
