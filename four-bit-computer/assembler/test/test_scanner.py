import unittest
from scanner import Scanner
from token_type import TokenType

class TestScanner(unittest.TestCase):
    
    def test_mnemonics(self):
        source = "LOAD 1"
        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        self.assertEqual(tokens[0].tt, TokenType.LOAD.name)
        self.assertEqual(tokens[0].lexeme, TokenType.LOAD.value)
        self.assertEqual(tokens[1].tt, TokenType.NUMBER.name)
        self.assertEqual(tokens[1].lexeme, str(1))
        self.assertEqual(tokens[2].tt, TokenType.EOF.name)


if __name__ == "__main__":
    unittest.main()