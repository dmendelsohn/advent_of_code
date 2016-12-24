INPUT = '10001110011110000'
SIZE_1 = 272
SIZE_2 = 35651584

I = {'1': '0', '0':'1'}

def dragon(s):
	return (s + '0' + ''.join(I[c] for c in s[::-1]))

def compress(s):
	return ''.join(['1' if s[2*i] == s[2*i+1] else '0' for i in range(len(s)/2)])

def answer(cap):
	s = INPUT
	while len(s) < cap: #Dragon to size
		s = dragon(s)
	if len(s) > cap:  #Cut off extra
		s = s[:cap]
	while len(s)%2==0: #Compress until odd
		s = compress(s)
	return s

if __name__ == "__main__":
	print("Part 1: %s" % (answer(SIZE_1),))
	print("Part 2: %s" % (answer(SIZE_2),))

