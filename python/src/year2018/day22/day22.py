DEPTH = 5616
TARGET = 10,785
MODULO = 20183

## TEST VALUES
#DEPTH = 510
#TARGET = 10, 10

ROCKY = '.'
WET = '='
NARROW = '|'


def get_danger_level(t):
    if t == ROCKY:
        return 0
    elif t == WET:
        return 1
    else:
        return 2


def get_type(geo_index):
    erosion = (geo_index + DEPTH) % MODULO
    if erosion%3 == 0:
        return ROCKY
    elif erosion%3 == 1:
        return WET
    else:
        return NARROW


def get_geo_index(x, y, memo):
    if (x,y) in memo:
        return memo[(x,y)]

    if (x,y) == (0,0) or (x,y) == TARGET:
        index = 0
    elif x == 0:
        index = y * 48271
    elif y == 0:
        index = x * 16807
    else:
        index = (get_geo_index(x-1, y, memo) + DEPTH) * (get_geo_index(x, y-1, memo) + DEPTH)
    index = index % MODULO
    memo[(x,y)] = index
    return index

def get_region(x, y, memo):
    return get_type(get_geo_index(x, y, memo))


# 8648 is too low
def part1Answer(f):
    total = 0
    memo = {}
    for x in range(0, TARGET[0]+1):
        for y in range(0, TARGET[1]+1):
            index = get_geo_index(x, y, memo)
            t = get_type(index)
            danger = get_danger_level(t)
            total += danger
            #print('({},{}): geo_index={}, type={}'.format(x, y, index, t))
    return total

ALLOWED = {
    ROCKY: ('T', 'C'),
    WET: ('C', 'N'),
    NARROW: ('T', 'N')
}

def get_neighbors(current, memo):
    # Return set of (node, distance) tuples for each neighbor
    x, y, gear = current
    region = get_region(x, y, memo)
    neighbors = set()

    # First the "change gear" neighbor
    for next_gear in 'TCN':
        if next_gear in ALLOWED[region] and next_gear != gear:
            neighbor = (x, y, next_gear)
            neighbors.add((neighbor, 7))

    # Next add 4 neighbors.  Check our current gear is okay there
    for (xoff, yoff) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nextx = x + xoff
        nexty = y + yoff
        if nextx < 0 or nexty < 0:
            continue

        next_region = get_region(nextx, nexty, memo)
        if gear in ALLOWED[next_region]:
            neighbor = (nextx, nexty, gear)
            neighbors.add((neighbor, 1))

    return neighbors



def part2Answer(f):
    memo = {}

    # unvisited = {node: None for node in nodes} #using None as +inf
    distances = {}  # Keep track of distances so far, only finalized once a node is visited
    unvisited = set()  # Seen as a neighbor, not yet visited
    visited = set()
    current = (0, 0, 'T')  # There's T (torch), C (climbing), N (neither)
    STOP = (TARGET[0], TARGET[1], 'T')

    distances[current] = 0
    unvisited.add(current)
    while STOP not in visited:
        for neighbor, distance in get_neighbors(current, memo):
            if neighbor in visited:
                continue

            unvisited.add(neighbor)
            new_distance = distances[current] + distance
            if distances.get(neighbor, float('inf')) > new_distance:  # Found a shorter path
                distances[neighbor] = new_distance

        visited.add(current)
        # heur = abs(TARGET[0]-current[0]) + abs(TARGET[1]-current[1])
        # print('Visiting: {}, Heuristic: {}'.format(current, heur))
        unvisited.remove(current)
        # Should do a priority queue for unvisited but I don't feel like it right now
        current = min(unvisited, key = lambda x: distances[x] + abs(TARGET[0] - x[0]) + abs(TARGET[1] - x[1]))

    #print(distances)
    return distances[STOP]


if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

