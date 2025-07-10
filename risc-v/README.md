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
* **Instruction memory:** Holds the program's instruction (code)
* **Data memory:** Stores the data that the program manipulates

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

## RISC-V Instruction Bit Fields
All RISC_V instructions are 32 bits, numbered from 31(MSB) to 0 (LSB):

```
Bit Position: 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
```

### Common Fields Across All Formats:

* Opcode [6:0] - Always bits 6-0
```verilog
wire [6:0] opcode = current_instruction[6:0];
```

* rd[11:7] - Destination register (when present)
```verilog
wire [4:0] rd = current_instruction[11:7];
```

* funct3[14:12] - Function field (when present)
```verilog
wire [2:0] funct3 = current_instruction[14:12];
```

* rs1[19:15] - Source register 1 (when present)
```verilog
wire [4:0] rs1 = current_instruction[19:15];
```

* rs2[24:20] - Source register 2 (when present)
```verilog
wire [4:0] rs2 = current_instruction[24:20];
```

* funct7[31:25] - Function field for R-type
```verilog
wire [6:0] funct7 = current_instruction[31:25];
```

### Format-Specific Immediate Fields:
* I-Type Immediate [31:20]
```verilog
wire [11:0] imm_i = current_instruction[31:20];
```

* S-Type Immediate (split across two locations)
```verilog
wire [11:0] imm_s = {current_instruction[31:25], current_instruction[11:7]};
```

* B-Type Immediate (split and reordered)
```verilog
wire [12:0] imm_b = {current_instruction[31], current_instruction[7], current_instruction[30:25], current_instruction[11:8], 1'b0};
```

* U-Type Immediate [31:12]
```verilog
wire [19:0] imm_u = current_instruction[31:12];
```

* J-Type Immediate (split and reordered)
```verilog
wire [20:0] imm_j = {current_instruction[31], current_instruction[19:12], current_instruction[20], current_instruction[30:21], 1'b0};
```


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

## What are Register Files?
The **register file** is a small, fast memory inside the CPU that stores temporary data during instruction execution. Think of it as the CPU's workspace.

### RISC-V Register File Specifications:
* **32 registers** total (x0 through x31)
* Each register is **32 bits wide** (for RV32I)
* **x0 is special** - always contains 0 (hardwired)
* **x1-x31** can store any 32-bit value

### Why do we need it?
**Example:** `ADD x1, x2, x3` (x1 = x2 + x3)

1. **Read** x2 and x3 from register file
2. **Send** those value to ALU
3. **Get** result from ALU
4. **Write** result back to x1 in register file

### How should we decide how many bits are needed to address registers?
* Let's say we have a registers array like this: `reg [31:0] registers [0:31]`, since we are building RISC-V CPU, we should have 2 read registers and 1 write register.
* To fetch the correct register from the registers array, how many do we need for the read and write registers?
* To calculate that, we can use the formula: `Number of bits = log(number of register) base 2`
* In our case, we have 32 registers. So the number of bits = 5

## Data signals and Control signals
These are fundamental concepts in digital design.

### Data Signals
**Data signals** carry the actual information (number, addresses, etc.) between components.

**In our Register file context**:
* **Read data:** What values comes OUT of the registers when you read them.
* **Write data:** What value goes INTO a register when you write to it.

**Examples:**
* `read_data1` - the 32 bit value from first register
* `read_data2` - the 32 bit value from second register
* `write_data` - the 32 bit value you want to store

### Control Signals
**Control signals** tell components WHEN and HOW to operate. They're like switches or commands.

**In our Register file context:**
* **Write Enable:** "Should I actually write, or just ignore the write inputs?"
* **Clock:** "When should writing happen?"
* **Reset:** "Should I clear registers?"

