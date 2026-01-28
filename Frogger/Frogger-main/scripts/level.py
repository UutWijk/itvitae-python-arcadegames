import pygame
import sys
import os
from car_lane import CarLane
from water_lane import WaterLane
from player import Player
from gameover import GameOver
from highscore import HighScore
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Level:
    def __init__(self, player: Player, game_over: GameOver, highscore: HighScore = None):
        self.player = player
        self.gameover = game_over
        self.highscore = highscore
        self.startfinish_color = (0, 255, 0)  # green
        self.platform_color = (100, 100, 100)  # grey

        #textures
        script_dir = os.path.dirname(__file__)
        grass_image_path = os.path.join(script_dir, '..', 'assets', 'Grass.png')
        self.grass_image = pygame.image.load(grass_image_path).convert_alpha()

        finish_image_path = os.path.join(script_dir, '..', 'assets', 'Finish.png')
        self.finish_image = pygame.image.load(finish_image_path).convert_alpha()

        # self.platforms = []
        # self.platforms.append(pygame.Rect(0, 386, self.screen_width, 64))
        # self.platforms.append(pygame.Rect(0, 448, self.screen_width, 64))

        self.finish_zone = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        self.start_zone = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

        self.car_lanes: list[CarLane] = []
        self.water_lanes: list[WaterLane] = []
        # self.car_lanes: list[CarLane] = [CarLane(384, True), CarLane(448, False), CarLane(512, True, 1.5)]
        # self.water_lanes = [
        #    WaterLane(128, moving_right=True, speed=2, log_count=3),
        #    WaterLane(192, moving_right=False, speed=3, log_count=2),
        #    WaterLane(256, moving_right=True, speed=2, log_count=4),
        # ]

        self._on_start_last_frame = False
        self._on_finish_last_frame = False
        self.game_over = False

        self.generate_level(self.player.get_score())

    def update(self, dt):
        if self.game_over:
            return
        else:
            # Hier zou je enemies/platform logic updaten
            for car_lane in self.car_lanes:
                car_lane.update(dt)

            for water_lane in self.water_lanes:
                water_lane.update()

            self.check_water()
            self.check_collisions()

            on_start = self.player.rect.colliderect(self.start_zone)
            if on_start and not self._on_start_last_frame:
                print("Player on start zone")
            self._on_start_last_frame = on_start

            on_finish = self.player.rect.colliderect(self.finish_zone)
            if on_finish and not self._on_finish_last_frame:
                print("Finished!")
                self.player.reset_player()
                self.generate_level(self.player.get_score())
            self._on_finish_last_frame = on_finish

    def clear_lanes(self):
        self.car_lanes.clear()
        self.water_lanes.clear()

    def generate_level(self, score: int):
        self.clear_lanes()

        # increase car speed
        CarLane.speed = 200 + score

        # load new lanes
        # every {lane_count_scaling} score add 1 water or car lane
        open_lanes = list(range(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE, TILE_SIZE))
        level_difficulty = 200 + score
        lane_count_scaling = 50
        while (
            level_difficulty > random.randint(0, lane_count_scaling)
            and len(open_lanes) >= 1
        ):
            next_lane = open_lanes[random.randint(0, len(open_lanes) - 1)]
            open_lanes.remove(next_lane)
            self.generate_lane(next_lane)
            level_difficulty -= lane_count_scaling

        # remove multi empty lanes
        previus_open_lane = 0
        for open_lane in open_lanes:
            if open_lane == previus_open_lane + TILE_SIZE:
                self.generate_lane(open_lane)
            else:
                previus_open_lane = open_lane

    def generate_lane(self, y: int):
        if random.randint(0, 1) == 0:
            self.car_lanes.append(
                CarLane(y, random.randint(0, 1) == 0, random.random() * 0.4 + 0.8)
            )
        else:
            self.water_lanes.append(
                WaterLane(
                    y,
                    random.randint(0, 1) == 0,
                    random.randint(2, 3),
                    random.randint(2, 4),
                )
            )

    def check_water(self):
        if self.game_over:
            return

        on_water = False
        on_log = False

        for water_lane in self.water_lanes:
            if (
                self.player.rect.top < water_lane.y_pos + water_lane.height
                and self.player.rect.bottom > water_lane.y_pos
            ):
                on_water = True
                # print(f"Player in water lane at y={water_lane.y_pos}")  # DEBUG
                log = water_lane.get_log_at_position(self.player.rect)

                if log:
                    on_log = True
                    # print(f"Player on log!")  # DEBUG
                    self.player.move_with_log(water_lane.speed_x)
                    break

        # print(f"on_water: {on_water}, on_log: {on_log}")  # DEBUG
        if on_water and not on_log:
            print("Player drowned!")
            final_score = self.player.get_score()
            # self.player.reset_after_death()
            self.set_game_over(final_score)
            self.player.set_game_over()
            self.gameover.set_game_over()

    def check_collisions(self):
        if self.game_over:
            return
        for car_lane in self.car_lanes:
            if (
                self.player.rect.collidelist([car.hitbox for car in car_lane.cars])
                != -1
            ):
                # hit car code
                print("Player hit by car!")
                final_score = self.player.get_score()
                # self.player.reset_after_death()
                self.set_game_over(final_score)
                self.player.set_game_over()
                self.gameover.set_game_over()

    def draw(self, screen):
        #grass
        self.draw_grass(screen)

        # Start/Finish zones
        for x in range(0, SCREEN_WIDTH, self.finish_image.get_width()):
            screen.blit(self.finish_image, (x, 0))

        # Platforms
        # for plat in self.platforms:
        #    pygame.draw.rect(screen, self.platform_color, plat)

        # Cars
        for car_lane in self.car_lanes:
            car_lane.draw(screen)

        # Water lanes
        for water_lane in self.water_lanes:
            water_lane.draw(screen)
        # the reset_player function has been moved to player.py

        #    def reset_player(self):
        #        self.player.pos.update(self.screen_width // 2, self.screen_height - 100)
        #        self.player.rect.topleft = (
        #            self.player.pos.x,
        #            self.player.pos.y,
        # )  # this line is redundant. It doesn't seem to be causing issues, but it gives an error in my code editor.
        #

    def draw_grass(self, screen):
        for y in range(self.finish_image.get_height(), SCREEN_HEIGHT, self.grass_image.get_height()):
            for x in range(0, SCREEN_WIDTH, self.grass_image.get_width()):
                screen.blit(self.grass_image, (x, y))

    def set_game_over(self, final_score):
        self.game_over = True
        if self.highscore:
            new_hs = self.highscore.update(final_score)
            if new_hs:
                print(f"New High Score: {final_score}!")

    def restart(self):
        self.game_over = False
        self.player.reset_after_death()
        self.gameover.reset()
        self._on_start_last_frame = False
        self._on_finish_last_frame = False
        self.generate_level(self.player.get_score())

