from __future__ import annotations
from enum import auto, StrEnum

from constants import *

class Operator(StrEnum):
    NONE = auto() # Keine Operation, leerer Befehl
    LOAD = auto()
    STORE = auto()
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    END = auto()
    GOTO = auto()
    IF_EQ = auto()
    IF_NE = auto()
    IF_LT = auto()
    IF_LE = auto()
    IF_GT = auto()
    IF_GE = auto()
    CLOAD = auto()
    CADD = auto()
    CSUB = auto()
    CMULT = auto()
    CDIV = auto()
    INDLOAD = auto()
    INDSTORE = auto()
    INDADD = auto()
    INDSUB = auto()
    INDMULT = auto()
    INDDIV = auto()

    @classmethod
    def from_string(cls, name):
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"'{name}' is no valid Operator")

# Alle Befehle, die aus einem Wort und einer Zahl bestehen
SIMPLE_INSTRUCTIONS = [
    'load',
    'store',
    'add',
    'sub',
    'mult',
    'div',
    'goto',
    'cload',
    'cadd',
    'csub',
    'cmult',
    'cdiv',
    'indload',
    'indstore',
    'indadd',
    'indsub',
    'indmult',
    'inddiv'
]

class InvalidOperand(Exception):
    pass

class InvalidOperator(Exception):
    pass

class InvalidSyntax(Exception):
    pass

def canonicalize(string: str) -> str:
    return string.lower().replace('\\s+', ' ').lstrip().rstrip()

class Instruction:
    def __init__(self, operator: Operator, operand: int):
        self.operator: Operator = operator
        self.operand = operand % Constants.REGISTER_LIMIT

    def __str__(self) -> str:
        op = self.operator
        match op:
            case Operator.END:
                return Operator.END.value
            case Operator.IF_EQ | Operator.IF_GE | Operator.IF_GT | Operator.IF_LE | Operator.IF_LT:
                comparator = ''
                match op:
                    case Operator.IF_EQ:
                        comparator = '='
                    case Operator.IF_NE:
                        comparator = '!='
                    case Operator.IF_LT:
                        comparator = '<'
                    case Operator.IF_LE:
                        comparator = '<='
                    case Operator.IF_GT:
                        comparator = '>'
                    case Operator.IF_GE: 
                        comparator = '>='
                return f'if {comparator} {str(self.operand)}'                   
            case _:
                return self.operator.replace('_', ' ') + ' ' + str(self.operand)
    
    @staticmethod
    def from_string(source: str) -> Instruction:
        # Kommentare ignorieren
        if source.startswith('#'):
            return Instruction(Operator.NONE, 0)
        
        parts = canonicalize(source).split(' ')
        operator = parts[0]
        part1 = ''
        part2 = ''
        try:
            part1 = parts[1]
        except IndexError:
            part1 = Operator.NONE
        try:
            part2 = parts[2]
        except IndexError:
            part2 = Operator.NONE
        match operator:
            case '':
                return Instruction(Operator.NONE, 0)
            case operator if operator in SIMPLE_INSTRUCTIONS:
                if len(parts) > 2:
                    raise InvalidSyntax(f'Instruction {operator} expects only one operand')
                operand = 0
                try:
                    operand = int(part1)
                except ValueError:
                    raise InvalidOperand(f'Operand {part1} is not an integer')
                return Instruction(Operator.from_string(operator), operand)
            case 'if':
                if len(parts) != 3:
                    raise InvalidSyntax(f'IF-Statements expect a comparator and a comparison value')
                operand = 0
                try:
                    operand = int(part2)
                except ValueError:
                    if part2 == Operator.NONE:
                        raise InvalidSyntax(f'IF-Statements expect a comparator and a comparison value')
                    raise InvalidOperand(f'Operand {part2} is not an integer')
                mode = part1
                match mode:
                    case '=':
                        return Instruction(Operator.IF_EQ, operand)
                    case '!=':
                        return Instruction(Operator.IF_NE, operand)
                    case '<':
                        return Instruction(Operator.IF_LT, operand)
                    case '<=':
                        return Instruction(Operator.IF_LE, operand)
                    case '>':
                        return Instruction(Operator.IF_GT, operand)
                    case '>=':
                        return Instruction(Operator.IF_GE, operand)
                    case _:
                        raise InvalidOperand(f'Comparator {part1} is invalid')
            case Operator.END:
                return Instruction(Operator.END, 0)
            case _:
                raise InvalidOperator(f'Operator {operator} is invalid')
