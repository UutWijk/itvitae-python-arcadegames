import pygame
import math
from .bullet import Bullet
import os

class UFO(pygame.sprite.Sprite):
    def __init__(self, screenwidth, screenheight, bullets):
        super().__init__()
        SCALE = 0.15
        self.bullets = bullets
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(self.current_dir, "sprites/ufo.png"))
        self.maskimage = pygame.image.load(os.path.join(self.current_dir, "sprites/ufo_mask.png"))
        self.animation_timer = 0
        self.rect = self.image.get_rect()
        w, h = self.image.get_size()
        self.image = pygame.transform.smoothscale(
            self.image,
            (int(w * SCALE), int(h * SCALE)))
        self.maskimage = pygame.transform.smoothscale(
            self.maskimage,
            (int(w * SCALE), int(h * SCALE)))
        self.mask = pygame.mask.from_surface(self.maskimage)
        self.rect.center = (screenwidth // 2, screenheight // 2)
        self.angle = 0
        self.shoot_delay = 0.25 #seconds between shots
        self.time_since_last_shot = 0

        self.pos = pygame.Vector2(self.rect.center)        

        #these are for the acceleration of the player, its used in the update function and used in the up arrow key
        self.vel_x = 0 #track movement
        self.vel_y = 0 #   ^
        self.acceleration = 750 #how fast the ship speeds up
        self.friction = 0.98 #slows player slightly to prevent high speeds

        self.lives = 3
        self.invincible = False
        self.invincible_duration = 1.0  # seconds
        self.invincible_timer = 0.0


    def update(self, dt):


        # 2. Handle Rotation Input
        rotation_speed = 270
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.angle += rotation_speed * dt
        if pressed_keys[pygame.K_RIGHT]:
            self.angle -= rotation_speed * dt

        # 3. Determine base image (Animation) and apply rotation
        # Use a local variable so we don't destroy our source images
        if pressed_keys[pygame.K_UP]:
            self.animation_timer += 1
            # Toggle between default and boosting for a flicker effect
            base_surf = self.image_boosting if (self.animation_timer // 5) % 2 == 0 else self.image_default
            
            # Acceleration logic
            rad = math.radians(self.angle)
            self.vel_x += -math.sin(rad) * self.acceleration * dt
            self.vel_y += -math.cos(rad) * self.acceleration * dt
        else:
            base_surf = self.image_default

        # 1. Handle Invincibility
        if self.invincible:
            self.animation_timer += 1
            # Flicker effect
            base_surf = pygame.Surface((1, 1), pygame.SRCALPHA) if (self.animation_timer // 5) % 2 == 0 else self.image_default
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

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

        self.time_since_last_shot += dt
        if pressed_keys[pygame.K_SPACE]:
            self.shoot()
        
    def draw(self,surface):
        surface.blit(self.image, self.rect)

    def shoot(self):
        if self.time_since_last_shot < self.shoot_delay:
            return
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        self.bullets.add(new_bullet)
        self.time_since_last_shot = 0