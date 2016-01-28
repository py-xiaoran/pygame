#/usr/bin/python2.7
import sys,os
import pygame
from pygame.locals import *
import math
import random
import time
image_dir = os.path.join('.','image')
window_size = (400,500)
# direction : 0,up  1,down  2,left  3,right
#
#

def load_image(file):
	path = os.path.join(image_dir,file)
	if os.path.exists(path):
		return  pygame.image.load(path).convert_alpha()
	raise SystemExit("could not load imag!%s"%path)

def random_pos(pos = window_size):
	return (random.randint(0,pos[0]-50),random.randint(0,pos[1]-20))
	
def random_dit():
	return (random.randint(0,4))

def rotate_img(img,angle):
	return pygame.transform.rotate(img,angle)

class Tank(pygame.sprite.Sprite):
	images = []
	def __init__(self,speed = 5):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.direction = 0
		self.speed = speed
	def setpos(self,pos):
		self.rect.move_ip(pos)
	def update(self):
		rect_tmp = self.rect.copy()
		if self.direction == 0:
			rect_tmp.move_ip(0,-self.speed)
			self.image = self.images[0]
		elif self.direction == 1:
			rect_tmp.move_ip(0,self.speed)
			self.image = self.images[1]
		elif self.direction == 2:
			rect_tmp.move_ip(-self.speed,0)
			self.image = self.images[2]
		elif self.direction == 3:
			rect_tmp.move_ip(self.speed,0)
			self.image = self.images[3]
		else:
			self.direction = 0
		if rect_tmp.right >= window_size[0] or rect_tmp.bottom >= window_size[1]:
			return False
		if rect_tmp.left < 0 or rect_tmp.top < 0:
			return False
		self.rect = rect_tmp
		return True		

	def setDit(self,dit):
		if dit <= 3 and dit >= 0:
			self.direction = dit
	def setSpeed(self,speed):
		self.speed = speed

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
	images = []
	def __init__(self,pos,direct):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[direct]
		self.rect = self.image.get_rect()
		self.speed = 15 
		self.direction = direct
		pos = (pos[0] - self.rect.center[0],pos[1] + self.rect.center[1])
		self.rect = pygame.Rect(pos,self.image.get_size())
	def update(self):
		if self.direction == 0:
			self.rect.move_ip(0,-self.speed)
		elif self.direction == 1:
			self.rect.move_ip(0,self.speed)
		elif self.direction == 2:
			self.rect.move_ip(-self.speed,0)
		elif self.direction == 3:
			self.rect.move_ip(self.speed,0)
		else:
			raise TypeError

def main():
	pygame.init()
	pygame.font.init()
	screen =pygame.display.set_mode(window_size)
	clock  = pygame.time.Clock()
	back_ground = load_image('floor.jpg').convert()
	back_ground = pygame.transform.scale(back_ground,screen.get_size())
	screen.blit(back_ground,screen.get_rect(),area=screen.get_rect())
	tank_img = load_image('tank2.png').convert_alpha()
	tank_img = pygame.transform.scale(tank_img,(40,20))
	Tank.images.append(rotate_img(tank_img,90*3)) 
	Tank.images.append(rotate_img(tank_img,90)) 
	Tank.images.append(tank_img)
	Tank.images.append(rotate_img(tank_img,90*2))
	
	bullet_img = load_image('bullet.png').convert_alpha()
	bullet_img = pygame.transform.scale(bullet_img,(18,13))
	Bullet.images.append(rotate_img(bullet_img, 90*3))
	Bullet.images.append(rotate_img(bullet_img, 90))
	Bullet.images.append(bullet_img)
	Bullet.images.append(rotate_img(bullet_img , 90*2))
	
	explode_img = load_image('explosion1.gif')
	explode_img = pygame.transform.scale(explode_img,(45,45))
	Explode.images.append(explode_img)
	explode = pygame.sprite.Group()

	t = Tank()
	player_tk = pygame.sprite.Group()
	player_tk.add(t)
	player_bullet_tk = pygame.sprite.Group()
	enemy_bullet_tk = pygame.sprite.Group()
	enemy_tk = pygame.sprite.Group()
	for i in xrange(4):
		t2 = Tank()
		t2.setpos(random_pos())
		t2.setDit(random_dit())
		enemy_tk.add(t2)
#	shoot_event = 1
#	chg_dit_event = 2
#	pygame.time.set_timer(chg_dit_event,1000)
#	pygame.time.set_timer(shoot_event,2500)
	ti1,ti2 = 0,0
	while t.alive():
		for event in pygame.event.get():
			if event.type == QUIT:
				t.kill()
			elif event.type == KEYDOWN and event.key == K_q:
					t.kill()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					t.setDit(0)
					t.setSpeed(5)
				elif event.key == K_DOWN:
					t.setDit(1)
					t.setSpeed(5)
				elif event.key == K_LEFT:
					t.setDit(2)
					t.setSpeed(5)
				elif event.key == K_RIGHT:
					t.setDit(3)
					t.setSpeed(5)
				elif event.key == K_SPACE:
					player_bullet_tk.add(t.shoot())
			#	else:
			#		continue
			#	player_tk.update()
			elif event.type == KEYUP:
				if event.key in (K_UP,K_DOWN,K_RIGHT,K_LEFT):
					t.setSpeed(0)
		ti_now = pygame.time.get_ticks()
		if ti_now - ti1 > 500:
			ti1 = ti_now
			for enemy in enemy_tk.sprites():
				enemy.setDit(random_dit())
				enemy.setSpeed(random.randint(0,10))
		if ti_now - ti2 > 1000:
			ti2 = ti_now
			for enemy in enemy_tk.sprites():
				enemy_bullet_tk.add(enemy.shoot())
			 	
		# if over or confilt?
		pygame.sprite.groupcollide(player_tk,enemy_tk,True,True)
		pygame.sprite.groupcollide(player_tk, enemy_bullet_tk,True,True)
		sprite_dict = pygame.sprite.groupcollide(enemy_tk, player_bullet_tk,True,True)
		for sprite_tk in sprite_dict.iterkeys():
			pos = sprite_tk.rect.center
			explode.add(Explode(pos))		

		#re draw
		explode.update()
		screen.blit(back_ground,(0,0))
		player_tk.update()
		player_bullet_tk.update()
		enemy_bullet_tk.update()
		for enem in enemy_tk.sprites():
			if not enem.update():
				enem.setDit(random_dit())

		explode.draw(screen)
		player_bullet_tk.draw(screen)
		player_tk.draw(screen)
		enemy_bullet_tk.draw(screen)
		enemy_tk.draw(screen)

		pygame.display.flip()
		clock.tick(20)
	
	font_type = pygame.font.get_default_font()
	font =  pygame.font.Font(None,50)
	w_surface = font.render('Game over',True,(255,255,255))
	posx,posy = screen.get_rect().center
	posx -= w_surface.get_rect().right/2
	screen.blit(w_surface,(posx,posy))
	pygame.display.flip()
	time.sleep(2)
	pygame.quit()
	exit()

if __name__ == '__main__':
	main()
