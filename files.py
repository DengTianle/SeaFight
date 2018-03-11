# -*- coding: cp936 -*-
"""һ��ģ��������������ļ���"""

import os
import pygame
from pygame.locals import *

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, "..", "Data"))

def load(filename, mode = "rb"):
    """һ���������������ļ�"""
    return open(os.path.join(data_dir, filename), mode)

def load_image(filename, colorkey = False):
    """һ��������������ͼ�������"""
    img = pygame.image.load(os.path.join(data_dir, filename))
      
    if not colorkey == False:
        img.set_alpha(None)
        img.set_colorkey(colorkey)
        
    return img

def load_sound(filename, volume):
    """һ����������������Ч������"""
    sound = pygame.mixer.Sound(os.path.join(data_dir, filename))
    sound.set_volume(volume)
    return sound

def load_music(filename, volume, repeat):
    """һ�������������뱳�����ָ�����"""
    #tmp = 'ambient.mp3'#os.path.join(data_dir, filename)
    music = pygame.mixer.music.load(os.path.join(data_dir, filename))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(repeat)
