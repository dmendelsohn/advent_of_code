def parse_input(f):
    text = f.read().strip().split('\t')
    return [int(num) for num in text]

def step(nums):
    max_num = max(nums)
    index = 0
    while nums[index] != max_num:
        index += 1
    nums[index] = 0
    while max_num > 0:
        index = (index+1)%len(nums)
        nums[index] += 1
        max_num -= 1

def answer(f, part_2):
    nums = parse_input(f)
    seen = {} # tuple: first seen step
    count = 0
    while tuple(nums) not in seen:
        seen[tuple(nums)] = count
        step(nums)
        count += 1
    if part_2:
        return count - seen[tuple(nums)]
    else:
        return count

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (answer(f, False),))
    f.seek(0)
    print("Part 2: %d" % (answer(f, True),))

