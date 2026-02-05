import pygame
import math
import random
from .bullet import Bullet
from .sounds import Sound
import os

class UFO(pygame.sprite.Sprite):
    def __init__(self, screenwidth, screenheight, bullets, obstacles, sounds):
        super().__init__()
        self.sounds = sounds
        self.sounds.ufo()
        SCALE = 0.125
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

        self.speed = 200
        self.angle = random.randrange(0, 360)
        sides = ['top', 'bottom', 'left', 'right']
        def randomizespawnpoint():
            side = random.choice(sides)
            if side == 'top':
                self.rect.center = (random.randrange(0, screenwidth), 0)
            elif side == 'bottom':
                self.rect.center = (random.randrange(0, screenwidth), screenheight)
            elif side == 'left':
                self.rect.center = (0, random.randrange(0, screenheight))
            elif side == 'right':
                self.rect.center = (screenwidth, random.randrange(0, screenheight))
            self.angle = 0
            
            if side == 'top':
                self.angle = random.randrange(150, 210)
            elif side == 'bottom':
                self.angle = random.randrange(-30, 30)
            elif side == 'left':
                self.angle = random.randrange(-120, -60)
            elif side == 'right':
                self.angle = random.randrange(60, 120)
            for obstacle in obstacles:
                if pygame.Vector2(self.rect.center).distance_to(obstacle.pos) < 300:
                    randomizespawnpoint()
        randomizespawnpoint()

        self.turnclockwise = False
        self.turncounterclockwise = False
        self.turntimer = 0.0
        self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle)
        self.shoot_delay = 1 #seconds between shots
        self.time_since_last_shot = 0

        self.flicker_timer = 0
        self.hit = False

        self.pos = pygame.Vector2(self.rect.center)


    def update(self, dt, player, obstacles):

        self.sounds.fade_ufo(dt / 4)
        if not (self.turnclockwise or self.turncounterclockwise):
            self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle)
            for obstacle in obstacles:
                distance = self.pos.distance_to(obstacle.pos)
                if distance < 150:
                    angle = self.pos.angle_to(obstacle.pos)
                    if angle - self.angle < 90:
                        if self.angle > angle:
                            self.turnclockwise = True
                        else:
                            self.turncounterclockwise = True
        else:
            self.turntimer += dt
            if self.turntimer > 0.5:
                self.turnclockwise = False
                self.turncounterclockwise = False
            if self.turnclockwise:
                self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle - 60)
            if self.turncounterclockwise:
                self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle + 60)
        self.pos += self.velocity * dt
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        if self.hit:
            self.flicker_timer += dt
            if self.flicker_timer % 0.1 < 0.05:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
            if self.flicker_timer >= 0.5:
                self.death()

        # Screen Wrap
        if self.rect.right < 0: self.pos.x = self.screenwidth
        elif self.rect.left > self.screenwidth: self.pos.x = 0
        if self.rect.bottom < 0: self.pos.y = self.screenheight
        elif self.rect.top > self.screenheight: self.pos.y = 0
        
        # Finalize rect position
        self.rect.center = self.pos

        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.shoot_delay:
            self.shoot(player)
            

        
    def draw(self,surface):
        surface.blit(self.image, self.rect)

    def shoot(self, player):
        if self.time_since_last_shot < self.shoot_delay:
            return
        shoot_angle = math.degrees(math.atan2(
            player.pos.y - self.rect.centery,
            player.pos.x - self.rect.centerx))
        shoot_angle += 90
        if player.score < 1000:
            shoot_angle += random.randrange(-45,45)
        else:
            shoot_angle += random.randrange(-45,45) * 1000 / player.score
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, -shoot_angle, lifetime=3, speed=400, kills=True, ufo=True)
        self.bullets.add(new_bullet)
        self.time_since_last_shot = 0
    
    def death(self):
        self.sounds.fade_ufo(0.5)
        self.kill()