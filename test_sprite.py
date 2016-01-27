#/usr/bin/python2.7
import pygame
from pygame.locals import *

class fish(pygame.sprite.Sprite):
	def __init__(self,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.move = 9
		self.rect = self.image.get_rect()
	def update(self):
		if self.rect.left > 300 or self.rect.left < 0:
			self.move = -self.move
		self.rect.move_ip(self.move,0)
		
class hand(pygame.sprite.Sprite):
	def __init__(self,image):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = image.get_rect()
	def update(self):
		self.rect.midtop = pygame.mouse.get_pos()

def main():
	pygame.init()
	screen = pygame.display.set_mode((300 ,100))
	back_ground = pygame.Surface(screen.get_size()).convert()
	back_ground.fill((255,255,255))
	img = pygame.image.load('chimp.bmp').convert()
	print img.get_at((0,0))
	img.set_colorkey(img.get_at((0,0)),RLEACCEL)
	f = fish(img)
	img2 = pygame.image.load('fist.bmp').convert()
	img2.set_colorkey(img2.get_at((0,0)),RLEACCEL)
	h = hand(img2)
	pygame.mouse.set_visible(False)
	allsprites = pygame.sprite.RenderPlain((f,h))
	clock = pygame.time.Clock()
	while True:
		clock.tick(20)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		screen.blit(back_ground,screen.get_rect())
		allsprites.update()
		allsprites.draw(screen)
		pygame.display.flip()

if __name__ == "__main__":
	main()
