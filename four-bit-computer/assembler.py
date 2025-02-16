#!/usr/bin/env python3

from enum import Enum
from typing import List, Callable


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
    SEMICOLON   = "SEMICOLON"
    NUMBER      = "NUMBER"
    EOF         = "EOF"


class Token:
    def __init__(self, tt: TokenType, lexeme: str, literal: object = None):
        self.tt = tt
        self.lexeme = lexeme
        self.literal = literal

    def __repr__(self):
        return f"[Token type: {self.tt}, Lexeme: {self.lexeme}]"


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

    def scan_tokens(self):
        while not self.is_at_end():
            self.start_position = self.current_position
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, ""))

    def scan_token(self):
        c: str = self.advance()

        token_dict: dict = {
            ";": lambda: self.handle_semicolon()
        }

        try:
            fn: Callable = token_dict.get(c, lambda: self.default_case(c))
            fn()
        except:
            raise Exception(f"Unknown token: {c}")

    def add_token(self, token: Token):
        self.tokens.append(token)

    def handle_semicolon(self):
        while (self.peek() != "\n" and not self.is_at_end()):
            self.advance()

    def default_case(self, c: str):
        if self.isDigit(c):
            self.number()
        elif self.isAlpha(c):
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
            TokenType.NUMBER.name, text
        )
        self.add_token(token)

    def string(self):
        while (self.isAlpha(self.peek())):
            self.advance()
        text: str = self.source[self.start_position:self.current_position]
        token_type: TokenType = self.keywords.get(text)
        token: Token = Token(
            token_type, text
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
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')

    def match(self, expected_token: str) -> bool:
        if (self.peek() == expected_token): return True
        return False

    def advance(self) -> str:
        self.current_position += 1
        return self.source[self.current_position - 1]

    def peek(self) -> str:
        if self.is_at_end(): return "\0"
        return self.source[self.current_position]

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.source)

    @property
    def get_tokens(self) -> List[Token]:
        return self.tokens
    ############### END OF HELPER FUNCTIONS ###########


if __name__ == "__main__":

    with open("instructions.txt", "r") as f:
        source = f.read()

    scanner = Scanner(source)
    scanner.scan_tokens()
    print(scanner.get_tokens)