class Robot:
	def __init__(self, rid):
		self.nums = []
		self._id = rid
		self._type = 'bot'
		self.output_low = None
		self.output_high = None

	def process_input(self, num):
		if len(self.nums) < 2: # Check if the robot has room for the new num
			self.nums.append(num)
		self.propagate()

	def set_output_high(self, obj):
		self.output_high = obj
		self.propagate()

	def set_output_low(self, obj):
		self.output_low = obj
		self.propagate()

	def propagate(self):
		if len(self.nums) == 2:
			if max(self.nums) == 61 and min(self.nums) == 17:
				print ('Part 1: %d' % (self._id,)) # We found our robot
			if self.output_low: # If we have a low connection
				self.output_low.process_input(min(self.nums))
				self.output_low = None
			if self.output_high: # If we have a high connection
				self.output_high.process_input(max(self.nums))
				self.output_high = None

class Output:
	def __init__(self, oid):
		self.val = None
		self._id = oid
		self._type = 'output'

	def process_input(self, num):
		self.val = num

# Returns (rid, value) or (rid, (low_type, low_id), (high_type, high_id))
def parse_inst(text):
	parts = text.split()
	if len(parts) == 6: # e.g. value 7 goes to bot 22
		rid = int(parts[5])
		value = int(parts[1])
		return (rid, value)
	elif len(parts) == 12: # e.g. bot 0 gives low to bot 1 and high to bot 2
		rid = int(parts[1])
		low_type = parts[5]
		low_id = int(parts[6])
		high_type = parts[10]
		high_id = int(parts[11])
		return (rid, (low_type, low_id), (high_type, high_id))
	else:
		print("Parsing error for %s" % (text,))

def get_obj(robots, outputs, tag): # dict, dict, ('bot' | 'output', id)
	num = tag[1]
	if tag[0] == 'bot':
		if num not in robots:
			robots[num] = Robot(num)
		return robots[num]
	elif tag[0] == 'output':
		if num not in outputs:
			outputs[num] = Output(num)
		return outputs[num]
	else:
		print("Bad tag: %s" % (str(tag),))

def part1Answer(f):
	lines = f.read().strip().split('\n')
	robots = {}  # Dict mapping robot id to robot obj
	outputs = {}
	insts = [parse_inst(line) for line in lines]
	for inst in insts:
		robot = get_obj(robots, outputs, ('bot', int(inst[0])))
		if len(inst) == 2: # Value -> Robot type
			value = int(inst[1])
			robot.process_input(value)
		elif len(inst) == 3: # Robot -> other stuff
			robot.set_output_low(get_obj(robots, outputs, inst[1]))
			robot.set_output_high(get_obj(robots, outputs, inst[2]))
		else:
			print("Bad instruction")
	return outputs

def part2Answer(outputs):
	if 0 in outputs and 1 in outputs and 2 in outputs:
		return outputs[0].val * outputs[1].val * outputs[2].val
	else:
		print("Could not multiply outputs")
		return 0

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	outputs = part1Answer(f)
	print("Part 2: %d" % (part2Answer(outputs),))

