#Note: I was going for speed on this one, not pretty code

def parseLine(line):
	parts = line.strip().split(' ')
	sueNum = int(parts[1].strip(':'))
	parts = parts[2:] #Just data now
	d = {}
	for i in range(len(parts)/2):
		attribute = parts[2*i].strip(':')
		num = parts[2*i+1].strip(',')
		d[attribute] = int(num)
	return (sueNum, d)

def sueIsMatch(d):
	if 'children' in d and d['children'] != 3:
		return False
	if 'cats' in d and d['cats'] != 7:
		return False
	if 'samoyeds' in d and d['samoyeds'] != 2:
		return False
	if 'pomeranians' in d and d['pomeranians'] != 3:
		return False
	if 'akitas' in d and d['akitas'] != 0:
		return False
	if 'vizslas' in d and d['vizslas'] != 0:
		return False
	if 'goldfish' in d and d['goldfish'] != 5:
		return False
	if 'trees' in d and d['trees'] != 3:
		return False
	if 'cars' in d and d['cars'] != 2:
		return False
	if 'perfumes' in d and d['perfumes'] != 1:
		return False
	return True

def sueIsMatch2(d):
	if 'children' in d and d['children'] != 3:
		return False
	if 'cats' in d and d['cats'] <= 7:
		return False
	if 'samoyeds' in d and d['samoyeds'] != 2:
		return False
	if 'pomeranians' in d and d['pomeranians'] >= 3:
		return False
	if 'akitas' in d and d['akitas'] != 0:
		return False
	if 'vizslas' in d and d['vizslas'] != 0:
		return False
	if 'goldfish' in d and d['goldfish'] >= 5:
		return False
	if 'trees' in d and d['trees'] <= 3:
		return False
	if 'cars' in d and d['cars'] != 2:
		return False
	if 'perfumes' in d and d['perfumes'] != 1:
		return False
	return True


def part1Answer(f):
	i = 1
	for line in f:
		num, d = parseLine(line)
		if sueIsMatch(d):
			return i
		else:
			i += 1
	return -1

def part2Answer(f):
	i = 1
	for line in f:
		num, d = parseLine(line)
		if sueIsMatch2(d):
			return i
		else:
			i += 1
	return -1



if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