**Examples:**
* `write_enable` - 1 bit signal (1 = write, 0 = don't write)
* `clk` - clock signal for timing
* `reset` - 1 bit signal to clear everything

### Why do we Need Both?
**Data Without Control = Chaos**:
* You provide `write_data`, but WHEN should it be written?
* Without `write_enable`, it might write constantly!

**Real Example:**
```verilog
// Data signals
write_data = 43;            // What to write
write_addr = 5;             // where to write

// Control signals
write_enable = 1;           // whether to write
// On clock edge            // when to write
```

## Combinational Logic and Sequential Logic (in terms of registers)
* **Combinational logic** (`always @(*)`) = immediate response, use `=`
* **Sequential logic** (`always @(posedge clk)`) = wait for clock, use `<=`
* **Register writes** are typically sequential in real CPUs

## Signal Direction: Who Controls the Signal?
* This is basically to understand which component drives the signal (like `wire` and `reg`).
* Let's say we have a module like:
```verilog
module register_file(
    input [4:0] read_addr1,
    input [4:0] read_addr2,
    input [4:0] write_addr,
    input [31:0] write_data,
    input write_enable,
    input clk,
    output [31:0] read_data1,
    output [31:0] read_data2
);
endmodule
```
* In the above code, the inputs and outputs mentioned are `wire` signal by default.
* And we write a testbench to test the above module. In the testbench, we need to define the signals correctly for the module to get the correct data from the testbench. Here is how it looks:
```verilog
module register_file_tb;
    reg [4:0] read_addr1;
    reg [4:0] read_addr2;
    reg [4:0] write_addr;
    reg [31:0] write_data;
    reg write_enable;
    reg clk;
    wire [31:0] read_data1;
    wire [31:0] read_data2;
endmodule
```
* Why `clk`, `read_addr`, `read_addr2`, `write_addr`, `write_data`, `write_enable` is defined as `reg` signal type and `read_data1` and `read_data2` are defined as `wire` signal type? Lets look at that:
    * Why `reg` signal type for `clk` and other mentioned ones?
        * **Testbench generates** the clock signal
        * **Testbench drives** `clk` into the module
        * In testbench, **you control** when `clk` changes
        * `reg` = "I (testbench) am driving the signal"
    * Why `wire` signal type for `read_data1` and `read_data2`?
        * **Register file module outputs** these signals
        * **Module drives** the data to testbench
        * **Testbench receives** the data (doesn't control it)
        * `wire` = "The module is driving this signal to me"

### Signal Direction Rule:
| Signal Type | Direction | Testbench Declaration |
|-------------|-----------|-----------------------|
| Inputs to module | Testbench -> Module | `reg` |
| Outputs from module | Module -> Testbench | `wire` |

**Think of it like:**
* `reg` = "I have a remote control for this"
* `wire` = "I'm just watching what comes out"

## What is a Control Logic?
Control logic is the "brain" of a CPU that decides what each component should do based on the current instruction.

Control logic generates **control signals** that tell different parts of the CPU how to operate. Think of it as the conductor of an orchestra - it coordinates all the components to work together.

### In our CPU context
**Control logic takes:**
* **opcode** (what type of instruction?)
* **funct3/funct7** (specific operation details)

**Control Logic Generates**:
* **ALU operation code** (`alu_op`)
* **Write enable** (`write_enable`)
* **Multiplexer select signals**
* **Data path control signals**

### In our current code:
Our `always @(*)` block in `cpu.v` is where our control logic will live. It needs to:
* Look at the opcode
* Decide what each component should do
* Generate the appropriate control signals

## OP_IMM Instruction overview
`OP_IMM` (0010011) includes:
* **ADDI** - ADD immediate
* **ANDI** - AND immdiate
* **ORI** - OR immediate
* **XORI** - XOR immediate
* **SLTI** - Set less than immediate
* **SLTIU** - Set less than immediate unsigned

### For OP_IMM, What should the Control Logic do?
1. Extract the immediate value first:
We need to get the 12-bit immediate from bits [31:20]:
```verilog
reg [11:0] imm_i = current_instruction[31:20];
```
2. Control signals for OP_IMM:
Think about what each signal should be:
* `write_enable`: should OP_IMM write to a register?
* `alu_src` - should ALU use `rs2_data` or immediate
* `reg_write_src`: What data should go to register file's write_data?
* `alu_op` - How do you tell ALU which operation to perform
3. ALU Operation Selection:
For OP_IMM, the specific operation depends on `funct3`:
* `funct3 = 000` -> ADDI (ADD)
* `funct3 = 001` -> ANDI (AND)
* `funct3 = 010` -> ORI (OR)
* `funct3 = 100` -> XORI (XOR)
* etc.

### Questions to guide our implementation
1. For `ADDI x1, x2, 100`:
  * What should `write_enable` be?
  * What should go into ALU's A input? (rs1_data or rs2_data)
  * What should go into ALU's B input? (rs2_data or immediate)
  * What should `write_data` in register file be?
2. How do you extract and sign-extend the immediate?
  * 12-bit immediate needs to become 32-bit
  * Should negative immediates work correctly?
3. How do you pass the right operation to ALU?
  * Your ALU probably has operation codes like ADD, AND, OR
  * How do you map `funct3` to your ALU's operation codes?

09-07-2025
---
Man I don't understand shit on how to implement functionality for `OP_IMM`. I think I need to take one step at a time. What needs to be done? But first what is `OP_IMM`?

`OP_IMM` stands for operation immediate, its part of instruction encoding, where we get the immediate value from the instruction.

## Things I have done so far
Logging my journey here.

### 04-07-2025
* Implemented the base cpu module with the following
    * Created a program counter
    * Created an instruction memory
    * Fetching the instruction from instruction memory
    * Updating the program counter synchronously
    * Decode the instruction (Asynchronously)

### 05-07-2025
* Implemented Register files (register_file.v)

### 10-07-2025
* Finished implementing `OP_IMM` functionality