def collapse(polymer):
    polymer = list(polymer)
    i = 0
    while i < len(polymer) - 1:
        if polymer[i].lower() == polymer[i+1].lower() and polymer[i] != polymer[i+1]:
            # Remove both i and i+1 indices, set i back to max(0, i-1)
            del polymer[i:i+2]
            i = max(0, i-1)
        else:
            i += 1
    return ''.join(polymer)

def part1Answer(f):
    polymer = f.read().strip()
    polymer = collapse(polymer)
    return len(polymer)

def part2Answer(f):
    polymer = f.read().strip()
    shortest = len(polymer)
    chars = {l.lower() for l in polymer}
    for char in chars:
        subpoly = polymer.replace(char, '').replace(char.upper(), '')
        subpoly = collapse(subpoly)
        shortest = min(shortest, len(subpoly))
    return shortest

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

