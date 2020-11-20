# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 01:12:35 2017

@author: Pistachio
"""
import pygame
import random
from sys import exit
import os
from typing import Union

pygame.init()
SCREEN_SIZE = (450, 800)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
game_name = "虫族入侵大作战"
pygame.display.set_caption(game_name)

font = pygame.font.Font('my_font.ttf', 32)
font_over = pygame.font.Font('my_font.ttf', 64)

os.chdir('imgs')

# background = pygame.transform.scale(pygame.image.load('罗小黑战记.jpg').convert(), SCREEN_SIZE)
# my_plane_img = pygame.transform.scale(pygame.image.load('小黑.jpg').convert_alpha(), (60, 60))
# enemy_img = pygame.transform.scale(pygame.image.load('黄受.jpg').convert_alpha(), (60, 60))
background = pygame.transform.scale(pygame.image.load('background.jpg').convert(), SCREEN_SIZE)
my_plane_img = pygame.transform.scale(pygame.image.load('petwings.jpg').convert_alpha(), (60, 60))
enemy_img = pygame.transform.scale(pygame.image.load('octopus.jpg').convert_alpha(), (60, 60))
user_bullet_img = pygame.image.load('bullet.jpg').convert_alpha()  # size is (4,11)
boss_bullet_img = pygame.image.load('blue_bullet.jpg').convert_alpha()  # size is (22,22)
boss_img = pygame.transform.scale(pygame.image.load('bunblebee.jpg').convert_alpha(), (300, 200))
strong_enemy = pygame.transform.scale(pygame.image.load('owl.jpg').convert_alpha(), (85, 50))
win_img = pygame.transform.scale(pygame.image.load('win.jpg').convert_alpha(), (420, 280))
lose_img = pygame.image.load('lose.jpg').convert_alpha()

screen_width, screen_height = pygame.display.get_surface().get_size()


class DisplayableObject:
    image_object = None

    @property
    def image(self):
        return type(self).image_object

    @property
    def width(self):
        return type(self).image_object.get_width()

    @property
    def height(self):
        return type(self).image_object.get_height()


class MovingObject:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self):
        pass


def check_collision(user_plane: Union[MovingObject, DisplayableObject],
                    enemy: Union[MovingObject, DisplayableObject], scale_factor=0.7) -> bool:
    return (user_plane.x + scale_factor * user_plane.width > enemy.x) and \
           (user_plane.x + (1 - scale_factor) * user_plane.width < enemy.x + enemy.width) and \
           (user_plane.y + scale_factor * user_plane.height > enemy.y) and \
           (user_plane.y + (1 - scale_factor) * user_plane.height < enemy.y + enemy.height)


class Plane(DisplayableObject, MovingObject):
    image_object = my_plane_img

    def __init__(self):
        super(Plane, self).__init__()
        w, h = pygame.display.get_surface().get_size()
        self.x = w / 2
        self.y = h / 2
        self.level = 1
        self.gun = SingleFireGun(initial_capacity=self.level + 1)

    def move(self):
        x, y = pygame.mouse.get_pos()
        self.x = x - self.width / 2
        self.y = y - self.height / 2

    def restart(self):
        self.x = 200
        self.y = 600
        self.gun.reload()

    def fire(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.gun.fire(mouse_x, mouse_y)

    def upgrade(self):
        self.level += 1
        UserBullet.upgrade()
        if self.level == 2:
            self.gun = DoubleFireGun(initial_capacity=self.level + 1)
        elif self.level == 3:
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
        self.gun = SingleFireGun(initial_capacity=self.level + 1)

    def show(self):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return f"{type(self).__name__} position: ({self.x}, {self.y})"


class GunInterface:
    def show_active_bullets(self):
        pass

    def check_fired_bullets_hit_enemy(self):
        pass

    def fire(self, position_x, position_y):
        pass

    def increase_capacity(self):
        pass

    def upgrade(self):
        pass

    def reload(self):
        pass


class UserGun(GunInterface):
    def __init__(self, initial_capacity):
        self.barrels = []
        """初始化子弹容量"""
        self.current_bullet_capacity = 0
        for _ in range(initial_capacity):
            self.increase_capacity()

    def show_active_bullets(self):
        for bullets in self.barrels:
            for b in bullets:
                if b.active:
                    b.move()
                    b.show()

    def check_fired_bullets_hit_enemy(self):
        for bullets in self.barrels:
            for b in bullets:
                if b.active:
                    global enemies
                    for e in enemies:
                        if b.try_hit(e):
                            break

    def fire(self, position_x, position_y):
        for bullets in self.barrels:
            at_least_one_flying = False
            for b in bullets:
                if b.active:
                    at_least_one_flying = True
            if not at_least_one_flying:
                for b in bullets:
                    b.restart(position_x, position_y)
                return

    def reload(self):
        """填充所有子弹，不论子弹状态"""
        for bullets in self.barrels:
            for b in bullets:
                b.active = False

    def upgrade(self):
        self.increase_capacity()

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        self._append_bullets()

    def _append_bullets(self):
        pass


class SingleFireGun(UserGun):
    def _append_bullets(self):
        self.barrels.append((SingleStraightBullet(),))


class DoubleFireGun(SingleFireGun):
    def _append_bullets(self):
        self.barrels.append((LeftStraightBullet(), RightStraightBullet()))


class TripleFireGun(SingleFireGun):
    def _append_bullets(self):
        bullets_tuple = (LeftStraightBullet(), RightStraightBullet(), RightObliqueBullet())
        self.barrels.append(bullets_tuple)


class QuadraFireGun(SingleFireGun):
    def _append_bullets(self):
        bullets_tuple = (LeftObliqueBullet(), LeftStraightBullet(), RightStraightBullet(), RightObliqueBullet())
        self.barrels.append(bullets_tuple)


class HexaFireGun(SingleFireGun):
    def _append_bullets(self):
        bullets_tuple = (SecondLeftObliqueBullet(), LeftObliqueBullet(), LeftStraightBullet(), RightStraightBullet(),
                         RightObliqueBullet(), SecondRightObliqueBullet())
        self.barrels.append(bullets_tuple)


class BossGun(GunInterface):
    def __init__(self, initial_capacity=20, cd=210):
        self.cd = cd
        self.interval_b = cd
        self.initial_capacity = initial_capacity
        self.current_bullet_capacity = 0
        self.barrels = []
        for _ in range(self.initial_capacity):
            self.increase_capacity()

    def show_active_bullets(self):
        for bullets in self.barrels:
            for b in bullets:
                if b.active:
                    b.move()
                    b.show()

    def check_fired_bullets_hit_enemy(self):
        self.interval_b -= 1
        if self.interval_b < 0:
            for bullets in self.barrels:
                for b in bullets:
                    if b.active:
                        global plane
                        if b.try_hit(plane):
                            return

    def fire(self, x, y):
        self.interval_b -= 1
        if self.interval_b < 0:
            for bullets in self.barrels:
                at_least_one_flying = False
                for b in bullets:
                    if b.active:
                        at_least_one_flying = True
                if not at_least_one_flying:
                    bullets[0].restart(x, y, x_speed=-0.8, y_speed=-0.8)
                    bullets[1].restart(x, y, x_speed=-0.4, y_speed=-0.8)
                    bullets[2].restart(x, y, x_speed=0.0, y_speed=-0.8)
                    bullets[3].restart(x, y, x_speed=0.0, y_speed=-0.8)
                    bullets[4].restart(x, y, x_speed=0.4, y_speed=-0.8)
                    bullets[5].restart(x, y, x_speed=0.8, y_speed=-0.8)
                    self.interval_b = self.cd
                    return

    def increase_capacity(self):
        self.current_bullet_capacity += 1
        self.barrels.append((BossBullet(), BossBullet(), BossBullet(), BossBullet(), BossBullet(), BossBullet()))


class Bullet(DisplayableObject, MovingObject):
    image_object = None

    def __init__(self):
        super(Bullet, self).__init__()
        self.active = False

    def move(self):
        pass

    def restart(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def try_hit(self, other) -> bool:
        pass

    def show(self):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return f"status: {self.active}, position({self.x}, {self.y}), type: {type(self).__name__}"


class UserBullet(Bullet):
    damage = 1
    image_object = user_bullet_img

    @classmethod
    def upgrade(cls):
        cls.damage *= 1.25

    @classmethod
    def reset(cls):
        cls.damage = 1

    def try_hit(self, enemy) -> bool:
        # print(self.active)
        assert self.active is True
        if enemy.is_active and check_collision(self, enemy, scale_factor=0.75):
            # print("hit", enemy.life, type(self).damage, plane.level)
            enemy.life -= type(self).damage
            self.active = False
            global score, game_level
            score += 1
            if enemy.life <= 0:
                enemy.is_active = False
                score += enemy.score_reward * 0.8 * game_level
            return True
        return False


class SingleStraightBullet(UserBullet):
    def move(self):
        if self.active:
            self.y -= 10.0
        if self.y < 0:
            self.active = False


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
            self.y -= 8.8
            self.x -= 2.0
        if self.y < 0 or self.x < 0:
            self.active = False


class SecondLeftObliqueBullet(LeftStraightBullet):
    def move(self):
        if self.active:
            self.y -= 8.0
            self.x -= 3.0
        if self.y < 0 or self.x < 0:
            self.active = False


class RightObliqueBullet(RightStraightBullet):
    def move(self):
        if self.active:
            self.y -= 8.8
            self.x += 2.0
        if self.y < 0 or self.x > screen_width:
            self.active = False


class SecondRightObliqueBullet(RightStraightBullet):
    def move(self):
        if self.active:
            self.y -= 8.0
            self.x += 3.0
        if self.y < 0 or self.x < 0:
            self.active = False


class BossBullet(Bullet):
    image_object = boss_bullet_img

    def __init__(self):
        super(BossBullet, self).__init__()
        self.x_speed = 0.4
        self.y_speed = 0.4
        self.active = False

    def restart(self, x, y, x_speed=0.4, y_speed=0.4):
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

    def try_hit(self, user_plane: Plane) -> bool:
        assert self.active is True
        if check_collision(self, user_plane, scale_factor=0.7):
            self.active = False
            global game_over, you_win
            you_win = False
            game_over = True
            return True
        return False

    def __str__(self):
        return f"x:{self.x} y:{self.y} active:{self.active}"


class EnemyObject(DisplayableObject, MovingObject):
    image_object = enemy_img
    count = 1

    def __init__(self):
        super(EnemyObject, self).__init__()
        self.score_reward = 100
        self.x = 0
        self.y = 0
        self.life = 0
        self.id = type(self).count
        self.is_active = True
        type(self).count += 1

    def move(self):
        pass

    def show(self):
        if self.is_active:
            screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return f"{type(self).__name__}-{self.id}: active: {self.is_active}, life: {self.life}, position: ({self.x}, {self.y})"


class BasicEnemy(EnemyObject):
    image_object = enemy_img
    count = 1
    life_max = 2
    base_speed = 0.8

    def __init__(self):
        super(BasicEnemy, self).__init__()
        self.score_reward = 100
        self.y_speed = 0.8
        self.x_speed = 0.8
        self.life = type(self).life_max
        self.restart()

    def move(self):
        if self.y < screen_height:
            self.y += self.y_speed
        else:
            self.is_active = False

    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        # base speed is 0.3
        self.y_speed = random.random() * 4 + type(self).base_speed
        self.x_speed = type(self).base_speed
        self.life = type(self).life_max
        self.is_active = True

    @classmethod
    def upgrade(cls):
        cls.life_max *= 2

    @classmethod
    def reset(cls):
        cls.life_max = 2


class StrongEnemy(BasicEnemy):
    image_object = strong_enemy
    count = 1

    def __init__(self):
        super(StrongEnemy, self).__init__()
        self.score_reward = 150
        self.change_direction_interval = 1000

    def move(self):
        self.change_direction_interval -= 1
        if self.change_direction_interval <= 1:
            self.change_direction_interval = 1000
            self.x_speed = -self.x_speed

        if self.y < screen_height:
            self.y += self.y_speed
            self.x += self.x_speed
        else:
            self.is_active = False


class Boss(EnemyObject):
    image_object = boss_img
    count = 1

    def __init__(self):
        super(Boss, self).__init__()
        self.y = 0
        self.x = 0.5 * screen_width - 0.5 * self.width
        self.score_reward = 15000
        self.life = 2000
        self.x_speed = 0.8
        self.y_speed = 0.8
        self.gun = BossGun(initial_capacity=10)

    def fire(self):
        self.gun.fire(self.x + self.width / 2, self.y + self.height)

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
        pass


enemies = []
# enemies.append(Boss())
for i in range(5):
    enemies.append(BasicEnemy())

plane = Plane()
game_over = False
you_win = False
score = 0

threshold = 1000
game_level = 1
# control the frame rate
clock = pygame.time.Clock()


def show_all_objects():
    for e in enemies:
        e.show()
        if isinstance(e, Boss):
            e.gun.show_active_bullets()
    plane.gun.show_active_bullets()
    plane.show()


while True:
    clock.tick(60)
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
            score = 0
            game_over = False
            you_win = False

            game_level = 1
            threshold = 1000
            plane.reset()
            BasicEnemy.reset()
            UserBullet.reset()

            enemies.clear()
            for i in range(5):
                enemies.append(BasicEnemy())
            # print("========")
            # print(BasicEnemy.life_max, enemies[0].life_max)
            # print(StrongEnemy.life_max)
            # print(UserBullet.damage, plane.gun.barrels)
    screen.blit(background, (0, 0))

    if not game_over:
        if plane_fired:
            plane.fire()
        plane.move()
        plane.gun.check_fired_bullets_hit_enemy()
        for e in enemies:
            if e.is_active:
                assert e.life > 0
                if check_collision(plane, e):
                    game_over = True
                e.move()
                if isinstance(e, Boss):
                    e.fire()
                    e.gun.check_fired_bullets_hit_enemy()
            else:
                if not isinstance(e, Boss):
                    e.restart()

            if isinstance(e, Boss) and e.life <= 0:
                game_over = True
                you_win = True
                break

        show_all_objects()

        score = int(score)
        text = font.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        screen.blit(text, (0, 0))
        if score >= threshold:
            threshold *= 2
            BasicEnemy.upgrade()
            enemies.append(StrongEnemy())
            plane.upgrade()
            game_level += 1

    elif you_win:
        w, h = pygame.display.get_surface().get_size()
        screen.blit(win_img, (w / 2 - win_img.get_width() / 2, h / 4))
        score = int(score)
        text_score = font_over.render("Score: {score}".format(score=score), 1, (0, 0, 0))
        score_text_length = text_score.get_width()
        screen.blit(text_score, (w / 2 - score_text_length / 2, h / 6))

        if plane_fired:
            plane.fire()
        plane.move()
        plane.gun.check_fired_bullets_hit_enemy()
        for e in enemies:
            if isinstance(e, Boss):
                e.gun.check_fired_bullets_hit_enemy()
            if e.life > 0:
                if check_collision(plane, e):
                    game_over = True
                    you_win = False

        show_all_objects()

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
