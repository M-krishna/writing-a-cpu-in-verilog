import unittest
from scanner import Scanner


class TestScanner(unittest.TestCase):
    def test_mnemonics(self):
        source = """
            LOAD R0, R1
            LOAD R0, 1
            ADD R1, R0
            ADD R0, 5
            SUB R0, R1
            SUB R1, 10
            AND R1, R0
            AND R0, 3
            OR R0, R1
            OR R0, 4
            XOR R0, R1
            XOR R1, 2
            JMP
            HLT
        """