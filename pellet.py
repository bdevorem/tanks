import sys
import os
import pygame
import math
from pygame.locals import *
from explode import Explosion

class Pellet(pygame.sprite.Sprite):
	def __init__(self, source, angle, center, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.source = source
		self.angle = angle
		self.image = pygame.image.load("imgs/pellet.png")
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.bounce = 0
		self.dx = math.cos(self.angle)*5
		self.dy = math.sin(self.angle)*-5

	def tick(self):
		self.checkBounce()
		self.move()
		self.checkCollision()

	def move(self):
		self.rect = self.rect.move(self.dx, self.dy)

	def checkBounce(self):
		self.temp_rect = self.rect.move(self.dx, 0)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect) and self.bounce == 0:
				self.dx = -1*self.dx
				self.bounce += 1
			else:
				pass
				#self.explode()
		self.temp_rect = self.rect.move(0, self.dy)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect) and self.bounce == 0:
				self.dy = -1*self.dy
				self.bounce += 1
			else:
				pass
#				self.explode()

	def checkCollision(self):
#		if pygame.Rect.colliderect(self.rect, self.gs.player.rect):
#			self.explode()
#			self.gs.player.explode()
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
				#print 'pellet collision'

	def explode(self):
		self.gs.pellets.remove(self)
		self.gs.explosions.append(Explosion(self.rect.center, self.gs))


