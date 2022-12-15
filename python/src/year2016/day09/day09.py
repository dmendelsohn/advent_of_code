import re

PAT = '\(\d+x\d+\)'

def decompress(text):
	pattern = re.compile(PAT)
	index = 0
	result = []
	while True:
		match = pattern.search(text, index)
		if not match:
			if index < len(text):
				result.append(text[index:]) # Add last string
			break
		start, end = match.span()
		result.append(text[index:start]) # Add string up til match to list
		parts = match.group()[1:-1].split('x')
		A = int(parts[0])
		B = int(parts[-1])
		repeat_text = text[end:end+A]
		result.extend([repeat_text]*B) # Add all the repeats
		index = end+A
	return ''.join(result)

def part1Answer(f):
	text = f.read().strip()
	decomp = decompress(text)
	return len(decomp)

def get_decomp_len(text):
	pattern = re.compile(PAT)
	index = 0
	total_len = 0
	while True:
		match = pattern.search(text, index)
		if not match: # We are done
			total_len += len(text) - index  #Account for any trailing text
			return total_len
		start, end = match.span()
		total_len += (start - index) # Add string length up til match
		parts = match.group()[1:-1].split('x')
		A = int(parts[0])
		B = int(parts[-1])
		repeat_text = text[end:end+A]
		total_len += (B * get_decomp_len(repeat_text))
		index = end+A

def part2Answer(f):
	text = f.read().strip()
	return get_decomp_len(text)

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

