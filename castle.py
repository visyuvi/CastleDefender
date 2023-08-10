import pygame.transform
import math
from bullet import Bullet


class Castle:
    def __init__(self, image100, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 0
        self.score = 0

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image = self.image100
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0

    def shoot(self, bullet_img, bullet_group):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        # get mouse click
        if pygame.mouse.get_pressed()[0] and not self.fired:
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
            self.fired = True

        # reset mouse click
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
