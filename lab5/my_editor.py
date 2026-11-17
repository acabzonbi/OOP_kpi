import os
import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from shapes import (Point, Line, Rect, Ellipse,
                    LineWithCircles, Cube)
from my_table import MyTable


ICONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

ICON_FILES = {
    "POINT": "point.png",
    "LINE": "line.png",
    "RECT": "rectangle.png",
    "ELLIPSE": "circle.png",
    "LINE-W-CIRCLES": "line_with_circles.png",
    "CUBE": "cube.png",
    "CLEAR": "trash.png",
    "TABLE": "table.png"
}


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
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # статичний масив вказівників (імітація)
        self.pcshape = [None] * self.N
        self.count = 0

        self.current_type = "RECT"
        self.drawing = False
        self.current_shape = None
        self.rubber_ids = []          # для складних фігур
        self.type_var = tk.StringVar(value=self.current_type)

        self._shape_factory = {
            "POINT": Point,
            "LINE": Line,
            "RECT": Rect,
            "ELLIPSE": Ellipse,
            "LINE-W-CIRCLES": LineWithCircles,
            "CUBE": Cube,
        }

        # Таблиця
        self.table = MyTable(self.root, self)

        self._create_menu()
        self._create_toolbar()
        self._create_canvas()
        self._update_menu_check()
        self._update_title()

    def _create_menu(self):
        self.menubar = tk.Menu(self.root)

        # Файл
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Зберегти як CSV...", command=self.save_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.on_exit)
        self.menubar.add_cascade(label="Файл", menu=file_menu)

        # Об'єкти (типи фігур)
        objects_menu = tk.Menu(self.menubar, tearoff=0)
        for name in self._shape_factory:
            objects_menu.add_radiobutton(
                label=name,
                variable=self.type_var,
                value=name,
                command=lambda n=name: self.set_type(n),
            )
        objects_menu.add_separator()
        objects_menu.add_command(label="Очистити все", command=self.clear_all)
        self.menubar.add_cascade(label="Об'єкти", menu=objects_menu)

        # Вікно (таблиця)
        window_menu = tk.Menu(self.menubar, tearoff=0)
        window_menu.add_command(label="Таблиця об'єктів", command=self.toggle_table)
        self.menubar.add_cascade(label="Вікно", menu=window_menu)

        # Довідка
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        self.menubar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=self.menubar)

    def _update_menu_check(self):
        self.type_var.set(self.current_type)

    def _update_title(self):
        self.root.title(f"Lab5: Об'єктів: {self.count}/{self.N}")

    def _create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.icons = {}

        for shape_name in self._shape_factory:
            file_name = ICON_FILES.get(shape_name)
            btn_opts = {}
            if file_name:
                try:
                    self.icons[shape_name] = tk.PhotoImage(
                        file=os.path.join(ICONS_DIR, file_name))
                    btn_opts["image"] = self.icons[shape_name]
                except tk.TclError:
                    pass
            if "image" not in btn_opts:
                btn_opts["text"] = shape_name

            btn = tk.Radiobutton(
                toolbar,
                indicatoron=False,
                variable=self.type_var,
                value=shape_name,
                relief=tk.RAISED,
                padx=4, pady=4,
                command=lambda n=shape_name: self.set_type(n),
                **btn_opts
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            ToolTip(btn, shape_name)

        tk.Frame(toolbar, width=8).pack(side=tk.LEFT)

        clear_opts = {"text": "🗑", "font": ("Segoe UI", 14), "width": 3}
        try:
            self.icons["CLEAR"] = tk.PhotoImage(
                file=os.path.join(ICONS_DIR, ICON_FILES["CLEAR"]))
            clear_opts = {"image": self.icons["CLEAR"]}
        except tk.TclError:
            pass
        clear_btn = tk.Button(toolbar, relief=tk.RAISED, padx=4, pady=4,
                              command=self.clear_all, **clear_opts)
        clear_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        ToolTip(clear_btn, "CLEAR")

        table_opts = {"text": "т", "font": ("Segoe UI", 14), "width": 3}
        try:
            self.icons["TABLE"] = tk.PhotoImage(
                file=os.path.join(ICONS_DIR, ICON_FILES["TABLE"]))
            table_opts = {"image": self.icons["TABLE"]}
        except tk.TclError:
            pass
        table_btn = tk.Button(toolbar, relief=tk.RAISED, padx=4, pady=4,
                              command=self.toggle_table, **table_opts)
        table_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        ToolTip(table_btn, "TABLE")


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
        self.table.refresh()      # Оновити таблицю, якщо вона відкрита

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
        self.table.refresh()

    def toggle_table(self):   # відкрити або закрити вінко таблиці
        self.table.toggle()

    def save_to_csv(self):   # зберегти таблицю у csv
        if self.count == 0:
            messagebox.showinfo("Збереження", "Немає об'єктів для збереження.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Зберегти об'єкти як CSV",
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["type", "x1", "y1", "x2", "y2"])
                for i in range(self.count):
                    shape = self.pcshape[i]
                    if shape is None:
                        continue
                    name = shape.get_type_name()
                    x1, y1, x2, y2 = shape.get_coords()
                    writer.writerow([name, x1, y1, x2, y2])
            messagebox.showinfo("Збереження", f"Збережено {self.count} об'єктів у\n{path}")
        except OSError as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def on_exit(self):  # при закритті головного вікна програми
        self.table.hide()
        self.root.destroy()

    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Лабораторна робота 5\n"
            "Варіант: 19\n"
            "Глобальний статичний об'єкт MyEditor (Singleton)\n"
            "Збереження об'єктів у CSV\n"
            "Масив статичний, N = 120\n"
        )


# глобальний статичний об'єкт (Singleton)
editor = None


def get_editor(root=None):
    global editor  # повертає глобальний статичний екземпляр MyEditor
    if editor is None:
        if root is None:
            raise RuntimeError("Потрібно передати root")
        editor = MyEditor(root)
    return editor
