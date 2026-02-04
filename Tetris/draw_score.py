import os
import pygame

tetris_dir = os.path.dirname(os.path.abspath(__file__))
font2 = pygame.font.Font(os.path.join(tetris_dir, "assets", "nintendo-nes-font.ttf"), 20)
next_text = font2.render('NEXT', True, 'white')

def draw_array(array, display_surface: pygame.Surface, position) -> None:
    scoresurface = pygame.Surface((165, 165))
    piece_position_x = 16
    piece_position_y = 33
    scoresurface.fill("black")

    scoresurface.blit(next_text, (2, 2))

    if len(array) == 2:
         piece_position_x += 33
         piece_position_y += 33
    elif len(array) == 3:
         piece_position_x += 15

    spritesheet = pygame.image.load(
        os.path.join(tetris_dir, "assets", "blocks", "sprites.png")
    ).convert_alpha()

    for r in range(len(array)):
        for c in range(len(array[r])):
            value_of_piece = array[r][c]

            if value_of_piece:
                letter, number = value_of_piece

                row = ord(letter) - ord('a')
                col = int(number) - 1

                sprite_rect = pygame.Rect(
                    col * 30,
                    row * 30,
                    30,
                    30
                )

                img = spritesheet.subsurface(sprite_rect)

                scoresurface.blit(img, (c * 33 + piece_position_x, r * 33 + piece_position_y))

    display_surface.blit(scoresurface, position)
