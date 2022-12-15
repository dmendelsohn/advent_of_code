import json

def addAllNumbers(obj, exclude=None):
	total = 0
	if isinstance(obj, dict):
		if exclude != None and exclude in obj.values():
			return 0 # We found an excluded object
		else:
			for elt in obj.values():
				total += addAllNumbers(elt, exclude)
	elif isinstance(obj, list):
		for elt in obj:
			total += addAllNumbers(elt, exclude)
	elif isinstance(obj, str):
		pass
	elif isinstance(obj, int):
		total += obj
	return total

def part1Answer(f):
	jsonText = f.read()
	obj = json.loads(jsonText)
	return addAllNumbers(obj)

def part2Answer(f):
	jsonText = f.read()
	obj = json.loads(jsonText)
	return addAllNumbers(obj, 'red')

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

