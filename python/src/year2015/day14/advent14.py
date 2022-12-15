def parseLine(line):
	parts = line.strip().split(' ')
	name = parts[0]
	speed = int(parts[3])
	flyTime = int(parts[6])
	restTime = int(parts[13])
	return (name, speed, flyTime, restTime)

def getDistanceTraveled(speed, flyTime, restTime, timeElapsed):
	cycles = int(timeElapsed/(flyTime+restTime))
	distance = speed*flyTime*cycles
	leftOverTime = timeElapsed - cycles*(flyTime+restTime)
	distance += speed*min(flyTime, leftOverTime)
	return distance

def getReindeer(f):
	return [parseLine(line) for line in f]

def getFarthestDistance(reindeer, numSeconds):
	distances = []
	for r in reindeer:
		dist = getDistanceTraveled(r[1], r[2], r[3], numSeconds)
		distances.append(dist)
	longest = max(distances)
	winners = []
	for i in range(len(reindeer)):
		if distances[i] == longest:
			winners.append(reindeer[i][0])
	return longest, winners

def getWinningPoints(f):
	reindeer = getReindeer(f)
	points = {}
	for r in reindeer:
		points[r[0]] = 0
	for i in range(1, 2504):
		longest, winners = getFarthestDistance(reindeer, i)
		for name in winners:
			points[name] += 1
	return max(points.values())

def part1Answer(f):
	return getFarthestDistance(getReindeer(f), 2503)[0]

def part2Answer(f):
	return getWinningPoints(f)


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

