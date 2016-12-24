from collections import Counter

def part1Answer(f):
	lines = f.read().strip().split('\n')
	password = ""
	for i in range(len(lines[0])):
		all_chars = [l[i] for l in lines]
		password += Counter(all_chars).most_common(1)[0][0]
	return password

def part2Answer(f):
	lines = f.read().strip().split('\n')
	password = ""
	for i in range(len(lines[0])):
		all_chars = [l[i] for l in lines]
		password += Counter(all_chars).most_common()[-1][0]
	return password

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %s" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %s" % (part2Answer(f),))

