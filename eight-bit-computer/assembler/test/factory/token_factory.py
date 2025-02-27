from token_internal import Token
from .token_builder import TokenBuilder


class TokenFactory:
    @staticmethod
    def create_token(tt: str, lexeme: str, line: int = 0, literal: object = None) -> Token:
        return (TokenBuilder()
                .set_token_type(tt)
                .set_lexeme(lexeme)
                .set_line(line)
                .set_literal(literal)
                .build()
                )