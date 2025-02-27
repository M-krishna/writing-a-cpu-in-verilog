# Notes for 8-bit CPU
Overview of the 8-bit cpu

### Instruction memory format
* `0000 0000 => 8 bits`
* The first 3 bits starting MSB is used for opcode, which gives us 7 unique instructions
* The next 5 bits are used for data (immediate value)
* The total number of instructions it can hold is 256 (0 to 255) and each of the instruction is 8 bits


### Register file
For the initial implementation, we will not have a separate register file. Instead we will follow an accumulator based approach

### Update on our CPU instruction encoding/decoding
Initially I planned to have only one register (register A) which acts as an accumulator. While writing the assembler I was thinking of adding more stuffs into my custom assembly language. Things like `.text`, `.bss`, `.data` and so on.

And to make the laguage more flexible I was thinking adding `CALL/RET` like feature. Due to this fact, I needed one more register.

### Complications with adding one more register.
The problem with adding one more register is that, we have to change the way how we encode and decode instructions.

Earlier we had:
* Bit 7 to 5 for opcode
* And the rest of bits for immediate value

After adding one more register:
* Bit 7 to 5 for opcode
* Bit 4 decides whether the operand of an instruction is either an immediate value or a register
    * If the value of the 4th bit is 0, then the bits 3 to 0 are considered as an immediate value
    * If the value of the 4th bit is 1, then this selects the register
        * If the 4 bits (3 to 0) is 0, then we select register 1 (r1)
        * If the 4 bits (3 to 0) is 1, then we select register 2 (r2)

Hope this is clear enough.


### What if?
**What if we add support to our assembly lannguage like `LOAD r1, 1`???**
* We'll stick with having two registers r1 and r2
* We can use one bit to choose between r1 and r2
* We'll have remaining 4 bits which we can use for immediate value

**For example:**
* If this is our instruction memory => `0000 0000` (8 bits in total)
* We'll use the first 3 bits starting from MSB for opcode
* The next bit, will be used to choose between registers
    * If its 0, then choose r0
    * If its 1, then choose r1
* The next 4 bits will be used for immediate value

Let me try to implement the above. This would require a significant change is our Assembler, but thats okay.

### What is a Register file?
A register file is a small memory structure within a CPU that contains a set of registers. Rather than having each register implemented with its own dedicated wiring for each operation, a register file organizes multiple registers in an array-like structure.

This allows the CPU to use decoders and multiplexers to select which register to read from or write to based on an encoded register identifier.

### Grammar for our 8-bit CPU Assembly
```
<program> ::= { <line> }

<line> ::= <instruction> | <label> | <comment> | <empty>

<instruction> ::= <mnemonic> [ <operand_list> ]

<mnemonic> ::= "LOAD" | "ADD" | "SUB" | "AND" | "OR" | "XOR" | "JMP" | "HLT"

<operand_list> ::= <operand> { "," <operand> }

<operand> ::= <immediate_value> | <register>

<immediate_value> ::= <number> (a number between 0 and 15)

<register> ::= "R0" | "R1"

<label> ::= <identifier> ":"

<comment> ::= ";" <any_text>

<empty_line> ::= /* empty line */

<identifier> ::= <letter> { <letter> | <digit> | "_" }
<letter> ::= "A" | ... | "Z" | "a" | ... | "z"
<digit> ::= "0" | "1" | ... | "9"

<number> ::= <digit> { <digit> }
```