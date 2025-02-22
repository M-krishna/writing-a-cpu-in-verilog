from typing import NamedTuple
from token_internal import Token


class InstructionToken(NamedTuple):
    location_counter: int
    mnemonic: Token
    operand: Token

class Instruction:
    def __init__(self, mnemonic: str, data: str, address: int = 0):
        self.mnemonic = mnemonic
        self.data = data
        self.address = address

    def __repr__(self):
        return f"Instruction({self.mnemonic}, {self.data})"