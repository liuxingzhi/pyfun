# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 01:12:35 2017

@author: Pistachio
"""
import pygame
import random
from sys import exit

class Plane:
    def __init__(self):
        image = pygame.image.load('xiaohei.jpg').convert_alpha()
        self.image = pygame.transform.scale(image, (60, 60))
        w, h = pygame.display.get_surface().get_size()
        self.x = w/2
        self.y = h/2

    def move(self):
        x, y = pygame.mouse.get_pos()
        self.x = x - self.image.get_width()/2
        self.y = y - self.image.get_height()/2

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def restart(self):
        self.x = 200
        self.y = 600

    def __str__(self):
        return "plane: x is {x}, y is {y}".format(x=self.x, y=self.y)


class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.jpg').convert_alpha()
        self.active = False

    def move(self):
        if self.active:
            self.y -= 3
        if self.y < 0:
            self.active = False

    def restart(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        self.active = True

    def show(self):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
        else:
            pass

    def __str__(self):
        return "x is {x}, y is {y}, active is {active}".format(x=self.x, y=self.y, active=self.active)


class Enemy:
    count = 1

    def __init__(self):
        self.x = 200
        self.y = -50
        image = pygame.image.load('huangshou.jpg').convert_alpha()
        self.image = pygame.transform.scale(image, (60, 60))
        self.speed = 0.3
        self.id = Enemy.count
        Enemy.count += 1

    def move(self):
        if self.y < 800:
            self.y += self.speed
        else:
            self.restart()

    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        # base speed is 0.1
        self.speed = random.random() + 0.1

    def __str__(self):
        return "x is {x}, y is {y}, id is {id}".format(x=self.x, y=self.y, id=self.id)


def check_hit(bullet, enemy):
    if (enemy.x <= bullet.x <= enemy.x + enemy.image.get_width()) and \
            (enemy.y <= bullet.y <= enemy.y + enemy.image.get_height()):
        enemy.restart()
        # print("hitted",enemy)
        bullet.active = False
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
pygame.display.set_caption("luoxiaoheidazuozhan")

image = pygame.image.load('luoxiaoheizhanji.jpg').convert()
background = pygame.transform.scale(image, (450, 800))

# plane = pygame.image.load('plane.jpg').convert_alpha()
enemies = []
for i in range(5):
    enemies.append(Enemy())
bullets = []
for i in range(5):
    bullets.append(Bullet())
    # print(bullets[i])
count_b = len(bullets)
index_b = 0
interval_b = 100
plane = Plane()
game_over = False
score = 0
font = pygame.font.Font(None, 32)
font_over = pygame.font.Font(None, 64)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_over and event.type == pygame.MOUSEBUTTONUP:
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            game_over = False

    screen.blit(background, (0, 0))

    if not game_over:
        interval_b -= 1
        if interval_b < 0:
            bullets[index_b].restart()
            interval_b = 100
            index_b = (index_b + 1) % count_b
        for b in bullets:
            if b.active:
                for e in enemies:
                    if check_hit(b, e):
                        score += 125
                b.move()
                b.show()
        for e in enemies:
            if check_crash(plane,e):
                game_over = True
            e.move()
            screen.blit(e.image, (e.x, e.y))
        plane.move()
        plane.show()
        # print(plane)
        text = font.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        screen.blit(text, (0, 0))

    else:
        # show score
        text = font_over.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        w, h = pygame.display.get_surface().get_size()
        screen.blit(text, (w/4, h/5))

    pygame.mouse.set_visible(False)
    pygame.display.update()

