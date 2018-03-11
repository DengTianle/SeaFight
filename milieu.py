#-*- coding: cp936 -*-
"""环境管理模块，用来创建程序的背景环境"""
import pygame
from pygame.locals import *

import random

class Fish(pygame.sprite.Sprite):
    """小鱼类"""
    def __init__(self, image, location, speed, screen):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        self.fish = image
        self.fish_turn = pygame.transform.flip(self.fish, True, False)
        self.image = self.fish
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #定义自身数据
        self.screen = screen
        self.turn_cur = 0
        
    def avoid(self, minepos):
        """一个方法用来让鱼躲开炸弹"""        
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
        """一个方法用来更新鱼的位置，
        同时还检查是否需要掉头
        """  
        self.rect = self.rect.move(self.speed)
        self.turn_cur += 1
        
        #检查位置是否越界
        if self.rect.right > self.screen.get_width()-30 and self.speed[0] > 0:
            self.speed[0] = -self.speed[0]
            
        if self.rect.left < self.rect.width+30 and self.speed[0] < 0:
            self.speed[0] = -self.speed[0]
            
        #检查是否需要掉头
        if self.turn_cur >= random.randint(150, 250):
            self.speed[0] = -self.speed[0]
            self.turn_cur = 0
        
        #改正图片方向
        if self.speed[0] < 0:
            self.image = self.fish_turn
        
        else:
            self.image = self.fish

class Foliage(pygame.sprite.Sprite):
    """水草类"""
    def __init__(self, img_list, location, screen):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        self.img_list = img_list
        self.image = img_list[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
        #定义自身数据30
        self.screen = screen
        self.cur = 0
        self.end = 1
    
    def update(self):
        """一个方法用来更新水草姿势"""
        self.cur += 0.1
        
        if int(self.cur) > self.end:
            self.cur = 0
            
        self.image = self.img_list[int(self.cur)]
        self.screen.blit(self.image, self.rect.topleft)
        
class Sky:
    """天空类"""
    def __init__(self, skyimg, cloudimg, location, screen):
        #定义图片变量
        self.skyimg = skyimg
        self.cloudimg = cloudimg
        
        #定义自身数据
        self.location = location
        self.screen = screen
        self.scroll = 0
        
    def update(self):
        """一个方法用来重绘天空和云的图片，
        同时还改变云的位置
        """        
        #改变云的位置
        self.scroll += 0.1
        if self.scroll > self.screen.get_width():
            self.scroll = 0
        
        #重绘天空和云
        self.screen.blit(self.skyimg, self.location)
        self.screen.blit(self.cloudimg, [self.scroll, 100])
        self.screen.blit(self.cloudimg, [self.scroll - self.screen.get_width(), 100])
        
class Ocean:
    """海洋类"""
    def __init__(self, waterimg, waveimg, location, screen):
        #定义图片变量
        self.waterimg = waterimg
        self.waveimg = waveimg
        
        #定义自身数据
        self.location = location
        self.screen = screen
        self.surf = pygame.surface.Surface((screen.get_width(),  \
                screen.get_height() - self.location[1]))
        self.surf.fill((255, 255, 255))
        self.scroll = 0
        
    def update(self):
        """一个方法用来重绘海水和海浪的图片，
        同时还制造水的流动感
        """                
        #制造水的流动感(改变水的位置)
        self.scroll += 1
        if self.scroll > self.screen.get_width():
            self.scroll = 0
        
        #重绘海水和海浪
        self.surf.blit(self.waterimg, [0, 0])
        self.surf.blit(self.waveimg, [self.scroll, 0])
        self.surf.blit(self.waveimg, [self.scroll - self.waterimg.get_width(), 0])
        self.screen.blit(self.surf, self.location)
        
class Seabed:
    """海底类"""
    def __init__(self, location, size, colour, screen):
        #定义图片变量
        self.seabedimg = pygame.surface.Surface(size)
        self.seabedimg.fill(colour)
        
        #定义自身数据
        self.location = location
        self.screen = screen
    def update(self):
        """一个方法用来重绘海底图片"""
        self.screen.blit(self.seabedimg, self.location)
    
class Milieu:
    """主类环境管理类"""
    def __init__(self, img_dict, screen, beauty):
        #定义自身数据
        self.screen = screen
        self.sealevel = img_dict["sky"].get_rect().height#海面高度
        bedheight = 10
        self.bedlevel = screen.get_height() - bedheight#海底高度
        self.foliage_group = pygame.sprite.Group()
        self.fishs = pygame.sprite.Group()
        
        #创造实例
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
        """一个方法用来重绘环境图片"""
        self.sky_obj.update()
        self.ocean_obj.update()
        self.seabed_obj.update()
        self.foliage_group.update()
        self.fishs.update()
        self.fishs.draw(self.screen)
        
