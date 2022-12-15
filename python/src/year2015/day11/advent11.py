BAD_LETTERS = ['i', 'o', 'l']
ALPHABET = 'abcdefghijklmnopqrstuvxyz'
PASSWORD = 'hxbxwxba'

def getRuns():
	runs = []
	run = 'abc'
	while run != 'xyz':
		runs.append(run)
		run = run[1:] + increment(run[-1])
	runs.append(run)
	return runs

def containsRun(password):
	for run in getRuns():
		if run in password:
			return True
	return False

def containsBadLetter(password):
	for letter in BAD_LETTERS:
		if letter in password:
			return True
	return False

def containsTwoRepeats(password):
	numRepeats = 0
	for letter in ALPHABET:
		double_letter = letter + letter
		if double_letter in password:
			numRepeats += 1
	return numRepeats >= 2		

def isValidPassword(password):
	return containsRun(password) and not containsBadLetter(password) \
			and containsTwoRepeats(password)

# Increments a fixed length alphanumeric string
def increment(string):
	if string[-1] != 'z':
		return string[:-1] + chr(ord(string[-1]) +1)
	elif len(string) == 1:
		raise ValueError("Cannot increment all Z string")
	else:
		return increment(string[:-1]) + 'a'
			
def nextPassword(password, func):
	password = increment(password)
	while not func(password):
		password = increment(password)
	return password

def part1Answer():
	return nextPassword(PASSWORD, isValidPassword)

def part2Answer():
	password = nextPassword(PASSWORD, isValidPassword)
	return nextPassword(password, isValidPassword)

if __name__ == "__main__":
	print("Part 1: %s" % (part1Answer(),))
	print("Part 2: %s" % (part2Answer(),))

