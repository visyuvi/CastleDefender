# import libraries
import pygame
from castle import Castle
from constants import *
from enemy import Enemy
from crosshair import Crosshair

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
castle_img_50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_img_25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()


# bullet images
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * scale),  int(b_h * scale)))

# load enemy images
enemy_animations = []
enemy_types = ['knight']
enemy_health = [75]

animation_types = ['walk', 'attack', 'death']
for enemy in enemy_types:
    # load animation
    animation_list = []
    for animation in animation_types:
        # reset temporary list of images
        temp_list = []
        # define number of frames
        num_of_frames = 20
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

# create group
bullet_group = pygame.sprite.Group()

# create castle
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

# create crosshair
crosshair = Crosshair(0.025)

# create enemies
enemy_1 = Enemy(enemy_health[0], enemy_animations[0], 400, SCREEN_HEIGHT - 100, 1)
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy_1)

# game loop

run = True
while run:

    clock.tick(FPS)

    # draw background
    screen.blit(bg, (0, 0))

    # draw castle
    castle.draw(screen)
    castle.shoot(bullet_img, bullet_group)

    # draw crosshair
    crosshair.draw(screen)

    # draw bullets
    bullet_group.update()
    bullet_group.draw(screen)

    # draw enemies
    enemy_group.update(screen, castle, bullet_group)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.flip()

pygame.quit()
