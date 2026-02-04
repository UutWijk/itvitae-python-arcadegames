from game import Game
from Space_Invaders.Player import Player
from Space_Invaders.Bunker import Bunker, spawn_bunkers
from Space_Invaders.enemy import EnemiesContainer
from Space_Invaders.constants import *
from Space_Invaders.Bullet import Bullet, bullet_player_collisions, bullet_bunker_collisions, bullet_enemy_collisions
from Space_Invaders.assets import player_death_sound
from Space_Invaders.UI import *
from Space_Invaders.ufo import Ufo
import pygame
from pygame.locals import K_a, K_b

class SpaceInvaders(Game):
    def __init__(self, screen):
        super().__init__(screen)

        self.clock = pygame.time.Clock()

        self.screen = screen
        screen.fill(BLACK)
        print("made black")
        pygame.display.set_caption("Space Invaders")

        self.score = 0
        self.highscore_checked = False
        self.death_sound_played = False
        self.DEATH_CHANNEL = pygame.mixer.Channel(7) # exists to avoid bugs when playing death sound

        #instance game state variables
        self.game_playing = 0
        self.game_over = 1
        self.main_menu = 2

        #initial game state
        self.game_state = self.main_menu

        self.player, self.enemies, self.bunkers, self.objects, self.ufo = self.reset_game()

        
    #starts and restarts the game loop
    def reset_game(self):
        self.score = 0
        self.highscore_checked = False
        self.death_sound_played = False

        #initialise all game objects
        player = Player()
        enemies = EnemiesContainer()
        ufo = Ufo()
        bunkers = spawn_bunkers()

        self.clock.tick()

        objects = [player, enemies, ufo] + bunkers
        return player, enemies, bunkers, objects, ufo
    
    def update(self, dt):      
        # for event in pygame.event.get():
        #     if event.type == QUIT:
        #         self.next_state = "MENU"
        self.keys = pygame.key.get_pressed()             #used for direct player controls
        self.key_up = pygame.key.get_just_released()     #used for menu buttons, to avoid duplicate inputs
        self.key_down = pygame.key.get_just_pressed()

        if self.game_state == self.game_playing:              #running the game
            self.screen.fill(BLACK)            

            if self.key_down[K_a] and not self.player.player_killed:               #calls shoot function in player object
                self.bullet_player = self.player.shoot(self.objects)
                if self.bullet_player:
                    self.objects.append(self.bullet_player)

            self.bullet_enemy = self.enemies.shoot(dt, self.score, self.objects)
            if self.bullet_enemy:
                self.objects.append(self.bullet_enemy)        
                
            self.enemies.bunker_collision(self.bunkers)       #Check collision between enemies and bunkers
            self.enemies.player_collision(self.player)        #Check collision between enemies and player

            for obj in self.objects:                     #update all game objects every frame
                obj.update(dt)
                if isinstance(obj, Bullet): #Check bullet collisions and delete when set to dead
                    self.score += bullet_enemy_collisions(obj, self.enemies, self.ufo)
                    bullet_bunker_collisions(obj, self.bunkers)
                    bullet_player_collisions(obj, self.player)
                    if obj.dead:
                        self.objects.remove(obj)
                elif isinstance(obj, Bunker): #Delete bunker when it's set to dead
                    if obj.dead:
                        self.objects.remove(obj)
                        self.bunkers.remove(obj)

            if self.enemies.new_wave == True: # reset bunkers when new wave starts
                for bunker in self.bunkers:
                    if bunker in self.objects:
                        self.objects.remove(bunker)
                self.bunkers = spawn_bunkers()
                self.objects.extend(self.bunkers)
                self.enemies.new_wave = False

            score_tracker(self.screen, self.score)
            level_tracker(self.screen, self.enemies.current_wave)
            display_lives(self.screen, self.player.lives)

            if self.player.lives <= 0 and self.player.respawn_timer > 1:
                self.game_state = self.game_over

            for obj in self.objects:                     #draw all game objects every frame
                obj.draw(self.screen)

            # pygame.display.update()
            dt = self.clock.tick(FPS) / 1000.0

        #Game Over screen
        if self.game_state == self.game_over:
            if not self.death_sound_played: # stops all playing sounds
                for i in range(pygame.mixer.get_num_channels()):
                    if i != 7:
                        pygame.mixer.Channel(i).stop()

                self.DEATH_CHANNEL.play(player_death_sound) # plays the death sound on a different mixer to avoid bugs
                self.death_sound_played = True
            
            if self.highscore_checked == False:
                game_over_screen(self.screen, self.score)
                self.highscore_checked = True    

            #Restart game
            if self.key_down[K_a]:
                self.player, self.enemies, self.bunkers, self.objects, self.ufo = self.reset_game()
                self.game_state = self.game_playing
                self.highscore_checked = False
            
            #Go to main menu
            elif self.key_down[K_b]:
                self.screen.fill(BLACK)
                self.game_state = self.main_menu

        if self.game_state == self.main_menu:                #Main Menu screen
            main_menu_screen(self.screen)

            if self.key_down[K_a]:                    #Start the game
                self.game_state = self.game_playing
                self.player, self.enemies, self.bunkers, self.objects, self.ufo = self.reset_game()

            elif self.keys[K_b]:                   #Exit the game
                self.next_state = "MENU"