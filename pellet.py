import sys
import os
import pygame
import math
from pygame.locals import *
from explode import Explosion
from copy import deepcopy

# Pellet class (the shot that is fired)
class Pellet(pygame.sprite.Sprite):
	def __init__(self, source, angle, center, gs=None):
		# Normal init
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.source = source
		self.angle = angle
		self.image = pygame.image.load("imgs/pellet.png")
		self.image = pygame.transform.scale(self.image, (10,10))
		self.rect = self.image.get_rect()
		self.rect.center = center
		# How many times it has bounced on a wall
		self.bounce = 0
		# Save the direction it should be moving
		self.dx = math.cos(self.angle)*3
		self.dy = math.sin(self.angle)*-3
		# If it has exploded or not
		self.exploded = False

		# Center of the rect
		self.x = self.rect.centerx
		self.y = self.rect.centery

	def tick(self):
		# As long as it's alive, check for wall collision, move, then check
		# tank collision
		if not self.exploded:
			self.checkBounce()
			self.move()
			self.checkCollision()

	def move(self):
		# Change your position based on your dx, dy values
		self.x += self.dx
		self.y += self.dy
		self.rect.center = (self.x, self.y)

	def checkBounce(self):
		# Save the original info
		orig_center = self.rect.center
		# "feeler" rectangle
		self.temp_rect = self.rect.copy()
		# Testing bools
		horiz_coll = False
		vert_coll = False
		# Move in the x direction
		self.temp_rect = self.temp_rect.move((int)(self.dx), 0)
		for block in self.gs.blocks:
			# If it hits a block in the x direction, mark horiz_coll true
			if pygame.Rect.colliderect(self.temp_rect, block.rect) and self.bounce == 0:
				horiz_coll = True
			# If it has already boucned, explode
			elif pygame.Rect.colliderect(self.temp_rect, block.rect):
				self.explode(True)
		# Again, another feeler
		self.temp_rect = self.rect.copy()
		# Test this in the y direction
		self.temp_rect = self.rect.move(0, (int)(self.dy))
		for block in self.gs.blocks:
			# If it collides with block, mark vert_coll
			if pygame.Rect.colliderect(self.temp_rect, block.rect) and self.bounce == 0:
				vert_coll = True
			# If it collides and has already bounced, explode
			elif pygame.Rect.colliderect(self.temp_rect, block.rect):
				self.explode(True)
		# Change direction if collision
		if horiz_coll:
			self.dx = -1 * self.dx
		if vert_coll:
			self.dy = -1 * self.dy
		# If it collided, mark bounce and move
		if (horiz_coll or vert_coll) and not self.exploded:
			self.bounce += 1
			self.move()
			
	# Check for collision with tank
	def checkCollision(self):
		# Player one
		if pygame.Rect.colliderect(self.rect, self.gs.tank1.rect):		
			self.explode(False)
			self.gs.tank1.explode()
		# Teammate
		if pygame.Rect.colliderect(self.rect, self.gs.teammate.rect):
			self.explode()
			self.gs.teammate.explode()
		# enemies
		for enemy in self.gs.enemies:
			if pygame.Rect.colliderect(self.rect, enemy.rect):
				self.explode(False)
				enemy.explode()
		# other pellets
		for pellet in self.gs.pellets:
			if pygame.Rect.colliderect(self.rect, pellet.rect) and pellet.rect != self.rect:
				self.explode(True)
				pellet.explode(False)

	# Explosion function
	def explode(self, graphics):
		if not self.exploded:
			# Remove yourself from the list so no more ticks
			self.gs.pellets.remove(self)
			self.exploded = True
			if graphics:
				# If this one should create a graphic, then show the explosion
				# Sometimes false so you don't have two explosions for one
				# collision
				expl_center = deepcopy(self.rect.center)
				self.gs.explosions.append(Explosion(expl_center, self.gs))
