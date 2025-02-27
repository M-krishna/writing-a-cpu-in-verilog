import unittest
from scanner import Scanner
from parser import Parser


class TestParser(unittest.TestCase):
    def test_load(self):
        source = "LOAD R0, R1"

        scanner = Scanner(source)
        scanner.scan_tokens()

        parser = Parser(scanner.get_tokens)
        parser.parse_tokens()

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