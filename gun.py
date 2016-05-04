#!/usr/bin/env python2
# Breanna McDonald
# Elliott Runburg
# gun.py

import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet

class Gun(pygame.sprite.Sprite):
	def __init__(self, center=None, gs=None):
		"""
		Not too complicated, load gun images and set
		rect to that of the tank. The gun image has
		a transparent backgound and will share a center
		with the tank to allow for easy rotations
		"""
		self.gs = gs
		self.image = pygame.image.load("imgs/gun.png")
		self.orig_image = pygame.image.load("imgs/gun.png")
		self.rect = self.image.get_rect()
		self.rect.center = center

	def move(self, center):
		"""
		Moves depending on the key that gets collected
		in the tank class
		"""
		#print "made it"
		self.rect = self.rect.move(center)

	def rotate(self, dx, dy):
		"""
		Rotate depending on the key collected in tank
		"""
		self.image = pygame.transform.rotate(self.orig_image, 
							math.atan2(dy,dx)/math.pi*180)
		self.rect = self.image.get_rect(center=self.rect.center)


