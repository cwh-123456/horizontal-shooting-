class Settings:
    '''存储游戏《横向射击》中所有设置的类'''

    def __init__(self):
        '''初始化游戏的静态设置'''
        #屏幕设置
        self.bg_color = (230, 230, 230)
        #登录页面
        self.login_width = 1200
        self.login_height = 900
        #主页面
        self.screen_width = 1200
        self.screen_height = 900

        #飞船的设置
        self.ship_limit = 3

        #玩家子弹的设置
        self.bullet_width = 15
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)

        #敌人子弹的设置
        self.bullet_width1 = 3
        self.bullet_height1 = 3
        self.bullet_color1 = (60, 60, 60)
        self.bullet_color2 = (255, 155, 0)
        self.bullet_color3 = (230, 0, 0)
        self.bullet_power1 = 10
        self.bullet_power2 = 20
        self.bullet_power3 = 30

        #敌人设置
        self.fleet_left_speed = 5.0

        #难度：正常
        #以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        #敌人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.bullet_speed1 = 2.0
        self.bullet_speed2 = 1.0
        self.enemy_speed = 0.5
        self.enemy_points = 50

        #fleet_direction为1表示向下运动，为-1表示向上运动
        self.fleet_direction = 1

    def increase_speed(self):
        '''提高可变设置的值'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bullet_speed1 *= self.speedup_scale
        self.bullet_speed2 *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)