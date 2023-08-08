# import libraries
import pygame
from  castle import Castle
# initialize pygame
pygame.init()

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Castle Defender")

clock = pygame.time.Clock()
FPS = 60

#  load images
bg = pygame.image.load('img/bg.png').convert_alpha()
# castle
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
# game loop

# create castle
castle = Castle(castle_img_100, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)


run = True
while run:

    clock.tick(FPS)

    # draw background
    screen.blit(bg, (0, 0))

    # draw castle
    castle.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.flip()

pygame.quit()
