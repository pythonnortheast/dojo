"""
Destroyer - refactored version with improved spawn zone avoidance.

"""
import rg
import numpy
import random

class Robot:
	next_locations = {}
	last_turn = -1
	enemies = None

	def act(self, game):
		if game.turn != self.last_turn:
			self.next_locations = {}
			self.last_turn = game.turn

			self.enemies = numpy.array([location for location, bot in
				game.robots.iteritems()	if bot.player_id != self.player_id])

		# try to escape from the spawn location
		if "spawn" in rg.loc_types(self.location):
			targets = rg.locs_around(self.location, filter_out=["spawn", "obstacle"])
			if not targets:
				targets = rg.locs_around(self.location, filter_out=["obstacle"])
			random.shuffle(targets)
			for target in targets:
				if target not in self.enemies and target not in self.next_locations:
					self.next_locations[target] = self.robot_id
					return ["move", target]

		# calculate manhattan distance between current robot and all enemies
		try:
			distances = numpy.sum(numpy.abs(self.enemies - self.location), axis=1)
		except ValueError:
			distances = []

		# index sort distances
		indices = numpy.argsort(distances)

		# if no enemies on the map, move towards center
		if len(indices) == 0:
			target = rg.toward(self.location, rg.CENTER_POINT)
			self.next_locations[target] = self.robot_id
			return ["move", target]

		# select 4 nearest enemies
		# count how many of them are in attacking distance
		count_near = numpy.sum(distances[indices[:4]] == 1)

		# commit suicide if surrounded and likely to die soon
		if count_near >= 2 and (self.hp < 1 + 10 * count_near or game.turn % 10 == 9):
			return ["suicide"]

		# choose an enemy to persuit
		for i in indices:
			enemy = tuple(self.enemies[i])

			# attack if enemy is close enough
			if distances[i] == 1:
				self.next_locations[self.location] = self.robot_id
				return ["attack", enemy]

			target = rg.toward(self.location, enemy)

			# don't move into the spawn zone before the spawn round
			if (game.turn % 10 == 0 or game.turn % 10 > 7):
				if "spawn" in rg.loc_types(target):
					continue

			# move if no other robot is moving into the same position
			if target not in self.next_locations:
				self.next_locations[target] = self.robot_id
				return ["move", target]

		# if you can't attack or move near an enemy, move to where you can
		targets = rg.locs_around(self.location, filter_out=["spawn", "obstacle"])
		random.shuffle(targets)
		for target in targets:
			if target not in self.next_locations:
				self.next_locations[target] = self.robot_id
				return ["move", target]

		# if you can't move, guard
		self.next_locations[self.location] = self.robot_id
		return ["guard"]
