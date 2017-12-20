def parse_input(f):
    lines = f.read().split('\n')
    grid = {}
    for y in range(len(lines)):
        line = lines[y]
        line = line.replace(' ', '.') # Because whitespace is annoying
        for x in range(len(line)):
            grid[(x,y)] = line[x]
    return grid

def find_start_x(grid):
    x = 0
    while grid.get((x,0), '.') == '.':
        x += 1
    return x

# Return newloc, newvec
def step(grid, loc, vec, letters):
    if grid.get(loc, '.') == '.': # If we reach empty space, we're done.  Indicate by putting '.' at end of letters
        letters.append('.')
        return loc, dir
    elif grid.get(loc, '.') == '+':
        newvec = 1-abs(vec[0]), 1-abs(vec[1]) # Orthogonal
        newloc = (loc[0]+newvec[0], loc[1]+newvec[1])
        if grid.get(newloc, '.') != '.': # We found the correct turn
            return newloc, newvec
        newvec = (-newvec[0], -newvec[1]) # Other orthogonal
        newloc = (loc[0]+newvec[0], loc[1]+newvec[1])
        if grid.get(newloc, '.') != '.': # We found the correct turn
            return newloc, newvec
        raise Exception # Neither turn worked
    elif grid.get(loc, '.') in '-|':
        return (loc[0]+vec[0], loc[1]+vec[1]), vec # Step in same direction
    else: # We found a letter
        letters.append(grid.get(loc, '.'))
        return (loc[0]+vec[0], loc[1]+vec[1]), vec # Step in same direction
        


def answer(f, part):
    grid = parse_input(f)
    loc = find_start_x(grid), 0
    vec = (0, 1)
    letters = [] # List of chars
    count = 0
    while not (letters and letters[-1] == '.'):
        loc, vec = step(grid, loc, vec, letters)
        count += 1
    if part==1:
        return ''.join(letters[:-1])
    else:
        return count-1 # Overcount by stepping past

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(answer(f,1)))
    f.seek(0)
    print("Part 2: {}".format(answer(f,2)))

