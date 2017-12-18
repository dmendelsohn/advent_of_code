def parse_move(text):
    if text[0] == 's':
        return 'spin', int(text[1:])
    elif text[0] == 'x':
        parts = text[1:].split('/')
        return 'exchange', int(parts[0]), int(parts[1])
    elif text[0] == 'p':
        parts = text[1:].split('/')
        return 'partner', parts[0], parts[1]
    else:
        raise Exception

def parse_input(f):
    return map(parse_move, f.read().strip().split(','))

# State is permutation of 'abcdefghijklmnop'
def make_move(state, move):
    if move[0] == 'spin':
        if 0 < move[1] < len(state):
            return state[-move[1]:] + state[:-move[1]]
        else:
            return state
    elif move[0] == 'exchange':
        tmp = list(state)
        tmp[move[1]], tmp[move[2]] = tmp[move[2]], tmp[move[1]]
        return ''.join(tmp)
    elif move[0] == 'partner':
        return state.replace(move[1], '1').replace(move[2], '2').replace('1', move[2]).replace('2', move[1])
    else:
        raise Exception

def part1Answer(f):
    moves = parse_input(f)
    state = 'abcdefghijklmnop'
    for move in moves:
        state = make_move(state, move)
    return state

def part2Answer(f):
    ends = {}
    count = 0
    moves = parse_input(f)
    state = 'abcdefghijklmnop'
    while state not in ends:
        ends[state] = count
        for move in moves:
            state = make_move(state, move)
        count += 1
    period = count - ends[state]
    answer_index = (10**9 - count)%period
    while (answer_index + period) in ends.values():
        answer_index += period
    for (k, v) in ends.items():
        if v == answer_index:
            return k

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

