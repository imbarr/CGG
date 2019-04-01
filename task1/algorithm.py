from math import ceil
import configparser

import numpy as np

config = configparser.ConfigParser()
config.read('config.ini')
colors = config['colors']


class Drawer:
    def __init__(self, width, height, left, right, func, draw_line):
        np.seterr(*(['raise']*5))

        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.func = func
        self.draw_line = draw_line

    def draw(self):
        self.count_bounds()
        self.count_steps()
        self.count_shifts()
        self.draw_grid()
        self.draw_axis()
        self.draw_func()

    def count_bounds(self):
        self.inf, self.sup = [self.func(self.left)]*2
        for x in np.linspace(self.left, self.right, self.width):
            y = self.func(x)
            if y < self.inf:
                self.inf = y
            elif y > self.sup:
                self.sup = y

    def count_steps(self):
        horizontal_pixels = self.right - self.left
        vertical_pixels = self.sup - self.inf
        self.step_x = horizontal_pixels / self.width
        self.step_y = vertical_pixels / self.height
        self.step = max(self.step_x, self.step_y)

    def count_shifts(self):
        empty_horizontal_space_share = 1 - self.step_x / self.step
        self.shift_x = empty_horizontal_space_share * self.width / 2
        empty_vertical_space_share = 1 - self.step_y / self.step
        self.shift_y = empty_vertical_space_share * self.height / 2

    def draw_grid(self):
        step = self.get_grid_step()
        left = self.from_screen_x(0)
        right = self.from_screen_x(self.width)
        top = self.from_screen_y(0)
        bottom = self.from_screen_y(self.height)

        negative_x = np.arange(0, left, -step)
        positive_x = np.arange(0, right, step)
        for x in np.concatenate((negative_x, positive_x)):
            self.draw_vertical_grid_line(x)

        negative_y = np.arange(0, bottom, -step)
        positive_y = np.arange(0, top, step)
        for y in np.concatenate((negative_y, positive_y)):
            self.draw_horizontal_grid_line(y)

    def draw_axis(self):
        zero_x = self.to_screen_x(0)
        zero_y = self.to_screen_y(0)
        self.draw_line(0, zero_y, self.width, zero_y, colors['axis'])
        self.draw_line(zero_x, 0, zero_x, self.height, colors['axis'])

    def draw_func(self):
        screen_left = int(self.to_screen_x(self.left))
        screen_right = int(ceil(self.to_screen_x(self.right)))
        for x in range(screen_left, screen_right):
            self.draw_line(x, self.screen_func(x), x + 1, self.screen_func(x + 1), colors['function'])

    def to_screen_x(self, x):
        length = x - self.left
        return self.shift_x + self.to_screen_length(length)

    def to_screen_y(self, y):
        length = y - self.inf
        flipped_screen_y = self.shift_y + self.to_screen_length(length)
        return self.height - flipped_screen_y

    def from_screen_x(self, x):
        screen_length = x - self.shift_x
        length = self.from_screen_length(screen_length)
        return self.left + length

    def from_screen_y(self, y):
        screen_length = y - self.shift_y
        flipped_screen_length = self.height - screen_length
        length = self.from_screen_length(flipped_screen_length)
        return self.inf + length

    def to_screen_length(self, length):
        return length / self.step

    def from_screen_length(self, length):
        return length * self.step

    def get_grid_step(self):
        # TODO: change alg
        return int(ceil(20*self.step))

    def draw_vertical_grid_line(self, x):
        screen_x = self.to_screen_x(x)
        self.draw_line(screen_x, 0, screen_x, self.height, colors['grid'])

    def draw_horizontal_grid_line(self, y):
        screen_y = self.to_screen_y(y)
        self.draw_line(0, screen_y, self.width, screen_y, colors['grid'])

    def screen_func(self, screen_x):
        x = self.from_screen_x(screen_x)
        y = self.func(x)
        screen_y = self.to_screen_y(y)
        return screen_y
