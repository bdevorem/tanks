import pygame
import sys
import os
from pygame.locals import *

class Block(pygame.sprite.Sprite):
	def __init__(self, x, y, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("imgs/brick.png")
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
	
	def tick(self):
		pass
