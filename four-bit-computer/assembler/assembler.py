#!/usr/bin/env python3

import sys
from scanner import Scanner
from parser import Parser
from code_generator import CodeGenerator

if __name__ == "__main__":

    arg = sys.argv

    if len(arg) <= 1:
        print(f"Usage: assembler.py FILE=<instructions_file_name>")

    file_path = arg[1]

    with open(file_path, "r") as f:
        source = f.read()

    scanner = Scanner(source)
    scanner.scan_tokens()

    parser = Parser(scanner.get_tokens)
    parser.parse_tokens()

    code_generator = CodeGenerator(parser.get_instructions)
    code_generator.generate_binary_code()
    code_generator.generate_hex_code()