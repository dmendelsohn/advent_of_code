import re
from collections import namedtuple

Claim = namedtuple('Claim', ['claim_id', 'x', 'y', 'width', 'height'])

#1 @ 429,177: 12x27

def parse_claim(line):
    PATTERN = '#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)'
    m = re.search(PATTERN, line)
    return Claim(*map(int, m.groups()))

def parse(f):
    return map(parse_claim, f.read().strip().split('\n'))

def part1Answer(f):
    claims = parse(f)
    num_claims = {}
    for claim in claims:
        for x in range(claim.x, claim.x + claim.width):
            for y in range(claim.y, claim.y + claim.height):
                num_claims[(x,y)] = num_claims.get((x,y), 0) + 1
    return sum(map(lambda val: val >= 2, num_claims.values()))

def is_overlap(claim1, claim2):
    x_overlap = (claim1.x <= claim2.x < (claim1.x + claim1.width) or \
            claim2.x <= claim1.x < (claim2.x + claim2.width))
    y_overlap = (claim1.y <= claim2.y < (claim1.y + claim1.height) or \
            claim2.y <= claim1.y < (claim2.y + claim2.height))
    return x_overlap and y_overlap

def part2Answer(f):
    claims = parse(f)
    for claim in claims:
        is_overlapping = False
        for other in claims:
            if claim.claim_id != other.claim_id and is_overlap(claim, other):
                is_overlapping = True
                break
        if not is_overlapping:
            return claim.claim_id
    return 'They all overlap'

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

