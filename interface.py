import tkinter
from tkinter import ttk
from client import request_name, unregister_name, register_name


class Interface(tkinter.Tk):
    # Cria a interface.
    def __init__(self):
        super().__init__()
        self.create_interface()

    # Coloca os elementos visuais na interface.
    def create_interface(self):
        self.title("LOGIN")

        ttk.Label(self, text="Nome de usuário: ").pack(side="left")
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(side="left")

        ttk.Button(self, text="Cadastrar", command=self.register_name).pack(pady=5)
        ttk.Button(self, text="Descadastrar", command=self.unregister_name).pack(pady=5)
        ttk.Button(self, text="Requisitar", command=self.request_name).pack(pady=5)

    # Chama a função de registrar nome do cliente.
    def register_name(self):
        register_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    # Chama a função de desregistrar nome do cliente.
    def unregister_name(self):
        unregister_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    # Chama a função de requisitar informações por um nome do cliente.
    def request_name(self):
        request_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    # Callback ao fechar interface.
    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()
