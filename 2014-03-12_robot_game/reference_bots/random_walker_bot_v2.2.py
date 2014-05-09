"""

random_walker_bot_v2.2.py

This bot attacks any enemies that are close by or otherwise moves
around randomly.

And now avoids moving into the locations where its own bots are.


"""

import random

import rg

class Robot:

    def act(self, game):
        # If there are enemies around, attack them.
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        own_locs = [loc for loc, bot in game.robots.iteritems()
                    if bot.player_id == self.player_id]

        random.seed()
        # Otherwise move around pick a direction that can randomly
        # move to and move there.
        moves = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))
        # Filter out those possible moves where own bots are.
        moves = [loc for loc in moves if loc not in own_locs]

        if len(moves) > 0:
            return ['move', random.choice(moves)]

        # If no moves available just guard
        return ['guard']
