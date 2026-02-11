import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    '''显示得分信息的类'''

    def __init__(self, hs_game):
        '''初始化显示得分涉及的属性'''
        self.hs_game = hs_game
        self.screen = hs_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = hs_game.settings
        self.stats = hs_game.stats

        #显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #准备包含最高分，当前得分和hp的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_hp()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''将得分渲染为图像'''
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        #在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def check_high_score(self):
        '''检查是否诞生了新的最高分'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_high_score(self):
        '''将最高分渲染为图像'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = f'{high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
        
        #将最高分放在屏幕顶部的中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_hp(self):
        '''显示生命值'''
        hp_str = f'hp : {self.stats.hp}'
        self.hp_image = self.font.render(hp_str, True,
                self.text_color, self.settings.bg_color)
        
        #在屏幕左上方显示生命值
        self.hp_rect = self.hp_image.get_rect()
        self.hp_rect.left = 20
        self.hp_rect.top = 20

    def prep_level(self):
        '''将等级渲染为图像'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
        
        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''显示还余下多少艘飞船'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.hs_game, 1)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 50
            self.ships.add(ship)

    def show_score(self):
        '''在屏幕上显示得分，生命值，等级和余下的飞船数'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.hp_image, self.hp_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
