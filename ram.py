class RAM:
    def __init__(self, size=256):
        self.memory = [0] * size

    def read(self, address):
        return self.memory[address]

    def write(self, address, data):
        self.memory[address] = data

ram = RAM()