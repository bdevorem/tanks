import sys
import os
import pygame
import math
from pygame.locals import *

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.expl_imgs = [pygame.image.load("imgs/explosion/frames016a.png"),
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
						pygame.image.load("imgs/explosion/frames015a.png")]
		self.curr_im = 0
		self.center = center
		self.image = self.expl_imgs[self.curr_im]
		self.rect = self.image.get_rect()
		self.rect.center = self.center
		self.death_tick = 0

	def tick(self):
		self.death_tick += 1
		if self.death_tick % 8 == 0 and self.curr_im < 15:
			self.curr_im += 1
			self.image = self.expl_imgs[self.curr_im]
			self.rect = self.image.get_rect()
			self.rect.center = self.cenbter