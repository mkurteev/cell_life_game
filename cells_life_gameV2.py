import tkinter as tk
import copy
import mouse
from tkinter import messagebox
from tkinter import filedialog

GRID_STEP = 10
VISIBLE_AREA = 1000
START_GAME_SPEED = 300
FRAME_WIDTH = 2

class Game():
    def __init__(self) -> None:
        self.alive_cell = []
        self.active_area = []
        self.last_start_dump = []
        self.alive_cell_count = 0
        self.speed = START_GAME_SPEED
        self.life_in_progress = False

        self.create_grid()
        self.add_widgets()

    def life_toggle(self):
        if self.life_in_progress:
            self.btn.config(text="Старт", font = ('Sans','10'), bg='green')
        else:
            self.btn.config(text="Стоп", font = ('Sans','10','bold'), bg='red')

        self.life_in_progress = not self.life_in_progress
        if self.life_in_progress: 
            self.last_start_dump = copy.deepcopy(self.alive_cell)
            self.life_cycle()

    def restore_cells(self, dump=None):
        if not self.life_in_progress:
            if dump:
                self.alive_cell = copy.deepcopy(dump)
            else:
                self.alive_cell.clear()

            self.redraw_alive_cells()
            self.update_label()
        else:
            self.in_progress_info()

    def speed_up(self):
        if self.speed < 9500:
            self.speed = self.speed * 2
            self.update_label()

    def speed_down(self):
        if self.speed > 10:
            self.speed = self.speed / 2
            self.update_label()

    def in_progress_info(self):
        messagebox.showinfo("Невозможно", "Сначала нажмите 'Стоп'")

    def save_to_file(self):
        if not self.life_in_progress:
            file_path = filedialog.asksaveasfilename(title="Выберите файл для сохранения...", \
                                                    filetypes = [('Text Document', '*.txt')], defaultextension = [('Text Document', '*.txt')])
            if file_path:
                with open(file_path, mode='w+') as file:
                    for coords in self.alive_cell:
                        file.write('%s\n' %",".join(map(str, coords)))
                file.close()
        else:
            self.in_progress_info()

    def load_from_file(self):
        if not self.life_in_progress:
            file_path = filedialog.askopenfilename(title="Выберите файл для загрузки...", filetypes=[("Text files", "*.txt")])
            if file_path:
                dump_from_file = []
                file = open(file_path, 'r')
                for f_string in file.readlines():
                    dump_from_file.append(list(map(int, f_string.replace('\n', '').split(','))))
                file.close()
                self.restore_cells(dump_from_file)
        else:
            self.in_progress_info()

    def mouse_click_cell(self, event=None):
        x_click = canvas.winfo_pointerx() - canvas.winfo_rootx() - FRAME_WIDTH
        y_click = canvas.winfo_pointery() - canvas.winfo_rooty() - FRAME_WIDTH
        x_cell = (x_click // GRID_STEP)
        y_cell = (y_click // GRID_STEP)
        self.toggle_cell(x_cell, y_cell)

    def create_grid(self, event=None):
        win_width = canvas.winfo_width() # Get current width of canvas
        win_height = canvas.winfo_height() # Get current height of canvas
        canvas.delete('grid_line')

        # Creates all vertical lines at intevals of 100
        for i in range(0, win_width, GRID_STEP):
            canvas.create_line([(i, 0), (i, win_height)], tag='grid_line', fill='gray')

        # Creates all horizontal lines at intevals of 100
        for j in range(0, win_height, GRID_STEP):
            canvas.create_line([(0, j), (win_width, j)], tag='grid_line', fill='gray')

    def add_widgets(self):
        self.btn = tk.Button(root, text="Старт", font = ('Sans','10'), bg='green', width=8, command=self.life_toggle)
        self.btn.pack(side=tk.LEFT, padx=10, pady=15)

        self.btn_erase = tk.Button(root, text="Сброс", width=8, command=self.restore_cells)
        self.btn_erase.pack(side=tk.LEFT, pady=15)

        self.btn_restore = tk.Button(root, text="Восстан.", width=8, command=lambda: self.restore_cells(self.last_start_dump))
        self.btn_restore.pack(side=tk.LEFT, padx=10, pady=15)

        self.btn_save = tk.Button(root, text="Сохран.", width=8, command=self.save_to_file)
        self.btn_save.pack(side=tk.LEFT, pady=15)

        self.btn_open = tk.Button(root, text="Загруз.", width=8, command=self.load_from_file)
        self.btn_open.pack(side=tk.LEFT, padx=10, pady=15)

        self.btn_speed_minus = tk.Button(root, text="-", width=2, command=self.speed_down)
        self.btn_speed_minus.pack(side=tk.LEFT, padx=5, pady=15)

        self.label_speed = tk.Label(root, text=f'Шаг: {round(self.speed / 1000, 2)} c', width=10, font=('consolas', 12))
        self.label_speed.pack(side=tk.LEFT)

        self.btn_speed_plus = tk.Button(root, text="+", width=2, command=self.speed_up)
        self.btn_speed_plus.pack(side=tk.LEFT, padx=5, pady=15)

        self.label = tk.Label(root, text=f'Живых клеток: {self.alive_cell_count}', width=20, font=('consolas', 24))
        self.label.pack(side=tk.RIGHT, padx=15)

    def update_label(self):
        self.alive_cell_count = len(self.alive_cell)
        self.label.config(text=f'Живых клеток: {self.alive_cell_count}')

        self.label_speed.config(text=f'Шаг: {round(self.speed / 1000, 2)} c')

    def toggle_cell(self, x, y):
        if not self.life_in_progress:
            if self.is_it_alive(x, y):
                self.alive_cell.remove([x, y])
            else:
                self.alive_cell.append([x, y])
            self.redraw_alive_cells()
            self.update_label()
        else:
            messagebox.showinfo("Невозможно", "Сначала нажмите 'Стоп'") 

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
                if check_neighbors < 2 or check_neighbors > 3:
                    active_area_temp.remove([x1, y1])
                    pass
            else:
                if check_neighbors != 3:
                    active_area_temp.remove([x1, y1])
                    pass

        
        self.alive_cell = copy.deepcopy(active_area_temp)
        self.redraw_alive_cells()
        self.update_label()

        if self.life_in_progress:
            root.after(int(self.speed), self.life_cycle)

    def redraw_alive_cells(self):
        canvas.delete('alive_cell')
        for coords in self.alive_cell:
            x, y = coords
            canvas.create_rectangle(1 + GRID_STEP * x, 1 + GRID_STEP * y, GRID_STEP * (x + 1), GRID_STEP * (y + 1), fill='green', tag='alive_cell', width=0)

# ==========================================================================================

def main():
    global root
    root = tk.Tk()
    root.title("Игра жизнь (клеточный автомат)")

    global canvas
    canvas = tk.Canvas(root, height=400, width=600, bg='black')
    canvas.pack(fill = tk.BOTH, expand = True)
    canvas.update()

    game = Game()
    root.bind("<Configure>", game.create_grid)
    canvas.bind("<Button-1>", game.mouse_click_cell)
    messagebox.showinfo("О игре", "Игровое поле - чашка Петри, в ней развиваются клетки.\n\
Черные клетки - мертвые, зеленые - живые.\n\n\
Перед тем как запустить жизнь, игрок выбирает начальное состояние - какие клетки живые в начале.\n\n\
Каждый шаг иргы развивается новое поколение по выбранным правилам.\n\n\
Например стандартные правила B3\S23 - клетка рождается в следующем покалении, если в предыдущем у нее было 3 соседних живых клетки, и продолжает жить, если у нее 2 или 3 соседа.\n\n\
")

    root.mainloop()

if __name__ == '__main__':
    main()