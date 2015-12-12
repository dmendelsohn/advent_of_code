AND = "AND"
OR = "OR"
NOT = "NOT"
LSHIFT = "LSHIFT"
RSHIFT = "RSHIFT"
CONST = "CONST"

# Returns (key, value), where key is the wire being driven, and 
# value is a (src1, src2, op) tuple.  Sources can be a string, representing
# another wire, or a number, representing a constant input.
# op is one of "AND", "OR", "NOT", "LSHIFT", "RSHIFT", "CONST"
def getCircuitElement(line):
	parts = line.strip().split(' ')
	wire = parts[-1]
	parts = parts[:-2] #Chop off last two
	if len(parts) == 1: #Direct connection
		src1 = parts[0]
		src2 = None
		op = CONST
	elif len(parts) == 2: # one input throw a NOT gate
		src1 = parts[1]
		src2 = None
		op = NOT
	else: # two input gate
		src1 = parts[0]
		src2 = parts[2]
		op = parts[1]
	try:
		src1 = int(src1)
	except:
		pass
	try:
		src2 = int(src2)
	except:
		pass
	return (wire, (src1, src2, op))

# Returns a dictionary mapping wires to final values
# Circuit is a dictionary of circuit elements, mapping wires
# to the logic driving them
def resolveCircuit(circuit):
	values = {}
	for wire in circuit:
		if wire not in values:
			resolveWire(circuit, wire, values)
	return values

# Recursive helper method that resolves a specific wire,
# and any wires it depends upon.
# Modifies the values dict, returns None
def resolveWire(circuit, wire, values):
	(src1, src2, op) = circuit[wire]
	if src1 is None:
		num1 = None
	elif src1 in values:
		num1 = values[src1]
	else:
		try:
			num1 = int(src1)
		except ValueError:
			resolveWire(circuit, src1, values)
			num1 = values[src1]
	if src2 is None:
		num2 = None
	elif src2 in values:
		num2 = values[src2]
	else:
		try:
			num2 = int(src2)
		except ValueError:
			resolveWire(circuit, src2, values)
			num2 = values[src2]
	values[wire] = applyOp(num1, num2, op)

def applyOp(value1, value2, op):
	if op == CONST:
		return value1
	elif op == NOT:
		return (2**16) - 1 - value1
	elif op == AND:
		return value1 & value2
	elif op == OR:
		return value1 | value2
	elif op == LSHIFT:
		return value1 << value2
	elif op == RSHIFT:
		return value1 >> value2
	else:
		raise ValueError("Invalid applyOp: %d, %d, %s" % (value1, value2, op))


def part1Answer(f):
	#Build the circuit
	circuit = {}
	for line in f:
		(key, value) = getCircuitElement(line)
		circuit[key] = value
	values = resolveCircuit(circuit)
	return values['a']

def part2Answer(f):
	circuit = {}
	for line in f:
		(key, value) = getCircuitElement(line)
		circuit[key] = value
	circuit['b'] = (16076, None, CONST)
	values = resolveCircuit(circuit)
	return values['a']

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	print("Part 1: %d" % (part1Answer(f),))
	f.seek(0)
	print("Part 2: %d" % (part2Answer(f),))

