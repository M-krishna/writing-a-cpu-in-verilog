from instruction import Instruction
from token_internal import Token
from token_type import TokenType


class InstructionBuilder:
    def __init__(self):
        self.mnemonic: str          = None
        self.operand1: str | Token  = None
        self.operand2: str | Token  = None
        self.address: int           = 0

    def set_mnemonic(self, mnemonic: str) -> 'InstructionBuilder':
        self.mnemonic = mnemonic
        return self

    def set_operand1(self, operand1: str | Token) -> 'InstructionBuilder':
        self.operand1 = operand1
        return self

    def set_operand2(self, operand2: str | Token) -> 'InstructionBuilder':
        self.operand2 = operand2
        return self

    def set_address(self, address: int) -> 'InstructionBuilder':
        self.address = address
        return self

    def build(self) -> 'InstructionBuilder':
        # JMP instruction takes only one operand
        # HLT instruction doesn't take any operand
        required_fields = {
            "JMP": ["mnemonic", "operand1"],
            "HLT": ["mnemonic"],
            "default": ["mnemonic", "operand1", "operand2"]
        }
        instruction_type = self.mnemonic if self.mnemonic in required_fields else "default"
        for field in required_fields[instruction_type]:
            if not getattr(self, field):
                raise ValueError(f"{field} value must be set for {instruction_type} instruction")
        
        return Instruction(self.mnemonic, self.operand1, self.operand2, self.address)