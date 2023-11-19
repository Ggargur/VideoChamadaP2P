import tkinter as tk
from tkinter import ttk
from client import request_name, unregister_name, register_name


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.show_page(Page1)

    def screen_specs(self, page):
        match page:
            case 'StartPage':
                self.title("Video Chamada P2P")
                self.geometry("280x80")
                self.resizable(False, False)
                return

            case 'Page1':
                self.title("Video Chamada P2P")
                self.geometry("600x600")

    def show_page(self, page):
        self.screen_specs(page.__name__)
        self.container.pack()
        p = page(self.container, self)
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
        self.destroy()
        self.controller.show_page(Page1)

    def register_name(self):
        register_name(self.user_entry.get())
        self.user_entry.delete(0, 100)

    def on_closing(self):
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
        self.create_tabs()

    def create_tabs(self):
        first_tab = ttk.Frame(self.tabs, width=600, height=600)
        second_tab = ttk.Frame(self.tabs, width=600, height=600)
        self.tabs.add(first_tab, text='Descadastar')
        self.tabs.add(second_tab, text='Requisitar')
        self.tabs.pack(expand=1, fill='both')

    def unregister_name(self):
        pass

    def request_name(self):
        pass


app = App()
app.mainloop()
