# 雪花从天而降,从顶部开始随机
# practice for python
# coding=UTF-8
import pygame
import random
from musicUtils import BackgroundMusic

frame_rate = 30
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
    def __init__(self, collection):
        self.x = random.randrange(0, SCREEN_SIZE[0])
        self.y = -0.1 * SCREEN_HEIGHT
        self.sx = random.uniform(-1 * speed_unit, 1 * speed_unit)  # x speed
        self.sy = random.uniform(2 * speed_unit, 4 * speed_unit)  # y speed
        self.r = random.randint(1, 4)
        self.to_be_deleted = False
        self.collection = collection

    def fly(self):
        self.x += self.sx
        self.y += self.sy
        if self.y > SCREEN_SIZE[1]:
            self.collection.remove(self)


class SnowflakeBackground:
    def __init__(self, fall_rate: float = 0.5):
        self.snowflake_collection = set()
        self.fluctuation = 1
        self.max_rate = 36
        self.min_rate = -1.5 * self.fluctuation
        self.fall_rate = fall_rate if fall_rate < self.max_rate else self.max_rate
        self.active = True

    def generate_snowflakes(self):
        new_snows = int(random.normalvariate(self.fall_rate, self.fluctuation))
        if new_snows <= 0:
            return
        for _ in range(new_snows):
            self.snowflake_collection.add(Snowflake(self.snowflake_collection))

    def update(self):
        # print(len(self.snowflake_collection))
        if self.active:
            self.generate_snowflakes()
            for snowflake in self.snowflake_collection.copy():
                snowflake.fly()
                pygame.draw.circle(screen, (255, 255, 255), (round(snowflake.x), round(snowflake.y)), snowflake.r)

    def increase_snowflakes(self, rate: float = 0.5):
        if self.fall_rate < self.max_rate:
            self.fall_rate += rate + (self.fall_rate * 0.1)

    def decrease_snowflakes(self, rate: float = 0.5):
        if self.fall_rate > self.min_rate:
            self.fall_rate -= rate + (self.fall_rate * 0.1)

    def switch_visibility(self):
        self.active = not self.active


if __name__ == '__main__':
    # set the frame rate
    clock = pygame.time.Clock()
    snow_background = SnowflakeBackground(1)
    with BackgroundMusic("luoxiaohei.mp3", forever=True):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit(0)
                    elif event.unicode == "+":
                        snow_background.increase_snowflakes()
                    elif event.key == pygame.K_MINUS:
                        snow_background.decrease_snowflakes()
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
