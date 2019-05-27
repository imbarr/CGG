import tkinter as tk
from tkinter import Canvas, Tk


class App(Tk):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def line(self, p1, p2, fill):
        scale = 50
        self.canvas.create_line(960 + scale * p1.x, 540 - scale * p1.y, 960 + scale * p2.x, 540 - scale * p2.y, fill=fill)


class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return P(
            self.x - other.x,
            self.y - other.y
        )

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


def triangulate(polygon):
    segments = []
    for i in range(0, len(polygon) - 3):
        for index, _ in enumerate(polygon):
            segment = get_neighbours(polygon, index)
            if segment_inside_polygon(polygon, segment):
                segments.append(segment)
                del polygon[index]
                break
    return segments


def segment_inside_polygon(polygon, segment):
    for s in all_segments(polygon):
        if segments_intersection(segment, s) in ("exclusive", "inclusive-2"):
            return False
    middle = P((segment[0].x + segment[1].x) / 2, (segment[0].y + segment[1].y) / 2)
    ray = (middle, P(100000, middle.y))
    intersections = 0
    prev_sign = 0
    for s in all_segments(polygon):
        intersection = segments_intersection(ray, s)
        if intersection == "exclusive":
            intersections += 1
        elif intersection == "inclusive-2":
            if prev_sign == 1 and s[1].y < middle.y:
                intersections += 1
                prev_sign = 0
            elif prev_sign == -1 and s[1].y > middle.y:
                intersections += 1
                prev_sign = 0
            elif prev_sign == 0:
                prev_sign = -1 if s[1].y < middle.y else 1
            else:
                prev_sign = 0
    return intersections % 2 == 1


def all_segments(polygon):
    for i in range(-1, len(polygon) - 1):
        yield (polygon[i], polygon[i + 1])


def segments_intersection(s1, s2):
    x1, y1 = s1[0].x, s1[0].y
    x2, y2 = s1[1].x, s1[1].y
    x3, y3 = s2[0].x, s2[0].y
    x4, y4 = s2[1].x, s2[1].y
    denom = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
    if denom == 0:
        return "none"
    x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        if min(x3, x4) < x < max(x3, x4) or min(y3, y4) < y < max(y3, y4):
            return "exclusive"
        if (min(x1, x2) == x or x == max(x1, x2)) and (min(y1, y2) == y or y == max(y1, y2)):
            return "inclusive-1"
        if (min(x3, x4) == x or x == max(x3, x4)) and (min(y3, y4) == y or y == max(y3, y4)):
            return "inclusive-2"
    return "none"


def get_neighbours(polygon, index):
    if index == len(polygon) - 1:
        return polygon[-2], polygon[0]
    else:
        return polygon[index - 1], polygon[index + 1]


if __name__ == '__main__':
    app = App()
    # polygon = [P(0, 0), P(0, 2), P(2, 2), P(2, 0)]
    # polygon = [P(0, 0), P(0, 2), P(1, 4), P(2, 2), P(5, 3), P(8, 1), P(9, -1), P(8, -3), P(7, -4), P(6, -3), P(5, -4), P(4, -2), P(2, -3)]
    # polygon = [P(0, 0), P(0, 1), P(1, 3), P(2, 1), P(3, 3), P(4, 1), P(5, 3), P(6, 1), P(6, 0)]
    polygon = [P(0, 0), P(0, 5), P(1, 5), P(2, 4), P(2, 2), P(1, 1), P(4, 1), P(3, 2), P(3, 4), P(4, 5), P(5, 5),
               P(6, 4), P(6, 2), P(5, 1), P(8, 1), P(7, 2), P(7, 4), P(8, 5), P(9, 5), P(8, 4), P(8, 2), P(9, 1), P(9, 0)]
    for i, _ in enumerate(polygon):
        app.line(polygon[i - 1], polygon[i], 'red')
    result = triangulate(polygon)
    print(result)
    for segment in result:
        app.line(segment[0], segment[1], 'blue')
    app.mainloop()

