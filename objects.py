# Elliott Runburg
# Breanna Devore-McDonald
# Tanks Game
# Programming Paradigms final project
# 4-23-16
# Objects file

import sys
import os
import pygame
import math
from pygame.locals import *

class DeathStar(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("deathstar.png")
		self.orig_image = pygame.image.load("deathstar.png")
		self.rect = self.image.get_rect()
		self.rect.center = (100,200)
		self.fire_x = 0
		self.fire_y = 0

		self.tofire = False
	
	def tick(self):
		mx, my = pygame.mouse.get_pos()
		dx = mx - self.rect.centerx
		dy = self.rect.centery - my

		if self.tofire == True:
			laser = Laser(math.atan2(self.rect.centery-self.fire_y,self.fire_x-self.rect.centerx), self.rect.center, self.gs)
			self.gs.lasers.append(laser)
			if pygame.mixer.music.get_busy() == False:
				pygame.mixer.music.load("screammachine.wav")
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
		else:
			pygame.mixer.stop()
			if dx != 0:
				self.image = pygame.transform.rotate(self.orig_image, math.atan2(dy,dx)/math.pi*180-40)
				self.rect = self.image.get_rect(center=self.rect.center)


	def move(self, keycode):
		if keycode == 273:
			self.rect = self.rect.move(0, -5)
		elif keycode == 274:
			self.rect = self.rect.move(0, 5)
		elif keycode == 275:
			self.rect = self.rect.move(5, 0)
		elif keycode == 276:
			self.rect = self.rect.move(-5, 0)


class Laser(pygame.sprite.Sprite):
	def __init__(self, angle, center, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("laser.png")
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.angle = angle

	def tick(self):
		dx = math.cos(self.angle)*3
		dy = math.sin(self.angle)*-3

		self.rect = self.rect.move(dx, dy)
		if self.rect.centerx > 640 or self.rect.centery > 480:
			self.gs.lasers.remove(self)


class Planet(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.image = pygame.image.load("globe.png")
		self.red_im = pygame.image.load("globe_red100.png")
		self.blank = pygame.image.load("empty.png")
		self.rect = self.image.get_rect()
		self.rect.center = (500,480)
		self.hp = 1000
		self.radius = self.rect.width/2-20
		
	def tick(self):
		if self.hp > 0:
			for laser in self.gs.lasers:
				if pygame.sprite.collide_circle(self, laser):
					self.hp -= 15
					self.gs.lasers.remove(laser)
			if self.hp <= 500:
				self.image = self.red_im
				self.rect = self.image.get_rect()
				self.rect.center = (500, 480)
		else:
			self.image = self.blank


class Explosion(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.gs = gs
		self.expl_imgs = [pygame.image.load("explosion/frames016a.png"),
					 pygame.image.load("explosion/frames000a.png"),
					 pygame.image.load("explosion/frames001a.png"),
					 pygame.image.load("explosion/frames002a.png"),
					 pygame.image.load("explosion/frames003a.png"),
					 pygame.image.load("explosion/frames004a.png"),
					 pygame.image.load("explosion/frames005a.png"),
					 pygame.image.load("explosion/frames006a.png"),
					 pygame.image.load("explosion/frames007a.png"),
					 pygame.image.load("explosion/frames008a.png"),
					 pygame.image.load("explosion/frames009a.png"),
					 pygame.image.load("explosion/frames010a.png"),
					 pygame.image.load("explosion/frames011a.png"),
					 pygame.image.load("explosion/frames012a.png"),
					 pygame.image.load("explosion/frames013a.png"),
					 pygame.image.load("explosion/frames014a.png"),
					 pygame.image.load("explosion/frames015a.png")]
		self.curr_im = 0
		self.image = self.expl_imgs[self.curr_im]
		self.rect = self.image.get_rect()
		self.rect.center = (500,400)	
		self.death_tick = 0

	def tick(self):	
		self.death_tick += 1
		if self.death_tick % 8 == 0 and self.curr_im < 15:
			self.curr_im += 1
			self.image = self.expl_imgs[self.curr_im]
			self.rect = self.image.get_rect()
			self.rect.center = (500,400)
			pygame.mixer.music.load("explode.wav")
			pygame.mixer.music.play()


