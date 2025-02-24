# Notes for 8-bit CPU
Overview of the 8-bit cpu

### Instruction memory format
* `0000 0000 => 8 bits`
* The first 3 bits starting MSB is used for opcode, which gives us 7 unique instructions
* The next 5 bits are used for data (immediate value)
* The total number of instructions it can hold is 256 (0 to 255) and each of the instruction is 8 bits


### Register file
For the initial implementation, we will not have a separate register file. Instead we will follow an accumulator based approach