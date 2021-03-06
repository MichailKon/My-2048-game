import tkinter
import random
from copy import deepcopy
import math

ARROWS = ['Up', 'Down', 'Right', 'Left']
COLORS = {
    '2': '#eee4da',
    '4': '#ede0c8',
    '8': '#f2b179',
    '16': '#f59563',
    '32': '#f67c5f',
    '64': '#f65e3b',
    '128': '#edcf72',
    '256': '#edcc61',
    '512': '#edc850',
    '1024': '#edc53f',
    '2048': '#edc22e',
    '4096': '#3c3a32',
    '8192': '#3c3c3c',
    '16384': '#311c33',
    'beyond': '#3c3ccc'
}


class Game2048:
    def __init__(self):
        self.STEP = 120
        self.STEP_TO_MOVE = 1
        self.N_X = self.N_Y = 5
        self.MAX_X = self.STEP * self.N_X
        self.MAX_Y = self.STEP * self.N_Y
        self.MIN_X = self.MIN_Y = 0

        self.score = 0
        self.cells = [[None for i in range(self.N_Y)] for j in range(self.N_X)]

        self.master = tkinter.Tk()
        self.master.columnconfigure(0, pad=3)
        self.master.columnconfigure(1, pad=3)
        self.master.columnconfigure(2, pad=3)
        self.master.columnconfigure(3, pad=3)
        self.master.columnconfigure(4, pad=3)
        self.master.rowconfigure(0, pad=3)
        self.master.rowconfigure(1, pad=3)
        self.master.rowconfigure(2, pad=3)
        self.master.rowconfigure(3, pad=3)
        self.master.rowconfigure(4, pad=3)
        self.master.rowconfigure(5, pad=3)
        self.master.rowconfigure(6, pad=3)
        self.master.rowconfigure(7, pad=3)

        self.main_label = tkinter.Label(self.master, text='Game 2048', font='Courier 15')
        self.main_label.grid(row=0, column=2)
        self.score_label = tkinter.Label(self.master, text='Score: 0', font='Courier 15')
        self.score_label.grid(row=1, column=2)
        self.canvas = tkinter.Canvas(self.master, bg='white', height=self.N_X * self.STEP, width=self.N_X * self.STEP)
        self.canvas.grid(row=2, column=0, columnspan=self.N_X, rowspan=self.N_Y)
        self.button_to_3_by_3 = tkinter.Button(self.master, text='3 by 3', font='Courier 14',
                                               command=self.change_to_3_by_3)
        self.button_to_3_by_3.grid(row=7, column=0)
        self.button_to_4_by_4 = tkinter.Button(self.master, text='4 by 4', font='Courier 14',
                                               command=self.change_to_4_by_4)
        self.button_to_4_by_4.grid(row=7, column=1)
        self.restart_button = tkinter.Button(self.master, text='restart', font='Courier 14',
                                             command=self.restart)
        self.restart_button.grid(row=7, column=2)
        self.button_to_5_by_5 = tkinter.Button(self.master, text='5 by 5', font='Courier 14',
                                               command=self.change_to_5_by_5)
        self.button_to_5_by_5.grid(row=7, column=3)
        self.button_to_6_by_6 = tkinter.Button(self.master, text='6 by 6', font='Courier 14',
                                               command=self.change_to_6_by_6)
        self.button_to_6_by_6.grid(row=7, column=4)
        self.game_over_button = tkinter.Button(self.master, text='Game Over\nRestart?', font='Courier 20',
                                               command=self.restart)
        self.master.bind("<KeyPress>", self.key_pressed)

    def change_to_3_by_3(self): self.change_field_size(3)
    def change_to_4_by_4(self): self.change_field_size(4)
    def change_to_5_by_5(self): self.change_field_size(5)
    def change_to_6_by_6(self): self.change_field_size(6)

    def change_field_size(self, new_size):
        self.N_X = self.N_Y = new_size
        self.STEP = self.MAX_X // self.N_X
        self.restart()
        self.make_frame()

    def make_lines_and_field(self):
        self.canvas.delete("all")
        for i in range(self.N_X + 1):
            self.canvas.create_line(self.MIN_X + 1, self.STEP * i + 1, self.MAX_X + 1, self.STEP * i + 1)
        for i in range(self.N_Y + 1):
            self.canvas.create_line(self.STEP * i + 1, self.MIN_Y + 1, self.STEP * i + 1, self.MAX_Y + 1)

    def put_random_number(self):
        free_cells = []
        for i in range(self.N_X):
            for j in range(self.N_Y):
                if self.cells[i][j] is None:
                    free_cells.append((i, j))
        if not free_cells:
            return
        row, col = random.choice(free_cells)
        number = random.choice([2, 2, 2, 4])
        x_cord = (self.STEP * col + self.STEP * (col + 1)) // 2
        y_cord = (self.STEP * row + self.STEP * (row + 1)) // 2

        number = str(number)
        rect = self.canvas.create_rectangle(self.STEP * col, self.STEP * row,
                                            self.STEP * (col + 1), self.STEP * (row + 1),
                                            fill=COLORS[number] if number in COLORS.keys() else COLORS['beyond'])
        label = self.canvas.create_text(x_cord, y_cord, font='Courier 27', text=number)
        self.cells[row][col] = [int(number), rect, label]

    def make_frame(self):
        if all(map(lambda x: x == [None] * self.N_Y, self.cells)):
            self.put_random_number()
        self.score_label.config(text=f'Score: {self.score}')

    def make_anim_without_merge(self, row1, col1, row2, col2):
        """ move cell from {row1, col1} to {row2, col2} """
        sign1 = math.copysign(col2 != col1, col2 - col1)
        sign2 = math.copysign(row2 != row1, row2 - row1)
        for j in range(0, self.STEP, self.STEP_TO_MOVE):
            self.canvas.move(self.cells[row1][col1][1], self.STEP_TO_MOVE * sign1, 0)
            self.canvas.move(self.cells[row1][col1][1], 0, self.STEP_TO_MOVE * sign2)
            self.canvas.move(self.cells[row1][col1][2], self.STEP_TO_MOVE * sign1, 0)
            self.canvas.move(self.cells[row1][col1][2], 0, self.STEP_TO_MOVE * sign2)

    def merge_anim(self, row1, col1, row2, col2):
        """ merge cells {row1, col1} and {row2, col2} """
        self.canvas.delete(self.cells[row2][col2][1], self.cells[row2][col2][2])
        num = str(self.cells[row1][col1][0])
        self.canvas.itemconfig(self.cells[row1][col1][2], text=f'{num}')
        self.canvas.itemconfig(self.cells[row1][col1][1], fill=COLORS[str(num)])

    def restart(self):
        self.game_over_button.grid_forget()
        self.score = 0
        self.cells = [[None for i in range(self.N_Y)] for j in range(self.N_X)]
        self.make_lines_and_field()
        self.make_frame()

    def is_game_over(self):
        was_cells = deepcopy(self.cells)
        was_score = deepcopy(self.score)
        can_merge = any(map(lambda x: None in x, was_cells))
        can_merge |= self.make_up()
        can_merge |= self.make_right()
        can_merge |= self.make_down()
        can_merge |= self.make_left()
        self.cells = deepcopy(was_cells)
        self.score = deepcopy(was_score)
        if not can_merge:
            self.game_over_button.grid(row=3, rowspan=2, column=2)

    def key_pressed(self, event):
        if event.keysym == 'Up':
            self.make_up()
        elif event.keysym == 'Down':
            self.make_down()
        elif event.keysym == 'Right':
            self.make_right()
        elif event.keysym == 'Left':
            self.make_left()
        if event.keysym in ARROWS:
            self.put_random_number()
            self.make_frame()
            # self.is_game_over()

    def try_and_merge(self, row1, col1, row2, col2):
        if not (0 <= row1 < self.N_X) or not (0 <= row2 <= self.N_X) or \
           not (0 <= col1 < self.N_Y) or not (0 <= col2 < self.N_Y):
            return False
        if self.cells[row1][col1] is not None and self.cells[row2][col2] is not None \
           and self.cells[row1][col1][0] == self.cells[row2][col2][0]:
            self.cells[row1][col1][0] *= 2
            self.merge_anim(row1, col1, row2, col2)
            self.cells[row2][col2] = None
            self.score += self.cells[row1][col1][0]
            return True
        return False

    def make_up(self):
        was_merge = False
        for row in range(self.N_X - 1):
            for col in range(self.N_Y):
                if self.try_and_merge(row, col, row + 1, col):
                    was_merge = True
                elif self.cells[row][col] is None and self.cells[row + 1][col] is not None:
                    row1 = row
                    while row1 > -1 and self.cells[row1][col] is None:
                        self.make_anim_without_merge(row1 + 1, col, row1, col)
                        self.cells[row1][col] = self.cells[row1 + 1][col]
                        self.cells[row1 + 1][col] = None
                        row1 -= 1
                    if self.try_and_merge(row1, col, row1 + 1, col):
                        was_merge = True
        return was_merge

    def make_down(self):
        was_merge = False
        for row in range(self.N_X - 1, 0, -1):
            for col in range(self.N_Y):
                if self.try_and_merge(row, col, row - 1, col):
                    was_merge = True
                elif self.cells[row][col] is None and self.cells[row - 1][col] is not None:
                    row1 = row
                    while row1 < self.N_X and self.cells[row1][col] is None:
                        self.make_anim_without_merge(row1 - 1, col, row1, col)
                        self.cells[row1][col] = self.cells[row1 - 1][col]
                        self.cells[row1 - 1][col] = None
                        row1 += 1
                    if self.try_and_merge(row1, col, row1 - 1, col):
                        was_merge = True
        return was_merge

    def make_right(self):
        was_merge = False
        for row in range(self.N_X):
            for col in range(self.N_Y - 1, 0, -1):
                if self.try_and_merge(row, col, row, col - 1):
                    was_merge = True
                elif self.cells[row][col] is None and self.cells[row][col - 1] is not None:
                    col1 = col
                    while col1 < self.N_Y and self.cells[row][col1] is None:
                        self.make_anim_without_merge(row, col1 - 1, row, col1)
                        self.cells[row][col1] = self.cells[row][col1 - 1]
                        self.cells[row][col1 - 1] = None
                        col1 += 1
                    if self.try_and_merge(row, col1, row, col1 - 1):
                        was_merge = True
        return was_merge

    def make_left(self):
        was_merge = False
        for row in range(self.N_X):
            for col in range(self.N_Y - 1):
                if self.try_and_merge(row, col, row, col + 1):
                    was_merge = True
                elif self.cells[row][col] is None and self.cells[row][col + 1] is not None:
                    col1 = col
                    while col1 > -1 and self.cells[row][col1] is None:
                        self.make_anim_without_merge(row, col1 + 1, row, col1)
                        self.cells[row][col1] = self.cells[row][col1 + 1]
                        self.cells[row][col1 + 1] = None
                        col1 -= 1
                    if self.try_and_merge(row, col1, row, col1 + 1):
                        was_merge = True
        return was_merge

    def run(self):
        self.restart()
        self.make_frame()
        self.master.mainloop()


if __name__ == '__main__':
    game = Game2048()
    game.run()
