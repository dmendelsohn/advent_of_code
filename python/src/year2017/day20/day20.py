def helper(a, v, d, t):
    return a*t*(t+1)//2 + v*t + d

def get_pos(particle, t):
   return [helper(particle[2][i], particle[1][i], particle[0][i], t) for i in range(3)]

def mag(vec):
    return sum(map(abs, vec))

def long_term_metric(particle):
    return (mag(particle[2]), mag(particle[1]), mag(particle[0]))

def parse_vector(vec):
    return map(int, vec[1:-1].split(','))

def parse_line(line):
    parts = line.replace(', ', ' ').split(' ')
    return [parse_vector(part[2:]) for part in parts]

def parse_input(f):
    return [parse_line(line) for line in f.read().strip().split('\n')]

def part1Answer(f):
    particles = parse_input(f)
    lowest_a = min(enumerate(particles), key=lambda p: long_term_metric(p[1]))
    print(lowest_a)
    return lowest_a[0]

def part2Answer(f):
    particles = parse_input(f)
    t = 0
    while t < 100:
        #print(t, len(particles))
        locations = {}
        for p in particles:
            loc = tuple(get_pos(p, t))
            locations[loc] = locations.get(loc, []) + [p]
        filtered_locations = {k: v[0] for (k, v) in locations.items() if len(v) == 1}
        particles = filtered_locations.values() # Rebuild particle list
        t += 1
    return len(particles)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

