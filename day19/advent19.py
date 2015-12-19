#Excuse the lack of comments, this is one-off code, not for reuse
import re

LEFT_PAREN = 'Rn'
COMMA = 'Y'
RIGHT_PAREN = 'Ar'
	
def parseInput(f, reverse=False):
	lines = []
	for line in f:
		lines.append(line.strip())
	lines, start = lines[:-1], lines[-1]
	mappings = {} #Maps to a tuple of things we can map to
	for line in lines:
		if line != '':
			parts = line.split(' ')
			if reverse:
				key, value = parts[2], parts[0]
			else:
				key, value = parts[0], parts[2]
			if key in mappings:
				mappings[key] += (value,)
			else:
				mappings[key] = (value,)
	return mappings, start

def tokenize(molecule):
	result = []
	i = 0
	while i < len(molecule):
		if molecule[i].isupper() and (i+1) < len(molecule) \
				and molecule[i+1].islower():
			result.append(molecule[i:i+2])
			i += 2
		else:
			result.append(molecule[i])
			i += 1
	return result

#Parses 'element' tokens to find the embedded 'tuples'
def parse(tokens):
	if len(tokens) == 0:
		return []
	elif tokens[0] == LEFT_PAREN:
		i = 1
		j = findMatchingRightParen(tokens, 0)
		parsed = ()
		clause = []
		while i < j:
			if tokens[i] == LEFT_PAREN:
				nextI = findMatchingRightParen(tokens, i)
				clause.append(parse(tokens[i:nextI])[0])
				i = nextI
			elif tokens[i] == COMMA or tokens[i] == RIGHT_PAREN:
				parsed += (clause[:],)
				clause = []
				i += 1
			else:
				clause.append(tokens[i])
				i += 1
		return [parsed] + parse(tokens[i:])	
	else:
		return [tokens[0]] + parse(tokens[1:])

# Tokens is a list of tokens, i is the position of the left paren to be matched
# Returns first index AFTER matching right paren
def findMatchingRightParen(tokens, i):
	j = i + 1
	parenDiffCount = 1
	while parenDiffCount > 0:
		if tokens[j] == LEFT_PAREN:
			parenDiffCount += 1
		elif tokens[j] == RIGHT_PAREN:
			parenDiffCount -= 1
		j += 1
	return j

def getNumReductions(parsed_token):
	if isinstance(parsed_token, list):
		num = sum([getNumReductions(elt) for elt in parsed_token])
	elif isinstance(parsed_token, tuple):
		num = sum([getNumReductions(elt) for elt in parsed_token]) \
				- len(parsed_token) + 1
	else:
		num = 1
	return num

def getOutputs(mappings, start):
	outputs = []
	for key in mappings:
		indices = [m.start() for m in re.finditer(key, start)]
		for index in indices:
			for replacement in mappings[key]:
				output = start[:index] + replacement + start[index+len(key):]
				outputs.append(output)
	return list(set(outputs))

def part1Answer(f):
	mappings, start = parseInput(f)
	return len(getOutputs(mappings, start))

def part2Answer(f):
	mappings, start = parseInput(f)
	tokens = tokenize(start)
	parsed = parse(tokens)
	return getNumReductions(parsed) - 1

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

