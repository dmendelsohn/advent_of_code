def part1Answer(f):
    nums = map(int, f.read().split())
    return sum(nums)

def part2Answer(f):
    nums = map(int, f.read().split())
    seen = set()
    freq = 0
    while True:
        for num in nums:
            if freq in seen:
                return freq
            seen.add(freq)
            freq += num
    return 0

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

