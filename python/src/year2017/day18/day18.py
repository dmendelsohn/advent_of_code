def parse_value(val):
    try:
        return int(val)
    except ValueError:
        return val

def parse_input(f):
    # Return list of instructions
    lines = f.read().strip().split('\n')
    moves = []
    for line in lines:
        parts = line.split(' ')
        op = parts[0]
        reg = parse_value(parts[1])
        if len(parts) < 3:
            moves.append((op, reg)) 
        else:
            val = parse_value(parts[2])
            moves.append((op, reg, val))
    return moves

def value(key, registers):
    if isinstance(key, int):
        return key
    else:
        if not ord('a') <= ord(key) <= ord('p'):
            raise Exception
        return registers.get(key, 0)

# Returns newpc, rcv (None if nothing recovered)
def execute_p1(program, pc, registers):
    inst = program[pc]
    rcv = None
    if inst[0] == 'set':
        registers[inst[1]] = value(inst[2], registers)
    elif inst[0] == 'add':
        registers[inst[1]] = value(inst[1], registers) + value(inst[2], registers)
    elif inst[0] == 'mul':
        registers[inst[1]] = value(inst[1], registers) * value(inst[2], registers)
    elif inst[0] == 'mod':
        registers[inst[1]] = value(inst[1], registers) % value(inst[2], registers)
    elif inst[0] == 'rcv':
        if value(inst[1], registers) > 0:
            rcv = registers['SOUND']
    elif inst[0] == 'jgz':
        if value(inst[1], registers) > 0:
            pc += value(inst[2], registers) - 1
    elif inst[0] == 'snd':
        registers['SOUND'] = value(inst[1], registers)
    else:
        raise ValueError('Bad op: {}'.format(inst))
    return pc+1, rcv

# Returns newpc, is_blocked
def execute(program, pc, registers, in_queue, out_queue):
    inst = program[pc]
    is_blocked = False
    if inst[0] == 'set':
        registers[inst[1]] = value(inst[2], registers)
    elif inst[0] == 'add':
        registers[inst[1]] = value(inst[1], registers) + value(inst[2], registers)
    elif inst[0] == 'mul':
        registers[inst[1]] = value(inst[1], registers) * value(inst[2], registers)
    elif inst[0] == 'mod':
        registers[inst[1]] = value(inst[1], registers) % value(inst[2], registers)
    elif inst[0] == 'rcv':
        if in_queue:
            registers[inst[1]] = in_queue.pop(0)
        else:
            is_blocked = True
            pc -= 1 # Back up so we repeat instruction
    elif inst[0] == 'jgz':
        if value(inst[1], registers) > 0:
            pc += value(inst[2], registers) - 1
    elif inst[0] == 'snd':
        snd = value(inst[1], registers)
        out_queue.append(snd)
    else:
        raise ValueError('Bad op: {}'.format(inst))
    return pc+1, is_blocked

def part1Answer(f):
    program = parse_input(f)
    pc = 0
    rcv = None
    registers = {}
    while rcv is None:
        pc, rcv = execute_p1(program, pc, registers)
    return rcv

def part2Answer(f):
    program = parse_input(f)
    count = 0
    #program = [('snd', 1), ('snd', 2), ('snd', 'p'), ('rcv', 'a'), ('rcv', 'b'), ('rcv', 'c'), ('rcv', 'd')]
    pc0, reg0, q0, snd_count0 = 0, {'p': 0}, [], 0
    pc1, reg1, q1, snd_count1 = 0, {'p': 1}, [], 0
    while 0 <= pc0 < len(program) and 0 <= pc1 < len(program):
        count += 1
        q0_before = len(q0)
        pc0, is_blocked0 = execute(program, pc0, reg0, q1, q0)
        if len(q0) > q0_before:
            snd_count0 += 1
        q1_before = len(q1)
        pc1, is_blocked1 = execute(program, pc1, reg1, q0, q1)
        if len(q1) > q1_before:
            snd_count1 += 1
        if is_blocked0 and is_blocked1:
            break

        if count%100000==0:
            print(snd_count1)
    return snd_count1

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

