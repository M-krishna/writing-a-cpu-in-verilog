import unittest
from scanner import Scanner
from parser import Parser
from code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def test_simple_instruction(self):
        source = "LOAD 1"

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        parser = Parser(tokens)
        parser.parse_tokens()
        instructions = parser.get_instructions

        code_generator = CodeGenerator(instructions)

if __name__ == "__main__":
    unittest.main()