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
        
        # asset loading
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(self.current_dir, "sprites/ufo.png"))
        self.maskimage = pygame.image.load(os.path.join(self.current_dir, "sprites/ufo_mask.png"))
        self.animation_timer = 0
        self.rect = self.image.get_rect()

        # transforming image and mask to scale
        w, h = self.image.get_size()
        self.image = pygame.transform.smoothscale(
            self.image,
            (int(w * SCALE), int(h * SCALE)))
        self.maskimage = pygame.transform.smoothscale(
            self.maskimage,
            (int(w * SCALE), int(h * SCALE)))
        self.mask = pygame.mask.from_surface(self.maskimage)

        # movement parameters
        self.speed = 200
        self.angle = random.randrange(0, 360)

        # generate random entry side
        def randomizespawnpoint():
            valid = False
            while not valid:
                side = random.choice(['top', 'bottom', 'left', 'right'])
                if side == 'top':
                    start_pos = pygame.Vector2(random.randrange(100, screenwidth-100), -50)
                    start_angle = random.randrange(255, 285) 
                elif side == 'bottom':
                    start_pos = pygame.Vector2(random.randrange(100, screenwidth-100), screenheight + 50)
                    start_angle = random.randrange(75, 105)
                elif side == 'left':
                    start_pos = pygame.Vector2(-50, random.randrange(100, screenheight-100))
                    start_angle = random.randrange(-15, 15)
                elif side == 'right':
                    start_pos = pygame.Vector2(screenwidth + 50, random.randrange(100, screenheight - 100))
                    start_angle =  random.randrange(165, 195)

                # check asteroid distance
                if all(start_pos.distance_to(obs.pos) > 300 for obs in obstacles):
                    return start_pos, start_angle

        # "turning" to dodge asteroids
        self.turnclockwise = False
        self.turncounterclockwise = False
        self.turntimer = 0.0

        # movement parameters
        self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle)
        self.shoot_delay = 1.5 # seconds between shots
        self.time_since_last_shot = 0

        self.flicker_timer = 0
        self.hit = False
        x, y = randomizespawnpoint()
        self.pos = pygame.Vector2(x, y)


    def update(self, dt, player, obstacles):
        # dampen entry sound over time
        self.sounds.fade_ufo(dt / 4)
        if player.score > 2000:
            self.speed = 175 + player.score / 80
        # asteroid dodging logic
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

        # generic position update
        self.pos += self.velocity * dt
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        # death animation
        if self.hit:
            self.flicker_timer += dt
            if self.flicker_timer % 0.1 < 0.05:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
            if self.flicker_timer >= 0.5:
                self.death()

        # Use half of the rect's width and height (original image) for wrapping
        half_w = self.rect.width / 2
        half_h = self.rect.height / 2

        # Wrap horizontally
        if self.pos.x < -half_w:
            self.pos.x = self.screenwidth + half_w
        elif self.pos.x > self.screenwidth + half_w:
            self.pos.x = -half_w

        # Wrap vertically
        if self.pos.y < -half_h:
            self.pos.y = self.screenheight + half_h
        elif self.pos.y > self.screenheight + half_h:
            self.pos.y = -half_h
        
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

        # if player score is over 2000, shoot more accurately 
        # (4000 is twice as accurate, 6000 three times, etc.)
        if player.score < 2000:
            shoot_angle += random.randrange(-45,45)
        else:
            shoot_angle += random.randrange(-45,45) * 2000 / player.score
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, -shoot_angle, lifetime=2, speed=400, kills=True, ufo=True)
        self.bullets.add(new_bullet)
        self.time_since_last_shot = 0
    
    def death(self):
        self.sounds.fade_ufo(0.5)
        self.kill()