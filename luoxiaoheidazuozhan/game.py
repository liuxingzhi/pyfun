# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 01:12:35 2017

@author: Pistachio
"""
import pygame
import random
from sys import exit
import os

os.chdir('imgs')
my_plane_img = '小黑.jpg'
background_img = '罗小黑战记.jpg'
enemy_img = '黄受.jpg'
bullet_img = 'bullet.jpg'
game_name = "罗小黑大作战"
boss_img = "boss.jpg"


class Plane:
    def __init__(self):
        image = pygame.image.load(my_plane_img).convert_alpha()
        self.image = pygame.transform.scale(image, (60, 60))
        w, h = pygame.display.get_surface().get_size()
        self.x = w / 2
        self.y = h / 2
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
        self.gun.upgrade()
        if self.level == 3:
            self.gun = DoubleFireGun()
        elif self.level == 5:
            self.gun = TripleFireGun()
        elif self.level >= 7:
            self.gun = QuaterFireGun()

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return "plane: x is {x}, y is {y}".format(x=self.x, y=self.y)


class SingleFireGun:
    def __init__(self):
        """子弹冷却时间"""
        self.cd = 150
        self.interval_b = self.cd
        self.barrels = []

        """初始化子弹容量"""
        self.initial_capacity = 1
        self.bullet_capacity = 0
        for i in range(self.initial_capacity):
            self.increase_capacity()

    def fire(self):
        self.reload()
        for bullets in self.barrels:
            for b in bullets:
                if b.active:
                    global enemies
                    for e in enemies:
                        if check_hit(b, e):
                            b.active = False
                            global score
                            score += 1
                    b.move()
                    b.show()

    def upgrade(self):
        self.cd -= 1
        self.increase_capacity()

    def reload(self):
        self.interval_b -= 1
        if self.interval_b < 0:
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

    def reload_all(self):
        for bullet in self.barrels:
            bullet.active = False

    def increase_capacity(self):
        self.bullet_capacity += 1
        self.barrels.append((SingleStraightBullet(),))


class DoubleFireGun(SingleFireGun):
    def __init__(self):
        SingleFireGun.__init__(self)
        self.initial_capacity = 2

    def increase_capacity(self):
        self.bullet_capacity += 1
        self.barrels.append((LeftStraightBullet(), RightStraightBullet()))


class TripleFireGun(SingleFireGun):
    def __init__(self):
        SingleFireGun.__init__(self)
        self.initial_capacity = 3

    def increase_capacity(self):
        self.bullet_capacity += 1
        bullets_tuple = (LeftStraightBullet(), RightStraightBullet(), RightObliqueBullet())
        self.barrels.append(bullets_tuple)


class QuaterFireGun(SingleFireGun):
    def __init__(self):
        SingleFireGun.__init__(self)
        self.initial_capacity = 4

    def increase_capacity(self):
        self.bullet_capacity += 1
        bullets_tuple = (LeftObliqueBullet(), LeftStraightBullet(), RightStraightBullet(), RightObliqueBullet())
        self.barrels.append(bullets_tuple)


class SingleStraightBullet:
    def __init__(self):
        self.x = 300
        self.y = 600
        self.image = pygame.image.load(bullet_img).convert_alpha()
        self.active = False

    def move(self):
        if self.active:
            self.y -= 2.5
        if self.y < 0:
            self.active = False

    def restart(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def upgrade(self):
        pass

    def show(self):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
        else:
            pass

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


class RightObliqueBullet(RightStraightBullet):
    def move(self):
        if self.active:
            self.y -= 2.2
            self.x += 0.5
        if self.y < 0 or self.x > screen.get_width():
            self.active = False


class Enemy:
    count = 1
    life = 2
    base_speed = 0.0

    def __init__(self):
        image = pygame.image.load(enemy_img).convert_alpha()
        self.image = pygame.transform.scale(image, (60, 60))
        self.x = 0
        self.y = 0
        self.speed = 0.3
        self.life = Enemy.life
        self.id = Enemy.count
        self.restart()
        Enemy.count += 1

    def move(self):
        if self.y < 800:
            self.y += self.speed
        else:
            self.restart()

    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        # base speed is 0.3
        self.speed = random.random() + Enemy.base_speed
        self.life = Enemy.life

    @staticmethod
    def upgrade():
        Enemy.life *= 2

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return "x is {x}, y is {y}, id is {id}".format(x=self.x, y=self.y, id=self.id)


def check_hit(bullet, enemy):
    if (enemy.x <= bullet.x <= enemy.x + enemy.image.get_width()) and \
            (enemy.y <= bullet.y <= enemy.y + enemy.image.get_height()):
        enemy.life -= 1
        if enemy.life <= 0:
            enemy.restart()
            global score, level
            score += 100 * 0.8 * level
        return True
    return False


def check_crash(plane, enemy):
    if (plane.x + 0.7 * plane.image.get_width() > enemy.x) and (
            plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) and (
            plane.y + 0.7 * plane.image.get_height() > enemy.y) and (
            plane.y + 0.3 * plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False


pygame.init()
screen = pygame.display.set_mode((450, 800), 0, 32)
pygame.display.set_caption(game_name)

image = pygame.image.load(background_img).convert()
background = pygame.transform.scale(image, (450, 800))

enemies = []
for i in range(5):
    enemies.append(Enemy())

plane = Plane()
game_over = False
score = 0
font = pygame.font.Font(None, 32)
font_over = pygame.font.Font(None, 64)

threshold = 1000
level = 1
# control the frame rate
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_over and event.type == pygame.MOUSEBUTTONUP:
            plane.restart()
            for e in enemies:
                e.restart()
            score = 0
            game_over = False

    screen.blit(background, (0, 0))

    if not game_over:
        plane.fire()
        for e in enemies:
            if check_crash(plane, e):
                game_over = True
            e.move()
            e.show()
        plane.move()
        plane.show()
        # print(plane)
        text = font.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        screen.blit(text, (0, 0))
        if score >= threshold:
            threshold *= 2
            Enemy.upgrade()
            enemies.append(Enemy())
            plane.upgrade()
            level += 1
        clock.tick(250)

    else:
        # show score
        text = font_over.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        w, h = pygame.display.get_surface().get_size()
        screen.blit(text, (w / 4, h / 5))

    pygame.mouse.set_visible(False)
    pygame.display.update()
