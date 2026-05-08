import pygame

exit_img = pygame.image.load("img/exit.png")
exit_img = pygame.transform.scale(exit_img, (30, 40))

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = exit_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

