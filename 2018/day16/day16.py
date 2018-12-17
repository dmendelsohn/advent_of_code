OPERATIONS = ['addr', 'addi', 'mulr', 'muli', 'borr', 'bori', 'banr', 'bani',
              'setr', 'seti', 'gtri', 'gtir', 'gtrr', 'eqri', 'eqir', 'eqrr']

def parse1(f):
    lines = f.read().split('\n')
    cases = []
    for i in range(len(lines)/4):
        before = eval(lines[4*i][8:])
        inst = map(int, lines[4*i+1].split())
        after = eval(lines[4*i+2][7:])
        cases.append((inst, before, after))
    return cases

def parse2(f):
    lines = f.read().strip().split('\n')
    return [map(int, line.split()) for line in lines]

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


def get_possibles(case):
    raw_inst, before, after = case
    possibles = set()
    for op in OPERATIONS:
        inst = [op] + raw_inst[1:]
        regs = do_inst(inst, before)
        if regs == after:
            possibles.add(op)
    return possibles

def part1Answer(f):
    cases = parse1(f)
    count = sum(len(get_possibles(case)) >= 3 for case in cases)
    return count


def get_opcodes(cases):
    overall_possibles = {}
    for i in range(16):
        op_cases = filter(lambda c: c[0][0] == i, cases)
        possibles = set(OPERATIONS)
        for case in op_cases:
            possibles = possibles & get_possibles(case)
        overall_possibles[i] = possibles
    print(overall_possibles)

    opcodes = {}
    while len(opcodes) < 16:
        for key in overall_possibles.keys():
            if len(overall_possibles[key]) == 1:
                op = list(overall_possibles[key])[0]
                del overall_possibles[key]
                opcodes[key] = op
                for other in overall_possibles:
                    other_possibles = overall_possibles[other]
                    if op in other_possibles:
                        other_possibles.remove(op)
    return opcodes

def execute_program(raw_insts, opcodes):
    regs = [0]*4
    for raw_inst in raw_insts:
        op = opcodes[raw_inst[0]]
        inst = [op] + raw_inst[1:]
        regs = do_inst(inst, regs)
    return regs


def part2Answer(f1, f2):
    cases = parse1(f1)
    opcodes = get_opcodes(cases)
    print('Opcodes: {}'.format(opcodes))
    raw_insts = parse2(f2)
    regs = execute_program(raw_insts, opcodes)
    return regs

OPCODES = {
    0: None,
    1: None,
    2: None,
    3: None,
}

if __name__ == "__main__":
    f1 = open('input1.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f1)))
    f1.seek(0)
    f2 = open('input2.txt', 'rt')
    print("Part 2: {}".format(part2Answer(f1, f2)))

