import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0  # 0: walk, 1: attack, 2: death
        self.update_time = pygame.time.get_ticks()

        # select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 25, 40)
        self.rect.center = (x, y)

    def update(self, surface, target, bullet_group):

        # if enemy is alive
        if self.alive:

            # check for collision with bullets
            if pygame.sprite.spritecollide(self, bullet_group, True):
                # lower enemy health
                self.health -= 25

            # check if enemy has reached the castle
            if self.rect.right > target.rect.left:
                self.update_action(1)

            # move enemy
            if self.action == 0:
                # update rectangle position
                self.rect.x += self.speed

            # check if health has dropped to zero
            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2)  # death
                self.alive = False

        self.update_animation()

        #  draw image on screen
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
        surface.blit(self.image, (self.rect.x - 10, self.rect.y - 15))

    def update_animation(self):

        # define animation cooldown
        ANIMATION_COOLDOWN = 50

        # update image depending on current action
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame_index if the animation has run out
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation  settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

