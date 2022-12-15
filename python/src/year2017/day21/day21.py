# Tile is a string of length 4 or 9 representing
# a square of spaces.  Return tile rotated 90 degrees.
def rotate(tile):
    if len(tile) == 4:
        return tile[2] + tile[0] + tile[3] + tile[1]
    elif len(tile) == 9:
        return tile[6] + tile[3] + tile[0] + tile[7] + tile[4] + tile[1] + tile[8] + tile[5] + tile[2]
    else:
        raise ValueError('Invalid tile: {}'.format(tile))

# Tile is a string of length 4 or 9 representing
# a square of spaces.  Return flipped about x axis
def flip(tile):
    if len(tile) == 4:
        return tile[2:] + tile[:2]
    elif len(tile) == 9:
        return tile[6:] + tile[3:6] + tile[:3]
    else:
        raise ValueError('Invalid tile: {}'.format(tile))


# Split 4x4 tile into 4 2x2 tiles
def split(tile):
    return [
        tile[0:2] + tile[4:6],
        tile[2:4] + tile[6:8],
        tile[8:10] + tile[12:14],
        tile[10:12] + tile[14:16]
    ]

def parse_input(f):
    tile_mappings = {}
    for line in f.read().strip().split('\n'):
        parts = line.replace('/', '').split(' ')
        key, value = parts[0], parts[2]
        for i in range(2):
            for j in range(4):
                tile_mappings[key] = value
                key = rotate(key)
            key = flip(key)
    return tile_mappings

def count_on(tilegrid):
    count = 0
    for tilerow in tilegrid:
        for tile in tilerow:
            count += tile.count('#')
    return count

def step(tilegrid, mapping):
    output = []
    for tilerow in tilegrid:
        toprow, bottomrow = [], []
        if len(tilerow[0]) == 4:
            for tile in tilerow:
                toprow.append(mapping[tile])
            output.append(toprow)
        elif len(tilerow[0]) == 9:
            for tile in tilerow:
                newtiles = split(mapping[tile]) # List of 4 tiles
                #print("DEBUG")
                #print(tile)
                #print(mapping[tile])
                #print(newtiles)
                toprow.extend(newtiles[:2])
                bottomrow.extend(newtiles[2:])
            output.append(toprow)
            output.append(bottomrow)
        else:
            raise ValueError("Invalid first tile in row: {}".format(tilerow[0]))
    return output


def print_tilerow(tilerow):
    top = ''
    middle = ''
    bottom = ''
    for tile in tilerow:
        if len(tile) == 4:
            top += tile[:2]
            middle += tile[2:]
        else:
            top += tile[:3]
            middle += tile[3:6]
            bottom += tile[6:]
    print(top)
    print(middle)
    if len(tilerow[0]) > 4:
        print(bottom)

def print_tilegrid(tilegrid):
    for tilerow in tilegrid:
        print_tilerow(tilerow)

def part1Answer(f):
    mapping = parse_input(f)
    tilegrid = [['.#...####']]
    for i in range(5):
        print('i = {}'.format(i))
        print_tilegrid(tilegrid)
        tilegrid = step(tilegrid, mapping)
    print("Final")
    print_tilegrid(tilegrid)
    return count_on(tilegrid)

def part2Answer(f):
    return 0

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

