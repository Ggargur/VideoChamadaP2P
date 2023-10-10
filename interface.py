import tkinter
from tkinter import ttk
from client import request_name, unregister_name, register_name


class Interface(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.create_interface()

    def create_interface(self):
        self.columnconfigure(0)

        self.title("LOGIN")

        ttk.Label(self, text="Nome de usuário: ").pack(side='left')
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(side='left')

        ttk.Button(self, text="Cadastrar", command=self.register_name).pack(pady=5)
        ttk.Button(self, text="Descadastrar", command=self.unregister_name).pack(pady=5)
        ttk.Button(self, text="Requisitar", command=self.request_name).pack(pady=5)

    def register_name(self):
        register_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    def unregister_name(self):
        unregister_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    def request_name(self):
        register_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()
