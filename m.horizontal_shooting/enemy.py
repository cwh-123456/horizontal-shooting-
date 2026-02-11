import pygame
from pygame.sprite import Sprite

from vector import Vector

class Enemy(Sprite):
    '''表示单个敌人的类'''

    def __init__(self, hs_game):
        '''初始化外星人并设置其起始位置'''
        super().__init__()
        self.screen = hs_game.screen
        self.settings = hs_game.settings

        #加载敌人图像并设置其rect属性
        self.image = pygame.image.load('image/ship.bmp')
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()

        #每个敌人最初都在屏幕的右上角附近
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.rect.height + 100

        #存储敌人的精确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.position = Vector([self.x, self.y])

    def check_edges(self):
        '''如果敌人位于屏幕边缘，就返回True'''
        screen_rect = self.screen.get_rect()
        return (self.rect.top < 100) or (self.rect.bottom > screen_rect.bottom)

    def update(self):
        '''向上或向下移动敌人'''
        self.y += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.y = self.y
