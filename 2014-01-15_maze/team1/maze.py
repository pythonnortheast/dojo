from copy import copy
from random import randint

OPEN = '.'
CLOSED = '#'

entrance = 1
exit = 1
maze_size = 12


def base_maze(size):
    global maze
    global entrance
    global exit
    global maze_size

    maze_size = size

    horizontal_wall = [CLOSED] * (size + 2)
    inner_wall = [CLOSED]
    for col in range(size):
        inner_wall.append(OPEN)
    inner_wall.append(CLOSED)
    maze = [horizontal_wall]

    for line in range(size):
        maze.append(copy(inner_wall))

    maze.append(horizontal_wall)
    entrance = randint(1, size)
    exit = randint(1, size)
    maze[entrance][0] = '!'
    maze[exit][size + 1] = '!'


def count_adjacent(x, y):
    """Count the adjacent tiles to the given x and y.
    """
    walls = maze[y][x-1], maze[y][x+1], maze[y-1][x], maze[y+1][x]
    return sum(w == CLOSED for w in walls)


def count_diagonal(x, y):
    """
    """
    walls = maze[y-1][x-1], maze[y-1][x+1], maze[y+1][x-1], maze[y+1][x+1]
    return sum(w == CLOSED for w in walls)


def maze_closed(x, y):
    """Special function that tells us if it blocks the entrance.
    """
    return y == 6 and (x in (1, 13))


def diagonals_allowed(x, y):
    """
    """
    if x in (1, maze_size + 1) and y in (entrance, exit):
        return 0
    elif x in (1, maze_size + 1) or y in (1, maze_size + 1):
        return 2
    else:
        return 0


def can_drop(x, y):
    """
    """
    return (
        count_adjacent(x, y) <= 1 and not maze_closed(x, y) and
        count_diagonal(x, y) <= diagonals_allowed(x, y))


def is_wall(x, y):
    """
    """
    return maze[y][x] == CLOSED


def drop_wall():
    for x in range(10):
        x = randint(1, maze_size)
        y = randint(1, maze_size)
        if not is_wall(x, y):
            break

    if can_drop(x, y):
        maze[y][x] = CLOSED


def print_maze():
    return '\n'.join(''.join(line) for line in maze)



def generate_maze():
    for x in range(100000):
        drop_wall()


if __name__ == '__main__':
    import sys
    base_maze(int(sys.argv[1]))
    generate_maze()
    print print_maze()
