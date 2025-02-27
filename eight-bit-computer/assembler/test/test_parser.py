import unittest
from typing import List
from scanner import Scanner
from parser import Parser
from instruction import Instruction
from test.factory.instruction_factory import InstructionFactory


class TestParser(unittest.TestCase):
    def test_load(self):
        source = "LOAD R0, R1"

        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(scanner.get_tokens)
        parser.parse_tokens()

        expected_instruction: Instruction = InstructionFactory.create_instruction(
            "LOAD", "R0", "R1"
        )
        result_instructions: List[Instruction] = parser.get_instructions

        for _, instruction in enumerate(result_instructions):
            self.assertEqual(instruction.mnemonic, expected_instruction.mnemonic)
            self.assertEqual(instruction.operand_1.lexeme, expected_instruction.operand_1)
            self.assertEqual(instruction.operand_2.lexeme, expected_instruction.operand_2)
            self.assertEqual(instruction.address, expected_instruction.address)


    def test_hlt(self):
        source = "HLT"

        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(scanner.get_tokens)
        parser.parse_tokens()

    def test_load_with_numbers(self):
        source = "LOAD R0, 1"

        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(scanner.get_tokens)
        parser.parse_tokens()

    @unittest.skip
    def test_jmp(self):
        source = """
            JMP TEST_1

            TEST_1:
                LOAD R0, 1
                ADD R1, R0
                HLT
        """

        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(scanner.get_tokens)
        parser.parse_tokens()

if __name__ == "__main__":
    unittest.main()