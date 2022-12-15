import re

TEST = False
if TEST:
    INIT_STATE = '#..#.#..##......###...###'
    FILE = 'input2.txt'
else:
    INIT_STATE = '###.#..#..##.##.###.#.....#.#.###.#.####....#.##..#.#.#..#....##..#.##...#.###.#.#..#..####.#.##.#'
    FILE = 'input.txt'

def parse(f):
    lines = f.read().strip().split('\n')
    PATTERN = '([#.]{5}) => ([#.])'
    rules = {} # Map 5 char string to 1 char state
    for line in lines:
        key, val = re.search(PATTERN, line).groups()
        rules[key] = val
    return rules

def get_next_state(state, index, rules):
    padded_state = '.'*4 + state + '.'*4
    next_state = []  # List of chars so we can mutate it
    for i in range(2, len(padded_state)-2):
        key = padded_state[i-2:i+3]
        next_state.append(rules.get(key, '.'))
    # Later: can do some truncation if needed
    next_state = ''.join(next_state)
    first_plant = next_state.find('#')
    last_plant = next_state.rfind('#')
    next_state = next_state[first_plant:last_plant+1]
    return next_state, index-2+first_plant


def sum_plant_positions(state, index):
    total = 0
    for i in range(len(state)):
        if state[i] == '#':
            total += (i+index)
    return total

def part1Answer(f):
    rules = parse(f)
    state, index = INIT_STATE, 0
    print('Initial: {}'.format(state))
    for i in range(20):
        state, index = get_next_state(state, index, rules)
        total = sum_plant_positions(state, index)
        print('Step {:02d}: {} (Index = {}, Sum = {})'.format(i+1, state, index, total))
    return sum_plant_positions(state, index)

def part2Answer(f):
    # Observed pattern that for N >= 100, f(N) = 50*N + 1175
    N = 5*(10**10)
    return 50*N + 1175

if __name__ == "__main__":
    f = open(FILE, 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

