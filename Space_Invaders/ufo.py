import pygame
from Space_Invaders.GameObject import GameObject
from Space_Invaders.constants import *
from Space_Invaders.assets import ufo_sprite, ufo_sound
from random import randint

class Ufo(GameObject):

    #Create UFO object
    def __init__(self):
        self.image = pygame.image.load(ufo_sprite)
        self.image = pygame.transform.scale_by(self.image, GAME_SCALE)
        self.speed = 200 * GAME_SCALE
        self.respawn()

    #Update UFO object
    def update(self, delta):

        #Play sound when UFO comes onto the screen
        if self.direction == 1:
            if self.rect.right >= 0 and self.sound_playing == False:
                ufo_sound.play()
                self.sound_playing = True
            #Reset the UFO when it leaves the screen
            elif self.rect.left > SCREEN_WIDTH:
                self.respawn()
        
        #Play sound when UFO comes onto the screen
        elif self.direction == -1:
            if self.rect.left <= SCREEN_WIDTH and self.sound_playing == False:
                 ufo_sound.play()
                 self.sound_playing = True
            #Reset the UFO when it leaves the screen
            elif self.rect.right < 0:
                self.respawn()

        #Move the UFO in the current directions
        self.rect.move_ip(self.speed * self.direction * delta, 0)

    #Draw UFO object
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    #When the UFO is hit by a bullet, reset it and increment score
    def hit(self)-> int:
        score_index = randint(0,15) #Score are weighted, like in the original arcade game
        if score_index < 5:
            score = 50
        elif score_index < 13:
            score = 100
        elif score_index < 15:
            score = 150
        else:
            score = 300
        self.respawn()
        ufo_sound.stop()
        return score

    #Respawn the UFO off screen so it takes ~10sec to come back onto the screen
    def respawn(self):
        self.sound_playing = False

        if randint(0, 1) == 1:
            self.direction = 1
            y = self.speed * -10
        else:
            self.direction = -1
            y = SCREEN_WIDTH + self.speed * 10
        
        self.rect = self.image.get_rect(center=(y, 60 * GAME_SCALE))
