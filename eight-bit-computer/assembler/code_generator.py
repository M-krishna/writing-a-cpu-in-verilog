from typing import List, Tuple
from instruction import Instruction

"""
Instruction Set Architecture

Memory bits:    0000 0000   -> 8 bits

* First 3 bits starting from MSB is used for Opcode
* The next bit is used to choose between registers.
    * We have two registers R0 & R1
    * If the bit is 0, then pick R0. If the bit is 1, then pick R1
    * The next four bits is used for immediate value (4 bits == Max value of 15)
"""

class CodeGenerator:

    OPCODES: dict = {
        "LOAD": "000",
        "ADD": "001",
        "SUB": "010",
        "AND": "011",
        "OR": "100",
        "XOR": "101",
        "JMP": "110",
        "HLT": "111"
    }

    REGISTERS: dict = {
        "R0": 0,
        "R1": 1
    }

    MIN_VALUE: int = 0
    MAX_VALUE: int = 15

    def __init__(self, instructions: List[Instruction]):
        self.instructions: List[Instruction] = instructions
        self.binary_code = []
        self.hex_code = []

    def generate_binary_code(self):
        for instruction in self.instructions:
            mnemonic, operand_1, operand_2, address = self.destruct_instruction(instruction)
            opcode = None
            mode = None
            op_field = None

            if mnemonic not in ["JMP", "HLT"]:
                opcode = self.OPCODES.get(mnemonic)
                mode = self.REGISTERS.get(operand_1)
                # The last 4 bits can be either a register value or immediate value
                # If its a number, convert it to binary (4 bits)
                # If its a register, convert it to binary (4 bits)
                is_register = self.is_register(operand_2) # for JMP and HLT instructions, this will be None
                if is_register:
                    op_field = format(self.REGISTERS.get(operand_2), '04b')
                else:
                    # Its an immediate value
                    # We should restrict it to 4 bits
                    if (int(operand_2) < self.MIN_VALUE) and (int(operand_2) > self.MAX_VALUE):
                        raise ValueError(f"The value of immediate should be between {self.MIN_VALUE} and {self.MAX_VALUE}")
                    op_field = format(int(operand_2), '04b')
            elif mnemonic == "JMP":
                opcode = self.OPCODES.get(mnemonic)
                mode = 0
                op_field = format(operand_1, "04b")
            else:
                # It must be HLT instruction
                opcode = self.OPCODES.get(mnemonic)
                mode = 0
                op_field = format(0, '04b')
            
            binary_code = str(opcode) + str(mode) + str(op_field)
            self.binary_code.append(binary_code)
    
    def is_register(self, operand_2) -> bool:
        return operand_2 in self.REGISTERS

    def destruct_instruction(self, instruction: Instruction) -> Tuple[str, str, str, int]:
        mnemonic = instruction.mnemonic
        operand_1 = instruction.operand_1
        operand_2 = instruction.operand_2
        address = instruction.address
        return (mnemonic, operand_1, operand_2, address)
        
    def generate_hex_code(self):
        if self.is_binary_code_empty(): self.generate_binary_code()
        for bin_code in self.binary_code:
            self.hex_code.append(format(int(str(bin_code), 2), 'x'))

    def is_binary_code_empty(self) -> bool:
        return len(self.binary_code) > 0

    def get_binary_instructions(self):
        return self.binary_code

    def get_hex_instructions(self):
        return self.hex_code