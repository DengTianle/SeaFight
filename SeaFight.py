#-*- coding: cp936 -*-
"""
SeaFight.py
邓天乐2014-2015年编写。

大海战1，
有关级和精致的用户界面。
"""

import sys
import os
try:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Lib'))
    sys.path.insert(0, libdir)
except:
    pass

import MainGame

#开始游戏
game = MainGame.Game()
