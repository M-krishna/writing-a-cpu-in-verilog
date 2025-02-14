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
            while (self.isDigit(self.peek())):
                self.advance()
            number: str = self.source[self.start_position:self.current_position]
            self.generate_and_add_token(TokenType.NUMBER.name, literal=number)
        elif self.isWhiteSpace(c):
            pass # Ignore whitespace
        elif self.isAlpha(c):
            while (self.isAlpha(self.peek())):
                self.advance()
            text: str = self.source[self.start_position:self.current_position]
            token_type: TokenType = self.keywords.get(text)
            self.generate_and_add_token(token_type, literal=text)
        else:
            print(f"Invalid character: {c}")

    ######### HELPER METHODS ###########
    def advance(self) -> str:
        self.current_position += 1
        return self.source[self.current_position - 1]

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current_position]

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
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')

    @property
    def get_tokens(self) -> List[Token]:
        return self.tokens
    ######### END OF HELPER METHODS ####


class Instruction:
    def __init__(self, mnemonic, operand):
        self.mnemonic = mnemonic
        self.operand = operand

    def __repr__(self):
        return f"Instruction({self.mnemonic}, {self.operand})"
class Parser:

    MNEMONICS: List[str] = ["LOAD", "ADD", "SUB", "STORE"]

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_position = 0
        self.instructions: List[Instruction] = []


    def parse(self):
        while not self.isEnd():
            instruction: Instruction = self.parse_instructions()
            self.instructions.append(instruction)

    def parse_instructions(self) -> Instruction:
        current_token: Token = self.advance()

        if current_token.tt not in self.MNEMONICS:
            raise Exception(f"Syntax error: Unknown token: {current_token}")

        mnemonic: Token = current_token.lexeme.upper()

        # After the mnemonic, it should be number
        operand_token = self.advance()
        operand = int(operand_token.lexeme)
        if operand not in [0, 1]:
            raise SyntaxError(f"Unknown operand: {operand} for mnemonic: {mnemonic}")
        
        return Instruction(mnemonic, operand)

    ########### HELPER METHODS #############
    def peek(self) -> Optional[Token]:
        if not self.isEnd():
            return self.tokens[self.current_position]
        return None

    def advance(self) -> Token:
        current_token = self.peek()
        if current_token:
            self.current_position += 1
            return current_token
        raise Exception("Reached end of tokens")

    def isEnd(self) -> bool:
        return (self.current_position >= len(self.tokens)) or (self.tokens[self.current_position].tt == TokenType.EOF.name)

    @property
    def get_instructions(self) -> List[Instruction]:
        return self.instructions
    ########### END OF HELPER METHODS ######

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

    parser = Parser(scanner.get_tokens)
    parser.parse()
    print(parser.get_instructions)