#/usr/bin/python2.7 
import math
import random

COMMON_MAX_LIFE = 10
COMMON_SPEED = 3

class space_mgr():
	def __init__(self,window_size):
		self.window_size = window_size
	def use_space(self):
		pass
	def is_in_window(self):
		pass

	def is_used(self,pos):
		pass

	def free_space(self):
		pass

class bullet_base:
	def __init__(pos,diction,speed=10):
		self.pos=pos
		self.diction = diction
		self.speed = speed

	def move(self):

class weapen_base:
	def __init__(self):
		
	def fire(self,pos,diction):
		return bullet_base(pos,diction)
	

class Tank_base:
	def __init__(self,id,diction='stop', pos=(0,0)):
		self.diction = diction
		self.life = COMMON_MAX_LIFE
		self.weapen = weapen_base()
		self.speed = COMMON_SPEED
		self.pos = pos
		self.size = (3,2)
		self.bullet_time = 4
		self.id = id

	def move(self):
		if self.diction == 'stop':
			pass
		elif self.diction == 'left':
			self.pos[0] -= self.speed
		elif self.diction == 'right':
			self.pos[0] += self.speed
		elif self.diction == 'up':
			self.pos[1] += speed
		elif self.diction == 'down':
			self.pos[1] -= speed
		check_pos()

	def check_pos(self):
		pass
	
	def launch_bullet(self):
		return self.weapen.fire()
	  	
	def change_diction(dic):
		self.diction = dic;

