import sys
import os
import pygame
import math
from pygame.locals import *
from explode import Explosion
from copy import deepcopy

class Pellet(pygame.sprite.Sprite):
	def __init__(self, source, angle, center, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.source = source
		self.angle = angle
		self.image = pygame.image.load("imgs/pellet.png")
		self.image = pygame.transform.scale(self.image, (10,10))
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.bounce = 0
		self.dx = math.cos(self.angle)*5
		self.dy = math.sin(self.angle)*-5
		self.exploded = False

	def tick(self):
		if not self.exploded:
			self.checkBounce()
			self.move()
			self.checkCollision()

	def move(self):
		self.rect = self.rect.move(self.dx, self.dy)

	def checkBounce(self):
		orig_center = self.rect.center
		self.temp_rect = self.rect.copy()
		horiz_coll = False
		vert_coll = False
		self.temp_rect = self.temp_rect.move(self.dx, 0)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect) and self.bounce == 0:
				horiz_coll = True
			elif pygame.Rect.colliderect(self.temp_rect, block.rect):
				self.explode()
		self.temp_rect = self.rect.copy()
		self.temp_rect = self.rect.move(0, self.dy)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect) and self.bounce == 0:
				vert_coll = True
			elif pygame.Rect.colliderect(self.temp_rect, block.rect):
				self.explode()
		if horiz_coll:
			self.dx = -1 * self.dx
		if vert_coll:
			self.dy = -1 * self.dy
		if (horiz_coll or vert_coll) and not self.exploded:
			self.bounce += 1
			self.move()
			

	def checkCollision(self):
		if pygame.Rect.colliderect(self.rect, self.gs.tank1.rect):		
			self.explode()
			self.gs.tank1.explode()
#		if pygame.Rect.colliderect(self.rect, self.gs.teammate.rect):
#			self.explode()
#			self.gs.teammate.explode()
#		for enemy in self.gs.enemies:
#			if pygame.Rect.colliderect(self.rect, enemy.rect):
#				self.explode()
#				enemy.explode()
		for pellet in self.gs.pellets:
			if pygame.Rect.colliderect(self.rect, pellet.rect) and pellet.rect != self.rect:
				self.explode()
				pellet.explode()

	def explode(self):
		if not self.exploded:
			self.gs.pellets.remove(self)
			self.exploded = True
			expl_center = deepcopy(self.rect.center)
			self.gs.explosions.append(Explosion(expl_center, self.gs))

