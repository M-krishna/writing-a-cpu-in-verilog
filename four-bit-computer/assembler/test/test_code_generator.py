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
        code_generator.generate_binary_code()
        code_generator.generate_hex_code()

        binary_code_instructions = code_generator.get_binary_code_instruction
        hex_code_instructions = code_generator.get_hex_code_instructions

        self.assertEqual(binary_code_instructions[0], str('0001'))
        self.assertEqual(hex_code_instructions[0], str(1))

    def test_load_add_sub_instruction(self):
        source = """
            LOAD 1
            ADD 1
            SUB 1
        """

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        parser = Parser(tokens)
        parser.parse_tokens()
        instructions = parser.get_instructions

        code_generator = CodeGenerator(instructions)
        code_generator.generate_binary_code()
        code_generator.generate_hex_code()

        binary_code_instructions = code_generator.get_binary_code_instruction
        hex_code_instructions = code_generator.get_hex_code_instructions

        expected_binary_code_instructions = ['0001', '0011', '0101']
        expected_hex_code_instructions = ['1', '3', '5']

        for index, expected_bin_instruction_code in enumerate(expected_binary_code_instructions):
            with self.subTest(index):
                self.assertEqual(binary_code_instructions[index], expected_bin_instruction_code)

        for index, expected_hex_instruction_code in enumerate(expected_hex_code_instructions):
            with self.subTest(index):
                self.assertEqual(hex_code_instructions[index], expected_hex_instruction_code)

    def test_label(self):
        source = """
            JMP TEST_2

            TEST_1:
                LOAD 1
                ADD 1
                JMP 1

            TEST_2:
                LOAD 1
                ADD 1
                ADD 1
        """

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        parser = Parser(tokens)
        parser.parse_tokens()
        instructions = parser.get_instructions

        code_generator = CodeGenerator(instructions)
        code_generator.generate_binary_code()
        code_generator.generate_hex_code()

        print(code_generator.get_binary_code_instruction)
        print(code_generator.get_hex_code_instructions)


if __name__ == "__main__":
    unittest.main()