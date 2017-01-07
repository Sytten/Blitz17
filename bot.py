from random import choice
from game import Game
from ai import a_star_search

class Bot:
    def move(self, state):
        game = Game(state)
        id = state['hero']['id']
        hero = game.heroes[id]

        path = a_star_search(game, hero.pos, game.burger_locs[0])

class RandomBot(Bot):
    def move(self, state):
        game = Game(state)

        dirs = ['Stay', 'North', 'South', 'East', 'West']

        return choice(dirs)
