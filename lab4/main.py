import tkinter as tk
from my_editor import get_editor


if __name__ == "__main__":
    root = tk.Tk()
    app = get_editor(root)
    root.mainloop()