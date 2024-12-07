program = [
    "LOAD 100 R1",
    "LOAD 101 R2",
    "LOAD [R1] ACC",
    "LOOP:",
    "INC R1",
    "DEC R2",
    "JZ END",
    "CMP [R1] ACC",
    "JMP LOOP",
    "END:",
    "STORE ACC 200",
    "HALT"
]