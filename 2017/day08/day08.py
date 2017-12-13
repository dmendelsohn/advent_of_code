INCREMENTORS = {
    'inc': lambda x, y: x + y,
    'dec': lambda x, y: x - y
}

COMPARATORS = {
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '<=': lambda x, y: x <= y,
    '<': lambda x, y: x < y
}

def parse_input(f):
    lines = f.read().strip().split('\n')
    program = []
    for line in lines:
        parts = line.split(' ')
        program.append((parts[0], INCREMENTORS[parts[1]], int(parts[2]),
                        parts[4], COMPARATORS[parts[5]], int(parts[6])))
    return program

def step(registers, program, pc):
    reg_a, incrementor, delta, reg_b, comparator, num = program[pc]
    reg_b_value = registers.get(reg_b, 0)
    if comparator(reg_b_value, num):
        reg_a_value = registers.get(reg_a, 0)
        registers[reg_a] = incrementor(reg_a_value, delta)
    return pc+1

def part1Answer(f):
    program = parse_input(f)
    pc = 0
    registers = {}
    while 0 <= pc < len(program):
        pc = step(registers, program, pc)
    return max(registers.values())

def part2Answer(f):
    program = parse_input(f)
    pc = 0
    registers = {}
    max_so_far = 0
    while 0 <= pc < len(program):
        pc = step(registers, program, pc)
        max_so_far = max([max_so_far] + list(registers.values()))
    return max_so_far

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

