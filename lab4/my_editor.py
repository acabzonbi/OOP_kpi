import tkinter as tk
from tkinter import messagebox
from shapes import (Point, Line, Rect, Ellipse,
                    LineWithCircles, Cube)


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffff",
                         relief="solid", borderwidth=1, font=("Segoe UI", 9))
        label.pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


class MyEditor:
    N = 120  # розмір статичного масиву

    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600")

        # статичний масив вказівників (імітація)
        self.pcshape = [None] * self.N
        self.count = 0

        self.current_type = "Прямокутник"
        self.drawing = False
        self.current_shape = None
        self.rubber_ids = []          # може бути список (для складних фігур)

        self.type_var = tk.StringVar(value=self.current_type)

        #легко додавати нові типи
        self._shape_factory = {
            "Крапка": Point,
            "Лінія": Line,
            "Прямокутник": Rect,
            "Еліпс": Ellipse,
            "Лінія з кружечками": LineWithCircles,
            "Каркас куба": Cube,
        }

        self._create_menu()
        self._create_toolbar()
        self._create_canvas()
        self._update_menu_check()
        self._update_title()

    def _create_menu(self):
        self.menubar = tk.Menu(self.root)

        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Очистити", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        self.menubar.add_cascade(label="Файл", menu=file_menu)

        self.objects_menu = tk.Menu(self.menubar, tearoff=0)
        for name in self._shape_factory:
            self.objects_menu.add_radiobutton(
                label=name,
                variable=self.type_var,
                value=name,
                command=lambda n=name: self.set_type(n)
            )
        self.menubar.add_cascade(label="Об'єкти", menu=self.objects_menu)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        self.menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=self.menubar)

    def _update_menu_check(self):
        self.type_var.set(self.current_type)

    def _update_title(self):
        self.root.title(f"Lab4: Об'єктів: {self.count}/{self.N}")

    def _create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("●", "Крапка", "Крапка"),
            ("／", "Лінія", "Лінія"),
            ("▭", "Прямокутник", "Прямокутник"),
            ("○", "Еліпс", "Еліпс"),
            ("⚬─⚬", "Лінія з кружечками", "Лінія з кружечками"),
            ("◻︎", "Каркас куба", "Каркас куба"),
        ]

        for icon, tip, shape_name in buttons:
            btn = tk.Button(
                toolbar,
                text=icon,
                font=("Segoe UI", 12),
                width=4,
                relief=tk.RAISED,
                command=lambda n=shape_name: self.set_type(n)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            ToolTip(btn, tip)

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
        self._update_menu_check()

    def on_press(self, event):
        if self.count >= self.N:
            messagebox.showwarning("Увага", "Масив заповнений!")
            return
        self.drawing = True
        self.current_shape = self._create_shape()
        self.current_shape.set_start(event.x, event.y)

    def on_drag(self, event):
        if not self.drawing or self.current_shape is None:
            return
        self._clear_rubber()
        result = self.current_shape.draw_rubber(self.canvas, event.x, event.y)
        if result is None:
            self.rubber_ids = []
        elif isinstance(result, (list, tuple)):
            self.rubber_ids = list(result)
        else:
            self.rubber_ids = [result]

    def on_release(self, event):
        if not self.drawing or self.current_shape is None:
            return
        self._clear_rubber()

        self.current_shape.set_end(event.x, event.y)
        self.current_shape.draw(self.canvas)

        self.pcshape[self.count] = self.current_shape
        self.count += 1
        self.drawing = False
        self.current_shape = None
        self._update_title()

    def _clear_rubber(self):
        for rid in self.rubber_ids:
            if rid is not None:
                self.canvas.delete(rid)
        self.rubber_ids = []

    def _create_shape(self):
        cls = self._shape_factory.get(self.current_type, Point)
        return cls()

    def clear_all(self):
        self.canvas.delete("all")
        self.pcshape = [None] * self.N
        self.count = 0
        self._update_title()

    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота 4\n"
            "Варіант: 19\n"
            "Масив: статичний, N = 120\n"
            "Гумовий слід: пунктирна лінія\n"
            "Нові фігури (множинне успадкування):\n"
            "  • Лінія з кружечками (Line + Ellipse)\n"
            "  • Каркас куба (Line + Rect)\n"
            "Прямокутник: по двох кутах, біле заповнення\n"
            "Еліпс: від центру, без заповнення"
        )


#глобальний статичний об'єкт
editor = None


def get_editor(root=None):
    global editor  # повертає глобальний статичний екземпляр MyEditor
    if editor is None:
        if root is None:
            raise RuntimeError("Потрібно передати root")
        editor = MyEditor(root)
    return editor