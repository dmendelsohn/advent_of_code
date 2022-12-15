import hashlib

INPUT = 'ngcjuoqr'
def hash_n(x, n=1):
	text = INPUT+str(x)
	for i in range(n):
		text = hashlib.md5(text).hexdigest()
	return text

def get_n_runners(s, n):
	runners = ''
	cur_char = ''
	count = 0
	for c in s:
		if c == cur_char:
			count+=1
			if count == n and c not in runners:
				runners += c # Found a new one!
		else:
			cur_char = c
			count = 1
	return runners

def get_first_n_runner(s, n):
	cur_char = ''
	count = 0
	for c in s:
		if c == cur_char:
			count+=1
			if count == n:
				return c
		else:
			cur_char = c
			count = 1
	return ''

def answer(stretch=1):
	i = 0
	key_indices = []
	quints = {} # Maps index to str (possibly empty) of quints in hash
	while len(key_indices) < 64:
		quints[i] = get_n_runners(hash_n(i, stretch), 5)
		j = i-1000
		if j >= 0:
			trip = get_first_n_runner(hash_n(j, stretch), 3)
			if trip: # If we have a triple
				for k in range(j+1, j+1001):
					if trip in quints[k]:
						key_indices.append(j)
						if stretch > 20: # Let's print updates
							print("Key index %d is %d" % (len(key_indices), j))
						break   # out of the for loop
		i += 1
	return key_indices[63]

def part2Answer():
	return 0

if __name__ == "__main__":
	from datetime import datetime as dt
	t1 = dt.now()
	print("Part 1: %d" % (answer(),))
	t2 = dt.now()
	print("...in time %s" % (str(t2-t1),))
	print("Part 2: %d" % (answer(2017),))
	print("...in time %s" % (str(dt.now()-t2),))
