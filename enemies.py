# -*- coding: cp936 -*-
"""一个模块用来建立战舰的可移动敌人。"""
import pygame
from pygame.locals import *

import random

class Submarine(pygame.sprite.Sprite):
    """敌人潜艇类"""
    def __init__(self, image, location, speed, shoot_timer, screen):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        if speed[0] < 0: 
            self.image = pygame.transform.flip(image, True, False)
        else: 
            self.image = image            
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #定义自身数据
        self.screen = screen
        self.shoot = False
        self.shoot_cur = 0
        self.shoot_timer = shoot_timer
        self.turn_cur = 0 
        self.find_cur = 0
        
    def update(self):
        """一个方法用来更新潜艇的位置，
        同时还检查各操作的时间是否已到
        """        
        self.rect = self.rect.move(self.speed)
        self.shoot = False
        
        #检查位置是否越界
        if self.rect.right > (self.screen.get_width() + 100):
            self.kill()
            
        if self.rect.left < -(self.rect.width+100):
            self.kill()
        
        #更新时间计数
        self.shoot_cur+= 1
        self.turn_cur += 1
        
        #检查是否已到时间发射鱼雷
        if self.shoot_cur >= random.randint(self.shoot_timer-15, self.shoot_timer+15):
            self.shoot = True
            self.shoot_cur = 0
        
        #检查是否已到时间改变方向
        if self.turn_cur >= random.randint(290, 440):
            self.speed[0] = -self.speed[0]
            self.turn_cur = 0
        
    def find_warship(self, warship_pos, timer):
        #更新时间计数
        self.find_cur += 1
        
        #检查是否已到时间追击战舰
        if self.find_cur >= timer:
            if warship_pos[0] > self.rect.right:
                if not self.speed[0] > 0:
                    self.speed[0] = -self.speed[0]
                    
            elif warship_pos[0] < self.rect.left:
                if not self.speed[0] < 0:
                    self.speed[0] = -self.speed[0]
                    
            self.find_cur = 0
        
class Diver(pygame.sprite.Sprite):
    """敌人潜水员类"""
    def __init__(self, images, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        if speed[0] < 0: 
            self.image_list = [pygame.transform.flip(images[0], True, False),   \
                    pygame.transform.flip(images[1], True, False)]
        else: 
            self.image_list = images
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #定义自身数据
        self.screen = screen
        self.updown_cur = 0
        self.changeimage_cur = 0
        self.changeimage_timer = 12
        
    def update(self):
        """一个方法用来更新潜水员的位置，
        同时还检查改变上下方向的时间是否已到
        """                        
        self.rect = self.rect.move(self.speed)
        
        #检查位置是否越界
        if self.rect.right > self.screen.get_width()+10:
            self.rect.left = -25
            
        if self.rect.left < -self.rect.width:
            self.rect.left = self.screen.get_width() + 25
            
        if self.rect.top < 220 and self.speed[1] < 0:
            self.speed[1] = -self.speed[1]
            
        if self.rect.top > 550 and self.speed[1] > 0:
            self.speed[1] = -self.speed[1]
                   
        #更新时间计数
        self.updown_cur += 1
        self.changeimage_cur += 1
        
        #检查是否已到时间改变上下方向
        if self.updown_cur >= random.randint(540, 640):
            self.speed[1] = -self.speed[1]
            self.updown_cur = 0
            
        #检查是否已到时间更新动画
        if self.changeimage_cur >= self.changeimage_timer:
            if self.image == self.image_list[0]:
                self.image = self.image_list[1]
            else:
                self.image = self.image_list[0]
           
            self.changeimage_cur = 0
        
    