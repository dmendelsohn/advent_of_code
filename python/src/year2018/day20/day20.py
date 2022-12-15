from collections import namedtuple

class Vector(namedtuple('Vector', ['x', 'y'])):
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

OFFSETS = {
    'N': Vector(0, -1),
    'S': Vector(0, 1),
    'E': Vector(1, 0),
    'W': Vector(-1, 0)
}

def split(reg):  # Return (list of options, the rest)
    if len(reg) == 0:
        return [], ''
    elif reg[0] in 'NSEW':
        return [reg[0]], reg[1:]
    elif reg[0] == '(':
        count = 1  # Left minus right parens
        parts = []
        cur_part_start = 1
        i = 1
        while count > 0:
            c = reg[i]
            if c == '(':
                count += 1
            elif c == ')':
                count -=1

            if c == '|' and count == 1:
                parts.append(reg[cur_part_start:i])                
                cur_part_start = i+1
            i += 1
        parts.append(reg[cur_part_start:i-1])
        return parts, reg[i:]



def find_doors(reg, pos, doors):
    while reg:
        #print('Splitting: {}'.format(reg))
        options, reg = split(reg)
        #print('Options: {}, Remainder: {}'.format(options,reg))
        if len(options) == 1 and options[0] in OFFSETS:  # Be lazy to avoid recursion limit
            next_pos = pos+OFFSETS[options[0]]
            new_door = (min(pos, next_pos), max(pos, next_pos))
            # print('New door: {}, Pos: {}, Option: {}'.format(new_door, pos, options[0]))
            doors.add(new_door)
            pos = next_pos
            continue

        for option in options:
            find_doors(option, pos, doors)


def get_neighbors(pos, doors):
    neighbors = set()
    for offset in OFFSETS.values():
        neighbor = pos+offset
        if (min(pos,neighbor), max(pos, neighbor)) in doors:
            neighbors.add(neighbor)
    return neighbors


def get_distances(doors):
    origin = Vector(0, 0)
    distances = {}
    queue = [(origin, 0)]
    while queue:
        pos, distance = queue.pop(0)
        distances[pos] = distance
        for neighbor in get_neighbors(pos, doors):
            if neighbor not in distances:  # Careful not to revisit
                queue.append((neighbor, distance+1))
    return distances


# def print_map(doors):
#     points = set()
#     for door in doors:
#         points.add(door[0])
#         points.add(door[1])
#     minx = min(p.x for p in points)
#     maxx = max(p.x for p in points)
#     miny = min(p.y for p in points)
#     maxy = max(p.y for p in points)
#     for y in range(miny, maxy+1):
#         row 
#         for x in range(minx, maxx+1):



def part1Answer(f):
    reg = 'ENWWW(NEEE|SSE(EE|N))'  # Test case 1, answer = 10
    reg = 'ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN'  # Test case 2, answer = 18
    reg = 'ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))'  # Test case 3, answer = 23
    reg = 'WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))'  # Test case 4, answer = 31
    reg = f.read().strip()[1:-1]
    pos = Vector(0, 0)
    doors = set()
    find_doors(reg, pos, doors)
    distances = get_distances(doors)
    return max(distances.values())

def part2Answer(f):
    reg = f.read().strip()[1:-1]
    pos = Vector(0, 0)
    doors = set()
    find_doors(reg, pos, doors)
    distances = get_distances(doors)
    return len(filter(lambda x: x>=1000, distances.values()))

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

