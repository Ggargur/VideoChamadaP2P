import tkinter
from tkinter import ttk
from client import request_name, unregister_name, register_name


class Interface(tkinter.Tk):
    # Cria a interface.
    def __init__(self):
        super().__init__()
        self.frame1 = tkinter.Frame(self)
        self.frame2 = tkinter.Frame(self)
        self.user_entry = ttk.Entry(self.frame1)
        self.create_interface()

    def screen_specs(self):
        self.title("Video Chamada P2P")
        self.geometry("280x80")
        self.resizable(False, False)

    def create_name_field(self):
        ttk.Label(self.frame1, text="Nome de usuário:").grid(column=0, row=0, sticky=tkinter.NW, padx=5, pady=5)
        self.user_entry.grid(column=1, row=0, sticky=tkinter.NE, padx=5, pady=5)

    def create_buttons(self):
        ttk.Button(self.frame2, text="Cadastrar", command=self.register_name).pack(side='left', padx=5, pady=5)
        ttk.Button(self.frame2, text="Descadastrar", command=self.unregister_name).pack(side='left', padx=5, pady=5)
        ttk.Button(self.frame2, text="Requisitar", command=self.request_name).pack(side='left', padx=5, pady=5)

    # Coloca os elementos visuais na interface.
    def create_interface(self):
        self.screen_specs()

        self.create_buttons()
        self.create_name_field()

        self.frame1.pack()
        self.frame2.pack()

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
