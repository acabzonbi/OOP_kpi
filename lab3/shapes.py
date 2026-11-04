from abc import ABC, abstractmethod

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
        canvas.create_oval(self.x1-r, self.y1-r, self.x1+r, self.y1+r,
                           fill="black", outline="black")

    def draw_rubber(self, canvas, x, y):
        pass


class Line(Shape):
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill="black", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_line(self.x1, self.y1, x, y,
                                  fill="black", width=1)


class Rect(Shape):
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                outline="black", fill="white", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_rectangle(self.x1, self.y1, x, y,
                                       outline="black", width=1)


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
        return canvas.create_oval(cx-dx, cy-dy, cx+dx, cy+dy,
                                  outline="black", width=1)
