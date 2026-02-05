import pygame
from pygame.sprite import Sprite, Group
from .player import Player
from .obstacle import Obstacle
from .bullet import Bullet
from .ufo import UFO
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.highscore_file = os.path.join(current_dir, "highscores.txt")
        self.highscore_list = []
        with open(self.highscore_file, "a+") as f:
            f.seek(0)
            content = f.readlines()
            if not content:
                f.write("0")
            else:
                self.highscore_list = [line.strip() for line in content]
        self.sort_highscores()
        ship_image = pygame.image.load(os.path.join(current_dir, "sprites/spaceship_default.png")).convert_alpha()
        self.font = pygame.font.Font(os.path.join(current_dir, "fonts", "Orbitron", "static", "Orbitron-Regular.ttf"), 30)
        self.font_mega = pygame.font.Font(os.path.join(current_dir, "fonts", "Orbitron", "static", "Orbitron-Regular.ttf"), 120)
        self.font_large = pygame.font.Font(os.path.join(current_dir, "fonts", "Orbitron", "static", "Orbitron-Regular.ttf"), 60)
        self.font_small = pygame.font.Font(os.path.join(current_dir, "fonts", "Orbitron", "static", "Orbitron-Regular.ttf"), 20)
        w, h = ship_image.get_size()
        ship_image = pygame.transform.smoothscale(
            ship_image,
            (int(w * SCALE), int(h * SCALE)))
        self.ship_image = ship_image

        self.game_over_timer = 0.0


        self.states = [
            "gameplay",
            "title",
            "game_over"
        ]
        self.current_state = "title"
        
        self.start_count = 4
        self.current_count = 4
        self.bullets = Group()
        self.player = Player(screen.get_width(), screen.get_height(), self.bullets, self.sounds)
        self.obstacles = Group()
        self.ufos = Group()
        self.ufo_timer = 20
        # for title screen background
        for _ in range(self.current_count):
            self.spawn_obstacle()
            self.spawn_obstacle(stage=2)
            self.spawn_obstacle(stage=3)

            


    def update(self, dt) -> None:
        if self.current_state != "title":
            self.player.update(dt, self.pressed, self.just_pressed)
            
            #collision detection
            if len(self.obstacles) == 0:
                self.current_count += 1
                for _ in range(self.current_count):
                    self.spawn_obstacle()
            obstacle_in_center = False

            # whether ufos and the player hit eachother
            for bullet in self.bullets:
                if bullet.ufo:
                    if pygame.sprite.collide_mask(bullet, self.player):
                        bullet.kill()
                        self.player_lose_life()
                else:
                    for ufo in self.ufos:
                        if pygame.sprite.collide_mask(bullet, ufo) and bullet.kills and not bullet.ufo:
                            bullet.kill()
                            self.player.add_score(50 * self.current_count)
                            ufo.hit = True
                            self.sounds.ufo_impact() 

            
            for obstacle in self.obstacles:

                # for multiple obstacles hit in same frame
                hit_obstacles = []

                # whether ufo hits obstacle
                for ufo in self.ufos:
                    if pygame.sprite.collide_mask(obstacle, ufo):
                        ufo.hit = True
                        hit_obstacles.append(obstacle)  

                # whether player hits obstacle                      
                if not self.player.invincible:
                    if self.player.respawning:
                        if obstacle.pos.distance_to(pygame.Vector2(self.screen.get_width() // 2, self.screen.get_height() // 2)) < 150:
                            obstacle_in_center = True
                    else:
                        player_hit = pygame.sprite.spritecollide(
                            self.player, self.obstacles, False, pygame.sprite.collide_mask
                        )
                        if player_hit:
                            self.player_lose_life() 
                        hit_obstacles.extend(player_hit)

                        # handles obstacle breaking
                        if hit_obstacles:                                                                                  
                            for obstacle in hit_obstacles:
                                new_obstacles = obstacle.killed()
                                self.sounds.asteroid_break()
                                if new_obstacles:
                                    self.obstacles.add(new_obstacles)
                
                # whether player bullet hits obstacle
                for bullet in self.bullets:   
                    if pygame.sprite.collide_mask(bullet, obstacle) and bullet.kills and bullet.ufo == False:
                        bullet.kill()              
                        match obstacle.stage:
                            case 1:
                                self.player.add_score(5 * self.current_count)
                            case 2:
                                self.player.add_score(10 * self.current_count)
                            case 3:
                                self.player.add_score(25 * self.current_count)

                        # kills = False bullets are for particle effects only        
                        for _ in range(random.randint(2, 5)):
                            self.bullets.add(Bullet(obstacle.pos.x, obstacle.pos.y, random.uniform(0, 360), lifetime=random.uniform(0.1, 1.6), speed=random.uniform(10, 200), kills=False))

                        # handles obstacle breaking    
                        new_obstacles = obstacle.killed()
                        self.sounds.asteroid_break()
                        if new_obstacles:
                            self.obstacles.add(new_obstacles)

            # player respawn conditions:
            # - player must be in respawning state
            # - no obstacles near center (prevents player from spawning on top of an asteroid)
            # - respawning animation reached minimum time
            # - player has lives
            if self.player.respawning and not obstacle_in_center and self.player.respawn_timer >= self.player.respawn_duration and self.player.lives > 0:
                self.player.respawn()
            
        # update game objects
        self.bullets.update(dt)
        self.obstacles.update(dt)
        self.ufos.update(dt, self.player, self.obstacles)

        # random ufo spawning
        if self.current_state == "gameplay":
            self.ufo_timer -= dt
            if self.ufo_timer <= 0:
                self.ufos.add(UFO(self.screen.get_width(), self.screen.get_height(), self.bullets, self.obstacles, self.sounds))
                self.ufo_timer = random.randint(15, 30)

        # game over state input handling
        if self.current_state == "game_over":
            self.game_over_timer += dt
            if self.game_over_timer > 1.0:
                if self.pressed["a"]:
                    self.reset()
                if self.pressed["b"]:
                    self.reset()
                    self.next_state = "MENU"
                return

    
    def player_lose_life(self):
        self.player.lives -= 1

        # game over handling
        if self.player.lives <= 0:
            self.current_state = "game_over"
            self.game_over_timer = 0.0  

            # Check and update high scores
            if len(self.highscore_list) < 10 or self.player.score > int(self.highscore_list[-1]):
                self.highscore_list.append(str(self.player.score))
                self.sort_highscores()
                with open(self.highscore_file, "w") as f:
                    f.write("\n".join(self.highscore_list))

        # kills = False bullets as particle effect
        for _ in range(random.randint(3, 6)):
            self.bullets.add(Bullet(self.player.pos.x + random.randrange(0,10), self.player.pos.y + random.randrange(0,10), random.uniform(0, 360), lifetime=random.uniform(0.1, 2.5), speed=random.uniform(10, 50), kills=False))
        self.player.death()


    def draw(self) -> None:
        self.screen.fill("#000000")

        # player, lives and score
        if self.current_state is not "title":
            self.player.draw(self.screen)
            for _ in range(self.player.lives):
                self.screen.blit(self.ship_image, (10 + _ * 40, 60))
            self.screen.blit(self.font.render(f"Score: {self.player.score}", True, (255, 255, 255)), (10, 10))

        # game objects
        self.bullets.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.ufos.draw(self.screen, self.player.pos)

        # title screen
        if self.current_state == "title":
            semi_opaque_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            semi_opaque_surface.set_alpha(150)
            semi_opaque_surface.fill((0, 0, 0))
            self.screen.blit(semi_opaque_surface, (0, 0))
            title_text = self.font_mega.render("ASTEROIDS", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
            instruction_text = self.font.render("Press A to Start", True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
            back_to_menu_text = self.font_small.render("Press B to return to menu", True, (255, 255, 255))
            back_to_menu_rect = back_to_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 165))
            self.screen.blit(title_text, title_rect)
            if pygame.time.get_ticks() // 500 % 2 == 0:
                self.screen.blit(instruction_text, instruction_rect)
            self.screen.blit(back_to_menu_text, back_to_menu_rect)
            if self.pressed["a"]:
                self.reset()
            if self.pressed["b"]:
                self.next_state = "MENU"
            return

        #game over screen
        if self.current_state == "game_over":
            semi_opaque_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            if self.game_over_timer < 1.0:
                alpha = int(self.game_over_timer * 180)
                semi_opaque_surface.set_alpha(alpha)
            else:
                semi_opaque_surface.set_alpha(180)
            semi_opaque_surface.fill((0, 0, 0))
            self.screen.blit(semi_opaque_surface, (0, 0))
            game_over_text = self.font_large.render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 120))
            score_text = self.font.render("Final Score:", True, (255, 255, 255))
            score_number = self.font_large.render(f"{self.player.score}", True, (255, 255, 255))
            
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            score_number_rect = score_number.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 65))
            new_game_text = self.font.render("Press A to play again", True, (255, 255, 255))
            new_game_rect = new_game_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 180))
            back_to_menu_text = self.font_small.render("Press B to return to menu", True, (255, 255, 255))
            back_to_menu_rect = back_to_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 245))
            if self.game_over_timer > 1.0:
                self.screen.blit(score_text, score_rect)
            if self.game_over_timer > 2.0:
                self.screen.blit(score_number, score_number_rect)
            if self.game_over_timer > 3.0:
                if self.game_over_timer * 2 % 2 < 1:
                    self.screen.blit(new_game_text, new_game_rect)
                self.screen.blit(back_to_menu_text, back_to_menu_rect)
            self.screen.blit(game_over_text, text_rect)

            # when game over animation is done
            if self.game_over_timer > 3.0:

                # High scores
                hs_title = self.font.render("High Scores", True, (255, 255, 255))
                hs_x = self.screen.get_width() * 0.88
                hs_y_start = 50
                
                self.screen.blit(hs_title, hs_title.get_rect(center=(hs_x, hs_y_start)))
                top_ten = self.highscore_list[:10]
                for i, score in enumerate(top_ten):
                    index_str = f"{i + 1}."
                    hs_index_text = self.font_small.render(index_str, True, (255, 255, 255))
                    index_rect = hs_index_text.get_rect(left=hs_x - 100, top=hs_y_start + 50 + (i * 35))
                    self.screen.blit(hs_index_text, index_rect)
                    score_str = f"{score}"
                    hs_entry_text = self.font_small.render(score_str, True, (255, 255, 255))
                    entry_rect = hs_entry_text.get_rect(left=hs_x - 50, top=hs_y_start + 50 + (i * 35))
                    self.screen.blit(hs_entry_text, entry_rect)

    # spawns an obstacle randomly on the screen
    def spawn_obstacle(self, stage = 1):
        random_x = random.randint(0, self.screen.get_width())
        random_y = random.randint(0, self.screen.get_height())

        # if coordinates are too close to player, try again
        if pygame.Vector2(random_x, random_y).distance_to(self.player.pos) < 200:
            self.spawn_obstacle(stage)
        else:
            self.obstacles.add(Obstacle(random_x, random_y, self.screen.get_width(), self.screen.get_height(), stage))

    # resets all game variables
    def reset(self):
        self.current_state = "gameplay"
        self.bullets.empty()
        self.obstacles.empty()
        self.ufos.empty()
        self.ufo_timer = 20

        self.player = Player(self.screen.get_width(), self.screen.get_height(), self.bullets, self.sounds)
        self.current_count = self.start_count
        self.y_offset = 750 # high score animation offset
        self.bullets = Group()
        self.player = Player(self.screen.get_width(), self.screen.get_height(), self.bullets, self.sounds)
        self.obstacles = Group()
        for _ in range(self.current_count):
            self.spawn_obstacle()


    def sort_highscores(self):
        self.highscore_list.sort(key=lambda x: int(x), reverse=True)
        self.highscore_list = self.highscore_list[:10]
        