#-*- coding: cp936 -*-
"""游戏主模块，
整个游戏的主控制都在这里。
"""

import sys
import random
import math

import pygame
from pygame.locals import *

import warship
import enemies
import milieu
import files
import catch_coin

class MessageBox:
    """信息盒类"""
    def __init__(self, title, msgs, screen):
        self.surf = pygame.surface.Surface((screen.get_width()/2, screen.get_height()/2))
        self.msgs = []
        font = pygame.font.SysFont("KaiTi", 20)
        self.fntH = font.get_height()
        for msg in msgs:
            self.msgs.append(font.render(msg, True, (255, 255, 255)))
        w = self.surf.get_width()
        h = self.surf.get_height()
        x = screen.get_width()/2 - w/2 
        y = screen.get_height()/2 - h/2
        self.surf.fill((0,0,0))
        self.surf.set_alpha(100)
        screen.blit(self.surf, (x, y))
        x = x + 20
        y = y + 60
        for i in xrange(len(self.msgs)):
            w = self.msgs[i].get_width()
            screen.blit(self.msgs[i], (screen.get_width()/2-w/2, y + self.fntH*i))

        tmp = font.render(u"按[Enter]键继续。", True, (0, 255, 0))
        screen.blit(tmp, (screen.get_width()/2-tmp.get_width()/2,screen.get_height()/2+h/2-(2*self.fntH)))
        tmp = font.render(u"按[Esc]键退出。", True, (0, 255, 0))
        screen.blit(tmp, (screen.get_width()/2-tmp.get_width()/2,screen.get_height()/2+h/2-self.fntH))
        screen.blit(title, (screen.get_width()/2-title.get_width()/2, screen.get_height()/2-h/2))
        pygame.display.flip()                

    def show(self):
        done = False
        while not(done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    elif event.key == K_RETURN:
                        done = True

class Mine(pygame.sprite.Sprite):
    """深水炸弹类"""
    def __init__(self, image, location, speed):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #定义自身数据
        self.swing_cur = 0
        self.swing_timer = 5
        
    def update(self):
        """一个方法用来更新深水炸弹的位置，
        同时还检查摇摆的时间是否已到
        """                
        self.rect = self.rect.move(self.speed)
        
        #更新时间计数
        self.swing_cur += 1
        
        #检查是否已到时间摇摆
        if self.swing_cur >= self.swing_timer:
            self.speed[0] = -self.speed[0]
            self.swing_cur = 0
            
class Torpedo(pygame.sprite.Sprite):
    """鱼雷类"""
    def __init__(self, image, location, speed, advanced):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        
        #定义自身数据
        self.swing_cur = 0
        
        #调整图片至正确角度
        if advanced:
            self.rotate_img(self.speed)
            #self.advanced = True
        #else:self.advanced=False
            
    def rotate_img(self, vel):
        """一个方法用来调整鱼雷图片
        至正确角度
        """         
        img = self.image
        self.image = pygame.transform.rotate(self.image, 360-math.atan(vel[0]/vel[1]*-1)*180.0/math.pi)
        
    def update(self):
        """一个方法用来更新鱼雷的位置，
        同时还不断增加速度来模仿加速度
        """                
        self.rect = self.rect.move(self.speed)

        #增加速度
        self.speed[1] -= 0.1
        
class Supermine(Mine):
    """子类救命弹类"""
    def __init__(self, image, location, speed):
        Mine.__init__(self, image, location, speed)#初始化深水炸弹基类
        
        #定义自身数据
        self.boom = False
        self.boom_cur = 0
        self.boom_timer = 50
        
    def tick_boom(self):
        """一个方法用来检查自爆的时间是否已到"""
        self.boom_cur += 1
        
        #检查是否已到时间自爆
        if self.boom_cur >= self.boom_timer:
            self.boom = True
            
class Boom(pygame.sprite.Sprite):
    """爆炸类"""
    def __init__(self, img_list, type, obj_rect):
        pygame.sprite.Sprite.__init__(self)#初始化精灵基类
        
        #定义精灵属性
        self.img_list = img_list
        self.image = img_list[0]
        
        self.rect = self.image.get_rect()
        self.rect.center = obj_rect.center
        
        #定义基本变量
        self.type = type
        self.cur = 0
        
        #判断爆炸类型
        if self.type == 'c':
            self.end = 3
        elif self.type == 's':
            self.end = 6
            self.rect.top -= 13

    def update(self):
        """一个方法用来更新爆炸动画"""
        self.cur += 0.2
        
        #检查动画是否已完成
        if self.cur < self.end:
            self.image = self.img_list[int(self.cur)]
        else:
            self.kill()
            
class Game:
    """主类游戏类"""
    def __init__(self):
        self.init_pygame()
        self.init_timer()
        self.load_files()
        self.set_level(0)
        self.prepare_objs()
        self.run()
        
    def init_pygame(self):
        """一个方法用来初始化pygame"""
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1400, 646))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("")#"Sea fight")
        pygame.key.set_repeat(150, 100)
        pygame.mouse.set_visible(False)
        self.full_screen = False
        
    def init_timer(self):
        """一个方法用来初始化计时器及相关事项"""
        self.timer_rect=Rect(0,15,400,30)
        self.timer_rect.centerx=self.screen.get_rect().centerx
        self.timertube_linewidth=3
        self.timertube_rect = Rect(0,0,self.timer_rect.width+self.timertube_linewidth*2,   \
                                self.timer_rect.height+self.timertube_linewidth*2)
        self.timertube_rect.center = self.timer_rect.center

    def load_files(self):
        """一个方法用来导入各种文件"""
        #导入图片
        self.ico = pygame.surface.Surface((32, 32))#files.load_image("SeaFight_ship.png")
        self.ico.set_alpha(255)
        self.msgtitle_image = files.load_image("name_title.png")
        self.icons_image = files.load_image("icons.png")
        
        self.sky_image = files.load_image("sky.jpg")    
        self.cloud_image = files.load_image("cloud.png")
        self.water_image = files.load_image("ocean.jpg")
        self.wave_image = files.load_image("waves.png")
        
        self.fish1_image = files.load_image("fish1.png")
        self.fish2_image = files.load_image("fish2.png")
        self.foliage1_image = files.load_image("grass1.png")
        self.foliage2_image = files.load_image("grass2.png")
        
        self.hero_image  = files.load_image("warship.png")
        self.livehero_image = files.load_image("livewarship.png")
        
        self.sub_image = files.load_image("sub.png")
        self.diver1_image = files.load_image("diver1.png")
        self.diver2_image = files.load_image("diver2.png")
        
        self.mine_image = files.load_image("mine.png")
        self.torpedo_image = files.load_image("torpedo.png")
        self.supermine_image = files.load_image("supermine.png")
        
        splash_image0 = files.load_image("splash0.png")
        splash_image1 = files.load_image("splash1.png")
        splash_image2 = files.load_image("splash2.png")
        splash_image3 = files.load_image("splash3.png")
        splash_image4 = files.load_image("splash4.png")
        splash_image5 = files.load_image("splash5.png")
        splash_image6 = files.load_image("splash6.png")        
        sboom_image1 = files.load_image("boom1.png")#小规模爆炸1
        sboom_image2 = files.load_image("boom2.png")#小规模爆炸2
        sboom_image3 = files.load_image("boom3.png")#小规模爆炸3       
        mboom_image1 = pygame.transform.scale(sboom_image1, [100, 70])#中等规模爆炸1
        mboom_image2 = pygame.transform.scale(sboom_image2, [100, 70])#中等规模爆炸2
        mboom_image3 = pygame.transform.scale(sboom_image3, [100, 70])#中等规模爆炸3
        self.bboom_image = pygame.transform.scale(sboom_image1, [220, 100])#大规模爆炸1(战舰爆炸)
        
        self.splash_images = [splash_image0, splash_image1, splash_image2, splash_image3,   \
                        splash_image4, splash_image5, splash_image6]        
        self.sboom_images = [sboom_image1, sboom_image2, sboom_image3]
        self.mboom_images = [mboom_image1, mboom_image2, mboom_image3]
        
        #导入声音
        files.load_music('ambient.wav',0.4,-1)
        
        self.warn_sound = files.load_sound('warning.wav', 0.3)
        self.boom_sound=files.load_sound('boom.wav',0.5)
        self.splash_sound=files.load_sound('splash.wav',0.4)
        self.hitland_sound=files.load_sound('hithard.wav',0.3)        
        self.hitdiver_sound=files.load_sound('ping.wav',0.5)       
        self.boomdiver_sound=files.load_sound('death.wav',0.5)
        
    def set_level(self, level):
        """一个方法用来设定关级及相关属性"""
        self.level = level
        
        #设定分数
        if self.level == 0:
            self.score = 0
        
        #设定加分机会
        if self.level == 0:
            self.chance_cur = 0
            self.chance_require = 300        
        
        #设定游戏时间
        self.total_cur = (self.level+1)*30
        self.total_secondcur = 0
        self.total_timer = (self.level+1)*30
        
        #设定升级要求
        self.hit_subs = 0
        self.hit_divers = 0
        self.uplevel = {"subs" : 1+self.level*2, "divers" : 0}
        if self.level >= 2:
            self.uplevel["divers"] = self.level - 1
        
        #设定炸弹数量
        self.mine_number = 25 + self.level*5
        self.supermine_number =(self.level + 1)*10
        
        #设定潜艇的能力
        self.subs_timer = {"shoot" : 30*8 - self.level*20, "find" : 5*30 - self.level*10}
        if 30*5 - self.level*10 <= 2*30:
            self.subs_timer["shoot"] = 2*30
        if 6*30 - self.level*10 <= 3*30:
            self.subs_timer["find"] = 3* 30
        
        #设定添加实例的时间
        self.add_cur = 0
        if self.level < 2:
            self.add_timer = 20*30 - self.level*20
        else:
            self.add_timer = 7*30 - self.level*15
        if 7*30 - self.level*15 < 3*30:
            self.add_timer = 3*30
        
        #设定游戏高级程度
        if self.level >= 2:
            self.beauty = True
        else:
            self.beauty = False
        
        if self.level >= 4:
            self.diver_relive = True
        else:
            self.diver_relive= False
        
        #设定加分标准
        self.add_scores = {"hit sub":20, "hit diver":10, "boom diver":-100}
        
        #设定各种文字提醒
        self.level_msgs1 = []
        if self.level == 0:
            self.level_msgs1 = [u"第%s关" % str(self.level)] 
            self.level_msgs1.append(u"投掷深水炸弹(按[空格]键)去炸潜艇")
            self.level_msgs1.append(u"炸中一艘潜艇可加%s分" % str(self.add_scores["hit sub"]))
            self.level_msgs1.append(u"按回车键可投掷救命弹")
            self.level_msgs1.append(u"升级要求:炸%s艘潜艇" % str(self.uplevel["subs"]))       
            
        elif self.level == 2:
            self.level_msgs1 = [u"第%s关" % str(self.level)] 
            self.level_msgs1.append(u"从本关级开始增加了潜水员,救援一个")
            self.level_msgs1.append(u"潜水员可加%s分，误炸" % str(self.add_scores["hit diver"]))
            self.level_msgs1.append(u"一个潜水员扣%s分" % str(self.add_scores["boom diver"]*-1))  
            self.level_msgs1.append(u"升级要求:炸%s艘潜艇" % str(self.uplevel["subs"]))
            self.level_msgs1.append(u"并救%s名潜水员" % str(self.uplevel["divers"]))
            
        elif self.level > 2:
            self.level_msgs1 = [u"第%s关" % str(self.level)] 
            self.level_msgs1.append(u"升级要求:炸%s艘潜艇" % str(self.uplevel["subs"]))
            self.level_msgs1.append(u"并救%s名潜水员" % str(self.uplevel["divers"]))
            
        else:
            self.level_msgs1 = [u"第%s关" % str(self.level)] 
            self.level_msgs1.append(u"升级要求:炸%s艘潜艇" % str(self.uplevel["subs"]))
        self.level_msgs1.append(u"升级方式:按[Ctrl]键")
               
    def prepare_objs(self):
        """一个方法用来准备精灵组、实例及字体"""
        self.clock = pygame.time.Clock()
        
        #准备精灵组
        self.mines = pygame.sprite.Group()#此精灵组包括救命弹
        self.torpedoes = pygame.sprite.Group()
        self.supermines = pygame.sprite.Group()
        self.submarines = pygame.sprite.Group()
        self.fishs = pygame.sprite.Group()
        self.divers = pygame.sprite.Group()
        self.booms = pygame.sprite.Group()
        
        #准备时间实例
        self.clock = pygame.time.Clock()
        
        #准备字体
        self.font = pygame.font.SysFont("KaiTi", 15)
        
        #准备实例
        self.milieu_images = {"sky" : self.sky_image, "cloud" : self.cloud_image,   \
                "water" : self.water_image, "wave" : self.wave_image,   \
                "fishs" : [self.fish1_image, self.fish2_image], "foliage" :    \
                [self.foliage1_image, self.foliage2_image]}  
        self.milieu = milieu.Milieu(self.milieu_images, self.screen, self.beauty)
        
        self.hero = warship.Warship(self.hero_image, [150, self.milieu.sealevel-   \
                self.hero_image.get_rect().height+15], [40, 0], self.screen)
        
        #添加初始实例
        screen = self.screen
        self.submarines.add(enemies.Submarine(self.sub_image, [200,350], [3, 0], self.subs_timer["shoot"], screen))
        self.submarines.add(enemies.Submarine(self.sub_image, [600,450], [2, 0], self.subs_timer["shoot"], screen))
        self.submarines.add(enemies.Submarine(self.sub_image, [750,380], [3, 0], self.subs_timer["shoot"], screen))
        if self.level >= 3:
            self.divers.add(enemies.Diver([self.diver1_image, self.diver2_image], [100, 300], [3, -1], screen))
            self.divers.add(enemies.Diver([self.diver1_image, self.diver2_image], [234, 430], [4, -1], screen))
            self.divers.add(enemies.Diver([self.diver1_image, self.diver2_image], [120, 380], [2, -2], screen))
            self.divers.add(enemies.Diver([self.diver1_image, self.diver2_image], [400, 470], [3.5, -2.5], screen))
            
    def game_over(self, type):
        """一个方法用来处理游戏结束时的事项"""
        if type == "timeout":
            msg = MessageBox(self.msgtitle_image, [u"游戏结束", u"时间到！"], self.screen)
            msg.show()
        else:
            msg = MessageBox(self.msgtitle_image, [u"游戏结束", u"舰队被炸毁！"], self.screen)
            msg.show()
        
        self.set_level(self.level)
        self.prepare_objs()
        self.init_timer()
        pygame.display.update(self.display())
        msg = MessageBox(self.msgtitle_image, self.level_msgs1, self.screen)
        msg.show()
    
    def addscore(self, score):
        """一个方法用来加分"""
        self.score += score
        self.chance_cur += score
        
    def update(self):
        """一个方法用来刷新各精灵"""
        self.submarines.update()
        self.mines.update()
        self.torpedoes.update()
        self.divers.update()  
        self.booms.update()
        for obj in self.supermines:
            obj.tick_boom()
        
        #潜艇找战舰
        if self.level >= 3:
            for obj in self.submarines:
                obj.find_warship(self.hero.rect.topleft, self.subs_timer["find"])
        
        #更新规定时间的时间计数
        self.total_secondcur += 1
        
        if self.total_secondcur >= 30:
            self.total_cur -= 1
            self.total_secondcur = 0
        
        #如果时间少于10秒就报警
        if self.total_cur <= 10:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(100)
                self.warn_sound.play()
            else:
                if not(pygame.mixer.music.get_busy()):
                    pygame.mixer.music.play(False)
       
    def display(self):
        """一个方法用来画出各精灵及其他组件"""
        self.milieu.update()#环境管理实例的update方法会自动画图
        self.hero.draw()
       
        self.submarines.draw(self.screen)
        self.mines.draw(self.screen)
        self.torpedoes.draw(self.screen)
        self.divers.draw(self.screen) 
        self.booms.draw(self.screen)
        
        #画出信息板
        self.screen.blit(self.icons_image, [5, 5])
        self.screen.blit(self.font.render(str(self.level), 1, (0, 0, 0)), [40, 8])
        self.screen.blit(self.font.render(str(self.score), 1, (0, 0, 0)), [40, 29])
        self.screen.blit(self.font.render(str(self.mine_number), 1, (0, 0, 0)), [40, 53])
        self.screen.blit(self.font.render(str(self.supermine_number/10), 1, (0, 0, 0)), [40, 78])
        self.screen.blit(self.font.render(str(self.hit_subs), 1, (0, 0, 0)), [40, 105])
        self.screen.blit(self.font.render(str(self.hit_divers), 1, (0, 0, 0)), [40, 125])
        
        #显示时间状态栏
        if not self.total_cur <= 0:
            pygame.draw.rect(self.screen, (247, 247, 150), [self.timer_rect.left, self.timer_rect.top  \
                    , float(self.timer_rect.width)/self.total_timer*self.total_cur, self.timer_rect.height], 0)
        pygame.draw.rect(self.screen, (0, 0, 0), self.timertube_rect, self.timertube_linewidth)
        
        tmp = u"剩余时间:%s分钟%s秒" % (str(self.total_cur/60),str(self.total_cur%60))    
        tmptext = self.font.render(tmp, 1, (0, 0, 0))
        tmprect = tmptext.get_rect()
        tmprect.center = self.timertube_rect.center
        tmprect.centery += self.timertube_rect.height        
        self.screen.blit(tmptext, tmprect)
        
        #显示还有几条命(用livewarship)
        for i in range(1, self.hero.lives):
            tmp = self.screen.get_width()-100*i
            tmp -= i*4
            self.screen.blit(self.livehero_image, [tmp, 20])
        
        pygame.display.update()
        
    def collide(self):
        """一个方法用来检测各精灵间的碰撞"""
        
        #检测船与鱼雷的碰撞
        warship_list = pygame.sprite.spritecollide(self.hero, self.torpedoes, 1)
        if len(warship_list) > 0:
            self.boom_sound.set_volume(0.2)
            for i in range(15):
                self.boom_sound.play()
            self.hero.lives -= 1
            rect = self.bboom_image.get_rect()
            rect.center = self.hero.rect.center
            self.hero.rect.topleft = [150, self.milieu.sealevel-self.hero.rect.height+15]
            pygame.display.update(self.screen.blit(self.bboom_image, rect))
            pygame.time.delay(1000)
        
        #检测船与潜水员的碰撞
        diverlist = pygame.sprite.spritecollide(self.hero, self.divers, 1)
        for diverobj in diverlist:
            self.hitdiver_sound.play()          
            self.addscore(self.add_scores["hit diver"])
            self.hit_divers += 1
            
            if self.diver_relive and self.score >= 300:
                if random.choice([0, 1]) == 1:
                    diver_speed = [random.choice([3, 3.5, 4]), random.choice([-1, -2, -2.5])]
                    location = [-100, random.randint(self.milieu.sealevel+100, self.screen.get_height()-50)]
                    self.divers.add(enemies.Diver([self.diver1_image, self.diver2_image], location,     \
                            diver_speed, self.screen))  
            
        #检测潜艇与深水炸弹(包括救命弹)的碰撞
        sub_dict = pygame.sprite.groupcollide(self.submarines, self.mines, 1, 1)
        for subobj in sub_dict.keys():
            self.boom_sound.set_volume(0.4)
            self.boom_sound.play()
            self.booms.add(Boom(self.mboom_images, "c", subobj.rect))
            
            self.addscore(self.add_scores["hit sub"])
            self.hit_subs += 1
            if self.hit_subs%4 == 0:
                self.mine_number += 1
                    
        #检测鱼雷与深水炸弹的碰撞
        torpedo_dict = pygame.sprite.groupcollide(self.mines, self.torpedoes, 1, 1)
        for t in torpedo_dict.keys():
            self.boom_sound.set_volume(0.4)
            self.boom_sound.play()
            self.booms.add(Boom(self.sboom_images, "c", t.rect))
        
        #检测潜水员与深水炸弹的碰撞
        diver_dict = pygame.sprite.groupcollide(self.divers, self.mines, 1, 1)
        for diverobj in diver_dict.keys():
            self.booms.add(Boom(self.sboom_images, "c", diverobj.rect))
            self.addscore(self.add_scores["boom diver"])
            self.boomdiver_sound.play()
            
        #检测小鱼与深水炸弹的碰撞  
        fish_dict = pygame.sprite.groupcollide(self.milieu.fishs, self.mines, 0, 0)
        for fishobj in fish_dict.keys():
            fishobj.avoid(fish_dict[fishobj][0].rect.topleft)
        
        #检测两种炸弹的位置是否越界
        for mineobj in self.mines:
            if mineobj.rect.top >= self.milieu.bedlevel-mineobj.rect.height:
                self.hitland_sound.play()
                mineobj.kill()
        
        for tobj in self.torpedoes:
            if tobj.rect.top <= self.milieu.sealevel:
                self.splash_sound.play()
                self.booms.add(Boom(self.splash_images, "s", tobj.rect))
                tobj.kill()
                
    def gen_objs(self):
        """一个方法用来生成精灵及检测精灵发出的信息"""
        self.add_cur += 1
        if self.add_cur >= random.randint(self.add_timer-10, self.add_timer+10):
            xlist = [-2, -3, -3.5, 2, 3, 3.5]
            sub_ylist = [0, 0]
            diver_ylist = [-1, -2, -2.5]
            sub_speed = [random.choice(xlist), random.choice(sub_ylist)]
            diver_speed = [random.choice(xlist), random.choice(diver_ylist)]
            sealevel = self.milieu.sealevel        
            
            #选择生成精灵的属性
            if self.level == 0:
                list = ["sub"]
            elif self.level == 1:
                list = ["sub"]
            elif self.level == 2 or self.level == 3:
                list = ["diver", "sub", "sub"]
            elif self.level >= 4:
                list = ["diver", "sub"]
            random_type = random.choice(list)
            
            #设定生成精灵的位置
            if random_type == "sub":   
                if sub_speed[0] < 0:
                    location = [self.screen.get_width(), random.randint(sealevel+100, self.screen.get_height()-50)]
                else:
                    location = [-100, random.randint(sealevel+100, self.screen.get_height()-50)]
            elif random_type == "diver":               
                if diver_speed[0] < 0:
                    location = [self.screen.get_width(), random.randint(sealevel+100, self.screen.get_height()-50)]
                else:
                    location = [-25, random.randint(sealevel+100, self.screen.get_height()-50)]
            
            #生成精灵  
            if random_type == "sub":
                self.submarines.add(enemies.Submarine(self.sub_image, location, sub_speed,  \
                        self.subs_timer["shoot"], self.screen))
                
            elif random_type == "diver":
                self.divers.add(enemies.Diver([self.diver1_image, self.diver2_image], location,     \
                        diver_speed, self.screen))
                
            self.add_cur = 0
            
        #检测精灵发出的信息
        for obj in self.submarines:
            if obj.shoot:
                if self.beauty: 
                    vel = [random.choice([-2.0, -1.5, 0, 0, 1.5, 2.0]), -3]
                    #img = pygame.transform.rotate(self.torpedo_image, 360-math.atan(vel[0]/vel[1]*-1)*180.0/math.pi)
                else: 
                    vel = [0, -3]
                
                img = self.torpedo_image                    
                self.torpedoes.add(Torpedo(img, [obj.rect.centerx, obj.rect.bottom], vel, self.beauty))
                
        #检查救命弹是否已自爆
        for obj in self.supermines:
            if obj.boom:
                self.booms.add(Boom(self.sboom_images, "c", obj.rect))
                self.boom_sound.set_volume(0.1)
                self.boom_sound.play()
                obj.kill()
                
    def run(self):
        """一个方法用来运行主窗口循环"""
        pygame.display.set_icon(self.ico)
        pygame.display.update(self.milieu.update())
        msg = MessageBox(self.msgtitle_image, ["", u"开始游戏"], self.screen)
        msg.show()
        pygame.display.update(self.milieu.update())
        msg = MessageBox(self.msgtitle_image, self.level_msgs1, self.screen)
        msg.show()    
                
        while True:
            self.clock.tick(30)          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        msg = MessageBox(self.msgtitle_image, ["", "", u"暂时休战"], self.screen)
                        msg.show()
                        
                    elif event.key == pygame.K_RIGHT:
                        self.hero.update(1)
                        
                    elif event.key == pygame.K_LEFT:
                        self.hero.update(-1)
                
                    elif event.key == pygame.K_SPACE:
                        if not self.mine_number <= 0:
                            mineobj = Mine(self.mine_image, [self.hero.rect.centerx, self.hero.rect.bottom], [1, 3])
                            self.mines.add(mineobj)
                            self.mine_number -= 1
                                         
                    elif event.key == pygame.K_RETURN:
                        if not self.supermine_number <= 0:
                            w = self.mine_image.get_rect().width
                            for i in range(0, w*10, w):
                                supermine_obj = Supermine(self.supermine_image,[self.hero.rect.left+i,   \
                                        self.hero.rect.bottom], [1, 3] )
                                self.mines.add(supermine_obj)
                                self.supermines.add(supermine_obj)
                                self.supermine_number -= 1
                    
                    elif event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                        if self.hit_subs >= self.uplevel["subs"] and self.hit_divers >= self.uplevel["divers"]:
                            msg = MessageBox(self.msgtitle_image, [u"恭喜", u"您已成功过关！"], self.screen)
                            msg.show()
                            pygame.display.update(self.display())
                            self.set_level(self.level+1)
                            self.prepare_objs()
                            if not(pygame.mixer.music.get_busy()):
                                files.load_music('ambient.mp3',0.4,-1)
                            msg = MessageBox(self.msgtitle_image, self.level_msgs1, self.screen)
                            msg.show()
                        else:
                            msgs = ["", u"还要炸%s艘潜艇" % str(self.uplevel["subs"] - self.hit_subs)]
                            if self.beauty and self.hit_divers >= 0:
                                msgs.append(u"并救%s名潜水员" % str(self.uplevel["divers"]-self.hit_divers))
                            msg = MessageBox(self.msgtitle_image, msgs, self.screen)    
                            msg.show()
                            
                    elif event.key==pygame.K_f:
                        if self.full_screen:
                            self.screen=pygame.display.set_mode((1400,646))
                            self.full_screen = False
                        else:
                            self.full_screen = True
                            self.screen=pygame.display.set_mode([1400,646],FULLSCREEN)
                            
                        self.display()
                
            self.gen_objs()
            self.update()
            self.collide()
            self.display()
            
            if self.hero.lives <= 0:
                self.game_over("liveout")
            if self.total_cur <= 0:
                self.game_over("timeout")
                
            if self.chance_cur >= self.chance_require:
                msgs = [u"恭喜", u"你现在有一个加分机会", u"通过移动鼠标移动木篓",  \
                       u"用木篓接住一个金币可加1分"]
                msg = MessageBox(self.msgtitle_image, msgs, self.screen)
                msg.show()
                w = self.screen.get_width()/2
                h = self.screen.get_height()/2+100
                catch_obj = catch_coin.Main(pygame.surface.Surface((w, h)), self.screen)
                self.score += catch_obj.catch_coins
                files.load_music('ambient.mp3',0.4,-1)
                self.chance_cur = 0
                self.chance_require = self.score*2 - 100
                
                
            