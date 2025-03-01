from typing import List, Optional, Tuple
from token_internal import Token
from token_type import TokenType
from instruction import Instruction, InstructionToken


class Parser:

    MNEMONICS = ["LOAD", "ADD", "SUB", "AND", "OR", "XOR", "JMP", "HLT"]
    REGISTERS = ["R0", "R1"]

    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.current_position: int = 0
        self.instructions: List[Instruction] = []
        self.location_counter: int = 0
        self.symbol_table: dict = {}
        self.instruction_token: List[InstructionToken] = []

    def parse_tokens(self):
        self.first_pass()
        self.second_pass()
        # while not self.is_at_end():
        #     instruction: Instruction = self.parse_instruction()
        #     self.instructions.append(instruction)

    def parse_instruction(self) -> InstructionToken:
        mnemonic: Token = self.parse_mnemonic()

        # For instructions that don't need operand (for eg. HLT)
        # return early
        if mnemonic.lexeme == TokenType.HLT.name:
            return self.add_instruction_token(mnemonic, location_counter=self.location_counter)
        elif mnemonic.lexeme == TokenType.JMP.name:
            op1 = self.parse_jmp_operand()
            return self.add_instruction_token(mnemonic, op1, location_counter=self.location_counter)
        else:
            op1, op2 = self.parse_operands()
            return self.add_instruction_token(mnemonic, op1, op2, location_counter=self.location_counter)

    def add_instruction(self, mnemonic: str, op1: Token = None, op2: Token = None) -> Instruction:
        return Instruction(
            mnemonic, op1, op2
        )
    
    def add_instruction_token(self, mnemonic: Token, op1: Token = None, op2: Token = None, location_counter: int = 0) -> InstructionToken:
        return InstructionToken(
            mnemonic=mnemonic, location_counter=location_counter,
            operand_1=op1, operand_2=op2
        )

    def parse_mnemonic(self) -> Token:
        token: Token = self.advance()
        if token.lexeme not in self.MNEMONICS:
            raise SyntaxError(f"Unknown mnemonic {token.lexeme} at line {token.line}")
        return token

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

    def parse_jmp_operand(self) -> Token:
        # the operand value of the JMP instruction can be any of the two
        # It can be a label reference or
        # It can be a direct address
        # So we have to handle two cases
        # The token type can either IDENTIFIER or NUMBER
        operand_token: Token = self.advance()
        if (operand_token.tt != TokenType.IDENTIFIER.name) and (operand_token.tt != TokenType.NUMBER.name):
            raise SyntaxError(f"Unknown operand type: {operand_token.tt} for JMP instruction at line {operand_token.line}")
        return operand_token

    def first_pass(self):
        while not self.is_at_end():
            current_token: Token = self.peek()
            # Check if its a LABEL token.
            if current_token.tt == TokenType.LABEL.name and current_token.lexeme.endswith(":"):
                label_name: str = current_token.lexeme.rstrip(":")
                if label_name in self.symbol_table:
                    raise SyntaxError(f"Duplicate label: {label_name} at line {current_token.line}")
                self.symbol_table[label_name] = self.location_counter
                self.advance() # consume the token
            else:
                # Otherwise this should be an instruction
                instruction_token: InstructionToken = self.parse_instruction()
                self.instruction_token.append(instruction_token)
                self.location_counter += 1

    def second_pass(self):
        for mnemonic, operand_1, operand_2, location_counter in self.instruction_token:
            print(mnemonic, operand_1, operand_2, location_counter)

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