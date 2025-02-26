from enum import Enum


class TokenType(Enum):
    # Mnemonics
    LOAD    = "LOAD"
    ADD     = "ADD"
    SUB     = "SUB"
    AND     = "AND"
    OR      = "OR"
    XOR     = "XOR"
    JMP     = "JMP"
    HLT     = "HLT"

    # Others
    NUMBER      = "NUMBER"
    IDENTIFIER  = "IDENTIFIER"
    SEMICOLON   = "SEMICOLON"
    COLON       = "COLON"
    COMMA       = "COMMA"
    LABEL       = "LABEL"
    EOF         = "EOF"