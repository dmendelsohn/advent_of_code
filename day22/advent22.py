US_HP = 50
US_MANA = 500
BOSS_HP = 55
BOSS_POWER = 8

MISSILE = {'Name':'Missile', 'Cost':53}
DRAIN = {'Name':'Drain', 'Cost':73}
SHIELD = {'Name': 'Shield', 'Cost':113}
POISON = {'Name':'Poison', 'Cost':173}
RECHARGE = {'Name':'Recharge', 'Cost':229}
SPELLS = [MISSILE, DRAIN, SHIELD, POISON, RECHARGE]

MEMO = {}

def applyEffects(mana, bossHp, shieldCount, poisonCount, rechargeCount):
	if rechargeCount > 0:
		mana += 101
		rechargeCount -= 1
	if poisonCount > 0:
		bossHp -= 3
		poisonCount -= 1
	if shieldCount > 0:
		shieldCount -= 1
	return (mana, bossHp, shieldCount, poisonCount, rechargeCount)

#Returns minimum cost to win given a state of the game before beginning
#of the player's turn, or None if it's impossible to win.
def costToWin(bossHp, usHp, mana, \
		shieldCount, poisonCount, rechargeCount, spell, hardMode=False):
	inputs = (bossHp, usHp, mana, \
			shieldCount, poisonCount, rechargeCount, spell['Name'], hardMode)
	if inputs in MEMO: #Check if we've already computed this case
		return MEMO[inputs]

	#Apply hard mode rule
	if hardMode:
		usHp -= 1
		if usHp <= 0:
			MEMO[inputs] = None
			return None #We died

	#First apply effects at beginning of player's turn
	mana, bossHp, shieldCount, poisonCount, rechargeCount = \
			applyEffects(mana, bossHp, shieldCount, poisonCount, rechargeCount)

	#Check for game-ending conditions
	if bossHp <= 0:
		MEMO[inputs] = 0
		return 0 #It required no further mana to win
	if mana < 53:
		MEMO[inputs] = None
		return None #Can't afford to cast a spell, so we lose

	#Deal with the cost of the spell, and then cast it
	if spell['Cost'] > mana:
		MEMO[inputs] = None
		return None #We can't afford this spell
	else:
		mana -= spell['Cost'] # Pay up!
	name = spell['Name']
	if name == 'Missile':
		bossHp -= 4
	elif name == 'Drain':
		bossHp -= 2
		usHp += 2
	elif name == 'Shield':
		if shieldCount > 0:
			MEMO[inputs] = None
			return None #We played an invalid spell, so no way to win thusly
		else:
			shieldCount = 6
	elif name == 'Poison':
		if poisonCount > 0:
			MEMO[inputs] = None
			return None #We played an invalid spell, so no way to win thusly
		else:
			poisonCount = 6
	elif name == 'Recharge':
		if rechargeCount > 0:
			MEMO[inputs] = None
			return None #We played an invalid spell, so no way to win thusly
		else:
			rechargeCount = 5
	else:
		raise ValueError("Invalid spell")

	#Apply effects at beginning of boss turn
	mana, bossHp, shieldCount, poisonCount, rechargeCount = \
			applyEffects(mana, bossHp, shieldCount, poisonCount, rechargeCount)

	#Check for game-ending conditions
	if bossHp <= 0:
		MEMO[inputs] = spell['Cost']
		return spell['Cost'] #This last spell won us the game!

	#Boss attacks
	damage = BOSS_POWER
	if shieldCount > 0:
		damage -= 7 #Apply the shield, if necessary
	damage = max(1, damage) #Remember the minimum is 1
	usHp -= damage

	#Check for game-ending conditions
	if usHp <= 0:
		MEMO[inputs] = None
		return None #We died

	#Recursive call for next turn
	options = [costToWin(bossHp, usHp, mana, shieldCount, poisonCount, \
			rechargeCount, nextSpell, hardMode) for nextSpell in SPELLS]
	options = [o for o in options if o is not None]
	if len(options) == 0: #No way to win
		MEMO[inputs] = None
		return None
	else:
		best = min(options) + spell['Cost']
		MEMO[inputs] = best
		return best

def part1Answer():
	options = [costToWin(BOSS_HP, US_HP, US_MANA, 0, 0, 0, spell, False) \
			for spell in SPELLS]
	return min(options)

def part2Answer():
	options = [costToWin(BOSS_HP, US_HP, US_MANA, 0, 0, 0, spell, True) \
			for spell in SPELLS]
	return min(options)

if __name__ == "__main__":
	print("Part 1: %d" % (part1Answer(),))
	print("Part 2: %d" % (part2Answer(),))

