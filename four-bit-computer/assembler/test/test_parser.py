import unittest
from scanner import Scanner
from parser import Parser
from instruction import Instruction
from token_type import TokenType
from typing import List

class TestParser(unittest.TestCase):
    
    def test_parse_load(self):
        source = "LOAD 1"
        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(tokens=scanner.get_tokens)
        parser.parse_tokens()
        instructions: Instruction = parser.get_instructions

        # (expected_mnemonic, expected_data)
        expected = [
            (TokenType.LOAD.name, str(1))
        ]

        self.assertEqual(len(instructions), len(expected), "Instruction count mismatch")

        for index, (expected_mnemonic, expected_operand) in enumerate(expected):
            with self.subTest(index):
                self.assertEqual(instructions[index].mnemonic, expected_mnemonic)
                self.assertEqual(instructions[index].data, expected_operand)


    def test_parse_label(self):
        source = """
            JMP TEST_1

            TEST_1:
                LOAD 1
                ADD 1
                JMP 0
        """
        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(tokens=scanner.get_tokens)
        parser.parse_tokens()

        instructions: List[Instruction] = parser.get_instructions

        # (expected_mnemonic, expected_operand)
        expected = [
            (TokenType.JMP.name, 1),
            (TokenType.LOAD.name, str(1)),
            (TokenType.ADD.name, str(1)),
            (TokenType.JMP.name, str(0))
        ]

        self.assertEqual(len(instructions), len(expected), "Instruction count mismatch")

        for index, (expected_mnemonic, expected_operand) in enumerate(expected):
            with self.subTest(index):
                self.assertEqual(instructions[index].mnemonic, expected_mnemonic)
                self.assertEqual(instructions[index].data, expected_operand)

    def test_multiple_labels(self):
        source = """
            JMP TEST_2

            TEST_1:
                LOAD 1
                ADD 1
                JMP 0

            TEST_2:
                LOAD 1
                ADD 1
                ADD 1
        """
        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(tokens=scanner.get_tokens)
        parser.parse_tokens()

        instructions: List[Instruction] = parser.get_instructions

        expected = [
            Instruction(TokenType.JMP.name, 4),
            Instruction(TokenType.LOAD.name, str(1)),
            Instruction(TokenType.ADD.name, str(1)),
            Instruction(TokenType.JMP.name, str(0)),
            Instruction(TokenType.LOAD.name, str(1)),
            Instruction(TokenType.ADD.name, str(1)),
            Instruction(TokenType.ADD.name, str(1))
        ]

        self.assertEqual(len(instructions), len(expected), "Instructions count mismatch")

        for index, expected_instruction in enumerate(expected):
            with self.subTest(index):
                self.assertEqual(instructions[index].mnemonic, expected_instruction.mnemonic)
                self.assertEqual(instructions[index].data, expected_instruction.data)

if __name__ == "__main__":
    unittest.main()