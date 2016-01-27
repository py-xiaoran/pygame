#!/usr/bin/python
import pygame 
from pygame.locals import *
class basheng:
	def __init__(self,image,size):
		self.image = image   #pygame.image.load(file).convert()
		self.rect = self.image.get_rect()
		self.img_size = size
		self.count = self.rect.left/self.img_size[0]*self.rect.bottom/self.img_size[1]
		self.cur_img = 0
		self.cur_rect = pygame.Rect(0,0,self.img_size[0],self.img_size[1])
	def update(self,target):
		self.cur_img += 1
		if self.cur_img >= self.count:
			self.cur_img = 0
		top = self.img_size[1]*target
		self.cur_rect.top = top
		self.cur_rect.bottom = top + self.img_size[1]
		self.cur_rect.move_ip(self.img_size[0],0)
		#self.cur_rect = pygame.Rect(self.cur_rect.left,top,self.img_size[0],self.img_size[1])
		if self.cur_rect.right > self.rect.right:
			self.cur_rect = pygame.Rect(0,top,self.img_size[0],self.img_size[1])
		#if self.cur_rect.bottom > self.rect.bottom:
		#	self.cur_rect = pygame.Rect(0,0,self.img_size[0],self.img_size[1])

def main():
	pygame.init()
	screen = pygame.display.set_mode((200,200))
	file = './data/basheng.png'
	image = pygame.image.load(file).convert()
	image_size = image.get_size()
	signal_size = (image_size[0]/6,image_size[1]/6)
	bh = basheng(image,signal_size)
	screen = pygame.display.set_mode(signal_size,pygame.NOFRAME)
	going = True
	target = 0
	clock = pygame.time.Clock()
	while going:
		clock.tick(20)
		for event in pygame.event.get():
			if event.type == QUIT:
				going = False
			if event.type == KEYDOWN:
				if event.key == K_q:
					going = False
				elif event.key == K_a:
					target = 0
					#bh.update(0)#('light_hand')
				elif event.key == K_s:
					target = 1
					#bh.update(1)#('high_hand')
				elif event.key == K_d:
					target = 2
					#bh.update(2)#('light_foot')
				elif event.key == K_f:
					target = 3
					#bh.update(3)#('high_foot1')
				elif event.key == K_g:
					target = 4
					#bh.update(4)#('light_foot2')
				elif event.key == K_h:
					target = 5
					#bh.update(5)#('light_foot2')
		screen.fill((255,255,255))
		screen.blit(bh.image,(0,0),area=bh.cur_rect)
		bh.update(target)
		pygame.display.flip()
	pygame.quit()
	exit()

if __name__ == '__main__':
	main()
