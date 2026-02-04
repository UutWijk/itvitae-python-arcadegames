import pygame
from Space_Invaders.GameObject import GameObject
from pygame.locals import K_LEFT,K_RIGHT
from Space_Invaders.constants import *
# from animated import AnimatedSprite
from Space_Invaders.assets import player_sprite, player_shoot_sound, player_hit_sound, player_dead
from Space_Invaders.Bullet import Bullet

clock = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE.fill(WHITE)

class Player(GameObject):

    #Create player object
    def __init__(self):
        self.player_image = pygame.image.load(player_sprite)
        self.image = self.player_image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image = pygame.transform.scale_by(self.image, GAME_SCALE)
        
        self.rect = self.image.get_rect(left=125 * GAME_SCALE, top=SCREEN_HEIGHT - 150 * GAME_SCALE)
        self.lives = 3

        self.index = 0

        self.images = player_dead
        self.player_killed = False
        self.respawn_timer = 0

        self.speed = 250 * GAME_SCALE #movement speed of the player
        self.respawn()

    
    #Update player object
    def update(self, delta: float):
        pressed_key = pygame.key.get_pressed()
        if self.rect.left > 0 and self.player_killed is False:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-1 * self.speed * delta, 0)
        if self.rect.right < SCREEN_WIDTH and self.player_killed is False:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(self.speed * delta, 0)

        if self.player_killed is True:
            self.respawn_timer += delta

        if self.player_killed is True and self.respawn_timer > 1:               
            if self.lives > 0: self.respawn()
            self.player_killed = False
            self.index = 0



    #Shoots a bullet object from the player object
    def shoot(self, objects: list) -> Bullet:
        #Check if there is already a player bullet on the screen
        bullet_on_screen = False
        for obj in objects:
            if isinstance(obj, Bullet) and obj.type == "player":
                bullet_on_screen = True
                break

        #Create a new bullet if there isn't one already on screen
        if not bullet_on_screen:
            player_shoot_sound.play()
            return Bullet("player", (self.rect.centerx, self.rect.centery), -800 * GAME_SCALE)
        return None
    
    #Draw player object
    def draw(self, surface: pygame.Surface):

        if self.player_killed == True:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 9
            self.image = self.images[self.index]
        
        surface.blit(self.image, self.rect)
        

    def respawn(self):
        self.rect = self.image.get_rect(left=125 * GAME_SCALE, top=SCREEN_HEIGHT - 150 * GAME_SCALE)
        self.respawn_timer = 0
        self.image = self.player_image
        

    def killed(self, lives: int):
        self.lives = lives
        self.player_killed = True
        player_hit_sound.play()
        # if self.lives > 0: self.respawn()
        # AnimatedSprite.update_time_dependent(self.rect, player_dead)



