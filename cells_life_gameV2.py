import tkinter as tk
import copy

GRID_STEP = 10
VISIBLE_AREA = 10
GAME_SPEED = 1000

class Game:
    def __init__(self) -> None:
        self.alive_cell = []
        self.create_grid()
        self.add_some_points()
        print(self.alive_cell)
        self.redraw_alive_cells()
        print(self.is_it_alive(8,7))
        print(self.is_it_alive(8,2))
        print(self.is_it_alive(8,9))

    def create_grid(self):
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
        self.alive_cell.append([7, 6])
        self.alive_cell.append([8, 7])
        self.alive_cell.append([9, 7])
        self.alive_cell.append([9, 8])
        self.alive_cell.append([8, 9])

    def is_it_alive(self, x, y):
        if [x, y] in self.alive_cell:
            return True
        else:
            return False

    def life_cycle(self):
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
        for coords in self.alive_cell:
            x, y = coords
            canvas.create_rectangle(1 + GRID_STEP * x, 1 + GRID_STEP * y, GRID_STEP * (x + 1), GRID_STEP * (y + 1), fill='green', tag='alive_cell', width=0)

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