from enum import auto, StrEnum
from result import Result, Ok, Err
from typing import Self

class Operator(StrEnum):
    NONE = auto() # No operation, empty statement
    LOAD = auto()
    STORE = auto()
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    END = auto()
    GO_TO = auto()
    IF_EQ = auto()
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



class Instruction:
    def __init__(self, operator: Operator, operand: int):
        self.operator: Operator = operator
        self.operand = operand

    def __str__(self) -> str:
        op = self.operator
        match op:
            case Operator.END:
                return Operator.END.value
            case Operator.IF_EQ | Operator.IF_GE | Operator.IF_GT | Operator.IF_LE | Operator.IF_LT:
                comparator = '<ERROR>' #TODO find ich bisschen komisch, vllt ueberarbeiten
                match op:
                    case Operator.IF_EQ:
                        comparator = '='
                    case Operator.IF_LT:
                        comparator = '<'
                    case Operator.IF_LE:
                        comparator = '<='
                    case Operator.IF_GT:
                        comparator = '>'
                    case Operator.IF_GE: 
                        comparator = '>='
                return f'IF {comparator} {str(self.operand)}'                   
            case _:
                return self.operator.replace('_', ' ') + ' ' + str(self.operand)
    
    def from_string(source: str) -> Result[Self, str]:
        #split source
        parts = source.split(' ')
        operator = parts[0].lower()
        part1 = ''
        part2 = ''
        try:
            part1 = parts[1].lower()
        except IndexError:
            part1 = Operator.NONE
        try:
            part2 = parts[2].lower()
        except IndexError:
            part2 = Operator.NONE
        match operator:
            case '':
                return Ok(Instruction(Operator.NONE, 0))
            case operator if operator in Operator:
                operand = 0
                try:
                    operand = int(part1)
                except ValueError:
                    return Err(f'Operand {part1} is not an integer')
                return Ok(Instruction(operator, operand))
            case 'GO':
                if part1 == 'TO':
                    operand = 0
                    try:
                        operand = int(part2)
                    except ValueError:
                        return Err(f'Operand {part2} is not an integer')
                    return Ok(Instruction(Operator.GO_TO, operand))
                return Err('Expected TO after GO')
            case 'GOTO':
                operand = 0
                try:
                    operand = int(part1)
                except ValueError:
                    return Err(f'Operand {part1} is not an integer')
                return Ok(Instruction(Operator.GO_TO, operand))
            case 'IF':
                operand = 0
                try:
                    operand = int(part2)
                except ValueError:
                    if part2 == Operator.NONE:
                        return Err(f'IF-Statements expect a comparator and a comparison value')
                    return Err(f'Operand {part2} is not an integer')
                mode = part1
                match mode:
                    case '=':
                        return Ok(Instruction(Operator.IF_EQ, operand))
                    case '<':
                        return Ok(Instruction(Operator.IF_LT, operand))
                    case '<=':
                        return Ok(Instruction(Operator.IF_LE, operand))
                    case '>':
                        return Ok(Instruction(Operator.IF_GT, operand))
                    case '>=':
                        return Ok(Instruction(Operator.IF_GE, operand))
                    case _:
                        return Err(f'Comparator {part1} is invalid')
            case Operator.END:
                return Ok(Instruction(Operator.END, 0))
            case _:
                return Err(f'Operator {operator} is invalid')