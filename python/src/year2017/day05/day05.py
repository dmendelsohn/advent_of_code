def parse_input(f):
    return [int(line) for line in f.read().strip().split('\n')]

def step(nums, pos, part_2):
    if pos < 0 or pos >= len(nums):
        raise ValueError()
    next_pos = pos + nums[pos]
    if part_2 and nums[pos] >= 3:
        nums[pos] -= 1
    else:
        nums[pos] += 1
    return next_pos

def get_answer(f, part_2=False):
    nums = parse_input(f)
    steps, pos = 0, 0
    while 0 <= pos < len(nums):
        pos = step(nums, pos, part_2)
        steps += 1
    return steps

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (get_answer(f, False),))
    f.seek(0)
    print("Part 2: %d" % (get_answer(f, True),))

