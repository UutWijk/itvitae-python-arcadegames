import pygame
import os

# Initializing Sound class
class Sound:
    def __init__(self):
        # Creating current working directory variable
        cwd = os.path.dirname(os.path.abspath(__file__))

        # Loading in assets
        self.theme1_music = pygame.mixer.Sound(os.path.join(cwd, "assets", "sounds", "pong_theme1.mp3"))
        self.theme2_music = pygame.mixer.Sound(os.path.join(cwd, "assets", "sounds", "pong_theme2.mp3"))

        # Placeholders to keep track of which channel is playing which track
        self.theme1_channel = None
        self.theme2_channel = None

    # Startscreen musical theme method
    def theme1(self):
        # get_busy() checks if the audio is currently playing on that channel
        if self.theme1_channel is None or not self.theme1_channel.get_busy():
            self.theme1_music.set_volume(0.1)
            # play(-1) makes the music loop forever. 2000 is a 2-second 'fade-in'
            self.theme1_channel = self.theme1_music.play(-1, 0, 2000)
    
    # Startscreen fadeout method
    def theme1_fadeout(self):
        if self.theme1_channel and self.theme1_channel.get_busy():
            # fadeout of 1 second
            self.theme1_music.fadeout(1000)
    
    # Background musical theme when playing game method
    def theme2(self):
        if self.theme2_channel is None or not self.theme2_channel.get_busy():
            self.theme2_music.set_volume(0.08)
            self.theme2_channel = self.theme2_music.play(-1, 0, 2000)  

    # Background music stops method
    def theme2_stop(self):
        self.theme2_music.stop()    
