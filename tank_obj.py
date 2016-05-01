#!/usr/bin/env python2
import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet
from explode import Explosion

class tank(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("imgs/tank1.png")
		self.orig_image = pygame.image.load("imgs/tank1.png")
		# tank is a tad smaller than gun bc collision detecting
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.orig_image = pygame.transform.scale(self.orig_image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.center = (55,425)
		self.fire_x = 0
		self.fire_y = 0
		self.fire_timer = 0
		self.tofire = False
		
		self.gun = gun(self.rect.center, self.gs)
	
	def tick(self):
		mx, my = pygame.mouse.get_pos()
		dx = mx - self.rect.centerx
		dy = self.rect.centery - my
		if self.fire_timer != 0:
			self.fire_timer -= 1
		if self.tofire == True and self.fire_timer == 0:
			self.fire_timer = 25
			# can still come from center of tank since the 
			# gun will be pointing in the same direction
			# ^^ jk because of collision detection

			fire_x, fire_y = pygame.mouse.get_pos()
			angle = math.atan2(self.rect.centery-fire_y, fire_x-self.rect.centerx)
			pellet_center = (self.rect.centerx+math.cos(angle)*36,self.rect.centery-math.sin(angle)*36)
			pellet = Pellet(self, angle, pellet_center, self.gs)
			self.gs.pellets.append(pellet)

			#########################################################
			# SOUND
			#if pygame.mixer.music.get_busy() == False:
			#	pygame.mixer.music.load("screammachine.wav")
			#	pygame.mixer.music.set_volume(1)
			#	pygame.mixer.music.play()
		else:
			#pygame.mixer.stop()
			if dx != 0:
				self.gun.rotate(dx, dy)

	def move(self, keycode):
		"""
		Called when keydown is detected in main
		"""
		#self.gun.move(keycode)

		if keycode == 273:
			# trial
			if self.checkBlocks((0, -3)) is False:
				self.rect = self.rect.move(0, -3)
				self.gun.move((0,-3))
		elif keycode == 274:
			if self.checkBlocks((0, 3)) is False:
				self.rect = self.rect.move(0, 3)
				self.gun.move((0, 3))
		elif keycode == 275:
			if self.checkBlocks((3, 0)) is False:
				self.rect = self.rect.move(3, 0)
				self.gun.move((3, 0))
		elif keycode == 276:
			if self.checkBlocks((-3, 0)) is False:
				self.rect = self.rect.move(-3, 0)
				self.gun.move((-3, 0))

	def checkBlocks(self, movement):
		"""
		Return True if there is any overlap
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
		if self.gs.tank1_life:
			self.gs.tank1_life = False
			center = deepcopy(self.rect.center)
			self.gs.explosions.append(Explosion(center, self.gs))

class gun(pygame.sprite.Sprite):
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



################################################################
