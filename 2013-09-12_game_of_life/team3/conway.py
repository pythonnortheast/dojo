# encoding: utf8
import copy
import os
import time
import random
import termcolor

WIDTH = 50
HEIGHT = 50

def print_grid(grid):
    alive_char = u'X'
    empty_char = u' '
    title = "TEAM 3's AWESOME GAME OF LIFE! YEH!"
    print title
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):

            if cell:
                print termcolor.colored('X', 'green' if alive_in_next_gen(grid, (x,y)) else 'red'),
            else:
                print '.' if alive_in_next_gen(grid, (x,y)) else ' ',
        print



def number_of_live_neighbours(grid, (x, y)):
    counter = 0

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if grid[(x + i) % WIDTH][(y + j) % HEIGHT]:
                counter += 1

    return counter

def alive_in_next_gen(grid, (x,y)):
    currently_alive = grid[x][y]
    live_neighbours = number_of_live_neighbours(grid, (x,y))

    if live_neighbours < 2 or live_neighbours > 3:
        return False
    elif live_neighbours in [2,3] and currently_alive:
        return True
    elif live_neighbours == 3 and not currently_alive:
        return True

    return currently_alive

if __name__ == '__main__':
    grid = [[bool(random.getrandbits(1)) for x in range(WIDTH)] for y in range(HEIGHT)]

    while True:
        os.system('clear')
        print_grid(grid)
        new_grid = copy.deepcopy(grid)

        for x in range(WIDTH):
            for y in range(HEIGHT):
                new_grid[x][y] = alive_in_next_gen(grid, (x,y))


        grid = new_grid

        time.sleep(0.2)
