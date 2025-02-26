from typing import List, Optional
from token_internal import Token
from instruction import Instruction


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.current_position: int = 0
        self.instructions: List[Instruction] = []

    def parse_tokens(self):
        while not self.is_at_end():
            self.parse_token()

    def parse_token(self):
        current_token: Token = self.advance()


    ############### HELPER METHODS ###############
    def peek(self) -> Optional[Token]:
        if not self.is_at_end():
            return self.tokens[self.current_position]
        return None

    def advance(self) -> Token:
        current_token: Token = self.tokens[self.current_position]
        self.current_position += 1
        return current_token

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.tokens)
    ############### END OF HELPER METHODS ########