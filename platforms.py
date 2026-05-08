import pygame

platform_x_img = pygame.image.load("img/platform_x.png")
platform_x_img = pygame.transform.scale(platform_x_img, (80, 30))

platform_y_img = pygame.image.load("img/platform_y.png")
platform_y_img = pygame.transform.scale(platform_y_img, (80, 30))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)

        if move_x == True and move_y == False:
            self.image = platform_x_img
        elif move_x == False and move_y == True:
            self.image = platform_y_img

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = move_x
        self.move_y = move_y
        self.speed = 1
        self.stepCounter = 0
        self.maxRange = 150
        self.direction = -1   # -1(upward), 1(downward)

    def update(self):
        # if it is a vertical moving platform
        if self.move_y:
            self.rect.y += self.speed * self.direction
            self.stepCounter += self.speed
            if self.stepCounter > self.maxRange:
                self.direction *= -1
                self.stepCounter = 0

        # else if it is a horizontal moving platform
        elif self.move_x:
            self.rect.x += self.speed * self.direction
            self.stepCounter += self.speed
            if self.stepCounter > self.maxRange:
                self.direction *= -1
                self.stepCounter = 0
























