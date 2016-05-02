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

from twisted.internet.protocol import ClientFactory
from twisted.itnernet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

from level import Level
from block import Block
from tank_obj import tank
from pellet import Pellet
from explode import Explosion
from enemy import Enemy

CLIENT_PORT = 40035
CLIENT_HOST = 'localhost'

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
		self.hold = False
		
		def tick(self):
		#4) Clock tick regulation
		self.clock.tick(60)

		#5) Handle user inputs
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == KEYUP:
				self.tank1.hold = False
				self.tank1.key = 0
			#	print 'keyup'
			#elif hold is True:
			#	print 'yes'
			#	self.tank1.move(key)
			elif event.type == KEYDOWN:
				if event.key == 32:
					self.tank1.tofire = True
					self.tank1.fire_x, self.tank1.fire_y = pygame.mouse.get_pos()
				else:
					self.tank1.hold = True
					self.tank1.key = event.key
			#	key = event.key
			#	self.tank1.move(event.key)
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
		for enemy in self.enemies:
			enemy.tick()

		#7) Display game objects
		if len(self.enemies) >= 1:
			if not self.endgame:
				self.screen.blit(self.background, self.back_rect)
				if self.tank1_life:
					self.screen.blit(self.tank1.image, self.tank1.rect)
					self.screen.blit(self.tank1.gun.image,self.tank1.gun.rect)
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

if __name__ == '__main__':
	gs = GameSpace()
	gs.start()
	lc = LoopingCall(gs.tick())

	cf = ConnFactory(gs, lc)
	reactor.connectTCP(CLIENT_HOST, CLIENT_PORT, cf)
	reactor.run()

class ConnFactory(ClientFactory):
	def __init__(self, gs, lc):
		self.gs = gs
		self.lc = lc

	def buildProtocol(self, addr):
		self.addr = addr
		self.conn = Connection(addr, self.gs, self.lc)

class Connection(Protocol):
	def __init__(self, addr, gs, lc):
		self.addr = addr
		self.gs = gs
		self.lc = lc

	def connectionMade(self):
		print "connection made"
		lc.start(1/60)

	def dataReceived(self, data):
		print "data received", data
		self.gs.addData(data)

	def connectionLost(self, reason):
		print "lost connection"		
