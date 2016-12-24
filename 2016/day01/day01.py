DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
TURNS = {'R': 1, 'L': -1}


def part1Answer(f):
	cur_dir = 0
	cur_pos = (0,0)
	tokens = f.read().strip().split(' ')
	for token in tokens:
		token = token.strip(',')
		(turn, dist) = (TURNS[token[0]], int(token[1:]))
		cur_dir += turn
		cur_dir %= len(DIRS)
		new_x = cur_pos[0] + dist*DIRS[cur_dir][0]
		new_y = cur_pos[1] + dist*DIRS[cur_dir][1]
		cur_pos = new_x, new_y
	return abs(cur_pos[0]) + abs(cur_pos[1])

def part2Answer(f):
	cur_dir = 0
	cur_pos = (0, 0)
	visited = {cur_pos: None}
	tokens = f.read().strip().split(' ')
	for token in tokens:
		token = token.strip(',')
		(turn, dist) = (TURNS[token[0]], int(token[1:]))
		cur_dir += turn
		cur_dir %= len(DIRS)
		for i in range(dist):
			new_x = cur_pos[0] + DIRS[cur_dir][0]
			new_y = cur_pos[1] + DIRS[cur_dir][1]
			cur_pos = new_x, new_y
			if cur_pos in visited:
				return abs(cur_pos[0]) + abs(cur_pos[1])
			else:
				visited[cur_pos] = None
	return abs(cur_pos[0]) + abs(cur_pos[1])


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

