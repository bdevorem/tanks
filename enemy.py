import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet
from explode import Explosion

class Enemy(pygame.sprite.Sprite):
	def __init__(self, center, gs=None)
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("imgs/tank3.png")
		self.orig_image = pygame.image.load("imgs/tank3.png")
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.orig_image = pygame.transform.scale(self.orig_image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.center = center

	def tick(self):
		
