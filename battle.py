import pygame
from pygame.locals import *
pygame.init()
import random
import time
import math
import _thread


pygame.font.init()
bg_img = pygame.image.load("bg_img.jpg")
width = 500
height = 400

scr = pygame.display.set_mode((width ,height))
pygame.display.set_caption("Battle")
imgs = [pygame.transform.scale2x(pygame.image.load("sp1.png")) , pygame.transform.scale2x(pygame.image.load("sp2.png"))]
E =[pygame.transform.scale2x(pygame.image.load("enemy1.png")),pygame.transform.scale2x(pygame.image.load("enemy2.png")),pygame.transform.scale2x(pygame.image.load("enemy3.png")),
pygame.transform.scale2x(pygame.image.load("enemy4.png"))]
fire = pygame.transform.scale2x(pygame.image.load("fire.png"))
enemy_fire = pygame.transform.scale2x(pygame.image.load("enemy_fire.png"))
kill = pygame.transform.scale2x(pygame.image.load("en-af.png"))

explosion = pygame.mixer.Sound("explosion.wav")

player_explosion = pygame.mixer.Sound("player_explosion1.wav")

bg_color = (0,0,0)
yellow = (255,255,0)
game = True
font2 = pygame.font.SysFont("comicsans", 20)
font3 = pygame.font.SysFont("comicsans", 90)
font1 = pygame.font.SysFont("comicsans", 30)
class Player:
	def __init__(self):
		self.p1 = imgs[0]
		self.p2 = imgs[1]
		self.rect = self.p1.get_rect()
		self.speed = 3
		self.rect[0] = 140
		self.rect[1] = 200
		self.img = self.p1
	def initial(self ,win):
		self.img = self.p1
		win.blit(self.img ,self.rect)

	def	move_left(self ,win):
		win.blit(self.img, self.rect)
		if(self.rect.left>0):
			self.img =self.p2
			self.rect = self.rect.move([self.speed*(-1) , 0])
			scr.fill(bg_color)
			scr.blit(bg_img,(0,0))
			win.blit(self.img ,self.rect)
	def	move_right(self ,win):
		win.blit(self.img, self.rect)
		if(self.rect.right<width):
			self.img =self.p2
			self.rect = self.rect.move([self.speed*(1) , 0])
			scr.fill(bg_color)
			scr.blit(bg_img,(0,0))
			win.blit(self.img ,self.rect)
	def	move_up(self ,win):
		win.blit(self.img, self.rect)
		if(self.rect.top>0):
			self.img =self.p2
			self.rect = self.rect.move([0,self.speed*(-1)])
			scr.fill(bg_color)
			scr.blit(bg_img,(0,0))
			win.blit(self.img ,self.rect)
	def	move_down(self ,win):
		win.blit(self.img, self.rect)
		if(self.rect.bottom<height):
			self.img =self.p2
			self.rect = self.rect.move([0,self.speed*(1)])
			scr.fill(bg_color)
			scr.blit(bg_img,(0,0))
			win.blit(self.img ,self.rect)
	def player_mask(self):
		return pygame.mask.from_surface(self.img)									

class Fire:
	def __init__(self, rect ,y):#5,54.5
		self.fire = fire
		self.y =y
		self.rect = self.fire.get_rect()
		self.rect[0]=rect[0]+16
		self.rect[1] = rect[1]+self.y
		self.speed= 5
	def pos(self,win):
		win.blit(self.fire,self.rect)
		self.rect[0]=self.speed + self.rect[0]
	def firemask(self):
		return pygame.mask.from_surface(self.fire)		
						
