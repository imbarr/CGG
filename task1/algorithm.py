from math import ceil
import configparser

import numpy as np

config = configparser.ConfigParser()
config.read('config.ini')
colors = config['colors']


def draw(width, height, func, left, right, line):
    inf, sup = [func(left)] * 2
    for x in np.linspace(left, right, width):
        y = func(x)
        if y < inf:
            inf = y
        if y > sup:
            sup = y

    step_x = (right - left) / width
    step_y = (sup - inf) / height
    step = max(step_x, step_y)
    shift_x = (1 - step_x / step) * width / 2
    shift_y = (1 - step_y / step) * height / 2

    to_screen_x = lambda x: shift_x + (x - left) / step
    to_screen_y = lambda y: height - (y - inf) / step - shift_y
    from_screen_x = lambda x: (x - shift_x) * step + left
    from_screen_y = lambda y: (- y + height - shift_y) * step + inf
    screen_func = lambda x: to_screen_y(func(from_screen_x(x)))

    grid_step = int(ceil(20*step))

    for x in range(0, ceil(from_screen_x(width)), grid_step):
        line(to_screen_x(x), 0, to_screen_x(x), height, colors['grid'])

    for x in range(0, ceil(from_screen_x(0)), -grid_step):
        line(to_screen_x(x), 0, to_screen_x(x), height, colors['grid'])

    for y in range(0, ceil(from_screen_y(height)), -grid_step):
        line(0, to_screen_y(y), width, to_screen_y(y), colors['grid'])

    for y in range(0, ceil(from_screen_y(0)), grid_step):
        line(0, to_screen_y(y), width, to_screen_y(y), colors['grid'])

    line(0, to_screen_y(0), width, to_screen_y(0), colors['axis'])
    line(to_screen_x(0), 0, to_screen_x(0), height, colors['axis'])

    for x in range(int(to_screen_x(left)), int(to_screen_x(right)) + 1):
        line(x, screen_func(x), x + 1, screen_func(x + 1), colors['function'])

