import pygame
from Space_Invaders.constants import *
from Space_Invaders.GameObject import GameObject
from Space_Invaders.assets import first_alien_sprite, first_alien_sprite_2, second_alien_sprite, second_alien_sprite_2, third_alien_sprite, third_alien_sprite_2, alien_hit_sound, alien_move_sound
from Space_Invaders.Bullet import Bullet
from random import randint

class Enemy:
    #Create an individual enemy with the provided location and size
    def __init__(self, row:int, x:int, y:int):

        #set enemy type based on the row
        if row == 0:
            self.type = 3
            self.sprite = third_alien_sprite
            self.sprite2 = third_alien_sprite_2
        elif row <= 2:
            self.type = 2
            self.sprite = second_alien_sprite
            self.sprite2 = second_alien_sprite_2
        else:
            self.type = 1
            self.sprite = first_alien_sprite
            self.sprite2 = first_alien_sprite_2

        #Create the enemy
        self.image = pygame.image.load(self.sprite)
        self.image = pygame.transform.scale_by(self.image, GAME_SCALE)
        self.rect = self.image.get_rect(left=x,top=y)
        self.move_counter = 0

    #Move the enemy object
    def move(self, x: int, y: int):
        self.rect.move_ip(x, y)
        self.move_counter += 1

    #Draw the enemy on the screen
    def draw(self, surface: pygame.Surface):
        if self.move_counter%2 == 0:
            self.image = pygame.image.load(self.sprite2)
        else:
            self.image = pygame.image.load(self.sprite)
        surface.blit(self.image, self.rect)

