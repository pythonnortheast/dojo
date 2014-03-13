"""

random_walker_bot_v2.3.py

This bot randomly walks around and attacks any enemies that are close
by.


"""

import random

import rg

class Robot:
    new_locs = []

    def act(self, game):

        # If there are enemies around, attack them.
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    self.new_locs.append(self.location)
                    return ['attack', loc]

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
