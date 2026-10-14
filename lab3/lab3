import tkinter as tk
from tkinter import messagebox
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



class ToolTip: #спливаюча підказка
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None           #вікно підказки, спочатку порожнє
        widget.bind("<Enter>", self.show) #курсор навели на віджет
        widget.bind("<Leave>", self.hide) #курсор відвели від віджета

    def show(self, event=None):
        if self.tip:   #переврка, якщо підказка вже показана то нічого не робити
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5   #координати розмущення підказки відносно кнопки
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  #прибирає рамку і заголовок вікна
        tw.wm_geometry(f"+{x}+{y}")  #розміщує підказку по вказаних координатах
        label = tk.Label(tw, text=self.text, background="#ffffff",
                         relief="solid", borderwidth=1, font=("Segoe UI", 9))
        label.pack()

    def hide(self, event=None):  #закриває вікно з підказкою
        if self.tip:
            self.tip.destroy()
            self.tip = None


class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600")

        #імітація статичного масиву
        self.N = 120
        self.pcshape = [None] * self.N
        self.count = 0

        self.current_type = "Прямокутник"
        self.drawing = False
        self.current_shape = None
        self.rubber_id = None
        self.type_var = tk.StringVar(value=self.current_type) #пов'язана з radiobutton у меню, вона визначає який пункт позначено

        self._create_menu()
        self._create_toolbar()
        self._create_canvas()
        self._update_menu_check()
        self._update_title()

    def _create_menu(self):
        self.menubar = tk.Menu(self.root)

        # Файл
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Очистити", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        self.menubar.add_cascade(label="Файл", menu=file_menu)

        #Об'єкти
        self.objects_menu = tk.Menu(self.menubar, tearoff=0)
        for name in ("Крапка", "Лінія", "Прямокутник", "Еліпс"):
            self.objects_menu.add_radiobutton(
                label=name,
                variable=self.type_var, #тут використовуєтся StringVar()
                value=name,
                command=lambda n=name: self.set_type(n) #виконуєтся при перемиканні обраної фігури
            )
        self.menubar.add_cascade(label="Об'єкти", menu=self.objects_menu)

        # Довідка
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        self.menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=self.menubar)

    def _update_menu_check(self):
        self.type_var.set(self.current_type) # аналог OnInitMenuPopup у пайтоні

    def _update_title(self): #оновлення заголовку
        self.root.title(f"Lab3: Об'єктів: {self.count}/{self.N}")

    def _create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        buttons = [
            ("●", "Крапка", "Крапка"),
            ("／", "Лінія", "Лінія"),
            ("▭", "Прямокутник", "Прямокутник"),
            ("○", "Еліпс", "Еліпс"),
        ]

        for icon, tip, shape_name in buttons: # розміщує кнопки
            btn = tk.Button(
                toolbar,
                text=icon,
                font=("Segoe UI", 14),
                width=3,
                relief=tk.RAISED,
                command=lambda n=shape_name: self.set_type(n)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            ToolTip(btn, tip)          # викликаєтся клас підказки

        # роздільник та кнопка очистки
        tk.Frame(toolbar, width=8).pack(side=tk.LEFT)
        clear_btn = tk.Button(toolbar, text="🗑", font=("Segoe UI", 14),
                              width=3, relief=tk.RAISED, command=self.clear_all)
        clear_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        ToolTip(clear_btn, "Очистка")


    def _create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)


    def set_type(self, shape_type):
        self.current_type = shape_type
        self._update_menu_check()          # оновлюємо галочку в меню

    def on_press(self, event):
        if self.count >= self.N: #перевірка чи заповнений масив
            messagebox.showwarning("Увага", "Масив заповнений!")
            return
        self.drawing = True
        self.current_shape = self._create_shape()
        self.current_shape.set_start(event.x, event.y)

    def on_drag(self, event):
        if not self.drawing or self.current_shape is None:
            return
        if self.rubber_id is not None:
            self.canvas.delete(self.rubber_id)
        self.rubber_id = self.current_shape.draw_rubber(self.canvas, event.x, event.y)

    def on_release(self, event):
        if not self.drawing or self.current_shape is None:
            return
        if self.rubber_id is not None:
            self.canvas.delete(self.rubber_id)
            self.rubber_id = None

        self.current_shape.set_end(event.x, event.y)
        self.current_shape.draw(self.canvas)

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
            "Варіант: 20\n"
            "Масив: статичний, N = 120\n"
            "Гумовий слід: суцільна чорна лінія\n"
            "Прямокутник: по двох кутах, біле заповнення\n"
            "Еліпс: від центру, без заповнення\n"
            "Позначка типу: у меню Об'єкти"
        )



if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicEditor(root)
    root.mainloop()