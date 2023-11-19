import tkinter as tk
from tkinter import ttk
from client import request_name, unregister_name, register_name


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.pages = {}

        for p in (StartPage, Page1):
            container = tk.Frame(self)
            container.pack()
            page = p(container, self)
            self.pages[p] = page
            page.pack()

        self.show_frame(StartPage)

    def screen_specs(self, page):
        match page:
            case 'StartPage':
                self.title("Video Chamada P2P")
                self.geometry("280x80")
                self.resizable(False, False)
                return

            case 'Page1':
                self.title("Video Chamada P2P")
                self.geometry("300x300")

    def show_frame(self, cont):
        self.screen_specs(cont.__name__)
        frame = self.pages[cont]
        frame.tkraise()

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
        ttk.Button(self.second_frame, text="Cadastrar", command=lambda: self.show_frame()).pack(
            side='left', padx=5, pady=5)
        ttk.Button(self.second_frame, text="Sair", command=self.on_closing).pack(side='left', padx=5, pady=5)


    def show_frame(self):
        self.destroy()
        self.controller.show_frame(Page1)

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
        self.second_frame = ttk.Frame(self)
        self.second_frame.pack()
        self.create_buttons()

    def create_buttons(self):
        ttk.Button(self.second_frame, text="Descadastrar", command=self.unregister_name).pack(side='left', padx=5,
                                                                                              pady=5)
        ttk.Button(self.second_frame, text="Requisitar", command=self.request_name).pack(side='left', padx=5, pady=5)

    def unregister_name(self):
        pass

    def request_name(self):
        pass


app = App()
app.mainloop()
