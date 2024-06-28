import tkinter as tk
import copy

GRID_STEP = 10
VISIBLE_AREA = 1000
GAME_SPEED = 50

class Game:
    def __init__(self) -> None:
        self.create_grid()
        self.add_some_points()
        self.life_cycle()

    def create_grid(self):
        self.cell_status = [[False]*VISIBLE_AREA for i in range(VISIBLE_AREA)]

        win_width = canvas.winfo_width() # Get current width of canvas
        win_height = canvas.winfo_height() # Get current height of canvas
        canvas.delete('grid_line')

        # Creates all vertical lines at intevals of 100
        for i in range(0, win_width, GRID_STEP):
            canvas.create_line([(i, 0), (i, win_height)], tag='grid_line', fill='gray')

        # Creates all horizontal lines at intevals of 100
        for j in range(0, win_height, GRID_STEP):
            canvas.create_line([(0, j), (win_width, j)], tag='grid_line', fill='gray')

    def add_some_points(self):
        cell_x = 71
        cell_y = 40
        self.cell_status[cell_x][cell_y - 1] = True
        self.cell_status[cell_x - 1][cell_y - 1] = True
        self.cell_status[cell_x][cell_y] = True
        self.cell_status[cell_x - 1][cell_y] = True
        self.cell_status[cell_x - 2][cell_y] = True

    def life_cycle(self):
        self.redraw_alive_cells()
        new_cell_status = copy.deepcopy(self.cell_status)
        for i in range(0, VISIBLE_AREA, 1):
            for j in range(0, VISIBLE_AREA, 1):
                check_neighbors = 0
                for k in range(({True: i - 1, False: 0} [i > 0]), ({True: i + 2, False: VISIBLE_AREA} [i < VISIBLE_AREA - 1]), 1):
                    for l in range(({True: j - 1, False: 0} [j > 0]), ({True: j + 2, False: VISIBLE_AREA} [j < VISIBLE_AREA - 1]), 1):
                        if not(i == k and j == l):
                            if self.cell_status[k][l] == True:
                                check_neighbors += 1
                if self.cell_status[i][j]:
                    if check_neighbors != 2 and check_neighbors != 3:
                        new_cell_status[i][j] = False
                else:
                    if check_neighbors == 3:
                        new_cell_status[i][j] = True

        self.cell_status = copy.deepcopy(new_cell_status)
        root.after(int(GAME_SPEED), self.life_cycle)

    def redraw_alive_cells(self):
        canvas.delete('alive_cell')
        for i in range(0, VISIBLE_AREA, 1):
            for j in range(0, VISIBLE_AREA, 1):
                if self.cell_status[i][j] == 1:
                    canvas.create_rectangle(1 + GRID_STEP * i, 1 + GRID_STEP * j, GRID_STEP * (i + 1), GRID_STEP * (j + 1), fill='green', tag='alive_cell', width=0)

    def show_cells_status(self):
        print(self.cell_status)

# ==========================================================================================

def main():
    global root
    root = tk.Tk()

    global canvas
    canvas = tk.Canvas(root, height=700, width=1400, bg='black')
    canvas.pack(fill = tk.BOTH, expand = True)
    canvas.update()

    game = Game()

    root.mainloop()

if __name__ == '__main__':
    main()