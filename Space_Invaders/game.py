from Player import Player
from Bunker import Bunker
from enemy import EnemiesContainer
from constants import *
from Bullet import *
from UI import *
from ufo import Ufo
import pygame
import sys
from timer import Timer
from pygame.locals import QUIT,K_SPACE,K_RETURN,K_ESCAPE, K_0

pygame.init()

clock = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE.fill(BLACK)
pygame.display.set_caption("Game")

font = pygame.font.SysFont("Verdana", 30)
font_small = pygame.font.SysFont("Verdana", 15)

score = 0
highscore_checked = False

game_playing = 0
game_over = 1
main_menu = 2

game_state = main_menu

def ResetGame():
    global game_state, score, highscore_checked

    game_state = game_playing
    score = 0
    highscore_checked = False
    main()

def main():

    delta = 0.0
    display_timer = Timer()

    player = Player()
    enemies = EnemiesContainer()
    ufo = Ufo()

    bunker1 = Bunker(110, 500)
    bunker2 = Bunker(350, 500)
    bunker3 = Bunker(550, 500)
    bunker4 = Bunker(790, 500)

    bunkers = [bunker1, bunker2, bunker3, bunker4]

    objects = [player] + [enemies] + [ufo] + bunkers + [display_timer]

    global game_state, score, highscore_checked

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        key_up = pygame.key.get_just_released()

        if game_state == game_playing:
            DISPLAY_SURFACE.fill(BLACK)            

            if keys[K_SPACE]:
                bullet_player = player.shoot(objects)
                if bullet_player:
                    objects.append(bullet_player)

            if keys[K_0]:
                game_state = game_over

            bullet_enemy = enemies.shoot(delta, score, objects)
            if bullet_enemy:
                objects.append(bullet_enemy)        
                
            for obj in objects:
                obj.update(delta)
                if isinstance(obj, Bullet):
                    score += bullet_enemy_collisions(obj, enemies)
                    bullet_bunker_collisions(obj, bunkers)
                    if obj.dead:
                        objects.remove(obj)

            score_tracker(DISPLAY_SURFACE, score)

            for obj in objects:
                obj.draw(DISPLAY_SURFACE)

            pygame.display.update()
            delta = clock.tick(FPS) / 1000.0

        if game_state == game_over:
            if highscore_checked == False:
                game_over_screen(DISPLAY_SURFACE, score)
                highscore_checked = True

            if keys[K_RETURN]:
                ResetGame()
                return
            
            elif key_up[K_ESCAPE]:
                DISPLAY_SURFACE.fill(BLACK)
                game_state = main_menu

        if game_state == main_menu:
            main_menu_screen(DISPLAY_SURFACE)

            if key_up[K_SPACE]:
                game_state = game_playing

            elif keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()