import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load("img/blob.png")
        self.image = pygame.transform.scale(self.image, (46, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1     # 1 = right; -1 = left
        self.alive = True
        self.opacity = 255     # starts fully visible

    # update() function runs forever
    def update(self, tile_list):
        # if dying, fade out instead of continue moving
        if not self.alive:
            self.opacity -= 10
            self.image.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.kill()
            return  # kill the function and to skip all codes below

        # move horizontally
        self.rect.x += self.direction * self.speed

        # wall detection
        for tile, tile_rect in tile_list:
            if self.rect.colliderect(tile_rect):
                # undo previous frame's movement
                self.rect.x -= self.direction * self.speed

                # flip enemy direction
                self.direction *= -1

                # end function early to avoid double flipping
                return

        # edge detection
        # predict enemy's front feet position
        feet_x = self.rect.centerx + (self.direction * (self.rect.width // 2 + 5))
        feet_y = self.rect.bottom + 5

        # check if there is a solid tile block ahead
        on_ground = False
        for tile, tile_rect in tile_list:
            if tile_rect.collidepoint(feet_x, feet_y):
                on_ground = True
                break

        # if no ground ahead, flip direction
        if not on_ground:
            self.direction *= -1





















