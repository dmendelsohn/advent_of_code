import itertools
from operator import mul

def getMinQ(weights, nGroups):
	groupWeight = sum(weights)/nGroups
	bestQ = reduce(mul, weights, 1)
	comboFound = False
	for r in range(len(weights)/nGroups):
		for combo in itertools.combinations(weights, r):
			if sum(combo) == groupWeight:
				comboFound = True
				q = reduce(mul, combo, 1)
				if q < bestQ:
					bestQ = q
		if comboFound:
			break
	return bestQ	

def part1Answer(weights):
	return getMinQ(weights, 3)

def part2Answer(weights):
	return getMinQ(weights, 4)

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	weights = [int(line) for line in f]
	print("Part 1: %d" % (part1Answer(weights),))
	print("Part 2: %d" % (part2Answer(weights),))

