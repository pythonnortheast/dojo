#!/usr/bin/env python
"""
Simple text-based adventure game with Santa theme.

"""
import random
from collections import OrderedDict


class Location:
	def __init__(self, description, options):
		self.options = options
		self.description = description

	def play(self):
		print description
		self.read_action(0)

	def read_action(self, level):
		actions = self.options[level].keys()[:]
		# remember first action, which is leading to next level
		next_level_action = actions[0]
		# shuffle actions order
		random.shuffle(actions)

		print next_level_action, actions

		# display possible actions
		for i, action in enumerate(actions):
			print "[{0}] {1}".format(i, action)

		# read user choice
		while True:
			choice = raw_input("What do you want to do? ")
			try:
				choice = int(choice)
				action = actions[choice]
				break
			except ValueError:
				print "Don't be naughty."
				continue

		result = self.options[level][action]

		# if result is a location object, go to next the location
		if type(result) != str:
			result.play()
			return

		# move to the next level
		if next_level_action == action:
			print "\n", result
			self.read_action(level + 1)
		# stay on current level
		else:
			print "\n", result
			self.read_action(level)

"""
STORY
1. find out whats wrong
2. go to last location
3. hotel for raindeer
4. talk to manager - raindeer called, he needs help
5. zombies
6. fight them with fire
"""

description = "You are in the Santa's house."
options = [
	OrderedDict({
		"ask what's wrong": "Brian, the reindeer is missing.",
		"ask for a present": "Santa says you should wait till Christmas.",
		"ask for a cup of tea": "Santa brings you a cup of warm deliciously smelling cup of tea."
	}),
	OrderedDict({
		"ask for Brian last known location": "You WON!!",
		"ask why Santa named a reindeer Brain": "It's after Brian May, the guitarist from Queen.",
		"ask why Brian is so important": "He's the fastest and strongest reindeer ever."
	})
]
loc_santa = Location(description, options)

description = "You have received a letter from a Santa."
options = [
	OrderedDict({
		"read the letter": "Letter says: 'I need your help. Could you come and visit me?'",
		"eat the letter": "The letter is written with large font. It will take you a week to eat it."
	}),
	OrderedDict({
		"go to north pole": loc_santa,
		"go home": "Hey! You can't let down all the kids!"
	})
]
loc_letter = Location(description, options)

loc_letter.play()

