import pygame
from GameObject import GameObject
from constants import *
from assets import enemy_bullet_sprite

class Bullet(GameObject):
    def __init__(self, type:str, pos:tuple, speed:int):
        self.type = type

        #Set attributes of player bullet
        if self.type == "player":
            self.image = pygame.Surface((4, 16))
            self.image.fill(WHITE)
        
        #Set attributes of enemy bullets
        else:
            self.image = pygame.image.load(enemy_bullet_sprite)
        
        #Create the bullet
        self.image = pygame.transform.scale_by(self.image, GAME_SCALE)
        self.speed = speed
        self.rect = self.image.get_rect(center=pos)
        self.dead = False

    def update(self, delta: float):
        self.rect.y += self.speed * delta
        if self.rect.bottom < 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dead = True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

def bullet_enemy_collisions(bullet: Bullet, enemies: GameObject, ufo: GameObject) -> int:
    if bullet.type != "player": return 0
    
    score = enemies.bullet_collision(bullet)
    if not score:
        if bullet.rect.colliderect(ufo.rect):
            score = ufo.hit()

    if score:
        bullet.dead = True
        return score
    else:
        return 0

def bullet_bunker_collisions(bullet: Bullet, bunkers: GameObject) -> None:
    hit_bunker = pygame.sprite.spritecollideany(bullet, bunkers)
    if hit_bunker is not None:
        hit_bunker.destruction(hit_bunker.lives - 1)
        # hit_bunker.damage()
        bullet.dead = True

def bullet_player_collisions(bullet: Bullet, player: GameObject) -> None:
    if bullet.type == "enemy" and bullet.rect.colliderect(player.rect):
        player.killed(player.lives - 1)
        bullet.dead = True
