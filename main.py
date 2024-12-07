from ram import ram
from compile import compile
from cpu import CPU
from program import program

array = [5, 24, 417, 7, 85]

array_base_address = 102
array_count = len(array)

for i, value in enumerate(array):
    ram.write(array_base_address + i, value)

ram.write(100, array_base_address)
ram.write(101, array_count)

machine_code = compile(program)

for i, instruction in enumerate(machine_code):
    ram.write(i, instruction)

cpu = CPU(ram)
cpu.run()

print("Максимальное число:", ram.read(200))