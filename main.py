from tkinter import Tk, Canvas, Menu, filedialog
import time
import os
import json


with open('settings.json') as f:
    settings = json.load(f)

X = settings['x']
Y = settings['y']
CANVAS_SIZE = settings['canvas_size']
DELAY = settings['delay']

root = Tk()
root.title('Maze Solver')

canvas = Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
canvas.grid(row=0)


class Maze:
    def __init__(self, canvas: Canvas, file: str, delay: int):
        with open(file) as f:
            self.maze = [[True if x == '.' else False for x in r] for r in f.readlines()]
        self.canvas = canvas
        self.size = len(self.maze)
        self.pixel_size = CANVAS_SIZE / self.size
        self.delay = delay
        self.solved = False

    def show(self):
        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_rectangle(i * self.pixel_size, j * self.pixel_size,
                                        (i + 1) * self.pixel_size, (j + 1) * self.pixel_size,
                                        fill='white' if self.maze[j][i] else 'black', outline='')
        root.update()
        root.update_idletasks()

    def __solve_with_animation(self, x, y, history=None, route=None):
        if not self.solved:
            if not history:
                history = [[False] * len(self.maze) for _ in range(len(self.maze))]
            if not route:
                route = tuple()

            history[y][x] = True
            route = (*route, [x, y])

            canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                    (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                    fill='purple', outline='')
            root.update()
            root.update_idletasks()
            time.sleep(self.delay)

            if 0 < x:
                if self.maze[y][x - 1] and not history[y][x - 1]:
                    self.__solve_with_animation(x - 1, y, history, route)
            if x < self.size - 1:
                if self.maze[y][x + 1] and not history[y][x + 1]:
                    self.__solve_with_animation(x + 1, y, history, route)
            if 0 < y:
                if self.maze[y - 1][x] and not history[y - 1][x]:
                    self.__solve_with_animation(x, y - 1, history, route)
            if y < self.size - 1:
                if self.maze[y + 1][x] and not history[y + 1][x]:
                    self.__solve_with_animation(x, y + 1, history, route)
            if x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1:
                for x, y in route:
                    canvas.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                            (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                            fill='green', outline='')

                self.solved = True

    def animation(self, x, y):
        self.solved = False
        self.show()
        self.__solve_with_animation(x, y)


menu = Menu(root)
root.config(menu=menu)

maze = None


def new_maze():
    global maze
    if maze:
        maze.solved = True

    file = filedialog.askopenfilename(initialdir=os.getcwd())
    maze = Maze(canvas, file, DELAY)
    maze.show()


def animation():
    if isinstance(maze, Maze):
        maze.animation(X, Y)


menu.add_command(label='New', command=new_maze)
menu.add_command(label='Play', command=animation)

root.mainloop()
