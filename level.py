import sys
import os
import pygame
import math
from pygame.locals import *
from block import Block

class Level():
	def __init__(self, gs=None):
		self.gs = gs

	def createObjects(self):
		objects = {}
		#objects['Player 1'] = PlayerTank()
		#objects['Player 2'] = PlayerTank()

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

		return objects