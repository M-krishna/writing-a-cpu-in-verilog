# Implementing RISC-V in Verilog
Hopefully I can finish this project. PLEASE GOD.

I'm taking help from Claude on what needs to be done and not the code part. I have to implement it from scratch and Icarus Verilog is my only friend for my program

Claude asks me to implement ALU first. Let me do that.


## RISC-V Standards
- To be Added


## What is Variable length instructions?
Variable-length instructions are computer instructions where different instructions can have different sizes (number of bytes). This contrasts with **fixed-length instructions**, where all instructions occupy the same amount of space.

Variable-length instructions are a characteristics of Complex-Instructions Set Computing (CISC) architectures like x86, while Reduced Instruction Set Computing (RISC) architectures typically use fixed-length instructions

## What is the difference between Instruction memory and Data memory?
Instruction memory: Holds the program's instruction (code)
Data memory: Stores the data that the program manipulates

## How can we fetch the current instruction using Program counter?
* Our program counter is 32-bits or 4-bytes.
```verilog
reg [31:0] program_counter;
```
* Our instruction memory is 4KB (1024 bytes) and each instruction is 32-bits wide or 4-bytes wide;
* This is how our *instruction memory* looks like:
```verilog
reg [31:0] instruction_memory [0:1023]; // 4KB in size
```
* At `instruction_memory[0]`, the first instruction would present.
* At `instruction_memory[1]`, the second instruction would present. And so on.
* Since we know that *instruction_memory* is index based (0, 1, 2, ...), we could do `instruction_memory[program_counter]`. Where the initial value of *program_counter* is 0 and at each clock cycle it *increments by 1*
* But to depict the real CPU working, we should do something different.
    * Instead of access the instruction memory as `instruction_memory[program_counter]`, we should do `instruction_memory[program_counter / 4]`.
    * Why divide by 4? In this case, we have 32-bits (ie. 4 bytes) of instruction memory.
    * Since the value of program counter is in bytes and the instruction memory is index based like 0, 1, 2, ... N.
    * We are dividing the value of program counter by 4, to get the instructions from instruction memory.


## How to increment the program counter to fetch the instruction from instruction memory?
For our RISC-V CPU, we have a program counter like: `reg [31:0] program_counter`. And we have an instruction memory like: `reg [31:0] instruction_memory [0:1024]`. In code:
```verilog
reg [31:0] program_counter;
reg [31:0] instruction_memory [0:1024]; // 1KB of instruction memory
```
Here each instructions are *32-bits* or *4-bytes*. Our program counter starts at 0, fetching the first instruction in the *instruction_memory*. Once the *decode and execute* stages are finished for the first instruction, we need to increment the program counter.

Previously I was under the impression that we should do `program_counter + 1`. This was wrong. Because since each of the instructions are 4-bytes long, we should increment the *program_counter* by *4 bytes* and not *1*.

So we should do `program_counter <= program_counter + 4`


## What are all the available instruction formats in RISC-V?
RISC-V has **6 main instruction formats**, each 32 bits wide but with different field layouts:

### 1. R-Type (Register-Register operations)
```
31    25 24  20 19  15 14  12 11   7 6     0
[funct7][  rs2 ][  rs1 ][funct3][  rd  ][opcode]
  7 bits  5 bits  5 bits  3 bits  5 bits  7 bits
```
**Used for**: ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU.

**Example:** `ADD x1, x2, x3` (x1 = x2 + x3)

### 2. I-Type (Immediate operations)
```
31           20 19  15 14  12 11   7 6     0
[   imm[11:0]  ][  rs1 ][funct3][  rd  ][opcode]
    12 bits      5 bits  3 bits  5 bits  7 bits
```
**Used for:** ADDI, ANDI, ORI, XORI, SLTI, SLTIU, loads (LWI, LB, etc.)

**Example:** `ADDI x1, x2, 100` (x1 = x2 + 100)

### 3. S-Type (Store operations)
```
31    25 24  20 19  15 14  12 11    7 6     0
[imm[11:5]][  rs2 ][  rs1 ][funct3][imm[4:0]][opcode]
  7 bits    5 bits  5 bits  3 bits  5 bits   7 bits
```
**Used for:** SW, SB, SH (store operations)

**Example:** `SW x2, 8(x1)` (store x2 to memory[x1 + 8])

### 4. B-Type (Branch Operations)
```
31  30    25 24  20 19  15 14  12 11  8 7  6     0
[imm[12]][imm[10:5]][rs2][rs1][funct3][imm[4:1]][imm[11]][opcode]
  1 bit    6 bits    5    5     3        4        1       7
```
**Used for:** BEQ, BNE, BLT, BGE, BLTU, BGEU

**Example:** `BEQ x1, x2, label` (if x1 == x2, jump to label)

### 5. U-Type (Upper Immediate)
```
31           12 11   7 6     0
[   imm[31:12] ][  rd  ][opcode]
    20 bits      5 bits  7 bits
```
**Used for:** LUI, AUIPC

**Example:** `LUI x1, 0x12345` (load upper immediate)

### 6. J-Type (Jump)
```
31  30      21 20 19      12 11   7 6     0
[imm[20]][imm[10:1]][imm[11]][imm[19:12]][rd][opcode]
  1 bit    10 bits   1 bit    8 bits    5   7 bits
```
**Used for:** JAL

**Example:** `JAL x1, function` (jump and link)