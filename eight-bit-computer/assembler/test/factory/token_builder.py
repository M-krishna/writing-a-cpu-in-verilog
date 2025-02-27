from token_internal import Token


class TokenBuilder:
    def __init__(self):
        self.__tt = None
        self.__lexeme = None
        self.__line = 0
        self.__literal = None

    def set_token_type(self, tt: str) -> 'TokenBuilder':
        self.__tt = tt
        return self

    def set_lexeme(self, lexeme: str) -> 'TokenBuilder':
        self.__lexeme = lexeme
        return self
    
    def set_line(self, line: int) -> 'TokenBuilder':
        self.__line = line
        return self
    
    def set_literal(self, literal: object) -> 'TokenBuilder':
        self.__literal = literal
        return self

    def build(self) -> Token:
        if self.__tt is None or self.__lexeme is None:
            raise ValueError("Token type and lexeme must be set")
        return Token(self.__tt, self.__lexeme, self.__line, self.__literal)