def parse(f):
    lines = f.read().strip().split('\n')
    ip_binding = int(lines[0][-1])
    program = []
    for line in lines[1:]:
        parts = line.split(' ')
        program.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
    return ip_binding, program

def do_inst(inst, regs):
    regs = regs[:]
    if inst[0][:3] in ('add', 'mul', 'bor', 'ban'):
        a = regs[inst[1]]
        b = regs[inst[2]] if inst[0][3] == 'r' else inst[2]
        if inst[0].startswith('add'):
            result = a + b
        elif inst[0].startswith('mul'):
            result = a * b
        elif inst[0].startswith('bor'):
            result = a | b
        elif inst[0].startswith('ban'):
            result = a & b

    elif inst[0].startswith('set'):
        result = regs[inst[1]] if inst[0][3] == 'r' else inst[1]

    else:
        a = regs[inst[1]] if inst[0][2] == 'r' else inst[1]
        b = regs[inst[2]] if inst[0][3] == 'r' else inst[2]
        if inst[0].startswith('gt'):
            result = int(a > b)
        elif inst[0].startswith('eq'):
            result = int(a == b)

    regs[inst[3]] = result
    return regs


def execute_program(ip_binding, program):
    ip = 0
    regs = [0]*6
    while 0 <= ip < len(program):
        if ip == 28:  # Inspect R1 at this point
            print('At IP=28, R1={}'.format(regs[1]))
            return regs[1]

        parts = ['ip={}'.format(ip)]

        regs[ip_binding] = ip

        parts.append(str(regs))
        parts.append(str(program[ip]))

        regs = do_inst(program[ip], regs)

        parts.append(str(regs))

        ip = regs[ip_binding] + 1
        # print ' '.join(parts)
    return regs[0]


R1_INIT = 6663054
R2_INIT = 65536
MASK24 = 16777215
MULTIPLIER = 65899

def next_r2(r2=R2_INIT):
    r2 = r2 | R2_INIT
    r1 = R1_INIT
    while r2:
        r2, remainder = r2/256, r2%256
        r1 = ((r1 + remainder) * MULTIPLIER) & MASK24
    return r1


def part1Answer(f):
    ip_binding, program = parse(f)
    return execute_program(ip_binding, program)

# 2495768 is too low
def part2Answer(f):
    r2 = next_r2()
    print('First answer: {}'.format(r2))
    seen = set()
    #while r2 not in seen:
    while True:
        if r2 not in seen:
            print('NEW VAL: {}'.format(r2))
            seen.add(r2)
        last_r2, r2 = r2, next_r2(r2)
        #print('{} yields {}'.format(last_r2, r2))
    return last_r2


if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))



