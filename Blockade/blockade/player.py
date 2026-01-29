import pygame

class Player():
    def __init__(self, x, y, colour, controls, starting_direction):
        # Sets the starting position that you put in the init of the player
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.starting_direction = starting_direction

        self.reset() # For resetting position after winning a round

        self.colour = colour # Sets the colour of your brick thing
        self.controls = controls # This will be a dictionary with the WASD keys and the arrow keys {"up": K_w, "down": K_s, etc...}
        self.direction = (0,0) # Direction of where the player will go
        self.next_direction = starting_direction # This is for fixing a bug that caused suicide if you pressed directions too fast
        self.trail = [(self.x, self.y)] # Stores the trail of blocks for player

    # Function for resetting the players after a round is won
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = self.starting_direction
        self.next_direction = self.starting_direction
        self.trail = [(self.x, self.y)]

    def player_input(self, keys):
        # This will 'turn' your blockade to the direction you want to go in, while preventing going back into yourself.
        if keys["up"] and self.direction != (0,1):
            self.next_direction = (0, -1)
        elif keys["down"] and self.direction !=(0,-1):
            self.next_direction = (0, 1)
        elif keys["left"] and self.direction !=(1,0):
            self.next_direction = (-1,0)
        elif keys["right"] and self.direction !=(-1,0):
            self.next_direction = (1,0)

    # This handles player movement and block placement
    def move(self):
        self.direction = self.next_direction
        if self.direction != (0,0):
            self.x += self.direction[0]
            self.y += self.direction[1]
            self.trail.append((self.x, self.y))

    # For drawing the player on the screen
    def draw(self, surface, offset_x, offset_y, cell_size):
        for cell in self.trail:
            rect = pygame.Rect(
                offset_x + cell[0] * cell_size,
                offset_y + cell[1] * cell_size,
                cell_size,
                cell_size
            )

            base = pygame.Color(self.colour)
            outline = (
                max(0, min(255, int(base.r -75))),
                max(0, min(255, int(base.g -75))),
                max(0, min(255, int(base.b -75)))
                )
            outline_thickness = 2

            # Draws the coloured square
            pygame.draw.rect(surface, base, rect)

            # Draws the outline
            pygame.draw.rect(surface, outline, rect, outline_thickness)

            # Draws horizontal lines for the brick effect
            brick_rows = 2
            for i in range(1, brick_rows +1):
                y = rect.top + i * rect.height // (brick_rows + 1)
                pygame.draw.line(surface, outline, (rect.left, y), (rect.right -1, y), outline_thickness)
            
            # Draws vertical lines for the brick effect
            brick_columns = 2
            row_height = rect.height // (brick_rows +1)
            for i in range(brick_rows + 1):
                y_start = rect.top + i * row_height
                y_end = rect.top + (i + 1) * row_height 

                # For offsetting the brick lines
                offset = 0
                if i%2  == 1:
                    offset = row_height // (2 * brick_rows)
                for j in range(1, brick_rows + 1):
                    x = rect.left + j * rect.width // (brick_columns +1) + offset
                    pygame.draw.line(surface, outline, (x, y_start), (x, y_end), outline_thickness)

            
    # For checking collision
    def check_collision(self, columns, rows, opponent):
        if self.x <= 0 or self.x >= columns - 1 or self.y <= 0 or self.y >= rows - 1:
            return True
        
        if (self.x, self.y) in self.trail[:-1]:
            return True
        
        if (self.x, self.y) in opponent:
            return True