#Elliott Runburg
#PyGame Primer
#4-12-16
#GameSpace/main file

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
		self.black = (0,0,0)

		#2) Set up game objects
		self.clock = pygame.time.Clock()
		self.deathstar = DeathStar(self)
		self.planet = Planet(self)
		self.lasers = []
		self.explosion = Explosion(self)

		#3) Start game loop
		while 1:
			#4) Clock tick regulation
			self.clock.tick(60)

			#5) Handle user inputs
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					self.deathstar.move(event.key)
				elif event.type == MOUSEBUTTONDOWN:
					self.deathstar.tofire = True
					self.deathstar.fire_x, self.deathstar.fire_y = pygame.mouse.get_pos()
				elif event.type == MOUSEBUTTONUP:
					self.deathstar.tofire = False

			#6) Send ticks to objects
			self.deathstar.tick()
			if self.planet.hp <= 0:
				self.explosion.tick()
			self.planet.tick()
			for laser in self.lasers:
				laser.tick()


			#7) Display game objects
			self.screen.fill(self.black)
			for laser in self.lasers:
				self.screen.blit(laser.image, laser.rect)
			self.screen.blit(self.deathstar.image, self.deathstar.rect)
			if self.planet.hp <= 0:
				self.screen.blit(self.explosion.image, self.explosion.rect)
			self.screen.blit(self.planet.image, self.planet.rect)
			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.start()		
