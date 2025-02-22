import re
from token_type import TokenType
from token_internal import Token
from typing import List, Optional
from instruction import Instruction


class Parser:
    
    MNEMONICS = ["LOAD", "ADD", "SUB", "AND", "OR", "XOR", "JMP", "HLT"]

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_position: int = 0
        self.instructions = []
        self.location_counter: int = 0
        self.symbol_table: dict = {}

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

    def parse_token_v2(self):
        current_token: Token = self.advance()
        mnemonic: str = current_token.lexeme
        if mnemonic in self.MNEMONICS:
            # check the operand
            # an operand can be a number or an identifier(which is label)
            current_token: Token = self.advance()
            operand: str = current_token.lexeme
            if self.isDigit(operand):
                if int(operand) not in [0, 1]:
                    raise SyntaxError(f"Unknown operand: {operand} at line number: {current_token.line}")
            elif self.isAlphaNumeric(operand):
                # here we are expecting an operand that doesn't end with a colon(:)
                instruction: Instruction = Instruction(
                    mnemonic, operand, self.location_counter
                )
                self.instructions.append(instruction)
                self.location_counter += 1
        else:
            # It must be a Label, that ends with a colon(:)
            # Check whether it is a label or not.
            # If it's a label, then put it inside the symbol table
            if current_token.tt == TokenType.LABEL.name:
                label_name: str = current_token.lexeme.rstrip(":")
                if label_name in self.symbol_table:
                    raise SyntaxError(f"Duplicate label: ${label_name} at line: ${current_token.line}")
                # Assign current instruction address to label
                self.symbol_table[label_name] = self.location_counter

    ################ HELPER FUNCTIONS #############
    def isDigit(self, c: str) -> bool:
        return re.match(r"^[0-9]\d*$", c) is not None

    def isAlphaNumeric(self, c: str) -> bool:
        return re.match(r"^[a-zA-Z0-9_:]+$", c) is not None

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
