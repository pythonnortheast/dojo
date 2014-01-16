from __future__ import print_function

import random


SIZE=30

maze = [[[1,1] for i in range(SIZE)] for j in range(SIZE)]
top_maze = [" _"] * SIZE
path = {}

def display(maze):
    print("".join(top_maze))
    for row in maze:

        for left, bottom in row:
            pipe = "|" if left else " "
            underscore = "_" if bottom else " "
            print("{0}{1}".format(pipe, underscore), end="")
        print("|")

def draw_path(maze):
    x, y = random.randint(0, SIZE), 0
    top_maze[x] = "  "
    while y < SIZE:
        direction = random.randint(0, 8)

        if direction == 0:
            maze[y][x][1] = 0
            y += 1
            path[(x,y)] = True

        elif direction % 2 == 0:
            if x > 0:
                maze[y][x][0] = 0
                x = x - 1
                path[(x,y)] = True

        else:
            if x < SIZE - 1:
                x = x + 1
                maze[y][x][0] = 0
                path[(x,y)] = True

        """
        elif direction == 3:
            if y > 0:
                maze[y][x][1] = 0
                y -= 1
        """

def randomize(maze, path):
    for i in range(SIZE*SIZE):
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 2)

        if (x,y) not in path:
            if sum(maze[y][x]) > 0:
                wall = random.randint(0, 1)
                #if x > 0 and wall > 0:
                maze[y][x][wall] = 0

draw_path(maze)
#randomize(maze, path)
display(maze)



