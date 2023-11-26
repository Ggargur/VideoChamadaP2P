import tkinter as tk
from tkinter import Image, ttk
from tkinter import messagebox
from client import (
    request_name,
    unregister_name,
    register_name,
    get_all_registered_names,
    connect_with,
    update_request_method,
    stop_call
)


# metodo para a retirada de nomes na lista de descadastrar
def call_with_args(func, *args):
    def callback():
        func(*args)

    return callback


# cria a interface do aplicativo, gerencia paginas e o tamanho de janelas
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Video Chamada P2P")
        self.pages = tk.Frame(self)
        self.show_page(StartPage)
        self.data = {}

    # gerencia do tamanho das janelas do aplicativo
    def screen_specs(self, page):
        match page:
            case "StartPage":
                self.geometry("280x80")
                self.resizable(False, False)

            case "Page1":
                self.geometry("650x600")

    # mostra a pagina atual
    def show_page(self, page):
        self.screen_specs(page.__name__)
        self.pages.pack()
        p = page(self.pages, self)
        p.pack()
        p.tkraise()

    # callback para fechar o arquivo
    def on_closing(self):
        if not messagebox.askyesno("Aviso", "Deseja sair?"):
            return
        stop_call()
        self.quit()


# primeira pagina do aplicativo, onde e realizado o cadastro de usuario
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.first_frame = ttk.Frame(self)
        self.second_frame = ttk.Frame(self)
        self.user_entry = ttk.Entry(self.first_frame)
        self.init_page()

    # cria o campo para cadastro do usuario e sua label 'Nome de Usuário'
    def create_name_field(self):
        ttk.Label(self.first_frame, text="Nome de usuário:").grid(
            column=0, row=0, sticky=tk.NW, padx=5, pady=5
        )
        self.user_entry.grid(column=1, row=0, sticky=tk.NE, padx=5, pady=5)

    # cria os botoes para cadastro e saida do programa
    def create_buttons(self):
        ttk.Button(self.second_frame, text="Cadastrar", command=self.show_page).pack(
            side="left", padx=5, pady=5
        )
        ttk.Button(
            self.second_frame, text="Sair", command=self.controller.on_closing
        ).pack(side="left", padx=5, pady=5)

    # sobrecarga do metodo show_page: carrega as informacoes obtidas do campo de cadastro e todos os nomes de usuario,
    # obtidos do servidor, que serao colocados como atributos da class Page1. Caso o campo de cadastro estja vazio,
    # aparecera uma mensagem de erro
    def show_page(self):
        if self.user_entry.get() == "":
            messagebox.showerror("ERRO", "O campo nome não pode estar vazio")
            return

        register_name(self.user_entry.get())
        self.controller.data["username"] = self.user_entry.get()
        self.controller.data["all_names"] = get_all_registered_names()
        self.destroy()
        self.controller.show_page(Page1)

    # carrega os elementos de StartPage
    def init_page(self):
        self.first_frame.pack()
        self.second_frame.pack()
        self.create_name_field()
        self.create_buttons()


# contem a lista de nomes do usuario para serem descadastrados e a busca para a requisicao de videoconferencias
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.greetings = ttk.Frame(self)
        self.tabs = ttk.Notebook(self, width=650, height=490)
        self.buttons = ttk.Frame(self)
        self.init_page()

    # frase de boas vindas, com a inclusao do nome de usuario atual
    def add_name_to_greetings(self):
        greeting_label = ttk.Label(
            self.greetings, text=f"Bem vindo, {self.controller.data['username']}"
        )
        greeting_label.grid(column=0, row=0, sticky=tk.N, padx=5, pady=5)
        greeting_label.config(font=12)
        self.greetings.pack()

    # criacao de tabs da segunda pagina do aplicativo, contendo a lista de nomes para descadastrar e
    # a de busca de usuario para inciar uma videoconferencia
    def create_tabs(self):
        self.first_tab = ttk.Frame(self.tabs)
        self.second_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.first_tab, text='Descadastar')
        self.create_list(self.first_tab)
        self.tabs.add(self.second_tab, text='Requisitar')
        self.create_searchbar(self.second_tab)
        self.tabs.pack(expand=1, fill='both')

    def connect_to(self, name, host, ip):
        print("conectando-se a", name, host, ip)

    # descadastra um nome de usuario da lista presente na tab 'Descadastrar'. Caso esse nome seja o atual do usuário,
    # o aplicativo e fechado
    def unregister_name(self, name: str, btn: ttk.Button):
        if not messagebox.askyesno("Aviso", "Deseja deletar esse nome?"):
            return
        else:
            unregister_name(name)
            if self.controller.data["username"] == name:
                self.controller.quit()
            else:
                btn.destroy()

    def request_name(self, entry: ttk.Entry):
        name = entry.get()
        if name == "":
            if not messagebox.showwarning("Alerta", "Nome não pode ser vazio"):
                return
            return
        host, ip = request_name(name)
        if ip <0:
            messagebox.showwarning("Não encontrado", f"Usuário {name} não encontrado")
            return
        else:
            messagebox.showinfo("Usuário Encontrado", f"Usuário {name} encontrado em {host}:{ip}")
        b = ttk.Button(self.second_tab, text=f"Conectar-se a {name}")
        b['command'] = call_with_args(self.connect_to, name, host, ip)
        b.pack(padx=4, pady=4)

    # Cria botoes em Page1 que permitem ao usuario voltar para StartPage ou sair do aplicativo
    def create_buttons(self):
        ttk.Button(self.buttons, text="Voltar ao login", command=self.show_page).pack(
            side="left", padx=10, pady=10
        )
        ttk.Button(self.buttons, text="Sair", command=self.controller.on_closing).pack(
            side="left", padx=10, pady=10
        )
        self.buttons.pack()

    # cria a lista de nomes de usuario para descadastro
    def create_list(self, tab):
        for b in range(len(self.controller.data["all_names"])):
            btn = ttk.Button(
                tab, text=f"{self.controller.data['all_names'][b]}", width=90
            )
            btn["command"] = call_with_args(
                self.unregister_name, self.controller.data["all_names"][b], btn
            )
            btn.grid(row=b + 1, padx=4, pady=4)

    # cria o campo de busca, o botao para realiza-la e uma label na tab requisitar
    def create_searchbar(self, tab):
        second_tab_frame = ttk.Frame(tab)
        label = ttk.Label(second_tab_frame, text='Digite o nome de um usuário')
        search_entry = ttk.Entry(second_tab_frame, width=50)
        b = ttk.Button(second_tab_frame, text='Buscar')
        b.pack(padx=10, pady=10)
        b['command'] = call_with_args(self.request_name, search_entry)
        label.config(font=12)
        label.pack(padx=10, pady=10)
        search_entry.pack(padx=10, pady=10)
        second_tab_frame.pack(anchor='center', expand=1)

    #carrega os elementos da pagina
    def init_page(self):
        self.add_name_to_greetings()
        self.create_tabs()
        self.create_buttons()

    # sobrecarga do metodo show_page: neste metodo a saida faz com que os dados passados como atributos por StartPage
    # sejam eliminados
    def show_page(self):
        self.controller.data = {}
        self.destroy()
        self.controller.show_page(StartPage)


app = App()
app.mainloop()
