INC = 'inc'
DEC = 'dec'
TGL = 'tgl'
CPY = 'cpy'
JNZ = 'jnz'
MUL = 'mul'  # My own instruction
TOGGLE = {INC: DEC, DEC: INC, TGL: INC, JNZ: CPY, CPY: JNZ}  # Defines how to toggle instructions

# Returns inst as op (str), src (int for const or str for reg), dest (int for offset, str for reg)
def parse_inst(text):
	parts = text.split()
	op = parts[0]
	if len(parts) == 2:
		src, dest = parts[1], None
	elif op == 'jnz':
		if parts[1] in 'abcd':  # jnz reg
			src = parts[1]
		else:  # jnz const
			src = int(parts[1])
		if parts[2] in 'abcd': # offset is from reg
			dest = parts[2]
		else: # offset is constant
			dest = int(parts[2])
	else: # cpy
		if parts[1] in 'abcd':  # reg -> reg cpy
			src = parts[1]
		else:	# const -> reg cpy
			src = int(parts[1])
		dest = parts[2]
	return (op, src, dest)

# From day12, added TGL and MUL support, JNZ with register value offset, and skipping invalid CPY insts
def ex(program, pc, reg): # returns pc offset, modifies registers and program
	(op, src, dest) = program[pc]
	if op == MUL:  # My own convenience instruction
		reg[src] *= reg[dest]
	elif op == TGL:
		pc_target = pc + reg[src]
		if 0 <= pc_target < len(program):
			old_inst = program[pc_target]
			program[pc_target] = TOGGLE[old_inst[0]], old_inst[1], old_inst[2]
	elif op == INC:
		reg[src] += 1
	elif op == DEC:
		reg[src] -= 1
	elif op == JNZ:
		if isinstance(src, int): # jnz const
			val = src
		else: # jnz reg
			val = reg[src]
		if val != 0:  # Do the jump
			if isinstance(dest, int):  # Offset is const
				return dest
			else:
				return reg[dest]  # Offset is reg value
	else: # cpy
		if isinstance(dest, int):  # This is an invalid copy
			pass  # No data to change
		elif isinstance(src, int): # cpy const
			reg[dest] = src
		else: # cpy reg
			reg[dest] = reg[src]
	return 1 # All other cases return 1

def part1Answer(program):
	pc = 0
	reg = {'a':7, 'b':0, 'c':0, 'd':0}
	while pc < len(program):
		pc += ex(program, pc, reg)
	return reg['a']


def part2Answer(program):
	new_block = [(MUL, 'a', 'b')] + [(CPY, 1,2)]*7  # Include 7 filler instructions, essentially NOP
	program = program[:2] + new_block + program[10:]  # Replace inefficient multiplication
	pc = 0
	reg = {'a':12, 'b':0, 'c':0, 'd':0}
	while pc < len(program):
		pc += ex(program, pc, reg)
	return reg['a']

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	i = [parse_inst(x) for x in f.read().strip().split('\n')]
	print("Part 1: %d" % (part1Answer(i[:]),))
	print("Part 2: %d" % (part2Answer(i[:]),))

