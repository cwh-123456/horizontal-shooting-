import csv

class GameStats:
    '''跟踪游戏的统计信息'''

    def __init__(self, hs_game):
        '''初始化统计信息'''
        self.settings = hs_game.settings
        self.reset_stats()

        #在任何情况下都不应重置最高分
        self.high_score = 0
        with open('users.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == hs_game.login.text:
                    self.high_score = int(row['highest score'])

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left = self.settings.ship_limit
        self.hp = 100
        self.score = 0
        self.level = 1