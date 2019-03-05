from tkinter import Frame, OptionMenu, Entry, StringVar, DoubleVar, Canvas, BOTH, YES, END, Tk, Label, S, N, E, W, TclError
from threading import Thread
from algorithm import draw
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
app = config['app']


class App(Tk):
    def __init__(self, functions, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(background=app['theme'])
        f = Frame(self, background=app['theme'])
        f.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        f.rowconfigure(7, weight=1)
        f.columnconfigure(3, weight=1)

        Label(f, text='Функция', background=app['theme']).grid(row=1, column=1, sticky=E, padx=10, pady=5)
        func = StringVar(f)
        func.set(list(functions)[0])
        func_entry = OptionMenu(f, func, *list(functions))
        func_entry.configure(borderwidth=0)
        func_entry.grid(row=1, column=2, sticky=W+E)

        Label(f, text='Левая граница', background=app['theme']).grid(row=2, column=1, sticky=E, padx=10, pady=5)
        left = DoubleVar(f)
        left.set(-0.1)
        left_entry = Entry(f, textvariable=left)
        left_entry.grid(row=2, column=2, sticky=W)

        Label(f, text='Правая граница', background=app['theme']).grid(row=3, column=1, sticky=E, padx=10, pady=5)
        right = DoubleVar(f)
        right.set(0.1)
        right_entry = Entry(f, textvariable=right)
        right_entry.grid(row=3, column=2, sticky=W)

        Label(f, text='a', background=app['theme']).grid(row=4, column=1, sticky=E, padx=10, pady=5)
        a_var = DoubleVar(f)
        a_var.set(1)
        a_entry = Entry(f, textvariable=a_var)
        a_entry.grid(row=4, column=2, sticky=W)

        Label(f, text='b', background=app['theme']).grid(row=5, column=1, sticky=E, padx=10, pady=5)
        b_var = DoubleVar(f)
        b_var.set(1)
        b_entry = Entry(f, textvariable=b_var)
        b_entry.grid(row=5, column=2, sticky=W)

        Label(f, text='c', background=app['theme']).grid(row=6, column=1, sticky=E, padx=10, pady=5)
        c_var = DoubleVar(f)
        c_var.set(1)
        c_entry = Entry(f, textvariable=c_var)
        c_entry.grid(row=6, column=2, sticky=W)

        canvas_wrapper = Frame(f, background=app['canvas'])
        canvas_wrapper.grid(row=7, column=1, columnspan=3, sticky=N+S+W+E)
        self.canvas = Canvas(canvas_wrapper, borderwidth=0, highlightthickness=0, background=app['canvas'])
        self.canvas.pack(fill=BOTH, expand=YES)

        def draw_all(*args):
            try:
                a, b, c = a_var.get(), b_var.get(), c_var.get()
                l, r = left.get(), right.get()
                function = functions[func.get()]

                def reduced(x):
                    return function(x, a, b, c)

                width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
                self.async_draw(width, height, reduced, l, r, self.line)
            except TclError:
                pass

        self.canvas.bind("<Configure>", draw_all)

        for widget in [func, left, right, a_var, b_var, c_var]:
            widget.trace("w", draw_all)

        self.drawing = False

    def line(self, x1, y1, x2, y2, color):
        self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def async_draw(self, *args):
        def draw_with_flags():
            self.drawing = True
            self.canvas.delete('all')
            self.canvas.pack_forget()
            try:
                draw(*args)
            except Exception:
                pass
            self.canvas.pack(fill=BOTH, expand=YES)
            self.drawing = False

        if not self.drawing:
            Thread(target=draw_with_flags).start()

