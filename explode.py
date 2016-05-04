import sys
import os
import pygame
import math
from pygame.locals import *
from copy import deepcopy

# These are global so that they don't have to be reloaded each explosion
# It caused a bit of lag while doing it for every explosion
expl_imgs = [pygame.image.load("imgs/explosion/frames016a.png"),
						pygame.image.load("imgs/explosion/frames000a.png"),
						pygame.image.load("imgs/explosion/frames001a.png"),
						pygame.image.load("imgs/explosion/frames002a.png"),
						pygame.image.load("imgs/explosion/frames003a.png"),
						pygame.image.load("imgs/explosion/frames004a.png"),
						pygame.image.load("imgs/explosion/frames005a.png"),
						pygame.image.load("imgs/explosion/frames006a.png"),
						pygame.image.load("imgs/explosion/frames007a.png"),
						pygame.image.load("imgs/explosion/frames008a.png"),
						pygame.image.load("imgs/explosion/frames009a.png"),
						pygame.image.load("imgs/explosion/frames010a.png"),
						pygame.image.load("imgs/explosion/frames011a.png"),
						pygame.image.load("imgs/explosion/frames012a.png"),
						pygame.image.load("imgs/explosion/frames013a.png"),
						pygame.image.load("imgs/explosion/frames014a.png"),
						pygame.image.load("imgs/explosion/frames015a.png"),
						pygame.image.load("imgs/wood.png")]

# Class for explosions
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, gs=None):
		# Normal init
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs

		# Mark the current image, and the center of the explosion (passed from pellet
		self.curr_im = 0
		self.center = deepcopy(center)
		# Image is pointing to the current image
		self.image = expl_imgs[self.curr_im]
		# Rect is from the image
		self.rect = self.image.get_rect()
		# match the center
		self.rect.center = self.center
		# tick counter
		self.death_tick = 0

	def tick(self):
		self.death_tick += 1
		if self.death_tick % 5 == 0 and self.curr_im < 16:
			# Increase the tick count, change the image
			self.curr_im += 1
			self.image = expl_imgs[self.curr_im]
			self.rect = self.image.get_rect()
			self.rect.center = self.center
			
			# End the game if you're the tank
			if self.curr_im == 10:
				if not self.gs.tank1_life:
					self.gs.endgame = True

		# at the end, get rid of yourself
		elif self.death_tick % 8 == 0 and self.curr_im >= 16:
			self.gs.explosions.remove(self)
		
