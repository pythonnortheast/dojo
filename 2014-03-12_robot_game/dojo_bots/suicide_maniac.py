
import random
import rg

class Robot:
    new_locs = []
    last_turn = 0
    
    def act(self, game):
        bots = {
            'attackable_bots': [],
            'friendly_bots': []
        }
        
        # When a new turn is started need to clear the new_locs list.
        if self.last_turn != game.turn:
            self.new_locs = []
            self.last_turn = game.turn
    
        # If there are enemies around, attack them.
        for loc, bot in game.robots.iteritems():
            if rg.dist(loc, self.location) <= 1:
                if bot.player_id != self.player_id:
                    bots['attackable_bots'].append(bot)
                else:
                    bots['friendly_bots'].append(bot)
        
        # Suicide
        sorted(bots['attackable_bots'], key=lambda k: k['hp']) 
        if bots['attackable_bots']:
            if len(bots['attackable_bots']) == 1:
                return ['attack', bots['attackable_bots'][0].location]
            total_hp = sum([bot.hp for bot in bots['attackable_bots']])
            
            if len(bots['attackable_bots']) * 10 > self.hp:
                return ['suicide']
            else:
                return ['attack', bots['attackable_bots'][0].location]

        own_locs = [loc for loc, bot in game.robots.iteritems()
                    if bot.player_id == self.player_id]
                    
        # Otherwise find possible moves around the bot and then
        # randomly pick one.
        moves = [loc for loc in rg.locs_around(self.location, filter_out=('invalid', 'obstacle')) if loc not in own_locs]

        # Create a list of distances to the enemy bots and their
        # locations.
        enemy_dist_and_locs = [(rg.dist(loc, self.location), loc)
            for loc, bot in game.robots.iteritems() if
            bot.player_id != self.player_id ]

        # Now sort by distance.
        enemy_dist_and_locs = sorted(enemy_dist_and_locs)

        closest_dist, closest_loc = enemy_dist_and_locs[0]
        
        if closest_dist <= 1:
            self.new_locs.append(self.location)
            return ['attack', closest_loc]
        #elif closest_dist > 9:
        move_towards = rg.toward(self.location, closest_loc)
        #else:
        #    sorted(bots['friendly_bots']) 
        #    move_towards = rg.toward(self.location, bots['friendly_bots'][0])
        
        
        
        self.new_locs.append(move_towards)
        return ['move', move_towards]