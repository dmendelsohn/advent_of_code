def parse(f):
    lines = f.read().strip().split('\n')
    return [(line[5], line[36]) for line in lines]


def is_root(edges, node):
    return not any(node == e[1] for e in edges)

def top_sort(edges):
    edges = set(edges)  # Make a copy
    nodes = set(e[0] for e in edges).union(set(e[1] for e in edges))
    L = []  # Will contain final sort
    S = {node for node in nodes if is_root(edges, node)}
    while S:
        node = min(S)
        S.remove(node)
        L.append(node)
        for e in list(edges):  # Copy so we don't change while iterating
            if e[0] == node:
                edges.remove(e)
            if is_root(edges, e[1]):
                S.add(e[1])
    if edges:
        return 'CYCLE!'
    else:
        return L

def get_time(node):
    return ord(node) - ord('A') + 61


def complete_tasks(edges, workers):
    edges = set(edges)  # Make a copy
    nodes = set(e[0] for e in edges).union(set(e[1] for e in edges))
    S = {node for node in nodes if is_root(edges, node)}  # Available to start
    finishes = set()  # Set of (time, node) tuples for current jobs
    time = 0
    while S or finishes:  # Tasks still to do or tasks in progress
        while S and len(finishes) < workers: # Start a task
            node = min(S)   # Pick alphabetically first of available tasks
            S.remove(node)
            print('Starting {} at t={}'.format(node, time))
            finish_time = time + get_time(node)
            finishes.add((finish_time, node))
        # That's all the assignments we can do now, wait a task to finish
        time = min(f[0] for f in finishes)
        for finish_time, node in list(finishes):
            if finish_time == time:  # This tasks is now finished
                print('Finishing {} at t={}'.format(node, finish_time))
                finishes.remove((finish_time, node))
                for e in list(edges):  # Copy so we don't change while iterating
                    if e[0] == node:
                        edges.remove(e)
                    if is_root(edges, e[1]):
                        S.add(e[1])
    return time


def part1Answer(f):
    edges = parse(f)
    return ''.join(top_sort(edges))

NUM_WORKERS = 5
def part2Answer(f):
    edges = parse(f)
    return complete_tasks(edges, NUM_WORKERS)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    # f = open('input2.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

