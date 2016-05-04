import pygame
import sys
import os
from pygame.locals import *

# Block class
class Block(pygame.sprite.Sprite):
	# Position and gamespace are defined
	def __init__(self, x, y, gs=None):
		pygame.sprite.Sprite.__init__(self)

		# Save gamespace, load image
		self.gs = gs
		self.image = pygame.image.load("imgs/brick.png")
		# Put our space as the provided rect
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
	
	def tick(self):
		# Nothing to due on tick!
		pass
