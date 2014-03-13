"""

random_walker_bot_v2.3.1.py

This bot randomly walks around and attacks any enemies that are close
by.

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
