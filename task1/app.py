from tkinter import Frame, OptionMenu, Entry, StringVar, DoubleVar, Canvas, Tk, Label, TclError
import tkinter as tk
from threading import Thread
from algorithm import Drawer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
app = config['app']


class App(Tk):
    def __init__(self, functions, master=None, **kw):
        super().__init__(master, **kw)
        self.functions = functions

        self.configure(background=app['theme'])
        wrapper = Frame(self, background=app['theme'])
        wrapper.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
        wrapper.rowconfigure(7, weight=1)
        wrapper.columnconfigure(3, weight=1)

        self.create_entries(wrapper)
        self.create_canvas(wrapper)
        self.bind_redraw_events()
        self.drawing = False

    def create_entries(self, master):
        self.func = App.create_function_entry(master, self.functions)
        self.left = App.create_real_entry(master, text='Левая граница', row=2, initial_value=-0.1)
        self.right = App.create_real_entry(master, text='Правая граница', row=3, initial_value=0.1)
        self.a = App.create_real_entry(master, text='a', row=4, initial_value=1)
        self.b = App.create_real_entry(master, text='b', row=5, initial_value=1)
        self.c = App.create_real_entry(master, text='c', row=6, initial_value=1)

    def create_canvas(self, master):
        canvas_wrapper = Frame(master, background=app['canvas'])
        canvas_wrapper.grid(row=7, column=1, columnspan=3, sticky=tk.N + tk.S + tk.W + tk.E)
        self.canvas = Canvas(canvas_wrapper, borderwidth=0, highlightthickness=0, background=app['canvas'])
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def bind_redraw_events(self):
        self.canvas.bind("<Configure>", self.retrieve_parameters_and_draw)
        for widget in [self.func, self.left, self.right, self.a, self.b, self.c]:
            widget.trace("w", self.retrieve_parameters_and_draw)

    @staticmethod
    def create_function_entry(master, functions):
        Label(master, text='Функция', background=app['theme'])\
            .grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)
        func = StringVar(master)
        func.set(list(functions)[0])
        func_entry = OptionMenu(master, func, *list(functions))
        func_entry.configure(borderwidth=0)
        func_entry.grid(row=1, column=2, sticky=tk.W + tk.E)
        return func

    @staticmethod
    def create_real_entry(master, text, row, initial_value):
        Label(master, text=text, background=app['theme'])\
            .grid(row=row, column=1, sticky=tk.E, padx=10, pady=5)
        var = DoubleVar(master)
        var.set(initial_value)
        left_entry = Entry(master, textvariable=var)
        left_entry.grid(row=row, column=2, sticky=tk.W)
        return var

    def retrieve_parameters_and_draw(self, *args):
        try:
            a, b, c = self.a.get(), self.b.get(), self.c.get()
            left, right = self.left.get(), self.right.get()
            function = self.functions[self.func.get()]
            width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
            self.async_draw(width, height, left, right, lambda x: function(x, a, b, c))
        except TclError:
            self.show_message("Некорректные параметры")

    def async_draw(self, width, height, left, right, func):
        def draw():
            self.drawing = True
            self.canvas.delete('all')
            self.canvas.pack_forget()
            drawer = Drawer(width, height, left, right, func, self.draw_line)
            try:
                drawer.draw()
            except (ArithmeticError, ValueError, TypeError):
                self.show_message("Функция не определена")
            self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
            self.drawing = False

        if not self.drawing:
            Thread(target=draw).start()

    def show_message(self, text):
        self.canvas.delete('all')
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.create_text(width / 2, height / 2, text=text)

    def draw_line(self, x1, y1, x2, y2, color):
        self.canvas.create_line(x1, y1, x2, y2, fill=color)
