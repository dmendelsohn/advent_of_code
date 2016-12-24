PLACES = {\
		'Faerun': 0 \
		, 'Norrath': 1 \
		, 'Tristram': 2 \
		, 'AlphaCentauri': 3 \
		, 'Arbre' : 4 \
		, 'Snowdin': 5 \
		, 'Tambi' : 6 \
		, 'Straylight' : 7 \
		}

def getDistanceMap(f):
	distances = {}
	for line in f:
		(place1, place2, dist) = parseLine(line)
		distances[(place1, place2)] = dist
		distances[(place2, place1)] = dist
	return distances

def parseLine(line):
	parts = line.strip().split(' ')
	place1 = PLACES[parts[0]]
	place2 = PLACES[parts[2]]
	dist = int(parts[4])
	return (place1, place2, dist)

#Remaining includes the current one
#Current can be None if we can pick any current spot
def getPathDist(distances, current, remaining, func):
	if len(remaining) == 1:
		return 0
	else:
		if current != None and current in remaining:
			remaining.remove(current)
		options = []
		for nextPlace in remaining:
			if current is None:
				dist = 0
			else:
				dist = distances[(current, nextPlace)]
			rest = getPathDist(distances, nextPlace, remaining[:], func)
			options.append(dist + rest)
		return func(options)

def part1Answer(f):
	distances = getDistanceMap(f)
	return getPathDist(distances, None, PLACES.values(), min)

def part2Answer(f):
	distances = getDistanceMap(f)
	return getPathDist(distances, None, PLACES.values(), max)


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

