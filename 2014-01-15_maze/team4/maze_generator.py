"""

Usage: maze_generator.py  <n>

"""

import docopt
import random
import copy

DIRS = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]
LOOKUPS = [ [[-1, -1], [-2, -1], [-2,0], [-2, 1], [-1,1]],
            [[1,1], [2,1], [2, 0], [2, -1], [1, -1]],
            [[-1,-1], [-1,-2], [0, -2], [1,-2], [1,-1]],
            [[1,1], [1,2], [0,2], [-1,2], [-1,1]]
             ]

def print_maze(grid):
    for x in grid:
        print ''.join(x)


def run(size):
    grid = [["X" for x in range(size) ] for x in range(size)]
    print_maze(grid)

    # start at top, end on bottom row

    # in order to have walls at the edge the col position of start and
    # end has to be between col 1 and size -2:
    start = (0, random.randint(1, size-2))
    end = (size-1, random.randint(1, size-2))

    if pick(grid, size, start, end, start):
        print "Solved"
        print_maze(grid)


def pick(grid, size, start, end, position):
    grid = copy.deepcopy(grid)
    # __TODO__ Change this:
    # find all our neighbours
    neighbours = [(position[0]+DIRS[i][0], position[1]+DIRS[i][1]) for i in range(4)]
    if end in neighbours:
        position = end
        grid[position[0]][position[1]] = "E"
        return True
    directions = [ d for d in (0, 1, 2, 3)
                   if (neighbours[d][0] >= 0 and neighbours[d][0] < size)
                   and (neighbours[d][1] >= 0 and neighbours[d][1] < size)
                   and grid[neighbours[d][0]][neighbours[d][1]] == 'X' ]

    # directions = [d for d in directions if grid[p[0]][p[1]] == 'X']

    tmp = []
    for d in directions:
        for t in LOOKUPS[d]:
            okay = False
            x = position[0] + t[0]
            y = position[1] + t[1]
            if x < 0 or x >= size or y < 0 or y >= size:
                break
            if (x,y) == end:
                okay = True
                break
            if grid[x][y] != 'X':
                break
            okay = True
        if okay:
            tmp.append(d)
    directions = tmp

    # shuffle list of neighbours
    random.shuffle(directions)

    print 'directions',  directions
    print 'position', position
    if position[0] == size-1:
        raw_input()


    # currently finding no possible directions when at the end of
    # the maze

    grid[position[0]][position[1]] = " "
    print 'start', start
    print 'end', end
    print_maze(grid)
    # raw_input()
    # for loop over test for neighbours
    for d in directions:
        # new_pos = (position[0] + n[0], position[1] + n[1])
        success = pick(grid, size, start, end, neighbours[d])
        if success:
            return True
    return False


    # return t/f for success or failure



if __name__ == "__main__":
    run(11)
