START = "1113222113"

# num is a string like "1112"
def lookAndSay(num):
	newNum = ""
	lastDigit = num[0]
	runCount = 0
	for digit in num:
		if digit == lastDigit:
			runCount += 1
		else:
			newNum += str(runCount) + lastDigit
			lastDigit = digit
			runCount = 1
	newNum += str(runCount) + lastDigit
	return newNum

def iterLookAndSay(start, numTimes):
	num = start
	for i in range(numTimes):
		num = lookAndSay(num)
	return num

def part1Answer():
	return len(iterLookAndSay(START, 40))

def part2Answer():
	return len(iterLookAndSay(START, 50))


if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(),))
	print("Part 2: %d" % (part2Answer(),))

