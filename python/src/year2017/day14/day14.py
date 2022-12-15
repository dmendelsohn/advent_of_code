import operator

INPUT = 'stpzcrnm'
#INPUT = 'flqrgnkx'

def step(nums, index, span, skip):
    # Reverse nums[index:index+span], and return new (nums, index, skip)
    nums = nums[index:] + nums[:index] # Translate so index is at beginning
    if span: # Avoid 0 corner case
        nums[:span] = nums[span-1::-1] # Reverse span
    nums = nums[-index:] + nums[:-index] # Translate back
    return (nums, (index+span+skip)%len(nums), skip+1)

def condense(nums): # Condense 256 8-bit nums to 16 by XORing in groups of 16
    return [reduce(operator.xor, nums[i*16:(i+1)*16]) for i in range(16)]

def get_hex_string(nums): # Convert list of 16 [0-255] ints to 32 char hexstring
    return ''.join('%02x' % num for num in nums)

def knot_hash(key, num_rounds=1): # Return binary list
    spans = map(ord, key) + [17, 31, 73, 47, 23]
    nums = list(range(256))
    index, skip = 0, 0
    for i in range(num_rounds):
        for span in spans:
            nums, index, skip = step(nums, index, span, skip)
    return ''.join('{:08b}'.format(byte) for byte in condense(nums))

def part1Answer():
    rows = [knot_hash('{}-{}'.format(INPUT, i), 64) for i in range(128)]
    return sum(sum(int(c) for c in row) for row in rows)

def dfs(grid, seen, x, y):
    if grid.get((x,y)) and (x,y) not in seen: # Check that square is used and unseen
        seen.add((x,y))
        for (x_diff, y_diff) in [(0,-1),(0,1),(-1,0),(1,0)]:
            dfs(grid, seen, x+x_diff, y+y_diff)

def count_regions(grid):
    count = 0
    seen = set()
    for (x,y) in grid:
        if grid[(x,y)] and (x,y) not in seen:
            dfs(grid, seen, x, y)
            count += 1
    return count

def part2Answer():
    rows = [knot_hash('{}-{}'.format(INPUT, i), 64) for i in range(128)]
    grid = {}
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            grid[(i,j)] = int(rows[i][j])
    grid = {(i,j): int(rows[i][j]) for i in range(128) for j in range(128)}
    return count_regions(grid)

if __name__ == "__main__":
    print("Part 1: %d" % (part1Answer(),))
    print("Part 2: %d" % (part2Answer(),))

