import pygame

coin_img = pygame.image.load("img/coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y