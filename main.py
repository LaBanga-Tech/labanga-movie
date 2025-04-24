from customtkinter import (
    CTk,
    CTkButton,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkScrollableFrame,
    StringVar,
)
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd
import requests as r
import threading


# ? CONVERTE A IMAGEM RECEBIDA EM BYTES
def TratarImagem(url):
    image = BytesIO(r.get(url).content)
    return image


# ! ESTRUTURA DO ÍTEM QUE SERÁ APRESENTADO COMO RESULTADO
def Item(master, titulo: str, tipo: str, ano_lancamento: str, poster: str):
    poster_tk = ImageTk.PhotoImage(Image.open(poster).resize((200, 200)))

    result = CTkFrame(
        master,
        border_color="#bb2727",
        fg_color="#121212",
        border_width=1,
        height=150,
        corner_radius=1,
    )
    result.pack(fill="x", side="top", pady=10, padx=(15, 0))

    CTkLabel(result, width=10, height=10, image=poster_tk, text=None).grid(
        column=0,
        row=0,
        padx=5,
        pady=5,
    )

    info = CTkFrame(result, fg_color="#121212")
    info.grid(column=1, row=0, pady=5, padx=5)

    CTkLabel(
        info,
        text=titulo,
        font=("Arial", 28, "bold"),
        wraplength=700,
    ).grid(column=1, row=0, pady=3, sticky="e")

    CTkLabel(
        info,
        text=f"        {ano_lancamento}        ",
        font=("Arial", 15),
        fg_color="#bb2727",
    ).grid(column=1, row=1, sticky="w", pady=3)

    CTkLabel(
        info,
        text=tipo,
        font=("Arial", 15),
        text_color="#bb2727",
    ).grid(column=1, row=2, sticky="w")


# ! CONFIGURAÇÃO DA JANELA
win = CTk("#1a1a1a")
win_height = win.winfo_screenheight() - 70
win_width = win.winfo_screenwidth() - 200
pad_left = (win.winfo_screenwidth() - win_width) // 2
win.title("LaBanga Movie")
win.minsize(win_width, win_height)
win.geometry(f"{win_width}x{win_height}+{pad_left}+10")
win.iconbitmap("./imagens/logo2.ico")

# ** PRIMEIRO FRAME
frame1 = CTkFrame(win, height=10, corner_radius=0)
frame1.pack(side="top", fill="both")

# IMAGEM DE FUNDO
image = Image.open("./imagens/back.jpg")
image_tk = ImageTk.PhotoImage(image)

back_image = CTkLabel(
    frame1, text=None, image=image_tk, height=350, fg_color="red", width=300
)
back_image.pack(fill="x")

# ** SEGUNDO FRAME
frame2 = CTkFrame(win, fg_color="red", height=100, corner_radius=0)
frame2.place(relx=0.25, y=370)

# CAIXA DE TEXTO
ct_valor = StringVar(value="")
c_texto = CTkEntry(
    frame2,
    width=500,
    height=40,
    placeholder_text="Pesquisar aqui...",
    corner_radius=1,
    border_width=1,
    fg_color="#fff",
    text_color="#531414",
    border_color="#bb2727",
    textvariable=ct_valor,
)
c_texto.bind("<Return>", lambda e: Insert)
c_texto.grid(column=0, row=0)


# LIMPA E ADICIONA DADOS
def Limpar_Adicionar_Dados(dados):
    # LIMPANDO
    for widget in frame3.winfo_children():
        widget.destroy()

    # ADICIONANDO
    for conteudo in dados["Search"]:
        Item(
            frame3,
            conteudo["Title"],
            conteudo["Type"],
            conteudo["Year"],
            TratarImagem(conteudo["Poster"]),
        )


# Chave da API
def Chave_API():
    chave = ""
    with open("./.env", "r") as file:
        chave = file.readline().split("=")[1].strip()
    return chave


# ** INSERINDO OS DADOS RECEBIDOS DA API
def Insert(botao_pesquisar):
    texto = ct_valor.get().strip()

    # BUSCANDO DADOS
    def Buscando_Dados():
        # DESABILITANDO O BOTÃO DE PESQUISA
        botao_pesquisar.configure(state="disabled", image=icone_loading_tk)

        # - URL
        url = f"https://www.omdbapi.com/?s={texto}&apikey={Chave_API()}"

        try:
            requisicao = r.get(url).json()
            print(url)

            if requisicao:
                try:
                    dados = pd.DataFrame(requisicao)

                    Limpar_Adicionar_Dados(dados)
                except:
                    messagebox.showinfo(
                        "LaBanga Movie - Aviso",
                        "Filme/Série não encontrado(a)!",
                    )

        except Exception as Error:
            print("Erro: ", Error)
            messagebox.showinfo(
                "LaBanga Movie - Aviso",
                "Verifique sua conexão com a internet!",
            )
        finally:
            # HABILITANDO O BOTÃO DE PESQUISA
            botao_pesquisar.after(
                0,
                lambda: botao_pesquisar.configure(
                    state="normal", image=icone_search_tk
                ),
            )

    if texto != "":
        threading.Thread(target=Buscando_Dados).start()


# ÍCONE DO BOTÃO
icone_search = Image.open("./imagens/search-icon.png")
icone_loading = Image.open("./imagens/loading-icon.png")
icone_search_tk = ImageTk.PhotoImage(icone_search.resize((24, 24)))
icone_loading_tk = ImageTk.PhotoImage(icone_loading.resize((24, 24)))

# ! BOTÃO PESQUISAR
bt_pesquisar = CTkButton(
    frame2,
    width=100,
    corner_radius=1,
    height=40,
    fg_color="#bb2727",
    hover_color="#531414",
    image=icone_search_tk,
    anchor="center",
    border_color="#bb2727",
    command=lambda: Insert(bt_pesquisar),
    text_color_disabled="green",
    text=None,
)
bt_pesquisar.grid(column=1, row=0)

# ? TERCEIRO FRAME - OS RESULTADOS SERÃO APRESENTADOS AQUI
frame3 = CTkScrollableFrame(
    win,
    fg_color="#121212",
    width=1000,
    height=500,
    scrollbar_button_color="#121212",
    scrollbar_button_hover_color="#bb2727",
    corner_radius=1,
)
frame3.pack(pady=(80, 10), fill="y", side="top")

win.mainloop()
