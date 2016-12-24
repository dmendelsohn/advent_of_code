# Returns inst as op (str), src (int for const or str for reg), dest (int for offset, str for reg)
def parse_inst(text):
	parts = text.split()
	op = parts[0]
	if len(parts) == 2:
		return (op, parts[1], None)
	elif op == 'jnz':
		if parts[1] in 'abcd':  # jnz reg
			return (op, parts[1], int(parts[2]))
		else:  # jnz const
			return (op, int(parts[1]), int(parts[2]))
	else: # cpy
		if parts[1] in 'abcd':  # reg -> reg cpy
			return (op, parts[1], parts[2])
		else:	# const -> reg cpy
			return (op, int(parts[1]), parts[2])

def ex(inst, reg): # returns pc offset, modifies registers
	(op, src, dest) = inst
	if op == 'inc':
		reg[src] += 1
	elif op == 'dec':
		reg[src] -= 1
	elif op == 'jnz':
		if isinstance(src, int): # jnz const
			val = src
		else: # jnz reg
			val = reg[src]
		if val != 0:
			return dest
	else: # cpy
		if isinstance(src, int): # cpy const
			reg[dest] = src
		else: # cpy reg
			reg[dest] = reg[src]
	return 1 # All other cases return 1

def part1Answer(insts):
	pc = 0
	reg = {'a':0, 'b':0, 'c':0, 'd':0}
	while pc < len(insts):
		pc += ex(insts[pc], reg)
	return reg['a']

def part2Answer(insts):
	pc = 0
	reg = {'a':0, 'b':0, 'c':1, 'd':0}
	while pc < len(insts):
		pc += ex(insts[pc], reg)
	return reg['a']

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	i = [parse_inst(x) for x in f.read().strip().split('\n')]
	print("Part 1: %d" % (part1Answer(i),))
	print("Part 2: %d" % (part2Answer(i),))

