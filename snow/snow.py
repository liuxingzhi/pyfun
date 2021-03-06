# learn from Crossin's wechat
# practice for python
# coding=UTF-8
import pygame
import random
from musicUtils import BackgroundMusic
from typing import Dict, Set
import itertools

frame_rate = 45
speed_unit = 60 / frame_rate

pygame.init()
SCREEN_SIZE = (450, 869)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
screen = pygame.display.set_mode(SCREEN_SIZE)
# screen = pygame.display.set_mode()
# SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
# SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.display.set_caption("雪花飘飘")
origin = pygame.image.load('xiaohei.jpg')
bg = pygame.transform.scale(origin, SCREEN_SIZE)


class Snowflake:
    def __init__(self):
        self.x = random.randrange(0, SCREEN_SIZE[0])
        self.y = random.randrange(0, SCREEN_SIZE[1])
        self.sx = random.uniform(-1 * speed_unit, 1 * speed_unit)  # x speed
        self.sy = random.uniform(2 * speed_unit, 4 * speed_unit)  # y speed
        self.r = random.randint(1, 4)

    def fly(self):
        self.x += self.sx
        self.y += self.sy
        if self.y > SCREEN_SIZE[1]:
            self.x = random.randrange(0, SCREEN_SIZE[0])
            self.y = random.randrange(-50, -10)


class SnowflakeBackground:
    def __init__(self, snowflake_num: int = 150):
        self.max_number = 5000
        self.initial_snowflake_num = snowflake_num
        self.snowflake_list = []
        self.increase_snowflakes(self.initial_snowflake_num)
        self.active = True

    def update(self):
        if self.active:
            for snowflake in self.snowflake_list.copy():
                snowflake.fly()
                pygame.draw.circle(screen, (255, 255, 255), (round(snowflake.x), round(snowflake.y)), snowflake.r)

    def increase_snowflakes(self, snowflake_num: int = 50):
        # print(len(self.snowflake_list))
        if len(self.snowflake_list) < self.max_number:
            normed = snowflake_num + round(len(self.snowflake_list) * 0.2)
            for _ in range(normed):
                self.snowflake_list.append(Snowflake())

    def decrease_snowflakes(self, snowflake_num: int = 50):
        normed = snowflake_num + round(len(self.snowflake_list) * 0.2)
        self.snowflake_list = self.snowflake_list[:-normed]

    def switch_visibility(self):
        self.active = not self.active


if __name__ == '__main__':
    # set the frame rate
    clock = pygame.time.Clock()
    snow_background = SnowflakeBackground(150)
    with BackgroundMusic("luoxiaohei.mp3", forever=True):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit(0)
                    elif event.unicode == "+":
                        snow_background.increase_snowflakes(50)
                    elif event.key == pygame.K_MINUS:
                        snow_background.decrease_snowflakes(50)
                    elif event.key == pygame.K_s:
                        snow_background.switch_visibility()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            screen.blit(bg, (0, 0))
            snow_background.update()
            # update the contents of the entire display
            pygame.display.flip()
            clock.tick(frame_rate)
