#!/usr/bin/env python
# coding: utf-8
"""
RPSLS game - dojo version. A bit messy, but works (except draws) :P
AI strategy is to play randomly after a win and to counter opponent's
last move after a loss.

"""
import random

rules = {
	"r": ["ls", "crushes", "breaks"],
	"p": ["rS", "covers", "disproves"],
	"s": ["pl", "cut", "decapitate"],
	"l": ["pS", "eats", "poisons"],
	"S": ["rs", "vaporises", "smashes"],
}

names = {
	"r": "Rock",
	"p": "Paper",
	"s": "Scissors",
	"l": "Lizard",
	"S": "Spock",
}

class AI:
	def __init__(self):
		self.action = None

	def choice(self):
		if self.action:
			return self.action
		return random.choice("rpslS")

	def update(self, choice, winner):
		if winner == "AI":
			self.action = None
		else:
			options = [key for key, value in rules.items() if choice in value[0]]
			if options[0] in rules[options[1]][0]:
				self.action = options[1]
			else:
				self.action = options[0]


def result(choice, ai_choice):
	if ai_choice in rules[choice][0]:
		winner = names[choice]
		loser = names[ai_choice]
		index = rules[choice][0].find(ai_choice) + 1
		action = rules[choice][index]
		return " ".join([winner, action, loser]), "PLAYER"
	if choice in rules[ai_choice][0]:
		winner = names[ai_choice]
		loser = names[choice]
		index = rules[ai_choice][0].find(choice) + 1
		action = rules[ai_choice][index]
		return " ".join([winner, action, loser]), "AI"
	return "", "DRAW"


ai = AI()
points = (0, 0)

print "Let's play rock, paper, scissors, lizard, Spock!"

for i in range(10):
	print "Round " + str(i+1)
	while True:
		choice = raw_input("r/p/s/l/S ?")
		if choice in "rpslS":
			break

	ai_choice = ai.choice()
	message, winner = result(choice, ai_choice)
	ai.update(choice, winner)

	if winner == "PLAYER":
		points = (points[0] + 1, points[1])
	elif winner == "AI":
		points = (points[0], points[1] + 1)

	print "{0}\t({1})\t{2[0]}:{2[1]}".format(message, winner, points)
