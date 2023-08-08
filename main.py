# import libraries
import pygame
from castle import Castle
from constants import *

# initialize pygame
pygame.init()

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Castle Defender")

clock = pygame.time.Clock()
FPS = 60


#  load images
bg = pygame.image.load('img/bg.png').convert_alpha()
# castle
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()

# bullet images
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * scale),  int(b_h * scale)))

# create group
bullet_group = pygame.sprite.Group()

# create castle
castle = Castle(castle_img_100, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

# game loop

run = True
while run:

    clock.tick(FPS)

    # draw background
    screen.blit(bg, (0, 0))

    # draw castle
    castle.draw(screen)
    castle.shoot(bullet_img, bullet_group)

    # draw bullets
    bullet_group.update()
    bullet_group.draw(screen)
    print(len(bullet_group))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.flip()

pygame.quit()
