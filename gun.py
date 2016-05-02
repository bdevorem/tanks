#!/usr/bin/env python2
import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet

class Gun(pygame.sprite.Sprite):
	def __init__(self, center=None, gs=None):
		self.gs = gs
		self.image = pygame.image.load("imgs/gun.png")
		self.orig_image = pygame.image.load("imgs/gun.png")
		self.rect = self.image.get_rect()
		self.rect.center = center

	def move(self, center):
		#print "made it"
		self.rect = self.rect.move(center)

	def rotate(self, dx, dy):
		self.image = pygame.transform.rotate(self.orig_image, 
							math.atan2(dy,dx)/math.pi*180)
		self.rect = self.image.get_rect(center=self.rect.center)
