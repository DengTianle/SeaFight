#-*- coding: cp936 -*-
"""
SeaFight.py
������2014-2015���д��

��ս1��
�йؼ��;��µ��û����档
"""

import sys
import os
try:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Lib'))
    sys.path.insert(0, libdir)
except:
    pass

import MainGame

#��ʼ��Ϸ
game = MainGame.Game()
