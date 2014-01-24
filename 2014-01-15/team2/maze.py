from collections import namedtuple, deque
from random import random
import sys

Cell = namedtuple('Cell', 'visited x y')


class Mazer(object):
    """Maze generator"""
    def __init__(self):
        self.maze = self._gen_maze()
        self.origin = self.maze[0][0]
        self.walls = set(self.maze)
    
    def prims(self):
        pass

    @classmethod
    def _gen_maze(cls):
        return [[Cell(visited=False, x=c, y=r) for c in xrange(9)] for r in xrange(9)]

    def get_cell_walls(self, cell):
        """Get the walls of a cell"""
        x = cell.x
        y = cell.y
        walls = []
        
        try:
            walls.append(self.maze[y+1][x])
        except IndexError:
            pass

        try:
            walls.append(self.maze[y-1][x])
        except IndexError:
            pass

        try:
            walls.append(self.maze[y][x+1])
        except IndexError:
            pass

        try:
            walls.append(self.maze[y][x-1])
        except IndexError:
            pass
        
        return walls

if __name__ == 'main':
    mazer = Mazer()
