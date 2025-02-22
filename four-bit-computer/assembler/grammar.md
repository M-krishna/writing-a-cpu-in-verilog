# Grammar for the Assembler of 4-bit CPU

```
<instruction> ::= <mnemonic> <operand>

<mnemonic> ::= "LOAD" | "ADD" | "SUB" | "AND" | "OR" | "XOR" | "JMP" | "HLT"

<operand> ::= (any numbers ranging from 0 to 9 | <label:>)

<label:> ::= IDENTIFIER
```