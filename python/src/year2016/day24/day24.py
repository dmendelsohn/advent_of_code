from Queue import Queue
import itertools
DIRS = [(0,1),(1,0),(0,-1),(-1,0)]


# These will get filled in
def parse(lines):
	return {(i,j):lines[i][j] for i in range(len(lines)) for j in range(len(lines[0]))}

def process(grid):  # returns grid dict of True for empty, False for wall, and dict of all waypoints
	waypoints = {}
	for coord in grid:
		try:
			num = int(grid[coord])
			waypoints[num] = coord
		except:
			pass  # Most of the time it won't work
	grid = {c:(grid[c] != '#') for c in grid}
	return grid, waypoints

def get_neighbors(grid, (x,y)):
	neighbors = []
	for d in DIRS:
		coord = x+d[0], y+d[1]
		if coord in grid and grid[coord]:
			neighbors.append(coord)
	return neighbors

def shortest_path(grid, start, end):  # BFS
	queue = Queue()
	visited = set()
	queue.put((start,0))
	visited.add(start)
	while not queue.empty():
		(coord, step) = queue.get()
		neighbors = get_neighbors(grid, coord)
		for n in neighbors:
			if n == end:
				return step + 1
			elif n not in visited:
				queue.put((n, step+1))
				visited.add(n)
	return -1 # Could not find path 

def answer(grid, waypoints, part):
	dists = {}  # Maps (waypoint, waypoint) keys to distance between those waypoints
	for (a,b) in itertools.combinations(waypoints.keys(), 2):
		dist = shortest_path(grid, waypoints[a], waypoints[b])
		dists[(a,b)] = dist
		dists[(b,a)] = dist
	print(dists)
	print(waypoints)

	# Now it's a traveling salesman problem
	best = 10**10 # Way to big, obviously
	del waypoints[0]  # We don't really need waypoints, other than to keep track of which waypoints we have
	for p in itertools.permutations(waypoints.keys()):  # Not including 0 since we MUST start with it
		p = (0,) + p  # add zero to front of waypoint order tuple
		if part == 1:
			start = 1
		else:
			start = 0
		total = sum(dists[(p[i-1],p[i])] for i in range(start, len(p)))
		best = min(best, total)
	return best

if __name__ == "__main__":
	lines = open('input.txt', 'rt').read().strip().split('\n')
	grid = parse(lines)
	grid, waypoints = process(grid)
	print("Part 1: %d" % (answer(grid, waypoints.copy(), 1),))
	print("Part 2: %d" % (answer(grid, waypoints.copy(), 2),))

