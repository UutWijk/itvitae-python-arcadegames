import pygame
from pygame.sprite import Sprite, Group
from .player import Player
from .obstacle import Obstacle
from .bullet import Bullet
import random
import os
import sys
from .sounds import Sound

from game import Game

class Asteroids(Game):
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.sounds = Sound()
        
        SCALE = 0.1
        self.start_count = 4
        self.current_count = 4
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ship_image = pygame.image.load(os.path.join(current_dir, "sprites/spaceship_default.png")).convert_alpha()
        self.font = pygame.font.SysFont(os.path.join(current_dir, "fonts/Orbitron-VariableFont_wght.ttf"), 30)
        w, h = ship_image.get_size()
        ship_image = pygame.transform.smoothscale(
            ship_image,
            (int(w * SCALE), int(h * SCALE)))
        self.ship_image = ship_image

        self.game_over = False

        self.bullets = Group()
        self.player = Player(screen.get_width(), screen.get_height(), self.bullets, self.sounds)
        self.obstacles = Group()
        for _ in range(self.current_count):
            self.spawn_obstacle()

    def update(self, dt) -> None:
        self.player.update(dt)
        self.bullets.update(dt)
        self.obstacles.update(dt)


        #collision detection
        if len(self.obstacles) == 0:
            self.current_count += 1
            for _ in range(self.current_count):
                self.spawn_obstacle()
        obstacle_in_center = False
        for obstacle in self.obstacles:    
            if not self.player.invincible:
                if self.player.respawning:
                    if obstacle.pos.distance_to(pygame.Vector2(self.screen.get_width() // 2, self.screen.get_height() // 2)) < 150:
                        obstacle_in_center = True
                else:
                    hit_obstacles = pygame.sprite.spritecollide(
                        self.player, self.obstacles, False, pygame.sprite.collide_mask
                    )
                    if hit_obstacles:
                        self.player.lives -= 1
                        if self.player.lives <= 0:
                            self.game_over = True                    
                        for _ in range(random.randint(3, 6)):
                            self.bullets.add(Bullet(self.player.pos.x, self.player.pos.y, random.uniform(0, 360), lifetime=random.uniform(0.1, 1.0), speed=random.uniform(50, 200), kills=False))
                        self.player.death()
                        
                        # kill the obstacle that hit them                            
                        for obstacle in hit_obstacles:
                            new_obstacles = obstacle.killed()
                            self.sounds.asteroid_break()
                            if new_obstacles:
                                self.obstacles.add(new_obstacles)
            for bullet in self.bullets:
                if pygame.sprite.collide_mask(bullet, obstacle) and bullet.kills:
                    bullet.kill()
                    match obstacle.stage:
                        case 1:
                            self.player.add_score(10)
                        case 2:
                            self.player.add_score(20)
                        case 3:
                            self.player.add_score(50)
                    for _ in range(random.randint(2, 6)):
                        self.bullets.add(Bullet(obstacle.pos.x, obstacle.pos.y, random.uniform(0, 360), lifetime=random.uniform(0.1, 0.6), speed=random.uniform(100, 200), kills=False))
                    new_obstacles = obstacle.killed()
                    self.sounds.asteroid_break()
                    if new_obstacles:
                        self.obstacles.add(new_obstacles)
        if self.player.respawning and not obstacle_in_center and self.player.respawn_timer >= self.player.respawn_duration and self.player.lives > 0:
            self.player.respawn()

    def draw(self) -> None:
        self.screen.fill("#000000")
        self.player.draw(self.screen)
        self.bullets.draw(self.screen)
        self.obstacles.draw(self.screen)
        for _ in range(self.player.lives):
            self.screen.blit(self.ship_image, (10 + _ * 40, 60))
        self.screen.blit(self.font.render(f"Score: {self.player.score}", True, (255, 255, 255)), (10, 10))
        if self.game_over:
            semi_opaque_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            semi_opaque_surface.set_alpha(180)  # Set transparency level (0-255)
            semi_opaque_surface.fill((0, 0, 0))  # Fill with black color
            self.screen.blit(semi_opaque_surface, (0, 0))
            game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            score_text = self.font.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))
            self.screen.blit(score_text, score_rect)
            self.screen.blit(game_over_text, text_rect)

    def spawn_obstacle(self):
        random_x = random.randint(0, self.screen.get_width())
        random_y = random.randint(0, self.screen.get_height())
        if pygame.Vector2(random_x, random_y).distance_to(self.player.pos) < 200:
            self.spawn_obstacle()
        else:
            self.obstacles.add(Obstacle(random_x, random_y, self.screen.get_width(), self.screen.get_height(), 1))

    def reset(self):
        self.game_over = False
        self.bullets.empty()
        self.obstacles.empty()
        self.player.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.player.pos = pygame.Vector2(self.player.rect.center)
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.player.lives = 3
        self.player.score = 0
        self.current_count = self.start_count
        for _ in range(self.current_count):
            self.obstacles.add(Obstacle(
                            random.choice([random.randint(0, self.screen.get_width()//2-200), random.randint(self.screen.get_width()//2+200, self.screen.get_width())]),
                            random.choice([random.randint(0, self.screen.get_height()//2-200), random.randint(self.screen.get_height()//2+200, self.screen.get_height())]),                
                            self.screen.get_width(), self.screen.get_height(), 1))
        