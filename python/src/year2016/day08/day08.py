HEIGHT = 6
WIDTH = 50

# Returns list of moves as ("rect" | "column" | "row", A, B)
def parse_file(f):
	lines = f.read().strip().split('\n')
	return [parse_line(line) for line in lines]

def parse_line(line):
	parts = line.split()
	if len(parts) == 2:
		op = parts[0]
		subparts = parts[1].split('x')
		A = int(subparts[0])
		B = int(subparts[-1])
	elif len(parts) == 5:
		op = parts[1]
		subparts = parts[2].split('=')
		A = int(subparts[-1])
		B = int(parts[4])
	else:
		print("Error parsing line %s" % (line,))
	return (op, A, B)

def do_move(grid, move):
	(op, A, B) = move
	if op == 'rect':
		for x in range(A):
			for y in range(B):
				grid[x][y] = True
	elif op == 'column': # x=A by B
		new_col = rotate_vect(grid[A], B)
		grid[A] = new_col
	elif op == 'row': #y=A by B
		old_row = [grid[x][A] for x in range(WIDTH)]
		new_row = rotate_vect(old_row, B)
		for x in range(WIDTH):
			grid[x][A] = new_row[x]
	else:
		print("Error doing operation %s" % (op,))

def rotate_vect(vect, num):
	num %= len(vect)
	return vect[-num:] + vect[:-num]

def print_grid(grid):
	s = ''
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if grid[x][y]:
				s += '#'
			else:
				s += '.'
		s += '\n'
	print(s)

def part1Answer(f):
	moves = parse_file(f)
	grid = [[False for y in range(HEIGHT)] for x in range(WIDTH)]
	for i in range(len(moves)):
		move = moves[i]
		do_move(grid, move)
	print_grid(grid)
	return sum([grid[i].count(True) for i in range(len(grid))])

def part2Answer(f):
	return 'See printed ASCII art string from Part 1'

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %s" % (part2Answer(f),))

