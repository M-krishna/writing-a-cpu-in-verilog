#!/usr/bin/env python3

from enum import Enum
from typing import List, Callable, Optional


class TokenType(Enum):
    # KEYWORDS(MNEMONICS)
    LOAD    = "LOAD"
    ADD     = "ADD"
    SUB     = "SUB"
    AND     = "AND"
    OR      = "OR"
    XOR     = "XOR"
    JMP     = "JMP"
    HLT     = "HLT"

    # OTHERS
    NUMBER      = "NUMBER"
    SEMICOLON   = "SEMICOLON"
    UNDERSCORE  = "UNDERSCORE"
    COLON       = "COLON"
    EOF         = "EOF"


class Token:
    def __init__(self, tt: TokenType, lexeme: str, literal: object = None, line: int = 0):
        self.tt = tt
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"[Token type: {self.tt}, Lexeme: {self.lexeme}, Line: {self.line}]"


class Scanner:

    keywords: dict = {
        "LOAD"      : TokenType.LOAD.name,
        "ADD"       : TokenType.ADD.name,
        "SUB"       : TokenType.SUB.name,
        "AND"       : TokenType.AND.name,
        "OR"        : TokenType.OR.name,
        "XOR"       : TokenType.XOR.name,
        "JMP"       : TokenType.JMP.name,
        "HLT"       : TokenType.HLT.name
    }

    def __init__(self, source: str):
        self.source = source
        self.start_position = 0
        self.current_position = 0
        self.tokens: List[Token] = []
        self.line: int = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start_position = self.current_position
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF.name, "EOF", line=self.line + 1))

    def scan_token(self):
        c: str = self.advance()

        token_dict: dict = {
            ";": lambda: self.handle_semicolon(),
            ":": lambda: self.handle_colon()
        }

        try:
            fn: Callable = token_dict.get(c, lambda: self.default_case(c))
            fn()
        except:
            raise Exception(f"Unknown token: {c}")

    def add_token(self, token: Token):
        self.tokens.append(token)

    def handle_colon(self):
        text: str = self.source[self.start_position:self.current_position]
        token: Token = Token(
            TokenType.COLON.name,
            lexeme=text,
            line=self.line
        )
        self.add_token(token)

    def handle_semicolon(self):
        while (self.peek() != "\n" and not self.is_at_end()):
            self.advance()

    def default_case(self, c: str):
        if self.isDigit(c):
            self.number()
        elif self.isAlphaNumeric(c):
            self.string()
        elif self.isWhitespace(c):
            self.whitespace()
        else:
            raise SyntaxError(f"Invalid character: {c}")

    def number(self):
        while (self.isDigit(self.peek())):
            self.advance()
        text: str = self.source[self.start_position:self.current_position]
        token: Token = Token(
            TokenType.NUMBER.name, text, line=self.line
        )
        self.add_token(token)

    def string(self):
        while (self.isAlphaNumeric(self.peek())):
            self.advance()
        text: str = self.source[self.start_position:self.current_position]
        token_type: TokenType = self.keywords.get(text)
        token: Token = Token(
            token_type, text, line=self.line
        )
        self.add_token(token)

    def whitespace(self):
        while (self.isWhitespace(self.peek())):
            self.advance()

    ############### HELPER FUNCTIONS ##################
    def isWhitespace(self, c: str) -> bool:
        WHITESPACE      = " "
        TABSPACE        = "\t"
        NEWLINE         = "\n"

        return c in [WHITESPACE, TABSPACE, NEWLINE]

    def isDigit(self, c: str) -> bool:
        return c >= '0' and c <= '9'

    def isAlpha(self, c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == "_")

    def isAlphaNumeric(self, c: str) -> bool:
        return self.isDigit(c) or self.isAlpha(c)

    def advance(self) -> str:
        character = self.source[self.current_position]
        self.current_position += 1
        if character == "\n":
            self.line += 1
        return character

    def peek(self) -> str:
        if self.is_at_end(): return "\0"
        return self.source[self.current_position]

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.source)

    @property
    def get_tokens(self) -> List[Token]:
        return self.tokens
    ############### END OF HELPER FUNCTIONS ###########


class Instruction:
    def __init__(self, mnemonic: str, data: str):
        self.mnemonic = mnemonic
        self.data = data

    def __repr__(self):
        return f"Instruction({self.mnemonic}, {self.data})"

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


class CodeGenerator:

    class FileType(Enum):
        HEX_FILE    = "HEX_FILE"
        BINARY_FILE = "BIN_FILE"
    
    # File data
    INPUT_FILE      = "instructions.txt"
    OUTPUT_HEX_FILE = "instructions.hex"
    OUTPUT_BIN_FILE = "instructions.bin"

    opcodes: dict = {
        "LOAD"  : "000",
        "ADD"   : "001",
        "SUB"   : "010",
        "AND"   : "011",
        "OR"    : "100",
        "XOR"   : "101",
        "JMP"   : "110",
        "HLT"   : "111"
    }

    def __init__(self, instructions: List[Instruction]):
        self.instructions   = instructions
        self.binary_code    = []
        self.hex_code       = []

    def generate_binary_code(self):
        for instruction in self.instructions:
            binary_code = self.opcodes.get(instruction.mnemonic) + str(instruction.data)
            self.binary_code.append(binary_code)
        self.write_to_file(self.FileType.BINARY_FILE)

    def generate_hex_code(self):
        for instruction in self.instructions:
            opcode = int(self.opcodes.get(instruction.mnemonic), 2)
            data = int(instruction.data)

            hex_code = (opcode << 1) | (data & 1)
            hex_instruction = "{:x}".format(hex_code)
            self.hex_code.append(hex_instruction)
        self.write_to_file(self.FileType.HEX_FILE)

    def write_to_file(self, file_type: FileType):
        instructions: str = self.binary_code if file_type.value == "BIN_FILE" else self.hex_code
        file: str = self.OUTPUT_BIN_FILE if file_type.value == "BIN_FILE" else self.OUTPUT_HEX_FILE

        with open(file, "w") as f:
            for instruction in instructions:
                f.write(str(instruction) + "\n")

if __name__ == "__main__":

    with open("instructions.txt", "r") as f:
        source = f.read()

    scanner = Scanner(source)
    scanner.scan_tokens()

    parser = Parser(scanner.get_tokens)
    parser.parse_tokens()

    code_generator = CodeGenerator(parser.get_instructions)
    code_generator.generate_binary_code()
    code_generator.generate_hex_code()