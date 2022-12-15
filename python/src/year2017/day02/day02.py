import itertools

def get_only_int_division(nums):
    for (a,b) in itertools.permutations(nums, 2):
        if a%b == 0:
            return a//b

def parse_file(f):
    lines = f.read().strip().split('\n')
    lines = map(lambda line: map(int, line.split('\t')), lines)
    return lines

def part1Answer(f):
    lines = parse_file(f)
    total = 0
    for line in lines:
        total += (max(line) - min(line))
    return total

def part2Answer(f):
    lines = parse_file(f)
    total = 0
    for line in lines:
        total += get_only_int_division(line)
    return total

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

