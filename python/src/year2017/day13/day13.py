def parse_input(f):
    lines = f.read().strip().split('\n')
    firewall = {}
    for line in lines:
        line = line.replace(':', '')
        parts = line.split(' ')
        firewall[int(parts[0])] = int(parts[1])
    return firewall

def get_cost(firewall, start=0, penalize_row_0=False):
    cost = 0
    for (row, depth) in firewall.items():
        if (start+row)%(2*(depth-1)) == 0:
            cost += row*depth
    if penalize_row_0 and start%(2*(firewall[0]-1)) == 0:
        cost += 1
    return cost

def part1Answer(f):
    firewall = parse_input(f)
    return get_cost(firewall)

def part2Answer(f):
    firewall = parse_input(f)
    start = 0
    while get_cost(firewall, start, True) != 0:
        start += 1
    return start

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

