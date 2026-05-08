import pygame
from world import World
import world_data
from button import Button
from world_data import all_world_data
import random

pygame.init()

clock = pygame.time.Clock()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Platformer - 60fps")

bg_img = pygame.image.load("img/sky.png")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
restart_img = pygame.image.load("img/restart_btn.png")
start_img = pygame.image.load("img/start_btn.png")
exit_img = pygame.image.load("img/exit_btn.png")
soundOn_img = pygame.image.load("img/Sound_on.png")
soundOff_img = pygame.image.load("img/Sound_off.png")
soundOn_img = pygame.transform.scale(soundOn_img, (60, 60))
soundOff_img = pygame.transform.scale(soundOff_img, (60, 60))


# build buttons
restart_btn = Button(350, 380, restart_img)
start_btn = Button(200, 500, pygame.transform.scale(start_img, (140, 63)))
exit_btn = Button(460, 500, pygame.transform.scale(exit_img, (140, 63)))
sound_btn = Button(380, 600, soundOn_img)


game_over = 0
main_menu = True


# load font and define game title
font = pygame.font.Font("img/PressStart2P.ttf", 30)
title = font.render("Mario City 1.0", True, (0, 0, 0))


# load and play bgm
pygame.mixer.music.load("img/music.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
bgm = True


load_next_level = False
max_level = 5
current_level = 0


# timer variables
totalTime = 30
timeLeft = totalTime
start_ticks = 0

coin_sound = pygame.mixer.Sound("img/coin.wav")
coin_sound.set_volume(0.5)
coinCount = 0


def reset_level(level):
    global enemy_group
    global exit_group
    global lava_group
    global coin_group
    global platform_group

    enemy_group.empty()
    exit_group.empty()
    lava_group.empty()
    coin_group.empty()
    platform_group.empty()

    current_world_data = all_world_data[level]

    # rebuild the world
    return World(current_world_data, enemy_group, exit_group, lava_group, coin_group, platform_group)




class Player:
    def __init__(self, x, y):
        self.reset(x, y)
        self.base_speed = 5
        self.base_jump = -16
        self.speed = self.base_speed
        self.jump_power = self.base_jump
        self.boosted = False
        self.boost_duration = 180    # 180 frames = 3s in 60 FPS setting
        self.boost_timer = 0


    def reset(self, x, y):
        self.right_images = []
        self.left_images = []

        for i in range(1, 5, 1):
            right_img = pygame.image.load(f"img/guy{i}.png")
            right_img = pygame.transform.scale(right_img, (22, 44))
            left_img = pygame.transform.flip(right_img, True, False)
            self.left_images.append(left_img)
            self.right_images.append(right_img)

        self.image = self.right_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 0
        self.gravity = 1
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumping = False
        self.inTheAir = True
        self.direction = "right"
        self.imgIndex = 0
        self.animCounter = 0
        self.animCooldown = 4   # wait 4 frames before switching costume
        self.health = 5
        self.invincible = False
        self.invincible_timer = 0
        self.dead_image = pygame.image.load("img/ghost.png")


    # the player has to update its costume, x, y... every frame
    def update(self):
        dy = 0     # differential change in player y
        dx = 0

        global game_over
        global load_next_level
        global totalTime
        global coin_group

        # randomized reward upon coin collection
        collision = pygame.sprite.spritecollide(self, coin_group, True)
        if collision:
            randomReward = random.randint(1, 2)
            if randomReward == 1:
                totalTime += 10
            elif randomReward == 2:
                self.boosted = True
                self.speed = 10
                self.jump_power = -32
                self.boost_timer = self.boost_duration


        if self.health < 1:
            game_over = 1

        if game_over == 0:

            # motion control
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.direction = "left"
                dx = -self.speed
                self.animCounter += 1
            if keys[pygame.K_d]:
                self.direction = "right"
                dx = self.speed
                self.animCounter += 1
            if keys[pygame.K_w] and not self.jumping and not self.inTheAir:
                self.jumping = True
                self.y_speed = self.jump_power
            if not keys[pygame.K_w]:
                self.jumping = False


            # handle boost timer
            if self.boosted:
                self.boost_timer -= 1
                if self.boost_timer <= 0:
                    self.speed = self.base_speed
                    self.jump_power = self.base_jump
                    self.boosted = False


            # animation
            if self.animCounter >= self.animCooldown:
                self.animCounter = 0
                if self.imgIndex >= 4:
                    self.imgIndex = 0
                if self.direction == "left":
                    self.image = self.left_images[self.imgIndex]
                if self.direction == "right":
                    self.image = self.right_images[self.imgIndex]
                self.imgIndex += 1



            # add gravity (gravity -> y_speed -> dy -> y)
            self.y_speed += self.gravity
            if self.y_speed > 50:       # terminal velocity
                self.y_speed = 50
            dy += self.y_speed
            self.inTheAir = True


            # check if the player collides with the portal
            if pygame.sprite.spritecollide(self, exit_group, False):
                load_next_level = True

            # check if the player collides with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                self.health = 0


            # check if the player collides with a moving platform
            for mp in platform_group:
                # collision in the vertical direction
                # early detection (if the player collides with the moving platform on the next frame)
                if mp.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if collision happens above the platform
                    # check if player bottom edge is above the platform top edge
                    # LANDING ON PLATFORM (player falling)
                    if self.y_speed >= 0 and self.rect.bottom <= mp.rect.top + 10:
                        dy = mp.rect.top - self.rect.bottom
                        self.y_speed = 0
                        self.inTheAir = False

                    # HITTING FROM BELOW (player jumping)
                    elif self.y_speed < 0 and self.rect.top >= mp.rect.bottom - 10:
                        self.y_speed = 0
                        dy = 0

                    # make player moves sideways on a horizontal mp
                    if mp.move_x:
                        self.rect.x += mp.speed * mp.direction

                # collision detection in the horizontal direction
                if mp.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    # ONLY block if player is hitting the SIDE of platform
                    if self.rect.bottom > mp.rect.top + 10:
                        dx = 0



            # each solid tile on the map has to check if it collides with the player
            for tile_info in map.tile_list:
                # collision detection in y direction
                if tile_info[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if collision happened down below the player (falling)
                    if self.y_speed >= 0:
                        dy = tile_info[1].top - self.rect.bottom
                        self.y_speed = 0
                        self.inTheAir = False
                    elif self.y_speed < 0:
                        # check for collision up above the player (jumping)
                        dy = tile_info[1].bottom - self.rect.top
                        self.y_speed = 0

                # collision detection in x direction
                if tile_info[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0


            # apply dy to player y
            self.rect.y += dy
            self.rect.x += dx

            # enemy collision detection
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect):
                    # check if the player is falling onto the enemy
                    if self.y_speed > 0 and self.rect.bottom > enemy.rect.top:
                        enemy.alive = False
                        self.y_speed = -10    # makes the player bounce
                        self.inTheAir = True  # disable jumping

                    # check if the enemy is coming from the side
                    elif not self.invincible and enemy.alive:
                        self.health -= 1
                        self.invincible = True
                        self.invincible_timer = 60   # 60 frames = 1s

            # handle invincible timer and blinking effect
            if self.invincible:
                self.invincible_timer -= 1
                if self.invincible_timer <= 0:
                    self.invincible = False
                # make it blink every 3 frames
                if self.invincible_timer % 3 == 0:
                    pass
                else:
                    screen.blit(self.image, self.rect)
            else:
                screen.blit(self.image, self.rect)

        elif game_over == 1:
            # when the player is dead
            self.image = self.dead_image
            if self.rect.y > 0:  # if it's below the top edge
                self.rect.y -= 5
            screen.blit(self.image, self.rect)




enemy_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()


# build a player object
myPlayer = Player(50, 50)

# build the map
map = World(world_data.world_data_0, enemy_group, exit_group, lava_group, coin_group, platform_group)


# Main Game Loop
GameRunning = True

while GameRunning:
    clock.tick(60)

    screen.blit(bg_img, (0, 0))

    if main_menu:
        # load main menu
        screen.blit(title, (200, 200))
        if start_btn.draw(screen):
            main_menu = False
            start_ticks = pygame.time.get_ticks()  # pygame clock starts ticking

        if exit_btn.draw(screen):
            GameRunning = False
        if sound_btn.draw(screen):
            bgm = not bgm    # flipping
            if bgm:
                pygame.mixer.music.unpause()
                sound_btn.image = soundOn_img
            else:
                pygame.mixer.music.pause()
                sound_btn.image = soundOff_img

    else:
        # load game screen
        map.draw(screen)
        enemy_group.draw(screen)
        exit_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        platform_group.draw(screen)

        myPlayer.update()
        platform_group.update()
        enemy_group.update(map.tile_list)

        # coin collection logic
        if pygame.sprite.spritecollide(myPlayer, coin_group, False):
            coin_sound.play()
            coinCount += 1
        coin_label = font.render(f"Coins:{coinCount}", True, (0, 0, 0))
        screen.blit(coin_label, (20, 10))


        if game_over == 1:
            if restart_btn.draw(screen):
                # check if the time has run out
                if timeLeft == 0:
                    current_level = 0   # restart game from level 0
                    start_ticks = pygame.time.get_ticks()  # reset timer
                    totalTime = 30

                # reset player
                myPlayer.reset(50, 50)
                game_over = 0
                # reset level
                map = reset_level(current_level)

        # if we clear a level
        if load_next_level:
            load_next_level = False
            current_level += 1
            map = reset_level(current_level)
            myPlayer.reset(100, 100)

        # timer logic
        minutes = timeLeft // 60
        seconds = timeLeft % 60
        time_string = f"{minutes:02}:{seconds:02}"
        timer_text = font.render(time_string, True, (0, 0, 0))
        screen.blit(timer_text, (350, 10))
        timeLapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        timeLeft = totalTime - timeLapsed
        if timeLeft <= 0:
            timeLeft = 0
            game_over = 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False

    # to update the game screen every frame
    pygame.display.update()

pygame.quit()















