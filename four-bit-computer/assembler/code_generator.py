import os
from enum import Enum
from typing import List
from instruction import Instruction


class FileType(Enum):
    HEX_FILE    = "HEX_FILE"
    BINARY_FILE = "BIN_FILE"


class CodeGenerator:

    
    # File data
    OUTPUT_DIR      = "output"
    OUTPUT_HEX_FILE = f"{OUTPUT_DIR}/instructions.hex"
    OUTPUT_BIN_FILE = f"{OUTPUT_DIR}/instructions.bin"

    opcodes: dict = {
        "LOAD"  : "000",
        "ADD"   : "001",
        "SUB"   : "010",
        "AND"   : "011",
        "OR"    : "100",
        "XOR"   : "101",
        "JMP"   : "110",
        "HLT"   : "111"
    }

    def __init__(self, instructions: List[Instruction]):
        self.instructions   = instructions
        self.binary_code    = []
        self.hex_code       = []

    def generate_binary_code(self):
        for instruction in self.instructions:
            binary_code = self.opcodes.get(instruction.mnemonic) + str(instruction.data)
            self.binary_code.append(binary_code)

    def generate_hex_code(self):
        for instruction in self.instructions:
            opcode = int(self.opcodes.get(instruction.mnemonic), 2)
            data = int(instruction.data)

            hex_code = (opcode << 1) | (data & 1)
            hex_instruction = "{:x}".format(hex_code)
            self.hex_code.append(hex_instruction)

    def write_to_file(self, file_type: FileType):
        instructions: str = self.binary_code if file_type.value == "BIN_FILE" else self.hex_code
        file: str = self.OUTPUT_BIN_FILE if file_type.value == "BIN_FILE" else self.OUTPUT_HEX_FILE

        with open(file, "w") as f:
            for instruction in instructions:
                f.write(str(instruction) + "\n")
