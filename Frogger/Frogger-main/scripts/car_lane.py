import pygame
import random
import os
from car import Car
from constants import SCREEN_WIDTH

class CarLane:
    speed = 200.0
    #time between cars in miniseconds
    _min_time_between_cars = 1000
    _max_time_between_cars = 4000

    def __init__(self, y: int, driving_rightwards: bool, speed_multiplier: float = 1):
        self.y: int = y
        self.driving_rightwards: bool = driving_rightwards
        self.cars: list[Car] = []
        self.time_until_next_car: float = 0.0
        self.speed_multiplier = speed_multiplier

        script_dir = os.path.dirname(__file__)
        road_path = os.path.join(script_dir, '..', 'assets', 'Road.png')
        self.road_image = pygame.image.load(road_path).convert_alpha()

        self.init_start_cars()

    def init_start_cars(self):
        x_pos = -128.0
        while x_pos < SCREEN_WIDTH:
            x_pos += random.randint(CarLane._min_time_between_cars, CarLane._max_time_between_cars) / 1000 * CarLane.speed * self.speed_multiplier
            self.cars.append(Car(x_pos, self.y, self.driving_rightwards, CarLane.speed * self.speed_multiplier))
        if not self.driving_rightwards:
            self.cars.reverse()
            self.time_until_next_car = (x_pos - SCREEN_WIDTH) / CarLane.speed / self.speed_multiplier

    def update(self, dt: float):
        # update cars
        for car in self.cars:
            car.update(dt)

        # remove offscreen cars
        if len(self.cars) > 0:
            first_car = self.cars[0]
            if first_car.hitbox.right < 0 or first_car.hitbox.left > SCREEN_WIDTH:
                self.cars.remove(first_car)

        # add new cars
        self.time_until_next_car -= dt
        if self.time_until_next_car <= 0:
            if self.driving_rightwards:
                self.cars.append(Car(-128, self.y, True, CarLane.speed * self.speed_multiplier))
            else:
                self.cars.append(Car(SCREEN_WIDTH, self.y, False, CarLane.speed * self.speed_multiplier))
            self.time_until_next_car += random.randint(CarLane._min_time_between_cars, CarLane._max_time_between_cars) / 1000

    def draw(self, surface: pygame.Surface):
        #road
        tile_width = self.road_image.get_width()
        for x in range(0, SCREEN_WIDTH, tile_width):
            surface.blit(self.road_image, (x, self.y))

        #cars
        for car in self.cars:
            car.draw(surface)