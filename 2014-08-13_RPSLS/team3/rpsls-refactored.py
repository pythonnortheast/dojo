#!/usr/bin/env python
# coding: utf-8
"""
RPSLS game - refactored version. Handles the gameplay correctly
and uses more complex AI that tries to learn and counter the human's
strategy.

"""
import random
from collections import defaultdict


class Counters(dict):
	"""
	Dictionary of counters to each weapon.

	"""
	def __init__(self, file_name):
		counters = defaultdict(dict)

		with open(file_name) as rules:
			for rule in rules:
				winner, action, loser = rule.split()
				counters[loser].update([(winner, action)])

		self.update(counters)


class AI:
	"""
	Choose single counter or double counter play depending on
	the rate of success of each startegy in the past.

	"""
	def __init__(self):
		self.weapon = None
		self.strategy = "random"
		self.wins = defaultdict(int)
		self.loses = defaultdict(int)

	def choose_weapon(self):
		if self.weapon:
			return self.weapon
		self.strategy = "random"
		return random.choice(counters.keys())

	def update(self, weapon, has_won):
		if has_won:
			self.wins[self.strategy] += 1
			self.weapon = None
		else:
			self.loses[self.strategy] += 1
			# check how successful each strategy has been so far
			deltas = [self.wins[s] - self.loses[s] for s in ["single", "double"]]

			# single counter strategy
			self.strategy = "single"
			options = counters[weapon].keys()
			if options[0] in counters[options[1]]:
				self.weapon = options[0]
			else:
				self.weapon = options[1]

			# double counter strategy (if double was more successful)
			if deltas[0] < deltas[1]:
				self.strategy = "double"
				options = set(counters.keys())
				# find weapons countering my best counter
				player_weapons = counters[self.weapon].keys()
				# find a weapon that counters them both
				for weapon in player_weapons:
					options = options.intersection(counters[weapon].keys())
				self.weapon = options.pop()


def fight(player_weapon, ai_weapon):
	if player_weapon in counters[ai_weapon]:
		result = " ".join([player_weapon, counters[ai_weapon][player_weapon], ai_weapon])
		return result, "PLAYER"

	if ai_weapon in counters[player_weapon]:
		result = " ".join([ai_weapon, counters[player_weapon][ai_weapon], player_weapon])
		return result, "AI"

	result = " ".join([player_weapon, "does nothing to", ai_weapon])
	return result, "DRAW"


counters = Counters("rules.txt")
ai = AI()
score = [0, 0]

weapons = {weapon[0].lower():weapon for weapon in counters.keys() if weapon != "Spock"}
weapons["S"] = "Spock"

print "Let's play rock-paper-scissors-lizard-Spock!"

for i in range(1, 11):
	print "Round", str(i)
	while True:
		choice = raw_input("Your weapon (r/p/s/l/S)? ")
		if choice in "rpslS":
			player_weapon = weapons[choice]
			break

	ai_weapon = ai.choose_weapon()
	result, winner = fight(player_weapon, ai_weapon)
	ai.update(player_weapon, winner == "AI")

	if winner == "PLAYER":
		score[0] += 1
	elif winner == "AI":
		score[1] += 1

	print "{0:35} {1:6}  {2[0]}:{2[1]}".format(result, winner, score)

if score[1] > score[0]:
	print "\nI won using these strategies:"
	print dict(ai.wins)