class Enemy:
	def __init__(self ,win ):
		self.enemy = E[0]
		self.rect = self.enemy.get_rect()
		self.rect[0] = random.randint(600,1200)
		self.rect[1] = random.randint(0,336)
		self.counter = 0
		self.ps = 0
		self.t = 0
		self.yspeed = random.choice([1,2])
		self.speed = random.choice([2,3,4])
		win.blit(self.enemy ,self.rect)
	def move(self ,win):
		self.t+=1
		self.rect[0] = self.rect[0] - self.speed
		self.rect[1] = self.rect[1] + self.yspeed
		if self.t>50:
			self.t =0
			self.yspeed = -self.yspeed
		if self.counter == 4:
			self.counter = 0
		win.blit(E[int(self.counter%4)],(self.rect[0],self.rect[1]))
		self.ps+=1
		if self.ps>10:
			self.counter+=1	
			self.ps =0
	def enemy_collision(self ,player):
			player_mask = player.player_mask()	
			enemy_mask = pygame.mask.from_surface(self.enemy)
			if player.rect[0]> self.rect[0]-64 and player.rect[0]<self.rect[0]+64:
				if player.rect[1]> self.rect[1]-64 and player.rect[1]<self.rect[1]+64:
					result = player_mask.overlap(enemy_mask ,(self.rect[0]-player.rect[0],self.rect.top-player.rect.top))
					if result:
						return 1
			return 0
	def fire_collision(self,fire):
			fmask = fire.firemask()	
			enemy_mask = pygame.mask.from_surface(self.enemy)
			if fire.rect[0]> self.rect[0]-64 and fire.rect[0]<self.rect[0]+64:
				if fire.rect[1]> self.rect[1]-64 and fire.rect[1]<self.rect[1]+64:
					result = fmask.overlap(enemy_mask ,(self.rect[0]-fire.rect[0],self.rect.top-fire.rect.top))
					if result:
						return 1			
class Enemy_Fire:
	def __init__(self ,win ):
		self.enemy = enemy_fire
		self.rect = self.enemy.get_rect()
		self.rect[0] = random.randint(500,1400)
		self.rect[1] = random.randint(0,395)
		win.blit(self.enemy ,self.rect)
		
	def move(self ,win, speed):
		self.speed = speed
		self.rect[0] = self.rect[0]- self.speed
		win.blit(self.enemy ,self.rect)
	def player_collision(self ,player):
		player_mask = player.player_mask()	
		enemy_mask = pygame.mask.from_surface(self.enemy)
		if player.rect[0]> self.rect[0]-64 and player.rect[0]<self.rect[0]+64:
			if player.rect[1]> self.rect[1]-64 and player.rect[1]<self.rect[1]+64:
				result = player_mask.overlap(enemy_mask ,(self.rect[0]-player.rect[0],self.rect.top-player.rect.top))
				if result:
					return 1
		return 0	

def writescore(score,HighScore,life, scr):
	t1 = font1.render("Score: " + str(score),False,(255,255,255))
	t2 = font2.render("Highest Score: " + str(HighScore),False,(255,255,255))
	t3 = font2.render("Life: " + str(life),False,(255,255,255))
	scr.blit(t1, (0,15))
	scr.blit(t2, (0,0))
	scr.blit(t3, (150,0))

def gameover(score,scr):
	t1 = font3.render("GAME OVER" ,False,(200,200,200))
	t2 =font1.render("Score: "+str(score) ,False ,(212,190,255))
	scr.blit(t1,(64,120))
	scr.blit(t2,(210,180))


class Kill:
	def __init__(self, loc, win):
		self.kill = kill
		self.duration = 10
		self.loc = loc
		self.win = win

	def showUp(self):
		self.win.blit(self.kill,(self.loc[0],self.loc[1]))
		self.duration-=1

kill_list = []

