#-*- coding: cp936 -*-
"""��������ģ�飬������������ı�������"""
import pygame
from pygame.locals import *

import random

class Fish(pygame.sprite.Sprite):
    """С����"""
    def __init__(self, image, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)#��ʼ���������
        
        #���徫������
        self.fish = image
        self.fish_turn = pygame.transform.flip(self.fish, True, False)
        self.image = self.fish
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #������������
        self.screen = screen
        self.turn_cur = 0
        
    def avoid(self, minepos):
        """һ��������������㿪ը��"""        
        if minepos[0] > self.rect.centerx:
            if not self.speed[0] > 1:
                self.speed[0] = -self.speed[0]
                self.image = self.fish_turn
        else:
            if not self.speed[0] < 1:
                self.speed[0] = -self.speed[0]    
                self.image = self.fish_turn
        
        self.rect = self.rect.move([self.speed[0]*25, self.speed[1]])
    
    def update(self):
        """һ�����������������λ�ã�
        ͬʱ������Ƿ���Ҫ��ͷ
        """  
        self.rect = self.rect.move(self.speed)
        self.turn_cur += 1
        
        #���λ���Ƿ�Խ��
        if self.rect.right > self.screen.get_width()-30 and self.speed[0] > 0:
            self.speed[0] = -self.speed[0]
            
        if self.rect.left < self.rect.width+30 and self.speed[0] < 0:
            self.speed[0] = -self.speed[0]
            
        #����Ƿ���Ҫ��ͷ
        if self.turn_cur >= random.randint(150, 250):
            self.speed[0] = -self.speed[0]
            self.turn_cur = 0
        
        #����ͼƬ����
        if self.speed[0] < 0:
            self.image = self.fish_turn
        
        else:
            self.image = self.fish

class Foliage(pygame.sprite.Sprite):
    """ˮ����"""
    def __init__(self, img_list, location, screen):
        pygame.sprite.Sprite.__init__(self)#��ʼ���������
        
        #���徫������
        self.img_list = img_list
        self.image = img_list[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
        #������������30
        self.screen = screen
        self.cur = 0
        self.end = 1
    
    def update(self):
        """һ��������������ˮ������"""
        self.cur += 0.1
        
        if int(self.cur) > self.end:
            self.cur = 0
            
        self.image = self.img_list[int(self.cur)]
        self.screen.blit(self.image, self.rect.topleft)
        
class Sky:
    """�����"""
    def __init__(self, skyimg, cloudimg, location, screen):
        #����ͼƬ����
        self.skyimg = skyimg
        self.cloudimg = cloudimg
        
        #������������
        self.location = location
        self.screen = screen
        self.scroll = 0
        
    def update(self):
        """һ�����������ػ���պ��Ƶ�ͼƬ��
        ͬʱ���ı��Ƶ�λ��
        """        
        #�ı��Ƶ�λ��
        self.scroll += 0.1
        if self.scroll > self.screen.get_width():
            self.scroll = 0
        
        #�ػ���պ���
        self.screen.blit(self.skyimg, self.location)
        self.screen.blit(self.cloudimg, [self.scroll, 100])
        self.screen.blit(self.cloudimg, [self.scroll - self.screen.get_width(), 100])
        
class Ocean:
    """������"""
    def __init__(self, waterimg, waveimg, location, screen):
        #����ͼƬ����
        self.waterimg = waterimg
        self.waveimg = waveimg
        
        #������������
        self.location = location
        self.screen = screen
        self.surf = pygame.surface.Surface((screen.get_width(),  \
                screen.get_height() - self.location[1]))
        self.surf.fill((255, 255, 255))
        self.scroll = 0
        
    def update(self):
        """һ�����������ػ溣ˮ�ͺ��˵�ͼƬ��
        ͬʱ������ˮ��������
        """                
        #����ˮ��������(�ı�ˮ��λ��)
        self.scroll += 1
        if self.scroll > self.screen.get_width():
            self.scroll = 0
        
        #�ػ溣ˮ�ͺ���
        self.surf.blit(self.waterimg, [0, 0])
        self.surf.blit(self.waveimg, [self.scroll, 0])
        self.surf.blit(self.waveimg, [self.scroll - self.waterimg.get_width(), 0])
        self.screen.blit(self.surf, self.location)
        
class Seabed:
    """������"""
    def __init__(self, location, size, colour, screen):
        #����ͼƬ����
        self.seabedimg = pygame.surface.Surface(size)
        self.seabedimg.fill(colour)
        
        #������������
        self.location = location
        self.screen = screen
    def update(self):
        """һ�����������ػ溣��ͼƬ"""
        self.screen.blit(self.seabedimg, self.location)
    
class Milieu:
    """���໷��������"""
    def __init__(self, img_dict, screen, beauty):
        #������������
        self.screen = screen
        self.sealevel = img_dict["sky"].get_rect().height#����߶�
        bedheight = 10
        self.bedlevel = screen.get_height() - bedheight#���׸߶�
        self.foliage_group = pygame.sprite.Group()
        self.fishs = pygame.sprite.Group()
        
        #����ʵ��
        self.sky_obj = Sky(img_dict["sky"], img_dict["cloud"], (0, 0), screen)
        self.ocean_obj = Ocean(img_dict["water"], img_dict["wave"], (0,self.sealevel), screen)
        self.seabed_obj = Seabed((0, self.bedlevel), (screen.get_width(), bedheight), (132, 82, 55), screen)
        
        if beauty:
            self.fishs.add(Fish(img_dict["fishs"][0],[1100,550],[3, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][0],[1000,580],[3, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][1],[900,600],[2, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][0],[300,530],[3, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][1],[400,540],[3, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][1],[320,515],[2, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][0],[200,500],[2, 0],screen))
            self.fishs.add(Fish(img_dict["fishs"][1],[100,580],[3, 0],screen))     
            
            for x in range(30):
                self.foliage_group.add(Foliage(img_dict["foliage"], (random.randint(x*40, x*50), self.bedlevel - 30), screen))
            
    def update(self):
        """һ�����������ػ滷��ͼƬ"""
        self.sky_obj.update()
        self.ocean_obj.update()
        self.seabed_obj.update()
        self.foliage_group.update()
        self.fishs.update()
        self.fishs.draw(self.screen)
        
