class Instruction:
    def __init__(self, mnemonic: str, data: str):
        self.mnemonic = mnemonic
        self.data = data

    def __repr__(self):
        return f"Instruction({self.mnemonic}, {self.data})"