HighScore =0
score=0
def main(game ,score, HighScore):
	player = Player()
	enemies = []
	init = True
	clock = pygame.time.Clock()
	morse =0
	fired = False
	fires =[]
	enfi = []
	en_speed = 2.2
	for _ in range(7):
		enemy = Enemy(scr)
		enemies.append(enemy)
	for _ in range(3):
		fi = Enemy_Fire(scr)
		enfi.append(fi)	
	allowed = 1000
	lives = 3
	while(game):
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game = False
		keys = pygame.key.get_pressed()
		scr.fill(bg_color)
		scr.blit(bg_img,(0,0))
		#Collision Checkings---------
		for i,fi in enumerate(enfi):
			fi.move(scr , 6)
			if fi.player_collision(player):
				player_explosion.play()
				lives-=1
				#print(lives)
				if lives ==0:
					scr.blit(kill,player.rect)
					gameover(score,scr)
					pygame.display.update()
					
					kill_list.clear()
					pygame.time.delay(2000)
					game = False
					score = 0
					main(True ,score,HighScore)
				enfi.remove(enfi[i])
				new = Enemy_Fire(scr)
				enfi.append(new)
		for i, enemy in enumerate(enemies):
			enemy.move(scr)	
			if enemy.enemy_collision(player):
				player_explosion.play()
				kill_list.append(Kill(enemy.rect,scr))
				lives-=1
				if lives ==0:
					scr.blit(kill,player.rect)
					gameover(score,scr)
					pygame.display.update()

					kill_list.clear()
					game = False
					pygame.time.delay(2000)
					score = 0
					main(True ,score,HighScore)
				enemies.remove(enemies[i])
				new = Enemy(scr)
				enemies.append(new)
			for	j,fire in enumerate(fires):
				if enemy.fire_collision(fire)==1:	
					score+=1
					if score>HighScore:
						HighScore+=1
					fires.remove(fires[j])
					enemies.remove(enemies[i])
					explosion.play()
					kill_list.append(Kill(enemy.rect,scr))
					new = Enemy(scr)
					enemies.append(new)

		for b_index,blasts in enumerate(kill_list):
			if blasts.duration<0:
				kill_list.remove(kill_list[b_index])
				continue
			else:
				blasts.showUp()	

		if score>10:
			en_speed =1.7	
		if(keys[pygame.K_LEFT]):
			morse =0
			init =False	
			player.move_left(scr)
			for en in enemies:
				scr.blit(E[int(en.counter%4)],(en.rect[0],en.rect[1]))
			for fi in enfi:
				scr.blit(fi.enemy,fi.rect)	

			for b_index,blasts in enumerate(kill_list):
				if blasts.duration<0:
					kill_list.remove(kill_list[b_index])
					continue
				else:
					blasts.showUp()	
					
		if(keys[pygame.K_RIGHT]):
			morse =0
			init =False	
			player.move_right(scr)
			for en in enemies:
				scr.blit(E[int(en.counter%4)],(en.rect[0],en.rect[1]))
			for fi in enfi:
				scr.blit(fi.enemy,fi.rect)	

			for b_index,blasts in enumerate(kill_list):
				if blasts.duration<0:
					kill_list.remove(kill_list[b_index])
					continue
				else:
					blasts.showUp()	

		if(keys[pygame.K_UP]):
			morse =0
			init =False	
			player.move_up(scr)
			for en in enemies:
				scr.blit(E[int(en.counter%4)],(en.rect[0],en.rect[1]))
			for fi in enfi:
				scr.blit(fi.enemy,fi.rect)	

			for b_index,blasts in enumerate(kill_list):
				if blasts.duration<0:
					kill_list.remove(kill_list[b_index])
					continue
				else:
					blasts.showUp()		

		if(keys[pygame.K_DOWN]):
			morse =0
			init =False	
			player.move_down(scr)
			for en in enemies:
				scr.blit(E[int(en.counter%4)],(en.rect[0],en.rect[1]))
			for fi in enfi:
				scr.blit(fi.enemy,fi.rect)	

			for b_index,blasts in enumerate(kill_list):
				if blasts.duration<0:
					kill_list.remove(kill_list[b_index])
					continue
				else:
					blasts.showUp()	
		if(keys[pygame.K_SPACE]):
			if allowed > 100:
				fired =True
				rekt=[]
				for i in player.rect:
					rekt.append(i)
				fire1 =Fire(rekt ,5)
				fire2 = Fire(rekt, 54.5)
				fires.append(fire1)
				fires.append(fire2)

				allowed = 0		
		allowed+=2		
		morse+=1	

		if init or  morse>2:
			player.initial(scr)	
			pan = False

		if fired:
			for i,fire in enumerate(fires):	
				fire.pos(scr)
				if fire.rect[0]>510:
					fires.remove(fires[i])
		for i,enemy in enumerate(enemies):
			if enemy.rect[0] < -150:
				enemies.remove(enemies[i])
				new = Enemy(scr)
				enemies.append(new)	
		for i,enemy in enumerate(enfi):
			if enemy.rect[0] < -150:
				enfi.remove(enfi[i])
				new = Enemy_Fire(scr)
				enfi.append(new)			
		writescore(score,HighScore,lives,scr)
		pygame.display.update()


if __name__=="__main__":
	main(game ,score,HighScore)