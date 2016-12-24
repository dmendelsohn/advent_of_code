INPUT = 3018458

def part1AnswerA():
	elves = {i:(i+1)%INPUT for i in range(INPUT)} # map elf to next elf
	i = 1 # index of current elf
	while elves[i] != i:
		elves[i] = elves[elves[i]] # Point to your pointee's pointee
		i = elves[i]
	return i

def part1Answer():
	prev = 0
	for i in range(2, INPUT+1):
		prev = (prev+2)%i
	return prev+1 # Due to 1-indexing

def part2Answer():
	prev = 0
	for i in range(2, INPUT+1): # Do step i
		prev += 1  # To account for the fact that it's the next person's turn
		if prev >= i/2:
			prev += 1
		prev %= i
	return prev+1 # Due to 1-indexing


if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(),))
	print("Part 2: %d" % (part2Answer(),))

