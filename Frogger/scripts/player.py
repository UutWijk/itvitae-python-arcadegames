import pygame
import os
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, DEVELOPMENT_MODE

pygame.init()


class Player:
    def __init__(self, location: pygame.Vector2) -> None:
        self.pos = location
        script_dir = os.path.dirname(__file__)
        if os.name == "posix":
            self.path = os.path.join("..", "assets", "Frog.png")
            self.hop_sound_path = os.path.join("..", "assets", "sounds", "Hop.wav")
        elif os.name == "nt":
            self.path = os.path.join("assets", "Frog.png")
            self.hop_sound_path = os.path.join("assets", "sounds", "Hop.wav")
        else:
            print("Error with asset loading, please report")
            sys.exit()
            # if os.name == "posix":
            #    self.sprite = pygame.image.load("../assets/Frog.png")
            # elif os.name == "nt":
            #    self.sprite = pygame.image.load("..\\assets\\Frog.png")
        splash_dir = os.path.join(script_dir, "..", "assets", "FrogDrown")
        self.splash_anim = [
            pygame.image.load(os.path.join(splash_dir, "FrogDrown_0001.png")),
            pygame.image.load(os.path.join(splash_dir, "FrogDrown_0002.png")),
            pygame.image.load(os.path.join(splash_dir, "FrogDrown_0003.png")),
            pygame.image.load(os.path.join(splash_dir, "FrogDrown_0004.png")),
            pygame.image.load(os.path.join(splash_dir, "FrogDrown_0005.png")),
            pygame.image.load(os.path.join(splash_dir, "FrogDrown_0006.png")),
        ]
        crash_dir = os.path.join(script_dir, "..", "assets", "FrogCrash")
        self.crash_anim = [
            pygame.image.load(os.path.join(crash_dir, "FrogCrash_0001.png")),
            pygame.image.load(os.path.join(crash_dir, "FrogCrash_0002.png")),
            pygame.image.load(os.path.join(crash_dir, "FrogCrash_0003.png")),
            pygame.image.load(os.path.join(crash_dir, "FrogCrash_0004.png")),
        ]
        self.sprite = pygame.image.load(self.path)
        self.rot_sprite = self.sprite
        self.curr_sprite = self.sprite
        self.rect = self.sprite.get_rect(topleft=self.pos)
        self.hop_sound = pygame.Sound(self.hop_sound_path)

        self._score = 0
        self._score_multiplier = 1.0
        self._score_marker = self.pos.y
        self._lives = 3
        self.is_alive = True
        self.game_over = False
        self.freeze = False
        self.dt = 0.0

        self.dying = False
        self.dead_timer = 0.0
        self.dying_type = "None"

    def update(self, dt: float):
        self.dt = dt
        if self.dying:
            if self.dying_type == "splash":
                self.splash_death()
            elif self.dying_type == "crash":
                self.crash_death()
            return
        if self.game_over or self.freeze:
            return
        else:
            keys = pygame.key.get_just_pressed()  # input handling happens within the update function for now. We could implement an input handling script later and pass it as a parameter.
            if keys[pygame.K_w]:
                self.pos.y -= TILE_SIZE
                self.rot_sprite = pygame.transform.rotate(self.sprite, 0)
                self.hop_sound.play()
                self._score_multiplier += 0.1
            if keys[pygame.K_s]:
                self.rot_sprite = pygame.transform.rotate(self.sprite, 180)
                self.pos.y += TILE_SIZE
                if self.pos.y > SCREEN_HEIGHT - self.rect.width:
                    self.pos.y -= TILE_SIZE
                self._score_multiplier = 1.0
                self.hop_sound.play()
            if keys[pygame.K_a]:
                self.rot_sprite = pygame.transform.rotate(self.sprite, 90)
                self.pos.x -= TILE_SIZE
                if self.pos.x < 0:
                    self.pos.x += TILE_SIZE
                self.hop_sound.play()
            if keys[pygame.K_d]:
                self.rot_sprite = pygame.transform.rotate(self.sprite, -90)
                self.pos.x += TILE_SIZE
                if self.pos.x > SCREEN_WIDTH - self.rect.width:
                    self.pos.x -= TILE_SIZE
                self.hop_sound.play()
            # skip level
            if keys[pygame.K_p] and DEVELOPMENT_MODE:
                for i in range(int(self.pos.y // TILE_SIZE) - 1):
                    self._score += int(100 * self._score_multiplier)
                    self._score_multiplier += 0.1
                self.pos.y = 0

            HITBOX_SHRINK = 6
            self.rect = pygame.Rect(
                self.pos.x + HITBOX_SHRINK,
                self.pos.y + HITBOX_SHRINK,
                TILE_SIZE - 2 * HITBOX_SHRINK,  # 52x wide
                TILE_SIZE - 2 * HITBOX_SHRINK,  # 52px high (was 64x64)
            )
            self.curr_sprite = self.rot_sprite
            # self.rect = pygame.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
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
        screen.blit(self.curr_sprite, self.pos)

    def get_score(self) -> int:
        return self._score

    def update_score(self):
        if self.pos.y < self._score_marker:
            self._score += int(100 * self._score_multiplier)
            # self._score_multiplier += 0.1
            self._score_marker = self.pos.y

    def get_lives(self) -> int:
        return self._lives

    def lose_live(self):
        self._lives -= 1
        self._score_multiplier = 1.0

    def reset_player(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - TILE_SIZE)
        self.rect.topleft = (self.pos.x, self.pos.y)  # Update rect position
        self._score_marker = self.pos.y
        self.game_over = False
        self.is_alive = True

    def get_modifier(self):
        return str(round(self._score_multiplier, 2))

    def reset_after_death(self):
        self._score = 0
        self._lives = 3
        self.pos = pygame.Vector2(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - TILE_SIZE
        )  # reset position
        self.rect.topleft = (self.pos.x, self.pos.y)
        self._score_marker = self.pos.y
        self.is_alive = True
        self.game_over = False

    def splash_death(self):
        self.dead_timer += self.dt
        if self.dead_timer < 0.1:
            self.curr_sprite = self.splash_anim[0]
        elif self.dead_timer < 0.2:
            self.curr_sprite = self.splash_anim[1]
        elif self.dead_timer < 0.3:
            self.curr_sprite = self.splash_anim[2]
        elif self.dead_timer < 0.4:
            self.curr_sprite = self.splash_anim[3]
        elif self.dead_timer < 0.5:
            self.curr_sprite = self.splash_anim[4]
        elif self.dead_timer < 1.1:
            self.curr_sprite = self.splash_anim[5]
        else:
            self.dying = False
            self.dying_type = "None"
            self.dead_timer = 0.0

    def crash_death(self):
        self.dead_timer += self.dt
        if self.dead_timer < 0.1:
            self.curr_sprite = self.crash_anim[0]
        elif self.dead_timer < 0.2:
            self.curr_sprite = self.crash_anim[1]
        elif self.dead_timer < 0.3:
            self.curr_sprite = self.crash_anim[2]
        elif self.dead_timer < 1.1:
            self.curr_sprite = self.crash_anim[3]
        else:
            self.dying = False
            self.dying_type = "None"
            self.dead_timer = 0.0

    def set_dying_type(self, type: str):
        self.dying = True
        self.dying_type = type

    def set_game_over(self):
        self.game_over = True

    def set_freeze(self, state: bool):
        self.freeze = state
