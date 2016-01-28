#/usr/bin/python2.7
import sys,os
import pygame
from pygame.locals import *
import math
import random
import time
image_dir = os.path.join('.','image')
window_size = (400,500)
TK_SIZE1 = (40,20)
BT_SIZE1 = (10,10)
# direction : 0,up  1,down  2,left  3,right
#
#
#pygame to std degree
def degree_trans(degree):
	return degree+180

def angle_degree(angle):
	return angle*180/math.pi

def load_image(file):
	path = os.path.join(image_dir,file)
	if os.path.exists(path):
		return  pygame.image.load(path).convert_alpha()
	raise SystemExit("could not load imag!%s"%path)

def random_pos(pos = window_size):
	return (random.randint(0,pos[0]-50),random.randint(0,pos[1]-20))
	
def random_dit():
	return (random.randint(0,4))

#angle is std degree
def rotate_img(img,angle):
	return pygame.transform.rotate(img,angle)

class Tank(pygame.sprite.Sprite):
	container = None
	all_container = []
	image = None
	def __init__(self,speed = 5):
		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.direction = Vector(0,0)
		self.direction.set_special(0)
		self.speed = speed
		self.change_dirt = False
	def setpos(self,pos):
		self.rect.move_ip(pos)
	def update(self):
		pos = self.direction.move(self.speed)
		self.rect.move_ip(pos)
		if not self.move_ok():
			self.rect.move_ip((-pos[0],-pos[1]))
		if self.change_dirt:
			angle = self.direction.get_angel()
		#	angle = degree_trans(angle)	
		#	self.image = pygame.transform.rotate(self.image,angle)#images[]
	def setDit(self,dit):
		if not self.direction.is_same_angel(dit.get_angel()):
			self.direction = dit
			self.change_dirt = True
	def run(self):
		self.setSpeed()
	def setSpeed(self,speed=5):
		self.speed = speed
	def stop(self):
		self.speed = 0

	def move_ok(self):
		for con in self.all_container:
			if pygame.sprite.spritecollide(self,con,False):
				return False
		if self.rect.left < 0 or self.rect.bottom > window_size[1] or self.rect.right > window_size[0] or self.rect.top < 0:
			#self.direction.set_special(random_dit())
			return False
		return True 		

	def shoot(self):
		return Bullet(self.rect.center,self.direction)



class Wall(pygame.sprite.Sprite):
	images = []
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.imags[0]
		self.rect = self.image.get_rect()
	def update(self):
		pass

class Explode(pygame.sprite.Sprite):
	images = []
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[0]
		self.rect =self.image.get_rect()
		self.rect.move_ip(pos)
		self.count = 3 
	def update(self):
		self.count -= 1
		if self.should_kill():
			self.kill()

	def should_kill(self):
		if self.count <= 0:
			return True
		else:
			return False

class Bullet(pygame.sprite.Sprite):
	image = None
	def __init__(self,pos,direct):
		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.speed = 15 
		self.direction = direct
		pos = (pos[0] - self.rect.center[0],pos[1] + self.rect.center[1])
		self.rect = pygame.Rect(pos,self.image.get_size())
	def update(self):
		pos = self.direction.move(self.speed)
		self.rect.move_ip(pos)


class bullet_light(pygame.sprite.Sprite):
	image = None
	def __init__(self,pos,direct,file):
		pygame.sprite.Sprite.__init__(self)
		angle = direct.get_angle()
		rotate_img(self.image,direct.get_angle())
		self.rect = self.image.get_rect()
		self.rect.move_ip(pos)
		self.direct = direct
	def update(self):
		self.direct.move(speed)

# using pygame x,y
# if want std angle should transform
class Vector():
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __add__(self,vec):
		return Vector(self.x + vec.x, self.y + vec.y)
	def get_angel(self):
		if self.x == 0:
			return self.y*math.pi/4
		return math.atan(float(self.y)/self.x)
		#return math.
	def __sub__(self,vec):
		return Vector(self.x - vec.x, self.y - vec.y)
	def is_same_angel(self,angel):
		return angel == self.get_angel()
	def set_special(self,dit_id):
		#speical direction : 0:up, 1:down  2:left 3:right
		if dit_id == 0:
			self.x = 0
			self.y = -1
		elif dit_id == 1:
			self.x = 0
			self.y = 1
		elif dit_id == 2:
			self.x = -1
			self.y = 0
		elif dit_id == 3:
			self.x = 1
			self.y = 0
	#return ^x and ^y
	def move(self,len):
		angel = self.get_angel()
		return (len*self.x,len*self.y)
		#areturn (len*math.sin(angel),len*math.cos(angel))


class Battery(pygame.sprite.Sprite):
	images = []
	def __init__(self,pos):
		pygame.sprite.Sprite(self)
		self.direction = Vector(0,0)
		self.direction.set_special(0)
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.move_ip(pos)
	def update(self):
		self.rect.move_ip(self.direction.move(speed))

