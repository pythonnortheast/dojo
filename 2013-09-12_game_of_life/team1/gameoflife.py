"""
Grid
"""
import os
import random
import time


class Game(object):
    empty = u' '
    alive = u'\4'

    @classmethod
    def clear_screen(cls):
        if not hasattr(cls, '_clear_screen'):
            if os.name == 'nt':
                cls._clear_screen = 'cls'
            else:
                cls._clear_screen = 'clear'
        os.system(cls._clear_screen)
        print("Conway's Game of Life")
    
    def __init__(self, size=(10,10), cells=None):
        if cells is None:
            cells = []
        self.size = size
        if cells:
            self.grid = [[self.alive if (y,x) in cells else self.empty for x in range(self.size[0])] for y in range(self.size[1])]
        else:
            self.grid = [[random.choice([self.empty, self.alive]) for x in range(self.size[0])] for y in range(self.size[1])]

    def cell_alive(self, row, col):
        if row < 0 or col < 0:
            return False
        try:
            return self.grid[row][col] == self.alive
        except IndexError:
            return False
                
    def cell_survives(self, row, col):
        alive = self.cell_alive(row, col)
        living_neighbours = self.living_neighbours(row, col)
        if living_neighbours == 2:
            return alive
        elif living_neighbours == 3:
            return True
        return False
        
    def living_neighbours(self, row, col):
        above = self.cell_alive(row - 1, col)
        below = self.cell_alive(row + 1, col)
        left = self.cell_alive(row, col - 1)
        right = self.cell_alive(row, col + 1)
        return above+below+left+right

    def take_turn(self):
        grid = [[self.empty for x in range(self.size[0])] for y in range(self.size[1])]
        for row_number,row in enumerate(self.grid):
            for cell_number,_ in enumerate(row):
                if self.cell_survives(row_number, cell_number):
                    grid[row_number][cell_number] = '{}'.format(self.alive)
        keep_going = self.grid != grid
        self.grid = grid
        self.print_grid()
        return keep_going

    def print_grid(self):
        for row in self.grid:
            print(''.join(cell for cell in row))

    def play(self):
        self.clear_screen()
        while self.take_turn():
            time.sleep(.5)
            self.clear_screen()
            

if __name__ == '__main__':
    game = Game(size=(45,30))
    game.play()
