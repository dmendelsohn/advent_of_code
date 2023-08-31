import enum
import re
from dataclasses import dataclass, field
from typing import Any, FrozenSet, Optional


class Resource(enum.IntEnum):
    ORE = enum.auto()
    CLAY = enum.auto()
    OBSIDIAN = enum.auto()
    GEODE = enum.auto()


# Mapping from {key}-mining robot, to the resources required to build it
Blueprint = dict[Resource, dict[Resource, int]]
Inventory = dict[Resource, int]
Fleet = dict[Resource, int]


def get_max_fleet(blueprint: Blueprint) -> Fleet:
    return {
        resource: max(requirements.get(resource, 0) for requirements in blueprint.values())
        for resource in Resource
        if resource != Resource.GEODE
    }


def get_blueprints(puzzle_input: str) -> dict[int, Blueprint]:
    blueprints = {}
    pattern = (
        r"Blueprint (\d+):\s+"
        r"Each ore robot costs (\d+) ore.\s+"
        r"Each clay robot costs (\d+) ore.\s+"
        r"Each obsidian robot costs (\d+) ore and (\d+) clay.\s+"
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    for (
        blueprint_id,
        ore_ore,
        clay_ore,
        obsidian_ore,
        obsidian_clay,
        geode_ore,
        geode_obsidian,
    ) in re.findall(pattern, puzzle_input):
        blueprint = {
            Resource.ORE: {Resource.ORE: int(ore_ore)},
            Resource.CLAY: {Resource.ORE: int(clay_ore)},
            Resource.OBSIDIAN: {Resource.ORE: int(obsidian_ore), Resource.CLAY: int(obsidian_clay)},
            Resource.GEODE: {Resource.ORE: int(geode_ore), Resource.OBSIDIAN: int(geode_obsidian)},
        }
        blueprints[int(blueprint_id)] = blueprint

    return blueprints


@dataclass(frozen=True)
class State:
    inventory: Inventory = field(default_factory=lambda: {res: 0 for res in Resource})
    fleet: Fleet = field(default_factory=lambda: {res: 0 for res in Resource})

    def copy(self) -> "State":
        return State(self.inventory.copy(), self.fleet.copy())

    @property
    def cache_key(self):
        return tuple(sorted(self.inventory.items())), tuple(sorted(self.fleet.items()))


def get_max_geodes(
    blueprint: Blueprint,
    state: State,
    time_left: int,
    *,
    max_fleet: Fleet,
    do_not_build: Optional[FrozenSet[Resource]] = None,
    cache: Optional[dict[Any, int]] = None,
) -> int:
    """Note: we are allowed to modify inputs however we want"""
    max_geodes = state.inventory[Resource.GEODE]
    if time_left <= 0:
        return max_geodes

    if cache is None:
        cache = {}

    cache_key = (state.cache_key, time_left)
    if cache_key in cache:
        return cache[cache_key]

    buildable_robot_types = set()
    for robot_type in Resource:
        if robot_type in max_fleet and state.fleet[robot_type] >= max_fleet[robot_type]:
            continue
        requirements = blueprint[robot_type]
        if all(requirements[resource] <= state.inventory[resource] for resource in requirements):
            buildable_robot_types.add(robot_type)

    # Update inventory in-place after calculating buildable robots
    for resource, count in state.fleet.items():
        state.inventory[resource] += count

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
        next_inventory = state.inventory.copy()
        for resource, build_cost in blueprint[robot_type].items():
            next_inventory[resource] -= build_cost

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
        start_state = State()
        start_state.fleet[Resource.ORE] += 1  # Start with one ore-mining robot
        max_fleet = get_max_fleet(blueprint)
        max_geodes = get_max_geodes(blueprint, start_state, 24, max_fleet=max_fleet)
        total_quality += blueprint_id * max_geodes
    return total_quality


def part_2(puzzle_input: str) -> str | int:
    blueprints = get_blueprints(puzzle_input)
    total = 1
    for blueprint_id, blueprint in blueprints.items():
        if blueprint_id > 3:
            continue
        start_state = State()
        start_state.fleet[Resource.ORE] += 1  # Start with one ore-mining robot
        max_fleet = get_max_fleet(blueprint)
        max_geodes = get_max_geodes(blueprint, start_state, 32, max_fleet=max_fleet)
        print(f"{max_geodes=} for {blueprint_id=}")
        total *= max_geodes
    return total


# Optimization ideas:
# Use numpy arrays (of length 4) everywhere
# Use greedy method (build highest-level robot possible, up to max) to get a lower bound on answer
# - then, use that lower bound to prune search paths that have no hope of getting there
# Considering branching based on a "goal" type of a robot, rather than second-by-second
