import pygame
import sys
import os
from pygame.locals import *

class Block(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("brick.png")
		self.rect = self.image.get_rect()

	def tick(self):
		pass
