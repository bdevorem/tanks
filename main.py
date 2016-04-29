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

class GameSpace(object):
	def start(self):
		#1) Basic initialization
		pygame.init()

		self.size = width,height = (640,480)
		self.screen = pygame.display.set_mode(self.size)
		self.background = pygame.image.load("wood.png")
		self.back_rect = self.background.get_rect()

		#2) Set up game objects
		self.clock = pygame.time.Clock()

		#3) Start game loop
		while 1:
			#4) Clock tick regulation
			self.clock.tick(60)

			#5) Handle user inputs
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
			self.screen.blit(self.background, self.back_rect)

			#6) Send ticks to objects

			#7) Display game objects
			pygame.display.flip()


if __name__ == '__main__':
	gs = GameSpace()
	gs.start()		
