def getGrid(f):
	grid = []
	for line in f:
		line = line.strip()
		row = []
		for char in line:
			if char == '#':
				row.append(True)
			elif char == '.':
				row.append(False)
		grid.append(row)
	return grid

def step(grid, cornersStuck=False):
	n = len(grid)
	new_grid = []
	for row in range(n):
		new_grid.append([False]*n)
	for i in range(n):
		for j in range(n):
			neighbors = getNumAdjacent(grid, i, j)
			if grid[i][j]:
				if neighbors == 2 or neighbors == 3:
					new_grid[i][j] = True
			if not grid[i][j]:
				if neighbors == 3:
					new_grid[i][j] = True
	if cornersStuck:
		turnOnCorners(new_grid)
	return new_grid

def turnOnCorners(grid):
	n = len(grid)
	grid[0][0] = True
	grid[0][n-1] = True
	grid[n-1][0] = True
	grid[n-1][n-1] = True

def getNumAdjacent(grid, i, j):
	count = 0
	n = len(grid)
	for a in range(i-1, i+2):
		for b in range(j-1, j+2):
			if ((a != i or b != j) and a >= 0 and b >= 0 and a < n and b < n \
					and grid[a][b]):
				count += 1
	return count

def getCount(grid, val):
	count = 0
	for row in grid:
		for elt in row:
			if elt == val:
				count += 1
	return count

def part1Answer(f):
	grid = getGrid(f)
	for i in range(100):
		grid = step(grid)
	return getCount(grid, True)


def part2Answer(f):
	grid = getGrid(f)
	turnOnCorners(grid)
	for i in range(100):
		grid = step(grid, True)
	return getCount(grid, True)

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

