def score(line):
    score_so_far = 0
    garbage_count = 0
    num_groups_open = 0
    is_garbage = False
    is_cancel = False
    for c in line:
        # Skip char if cancelled
        if is_cancel:
            is_cancel = False
            continue

        if is_garbage and c not in ['!', '>']:
            garbage_count += 1

        if c == '{':
            if not is_garbage:
                num_groups_open += 1
                score_so_far += num_groups_open
        elif c == '}':
            if not is_garbage:
                num_groups_open -= 1
        elif c == '<':
            is_garbage = True
        elif c == '>':
            is_garbage = False
        elif c == '!':
            is_cancel = True

    return score_so_far, garbage_count

def answer(f, part):
    lines = f.read().strip().split('\n')
    return sum(score(line)[part-1] for line in lines)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (answer(f, 1),))
    f.seek(0)
    print("Part 2: %d" % (answer(f, 2),))

