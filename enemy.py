import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet
from explode import Explosion
import random

class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.angle = random.uniform(1, 360)
		self.center = (random.randint(1, 300), random.randint(1, 300))

		self.image = pygame.image.load("imgs/tank3.png")
		self.orig_image = pygame.image.load("imgs/tank3.png")
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.orig_image = pygame.transform.scale(self.orig_image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.center = self.center
		self.dx = math.cos(self.angle)*5
		self.dy = math.sin(self.angle)*-5
		self.exploded = False

	def tick(self):
		if not self.exploded:
			self.checkBounce()
			self.move()

	def move(self):
		self.rect = self.rect.move(self.dx, self.dy)

	def checkBounce(self):
		orig_center = self.rect.center
		self.temp_rect = self.rect.copy()
		horiz_coll = False
		vert_coll = False

		self.temp_rect = self.temp_rect.move(self.dx, 0)		
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				horiz_coll = True
		
		self.temp_rect = self.rect.copy()
		self.temp_rect = self.rect.move(0, self.dy)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				vert_coll = True

		if horiz_coll:
			self.dx = -1 * self.dx
		if vert_coll:
			self.dy = -1 * self.dy
		if (horiz_coll or vert_coll):
			self.move()

	def explode(self):
		if not self.exploded:
			self.gs.enemies.remove(self)
			self.exploded = True
			expl_center = deepcopy(self.rect.center)
			self.gs.explosions.append(Explosion(expl_center, self.gs))



