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

        self.assertEqual(instructions[0].mnemonic, TokenType.LOAD.name)
        self.assertEqual(instructions[0].data, str(1))

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

        self.assertEqual(instructions[0].data, 1)
        self.assertEqual(instructions[0].mnemonic, TokenType.JMP.name)
        self.assertEqual(instructions[1].data, str(1))
        self.assertEqual(instructions[1].mnemonic, TokenType.LOAD.name)
        self.assertEqual(instructions[2].data, str(1))
        self.assertEqual(instructions[2].mnemonic, TokenType.ADD.name)
        self.assertEqual(instructions[3].data, str(0))
        self.assertEqual(instructions[3].mnemonic, TokenType.JMP.name)

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
        print(instructions)

if __name__ == "__main__":
    unittest.main()