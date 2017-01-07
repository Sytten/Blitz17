from random import choice
from game import Game
from game import Hero
from ai import next_move

import math

deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Bot:
    def move(self, state):
        game = Game(state)
        hero = Hero(state['hero'])

        if self.hero.life < 40:
            life_id = self.nearest(self.game.taverns_locs)
            direction = self.request_direction(self.game.taverns_locs[life_id])
        else:
            customer_id = self.nearest(self.game.customers_locs)
            if not self.require_burgers(self.game.customers[customer_id]) and not self.require_fries(
                    self.game.customers[customer_id]):
                direction = self.request_direction(self.game.customers_locs[customer_id])
            elif self.require_burgers(self.game.customers[customer_id]):
                direction = self.request_direction(self.nearest_dict(self.game.burger_locs))
            elif self.require_fries(self.game.customers[customer_id]):
                direction = self.request_direction(self.nearest_dict(self.game.fries_locs))
        return direction


        goal = game.burger_locs.keys()[0]
        possible_pos = []
        for delta in deltas:
            possible_pos.append((goal[0] + delta[0], goal[1] + delta[1]))
        possible_pos = filter(game.board.passable, possible_pos)

        return next_move(game, hero.pos, possible_pos[0])

    def nearest(self, positions):
        distance = 999999
        x1 = self.hero.pos['x']
        y1 = self.hero.pos['y']
        for i in range(len(positions)):
            print positions
            x2 = positions[i][0]
            y2 = positions[i][1]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < distance:
                distance = dist
                nearest = i
        return nearest

    def nearest_dict(self, positions):
        distance = 999999
        x1 = self.hero.pos['x']
        y1 = self.hero.pos['y']
        for key, value in positions.iteritems():
            x2 = key[0]
            y2 = key[1]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < distance:
                distance = dist
                nearest = key
        return nearest


class RandomBot(Bot):
    def move(self, state):
        game = Game(state)

        dirs = ['Stay', 'North', 'South', 'East', 'West']

        return choice(dirs)
