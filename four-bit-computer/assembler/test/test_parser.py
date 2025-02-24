import unittest
from scanner import Scanner
from parser import Parser
from instruction import Instruction
from token_type import TokenType

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


if __name__ == "__main__":
    unittest.main()