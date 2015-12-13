def getRawLen(line):
	return len(line)

def getDecodedLen(line):
	return len(line.decode('string-escape')) - 2 #Subtract 2 for quotes

def getEncodedLen(line):
	num = len(line.encode('string-escape')) + 2 #Add 2 for quotes
	numQuotes = line.count('"') # Correct encode() problem with " character
	return num + numQuotes

def part1Answer(f):
	rawLenTotal = 0
	decodedLenTotal = 0
	for line in f:
		line = line.strip()
		rawLenTotal += getRawLen(line)
		decodedLenTotal += getDecodedLen(line)
	return rawLenTotal - decodedLenTotal

def part2Answer(f):
	rawLenTotal = 0
	encodedLenTotal = 0
	for line in f:
		line = line.strip()
		rawLenTotal += getRawLen(line)
		encodedLenTotal += getEncodedLen(line)
	return encodedLenTotal - rawLenTotal


if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

