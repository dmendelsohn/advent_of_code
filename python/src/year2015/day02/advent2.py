def getWrappingNeeded(dims):
	(w, h, l) = dims
	return 2*(w*h + w*l + h*l) + min(w*h, w*l, h*l)

def getRibbonNeeded(dims):
	(w, h, l) = dims
	return w*h*l + 2*min(w+h, w+l, h+l)

def getDimensions(string):
	l = string.split("x")
	(w, h, l) = int(l[0]), int(l[1]), int(l[2])
	return (w, h, l)

def part1Answer(f):
	return sum([getWrappingNeeded(getDimensions(line)) for line in f])

def part2Answer(f):
	return sum([getRibbonNeeded(getDimensions(line)) for line in f])

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))


