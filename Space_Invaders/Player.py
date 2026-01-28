import pygame
from GameObject import GameObject
from pygame.locals import K_LEFT,K_RIGHT
from constants import *
from assets import player_sprite, player_shoot_sound
from Bullet import Bullet

clock = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE.fill(WHITE)

class Player(GameObject):

    def __init__(self):
        self.image = pygame.image.load(player_sprite)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(left=100, top=SCREEN_HEIGHT - 130)

        self.speed = 250 #movement speed of the player

    def update(self, delta: float):

        pressed_key = pygame.key.get_pressed()
        if 26 < self.rect.x:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-1 * self.speed * delta, 0)
        if self.rect.x < SCREEN_WIDTH - 26:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(self.speed * delta, 0)

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
            return Bullet("player", (self.rect.x, self.rect.y), -800)
        return None

    def draw(self, surface: pygame.Surface):
        image_rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
        surface.blit(self.image, image_rect)

