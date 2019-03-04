from tkinter import Frame, Canvas, BOTH, YES
import numpy as np


class App(Frame):
    def __init__(self, func, a, b, master=None, **kw):
        super().__init__(master, **kw)
        self.pack(fill=BOTH, expand=YES)
        self.func = func
        self.a = a
        self.b = b
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.bind("<Configure>", lambda e: self.draw(e.width, e.height, self.func, self.a, self.b))

    def span(self, width, func, a, b):
        inf, sup = [func(a)] * 2
        for x in np.linspace(a, b, width):
            y = func(x)
            if y < inf:
                inf = y
            if y > sup:
                sup = y
        return inf, sup

    def draw(self, width, height, func, a, b):
        self.canvas.delete('all')
        step_x = (b - a)/width
        inf, top = self.span(width, func, a, b)
        step_y = (top - inf)/height
        step = max(step_x, step_y)
        shift_x = (1 - step_x/step)*width/2
        shift_y = (1 - step_y/step)*height/2

        to_screen_x = lambda x: shift_x + (x - a)/step
        to_screen_y = lambda y: height - (y - inf)/step - shift_y
        from_screen_x = lambda x: (x - shift_x)*step + a
        # from_screen_y = lambda y: (y + inf)*step - self.height + shift_y
        screen_func = lambda x: to_screen_y(func(from_screen_x(x)))

        self.canvas.create_line(0, to_screen_y(0), width, to_screen_y(0), fill='green')
        self.canvas.create_line(to_screen_x(0), 0, to_screen_x(0), height, fill='green')

        for x in range(int(to_screen_x(a)), int(to_screen_x(b)) + 1):
            self.canvas.create_line(x, screen_func(x), x + 1, screen_func(x + 1))
