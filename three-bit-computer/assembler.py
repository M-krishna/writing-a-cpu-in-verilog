#!/usr/bin/env python3

# Simple Assembler for 3-bit CPU


from enum import Enum
from typing import List, Optional, Callable

class Assembler:
    INPUT_FILE = "instructions.txt"
    OUTPUT_FILE = "instructions.hex"

    def __init__(self):
        self.file_contents = []
        self.hex_instruction_format = []

    def read(self):
        with open(self.INPUT_FILE, "r") as f:
            self.file_contents = f.readlines()
        self.assemble_instructions()

    def assemble_instructions(self):
        for c in self.file_contents:
            striped_line = c.strip().rstrip(";")
            instruction = striped_line.split(" ")

            mnemonic = instruction[0]
            data = int(instruction[1])

            if mnemonic == "LOAD":
                opcode = 0b00
            elif mnemonic == "ADD":
                opcode = 0b01
            elif mnemonic == "SUB":
                opcode = 0b10
            elif mnemonic == "STORE":
                opcode = 0b11;
            else:
                raise Exception(f"Unknown mnemonic: {mnemonic}")

            hex_instruction = (opcode << 1) | (data & 1)
            self.hex_instruction_format.append(str(hex_instruction))
        self.write()

    def write(self):
        with open(self.OUTPUT_FILE, "w") as f:
            for i in self.hex_instruction_format:
                f.write(i + "\n")


class TokenType(Enum):
    
    # MNEMONICS (KEYWORDS)
    LOAD  = "LOAD"
    ADD   = "ADD"
    SUB   = "SUB"
    STORE = "STORE"

    NUMBER = "NUMBER"

    # OTHERS
    NEW_LINE    = "NEW_LINE"
    SLASH       = "SLASH"
    SEMICOLON   = "SEMICOLON"
    EOF         = "EOF"


class Token:
    def __init__(self, tt: TokenType, lexeme: str, literal: object, line: int = 0):
        self.tt = tt
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"[Token type: {self.tt}, Lexeme: {self.lexeme}]"


class Scanner:

    # Assembly keywords
    keywords: object = {
        "LOAD"  : TokenType.LOAD.name,
        "ADD"   : TokenType.ADD.name,
        "SUB"   : TokenType.SUB.name,
        "STORE" : TokenType.STORE.name
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start_position = 0
        self.current_position = 0

    def scan_tokens(self):
        while not self.is_at_end():
            self.start_position = self.current_position
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF.name, "", None)) # This helps in parsing the tokens
    
    def scan_token(self):
        c: str = self.advance()

        switch_dict: object = {
            ";": lambda: self.handle_semicolon()
        }

        try:
            fn: Callable = switch_dict.get(c, lambda: self.default_case(c))
            fn()
        except Exception:
            raise SyntaxError(f"Something went wrong")
    
    def generate_and_add_token(self, token_type: TokenType, literal: object = None):
        text: str = self.source[self.start_position:self.current_position]
        token = Token(
            tt=token_type,
            lexeme=text,
            literal=literal
        )
        self.tokens.append(token)

    def handle_semicolon(self):
        while (self.peek() != "\n" and not self.is_at_end()):
            self.advance()

    def default_case(self, c: str):
        if self.isDigit(c):
            pass
        elif self.isWhiteSpace(c):
            pass # Ignore whitespace
        elif self.isAlpha(c):
            pass
        else:
            print(f"Invalid character: {c}")

    ######### HELPER METHODS ###########
    def advance(self) -> str:
        self.current_position += 1
        return self.source[self.current_position - 1]

    def peek(self) -> Optional[str]:
        if not self.is_at_end():
            return self.source[self.current_position]
        return None

    def match(self, expected_token: str) -> bool:
        if self.is_at_end(): return False
        if (self.source[self.current_position] != expected_token): return False

        # consume the token and return True
        self.current_position += 1
        return True

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.source)

    def isDigit(self, c: str) -> bool:
        return c >= '0' and c <= '9'

    def isWhiteSpace(self, c: str) -> bool:
        SPACE       = " "
        TABSPACE    = "\t"
        NEWLINE     = "\n"

        return c in [SPACE, TABSPACE, NEWLINE]

    def isAlpha(self, c: str) -> bool:
        pass

    @property
    def get_tokens(self) -> List[Token]:
        return self.tokens
    ######### END OF HELPER METHODS ####


if __name__ == "__main__":
    """
    assembler = Assembler()
    assembler.read()
    """
    with open("instructions.txt", "r") as f:
        contents = f.read()
    
    scanner = Scanner(source=contents)
    scanner.scan_tokens()
    print(scanner.get_tokens)