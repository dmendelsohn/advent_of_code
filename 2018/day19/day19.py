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
        parts = ['ip={}'.format(ip)]
        regs[ip_binding] = ip
        parts.append(str(regs))
        parts.append(str(program[ip]))
        regs = do_inst(program[ip], regs)
        parts.append(str(regs))
        ip = regs[ip_binding] + 1
        print ' '.join(parts)
    return regs[0]


def part1Answer(f):
    ip_binding, program = parse(f)
    reg0 = execute_program(ip_binding, program)
    return reg0


def sum_of_factors(num):
    total = 0
    for i in range(1, (num/2)+1):
        if num%i == 0: total += i
    total += num
    print('Sum of factors of {} is {}'.format(num, total))
    return total

def part2Answer(f):
    sum_of_factors(976)
    return sum_of_factors(10551376)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

