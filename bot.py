from random import choice
from game import Game
from game import Hero
from ai import next_move

deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Bot:
    def move(self, state):
        game = Game(state)
        hero = Hero(state['hero'])

        goal = game.burger_locs.keys()[0]
        possible_pos = []
        for delta in deltas:
            possible_pos.append((goal[0] + delta[0], goal[1] + delta[1]))
        possible_pos = filter(game.board.passable, possible_pos)

        return next_move(game, hero.pos, possible_pos[0])

class RandomBot(Bot):
    def move(self, state):
        game = Game(state)

        dirs = ['Stay', 'North', 'South', 'East', 'West']

        return choice(dirs)
