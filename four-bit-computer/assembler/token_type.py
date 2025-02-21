from enum import Enum

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

    # LABEL
    LABEL   = "LABEL"

    # OTHERS
    NUMBER      = "NUMBER"
    SEMICOLON   = "SEMICOLON"
    UNDERSCORE  = "UNDERSCORE"
    COLON       = "COLON"
    EOF         = "EOF"