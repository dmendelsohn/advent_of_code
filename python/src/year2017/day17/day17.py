INPUT = 301

# Return new current_index, modify buf in place
def step(buf, num, current_index):
    current_index = (current_index + INPUT) % len(buf) + 1
    buf.insert(current_index, num)
    return current_index

def part1Answer():
    buf = [0]
    current_index = 0
    for i in range(1, 2018):
        current_index = step(buf, i, current_index)
    index = (buf.index(2017) + 1) % len(buf)
    return buf[index]

def part2Answer():
    current_index = 0
    answer_so_far = None
    for i in range(1, 50000001):
        current_index = (current_index + INPUT) % i + 1
        if current_index == 1:
            answer_so_far = i
    return answer_so_far

if __name__ == "__main__":
    print("Part 1: {}".format(part1Answer()))
    print("Part 2: {}".format(part2Answer()))

