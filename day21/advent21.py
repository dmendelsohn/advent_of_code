import math

def parseInput(f):
	lines = [line.strip() for line in f]
	hp = int(lines[0].split(' ')[-1])
	damage = int(lines[1].split(' ')[-1])
	armor = int(lines[2].split(' ')[-1])
	return (hp, damage, armor)

def parseShop(f):
	lines = [line.strip() for line in f if len(line.strip())>0]
	currentType = None
	weapons = []
	armor = []
	rings = []
	for line in lines:
		parts = line.split()
		if parts[0][-1] == ':':
			currentType = parts[0][:-1]
		else:
			name = parts[0]
			cost = int(parts[1])
			damage = int(parts[2])
			arm = int(parts[3])
			if currentType == 'Weapons':
				weapons.append((cost, damage, arm, name))
			elif currentType == 'Armor':
				armor.append((cost, damage, arm, name))
			elif currentType == 'Rings':
				rings.append((cost, damage, arm, name))
			else:
				raise ValueError("Invalid input in shop text file")
	return (weapons, armor, rings)

#Both us and them are of the form hp, damage, armor 
def isWin(us, them):
	dealt = max(us[1] - them[2], 1)
	received = max(them[1] - us[2], 1)
	turnsToWin = math.ceil(float(them[0]) / dealt)
	turnsToLose = math.ceil(float(us[0]) / received)
	return turnsToWin <= turnsToLose

def getMinimumKit(usHp, them, shop):
	(weapons, bodyArmor, rings) = shop
	bodyArmor = bodyArmor[:]
	rings = rings[:]
	bodyArmor.append((0, 0, 0, "NoArmor")) #Augment with null armor
	rings.append((0, 0, 0, "NoRings1")) #Augment with first null rings
	rings.append((0, 0, 0, "NoRings2")) #Augment with second null rings
	bestSoFar = (1000, None, None, None, None)
	for weapon in weapons:
		for ba in bodyArmor:
			for ring1 in rings:
				for ring2 in rings:
					if ring1 != ring2:
						cost = weapon[0] + ba[0] + ring1[0] + ring2[0]
						usDamage = weapon[1] + ba[1] + ring1[1] + ring2[1]
						usArmor = weapon[2] + ba[2] + ring1[2] + ring2[2]
						us = (usHp, usDamage, usArmor)
						if isWin(us, them) and cost < bestSoFar[0]:
							bestSoFar = (cost, weapon[3], ba[3], \
									ring1[3], ring2[3])
	return bestSoFar

def getMaximumKit(usHp, them, shop):
	(weapons, bodyArmor, rings) = shop
	bodyArmor = bodyArmor[:]
	rings = rings[:]
	bodyArmor.append((0, 0, 0, "NoArmor")) #Augment with null armor
	rings.append((0, 0, 0, "NoRings1")) #Augment with first null rings
	rings.append((0, 0, 0, "NoRings2")) #Augment with second null rings
	bestSoFar = (0, None, None, None, None)
	for weapon in weapons:
		for ba in bodyArmor:
			for ring1 in rings:
				for ring2 in rings:
					if ring1 != ring2:
						cost = weapon[0] + ba[0] + ring1[0] + ring2[0]
						usDamage = weapon[1] + ba[1] + ring1[1] + ring2[1]
						usArmor = weapon[2] + ba[2] + ring1[2] + ring2[2]
						us = (usHp, usDamage, usArmor)
						if not isWin(us, them) and cost > bestSoFar[0]:
							bestSoFar = (cost, weapon[3], ba[3], \
									ring1[3], ring2[3])
	return bestSoFar



def part1Answer(them, shop):
	minKit = getMinimumKit(100, them, shop)
	print("Cheapest winning kit: %s" % (str(minKit),))
	return minKit[0]

def part2Answer(them, shop):
	maxKit = getMaximumKit(100, them, shop)
	print("Most expensive losing kit: %s" % (str(maxKit),))
	return maxKit[0]

if __name__ == "__main__":
	f = open('input.txt', 'rt')
	them = parseInput(f)
	f = open('shop.txt', 'rt')
	shop = parseShop(f)
	print("Part 1: %d" % (part1Answer(them, shop),))
	print("Part 2: %d" % (part2Answer(them, shop),))

