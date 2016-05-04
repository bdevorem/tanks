#!/usr/bin/env python2
# Breanna Devore-McDonald
# Elliott Runburg
# tank_obj.py
# class for user player

import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet
from explode import Explosion
from copy import deepcopy
from gun import Gun

class tank(pygame.sprite.Sprite):
	def __init__(self, center, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("imgs/tank1.png")
		self.orig_image = pygame.image.load("imgs/tank1.png")
		# tank is a tad smaller than gun bc collision detecting
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.orig_image = pygame.transform.scale(self.orig_image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.fire_x = 0
		self.fire_y = 0
		self.fire_timer = 0
		self.tofire = False
		self.mx = 0
		self.my = 0
		self.life = True

		#attach gun, has to be a different part in order
		# to move around seemlessly (as opposed to a weird
		# rotating square)
		self.gun = Gun(self.rect.center, self.gs)
		self.hold = False
		self.key = 0

	def tick(self):
		#allow for coasting w a variable set in gamespace
		if self.hold and self.key is not 0:
			self.move(self.key)

		# get movement
		dx = self.mx - self.rect.centerx
		dy = self.rect.centery - self.my
		if self.fire_timer != 0:
			self.fire_timer -= 1
		if self.tofire == True and self.fire_timer == 0:
			self.fire_timer = 60
			# can still come from center of tank since the 
			# gun will be pointing in the same direction
			# ^^ jk because of collision detection

			fire_x = self.mx
			fire_y = self.my
			# move bullets to start outside of rect, so they 
			# don't get stuck bc of collision detection
			angle = math.atan2(self.rect.centery-fire_y, fire_x-self.rect.centerx)
			pellet_center = (self.rect.centerx+math.cos(angle)*36,self.rect.centery-math.sin(angle)*36)
			pellet = Pellet(self, angle, pellet_center, self.gs)
			self.gs.pellets.append(pellet)
		else:
			# if we are moving, rotate gun
			# this class is completely referenced through
			# the tank class since it is not a real sprite,
			# jsut a sub sprite
			if dx != 0:
				self.gun.rotate(dx, dy)

	def move(self, keycode):
		"""
		Called when keydown is detected in main
		Moves objects according to key
		"""
		#self.gun.move(keycode)

		if keycode == 273 or keycode == 119:
			# trial
			if self.checkBlocks((0, -3)) is False:
				self.rect = self.rect.move(0, -3)
				self.gun.move((0,-3))
		elif keycode == 274 or keycode == 115:
			if self.checkBlocks((0, 3)) is False:
				self.rect = self.rect.move(0, 3)
				self.gun.move((0, 3))
		elif keycode == 275 or keycode == 100:
			if self.checkBlocks((3, 0)) is False:
				self.rect = self.rect.move(3, 0)
				self.gun.move((3, 0))
		elif keycode == 276 or keycode == 97:
			if self.checkBlocks((-3, 0)) is False:
				self.rect = self.rect.move(-3, 0)
				self.gun.move((-3, 0))

	def checkBlocks(self, movement):
		"""
		Return True if there is any overlap
		in tank and blocks, no explosion
		"""
		collide = False
		self.temp_rect = self.rect.move(movement[0], 0)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				collide = True
		
		self.temp_rect = self.rect.move(0, movement[1])
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				collide = True
		
		return collide

	def explode(self):
		"""
		Create a new explosion at the center of the collision
		Explosion is another sprite, gets sent to gs
		"""
		if self.gs.tank1_life:
			self.life = False
			center = deepcopy(self.rect.center)
			self.gs.explosions.append(Explosion(center, self.gs))



