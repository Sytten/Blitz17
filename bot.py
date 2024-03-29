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

        try:
            customer_id = self.nearest(self.game.customers_locs)

            if self.should_go_to_nearest_life() and self.hero.calories >= 30 and not self.can_deliver(customer_id):
                print "Need life"
                life_id = self.nearest(self.game.taverns_locs)
                target = self.game.taverns_locs[life_id]
            else:
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
        except:
            return "Stay"

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

        if goal not in came_from:
            return 1000000, [start, start]

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

        if self.hero.life - life_losing < self.calculate_life_buffer():
            return True
        return False

    def calculate_life_buffer(self):
        buffer = 10
        total_items = self.hero.burgers + self.hero.fries
        buffer += total_items * 3
        return min(buffer, 30)

    def can_deliver(self, customer_id):
        customer = self.game.customers[customer_id]
        if self.hero.burgers >= customer.burger and self.hero.fries >= customer.french_fries:
            target = self.game.customers_locs[customer_id]
            temp = self.game.board.tiles[target[0]][target[1]]
            self.game.board.tiles[target[0]][target[1]] = -1
            path_len, path = self.get_path_length(self.hero.pos, target)
            self.game.board.tiles[target[0]][target[1]] = temp

            life_losing = path_len
            for tile in path:
                if tile in self.game.spikes_locs:
                    life_losing += 10

            if self.hero.life - life_losing > 0:
                return True
        return False

class RandomBot(Bot):
    def move(self, state):
        game = Game(state)

        dirs = ['Stay', 'North', 'South', 'East', 'West']

        return choice(dirs)
