import os
import pygame

pygame.init()

player_sprite = os.path.join(os.path.dirname(__file__), "assets", "player.png")
first_alien_sprite = os.path.join(os.path.dirname(__file__), "assets", "alien_row_1.png")
second_alien_sprite = os.path.join(os.path.dirname(__file__), "assets", "alien_row_2.png")
third_alien_sprite = os.path.join(os.path.dirname(__file__), "assets", "alien_row_3.png")
bunker_sprite = os.path.join(os.path.dirname(__file__), "assets", "bunker.png")
enemy_bullet_sprite = os.path.join(os.path.dirname(__file__), "assets", "enemy_bullet.png")
ufo_sprite = os.path.join(os.path.dirname(__file__), "assets", "ufo.png")


# sounds
player_shoot_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "player_shoot.mp3"))
player_destroyed_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "player_destroyed1.mp3"))
explosion_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "explosion1.mp3"))
alien_hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "alien_hit1.mp3"))
alien_move_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "alien_move2.mp3"))
ufo_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "UFO_sound.mp3"))