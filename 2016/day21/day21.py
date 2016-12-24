START = 'abcdefgh' # Forward from here
SCRAM = 'fbgdceah'  # Back from here

FORWARD_TABLE = [1, 2, 3, 4, 6, 7, 8, 9]
REVERSE_TABLE = [7, -1, 2, -2, 1, -3, 0, -4]  # For reversing "move based"
# index of where it is -> where it should go back to (rotation required)
# 0 -> 7 (7)
# 1 -> 0 (-1)
# 2 -> 4 (2)
# 3 -> 1 (-2)
# 4 -> 5 (1)
# 5 -> 2 (-3)
# 6 -> 6 (0)
# 7 -> 3 (-4)

def rotate(arr, num): # Right is positive
	if num == 0: # Special case
		return arr
	num %= len(arr)
	return arr[-num:] + arr[:-num]


def answer(inp, start, back=False):
	text = [c for c in start]
	for inst in inp:
		parts = inst.split()
		if (parts[0],parts[1]) == ('swap','position'):
			x, y = int(parts[2]), int(parts[5])
			text[x], text[y] = text[y], text[x]
		elif (parts[0],parts[1]) == ('swap', 'letter'):
			x, y = parts[2], parts[5]
			for i in range(len(text)):
				if text[i] == x:
					text[i] = y
				elif text[i] == y:
					text[i] = x
		elif (parts[0],parts[1]) == ('rotate', 'based'):
			x = parts[-1]
			index = text.index(x)
			if back:
				num = REVERSE_TABLE[index]
			else:
				num = FORWARD_TABLE[index]
			text = rotate(text, num)
		elif parts[0] == 'rotate':
			num = int(parts[2])
			if parts[1] == 'left':
				num *= -1
			if back:
				num *= -1
			text = rotate(text, num)
		elif parts[0] == 'reverse':
			x, y = int(parts[2]), int(parts[4])
			text = text[:x] + text[x:y+1][::-1] + text[y+1:]
		elif parts[0] == 'move':
			x, y = int(parts[2]), int(parts[5])
			if back:
				x, y = y, x
			c = text.pop(x)
			text.insert(y, c)
		else:
			print("ERROR")
			return
	return ''.join(text)

def part2Answer(inp):
	return 0

if __name__ == "__main__":
	inp = open('input.txt', 'rt').read().strip().split('\n')
	print("Part 1: %s" % (answer(inp, START, False),))
	print("Part 2: %s" % (answer(inp[::-1], SCRAM, True),))

