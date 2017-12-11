def parse_input(f):
    lines = f.read().strip().split('\n')
    return [line.split(' ') for line in lines]

def is_valid_passphrase(words, part_2=False):
    if part_2:
        words = [''.join(sorted(word)) for word in words]
    return len(words) == len(set(words))

def part1Answer(f):
    return sum(1 for line in parse_input(f) if is_valid_passphrase(line))

def part2Answer(f):
    return sum(1 for line in parse_input(f) if is_valid_passphrase(line, True))

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

