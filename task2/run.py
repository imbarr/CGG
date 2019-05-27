import math
import tkinter as tk
from tkinter import Canvas, Tk


class App(Tk):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def plot(self, x, y):
        self.canvas.create_line(960 + x, 540 - y, 961 + x, 540 - y, fill="black")

    def plot_all(self, x, y, b, c):
        self.plot(x, y)
        self.plot(y - c - b, x + b + c)
        self.plot(- 2*b - x, 2*c - y)
        self.plot(c - y - b, - x - b + c)

    def draw_hyperbola_slow(self, a, b, c):
        y = int(math.sqrt(a))
        for x in range(y, 10000):
            self.plot_all(x, y, b, c)
            delta = 2*x*y - 2*x*c + 2*y - 2*c + 2*b*y - 2*b*c - b - 1 - x - 2*a
            if delta > 0:
                y -= 1

    def draw_hyperbola_fast(self, a, b, c):
        x0 = int(math.sqrt(a)) - b
        y = int(math.sqrt(a)) + c
        delta = -math.sqrt(a)
        for x in range(int(x0), int(x0) + 1920):
            self.plot_all(x, y, b, c)
            if delta > 0:
                y -= 1
                delta += 2*y - 2*x - 2*c - 2*b - 5
            else:
                delta += 2*y - 2*c - 1


if __name__ == '__main__':
    app = App()
    app.canvas.create_line(960, 0, 960, 1080, fill="red")
    app.canvas.create_line(0, 540, 1920, 540, fill="red")
    app.draw_hyperbola_fast(10000, 200, 200)
    app.mainloop()
