import copy

def get_bounding_box(coords):
    minx = min(c[0] for c in coords)
    miny = min(c[1] for c in coords)
    maxx = max(c[0] for c in coords)
    maxy = max(c[1] for c in coords)
    return (minx, miny, maxx, maxy)

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Return a copy of the grid expanding all territory by 1, and marking ties with -1
def next_grid(grid):
    future_grid = copy.deepcopy(grid)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # print('Update {},{}?'.format(x,y))
            if grid[y][x] is not None:  # Already claimed
                continue
            resolved_next_val = None
            for d in DIRS:
                next_x = x + d[0]
                next_y = y + d[1]
                if 0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid):
                    next_val = grid[next_y][next_x]
                    if next_val is None:
                        pass  # Neighbor is empty, move on to next one
                    elif next_val == -1:
                        resolved_next_val = -1  # Neighbor is a tie, so we resolved to a tie
                    elif next_val == resolved_next_val:  # Neighbor is already what we're planning to set to
                        pass
                    # At this point, we've found a new claimant
                    elif resolved_next_val is None:  # Unclaimed!
                        resolved_next_val = next_val
                    elif resolved_next_val != -1:  # Tie, mark as such
                        resolved_next_val = -1
            # print('Setting to {}'.format(resolved_next_val))
            future_grid[y][x] = resolved_next_val
    return future_grid


def is_done(grid):
    for row in grid:
        if None in row:
            return False
    return True


def get_grid(coords):
    minx, miny, maxx, maxy = get_bounding_box(coords)
    grid = [[None for x in range(minx, maxx+1)] for y in range(miny, maxy+1)]
    # grid = {(x,y): None for x in range(minx, maxx+1) for y in range(miny, maxy+1)}
    for i, coord in enumerate(coords):
        #grid[coord] = i  # Seed the grid
        x, y = coord
        grid[y-miny][x-minx] = i  # Seed the grid
    return grid

# Get set of numbers that appear on the perimeter
def get_infinite_claims(grid):
    result = set()
    result.update(grid[0])  # Add top row
    result.update(grid[-1]) # Add bottom row
    result.update(grid[y][0] for y in range(len(grid)))  # Left
    result.update(grid[y][-1] for y in range(len(grid)))  # Right
    return result


def get_freqs(grid):
    freqs = {}
    for row in grid:
        for elt in row:
            freqs[elt] = freqs.get(elt, 0) + 1
    return freqs

def print_grid(grid):
    chars = list('GRID:\n')
    for row in grid:
        for elt in row:
            if elt is None:
                chars.append(' ')
            elif elt == -1:
                chars.append('.')
            else:
                chars.append(chr(65+elt))
        chars.append('\n')
    print(''.join(chars))

def parse(f):
    lines = f.read().strip().split('\n')
    coords = []
    for line in lines:
        parts = line.split(', ')
        coords.append((int(parts[0]), int(parts[1])))
    return coords

def part1Answer(f):
    coords = parse(f)
    grid = get_grid(coords)
    # print_grid(grid)
    while not is_done(grid):
        grid = next_grid(grid)
        # print_grid(grid)
    infinite_claims = get_infinite_claims(grid)
    print(infinite_claims)
    freqs = get_freqs(grid)
    print(freqs)
    for claim in infinite_claims:
        del freqs[claim]
    print(freqs)
    return max(freqs.values())


MAX_COST = 32  # Test
MAX_COST = 10000 # For real

def get_cost_of_value(locs, val):
    cost = 0
    for loc in locs:
        cost += abs(val - loc)
    return cost


def get_cost_lookup(locs):  # Just one dimenion
    locs = sorted(locs)
    median = locs[len(locs)/2]
    lut = {}
    i = median
    for offset in (-1, 1):
        while True:
            cost = get_cost_of_value(locs, i)
            lut[i] = cost
            if cost >= MAX_COST:
                i = median  # Reset
                break
            i += offset
    return lut


def part2Answer(f):
    coords = parse(f)
    x_costs = get_cost_lookup([c[0] for c in coords])
    print(x_costs)
    y_costs = get_cost_lookup([c[1] for c in coords])
    print(y_costs)
    count = 0
    for x in x_costs:
        for y in y_costs:
            if x_costs[x] + y_costs[y] < MAX_COST:
                count += 1
    return count


if __name__ == "__main__":
    f = open('input.txt', 'rt')
    #print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

