import re
from token_type import TokenType
from token_internal import Token
from typing import List, Optional
from instruction import Instruction, InstructionToken

class Parser:
    
    MNEMONICS = ["LOAD", "ADD", "SUB", "AND", "OR", "XOR", "JMP", "HLT"]

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_position: int = 0
        self.instructions = []
        self.location_counter: int = 0
        self.symbol_table: dict = {}
        self.instructions_token: List[InstructionToken] = [] # This is array of tuples. Tuple contains (location_counter, mnemonic, operand)

    def parse_tokens(self):
        while not self.is_at_end():
            self.parse_token_v3() # First pass
        self.second_pass()

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

    # This is the first pass of the assembler
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
                self.instructions_token.append((self.location_counter, mnemonic, operand))
                self.location_counter += 1
            elif self.isAlphaNumeric(operand):
                # here we are expecting an operand that doesn't end with a colon(:)
                self.instructions_token.append((self.location_counter, mnemonic, operand))
                self.location_counter += 1
        else:
            # It must be a Label, that ends with a colon(:)
            # Check whether it is a label or not.
            # If it's a label, then put it inside the symbol table
            if current_token.tt == TokenType.LABEL.name:
                label_name: str = current_token.lexeme.rstrip(":")
                if label_name in self.symbol_table:
                    raise SyntaxError(f"Duplicate label: {label_name} at line: {current_token.line}")
                # Assign current instruction address to label
                self.symbol_table[label_name] = self.location_counter

    # First pass
    def parse_token_v3(self):
        current_token: Token = self.advance()
        mnemonic_token = current_token
        if mnemonic_token.lexeme in self.MNEMONICS:
            operand_token: Token = self.advance()
            if self.isDigit(operand_token.lexeme):
                if int(operand_token.lexeme) not in [0, 1]:
                    raise SyntaxError(f"Unknown operand: {operand_token.lexeme} at line: {operand_token.line}")
                instruction_token: InstructionToken = InstructionToken(
                    self.location_counter, mnemonic_token, operand_token
                )
                self.instructions_token.append(instruction_token)
                self.location_counter += 1
            elif self.isAlphaNumeric(operand_token.lexeme):
                instruction_token: InstructionToken = InstructionToken(
                    self.location_counter, mnemonic_token, operand_token
                )
                self.instructions_token.append(instruction_token)
                self.location_counter += 1
        else:
            # Here we are dealing with labels
            if not (current_token.tt == TokenType.LABEL.name):
                raise SyntaxError(f"Unknow token type: {current_token} at line: {current_token.line}")
            label_name: str = current_token.lexeme.rstrip(":")
            if label_name in self.symbol_table:
                raise Exception(f"Duplicate label {label_name} found at line: {current_token.line}")
            self.symbol_table[label_name] = self.location_counter

    # Second pass of the assembler
    # This is where we resolve label instructions
    # Go through the instruction tokens and resolve the references
    def second_pass(self):
        for location_counter, mnemonic_token, operand_token in self.instructions_token:
            mnemonic = mnemonic_token.lexeme
            operand = None
            if operand_token:
                if operand_token.tt == TokenType.NUMBER.name:
                    operand = operand_token.lexeme
                elif operand_token.tt == TokenType.LABEL.name:
                    label_name: str = operand_token.lexeme
                    if label_name not in self.symbol_table:
                        raise SyntaxError(f"Undefined label: {label_name} at line: {operand_token.line}")
                    operand = self.symbol_table[label_name]
                else:
                    operand = operand_token.lexeme
            instruction: Instruction = Instruction(
                mnemonic, operand, location_counter
            )
            self.instructions.append(instruction)

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
