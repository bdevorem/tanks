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
		self.gs = gs
		self.x = 10

	def createObjects(self):
		objects = {}
		objects['Player 1'] = tank((55, 400), self.gs)
		objects['Player 2'] = tank((400, 55), self.gs)

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

		enemies = []
		for n in range(random.randint(1, 1)):
			self.x += 50
			x = self.x
			y = random.randint(50, 300)
			enemies.append(Enemy(self.gs, (x, y)))

		objects['Enemies'] = enemies

		return objects
