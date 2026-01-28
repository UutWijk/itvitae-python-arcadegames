import pygame
import os

class Sound:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.theme1_music = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "pong_theme1.mp3"))
        self.theme2_music = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "pong_theme2.mp3"))

        self.theme1_channel = None
        self.theme2_channel = None

    def theme1(self):
        if self.theme1_channel is None or not self.theme1_channel.get_busy():
            self.theme1_music.set_volume(0.08)
            self.theme1_channel = self.theme1_music.play(-1, 0, 2000)
    
    def theme1_fadeout(self):
        if self.theme1_channel and self.theme1_channel.get_busy():
            self.theme1_music.fadeout(1000)
    
    def theme2(self):
        if self.theme2_channel is None or not self.theme2_channel.get_busy():
            self.theme2_music.set_volume(0.05)
            self.theme2_channel = self.theme2_music.play(-1, 0, 2000)  

    def theme2_stop(self):
        self.theme2_music.stop()    
