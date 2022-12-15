import itertools
import copy
from Queue import PriorityQueue

PRINT_INTERVAL = 10000

ELTS_1 = {'thulium':0, 'plutonium':1, 'strontium':2, 'promethium':3, 'ruthenium':4} 
ELTS_2 = {'thulium':0, 'plutonium':1, 'strontium':2, 'promethium':3, 'ruthenium':4, \
		'elerium':5, 'dilithium':6}
NUM_FLOORS = 4

GOAL_1 = (3, (3, 3), (3, 3), (3, 3), (3, 3), (3, 3))
GOAL_2 = (3, (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3))

# state is dict of locs, where keys are 'G0'...'G4', 'M0'...'M4', and 'E'
def dict_to_tuple(state):
	elts = [(state['M'+str(i)], state['G'+str(i)]) for i in range(NUM_ELTS)]
	return tuple([state['E']] + sorted(elts))

# state tuple is (elevator_pos, (M G), (M G)...) sorted MG pairs
def tuple_to_dict(state): # Convert tuple of two-tuples to dict
	d = {}
	d['E'] = state[0]
	for i in range(NUM_ELTS):
		d['M'+str(i)] = state[i+1][0]
		d['G'+str(i)] = state[i+1][1]
	return d

def parse_input(f, elts): # returns initial state
	lines = f.read().strip().split('\n')
	state = {'E':0} # Elevator starts on 1st floor
	for i in range(NUM_FLOORS): # Should be 4 lines
		for elt in elts:
			if (elt + ' gen') in lines[i]:
				state['M' + str(elts[elt])] = i
			if (elt + '-comp') in lines[i]:
				state['G' + str(elts[elt])] = i
	return dict_to_tuple(state)

def is_okay(state_dict):
	has_gen = [False]*NUM_FLOORS
	for num in range(NUM_ELTS):
		has_gen[state_dict["G"+str(num)]] = True
	for num in range(NUM_ELTS):
		m_floor = state_dict['M'+str(num)]
		if has_gen[m_floor] and state_dict['G'+str(num)] != m_floor:
			return False
	return True
		
# Move elevator and 1-2 of the items on its floor to an adjacent floor
# Reject if elevator would fry a chip, or any destination floor would fry a chip
# Input and output in tuple of tuple format
def get_next_states(state):
	d = tuple_to_dict(state)
	cur_floor = d['E']
	del d['E']
	floors = [[] for i in range(NUM_FLOORS)]
	for key in d:
		floors[d[key]].append(key)
	lowest_filled = 0 # We never move something down into empty region
	while not floors[lowest_filled]:
		lowest_filled += 1
	next_states = []
	for delta in [-1, 1]: # direction of movement
		next_floor = cur_floor + delta
		if next_floor < lowest_filled or next_floor >= NUM_FLOORS:
			continue # Skip rest of this loop, target floor out of bounds
		for it in floors[cur_floor]:
			d[it] += delta
			if is_okay(d):
				d['E'] = next_floor
				next_states.append(dict_to_tuple(d))
				del d['E']
			d[it] -= delta # Restore the dictionary
		for it in itertools.combinations(floors[cur_floor], 2):
			d[it[0]] += delta
			d[it[1]] += delta
			ok_elevator = (it[0][0] == it[1][0] or it[0][1] == it[1][1])
			if is_okay(d) and ok_elevator:
				d['E'] = next_floor
				next_states.append(dict_to_tuple(d))
				del d['E']
			d[it[0]] -= delta # Restore the dictionary
			d[it[1]] -= delta
	return next_states

def bfs(start_state, goal):  # bfs through states
	print("Be patient, part 1 takes a minute or two")
	visited = {start_state:None} # Initially no visited states, will map state to dist to that state
	queue = [(start_state, 0)] # Queue indicates to expand start state, 0 steps to get there
	count = 0
	while len(queue) > 0:
		if count%PRINT_INTERVAL==0:
			print("Steps: %d, Depth: %d" % (count,queue[0][1]))
		count+=1
		state, num_steps = queue.pop(0)
		if state == goal:
			return num_steps
		neighbors = get_next_states(state)
		for n in neighbors:
			if n not in visited:
				visited[n] = None
				queue.append((n, num_steps+1))
	print("Could not reach goal")
	return -1

def a_star(start_state, goal):
	def h(s): # Counts on fact that 'E' comes first
		total = 0
		for i in range(1, len(s)):
			total += (2*NUM_FLOORS - 2 - s[i][0] - s[i][1])
		total -= (NUM_FLOORS - 1 - s[0])
		return total
	cost_so_far = {start_state: 0}
	queue = PriorityQueue()
	queue.put((h(start_state), start_state))
	count = 0
	while not queue.empty():
		p, state = queue.get()
		num_steps = cost_so_far[state]
		if state == goal:
			return num_steps
		for n in get_next_states(state):
			new_cost = num_steps + 1
			if n not in cost_so_far or new_cost < cost_so_far[n]:
				cost_so_far[n] = new_cost
				priority = new_cost + h(n)
				queue.put((priority, n))
	print("Could not reach goal")
	return -1


if __name__ == "__main__":
	global NUM_ELTS
	NUM_ELTS = len(ELTS_1)
	f = open('input.txt', 'rt')
	start_state = parse_input(f, ELTS_1)
	print("Part 1: %d" % (a_star(start_state, GOAL_1)))
	f = open('input_augmented.txt', 'rt')
	NUM_ELTS = len(ELTS_2)
	start_state = parse_input(f, ELTS_2)
	print("Part 2: %d" % (a_star(start_state, GOAL_2)))

