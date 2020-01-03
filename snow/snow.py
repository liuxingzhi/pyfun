# learn from Crossin's wechat
# practice for python
# coding=UTF-8
import pygame
import random

pygame.init()

SCREEN_SIZE = (450, 869)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("雪花飘飘")
origin = pygame.image.load('xiaohei.jpg')
bg = pygame.transform.scale(origin, SCREEN_SIZE)

snow_list = []


class Snowflake:
    def __init__(self):
        self.x = random.randrange(0, SCREEN_SIZE[0])
        self.y = random.randrange(0, SCREEN_SIZE[1])
        self.sx = random.randint(-1, 1)  # x speed
        self.sy = random.randint(2, 4)  # y speed
        self.r = random.randint(1, 4)

    def fly(self):
        self.x += self.sx
        self.y += self.sy
        if self.y > SCREEN_SIZE[1]:
            self.x = random.randrange(0, SCREEN_SIZE[0])
            self.y = random.randrange(-50, -10)


class SnowflakeBackground:
    def __init__(self, snowflake_num: int):
        self.snowflake_list = [Snowflake() for _ in range(snowflake_num)]

    def run(self):
        for snowflake in self.snowflake_list:
            snowflake.fly()
            pygame.draw.circle(screen, (255, 255, 255), (snowflake.x, snowflake.y), snowflake.r)


if __name__ == '__main__':
    # set the frame rate
    clock = pygame.time.Clock()
    snow_background = SnowflakeBackground(100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(bg, (0, 0))
        snow_background.run()
        # update the contents of the entire display
        pygame.display.flip()
        clock.tick(60)
