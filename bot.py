from random import choice
from game import Game
from game import Hero
from ai import next_move
from ai import reconstruct_path, a_star_search, manhattan_dist

import math

deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Bot:
    def move(self, state):
        self.game = Game(state)
        self.hero = Hero(state['hero'])

        target = self.hero.pos

        if self.should_go_to_nearest_life() and self.hero.calories >= 30:
            print "Need life"
            life_id = self.nearest(self.game.taverns_locs)
            target = self.game.taverns_locs[life_id]
        else:
            customer_id = self.nearest(self.game.customers_locs)
            if not self.require_burgers(self.game.customers[customer_id]) \
                    and not self.require_fries(self.game.customers[customer_id]):
                print "Go to customer"
                target = self.game.customers_locs[customer_id]
            elif self.require_burgers(self.game.customers[customer_id]):
                print "Go to burgers"
                target = self.nearest_dict(self.game.burger_locs)
            elif self.require_fries(self.game.customers[customer_id]):
                print "Go to fries"
                target = self.nearest_dict(self.game.fries_locs)

        self.game.board.tiles[target[0]][target[1]] = -1
        direction = next_move(self.game, self.hero.pos, target)

        return direction

    def nearest(self, positions):
        distance = 999999
        x1 = self.hero.pos[0]
        y1 = self.hero.pos[1]
        for i in range(len(positions)):
            x2 = positions[i][0]
            y2 = positions[i][1]

            temp = self.game.board.tiles[x2][y2]
            self.game.board.tiles[x2][y2] = -1

            dist = manhattan_dist((x1, y1), (x2, y2))

            self.game.board.tiles[x2][y2] = temp
            if dist < distance:
                distance = dist
                nearest = i
        return nearest

    def nearest_dict(self, positions):
        distance = 999999
        x1 = self.hero.pos[0]
        y1 = self.hero.pos[1]
        for key, value in positions.iteritems():
            x2 = key[0]
            y2 = key[1]

            temp = self.game.board.tiles[x2][y2]
            self.game.board.tiles[x2][y2] = -1

            dist = manhattan_dist((x1,y1), (x2,y2))

            self.game.board.tiles[x2][y2] = temp
            if dist < distance and str(value) != str(self.game.state['hero']['id']):
                distance = dist
                nearest = key
        return nearest

    def require_burgers(self, customer):
        if customer.burger > self.game.state['hero']['burgerCount']:
            return True
        return False

    def require_fries(self, customer):
        if customer.french_fries > self.game.state['hero']['frenchFriesCount']:
            return True
        return False

    def get_path_length(self, start, goal):
        came_from, cost_so_far = a_star_search(self.game, start, goal)

        path = reconstruct_path(came_from, start, goal)

        return len(path), path

    def should_go_to_nearest_life(self):
        life_id = self.nearest(self.game.taverns_locs)
        target = self.game.taverns_locs[life_id]

        temp = self.game.board.tiles[target[0]][target[1]]
        self.game.board.tiles[target[0]][target[1]] = -1
        path_len, path = self.get_path_length(self.hero.pos, target)
        self.game.board.tiles[target[0]][target[1]] = temp

        life_losing = path_len
        for tile in path:
            if tile in self.game.spikes_locs:
                life_losing += 10

        if self.hero.life - life_losing < 30:
            return True
        return False

class RandomBot(Bot):
    def move(self, state):
        game = Game(state)

        dirs = ['Stay', 'North', 'South', 'East', 'West']

        return choice(dirs)
