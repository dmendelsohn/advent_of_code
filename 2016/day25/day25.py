import math

# By exaning the assembly code, I realize I need to find the first
# Number higher than 7*365 that is of the form 1010101010...10 in binary
# and then subtract 7*365 from it

def answer():
	num = 2   # Lowest number with alternating 1s and 0s
	while num <= 7*365:
		num = 4*num + 2 # Append '10' to end of num
	return num - 7*365

if __name__ == "__main__":
	print("Part 1: %d" % (answer(),))

