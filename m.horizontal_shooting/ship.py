import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''管理飞船的类'''

    def __init__(self, hs_game, id = None):
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.screen = hs_game.screen
        self.settings = hs_game.settings
        self.screen_rect = hs_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('image/ship.bmp')
        self.image = pygame.transform.rotate(self.image,270)
        if id:
            self.image = pygame.transform.scale(self.image,
                    (int(self.image.get_width() * 0.7),
                     int(self.image.get_height() * 0.7)))
        self.rect = self.image.get_rect()

        #每艘新飞船都放在屏幕左边界的中央
        self.rect.left = 0
        self.rect.centery = self.screen_rect.centery + 50

        #在飞船的属性x, y中存储一个浮点数
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #移动标志（飞船一开始不移动）
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''根据移动标志调整飞船的位置'''
        if self.moving_up and self.rect.top > 100:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        '''将飞船放在屏幕左侧的中央'''
        self.rect.left = 0
        self.rect.centery = self.screen_rect.centery + 50
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

        