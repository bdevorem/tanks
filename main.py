#!/usr/bin/env python2

# Elliott Runburg
# Breanna Devore-McDonald
# Tanks game
# 4-23-16
# Programming Paradigms final project
# GameSpace/main file

import sys
import os
import pygame
from pygame.locals import *
from objects import *
from level import Level
from block import Block
from tank_obj import tank
from pellet import Pellet
from explode import Explosion

class GameSpace(object):
	def start(self):
		#1) Basic initialization
		pygame.init()

		self.size = width,height = (640,480)
		self.screen = pygame.display.set_mode(self.size)
		self.background = pygame.image.load("imgs/wood.png")
		self.back_rect = self.background.get_rect()

		#2) Set up game objects
		self.clock = pygame.time.Clock()
		self.level = Level(self)
		self.objects = self.level.createObjects()
		#self.player = self.objects['Player 1']
		#self.teammate = self.objects['Player 2']
		#self.enemies = self.objects['Enemies']
		self.blocks = self.objects['Blocks']
		self.tank1 = tank(self)
		self.pellets = []
		self.explosions = []
		self.tank1_life = True

		#3) Start game loop
		hold = False
		while 1:
			#4) Clock tick regulation
			self.clock.tick(60)

			#5) Handle user inputs
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				#elif event.type == KEYUP:
				#	hold = False
				#	print 'keyup'
				#elif hold is True:
				#	print 'yes'
				#	self.tank1.move(key)
				elif event.type == KEYDOWN:
				#	hold = True
				#	key = event.key
					self.tank1.move(event.key)
				elif event.type == MOUSEBUTTONDOWN:
					self.tank1.tofire = True
					self.tank1.fire_x, self.tank1.fire_y = pygame.mouse.get_pos()
				elif event.type == MOUSEBUTTONUP:
					self.tank1.tofire = False

			#6) Send ticks to objects
			self.tank1.tick()
			for pellet in self.pellets:
				pellet.tick()
			for expl in self.explosions:
				expl.tick()
	
			#7) Display game objects
			if self.tank1_life:
				self.screen.blit(self.background, self.back_rect)
				for block in self.blocks:
					self.screen.blit(block.image, block.rect)
				for pellet in self.pellets:
					self.screen.blit(pellet.image, pellet.rect)
				for expl in self.explosions:
					self.screen.blit(expl.image, expl.rect)
				self.screen.blit(self.tank1.image, self.tank1.rect)
				self.screen.blit(self.tank1.gun.image,self.tank1.gun.rect)
			else:
				self.background = pygame.image.load("imgs/gameover.png")
				self.back_rect = self.background.get_rect()
				self.screen.blit(self.background, self.back_rect)

			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.start()		
