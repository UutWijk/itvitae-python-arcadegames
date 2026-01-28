import pygame
import os
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

pygame.init()


class Player:
    def __init__(self, location: pygame.Vector2) -> None:
        self.pos = location
        if os.name == "posix":
            self.path = os.path.join("..", "assets", "Frog.png")
        elif os.name == "nt":
            self.path = os.path.join("assets", "Frog.png")
        else:
            print("Error with asset loading, please report")
            sys.exit()
        # if os.name == "posix":
        #    self.sprite = pygame.image.load("../assets/Frog.png")
        # elif os.name == "nt":
        #    self.sprite = pygame.image.load("..\\assets\\Frog.png")
        self.sprite = pygame.image.load(self.path)
        self.rot_sprite = self.sprite
        self.rect = self.sprite.get_rect(topleft=self.pos)

        self._score = 0
        self._score_marker = self.pos.y
        self.is_alive = True
        self.game_over = False

    def update(self):
        if self.game_over:
            return
        else:
            keys = pygame.key.get_just_pressed()  # input handling happens within the update function for now. We could implement an input handling script later and pass it as a parameter.
            if keys[pygame.K_w]:
                self.pos.y -= TILE_SIZE
                self.rot_sprite = pygame.transform.rotate(self.sprite, 0)
            if keys[pygame.K_s]:
                self.rot_sprite = pygame.transform.rotate(self.sprite, 180)
                self.pos.y += TILE_SIZE
                if self.pos.y > SCREEN_HEIGHT - self.rect.width:
                    self.pos.y -= TILE_SIZE
            if keys[pygame.K_a]:
                self.rot_sprite = pygame.transform.rotate(self.sprite, 90)
                self.pos.x -= TILE_SIZE
                if self.pos.x < 0:
                    self.pos.x += TILE_SIZE
            if keys[pygame.K_d]:
                self.rot_sprite = pygame.transform.rotate(self.sprite, -90)
                self.pos.x += TILE_SIZE
                if self.pos.x > SCREEN_WIDTH - self.rect.width:
                    self.pos.x -= TILE_SIZE
            self.rect = pygame.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
            self.update_score()

    def move_with_log(self, log_speed):
        self.pos.x += log_speed

        if self.pos.x < 0:
            self.pos.x = 0
            self.is_alive = False  # Of direct resetten
        elif self.pos.x > SCREEN_WIDTH - TILE_SIZE:  # 64 = player breedte
            self.pos.x = SCREEN_WIDTH - TILE_SIZE
            self.is_alive = False

        self.rect.x = int(self.pos.x)

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, "green", self.rect)
        screen.blit(self.rot_sprite, self.pos)

    def get_score(self) -> int:
        return self._score

    def update_score(self):
        if self.pos.y < self._score_marker:
            self._score += 1
            self._score_marker = self.pos.y

    def reset_player(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - TILE_SIZE)
        self.rect.topleft = (self.pos.x, self.pos.y)  # Update rect position
        self._score_marker = self.pos.y
        self.game_over = False
        self.is_alive = True

    def reset_after_death(self):
        self._score = 0
        self.pos = pygame.Vector2(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - TILE_SIZE
        )  # reset position
        self.rect.topleft = (self.pos.x, self.pos.y)
        self._score_marker = self.pos.y
        self.is_alive = True
        self.game_over = False

    def set_game_over(self):
        self.game_over = True
