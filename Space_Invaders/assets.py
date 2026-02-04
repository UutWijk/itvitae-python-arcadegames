import os
import pygame

pygame.init()

# sprites
player_sprite = os.path.join(os.path.dirname(__file__), "assets", "player.png")
first_alien_sprite = os.path.join(os.path.dirname(__file__), "assets", "alien_row_1.png")
second_alien_sprite = os.path.join(os.path.dirname(__file__), "assets", "alien_row_2.png")
third_alien_sprite = os.path.join(os.path.dirname(__file__), "assets", "alien_row_3.png")
first_alien_sprite_2 = os.path.join(os.path.dirname(__file__), "assets", "alien_row_1_2.png")
second_alien_sprite_2 = os.path.join(os.path.dirname(__file__), "assets", "alien_row_2_2.png")
third_alien_sprite_2 = os.path.join(os.path.dirname(__file__), "assets", "alien_row_3_2.png")
bunker_sprite = os.path.join(os.path.dirname(__file__), "assets", "bunker.png")
enemy_bullet_sprite = os.path.join(os.path.dirname(__file__), "assets", "enemy_bullet.png")
ufo_sprite = os.path.join(os.path.dirname(__file__), "assets", "ufo.png")

# death animation
player_dead1 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead1.png"))
player_dead2 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead2.png"))
player_dead3 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead3.png"))
player_dead4 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead4.png"))
player_dead5 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead5.png"))
player_dead6 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead6.png"))
player_dead7 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead7.png"))
player_dead8 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead8.png"))
player_dead9 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead9.png"))
player_dead10 = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "player_dead_animation", "player_dead10.png"))

#list of frames
player_dead = [player_dead1, player_dead2, player_dead3, player_dead4, player_dead5, player_dead6, player_dead7, player_dead8, player_dead9, player_dead10]


# sounds
player_shoot_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "player_shoot.mp3"))
player_death_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "player_destroyed1.mp3"))
player_hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "player_destroyed2.mp3"))
explosion_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "explosion1.mp3"))
alien_hit_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "alien_hit1.mp3"))
alien_move_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "alien_move2.mp3"))
ufo_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "assets", "audio", "UFO_sound_cut.mp3"))