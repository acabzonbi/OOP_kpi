import tkinter as tk


class Dialog1:
    def __init__(self, parent, callback):
        self.callback = callback
        self.top = tk.Toplevel(parent)
        self.top.title("Робота1")
        self.top.geometry("350x320")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        groups = [
            "ІМ-51мн", "ІМ-51мп", "ІМ-51ф", "ІМ-52",
            "ІМ-52мп", "ІМ-53", "ІМ-54", "ІМ-55",
            "ІМ-о51", "ІМ-61", "ІМ-61мн", "ІМ-61мп",
            "ІМ-61ф", "ІМ-62", "ІМ-62мп", "ІМ-63",
            "ІМ-64", "ІМ-65", "ІМ-66", "ІМ-о61"
        ]

        tk.Label(self.top, text="Оберіть групу:", font=("Arial", 11)).pack(pady=(15, 5))
        self.listbox = tk.Listbox(
            self.top,
            width=30,
            height=10,
            font=("Arial", 11),
            selectmode=tk.SINGLE
        )
        self.listbox.pack(pady=5)

        for group in groups: #добавляє групи зі списку у лістбокс
            self.listbox.insert(tk.END, group)

        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=15)
        tk.Button(
            btn_frame,
            text="Так",
            width=10,
            command=self._on_ok
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            btn_frame,
            text="Відміна",
            width=10,
            command=self._on_cancel
        ).pack(side=tk.LEFT, padx=10)

        parent.wait_window(self.top)   # чекаємо закриття вікна

    def _on_ok(self):
        selection = self.listbox.curselection()
        if selection:
            selected_text = self.listbox.get(selection[0])
            self.callback(selected_text)
        self.top.destroy()

    def _on_cancel(self):
        self.top.destroy()


def show_1(parent, callback):
    Dialog1(parent, callback)
