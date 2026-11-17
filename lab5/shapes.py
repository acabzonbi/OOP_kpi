from abc import ABC, abstractmethod
from contextlib import contextmanager


class Shape(ABC):
    TYPE_NAME = "Shape"

    def __init__(self):
        self.x1 = self.y1 = self.x2 = self.y2 = 0

    def set_start(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = x
        self.y2 = y

    def set_end(self, x, y):
        self.x2 = x
        self.y2 = y

    def get_type_name(self):
        return self.TYPE_NAME

    def get_coords(self):
        return self.x1, self.y1, self.x2, self.y2

    @contextmanager
    def _coords(self, x1, y1, x2, y2):
        # Тимчасово підставляє координати, щоб батьківський клас намалював свою частину фігури
        old = (self.x1, self.y1, self.x2, self.y2)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        try:
            yield
        finally:
            self.x1, self.y1, self.x2, self.y2 = old

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def draw_rubber(self, canvas, x, y):
        pass


class Point(Shape):
    TYPE_NAME = "Точка"

    def draw(self, canvas):
        r = 3
        canvas.create_oval(self.x1 - r, self.y1 - r,
                           self.x1 + r, self.y1 + r,
                           fill="black", outline="black")

    def draw_rubber(self, canvas, x, y):
        return None


class Line(Shape):
    TYPE_NAME = "Лінія"

    def draw(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                                  fill="black", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_line(self.x1, self.y1, x, y,
                                  fill="black", width=1, dash=(4, 3))


class Rect(Shape):
    TYPE_NAME = "Прямокутник"
    FILL = "white"

    def draw(self, canvas):
        return canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                       outline="black", fill=self.FILL, width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_rectangle(self.x1, self.y1, x, y,
                                       outline="black", width=1, dash=(4, 3))


class Ellipse(Shape):
    TYPE_NAME = "Еліпс"

    def set_end(self, x, y):
        cx, cy = self.x1, self.y1
        dx = abs(x - cx)
        dy = abs(y - cy)
        self.x1 = cx - dx
        self.y1 = cy - dy
        self.x2 = cx + dx
        self.y2 = cy + dy

    def draw(self, canvas):
        return canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                                  outline="black", width=1)

    def draw_rubber(self, canvas, x, y):
        # еліпс від центру
        cx, cy = self.x1, self.y1
        dx = abs(x - cx)
        dy = abs(y - cy)
        return canvas.create_oval(cx - dx, cy - dy, cx + dx, cy + dy,
                                  outline="black", width=1, dash=(4, 3))


class LineWithCircles(Line, Ellipse):
    TYPE_NAME = "Лінія з кружечками"
    RADIUS = 6

    def set_end(self, x, y):
        # кінці лінії
        self.x2 = x
        self.y2 = y

    def draw(self, canvas):
        r = self.RADIUS
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        Line.draw(self, canvas)

        for cx, cy in ((x1, y1), (x2, y2)):           # кружечки
            with self._coords(cx - r, cy - r, cx + r, cy + r):
                Ellipse.draw(self, canvas)

    def draw_rubber(self, canvas, x, y):
        r = self.RADIUS
        ids = [Line.draw_rubber(self, canvas, x, y)]  # пунктирна лінія

        # малює від центру до точки
        for cx, cy in ((self.x1, self.y1), (x, y)):
            with self._coords(cx, cy, cx, cy):
                ids.append(Ellipse.draw_rubber(self, canvas, cx + r, cy + r))
        return ids


class Cube(Line, Rect):
    TYPE_NAME = "Куб"
    DEPTH = 40   # зсув по глибині
    FILL = ""    # грані без заповнення

    def set_end(self, x, y):
        self.x2 = x
        self.y2 = y

    def _points(self, x2=None, y2=None):
        # Повертає 8 вершин куба
        x1, y1 = self.x1, self.y1
        x2 = self.x2 if x2 is None else x2
        y2 = self.y2 if y2 is None else y2
        d = self.DEPTH

        p0 = (x1, y1)              # передня грань
        p1 = (x2, y1)
        p2 = (x2, y2)
        p3 = (x1, y2)

        p4 = (x1 + d, y1 - d)      # задня грань (зсув вгору-вправо)
        p5 = (x2 + d, y1 - d)
        p6 = (x2 + d, y2 - d)
        p7 = (x1 + d, y2 - d)
        return p0, p1, p2, p3, p4, p5, p6, p7

    def draw(self, canvas):
        p0, p1, p2, p3, p4, p5, p6, p7 = self._points()

        # передня та задня грані
        for a, b in ((p0, p2), (p4, p6)):
            with self._coords(a[0], a[1], b[0], b[1]):
                Rect.draw(self, canvas)

        # бічні ребра
        for a, b in ((p0, p4), (p1, p5), (p2, p6), (p3, p7)):
            with self._coords(a[0], a[1], b[0], b[1]):
                Line.draw(self, canvas)

    def draw_rubber(self, canvas, x, y):
        p0, p1, p2, p3, p4, p5, p6, p7 = self._points(x, y)
        ids = []

        # грані пунктиром
        for a, b in ((p0, p2), (p4, p6)):
            with self._coords(a[0], a[1], a[0], a[1]):
                ids.append(Rect.draw_rubber(self, canvas, b[0], b[1]))

        # ребра пунктиром
        for a, b in ((p0, p4), (p1, p5), (p2, p6), (p3, p7)):
            with self._coords(a[0], a[1], a[0], a[1]):
                ids.append(Line.draw_rubber(self, canvas, b[0], b[1]))
        return ids
