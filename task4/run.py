from math import sin, cos, sqrt
import tkinter as tk
from tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageTk

colors = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255)
}

primary_step = 50
p1 = (-5, -3)
p2 = (2, 4)


class App(Tk):
    def __init__(self, width, height, function, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.width, self.height, self.function = width, height, function

        self.primary_step = primary_step
        self.secondary_step = self.width + self.height
        self.min_x, self.max_x = (0, 0)
        self.min_y, self.max_y = self.min_x, self.max_x

        image = Image.new('RGB', (width, height), colors['white'])
        self.draw = ImageDraw.Draw(image)
        self.draw_graphic()
        image_tk = ImageTk.PhotoImage(image)
        label = Label(self, image=image_tk)
        label.image = image_tk  # IMPORTANT
        label.pack(side="bottom", fill=tk.BOTH, expand=tk.YES)

    def draw_graphic(self):
        self.set_boundaries()
        self.draw_lines_x()
        self.draw_lines_y()

    def set_boundaries(self):
        for i in range(self.primary_step):
            x = x_with_step(i, self.primary_step)
            for j in range(self.secondary_step):
                y = y_with_step(j, self.secondary_step)
                self.set_boundaries_for(x, y)
        for i in range(self.primary_step):
            y = y_with_step(i, self.primary_step)
            for j in range(self.secondary_step):
                x = x_with_step(j, self.secondary_step)
                self.set_boundaries_for(x, y)

    def draw_lines_x(self):
        top, bottom = self.get_initial_top_and_bottom()
        for i in range(self.primary_step):
            x = x_with_step(i, self.primary_step)
            for j in range(self.secondary_step):
                y = y_with_step(j, self.secondary_step)
                self.draw_point(x, y, top, bottom)

    def draw_lines_y(self):
        top, bottom = self.get_initial_top_and_bottom()
        for i in range(self.primary_step):
            y = y_with_step(i, self.primary_step)
            for j in range(self.secondary_step):
                x = x_with_step(j, self.secondary_step)
                self.draw_point(x, y, top, bottom)

    def set_boundaries_for(self, x, y):
        z = self.function(x, y)
        xx, yy = isometric_projection(x, y, z)
        self.max_x, self.min_x = max(self.max_x, xx), min(self.min_x, xx)
        self.max_y, self.min_y = max(self.max_y, yy), min(self.min_y, yy)

    def get_initial_top_and_bottom(self):
        n = self.width + 1
        return [self.height] * n, [0] * n

    def draw_point(self, x, y, top, bottom):
        z = self.function(x, y)
        old_xx, old_yy = isometric_projection(x, y, z)
        xx = round((old_xx - self.min_x) / (self.max_x - self.min_x) * self.width)
        yy = round((old_yy - self.min_y) / (self.max_y - self.min_y) * self.height)
        if yy > bottom[xx]:
            self.plot(xx, yy, colors['red'])
            bottom[xx] = yy
        if yy < top[xx]:
            self.plot(xx, yy, colors['blue'])
            top[xx] = yy

    def plot(self, x, y, color):
        self.draw.point((x, y), color)


def isometric_projection(x, y, z):
    return (y - x) * sqrt(3) / 2, (x + y) / 2 - z


def x_with_step(i, steps):
    x1, x2 = p1[0], p2[0]
    return x2 + i * (x1 - x2) / steps


def y_with_step(j, steps):
    y1, y2 = p1[1], p2[1]
    return y2 + j * (y1 - y2) / steps


if __name__ == "__main__":
    app = App(1920, 1000, lambda x, y: sqrt(x ** 2 + y ** 2) + 3 * cos(sqrt(x ** 2 + y ** 2)) + 5)
    app.mainloop()
