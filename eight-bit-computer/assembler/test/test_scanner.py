import unittest
from token_internal import Token
from scanner import Scanner
from test.factory.token_factory import TokenFactory
from typing import List

class TestScanner(unittest.TestCase):
    def test_mnemonics(self):
        source = """
            LOAD R0, R1
        """

        load_token: Token = TokenFactory.create_token("LOAD", "LOAD")
        r0_token: Token = TokenFactory.create_token("IDENTIFIER", "R0")
        comma_token: Token = TokenFactory.create_token("COMMA", ",")
        r1_token: Token = TokenFactory.create_token("IDENTIFIER", "R1")
        eof_token: Token = TokenFactory.create_token("EOF", "")

        expected_tokens: List[Token] = [load_token, r0_token, comma_token, r1_token, eof_token]

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        for i, t in enumerate(tokens):
            with self.subTest(i):
                self.assertEqual(expected_tokens[i].tt, t.tt)
                self.assertEqual(expected_tokens[i].lexeme, t.lexeme)

    def test_mnemonics_one(self):
        source = """
            LOAD R1, 1
        """

        load_token: Token = TokenFactory.create_token("LOAD", "LOAD")
        r1_token: Token = TokenFactory.create_token("IDENTIFIER", "R1")
        comma_token: Token = TokenFactory.create_token("COMMA", ",")
        number_token: Token = TokenFactory.create_token("NUMBER", str(1))
        eof_token: Token = TokenFactory.create_token("EOF", "")

        expected_tokens: List[Token] = [load_token, r1_token, comma_token, number_token, eof_token]

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        for i, t in enumerate(tokens):
            with self.subTest(i):
                self.assertEqual(expected_tokens[i].tt, t.tt)
                self.assertEqual(expected_tokens[i].lexeme, t.lexeme)

    def test_mnemonics_two(self):
        source = """
            HLT
        """

        hlt_token: Token = TokenFactory.create_token("HLT", "HLT")

        scanner = Scanner(source)
        scanner.scan_tokens()
        tokens = scanner.get_tokens

        self.assertEqual(tokens[0].tt, hlt_token.tt)
        self.assertEqual(tokens[0].lexeme, hlt_token.lexeme)


if __name__ == "__main__":
    unittest.main()