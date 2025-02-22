21st Feb 2025
---
colon(":") can't be a standalone token. It is part of the label identifier.

For example, 
```
JMP TEST_1
TEST_1:
    LOAD 1
    ADD 1
    JMP 0
```
Here `TEST_1:` should be parsed as a single token

22nd Feb 2025
---

### First pass and Second pass
In a two pass assembler, the assembler goes through the source code two times.

### Pass 1: Building the Symbol table
During the first pass, the assembler reads through the source code line by line to determine the address of each instruction and record the label (symbol names) with the addresses at which they occur. The key steps are:

1. Initialize the Location Counter (LC):
This counter starts at a predefined base address (often 0, unless overridden by an assembler directive). Each instruction occupies one "address unit" (or more if instructions are larger)

2. Scan each line:
* **If the line contains a label (for example, a token ending in a colon like `TEST_1`):** Record the label in the symbol table along with the value of the Location counter (LC)

* **If the line is an instruction (or a directive that generates code):** Associate the current location counter with that instruction and increment the location counter by the size of that instruction

* Ignore comments and whitespace

**Example:**
```
JMP TEST_1

TEST_1:
    LOAD 1
    ADD 1
    JMP 1
```

* **Line 1:** `JMP TEST_1`
    * This is an instruction at address 0 (LC = 0)
    * The operand `TEST_1` is a label that isn't defined yet.

* **Line 2:** `TEST_1:1`
    * This is a label definition. Record `TEST_1` in the symbol table with the current LC value. At this point, the LC is 1 (since we already place one instruction)

* **Line 3:** `LOAD 1`
    * This is an instruction at address 1(LC = 1) and increments LC to 2.

* **Line 4:** `ADD 1`
    * This is an instruction at address 2(LC = 2) and increments LC to 3.

* **Line 5:** `JMP 1`
    * This is an instruction at address 3(LC = 3) and increments LC to 4.

At the end of pass 1, the symbol table will look like:
```
TEST_1 -> 1
```

And the assembler now knows the address of the all instructions even if some operands (like the first `JMP TEST_1`) still reference labels

### Pass 2: Resolving Symbols and Generating Machine code
In the second pass, the assembler goes through the source code (or an intermediate representation created in pass 1) and translates each instruction to its final machine code. During this pass, whenever an instruction references a label (like in a jump), the assembler consults the symbol table to the get the actual address and substitutes the value in the machine code.

**Continuing the Example:**
* **Instruction at address 0:** `JMP TEST_1`
    * In pass 2, the assembler looks up `TEST_1` in the symbol table. It finds that `TEST_1` is at address 1
    * The machine code for `JMP TEST_1` is then generated with the operand replaced by 1

* **Instruction at address 1:** `LOAD 1`
    * This instruction is already has a numeric operand, so it's translated directly.

* **Instruction at address 2:** `ADD 1`
    * Likewise, translated directly.

* **Instruction at address 3:** `JMP 1`
    * Here, the operand is already a number (1), so it's translated directly.

The output might be a series of binary or hexadecimal codes where the jump instruction at address 0 now contains the number 1(the resolved address of TEST_1)