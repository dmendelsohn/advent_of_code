def contains_abba(text):
	for i in range(len(text)-3):
		if is_abba(text[i:i+4]):
			return True
	return False

def is_abba(text):
	return len(text) == 4 and text[0] == text[3] \
			and text[1] == text[2] and text[0] != text[1]

def is_aba(text):
	return len(text) == 3 and text[0] == text[2] and text[0] != text[1]

def supports_tls(line):
	line += '[' # Add marker at end
	word = ''
	in_count, out_count = 0, 0
	for c in line:
		if c == '[':
			if contains_abba(word):
				out_count += 1
			word = ''
		elif c == ']':
			if contains_abba(word):
				in_count += 1
			word = ''
		else:
			word += c
	return out_count > 0 and in_count == 0

def extract_aba(text):
	aba_seqs = []
	for i in range(len(text)-2):
		if is_aba(text[i:i+3]):
			aba_seqs.append(text[i:i+3])
	return aba_seqs

def supports_ssl(line):
	line += '['
	aba_ins = []
	aba_outs = []
	word = ''
	for c in line:
		if c == '[':
			aba_outs.extend(extract_aba(word))
			word = ''
		elif c == ']':
			aba_ins.extend(extract_aba(word))
			word = ''
		else:
			word += c

	d = {}
	for aba in aba_outs:  # Populate dict
		d[(aba[0], aba[1])] = None
	for aba in aba_ins:
		if (aba[1], aba[0]) in d:
			return True
	return False

def part1Answer(f):
	lines = f.read().strip().split('\n')
	count = 0
	for line in lines:
		if supports_tls(line):
			count += 1
	return count

def part2Answer(f):
	lines = f.read().strip().split('\n')
	count = 0
	for line in lines:
		if supports_ssl(line):
			count += 1
	return count

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

