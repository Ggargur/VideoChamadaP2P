import tkinter
from tkinter import ttk
from client import register_name, request_name


class Interface(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.create_interface()

    def create_interface(self):
        
        self.title("LOGIN")

        ttk.Label(self, text="Nome de usuário: ").pack(side='left')
        ttk.Entry(self).pack(side='left')

        ttk.Button(self, text="Cadastrar", command=register_name).pack(pady=5)

        ttk.Button(self, text="Requisitar", command=request_name).pack(pady=5)

    def on_closing(self):
        self.destroy()




if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()
