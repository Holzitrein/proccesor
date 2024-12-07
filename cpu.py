class CPU:
    def __init__(self, ram):
        self.ram = ram
        self.registers = [0] * 3 # ACC, R1-R2
        self.PC = 0  # Номер операции
        self.IR = 0  # Регистр с инструкцией
        self.running = True

    def fetch(self):
        self.IR = self.ram.read(self.PC)
        self.PC += 1

    def decode_execute(self):
        opcode = (self.IR >> 24) & 0xFF
        mode_src = (self.IR >> 22) & 0x3
        mode_dest = (self.IR >> 20) & 0x3
        src = (self.IR >> 10) & 0x3FF
        dest = self.IR & 0x3FF

        if opcode == 0x1:  # LOAD
            if mode_src == 0:  # Регистр
                self.registers[dest] = self.registers[src]
            elif mode_src == 1:  # Прямая адресация
                self.registers[dest] = self.ram.read(src)
            elif mode_src == 2:  # Косвенная адресация
                self.registers[dest] = self.ram.read(self.registers[src])

        elif opcode == 0x3:  # INC
            self.registers[src] += 1

        elif opcode == 0x4:  # DEC
            if self.registers[src] > 0:
                self.registers[0x2] -= 1

        elif opcode == 0x5:  # JZ
            if self.registers[0x2] == 0:
                self.PC = src-1

        elif opcode == 0x6:  # JMP
            self.PC = src-1

        elif opcode == 0x2:  # CMP
            if self.ram.read(self.registers[src]) > self.registers[dest]:
                self.registers[dest] = self.ram.read(self.registers[src])

        elif opcode == 0x7:  # STORE
            if mode_dest == 1:
                self.ram.write(dest, self.registers[src])
            elif mode_dest == 2:
                self.ram.write(self.registers[dest], self.registers[src])

        elif opcode == 0x8:  # HALT
            self.running = False

    def run(self):
        while self.running:
            self.fetch()
            self.decode_execute()
            self.monitor_step()

    def monitor_step(self):
        print(f"ACC: {self.registers[0]}")
        for i, value in enumerate(self.registers[1:]): print(f'R{i+1}: {value}')
        print(f"PC: {self.PC}")
        print(f"IR: {self.IR}")
        instr_bin = str(bin(self.IR)[2:])
        print(f"IR: {hex(self.IR)} | {' '.join([instr_bin[i:i+4] for i in range(0, len(instr_bin), 4)])}")
        print("-" * 60)