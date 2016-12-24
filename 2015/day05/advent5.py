BAD_STRINGS = ["ab", "cd", "pq", "xy"]

def containsThreeVowels(s):
	return len([None for let in s if let in "aeiou"]) >= 3

def containsDoubleLetter(s):
	prevLetter = None
	for letter in s:
		if letter==prevLetter:
			return True
		prevLetter = letter
	return False

def containsBadString(s):
	for bad in BAD_STRINGS:
		if bad in s:
			return True
	return False

def containsRepeatedPair(s):
	pairs = {}
	if len(s) < 4:
		return False
	lastTwo = s[:2]
	for letter in s[2:]:
		newLastTwo = lastTwo[1] + letter
		if newLastTwo in pairs:
			return True
		pairs[lastTwo] = None #Only now add previous two to dict
		lastTwo = newLastTwo
	return False

def containsSandwich(s):
	for i in range(len(s)-2):
		if s[i] == s[i+2]:
			return True
	return False

def isNice1(s):
	return containsThreeVowels(s) and containsDoubleLetter(s) \
			and not containsBadString(s)

def isNice2(s):
	return containsRepeatedPair(s) and containsSandwich(s)

def part1Answer(f):
	return len([line for line in f if isNice1(line)])

def part2Answer(f):
	return len([line for line in f if isNice2(line)])

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

