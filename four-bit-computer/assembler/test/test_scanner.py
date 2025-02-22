import unittest
from scanner import Scanner
from token_type import TokenType

class TestScanner(unittest.TestCase):
    
    def test_mnemonics(self):
        source = "LOAD 1"
        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        # (mnemonic, lexeme)
        expected = [
            (TokenType.LOAD.name, TokenType.LOAD.value),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.EOF.name, "")
        ]

        self.assertEqual(len(tokens), len(expected), "Token count mismatch")

        for index, (expected_tt, expected_lexeme) in enumerate(expected):
            with self.subTest(index):
                self.assertEqual(tokens[index].tt, expected_tt)
                if expected_lexeme:
                    self.assertEqual(tokens[index].lexeme, expected_lexeme)

    def test_labels(self):
        source = """
            JMP TEST_1

            TEST_1:
                LOAD 1
                ADD 1
                JMP 1
        """
        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        # (mnemonic, lexeme)
        expected = [
            (TokenType.JMP.name, TokenType.JMP.name),
            (TokenType.LABEL.name, "TEST_1"),
            (TokenType.LABEL.name, "TEST_1:"),
            (TokenType.LOAD.name, TokenType.LOAD.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.ADD.name, TokenType.ADD.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.JMP.name, TokenType.JMP.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.EOF.name, "")
        ]

        # First, assert that we have the expected number of tokens
        self.assertEqual(len(tokens), len(expected), "Token mismatch count")

        # Use subtest to assert over each token and give context on failure
        for index, (expected_tt, expected_lexeme) in enumerate(expected):
            with self.subTest(index):
                self.assertEqual(tokens[index].tt, expected_tt)
                # only check lexeme if there is an expected value
                if expected_lexeme:
                    self.assertEqual(tokens[index].lexeme, expected_lexeme)


    def test_multiple_labels(self):
        source = """
            JMP TEST_2

            TEST_1:
                LOAD 1
                ADD 1
                JMP 1

            TEST_2:
                LOAD 1
                ADD 1
                JMP 0
        """

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        expected = [
            (TokenType.JMP.name, TokenType.JMP.name),
            (TokenType.LABEL.name, "TEST_2"),
            (TokenType.LABEL.name, "TEST_1:"),
            (TokenType.LOAD.name, TokenType.LOAD.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.ADD.name, TokenType.ADD.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.JMP.name, TokenType.JMP.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.LABEL.name, "TEST_2:"),
            (TokenType.LOAD.name, TokenType.LOAD.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.ADD.name, TokenType.ADD.name),
            (TokenType.NUMBER.name, str(1)),
            (TokenType.JMP.name, TokenType.JMP.name),
            (TokenType.NUMBER.name, str(0)),
            (TokenType.EOF.name, "")
        ]

        self.assertEqual(len(tokens), len(expected), "Token count mismatch")

        for index, (expected_tt, expected_lexeme) in enumerate(expected):
            with self.subTest(index):
                self.assertEqual(tokens[index].tt, expected_tt)
                if expected_lexeme:
                    self.assertEqual(tokens[index].lexeme, expected_lexeme)

if __name__ == "__main__":
    unittest.main()