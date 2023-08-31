import re
from dataclasses import dataclass
from typing import Any, FrozenSet, Optional

import numpy as np
import numpy.typing as npt

# Mapping from {key}-mining robot, to the resources required to build it
ResourceCounts = npt.NDArray[np.int32]  # Length-4 array of non-negative integers
Inventory = ResourceCounts
Fleet = ResourceCounts
Blueprint = list[ResourceCounts]  # Length-4 array representing the cost of building resource {i}


def get_max_fleet(blueprint: Blueprint) -> Fleet:
    max_fleet = np.array([50] * 4)  # Upper bound of 50 for all resource types will never be hit
    # Note we do NOT place a max on geode-robots
    for i in range(3):
        max_fleet[i] = max(counts[i] for counts in blueprint)
    return max_fleet


def get_blueprints(puzzle_input: str) -> dict[int, Blueprint]:
    blueprints = {}
    pattern = (
        r"Blueprint (\d+):\s+"
        r"Each ore robot costs (\d+) ore.\s+"
        r"Each clay robot costs (\d+) ore.\s+"
        r"Each obsidian robot costs (\d+) ore and (\d+) clay.\s+"
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    for match in re.findall(pattern, puzzle_input):
        match = list(map(int, match))
        blueprints[match[0]] = [
            np.array([match[1], 0, 0, 0]),
            np.array([match[2], 0, 0, 0]),
            np.array([match[3], match[4], 0, 0]),
            np.array([match[5], 0, match[6], 0]),
        ]

    return blueprints


@dataclass(frozen=True)
class State:
    inventory: Inventory
    fleet: Fleet

    def copy(self) -> "State":
        return State(self.inventory.copy(), self.fleet.copy())

    @property
    def cache_key(self):
        return tuple(self.inventory), tuple(self.fleet)


def get_max_geodes(
    blueprint: Blueprint,
    state: State,
    time_left: int,
    *,
    max_fleet: Fleet,
    do_not_build: Optional[FrozenSet[int]] = None,
    cache: Optional[dict[Any, int]] = None,
) -> int:
    """Note: we are allowed to modify inputs however we want"""
    max_geodes = state.inventory[3]
    if time_left <= 0:
        return max_geodes

    if cache is None:
        cache = {}

    # Clamp to maximum usable inventory
    loss_rate = max_fleet - state.fleet
    max_inventory = max_fleet + loss_rate * time_left
    state = State(inventory=np.minimum(max_inventory, state.inventory), fleet=state.fleet)

    cache_key = (state.cache_key, time_left)
    if cache_key in cache:
        return cache[cache_key]

    buildable_robot_types = set()
    for robot_type in range(4):
        if (blueprint[robot_type] > state.inventory).any():
            # Cannot build
            continue
        if state.fleet[robot_type] >= max_fleet[robot_type]:
            # No need to build, already at max for this type
            continue
        buildable_robot_types.add(robot_type)

    # Update inventory after calculating buildable robots
    state = State(inventory=state.inventory + state.fleet, fleet=state.fleet)

    # If we may be saving up for something, then consider building nothing
    # Note: set do_not_build, because there is no point waiting to build something we can build now
    if len(buildable_robot_types) < len(blueprint):
        max_geodes = max(
            max_geodes,
            get_max_geodes(
                blueprint,
                state.copy(),
                time_left - 1,
                do_not_build=frozenset(buildable_robot_types),
                cache=cache,
                max_fleet=max_fleet,
            ),
        )

    # Consider building one of the buildable types
    for robot_type in buildable_robot_types:
        if do_not_build and robot_type in do_not_build:
            continue

        next_inventory = state.inventory - blueprint[robot_type]
        next_fleet = state.fleet.copy()
        next_fleet[robot_type] += 1
        next_state = State(inventory=next_inventory, fleet=next_fleet)
        max_geodes = max(
            max_geodes,
            get_max_geodes(blueprint, next_state, time_left - 1, cache=cache, max_fleet=max_fleet),
        )

    cache[cache_key] = max_geodes
    return max_geodes


def part_1(puzzle_input: str) -> str | int:
    blueprints = get_blueprints(puzzle_input)
    total_quality = 0
    for blueprint_id, blueprint in blueprints.items():
        start_state = State(inventory=np.array([0, 0, 0, 0]), fleet=np.array([1, 0, 0, 0]))
        max_fleet = get_max_fleet(blueprint)
        max_geodes = get_max_geodes(blueprint, start_state, 24, max_fleet=max_fleet)
        total_quality += blueprint_id * max_geodes
    return total_quality


# This is not speedy, it takes like 30 seconds to run
# - Maintain a lower bound for the answer for a given blueprint, and prune when can't reach it.
# - Branch based on "next robot type to build", rather than making a second-by-second decision.
def part_2(puzzle_input: str) -> str | int:
    blueprints = get_blueprints(puzzle_input)
    total = 1
    for blueprint_id, blueprint in blueprints.items():
        if blueprint_id > 3:
            continue
        start_state = State(inventory=np.array([0, 0, 0, 0]), fleet=np.array([1, 0, 0, 0]))
        max_fleet = get_max_fleet(blueprint)
        max_geodes = get_max_geodes(blueprint, start_state, 32, max_fleet=max_fleet)
        total *= max_geodes
    return total
