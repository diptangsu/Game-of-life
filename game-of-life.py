import time
import os
import random
import sys
import copy

from seeds import *


CELLS = {
    DEAD: '⬜',
    LIVE: '⬛',
}


class Game:
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    @staticmethod
    def cls():
        """Clears the console using a system command.
        """
        if sys.platform.startswith('win'):
            os.system("cls")
        elif sys.platform.startswith('linux'):
            os.system("clear")
        else:
            print("Unable to clear terminal. \
                Your operating system is not supported.")

    @staticmethod
    def neighbors(x, y):
        """Generates the 8 adjacent neighboring cells
        """
        yield x + 1, y
        yield x - 1, y
        yield x + 1, y + 1
        yield x + 1, y - 1
        yield x - 1, y + 1
        yield x - 1, y - 1
        yield x, y + 1
        yield x, y - 1

    def draw(self):
        """Prints the board onto the console
        """
        print('Press <Ctrl+Z> or <Ctrl+C> to stop')
        for line in self.grid:
            print(*map(CELLS.get, line), sep='')

    def is_live(self, x, y):
        if x < 0 or y < 0 or x >= self.rows or y >= self.cols:
            return False

        return self.grid[x][y] == LIVE

    def next_gen(self):
        """Advances the board to the next generation
        """
        new_gen = copy.deepcopy(self.grid)
        for i in range(self.rows):
            for j in range(self.cols):
                population = sum(self.is_live(x, y)
                                 for x, y in self.neighbors(i, j))

                cell_value = self.grid[i][j]
                if population > 3:  # overpopulation, dies
                    cell_value = DEAD
                elif population < 2:  # underpopulation, dies
                    cell_value = DEAD
                elif population == 3:  # reproduction, lives
                    cell_value = LIVE
                elif cell_value == LIVE and population == 2 or population == 3:  # stasis, lives
                    cell_value = LIVE
                new_gen[i][j] = cell_value
        self.grid = new_gen


def run_game():
    seeds = dict(enumerate(SEEDS.keys()))
    print(*[f'{i}. {seed}' for i, seed in seeds.items()])
    try:
        seed = int(input('Pick a starting seed: '))
        INITIAL_SEED = SEEDS[seeds[seed]]
    except (ValueError, KeyError):
        print('Please enter a valid seed value')

    game = Game(INITIAL_SEED)
    while True:
        Game.cls()
        game.draw()
        game.next_gen()
        time.sleep(.3)


if __name__ == '__main__':
    run_game()
