import pygame
from pygame.sprite import Sprite

from enemy import Enemy

class Bullet(Sprite):
    '''管理飞船发射子弹的类'''

    #id为1表示是玩家发射的，为2,3,4表示是敌人发射的
    #id2为0表示向左上方发射，为1表示向左下方发射
    def __init__(self, hs_game, id, enemy = None, id2 = None):
        '''在飞船的当前位置创建一个子弹对象'''
        super().__init__()
        self.screen = hs_game.screen
        self.settings = hs_game.settings
        self.id = id
        self.id2 = id2
        match self.id:
            case 1:
                self.color = self.settings.bullet_color
            case 2:
                self.color = self.settings.bullet_color1
            case 3:
                self.color = self.settings.bullet_color2
            case 4:
                self.color = self.settings.bullet_color3

        #在(0,0)处创建一个表示子弹的矩形，再设置其正确位置
        if self.id == 1:
            self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                    self.settings.bullet_height)
            self.rect.midleft = hs_game.ship.rect.midright
        else:
            self.rect = pygame.Rect(0, 0, self.settings.bullet_width1,
                    self.settings.bullet_height1)
            self.rect.midright = enemy.rect.midleft

        #存储用浮点数表示的子弹位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        '''移动子弹'''
        #更新子弹的准确位置
        match self.id:
            case 1:
                self.x += self.settings.bullet_speed
            case 2:
                self.x -= self.settings.bullet_speed1
            case _:
                self.x -= self.settings.bullet_speed2
                if self.id2 == 1:
                    self.y += self.settings.bullet_speed2
                elif self.id2 == 0:
                    self.y -= self.settings.bullet_speed2
        #更新表示子弹的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen, self.color, self.rect)