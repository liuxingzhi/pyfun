# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 01:12:35 2017

@author: Pistachio
"""
import pygame
import random
from sys import exit
import os

pygame.init()
screen = pygame.display.set_mode((450, 800), 0, 32)
game_name = "虫族入侵大作战"
pygame.display.set_caption(game_name)

font = pygame.font.Font('my_font.ttf', 32)
font_over = pygame.font.Font('my_font.ttf', 64)

os.chdir('imgs')

# background = pygame.transform.scale(pygame.image.load('罗小黑战记.jpg').convert(), (450, 800))
# my_plane_img = pygame.transform.scale(pygame.image.load('小黑.jpg').convert_alpha(), (60, 60))
# enemy_img = pygame.transform.scale(pygame.image.load('黄受.jpg').convert_alpha(), (60, 60))
background = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (450, 800))
my_plane_img = pygame.transform.scale(pygame.image.load('petwings.jpg').convert_alpha(), (60, 60))
enemy_img = pygame.transform.scale(pygame.image.load('octopus.jpg').convert_alpha(), (60, 60))
bullet_img = pygame.image.load('bullet.jpg').convert_alpha()
boss_bullet_img = pygame.image.load('blue_bullet.jpg').convert_alpha()
boss_img = pygame.transform.scale(pygame.image.load('bunblebee.jpg').convert_alpha(), (300, 200))
strong_enemy = pygame.transform.scale(pygame.image.load('owl.jpg').convert_alpha(), (85, 50))
win_img = pygame.transform.scale(pygame.image.load('win.jpg').convert_alpha(), (420, 280))
lose_img = pygame.image.load('lose.jpg').convert_alpha()

screen_width, screen_height = pygame.display.get_surface().get_size()


class Plane:
    def __init__(self):
        self.image = my_plane_img
        w, h = pygame.display.get_surface().get_size()
        self.x = w / 2
        self.y = h / 2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.level = 1
        self.gun = SingleFireGun()

    def move(self):
        x, y = pygame.mouse.get_pos()
        self.x = x - self.image.get_width() / 2
        self.y = y - self.image.get_height() / 2

    def restart(self):
        self.x = 200
        self.y = 600
        self.gun.reload_all()

    def fire(self):
        self.gun.fire()

    def upgrade(self):
        self.level += 1
        SingleStraightBullet.upgrade()
        if self.level == 2:
            self.gun = DoubleFireGun(initial_capacity=self.level + 1)
        if self.level == 3:
            pass
        elif self.level == 4:
            self.gun = TripleFireGun(initial_capacity=self.level + 1)
        elif self.level == 5:
            self.gun = QuadraFireGun(initial_capacity=self.level + 1)
            """武器快升满级就可以打boss了"""
            global enemies
            enemies.append(Boss())
        elif self.level == 6:
            self.gun = HexaFireGun(initial_capacity=self.level + 1)

    def reset(self):
        self.level = 1
        self.gun = SingleFireGun()

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return "plane: x is {x}, y is {y}".format(x=self.x, y=self.y)


class SingleFireGun:
    def __init__(self, initial_capacity=2):
        self.barrels = []

        """初始化子弹容量"""
        self.initial_capacity = initial_capacity
        self.current_bullet_capacity = 0
        for i in range(self.initial_capacity):
            self.increase_capacity()

    def show_fire(self):
        for bullets in self.barrels:
            for b in bullets:
                if b.active:
                    global enemies
                    for e in enemies:
                        if b.check_hit(e):
                            b.active = False
                            global score
                            score += 1
                    b.move()
                    b.show()

    def fire(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for bullets in self.barrels:
            flying = False
            for b in bullets:
                if b.active:
                    flying = True
            if not flying:
                for b in bullets:
                    b.restart(mouse_x, mouse_y)
                return

    """填充所有子弹，不论子弹状态"""

    def reload_all(self):
        for bullets in self.barrels:
            for b in bullets:
                b.active = False

    def upgrade(self):
        self.increase_capacity()

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        self.barrels.append((SingleStraightBullet(),))


class DoubleFireGun(SingleFireGun):
    def __init__(self, initial_capacity=3):
        SingleFireGun.__init__(self, initial_capacity=initial_capacity)

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        self.barrels.append((LeftStraightBullet(), RightStraightBullet()))


class TripleFireGun(SingleFireGun):
    def __init__(self, initial_capacity=4):
        SingleFireGun.__init__(self, initial_capacity=initial_capacity)

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        bullets_tuple = (LeftStraightBullet(), RightStraightBullet(), RightObliqueBullet())
        self.barrels.append(bullets_tuple)


class QuadraFireGun(SingleFireGun):
    def __init__(self, initial_capacity=5):
        SingleFireGun.__init__(self, initial_capacity=initial_capacity)

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        bullets_tuple = (LeftObliqueBullet(), LeftStraightBullet(), RightStraightBullet(), RightObliqueBullet())
        self.barrels.append(bullets_tuple)


class HexaFireGun(SingleFireGun):
    def __init__(self, initial_capacity=6):
        SingleFireGun.__init__(self, initial_capacity=initial_capacity)

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        bullets_tuple = (SecondLeftObliqueBullet(), LeftObliqueBullet(), LeftStraightBullet(), RightStraightBullet(),
                         RightObliqueBullet(), SecondRightObliqueBullet())
        self.barrels.append(bullets_tuple)


class BossGun():
    def __init__(self, initial_capacity=20, cd=500):
        self.cd = cd
        self.interval_b = cd
        self.initial_capacity = initial_capacity
        self.current_bullet_capacity = 0
        self.barrels = []
        for i in range(self.initial_capacity):
            self.increase_capacity()

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        self.barrels.append((BossBullet(), BossBullet(), BossBullet(), BossBullet(), BossBullet(), BossBullet()))

    def show_fire(self):
        for bullets in self.barrels:
            for b in bullets:
                if b.active:
                    global plane
                    if b.check_hit(plane):
                        b.active = False
                        global game_over, you_win
                        you_win = False
                        game_over = True
                    b.move()
                    b.show()

    def fire(self, x, y):
        self.interval_b -= 1
        if self.interval_b < 0:
            for bullets in self.barrels:
                flying = False
                for b in bullets:
                    if b.active:
                        flying = True
                if not flying:
                    bullets[0].restart(x, y, x_speed=-0.2, y_speed=-0.2)
                    bullets[1].restart(x, y, x_speed=-0.1, y_speed=-0.2)
                    bullets[2].restart(x, y, x_speed=0.0, y_speed=-0.2)
                    bullets[3].restart(x, y, x_speed=0.0, y_speed=-0.2)
                    bullets[4].restart(x, y, x_speed=0.1, y_speed=-0.2)
                    bullets[5].restart(x, y, x_speed=0.2, y_speed=-0.2)
                    self.interval_b = self.cd
                    return


class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.active = False
        self.image = None

    def move(self):
        pass

    def restart(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def check_hit(self, who):
        pass

    def show(self):
        if self.active:
            screen.blit(self.image, (self.x, self.y))


class SingleStraightBullet(Bullet):
    damage = 1

    def __init__(self):
        Bullet.__init__(self)
        self.image = bullet_img
        self.active = False

    def move(self):
        if self.active:
            self.y -= 2.5
        if self.y < 0:
            self.active = False

    def check_hit(self, enemy):
        if (enemy.x + 0 * enemy.width <= self.x <= enemy.x + 1 * enemy.width) and \
                (enemy.y <= self.y <= enemy.y + enemy.height):
            enemy.life -= self.damage
            if enemy.life <= 0:
                enemy.restart()
                global score, game_level
                score += enemy.score_reward * 0.8 * game_level
            return True
        return False

    @staticmethod
    def upgrade():
        SingleStraightBullet.damage *= 1.25

    @staticmethod
    def reset():
        SingleStraightBullet.damage = 1

    def __str__(self):
        return "x is {x}, y is {y}, active is {active}".format(x=self.x, y=self.y, active=self.active)


class LeftStraightBullet(SingleStraightBullet):
    def restart(self, x, y):
        self.x = x - 10
        self.y = y
        self.active = True


class RightStraightBullet(SingleStraightBullet):
    def restart(self, x, y):
        self.x = x + 10
        self.y = y
        self.active = True


class LeftObliqueBullet(LeftStraightBullet):
    def move(self):
        if self.active:
            self.y -= 2.2
            self.x -= 0.5
        if self.y < 0 or self.x < 0:
            self.active = False


class SecondLeftObliqueBullet(LeftStraightBullet):
    def move(self):
        if self.active:
            self.y -= 2.0
            self.x -= 0.75
        if self.y < 0 or self.x < 0:
            self.active = False


class RightObliqueBullet(RightStraightBullet):
    def move(self):
        if self.active:
            self.y -= 2.2
            self.x += 0.5
        if self.y < 0 or self.x > screen.get_width():
            self.active = False


class SecondRightObliqueBullet(RightStraightBullet):
    def move(self):
        if self.active:
            self.y -= 2.0
            self.x += 0.75
        if self.y < 0 or self.x < 0:
            self.active = False


class BossBullet(Bullet):
    def __init__(self):
        Bullet.__init__(self)
        self.image = boss_bullet_img
        self.x_speed = 0
        self.y_speed = 0
        self.active = False

    def restart(self, x, y, x_speed=0.1, y_speed=0.1):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.active = True

    def move(self):
        if self.active:
            self.y -= self.y_speed
            self.x -= self.x_speed
        if not (screen_height > self.y > 0 and screen_width > self.x > 0):
            self.active = False

    def check_hit(self, plane):
        if (plane.x + 0.1 * plane.width <= self.x <= plane.x + 0.9 * plane.width) and \
                (plane.y + 0.1 * plane.height <= self.y <= plane.y + 0.9 * plane.height):
            return True
        return False

    def __str__(self):
        return f"x:{self.x} y:{self.y} active:{self.active}"


class Enemy:
    count = 1
    life_max = 1
    base_speed = 0.2

    def __init__(self):
        self.score_reward = 100
        self.image = enemy_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 0
        self.y = 0
        self.y_speed = 0.2
        self.x_speed = 0.2
        self.life = Enemy.life_max
        self.id = Enemy.count
        self.restart()
        Enemy.count += 1

    def move(self):
        if self.y < 800:
            self.y += self.y_speed
        else:
            self.restart()

    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        # base speed is 0.3
        self.y_speed = random.random() + Enemy.base_speed
        self.x_speed = Enemy.base_speed
        self.life = Enemy.life_max

    @staticmethod
    def upgrade():
        Enemy.life_max *= 2

    @staticmethod
    def reset():
        Enemy.life_max = 2

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return "x is {x}, y is {y}, id is {id}".format(x=self.x, y=self.y, id=self.id)


class StrongEnemy(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.image = strong_enemy
        self.score_reward = 150
        self.change_direction_interval = 1000

    def move(self):
        self.change_direction_interval -= 1
        if self.change_direction_interval <= 1:
            self.change_direction_interval = 1000
            self.x_speed = -self.x_speed

        if self.y < 800:
            self.y += self.y_speed
            self.x += self.x_speed
        else:
            self.restart()


class Boss:
    def __init__(self):
        self.image = boss_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = 0
        self.x = 0.5 * screen_width - 0.5 * self.width
        self.score_reward = 15000
        self.life = 2000
        self.x_speed = 0.2
        self.y_speed = 0.2
        self.is_alife = True
        self.gun = BossGun(initial_capacity=10)

    def fire(self):
        self.gun.fire(self.x + self.image.get_width() / 2, self.y + self.height)

    def move(self):
        if self.y < 100:
            self.y += self.y_speed
        else:
            if self.x <= 0:
                self.x_speed = -self.x_speed
            elif self.x + self.width >= screen_width:
                self.x_speed = -self.x_speed
            self.x += self.x_speed

    def restart(self):
        self.is_alife = False
        self.height = 0
        self.width = 0

    def show(self):
        if self.is_alife:
            screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return "x is {x}, y is {y}, life left: {life}".format(x=self.x, y=self.y, life=self.life)


def check_crash(plane, enemy):
    if (plane.x + 0.7 * plane.image.get_width() > enemy.x) and (
            plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) and (
            plane.y + 0.7 * plane.image.get_height() > enemy.y) and (
            plane.y + 0.3 * plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False


enemies = []
# enemies.append(Boss())
for i in range(5):
    enemies.append(Enemy())

plane = Plane()
game_over = False
you_win = False
score = 0

threshold = 1000
game_level = 1
# control the frame rate
clock = pygame.time.Clock()
while True:
    plane_fired = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                plane_fired = True

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_over and event.type == pygame.MOUSEBUTTONUP:
            plane.restart()
            for e in enemies:
                e.restart()
            score = 0
            game_over = False
            you_win = False

            game_level = 1
            threshold = 1000
            plane.reset()
            Enemy.reset()
            SingleStraightBullet.reset()
            enemies = []
            for i in range(5):
                enemies.append(Enemy())

    screen.blit(background, (0, 0))

    if not game_over:
        if plane_fired:
            plane.fire()
        plane.gun.show_fire()
        for e in enemies:
            if check_crash(plane, e):
                game_over = True
            if isinstance(e, Boss):
                if e.is_alife:
                    e.fire()
                    e.gun.show_fire()
                else:
                    game_over = True
                    you_win = True
                    break
            e.move()
            e.show()
        plane.move()
        plane.show()
        score = int(score)
        text = font.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        screen.blit(text, (0, 0))
        if score >= threshold:
            threshold *= 2
            Enemy.upgrade()
            enemies.append(StrongEnemy())
            plane.upgrade()
            game_level += 1
        clock.tick(250)

    elif you_win:
        w, h = pygame.display.get_surface().get_size()
        screen.blit(win_img, (w / 2 - win_img.get_width() / 2, h / 4))
        score = int(score)
        text_score = font_over.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        score_text_length = text_score.get_width()
        screen.blit(text_score, (w / 2 - score_text_length / 2, h / 6))

        for e in enemies:
            if e.life > 0:
                if check_crash(plane, e):
                    game_over = True
                    you_win = False
                e.show()
            if isinstance(e, Boss):
                e.gun.show_fire()
        if plane_fired:
            plane.fire()
        plane.gun.show_fire()
        plane.move()
        plane.show()

    else:
        # show score
        w, h = pygame.display.get_surface().get_size()
        screen.blit(lose_img, (w / 2 - lose_img.get_width() / 2, h / 3.5))
        score = int(score)
        text_score = font_over.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        score_text_length = text_score.get_width()
        screen.blit(text_score, (w / 2 - score_text_length / 2, h / 6))

    pygame.mouse.set_visible(False)
    pygame.display.update()
