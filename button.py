import pygame

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen):
        signal = False

        # trace mouse position
        mouse_pos = pygame.mouse.get_pos()

        # check if the button collides with the mouse pointer
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.clicked:
                    self.clicked = True
                    signal = True

        # if we let do the LMB
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return signal





















