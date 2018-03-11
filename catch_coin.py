# -*- coding: cp936 -*-
import sys
import random

import pygame
from pygame.locals import *

import files

class Coin(pygame.sprite.Sprite):
    def __init__(self, image, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.screen = screen
        
    def update(self):
        self.rect = self.rect.move(self.speed)
        
        if self.rect.bottom >= self.screen.get_height():
            self.kill()
            
class Basket(pygame.sprite.Sprite):
    def __init__(self, image, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Main:
    def __init__(self, surface, mainscreen):
        self.screen = mainscreen
        self.surface = surface
        self.surface.fill((70, 187, 217))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = mainscreen.get_rect().center
        self.init_timer()
        self.load_data()
        self.create_obj()
        self.run()
            
    def init_timer(self):
        self.total_cur = 0
        self.total_secondcur = 0
        self.total_timer = 30
        
        self.timer_rect=Rect(0,15,400,30)
        self.timer_rect.centerx=self.surface.get_rect().centerx
        self.timertube_linewidth=3
        self.timertube_rect = Rect(0,0,self.timer_rect.width+self.timertube_linewidth*2,   \
                                self.timer_rect.height+self.timertube_linewidth*2)
        self.timertube_rect.center = self.timer_rect.center
    
    def load_data(self):
        self.basket_img = files.load_image("basket.png")
        self.coin_img = files.load_image("coin.png")
        
        self.bg_music = files.load_music("bg_music.mp3", 0.3, -1)   
        self.getpoint_sound = files.load_sound("get_point.wav", 0.2)
        self.gameover_sound = files.load_sound("game_over.wav", 0.6)   
        
    def create_obj(self):
        self.done = False
        self.points = 0
        self.catch_coins = 0
        self.add_cur = 0
        self.add_timer = 10
        self.total_coins = 0
        self.clock = pygame.time.Clock()
        self.coin_group = pygame.sprite.Group()
        self.basket_obj = Basket(self.basket_img,   \
                            [270, self.surface.get_height()-self.basket_img.get_rect().height])
        
        self.font = pygame.font.SysFont("microsoftyahei", 30)
        
    def gen_objs(self):
        self.add_cur += 1
        if self.add_cur >= self.add_timer:
            self.total_coins += 1
            x = random.randint(0+50, self.surface.get_width()-50)
            y = 0 - self.coin_img.get_rect().height
            
            self.coin_group.add(Coin(self.coin_img, [x, y], [0, 9], self.surface))
            self.add_cur = 0
            
    def update(self):
        self.coin_group.update()
        
        self.total_secondcur += 1
        if self.total_secondcur >= 30:
            self.total_cur += 1
            self.total_secondcur = 0
            
    def collide(self):
        coin_list = pygame.sprite.spritecollide(self.basket_obj, self.coin_group, 1)
        for obj in coin_list:
            self.getpoint_sound.play()
            self.points += 1
            self.catch_coins += 1
            
    def display(self):
        self.surface.fill((70, 187, 217))
        self.screen.blit(self.surface, self.surface_rect)
        self.coin_group.draw(self.surface)
        self.surface.blit(self.basket_obj.image, self.basket_obj.rect)
        
        self.surface.blit(self.font.render(u"分数:%s" % str(self.points), 1, (0, 0, 0)), [10, 10])
        self.surface.blit(self.font.render(u"金币数:%s" % str(self.catch_coins), 1, (0, 0, 0)), [10, 50])  
        
        self.screen.blit(self.surface, self.surface_rect)
        pygame.display.update()
    
    def game_over(self):
        if not self.done:
            self.gameover_sound.play()
        screen = self.surface
        
        final_text1 = u"游戏结束"
        final_text2 = u"你加了%s分" % str(self.points)
        final_text3 = u"你捡到了%s个金币 (百分之%s)" %  \
        (str(self.catch_coins), str(int(float(self.catch_coins)/self.total_coins*100)))
        
        screen.fill((70, 187, 217))
        ft1_font = pygame.font.SysFont("microsoftyahei", 50)
        ft1_surf = ft1_font.render(final_text1, 1, (0, 0, 0))
        ft2_font = pygame.font.SysFont("microsoftyahei", 30)
        ft2_surf = self.font.render(final_text2, 1, (0, 0, 0))
        ft3_surf = self.font.render(final_text3, 1, (0, 0, 0))
        
        screen.blit(ft1_surf, [screen.get_width()/2 - ft1_surf.get_width()/2, 100])
        screen.blit(ft2_surf, [screen.get_width()/2 - ft2_surf.get_width()/2, 200])
        screen.blit(ft3_surf, [screen.get_width()/2 - ft3_surf.get_width()/2, 250])
        self.screen.blit(self.surface, self.surface_rect)
        pygame.display.update()
              
        pygame.mixer.music.fadeout(2000)     
        pygame.time.delay(5000)
        self.done = True
        
    def run(self):
        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                
                elif event.type == pygame.MOUSEMOTION:
                    if not self.done:
                        self.basket_obj.rect.centerx = event.pos[0]
                        if self.basket_obj.rect.right > self.surface.get_rect().right:
                            self.basket_obj.rect.right =  self.surface.get_rect().right

                        if self.basket_obj.rect.left < self.surface.get_rect().left:
                            self.basket_obj.rect.left = self.surface.get_rect().left
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    
                    elif event.key == pygame.K_RETURN:
                        if  self.done:
                            return
                    
            if not self.done:             
                self.gen_objs()
                self.update()
                self.collide()
                self.display()
            
            if self.total_cur >= self.total_timer:
                self.game_over()
            

            
                

                
        
        
        
        
    
    
            