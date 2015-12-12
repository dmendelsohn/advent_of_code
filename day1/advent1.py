filename = "input.txt"

f = open(filename, 'rt')
line = f.readline()

#Part 1
answer = line.count('(') - line.count(')')
print(answer)

#Part 2
count = 0
for i in range(len(line)):
	if line[i] == '(':
		count += 1
	elif line[i] == ')':
		count -= 1
	if count == -1:
		print(i+1)
		break
