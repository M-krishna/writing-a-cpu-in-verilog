from token_internal import Token
from typing import NamedTuple

class InstructionToken(NamedTuple):
    mnemonic        : Token
    operand_1       : Token
    operand_2       : Token
    location_counter:   int

class Instruction:
    def __init__(self,
                mnemonic: str,
                operand_1: str | Token = None,
                operand_2: str | Token = None,
                address: int = 0
                ):
        self.mnemonic = mnemonic
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.address = address

    def __repr__(self):
        return f"Instruction({self.mnemonic}, {self.operand_1}, {self.operand_2}, {self.address})"