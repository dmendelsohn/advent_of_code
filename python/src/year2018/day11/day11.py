N = 1723
MEMO = {}  # Map x,y,width,height to power in that rectangle

def power_level(x, y, n=N):
    power = x+10
    power *= y
    power += n
    power *= (x+10)
    power = (power/100)%10
    power -= 5
    return power

def get_max_box(min_side, max_side, n=N):
    maxsofar = 0
    maxloc = None
    for side in range(min_side, max_side+1):
        print('Checking side={}...so far maxloc={} with power {}'.format(side, maxloc, maxsofar))
        for x in range(1, 302-side):
            for y in range(1, 302-side):
                power = rect_power_level(x, y, side, side, n=n)
                if power > maxsofar:
                    maxsofar = power
                    maxloc = (x,y,side)
    return maxloc

# Assume either box, or nx1 situation, and that its in bounds
def rect_power_level(x, y, width, height, X=300, Y=300, n=N):
    global MEMO
    key = (x, y, width, height)
    if key in MEMO:
        return MEMO[key]

    if x+width-1 > X or y+height-1 > Y:
        raise ValueError('Out of bounds: {}'.format(key))

    if width == 1 and height == 1: # Case 1: cell, base case
        power = power_level(x, y, n)

    elif width == 1:  # Case 2: column
        power = rect_power_level(x, y, width, height-1, n=n)
        power += rect_power_level(x, y+height-1, 1, 1, n=n)  # So it gets memoized

    elif height == 1: # Case 3: row
        power = rect_power_level(x, y, width-1, height, n=n)
        power += rect_power_level(x+width-1, y, 1, 1, n=n)

    elif width == height:  # Case 4: square
        power = rect_power_level(x, y, width-1, height-1, n=n)
        power += rect_power_level(x+width-1, y, 1, height-1, n=n) # Right column
        power += rect_power_level(x, y+height-1, width-1, 1, n=n) # Bottom row
        power += rect_power_level(x+width-1, y+height-1, 1, 1, n=n) # Bottom-right corner

    else:
        raise ValueError('Invalid width, height: ({}, {})'.format(width, height))

    MEMO[key] = power
    return power

# For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29)
# For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30)

def part1Answer():
    return get_max_box(3, 3)

def part2Answer():
    return get_max_box(1, 300)

if __name__ == "__main__":
    print("Part 1: {}".format(part1Answer()))
    print("Part 2: {}".format(part2Answer()))

