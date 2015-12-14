def getCommandParts(com):
	parts = com.split()
	if parts[0] == "turn":
		parts = parts[1:]
	action = parts[0]
	(x1, y1) = parts[1].split(",")
	(x1, y1) = (int(x1), int(y1))
	(x2, y2) = parts[3].split(",")
	(x2, y2) = (int(x2), int(y2))
	return (action, (x1, y1), (x2, y2))	

def processCommand1(com, lights):
	(action, (x1, y1), (x2, y2)) = getCommandParts(com)
	for x in range(x1, x2+1):
		for y in range(y1, y2+1):
			if action == "on":
				lights[x][y] = 1
			elif action == "off":
				lights[x][y] = 0
			else:
				lights[x][y] = 1- lights[x][y]

def processCommand2(com, lights):
	(action, (x1, y1), (x2, y2)) = getCommandParts(com)
	for x in range(x1, x2+1):
		for y in range(y1, y2+1):
			if action == "on":
				lights[x][y] += 1
			elif action == "off":
				lights[x][y] = max(0, lights[x][y]-1)
			else:
				lights[x][y] += 2

def initLights():
	return [[0 for i in range(1000)] for j in range(1000)]

def countLights(lights):
	return sum([sum(row) for row in lights])

def part1Answer(f):
	lights = initLights()
	for line in f:
		processCommand1(line, lights)
	return countLights(lights)

def part2Answer(f):
	lights = initLights()
	for line in f:
		processCommand2(line, lights)
	return countLights(lights)


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

