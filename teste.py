import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from client import request_name, unregister_name, register_name, get_all_registered_names,connect_with


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Video Chamada P2P")
        self.pages = tk.Frame(self)
        self.show_page(StartPage)
        self.data = {}

    def screen_specs(self, page):
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

    def on_closing(self):
        # retirar o cliente da lista de requisições
        if not messagebox.askyesno("Aviso", "Deseja sair?"):
            return
        self.quit()


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
        ttk.Button(self.second_frame, text="Sair", command=self.controller.on_closing).pack(side='left', padx=5, pady=5)

    def show_page(self):
        if self.user_entry.get() == "":
            messagebox.showerror("ERRO", "O campo nome não pode estar vazio")
            return

        # a proxima pagina receberia uma lista dos nomes que o usuario possui

        register_name(self.user_entry.get())
        self.controller.data['username'] = self.user_entry.get()
        self.controller.data['all_names'] = get_all_registered_names()
        self.destroy()
        self.controller.show_page(Page1)

    def init_page(self):
        self.first_frame.pack()
        self.second_frame.pack()
        self.create_name_field()
        self.create_buttons()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.greetings = ttk.Frame(self)
        self.tabs = ttk.Notebook(self)
        self.buttons = ttk.Frame(self)
        self.add_name_to_greetings()
        self.create_tabs()
        self.create_buttons()

    def add_name_to_greetings(self):
        greeting_label = ttk.Label(self.greetings, text=f"Bem vindo, {self.controller.data['username']}")
        greeting_label.grid(column=0, row=0, sticky=tk.N, padx=5, pady=5)
        greeting_label.config(font=12)
        self.greetings.pack()

    def create_tabs(self):
        first_tab = ttk.Frame(self.tabs, width=550, height=490)
        second_tab = ttk.Frame(self.tabs, width=550, height=490)
        self.tabs.add(first_tab, text='Descadastar')
        self.create_list(first_tab)
        self.tabs.add(second_tab, text='Requisitar')
        self.create_searchbar(second_tab)
        self.tabs.pack(expand=1, fill='both')

    def unregister_name(self, name):
        if not messagebox.askyesno("Aviso", "Deseja deletar esse nome?"):
            return
        else:
            unregister_name(name)
            if self.controller.data['username'] == name:
                self.controller.quit()
            else:
                self.controller.data['all_names'] = get_all_registered_names()
                self.controller.show_page(Page1)

    def request_name(self):
        pass

    def create_buttons(self):
        ttk.Button(self.buttons, text="Voltar ao login", command=self.show_page).pack(side='left', padx=10, pady=10)
        ttk.Button(self.buttons, text="Sair", command=self.controller.on_closing).pack(side='left', padx=10, pady=10)
        self.buttons.pack()

    def create_list(self, tab):
        for b in range(len(self.controller.data['all_names'])):
            btn = ttk.Button(tab, text=f"{self.controller.data['all_names'][b]}", width=90,
                             command=lambda: self.unregister_name(self.controller.data['all_names'][b]))
            btn.grid(row=b + 1, padx=4, pady=4)

    def create_searchbar(self, tab):
        second_tab_frame = ttk.Frame(tab)
        label = ttk.Label(second_tab_frame, text='Digite o nome de um usuário')
        label.config(font=12)
        label.pack(padx=10, pady=10)
        search_entry = ttk.Entry(second_tab_frame, width=50).pack(padx=10, pady=10)
        ttk.Button(second_tab_frame, text='Buscar').pack(padx=10, pady=10, command=self.request_name)
        second_tab_frame.pack(anchor='center', expand=1)
    
    def show_page(self):
        self.controller.data = {}
        self.destroy()
        self.controller.show_page(StartPage)


app = App()
app.mainloop()
