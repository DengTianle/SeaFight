# -*- coding: cp936 -*-
"""一个模块用来导入各种文件。"""

import os
import pygame
from pygame.locals import *

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, "..", "Data"))

def load(filename, mode = "rb"):
    """一个函数用来导入文件"""
    return open(os.path.join(data_dir, filename), mode)

def load_image(filename, colorkey = False):
    """一个函数用来导入图像给程序"""
    img = pygame.image.load(os.path.join(data_dir, filename))
      
    if not colorkey == False:
        img.set_alpha(None)
        img.set_colorkey(colorkey)
        
    return img

def load_sound(filename, volume):
    """一个函数用来导入声效给程序"""
    sound = pygame.mixer.Sound(os.path.join(data_dir, filename))
    sound.set_volume(volume)
    return sound

def load_music(filename, volume, repeat):
    """一个函数用来导入背景音乐给程序"""
    #tmp = 'ambient.mp3'#os.path.join(data_dir, filename)
    music = pygame.mixer.music.load(os.path.join(data_dir, filename))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(repeat)
