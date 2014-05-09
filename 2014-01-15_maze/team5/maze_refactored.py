#!/usr/bin/env python
# coding: utf-8
"""
ASCII maze generator (with post dojo refactoring and comments).

"""
import random

SIZE = 39

H_WALL = "_"
V_WALL = "|"
EMPTY = " "

LEFT = (-1,0)
RIGHT = (1,0)
DOWN = (0,1)


def display(maze):
	for row in maze:
		print "".join("".join(cell) for cell in row)


def draw_path(maze):
	# generate random starting point on top of the maze
	x, y = random.randint(0, SIZE), 1
	# delete bottom wall of the starting cell
	maze[0][x][1] = EMPTY
	# remember coordinates of maze cells on the walkthrough path
	path = {}

	while y < SIZE + 1:
		# make move left or right 3 times as likely as move down
		move = random.choice([DOWN] + [LEFT] * 3 + [RIGHT] * 3)

		# don't move beyond left or right border
		if not 0 < x + move[0] < SIZE -1:
			continue

		# remember current path cell
		path[(x,y)] = True

		# move to a new cell
		x, y =  x + move[0], y + move[1]

		# remove wall while moving
		if move == DOWN:
			# bottom wall of cell above
			maze[y-1][x][1] = EMPTY
		elif move == LEFT:
			# left wall of cell on the right
			maze[y][x+1][0] = EMPTY
		else:
			# left wall of current cell
			maze[y][x][0] = EMPTY

	return path


def randomize(maze, path):
	altered = 0
	# try to alter every cell not in the path
	while altered < SIZE * SIZE - len(path):
		x = random.randint(0, SIZE - 1)
		y = random.randint(1, SIZE)
		# do not alter path cells or those already altered before
		if (x,y) in path or EMPTY in maze[y][x]:
			continue

		# new "full" cell was found
		altered += 1

		# select wall to remove (0 = left, 1 = bottom)
		wall = random.randint(0, 1)
		# keep edges of the maze unchanged (left or bottom)
		if wall == 0 and x == 0 or wall == 1 and y == SIZE:
			continue

		# remove one of the two walls of the cell
		maze[y][x][wall] = EMPTY


# generate maze top line
maze = [[[EMPTY, H_WALL] for i in range(SIZE)]]

# fill maze rows
# each maze cell is build of two characters: left and bottom wall
for i in range(SIZE):
	# extra column at the end of a row is needed to have maze right edge
	row = [[V_WALL, H_WALL] for i in range(SIZE)] + [[V_WALL, EMPTY]]
	maze.append(row)

path = draw_path(maze)
randomize(maze, path) # comment this to see the solution path only
display(maze)
