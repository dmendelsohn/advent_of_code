OFFSET = {"^":(0,1), "v":(0,-1), "<": (-1, 0), ">":(1, 0)}

def getVisitedDict(moves):
	(x, y) = (0, 0)
	visited = {(x,y): None}
	for char in moves:
		if char in OFFSET:
			(dx, dy) = OFFSET[char]
		else:
			(dx, dy) = (0, 0)
		(x, y) = (x+dx, y+dy)
		visited[(x,y)] = None
	return visited

def part1Answer(line):
	return len(getVisitedDict(line))

def part2Answer(line):
	p1Moves = []
	p2Moves = []
	for i in range(len(line)):
		if i%2==0:
			p1Moves.append(line[i])
		else:
			p2Moves.append(line[i])
	p1Moves = "".join(p1Moves)
	p2Moves = "".join(p2Moves)
	p1Visited = getVisitedDict(p1Moves)
	p2Visited = getVisitedDict(p2Moves)
	union = set(p1Visited.keys() + p2Visited.keys())
	return len(union)


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	line = f.readline().strip()
	print("Part 1: %d" % (part1Answer(line),))
	print("Part 2: %d" % (part2Answer(line),))

