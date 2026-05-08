import pygame
from enemy import Enemy
from exit import Exit
from lava import Lava
from coin import Coin
from platforms import Platform

grid_size = 40

class World():
    def __init__(self, world_data, enemy_group, exit_group, lava_group, coin_group, platform_group):
        self.tile_list = []

        dirt_img = pygame.image.load('img/dirt.png')
        dirt_img = pygame.transform.scale(dirt_img, (grid_size, grid_size))

        row_number = 0

        for row in world_data:
            for i in range(0, 20, 1):     # i = column number
                if row[i] == 1:
                    tile_img = dirt_img
                    tile_hit_box = tile_img.get_rect()
                    tile_hit_box.x = i * grid_size
                    tile_hit_box.y = row_number * grid_size
                    tile_info = (tile_img, tile_hit_box)
                    self.tile_list.append(tile_info)

                if row[i] == 2:
                    enemy = Enemy(i * grid_size, row_number * grid_size)
                    enemy_group.add(enemy)

                if row[i] == 3:
                    exit_portal = Exit(i * grid_size, row_number * grid_size)
                    exit_group.add(exit_portal)

                if row[i] == 4:
                    lava = Lava(i * grid_size, row_number * grid_size)
                    lava_group.add(lava)

                if row[i] == 5:
                    coin = Coin(i * grid_size, row_number * grid_size)
                    coin_group.add(coin)

                # vertical moving platform
                if row[i] == 6:
                    platformY = Platform(i * grid_size, row_number * grid_size, False, True)
                    platform_group.add(platformY)

                # horizontal moving platform
                if row[i] == 7:
                    platformX = Platform(i * grid_size, row_number * grid_size, True, False)
                    platform_group.add(platformX)


            row_number += 1

    def draw(self, screen):
        for tile_info in self.tile_list:
            screen.blit(tile_info[0], tile_info[1])











