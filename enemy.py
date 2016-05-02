import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet
from explode import Explosion
import random
from gun import Gun
from copy import deepcopy

class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs=None, center=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		self.angle = random.uniform(1, 360)
		
		self.center = center

		self.image = pygame.image.load("imgs/tank3.png")
		self.orig_image = pygame.image.load("imgs/tank3.png")
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.orig_image = pygame.transform.scale(self.orig_image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.center = self.center
		self.dx = math.cos(self.angle)*2
		self.dy = math.sin(self.angle)*-2
		self.exploded = False
		self.tofire = False
		self.gun = Gun(self.rect.center, self.gs)
		self.fire_interval = random.randint(100, 500)
		self.fire_timer = 0

	def tick(self):
		if not self.exploded:
			self.checkBounce()
			self.move(self.gs.tank1)

			self.fire_timer += 1
			if self.fire_timer == self.fire_interval:
				self.fire_timer = 0
				fire_x, fire_y = self.gs.tank1.rect.center
				angle = math.atan2(self.rect.centery-fire_y, 
									fire_x-self.rect.centerx)
				pellet_center = (self.rect.centerx+math.cos(angle)*36,
							self.rect.centery-math.sin(angle)*36)
				pellet = Pellet(self, angle, pellet_center, self.gs)
#				self.gs.pellets.append(pellet)


	def move(self, tank1):
		mx, my = tank1.rect.center
		dx = mx - self.rect.centerx
		dy = self.rect.centery - my

		self.rect = self.rect.move(self.dx, self.dy)
		self.gun.move((self.dx, self.dy))

		if dx != 0:
			self.gun.rotate(dx, dy)

	def checkBounce(self):
		orig_center = self.rect.center
		self.temp_rect = self.rect.copy()
		horiz_coll = False
		vert_coll = False

		self.temp_rect = self.temp_rect.move(self.dx, 0)		
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				horiz_coll = True
		for enemy in self.gs.enemies:
			if enemy is not self:
				if pygame.Rect.colliderect(self.temp_rect, enemy.rect):
					horiz_coll = True
	
		self.temp_rect = self.rect.copy()
		self.temp_rect = self.rect.move(0, self.dy)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				vert_coll = True
		for enemy in self.gs.enemies:
			if enemy is not self:
				if pygame.Rect.colliderect(self.temp_rect, enemy.rect):
					vert_coll = True

		if horiz_coll:
			self.dx = -1 * self.dx
		if vert_coll:
			self.dy = -1 * self.dy
		if (horiz_coll or vert_coll):
			self.move(self.gs.tank1)
			self.move(self.gs.tank1)

	def explode(self):
		if not self.exploded:
			self.gs.enemies.remove(self)
			self.exploded = True
			expl_center = deepcopy(self.rect.center)
			self.gs.explosions.append(Explosion(expl_center, self.gs))



