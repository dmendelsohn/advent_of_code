INPUT = 33100000
CUTOFF = INPUT/10

def prime_factors(n):
	i = 2
	factors = {}
	while i*i <= n:
		if n % i:
			i+=1
		else:
			n //= i
			if i in factors:
				factors[i] += 1
			else:
				factors[i] = 1
	if n > 1:
		if n in factors:
			factors[n] += 1
		else:
			factors[n] = 1
	return factors

def numPresents(num):
	factors = prime_factors(num)
	total = 10
	for (key, val) in factors.items():
		term = sum([key**i for i in range(val+1)])
		total *= term
	return total

def numPresents2(num):
	factors = prime_factors(num)
	divisors = getDivisors(factors)
	return 11*sum([d for d in divisors if d >= num/50])

def getDivisors(factors):
	if factors == {}:
		return [1]
	smallest = min(factors.keys())
	numTimes = factors[smallest]
	del factors[smallest]
	subdivisors = getDivisors(factors)
	divisors = []
	for i in range(numTimes+1):
		divisors.extend([elt * smallest**i for elt in subdivisors])
	return divisors

def part1Answer():
	i = 0
	while numPresents(i) < INPUT:
		i += 60 #Shortcut
	return i

def part2Answer():
	i = 0
	while numPresents2(i) < INPUT:
		i += 60 #Shortcut
	return i

if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(),))
	print("Part 2: %d" % (part2Answer(),))

