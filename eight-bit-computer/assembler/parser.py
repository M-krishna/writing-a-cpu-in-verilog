from typing import List, Optional, Tuple
from token_internal import Token
from token_type import TokenType
from instruction import Instruction


class Parser:

    MNEMONICS = ["LOAD", "ADD", "SUB", "AND", "OR", "XOR", "JMP", "HLT"]
    REGISTERS = ["R0", "R1"]

    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.current_position: int = 0
        self.instructions: List[Instruction] = []

    def parse_tokens(self):
        while not self.is_at_end():
            instruction: Instruction = self.parse_instruction()
            self.instructions.append(instruction)

    def parse_instruction(self) -> Instruction:
        mnemonic: str = self.parse_mnemonic()

        # For instructions that don't need operand (for eg. HLT)
        # return early
        if mnemonic == TokenType.HLT.name:
            return Instruction(mnemonic)
        else:
            op1, op2 = self.parse_operands()
            return Instruction(mnemonic, op1, op2)

    def parse_mnemonic(self) -> str:
        token: Token = self.advance()
        if token.lexeme not in self.MNEMONICS:
            raise SyntaxError(f"Unknown mnemonic {token.lexeme} at line {token.line}")
        return token.lexeme

    def parse_operands(self) -> Tuple[Optional[Token], Optional[Token]]:
        # First operand: Destination register
        destination_token: Token = self.advance()
        if destination_token.lexeme not in self.REGISTERS:
            raise SyntaxError(f"Unknown destination {destination_token.lexeme} at line {destination_token.line}")

        comma: Token = self.advance()
        if comma.tt != TokenType.COMMA.name:
            raise SyntaxError(f"Expected ',' at line {comma.line} but got {comma.lexeme}")

        # Second operand: could be a register or an immediate value
        source_token: Token = self.advance()
        if source_token.lexeme in self.REGISTERS:
            return (destination_token, source_token)
        elif self.isNumber(source_token.lexeme):
            return (destination_token, source_token)
        else:
            raise SyntaxError(f"Unknown operand {source_token.lexeme} at line {source_token.line}")

    ############### HELPER METHODS ###############
    def isNumber(self, operand: str) -> bool:
        try:
            num: int = int(operand)
            return 0 <= num <= 15
        except:
            return False

    def peek(self) -> Optional[Token]:
        if not self.is_at_end():
            return self.tokens[self.current_position]
        return None

    def advance(self) -> Token:
        current_token: Token = self.tokens[self.current_position]
        self.current_position += 1
        return current_token

    def is_at_end(self) -> bool:
        return (self.current_position >= len(self.tokens)) or (self.tokens[self.current_position].tt == TokenType.EOF.name)

    @property
    def get_instructions(self) -> List[Instruction]:
        return self.instructions
    ############### END OF HELPER METHODS ########