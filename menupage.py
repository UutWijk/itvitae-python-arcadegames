from menubutton import MenuButton

class Page:
    def __init__(self, game_names, page_rows, page_cols, screen_size, font, assets_path=None):
        self.rows = page_rows
        self.cols = page_cols
        self.buttons = [] # A 2D list: [row][col]
        
        screen_w, screen_h = screen_size
        gap_x = screen_w // (self.cols + 1)
        gap_y = screen_h // (self.rows + 1)

        button_width = 256
        button_height = 192

        y_offset = 0
        
        # Build the grid
        for r_idx in range(self.rows):
            button_row = []
            for c_idx in range(self.cols):
                # Calculate index in the flat list of 6 games
                flat_idx = r_idx * self.cols + c_idx
                
                if flat_idx < len(game_names):
                    name = game_names[flat_idx]
                    pos_x = (c_idx + 1) * gap_x - (button_width // 2)
                    pos_y = (r_idx + 1) * gap_y - (button_height // 2) + y_offset                    
                    button_row.append(MenuButton(name, pos_x, pos_y, button_width, button_height, font, assets_path))
            
            if button_row:
                self.buttons.append(button_row)

    def draw(self, screen, selected_coords):
        sel_row, sel_col = selected_coords
        for r_idx, row in enumerate(self.buttons):
            for c_idx, button in enumerate(row):
                is_selected = (r_idx == sel_row and c_idx == sel_col)
                button.draw(screen, is_selected)