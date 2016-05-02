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
from enemy import Enemy

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
		self.tank1 = self.objects['Player 1']
		self.teammate = self.objects['Player 2']
		self.enemies = self.objects['Enemies']
		self.blocks = self.objects['Blocks']
		self.pellets = []
		self.explosions = []
		self.tank1_life = True
		self.endgame = False

		#3) Start game loop
		hold = False
		while 1:
			#4) Clock tick regulation
			self.clock.tick(60)

			#5) Handle user inputs
			events = pygame.event.get()
			self.handleEvents(self.tank1, events, pygame.mouse.get_pos())

			#6) Send ticks to objects
			self.tank1.tick()
			for pellet in self.pellets:
				pellet.tick()
			for expl in self.explosions:
				expl.tick()
			for enemy in self.enemies:
				enemy.tick()

			#7) Display game objects
			if len(self.enemies) >= 1:
				if not self.endgame:
					self.screen.blit(self.background, self.back_rect)
					if self.tank1_life:
						self.screen.blit(self.tank1.image, self.tank1.rect)
						self.screen.blit(self.tank1.gun.image,self.tank1.gun.rect)
						self.screen.blit(self.teammate.image, self.teammate.rect)
						self.screen.blit(self.teammate.gun.image,self.teammate.gun.rect)	
					for enemy in self.enemies:
						self.screen.blit(enemy.image, enemy.rect)
						self.screen.blit(enemy.gun.image, enemy.gun.rect)
					for block in self.blocks:
						self.screen.blit(block.image, block.rect)
					for pellet in self.pellets:
						self.screen.blit(pellet.image, pellet.rect)
					for expl in self.explosions:
						self.screen.blit(expl.image, expl.rect)
				else:
					self.background = pygame.image.load("imgs/gameover.png")
					self.back_rect = self.background.get_rect()
					self.screen.blit(self.background, self.back_rect)
			else: #user wins
				self.background = pygame.image.load("imgs/youwin.png")
				self.back_rect = self.background.get_rect()
				self.screen.blit(self.background, self.back_rect)

			pygame.display.flip()

	def handleEvents(self, tank, events, mouse):
		for event in events:
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYUP:
				tank.hold = False
				tank.key = 0
			#	print 'keyup'
			#elif hold is True:
			#	print 'yes'
			#	self.tank1.move(key)
			elif event.type == KEYDOWN:
				if event.key == 32:
					tank.tofire = True
					tank.fire_x, tank.fire_y = mouse
				else:
					tank.hold = True
					tank.key = event.key
			#	key = event.key
			#	self.tank1.move(event.key)
			elif event.type == MOUSEBUTTONDOWN:
				tank.tofire = True
				tank.fire_x, tank.fire_y = mouse
			elif event.type == MOUSEBUTTONUP:
				tank.tofire = False


if __name__ == '__main__':
	gs = GameSpace()
	gs.start()		
