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
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall

import pickle

from level import Level
from block import Block
from tank_obj import tank
from pellet import Pellet
from explode import Explosion
from enemy import Enemy
from connection import *

CLIENT_PORT = 40035
CLIENT_HOST = 'localhost'

class GameSpace(object):
	def __init__(self):
		#1) Basic initialization
		pygame.init()

		self.size = width,height = (640,480)
		self.screen = pygame.display.set_mode(self.size)
		self.background = pygame.image.load("imgs/wood.png")
		self.back_rect = self.background.get_rect()

		self.cf = ServerConnFactory(self)	
		reactor.listenTCP(CLIENT_PORT, self.cf)
		reactor.run()

	def start(self):
		#2) Set up game objects
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
		
	def handleEvents(self, tank, events, mouse):	
		self.tank1.mx = mouse[0]
		self.tank1.my = mouse[1]
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
	
	def handleRemoteEvents(self, tank, events, mouse):
		for event in events:
			if event['type'] == 'quit':
				sys.exit()
			elif event['type'] == 'keyup':
				tank.hold = False
				tank.key = 0
			elif event['type'] == 'keydown':
				if event['key'] == 32:
					tank.tofire = True
					tank.fire_x, tank.fire_y = mouse
				else:
					tank.hold = True
					tank.key = event['key']
			elif event['type'] == 'mousedown':
				tank.tofire = True
				tank.fire_x, tank.fire_y = mouse
			elif event['type'] == 'mouseup':
				tank.tofire = False

	def packageEvents(self, events):
		evs = []
		for event in events:
			ev = {}
			ev['type'] = ''
			if event.type == QUIT:
				ev['type']='quit'
			elif event.type == KEYUP:
				ev['type']='keyup'
				ev['key']=event.key
			elif event.type == KEYDOWN:
				ev['type']='keydown'
				ev['key']=event.key
			elif event.type == MOUSEBUTTONDOWN:
				ev['type']='mousedown'
			elif event.type == MOUSEBUTTONUP:
				ev['type']='mouseup'
			evs.append(ev)
		return evs

	def tick(self):
		state = {}
		state['mouse_pos'] = pygame.mouse.get_pos()
		events = pygame.event.get()
		state['events'] = self.packageEvents(events)
		self.sendState(state)

		self.handleEvents(self.tank1, events, pygame.mouse.get_pos())

		#6) Send ticks to objects
		self.tank1.tick()
		self.teammate.tick()
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

	def addData(self, data):
		self.teammate_state = pickle.loads(data)
		try:
			mouse = self.teammate_state['mouse_pos']
			events = self.teammate_state['events']
			self.teammate.mx = mouse[0]
			self.teammate.my = mouse[1]
			self.handleRemoteEvents(self.teammate, events, mouse)
		except Exception as ex:
			pass

	def sendState(self, state):
		s = pickle.dumps(state)
		self.cf.conn.send(s)

if __name__ == '__main__':
	gs = GameSpace()

