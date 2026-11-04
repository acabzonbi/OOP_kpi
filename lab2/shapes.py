from abc import ABC, abstractmethod


class Shape(ABC): #Базовий клас
    def __init__(self):
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.color = "black"

    def set_start(self, x, y): # координати початку
        self.x1 = x
        self.y1 = y
        self.x2 = x
        self.y2 = y

    def set_end(self, x, y): #координати кінця
        self.x2 = x
        self.y2 = y

    @abstractmethod #абстрактні методі потрібні для усіх класів фігур
    def draw(self, canvas, **kwargs):
        pass

    @abstractmethod
    def draw_rubber(self, canvas, x, y):
        pass


class Point(Shape): #точка
    def draw(self, canvas, **kwargs):
        r = 5
        canvas.create_oval(self.x1 - r, self.y1 - r,
                           self.x1 + r, self.y1 + r,
                           fill="black", outline="black")

    def draw_rubber(self, canvas, x, y):
        pass


class Line(Shape): #лінія
    def draw(self, canvas, **kwargs):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill="black", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_line(self.x1, self.y1, x, y,
                                  fill="black", width=1, dash=(4, 4))


class Rect(Shape): #прямокутник
    def set_end(self, x, y):
        cx, cy = self.x1, self.y1
        dx = abs(x - cx) #відстань від центру до кута
        dy = abs(y - cy)
        self.x1 = cx - dx
        self.y1 = cy - dy
        self.x2 = cx + dx
        self.y2 = cy + dy

    def draw(self, canvas, **kwargs):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                outline="black", width=1)

    def draw_rubber(self, canvas, x, y):
        cx, cy = self.x1, self.y1
        dx = abs(x - cx)
        dy = abs(y - cy)
        return canvas.create_rectangle(cx - dx, cy - dy, cx + dx, cy + dy,
                                       outline="black", width=1, dash=(4, 4))


class Ellipse(Shape): #еліпс
    def draw(self, canvas, **kwargs):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                           outline="black", fill="yellow", width=1)

    def draw_rubber(self, canvas, x, y):
        return canvas.create_oval(self.x1, self.y1, x, y,
                                  outline="black", width=1, dash=(4, 4))
