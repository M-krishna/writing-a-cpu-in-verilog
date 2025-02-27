from token_type import TokenType


class Token:
    def __init__(self, tt: TokenType, lexeme: str, line: int = 0, literal: object = None):
        self.tt = tt
        self.lexeme = lexeme
        self.line = line
        self.literal = literal

    def __repr__(self):
        return f"[Token type: {self.tt}, Lexeme: {self.lexeme}, Line: {self.line}]"