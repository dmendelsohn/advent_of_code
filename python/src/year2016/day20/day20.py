def is_overlapping(a, b):
	return a[0] <= b[0] <= a[1]+1 or b[0] <= a[0] <= b[1]+1

def merge(a, b):
	return min(a[0], b[0]), max(a[1], b[1])

def part1Answer(inp):
	first = inp[0]
	for b in inp[1:]:
		if is_overlapping(first,b):
			first = merge(first,b)
	return(first[1]+1)

def part2Answer(inp):
	spans = []
	current = inp[0]
	for b in inp[1:]:
		if is_overlapping(current,b):
			current = merge(current,b)
		else:
			spans.append(current) # End of current range
			current = b
	spans.append(current) # Append the last one
	allowed = 2**32
	for s in spans:
		allowed -= s[1]-s[0]+1
	return allowed

if __name__ == "__main__":
	lines = open('input.txt', 'rt').read().strip().split('\n')
	inp = [map(int, l.split('-')) for l in lines]
	inp = sorted([tuple(i) for i in inp])
	print(inp)
	print("Part 1: %s" % (str(part1Answer(inp)),))
	print("Part 2: %s" % (str(part2Answer(inp)),))

