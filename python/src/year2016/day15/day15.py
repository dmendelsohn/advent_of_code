DISCS_1 = [(13, 1), (19, 10), (3, 2), (7, 1), (5, 3), (17, 5)]
DISCS_2 = DISCS_1 + [(11,  0)]
DISCS_3 = [(43, 2), (53, 7), (61, 10), (37, 2), (127, 9)] 
DISCS_4 = [(101, 2), (163, 7), (263, 10), (293, 2), (373, 9), (499, 0), (577, 0)]

def norm(discs):
	def norm_pos(num_slots, start_pos, i):
		return num_slots - (start_pos + i + 1)%num_slots
	return [(discs[i][0], norm_pos(discs[i][0],discs[i][1], i)) for i in range(len(discs))]

def gcd(a, b):
	while b:
		a, b = b, a%b
	return a

def lcm(a, b):
	return a*b/gcd(a,b)

def merge((moda, ka), (modb, kb)): # Uses Chinese Remainder Theorem Sieve, I think
	while ka % modb != kb:  # CRT sieve
		ka += moda
	return (lcm(moda, modb), ka)

def answer(discs):
	return reduce(merge, sorted(discs, reverse=True))[1]

if __name__ == "__main__":
	from datetime import datetime as dt
	t1 = dt.now()
	print("Part 1: %d" % (answer(norm(DISCS_1)),))
	print("Part 2: %d" % (answer(norm(DISCS_2)),))
	print("Part 3: %d" % (answer(norm(DISCS_3)),))
	print("Part 4: %d" % (answer(norm(DISCS_4)),))
	t2 = dt.now()
	print(t2-t1)
