import tkinter as tk


class Dialog2:

    def __init__(self, parent, callback):
        self.callback = callback

        self.top = tk.Toplevel(parent)
        self.top.title("Робота2")
        self.top.geometry("400x180")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        tk.Label(
            self.top,
            text="Введіть текст:",
            font=("Arial", 11)
        ).pack(pady=(20, 8))

        self.entry = tk.Entry(
            self.top,
            width=40,
            font=("Arial", 12)
        )
        self.entry.pack(pady=5)
        self.entry.focus_set()

        # Кнопки
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=20)

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

        parent.wait_window(self.top)

    def _on_ok(self): #при натисканні кнопки Так
        text = self.entry.get().strip()
        if text:                       
            self.callback(text)
        self.top.destroy()

    def _on_cancel(self): #при натискані Відміна
        self.top.destroy()


def show_2(parent, callback):
    Dialog2(parent, callback)
