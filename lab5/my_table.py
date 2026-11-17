import tkinter as tk
from tkinter import ttk


class MyTable:
    def __init__(self, parent, editor):
        self.parent = parent
        self.editor = editor
        self.window = None
        self.tree = None
        self._is_open = False

    @property
    def is_open(self):
        return self._is_open and self.window is not None and self.window.winfo_exists()

    def show(self):
        if self.is_open:
            self.window.deiconify()
            self.window.lift()
            self.refresh()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Таблиця об'єктів")
        self.window.geometry("520x320")
        self.window.minsize(400, 200)

        self.window.transient(self.parent)    # Немодальне, можна працювати з головним вікном
        self.window.protocol("WM_DELETE_WINDOW", self.hide)    # При закритті хрестиком вікно просто ховаєтся

        # Таблиця
        columns = ("name", "x1", "y1", "x2", "y2")
        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("name", text="Назва")
        self.tree.heading("x1", text="x1")
        self.tree.heading("y1", text="y1")
        self.tree.heading("x2", text="x2")
        self.tree.heading("y2", text="y2")

        self.tree.column("name", width=160, anchor="w")
        self.tree.column("x1", width=70, anchor="center")
        self.tree.column("y1", width=70, anchor="center")
        self.tree.column("x2", width=70, anchor="center")
        self.tree.column("y2", width=70, anchor="center")

        # Скролбар
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 8), pady=8)

        self._is_open = True
        self.refresh()
        self.window.bind("<Destroy>", self._on_destroy)

    def hide(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()
        self.window = None
        self.tree = None
        self._is_open = False

    def toggle(self): # перемикач вікна таблиці
        if self.is_open:
            self.hide()
        else:
            self.show()

    def refresh(self):  # оновити вміст таблиці з даних редактора
        if not self.is_open or self.tree is None:
            return

        # Очистити
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заповнити
        for i in range(self.editor.count):
            shape = self.editor.pcshape[i]
            if shape is None:
                continue
            name = shape.get_type_name()
            x1, y1, x2, y2 = shape.get_coords()
            self.tree.insert(
                "",
                "end",
                values=(name, x1, y1, x2, y2),
            )

    def _on_destroy(self, event):  # синхронізує стан вікна, якщо воно зникло не через метод hide()
        if event.widget is self.window:
            self._is_open = False
            self.window = None
            self.tree = None
