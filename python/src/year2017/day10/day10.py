import operator

def parse_input(f):
    return list(map(int, f.read().strip().split(',')))

def step(nums, index, span, skip):
    # Reverse nums[index:index+span], and return new (nums, index, skip)
    nums = nums[index:] + nums[:index] # Translate so index is at beginning
    if span: # Avoid 0 corner case
        nums[:span] = nums[span-1::-1] # Reverse span
    nums = nums[-index:] + nums[:-index] # Translate back
    return (nums, (index+span+skip)%len(nums), skip+1)

def part1Answer(f):
    spans = parse_input(f)
    nums = list(range(256))
    index, skip = 0, 0
    for span in spans:
        nums, index, skip = step(nums, index, span, skip)
    return nums[0]*nums[1]

def condense(nums): # Condense 256 8-bit nums to 16 by XORing in groups of 16
    return [reduce(operator.xor, nums[i*16:(i+1)*16]) for i in range(16)]

def get_hex_string(nums): # Convert list of 16 [0-255] ints to 32 char hexstring
    return ''.join('%02x' % num for num in nums)

def part2Answer(f):
    text = f.read().strip()
    spans = list(map(ord, text))
    print(text)
    print(spans)
    spans += [17, 31, 73, 47, 23]
    nums = list(range(256))
    index, skip = 0, 0
    for i in range(64):
        for span in spans:
            nums, index, skip = step(nums, index, span, skip)
    return get_hex_string(condense(nums))

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %s" % (part2Answer(f),))

