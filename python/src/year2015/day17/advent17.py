def getContainers(f):
	containers = [int(line.strip()) for line in f]
	return containers

def getCombinations(containers, numLiters):
	if len(containers) == 0:
		if numLiters == 0:
			return [[]]
		else:
			return []
	else:
		options = getCombinations(containers[1:], numLiters)
		if numLiters >= containers[0]:
			others = getCombinations(containers[1:], numLiters - containers[0])
			others = [[containers[0]] + l for l in others]
			options += others
		return options

def part1Answer(f):
	containers = getContainers(f)
	return len(getCombinations(containers, 150))

def part2Answer(f):
	containers = getContainers(f)
	options = getCombinations(containers, 150)
	minLen = min([len(o) for o in options])
	minOptions = [o for o in options if len(o) == minLen]
	return len(minOptions)

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

