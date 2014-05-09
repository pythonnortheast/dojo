#!/usr/bin/env python
# coding: utf-8

"""
Game of PONG, part of pygame tutorial.
Copyright (C) 2013  Paweł Widera

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details:
http://www.gnu.org/licenses/gpl.txt


Additional changes compared to the tutorial:
- computer controls player1
- game ends at 10 points and the score is reset
- extra sprite for game over animation
- all sprites dimensions are scaled to the screen resolution
- doctest examples, to run tests use "python -m doctest pong.py"

"""

import math
import random
import operator
import pygame

from pygame.sprite import Sprite


WIDTH = 320
HEIGHT = 240
FPS = 30
POINTS_TO_WIN = 10


class Ball(Sprite):
	"""
	Handles behaviour of the ball.

	"""
	def __init__(self, color, position, rackets, score):
		# call parent class constructor
		Sprite.__init__(self)

		# create surface
		self.image = pygame.Surface([HEIGHT/40, HEIGHT/40])
		# draw filled circle
		pygame.draw.circle(self.image, pygame.Color(color), (HEIGHT/80,HEIGHT/80), HEIGHT/80)

		# get sprite bounding box
		self.rect = self.image.get_rect()
		# set sprite initial position
		self.rect.center = position

		# two dimensional velocity vector
		self.velocity = [0,0]
		# remember starting point
		self.start = position
		# remember racket and score sprites
		self.rackets = rackets
		self.score = score

	def serve(self):
		# if the ball is already in play, do nothing
		if self.velocity[0] != 0:
			return

		# random angle in radians (between 0 and 60 degrees)
		angle = random.uniform(0, math.pi/3)
		angle *= random.choice([-1,1])

		# choose serving side randomly
		side = random.choice([-1,1])
		# rotate the velocity vector [1, 0], flip horizontally if side < 0
		self.velocity = [side * HEIGHT/48 * math.cos(angle), HEIGHT/48 * math.sin(angle)]

	def update(self):
		self.rect.move_ip(*self.velocity)

		# bounce the ball of the top screen border
		if self.rect.top < 0:
			self.velocity[1] *= -1
			self.rect.top = 1
		# bounce the ball of the bottom screen border
		elif self.rect.bottom > HEIGHT:
			self.velocity[1] *= -1
			self.rect.bottom = HEIGHT-1

		# detect collision with the rackets
		for racket in self.rackets:
			if self.rect.colliderect(racket.rect):
				# bounce the ball of the racket
				self.velocity[0] *= -1
				self.rect.x += self.velocity[0]
				# pass some racket velocity to the ball
				self.velocity[1] += 0.5 * racket.velocity
				# don't check both rackets
				break

		# detect goal
		if self.rect.centerx < 0 or self.rect.centerx > WIDTH:
			# add a point to the score
			side = 1 if self.rect.centerx < 0 else 0
			self.score.increase(side)
			# set the ball in the starting position
			self.rect.center = self.start
			self.velocity = [0,0]


class Racket(Sprite):
	"""
	Handles behaviour of the players racket.

	"""
	def __init__(self, color, position):
		Sprite.__init__(self)
		self.image = pygame.Surface([WIDTH/80, HEIGHT/12])
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, pygame.Color(color), self.rect)
		self.rect.center = position

		# one dimensional velocity vector (vertical axis only)
		self.velocity = 0

	def up(self):
		self.velocity -= HEIGHT/48

	def down(self):
		self.velocity += HEIGHT/48

	def update(self):
		"""
		>>> racket = Racket("red", (0,0))

		>>> racket.rect.top = 100
		>>> racket.velocity = -200
		>>> racket.update()
		>>> racket.rect.top
		0

		>>> racket.rect.bottom = HEIGHT-100
		>>> racket.velocity = 200
		>>> racket.update()
		>>> racket.rect.bottom == HEIGHT
		True
		"""
		self.rect.move_ip(0, self.velocity)
		# move only within the screen border
		self.rect.top = max(0, self.rect.top)
		self.rect.bottom = min(HEIGHT, self.rect.bottom)


class Score(Sprite):
	"""
	Displays the game score.

	"""
	def __init__(self, color, position):
		pygame.sprite.Sprite.__init__(self)
		self.color = pygame.Color(color)
		self.score = [0,0]

		# use system font of a given size
		self.font = pygame.font.SysFont("monospace", WIDTH/10, bold=True)
		self.render_text()

		self.rect = self.image.get_rect()
		self.rect.center = position

	def render_text(self):
		self.image = self.font.render("{0:>2d}  {1:<2d}".format(*self.score), True, self.color)

	def increase(self, side):
		self.score[side] += 1
		self.render_text()

	def reset(self):
		self.score = [0,0]
		self.render_text()


