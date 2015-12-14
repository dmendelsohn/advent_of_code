PEOPLE = {\
		'Alice': 0 \
		, 'Bob': 1 \
		, 'Carol': 2 \
		, 'David': 3 \
		, 'Eric': 4 \
		, 'Frank': 5 \
		, 'George': 6 \
		, 'Mallory': 7 \
		}

#Returns (person1, person2, delta)
def parseLine(line):
	parts = line.strip()[:-1].split(' ')
	if parts[2] == 'gain':
		mult = 1
	elif parts[2] == 'lose':
		mult = -1
	return (PEOPLE[parts[0]], PEOPLE[parts[-1]], mult*int(parts[3]))

#Returns the happiness dictionary
#Keys = (person1, person2), values = delta
#Person1 gets delta happiness units by sitting next to person2
def buildHappyDict(f, includeSelf=False):
	happyDict = {}
	for line in f:
		(person1, person2, delta) = parseLine(line)
		happyDict[(person1, person2)] = delta
	if includeSelf:
		for i in range(len(PEOPLE)):
			happyDict[(i, len(PEOPLE))] = 0
			happyDict[(len(PEOPLE), i)] = 0
	return happyDict

def maxHappiness(happyDict, seating, remaining):
	if len(remaining) == 0:
		return getHappiness(happyDict, seating)
	else:
		options = []
		for i in remaining:
			newSeating = seating[:]
			newSeating.append(i)
			newRemaining = remaining[:]
			newRemaining.remove(i)
			options.append(maxHappiness(happyDict, newSeating, newRemaining))
		return max(options)

def getHappiness(happyDict, seating):
	total = 0
	for i in range(len(seating)):
		j = (i+1)%len(seating)
		p1 = seating[i]
		p2 = seating[j]
		total += happyDict[(p1, p2)]
		total += happyDict[(p2, p1)]
	return total

def part1Answer(f):
	happyDict = buildHappyDict(f)
	seating = [0]
	remaining = PEOPLE.values()
	remaining.remove(0)
	return maxHappiness(happyDict, seating, remaining)

def part2Answer(f):
	happyDict = buildHappyDict(f, True)
	seating = [0]
	remaining = PEOPLE.values() + [len(PEOPLE)]
	remaining.remove(0)
	return maxHappiness(happyDict, seating, remaining)

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

