# learn from Crossin's wechat
# practice for python
# coding=UTF-8
import pygame
import random

pygame.init()

SIZE = (450, 869)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("雪花飘飘")
origin = pygame.image.load('xiaohei.jpg')
bg = pygame.transform.scale(origin, (450, 869))

snow_list = []


class Snowflake:
    def __init__(self):
        self.x = random.randrange(0, SIZE[0])
        self.y = random.randrange(0, SIZE[1])
        self.sx = random.randint(-1, 1)  # x speed
        self.sy = random.randint(3, 6)  # y speed
        self.r = random.randint(0, 3)

    def fly(self):
        self.x += self.sx
        self.y += self.sy


for i in range(270):
    snow = Snowflake()
    snow_list.append(snow)

# set the frame rate
clock = pygame.time.Clock()
done = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg, (0, 0))
    for snow in snow_list:
        pygame.draw.circle(screen, (255, 255, 255), (snow.x, snow.y), snow.r)

        snow.fly()

        if snow.y > SIZE[1]:
            snow.x = random.randrange(0, SIZE[0])
            snow.y = random.randrange(-50, -10)

    # update the contents of the entire display
    pygame.display.flip()
    clock.tick(40)
