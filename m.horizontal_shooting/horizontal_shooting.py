import pygame
import sys
from time import sleep
import csv

from settings import Settings
from login_page import LoginPage
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from vector import Vector

class HorizontalShooting:
    '''管理游戏资源和行为的类'''
    
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #页面标号，1为登录页面，2为主页面
        self.current_screen = 1
        #登录页面
        self.login = LoginPage(self)

        self.log_in()

    def log_in(self):
        '''登录操作'''
        while True:
            if self.login.check_events():
                self.login.text = self.login.text.replace('Your name: ', '')

                self.current_screen = 2
                break

            self.login.draw_screen()
            self.clock.tick(60)


    def create_main_page(self):
        '''创建主页面'''
        #主页面
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption('Horizontal Shooting')

        #主页面
        #创建存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.bullets1 = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        #self.bullets3 = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self._create_fleet()

        self._last_time = pygame.time.get_ticks()

        #游戏启动后处于非活动状态
        self.game_active = False
        self.pause = False
        self.difficulty_chosen = False

        #创建Play按钮
        self.play_button = Button(self, 'Play', 0)
        #创建难度按钮
        self.easy_button = Button(self, 'Easy', 1)
        self.normal_button = Button(self, 'Normal', 2)
        self.difficult_button = Button(self, 'Difficult', 3)

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_events()
            
            if self.game_active and not self.pause:
                self.ship.update()
                self._enemy_bullet()
                self._update_bullets()
                self._update_enemies()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._update_file()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''在玩家单击Play按钮时开始新游戏'''
        if (self.play_button.rect.collidepoint(mouse_pos) 
                and not self.game_active and self.difficulty_chosen):
            #还原游戏设置
            self.settings.initialize_dynamic_settings()

            #重置游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_hp()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            #清空敌人列表和子弹列表
            self.enemies.empty()
            self.bullets.empty()
            self.bullets1.empty()
            #self.bullets3.empty()

            #创建一个新的舰队，并将飞船放在屏幕左侧的中央
            self._create_fleet()
            self.ship.center_ship()

            #隐藏光标
            pygame.mouse.set_visible(False)
        elif (self.easy_button.rect.collidepoint(mouse_pos)
                and not self.game_active and not self.difficulty_chosen):
            self.settings.speedup_scale = 1.05
            self.settings.score_scale = 1.2
            self.difficulty_chosen = True
        elif (self.normal_button.rect.collidepoint(mouse_pos)
                and not self.game_active and not self.difficulty_chosen):
            self.difficulty_chosen = True
        elif (self.difficult_button.rect.collidepoint(mouse_pos)
                and not self.game_active and not self.difficulty_chosen):
            self.settings.speedup_scale = 1.2
            self.settings.score_scale = 2.0
            self.difficulty_chosen = True

    def _check_keydown_events(self, event):
        '''响应按下'''
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.pause = not self.pause
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        '''响应释放'''
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''创建一颗子弹，并将其加入编组bullets'''
        #玩家子弹
        new_bullet = Bullet(self, 1)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''更新子弹的位置并删除已消失的子弹'''
        #更新子弹的位置
        self.bullets.update()
        self.bullets1.update()
        self.bullets2.update()
        #self.bullets3.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width:
                self.bullets.remove(bullet)
        for bullet1 in self.bullets1.copy():
            if bullet1.rect.left < 0:
                self.bullets1.remove(bullet1)
        for bullet2 in self.bullets2.copy():
            if (bullet2.rect.left < 0 or bullet2.rect.top < 100 
                    or bullet2.rect.bottom > self.settings.screen_height):
                self.bullets2.remove(bullet2)
        #for bullet3 in self.bullets3.copy():
        #    if (bullet3.rect.left < 0 or bullet3.rect.top < 0 
        #            or bullet3.rect.bottom > self.settings.screen_height):
        #        self.bullets3.remove(bullet3)

        self._check_bullet_enemy_collisions()
        self._check_bullets_collisions()

    def _check_bullet_enemy_collisions(self):
        '''响应子弹和敌人的碰撞'''
        #检查是否有子弹击中了敌人，如果是，就删除相应的子弹和敌人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.enemies, True, True
        )

        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemies)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.enemies:
            #删除现有子弹并创建一个新的舰队
            self.bullets.empty()
            self.bullets1.empty()
            self.bullets2.empty()
            #self.bullets3.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _check_bullets_collisions(self):
        '''响应玩家子弹与敌人子弹的碰撞'''
        _ = pygame.sprite.groupcollide(
            self.bullets, self.bullets1, False, True
        )
        _ = pygame.sprite.groupcollide(
            self.bullets, self.bullets2, False, True
        )
        #_ = pygame.sprite.groupcollide(
            #self.bullets, self.bullets3, False, True
        #)

    def _create_fleet(self):
        '''创建一个舰队'''
        #创建一个敌人，再不断添加，直到没有空间添加敌人为止
        #敌人的间距为敌人的高度和敌人的宽度
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size

        current_y, current_x = (enemy_height + 100, 
                                self.settings.screen_width - enemy_width)
        for _ in range(0, 3):
            while current_y < (self.settings.screen_height - 2 * enemy_height):
                self._create_enemy(current_y, current_x)
                current_y += 3 * enemy_height

            #添加一列敌人后，重置current_y的值并递减current_x的值
            current_y = enemy_height + 100
            current_x -= 3 * enemy_width

    def _create_enemy(self, y_position, x_position):
        '''创建一个敌人并把它放入舰队中'''
        new_enemy = Enemy(self)
        new_enemy.y = y_position
        new_enemy.x = x_position
        new_enemy.rect.y = y_position
        new_enemy.rect.x = x_position
        self.enemies.add(new_enemy)

    def _check_fleet_edges(self):
        '''在有敌人到达边缘时采取相应的措施'''
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整个舰队向左移动，并改变它们的方向'''
        for enemy in self.enemies.sprites():
            enemy.rect.x -= self.settings.fleet_left_speed
        self.settings.fleet_direction *= -1

    def _update_enemies(self):
        '''检查是否有敌人位于屏幕边缘，并更新敌人的位置'''
        self._check_fleet_edges()
        self.enemies.update()
        self._ship_hit()

        for enemy in self.enemies.copy():
            if enemy.rect.right < 0:
                enemy.kill()

    def _ship_hit(self):
        '''响应飞船与敌人、敌人子弹的碰撞'''
        #检测敌人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.enemies):
            self.stats.hp = 0
            self.sb.prep_hp()
            self._ship_lose()

        #检测敌人子弹与飞船之间的碰撞
        if pygame.sprite.spritecollide(self.ship, self.bullets1, True):
            self.stats.hp -= self.settings.bullet_power1
            self.sb.prep_hp()
        if pygame.sprite.spritecollide(self.ship, self.bullets2, True):
            self.stats.hp -= self.settings.bullet_power2
            self.sb.prep_hp()
        #if pygame.sprite.spritecollide(self.ship, self.bullets3, True):
            #self.stats.hp -= self.settings.bullet_power3
        if self.stats.hp <= 0:
            self._ship_lose()

    def _ship_lose(self):
        '''飞船生命值为0'''
        #清空敌人和子弹列表
        self.enemies.empty()
        self.bullets.empty()
        self.bullets1.empty()
        self.bullets2.empty()
        #self.bullets3.empty()

        #创建一个新的舰队，并将飞船放在屏幕左侧的中央
        self._create_fleet()
        self.ship.center_ship()

        if self.stats.ships_left > 1:
            #减少飞船可用量，并初始化生命值
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.stats.hp = 100
            self.sb.prep_hp()

            #暂停
            sleep(0.5)
        else:
            self.game_active = False
            self.difficulty_chosen = False
            self._update_file()
            pygame.mouse.set_visible(True)

    def _enemy_bullet(self):
        '''创建敌人子弹，并分别加入编组'''
        #子弹每秒发射一次
        if pygame.time.get_ticks() - self._last_time >= 1000:
            self._last_time = pygame.time.get_ticks()
            #敌人子弹
            for enemy in self.enemies.sprites():
                new_bullet1 = Bullet(self, 2, enemy)
                self.bullets1.add(new_bullet1)
                new_bullet21 = Bullet(self, 3, enemy, 0)
                self.bullets2.add(new_bullet21)
                new_bullet22 = Bullet(self, 3, enemy, 1)
                self.bullets2.add(new_bullet22)
                #new_bullet3 = Bullet(self, 4, enemy)
                #self.bullets3.add(new_bullet3)

    def _update_file(self):
        '''更新文件'''
        rows = []
        with open('users.csv', 'r') as file:
            reader = csv.DictReader(file)
            isin = False
            for row in reader:
                if row['name'] == self.login.text:
                    row['highest score'] = self.stats.high_score
                    rows.append(row)
                    isin = True
            if not isin:
                rows.append({'name' : self.login.text,
                             'highest score' : self.stats.high_score})
        
        with open('users.csv', 'w', newline = '') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet1 in self.bullets1.sprites():
            bullet1.draw_bullet()
        for bullet2 in self.bullets2.sprites():
            bullet2.draw_bullet()
        #for bullet3 in self.bullets3.sprites():
            #bullet3.draw_bullet()
        self.ship.blitme()
        self.enemies.draw(self.screen)

        #显示得分
        self.sb.show_score()

        #绘制按钮
        if not self.difficulty_chosen:
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.difficult_button.draw_button()
        elif not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    hs = HorizontalShooting()
    if hs.current_screen == 2:
        hs.create_main_page()
        hs.run_game()