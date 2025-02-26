from typing import List, Callable
from token_type import TokenType
from token_internal import Token


class Scanner:

    KEYWORDS: dict = {
        "LOAD": TokenType.LOAD.name,
        "ADD": TokenType.ADD.name,
        "SUB": TokenType.SUB.name,
        "AND": TokenType.AND.name,
        "OR": TokenType.OR.name,
        "XOR": TokenType.XOR.name,
        "JMP": TokenType.JMP.name,
        "HLT": TokenType.HLT.name
    }

    def __init__(self, source: str):
        self.source: str = source
        self.start_position: int = 0
        self.current_position: int = 0
        self.tokens: List[Token] = []
        self.line: int = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start_position = self.current_position
            self.scan_token()
        self.add_token(Token(TokenType.EOF.name, "", self.line + 1))

    def scan_token(self):
        c: str = self.advance()

        token_dict: dict = {
            ";": lambda: self.handle_semicolon(),
            ",": lambda: self.handle_comma()
        }

        try:
            fn: Callable = token_dict.get(c, lambda: self.default_case(c))
            fn()
        except:
            raise Exception(f"Unknown token/character {c}")

    def add_token(self, token: Token):
        self.tokens.append(token)

    def handle_semicolon(self):
        # This function is to ignore the comment in the code.
        while (self.peek() != "\n" and not self.is_at_end()):
            self.advance()

    def handle_comma(self):
        c: str = self.advance()
        text: str = self.source[self.start_position:self.current_position]
        token: Token = Token(
            TokenType.COMMA.name, text, self.line
        )
        self.add_token(token)

    def default_case(self, c: str):
        if self.isDigit(c):
            self.number()
        elif self.isWhiteSpace(c):
            pass
        elif self.isAlpha(c):
            self.string()
        else:
            raise SyntaxError(f"Invalid character: {c}")

    def number(self):
        while (self.isDigit(self.peek())):
            self.advance()
        text: str = self.source[self.start_position:self.current_position]
        token: Token = Token(
            TokenType.NUMBER.name, text, self.line
        )
        self.add_token(token)

    def string(self):
        while (self.isAlphaNumeric(self.peek())):
            self.advance()
        text: str = self.source[self.start_position:self.current_position]
        # check if a keyword
        keyword: str = self.KEYWORDS.get(text, None)
        if not keyword: # then it must be an identifier
            self.handle_identifier()
        else:
            token: Token = Token(
                keyword, text, self.line
            )
            self.add_token(token)

    def handle_identifier(self):
        text: str = self.source[self.start_position:self.current_position]
        token: Token = Token(
            TokenType.IDENTIFIER.name, text, self.line
        )
        self.add_token(token)

    #################### HELPER FUNCTIONS #####################
    def isWhiteSpace(self, c: str) -> bool:
        WHITESPACE: str = " "
        TABSPACE: str = "\t"
        NEWLINE: str = "\n"
        return c in [WHITESPACE, TABSPACE, NEWLINE]

    def isDigit(self, c: str) -> bool:
        return (c >= '0') and (c <= '9')

    def isAlpha(self, c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == "_")

    def isAlphaNumeric(self, c: str) -> bool:
        return self.isDigit(c) or self.isAlpha(c)

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current_position]

    def advance(self) -> str:
        character: str = self.source[self.current_position]
        self.current_position += 1
        if character == "\n": self.line += 1
        return character

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.source)

    @property
    def get_tokens(self) -> List[Token]:
        return self.tokens
    #################### END OF HELPER FUNCTIONS ##############