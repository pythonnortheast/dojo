"""

seeker_bot_v3.1.py

This bot seeks out closest enemy and tries to move towards it, and when close enough attacks.

Avoids collisions with own bots by not moving into space where the bots will move to.

"""

import random

import rg

class Robot:
    new_locs = []
    last_turn = 0

    def act(self, game):

        # When a new turn is started need to clear the new_locs list.
        if self.last_turn != game.turn:
            self.new_locs = []
            self.last_turn = game.turn


        # Create a list of distances to the enemy bots and their
        # locations.
        enemy_dist_and_locs = [(rg.dist(loc, self.location), loc)
                                for loc, bot in game.robots.iteritems() if
                                bot.player_id != self.player_id ]

        # Now sort by distance.
        enemy_dist_and_locs = sorted(enemy_dist_and_locs)

        closest_dist, closest_loc = enemy_dist_and_locs[0]

        if closest_dist <= 1 :
            self.new_locs.append(self.location)
            return ['attack', closest_loc]

        move_towards = rg.toward(self.location, closest_loc)
        self.new_locs.append(move_towards)
        return ['move', move_towards]

        random.seed()
        # Otherwise move around pick a direction that can randomly
        # move to and move there.
        moves = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))
        moves = [loc for loc in moves if loc not in self.new_locs]

        if len(moves) > 0:
            choice = random.choice(moves)
            self.new_locs.append(choice)
            return ['move', choice]

        self.new_locs.append(self.location)
        return ['guard']
