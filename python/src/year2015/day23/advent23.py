#Return (command, r, offset), where r and offset can be None if need be
def parseLine(line):
	parts = line.strip().split()
	com = parts[0]
	r = None
	offset = None
	if com == 'jmp':
		offset = int(parts[1])
	elif com == 'jie' or com == 'jio':
		r = parts[1].strip(',')
		offset = int(parts[2])
	else:
		r = parts[1]
	return (com, r, offset)

#Returns newPc, a, b
def execute(inst, pc, a, b):
	(com, r, offset) = inst
	if com == 'jmp':
		return (pc + offset, a, b)

	# r is guaranteed to be filled at this point
	if r == 'a':
		reg = a
	elif r == 'b':
		reg = b
	if com == 'jie' or com == 'jio':
		if (com == 'jie' and reg%2==0) or (com == 'jio' and reg==1):
			return (pc + offset, a, b)
		else:
			return (pc + 1, a, b)

	if com == 'hlf':
		op = lambda x: x/2
	elif com == 'tpl':
		op = lambda x: 3*x
	elif com == 'inc':
		op = lambda x: x+1
	
	if r == 'a':
		return (pc + 1, op(a), b)
	else:
		return (pc + 1, a, op(b))
		

def part1Answer(f):
	program = [parseLine(line) for line in f]
	pc, a, b = 0, 0, 0
	while pc < len(program):
		(pc, a, b) = execute(program[pc], pc, a, b)
	return b

def part2Answer(f):
	program = [parseLine(line) for line in f]
	pc, a, b = 0, 1, 0
	while pc < len(program):
		(pc, a, b) = execute(program[pc], pc, a, b)
	return b

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

