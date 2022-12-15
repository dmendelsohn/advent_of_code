def part1Answer(triangles):
	count = 0
	for t in triangles:
		count += is_valid_triangle(t)
	return count

def part2Answer(triangles):
	count = 0
	for i in range(len(triangles)/3):
		for j in range(3):
			count += is_valid_triangle([triangles[3*i+k][j] for k in range(3)])
	return count

def is_valid_triangle(t):
	s = sorted(t)
	if s[0] + s[1] > s[2]:
		return 1
	else:
		return 0

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	lines = f.read().strip().split('\n')
	triangles = [[int(n) for n in l.split()] for l in lines]
	print("Part 1: %d" % (part1Answer(triangles),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(triangles),))

