import pygame
import sys

class LoginPage:
    '''创建登录页面'''

    def __init__(self, hs_game):
        self.settings = hs_game.settings
        self.width = self.settings.login_width
        self.height = self.settings.login_height

        #渲染图片
        self.login_screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Log in')
        self.rect = self.login_screen.get_rect()
        self.color = self.settings.bg_color

        #插入文本
        self.text_color = (0, 135, 0)
        self.font = pygame.font.SysFont(None, 36)
        self.text = 'Your name: '

        #初始时文本框处于非活动状态
        self.active = False

    def check_events(self):
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
            elif event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        return False

    def draw_screen(self):
        '''绘制屏幕'''
        self.login_screen.fill(self.color)
        self.msg_image = self.font.render(self.text, True, self.text_color,
                self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.login_screen.blit(self.msg_image, self.msg_image_rect)

        pygame.display.flip()