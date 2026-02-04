from Player import Player
from Bunker import Bunker, spawn_bunkers
from enemy import EnemiesContainer
from constants import *
from Bullet import Bullet, bullet_player_collisions, bullet_bunker_collisions, bullet_enemy_collisions
from assets import player_death_sound, player_dead
from UI import *
from ufo import Ufo
import pygame
import sys
from pygame.locals import QUIT,K_SPACE,K_RETURN,K_ESCAPE, K_0

pygame.init()

clock = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE.fill(BLACK)
pygame.display.set_caption("Game")

score = 0
highscore_checked = False
death_sound_played = False
DEATH_CHANNEL = pygame.mixer.Channel(7) # exists to avoid bugs when playing death sound

#instance game state variables
game_playing = 0
game_over = 1
main_menu = 2

#initial game state
game_state = main_menu

#starts and restarts the game loop
def reset_game():
    global score, highscore_checked, death_sound_played

    score = 0
    highscore_checked = False
    death_sound_played = False

    #initialise all game objects
    player = Player()
    enemies = EnemiesContainer()
    ufo = Ufo()
    bunkers = spawn_bunkers()

    clock.tick()

    objects = [player, enemies, ufo] + bunkers
    return player, enemies, bunkers, objects, ufo

#the game loop
def main():
    delta = 0.0

    player, enemies, bunkers, objects, ufo = reset_game()

    #set global variables
    global game_state, score, level, highscore_checked, death_sound_played

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()             #used for direct player controls
        key_up = pygame.key.get_just_released()     #used for menu buttons, to avoid duplicate inputs
        key_down = pygame.key.get_just_pressed()

        if game_state == game_playing:              #running the game
            DISPLAY_SURFACE.fill(BLACK)            

            if key_down[K_SPACE] and not player.player_killed:               #calls shoot function in player object
                bullet_player = player.shoot(objects)
                if bullet_player:
                    objects.append(bullet_player)

            bullet_enemy = enemies.shoot(delta, score, objects)
            if bullet_enemy:
                objects.append(bullet_enemy)        
                
            enemies.bunker_collision(bunkers)       #Check collision between enemies and bunkers
            enemies.player_collision(player)        #Check collision between enemies and player

            for obj in objects:                     #update all game objects every frame
                obj.update(delta)
                if isinstance(obj, Bullet): #Check bullet collisions and delete when set to dead
                    score += bullet_enemy_collisions(obj, enemies, ufo)
                    bullet_bunker_collisions(obj, bunkers)
                    bullet_player_collisions(obj, player)
                    if obj.dead:
                        objects.remove(obj)
                elif isinstance(obj, Bunker): #Delete bunker when it's set to dead
                    if obj.dead:
                        objects.remove(obj)
                        bunkers.remove(obj)

            if enemies.new_wave == True: # reset bunkers when new wave starts
                for bunker in bunkers:
                    if bunker in objects:
                        objects.remove(bunker)
                bunkers = spawn_bunkers()
                objects.extend(bunkers)
                enemies.new_wave = False

            score_tracker(DISPLAY_SURFACE, score)
            level_tracker(DISPLAY_SURFACE, enemies.current_wave)
            display_lives(DISPLAY_SURFACE, player.lives)

            if player.lives <= 0 and player.respawn_timer > 1:
                game_state = game_over

            for obj in objects:                     #draw all game objects every frame
                obj.draw(DISPLAY_SURFACE)

            pygame.display.update()
            delta = clock.tick(FPS) / 1000.0

        #Game Over screen
        if game_state == game_over:
            if not death_sound_played: # stops all playing sounds
                for i in range(pygame.mixer.get_num_channels()):
                    if i != 7:
                        pygame.mixer.Channel(i).stop()

                DEATH_CHANNEL.play(player_death_sound) # plays the death sound on a different mixer to avoid bugs
                death_sound_played = True
            
            if highscore_checked == False:
                game_over_screen(DISPLAY_SURFACE, score)
                highscore_checked = True    

            #Restart game
            if keys[K_SPACE]:
                player, enemies, bunkers, objects, ufo = reset_game()
                game_state = game_playing
                highscore_checked = False
            
            #Go to main menu
            elif key_up[K_ESCAPE]:
                DISPLAY_SURFACE.fill(BLACK)
                game_state = main_menu

        if game_state == main_menu:                #Main Menu screen
            main_menu_screen(DISPLAY_SURFACE)

            if key_up[K_SPACE]:                    #Start the game
                game_state = game_playing
                player, enemies, bunkers, objects, ufo = reset_game()

            elif keys[K_ESCAPE]:                   #Exit the game
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()