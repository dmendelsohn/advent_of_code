from collections import namedtuple
import itertools

class Point(namedtuple('Point', ['x', 'y', 'z', 't'])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z, self.t + other.t)

    @property
    def magnitude(self):
        return abs(self.x) + abs(self.y) + abs(self.z) + abs(self.t)

def parse(f):
    return [Point(*map(int, line.split(','))) for line in f.read().strip().split('\n')]

OFFSETS = set()
for x in itertools.product(*[range(-3, 4)]*4):
    p = Point(*x)
    if p.magnitude <= 3:          
        OFFSETS.add(p)
OFFSETS.remove(Point(0,0,0,0))

def get_neighbors(points, point):
    return {point+offset for offset in OFFSETS if point+offset in points}


def get_constellation(points, point, visited):  # Get constallation that includes point
    visited.add(point)
    const = set([point])
    neighbors = get_neighbors(points, point)
    for n in neighbors:
        if n not in visited:
            const = const.union(get_constellation(points, n, visited))
    return const


def get_constellations(points):
    unvisited = set(points)
    visited = set()
    num_consts = 0
    while unvisited:
        # Pick an arbitrary one to visit recursively
        point = next(iter(unvisited))
        const = get_constellation(points, point, visited)
        num_consts += 1
        unvisited -= const
    return num_consts


def part1Answer(f):
    points = parse(f)
    return get_constellations(points)

def part2Answer(f):
    return 0

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

