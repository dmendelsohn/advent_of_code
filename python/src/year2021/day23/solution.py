from pathlib import Path
from queue import PriorityQueue
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

MAX_INT = 10**10

Room = Tuple[str, ...]  # Length 4


class State(NamedTuple):
    hallway: Tuple[str, ...]  # Length 11
    a_room: Room
    b_room: Room
    c_room: Room
    d_room: Room

    def get_room_for_char(self, char: str) -> Room:
        return getattr(self, f"{char.lower()}_room")

    def __str__(self) -> str:
        grid = [[" "] * 11, [" "] * 11, [" "] * 11, [" "] * 11]
        for room_char in "ABCD":
            room = self.get_room_for_char(room_char)
            x_loc = ROOM_LOCS[room_char]
            for i, char in enumerate(room):
                grid[i][x_loc] = char or "."

        lines = ["".join(char or "." for char in self.hallway)]
        for y_loc in range(4):
            lines.append("".join(grid[y_loc]))
        return "\n".join(lines) + "\n"


CHAR_COST: Dict[str, int] = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOM_LOCS: Dict[str, int] = {"A": 2, "B": 4, "C": 6, "D": 8}


def get_start_state(use_test_input: bool) -> State:
    hallway = ("",) * 11
    if use_test_input:
        a_room = ("B", "D", "D", "A")
        b_room = ("C", "C", "B", "D")
        c_room = ("B", "B", "A", "C")
        d_room = ("D", "A", "C", "A")
    else:
        a_room = ("C", "D", "D", "B")
        b_room = ("A", "C", "B", "A")
        c_room = ("D", "B", "A", "B")
        d_room = ("D", "A", "C", "C")
    return State(hallway, a_room, b_room, c_room, d_room)


def get_dest_state() -> State:
    hallway = ("",) * 11
    a_room = ("A",) * 4
    b_room = ("B",) * 4
    c_room = ("C",) * 4
    d_room = ("D",) * 4
    return State(hallway, a_room, b_room, c_room, d_room)


def get_pushed_room(_room: Room, home_char: str) -> Optional[Tuple[Room, int]]:
    """Get the resulting room and dist of entering from the hallway (or None if impossible)"""
    room = list(_room)
    for i in range(3, -1, -1):
        if not room[i]:  # Found the lowest open spot
            room[i] = home_char
            return tuple(room), i + 1
        elif room[i] != home_char:  # This room cannot be entered
            return None
    return None  # Room is full of home char already


def get_popped_room(_room: Room) -> Tuple[Room, str, int]:
    """Pop top element out of room, return resulting room, popped char, and dist of exit"""
    room = list(_room)
    for i in range(4):
        if room[i]:  # Found the spot to pop
            popped_char = room[i]
            room[i] = ""
            return tuple(room), popped_char, i + 1
    raise RuntimeError("Could not get popped room")


def dist_to_reach_room(state: State, room_char: str, from_idx: int) -> Optional[int]:
    room_loc = ROOM_LOCS[room_char]
    is_passable = not any(
        state.hallway[i] for i in range(min(room_loc, from_idx) + 1, max(room_loc, from_idx))
    )
    return abs(room_loc - from_idx) if is_passable else None


def enter_neighbors(state: State) -> Dict[State, int]:
    """All valid moves where a entity is entering a room"""
    output = dict()
    for hall_idx, char in enumerate(state.hallway):
        # Check if there is an entity here
        if not char:
            continue
        # Check if the entity can reach its room
        hallway_dist = dist_to_reach_room(state, char, hall_idx)
        if hallway_dist is None:
            continue

        # Check if room can be entered
        result = get_pushed_room(state.get_room_for_char(char), char)
        if not result:
            continue
        new_room, entry_dist = result

        # We found a neighbor state, compute it and the move cost
        cost = (hallway_dist + entry_dist) * CHAR_COST[char]
        new_hallway = list(state.hallway)
        new_hallway[hall_idx] = ""
        new_state_dict = {
            **state._asdict(),
            "hallway": tuple(new_hallway),
            f"{char.lower()}_room": new_room,
        }
        output[State(**new_state_dict)] = cost
    return output


