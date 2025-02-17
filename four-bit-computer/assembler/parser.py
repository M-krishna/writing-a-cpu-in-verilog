from token_type import TokenType
from token_internal import Token
from typing import List, Optional
from instruction import Instruction


class Parser:
    
    MNEMONICS = ["LOAD", "ADD", "SUB", "AND", "OR", "XOR", "JMP", "HLT"]

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_position = 0
        self.instructions = []

    def parse_tokens(self):
        while not self.is_at_end():
            instruction: Instruction = self.parse_token()
            self.instructions.append(instruction)

    def parse_token(self) -> Instruction:
        current_token: Token = self.advance()
        mnemonic: str = current_token.lexeme
        if mnemonic not in self.MNEMONICS:
            raise SyntaxError(f"Unknown mnemonic: {mnemonic} at line number: {current_token.line}")

        # Right after the mnemonic we should have a number (data)
        current_token: Token = self.advance()
        operand: int = int(current_token.lexeme)

        if operand not in [0, 1]:
            raise SyntaxError(f"Unknown operand: {operand} at line number: {current_token.line}")

        return Instruction(mnemonic, operand)

    ################ HELPER FUNCTIONS #############
    def advance(self) -> Optional[Token]:
        current_token: Token = self.peek()
        if current_token:
            self.current_position += 1
            return current_token
        raise Exception("Reached end of tokens")

    def peek(self) -> Optional[Token]:
        if not self.is_at_end(): return self.tokens[self.current_position]
        return None

    def is_at_end(self) -> bool:
        return (self.current_position >= len(self.tokens)) or (self.tokens[self.current_position].tt == TokenType.EOF.name)

    @property
    def get_instructions(self) -> List[Instruction]:
        return self.instructions
    ################ END OF HELPER FUNCTIONS ######
