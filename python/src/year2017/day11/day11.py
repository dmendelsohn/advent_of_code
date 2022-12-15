DIST = {
    'n': (0, 2),
    'nw': (-1, 1),
    'ne': (1, 1),
    's': (0, -2),
    'sw': (-1, -1),
    'se': (1, -1)
}

def parse_input(f):
    return f.read().strip().split(',')

def get_distance(x_pos, y_pos):
    x_pos, y_pos = abs(x_pos), abs(y_pos)
    diag_steps = x_pos
    y_pos = max(y_pos - x_pos, 0)
    return diag_steps + y_pos // 2

def answer(f, part):
    steps = parse_input(f)
    (x_pos, y_pos) = (0, 0)
    max_dist = 0
    for step in steps:
        delta = DIST[step]
        x_pos += delta[0]
        y_pos += delta[1]
        max_dist = max(max_dist, get_distance(x_pos, y_pos))
    if part==1:
        return get_distance(x_pos, y_pos)
    elif part==2:
        return max_dist

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (answer(f,1),))
    f.seek(0)
    print("Part 2: %d" % (answer(f,2),))

