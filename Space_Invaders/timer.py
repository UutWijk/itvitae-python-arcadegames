import pygame
from GameObject import GameObject
from constants import *

font = pygame.font.SysFont("Verdana", 30)

class Timer(GameObject):

    def __init__(self):
        pass

    def update(self, delta):

        self.time = pygame.time.get_ticks()

    def draw(self, surface: pygame.Surface):
       
        seconds = int((self.time - self.time%1000)/1000)
        seconds_display = seconds%60
        minutes = int(seconds/60)
        if seconds_display < 10:
            actual_time = f"{minutes}:0{seconds_display}"
        else:
            actual_time = f"{minutes}:{seconds_display}"
        time_text = font.render(f"Time: [{actual_time}]", True, WHITE)
        surface.blit(time_text, time_text.get_rect(topright=(SCREEN_WIDTH - 10, 5)))


    