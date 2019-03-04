from app import App
import math


if __name__ == '__main__':
    def func(x):
        return x*x

    app = App(func, -1, 1)
    app.mainloop()
