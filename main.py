# import libraries
import pygame
from castle import Castle
from constants import *
from enemy import Enemy
from crosshair import Crosshair
from tower import Tower
import random
import os
import button

# initialize pygame
pygame.init()

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Castle Defender")

clock = pygame.time.Clock()
FPS = 60

# define game variables
level = 1
high_score = 0


level_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.1
game_over = False
next_level = False
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
TOWER_COST = 5000

tower_positions = [
    [SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150],
]
max_towers = len(tower_positions)

# load high score
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())


# define font
font_30 = pygame.font.SysFont('Futura', 30)
font_60 = pygame.font.SysFont('Futura', 60)

#  load images
bg = pygame.image.load('img/bg.png').convert_alpha()
# castle images
castle_img_100 = pygame.image.load('img/castle/castle_100.png').convert_alpha()
castle_img_50 = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_img_25 = pygame.image.load('img/castle/castle_25.png').convert_alpha()

# tower images
tower_img_100 = pygame.image.load('img/tower/tower_100.png').convert_alpha()
tower_img_50 = pygame.image.load('img/tower/tower_50.png').convert_alpha()
tower_img_25 = pygame.image.load('img/tower/tower_25.png').convert_alpha()

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

# load button images
# repair image
repair_img = pygame.image.load('img/repair.png').convert_alpha()
# armour image
armour_img = pygame.image.load('img/armour.png').convert_alpha()


# function to output text onto the screen
def draw_text(text, f, text_col, x, y):
    img = f.render(text, True, text_col)
    screen.blit(img, (x, y))


# function to display status
def show_info():
    draw_text("Money: " + str(castle.money), font_30, GREY, 10, 10)
    draw_text("Score: " + str(castle.score), font_30, GREY, 180, 10)
    draw_text("High Score: " + str(high_score), font_30, GREY, 180, 30)
    draw_text("Level: " + str(level), font_30, GREY, SCREEN_WIDTH // 2, 10)
    draw_text("Health: " + str(castle.health) + "/" + str(castle.max_health), font_30, GREY,
              SCREEN_WIDTH - 230, SCREEN_HEIGHT - 50)
    draw_text("1000", font_30, GREY, SCREEN_WIDTH - 220, 70)
    draw_text(str(TOWER_COST), font_30, GREY, SCREEN_WIDTH - 150, 70)
    draw_text("500", font_30, GREY, SCREEN_WIDTH - 70, 70)


# create groups
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# create castle
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

# create crosshair
crosshair = Crosshair(0.025)

# create buttons
repair_button = button.Button(SCREEN_WIDTH - 220, 10, repair_img, 0.5)
tower_buttton = button.Button(SCREEN_WIDTH - 140, 10, tower_img_100, 0.1)
armour_button = button.Button(SCREEN_WIDTH - 75, 10, armour_img, 1.5)

# game loop
run = True
while run:

    clock.tick(FPS)

    if not game_over:
        # draw background
        screen.blit(bg, (0, 0))

        # draw castle
        castle.draw(screen)
        castle.shoot(bullet_img, bullet_group)

        # draw towers
        tower_group.draw(screen)

        # draw crosshair
        crosshair.draw(screen)

        # draw bullets
        bullet_group.update()
        bullet_group.draw(screen)

        # draw enemies
        enemy_group.update(screen, castle, bullet_group)

        # draw towers
        tower_group.update(enemy_group, screen, bullet_img, bullet_group, castle)
        # show details
        show_info()

        # draw buttons
        if repair_button.draw(screen):
            castle.repair()
        if armour_button.draw(screen):
            castle.armour()
        if tower_buttton.draw(screen):
            # check if there is enough money to build a tower
            if castle.money >= TOWER_COST and len(tower_group) < max_towers:
                tower = Tower(
                    tower_img_100,
                    tower_img_50,
                    tower_img_25,
                    tower_positions[len(tower_group)][0],
                    tower_positions[len(tower_group)][1],
                    0.2)
                tower_group.add(tower)
                # subtract money
                castle.money -= TOWER_COST

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
            # update high score
            if castle.score > high_score:
                high_score = castle.score
                with open('score.txt', "w") as file:
                    file.write(str(high_score))
            if pygame.time.get_ticks() - level_reset_time > 2000:
                next_level = False
                level += 1
                last_enemy = pygame.time.get_ticks()
                target_difficulty = target_difficulty * DIFFICULTY_MULTIPLIER
                level_difficulty = 0
                enemy_group.empty()

        # check game over
        if castle.health <= 0:
            game_over = True

    else:
        draw_text("GAME OVER!", font_30, GREY, 300, 300)
        draw_text('Press "A" to play again!', font_30, GREY, 250, 360)
        pygame.mouse.set_visible(True)
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            # reset game variables
            game_over = False
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.money = 0
            pygame.mouse.set_visible(False)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.flip()

pygame.quit()
