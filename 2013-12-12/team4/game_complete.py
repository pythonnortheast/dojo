#!/usr/bin/env python
"""
Simple text-based adventure game with Santa theme.

"""
import json
import random
import curses
from collections import OrderedDict

class Screen:
	def __init__(self):
		# initialize curses window
		self.screen = curses.initscr()

		# initialize a color set
		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)

		# disable echoing of inserted characters
		curses.noecho()
		# disable input buffering to read single key presses
		curses.cbreak()

		# enable window auto scroll
		self.screen.scrollok(True)

	def destroy(self):
		# restore terminal settings and close curses window
		curses.echo()
		curses.nocbreak()
		curses.endwin()

	def add_text(self, text, color=1):
		self.screen.addstr(text, curses.color_pair(color))
		self.screen.refresh()

	def add_bold_text(self, text):
		self.add_text("{0}\n".format(text), 3)

	def add_actions(self, actions):
		for i, action in enumerate(actions):
			self.screen.addstr("[{0}] {1}\n".format(i + 1, action[0]), curses.color_pair(2))
		self.screen.refresh()

	def read_key(self):
		return self.screen.getkey()


class Location:
	def __init__(self, data):
		# add all objects in data as class fields
		self.__dict__.update(data)

		# remember actions leading to the next level (first action on the list)
		self.level_actions = [actions[0][0] for actions in self.actions]
		# shuffle the actions order on each level
		for level in self.actions:
			random.shuffle(level)

	def play(self):
		screen.add_text("\n{0}\n".format(self.description))
		# if one level of actions only - game completed
		if len(self.actions) == 1:
			screen.add_bold_text("\nVICTORY\n")

		# ask what to do
		if self.actions:
			self.read_action(0)
		# if no actions are given, game is over
		else:
			screen.add_bold_text("\nGAME OVER\n")
			screen.read_key()

	def read_action(self, level):
		# display possible actions at current level
		screen.add_actions(self.actions[level])

		# read user choice
		while True:
			choice = screen.read_key()
			try:
				choice = int(choice) - 1
				action, result = self.actions[level][choice]
				break
			except ValueError:
				if "q" == choice:
					return
				continue
			except IndexError:
				continue

		# if result is a location number, change location
		if int == type(result):
			locations[result].play()
			return

		# move to the next level
		if self.level_actions[level] == action:
			screen.add_text("\n{0}\n".format(result))
			self.read_action(level + 1)
		# stay at current level
		else:
			screen.add_text("\n{0}\n".format(result))
			self.read_action(level)


#initialise screen
screen = Screen()

# read game data
with open("locations.json") as input_file:
	locations = [Location(data) for data in json.load(input_file)]

# start the game
locations[0].play()

# restore terminal settings
screen.destroy()
