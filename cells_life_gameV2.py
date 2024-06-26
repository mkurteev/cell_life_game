import tkinter as tk
import time
import copy

GRID_STEP = 10
VISIBLE_AREA = 1000
GAME_SPEED = 500

class Game:
    def __init__(self) -> None:
        self.alive_cell = []
        self.active_area = []
        self.alive_cell_count = 0
        self.life_in_progress = False

        self.create_grid()
        self.add_some_points()

    def life_toggle(self):
        pass

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

        # self.btn = tk.Button(root, text="Get Answer", command=self.life_toggle)
        # self.btn.pack(side=tk.LEFT, padx=15, pady=15)

        # self.label = tk.Label(root, text=f'Живых клеток: {self.alive_cell_count}', font=('consolas', 24))
        # self.label.pack(side=tk.LEFT)

    def add_some_points(self):
        self.alive_cell.append([67, 36])
        self.alive_cell.append([68, 37])
        self.alive_cell.append([69, 37])
        self.alive_cell.append([69, 38])
        self.alive_cell.append([68, 39])
        # self.alive_cell.append([6, 9])

    def is_it_alive(self, x, y):
        if [x, y] in self.alive_cell:
            return True
        else:
            return False
        
    def get_active_area(self):
        self.active_area = copy.deepcopy(self.alive_cell)
        for coords1 in self.alive_cell:
            x1, y1 = coords1
            for coords2 in self.get_cell_env(x1, y1):
                x2, y2 = coords2
                if [x2, y2] not in self.active_area:
                    self.active_area.append([x2, y2])

    def get_cell_env(self, x, y):
        env_list = []
        for k in range(({True: x - 1, False: 0} [x > 0]), ({True: x + 2, False: VISIBLE_AREA} [x < VISIBLE_AREA - 1]), 1):
            for l in range(({True: y - 1, False: 0} [y > 0]), ({True: y + 2, False: VISIBLE_AREA} [y < VISIBLE_AREA - 1]), 1):
                if not(x == k and y == l): env_list.append([k, l])
        return env_list

    def life_cycle(self):
        self.redraw_alive_cells()
        self.get_active_area()
        active_area_temp = []
        active_area_temp = copy.deepcopy(self.active_area)

        for coords1 in self.active_area:
            x1, y1 = coords1
            check_neighbors = 0

            for coords2 in self.get_cell_env(x1, y1):
                x2, y2 = coords2
                if [x2, y2] in self.alive_cell:
                    check_neighbors += 1

            # print(f'x: {x1}, y: {y1} = {check_neighbors}')
            if [x1, y1] in self.alive_cell:
                if check_neighbors != 2 and check_neighbors != 3:
                    active_area_temp.remove([x1, y1])
                    pass
            else:
                if check_neighbors != 3:
                    active_area_temp.remove([x1, y1])
                    pass

        
        self.alive_cell = copy.deepcopy(active_area_temp)
        self.redraw_alive_cells()
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