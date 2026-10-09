import tkinter as tk
from tkinter import Menu
import module1
import module2


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("lab1")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.result_label = tk.Label(  #куди будет виводитися результат
            self.root,
            font=("Arial", 14),
            wraplength=450,
            justify="center"
        )
        self.result_label.pack(expand=True)

        # Меню
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        menubar.add_command(label="Робота1", command=self.robota1)
        menubar.add_command(label="Робота2", command=self.robota2)

    def update_result(self, text: str):   #оновлення результату у головному вікні
        self.result_label.config(text=text)

    def robota1(self):
        module1.show_1(self.root, self.update_result)

    def robota2(self):
        module2.show_2(self.root, self.update_result)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":    #запуск програми
    app = MainApp()
    app.run()
