import math
from bullet import Bullet
import pygame.sprite


class Tower(pygame.sprite.Sprite):
    def __init__(self, image100, image50, image25, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        width = image100.get_width()
        height = image100.get_height()
        self.got_target = False
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))

        self.image = self.image100
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()

    def update(self, enemy_group, screen, bullet_img, bullet_group, castle):
        self.got_target = False
        for e in enemy_group:
            if e.alive:
                target_x, target_y = e.rect.midright
                self.got_target = True
                break

        if self.got_target:
            x_dist = target_x - self.rect.midleft[0]
            y_dist = -(target_y - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_dist, x_dist))

            shot_cooldown = 1000
            # fire bullet
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                self.last_shot = pygame.time.get_ticks()
                bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)

        # check  which  image to use based on health
        if castle.health <= 250:
            self.image = self.image25
        elif castle.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100
