import pygame
from sys import exit
import numpy as np
from random import randint, choice
import sys, os

# sys.path.append(f"{os.getcwd()}/PIXEL_RUNNER/")
# os.chdir(path=f"{os.getcwd()}/PIXEL_RUNNER/")

print("HOla mundo")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            "graphics/player/player_walk_1.png"
        ).convert_alpha()
        player_walk_2 = pygame.image.load(
            "graphics/player/player_walk_2.png"
        ).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.space_key_pressed = False

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_SPACE]
            and self.rect.bottom == ground_rect.top
            and not self.space_key_pressed
        ):
            self.gravity = -20
            self.jump_sound.play()
            self.space_key_pressed = True
        elif not keys[pygame.K_SPACE]:
            self.space_key_pressed = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > ground_rect.top:
            self.rect.bottom = ground_rect.top

    def animation_stage(self):
        if self.rect.bottom < ground_rect.top:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_stage()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == "fly":
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1200), y_pos))

    def animation_stage(self):
        if self.type == "fly":
            self.animation_index += 0.5
        else:
            self.animation_index += 0.3
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def selfdestroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.animation_stage()
        self.rect.x -= 6
        self.selfdestroy()


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    current_time /= 1000
    current_time = int(current_time)
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite = Player()
        return False
    else:
        return True


# STARTS PYGAME
pygame.init()

# CREATE DISPLAY SURFACE
screen = pygame.display.set_mode((800, 400))

# SET TITLE
pygame.display.set_caption("Runner")

# CLOCK OBJET
clock = pygame.time.Clock()

# FONT AND TEXT
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# ACTIVE GAME
game_active = False

# TIME COUNT
start_time = 0

# SCORE
score = 0

bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.7)
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

# TEST SURFACE
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_rect = ground_surface.get_rect(midtop=(400, 300))

# score_surf=test_font.render('My game',False,(64,64,64) ).convert()
# score_rect=score_surf.get_rect(center=(400,50))

obstacle_group = pygame.sprite.Group()


obstacle_rect_list = []

# INTRO
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title_surf = test_font.render("Pixel Runner", False, (111, 196, 169)).convert()
title_rect = title_surf.get_rect(center=(400, 80))

game_message = test_font.render("Press space to run", False, (111, 196, 169)).convert()
game_message_rect = game_message.get_rect(center=(400, 330))

# TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        score = display_score()
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, ground_rect)
        # pygame.draw.rect(screen,"#c0e8ec",score_rect)
        # pygame.draw.rect(screen,"#c0e8ec",score_rect, 10)
        # pygame.draw.ellipse(screen,(255,255,0),pygame.Rect(50,200,100,100))
        # pygame.draw.rect(screen,"Pink",score_rect, 10)
        # screen.blit(score_surf,score_rect)
        display_score()

        # snail_rect.x-=4
        # if snail_rect.right<0:
        #     snail_rect.left=800

        # screen.blit(snail_surface,snail_rect)

        # PLAYER
        # player_gravity +=1
        # player_rect.y  += player_gravity

        # # print(player_rect.bottom)
        # if player_rect.bottom>ground_rect.top:
        #     player_rect.bottom=ground_rect.top
        # player_animation()
        # screen.blit(player_surf,player_rect)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        # Obstacle generator
        # obstacle_rect_list= obstacle_movement(obstacle_rect_list)

        # COLLISION
        game_active = collision_sprite()

        # keys=pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('JUMP')

        # if player_rect.colliderect(snail_rect):
        #     print('COLLISION')
        # mouse_pos = pygame.mouse.get_pos() #It returns a tuple of (x,y) position
        # if player_rect.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        screen.blit(title_surf, title_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # UPDATE EVERYTHING
    pygame.display.update()
    clock.tick(60)
