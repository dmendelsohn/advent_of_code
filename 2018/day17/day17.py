import re
SOURCE = (500, 0)

def parse(f):
    lines = f.read().strip().split('\n')
    walls = set()  # Set of tuples for all solid cells
    for line in lines:
        PATTERN = '([xy])=([\d]+), ([xy])=([\d]+)..([\d]+)'
        groups = re.search(PATTERN, line).groups()
        fixed = int(groups[1])
        varied = range(int(groups[3]), int(groups[4])+1)
        for val in varied:
            if groups[0] == 'x':
                walls.add((fixed, val))
            else:
                walls.add((val, fixed))

    cells = {w: '#' for w in walls}
    cells[SOURCE] = '+'

    # Set up a helpful global var
    global MAXY
    MAXY = max(w[1] for w in walls)

    return cells

def pretty_print(cells):
    minx = min(c[0] for c in cells)
    maxx = max(c[0] for c in cells)
    miny = min(c[1] for c in cells)
    maxy = max(c[1] for c in cells)
    x_index = minx-1

    # Only print from minx-1 to maxx+1, and from 0 to maxy
    grid = [['.' for x in range(maxx-minx+3)] for y in range(maxy+1)]
    for key, value in cells.items():
        grid[key[1]][key[0]-x_index] = value

    settled = 0
    passed = 0
    walls = 0
    for row in grid:
        print(''.join(row))
        settled += row.count('~')
        passed += row.count('|')
        walls += row.count('#')
    print('x_index: {}, Settled: {}, Passed: {}, Walls: {}\n'.format(x_index, settled, passed, walls))


def count_reached(cells):
    wall_y_vals = {key[1] for key in cells if cells[key] == '#'}
    miny = min(wall_y_vals)
    maxy = max(wall_y_vals)
    reached = 0
    for key, value in cells.items():
        if miny <= key[1] <= maxy and value in ('~', '|', '+'):
            reached += 1
    return reached

def reach_cells(cells, loc, visited=None):
    if cells.get(loc) in ('~', '#'):
        return

    if loc[1] > MAXY:  # No need to go here
        return

    if visited is None:
        visited = set()

    if loc in visited:
        return
    else:
        visited.add(loc)
        if loc not in cells:
            cells[loc] = '|'
        else:
            assert cells[loc] == '|' or loc == SOURCE, 'loc={}, value={}'.format(loc, cells.get(loc))

    below = (loc[0], loc[1]+1)
    if cells.get(below) in ('#', '~'):  # Something solid in the way, look left and right
        reach_cells(cells, (loc[0]-1, loc[1]), visited)
        reach_cells(cells, (loc[0]+1, loc[1]), visited)
    else:
        reach_cells(cells, below, visited)


def in_cup(cells, loc):
    for step in (-1, 1):  # Two directions
        next_loc = loc
        while True:  # Iterate until we hit wall or find hole
            if cells.get(next_loc) == '#':  # Found the wall
                break

            below = (next_loc[0], next_loc[1]+1)
            if cells.get(below) not in ('#', '~'):  # Found the hole
                return False

            next_loc = (next_loc[0] + step, next_loc[1])

    return True  # No hole found


def place_water(cells, loc):
    # maxy = max(key[1] for key in cells)
    if loc[1] > MAXY:  # No need to go here
        return False

    below = (loc[0], loc[1]+1)
    left = (loc[0]-1, loc[1])
    right = (loc[0]+1, loc[1])
    if cells.get(below) not in ('~', '#'):  # Cell below is free
        return place_water(cells, below)

    if cells.get(left) not in ('~', '#'):  # Cell left is free
        cells[loc] = '~'  # Prevent backwach
        is_placed = place_water(cells, left)
        cells[loc] = '|'  # Undo temporary mark
        if is_placed:
            return True  # No need to continue

    if cells.get(right) not in ('~', '#'):  # Cell right is free
        cells[loc] = '~'
        is_placed = place_water(cells, right)
        cells[loc] = '|'
        if is_placed:
            return True  # No need to continue

    if in_cup(cells, loc):
        cells[loc] = '~'
        return True

    return False   # Could not hold water here


def add_water(cells):
    # Add one unit of water and mark cells as full/passed as such

    # First, recursively find all cells the new unit of water can reach
    reach_cells(cells, SOURCE)

    # Then, use the 'left-hand' method to place the new unit, return whether placement was successful
    return place_water(cells, SOURCE)


def part1Answer(f):
    cells = parse(f)
    i = 0
    while add_water(cells):
        print(i)
        i += 1
        #pretty_print(cells, False)
        pass
    return count_reached(cells)


def part2Answer(f):
    return 0

import sys
sys.setrecursionlimit(4000)
if __name__ == "__main__":
    f = open('input.txt', 'rt')
    #import cProfile
    #ans = cProfile.run('part1Answer(f)')
    ans = part1Answer(f)
    print("Part 1: {}".format(ans))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

