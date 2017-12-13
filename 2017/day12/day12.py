def parse_input(f):
    # Return dict mapping ids -> list of neighbors
    lines = f.read().strip().split('\n')
    graph = {}
    for line in lines:
        line = line.replace(',', '')
        parts = line.split(' ')
        key = int(parts[0])
        neighbors = list(map(int, parts[2:]))
        graph[key] = neighbors
    return graph

def get_group(graph, node, seen=None):
    seen = seen or set()
    if node in seen:
        return seen
    else:
        seen.add(node)
        for neighbor in graph[node]:
            get_group(graph, neighbor, seen)
        return seen

def part1Answer(f):
    graph = parse_input(f)
    return len(get_group(graph, 0))

def part2Answer(f):
    graph = parse_input(f)
    num_groups = 0
    while len(graph) > 0:
        key = list(graph.keys())[0]
        group = get_group(graph, key)
        num_groups += 1
        for node in group:
            del graph[node]
    return num_groups

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %d" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

