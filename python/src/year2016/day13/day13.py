# (x,y) is open iff #1s in binary rep of (x*x + 3*x + 2*x*y + y + y*y + INPUT) is even
# (0-inf, 0-inf) is coord range
# find min steps from (1, 1) to (31, 39) (no diag steps allowed)

# Memoize walls, but I shouldn't really hit something twice

# Option 1: simple bfs
# Option 2: A* w/ taxicab heuristic
# Option 3: bi-directional bfs
INPUT = 1362
OPEN = {}
START = (1,1)
END = (31, 39)

def count_ones(val):
	if val == 0:
		return 0
	else:
		return val%2 + count_ones(val/2)

def is_open(coord):
	(x, y) = coord
	if x < 0 or y < 0:
		return False

	global OPEN
	if (x,y) in OPEN:
		return OPEN[(x,y)]
	else:
		result = (count_ones((x+y)**2 + 3*x + y + INPUT)%2 == 0)
		OPEN[(x,y)] = result
		return result

def get_neighbors(coord):
	(x, y) = coord
	neighbors = []
	for xd, yd in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
		if is_open((x+xd, y+yd)):
			neighbors.append((x+xd, y+yd))
	return neighbors

def bfs(start, end, max_steps=0):  # bfs through states
	visited = {start:None} # Initially no visited states, will map state to dist to that state
	queue = [(start, 0)] # Queue indicates to expand start state, 0 steps to get there
	while len(queue) > 0:
		coord, num_steps = queue.pop(0)
		if max_steps > 0 and num_steps >= max_steps:
			num_steps = -1
			break # We lose, couldn't find it
		if coord == end:
			break
		for n in get_neighbors(coord):
			if n not in visited:
				visited[n] = None
				queue.append((n, num_steps+1))
	return num_steps, len(visited)

def part1Answer():
	return bfs(START, END)[0]

def part2Answer():
	result = bfs(START, (-1, -1), 50)
	return result[1]

if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(),))
	print("Part 2: %d" % (part2Answer(),))

