from tkinter import Frame, Label, CENTER

import game_ai
import game_functions

EDGE_LENGTH = 400
EDGE_LENGTH1 = 300
CELL_COUNT = 4
CELL_PAD = 10

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY = "'d'"
AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"

LABEL_FONT = ("Verdana", 40, "bold")

GAME_COLOR = "#bbada0"

EMPTY_COLOR = "#cdc1b3"

TILE_COLORS = {2: "#eee4da", 4: "#ece0c8", 8: "#f3b27a", 16: "#f59563",
               32: "#f57c5f", 64: "#f65d3b", 128: "#edce71",
               256: "#edcc61", 512: "#ebc74f", 1024: "#ecc441",
               2048: "#ecc02c"}

LABEL_COLORS = {2: "#776e65", 4: "#776e65", 8: "#ffffff", 16: "#ffffff",
                32: "#ffffff", 64: "#ffffff", 128: "#ffffff",
                256: "#ffffff", 512: "#ffffff", 1024: "#ffffff",
                2048: "#ffffff"}


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: game_functions.move_up,
                         DOWN_KEY: game_functions.move_down,
                         LEFT_KEY: game_functions.move_left,
                         RIGHT_KEY: game_functions.move_right,
                         AI_KEY: game_ai.ai_move,
                         }

        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()
        self.mainloop()

    def build_grid(self):
        background2 = Frame(self, bg=GAME_COLOR,
                            width=700, height=150)
        background2.grid()

        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH1)
        background.grid()

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=LABEL_FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()

    def key_press(self, event):
        valid_game = True
        key = repr(event.char)
        if key == AI_PLAY_KEY:
            move_count = 0
            while valid_game:
                self.matrix, valid_game = game_ai.ai_move(self.matrix, 40, 30)
                if valid_game:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                move_count += 1
        if key == AI_KEY:
            self.matrix, move_made = game_ai.ai_move(self.matrix, 20, 30)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False

        elif key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False


gamegrid = Display()