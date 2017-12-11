def parse_line(line):
    parts = line.replace(',', '').split(' ')
    name = parts[0]
    weight = int(parts[1][1:-1])
    children = parts[3:]
    return (name, weight, children)

def parse_input(f):
    lines = f.read().strip().split('\n')
    tree = {}
    for line in lines:
        name, weight, children = parse_line(line)
        tree[name] = (weight, children)
    return tree

def get_base(tree):
    names = set()
    children_names = set()
    for name in tree:
        weight, children = tree[name]
        names.add(name)
        for child in children:
            children_names.add(child)
    parent_only = names - children_names
    if len(parent_only) != 1:
        raise ValueError('Not 1 parent')
    return list(parent_only)[0]

# Add 4th field (load) and 5th field (is_balanced) to each node
def augment_tree(tree, name):
    weight, children = tree[name]
    child_loads = [augment_tree(tree, child) for child in children]
    is_balanced = len(set(child_loads)) <= 1
    tree[name] = (weight, children, weight + sum(child_loads), is_balanced)
    return tree[name][2]

# Pre-condition: there's a wrong weight in subtree rooted at node with name
# diff is the amount by which we need to change this subtree's total weight (aka load)
# if diff is None, we don't yet know how much to change the load
def find_error(tree, name, diff=None):
    weight, children, load, is_balanced = tree[name]
    if is_balanced: # The current node is the culprit!
        return weight+diff
    elif len(children) > 2: # A child's subtree has an error, and we can find which one
        load_freq = {}
        for child in children:
            child_load = tree[child][2]
            load_freq[child_load] = load_freq.get(child_load, 0) + 1
        loads = list(load_freq.keys())
        if len(loads) != 2:
            raise Exception
        for i in range(2):
            if load_freq[loads[i]] == 1: # We may have found the problem
                if load_freq[loads[i-1]] != 1 or (loads[i-1] - loads[i]) == diff: # Found it!
                    bad_load = loads[i]
                    for child in children:
                        if tree[child][2] == bad_load:
                            return find_error(tree, child, loads[i-1]-loads[i])


def part1Answer(f):
    tree = parse_input(f)
    base = get_base(tree)
    return base

def part2Answer(f):
    tree = parse_input(f)
    base = get_base(tree)
    augment_tree(tree, base)
    return find_error(tree, base)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: %s" % (part1Answer(f),))
    f.seek(0)
    print("Part 2: %d" % (part2Answer(f),))

