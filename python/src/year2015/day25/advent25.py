ROW = 3010
COL = 3019

START = 20151125
MULTIPLIER = 252533
MODULUS =  33554393

def getIndexInSeq(r, c):
	return (r+c-1)*(r+c-2)/2 + c

def step(num):
	return (num * MULTIPLIER)%MODULUS

def ithNum(start, i):
	num = start
	while i > 1:
		num = step(num)
		i -= 1
	return num

def part1Answer():
	return ithNum(START, getIndexInSeq(ROW, COL))

def part2Answer():
	return 0

if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(),))
	print("Part 2: %d" % (part2Answer(),))

