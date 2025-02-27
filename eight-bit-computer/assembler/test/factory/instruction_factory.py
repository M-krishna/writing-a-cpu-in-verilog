from token_internal import Token
from .instruction_builder import InstructionBuilder


class InstructionFactory:
    @staticmethod
    def create_instruction(mnemonic: str,
                           operand1: str | Token = None,
                           operand2: str | Token = None,
                           address: int = 0 
                           ):
        return (InstructionBuilder()
                .set_mnemonic(mnemonic)
                .set_operand1(operand1)
                .set_operand2(operand2)
                .set_address(address)
                .build()
                )