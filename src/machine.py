# registermaschine - A simple register machine simulator
# Copyright (C) 2024  Tim Ernst, Vincent A. Hey

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import annotations
from decimal import DivisionByZero
from program import *
from constants import *
from typing import Callable
from data_manager import DataManager
        
class MachineRuntimeError(Exception):
    pass

class Machine:
    def __init__(self, data_manager: DataManager):
        # Befehlssatz besteht aus einem Dictionary, welches Operatoren auf Funktionen abbildet,
        # die eine Maschine und einen ganzzahligen Operanden entgegennehmen und eine Maschine zurueckgeben
        self.instruction_set: dict[Operator, Callable[[Machine, int], Machine]] = {}
        self.instruction_set[Operator.NONE] = lambda m, i: m
        self.instruction_set[Operator.END] = self.end
        self.program = Program()

        self.data_manager = data_manager
        self.data_manager.program_counter.set(1)
        self.memory = [0] * Constants.REGISTER_COUNT
        for i in range(Constants.REGISTER_COUNT):
            self.data_manager.registers[i].set('0')

    @staticmethod # Statisch, damit die Signatur passt
    def end(m: Machine, _: int) -> Machine:
        m.set_programcounter(m.program.size()+1)
        return m
    
    def set_programcounter(self, value: int) -> Machine:
        self.data_manager.program_counter.set(value)
        return self
    
    def change_programcounter(self, amount: int) -> Machine:
        self.data_manager.program_counter.set(self.data_manager.program_counter.get() + amount)
        return self
    
    def get_programcounter(self) -> int:
        return self.data_manager.program_counter.get()
    
    # Indexoperator fuer Register
    # Macht die Instruktionen s.u. "cleaner" und hat eine Indexpreufung und Wertebereichsbeschraenkung auf 0-Constants.REGISTER_LIMIT-1 (0-255)
    def __setitem__(self, index: int, value: int) -> Machine:
        if index < 0 or index >= len(self.memory):
            raise MachineRuntimeError(f'Invalid register index {index}. Must be between 0 and {len(self.memory)-1}')
        self.memory[index] = value % Constants.REGISTER_LIMIT
        self.data_manager.registers[index].set(str(self.memory[index]))
        return self

    def __getitem__(self, index: int) -> int:
        if index < 0 or index >= len(self.memory):
            raise MachineRuntimeError(f'Invalid register index {index}. Must be between 0 and {len(self.memory)-1}')
        return self.memory[index]

    def __str__(self) -> str:
        return f'Program: {self.program}\nBefehlszähler: {self.get_programcounter()}\nSpeicher: {self.memory}\n'
    
    def clear_memory(self) -> Machine:
        self.memory = [0] * Constants.REGISTER_COUNT
        for i in range(Constants.REGISTER_COUNT):
            self.data_manager.registers[i].set('0')
        return self
    
    def step(self) -> Machine:
        if self.get_programcounter() <= self.program.size() and self.program[self.get_programcounter() - 1].operator != Operator.END:
            # Aktuellen Befehl erhalten
            instruction = self.program[self.get_programcounter() - 1]
            # Zugehoeriges Lambda ausfuehren
            try:
                self.instruction_set[instruction.operator](self, instruction.operand)
            except KeyError:
                # Tritt auf, wenn ein Befehl nicht definiert ist
                raise MachineRuntimeError(f'Instruction {instruction.operator} is undefined')
            except DivisionByZero:
                # Kann durch die Divisionsinstruktionen auftreten
                raise MachineRuntimeError('Division by zero')
            except Exception as e:
                # Alle anderen Fehler werden weitergegeben
                raise MachineRuntimeError(f'An error occured: {e}')
            # Befehlszaehler inkrementieren
            self.change_programcounter(1)
        return self
    
    def run_program(self, program: Program) -> Machine:
        self.program = program
        while self.get_programcounter() <= self.program.size() and self.program[self.get_programcounter() - 1].operator != Operator.END:
            self.step()
        return self
    
    def run_file(self, path: str = 'prog.ram') -> Machine:
        return self.run_program(Program.from_file(path))

    def run_code(self, code: str) -> Machine:
        return self.run_program(Program.from_string(code))
    
    # Decorator, um Befehle zu registrieren
    # Der Name der Python-Funktion wird als Operator interpretiert
    # und die Python-Funktion wird im Befehlssatz abgelegt
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
    
    # 'Mathematische' Befehle hinzufuegen
    def add_math(self) -> Machine:
        @self.instruction()
        def load(m: Machine, i: int) -> Machine:
            m[0] = m[i]
            return m
    
        @self.instruction()
        def store(m: Machine, i: int) -> Machine:
            m[i] = m[0]
            return m
    
        @self.instruction()
        def add(m: Machine, i: int) -> Machine:
            m[0] = m[0] + m[i]
            return m
    
        @self.instruction()
        def sub(m: Machine, i: int) -> Machine:
            m[0] = m[0] - m[i]
            return m
    
        @self.instruction()
        def mult(m: Machine, i: int) -> Machine:
            m[0] = m[0] * m[i]
            return m
    
        @self.instruction()
        def div(m: Machine, i: int) -> Machine:
            m[0] = m[0] // m[i]
            return m
        
        return self
    
    # Konstanten
    def add_constants(self) -> Machine:
        @self.instruction()
        def cload(m: Machine, i: int) -> Machine:
            m[0] = i
            return m
    
        @self.instruction()
        def cadd(m: Machine, i: int) -> Machine:
            m[0] = m[0] + i
            return m
    
        @self.instruction()
        def csub(m: Machine, i: int) -> Machine:
            m[0] = m[0] - i
            return m
    
        @self.instruction()
        def cmult(m: Machine, i: int) -> Machine:
            m[0] = m[0] * i
            return m
    
        @self.instruction()
        def cdiv(m: Machine, i: int) -> Machine:
            m[0] = m[0] // i
            return m
        
        return self
    
    # Indirekte Adressierung
    def add_indirections(self) -> Machine:
        @self.instruction()
        def indload(m: Machine, i: int) -> Machine:
            m[0] = m[m[i]]
            return m
    
        @self.instruction()
        def indstore(m: Machine, i: int) -> Machine:
            m[m[i]] = m[0]
            return m
    
        @self.instruction()
        def indadd(m: Machine, i: int) -> Machine:
            m[0] = m[0] + m[m[i]]
            return m
    
        @self.instruction()
        def indsub(m: Machine, i: int) -> Machine:
            m[0] = m[0] - m[m[i]]
            return m
    
        @self.instruction()
        def indmult(m: Machine, i: int) -> Machine:
            m[0] = m[0] * m[m[i]]
            return m
    
        @self.instruction()
        def inddiv(m: Machine, i: int) -> Machine:
            m[0] = m[0] // m[m[i]]
            return m
        
        return self
    
    # Sprungbefehle
    def add_jumps(self) -> Machine:
        @self.instruction()
        def goto(m: Machine, i: int) -> Machine:
            m.set_programcounter(i-1)
            return m
        
        @self.instruction()
        def if_eq(m: Machine, i: int) -> Machine:
            if not m[0] == i:
                m.change_programcounter(1)
            return m
        
        @self.instruction()
        def if_ne(m: Machine, i: int) -> Machine:
            if not m[0] != i:
                m.change_programcounter(1)
            return m
        
        @self.instruction()
        def if_lt(m: Machine, i: int) -> Machine:
            if not m[0] < i:
                m.change_programcounter(1)
            return m
        
        @self.instruction()
        def if_le(m: Machine, i: int) -> Machine:
            if not m[0] <= i:
                m.change_programcounter(1)
            return m
        
        @self.instruction()
        def if_gt(m: Machine, i: int) -> Machine:
            if not m[0] > i:
                m.change_programcounter(1)
            return m
        
        @self.instruction()
        def if_ge(m: Machine, i: int) -> Machine:
            if not m[0] >= i:
                m.change_programcounter(1)
            return m
        
        return self
    
    # Alles zusammen
    def add_standard_instructions(self) -> Machine:
        return self.add_math().add_jumps().add_constants().add_indirections()
    
    # Nur ein nicer Befehl zum Debuggen
    def print(self) -> Machine:
        print(self)
        return self
