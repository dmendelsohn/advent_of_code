from collections import namedtuple
import re

Particle = namedtuple('Particle', ['xstart', 'ystart', 'xvel', 'yvel'])

def parse(f):
    lines = f.read().strip().split('\n')
    PATTERN = 'position=<([ 0-9\-]*),([ 0-9-]*)> velocity=<([ 0-9-]*),([ 0-9-]*)>'
    particles = [Particle(*map(int, re.search(PATTERN, line).groups())) for line in lines]
    return particles

def print_image(particles, t=0):
    xmin = min(p.xstart + p.xvel*t for p in particles)
    xmax = max(p.xstart + p.xvel*t for p in particles)
    ymin = min(p.ystart + p.yvel*t for p in particles)
    ymax = max(p.ystart + p.yvel*t for p in particles)
    print('t: {}, xwindow: [{}, {}], ywindow: [{},{}]'.format(t, xmin, xmax, ymin, ymax))
    # Print just the window
    chars = [['.' for x in range(xmin, xmax+1)] for y in range(ymin, ymax+1)]
    # Render particles
    for p in particles:
        xpixel = p.xstart + p.xvel*t - xmin
        ypixel = p.ystart + p.yvel*t - ymin
        chars[ypixel][xpixel] = '#'
    for row in chars:
        print(''.join(row))

def part1Answer(f):
    particles = parse(f)
    start = 10459
    steps = 1
    for t in range(start, start+steps):
        print_image(particles, t)
    return 0

def part2Answer(f):
    return 0

# MIN_WINDOW AT t=10459

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

# position=< 42045,  10623> velocity=<-4, -1>
