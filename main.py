# import libraries
import pygame
from castle import Castle
from constants import *
from enemy import Enemy
from crosshair import Crosshair
import random

# initialize pygame
pygame.init()

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Castle Defender")

clock = pygame.time.Clock()
FPS = 60

# define game variables
level = 1
level_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.1
game_over = False
next_level = False
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0

# define font
font_30 = pygame.font.SysFont('Futura', 30)
font_60 = pygame.font.SysFont('Futura', 60)

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
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * scale), int(b_h * scale)))

# load enemy images
enemy_animations = []
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin']
enemy_health = [75, 100, 125, 150]

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


# function to output text onto the screen
def draw_text(text, f, text_col, x, y):
    img = f.render(text, True, text_col)
    screen.blit(img, (x, y))


# create groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# create castle
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

# create crosshair
crosshair = Crosshair(0.025)

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

    # create enemies
    # check if level difficulty is less than target difficulty
    if level_difficulty < target_difficulty:
        if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
            # create enemies
            e = random.randint(0, len(enemy_types) - 1)
            enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_HEIGHT - 100, 1)
            enemy_group.add(enemy)
            # reset enemy timer
            last_enemy = pygame.time.get_ticks()
            # increase level difficulty by enemy health
            level_difficulty += enemy.health

    # check if all the enemies have been spawned
    if level_difficulty >= target_difficulty:
        # check how many are still alive
        enemies_alive = 0
        for e in enemy_group:
            if e.alive:
                enemies_alive += 1
        # if there are no enemies alive, then the level is complete
        if enemies_alive == 0 and not next_level:
            next_level = True
            level_reset_time = pygame.time.get_ticks()

    # move onto the next level
    if next_level:
        draw_text("LEVEL COMPLETE", font_60, WHITE, 200, 300)
        if pygame.time.get_ticks() - level_reset_time > 1500:
            next_level = False
            level += 1
            last_enemy = pygame.time.get_ticks()
            target_difficulty = target_difficulty * DIFFICULTY_MULTIPLIER
            level_difficulty = 0
            enemy_group.empty()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.flip()

pygame.quit()
