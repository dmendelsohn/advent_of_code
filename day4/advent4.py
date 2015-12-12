import hashlib

MY_KEY = "yzbqklnj"

def md5(string):
	m = hashlib.md5()
	m.update(string)
	return m.hexdigest()

def getFirstWithHashPrefix(myKey, match):
	num = 1
	while md5(myKey+str(num))[:len(match)] != match:
		num += 1
	return num

def part1Answer(myKey):
	return getFirstWithHashPrefix(myKey, "00000")

def part2Answer(myKey):
	return getFirstWithHashPrefix(myKey, "000000")


if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(MY_KEY),))
	print("Part 2: %d" % (part2Answer(MY_KEY),))

