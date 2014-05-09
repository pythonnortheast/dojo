"""
Destroyer - dojo version:
- won best of 3, draw best of 5 and lost best of 7 against Suicide Maniac

"""
import rg

class Robot:
	new_locs = {}

	def act(self, game):
		# list of distances to the enemy bots and their locations
		enemy_dist_and_locs = [(rg.dist(loc, self.location), loc) for loc, bot in game.robots.iteritems() if bot.player_id != self.player_id ]

		# sort by distance.
		enemy_dist_and_locs.sort()
		neighbours = [ (dist, loc) for dist, loc in enemy_dist_and_locs[:4] if dist <= 1 ]

		# try to escape from spawn location
		# (this is buggy)
		if (game.turn + 1) % 10 and rg.loc_types(self.location) == "spawn":
			location = rg.toward(self.location, rg.CENTER_POINT)
			if location in game.robots:
				return ["suicide"]
			else:
				return ["move", location]

		# commit suicide if surrounded and likely to die soon
		if len(neighbours) >= 2 and self.hp < 1 + len(neighbours) * 10:
			print "BOOOM", self.location
			return ["suicide"]

		# choose an enemy to destroy
		for dist, loc in enemy_dist_and_locs:
			# attack if close
			if dist == 1 :
				self.new_locs[self.robot_id] = self.location
				return ["attack", loc]

			# move if no other robot is moving into the same position
			move_towards = rg.toward(self.location, loc)
			for key, value in self.new_locs.items():
				if value == move_towards and key != self.robot_id:
					break
			else:
				self.new_locs[self.robot_id] = move_towards
				return ["move", move_towards]

		# if you can"t attack or move near an enemy, guard
		return ["guard"]