# args must have function: draw,update
class EventCtrl():
	def __init__(self,surface,back_ground ,fps = 20):
		self.fps = fps
		self.Clock = pygame.time.Clock()
		#self.draw_func()
		self.time = 0
		self.timer_li = {}
		self.back_ground = back_ground
		self.surface = surface
	def set_timer(self,time_tick_id,time_tick,func):
		self.timer_li[time_tick_id] = {'time_tick':time_tick,'time_last':0,'func':func}
		#self.time_li.append((time_tick,time_last,func,False))
	def ev_key_down(self):
		pass
	def ev_key_up(self):
		pass
	def ev_mouse(self):
		pass
	def ev_quit(self):
		going = False
	def draw_func(self,surface):
		pass
	def update_all(self):
		pass
	def event_loop(self):
		going = True
		while going:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.ev_quit()
				elif event.type == KEYDOWN:
					self.ev_key_down(event.key)
				elif event.type == KEYUP:
					self.ev_key_up(event.key)
				elif event.type == MOUSEMOTION:
					self.ev_mouse(event)
			time_now = pygame.time.get_ticks()
			for id,ti in self.timer_li.items():
				if time_now - ti['time_last'] >= ti['time_tick']:
					ti['time_last'] = time_now
					func = ti['func']
					func()
			self.ext_ctrl()
			self.update_all()
			self.surface.blit(self.back_ground,(0,0))
			self.draw_func(self.surface)
			self.Clock.tick(self.fps)
			pygame.display.flip()
		pygam.quit()
		exit()
	def update_all():
		pass
	def end(self):
		self.going = False
	def ext_ctrl(self):
		pass

class TankEvent(EventCtrl):
	player_group = None
	enemy_group = None
	player_bullet_group = None
	enemy_bullet_group = None
	explode_group = None
	wall_group  = None
	surface = None
	back_ground = None
	def __init__(self):
		EventCtrl.__init__(self,self.surface,self.back_ground)
		self.set_timer(1,500,self.change_dirt)
		self.set_timer(2,1000,self.shoot)
		self.player_tk = self.player_group.sprites()[0]
		self.level_ctrl = LevelCtrl()
		for enemy in self.level_ctrl.product_enemy():
			self.enemy_group.add(enemy)
	def ev_key_down(self,key):
		direction = Vector(0,0)
		if key == K_UP:
			direction.set_special(0)
			self.player_tk.setDit(direction)
			self.player_tk.run()
		elif key == K_DOWN:
			direction.set_special(1)
			self.player_tk.setDit(direction)
			self.player_tk.run()
		elif key == K_LEFT:
			direction.set_special(2)
			self.player_tk.setDit(direction)
			self.player_tk.run()
		elif key == K_RIGHT:
			direction.set_special(3)
			self.player_tk.setDit(direction)
			self.player_tk.run()
		elif key == K_SPACE:
			bullet = self.player_tk.shoot()
			self.player_bullet_group.add(bullet)
	def ev_key_up(self,key):
		if key in (K_DOWN,K_UP,K_LEFT,K_RIGHT):
			self.player_tk.stop()
	def ev_mouse(self,event):
		pass
	def change_dirt(self):
		for enemy in self.enemy_group.sprites():
			d = random_dit()
			vec = Vector(0,0)
			vec.set_special(d)
			enemy.setDit(vec)
	def shoot(self):
		for enemy in self.enemy_group.sprites():
			self.enemy_bullet_group.add(enemy.shoot())
	def draw_func(self,surface):
		self.player_group.draw(surface)
		self.enemy_group.draw(surface)
		self.player_bullet_group.draw(surface)
		self.enemy_bullet_group.draw(surface)
		self.exported_group.draw(surface)
		if self.wall_group:
			wall_group.draw(surface)
	
	def level_up():
		enemy_li = self.level_ctrl.next_level()
		if enemy_li():
			self.end()
		for enemy in enemy_li:
			enemy_group.add(enemy)
	def ext_ctrl(self):
		self.confilct_check()
		self.level_check()
	def level_check(self):
		if self.level_ctrl.enemy_empty():
			self.level_up()
	def update_all(self):
		self.player_group.update()
		self.enemy_group.update()
		self.player_bullet_group.update()
		self.enemy_bullet_group.update()
		if self.wall_group:
			self.wall_group.update()
	def confilct_check(self):
		pygame.sprite.groupcollide(self.enemy_group,self.player_bullet_group,True,True)
		pygame.sprite.groupcollide(self.player_bullet_group,self.enemy_bullet_group,True,True)

class LevelCtrl():
	def __init__(self):
	#	self.enemy_group = enemy_group
		self.cur_level = 1
		self.data = {1:[Tank]*3,
			     2:[Tank]*2+[Battery],
			     3:[Battery]*3,
				}
	def enemy_empty(self):
		if self.get_enemy_size() == 0:
			return True
		return False
	def get_enemy_size(self):
		return len(self.data[self.cur_level])
	def next_level(self):
		if self.cur_level < 3:
			self.cur_level += 1
			return self.product_enemy()
		else:
			return []
	def product_enemy(self):
		enemy_li = []
		for enemy_base in self.data[self.cur_level]:
			enemy = enemy_base()
			enemy.setpos(random_pos())
			enemy_li.append(enemy)
		return enemy_li
def Init_image():
	tk_image = load_image('tank2.png')
	bullet_image = load_image('bullet.png')
	Tank.image = pygame.transform.scale(tk_image,TK_SIZE1)
	Bullet.image = pygame.transform.scale(bullet_image,BT_SIZE1)

def app():
	pygame.init()
	pygame.font.init()
	font = pygame.font.Font(None,50)
	screen = pygame.display.set_mode(window_size)
	back_ground = load_image('floor.jpg')
	back_ground = pygame.transform.scale(back_ground,window_size)
	Init_image()
	player = Tank()
	TankEvent.surface = screen
	TankEvent.exported_group = pygame.sprite.Group()
	TankEvent.player_group = pygame.sprite.Group()
	TankEvent.player_group.add(player)
	TankEvent.enemy_group =  pygame.sprite.Group()
#	TankEvent.enemy_group.add
	TankEvent.enemy_bullet_group = pygame.sprite.Group()
	TankEvent.player_bullet_group = pygame.sprite.Group()
	TankEvent.explode = pygame.sprite.Group()
	TankEvent.back_ground = back_ground
	tk_ctrl = TankEvent()
	tk_ctrl.event_loop()

if __name__ == '__main__':
	app()
