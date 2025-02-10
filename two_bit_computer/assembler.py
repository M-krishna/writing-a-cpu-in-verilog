#!/usr/bin/env python3

# Simple Assembler for my 2-bit CPU

"""
Things needs to be done:
    * The instructions will be present in "instructions.txt" file
    * Read the contents of the "instructions.txt" file
    * Parse the instructions and generate binary or hexadecimal equivalent of those instructions
    * Save the converted ones in a "instructions.hex" file, if its a hexadecimal format
"""


"""
Current supported instructions
* LOAD == 0 -> loads the data into register A
* ADD  == 1 -> Adds the immediate value with value in register A and stores it in register A
"""

def assemble_instructions(line):
    striped_line = line.rstrip(";").split(" ")
    instruction = striped_line[0] # mnemonic
    data = int(striped_line[1]) # immediate value

    if instruction == "LOAD":
        opcode = 0
    elif instruction == "ADD":
        opcode = 1
    else:
        raise Exception(f"Unknown instruction: {instruction}")

    final_instruction = (opcode << 1) | (data & 1)
    return "{:x}".format(final_instruction)

def main():
    input_filename = "instructions.txt"
    output_filename = "instructions.hex"

    lines  = []
    with open(input_filename, "r") as f:
        lines = f.readlines()
    
    instructions = []
    for line in lines:
        assembled_instruction_hex = assemble_instructions(line.strip())
        if assembled_instruction_hex is not None:
            instructions.append(assembled_instruction_hex)

    with open(output_filename, "w") as f:
        for h in instructions:
            f.write(h + "\n")

if __name__ == "__main__":
    main()
