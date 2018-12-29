def parse(f):
    #return [list(line) for line in f.read().strip().split('\n')]
    return f.read().strip().split('\n')


def print_grid(grid):
    print('')
    for row in grid:
        print(''.join(row))
    print('')

OPEN = '.'
TREE = '|'
LUMBER = '#'

# Return open, tree, lumber surroundings
def summarize_surroundings(grid, x, y):
    offsets = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            offsets.add((i, j))
    offsets.remove((0, 0))
    neighbors = []
    for offset in offsets:
        newx = x + offset[0]
        newy = y + offset[1]
        if 0 <= newy < len(grid) and 0 <= newx < len(grid[0]):
            neighbors.append(grid[newy][newx])
    num_open = neighbors.count(OPEN)
    num_tree = neighbors.count(TREE)
    num_lumber = neighbors.count(LUMBER)
    return num_open, num_tree, num_lumber


def get_next_cell(grid, x, y):
    num_open, num_tree, num_lumber = summarize_surroundings(grid, x, y)
    next_cell = grid[y][x]  # Initially assume no change
    if grid[y][x] == OPEN:
        if num_tree >= 3:
            next_cell = TREE
    elif grid[y][x] == TREE:
        if num_lumber >= 3:
            next_cell = LUMBER
    else:
        if num_tree == 0 or num_lumber == 0:
            next_cell = OPEN
    return next_cell


def get_next_grid(grid):
    return [''.join([get_next_cell(grid, x, y) for x in range(len(grid[0]))]) for y in range(len(grid))]


def get_score(grid):
    num_tree = 0
    num_lumber = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == TREE:
                num_tree += 1
            elif grid[y][x] == LUMBER:
                num_lumber += 1
    return num_tree * num_lumber


def part1Answer(f):
    grid = parse(f)
    print_grid(grid)
    for i in range(10):
        grid = get_next_grid(grid)
        print_grid(grid)
    return get_score(grid)

# 178856 is too low
def part2Answer(f):
    grid = parse(f)

    NUM_ITERS = 1000000000
    CYCLE_LENGTH = 28
    CYCLE_START = 460

    MEMO = {}

    i = 0
    while True:
        i += 1
        key = '\n'.join(grid)
        if key in MEMO:
            grid = MEMO[key]
        else:
            print('cache miss')
            grid = get_next_grid(grid)
            MEMO[key] = grid

        score = get_score(grid)
        print(i, score)


        if i >= CYCLE_START and (NUM_ITERS - i)%CYCLE_LENGTH == 0:
            return score

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

