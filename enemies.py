# -*- coding: cp936 -*-
"""һ��ģ����������ս���Ŀ��ƶ����ˡ�"""
import pygame
from pygame.locals import *

import random

class Submarine(pygame.sprite.Sprite):
    """����Ǳͧ��"""
    def __init__(self, image, location, speed, shoot_timer, screen):
        pygame.sprite.Sprite.__init__(self)#��ʼ���������
        
        #���徫������
        if speed[0] < 0: 
            self.image = pygame.transform.flip(image, True, False)
        else: 
            self.image = image            
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #������������
        self.screen = screen
        self.shoot = False
        self.shoot_cur = 0
        self.shoot_timer = shoot_timer
        self.turn_cur = 0 
        self.find_cur = 0
        
    def update(self):
        """һ��������������Ǳͧ��λ�ã�
        ͬʱ������������ʱ���Ƿ��ѵ�
        """        
        self.rect = self.rect.move(self.speed)
        self.shoot = False
        
        #���λ���Ƿ�Խ��
        if self.rect.right > (self.screen.get_width() + 100):
            self.kill()
            
        if self.rect.left < -(self.rect.width+100):
            self.kill()
        
        #����ʱ�����
        self.shoot_cur+= 1
        self.turn_cur += 1
        
        #����Ƿ��ѵ�ʱ�䷢������
        if self.shoot_cur >= random.randint(self.shoot_timer-15, self.shoot_timer+15):
            self.shoot = True
            self.shoot_cur = 0
        
        #����Ƿ��ѵ�ʱ��ı䷽��
        if self.turn_cur >= random.randint(290, 440):
            self.speed[0] = -self.speed[0]
            self.turn_cur = 0
        
    def find_warship(self, warship_pos, timer):
        #����ʱ�����
        self.find_cur += 1
        
        #����Ƿ��ѵ�ʱ��׷��ս��
        if self.find_cur >= timer:
            if warship_pos[0] > self.rect.right:
                if not self.speed[0] > 0:
                    self.speed[0] = -self.speed[0]
                    
            elif warship_pos[0] < self.rect.left:
                if not self.speed[0] < 0:
                    self.speed[0] = -self.speed[0]
                    
            self.find_cur = 0
        
class Diver(pygame.sprite.Sprite):
    """����ǱˮԱ��"""
    def __init__(self, images, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)#��ʼ���������
        
        #���徫������
        if speed[0] < 0: 
            self.image_list = [pygame.transform.flip(images[0], True, False),   \
                    pygame.transform.flip(images[1], True, False)]
        else: 
            self.image_list = images
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #������������
        self.screen = screen
        self.updown_cur = 0
        self.changeimage_cur = 0
        self.changeimage_timer = 12
        
    def update(self):
        """һ��������������ǱˮԱ��λ�ã�
        ͬʱ�����ı����·����ʱ���Ƿ��ѵ�
        """                        
        self.rect = self.rect.move(self.speed)
        
        #���λ���Ƿ�Խ��
        if self.rect.right > self.screen.get_width()+10:
            self.rect.left = -25
            
        if self.rect.left < -self.rect.width:
            self.rect.left = self.screen.get_width() + 25
            
        if self.rect.top < 220 and self.speed[1] < 0:
            self.speed[1] = -self.speed[1]
            
        if self.rect.top > 550 and self.speed[1] > 0:
            self.speed[1] = -self.speed[1]
                   
        #����ʱ�����
        self.updown_cur += 1
        self.changeimage_cur += 1
        
        #����Ƿ��ѵ�ʱ��ı����·���
        if self.updown_cur >= random.randint(540, 640):
            self.speed[1] = -self.speed[1]
            self.updown_cur = 0
            
        #����Ƿ��ѵ�ʱ����¶���
        if self.changeimage_cur >= self.changeimage_timer:
            if self.image == self.image_list[0]:
                self.image = self.image_list[1]
            else:
                self.image = self.image_list[0]
           
            self.changeimage_cur = 0
        
    