class GameOver(Sprite):
	"""
	Displays the game over animated text.

	"""
	def __init__(self, color, position):
		pygame.sprite.Sprite.__init__(self)
		self.color = pygame.Color(color)
		self.position = position
		self.scale = 1.0
		self.angle = 1.0
		self.operator = operator.mul

		# use default font of a given size
		self.font = pygame.font.Font(None, WIDTH/10)
		self.image = self.font.render("GAME OVER", True, self.color)
		self.original = self.image

		self.rect = self.image.get_rect()
		self.rect.center = position

	def update(self):
		# scale change cycle: increase to 2, then decrease to 1, then increase again
		if self.scale > 2:
			self.operator = operator.div  # division function
		if self.scale < 1:
			self.operator = operator.mul  # multiplication function

		# apply the operator: equivalent to self.scale*1.05 or self.scale/1.05
		self.scale = self.operator(self.scale, 1.05)
		self.angle = self.operator(self.angle, 1.1)

		# modify original sprite image: scale and rotate
		self.image = pygame.transform.rotozoom(self.original, self.angle, self.scale)
		# get new bounding box
		self.rect = self.image.get_rect()
		# set sprite position
		self.rect.center = self.position


def move(player1, ball):
	"""
	CPU player. Tries to track the ball vertical position.

	>>> player = Racket("red", (0,0))
	>>> ball = Ball("red", (0,10), None, None)

	>>> player.rect.centery = 8
	>>> move(player, ball)
	>>> player.rect.centery
	10

	>>> player.rect.centery = 12
	>>> move(player, ball)
	>>> player.rect.centery
	10

	>>> distance = HEIGHT/48
	>>> player.rect.centery = 10 + 2*distance
	>>> move(player, ball)
	>>> player.rect.centery == 10 + distance
	True
	"""
	# calculate vertical distance
	delta = player1.rect.centery - ball.rect.centery
	# limit velocity to the max movement speed, but keep sign
	velocity = math.copysign(min(HEIGHT/48, abs(delta)), delta)
	# move player closer to the ball
	player1.rect.move_ip(0, -velocity)


# define a main function
def main():
	# create a screen surface of the given size
	screen = pygame.display.set_mode((WIDTH,HEIGHT))

	# set window caption
	pygame.display.set_caption("PONG")

	# create two rackets sprites
	player1 = Racket("green", (WIDTH/32, HEIGHT/2))
	player2 = Racket("orange", (WIDTH-WIDTH/32, HEIGHT/2))

	# create the score sprite
	pygame.font.init()
	score = Score("grey", (WIDTH/2,HEIGHT/12))

	# create the ball sprite
	ball = Ball("white", (WIDTH/2,HEIGHT/2), [player1, player2], score)

	# create the game over text sprite
	game_over = GameOver("red", (WIDTH/2,HEIGHT/2))

	# list of sprites to render
	sprites = pygame.sprite.RenderClear([ball, player1, player2, score])

	# create background surface
	background = pygame.Surface([WIDTH, HEIGHT])
	background.fill(pygame.Color("black"))
	for y in range(0, HEIGHT, HEIGHT/24):
		pygame.draw.line(background, pygame.Color("white"), (WIDTH/2,y), (WIDTH/2,y+HEIGHT/80))

	# draw background on screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# clock to control game framerate
	clock = pygame.time.Clock()

	# control variable for the main loop
	running = True

	# no operation, dummy function
	def nop():
		pass

	# game restart function
	def restart():
		# hide game over sprite
		sprites.remove(game_over)
		# reset the game score
		score.reset()
		# reassign space key to serve
		key_map[pygame.K_SPACE][0] = ball.serve

	# mapping between keys and functions
	key_map = {
		pygame.K_UP: [player2.up, player2.down],
		pygame.K_DOWN: [player2.down, player2.up],
		pygame.K_SPACE: [ball.serve, nop]
	}

	# main game loop
	while running:
		clock.tick(FPS)
		pygame.display.set_caption("PONG - {0:.2f} fps".format(clock.get_fps()))

		# move computer player
		move(player1, ball)

		# animate sprites
		sprites.update()
		sprites.draw(screen)

		# display screen
		pygame.display.flip()

		# draw background over sprites
		sprites.clear(screen, background)

		# read events from the event queue
		for event in pygame.event.get():
			# on QUIT event, exit the main loop
			if event.type == pygame.QUIT:
				running = False
			# on key press
			elif event.type == pygame.KEYDOWN and event.key in key_map:
				key_map[event.key][0]()
			# on key release
			elif event.type == pygame.KEYUP and event.key in key_map:
				key_map[event.key][1]()

		# end game
		if max(score.score) == POINTS_TO_WIN:
			if len(sprites) < 5:
				# show game over sprite
				sprites.add(game_over)
				# assign space key to game restart function
				key_map[pygame.K_SPACE][0] = restart


# if this module is executed as a script, run the main function
if __name__ == "__main__":
	main()
