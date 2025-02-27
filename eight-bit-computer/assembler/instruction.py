from token_internal import Token

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