from collections import namedtuple

Node = namedtuple('Node', ['children', 'manifest'])

def parse(f):
    return map(int, f.read().strip().split())

# Return Node, index
def parse_node(nums, index=0):
    num_children, num_manifest = nums[index:index+2]
    index += 2
    children = []
    for i in range(num_children):
        child, index = parse_node(nums, index)
        children.append(child)
    node = Node(children, nums[index:index+num_manifest])
    return node, index+num_manifest


def print_node(node, num_indent=0):
    line = '--'*num_indent + ' Manifest: {}'.format(node.manifest)
    print(line)
    for child in node.children:
        print_node(child, num_indent+1)

def sum_manifests(node):
    return sum(node.manifest) + sum(sum_manifests(c) for c in node.children)

def value(node):
    if not node.children:
        return sum(node.manifest)
    else:
        val = 0
        for index in node.manifest:
            index -= 1 # Silly problem definition
            if 0 <= index < len(node.children):
                val += value(node.children[index])
        return val

def part1Answer(f):
    nums = parse(f)
    root, _ = parse_node(nums)
    return sum_manifests(root)

def part2Answer(f):
    nums = parse(f)
    root, _ = parse_node(nums)
    return value(root)

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    #f = open('input2.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

