import string

def parse_room(room):
	parts = room.split('[')
	check = parts[1][:-1]
	parts = parts[0].split('-')
	return (parts[:-1], check, int(parts[-1])) # list of str rooms, str check, int id

def is_real_room(room):
	freq_table = get_freq_table(''.join(room[0]))
	freq_table.sort(key=lambda x: x[1], reverse=True)
	correct_check = ''.join([freq_table[i][0] for i in range(5)])
	return correct_check == room[1]

# Returns [(a, count(a)), (b, count(b)), ...]
def get_freq_table(text):
	d = {}
	for c in string.ascii_lowercase:
		d[c] = 0
	for c in text:
		d[c] += 1
	return sorted(d.items(), key=lambda x: x[0])	

def part1Answer(rooms):
	rooms = [parse_room(r) for r in rooms]
	total = 0
	for r in rooms:
		if is_real_room(r):
			total += r[2]
	return total

def shift(text, num):
	alph = string.ascii_lowercase
	return ''.join([alph[(alph.index(c)+num)%len(alph)] for c in text])

def part2Answer(rooms):
	rooms = [parse_room(r) for r in rooms]
	names = [' '.join([shift(word, r[2]) for word in r[0]]) for r in rooms]
	for i in range(len(rooms)):
		if 'pole' in names[i]:
			print("Room found: %s" % (names[i],))
			return rooms[i][2]
	print ("No room found")
	return 0

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	rooms = f.read().strip().split('\n')
	print("Part 1: %d" % (part1Answer(rooms),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(rooms),))

