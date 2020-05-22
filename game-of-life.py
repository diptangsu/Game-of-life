import time
import os
import random
import sys
import copy


def cls():
    """Clears the console using a system command based on the user's operating system.
    """
    if sys.platform.startswith('win'):
        os.system("cls")
    elif sys.platform.startswith('linux'):
        os.system("clear")
    else:
        print("Unable to clear terminal. Your operating system is not supported.")


LIVE, DEAD = 'O', '.'

chars = {
    DEAD: '⬜',
    LIVE: '⬛',
}

blinker = list(map(list, (
    '.........',
    '.........',
    '....O....',
    '....O....',
    '....O....',
    '.........',
    '.........',
)))

diehard = list(map(list, (
    '......O.',
    'OO......',
    '.O...OOO'
)))

seeds = {
    "diehard": [
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 1],
    ],
    "boat": [
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ],
    "r_pentomino": [
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0]
    ],
    "pentadecathlon": [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "beacon": [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ],
    "acorn": [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1]
    ],
    "spaceship": [
        [0, 0, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0],
        [0, 1, 1, 0, 0]
    ],
    "block_switch_engine": [
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
    ],
    "infinite": [
        [1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1],
    ],
}


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


def draw(grid):
    """Prints the board onto the console
    """
    for line in grid:
        print(*map(chars.get, line), sep='')


def draw2(rows: int, cols: int, cells: set):
    for i in range(rows):
        for j in range(cols):
            val = LIVE if (i, j) in cells else DEAD
            print(chars.get(val), end='')
        print()


def is_live(x, y, grid):
    rows, cols = len(grid), len(grid[0])
    if x < 0 or y < 0 or x >= rows or y >= cols:
        return False

    return grid[x][y] == LIVE


def next_gen(grid):
    """Advances the board to the next generation
    """
    new_gen = copy.deepcopy(grid)
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            population = sum(is_live(x, y, grid) for x, y in neighbors(i, j))

            cell_value = grid[i][j]
            if population > 3:  # overpopulation, dies
                cell_value = DEAD
            elif population < 2:  # underpopulation, dies
                cell_value = DEAD
            elif population == 3:  # reproduction, lives
                cell_value = LIVE
            elif cell_value == LIVE and population == 2 or population == 3:  # stasis, lives
                cell_value = LIVE
            new_gen[i][j] = cell_value
    return new_gen


def run_game():
    board = copy.deepcopy(blinker)
    for i in range(50):
        cls()
        draw(board)
        board = next_gen(board)
        time.sleep(.3)


if __name__ == '__main__':
    run_game()