def get_available_hallway_locs(hallway: Tuple[str, ...], start_idx: int) -> Set[int]:
    locs = set()

    # Look right
    dest_idx = start_idx + 1
    while dest_idx < len(hallway) and not hallway[dest_idx]:
        if dest_idx in ROOM_LOCS.values():  # Can't stop here
            dest_idx += 1
            continue
        locs.add(dest_idx)
        dest_idx += 1

    # Look left
    dest_idx = start_idx - 1
    while dest_idx >= 0 and not hallway[dest_idx]:
        if dest_idx in ROOM_LOCS.values():  # Can't stop here
            dest_idx -= 1
            continue
        locs.add(dest_idx)
        dest_idx -= 1
    return locs


def exit_neighbors(state: State) -> Dict[State, int]:
    """All valid moves where a entity is exiting a room"""
    output = dict()
    for room_char in "ABCD":
        room_attr = f"{room_char.lower()}_room"
        room = getattr(state, room_attr)
        if all(not char or char == room_char for char in room):
            continue  # This room is stable, don't empty it
        new_room, popped_char, room_dist = get_popped_room(room)

        start_idx = ROOM_LOCS[room_char]
        available_hallway_locs = get_available_hallway_locs(state.hallway, start_idx)

        for dest_idx in available_hallway_locs:
            # Calculate state and cost of moving
            hallway_dist = abs(dest_idx - start_idx)
            cost = (room_dist + hallway_dist) * CHAR_COST[popped_char]

            new_hallway = list(state.hallway)
            new_hallway[dest_idx] = popped_char
            new_state_dict = {**state._asdict(), "hallway": tuple(new_hallway), room_attr: new_room}
            output[State(**new_state_dict)] = cost

    return output


def get_neighbors(state: State) -> Dict[State, int]:  # Neighbor states and the cost of the move
    return {**exit_neighbors(state), **enter_neighbors(state)}


def find_min_cost(start: State) -> Optional[int]:
    """Implementation of Dijkstra's algorithm"""
    # Initialize things
    dest = get_dest_state()
    min_cost_per_state: Dict[State, int] = {start: 0}
    visited_states: Set[State] = set()

    queue: PriorityQueue = PriorityQueue()
    queue.put((min_cost_per_state[start], start))

    # Loop until we find the terminal state
    current_cost, current_state = queue.get()
    while True:
        # Print progress
        if len(visited_states) % 1000 == 0:
            print(f"Visited {len(visited_states)} states.  Cost min = {current_cost}")

        if current_state == dest:
            break

        for neighbor_state, move_cost in get_neighbors(current_state).items():
            if neighbor_state in visited_states:
                continue

            known_neighbor_cost = min_cost_per_state.get(neighbor_state, MAX_INT)
            proposed_neighbor_cost = current_cost + move_cost
            if proposed_neighbor_cost < known_neighbor_cost:
                min_cost_per_state[neighbor_state] = proposed_neighbor_cost
                queue.put((min_cost_per_state[neighbor_state], neighbor_state))

        # Mark as visited
        visited_states.add(current_state)

        # Pick next unvisited point off the queue
        while current_state in visited_states:
            # If queue is empty, we are stuck
            if queue.empty():
                print(f"Got stuck with empty queue with {len(visited_states)} visited states")
                return -1
            current_cost, current_state = queue.get()

    return min_cost_per_state.get(dest)


def part_1(use_test_input: bool = False) -> str:
    return "10526"  # Did by hand


def part_2(use_test_input: bool = False) -> str:
    start_state = get_start_state(use_test_input)
    min_cost = find_min_cost(start_state)
    return f"{min_cost}"


# DEBUGGING HELPERS
def get_expected_state_sequence() -> List[State]:
    lines = open(Path(__file__).parent / "test_input.txt").readlines()
    states = []
    while lines:
        lines_to_parse, lines = lines[:8], lines[8:]
        state = parse_state(lines_to_parse)
        states.append(state)
    return states


def parse_state(lines: List[str]) -> State:
    hallway = tuple(lines[1][i] if lines[1][i] in "ABCD" else "" for i in range(1, 12))
    a_room = tuple(lines[i][3] if lines[i][3] in "ABCD" else "" for i in range(2, 6))
    b_room = tuple(lines[i][5] if lines[i][5] in "ABCD" else "" for i in range(2, 6))
    c_room = tuple(lines[i][7] if lines[i][7] in "ABCD" else "" for i in range(2, 6))
    d_room = tuple(lines[i][9] if lines[i][9] in "ABCD" else "" for i in range(2, 6))
    return State(hallway, a_room, b_room, c_room, d_room)
