
import tkinter as tk
from tkinter import messagebox
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



class GraphicEditor: #головне вікно програми
    def __init__(self, root):
        self.root = root
        self.root.title("Lab2")
        self.root.geometry("900x650")

        #статичний масив, 119 елементів макс
        self.N = 119
        self.pcshape = [None] * self.N   # імітація статичного масиву
        self.count = 0

        self.current_type = "Прямокутник"   # фігура за замовчуванням
        self.drawing = False
        self.current_shape = None
        self.rubber_id = None

        self._create_menu()
        self._create_canvas()
        self._update_title()

    def _create_menu(self):
        menubar = tk.Menu(self.root)

        # меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Очистити", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # меню Об'єкти
        objects_menu = tk.Menu(menubar, tearoff=0)
        objects_menu.add_command(label="Крапка",
                                 command=lambda: self.set_type("Крапка"))
        objects_menu.add_command(label="Лінія",
                                 command=lambda: self.set_type("Лінія"))
        objects_menu.add_command(label="Прямокутник",
                                 command=lambda: self.set_type("Прямокутник"))
        objects_menu.add_command(label="Еліпс",
                                 command=lambda: self.set_type("Еліпс"))
        menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        # меню Довідка
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menubar)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_press) #при натисканні ЛКМ
        self.canvas.bind("<B1-Motion>", self.on_drag) #при перенесенні курсора з натиснутою ЛКМ
        self.canvas.bind("<ButtonRelease-1>", self.on_release) #при відпусканні ЛКМ

    def set_type(self, shape_type):
        self.current_type = shape_type
        self._update_title()

    def _update_title(self): #оновлення заголовку
        self.root.title(f"Об'єкт: {self.current_type} Об'єктів: {self.count}/{self.N}")

    def on_press(self, event):
        if self.count >= self.N: #перевірка чи заповнений масив
            messagebox.showwarning("Масив заповнений!")
            return

        self.drawing = True
        self.current_shape = self._create_shape() #задає щоб current_shape повертало вибраний клас фігури
        self.current_shape.set_start(event.x, event.y)

    def on_drag(self, event):
        if not self.drawing or self.current_shape is None: #перевірка чи почалося малювання
            return

        if self.rubber_id is not None: #видаляє попередній слід та малює новий
            self.canvas.delete(self.rubber_id)
        self.rubber_id = self.current_shape.draw_rubber(self.canvas, event.x, event.y)

    def on_release(self, event):
        if not self.drawing or self.current_shape is None: #перевіряє, чи треба щось робити при відпусканні
            return

        # видаляє гумовий слід
        if self.rubber_id is not None:
            self.canvas.delete(self.rubber_id)
            self.rubber_id = None

        self.current_shape.set_end(event.x, event.y)
        self.current_shape.draw(self.canvas) #викликає функцію draw() з класу обраної фігури

        # записує об'єкт у масив
        self.pcshape[self.count] = self.current_shape
        self.count += 1

        self.drawing = False
        self.current_shape = None
        self._update_title()

    def _create_shape(self):
        if self.current_type == "Крапка":
            return Point()
        elif self.current_type == "Лінія":
            return Line()
        elif self.current_type == "Прямокутник":
            return Rect()
        elif self.current_type == "Еліпс":
            return Ellipse()
        return Point()

    def clear_all(self):
        self.canvas.delete("all")
        self.pcshape = [None] * self.N
        self.count = 0
        self._update_title()

    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Варіант: 19\n"
            "Масив: статичний, N = 119\n"
            "Гумовий слід: пунктирна чорна лінія\n"
            "Прямокутник: від центру, без заповнення\n"
            "Еліпс: по двох протилежних кутах, жовте заповнення\n"
            "Позначка поточного типу: у заголовку вікна"
        )



if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditor(root)
    root.mainloop()