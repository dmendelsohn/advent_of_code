from collections import namedtuple

NUM_PLAYERS = 459
HI_MARBLE = 72103*100

# Returns index of "current marble" after move
# Modify marbles in place (and scores in place as well, if needed)
def do_turn_list(marbles, index, player, next_marble, scores):
    if next_marble % 23 == 0:
        # Remove marble 7 indices lower and update scores
        index = (index-7)%len(marbles)
        removed_marble = marbles[index]
        del marbles[index]
        scores[player] += (next_marble + removed_marble)
        return index
    else:
        # Place marble
        index = (index+2)%len(marbles)
        marbles.insert(index, next_marble)
        return index


class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


def insert_after(node, value):
    # Create a new node with the given value, insert after input node
    # Return the new node
    new_node = Node(value)
    next_node = node.next
    new_node.prev, new_node.next = node, next_node
    node.next, next_node.prev = new_node, new_node
    return new_node


def remove_node(node):
    # Remove the node and return its value
    node.prev.next = node.next
    node.next.prev = node.prev
    return node.value

def do_turn(current_node, player, next_marble, scores):
    # current_node is a node in a LL
    # player, next_marble are ints
    # scores is a list of scores for each player
    # Returns node of new "current marble" after move, modifying LL and scores if needed
    if next_marble % 23 == 0:
        # Remove marble 7 earlier and update scores
        for i in range(7):
            current_node = current_node.prev
        next_current_node = current_node.next
        removed_marble = remove_node(current_node)
        scores[player] += (next_marble + removed_marble)
        return next_current_node
    else:
        # Place marble
        next_current_node = insert_after(current_node.next, next_marble)
        return next_current_node


def answer(f, hi_marble):
    #marbles = [0]
    #index = 0
    current_node = Node(0)
    current_node.next = current_node
    current_node.prev = current_node
    player = 0
    scores = [0]*NUM_PLAYERS
    for next_marble in range(1, hi_marble+1):
        if next_marble % 100000 == 0:
            print(next_marble/100000)
        current_node = do_turn(current_node, player, next_marble, scores)
        player = (player+1)%NUM_PLAYERS
    return max(scores)


if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(answer(f, 72103)))
    f.seek(0)
    print("Part 2: {}".format(answer(f, 72103*100)))

