import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from client import request_name, unregister_name, register_name


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.pages = tk.Frame(self)
        self.show_page(StartPage)

    def screen_specs(self, page):
        self.title("Video Chamada P2P")
        match page:
            case 'StartPage':
                self.geometry("280x80")
                self.resizable(False, False)

            case 'Page1':
                self.geometry("650x600")

    def show_page(self, page):
        self.screen_specs(page.__name__)
        self.pages.pack()
        p = page(self.pages, self)
        p.pack()
        p.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.first_frame = ttk.Frame(self)
        self.second_frame = ttk.Frame(self)
        self.user_entry = ttk.Entry(self.first_frame)
        self.init_page()

    def create_name_field(self):
        ttk.Label(self.first_frame, text="Nome de usuário:").grid(column=0, row=0, sticky=tk.NW, padx=5, pady=5)
        self.user_entry.grid(column=1, row=0, sticky=tk.NE, padx=5, pady=5)

    def create_buttons(self):
        ttk.Button(self.second_frame, text="Cadastrar", command=self.show_page).pack(side='left', padx=5, pady=5)
        ttk.Button(self.second_frame, text="Sair", command=self.on_closing).pack(side='left', padx=5, pady=5)

    def show_page(self):
        if self.user_entry.get() == "":
            messagebox.showerror("ERRO", "O campo nome não pode estar vazio")
            return

        # register_name(self.user_entry.get()) a mudanca de pagina registra o usuário
        self.destroy()
        self.controller.show_page(Page1)

    def on_closing(self):
        if not messagebox.askyesno("Aviso", "Deseja sair?"):
            return
        self.controller.quit()

    def init_page(self):
        self.first_frame.pack()
        self.second_frame.pack()
        self.create_name_field()
        self.create_buttons()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.tabs = ttk.Notebook(self)
        self.buttons = ttk.Frame(self)
        self.create_tabs()
        self.create_buttons()

    def create_tabs(self):
        first_tab = ttk.Frame(self.tabs, width=550, height=530)
        second_tab = ttk.Frame(self.tabs, width=550, height=530)
        self.tabs.add(first_tab, text='Descadastar')
        self.create_list(first_tab)
        self.tabs.add(second_tab, text='Requisitar')
        self.tabs.pack(expand=1, fill='both')

    def unregister_name(self):
        pass

    def request_name(self):
        pass

    def create_buttons(self):
        ttk.Button(self.buttons, text="Voltar ao login", command=self.show_page).pack(side='left', padx=10, pady=10)

        ttk.Button(self.buttons, text="Sair", command=self.on_closing).pack(side='left', padx=10, pady=10)

        self.buttons.pack()

    def create_list(self, tab):
        for b in range(10):
            btn = ttk.Button(tab, text=f'Botão {b}', width=90)
            btn.grid(row=b + 1, padx=4, pady=4)

    def show_page(self):
        self.destroy()
        self.controller.show_page(StartPage)

    def on_closing(self):
        if not messagebox.askyesno("Aviso", "Deseja sair?"):
            return
        self.controller.quit()


app = App()
app.mainloop()
