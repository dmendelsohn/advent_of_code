import re
# pos=<-27274263,26777579,99003485>, r=96649598

def parse(f):
    bots = []
    for line in f.read().strip().split('\n'):
        PATTERN = 'pos=<(.*),(.*),(.*)>, r=(.*)'
        parts = map(int, re.search(PATTERN, line).groups())
        bots.append(((parts[0], parts[1], parts[2]), parts[3]))
    return bots

def part1Answer(f):
    bots = parse(f)
    bigbot = max(bots, key=lambda b: b[-1])
    count = 0
    for bot in bots:
        dist = abs(bigbot[0][0]-bot[0][0]) + abs(bigbot[0][1]-bot[0][1]) + abs(bigbot[0][2]-bot[0][2])
        if dist <= bigbot[-1]:
            count +=1 
    return count

def part2Answer(f):
    return 0

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

