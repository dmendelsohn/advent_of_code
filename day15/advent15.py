import operator
import functools

# Returns tuple (ingredient, (capacity, durability, flavor, texture, calories))
def parseIngredient(line):
	parts = line.strip().split(' ')
	name = parts[0].strip(':')
	return (name, tuple([int(parts[2*(i+1)].strip(',')) for i in range(5)]))

def buildIngredientDict(f):
	d = {}
	for line in f:
		(key, val) = parseIngredient(line)
		d[key] = val
	return d

# ingredDict - maps names to attribute tuple
# countDict - maps names to num tablespoons used
# Two dicts must have same keys
# exactColories - if given, anything with a different # of calories is score 0
def computeScore(ingredDict, countDict, exactCalories=None):
	totals = []
	for i in range(5):
		subtotal = 0
		for key in countDict:
			count = countDict[key]
			attributeScore = ingredDict[key][i]
			subtotal += count*attributeScore
		totals.append(max(subtotal, 0))
	if exactCalories is not None and totals[-1] != exactCalories:
		return 0 #Invalid recipe
	else:
		return functools.reduce(operator.mul, totals[:-1], 1)

def computeBestScore(ingredDict, countDictSoFar, numTeaspoonsLeft, \
		exactCalories=None):
	ingredDict = ingredDict.copy()
	countDictSoFar = countDictSoFar.copy()
	if len(ingredDict) == len(countDictSoFar):
		return computeScore(ingredDict, countDictSoFar, exactCalories)
	else:
		ingreds = ingredDict.keys()
		for ingred in countDictSoFar:
			ingreds.remove(ingred)
		nextIngred = ingreds[0]
		if len(ingreds) == 1: #Only one ingredient left
			countDictSoFar[nextIngred] = numTeaspoonsLeft
			return computeBestScore(ingredDict, countDictSoFar, 0, \
					exactCalories)
		else: # Multiple ingredients left
			options = []
			for i in range(numTeaspoonsLeft+1):
				countDictSoFar[nextIngred] = i
				options.append(computeBestScore(ingredDict, countDictSoFar, \
						numTeaspoonsLeft - i, exactCalories))
			return max(options)

def part1Answer(f):
	ingredDict = buildIngredientDict(f)
	return computeBestScore(ingredDict, {}, 100)

def part2Answer(f):
	ingredDict = buildIngredientDict(f)
	return computeBestScore(ingredDict, {}, 100, 500)


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

