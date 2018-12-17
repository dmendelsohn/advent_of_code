import argparse
from enum import Enum

class CartDirection(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'

    @classmethod
    def get_track_part(cls, direction):  # Helper for parsing input
        if direction in (cls.UP, cls.DOWN):
            return TrackPart.VERT
        else:
            return TrackPart.HORIZ

    @classmethod
    def get_next_direction(cls, direction, track_part, turn_count=0):  # Helper to execute turns
        if track_part == TrackPart.EMPTY:
            raise ValueError('Cart should not be on empty space')
        elif track_part in (TrackPart.HORIZ, TrackPart.VERT):
            return direction  # No need to change
        elif track_part == TrackPart.FWD_TURN:
            mapping = {  # Swap up <-> right, and down <-> left
                cls.RIGHT: cls.UP,
                cls.UP: cls.RIGHT,
                cls.LEFT: cls.DOWN,
                cls.DOWN: cls.LEFT
            }
            return mapping[direction]
        elif track_part == TrackPart.BACK_TURN:
            mapping = {  # Swap up <-> left, and down <-> right
                cls.UP: cls.LEFT,
                cls.LEFT: cls.UP,
                cls.DOWN: cls.RIGHT,
                cls.RIGHT: cls.DOWN
            }
            return mapping[direction]
        elif track_part == TrackPart.INTER:
            if turn_count % 3 == 0:  # Turn left
                mapping = {
                    cls.UP: cls.LEFT,
                    cls.LEFT: cls.DOWN,
                    cls.DOWN: cls.RIGHT,
                    cls.RIGHT: cls.UP
                }
                return mapping[direction]
            elif turn_count % 3 == 1: # Go straight
                return direction
            else:  # Turn right
                mapping = {
                    cls.UP: cls.RIGHT,
                    cls.RIGHT: cls.DOWN,
                    cls.DOWN: cls.LEFT,
                    cls.LEFT: cls.UP
                }
                return mapping[direction]
        else:
            raise TypeError('Unrecognized TrackPart {}'.format(track_part))


class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn_count = 0

    def do_move(self, track):
        self.do_step()
        track_part = track[self.y][self.x]
        self.do_turn(track_part)

    def do_step(self):
        if self.direction == CartDirection.UP:
            self.y -= 1
        elif self.direction == CartDirection.DOWN:
            self.y += 1
        elif self.direction == CartDirection.LEFT:
            self.x -= 1
        elif self.direction == CartDirection.RIGHT:
            self.x += 1
        else:
            raise TypeError('Unrecognized CartDirection {}'.format(self.direction))

    def do_turn(self, track_part):
        self.direction = CartDirection.get_next_direction(self.direction, track_part, self.turn_count)
        if track_part == TrackPart.INTER:
            self.turn_count += 1

    def __repr__(self):
        return 'Cart: (position={}, direction={}, turns={})'.format((self.x, self.y), self.direction.name, self.turn_count)


class TrackPart(Enum):
    EMPTY = ' '
    HORIZ = '-'
    VERT = '|'
    BACK_TURN= '\\'
    FWD_TURN = '/'
    INTER = '+'


def parse(f):
    carts = []
    track = []
    lines = f.read().split('\n')[:-1]  # Cut off empty row at the end

    # Find the carts and replace with actual track pieces
    for y, line in enumerate(lines):
        track_row = []
        for x, c in enumerate(line):
            try:
                cart_direction = CartDirection(c)
                track_row.append(CartDirection.get_track_part(cart_direction))
                carts.append(Cart(x, y, cart_direction))
            except ValueError:
                track_row.append(TrackPart(c))
        track.append(track_row)
    return track, carts


def print_track(track):
    for row in track:
        print(''.join(part.value for part in row))


def get_collision(carts):  # Return first collision found in list
    seen = set()
    for cart in carts:
        loc = (cart.x, cart.y)
        if loc in seen:
            return loc
        seen.add(loc)
    return None   # No collision


def run_until_first_collision(track, carts):
    collision = None
    while not collision:
        for cart in sorted(carts, key=lambda c: (c.x, c.y)):
            cart.do_move(track)
            collision = get_collision(carts)
            if collision:
                break
    return collision


def remove_collision(carts):  # 0 or 1 collisions
    seen = {} # Map location to cart at that location
    for cart in carts:
        loc = (cart.x, cart.y)
        if loc in seen:  # Remove both carts
            print('Found collision at {}'.format(loc))
            carts.remove(seen[loc])
            carts.remove(cart)
            return
        seen[loc] = cart


def run_until_last_collision(track, carts):
    while len(carts) > 1:
        for cart in sorted(carts, key=lambda c: (c.x, c.y)):
            if cart not in carts:  # It's been removed alrady
                continue
            cart.do_move(track)
            remove_collision(carts)
    return carts[0].x, carts[0].y

def part1Answer(f):
    track, carts = parse(f)
    collision = run_until_first_collision(track, carts)
    return collision

def part2Answer(f):
    track, carts = parse(f)
    last_loc = run_until_last_collision(track, carts)
    return last_loc

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    if args.test:
        FILE1 = 'test.txt'
        FILE2 = 'test2.txt'
    else:
        FILE1 = FILE2 = 'input.txt'

    f = open(FILE1, 'rt')
    print("Part 1: {}".format(part1Answer(f)))

    f = open(FILE2, 'rt')
    print("Part 2: {}".format(part2Answer(f)))

