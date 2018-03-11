# -*- coding: cp936 -*-
"""程序主角定义模块，用来创建可左右移动的战舰"""
import pygame
from pygame.locals import *

class Warship(pygame.sprite.Sprite):
    """主角战舰类"""
    def __init__(self, image, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        self.image = image       
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #定义自身数据
        self.screen = screen
        self.lives = 3
        
    def draw(self):
        """一个方法用来画出战舰"""
        self.screen.blit(self.image, self.rect)
        
    def update(self,dir):
        """一个方法用来更新战舰的位置，
        同时还检查位置是否越界 
        """        
        self.rect = self.rect.move([self.speed[0]*dir, self.speed[1]])
        
        #检查位置是否越界
        if self.rect.left < 0:
            self.rect.left = 0  
            
        if self.rect.left > self.screen.get_width()-self.rect.width:
            self.rect.left = self.screen.get_width()-self.rect.width
