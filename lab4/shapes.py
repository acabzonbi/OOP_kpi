from abc import ABC, abstractmethod
import tkinter as tk


class Shape(ABC):
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

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def draw_rubber(self, canvas, x, y):
        pass


class Point(Shape):
    def draw(self, canvas):
        r = 3
        canvas.create_oval(self.x1 - r, self.y1 - r,
                           self.x1 + r, self.y1 + r,
                           fill="black", outline="black")

    def draw_rubber(self, canvas, x, y):
        return None


class Line(Shape):
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill="black", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_line(self.x1, self.y1, x, y,
                                  fill="black", width=1, dash=(4, 3))


class Rect(Shape):
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                outline="black", fill="white", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_rectangle(self.x1, self.y1, x, y,
                                       outline="black", width=1, dash=(4, 3))


class Ellipse(Shape):
    def set_end(self, x, y):
        cx, cy = self.x1, self.y1
        dx = abs(x - cx)
        dy = abs(y - cy)
        self.x1 = cx - dx
        self.y1 = cy - dy
        self.x2 = cx + dx
        self.y2 = cy + dy

    def draw(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           outline="black", width=1)

    def draw_rubber(self, canvas, x, y):
        cx, cy = self.x1, self.y1
        dx = abs(x - cx)
        dy = abs(y - cy)
        return canvas.create_oval(cx - dx, cy - dy, cx + dx, cy + dy,
                                  outline="black", width=1, dash=(4, 3))



class LineWithCircles(Line, Ellipse):
    RADIUS = 6

    def set_end(self, x, y):
        # координати кінців лінії (від Line)
        self.x2 = x
        self.y2 = y

    def _draw_circles(self, canvas):
        r = self.RADIUS
        # кружечок на початку
        canvas.create_oval(self.x1 - r, self.y1 - r,
                           self.x1 + r, self.y1 + r,
                           outline="black", width=1)
        # кружечок на кінці
        canvas.create_oval(self.x2 - r, self.y2 - r,
                           self.x2 + r, self.y2 + r,
                           outline="black", width=1)

    def draw(self, canvas):
        Line.draw(self, canvas)          #лінія
        self._draw_circles(canvas)       #кружечки (через логіку Ellipse)

    def draw_rubber(self, canvas, x, y):
        # пунктирна лінія + пунктирні кружечки
        ids = []
        ids.append(Line.draw_rubber(self, canvas, x, y))
        r = self.RADIUS
        ids.append(canvas.create_oval(self.x1 - r, self.y1 - r,
                                      self.x1 + r, self.y1 + r,
                                      outline="black", width=1, dash=(4, 3)))
        ids.append(canvas.create_oval(x - r, y - r, x + r, y + r,
                                      outline="black", width=1, dash=(4, 3)))
        return ids   # список id для подальшого видалення


class Cube(Line, Rect):
    DEPTH = 40   # фіксований зсув по глибині

    def set_end(self, x, y):
        self.x2 = x
        self.y2 = y

    def _points(self):
        """Повертає 8 вершин куба (передня + задня грань)."""
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        d = self.DEPTH
     
        p0 = (x1, y1)    #передня грань
        p1 = (x2, y1)
        p2 = (x2, y2)
        p3 = (x1, y2)

        p4 = (x1 + d, y1 - d)      #задня грань (зсув вгору-вправо)
        p5 = (x2 + d, y1 - d)
        p6 = (x2 + d, y2 - d)
        p7 = (x1 + d, y2 - d)
        return p0, p1, p2, p3, p4, p5, p6, p7

    def draw(self, canvas):
        p0, p1, p2, p3, p4, p5, p6, p7 = self._points()

        # передня грань (Rect)
        canvas.create_rectangle(p0[0], p0[1], p2[0], p2[1],
                                outline="black", width=1)

        # задня грань
        canvas.create_rectangle(p4[0], p4[1], p6[0], p6[1],
                                outline="black", width=1)

        # бічні ребра (Line)
        for a, b in ((p0, p4), (p1, p5), (p2, p6), (p3, p7)):
            canvas.create_line(a[0], a[1], b[0], b[1],
                               fill="black", width=1)

    def draw_rubber(self, canvas, x, y):
        # тимчасово підставляємо кінець
        old_x2, old_y2 = self.x2, self.y2
        self.x2, self.y2 = x, y
        p0, p1, p2, p3, p4, p5, p6, p7 = self._points()
        self.x2, self.y2 = old_x2, old_y2

        ids = []
        # передня грань пунктиром
        ids.append(canvas.create_rectangle(p0[0], p0[1], p2[0], p2[1],
                                           outline="black", width=1, dash=(4, 3)))
        # задня
        ids.append(canvas.create_rectangle(p4[0], p4[1], p6[0], p6[1],
                                           outline="black", width=1, dash=(4, 3)))
        # ребра
        for a, b in ((p0, p4), (p1, p5), (p2, p6), (p3, p7)):
            ids.append(canvas.create_line(a[0], a[1], b[0], b[1],
                                          fill="black", width=1, dash=(4, 3)))
        return ids