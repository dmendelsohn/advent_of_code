import hashlib

INPUT = 'yjjvjgan'
OPEN = 'bcdef'
MOVES = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]

ROWS, COLS = 4, 4
START = (0, 0)
GOAL = (3, 3)

def get_next_states(state):
	h = hashlib.md5(INPUT+state[0]).hexdigest()[:4]
	next_states = []
	for i in range(4):
		move = MOVES[i]
		n = state[0]+move[0], state[1]+move[1], state[2]+move[2]
		if h[i] in OPEN and 0 <= n[1] < ROWS and 0 <= n[2] < COLS:
			next_states.append(n)
	return next_states

def answer():
	queue = [('', START[0], START[1])]
	shortest, longest = '', ''
	while queue:
		state  = queue.pop(0)
		next_states = get_next_states(state)
		for n in next_states:
			if (n[1],n[2]) == GOAL:
				if shortest == '':
					shortest = n[0]
				longest = n[0]
			else:
				queue.append(n)
	return (shortest, longest)

if __name__ == "__main__":
	shortest, longest = answer()
	print("Part 1: %s" % (shortest,))
	print("Part 2: %d" % (len(longest),))
