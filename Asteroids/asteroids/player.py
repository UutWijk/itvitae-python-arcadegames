import pygame
import math
from .bullet import Bullet
import os
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, screenwidth, screenheight, bullets, sounds):
        super().__init__()
        SCALE = 0.12
        self.bullets = bullets
        self.sounds = sounds
        self.screenwidth = screenwidth
        self.screenheight = screenheight

        # asset loading
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_default = pygame.image.load(os.path.join(self.current_dir, "sprites/spaceship_default.png"))
        self.image_boosting = pygame.image.load(os.path.join(self.current_dir, "sprites/spaceship_boosting.png"))

        # transforming images for in-game size and orientation
        self.rect = self.image_default.get_rect()
        w, h = self.image_default.get_size()
        self.image_default = pygame.transform.smoothscale(
            self.image_default,
            (int(w * SCALE), int(h * SCALE)))
        self.image_boosting = pygame.transform.smoothscale(
            self.image_boosting,
            (int(w * SCALE), int(h * SCALE)))
        self.image = self.image_default
        self.mask = pygame.mask.from_surface(self.image_default)

        # spawning position and orientation
        self.rect.center = (screenwidth // 2, screenheight // 2)
        self.angle = 0

        # shooting parameters
        self.shoot_delay = 0.2 #seconds between shots
        self.time_since_last_shot = 0

        # floating point vector for position tracking (rects round to int)
        self.pos = pygame.Vector2(self.rect.center)        

        # movement parameters
        self.vel_x = 0
        self.vel_y = 0 
        self.acceleration = 750 
        self.friction = 0.98 # decreases speed over time

        self.lives = 3
        self.score = 0
        
        self.respawning = False
        self.respawn_duration = 1.0  # seconds
        self.respawn_timer = 0.0

        self.beams = {}

        
        self.invincible = False
        self.invincible_duration = 1.0  # seconds
        self.invincible_timer = 0.0
        self.animation_timer = 0


    def update(self, dt, pressed, just_pressed):
        
        
        rotation_speed = 270
        if self.lives > 0 and not self.respawning:
            # Handle Rotation Input
            if pressed["left"]:
                self.angle += rotation_speed * dt
            if pressed["right"]:
                self.angle -= rotation_speed * dt

            # Acceleration
            if pressed["up"]:
                # "thruster" animation flicker
                self.animation_timer += 1
                base_surf = self.image_boosting if (self.animation_timer // 5) % 2 == 0 else self.image_default
                
                # acceleration logic
                rad = math.radians(self.angle)
                self.vel_x += -math.sin(rad) * self.acceleration * dt
                self.vel_y += -math.cos(rad) * self.acceleration * dt
            else:
                base_surf = self.image_default

        # 1. Handle Invincibility
        if self.invincible:
            self.animation_timer += 1
            # blinking animation when invincible
            base_surf = pygame.Surface((1, 1), pygame.SRCALPHA) if (self.animation_timer // 5) % 2 == 0 else self.image_default
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

        # move beams for death animation
        if self.respawning:
            base_surf = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.respawn_timer += dt
            for beam in self.beams.values():
                beam["pos"] += beam["velocity"] * dt                
                beam["angle"] += beam["rotationspeed"] * dt                
                beam["image"] = pygame.transform.rotate(beam["og_image"], beam["angle"])                
                beam["rect"] = beam["image"].get_rect(center=beam["pos"])

        # 4. Update the sprite image and mask
        self.image = pygame.transform.rotate(base_surf, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        # 5. Move and Wrap
        self.pos.x += self.vel_x * dt
        self.pos.y += self.vel_y * dt
        
        # Applying friction
        self.vel_x *= self.friction
        self.vel_y *= self.friction

        # Screen Wrap
        if self.rect.right < 0: self.pos.x = self.screenwidth
        elif self.rect.left > self.screenwidth: self.pos.x = 0
        if self.rect.bottom < 0: self.pos.y = self.screenheight
        elif self.rect.top > self.screenheight: self.pos.y = 0
        
        # Finalize rect position
        self.rect.center = self.pos

        # detect shooting input
        self.time_since_last_shot += dt
        if just_pressed["a"]:
            self.shoot()

        
    def draw(self,surface):
        surface.blit(self.image, self.rect)
        if self.respawning:            
            for beam in self.beams.values():
                surface.blit(beam["image"], beam["rect"])
            


    def shoot(self):
        if self.time_since_last_shot < self.shoot_delay or self.respawning or self.invincible:
            return
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        self.bullets.add(new_bullet)
        self.time_since_last_shot = 0
        self.sounds.laser()

    def death(self):
        self.sounds.ship_impact()
        self.respawning = True
        self.respawn_timer = 0.0
        
        right_raw = pygame.image.load(os.path.join(self.current_dir, "sprites/spaceship_sidebeam.png")).convert_alpha()
        center_raw = pygame.image.load(os.path.join(self.current_dir, "sprites/spaceship_centerbeam.png")).convert_alpha()
        
        w, h = right_raw.get_size()
        cw, ch = center_raw.get_size()
        SCALE = 0.12

        # 2. scale beam images
        rb = pygame.transform.smoothscale(right_raw, (int(w * SCALE), int(h * SCALE))).convert_alpha()
        cb = pygame.transform.smoothscale(center_raw, (int(cw * SCALE), int(ch * SCALE))).convert_alpha()
        lb = pygame.transform.flip(rb, True, False).convert_alpha()

        # dict for relevant beam data
        self.beams = {
            "right": {
                "og_image": rb, 
                "image": rb.copy(),
                "rect": rb.get_rect(center=self.pos),
                "angle": self.angle,
                "pos": pygame.Vector2(self.pos),
                "velocity": pygame.Vector2(random.uniform(-50,50) + 0.2 * self.vel_x, random.uniform(-50,50) + 0.2 * self.vel_y),
                "rotationspeed": random.uniform(0, 100)
            },
            "center": {
                "og_image": cb, 
                "image": cb.copy(),
                "rect": rb.get_rect(center=self.pos),
                "angle": self.angle,
                "pos": pygame.Vector2(self.pos),
                "velocity": pygame.Vector2(random.uniform(-50,50) + 0.2 * self.vel_x, random.uniform(-50,50) + 0.2 * self.vel_y),
                "rotationspeed": random.uniform(0, 100)
            },
            "left": {
                "og_image": lb, 
                "image": lb.copy(),
                "rect": rb.get_rect(center=self.pos),
                "angle": self.angle,
                "pos": pygame.Vector2(self.pos),
                "velocity": pygame.Vector2(random.uniform(-50,50) + 0.2 * self.vel_x, random.uniform(-50,50) + 0.2 * self.vel_y),
                "rotationspeed": random.uniform(0, 100)
            }
        }


    def respawn(self):
        if self.lives > 0:
            self.respawning = False
            self.respawn_timer = 0.0
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            self.pos.x = self.screenwidth // 2
            self.pos.y = self.screenheight // 2
            self.vel_x = 0
            self.vel_y = 0

    def add_score(self, points):
        # prevents points from being gained while already game over
        if self.lives > 0:
            self.score += points

        
