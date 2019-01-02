import re

class Group():
    def __init__(self, units, hp, attack_damage, attack_type, initiative, weaknesses, immunities):
        self.init_units = units
        self.units = units
        self.hp = hp
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.boost = 0

    @property
    def effective_power(self):
        return self.units * (self.attack_damage + self.boost)

    def calculate_received_damage(self, effective_power, attack_type):
        if attack_type in self.weaknesses:
            effective_power *= 2
        elif attack_type in self.immunities:
            effective_power = 0
        return effective_power        

    def receive_damage(self, effective_power, attack_type):  # Updates unit count and returns whether this group is destroyed
        damage = self.calculate_received_damage(effective_power, attack_type)
        self.units -= (damage / self.hp)
        if self.units <= 0:
            self.units = 0
            return True
        else:
            return False

    def __repr__(self):
        elts = sorted('{}={}'.format(k, v) for k, v in vars(self).items())
        return 'Group: ' + ', '.join(elts)


def parse(f):
    immune_system, infection = [], []
    for line in f.read().strip().split('\n'):
        if line == 'Immune System:':
            current = immune_system
        elif line == 'Infection:':
            current = infection
        elif line:  # Ignore empty lines
            current.append(parse_line(line))
    for i in range(len(immune_system)):
        immune_system[i].index = i
        immune_system[i].army = 0
    for i in range(len(infection)):
        infection[i].index = i
        infection[i].army = 1
    return immune_system, infection


# 17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
PATTERN = '([0-9]+) units each with ([0-9]+) hit points.*with an attack that does ([0-9]+) (.*) damage at initiative ([0-9]+)'
def parse_line(line):
    # First get the fixed fields that always appear once (no wekanesses or immunity)
    parts = re.search(PATTERN, line).groups()
    units = int(parts[0])
    hp = int(parts[1])
    attack_damage = int(parts[2])
    attack_type = parts[3]
    initiative = int(parts[4])

    weaknesses = []
    immunities = []
    start_index, end_index = line.find('('), line.find(')')
    if start_index != -1: 
        descriptions = line[start_index+1:end_index]
        descriptions = descriptions.replace(',', '').replace('; ', ';').split(';')  # Commas aren't useful, remove them, and extra space after semicolon
        for d in descriptions:
            if d.startswith('weak to '):
                weaknesses = d.split(' ')[2:]
            elif d.startswith('immune to '):
                immunities = d.split(' ')[2:]
            else:
                raise ValueError('Bad immunity or weakness description: {}'.format(d))

    return Group(units, hp, attack_damage, attack_type, initiative, weaknesses, immunities)


def select_targets(armies):  # Return tupe of list of target indices
    targets = ([-1]*len(armies[0]), [-1]*len(armies[1]))  # Initialize to all -1s
    for i in range(2):
        # Select by effective power
        selection_order = sorted(armies[i], key=lambda g: (g.effective_power, g.initiative), reverse=True)
        for group in selection_order:
            candidate_targets = filter(lambda g: g.index not in targets[i] and g.units > 0, armies[1-i])
            if not candidate_targets:  # No candidates remaining
                continue
            target = max(candidate_targets, key=lambda t: (t.calculate_received_damage(group.effective_power, group.attack_type), t.effective_power, t.initiative))
            would_deal = target.calculate_received_damage(group.effective_power, group.attack_type)
            if would_deal > 0:  # Only target if damage is positive
                # print('Army {}, Group {} selecting opponent Group {} to whom it would deal {} damage'.format(i, group.index, target.index, would_deal))
                targets[i][group.index] = target.index
    return targets


def execute_attacks(armies, targets):
    # TODO: execute attacks
    for group in sorted(armies[0]+armies[1], key=lambda g: g.initiative, reverse=True):
        if group.units > 0:
            target_army, target_index = 1-group.army, targets[group.army][group.index]
            if target_index < 0:  # No actual target
                #print('Army {}, Group {} has no target'.format(group.army, group.index))
                continue
            target = armies[target_army][target_index]
            target.receive_damage(group.effective_power, group.attack_type)
            #print('Army {}, Group {} attacked opponent Group {}'.format(group.army, group.index, target.index))
        else:
            pass
            #print('Army {}, Group {} is no longer alive and cannot attack opponent Group {}'.format(group.army, group.index, target.index))


def print_armies(armies):
    print('Immune System:')
    for group in armies[0]:
        print('Group {} has {} units\t({})'.format(group.index, group.units, group))
    print('Infection:')
    for group in armies[1]:
        print('Group {} has {} units\t({})'.format(group.index, group.units, group))


def is_alive(army):
    return any(group.units > 0 for group in army)

def battle(armies, boost=0):
    for group in armies[0]:  # Apply boost
        group.boost = boost
    for group in armies[0] + armies[1]:  # Rest units
        group.units = group.init_units
    # print_armies(armies)
    i = 0
    last_units_left = None
    units_left = sum(group.units for group in armies[0] + armies[1])
    while is_alive(armies[0]) and is_alive(armies[1]):
        i += 1
        #print('\nBEGIN STAGE {}'.format(i))
        targets = select_targets(armies)
        execute_attacks(armies, targets)
        #print_armies(armies)
        units_left = sum(group.units for group in armies[0] + armies[1])
        if last_units_left == units_left:  # Stalemate
            # print('Stalemate!')
            break
        last_units_left = units_left
        #print('{} units left'.format(units_left))
        #print('END STAGE {}\n'.format(i))
    if is_alive(armies[0]) and is_alive(armies[1]):
        return 0.5, units_left  # Draw
    elif is_alive(armies[1]):
        return 1, units_left
    else:
        return 0, units_left

def part1Answer(f):
    armies = parse(f)
    winner, units_left = battle(armies)
    # print('Winner: {}'.format(winner))
    return units_left


def part2Answer(f):
    # Binary search doesn't actually work because it's not monotonic.
    # The first win is at 90, but there are draws from 91-93.
    # At the end, hack where I drop by 5 and increment until I get it
    armies = parse(f)
    lo = 0
    hi = 10000
    while lo <= hi:
        mid = (hi + lo) / 2
        winner, _ = battle(armies, boost=mid)
        if winner == 0:  # Lower the boost
            hi = mid - 1
        else:  # Raise the boost
            lo = mid + 1
    boost = lo - 10  # Drop to account for non-monotonicity but only a little bit.  This is a hack
    while True:
        winner, left = battle(armies, boost=boost)
        if winner == 0:
            print('Minimum boost: {}'.format(boost))
            return left
        boost += 1

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))

