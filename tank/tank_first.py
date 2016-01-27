#/usr/bin/python2.7
import sys,os
import pygame
from pygame.locals import *
import math
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

def rotate_img(img,angle):
	return pygame.transform.rotate(img,angle)

class Tank(pygame.sprite.Sprite):
	images = []
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.direction = 0
		self.speed = 5
	def update(self):
		if self.direction == 0:
			self.rect.move_ip(0,-self.speed)
			self.image = self.images[0]
		elif self.direction == 1:
			self.rect.move_ip(0,self.speed)
			self.image = self.images[1]
		elif self.direction == 2:
			self.rect.move_ip(-self.speed,0)
			self.image = self.images[2]
		elif self.direction == 3:
			self.rect.move_ip(self.speed,0)
			self.image = self.images[3]
		else:
			self.direction = 0
	def setDit(self,dit):
		if dit <= 3 and dit >= 0:
			self.direction = dit
	def shoot(self):
		return Bullet((self.rect.left + 10,self.rect.top+10),self.direction)


class Wall(pygame.sprite.Sprite):
	images = []
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.imags[0]
		self.rect = self.image.get_rect()
	def update(self):
		pass

class Bullet(pygame.sprite.Sprite):
	images = []
	def __init__(self,pos,direct):
		pygame.sprite.Sprite.__init__(self)
		self.image = self.images[direct]
		self.rect = self.image.get_rect()
		self.speed = 15 
		self.direction = direct
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
	Bullet.images.append(rotate_img(bullet_img , 90))
	t = Tank()
	player_tk = pygame.sprite.Group()
	player_tk.add(t)
	bullet_tk = pygame.sprite.Group()
	dit = 1
	while t.alive():
		for event in pygame.event.get():
			if event.type == QUIT:
				t.kill()
			elif event.type == KEYDOWN and event.key == K_q:
				t.kill()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					dit = 0
				elif event.key == K_DOWN:
					dit = 1
				elif event.key == K_LEFT:
					dit = 2
				elif event.key == K_RIGHT:
					dit = 3
				elif event.key == K_SPACE:
					bullet_tk.add(t.shoot())
				t.setDit(dit)
				player_tk.update()

		#re draw
		# if over or confilt?
		screen.blit(back_ground,(0,0))
		player_tk.draw(screen)
		bullet_tk.draw(screen)
		player_tk.update()
		bullet_tk.update()
		pygame.display.flip()
		clock.tick(20)
	pygame.quit()
	exit()

if __name__ == '__main__':
	main()
