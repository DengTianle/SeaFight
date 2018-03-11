# -*- coding: cp936 -*-
"""�������Ƕ���ģ�飬���������������ƶ���ս��"""
import pygame
from pygame.locals import *

class Warship(pygame.sprite.Sprite):
    """����ս����"""
    def __init__(self, image, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)#��ʼ���������
        
        #���徫������
        self.image = image       
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #������������
        self.screen = screen
        self.lives = 3
        
    def draw(self):
        """һ��������������ս��"""
        self.screen.blit(self.image, self.rect)
        
    def update(self,dir):
        """һ��������������ս����λ�ã�
        ͬʱ�����λ���Ƿ�Խ�� 
        """        
        self.rect = self.rect.move([self.speed[0]*dir, self.speed[1]])
        
        #���λ���Ƿ�Խ��
        if self.rect.left < 0:
            self.rect.left = 0  
            
        if self.rect.left > self.screen.get_width()-self.rect.width:
            self.rect.left = self.screen.get_width()-self.rect.width
