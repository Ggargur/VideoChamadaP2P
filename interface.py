import tkinter
from tkinter import ttk
from client import register_name, request_name


class Interface(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.create_interface()

    def create_interface(self):
        self.columnconfigure(0)

        self.title("LOGIN")

        ttk.Label(self, text="Nome de usuário: ").
        ttk.Entry(self).

        ttk.Button(self, text="Cadastrar", command=register_name).

        ttk.Button(self, text="Requisitar", command=request_name).

    def on_closing(self):
        self.destroy()




if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()