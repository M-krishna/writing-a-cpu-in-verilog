#!/usr/bin/env python3

# Simple Assembler for 3-bit CPU

class Assembler:
    INPUT_FILE = "instructions.txt"
    OUTPUT_FILE = "instructions.hex"

    def __init__(self):
        self.file_contents = []
        self.hex_instruction_format = []

    def read(self):
        with open(self.INPUT_FILE, "r") as f:
            self.file_contents = f.readlines()
        self.assemble_instructions()

    def assemble_instructions(self):
        for c in self.file_contents:
            striped_line = c.strip().rstrip(";")
            instruction = striped_line.split(" ")

            mnemonic = instruction[0]
            data = int(instruction[1])

            if mnemonic == "LOAD":
                opcode = 0b00
            elif mnemonic == "ADD":
                opcode = 0b01
            elif mnemonic == "SUB":
                opcode = 0b10
            elif mnemonic == "STORE":
                opcode = 0b11;
            else:
                raise Exception(f"Unknown mnemonic: {mnemonic}")

            hex_instruction = (opcode << 1) | (data & 1)
            self.hex_instruction_format.append(str(hex_instruction))
        self.write()

    def write(self):
        with open(self.OUTPUT_FILE, "w") as f:
            for i in self.hex_instruction_format:
                f.write(i + "\n")


if __name__ == "__main__":
    assembler = Assembler()
    assembler.read()