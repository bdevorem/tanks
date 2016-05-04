#!/usr/bin/env python2
# Breanna Devore-McDonald
# Elliott Runburg
# enemy.py
# class for the random enemies
import sys
import os
import pygame
import math
from pygame.locals import *
from pellet import Pellet
from explode import Explosion
import random
from gun import Gun
from copy import deepcopy

class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs=None, center=None, angle=None, target=None, interval = None):
		"""
		Enemy class: sort of a hybrid between the user
		tank and the pellets. It is a tank, and the gun
		follows the user at all time. But it changes directions
		when it hits another enemy or a wall
		"""
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs

		self.angle = angle
		self.target = target		
		self.center = center

		self.image = pygame.image.load("imgs/tank3.png")
		self.orig_image = pygame.image.load("imgs/tank3.png")
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.orig_image = pygame.transform.scale(self.orig_image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.center = self.center
		self.dx = math.cos(self.angle)*2
		self.dy = math.sin(self.angle)*-2
		self.exploded = False
		self.tofire = False
		self.gun = Gun(self.rect.center, self.gs)

		#random interval at which to fire at user
		self.fire_interval = interval
		self.fire_timer = 0

	def tick(self):
		if not self.exploded:
			if not self.target.life:
				if self.target == self.gs.tank1:
					self.target = self.gs.teammate
				else:
					self.target = self.gs.tank1
			# first check if direction needs to be changed
			self.checkBounce()
			# then move. will always move, unlike user
			self.move(self.target)

			self.fire_timer += 1
			if self.fire_timer == self.fire_interval:
				#create pellets when the interval reaches
				# the time specified at creation
				self.fire_timer = 0
				fire_x, fire_y = self.target.rect.center
				angle = math.atan2(self.rect.centery-fire_y, 
									fire_x-self.rect.centerx)
				pellet_center = (self.rect.centerx+math.cos(angle)*36,
							self.rect.centery-math.sin(angle)*36)
				pellet = Pellet(self, angle, pellet_center, self.gs)
				self.gs.pellets.append(pellet)


	def move(self, tank1):
		"""
		Move tank at every tick in the same direction, until	
		another object is hit or we die
		"""
		mx, my = tank1.rect.center
		dx = mx - self.rect.centerx
		dy = self.rect.centery - my

		self.rect = self.rect.move(self.dx, self.dy)
		self.gun.move((self.dx, self.dy))

		if dx != 0:
			self.gun.rotate(dx, dy)

	def checkBounce(self):
		"""
		A check for if the motion needs to be changed due
		to a collision (a bounce)
		"""
		orig_center = self.rect.center
		self.temp_rect = self.rect.copy()
		horiz_coll = False
		vert_coll = False

		# loop through blocks and compare rectangles
		self.temp_rect = self.temp_rect.move(self.dx, 0)		
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				horiz_coll = True
		# same for other enemies besides self
		for enemy in self.gs.enemies:
			if enemy is not self:
				if pygame.Rect.colliderect(self.temp_rect, enemy.rect):
					horiz_coll = True
	
		# repeat for vertical collisions
		self.temp_rect = self.rect.copy()
		self.temp_rect = self.rect.move(0, self.dy)
		for block in self.gs.blocks:
			if pygame.Rect.colliderect(self.temp_rect, block.rect):
				vert_coll = True
		for enemy in self.gs.enemies:
			if enemy is not self:
				if pygame.Rect.colliderect(self.temp_rect, enemy.rect):
					vert_coll = True

		# change direction if there is 
		if horiz_coll:
			self.dx = -1 * self.dx
		if vert_coll:
			self.dy = -1 * self.dy
		if (horiz_coll or vert_coll):
			self.move(self.gs.tank1)
			self.move(self.gs.tank1)

	def explode(self):
		"""
		Function to create explosion object when enemy dies
		"""
		if not self.exploded:
			self.gs.enemies.remove(self)
			self.exploded = True
			expl_center = deepcopy(self.rect.center)
			self.gs.explosions.append(Explosion(expl_center, self.gs))