class EnemiesContainer(GameObject):
    def __init__(self):
        #Amount of enemy columns and rows
        self.columns = 11
        self.rows = 5
        self.enemies_total = self.rows * self.columns

        #Amount of space reserved for each enemy
        self.enemy_spacing = 60 * GAME_SCALE

        #Set the start location of the enemies
        self.left = 200 * GAME_SCALE
        self.top = 50 * GAME_SCALE

        #Amount the movement delay and speed
        self.speed_start = 15 * GAME_SCALE
        self.interval_start = 1 / 60 * self.enemies_total #In the original game, 1 enemy move per frame at 60fps
        self.speed_down = 40 * GAME_SCALE # how much the enemies move down each time they reach the edge

        #Used for a delay between move sounds
        self.move_skips = 0

        #Delay between shots in seconds
        self.shot_delay_max = 2
        self.shot_delay_min = 0.5
        self.max_score = 3000 #The score at which the lowest shot interval is reached
        self.shot_delay = self.shot_delay_max

        #Create the starting enemies
        self.create_enemies()

        # to keep track of what wave of enemies we are in
        self.new_wave = False
        self.current_wave = 1

    #Create all enemies
    def create_enemies(self):

        #Create container rectangle
        self.rect = pygame.Rect(self.left, self.top, 0, 0)

        #Create all enemies and save in a list
        self.enemies = []
        for r in range(self.rows):
            for c in range(self.columns):
                self.enemies.append(Enemy(r, self.rect.left + c * self.enemy_spacing,
                                          self.top + r * self.enemy_spacing))
                
        #Set the container to the correct size to include all enemies
        self.set_container_size()
        
        #Set the starting variables
        self.enemies_current = self.enemies_total
        self.interval_move = self.interval_start
        self.speed = self.speed_start

        #Start timers for movement and shooting
        self.timer_move = 0.0
        self.timer_shoot = 0.0

    #Handle enemy movement
    def update(self, delta: float):

        #Check if enough time has passed for the enemies to move
        self.timer_move += delta
        if self.timer_move >= self.interval_move:

            #If the next move would exceed the edges of the screen, move down and reverse direction
            if self.rect.right + self.speed > SCREEN_WIDTH or self.rect.left + self.speed < 0:
                delta_y = self.speed_down
                self.speed *= -1

                #If only 1 enemy is left, move faster when going to the right
                if self.enemies_current == 1:
                    if self.speed > 0:
                        self.speed = self.speed_start * 1.5
                    else:
                        self.speed = self.speed_start * -1

            else:
                delta_y = 0

            #Set horizontal movement speed
            delta_x = self.speed

            #Move the container and all enemies
            self.rect.move_ip(delta_x, delta_y)

            #Used to play sound every move, skips sounds depending on enemies left (too fast)
            if self.move_skips > 0:
                self.move_skips -= 1
            else:
                if self.enemies_current > 3:
                    alien_move_sound.play()
                    self.move_skips = 1
                elif self.enemies_current > 1:
                    alien_move_sound.play()
                    self.move_skips = 2
                else:
                    alien_move_sound.play()
                    self.move_skips = 3
                
            #Move all individual enemies
            for enemy in self.enemies:
                enemy.move(delta_x, delta_y)

            #Reset movement timer
            self.timer_move = 0.0

    #Draw all enemies on the screen
    def draw(self, surface: pygame.Surface):
        for enemy in self.enemies:
            enemy.draw(surface)
        
    #Set the container to the smallest size that contains all (remaining) enemies
    def set_container_size(self):

        #Get the extreme left, right, top and bottom values for the remaining enemies
        left, right, top, bottom = (SCREEN_WIDTH, 0, SCREEN_HEIGHT, 0)
        for enemy in self.enemies:
            rect = enemy.rect #.get_rect()
            if rect.left < left: left = rect.left 
            if rect.right > right: right = rect.right
            if rect.top < top: top = self.rect.top
            if rect.bottom > bottom: bottom = rect.bottom 

        #Set the new position and size of the container
        self.rect.update(left, top, right - left, bottom - top)

    #Handle enemy bullet shooting
    def shoot(self, delta:float, score: int, objects:list) -> Bullet:

        #Check if enough time has passed for the enemies to shoot
        self.timer_shoot += delta
        if self.timer_shoot >= self.shot_delay:
            self.timer_shoot = 0.0

            #Fire a new bulelt if there are less than 3 currently on screen
            bullets_on_screen = 0
            for obj in objects:
                if isinstance(obj, Bullet) and obj.type == "enemy":
                    bullets_on_screen += 1
            if bullets_on_screen < 3:

                #Calculate new shot delay based on the current score
                self.shot_delay = self.shot_delay_min + ((self.shot_delay_max - self.shot_delay_min) *
                                                         max(0, (self.max_score - score) / self.max_score))
                
                #Fire bullet from a random enemies' position
                enemy = self.enemies[randint(0, self.enemies_current - 1)]
                speed = 270 * GAME_SCALE if len(self.enemies) > 8 else 340 * GAME_SCALE
                return Bullet("enemy", enemy.rect.center, speed)
                
   #Handle collision between enemies and bullet
    def bullet_collision(self, bullet: Bullet) -> int:

        #Check if a player's bullet collides with an enemy
        enemy = None
        if bullet.type == "player":
            enemy = bullet.rect.collideobjects(self.enemies)

        if enemy:
            #Increment score based on enemy type
            score = enemy.type * 10

            #Delete the enemy that was hit
            self.enemies.remove(enemy)
            alien_hit_sound.play()
            self.enemies_current -= 1

            #Respawn all enemies if the last one died, enemies spawn lower on the screen every time
            if self.enemies_current <= 0:
                if self.top < 210 * GAME_SCALE: self.top += 20 * GAME_SCALE
                self.create_enemies()
                self.new_wave = True
                self.current_wave += 1
                self.move_skips = 0

            else:
                #Resize the container if required
                self.set_container_size()

                #Decrease the movement delay of the remaining enemies
                self.interval_move = self.interval_start * (self.enemies_current /self.enemies_total)
            
        #return the score gained from killing an enemy
            return score

    #Handle collision between enemies and bunkers
    def bunker_collision(self, bunkers: list[GameObject]):
        for bunker in bunkers:
            if bunker.rect.collideobjects(self.enemies):
                bunker.dead = True

    #If enemies reach player y level, set lives to 0 (game over)
    def player_collision(self, player: GameObject):
        if self.rect.bottom >= player.rect.top:
            player.killed(0)
