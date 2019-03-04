from tkinter import Frame, OptionMenu, Entry, StringVar, DoubleVar, Canvas, BOTH, YES, END, Tk, Label, S, N, E, W, TclError
import numpy as np
from threading import Thread
import math


class App(Tk):
    def __init__(self, functions, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(background='grey77')
        f = Frame(self, background='grey77')
        f.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        f.rowconfigure(7, weight=1)
        f.columnconfigure(3, weight=1)

        Label(f, text='Функция', background='grey77').grid(row=1, column=1, sticky=E, padx=10, pady=5)
        func = StringVar(f)
        func.set(list(functions)[0])
        func_entry = OptionMenu(f, func, *list(functions))
        func_entry.configure(borderwidth=0)
        func_entry.grid(row=1, column=2, sticky=W+E)

        Label(f, text='Левая граница', background='grey77').grid(row=2, column=1, sticky=E, padx=10, pady=5)
        left = DoubleVar(f)
        left.set(-0.1)
        left_entry = Entry(f, textvariable=left)
        left_entry.grid(row=2, column=2, sticky=W)

        Label(f, text='Правая граница', background='grey77').grid(row=3, column=1, sticky=E, padx=10, pady=5)
        right = DoubleVar(f)
        right.set(0.1)
        right_entry = Entry(f, textvariable=right)
        right_entry.grid(row=3, column=2, sticky=W)

        Label(f, text='a', background='grey77').grid(row=4, column=1, sticky=E, padx=10, pady=5)
        a_var = DoubleVar(f)
        a_var.set(1)
        a_entry = Entry(f, textvariable=a_var)
        a_entry.grid(row=4, column=2, sticky=W)

        Label(f, text='b', background='grey77').grid(row=5, column=1, sticky=E, padx=10, pady=5)
        b_var = DoubleVar(f)
        b_var.set(1)
        b_entry = Entry(f, textvariable=b_var)
        b_entry.grid(row=5, column=2, sticky=W)

        Label(f, text='c', background='grey77').grid(row=6, column=1, sticky=E, padx=10, pady=5)
        c_var = DoubleVar(f)
        c_var.set(1)
        c_entry = Entry(f, textvariable=c_var)
        c_entry.grid(row=6, column=2, sticky=W)

        self.canvas = Canvas(f, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=7, column=1, columnspan=3, sticky=N+S+W+E)

        def draw(*args):
            try:
                a, b, c = a_var.get(), b_var.get(), c_var.get()
                l, r = left.get(), right.get()

                def reduced(x):
                    return functions[func.get()](x, a, b, c)

                width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
                self.async_draw(width, height, reduced, l, r)
            except TclError:
                pass

        self.canvas.bind("<Configure>", draw)
        func.trace("w", draw)
        left.trace("w", draw)
        right.trace("w", draw)
        a_var.trace("w", draw)
        b_var.trace("w", draw)
        c_var.trace("w", draw)

        self.draw_thread = None
        self.drawing = False

    def async_draw(self, *args):
        def draw_with_flags():
            self.drawing = True
            self.canvas.grid_forget()
            self.draw(*args)
            self.canvas.grid(row=7, column=1, columnspan=3, sticky=N+S+W+E)
            self.drawing = False

        if self.drawing:
            self.draw_thread._stop()
        self.draw_thread = Thread(target=draw_with_flags).start()

    def draw(self, width, height, func, left, right):
        self.canvas.delete('all')
        step_x = (right - left) / width
        inf, top = self.span(width, func, left, right)
        step_y = (top - inf)/height
        step = max(step_x, step_y)
        shift_x = (1 - step_x/step)*width/2
        shift_y = (1 - step_y/step)*height/2

        to_screen_x = lambda x: shift_x + (x - left) / step
        to_screen_y = lambda y: height - (y - inf)/step - shift_y
        from_screen_x = lambda x: (x - shift_x) * step + left
        from_screen_y = lambda y: (- y + height - shift_y)*step + inf
        screen_func = lambda x: to_screen_y(func(from_screen_x(x)))

        for x in range(math.ceil(from_screen_x(0)), math.floor(from_screen_x(width)) + 1):
            self.canvas.create_line(to_screen_x(x), 0, to_screen_x(x), height, fill='gray69')

        for y in range(math.floor(from_screen_y(height)), math.ceil(from_screen_y(0)) + 1):
            self.canvas.create_line(0, to_screen_y(y), width, to_screen_y(y), fill='gray69')

        self.canvas.create_line(0, to_screen_y(0), width, to_screen_y(0), fill='gray30')
        self.canvas.create_line(to_screen_x(0), 0, to_screen_x(0), height, fill='gray30')

        for x in range(int(to_screen_x(left)), int(to_screen_x(right)) + 1):
            self.canvas.create_line(x, screen_func(x), x + 1, screen_func(x + 1), fill='black')

    def span(self, width, func, left, right):
        inf, sup = [func(left)] * 2
        for x in np.linspace(left, right, width):
            y = func(x)
            if y < inf:
                inf = y
            if y > sup:
                sup = y
        return inf, sup
