def get_freq_count(word):
    freqs = {}
    for c in word:
        freqs[c] = freqs.get(c, 0) + 1
    return freqs

def has_n_repeat(word, n):
    freqs = get_freq_count(word)
    return n in freqs.values()

def parse(f):
    return f.read().split()

def part1Answer(f):
    words = parse(f)
    num2 = sum(map(lambda word: has_n_repeat(word, 2), words))
    num3 = sum(map(lambda word: has_n_repeat(word, 3), words))
    return num2 * num3

def part2Answer(f):
    words = parse(f)
    seen = set()
    for word in words:
        for i in range(len(word)):
            key = (i, word[:i] + word[i+1:])
            if key in seen:
                return key[1]
            seen.add(key)
    return 'ERROR'

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

