import hashlib

INPUT = 'ugkcyxxp'

def part1Answer():
	num = 0
	password = ''
	while len(password) < 8:
		enc = hashlib.md5(INPUT + str(num)).hexdigest()
		if enc[:5] == '00000':
			password += enc[5]
			print(password)
		num += 1
	return password

def part2Answer():
	num = 0
	password = [None]*8
	while None in password:
		enc = hashlib.md5(INPUT + str(num)).hexdigest()
		if enc[:5] == '00000':
			if enc[5] in '01234567':
				index = int(enc[5])
				if password[index] is None:
					password[index] = enc[6]
					print(password)
		num += 1
	return ''.join(password)


if __name__ == "__main__":
	#print("Part 1: %s" % (part1Answer(),))
	print("Part 2: %s" % (part2Answer(),))

