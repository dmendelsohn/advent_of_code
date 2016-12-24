DIRS = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R':(1,0)}
NUMS_A = {
	(0, 2): '1',
	(1, 2): '2',
	(2, 2): '3',
	(0, 1): '4',
	(1, 1): '5',
	(2, 1): '6',
	(0, 0): '7',
	(1, 0): '8',
	(2, 0): '9'
}

NUMS_B = {
	(2, 4): '1',
	(1, 3): '2',
	(2, 3): '3',
	(3, 3): '4',
	(0, 2): '5',
	(1, 2): '6',
	(2, 2): '7',
	(3, 2): '8',
	(4, 2): '9',
	(1, 1): 'A',
	(2 ,1): 'B',
	(3, 1): 'C',
	(2, 0): 'D'
}

def part1Answer(f):
	insts = f.read().strip().split('\n')
	return solve_code(insts, (1, 1), NUMS_A)

def part2Answer(f):
	insts = f.read().strip().split('\n')
	return solve_code(insts, (0, 2), NUMS_B)

def solve_code(insts, start_pos, nums):
	code = ''
	cur_pos = start_pos
	for inst in insts:
		for let in inst:
			new_x = cur_pos[0] + DIRS[let][0]
			new_y = cur_pos[1] + DIRS[let][1]
			if (new_x, new_y) in nums:
				cur_pos = new_x, new_y
		code += nums[cur_pos]
	return code

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %s" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %s" % (part2Answer(f),))
