def compile(program):
    instruction_map = {
        "NOP": 0x0,
        "LOAD": 0x1,
        "CMP": 0x2,
        "INC": 0x3,
        "DEC": 0x4,
        "JZ": 0x5,
        "JMP": 0x6,
        "STORE": 0x7,
        "HALT": 0x8,
    }

    register_map = {
        "ACC": 0x0,
        "R1": 0x1,
        "R2": 0x2
    }

    machine_code = []
    labels = {}

    # Сбор меток (первый проход)
    address = 0
    for line in program:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if ":" in line:
            label = line.replace(":", "").strip()
            labels[label] = address
        else:
            address += 1

    # Генерация машинного кода (второй проход)
    for line in program:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        if ":" in line:
            continue  # Пропускаем метки

        parts = line.split()
        if not parts:
            continue

        # Получаем код операции
        opcode_str = parts[0].upper()
        opcode = instruction_map.get(opcode_str, None)
        if opcode is None:
            raise ValueError(f"Unknown instruction: {opcode_str}")

        instr = opcode << 24  # Код операции (биты 31-24)
        mode_src, mode_dest = 0, 0
        src, dest = 0, 0

        # Источник (src)
        if len(parts) > 1:
            src_str = parts[1]
            if src_str.startswith("[") and src_str.endswith("]"):  # Косвенная адресация
                mode_src = 0x2
                src_str = src_str[1:-1]  # Убираем квадратные скобки
                if src_str.upper() in register_map:
                    src = register_map[src_str.upper()]
                else:
                    raise ValueError(f"Invalid indirect source operand: {src_str}")
            elif src_str.upper() in register_map:  # Регистр
                mode_src = 0x0
                src = register_map[src_str.upper()]
            elif src_str.isdigit():  # Адрес памяти
                mode_src = 0x1
                src = int(src_str)
            elif src_str in labels:  # Метка
                mode_src = 0x1
                src = labels[src_str]+1
            else:
                raise ValueError(f"Unknown source operand: {src_str}")

        # Назначение (dest)
        if len(parts) > 2:
            dest_str = parts[2]
            if dest_str.startswith("[") and dest_str.endswith("]"):  # Косвенная адресация
                mode_dest = 0x2
                dest_str = dest_str[1:-1]  # Убираем квадратные скобки
                if dest_str.upper() in register_map:
                    dest = register_map[dest_str.upper()]
                else:
                    raise ValueError(f"Invalid indirect destination operand: {dest_str}")
            elif dest_str.upper() in register_map:  # Регистр
                mode_dest = 0x0
                dest = register_map[dest_str.upper()]
            elif dest_str.isdigit():  # Адрес памяти
                mode_dest = 0x1
                dest = int(dest_str)
            elif dest_str in labels:  # Метка
                mode_dest = 0x1
                dest = labels[dest_str]
            else:
                raise ValueError(f"Unknown destination operand: {dest_str}")

        # Формирование инструкции
        instr |= (mode_src & 0x3) << 22
        instr |= (mode_dest & 0x3) << 20
        instr |= (src & 0x3FF) << 10
        instr |= dest & 0x3FF
        machine_code.append(instr)

    return machine_code