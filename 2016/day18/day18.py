def is_trap(row, pos):
	return (pos-1 >= 0 and row[pos-1]) != (pos+1<len(row) and row[pos+1])

def answer(first_row, n):
	row = [(c == '^') for c in first_row]
	count = row.count(False)
	for i in range(1, n): # Generate row #i
		row = [is_trap(row, j) for j in range(len(row))]
		count += row.count(False)
	return count

if __name__ == "__main__":
	r = open('input.txt', 'rt').read().strip()
	print("Part 1: %d" % (answer(r, 40),))
	print("Part 2: %d" % (answer(r, 400000),))

