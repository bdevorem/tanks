#!/usr/bin/env python2
# Breanna Devore-McDonald
# Elliott Runburg
# level.py

import sys
import os
import pygame
import math
from pygame.locals import *
from block import Block
import random
from enemy import Enemy
from tank_obj import tank

class Level():
	def __init__(self, gs=None):
		"""
		This class sets up the main gamspace objects
		which is essentially the entire level
		"""
		self.gs = gs
		self.x = 10
		self.y = 30

	def createObjects(self):
		
		# create the two teammates and store in dictionary
		# this method is used for easy access of gamspace
		# objects in main
		objects = {}
		objects['Player 1'] = tank((55, 400), self.gs)
		objects['Player 2'] = tank((400, 55), self.gs)

		# create the border of blocks
		blocks = []
		for y in range(0,(int)((self.gs.size[1])/32)):
			block1 = Block(0, y*32, self.gs)
			block2 = Block(self.gs.size[0]-32, y*32, self.gs)
			blocks.append(block1)
			blocks.append(block2)
		for x in range(1,(int)(self.gs.size[0]/32-1)):
			block1 = Block(x*32, 0, self.gs)
			block2 = Block(x*32, self.gs.size[1]-32, self.gs)
			blocks.append(block1)
			blocks.append(block2)

		objects['Blocks'] = blocks
		
		####################################################

		# create the random set of enemies for the game
		# can be anywhere from 1 to 5
		# they all have fixed x locations to ensure no overlap,
		# but y location is random
		enemies = []
		angle = 25
		target = self.gs.tank1
		for n in range(1, 5):
			if target is self.gs.tank1:
				target = self.gs.teammate
			else:
				target = self.gs.tank1
			self.x += 50
			self.y += 50
			angle = angle + 37
			x = self.x
			y = self.y
			enemies.append(Enemy(self.gs, (x, y), angle, target))

		objects['Enemies'] = enemies

		return objects
