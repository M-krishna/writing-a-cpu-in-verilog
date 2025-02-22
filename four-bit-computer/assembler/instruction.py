class Instruction:
    def __init__(self, mnemonic: str, data: str, location_counter: int = 0):
        self.mnemonic = mnemonic
        self.data = data
        self.location_counter = location_counter

    def __repr__(self):
        return f"Instruction({self.mnemonic}, {self.data})"