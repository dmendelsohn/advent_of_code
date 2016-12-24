import itertools

X_LEN = 39
Y_LEN = 25

def parse(line):
	parts = line.split()
	subparts = parts[0].split('-')
	x = int(subparts[1][1:])
	y = int(subparts[2][1:])
	size = int(parts[1][:-1])
	used = int(parts[2][:-1])
	return ((x, y), size, used)


# Useful for debugging, assumes 2D array format, rather than dict format
def print_grid(grid):
	for y in range(Y_LEN):
		print ''.join(grid[y])

def make_array_grid(grid):
	return [[grid[(x,y)] for x in range(X_LEN)] for y in range(Y_LEN)]

def part1Answer(grid):
	def is_viable((a,b)):  # Can a go into b?  Each is (size, used)
		a_val, b_val = grid[a], grid[b]
		return 0 < a_val[1] <= (b_val[0]-b_val[1])
	return len(filter(is_viable, itertools.permutations(grid.keys(), 2)))

# 8 LEFT + 23 UP + 33 RIGHT gets '-' to top right + 5*37 to move G left 37 times

def part2Answer(grid):
	#a = sorted(grid.items(), key=lambda ((x,y),(size,used)): size-used, reverse=True)
	def classify((size,used)):
		if size - used > 40:
			return '-'  # Represents 'empty', initially just x=13, y=23
		elif size < 200:
			return '.' # Represents 'filled'
		else:
			return '#' # Represents 'wall'
	grid = {k:classify(grid[k]) for k in grid}
	grid[(38,0)] = 'G' # Represents 'special', the value we need to get to 0,0
	# print_grid(make_array_grid(grid)) # FOR DEBUGGING

	# The rest follows from observations from printed out grid
	EMPTY = (13, 23)
	GAP_X = 5 # Rightmost spot in 'gap' in the horizontal wall
	fewest = EMPTY[0]-GAP_X # Move empty spot left to the gap
	fewest += EMPTY[1] # Move up to op
	fewest += X_LEN-1-GAP_X # Move right to get empty to top right corner (and gets G to (X_LEN,0))
	fewest += 5 * (X_LEN-2) # 5 move sequence moves G to the left, need to do this X_LEN-2 times
	return fewest

if __name__ == "__main__":
	squares = map(parse, open('input.txt').read().strip().split('\n')[2:])
	grid = {s[0]:(s[1],s[2]) for s in squares}
	print("Part 1: %d" % (part1Answer(grid),))
	print("Part 2: %d" % (part2Answer(grid),))

