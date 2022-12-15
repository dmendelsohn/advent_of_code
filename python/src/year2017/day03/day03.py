INPUT = 277678
import math

def get_pos(num):
    level = int(math.sqrt(num-0.5))
    if level%2 == 0:
        level -= 1
    x_pos = 1 + level//2
    y_pos = -x_pos
    leftover = num - level**2
    y_pos += max(0, min(leftover, level+1))
    x_pos -= max(0, min(leftover-(level+1), level+1))
    y_pos -= max(0, min(leftover-2*(level+1), level+1))
    x_pos += max(0, min(leftover-3*(level+1), level+1))
    return abs(x_pos) + abs(y_pos)

def get_adjacent_sum(grid, x_pos, y_pos):
    total = 0
    for x_delta in range(-1, 2):
        for y_delta in range(-1, 2):
            total += grid.get((x_pos+x_delta, y_pos+y_delta), 0)
    total -= grid.get((x_pos, y_pos), 0)
    return total

def get_first_bigger(num):
    grid = {(0,0): 1}
    x_pos, y_pos = 1, -1
    side = 2
    while True:
        for (x_step, y_step) in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            for i in range(side):
                x_pos += x_step
                y_pos += y_step
                grid[(x_pos, y_pos)] = get_adjacent_sum(grid, x_pos, y_pos)
                if grid[(x_pos, y_pos)] > num:
                    return grid[(x_pos, y_pos)]
        side += 2
        x_pos += 1
        y_pos -= 1


def part1Answer():
    return get_pos(INPUT)

def part2Answer():
    return get_first_bigger(INPUT)

if __name__ == "__main__":
    print("Part 1: %d" % (part1Answer(),))
    print("Part 2: %d" % (part2Answer(),))

