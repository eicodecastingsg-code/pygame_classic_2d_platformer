import pygame

lava_img = pygame.image.load("img/lava2.jpg")
lava_img = pygame.transform.scale(lava_img, (40, 40))

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = lava_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
