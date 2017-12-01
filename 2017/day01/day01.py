def get_special_sum(str_num, offset=1):
    total = 0
    for i in range(-offset, len(str_num)-offset):
        if str_num[i] == str_num[i+offset]:
            total += int(str_num[i])
    return total

def part1Answer(f):
    str_num = f.read().strip()
    return get_special_sum(str_num)

def part2Answer(f):
    str_num = f.read().strip()
    return get_special_sum(str_num, len(str_num)//2)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

