# Importa a biblioteca Tkinter para criar interfaces gráficas
import tkinter as tk

# Importa componentes específicos do Tkinter:
# - `ttk` para widgets mais modernos
# - `Toplevel` para criar janelas secundárias
# - `StringVar` para manipular variáveis de texto
#       reativas na interface
# - `messagebox` para exibir caixas de diálogo e mensagens
# - `END` para indicar o final de uma entrada em um campo de texto
from tkinter import (
    ttk,
    Toplevel,
    StringVar,
    messagebox,
    END
)

from PIL.ImageOps import expand
from openpyxl.styles.builtins import styles, title
from pandas.core.indexes.base import str_t
from pandas.core.reshape.reshape import unstack
from reportlab.graphics.samples.excelcolors import backgroundGrey
from reportlab.lib.pdfencrypt import padding

"""
Onde encontrar mais emojis Unicode?
Se quiser encontrar mais ícones como esses, pode usar o seguinte site:

🔹 Emojipedia – Para procurar emojis e copiar diretamente.
    https://emojipedia.org/
"""

# Importa `Calendar` e `DateEntry` da biblioteca `tkcalendar`
# - `Calendar` permite exibir um calendário interativo
# - `DateEntry` é um campo de entrada para selecionar datas
from tkcalendar import Calendar, DateEntry

# Importa funcionalidades da biblioteca Pillow para manipulação de imagens
# - `Image` permite abrir, modificar e salvar imagens
# - `ImageTk` converte imagens para um formato compatível com Tkinter
from PIL import Image, ImageTk

# Importa `datetime` para manipulação e formatação de datas e horas
from datetime import datetime

# Importa o cliente `MongoClient` para conectar-se a um
#       banco de dados MongoDB
from pymongo import MongoClient, version_tuple

# Importa `ObjectId` para manipular identificadores únicos no MongoDB
from bson import ObjectId

# Importa `pandas` para manipulação e análise de dados em DataFrames
import pandas as pd

# -------------------------------------------------------------------------
# Conexão MongoDB
# -------------------------------------------------------------------------

# Cria uma conexão com o servidor do MongoDB que está rodando localmente
# "mongodb://localhost:27017/" significa que estamos
#       conectando ao MongoDB na máquina local (localhost)
# na porta padrão 27017, que é a porta padrão do MongoDB.
client = MongoClient("mongodb://localhost:27017/")

# Acessa o banco de dados chamado "Vagas_Estacionamento_db"
# Se esse banco de dados não existir, ele será criado
#       automaticamente ao inserir os primeiros dados.
db = client["Vagas_Estacionamento_db"]

# Abaixo, estamos criando referências para coleções (tabelas no MongoDB)
# O MongoDB organiza os dados em coleções, que são
#       semelhantes a tabelas em bancos relacionais.

# Cria ou acessa a coleção "usuarios", onde serão armazenadas
#       informações sobre os usuários do sistema.
colecao_usuarios = db["usuarios"]

# Cria ou acessa a coleção "clientes", onde serão armazenados
#       dados dos clientes do estacionamento.
colecao_clientes = db["clientes"]

# Cria ou acessa a coleção "veiculos", onde serão
#       cadastrados os veículos dos clientes.
colecao_veiculos = db["veiculos"]

# Cria ou acessa a coleção "blocos", que pode ser usada para
#       armazenar informações sobre setores ou áreas do estacionamento.
colecao_blocos = db["blocos"]

# Cria ou acessa a coleção "vagas", onde estarão registradas as
#       vagas disponíveis no estacionamento.
colecao_vagas = db["vagas"]

# Cria ou acessa a coleção "reservas", onde serão armazenados os
#       registros de reservas de vagas feitas pelos clientes.
colecao_reservas = db["reservas"]



# Define a função `centralizar_janela` que centraliza uma janela na tela.
# Parâmetros:
# - `janela`: a janela que será centralizada.
# - `largura`: a largura da janela desejada.
# - `altura`: a altura da janela desejada.
def centralizar_janela(janela, largura, altura):

    # Obtém a largura total da tela do usuário.
    # `winfo_screenwidth()` retorna a largura em pixels da tela principal.
    largura_tela = janela.winfo_screenwidth()

    # Obtém a altura total da tela do usuário.
    # `winfo_screenheight()` retorna a altura em pixels da tela principal.
    altura_tela = janela.winfo_screenheight()

    # Calcula a posição horizontal (x) para centralizar a janela na tela.
    # `(largura_tela - largura) // 2` desloca a janela
    #       para o centro horizontalmente.
    x = (largura_tela - largura) // 2

    # Calcula a posição vertical (y) para centralizar a janela na tela.
    # `(altura_tela - altura) // 2` desloca a janela
    #       para o centro verticalmente.
    y = (altura_tela - altura) // 2

    # Define a geometria da janela com a largura, altura e as
    #       coordenadas `x` e `y` calculadas.
    # O formato da string f"{largura}x{altura}+{x}+{y}"
    #       define o tamanho e a posição da janela.
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


# -------------------------------------------------------------------------
# Tela de Login
# -------------------------------------------------------------------------

# Função que cria e exibe a tela de login do sistema.
def tela_login():

    # Cria a janela principal da interface gráfica.
    root = tk.Tk()

    # Define o título da janela para "Login - Sistema de Estacionamento".
    root.title("Login - Sistema de Estacionamento")

    # Maximiza a janela automaticamente para ocupar toda a tela.
    # `zoomed` funciona como um modo de tela cheia, mas
    #       sem ocultar a barra de tarefas.
    root.state("zoomed")

    # Define a cor de fundo da janela principal.
    # "#ECEFF1" é um tom claro de cinza-azulado para um
    #       visual moderno e agradável.
    root.configure(bg="#ECEFF1")

    # Cria um estilo para os botões usando o
    #       módulo ttk (Themed Tkinter Widgets).
    estilo = ttk.Style()

    # Configura o estilo padrão dos botões (`TButton`).
    # Define a fonte como "Arial", tamanho 12, garantindo boa legibilidade.
    # Adiciona `padding=8`, que cria um espaçamento
    #       interno ao redor do texto do botão.
    estilo.configure("TButton", font=("Arial", 12), padding=8)

    # Cria um frame principal para centralizar os elementos da tela de login.
    # `bg="#ECEFF1"` define a cor de fundo do frame como um tom de cinza claro.
    frame_container = tk.Frame(root, bg="#ECEFF1")

    # Posiciona o frame no centro da tela.
    # `relx=0.5` define a posição horizontal no centro da tela.
    # `rely=0.5` define a posição vertical no centro da tela.
    # `anchor="center"` faz com que o ponto de referência do frame seja o centro.
    frame_container.place(relx=0.5, rely=0.5, anchor="center")

    # Cria um rótulo de título para a tela de login.
    # `text="🔒 Acesso ao Sistema"` define o texto exibido no
    #       rótulo com um ícone de cadeado.
    # `font=("Arial", 24, "bold")` define a fonte como Arial, tamanho 24, e negrito.
    # `foreground="#2E86C1"` define a cor do texto como azul vibrante.
    # `background="#ECEFF1"` define a cor de fundo do rótulo
    #       como o mesmo tom de cinza claro do frame.
    lbl_titulo = ttk.Label(frame_container,
                           text="🔒 Acesso ao Sistema",
                           font=("Arial", 24, "bold"),
                           foreground="#2E86C1",
                           background="#ECEFF1")

    # Exibe o rótulo na interface.
    # `pady=10` adiciona 10 pixels de espaçamento vertical ao
    #       redor do rótulo para separação visual.
    lbl_titulo.pack(pady=10)

    # Cria um frame para a caixa de login onde o usuário informará suas credenciais.
    # `frame_container` é o frame pai que contém esse elemento.
    # `text="Informe suas credenciais"` adiciona um título descritivo ao frame.
    # `padding=20` adiciona um espaçamento interno de 20 pixels
    #       para melhor organização visual.
    # `relief="ridge"` define uma borda em relevo ao redor do
    #       frame, dando um efeito de contorno.
    frame_formulario = ttk.LabelFrame(frame_container,
                                      text="Informe suas credenciais",
                                      padding=20,
                                      relief="ridge")

    # Exibe o frame na interface.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels
    #       abaixo do frame, para melhor separação dos elementos.
    frame_formulario.pack(pady=10)

    # Usuário
    # Cria um rótulo (label) para o campo de entrada do usuário.
    # `frame_formulario` é o frame onde o rótulo será inserido.
    # `text="Usuário:"` define o texto exibido no rótulo.
    # `font=("Arial", 14)` define a fonte como Arial,
    #       tamanho 14, para melhor legibilidade.
    # `grid(row=0, column=0, padx=5, pady=5, sticky="e")`
    #       posiciona o rótulo na primeira linha (row=0),
    #       primeira coluna (column=0), com espaçamento
    #       horizontal (padx=5) e vertical (pady=5).
    # `sticky="e"` alinha o rótulo à direita (leste) da célula na grade.
    ttk.Label(frame_formulario,
              text="Usuário:",
              font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (Entry) para que o usuário possa digitar seu nome.
    # `frame_formulario` é o frame onde o campo de entrada será inserido.
    # `width=30` define a largura do campo como 30 caracteres.
    # `font=("Arial", 14)` define a fonte do texto
    #       digitado no campo, para melhor visibilidade.
    entrada_usuario = ttk.Entry(frame_formulario, width=30, font=("Arial", 14))

    # Posiciona o campo de entrada na interface.
    # `grid(row=0, column=1, padx=5, pady=5)` o posiciona na primeira linha (row=0),
    # segunda coluna (column=1), com espaçamento horizontal (padx=5) e vertical (pady=5).
    entrada_usuario.grid(row=0, column=1, padx=5, pady=5)

    # Insere um nome padrão no campo de entrada quando a interface é aberta.
    # `insert(0, "clevison")` adiciona o texto "clevison" na
    #       posição inicial (índice 0) do campo.
    entrada_usuario.insert(0, "clevison")

    # Senha
    # Cria um rótulo (label) para o campo de entrada da senha.
    # `frame_formulario` é o frame onde o rótulo será inserido.
    # `text="Senha:"` define o texto exibido no rótulo.
    # `font=("Arial", 14)` define a fonte do texto como Arial,
    #       tamanho 14, garantindo boa legibilidade.
    # `grid(row=1, column=0, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na segunda linha (row=1),
    #       primeira coluna (column=0), com espaçamento
    #       horizontal (padx=5) e vertical (pady=5).
    # `sticky="e"` alinha o rótulo à direita (leste) da célula na grade.
    ttk.Label(frame_formulario,
              text="Senha:",
              font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (Entry) para que o usuário possa digitar sua senha.
    # `frame_formulario` é o frame onde o campo de entrada será inserido.
    # `width=30` define a largura do campo como 30 caracteres.
    # `show="*"` oculta os caracteres digitados no campo,
    #       substituindo-os por asteriscos (*), garantindo segurança.
    # `font=("Arial", 14)` define a fonte do texto digitado no
    #       campo, mantendo a visibilidade adequada.
    entrada_senha = ttk.Entry(frame_formulario,
                              width=30,
                              show="*",
                              font=("Arial", 14))

    # Posiciona o campo de entrada da senha na interface.
    # `grid(row=1, column=1, padx=5, pady=5)` o posiciona na segunda linha (row=1),
    # segunda coluna (column=1), com espaçamento horizontal (padx=5) e vertical (pady=5).
    entrada_senha.grid(row=1, column=1, padx=5, pady=5)

    # Insere um valor padrão no campo de senha quando a interface é aberta.
    # `insert(0, "555")` adiciona o texto "555" na
    #       posição inicial (índice 0) do campo.
    # OBS: Em um ambiente real, nunca se deve inserir
    #       senhas fixas por segurança.
    entrada_senha.insert(0, "555")

    # Espaçamento antes dos botões
    # Cria um rótulo vazio dentro do `frame_formulario` para
    #       adicionar espaçamento entre os elementos.
    # `ttk.Label(frame_formulario)` cria um rótulo sem texto.
    # `grid(row=2, column=0, columnspan=2, pady=5)` posiciona o
    #       rótulo na terceira linha (row=2),
    #       ocupando duas colunas (columnspan=2), e adiciona um
    #       espaçamento vertical de 5 pixels (pady=5).
    ttk.Label(frame_formulario).grid(row=2, column=0, columnspan=2, pady=5)

    # Cria um frame que conterá os botões da interface.
    # `tk.Frame(frame_container, bg="#ECEFF1")` define que o
    #       frame será um filho do `frame_container`,
    #       e que sua cor de fundo será `#ECEFF1` para manter a
    #       padronização visual.
    frame_botoes = tk.Frame(frame_container, bg="#ECEFF1")

    # Exibe o `frame_botoes` na interface e adiciona um espaçamento vertical.
    # `pack(pady=10)` posiciona o frame abaixo dos outros elementos e
    #       adiciona 10 pixels de espaçamento vertical.
    frame_botoes.pack(pady=10)


    # Define a função `autenticar`, responsável por validar o
    #       usuário e a senha inseridos.
    def autenticar():

        """
        Função responsável por autenticar um usuário no sistema.
        Ela verifica se o usuário e a senha informados existem no banco de dados
                e, em caso positivo, permite o acesso à tela principal do sistema.
        """

        # Obtém o valor digitado no campo de entrada de usuário.
        # `.strip()` remove espaços em branco no início e no final do texto,
        #       garantindo que não haja espaços indesejados.
        usuario = entrada_usuario.get().strip()

        # Obtém o valor digitado no campo de entrada da senha.
        # `.strip()` também remove espaços em branco desnecessários, garantindo
        #       que a senha seja tratada corretamente.
        senha = entrada_senha.get().strip()

        # Verifica se os campos de usuário ou senha estão vazios.
        # Se algum dos dois estiver vazio, exibe uma mensagem de erro e encerra a função.
        if not usuario or not senha:

            # Exibe uma mensagem de erro informando que o usuário e a senha são obrigatórios.
            # `messagebox.showerror()` cria um pop-up com título "Erro" e a mensagem informando o problema.
            # `parent=root` define que a janela principal (`root`) é a responsável pela mensagem exibida.
            messagebox.showerror("Erro",
                                 "Por favor, informe usuário e senha!", parent=root)

            # `return` encerra a execução da função imediatamente,
            #       impedindo que a autenticação continue.
            return

        # Exibe no console um log da tentativa de autenticação com os dados inseridos.
        # **Importante:** Nunca exiba a senha do usuário em logs em
        #       sistemas reais, pois isso compromete a segurança.
        print(f"Tentando autenticar: Usuário = {usuario}, Senha = {senha}")

        # 🔹 Busca o usuário no banco de dados
        # O método `find_one()` pesquisa na coleção `colecao_usuarios` um
        #       documento onde "usuario" corresponda ao valor informado.
        usuario_encontrado = colecao_usuarios.find_one({"usuario": usuario})

        # Verifica se o usuário foi encontrado no banco de dados.
        if usuario_encontrado:

            # Exibe no console os detalhes do usuário encontrado no
            #       banco para fins de depuração.
            print("Usuário encontrado no banco:", usuario_encontrado)

        else:

            # Se o usuário não for encontrado, exibe no console uma mensagem
            #       indicando a ausência do usuário no banco.
            print("Usuário não encontrado.")


        # Aqui, verificamos se o usuário foi encontrado e se a senha informada
        #       corresponde à senha armazenada no banco de dados.
        if usuario_encontrado and usuario_encontrado.get("senha") == senha:

            # Se as credenciais estiverem corretas, exibe uma mensagem
            #       informando que o login foi bem-sucedido.
            messagebox.showinfo("Sucesso",
                                f"Bem-vindo(a), {usuario}!", parent=root)

            # Fecha a janela de login, pois a autenticação foi concluída com sucesso.
            root.destroy()

            # Chama a função `tela_dashboard()`, que carrega a interface principal do sistema.
            # Essa função deve estar definida no código para que a transição ocorra corretamente.
            tela_dashboard()


        else:

            # Se a autenticação falhar (usuário não encontrado ou senha incorreta),
            # exibe uma mensagem de erro informando que os dados fornecidos são inválidos.
            messagebox.showerror("Erro", "Usuário ou senha inválidos!", parent=root)


    # Define a função `abrir_crud_usuarios()` para abrir a
    #       tela de gerenciamento de usuários.
    def abrir_crud_usuarios():

        # Chama a função `tela_usuarios_crud(None)` para abrir a
        #       interface de CRUD de usuários.
        # `None` pode ser um parâmetro opcional para inicializar a
        #       tela sem informações prévias.
        tela_usuarios_crud(None)


    # Cria um botão para realizar o login.
    # `text="✅ Entrar"` define o texto do botão, incluindo um
    #       ícone de check (✅) para melhorar a interface.
    # `command=autenticar` define que, ao clicar no botão, a
    #       função `autenticar()` será executada.
    # `width=15` define a largura do botão, garantindo que o
    #       tamanho seja consistente.
    btn_entrar = ttk.Button(frame_botoes,
                            text="✅ Entrar",
                            command=autenticar, width=15)

    # Posiciona o botão `btn_entrar` dentro do `frame_botoes`.
    # `row=0, column=0` define a posição do botão na grade (linha 0, coluna 0).
    # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do botão.
    btn_entrar.grid(row=0, column=0, padx=10, pady=5)

    # Cria um botão para abrir a tela de cadastro de usuários.
    # `text="➕ Cadastrar"` define o texto do botão com um ícone de
    #       adição (➕) para indicar cadastro.
    # `command=abrir_crud_usuarios` define que, ao clicar no
    #       botão, a função `abrir_crud_usuarios()` será executada.
    # `width=15` define a largura do botão para manter um tamanho uniforme.
    btn_cadastrar = ttk.Button(frame_botoes,
                               text="➕ Cadastrar",
                               command=abrir_crud_usuarios,
                               width=15)

    # Posiciona o botão `btn_cadastrar` dentro do `frame_botoes`.
    # `row=0, column=1` coloca o botão na linha 0, coluna 1 (ao lado do botão "Entrar").
    # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os botões.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels abaixo do botão.
    btn_cadastrar.grid(row=0, column=1, padx=10, pady=5)

    # Cria um botão para fechar a aplicação.
    # `text="🚪 Sair"` define o texto do botão com um ícone de porta (🚪) para indicar saída.
    # `command=root.destroy` define que, ao clicar no botão, a janela principal será fechada.
    # `width=15` define a largura do botão para manter um tamanho consistente.
    btn_sair = ttk.Button(frame_container,
                          text="🚪 Sair",
                          command=root.destroy, width=15)

    # Posiciona o botão `btn_sair` dentro do `frame_container`.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels
    #       acima e abaixo do botão para melhor visualização.
    btn_sair.pack(pady=10)

    # Inicia o loop principal do Tkinter para exibir a interface
    #       gráfica e aguardar interações do usuário.
    root.mainloop()


# -------------------------------------------------------------------------
# Tela Principal (Dashboard)
# -------------------------------------------------------------------------

# Define a função responsável por criar e exibir a tela do dashboard.
# Esta função inicializa a interface gráfica do dashboard principal.
def tela_dashboard():

    # Cria a janela principal do dashboard.
    # `tk.Tk()` inicializa a interface gráfica do Tkinter e
    #       gera a janela principal do dashboard.
    dash = tk.Tk()

    # Define o título da janela do dashboard.
    # `"Dashboard Principal"` será exibido na barra de título da janela.
    dash.title("Dashboard Principal")

    # Configura a janela para iniciar maximizada (em tela cheia).
    # `state('zoomed')` faz com que a janela ocupe toda a tela ao ser aberta.
    dash.state('zoomed')

    # Define a cor de fundo da janela do dashboard.
    # `bg="#F5F5F5"` aplica um tom de cinza claro ao fundo da
    #       interface para um visual mais limpo e profissional.
    dash.configure(bg="#F5F5F5")

    # Cria um estilo personalizado para os botões do dashboard.
    # `ttk.Style()` permite configurar estilos visuais para
    #       widgets da biblioteca Tkinter.
    estilo = ttk.Style()

    # Configura o estilo dos botões do tipo `TButton` dentro do Tkinter.
    # `font=("Arial", 14)` define a fonte dos botões
    #       como Arial, tamanho 14, proporcionando melhor legibilidade.
    # `padding=12` adiciona espaçamento interno de 12 pixels ao redor
    #       do texto dentro dos botões, tornando-os mais espaçosos.
    estilo.configure("TButton", font=("Arial", 14), padding=12)

    # Cria um frame que servirá como container principal
    #       dentro da janela do dashboard.
    # `bg="#F5F5F5"` define a cor de fundo como cinza claro.
    frame_container = tk.Frame(dash, bg="#F5F5F5")

    # Posiciona o frame no centro da tela.
    # `relx=0.5` define a posição no meio da largura da tela.
    # `rely=0.5` define a posição no meio da altura da tela.
    # `anchor="center"` faz com que o frame seja centralizado
    #       pelo seu próprio centro.
    frame_container.place(relx=0.5, rely=0.5, anchor="center")

    # Cria um rótulo de título para a tela do dashboard.
    # `text="📊 DASHBOARD PRINCIPAL"` define o texto que será exibido.
    # `font=("Arial", 28, "bold")` configura a fonte
    #       como Arial, tamanho 28, em negrito.
    # `foreground="#2E86C1"` define a cor do texto como azul escuro.
    # `background="#F5F5F5"` define a cor de fundo do rótulo como cinza claro.
    lbl_title = ttk.Label(frame_container,
                          text="📊 DASHBOARD PRINCIPAL",
                          font=("Arial", 28, "bold"),
                          foreground="#2E86C1",
                          background="#F5F5F5")

    # Exibe o rótulo na interface gráfica.
    # `pady=10` adiciona 10 pixels de espaçamento
    #       vertical acima e abaixo do rótulo.
    lbl_title.pack(pady=10)

    # Cria um frame para organizar os botões do dashboard.
    # `bg="#F5F5F5"` define a cor de fundo como cinza claro.
    frame_botoes = tk.Frame(frame_container, bg="#F5F5F5")

    # Exibe o frame que contém os botões na interface.
    # `pady=20` adiciona 20 pixels de espaçamento
    #       vertical abaixo do rótulo.
    frame_botoes.pack(pady=20)

    # Define a função para abrir a tela de CRUD de usuários.
    # `tela_usuarios_crud(dash)` chama a função correspondente e
    #       passa a janela do dashboard como parâmetro.
    def abrir_crud_usuarios():
        tela_usuarios_crud(dash)


    # Define a função para abrir a tela de CRUD de clientes.
    # `tela_clientes_crud(dash)` chama a função correspondente e
    #       passa a janela do dashboard como parâmetro.
    def abrir_crud_clientes():
        tela_clientes_crud(dash)

    # Define a função para abrir a tela de CRUD de veículos.
    # `tela_veiculos_crud(dash)` chama a função correspondente e
    #       passa a janela do dashboard como parâmetro.
    def abrir_crud_veiculos():
        tela_veiculos_crud(dash)

    # Define a função para abrir a tela de CRUD de blocos.
    # `tela_blocos_crud(dash)` chama a função correspondente e
    #       passa a janela do dashboard como parâmetro.
    def abrir_crud_blocos():
        tela_blocos_crud(dash)

    # Define a função para abrir o mapa de reservas.
    # `tela_mapa_reservas(dash)` chama a função correspondente e
    #       passa a janela do dashboard como parâmetro.
    def abrir_mapa():
        tela_mapa_reservas(dash)

    # Define a função para abrir a tela de relatórios.
    # `tela_relatorio(dash)` chama a função correspondente e
    #       passa a janela do dashboard como parâmetro.
    def abrir_rel():
        tela_relatorio(dash)


    # Define uma lista contendo os botões do dashboard.
    # Cada tupla contém um ícone com texto e a função
    #       correspondente ao botão.
    botoes = [
        ("👤 Usuários", abrir_crud_usuarios),  # Botão para abrir a tela de gerenciamento de usuários.
        ("👥 Clientes", abrir_crud_clientes),  # Botão para abrir a tela de gerenciamento de clientes.
        ("🚗 Veículos", abrir_crud_veiculos),  # Botão para abrir a tela de gerenciamento de veículos.
        ("🏢 Blocos", abrir_crud_blocos),  # Botão para abrir a tela de gerenciamento de blocos.
        ("🗺️ Mapa Reservas", abrir_mapa),  # Botão para abrir a tela de mapa de reservas.
        ("📑 Relatório", abrir_rel)  # Botão para abrir a tela de relatórios do sistema.
    ]

    # Percorre a lista de botões para criá-los dinamicamente.
    # `enumerate(botoes)` gera um índice `i` e os
    #       valores `texto` e `comando` de cada botão.
    for i, (texto, comando) in enumerate(botoes):

        # Cria um botão `ttk.Button` dentro do `frame_botoes`.
        # `text=texto` define o texto do botão, incluindo um ícone e a descrição.
        # `style="TButton"` aplica o estilo personalizado configurado anteriormente.
        # `command=comando` associa a função correta que
        #       será executada ao clicar no botão.
        # `width=20` define a largura do botão para
        #       garantir um tamanho uniforme.
        btn = ttk.Button(frame_botoes,
                         text=texto,
                         style="TButton",
                         command=comando,
                         width=20)

        # Posiciona o botão na grade (`grid`) dentro do `frame_botoes`.
        # `row=i // 2` organiza os botões em linhas, distribuindo-os de 2 em 2.
        # `column=i % 2` organiza os botões em colunas alternadas.
        # `padx=15` adiciona espaçamento horizontal entre os botões.
        # `pady=15` adiciona espaçamento vertical entre os botões.
        btn.grid(row=i // 2, column=i % 2, padx=15, pady=15)

    # Cria um botão para sair do sistema.
    # `text="🚪 Sair"` define o texto exibido no botão,
    #       incluindo um ícone de porta de saída.
    # `command=dash.destroy` associa a ação de fechar a
    #       janela ao clicar no botão.
    # `width=20` define a largura do botão para manter o
    #       alinhamento com os demais.
    btn_sair = ttk.Button(frame_container,
                          text="🚪 Sair",
                          command=dash.destroy, width=20)

    # Posiciona o botão no layout usando `pack()`.
    # `pady=20` adiciona um espaçamento vertical de 20 pixels
    #       para afastar o botão dos demais elementos.
    btn_sair.pack(pady=20)

    # Inicia o loop principal da interface gráfica.
    # `mainloop()` mantém a janela aberta e responde a
    #       interações do usuário.
    dash.mainloop()



# -------------------------------------------------------------------------
# Tela de Relatório (Treeview + Filtros)
# -------------------------------------------------------------------------

# Cria a função `tela_relatorio` para exibir um relatório completo.
# `parent` representa a janela principal que chama essa função.
def tela_relatorio(parent):

    # Cria uma nova janela `Toplevel`, que é uma janela
    #       secundária sobre a principal.
    janela = Toplevel(parent)

    # Define o título da janela como "Relatório Completo".
    janela.title("Relatório Completo")

    # Configura a janela para abrir no modo maximizado (tela cheia).
    janela.state("zoomed")

    # Aplica um estilo personalizado à janela, conforme
    #       definido em `criar_estilo_geral`.
    criar_estilo_geral(janela)

    # Cria um frame principal dentro da janela para
    #       organizar os elementos visuais.
    frame_main = ttk.Frame(janela)

    # O `pack` posiciona o frame na tela, expandindo-o para
    #       preencher o espaço disponível.
    # `fill="both"` permite que ele cresça tanto na horizontal quanto na vertical.
    # `expand=True` faz com que o frame ocupe todo o espaço possível.
    # `padx=10, pady=10` adiciona um espaçamento de 10 pixels em todas as direções.
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Cria um rótulo (`Label`) para exibir o título do relatório.
    lbl_title = ttk.Label(frame_main,  # Define que o rótulo pertence ao `frame_main`.
                          text="Relatório Geral de Reservas",  # Texto que será exibido no rótulo.
                          font=("Arial", 18, "bold"),  # Define a fonte como Arial, tamanho 18 e em negrito.
                          foreground="#3F51B5")  # Define a cor do texto como um tom de azul escuro.

    # Posiciona o rótulo na tela com um espaçamento
    #       vertical de 10 pixels (`pady=10`).
    lbl_title.pack(pady=10)

    # Filtros
    # Cria um frame para os filtros do relatório.
    # Esse frame será responsável por agrupar os campos de entrada do usuário.
    frame_filtro = ttk.Frame(frame_main)

    # Adiciona um espaçamento vertical de 5 pixels.
    frame_filtro.pack(pady=5)

    # Cria um rótulo para indicar o campo de filtro pelo CPF do cliente.
    # `text="Cliente (CPF):"` define o texto que será exibido no rótulo.
    # O rótulo será posicionado na primeira linha (row=0) e primeira coluna (column=0).
    # `padx=5, pady=5` adiciona espaçamento horizontal e vertical para melhor disposição.
    # `sticky="e"` alinha o rótulo à direita dentro da célula.
    ttk.Label(frame_filtro,
              text="Cliente (CPF):").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para o CPF do cliente.
    # `width=15` define a largura do campo como 15 caracteres,
    #       proporcionando um espaço adequado para inserir o CPF.
    # O campo de entrada será utilizado para filtrar os dados de
    #       reservas de um cliente específico, baseado no CPF.
    # `grid(row=0, column=1)` posiciona o campo de entrada na
    #       primeira linha (linha 0) e segunda coluna (coluna 1).
    # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical
    #       para que o campo de entrada tenha um visual mais organizado e espaçado.
    entry_cpf = ttk.Entry(frame_filtro, width=15)
    entry_cpf.grid(row=0, column=1, padx=5, pady=5)

    # Cria um rótulo (label) para indicar o campo de filtro pela placa do veículo.
    # `text="Veículo (Placa):"` define o texto que será exibido no
    #       rótulo. O texto informa ao usuário qual campo preencher.
    # O rótulo é posicionado na primeira linha (row=0) e terceira
    #       coluna (column=2) da grade (grid).
    # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao
    #       redor do rótulo, para que ele não fique encostado nas bordas.
    # `sticky="e"` alinha o texto do rótulo à direita, o que é
    #       comum para rótulos em campos de formulário.
    ttk.Label(frame_filtro,
              text="Veículo (Placa):").grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para a placa do veículo.
    # `width=15` define a largura do campo de entrada como 15
    #       caracteres, suficiente para a placa do veículo.
    # Este campo será usado para filtrar as reservas de um
    #       veículo específico, baseado na placa.
    # `grid(row=0, column=3)` posiciona o campo na primeira linha (linha 0) e
    #       quarta coluna (coluna 3) da grade (grid).
    # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao
    #       redor do campo de entrada, para um layout mais organizado.
    entry_placa = ttk.Entry(frame_filtro, width=15)
    entry_placa.grid(row=0, column=3, padx=5, pady=5)

    # Cria um rótulo (label) para indicar o campo de filtro pelo bloco.
    # `text="Bloco:"` define o texto exibido no rótulo, que
    #       orienta o usuário a inserir o nome do bloco.
    # O rótulo é posicionado na primeira linha (row=0) e quinta coluna (column=4) da grade.
    # `padx=5` e `pady=5` adicionam espaçamento ao redor do rótulo.
    # `sticky="e"` alinha o texto à direita, o que é comum para rótulos de campos de formulário.
    ttk.Label(frame_filtro,
              text="Bloco:").grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para o nome do bloco.
    # `width=10` define a largura do campo de entrada como 10
    #       caracteres, o suficiente para um nome de bloco curto.
    # Este campo será usado para filtrar as reservas de um bloco específico.
    # `grid(row=0, column=5)` posiciona o campo na primeira linha (linha 0) e
    #       sexta coluna (coluna 5) da grade (grid).
    # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do
    #       campo de entrada, criando um layout mais espaçado e organizado.
    entry_bloco = ttk.Entry(frame_filtro, width=10)
    entry_bloco.grid(row=0, column=5, padx=5, pady=5)

    # Cria um rótulo (label) para indicar o campo de filtro pelo status.
    # `text="Status:"` define o texto exibido no rótulo, orientando o
    #       usuário a inserir o status da reserva.
    # O rótulo é posicionado na primeira linha (row=0) e sétima coluna (column=6) da grade.
    # `padx=5` e `pady=5` adicionam espaçamento ao redor do rótulo.
    # `sticky="e"` alinha o texto à direita, o que é comum para
    #       rótulos de campos de formulário.
    ttk.Label(frame_filtro,
              text="Status:").grid(row=0, column=6, padx=5, pady=5, sticky="e")

    # Cria uma combobox para seleção do status da reserva.
    # `values=["","Reservado","Finalizado","Cancelado","Ocupada"]`
    #       define as opções disponíveis na combobox.
    # A primeira opção (uma string vazia) permite limpar a seleção e não aplicar filtro de status.
    # `state="readonly"` faz com que a combobox seja apenas para seleção e não para digitação.
    # `width=12` define a largura da combobox para acomodar as opções.
    # `grid(row=0, column=7, padx=5, pady=5)` posiciona a combobox na
    #       primeira linha (linha 0) e oitava coluna (coluna 7) da grade.
    # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao
    #       redor da combobox, tornando o layout mais espaçado e organizado.
    combo_st = ttk.Combobox(frame_filtro,
                            values=["", "Reservado", "Finalizado", "Cancelado", "Ocupada"],
                            state="readonly",
                            width=12)
    combo_st.grid(row=0, column=7, padx=5, pady=5)

    # Define a opção inicial da combobox como vazia (nenhum status selecionado).
    # Isso pode ser útil para permitir que o usuário inicie sem filtro.
    combo_st.set("")

    # Data Início e Data Fim usando DateEntry
    # Cria um rótulo (label) para indicar o campo de entrada da data de início.
    # `text="Data Início:"` define o texto exibido no rótulo.
    # `grid(row=1, column=0, padx=5, pady=5, sticky="e")`
    #       posiciona o rótulo na linha 1, coluna 0.
    # `padx=5` e `pady=5` adicionam espaçamento ao redor do rótulo.
    # `sticky="e"` alinha o rótulo à direita da célula na grade.
    ttk.Label(frame_filtro,
              text="Data Início:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada de data para o usuário selecionar a data de início.
    # `DateEntry(frame_filtro, date_pattern="dd/MM/yyyy", width=12)` cria o campo com
    #       formato de data brasileiro (dia/mês/ano).
    # `width=12` define a largura do campo de entrada.
    # `grid(row=1, column=1, padx=5, pady=5)` posiciona o campo na
    #       linha 1, coluna 1, ao lado do rótulo.
    date_ini = DateEntry(frame_filtro, date_pattern="dd/MM/yyyy", width=12)
    date_ini.grid(row=1, column=1, padx=5, pady=5)

    # Cria um rótulo (label) para indicar o campo de entrada da data de fim.
    # `text="Data Fim:"` define o texto exibido no rótulo.
    # `grid(row=1, column=2, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na linha 1, coluna 2.
    # `padx=5` e `pady=5` adicionam espaçamento ao redor do rótulo.
    # `sticky="e"` alinha o rótulo à direita da célula na grade.
    ttk.Label(frame_filtro,
              text="Data Fim:").grid(row=1, column=2, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada de data para o usuário selecionar a data de fim.
    # `DateEntry(frame_filtro, date_pattern="dd/MM/yyyy", width=12)` cria o campo
    #       com formato de data brasileiro (dia/mês/ano).
    # `width=12` define a largura do campo de entrada.
    # `grid(row=1, column=3, padx=5, pady=5)` posiciona o campo na
    #       linha 1, coluna 3, ao lado do rótulo.
    date_fim = DateEntry(frame_filtro, date_pattern="dd/MM/yyyy", width=12)

    # Posiciona o campo de entrada de data de fim na interface.
    # `row=1, column=3` define a posição do campo na grade.
    # `padx=5, pady=5` adicionam espaçamento ao redor do campo.
    date_fim.grid(row=1, column=3, padx=5, pady=5)

    # Treeview
    # Cria um frame (container) para a Tabela de Visualização (Treeview).
    # `ttk.Frame(frame_main)` cria um novo frame dentro do frame principal.
    frame_tv = ttk.Frame(frame_main)

    # Posiciona o frame na interface.
    # `fill="both"` permite que o frame expanda tanto na horizontal quanto na vertical.
    # `expand=True` garante que o frame ocupe todo o espaço disponível.
    frame_tv.pack(fill="both", expand=True)

    # Define as colunas da tabela de visualização (Treeview).
    # Cada elemento da tupla representa um nome de coluna que será exibido na tabela.
    colunas = (
        "id",  # Identificador único da reserva.
        "cliente_cpf",  # CPF do cliente associado à reserva.
        "cliente_nome",  # Nome do cliente que realizou a reserva.
        "veiculo_placa",  # Placa do veículo cadastrado na reserva.
        "veiculo_modelo",  # Modelo do veículo cadastrado na reserva.
        "data_entrada",  # Data em que a reserva começou.
        "hora_entrada",  # Hora exata de entrada do veículo.
        "data_saida",  # Data em que a reserva foi finalizada.
        "hora_saida",  # Hora exata de saída do veículo.
        "bloco",  # Bloco onde a vaga reservada está localizada.
        "numero_vaga",  # Número da vaga reservada.
        "status",  # Status da reserva (ex.: "Reservado", "Finalizado", "Cancelado").
        "valor_total"  # Valor total cobrado pela reserva.
    )

    # Cria a Tabela de Visualização (Treeview).
    # `columns=colunas` define as colunas da tabela com base na
    #       tupla de colunas previamente criada.
    # `show="headings"` faz com que apenas os cabeçalhos das colunas
    #       sejam exibidos, sem uma coluna extra à esquerda.
    # `height=20` define a altura da tabela, ou seja, quantas linhas
    #       serão exibidas por vez.
    tv = ttk.Treeview(frame_tv, columns=colunas, show="headings", height=20)

    # Posiciona a tabela na interface gráfica.
    # `fill="both"` permite que a tabela expanda tanto na horizontal
    #       quanto na vertical, ocupando todo o espaço disponível.
    # `expand=True` faz com que a tabela cresça conforme o espaço da interface.
    tv.pack(fill="both", expand=True)

    # Loop para configurar cada coluna definida na tabela.
    for c in colunas:

        # Define o nome do cabeçalho da coluna.
        # `tv.heading(c, text=c.capitalize())` ajusta o texto do cabeçalho da coluna.
        # `c.capitalize()` coloca a primeira letra em maiúscula para melhor apresentação.
        tv.heading(c, text=c.capitalize())

        # Define a largura padrão de cada coluna para 100 pixels.
        # `tv.column(c, width=100)` ajusta a largura inicial da coluna.
        tv.column(c, width=100)

    # Define uma largura menor para a coluna "id", pois contém menos caracteres.
    # `tv.column("id", width=50)` ajusta a largura da coluna "id"
    #       para 50 pixels, economizando espaço.
    tv.column("id", width=50)



    # Define a função `filtrar()` para aplicar filtros e atualizar os dados na tabela.
    def filtrar():

        # Remove todas as linhas atualmente exibidas na tabela antes
        #       de carregar os novos dados.
        # `tv.delete(*tv.get_children())` remove todos os itens da
        #       Treeview antes de inserir os filtrados.
        tv.delete(*tv.get_children())

        # Obtém os valores digitados nos campos de filtro pelo usuário.
        # `entry_cpf.get().strip()` captura e remove espaços extras no início e fim.
        cpf_ = entry_cpf.get().strip()

        # Converte a placa para maiúsculas para padronização.
        # `entry_placa.get().strip().upper()` garante que a placa
        #       seja pesquisada corretamente.
        plac_ = entry_placa.get().strip().upper()

        # Captura o nome do bloco digitado pelo usuário.
        blo_ = entry_bloco.get().strip()

        # Obtém o status selecionado no combobox.
        # `combo_st.get().strip()` remove espaços extras do status selecionado.
        st_ = combo_st.get().strip()

        # Obtém as datas selecionadas nos campos `DateEntry`.
        # `date_ini.get_date()` e `date_fim.get_date()` retornam
        #       valores no formato `datetime.date`.
        di_ = date_ini.get_date()
        df_ = date_fim.get_date()

        # Se o usuário não alterar as datas, o DateEntry
        #       automaticamente define o dia atual.
        # Convertendo as datas para string no formato `dd/mm/yyyy`.
        di_str = di_.strftime("%d/%m/%Y") if di_ else ""
        df_str = df_.strftime("%d/%m/%Y") if df_ else ""

        # Inicializa um dicionário `query` vazio que será
        #       preenchido com os filtros escolhidos.
        query = {}

        # Verifica se o campo CPF foi preenchido pelo usuário.
        # Se `cpf_` não estiver vazio, adiciona um filtro na query.
        # `"cliente_cpf": cpf_` filtra apenas reservas do cliente com esse CPF.
        if cpf_:
            query["cliente_cpf"] = cpf_

        # Verifica se o campo Placa foi preenchido.
        # Se `plac_` não estiver vazio, adiciona um filtro na query.
        # `"veiculo_placa": plac_` filtra apenas reservas do veículo com essa placa.
        if plac_:
            query["veiculo_placa"] = plac_

        # Verifica se o campo Bloco foi preenchido.
        # Se `blo_` não estiver vazio, adiciona um filtro na query.
        # `"bloco": blo_` filtra apenas reservas do bloco específico.
        if blo_:
            query["bloco"] = blo_

        # Verifica se o campo Status foi preenchido.
        # Se `st_` não estiver vazio, adiciona um filtro na query.
        # `"status": st_` filtra apenas reservas com esse status.
        if st_:
            query["status"] = st_

        # Executa a busca na coleção `colecao_reservas` com os filtros aplicados.
        # `list(colecao_reservas.find(query))` retorna todos os
        #       documentos que correspondem aos filtros.
        docs = list(colecao_reservas.find(query))

        # Inicializa a lista `results` para armazenar os registros
        #       finais após a filtragem por data.
        results = []

        # Percorre todos os documentos retornados da
        #       consulta `colecao_reservas.find(query)`.
        for r in docs:

            # Obtém a data de entrada da reserva do dicionário `r`.
            # Se a chave "data_entrada" não existir, retorna uma string vazia `""`.
            dtent = r.get("data_entrada", "")

            try:

                # Tenta converter a string da data de entrada (`dtent`)
                #       para um objeto `datetime`.
                # O formato esperado é `"%d/%m/%Y"` (exemplo: "25/02/2024").
                dtobj = datetime.strptime(dtent, "%d/%m/%Y")

                # Extrai apenas a parte da data (sem horário) para
                #       comparações futuras.
                dtdate = dtobj.date()

            except:

                # Se ocorrer um erro na conversão (formato inválido ou string vazia),
                # define `dtobj` e `dtdate` como `None` para evitar
                #       falhas nas comparações.
                dtobj = None
                dtdate = None

            # Filtro data início/fim
            # Inicializa a variável `ok` como `True`. Se alguma condição de
            #       filtro não for atendida, ela será alterada para `False`.
            ok = True

            # Se a string `di_str` (data de início) não estiver vazia,
            #       converte para `date` e filtra as datas menores.
            if di_str:

                # Converte a string `di_str` para um objeto `date` (`diobj`) no
                #       formato `"%d/%m/%Y"`.
                diobj = datetime.strptime(di_str, "%d/%m/%Y").date()

                # Se `dtdate` (data da reserva) existir e for menor que a
                #       data de início (`diobj`), marca `ok` como `False` para excluir esse registro.
                if dtdate and dtdate < diobj:
                    ok = False

            # Se a string `df_str` (data de fim) não estiver vazia, converte
            #       para `date` e filtra as datas maiores.
            if df_str:

                # Converte a string `df_str` para um objeto `date` (`dfobj`) no formato `"%d/%m/%Y"`.
                dfobj = datetime.strptime(df_str, "%d/%m/%Y").date()

                # Se `dtdate` (data da reserva) existir e for maior que a
                #       data de fim (`dfobj`), marca `ok` como `False` para excluir esse registro.
                if dtdate and dtdate > dfobj:
                    ok = False

            # Se `ok` ainda for `True`, significa que a reserva passou por todos os
            #       filtros e deve ser adicionada à lista `results`.
            if ok:
                results.append(r)

        # Percorre cada item da lista de resultados para processar e
        #       formatar os valores antes da exibição.
        for d in results:

            # Obtém o valor total da reserva a partir do dicionário.
            # `d.get("valor_total", 0)` verifica se existe o campo "valor_total".
            # Caso o campo não exista, assume 0 como valor padrão.
            valor = d.get("valor_total", 0)

            # Verifica se o valor obtido é um número inteiro (int) ou
            #       de ponto flutuante (float).
            # Isso garante que o valor pode ser formatado corretamente.
            if isinstance(valor, (int, float)):

                # Formata o valor para exibição no formato monetário brasileiro.
                # `f"{valor:,.2f}"` formata o número com duas casas decimais e separadores de milhar.
                # `.replace(",", "X").replace(".", ",").replace("X", ".")` ajusta a formatação
                # para seguir o padrão brasileiro (ponto como separador de
                #       milhar e vírgula como decimal).
                valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            else:

                # Caso o valor não seja numérico, define "0,00"
                #       como valor padrão para exibição.
                valor_formatado = "0,00"

            # Insere os dados processados na Treeview (`tv`), que representa a tabela de exibição.
            # O comando `tv.insert("", END, values=(...))` adiciona uma
            #       nova linha ao final da tabela.
            tv.insert("", END, values=(

                # Converte o identificador único (_id) para string
                #       antes de inseri-lo na tabela.
                str(d["_id"]),

                # Obtém e insere o CPF do cliente associado à reserva.
                # Se não houver CPF no documento, insere uma string vazia.
                d.get("cliente_cpf", ""),

                # Obtém e insere o nome do cliente.
                # Se o nome não existir no documento, insere uma string vazia.
                d.get("cliente_nome", ""),

                # Obtém e insere a placa do veículo associado à reserva.
                # Se não houver placa registrada, insere uma string vazia.
                d.get("veiculo_placa", ""),

                # Obtém e insere o modelo do veículo.
                # Se não houver modelo no documento, insere uma string vazia.
                d.get("veiculo_modelo", ""),

                # Obtém e insere a data de entrada da reserva.
                # Se não houver data registrada, insere uma string vazia.
                d.get("data_entrada", ""),

                # Obtém e insere a hora de entrada da reserva.
                # Se não houver hora registrada, insere uma string vazia.
                d.get("hora_entrada", ""),

                # Obtém e insere a data de saída da reserva.
                # Se não houver data de saída registrada, insere uma string vazia.
                d.get("data_saida", ""),

                # Obtém e insere a hora de saída da reserva.
                # Se não houver hora de saída registrada, insere uma string vazia.
                d.get("hora_saida", ""),

                # Obtém e insere o bloco onde a vaga está localizada.
                # Se não houver informação do bloco, insere uma string vazia.
                d.get("bloco", ""),

                # Obtém e insere o número da vaga associada à reserva.
                # Se não houver número de vaga registrado, insere uma string vazia.
                d.get("numero_vaga", ""),

                # Obtém e insere o status atual da reserva.
                # O status pode ser "Reservado", "Finalizado", "Cancelado" ou "Ocupada".
                # Se não houver status registrado, insere uma string vazia.
                d.get("status", ""),

                # Usa a variável `valor_formatado` para inserir o
                #       valor monetário corretamente formatado.
                valor_formatado

            ))


    # Define a função `limpar_`, que é responsável por limpar os
    #       campos de entrada e resetar os filtros.
    def limpar_():

        # Apaga o conteúdo do campo de entrada do CPF.
        entry_cpf.delete(0, END)

        # Apaga o conteúdo do campo de entrada da placa do veículo.
        entry_placa.delete(0, END)

        # Apaga o conteúdo do campo de entrada do bloco.
        entry_bloco.delete(0, END)

        # Reseta a seleção do campo de status para um valor vazio.
        combo_st.set("")

        # Reseta os campos de seleção de data para a data atual.
        date_ini.set_date(datetime.now())  # Define a data inicial como hoje.
        date_fim.set_date(datetime.now())  # Define a data final como hoje.

        # Remove todas as linhas da Treeview (`tv`), limpando
        #       completamente a tabela de exibição.
        tv.delete(*tv.get_children())


    # Define a função `exportar_excel`, que exporta os dados da
    #       tabela (Treeview) para um arquivo Excel.
    def exportar_excel():

        # Cria uma lista vazia para armazenar as linhas da tabela.
        rows = []

        # Percorre todos os itens (linhas) da Treeview.
        for item_id in tv.get_children():

            # Obtém os valores de cada linha.
            rowvals = tv.item(item_id, "values")

            # Adiciona os valores obtidos à lista de linhas.
            rows.append(rowvals)

        # `rows` agora contém todas as linhas da tabela como uma lista de tuplas.
        # Criamos um DataFrame do Pandas usando os dados coletados.
        df = pd.DataFrame(rows, columns=colunas)

        # Exportamos o DataFrame para um arquivo Excel chamado "relatorio.xlsx".
        # O parâmetro `index=False` garante que o Pandas não
        #       inclua uma coluna de índice no Excel.
        df.to_excel("relatorio.xlsx", index=False)

        # Exibe uma mensagem de sucesso informando que o relatório foi exportado.
        # O parâmetro `parent=janela` define que o alerta será
        #       exibido dentro da janela principal.
        messagebox.showinfo("Exportado",
                            "Relatório exportado para relatorio.xlsx",
                            parent=janela)


    # Cria um container (frame) para os botões dentro do frame principal.
    frame_btn = ttk.Frame(frame_main)

    # Adiciona um espaço vertical (pady=5) para melhorar a
    #       disposição dos elementos na tela.
    frame_btn.pack(pady=5)

    # Cria um botão para filtrar os dados com base nos critérios de pesquisa inseridos.
    # `text="Filtrar"` define o rótulo do botão como "Filtrar".
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=filtrar` vincula a ação de filtrar os dados ao pressionar o botão.
    # `side="left"` posiciona o botão à esquerda dentro do frame.
    # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os botões.
    ttk.Button(frame_btn,
               text="Filtrar",
               style="MyButton.TButton",
               command=filtrar).pack(side="left", padx=10)

    # Cria um botão para limpar os campos do formulário e
    #       redefinir os filtros para o estado inicial.
    # `text="Limpar"` define o rótulo do botão como "Limpar".
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=limpar_` vincula a ação de limpar os campos do formulário ao pressionar o botão.
    # `side="left"` posiciona o botão à esquerda dentro do frame.
    # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os botões.
    ttk.Button(frame_btn,
               text="Limpar",
               style="MyButton.TButton",
               command=limpar_).pack(side="left", padx=10)

    # Cria um botão para exportar os dados filtrados para um arquivo Excel.
    # `text="Exportar Excel"` define o rótulo do botão como "Exportar Excel".
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=exportar_excel` vincula a ação de exportação ao pressionar o botão.
    # `side="left"` posiciona o botão à esquerda dentro do frame.
    # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os botões.
    ttk.Button(frame_btn,
               text="Exportar Excel",
               style="MyButton.TButton",
               command=exportar_excel).pack(side="left", padx=10)

    # Ao abrir a tela, já carrega todos os dados disponíveis, sem filtro aplicado.
    # A função `filtrar()` é chamada automaticamente para preencher a tabela.
    filtrar()


# -------------------------------------------------------------------------
# Funções Auxiliares de Layout, Conexão, etc.
# -------------------------------------------------------------------------
def criar_estilo_geral(janela):

    """
    Configura o estilo geral da interface gráfica usando `ttk.Style`.

    Esse método define as cores de fundo e a aparência dos
            widgets `ttk` (como botões, rótulos e entradas).
    Ele também aplica um tema específico para garantir uma aparência mais moderna.

    Parâmetros:
    - janela: a instância principal da janela onde o estilo será aplicado.
    """

    # Define a cor de fundo da janela principal.
    # `#FAFAFA` é um tom de cinza claro, proporcionando um design mais suave.
    janela.configure(background="#FAFAFA")

    # Cria um objeto de estilo para modificar a aparência dos widgets `ttk`.
    # Esse objeto permitirá personalizar cores, fontes e
    #       comportamentos dos componentes da interface.
    style = ttk.Style(janela)

    # Define o tema a ser utilizado na interface.
    # O tema `"clam"` é um dos estilos disponíveis no Tkinter,
    #       proporcionando um visual moderno e consistente.
    style.theme_use("clam")

    # Configura o estilo do widget `TLabel`, que é um rótulo de texto.
    # `background="#FAFAFA"` define a cor de fundo do rótulo como um tom de cinza claro.
    # `foreground="#212121"` define a cor do texto como um tom escuro para contraste.
    # `font=("Arial", 12)` define a fonte usada no rótulo como Arial, tamanho 12.
    style.configure("TLabel",
                    background="#FAFAFA",
                    foreground="#212121",
                    font=("Arial", 12))

    # Configura o estilo do botão personalizado chamado "MyButton.TButton".
    # `background="#3F51B5"` define a cor de fundo do
    #       botão como um tom de azul.
    # `foreground="#FFFFFF"` define a cor do texto do
    #       botão como branco para contraste.
    # `font=("Arial", 12, "bold")` define a fonte do botão
    #       como Arial, tamanho 12 e negrito.
    # `padding=6` adiciona um espaçamento interno de 6 pixels ao
    #       redor do texto dentro do botão.
    style.configure("MyButton.TButton",
                    background="#3F51B5",
                    foreground="#FFFFFF",
                    font=("Arial", 12, "bold"),
                    padding=6)

    # Configura o mapeamento do botão "MyButton.TButton" para
    #       alterar sua aparência quando o usuário interage.
    # `background=[("active", "#303F9F")]` muda a cor de fundo do
    #       botão para um tom mais escuro de azul
    #       quando o botão está pressionado ou o mouse passa sobre ele.
    style.map("MyButton.TButton",
              background=[("active", "#303F9F")])



# -------------------------------------------------------------------------
# Mapa de Vagas (com Scrollbars, Calendar e filtragem por data e bloco)
# -------------------------------------------------------------------------

# Define a função `tela_mapa_reservas()` que cria a
#       interface para o mapa de reservas.
# `janela_pai`: Parâmetro que representa a janela principal da
#       aplicação, que servirá como parent desta janela.
def tela_mapa_reservas(janela_pai):

    # Cria uma nova janela secundária dentro da janela principal.
    # `janela_pai`: Referência à janela principal que abrirá esta nova janela.
    janela = tk.Toplevel(janela_pai)

    # Define o título da janela, exibindo um ícone de
    #       localização seguido do texto "Mapa de Reservas".
    janela.title("📍 Mapa de Reservas")

    # Define o tamanho da janela.
    # `largura = 800`: Define a largura da janela como 800 pixels.
    # `altura = 600`: Define a altura da janela como 600 pixels.
    largura, altura = 800, 600

    # Chama a função `centralizar_janela()` para posicionar a
    #       janela no centro da tela.
    # `janela`: Passa a referência da janela que será centralizada.
    # `largura, altura`: Passa os valores de largura e
    #       altura definidos anteriormente.
    centralizar_janela(janela, largura, altura)

    # Define a cor de fundo da janela como um tom claro de
    #       cinza (`#F5F5F5`), proporcionando um visual limpo e moderno.
    janela.configure(bg="#F5F5F5")

    # Cria um container principal dentro da janela para
    #       organizar os elementos da interface.
    # `tk.Frame(janela)`: Cria um frame dentro da
    #       janela principal para agrupar componentes.
    # `bg="#F5F5F5"`: Define a cor de fundo do frame
    #       como um tom claro de cinza.
    container_principal = tk.Frame(janela, bg="#F5F5F5")

    # Empacota o container dentro da janela, garantindo que
    #       ele ocupe todo o espaço disponível.
    # `expand=True`: Faz com que o container se expanda
    #       para preencher a área disponível.
    # `fill="both"`: Permite que o container seja preenchido
    #       tanto na largura quanto na altura.
    container_principal.pack(expand=True, fill="both")

    # --- Título ---
    # Cria um rótulo (label) que serve como título da tela do mapa de reservas.
    # `ttk.Label(container_principal)`: Cria um rótulo
    #       dentro do container principal.
    # `text="📌 Mapa de Reservas de Vagas"`: Define o texto do
    #       rótulo com um emoji de alfinete e a descrição do mapa.
    # `font=("Arial", 20, "bold")`: Define a fonte do texto
    #       como Arial, tamanho 20, em negrito.
    # `foreground="#2E86C1"`: Define a cor do texto como azul escuro.
    # `background="#F5F5F5"`: Define a cor de fundo do
    #       rótulo para combinar com o container.
    rotulo_titulo = ttk.Label(container_principal,
                              text="📌 Mapa de Reservas de Vagas",
                              font=("Arial", 20, "bold"),
                              foreground="#2E86C1",
                              background="#F5F5F5")

    # Posiciona o rótulo dentro do container principal.
    # `pady=10`: Adiciona um espaçamento vertical de
    #       10 pixels acima e abaixo do rótulo.
    rotulo_titulo.pack(pady=10)

    # --- Filtros ---

    # Cria um container (frame) para armazenar os
    #       filtros de busca no mapa de reservas.
    # `ttk.Frame(container_principal)`: Cria um frame
    #       dentro do container principal da janela.
    container_filtros = ttk.Frame(container_principal)

    # Posiciona o frame na interface.
    # `pady=10`: Adiciona um espaçamento vertical de 10 pixels
    #       entre o frame e os outros elementos.
    container_filtros.pack(pady=10)

    # Cria um rótulo para identificar o campo de seleção do bloco.
    # `text="🏢 Bloco:"` define o texto do rótulo com um ícone de prédio e a palavra "Bloco".
    # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
    # `row=0, column=0` posiciona o rótulo na primeira linha e primeira coluna do grid.
    # `padx=5, pady=5` adiciona espaçamento horizontal e
    #       vertical ao redor do rótulo.
    # `sticky="e"` alinha o rótulo à direita dentro da célula do grid.
    ttk.Label(container_filtros,
              text="🏢 Bloco:",
              font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria uma variável do tipo StringVar para armazenar a
    #       seleção do bloco feita pelo usuário.
    # Essa variável será vinculada ao combobox correspondente,
    #       permitindo armazenar e recuperar a seleção.
    var_bloco = tk.StringVar()

    # Cria um combobox para selecionar um bloco.
    # `container_filtros` define o contêiner onde o combobox será posicionado.
    # `textvariable=var_bloco` vincula o combobox à
    #       variável `var_bloco`, permitindo armazenar a seleção do usuário.
    # `state="readonly"` impede que o usuário digite manualmente no
    #       campo, permitindo apenas selecionar opções predefinidas.
    # `width=20` define a largura do combobox, garantindo espaço
    #       suficiente para exibir os nomes dos blocos.
    combo_bloco = ttk.Combobox(container_filtros,
                               textvariable=var_bloco,
                               state="readonly",
                               width=20)

    # Posiciona o combobox dentro do grid do contêiner de filtros.
    # `row=0, column=1` define a linha e a coluna onde o combobox
    #       será colocado, ficando ao lado do rótulo "Bloco".
    # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao
    #       redor do combobox para melhor organização visual.
    combo_bloco.grid(row=0, column=1, padx=5, pady=5)

    # Carregar blocos disponíveis
    # Obtém todos os documentos da coleção `colecao_blocos`.
    # `find()` retorna um cursor com todos os documentos da coleção.
    documentos_blocos = colecao_blocos.find()

    # Cria uma lista contendo apenas os nomes dos blocos extraídos dos documentos.
    # `doc["nome"]` acessa o campo "nome" de cada documento encontrado na consulta.
    # `sorted(...)` ordena os nomes em ordem alfabética para facilitar a busca pelo usuário.
    lista_blocos = sorted([doc["nome"] for doc in documentos_blocos])

    # Define os valores do combobox `combo_bloco` para
    #       permitir a seleção de blocos.
    # `["Todos"] + lista_blocos` adiciona a opção "Todos" no
    #       início da lista, permitindo visualizar todas as reservas.
    combo_bloco["values"] = ["Todos"] + lista_blocos

    # Define "Todos" como a opção padrão selecionada no
    #       combobox ao abrir a tela.
    combo_bloco.set("Todos")

    # Cria um rótulo (label) para indicar o campo de seleção de data.
    # `text="📅 Data:"` define o texto do rótulo, incluindo um
    #       ícone visual para melhor identificação.
    # `font=("Arial", 12)` define a fonte do texto como Arial, tamanho 12.
    # `.grid(...)` posiciona o rótulo na linha 0, coluna 2 do `container_filtros`.
    # `padx=5, pady=5` adiciona um espaçamento horizontal e vertical de 5 pixels.
    # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
    ttk.Label(container_filtros,
              text="📅 Data:",
              font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Cria um calendário para seleção de data.
    # O calendário pertence ao `container_filtros`,
    #       garantindo uma interface organizada.
    # `date_pattern="dd/MM/yyyy"` define o formato da
    #       data exibida no calendário como dia/mês/ano.
    calendario = Calendar(container_filtros, date_pattern="dd/MM/yyyy")

    # Posiciona o calendário no layout utilizando o grid.
    # `.grid(row=0, column=3)` coloca o calendário na linha 0,
    #       coluna 3 do `container_filtros`.
    # `padx=5, pady=5` adiciona 5 pixels de espaçamento
    #       horizontal e vertical ao redor do calendário.
    calendario.grid(row=0, column=3, padx=5, pady=5)

    # Define a data selecionada no calendário como a data atual.
    # `datetime.now()` pega a data e hora atuais do sistema.
    # `selection_set()` aplica essa data ao calendário para
    #       exibir a data atual como selecionada.
    calendario.selection_set(datetime.now())

    # Cria um container para os botões dentro da interface principal.
    # O container é um `ttk.Frame`, garantindo um layout bem organizado.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels
    #       ao redor do container de botões.
    container_botoes = ttk.Frame(container_principal)
    container_botoes.pack(pady=5)


    # Define a função carregar_mapa
    # Essa função é responsável por carregar os dados do mapa de reservas,
    # limpando os elementos anteriores e aplicando os filtros selecionados.
    def carregar_mapa():

        # Limpa o conteúdo anterior do mapa.
        # `winfo_children()` retorna todos os widgets filhos do frame `frame_mapa`.
        # `widget.destroy()` remove cada widget do frame,
        #       limpando a área para o novo conteúdo.
        for widget in frame_mapa.winfo_children():
            widget.destroy()

        # Pega a data selecionada no calendário.
        # `calendario.get_date()` retorna a data que foi
        #       selecionada no calendário,
        #       no formato especificado (dd/MM/yyyy).
        data_selecionada = calendario.get_date()

        # Pega o bloco selecionado no combobox de blocos.
        # `var_bloco.get()` retorna o valor do bloco selecionado.
        # `.strip()` remove espaços extras do início e fim da string
        #       para garantir que o valor esteja limpo.
        bloco_selecionado = var_bloco.get().strip()

        # Verifica se o valor selecionado para o bloco é "Todos"
        # Se o valor selecionado for "Todos", a consulta ao banco de
        #       dados irá retornar todas as vagas
        #       que não têm o status "Removido". Isso é feito
        #       utilizando a condição `{"status": {"$ne": "Removido"}}`,
        #       onde `$ne` significa "não é igual a". Ou seja, a
        #       consulta vai excluir qualquer vaga com status "Removido".
        if bloco_selecionado == "Todos":

            # Quando "Todos" é selecionado, busca todas as
            #       vagas com status diferente de "Removido".
            vagas = list(colecao_vagas.find({"status": {"$ne": "Removido"}}))

        else:

            # Quando um bloco específico é selecionado, busca
            #       todas as vagas desse bloco específico que
            #       não estão com o status "Removido".
            vagas = list(colecao_vagas.find({"bloco": bloco_selecionado, "status": {"$ne": "Removido"}}))

        # Ordena a lista de vagas primeiro por "bloco" e depois por "numero_vaga"
        # A função `sort()` organiza a lista `vagas` de acordo com o valor do bloco e o número da vaga.
        # A chave de ordenação (key) é definida por uma função `lambda` que retorna uma tupla contendo:
        # - `vaga["bloco"]` para garantir que as vagas serão agrupadas pelo bloco
        # - `int(vaga["numero_vaga"])` para garantir que as vagas sejam ordenadas
        #           numericamente dentro de cada bloco
        # A função `int()` é usada para garantir que o número da
        #       vaga seja tratado como um número inteiro para ordenação correta.
        vagas.sort(key=lambda vaga: (vaga["bloco"], int(vaga["numero_vaga"])))

        # Define o número de colunas por linha para a criação dos botões
        # A variável `colunas_por_linha` determina quantos botões de
        #       vaga serão exibidos em cada linha do mapa.
        # Aqui, estamos especificando que queremos 6 botões de vagas por linha.
        colunas_por_linha = 6

        # Inicializa as variáveis `linha` e `coluna` que serão usadas
        #       para controlar onde cada botão de vaga será colocado
        # O valor inicial de `linha` é 0, indicando que começaremos na primeira linha.
        # O valor inicial de `coluna` é 0, indicando que começaremos na primeira coluna.
        linha = 0
        coluna = 0

        # Itera sobre cada vaga na lista de vagas ordenadas
        # `for vaga in vagas:` começa um loop que vai percorrer
        #       todas as vagas que foram ordenadas na linha anterior
        # Cada elemento de `vagas` será armazenado na variável `vaga` dentro do loop.
        for vaga in vagas:

            # Recupera o valor do campo "bloco" da vaga
            # `bloco = vaga["bloco"]` armazena o nome do bloco da
            #       vaga atual em uma variável chamada `bloco`
            # Isso é feito para utilizar esse valor mais tarde
            #       na consulta à base de dados.
            bloco = vaga["bloco"]

            # Recupera o número da vaga
            # `numero_vaga = vaga["numero_vaga"]` armazena o número da
            #       vaga atual em uma variável chamada `numero_vaga`
            # Esse número será usado na consulta para verificar se a
            #       vaga já está reservada ou ocupada.
            numero_vaga = vaga["numero_vaga"]

            # Busca se há uma reserva para a vaga na data selecionada
            # `colecao_reservas.find_one({...})` executa uma consulta para
            #       verificar se existe uma reserva para a vaga
            # A consulta utiliza os parâmetros:
            # - `"bloco": bloco` para filtrar pelo bloco da vaga.
            # - `"numero_vaga": numero_vaga` para filtrar pelo número da vaga.
            # - `"data_entrada": data_selecionada` para verificar a
            #       reserva na data selecionada.
            # - `"status": {"$in": ["Reservado", "Ocupada"]}` para
            #       garantir que a vaga esteja reservada ou ocupada.
            # Caso uma reserva seja encontrada, ela será armazenada na variável `reserva`.
            reserva = colecao_reservas.find_one({

                "bloco": bloco,  # Filtro pelo bloco
                "numero_vaga": numero_vaga,  # Filtro pelo número da vaga
                "data_entrada": data_selecionada,  # Filtro pela data de entrada
                "status": {"$in": ["Reservado", "Ocupada"]}  # Verifica se a vaga está reservada ou ocupada

            })

            # Verifica se foi encontrada uma reserva para a vaga
            # `if reserva:` verifica se a variável `reserva` contém um
            #       valor (ou seja, se a consulta à base de dados retornou uma reserva).
            # Caso não tenha sido encontrada nenhuma reserva, `reserva`
            #       será `None` e a execução passará para o bloco `else`.
            if reserva:

                # Verifica se o status da reserva é "Ocupada"
                # `if reserva["status"] == "Ocupada":` verifica se o status da
                #       reserva retornada pela consulta é "Ocupada".
                # Caso o status seja "Ocupada", o código define que a vaga está ocupada.
                if reserva["status"] == "Ocupada":

                    # Define o status como "Ocupada"
                    # `status = "Ocupada"` armazena o status "Ocupada" para ser
                    #       usado em outras partes do código, se necessário.
                    status = "Ocupada"

                    # Cria o texto que será exibido na interface com o número do bloco e da vaga
                    # `texto = f"{bloco}-{numero_vaga}\n🟥 Ocupada"` define o texto a
                    #       ser mostrado na interface,
                    # informando o bloco, o número da vaga e o status "Ocupada", além
                    #       de adicionar o emoji correspondente.
                    texto = f"{bloco}-{numero_vaga}\n🟥 Ocupada"

                    # Define a cor de fundo como vermelha
                    # `cor_fundo = "#F44336"` atribui a cor vermelha (HEX: #F44336) à variável `cor_fundo`,
                    # para indicar visualmente que a vaga está ocupada.
                    cor_fundo = "#F44336"  # Vermelho

                else:

                    # Caso o status seja diferente de "Ocupada", verifica se é "Reservada"
                    # Caso o status seja "Reservada", o código define que a vaga está reservada.
                    status = "Reservada"

                    # Cria o texto que será exibido na interface com o
                    #       número do bloco e da vaga
                    # `texto = f"{bloco}-{numero_vaga}\n🟡 Reservada"` define o
                    #       texto a ser mostrado na interface,
                    # informando o bloco, o número da vaga e o status "Reservada",
                    #       além de adicionar o emoji correspondente.
                    texto = f"{bloco}-{numero_vaga}\n🟡 Reservada"

                    # Define a cor de fundo como amarela
                    # `cor_fundo = "#FFC107"` atribui a cor
                    #       amarela (HEX: #FFC107) à variável `cor_fundo`,
                    # para indicar visualmente que a vaga está reservada.
                    cor_fundo = "#FFC107"  # Amarelo

            else:

                # Caso não tenha sido encontrada uma reserva, a vaga está livre
                # `status = "Livre"` define o status como "Livre",
                #       pois não há reserva para a vaga.
                status = "Livre"

                # Cria o texto que será exibido na interface com o
                #       número do bloco e da vaga
                # `texto = f"{bloco}-{numero_vaga}\n🟩 Livre"` define o
                #       texto a ser mostrado na interface,
                # informando o bloco, o número da vaga e o status "Livre",
                #       além de adicionar o emoji correspondente.
                texto = f"{bloco}-{numero_vaga}\n🟩 Livre"

                # Define a cor de fundo como verde
                # `cor_fundo = "#4CAF50"` atribui a cor verde (HEX: #4CAF50) à
                #       variável `cor_fundo`,
                #       para indicar visualmente que a vaga está livre.
                cor_fundo = "#4CAF50"  # Verde

            # Botão da vaga
            # Cria um botão para cada vaga no mapa
            # `botao_vaga = tk.Button(...)` cria um objeto de botão para
            #       representar uma vaga no mapa.

            # `frame_mapa` é o contêiner onde o botão será exibido.
            # `text=texto` define o texto que aparecerá no botão. O `texto` é gerado na
            #       parte anterior do código, dependendo do status da
            #       vaga (livre, reservada, ocupada).
            # `width=12` define a largura do botão em termos de caracteres. Ajusta a
            #       largura do botão para que o texto caiba de forma confortável.
            # `height=3` define a altura do botão, garantindo que o botão tenha uma
            #       área adequada para visualização.
            # `bg=cor_fundo` define a cor de fundo do botão. A cor de fundo (`cor_fundo`) muda
            #       dependendo do status da vaga: vermelho para ocupada, amarelo para
            #       reservada e verde para livre.
            # `fg="white"` define a cor do texto dentro do botão como branca, para
            #       garantir boa visibilidade sobre o fundo colorido.
            # `font=("Arial", 10, "bold")` define a fonte do texto como Arial, com
            #       tamanho 10 e em negrito. Isso dá um visual mais chamativo ao texto.
            # `relief="raised"` define o estilo de relevo do botão, o que cria uma
            #       aparência de botão "pressionado" ou "em alto", adicionando
            #       profundidade ao botão.
            # `borderwidth=2` define a largura da borda do botão. Um valor maior
            #       pode tornar a borda mais visível.
            # `padx=5` e `pady=5` adicionam preenchimento dentro do botão. `padx`
            #       adiciona espaçamento horizontal e `pady` adiciona espaçamento vertical,
            #       ajudando a ajustar o tamanho e a aparência do botão.
            # `highlightbackground="#D1D1D1"` define a cor de fundo do botão quando ele
            #       não está em foco. Isso garante que o botão tenha uma aparência
            #       consistente quando não está ativo.
            # `activebackground="#616161"` define a cor de fundo do botão quando ele é
            #       pressionado ou ativado. Isso cria um feedback visual para o
            #       usuário ao clicar no botão.
            botao_vaga = tk.Button(frame_mapa,
                                   text=texto,
                                   width=12,
                                   height=3,
                                   bg=cor_fundo,
                                   fg="white",
                                   font=("Arial", 10, "bold"),
                                   relief="raised",
                                   borderwidth=2,
                                   padx=5,
                                   pady=5,
                                   highlightbackground="#D1D1D1",
                                   activebackground="#616161")

            # Define a função `acao_vaga` com dois parâmetros: `bloco_vaga` e `num_vaga`.
            # `bloco_vaga` e `num_vaga` recebem valores padrões (valores de `bloco` e
            #       `numero_vaga` do código anterior) para quando a função for
            #       chamada sem argumentos explícitos.
            # A função chama outra função chamada `popup_acoes_vaga_mapa`
            #       passando os parâmetros necessários, que abre uma
            #       janela de ações para a vaga específica.
            def acao_vaga(bloco_vaga=bloco, num_vaga=numero_vaga):

                # Chama a função popup_acoes_vaga_mapa para exibir uma tela de ações
                #       relacionadas à vaga específica.
                # `janela` é a janela principal do aplicativo, `bloco_vaga` e
                #       `num_vaga` são os dados da vaga.
                # `data_selecionada` é a data que foi escolhida pelo usuário.
                # `carregar_mapa` é uma função que recarrega o mapa após
                #       uma ação ser realizada (como uma reserva, por exemplo).
                popup_acoes_vaga_mapa(janela, bloco_vaga, num_vaga, data_selecionada, carregar_mapa)

            # Configura o botão `botao_vaga` para chamar a função `acao_vaga`
            #       quando for clicado.
            # Isso faz com que o comportamento do botão seja definido de acordo
            #       com a função `acao_vaga` para abrir o popup de ações para a vaga.
            botao_vaga.configure(command=acao_vaga)

            # Coloca o botão na grid (tabela) na posição específica, definida
            #       pelas variáveis `linha` e `coluna`.
            # `padx=8` e `pady=8` adicionam espaçamento interno ao redor do botão na
            #       grid, garantindo que o botão não fique colado nas bordas.
            botao_vaga.grid(row=linha, column=coluna, padx=8, pady=8)

            # Incrementa a variável `coluna` em 1 para passar para a
            #       próxima coluna na grid.
            # Isso permite que os botões de vagas sejam colocados em
            #       colunas sucessivas da grid.
            coluna += 1

            # Verifica se o número de colunas já atingiu o limite definido
            #       em `colunas_por_linha`.
            # Se `coluna` for maior ou igual a `colunas_por_linha`, significa
            #       que a linha atual está cheia e é necessário passar para a próxima linha.
            # Nesse caso, `coluna` é resetada para 0, para começar uma nova linha.
            if coluna >= colunas_por_linha:

                # Reseta a coluna para 0, começando a nova linha.
                coluna = 0

                # Incrementa a variável `linha` para passar para a
                #       próxima linha da grid.
                linha += 1

        # Atualiza a interface de tarefas pendentes no canvas.
        # `canvas_mapa.update_idletasks()` força a atualização do
        #       canvas, aplicando quaisquer mudanças ou alterações
        #       feitas na interface.
        # Isso garante que o canvas seja atualizado para refletir
        #       corretamente a posição de seus elementos antes de
        #       qualquer outra operação.
        canvas_mapa.update_idletasks()

        # Atualiza a região de rolagem do canvas para que a área
        #       de rolagem cubra todos os elementos desenhados.
        # `canvas_mapa.bbox("all")` retorna as coordenadas (caixa delimitadora) de
        #       todos os itens desenhados no canvas.
        # `canvas_mapa.configure(scrollregion=...)` ajusta a região de rolagem do
        #       canvas para cobrir a área necessária para exibir todos os elementos.
        canvas_mapa.configure(scrollregion=canvas_mapa.bbox("all"))


    # Botões de ações
    # Cria uma lista de tuplas, onde cada tupla contém o texto e o comando do botão
    # Cada tupla representa um botão que será exibido na interface.
    # Os botões são: "📌 Atualizar Mapa" com a função `carregar_mapa` e
    #       "❌ Fechar" com a função `janela.destroy`.
    botoes = [
        ("📌 Atualizar Mapa", carregar_mapa),
        ("❌ Fechar", janela.destroy)
    ]

    # Itera sobre cada item na lista de botões (tupla), criando os
    #       botões de forma dinâmica.
    # `enumerate(botoes)` retorna o índice (i) e os valores das
    #       tuplas (texto e comando) para cada botão.
    # `texto` é o rótulo a ser exibido no botão e `comando` é a
    #       função a ser chamada quando o botão for pressionado.
    for i, (texto, comando) in enumerate(botoes):

        # Cria o botão com o texto definido pela variável `texto` e a
        #       ação associada ao `comando`.
        # `width=18` define a largura do botão em termos de número de caracteres.
        # `command=comando` associa a função que será chamada ao pressionar o botão.
        # `row=0, column=i` posiciona os botões na linha 0, nas
        #       colunas de acordo com o índice (i).
        # `padx=10, pady=5` adiciona espaçamento horizontal e
        #       vertical ao redor de cada botão.
        ttk.Button(container_botoes,
                   text=texto,
                   command=comando,
                   width=18).grid(row=0, column=i, padx=10, pady=5)

    # --- Mapa de Vagas ---

    # Cria um container principal para o mapa.
    # `container_mapa` é um Frame do ttk, usado para
    #       agrupar o Canvas dentro da interface.
    # `container_principal` é o container pai
    #       onde o mapa será adicionado.
    container_mapa = ttk.Frame(container_principal)

    # Adiciona o `container_mapa` ao layout da janela.
    # `expand=True` faz com que o container ocupe
    #       todo o espaço disponível dentro de seu pai.
    # `fill="both"` faz com que o container preencha
    #       tanto horizontal quanto verticalmente.
    container_mapa.pack(expand=True, fill="both")

    # Cria um Canvas dentro do `container_mapa` para desenhar o mapa.
    # O Canvas é um widget que permite desenhar
    #       gráficos e elementos interativos.
    # O parâmetro `background="#FAFAFA"` define a cor
    #       de fundo do Canvas como cinza claro.
    canvas_mapa = tk.Canvas(container_mapa, background="#FAFAFA")

    # Posiciona o Canvas dentro do `container_mapa`.
    # `side="left"` define que o Canvas ficará ancorado à esquerda do container.
    # `fill="both"` faz o Canvas preencher toda a largura e altura do container.
    # `expand=True` permite que o Canvas se expanda para ocupar o espaço restante.
    canvas_mapa.pack(side="left", fill="both", expand=True)

    # Cria uma barra de rolagem vertical (`yview`) para o Canvas.
    # `container_mapa` é o contêiner onde o Canvas está, e a
    #       barra de rolagem será posicionada à direita.
    # `orient="vertical"` define a orientação da
    #       barra de rolagem como vertical.
    # `command=canvas_mapa.yview` associa a barra de rolagem à
    #       visualização vertical do Canvas, permitindo rolar o conteúdo na direção Y.
    barra_rolagem_y = ttk.Scrollbar(container_mapa,
                                    orient="vertical",
                                    command=canvas_mapa.yview)

    # Posiciona a barra de rolagem vertical à direita do `container_mapa`.
    # `side="right"` faz com que a barra de rolagem fique no
    #       lado direito do Canvas.
    # `fill="y"` faz com que a barra de rolagem preencha toda a
    #       altura do `container_mapa`, permitindo rolar o conteúdo verticalmente.
    barra_rolagem_y.pack(side="right", fill="y")

    # Cria uma barra de rolagem horizontal (`xview`) para o Canvas.
    # `container_principal` é o contêiner pai onde o Canvas está.
    # A barra de rolagem será posicionada na parte inferior.
    # `orient="horizontal"` define a orientação da barra de
    #       rolagem como horizontal.
    # `command=canvas_mapa.xview` associa a barra de rolagem à
    #       visualização horizontal do Canvas, permitindo rolar o
    #       conteúdo na direção X.
    barra_rolagem_x = ttk.Scrollbar(container_principal,
                                    orient="horizontal",
                                    command=canvas_mapa.xview)

    # Posiciona a barra de rolagem horizontal na parte inferior do `container_principal`.
    # `side="bottom"` faz com que a barra de rolagem fique na
    #       parte inferior do Canvas.
    # `fill="x"` faz com que a barra de rolagem preencha toda a
    # largura do `container_principal`, permitindo rolar o
    # conteúdo horizontalmente.
    barra_rolagem_x.pack(side="bottom", fill="x")

    # Associa a funcionalidade de rolagem horizontal e vertical ao canvas_mapa.
    # `xscrollcommand=barra_rolagem_x.set` vincula a barra de rolagem
    #       horizontal (`barra_rolagem_x`) à rolagem horizontal do canvas.
    # `yscrollcommand=barra_rolagem_y.set` vincula a barra de
    #       rolagem vertical (`barra_rolagem_y`) à rolagem vertical do canvas.
    # Isso permite que as barras de rolagem se movam conforme o
    #       conteúdo do canvas é rolado e vice-versa.
    canvas_mapa.configure(xscrollcommand=barra_rolagem_x.set,
                          yscrollcommand=barra_rolagem_y.set)

    # Cria um frame dentro do canvas_mapa para adicionar o conteúdo do mapa.
    # `ttk.Frame(canvas_mapa)` cria o frame dentro do canvas.
    # O frame será usado para armazenar o conteúdo que
    #       será exibido dentro do canvas.
    frame_mapa = ttk.Frame(canvas_mapa)

    # Cria uma janela dentro do canvas que pode conter o `frame_mapa`.
    # `create_window` cria uma janela no canvas no ponto especificado
    #       por `(0, 0)`, no canto superior esquerdo.
    # `window=frame_mapa` indica que o `frame_mapa` será o
    #       conteúdo dessa janela.
    # `anchor="nw"` significa que a posição `(0, 0)` é o **canto
    #       superior esquerdo** da janela dentro do canvas.
    canvas_mapa.create_window((0, 0),
                              window=frame_mapa,
                              anchor="nw")


    # Define a função ajustar_tamanho_mapa, que será chamada
    #       sempre que o tamanho do frame_mapa mudar.
    # A função usa o evento de configuração para
    #       atualizar o "scrollregion" do canvas_mapa,
    #       o que garante que as barras de rolagem cubram
    #       todo o conteúdo visível no canvas.
    def ajustar_tamanho_mapa(event):

        # Atualiza a região de rolagem do canvas_mapa para
        #       cobrir toda a área do conteúdo.
        # `canvas_mapa.bbox("all")` retorna as coordenadas de
        #       bounding box de todos os itens no canvas.
        # O `scrollregion` do canvas é configurado para essas
        #       coordenadas para garantir que as barras de rolagem
        #       cubram todo o conteúdo, mesmo quando o conteúdo se expandir.
        canvas_mapa.configure(scrollregion=canvas_mapa.bbox("all"))


    # Vincula a função ajustar_tamanho_mapa ao evento de
    #       configuração (`<Configure>`) do frame_mapa.
    # O evento `<Configure>` é disparado sempre que o
    #       frame_mapa é redimensionado.
    # Assim, sempre que o tamanho do frame_mapa mudar, a
    #       função ajustar_tamanho_mapa será chamada
    #       para ajustar a região de rolagem do canvas_mapa.
    frame_mapa.bind("<Configure>", ajustar_tamanho_mapa)

    # Chama a função carregar_mapa para carregar o mapa
    #       automaticamente quando a janela for aberta.
    # Isso garante que o mapa seja exibido corretamente
    #       logo que a interface for carregada.
    carregar_mapa()


# -------------------------------------------------------------------------
# Popup para mostrar Ações ao clicar na vaga
# -------------------------------------------------------------------------

# Define a função `popup_acoes_vaga_mapa` que cria uma janela pop-up
#       para ações relacionadas a uma vaga de estacionamento.
# `parent` é a janela principal (janela que chamou esse pop-up), `bloco` é
#       o bloco da vaga, `num_vaga` é o número da vaga,
# `data_sel` é a data selecionada para a vaga e `callback_recarregar` é
#       uma função que será chamada após alguma ação.
def popup_acoes_vaga_mapa(parent, bloco, num_vaga, data_sel, callback_recarregar):

    """
    Função responsável por criar e exibir um pop-up com as ações
                disponíveis para uma vaga de estacionamento.

    Parâmetros:
    - parent (Tk): Janela principal ou pai do pop-up.
    - bloco (str): Identificação do bloco onde a vaga está localizada.
    - num_vaga (int): Número da vaga dentro do bloco.
    - data_sel (str): Data específica para a qual a vaga está sendo consultada (formato "YYYY-MM-DD").
    - callback_recarregar (function): Função que será chamada para atualizar a interface após alguma ação.
    """

    # 🔹 Criação da janela pop-up (Toplevel)
    # `Toplevel(parent)` cria uma nova janela independente, associada à janela principal (`parent`).
    # Esse tipo de janela permite que o usuário continue interagindo com a interface
    #           principal enquanto o pop-up está aberto.
    top = Toplevel(parent)

    # 🔹 Define o título da janela pop-up
    # O título inclui o bloco e o número da vaga para que o usuário saiba exatamente
    #           qual vaga está sendo gerenciada.
    top.title(f"Ações - Vaga {bloco}-{num_vaga}")

    # 🔹 Centraliza a janela pop-up na tela
    # A função `centralizar_janela(top, 400, 300)` ajusta a posição do pop-up
    #           para que ele fique centralizado na tela.
    # Os valores `400, 300` representam a largura e altura da janela em pixels.
    centralizar_janela(top, 400, 300)

    # 🔹 Aplica um estilo geral à janela pop-up
    # `criar_estilo_geral(top)` define a aparência da janela, como cores, fontes e estilos visuais.
    # Isso garante que o pop-up siga o padrão visual do sistema.
    criar_estilo_geral(top)

    # 🔹 Criação do frame principal dentro do pop-up
    # `ttk.Frame(top)` cria um container dentro da janela pop-up (`top`).
    # Esse frame será responsável por conter e organizar os
    #        elementos visuais dentro do pop-up.
    frame_main = ttk.Frame(top)

    # 🔹 Posicionamento do frame principal dentro da janela pop-up
    # `.pack(fill="both", expand=True, padx=10, pady=10)`
    # - `fill="both"` permite que o frame se expanda tanto horizontal
    #        quanto verticalmente.
    # - `expand=True` faz com que o frame ocupe todo o espaço
    #        disponível dentro da janela pop-up.
    # - `padx=10, pady=10` adiciona um espaçamento de 10 pixels ao
    #        redor do frame para não ficar colado nas bordas.
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # 🔹 Criação de um rótulo informativo dentro do frame principal
    # `ttk.Label(frame_main, text=f"Vaga: {bloco}-{num_vaga}\nData: {data_sel}", ...)`
    # - Exibe o texto informando qual vaga está sendo gerenciada e a data da consulta.
    # - O texto utiliza interpolação (`f"..."`) para incluir
    #        dinamicamente o bloco, o número da vaga e a data.
    lbl_info = ttk.Label(
        frame_main,  # O rótulo será inserido dentro do frame principal (`frame_main`).
        text=f"Vaga: {bloco}-{num_vaga}\nData: {data_sel}",  # Texto informativo exibindo os detalhes da vaga.
        font=("Arial", 14, "bold"),  # Define a fonte como Arial, tamanho 14 e em negrito (bold) para destaque.
        foreground="#3F51B5"  # Define a cor do texto como azul escuro (#3F51B5) para um design elegante.
    )

    # 🔹 Exibição do rótulo na interface
    # `.pack(pady=10)` posiciona o rótulo dentro do frame com um
    #        espaçamento vertical de 10 pixels.
    # Isso cria um espaço entre o rótulo e os outros elementos da
    #        interface, melhorando a legibilidade.
    lbl_info.pack(pady=10)

    # 🔹 Tentativa de conversão da data para o formato correto
    try:

        # O método `strptime()` do módulo `datetime` converte a string `data_sel`
        #            de um formato específico ("YYYY-MM-DD") para um objeto de data.
        # - "%Y-%m-%d" representa o formato original da data (exemplo: "2024-03-06").
        # - `strftime("%d/%m/%Y")` converte a data para o formato brasileiro (exemplo: "06/03/2024").
        data_formatada = datetime.strptime(data_sel, "%Y-%m-%d").strftime("%d/%m/%Y")

    # 🔹 Captura um erro caso a data informada não esteja no formato esperado
    except ValueError:

        # Se a conversão falhar, mantém `data_formatada` com o valor original de `data_sel`.
        # Isso evita que o código quebre caso a data já esteja no formato correto ou inválido.
        data_formatada = data_sel

    # 🔹 Buscar no banco de dados apenas as reservas para a data específica
    # A função `find_one()` do MongoDB retorna o primeiro documento que satisfaz os critérios especificados.
    reserva_existente = colecao_reservas.find_one({
        "bloco": bloco,  # Filtra pelo bloco onde a vaga está localizada.
        "numero_vaga": num_vaga,  # Filtra pelo número da vaga dentro do bloco.
        "data_entrada": data_formatada,  # Filtra pela data formatada corretamente.
        "status": {"$in": ["Reservado", "Ocupada"]}
        # Filtra apenas reservas que estejam em status "Reservado" ou "Ocupada".
    })

    # 🔹 Se houver uma reserva para a data, define o status como "Reservado" ou "Ocupada"
    if reserva_existente:

        # Se a busca no banco de dados (`reserva_existente`) retornou um documento válido,
        # significa que a vaga está ocupada ou reservada na data específica.
        # O status será então definido com base no campo `"status"` do documento encontrado.
        status_vaga = reserva_existente["status"]

    else:

        # Se `reserva_existente` for `None`, significa que **não há reserva** para a data informada.
        # Nesse caso, definimos o status como `"Livre"`, indicando que a vaga pode ser utilizada.
        status_vaga = "Livre"

    # 🔹 Criação do frame que conterá os botões de ação
    # Esse frame (`frame_btn`) será usado para posicionar botões dinamicamente
    # de acordo com o status da vaga (por exemplo, um botão para reservar, ver detalhes, etc.).
    frame_btn = ttk.Frame(frame_main)

    # 🔹 Posicionamento do frame na interface
    # `pady=10` adiciona um espaçamento vertical de 10 pixels abaixo do frame.
    frame_btn.pack(pady=10)

    # 🔹 Exibição do status da vaga na interface gráfica
    # Criamos um rótulo (`Label`) para exibir o status atualizado da vaga.
    ttk.Label(

        # O rótulo será inserido dentro do `frame_main`.
        frame_main,

        # O texto exibido incluirá o status real da vaga.
        text=f"Status: {status_vaga}",

        # Define a fonte como Arial, tamanho 12, e negrito para destacar o status.
        font=("Arial", 12, "bold")

    ).pack()

    # 🔹 Se a vaga está reservada na data, exibir botão para ver detalhes
    if status_vaga == "Reservado":

        # Define uma função interna `ver_detalhes_reserva()` que será chamada ao clicar no botão.
        def ver_detalhes_reserva():

            # Fecha a janela atual (`top`) antes de abrir os detalhes da reserva.
            top.destroy()

            # Chama a função `popup_detalhes_reserva()` para abrir um novo pop-up
            # com mais informações sobre a reserva selecionada.
            # - `parent`: Passa a janela principal para o novo pop-up.
            # - `reserva_existente["_id"]`: Passa o identificador único da reserva.
            # - `callback_recarregar`: Função de recarregamento da interface para atualização dos dados.
            popup_detalhes_reserva(parent, reserva_existente["_id"], callback_recarregar)

        # 🔹 Criação do botão "Ver Detalhes"
        # - Esse botão será exibido **somente se a vaga estiver reservada na data selecionada**.
        # - `frame_btn`: O botão será adicionado dentro do frame de botões.
        # - `text="Ver Detalhes"`: Define o texto exibido no botão.
        # - `style="MyButton.TButton"`: Aplica um estilo customizado ao botão para manter o design padronizado.
        # - `command=ver_detalhes_reserva`: Define a função a ser executada quando o botão for clicado.
        # - `.pack(side="left", padx=5)`: Posiciona o botão à esquerda e adiciona um
        #           espaçamento horizontal de 5 pixels.
        ttk.Button(frame_btn,
                   text="Ver Detalhes",
                   style="MyButton.TButton",
                   command=ver_detalhes_reserva).pack(side="left", padx=5)

    # 🔹 Se a vaga está livre na data, permitir reserva
    elif status_vaga == "Livre":

        # Define uma função interna `reservar()` que será chamada ao clicar no botão.
        def reservar():

            # Chama a função `popup_reservar()` para abrir um novo pop-up
            # onde o usuário poderá concluir a reserva da vaga.
            # - `top`: Passa a janela atual como referência para o novo pop-up.
            # - `bloco`: Passa o bloco da vaga a ser reservada.
            # - `num_vaga`: Passa o número da vaga a ser reservada.
            # - `data_sel`: Passa a data específica para a reserva.
            # - `callback_recarregar`: Função de recarregamento para atualizar os dados após a reserva.
            popup_reservar(top, bloco, num_vaga, data_sel, callback_recarregar)

        # 🔹 Criação do botão "Reservar"
        # - Esse botão será exibido **somente se a vaga estiver livre na data selecionada**.
        # - `frame_btn`: O botão será adicionado dentro do frame de botões.
        # - `text="Reservar"`: Define o texto exibido no botão.
        # - `style="MyButton.TButton"`: Aplica um estilo customizado ao botão para manter o design padronizado.
        # - `command=reservar`: Define a função a ser executada quando o botão for clicado.
        # - `.pack(side="left", padx=5)`: Posiciona o botão à esquerda e adiciona um espaçamento
        #           horizontal de 5 pixels.
        ttk.Button(frame_btn,
                   text="Reservar",
                   style="MyButton.TButton",
                   command=reservar).pack(side="left", padx=5)

    # 🔹 Criação do botão "Fechar"
    ttk.Button(

        # O botão será adicionado dentro do frame principal (`frame_main`).
        frame_main,

        # Define o texto do botão como "Fechar".
        text="Fechar",

        # Aplica um estilo personalizado chamado "MyButton.TButton".
        style="MyButton.TButton",

        # Define a ação do botão: ao ser pressionado, a janela `top` será fechada.
        command=top.destroy

    ).pack(pady=10)  # Adiciona um espaçamento vertical (10 pixels) abaixo do botão.



# -------------------------------------------------------------------------
# Popup de Detalhes da Reserva (se vaga estava "Reservada")
# -------------------------------------------------------------------------

# Cria uma nova janela de pop-up para exibir os detalhes da reserva.
# Define a função e recebe os parâmetros necessários.
def popup_detalhes_reserva(parent, reserva_id, callback_recarregar):

    # `Toplevel(parent)` cria uma janela filha dentro da janela principal.
    top = Toplevel(parent)

    # Define o título da janela.
    # `title("Detalhes da Reserva")` exibe o texto no topo da janela.
    top.title("Detalhes da Reserva")

    # Centraliza a janela na tela com tamanho definido.
    # `centralizar_janela(top, 500, 400)` ajusta a posição e
    #       tamanho da janela para 500x400 pixels.
    centralizar_janela(top, 500, 400)

    # Aplica o estilo visual da interface à nova janela.
    # `criar_estilo_geral(top)` configura fontes, cores e outros estilos visuais.
    criar_estilo_geral(top)

    # Cria um contêiner principal dentro da janela para organizar os elementos.
    # `ttk.Frame(top)` cria um frame dentro da janela `top`.
    frame_main = ttk.Frame(top)

    # Expande o frame para preencher toda a área disponível.
    # `fill="both"` permite que o frame ocupe toda a área disponível
    #       horizontal e verticalmente.
    # `expand=True` faz com que o frame cresça automaticamente
    #       conforme o tamanho da janela.
    # `padx=10, pady=10` adiciona espaçamento interno para
    #       melhor organização dos elementos.
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Busca no banco de dados o documento da reserva correspondente ao ID fornecido.
    # Retorna o documento ou `None` se não encontrado.
    doc_r = colecao_reservas.find_one({"_id": ObjectId(reserva_id)})

    # Verifica se a reserva foi encontrada no banco de dados.
    if not doc_r:

        # Cria um rótulo (`Label`) para exibir a mensagem de erro caso a reserva não exista.
        # `text="Reserva não encontrada!"` define o texto que será exibido na tela.
        # `foreground="red"` define a cor do texto como vermelho para indicar um erro.
        # `pady=20` adiciona um espaçamento vertical para separar o rótulo dos outros elementos.
        ttk.Label(frame_main,
                  text="Reserva não encontrada!",
                  foreground="red").pack(pady=20)

        # Retorna imediatamente para evitar que a função continue a
        #       execução, pois não há dados para exibir.
        return

    # Exibe dados
    # Cria um rótulo para exibir o título da seção de detalhes da reserva.
    # `text="DETALHES DA RESERVA"` define o texto exibido no rótulo.
    # `font=("Arial",14,"bold")` define a fonte Arial, tamanho 14, em negrito.
    # `foreground="#3F51B5"` define a cor do texto como azul escuro.
    lbl_t = ttk.Label(frame_main,
                      text="DETALHES DA RESERVA",
                      font=("Arial", 14, "bold"),
                      foreground="#3F51B5")

    # Exibe o rótulo na tela.
    # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do rótulo.
    lbl_t.pack(pady=10)

    # Monta um texto formatado com as informações detalhadas da reserva.
    # `f"Cliente: {doc_r.get('cliente_nome','')} (CPF: {doc_r.get('cliente_cpf','')})\n"`
    # → Exibe o nome do cliente e seu CPF.
    # `f"Veículo: {doc_r.get('veiculo_modelo','')} (Placa: {doc_r.get('veiculo_placa','')})\n"`
    # → Exibe o modelo do veículo e sua placa.
    # `f"Data Entrada: {doc_r.get('data_entrada','')}   Hora Entrada: {doc_r.get('hora_entrada','')}\n"`
    # → Exibe a data e hora de entrada da reserva.
    # `f"Data Saída: {doc_r.get('data_saida','-')}   Hora Saída: {doc_r.get('hora_saida','-')}\n"`
    # → Exibe a data e hora de saída (se houver).
    # `f"Bloco: {doc_r.get('bloco','')}   Vaga: {doc_r.get('numero_vaga','')}\n"`
    # → Exibe o bloco e número da vaga reservada.
    # `f"Status: {doc_r.get('status','')}"` → Exibe o status atual da reserva.
    info_txt = (
        f"Cliente: {doc_r.get('cliente_nome', '')} (CPF: {doc_r.get('cliente_cpf', '')})\n"
        f"Veículo: {doc_r.get('veiculo_modelo', '')} (Placa: {doc_r.get('veiculo_placa', '')})\n"
        f"Data Entrada: {doc_r.get('data_entrada', '')}   Hora Entrada: {doc_r.get('hora_entrada', '')}\n"
        f"Data Saída: {doc_r.get('data_saida', '-')}   Hora Saída: {doc_r.get('hora_saida', '-')}\n"
        f"Bloco: {doc_r.get('bloco', '')}   Vaga: {doc_r.get('numero_vaga', '')}\n"
        f"Status: {doc_r.get('status', '')}"
    )

    # Cria um rótulo (`Label`) para exibir as informações da reserva na interface.
    # `text=info_txt` → Define o texto do rótulo como a variável `info_txt`
    #       contendo os detalhes da reserva.
    # `justify="left"` → Alinha o texto à esquerda para facilitar a leitura.
    lbl_d = ttk.Label(frame_main, text=info_txt, justify="left")

    # Adiciona o rótulo à interface com um espaçamento vertical de 5 pixels.
    lbl_d.pack(pady=5)

    # Cria um container (`Frame`) para organizar os botões na interface.
    frame_botoes = ttk.Frame(frame_main)

    # Adiciona o frame na interface com um espaçamento vertical
    #       de 20 pixels para separar dos outros elementos.
    frame_botoes.pack(pady=20)


    # Botão Cancelar
    # Define a função para cancelar a reserva.
    def cancelar_reserva():

        # Remove a reserva do banco de dados.
        # `delete_many({"_id": ObjectId(reserva_id)})` → Exclui qualquer
        #       documento da coleção `colecao_reservas` que tenha o ID correspondente.
        colecao_reservas.delete_many({"_id": ObjectId(reserva_id)})

        # Atualiza o status da vaga no banco de dados para "Livre".
        # → Busca a vaga pelo bloco e número da vaga e define seu status como "Livre".
        colecao_vagas.update_one({"bloco": doc_r["bloco"],
                                  "numero_vaga": doc_r["numero_vaga"]},
                                 {"$set": {"status": "Livre"}})

        # Exibe uma mensagem de confirmação informando que a reserva foi cancelada.
        # `messagebox.showinfo("OK", "Reserva cancelada!", parent=top)`
        # → Mostra uma caixa de diálogo informando o sucesso da operação.
        messagebox.showinfo("OK", "Reserva cancelada!", parent=top)

        # Fecha a janela de detalhes da reserva após o cancelamento.
        # `top.destroy()` → Fecha a janela pop-up atual.
        top.destroy()

        # Chama a função de recarregar o mapa de reservas para
        #       atualizar a interface com os novos dados.
        # `callback_recarregar()` → Atualiza a interface
        #       para refletir as mudanças.
        callback_recarregar()


    # Cria um botão para cancelar a reserva.
    # `text="Cancelar Reserva"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=cancelar_reserva` associa a ação de cancelar a
    #       reserva ao clicar no botão.
    # `pack(side="left", padx=10)` posiciona o botão no lado esquerdo do
    #       frame com espaçamento horizontal de 10 pixels.
    ttk.Button(frame_botoes,
               text="Cancelar Reserva",
               style="MyButton.TButton",
               command=cancelar_reserva).pack(side="left", padx=10)


    # Define a função para finalizar a reserva.
    def finalizar_reserva():

        # Comentário explicativo: Ao finalizar a reserva, a vaga
        #       pode ser marcada como "Ocupada" ou já como "Paga".
        # Isso depende do fluxo da aplicação. Neste caso, vamos
        #       pedir a data/hora de saída para calcular o valor.

        # Fecha a janela atual antes de abrir a próxima tela
        #       para finalizar a reserva.
        top.destroy()

        # Chama a função que abrirá a tela de finalização da reserva.
        # `popup_finalizar_reserva(parent, reserva_id, callback_recarregar)`:
        # - `parent`: Janela principal da aplicação.
        # - `reserva_id`: ID da reserva que será finalizada.
        # - `callback_recarregar`: Função para atualizar a interface
        #       após finalizar a reserva.
        popup_finalizar_reserva(parent, reserva_id, callback_recarregar)

    # Cria um botão para finalizar a reserva, ocupando a vaga ou processando o pagamento.
    # `text="Finalizar (Ocupar/Pagar)"` define o rótulo do botão.
    # `style="MyButton.TButton"` aplica um estilo customizado ao botão.
    # `command=finalizar_reserva` associa a função `finalizar_reserva` ao
    #       botão, que abre a tela de finalização.
    # `.pack(side="left", padx=10)` posiciona o botão à esquerda dentro do
    #       frame e adiciona espaçamento lateral de 10 pixels.
    ttk.Button(frame_botoes,
               text="Finalizar (Ocupar/Pagar)",
               style="MyButton.TButton",
               command=finalizar_reserva).pack(side="left", padx=10)

    # Cria um botão para fechar a janela.
    # `text="Fechar"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=top.destroy` associa a ação de fechar a janela ao botão.
    # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
    ttk.Button(frame_main,
               text="Fechar",
               style="MyButton.TButton",
               command=top.destroy).pack(pady=10)


# -------------------------------------------------------------------------
# Popup para Finalizar Reserva - pede data/hora de saída
# -------------------------------------------------------------------------

# Define a função para exibir o popup de finalização de reserva.
# Essa função cria uma janela para que o usuário insira a
#       data e a hora de saída de uma reserva existente.
def popup_finalizar_reserva(parent, reserva_id, callback_recarregar):

    # Cria uma nova janela (subjanela) dentro da janela principal.
    # `Toplevel(parent)` indica que a janela `top`
    #       será filha da janela `parent`.
    top = Toplevel(parent)

    # Define o título da janela de finalização da reserva.
    top.title("Finalizar Reserva - Inserir Data/Hora de Saída")

    # Centraliza a janela na tela e define seu tamanho para 400x300 pixels.
    # `centralizar_janela(top, 400, 300)` garante que a
    #       janela apareça centralizada.
    centralizar_janela(top, 400, 300)

    # Aplica estilos gerais à janela para manter a identidade visual do sistema.
    # `criar_estilo_geral(top)` define cores, fontes e outros elementos gráficos.
    criar_estilo_geral(top)

    # Busca no banco de dados a reserva correspondente ao ID fornecido.
    # `find_one` retorna o primeiro documento que corresponde à consulta.
    # `ObjectId(reserva_id)` converte a string do ID para um
    #       formato adequado para consultas no MongoDB.
    doc_r = colecao_reservas.find_one({"_id": ObjectId(reserva_id)})

    # Se a reserva não for encontrada, exibe uma mensagem na
    #       tela e interrompe a execução da função.
    if not doc_r:

        # Cria um rótulo (`Label`) na janela informando que a reserva não foi encontrada.
        # `foreground="red"` define a cor do texto como vermelha para destacar o erro.
        ttk.Label(top, text="Reserva não encontrada!", foreground="red").pack(pady=20)

        # `return` encerra a execução da função, pois não há dados para exibir.
        return

    # Cria um contêiner (`frame_main`) dentro da janela `top`
    #       para organizar os elementos da interface.
    frame_main = ttk.Frame(top)

    # Adiciona `frame_main` à janela e o expande para
    #       preencher o espaço disponível.
    # `fill="both"` permite que o frame ocupe todo o espaço
    #       disponível horizontal e verticalmente.
    # `expand=True` faz com que o frame cresça junto com a janela, se necessário.
    # `padx=10, pady=10` adiciona um espaçamento de 10 pixels ao
    #       redor do frame para um layout mais limpo.
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Cria um rótulo (`Label`) dentro do `frame_main` para exibir o
    #       título e informações da reserva.
    # O rótulo exibe a mensagem "Finalizar Reserva" seguida pelo
    #       bloco e número da vaga.
    #  Insere dinamicamente os dados da reserva.
    # `font=("Arial",14,"bold")` define a fonte como Arial, tamanho 14 e
    #       negrito para destacar o texto.
    # `foreground="#3F51B5"` altera a cor do texto para um
    #       azul escuro (#3F51B5) para melhorar a visibilidade.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels para
    #       separar o rótulo dos demais elementos.
    ttk.Label(frame_main,
              text=f"Finalizar Reserva\nBloco: {doc_r['bloco']} - Vaga: {doc_r['numero_vaga']}",
              font=("Arial", 14, "bold"),
              foreground="#3F51B5").pack(pady=10)

    # Obtém a data de entrada da reserva, se não houver valor,
    #       exibe "??/??/????" como padrão.
    data_entrada = doc_r.get("data_entrada", "??/??/????")

    # Obtém a hora de entrada da reserva, se não houver
    #       valor, exibe "00:00" como padrão.
    hora_entrada = doc_r.get("hora_entrada", "00:00")

    # Cria um rótulo (`Label`) dentro do `frame_main` para exibir a
    #       data e hora de entrada da reserva.
    # O rótulo exibe a mensagem "Entrada: " seguida pela data e hora da reserva.
    # `f"Entrada: {data_entrada} {hora_entrada}"` insere dinamicamente os
    #       valores obtidos anteriormente.
    # `font=("Arial",12,"bold")` define a fonte como Arial, tamanho 12 e
    #       em negrito para destacar o texto.
    # `pady=5` adiciona um pequeno espaçamento vertical para melhorar a
    #       organização da interface.
    ttk.Label(frame_main,
              text=f"Entrada: {data_entrada} {hora_entrada}",
              font=("Arial", 12, "bold")).pack(pady=5)

    # Cria um frame (`frame_saida`) dentro do `frame_main` para
    #       organizar os campos de saída.
    # Isso mantém a estrutura da interface organizada e agrupada.
    frame_saida = ttk.Frame(frame_main)
    frame_saida.pack()  # Exibe o frame na tela.

    # Chama a função `criar_campos_data`, que gera os campos de
    #       entrada para seleção da data de saída.
    # Os valores retornados são armazenados em `combo_sd_d`, `combo_sd_m`,
    #       `combo_sd_y`, e um valor extra descartado `_`.
    # O rótulo "Data Saída:" será exibido ao lado dos campos.
    combo_sd_d, combo_sd_m, combo_sd_y, _ = criar_campos_data(frame_saida, "Data Saída:")

    # Obtém a data atual usando `datetime.now()`, que retorna a
    #       data e hora do sistema no momento da execução.
    hoje = datetime.now()

    # Define os valores iniciais dos campos de seleção de data com a data atual do sistema.
    # `strftime("%d")` retorna o dia atual no formato de dois dígitos.
    # `strftime("%m")` retorna o mês atual no formato de dois dígitos.
    # `strftime("%Y")` retorna o ano atual com quatro dígitos.
    combo_sd_d.set(hoje.strftime("%d"))
    combo_sd_m.set(hoje.strftime("%m"))
    combo_sd_y.set(hoje.strftime("%Y"))

    # Cria um rótulo (`Label`) dentro do `frame_saida` para
    #       indicar o campo de entrada da hora de saída.
    # O texto exibido será "Hora Saída (HH:MM):".
    # `side="left"` mantém o rótulo alinhado à esquerda dentro do frame.
    # `padx=5` adiciona um pequeno espaçamento horizontal para não colar em outros elementos.
    ttk.Label(frame_saida, text="Hora Saída (HH:MM):").pack(side="left", padx=5)

    # Cria um campo de entrada (`Entry`) dentro do `frame_saida`
    #       para permitir que o usuário insira a hora de saída.
    # `width=8` define a largura do campo para caber uma hora no formato HH:MM.
    entry_hora = ttk.Entry(frame_saida, width=8)

    # Exibe o campo de entrada na tela, alinhado à esquerda do frame.
    # `padx=5` adiciona espaçamento horizontal para melhor separação dos elementos.
    entry_hora.pack(side="left", padx=5)

    # Insere a hora atual automaticamente no campo de entrada ao carregar a interface.
    # `datetime.now().strftime("%H:%M")` formata a hora no padrão HH:MM (exemplo: 14:30).
    entry_hora.insert(0, datetime.now().strftime("%H:%M"))

    # Cria um rótulo (`Label`) dentro do `frame_main` para
    #       exibir o valor calculado da reserva.
    # O texto inicial será "Valor Calculado: R$ 0,00", indicando que
    #       ainda não há um valor definido.
    # `font=("Arial",12,"bold")` define a fonte como Arial, tamanho 12, e
    #       em negrito para melhor visibilidade.
    lbl_valor = ttk.Label(frame_main,
                          text="Valor Calculado: R$ 0,00",
                          font=("Arial", 12, "bold"))

    # Exibe o rótulo na interface, adicionando um espaçamento
    #       vertical (`pady=10`) para não ficar colado nos outros elementos.
    lbl_valor.pack(pady=10)


    # Cria a função `calcular` para calcular o valor total da
    #       reserva com base no tempo de permanência.
    # O cálculo é feito comparando a diferença entre a
    #       data/hora de entrada e saída.
    def calcular():

        # `str_para_datetime(data_entrada, hora_entrada)` converte a
        #       string da data e hora de entrada para um objeto datetime.
        # Isso permite realizar operações matemáticas entre datas.
        dt_ent = str_para_datetime(data_entrada, hora_entrada)

        # Obtém a data de saída formatada corretamente a partir dos comboboxes.
        # O usuário seleciona o dia, mês e ano separadamente e essa
        #       função junta esses valores em uma string de data.
        data_saida_str = obter_data_de_combobox(combo_sd_d, combo_sd_m, combo_sd_y)

        # `entry_hora.get().strip()` pega o valor digitado no
        #       campo de entrada referente à hora de saída.
        # O método `.strip()` remove quaisquer espaços extras
        #       antes ou depois do texto.
        hr_sai = entry_hora.get().strip()

        # `str_para_datetime(data_saida_str, hr_sai)` converte a data e
        #       hora de saída para um objeto datetime.
        # Isso é necessário para calcular a diferença de tempo
        #       entre a entrada e saída.
        dt_sai = str_para_datetime(data_saida_str, hr_sai)

        # Se `dt_ent` ou `dt_sai` não forem válidos, significa que
        #       houve erro ao obter ou converter as datas/horas.
        if not dt_ent or not dt_sai:

            # `lbl_valor.config(text="Datas/hora inválidas!")` atualiza o rótulo na
            #       interface para informar o usuário sobre o erro.
            lbl_valor.config(text="Datas/hora inválidas!")

            # Retorna 0.0 para indicar que o cálculo não pôde ser
            #       realizado devido a erro nas datas.
            return 0.0

        # `(dt_sai - dt_ent).total_seconds() / 3600` calcula a
        #       diferença de tempo entre a entrada e a saída em horas.
        # `.total_seconds()` retorna a diferença em segundos, e a
        #       divisão por 3600 converte para horas.
        dif_horas = (dt_sai - dt_ent).total_seconds() / 3600

        # Se a diferença de horas (`dif_horas`) for negativa, significa
        #       que a data/hora de saída é anterior à entrada.
        # Isso não faz sentido e indica um erro de entrada do usuário.
        if dif_horas < 0:

            # Atualiza o rótulo na interface para exibir um aviso ao
            #       usuário de que a saída não pode ser menor que a entrada.
            lbl_valor.config(text="Saída < Entrada!")

            # Retorna 0.0 para indicar que o cálculo não
            #       foi realizado corretamente.
            return 0.0

        # Multiplica a diferença de horas pelo valor fixo da
        #       tarifa por hora (R$ 8,00).
        # Isso determina o valor total a ser cobrado pelo
        #       tempo de permanência.
        valor = dif_horas * 8.0

        # Atualiza o rótulo na interface gráfica para exibir o
        #       valor calculado ao usuário.
        # `f"Valor Calculado: R$ {valor:,.2f}"` formata o valor para
        #       exibição com duas casas decimais e separação correta de milhares.
        lbl_valor.config(text=f"Valor Calculado: R$ {valor:,.2f}")

        # Retorna o valor calculado para ser utilizado em outras
        #       partes do programa, se necessário.
        return valor


    # Define a função para o botão "Calcular".
    # Esta função chama a função `calcular()` que calcula o valor da estadia.
    def btn_calcular():
        calcular()


    # Define a função para o botão "Finalizar".
    def btn_finalizar():

        # Primeiro, chama a função `calcular()` para obter o valor da estadia.
        valor = calcular()

        # Verifica se o valor calculado é menor ou igual a zero.
        # Se for, a função retorna sem executar as próximas etapas,
        #       impedindo a finalização sem um valor válido.
        if valor <= 0.0:
            return

        # Vaga volta a ficar Livre
        # Atualiza a coleção de vagas no banco de dados.
        # Define o status da vaga como "Livre", permitindo novas
        #       reservas após a finalização.
        colecao_vagas.update_one(
            {"bloco": doc_r["bloco"], "numero_vaga": doc_r["numero_vaga"]},
            {"$set": {"status": "Livre"}}
        )

        # Obtém a data de saída a partir dos campos da interface gráfica.
        # `combo_sd_d`, `combo_sd_m`, `combo_sd_y` representam os
        #       campos de dia, mês e ano da saída.
        data_saida_str = obter_data_de_combobox(combo_sd_d, combo_sd_m, combo_sd_y)

        # Obtém a hora de saída digitada pelo usuário no campo de entrada de texto.
        # `strip()` é usado para remover espaços extras no início e no final.
        hr_sai = entry_hora.get().strip()

        # Atualiza a reserva para "Finalizado"
        # Atualiza a reserva no banco de dados, marcando-a como finalizada.
        # O documento identificado pelo `reserva_id` receberá os
        #       novos valores de data e hora de saída, além do valor total
        #       calculado e o status atualizado para "Finalizado".
        colecao_reservas.update_one(
            {"_id": ObjectId(reserva_id)},
            {
                "$set": {
                    "data_saida": data_saida_str,  # Define a data de saída fornecida pelo usuário.
                    "hora_saida": hr_sai,  # Define a hora de saída fornecida pelo usuário.
                    "valor_total": valor,  # Registra o valor total calculado para a estadia.
                    "status": "Finalizado"  # Marca a reserva como finalizada.
                }
            }
        )

        # Chama a função `gerar_comprovante(valor)` para exibir um
        #       comprovante de pagamento ao usuário.
        gerar_comprovante(valor)

        # Fecha a janela atual, pois a finalização já foi processada.
        # top.destroy()

        # Recarrega os dados para atualizar a interface gráfica e refletir as mudanças.
        callback_recarregar()


    # Cria a função `gerar_comprovante`, que será responsável por
    #       exibir um comprovante de pagamento.
    def gerar_comprovante(valor):

        # Cria uma nova janela (`Toplevel`) que servirá como o
        #       comprovante de pagamento.
        pop = Toplevel(top)

        # Define o título da janela como "Comprovante de Pagamento".
        pop.title("Comprovante de Pagamento")

        # Centraliza a janela do comprovante na tela, definindo
        #       largura e altura (400x200).
        centralizar_janela(pop, 400, 200)

        # Aplica o estilo geral da interface à janela do comprovante
        #       para manter a identidade visual do sistema.
        criar_estilo_geral(pop)

        # Cria um container (`Frame`) dentro da janela para
        #       organizar os elementos do comprovante.
        frame_cp = ttk.Frame(pop)

        # Posiciona o frame dentro da janela, permitindo que ele se
        #       expanda tanto horizontal quanto verticalmente.
        # `padx=10` e `pady=10` adicionam espaçamento ao redor do
        #       frame para melhor estética.
        frame_cp.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria um rótulo para exibir o título do comprovante.
        # `text="Comprovante - Reserva Finalizada"` define o texto exibido no rótulo.
        # `font=("Arial",14,"bold")` define a fonte Arial, tamanho 14, com negrito.
        # `foreground="#3F51B5"` define a cor do texto como azul escuro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical para separar dos outros elementos.
        ttk.Label(frame_cp,
                  text="Comprovante - Reserva Finalizada",
                  font=("Arial", 14, "bold"),
                  foreground="#3F51B5").pack(pady=10)

        # Cria um rótulo para exibir o valor pago no comprovante.
        # `text=f"Valor Pago: R$ {valor:,.2f}"` formata o valor como
        #       moeda brasileira, com duas casas decimais.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       abaixo do texto para melhor legibilidade.
        ttk.Label(frame_cp, text=f"Valor Pago: R$ {valor:,.2f}").pack(pady=5)

        # Cria um rótulo para exibir uma mensagem de agradecimento ao cliente.
        # `text="Obrigado pela preferência!"` define o texto exibido no rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       abaixo do texto para melhor apresentação.
        ttk.Label(frame_cp, text="Obrigado pela preferência!").pack(pady=5)

        # Cria um botão para fechar a janela do comprovante.
        # `text="Fechar"` define o texto exibido no botão.
        # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
        # `command=pop.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
        ttk.Button(frame_cp,
                   text="Fechar",
                   style="MyButton.TButton",
                   command=pop.destroy).pack(pady=10)


        # Abre a Janela na tela
        pop.mainloop()


    # Cria um frame (container) para os botões, dentro do frame principal.
    # Isso organiza os botões em um local específico da interface.
    frame_btn = ttk.Frame(frame_main)

    # Adiciona um espaçamento vertical de 10 pixels.
    frame_btn.pack(pady=10)

    # Cria um botão para calcular o valor da estadia.
    # `text="Calcular Valor"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=btn_calcular` associa a função `btn_calcular` ao clique do botão.
    # `pack(side="left", padx=10)` posiciona o botão à esquerda e
    #       adiciona um espaçamento horizontal de 10 pixels.
    ttk.Button(frame_btn,
               text="Calcular Valor",
               style="MyButton.TButton",
               command=btn_calcular).pack(side="left", padx=10)

    # Cria um botão para finalizar a reserva e processar o pagamento.
    # `text="Finalizar/Pagar"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=btn_finalizar` associa a função `btn_finalizar` ao clique do botão.
    # `pack(side="left", padx=10)` posiciona o botão à esquerda e
    #       adiciona um espaçamento horizontal de 10 pixels.
    ttk.Button(frame_btn,
               text="Finalizar/Pagar",
               style="MyButton.TButton",
               command=btn_finalizar).pack(side="left", padx=10)



# Define a função `criar_campos_data` para criar um conjunto de
#       campos de data (dia, mês e ano).
# `parent` define o widget pai onde os campos serão posicionados.
# `label_text` define o texto do rótulo acima dos campos de data.
def criar_campos_data(parent, label_text):

    # Cria um frame (`frame_data`) dentro do widget pai (`parent`)
    #       para organizar os elementos da data.
    frame_data = ttk.Frame(parent)

    # Exibe o frame dentro do widget pai.
    # `side="left"` posiciona o frame à esquerda do layout.
    # `padx=5, pady=5` adiciona espaçamento horizontal e vertical
    #       para organização visual.
    frame_data.pack(side="left", padx=5, pady=5)

    # Cria um rótulo (`Label`) com o texto especificado em `label_text`.
    # Este rótulo será exibido acima dos campos de seleção de data.
    lbl = ttk.Label(frame_data, text=label_text)

    # Exibe o rótulo dentro do frame de data.
    lbl.pack()

    # Chama a função `gerar_listas_data()`, que retorna três
    #       listas: dias, meses e anos.
    dias, meses, anos = gerar_listas_data()

    # Cria um combobox (`combo_dia`) para selecionar o dia.
    # `frame_data` é o widget pai onde o combobox será posicionado.
    # `values=dias` define a lista de opções para os dias (01 a 31).
    # `width=3` define a largura do campo para acomodar dois dígitos.
    # `state="readonly"` impede que o usuário digite valores
    #       manualmente, permitindo apenas a seleção.
    combo_dia = ttk.Combobox(frame_data,
                             values=dias,
                             width=3,
                             state="readonly")

    # Exibe o combobox do dia dentro do `frame_data`.
    # `side="left"` posiciona o elemento à esquerda dentro do frame.
    # `padx=2` adiciona um pequeno espaçamento horizontal entre os elementos.
    combo_dia.pack(side="left", padx=2)

    # Cria um combobox (`combo_mes`) para selecionar o mês.
    # `values=meses` define a lista de opções para os meses (01 a 12).
    # `width=3` define a largura do campo para acomodar dois dígitos.
    # `state="readonly"` impede que o usuário digite
    #       valores, permitindo apenas a seleção.
    combo_mes = ttk.Combobox(frame_data,
                             values=meses,
                             width=3,
                             state="readonly")

    # Exibe o combobox do mês dentro do `frame_data`.
    # `side="left"` posiciona o elemento à esquerda do próximo elemento.
    # `padx=2` adiciona um pequeno espaçamento horizontal entre os elementos.
    combo_mes.pack(side="left", padx=2)

    # Cria um combobox (`combo_ano`) para selecionar o ano.
    # `values=anos` define a lista de opções de anos (de um
    #       intervalo de 5 anos para trás até 5 anos para frente).
    # `width=5` define a largura do campo para acomodar quatro dígitos.
    # `state="readonly"` impede que o usuário digite valores
    #       manualmente, permitindo apenas a seleção.
    combo_ano = ttk.Combobox(frame_data,
                             values=anos,
                             width=5,
                             state="readonly")

    # Exibe o combobox do ano dentro do `frame_data`.
    # `side="left"` posiciona o elemento à esquerda do próximo elemento.
    # `padx=2` adiciona um pequeno espaçamento horizontal entre os elementos.
    combo_ano.pack(side="left", padx=2)

    # Retorna os três comboboxes (`combo_dia`, `combo_mes`, `combo_ano`) e o frame (`frame_data`).
    # Isso permite que esses elementos sejam acessados e
    #       manipulados posteriormente.
    return combo_dia, combo_mes, combo_ano, frame_data



# Define a função `gerar_listas_data`, que gera listas de dias,
#       meses e anos para serem usadas em seletores de data.
# Retorno:
# - `dias`: lista contendo os dias do mês, de "01" a "31".
# - `meses`: lista contendo os meses do ano, de "01" a "12".
# - `anos`: lista contendo anos desde cinco anos atrás até
#       cinco anos à frente do ano atual.

def gerar_listas_data():

    # Gera uma lista de dias formatados com dois dígitos (01 a 31).
    # Utiliza list comprehension para criar a lista, garantindo
    #       que os números tenham sempre dois dígitos.
    dias = [f"{d:02d}" for d in range(1, 32)]  # "01".."31"

    # Gera uma lista de meses formatados com dois dígitos (01 a 12).
    # Também utiliza list comprehension para manter o formato de dois dígitos.
    meses = [f"{m:02d}" for m in range(1, 13)]  # "01".."12"

    # Obtém o ano atual utilizando `datetime.now().year`.
    ano_atual = datetime.now().year

    # Gera uma lista de anos em formato de string, indo de 5 anos
    #       antes até 5 anos depois do ano atual.
    anos = [str(y) for y in range(ano_atual - 5, ano_atual + 6)]

    # Retorna as três listas: `dias`, `meses` e `anos`.
    return dias, meses, anos


# Define a função `str_para_datetime`, que converte strings de
#       data e hora para um objeto `datetime`.
# Parâmetros:
# - `data_str`: uma string representando a data no formato "dd/mm/aaaa".
# - `hora_str`: uma string representando a hora no formato "HH:MM".
# Retorno:
# - Um objeto `datetime` combinando a data e hora fornecidas, ou
#       `None` se houver erro na conversão.
def str_para_datetime(data_str, hora_str):

    # Utiliza um bloco `try-except` para evitar que o programa
    #       quebre caso os valores fornecidos sejam inválidos.
    try:

        # Converte a string `data_str` em um objeto `datetime`
        #       usando o formato "dd/mm/yyyy".
        dt = datetime.strptime(data_str, "%d/%m/%Y")

        # Converte a string `hora_str` em um objeto `time` usando o formato "HH:MM".
        tm = datetime.strptime(hora_str, "%H:%M").time()

        # Combina a data (`dt`) e a hora (`tm`) em um
        #       único objeto `datetime`.
        return datetime.combine(dt, tm)

    # Se houver erro na conversão (por exemplo, se a string
    #       estiver no formato errado), retorna `None`.
    except:
        return None



# Obtém a data selecionada pelos comboboxes e a retorna formatada.
def obter_data_de_combobox(combo_dia, combo_mes, combo_ano):

    # Obtém o valor selecionado no combobox do dia.
    # `.get()` recupera o valor atual do combobox.
    # `.strip()` remove espaços em branco no início e
    #       no final, caso existam.
    d = combo_dia.get().strip()

    # Obtém o valor selecionado no combobox do mês.
    # `.get()` recupera o valor atual do combobox.
    # `.strip()` remove espaços em branco no início e no final, caso existam.
    m = combo_mes.get().strip()

    # Obtém o valor selecionado no combobox do ano.
    # `.get()` recupera o valor atual do combobox.
    # `.strip()` remove espaços em branco no início e
    #       no final, caso existam.
    a = combo_ano.get().strip()

    # Verifica se algum dos campos está vazio.
    # Se um dos valores não foi selecionado, retorna uma string vazia.
    if not d or not m or not a:
        return ""

    # Retorna a data formatada no padrão brasileiro (DD/MM/AAAA).
    return f"{d}/{m}/{a}"


# Define a função popup_reservar que cria uma janela pop-up para reservar uma vaga.
# `parent` define a janela principal que abrirá o pop-up.
# `bloco` é o nome do bloco onde a vaga se encontra.
# `num_vaga` é o número da vaga que está sendo reservada.
# `data_sel` é a data selecionada para a reserva.
# `callback_recarregar` é a função a ser chamada para
#       recarregar a interface após a reserva.
def popup_reservar(parent, bloco, num_vaga, data_sel, callback_recarregar):

    # Cria uma nova janela pop-up utilizando Toplevel, que é
    #       uma janela filha da janela principal.
    # `Toplevel(parent)` cria a nova janela associada ao widget pai `parent`.
    top = Toplevel(parent)

    # Define o título da janela pop-up.
    # `top.title(f"Reservar - {bloco}-{num_vaga}")` define o título
    #       com a palavra "Reservar" seguida pelo bloco e número da vaga.
    top.title(f"Reservar - {bloco}-{num_vaga}")

    # Centraliza a janela pop-up na tela e define seu tamanho.
    # `centralizar_janela(top, 400, 400)` centraliza a janela e
    #       define sua largura e altura como 400 pixels cada.
    centralizar_janela(top, 400, 400)

    # Aplica o estilo visual geral à janela pop-up.
    # `criar_estilo_geral(top)` configura a aparência da janela, como
    #       cores, fontes e outros parâmetros visuais, de acordo com o padrão da aplicação.
    criar_estilo_geral(top)

    # Cria um frame principal dentro da janela pop-up.
    # `ttk.Frame(top)` cria um contêiner que agrupa os elementos da
    #       interface dentro da janela `top`.
    frame_main = ttk.Frame(top)

    # Ajusta o frame para ocupar todo o espaço disponível dentro da janela.
    # `fill="both"` permite que o frame expanda tanto na horizontal quanto na vertical.
    # `expand=True` permite que o frame cresça junto com a janela
    #       caso ela seja redimensionada.
    # `padx=10, pady=10` adiciona espaçamento interno de 10 pixels nas
    #       bordas do frame, para melhor estética.
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Cria um rótulo (label) que exibe as informações da reserva.
    # `frame_main` define o contêiner pai onde o rótulo será inserido.
    # `text=f"Reserva para {bloco}-{num_vaga}\nData: {data_sel}"`
    #       define o texto do rótulo, onde `{bloco}` e `{num_vaga}` são
    #       substituídos pelo bloco e número da vaga escolhidos.
    #  `{data_sel}` exibe a data da reserva no formato correto.
    # `font=("Arial", 14, "bold")` define a fonte como Arial,
    #       tamanho 14, e estilo negrito para dar destaque.
    # `foreground="#3F51B5"` define a cor do texto como azul escuro (#3F51B5)
    #       para manter o padrão visual do sistema.
    lbl_info = ttk.Label(frame_main,
                         text=f"Reserva para {bloco}-{num_vaga}\nData: {data_sel}",
                         font=("Arial", 14, "bold"),
                         foreground="#3F51B5")

    # Posiciona o rótulo na interface gráfica.
    # `pady=10` adiciona 10 pixels de espaçamento vertical para
    #       separar o rótulo dos outros elementos.
    # Isso melhora a organização visual e torna o texto mais legível.
    lbl_info.pack(pady=10)

    # Escolher Cliente
    # Cria um rótulo (label) para indicar ao usuário que ele deve selecionar um cliente.
    # `frame_main` é o contêiner pai onde o rótulo será inserido.
    # `text="Selecione o Cliente:"` define o texto do rótulo para orientar o usuário.
    # `font=("Arial", 12, "bold")` define a fonte como Arial,
    #       tamanho 12, e em negrito para dar destaque.
    ttk.Label(frame_main,
              text="Selecione o Cliente:",
              font=("Arial", 12, "bold")).pack(pady=5)

    # Cria uma variável `StringVar()` para armazenar a
    #       seleção do cliente no combobox.
    # Isso permite que o valor selecionado possa ser
    #       recuperado facilmente no código.
    combo_cvar = StringVar()

    # Cria um combobox (caixa de seleção) para escolher um cliente.
    # `frame_main` define que este widget será inserido dentro do
    #       contêiner principal da interface.
    # `textvariable=combo_cvar` associa o combobox à variável `combo_cvar`,
    #       permitindo recuperar o valor selecionado.
    # `state="readonly"` impede que o usuário digite no combobox,
    #       garantindo que apenas seleções válidas sejam feitas.
    # `width=35` define a largura do combobox, garantindo espaço
    #       suficiente para exibir os nomes dos clientes.
    combo_c = ttk.Combobox(frame_main,
                           textvariable=combo_cvar,
                           state="readonly",
                           width=35)

    # Posiciona o combobox na interface gráfica.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels entre o
    #       combobox e os outros elementos para melhorar a organização visual.
    combo_c.pack(pady=5)

    # Carregar clientes
    # Recupera todos os documentos da coleção `colecao_clientes` e
    #       os armazena em uma lista.
    # `list(colecao_clientes.find())` busca todos os registros de
    #       clientes do banco de dados.
    docs_c = list(colecao_clientes.find())

    # Cria uma lista formatada contendo CPF e Nome de cada cliente.
    # Para cada cliente (`d`) encontrado em `docs_c`, é gerada uma
    #       string no formato "CPF - Nome".
    # Isso facilita a visualização e a escolha do cliente no combobox.
    lst_c = [f"{d['cpf']} - {d['nome']}" for d in docs_c]

    # Define os valores disponíveis no combobox como a
    #       lista formatada de clientes (`lst_c`).
    # Isso permite que o usuário selecione um cliente na
    #       interface gráfica.
    combo_c["values"] = lst_c

    # Escolher Veículo do Cliente
    # Cria um rótulo (label) para informar ao usuário que deve
    #       selecionar um veículo do cliente.
    # O texto é "Selecione o Veículo (do Cliente):".
    # A fonte usada é Arial, tamanho 12, e em negrito.
    # O espaçamento vertical (pady) é de 5 pixels para melhor separação visual.
    ttk.Label(frame_main,
              text="Selecione o Veículo (do Cliente):",
              font=("Arial", 12, "bold")).pack(pady=5)

    # Cria uma variável de controle (`StringVar`) para armazenar o
    #       valor selecionado no combobox.
    # Essa variável manterá a seleção do usuário para posterior uso.
    combo_vvar = StringVar()

    # Cria um combobox (`ttk.Combobox`) dentro do `frame_main`,
    #       associado à variável `combo_vvar`.
    # O estado `readonly` impede que o usuário digite manualmente,
    #       permitindo apenas seleções da lista.
    # A largura do combobox é definida como 35 caracteres para
    #       melhor visualização das opções.
    combo_v = ttk.Combobox(frame_main,
                           textvariable=combo_vvar,
                           state="readonly",
                           width=35)

    # Adiciona um espaçamento vertical (`pady=5`) e exibe o
    #       combobox na interface gráfica.
    combo_v.pack(pady=5)

    # Define a função que será chamada ao selecionar um cliente no combobox.
    # Essa função atualiza a lista de veículos do cliente selecionado.
    def ao_escolher_cliente(event):

        # Obtém o valor selecionado no combobox de clientes e
        #       remove espaços em branco extras.
        sel_c = combo_cvar.get().strip()

        # Se nenhum cliente for selecionado, a lista de veículos será limpa.
        if not sel_c:

            # Remove todas as opções do combobox de veículos.
            combo_v["values"] = []

            # Define o valor do combobox de veículos como vazio.
            combo_v.set("")

            # Desativa o combobox de veículos, impedindo a seleção
            #       de um veículo sem cliente.
            combo_v.config(state="disabled")

            # Sai da função, pois não há mais nada a ser feito.
            return

        # Agora buscamos diretamente pelo campo 'proprietario'
        proprietario = sel_c

        # Buscar TODOS os veículos do cliente (sem filtrar por status)
        docs_v = list(colecao_veiculos.find({"proprietario": proprietario}))

        # Verificar e preencher a combobox
        # Verifica se há veículos cadastrados para o cliente selecionado.
        if docs_v:

            # Cria uma lista vazia para armazenar as opções do combobox de veículos.
            lst_v = []

            # Percorre todos os veículos encontrados no banco de dados.
            for dv in docs_v:

                # Exibe no console os detalhes do veículo encontrado para depuração.
                print(f"🔍 Veículo encontrado: {dv}")

                # Obtém a placa do veículo, se não existir, define como string vazia.
                placa = dv.get("placa", "")

                # Obtém o modelo do veículo, se não existir, define como string vazia.
                modelo = dv.get("modelo", "")

                # Obtém a cor do veículo, se não existir, define como string vazia.
                cor = dv.get("cor", "")

                # Formata a string com os dados do veículo e adiciona à lista.
                # Exemplo: "XYZ-1234 - Fiesta - Prata"
                lst_v.append(f"{placa} - {modelo} - {cor}")

            # Atualiza os valores do combobox de veículos com a lista formatada.
            combo_v["values"] = lst_v

            # Define um texto padrão no combobox indicando que o
            #       usuário deve selecionar um veículo.
            combo_v.set("Selecione um veículo")

            # Ativa o combobox, permitindo a seleção de veículos.
            combo_v.config(state="readonly")

        # Habilita a combo
        # Caso o cliente selecionado não tenha veículos cadastrados:
        else:

            # Define a lista de valores do combobox de veículos com
            #       uma mensagem informativa.
            combo_v["values"] = ["Nenhum veículo encontrado"]

            # Define o valor exibido na combo box para "Nenhum
            #       veículo encontrado".
            combo_v.set("Nenhum veículo encontrado")

            # Desativa o combobox para impedir seleção, pois
            #       não há veículos disponíveis.
            combo_v.config(state="disabled")

    # Vincular evento de mudança de cliente
    # Associa a função `ao_escolher_cliente` ao evento de
    #       seleção da combobox de clientes.
    # Quando o usuário selecionar um cliente, a função `ao_escolher_cliente`
    #       será chamada automaticamente.
    combo_c.bind("<<ComboboxSelected>>", ao_escolher_cliente)

    # Cria um rótulo (Label) para indicar ao usuário que ele
    #       deve inserir a hora de entrada da reserva.
    # O texto do rótulo será "Hora de Entrada (HH:MM)".
    # A fonte utilizada será Arial, tamanho 12, e em negrito
    #       para destacar a informação.
    ttk.Label(frame_main,
              text="Hora de Entrada (HH:MM):",
              font=("Arial", 12, "bold")).pack(pady=5)

    # Cria um campo de entrada (Entry) para que o usuário
    #       digite a hora de entrada da reserva.
    # O `width=10` define que o campo de entrada terá largura
    #       suficiente para exibir 10 caracteres.
    entry_hora = ttk.Entry(frame_main, width=10)
    entry_hora.pack(pady=5)

    # Insere automaticamente a hora atual dentro do campo de
    #       entrada assim que a janela for aberta.
    # A hora será formatada no padrão "HH:MM" (horas e minutos).
    entry_hora.insert(0, datetime.now().strftime("%H:%M"))

    # Cria um frame (container) para organizar os
    #       botões dentro da janela.
    # Esse frame mantém os botões alinhados e com um
    #       espaçamento adequado.
    frame_btn = ttk.Frame(frame_main)
    frame_btn.pack(pady=10)

    # Função `salvar` responsável por validar e
    #       registrar uma reserva de vaga.
    def salvar():

        # Obtém o valor selecionado na combobox de clientes e
        #       remove espaços extras do início e fim.
        sc = combo_cvar.get().strip()

        # Obtém o valor selecionado na combobox de veículos e remove
        #       espaços extras do início e fim.
        sv = combo_vvar.get().strip()

        # Obtém a hora de entrada digitada pelo usuário e
        #       remove espaços extras do início e fim.
        hr_ = entry_hora.get().strip()

        # Verifica se um cliente foi selecionado corretamente.
        # A string deve conter " - " para separar CPF e nome.
        if not sc or " - " not in sc:
            messagebox.showerror("Erro", "Selecione um cliente!", parent=top)
            return

        # Verifica se um veículo foi selecionado corretamente.
        # A string deve conter " - " para separar placa e modelo do veículo.
        # Além disso, impede a seleção de "Nenhum veículo encontrado".
        if not sv or " - " not in sv or sv == "Nenhum veículo encontrado":
            messagebox.showerror("Erro", "Selecione um veículo válido!", parent=top)
            return

        # Separa o CPF e o nome do cliente a partir do valor selecionado na combobox.
        cpf_, nm_ = sc.split(" - ", 1)

        # Separa a placa e o modelo do veículo a partir do valor selecionado na combobox.
        placa_, mod_ = sv.split(" - ", 1)

        # Criar documento de reserva
        # O dicionário `doc_res` contém todas as informações
        #       necessárias para registrar uma reserva.
        doc_res = {

            # Armazena o CPF do cliente que fez a reserva.
            "cliente_cpf": cpf_,

            # Armazena o nome do cliente que fez a reserva.
            "cliente_nome": nm_,

            # Armazena a placa do veículo associado à reserva.
            "veiculo_placa": placa_,

            # Armazena o modelo do veículo associado à reserva.
            "veiculo_modelo": mod_,

            # Armazena a data de entrada selecionada no calendário.
            "data_entrada": data_sel,

            # Armazena a hora de entrada informada pelo usuário.
            "hora_entrada": hr_,

            # Define a data de saída como "-" (indica que
            #       ainda não foi definida).
            "data_saida": "-",

            # Define a hora de saída como "-" (indica que ainda não foi definida).
            "hora_saida": "-",

            # Armazena o nome do bloco onde a vaga está localizada.
            "bloco": bloco,

            # Armazena o número da vaga reservada.
            "numero_vaga": num_vaga,

            # Define o valor total da reserva como 0, pois
            #       ainda não foi calculado.
            "valor_total": 0,

            # Define o status da reserva como "Reservado" (aguardando ocupação).
            "status": "Reservado"

        }

        # Insere o documento `doc_res` na coleção `colecao_reservas`
        #       do banco de dados.
        colecao_reservas.insert_one(doc_res)

        # Atualiza o status da vaga para "Reservada".
        # Isso garante que a vaga não seja ocupada por outro cliente no mesmo período.
        colecao_vagas.update_one(

            # Filtra a vaga pelo bloco e número da vaga.
            {"bloco": bloco, "numero_vaga": num_vaga},

            # Define o status da vaga como "Reservada".
            {"$set": {"status": "Reservada"}}

        )

        # Exibe um alerta informando que a reserva foi realizada com sucesso.
        # `title="Sucesso"` define o título da mensagem.
        # `message=f"Reserva efetuada para {bloco}-{num_vaga}!"` exibe a
        #       confirmação com os detalhes da vaga.
        # `parent=top` garante que a mensagem apareça vinculada à janela de reserva.
        messagebox.showinfo(title="Sucesso",
                            message=f"Reserva efetuada para {bloco}-{num_vaga}!",
                            parent=top)

        # Fecha a janela de reserva após a confirmação da operação.
        # Isso evita que o usuário faça múltiplas reservas sem necessidade.
        top.destroy()

        # Recarrega a interface do mapa para exibir a vaga como "Reservada".
        # Isso mantém a interface atualizada com os dados mais recentes.
        callback_recarregar()

    # Cria um botão para salvar a reserva.
    # `text="Salvar Reserva"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=salvar` associa a ação de salvar a reserva ao clicar no botão.
    # `side="left"` posiciona o botão à esquerda dentro do frame.
    # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os botões.
    ttk.Button(frame_btn,
               text="Salvar Reserva",
               style="MyButton.TButton",
               command=salvar).pack(side="left", padx=10)

    # Cria um botão para fechar a janela de reserva.
    # `text="Fechar"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=top.destroy` associa a ação de fechar a janela ao clicar no botão.
    # `side="left"` posiciona o botão à esquerda dentro do
    #       frame, ao lado do botão de salvar.
    # `padx=10` adiciona um espaçamento horizontal de
    #       10 pixels entre os botões.
    ttk.Button(frame_btn,
               text="Fechar",
               style="MyButton.TButton",
               command=top.destroy).pack(side="left", padx=10)



# -------------------------------------------------------------------------
# CRUD de Blocos (gera Vagas)
# -------------------------------------------------------------------------

# Define uma função chamada `tela_blocos_crud` que recebe `janela_pai` como parâmetro.
# Esta função cria uma nova janela para gerenciar blocos.
def tela_blocos_crud(janela_pai):

    # Cria uma nova janela secundária (`Toplevel`) a partir da `janela_pai`.
    janela = tk.Toplevel(janela_pai)

    # Define o título da janela como "Gerenciamento de Blocos".
    janela.title("Gerenciamento de Blocos")

    # Define a largura e a altura da janela, com valores de 900x500 pixels.
    largura, altura = 900, 500

    # Chama a função `centralizar_janela` para posicionar a
    #       janela no centro da tela.
    # A função `centralizar_janela` precisa estar definida no
    #       código e recebe a `janela`,
    #       largura e altura como parâmetros.
    centralizar_janela(janela, largura, altura)

    # Define a cor de fundo da janela para um tom de
    #       cinza claro (`#F5F5F5`).
    janela.configure(bg="#F5F5F5")

    # Cria um container principal dentro da `janela`, onde
    #       todos os elementos da interface serão organizados.
    # Define a cor de fundo como `#F5F5F5`, um tom de cinza claro.
    container_principal = tk.Frame(janela, bg="#F5F5F5")

    # Empacota (`pack()`) o container para ocupar todo o
    #       espaço disponível.
    # `expand=True` permite que o container se expanda para
    #       preencher o espaço disponível.
    # `fill="both"` faz com que ele preencha tanto a
    #       largura quanto a altura da janela.
    container_principal.pack(expand=True, fill="both")

    # Cria um rótulo (`Label`) dentro do `container_principal`
    #       para exibir o título da janela.
    # O título informa que esta tela gerencia blocos e
    #       vagas de estacionamento.
    rotulo_titulo = ttk.Label(container_principal,  # Define o container onde o rótulo será inserido.
                              text="🏢 Gerenciar Blocos e Vagas",  # Define o texto exibido no rótulo.
                              font=("Arial", 22, "bold"),  # Define a fonte do texto como Arial, tamanho 22, em negrito.
                              foreground="#2E86C1",  # Define a cor do texto para um tom de azul (`#2E86C1`).
                              background="#F5F5F5")  # Define a cor de fundo do rótulo para o mesmo tom de cinza claro do container.

    # Adiciona um espaçamento vertical (`pady=10`) ao
    #       redor do rótulo para melhor organização visual.
    rotulo_titulo.pack(pady=10)

    # Cria um frame (`Frame`) dentro do `container_principal`
    #       para organizar os campos do formulário.
    # Esse frame servirá como um agrupador para os
    #       campos de entrada do usuário.
    container_formulario = ttk.Frame(container_principal)

    # Empacota (`pack()`) o frame dentro do container principal.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels ao
    #       redor do frame, garantindo melhor organização visual.
    container_formulario.pack(pady=10)

    # Cria um rótulo (`Label`) para identificar o campo de entrada
    #       onde o usuário informará o nome do bloco.
    # `text="Nome do Bloco:"` define o texto que será exibido ao
    #       lado do campo de entrada.
    # `font=("Arial", 12)` especifica a fonte do texto no rótulo,
    #       utilizando a fonte Arial no tamanho 12.
    # `.grid(row=0, column=0, padx=5, pady=5, sticky="e")`
    #       posiciona o rótulo na linha 0, coluna 0,
    #       adicionando um espaçamento de 5 pixels nas margens
    #       horizontal (`padx`) e vertical (`pady`).
    # O argumento `sticky="e"` alinha o texto à direita
    #       dentro da célula do grid.
    ttk.Label(container_formulario,
              text="Nome do Bloco:",
              font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (`Entry`) onde o usuário
    #       poderá digitar o nome do bloco.
    # `width=30` define a largura do campo, permitindo a
    #       entrada de até 30 caracteres visíveis.
    # `font=("Arial", 12)` define que o texto digitado no
    #       campo usará a fonte Arial no tamanho 12.
    campo_nome = ttk.Entry(container_formulario,
                           width=30,
                           font=("Arial", 12))

    # Posiciona o campo de entrada na interface gráfica.
    # `row=0, column=1` coloca o campo na mesma linha que o
    #       rótulo, mas na segunda coluna.
    # `padx=5, pady=5` adiciona espaçamento de 5 pixels ao
    #       redor do campo, melhorando a legibilidade.
    # Como o rótulo está alinhado à direita, o campo será
    #       alinhado corretamente ao lado do rótulo.
    campo_nome.grid(row=0, column=1, padx=5, pady=5)

    # Cria um rótulo de texto para exibir "Quantidade de Vagas:" na interface gráfica.
    # `text="Quantidade de Vagas:"` define o texto visível ao usuário.
    # `font=("Arial", 12)` define a fonte como Arial no
    #       tamanho 12 para melhor legibilidade.
    # `grid(row=1, column=0, padx=5, pady=5, sticky="e")`
    #       posiciona o rótulo na linha 1, coluna 0.
    # `padx=5, pady=5` adiciona espaçamento horizontal e
    #       vertical para evitar elementos colados.
    # `sticky="e"` alinha o texto à direita dentro da célula,
    #       garantindo alinhamento com o campo de entrada.
    ttk.Label(container_formulario,
              text="Quantidade de Vagas:",
              font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para que o usuário informe a
    #       quantidade de vagas do bloco.
    # `ttk.Entry(container_formulario)` cria um campo de
    #       entrada dentro do `container_formulario`.
    # `width=10` define a largura do campo, permitindo inserir
    #       até 10 caracteres de forma visível.
    # `font=("Arial", 12)` define a fonte como Arial, tamanho 12,
    #       garantindo melhor leitura e consistência com os outros elementos da interface.
    campo_qtd_vagas = ttk.Entry(container_formulario,
                                width=10,
                                font=("Arial", 12))

    # Posiciona o campo de entrada na interface usando o método `grid()`.
    # `row=1` indica que o campo será posicionado na segunda linha da
    #       grade, abaixo do rótulo "Quantidade de Vagas".
    # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo.
    # `padx=5, pady=5` adiciona um espaçamento de 5 pixels horizontal e
    #       verticalmente, evitando que os elementos fiquem colados.
    campo_qtd_vagas.grid(row=1, column=1, padx=5, pady=5)

    # Cria um container (Frame) para agrupar os botões de ação.
    # `ttk.Frame(container_principal)` cria um novo frame dentro do
    #       `container_principal`, onde os botões serão adicionados.
    container_botoes = ttk.Frame(container_principal)

    # Posiciona o container de botões na interface usando o método `pack()`.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels,
    #       separando o container de botões dos outros elementos.
    container_botoes.pack(pady=10)


    # Define a função `carregar_lista` para carregar os
    #       blocos cadastrados na tabela.
    def carregar_lista():

        # Remove todos os itens da tabela antes de carregar os novos dados.
        # `delete(*tabela_blocos.get_children())`: Garante que a
        #       tabela seja limpa antes de adicionar novos registros.
        tabela_blocos.delete(*tabela_blocos.get_children())

        # Obtém todos os blocos cadastrados na coleção do banco de dados.
        # `colecao_blocos.find()`: Retorna todos os
        #       documentos (blocos) cadastrados na coleção.
        blocos = colecao_blocos.find()

        # Itera sobre cada bloco encontrado na base de dados.
        for bloco in blocos:

            # Insere um novo bloco na tabela com os valores extraídos do banco de dados.
            # `"values=(str(bloco["_id"]), bloco["nome"], bloco["quantidade"])"`
            # - `bloco["_id"]`: Converte o identificador único do bloco em string.
            # - `bloco["nome"]`: Exibe o nome do bloco.
            # - `bloco["quantidade"]`: Exibe a quantidade de vagas disponíveis.
            tabela_blocos.insert("",
                                 "end",
                                 values=(str(bloco["_id"]), bloco["nome"], bloco["quantidade"]))


    # Define a função `cadastrar()` para adicionar um
    #       novo bloco de estacionamento.
    def cadastrar():

        # Obtém o valor do campo `campo_nome`, removendo
        #       espaços extras no início e no final.
        nome = campo_nome.get().strip()

        # Obtém o valor do campo `campo_qtd_vagas`, removendo
        #       espaços extras no início e no final.
        quantidade = campo_qtd_vagas.get().strip()

        # Verifica se os campos `nome` ou `quantidade` estão vazios.
        # Se estiverem vazios, exibe uma mensagem de erro e
        #       interrompe a execução da função.
        if not nome or not quantidade:
            messagebox.showerror("Erro",
                                 "Nome e quantidade são obrigatórios!",
                                 parent=janela)
            return

        # Tenta converter o valor da variável `quantidade`
        #       para um número inteiro
        try:

            # Converte a string `quantidade` para inteiro e armazena em `qtd_int`
            qtd_int = int(quantidade)

            # Verifica se o número convertido é menor que 1
            if qtd_int < 1:

                # Exibe uma mensagem de erro informando que a quantidade de
                #       vagas deve ser maior que 0
                messagebox.showerror("Erro",
                                     "A quantidade de vagas deve ser maior que 0!",
                                     parent=janela)

                # Encerra a função, impedindo a continuação do cadastro
                return

        # Caso ocorra um erro na conversão (quando o usuário
        #       digitar um valor não numérico)
        except ValueError:

            # Exibe uma mensagem de erro informando que a quantidade
            #       precisa ser um número inteiro válido
            messagebox.showerror("Erro",
                                 "Quantidade inválida! Digite um número inteiro.",
                                 parent=janela)

            # Encerra a função, impedindo a continuação do cadastro
            return

        # Verifica se o nome do bloco já existe no banco de dados antes de cadastrá-lo
        # Procura um documento com o mesmo nome na coleção `colecao_blocos`
        if colecao_blocos.find_one({"nome": nome}):

            # Se encontrar um bloco já cadastrado com o mesmo nome,
            #       exibe uma mensagem de erro
            messagebox.showerror("Erro",
                                 "Este bloco já está cadastrado!",
                                 parent=janela)

            # Encerra a função, impedindo a duplicação de
            #       blocos no banco de dados
            return

        # Insere um novo documento na coleção `colecao_blocos`
        #       com os dados do bloco.
        # O documento contém o nome do bloco e a quantidade de vagas.
        colecao_blocos.insert_one({"nome": nome, "quantidade": qtd_int})

        # Chama a função `criar_vagas` para gerar as vagas
        #       associadas a esse bloco
        # A função recebe como parâmetros o nome do bloco e a
        #       quantidade de vagas a serem criadas
        criar_vagas(nome, qtd_int)

        # Exibe uma mensagem informando que o bloco foi cadastrado
        #       com sucesso e que as vagas foram geradas
        messagebox.showinfo("Sucesso",
                            "Bloco cadastrado e vagas geradas!",
                            parent=janela)

        # Atualiza a lista de blocos na interface, chamando a
        #       função responsável por recarregar os dados
        carregar_lista()

        # Limpa os campos do formulário para permitir um novo
        #       cadastro sem interferência de dados anteriores
        limpar_campos()


    # Define a função `criar_vagas` para criar vagas de
    #       estacionamento associadas a um bloco específico.
    # `bloco`: Nome do bloco onde as vagas serão criadas.
    # `qtd`: Número total de vagas a serem criadas.
    def criar_vagas(bloco, qtd):

        # Remove todas as vagas existentes associadas ao bloco
        #       informado antes de criar novas.
        # `delete_many({"bloco": bloco})` apaga todas as vagas que
        #       pertencem ao bloco para evitar duplicação.
        colecao_vagas.delete_many({"bloco": bloco})

        # Loop para criar a quantidade de vagas especificada.
        # `range(1, qtd + 1)`: Gera números de 1 até `qtd`,
        #       garantindo a sequência das vagas.
        for i in range(1, qtd + 1):

            # Insere uma nova vaga no banco de dados.
            # `insert_one()` adiciona um novo documento contendo as informações da vaga.
            # `"bloco": bloco` associa a vaga ao bloco correspondente.
            # `"numero_vaga": str(i)` define um número sequencial para
            #       cada vaga (convertido para string).
            # `"status": "Livre"` indica que a vaga está disponível para uso imediato.
            colecao_vagas.insert_one({
                "bloco": bloco,
                "numero_vaga": str(i),
                "status": "Livre"
            })


    # Define a função para alterar um bloco existente
    # `def alterar():` indica que essa função será chamada ao
    #       alterar um bloco selecionado na tabela.
    def alterar():

        # Obtém a linha selecionada na tabela de blocos
        # `selecionado = tabela_blocos.selection()` armazena a seleção do usuário.
        selecionado = tabela_blocos.selection()

        # Verifica se algum bloco foi selecionado
        # `if not selecionado:` impede que a alteração
        #       prossiga se nada for selecionado.
        if not selecionado:

            # Exibe uma mensagem de erro caso nenhum bloco tenha sido selecionado.
            # `messagebox.showerror("Erro", "Selecione um bloco para
            #       alterar!", parent=janela)` informa o usuário sobre a necessidade de seleção.
            messagebox.showerror("Erro",
                                 "Selecione um bloco para alterar!",
                                 parent=janela)

            # Encerra a função sem continuar a execução.
            return

        # Obtém os valores da linha selecionada na tabela
        # `valores = tabela_blocos.item(selecionado[0], "values")` coleta os
        #       dados do bloco escolhido.
        valores = tabela_blocos.item(selecionado[0], "values")

        # Extrai o ID do bloco selecionado
        # `_id = valores[0]` armazena o ID para realizar a
        #       alteração correta no banco de dados.
        _id = valores[0]

        # Obtém o nome do bloco digitado no campo de entrada
        # `nome = campo_nome.get().strip()` captura o nome, removendo espaços extras.
        nome = campo_nome.get().strip()

        # Obtém a quantidade de vagas digitada no campo de entrada
        # `quantidade = campo_qtd_vagas.get().strip()` captura a quantidade,
        #       também removendo espaços extras.
        quantidade = campo_qtd_vagas.get().strip()

        # Verifica se os campos Nome e Quantidade estão preenchidos.
        # `if not nome or not quantidade:` impede que a função
        #       continue caso um dos campos esteja vazio.
        if not nome or not quantidade:

            # Exibe uma mensagem de erro informando que Nome e
            #       Quantidade são obrigatórios.
            # `messagebox.showerror("Erro", "Nome e quantidade são
            #       obrigatórios!", parent=janela)` exibe o alerta dentro da janela correta.
            messagebox.showerror("Erro",
                                 "Nome e quantidade são obrigatórios!",
                                 parent=janela)

            # `return` interrompe a execução da função
            #       para evitar erros futuros.
            return

        # Tenta converter a quantidade digitada para um número inteiro.
        # Usa `try-except` para capturar erros caso o
        #       usuário insira um valor inválido.
        try:

            # Converte a entrada `quantidade` para um número inteiro.
            # `qtd_int = int(quantidade)` assegura que o valor seja numérico.
            qtd_int = int(quantidade)

            # Verifica se a quantidade de vagas é menor que 1.
            # `if qtd_int < 1:` impede que o usuário cadastre um bloco sem vagas.
            if qtd_int < 1:

                # Exibe uma mensagem de erro informando que a
                #       quantidade deve ser maior que 0.
                # `messagebox.showerror("Erro", "A quantidade de vagas
                #       deve ser maior que 0!", parent=janela)` exibe um alerta apropriado.
                messagebox.showerror("Erro",
                                     "A quantidade de vagas deve ser maior que 0!",
                                     parent=janela)

                # `return` interrompe a execução da função
                #       se a quantidade for inválida.
                return

        # Captura erro caso o usuário digite um valor
        #       que não seja um número inteiro.
        # `except ValueError:` será acionado quando a
        #       conversão para inteiro falhar.
        except ValueError:

            # Exibe uma mensagem de erro informando que a quantidade
            #       precisa ser um número inteiro.
            # `messagebox.showerror("Erro", "Quantidade inválida! Digite um
            #       número inteiro.", parent=janela)` informa ao usuário que o valor digitado não é válido.
            messagebox.showerror("Erro",
                                 "Quantidade inválida! Digite um número inteiro.",
                                 parent=janela)

            # `return` interrompe a função para evitar
            #       problemas com valores inválidos.
            return

        # Atualiza o bloco existente no banco de dados.
        # `{"_id": ObjectId(_id)}` filtra o bloco pelo seu
        #       identificador único.
        # `{"$set": {"nome": nome, "quantidade": qtd_int}}` define os
        #       novos valores para Nome e Quantidade.
        colecao_blocos.update_one({"_id": ObjectId(_id)},
                                  {"$set": {"nome": nome,
                                            "quantidade": qtd_int}})

        # Chama a função `criar_vagas(nome, qtd_int)` para
        #       garantir que a quantidade de vagas do bloco esteja correta.
        criar_vagas(nome, qtd_int)

        # Exibe uma mensagem informando que o bloco foi atualizado com sucesso.
        # `title="Sucesso"` define o título da caixa de mensagem.
        # `message="Bloco alterado e vagas atualizadas!"` exibe o
        #       texto informativo ao usuário.
        # `parent=janela` garante que a mensagem apareça na janela correta.
        messagebox.showinfo("Sucesso",
                            "Bloco alterado e vagas atualizadas!",
                            parent=janela)

        # Atualiza a interface carregando novamente a
        #       lista de blocos na tabela.
        carregar_lista()

        # Limpa os campos de entrada para evitar que os
        #       dados do último bloco editado fiquem na tela.
        limpar_campos()


    # Define a função `excluir`, responsável por
    #       remover um bloco selecionado na tabela.
    def excluir():

        # Obtém o bloco selecionado na tabela.
        # `tabela_blocos.selection()` retorna a lista de itens selecionados.
        # Se nenhum item estiver selecionado, exibe uma mensagem de
        #       erro e interrompe a execução.
        selecionado = tabela_blocos.selection()
        if not selecionado:

            # Exibe uma mensagem de erro informando que é
            #       necessário selecionar um bloco antes de excluir.
            # `title="Erro"` define o título da mensagem.
            # `message="Selecione um bloco para excluir!"` informa o motivo da falha.
            # `parent=janela` define que a mensagem pertence à janela principal.
            messagebox.showerror("Erro",
                                 "Selecione um bloco para excluir!",
                                 parent=janela)
            return

        # Obtém os valores do item selecionado na tabela.
        # `tabela_blocos.item(selecionado[0], "values")` retorna os
        #       dados do primeiro item selecionado.
        valores = tabela_blocos.item(selecionado[0], "values")

        # Armazena o identificador único do bloco, necessário para
        #       realizar a exclusão no banco de dados.
        _id = valores[0]

        # Exclui o bloco selecionado no banco de dados.
        # `delete_one({"_id": ObjectId(_id)})` remove o documento
        #       cujo `_id` corresponde ao bloco selecionado.
        colecao_blocos.delete_one({"_id": ObjectId(_id)})

        # Exibe uma mensagem informando que o bloco foi excluído com sucesso.
        # `title="Sucesso"` define o título da mensagem.
        # `message="Bloco excluído!"` informa o usuário sobre a exclusão.
        # `parent=janela` associa a mensagem à janela principal.
        messagebox.showinfo("Sucesso",
                            "Bloco excluído!",
                            parent=janela)

        # Atualiza a tabela para refletir a remoção do bloco.
        # `carregar_lista()` recarrega os dados na interface.
        carregar_lista()

        # Limpa os campos de entrada para evitar inconsistências na interface.
        # `limpar_campos()` remove qualquer dado que ainda esteja
        #       preenchido nos campos do formulário.
        limpar_campos()


    # Define a função `limpar_campos` para limpar os campos do
    #       formulário e remover a seleção na tabela.
    def limpar_campos():

        # Apaga o conteúdo do campo de entrada do nome do bloco.
        # `delete(0, tk.END)`: Remove qualquer texto existente no campo.
        campo_nome.delete(0, tk.END)

        # Apaga o conteúdo do campo de entrada da quantidade de vagas.
        # `delete(0, tk.END)`: Garante que o campo fique vazio para nova entrada.
        campo_qtd_vagas.delete(0, tk.END)

        # Remove a seleção na tabela de blocos.
        # `selection_remove(*tabela_blocos.selection())`: Desmarca
        #       qualquer item selecionado na tabela.
        tabela_blocos.selection_remove(*tabela_blocos.selection())


    # Define a função `preencher_campos` que será acionada ao
    #       clicar em um bloco da tabela.
    # `event`: Parâmetro que representa o evento de clique na tabela.
    def preencher_campos(event):

        # Obtém a linha selecionada na tabela de blocos.
        # `tabela_blocos.selection()`: Retorna a seleção atual da tabela.
        selecionado = tabela_blocos.selection()

        # Verifica se alguma linha foi selecionada.
        # Se nenhuma linha foi selecionada, a função encerra sem executar nada.
        if not selecionado:
            return

        # Obtém os valores da linha selecionada.
        # `tabela_blocos.item(selecionado[0], "values")`: Obtém os
        #       valores armazenados na linha selecionada.
        valores = tabela_blocos.item(selecionado[0], "values")

        # Preenche o campo de nome do bloco com o valor
        #       correspondente da linha selecionada.
        # `delete(0, tk.END)`: Remove qualquer valor existente no campo.
        # `insert(0, valores[1])`: Insere o novo valor do nome do bloco.
        campo_nome.delete(0, tk.END)
        campo_nome.insert(0, valores[1])

        # Preenche o campo de quantidade de vagas com o valor
        #       correspondente da linha selecionada.
        # `delete(0, tk.END)`: Remove qualquer valor existente no campo.
        # `insert(0, valores[2])`: Insere o novo valor da quantidade de vagas.
        campo_qtd_vagas.delete(0, tk.END)
        campo_qtd_vagas.insert(0, valores[2])


    # Cria uma lista contendo os botões e suas respectivas funções.
    # Cada tupla contém o texto a ser exibido no botão e a função correspondente.
    botoes = [

        ("✅ Cadastrar", cadastrar),  # Botão para cadastrar um novo bloco.
        ("✏️ Alterar", alterar),  # Botão para alterar um bloco existente.
        ("❌ Excluir", excluir),  # Botão para excluir um bloco.
        ("🧹 Limpar", limpar_campos)  # Botão para limpar os campos do formulário.

    ]

    # Loop para criar e posicionar os botões na interface gráfica.
    # `enumerate(botoes)`: Retorna o índice `i` e os
    #       valores `texto` e `comando` da tupla.
    for i, (texto, comando) in enumerate(botoes):

        # Cria um botão usando a biblioteca `ttk`.
        # `container_botoes`: Define o contêiner onde o botão será inserido.
        # `text=texto`: Define o texto do botão.
        # `command=comando`: Associa a função correspondente ao botão.
        # `width=15`: Define a largura do botão.
        # `.grid(row=0, column=i, padx=8, pady=5)`: Posiciona o botão na
        #       linha 0, coluna `i`, com espaçamento horizontal (`padx=8`) e vertical (`pady=5`).
        ttk.Button(container_botoes,
                   text=texto,
                   command=comando,
                   width=15).grid(row=0, column=i, padx=8, pady=5)

    # Define as colunas da tabela de blocos.
    # "ID" -> Identificador único do bloco.
    # "Nome" -> Nome do bloco cadastrado.
    # "Quantidade" -> Quantidade de vagas disponíveis no bloco.
    colunas = ("ID", "Nome", "Quantidade")

    # Cria um widget `Treeview` para exibir a lista de blocos na interface.
    # `container_principal`: Define o contêiner onde a tabela será inserida.
    # `columns=colunas`: Define as colunas que a tabela terá.
    # `show="headings"`: Oculta a primeira coluna padrão e exibe
    #       apenas os cabeçalhos das colunas definidas.
    # `height=10`: Define o número de linhas visíveis na tabela.
    tabela_blocos = ttk.Treeview(container_principal,
                                 columns=colunas,
                                 show="headings",
                                 height=10)

    # Expande a tabela para preencher todo o espaço disponível no contêiner.
    # `fill="both"`: Faz com que a tabela preencha tanto
    #       horizontal quanto verticalmente o espaço disponível.
    # `expand=True`: Permite que a tabela se expanda dentro do contêiner.
    # `padx=10, pady=10`: Adiciona um espaçamento interno
    #       de 10 pixels nas laterais e na parte superior/inferior.
    tabela_blocos.pack(fill="both", expand=True, padx=10, pady=10)

    # Associa um evento de duplo clique à função `preencher_campos`.
    # Sempre que um item for duplamente clicado na tabela, os
    #       dados desse item serão carregados nos campos do formulário.
    tabela_blocos.bind("<Double-1>", preencher_campos)

    # Chama a função `carregar_lista()` para preencher a tabela
    #       com os blocos armazenados no banco de dados.
    carregar_lista()

    # Inicia o loop principal da interface gráfica,
    #       garantindo que a janela permaneça aberta e interativa.
    janela.mainloop()


# -------------------------------------------------------------------------
# CRUD de Veículos (com botão HISTÓRICO)
# -------------------------------------------------------------------------

# Define a função 'tela_veiculos_crud' para gerenciar veículos na janela.
# O parâmetro 'janela_pai' recebe a janela que abrirá a
#       nova janela de gerenciamento de veículos.
def tela_veiculos_crud(janela_pai):

    # Cria uma nova janela de nível superior (Toplevel) a partir da janela pai.
    # A janela pai é passada como argumento e a nova
    #       janela será aberta como uma janela independente.
    janela = tk.Toplevel(janela_pai)

    # Define o título da janela como "Gerenciamento de Veículos".
    # Este título aparece na barra superior da janela, permitindo ao
    #       usuário identificar facilmente a janela.
    janela.title("Gerenciamento de Veículos")

    # Define o estado da janela como "zoomed", o que faz a janela ser
    #       maximizada automaticamente ao ser aberta.
    # A janela ocupará toda a área da tela disponível. "zoomed" é
    #       uma forma de maximizar a janela.
    janela.state("zoomed")

    # Configura o fundo da janela com uma cor cinza claro (#F5F5F5).
    # O código hexadecimal "#F5F5F5" define a cor de fundo da
    #       janela, que é um tom suave de cinza claro.
    # O cinza claro é uma cor neutra que promove uma interface limpa e fácil de usar.
    # Além disso, ele é suave nos olhos e não causa distração ao usuário.
    janela.configure(bg="#F5F5F5")  # Cor de fundo cinza claro (hex: #F5F5F5)

    # Container principal
    # Cria um container principal dentro da janela. O container vai
    #       armazenar todos os outros widgets dentro dele.
    # O parâmetro 'bg="#F5F5F5"' define a cor de fundo do container,
    #       utilizando a cor cinza claro.
    # O 'expand=True' faz com que o container se expanda para
    #       ocupar o máximo de espaço disponível.
    # 'fill="both"' garante que o container se estique tanto
    #       horizontal quanto verticalmente.
    container_principal = tk.Frame(janela, bg="#F5F5F5")
    container_principal.pack(expand=True, fill="both")

    # Cria um rótulo (label) para exibir o título "🚗 Gerenciar Veículos".
    # O 'text' define o texto exibido, neste caso o emoji de carro seguido do título.
    # A fonte é definida como "Arial", tamanho 22 e negrito ("bold")
    #       para tornar o título destacado.
    # 'foreground="#2E86C1"' define a cor do texto, neste caso um tom
    #       de azul claro (código hexadecimal #2E86C1).
    # 'background="#F5F5F5"' define a cor de fundo do rótulo, que é a
    #       mesma cor do fundo do container, criando uma harmonia visual.
    rotulo_titulo = ttk.Label(
        container_principal,
        text="🚗 Gerenciar Veículos",  # Define o texto do título, incluindo um emoji de carro.
        font=("Arial", 22, "bold"),  # Define a fonte do título como Arial, tamanho 22, negrito.
        foreground="#2E86C1",  # Define a cor do texto como azul claro.
        background="#F5F5F5"  # Define a cor de fundo como o mesmo cinza claro do container.
    )

    # Exibe o rótulo na tela.
    # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do rótulo,
    # garantindo que o título tenha uma boa separação dos outros elementos.
    rotulo_titulo.pack(pady=10)

    # Cria um container para o formulário dentro do container principal.
    # O container do formulário vai abrigar os campos de entrada,
    #       botões e outros elementos de interação.
    container_formulario = ttk.Frame(container_principal)

    # Exibe o container do formulário na tela.
    # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do container,
    # garantindo que o formulário não fique colado ao título ou a outros elementos.
    container_formulario.pack(pady=10)

    # Campos: Placa
    # Cria um rótulo (label) para o campo de "Placa".
    # `text="Placa:"` define o texto que será exibido no rótulo,
    #       indicando o campo para inserir a placa do veículo.
    # `font=("Arial", 12)` define a fonte como Arial com
    #       tamanho 12 para garantir boa legibilidade.
    # `row=0, column=0` posiciona o rótulo na linha 0, coluna 0 da grid.
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
    # `sticky="e"` alinha o texto à direita (East) dentro da célula da grid.
    ttk.Label(container_formulario,
              text="Placa:",
              font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (Entry) para que o usuário insira a placa do veículo.
    # `width=20` define a largura do campo de entrada para 20 caracteres.
    # `font=("Arial", 12)` define a fonte do texto dentro do campo de
    #       entrada como Arial, tamanho 12.
    # `row=0, column=1` posiciona o campo de entrada na linha 0, coluna 1
    #       da grid, ao lado do rótulo "Placa".
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
    campo_placa = ttk.Entry(container_formulario, width=20, font=("Arial", 12))
    campo_placa.grid(row=0, column=1, padx=5, pady=5)

    # Campos: Modelo
    # Cria um rótulo (label) para o campo de "Modelo".
    # `text="Modelo:"` define o texto que será exibido no rótulo,
    #       indicando o campo para inserir o modelo do veículo.
    # `font=("Arial", 12)` define a fonte como Arial com tamanho 12,
    #       garantindo boa legibilidade.
    # `row=1, column=0` posiciona o rótulo na linha 1, coluna 0 da grid.
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
    # `sticky="e"` alinha o texto à direita (East) dentro da célula da grid.
    ttk.Label(container_formulario,
              text="Modelo:",
              font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (Entry) para que o usuário insira o modelo do veículo.
    # `width=30` define a largura do campo de entrada para 30 caracteres,
    #       proporcionando um espaço adequado para modelos mais longos.
    # `font=("Arial", 12)` define a fonte do texto dentro do campo de entrada
    #       como Arial, tamanho 12, para manter a consistência.
    # `row=1, column=1` posiciona o campo de entrada na linha 1, coluna 1 da
    #       grid, ao lado do rótulo "Modelo".
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
    campo_modelo = ttk.Entry(container_formulario, width=30, font=("Arial", 12))
    campo_modelo.grid(row=1, column=1, padx=5, pady=5)

    # Campos: Cor
    # Cria um rótulo (label) para o campo de "Cor".
    # `text="Cor:"` define o texto exibido no rótulo, indicando o
    #       campo para inserir a cor do veículo.
    # `font=("Arial", 12)` define a fonte do rótulo como Arial,
    #       tamanho 12, para boa legibilidade.
    # `row=2, column=0` posiciona o rótulo na linha 2, coluna 0 da
    #       grid, abaixo dos outros campos.
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
    # `sticky="e"` alinha o texto à direita (East) dentro da célula da grid.
    ttk.Label(container_formulario,
              text="Cor:",
              font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (Entry) para que o usuário insira a cor do veículo.
    # `width=20` define a largura do campo de entrada para 20 caracteres, o
    #       que é suficiente para a cor do veículo.
    # `font=("Arial", 12)` define a fonte do texto dentro do campo de
    #       entrada como Arial, tamanho 12, para manter a consistência
    #       com os outros campos.
    # `row=2, column=1` posiciona o campo de entrada na linha 2,
    #       coluna 1 da grid, ao lado do rótulo "Cor".
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
    campo_cor = ttk.Entry(container_formulario, width=20, font=("Arial", 12))
    campo_cor.grid(row=2, column=1, padx=5, pady=5)

    # Campos: Categoria
    # Cria um rótulo (label) para o campo de "Categoria".
    # `text="Categoria:"` define o texto exibido no rótulo, indicando o
    #       campo para inserir a categoria do veículo.
    # `font=("Arial", 12)` define a fonte do rótulo como Arial,
    #       tamanho 12, para garantir boa legibilidade.
    # `row=3, column=0` posiciona o rótulo na linha 3, coluna 0 da grid,
    #       abaixo dos outros campos.
    # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
    # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
    # `sticky="e"` alinha o texto à direita (East) dentro da célula da grid.
    ttk.Label(container_formulario,
              text="Categoria:",
              font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="e")

    # Cria uma Combobox para selecionar a categoria do veículo.
    # `container_formulario` especifica o contêiner onde a combobox será exibida.
    # `values=["Carro", "Moto", "Caminhão"]` define as opções disponíveis
    #       para o usuário escolher. As opções são "Carro", "Moto" e "Caminhão".
    # `state="readonly"` garante que o usuário só pode selecionar uma
    #       opção da lista, e não digitar livremente.
    # `width=28` define a largura da Combobox para 28 caracteres,
    #       ajustando o tamanho do campo de acordo com o conteúdo.
    combo_categoria = ttk.Combobox(container_formulario,
                                    values=["Carro", "Moto", "Caminhão"],
                                    state="readonly",
                                    width=28)

    # Posiciona a Combobox na grid, na linha 3 e coluna 1,
    #       logo ao lado do rótulo "Categoria".
    # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e
    #       vertical, garantindo alinhamento com os outros campos.
    combo_categoria.grid(row=3, column=1, padx=5, pady=5)

    # Define o valor inicial da Combobox como "Carro",
    #       que é a primeira opção da lista.
    # Isso assegura que, ao abrir o formulário, a
    #       categoria "Carro" já estará selecionada.
    combo_categoria.set("Carro")

    # Campos: Proprietário (Cliente)
    # Cria um rótulo (label) para o campo "Proprietário (Cliente)".
    # `container_formulario` especifica o contêiner onde o rótulo será exibido.
    # `text="Proprietário (Cliente):"` define o texto que será
    #       exibido no rótulo, informando que este campo será para
    #       inserir o nome do proprietário (cliente).
    # `font=("Arial", 12)` define a fonte do texto, utilizando a
    #       fonte "Arial" no tamanho 12.
    # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e
    #       vertical ao redor do rótulo, garantindo que ele fique bem posicionado.
    # `sticky="e"` alinha o rótulo à direita (este alinhamento é útil
    #       quando o texto é mais longo ou você quer garantir que o texto
    #       seja bem alinhado com os outros campos).
    ttk.Label(container_formulario,
              text="Proprietário (Cliente):",
              font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de seleção (Combobox) para o "Proprietário (Cliente)".
    # `container_formulario` define o contêiner onde o Combobox será
    #       colocado, que é a área do formulário.
    # `state="readonly"` significa que o campo será somente para leitura, ou
    #       seja, o usuário não poderá digitar, apenas selecionar uma opção.
    # `width=28` define a largura do Combobox, fazendo com que ele seja
    #       suficientemente largo para exibir o nome do proprietário ou cliente de forma legível.
    combo_proprietario = ttk.Combobox(container_formulario,
                                      state="readonly",
                                      width=28)

    # Adiciona o Combobox ao layout do formulário, no qual a posição é
    #       determinada pela grade (grid).
    # `row=4, column=1` posiciona o Combobox na linha 4 e coluna 1, ou
    #       seja, ele ficará ao lado do rótulo "Proprietário (Cliente)".
    # `padx=5, pady=5` adiciona um pequeno espaço (5 pixels) de
    #       preenchimento (margem) ao redor do Combobox, tornando o layout mais agradável e espaçado.
    combo_proprietario.grid(row=4, column=1, padx=5, pady=5)

    # Função para carregar a lista de clientes no Combobox "Proprietário (Cliente)"
    # `carregar_clientes_no_combo()` é responsável por buscar todos os
    #       clientes da coleção e preencher o Combobox com o nome e CPF de cada cliente.
    def carregar_clientes_no_combo():

        # Realiza a busca de todos os documentos na coleção "colecao_clientes"
        # `colecao_clientes.find()` retorna todos os clientes cadastrados no banco de dados.
        clientes = colecao_clientes.find()

        # Cria uma lista de strings formatadas no formato "CPF - Nome",
        #       para facilitar a visualização no Combobox.
        # A list comprehension percorre todos os clientes e cria
        #       uma string no formato "cpf - nome" para cada um.
        lista_clientes = [f"{cliente['cpf']} - {cliente['nome']}" for cliente in clientes]

        # Preenche o Combobox com a lista de clientes formatada.
        # `combo_proprietario["values"]` é onde a lista de
        #       opções (clientes) será atribuída ao Combobox.
        combo_proprietario["values"] = lista_clientes

    # Chama a função para carregar os clientes no Combobox
    #       assim que a tela for carregada.
    carregar_clientes_no_combo()

    # Criação do contêiner (frame) onde os botões de CRUD (Criar,
    #       Ler, Atualizar, Excluir) serão colocados.
    # O `container_botoes` serve como um "contêiner" para
    #       organizar os botões na interface gráfica.
    container_botoes = ttk.Frame(container_principal)

    # Empacota o contêiner (frame) dos botões na interface, e
    #       define um preenchimento vertical de 10 pixels.
    # `pady=10` adiciona um espaçamento de 10 pixels ao redor do
    #       contêiner dos botões, criando um espaço visual
    #       agradável entre os elementos.
    container_botoes.pack(pady=10)


    # Função para cadastrar um novo veículo no banco de dados.
    # `cadastrar()` coleta os dados do formulário e insere um
    #       novo registro na coleção de veículos.
    def cadastrar():

        # Obtém e formata a entrada do campo "Placa".
        # `campo_placa.get()` captura o valor digitado pelo usuário.
        # `.strip()` remove espaços em branco no início e no final da string.
        # `.upper()` converte todos os caracteres para maiúsculas,
        #       garantindo que as placas fiquem padronizadas.
        placa = campo_placa.get().strip().upper()

        # Obtém e formata a entrada do campo "Modelo".
        # `.strip()` garante que espaços extras sejam removidos
        #       antes e depois do texto.
        modelo = campo_modelo.get().strip()

        # Obtém e formata a entrada do campo "Cor".
        # `.strip()` remove espaços desnecessários.
        cor = campo_cor.get().strip()

        # Obtém o valor selecionado no Combobox "Categoria".
        # `.strip()` assegura que não haja espaços em branco adicionais.
        categoria = combo_categoria.get().strip()

        # Obtém o valor selecionado no Combobox "Proprietário (Cliente)".
        # `.strip()` evita espaços desnecessários.
        proprietario = combo_proprietario.get().strip()

        # Valida se os campos obrigatórios "Placa" e "Modelo"
        #       foram preenchidos.
        # Se um desses campos estiver vazio, exibe uma
        #       mensagem de erro e interrompe o cadastro.
        if not placa or not modelo:
            messagebox.showerror("Erro",
                                 "Placa e Modelo são obrigatórios!",
                                 parent=janela)
            return

        # Insere um novo veículo na coleção do banco de dados.
        # `insert_one()` adiciona um documento com os dados informados.
        # Cada chave representa um campo armazenado no banco.
        colecao_veiculos.insert_one({
            "placa": placa,  # Armazena a placa do veículo em maiúsculas.
            "modelo": modelo,  # Armazena o modelo do veículo.
            "cor": cor,  # Armazena a cor do veículo.
            "categoria": categoria,  # Armazena a categoria do veículo (Carro, Moto, Caminhão).
            "proprietario": proprietario,  # Armazena o proprietário do veículo.
            "status": "Ativo"  # Define o status inicial do veículo como "Ativo".
        })

        # Exibe uma mensagem informando que o veículo foi cadastrado com sucesso.
        # `messagebox.showinfo()` cria uma janela de alerta com a mensagem de sucesso.
        # `parent=janela` define a janela principal como pai da mensagem.
        messagebox.showinfo("Sucesso",
                            "Veículo cadastrado com sucesso!",
                            parent=janela)

        # Atualiza a lista de veículos exibida na interface.
        # `carregar_lista()` recarrega os dados do banco e os exibe na tabela.
        carregar_lista()

        # Limpa os campos do formulário após o cadastro bem-sucedido.
        # `limpar_campos()` redefine todos os campos para seus valores padrão.
        limpar_campos()


    # Define a função para alterar um veículo cadastrado.
    def alterar():

        # Obtém o item selecionado na tabela de veículos.
        # `selection()` retorna uma lista com os
        #       identificadores dos itens selecionados.
        selecionado = tabela_veiculos.selection()

        # Verifica se algum item foi selecionado.
        # Se a lista estiver vazia, exibe uma mensagem de erro e interrompe a função.
        if not selecionado:
            messagebox.showerror("Erro",
                                 "Selecione um veículo!",
                                 parent=janela)
            return

        # Obtém os valores do item selecionado na tabela.
        # `item(selecionado[0], "values")` retorna uma tupla com os dados do veículo.
        valores = tabela_veiculos.item(selecionado[0], "values")

        # O primeiro valor da tupla corresponde ao ID do veículo no banco de dados.
        _id = valores[0]

        # Atualiza um veículo no banco de dados usando o ID selecionado
        colecao_veiculos.update_one(

            # Filtra pelo ID do veículo, convertendo a string para ObjectId
            {"_id": ObjectId(_id)},

            # Define os novos valores para os campos do veículo
            {"$set": {

                # Obtém o valor do campo de placa, remove espaços
                #       extras e converte para maiúsculas
                "placa": campo_placa.get().strip().upper(),

                # Obtém o modelo do veículo removendo espaços desnecessários
                "modelo": campo_modelo.get().strip(),

                # Obtém a cor do veículo sem espaços extras
                "cor": campo_cor.get().strip(),

                # Obtém a categoria do veículo removendo espaços extras
                "categoria": combo_categoria.get().strip(),

                # Obtém o nome do proprietário do veículo, garantindo que
                #       não haja espaços indesejados
                "proprietario": combo_proprietario.get().strip()

            }}
        )

        # Exibe uma mensagem informando que a alteração foi realizada com sucesso
        messagebox.showinfo("Sucesso", "Veículo alterado!", parent=janela)

        # Recarrega a lista de veículos para refletir as alterações na interface
        carregar_lista()

        # Limpa os campos do formulário para evitar erros em novas inserções
        limpar_campos()


    # Define uma função para excluir um veículo do banco de dados.
    def excluir():

        # Obtém a seleção do usuário na tabela de veículos.
        selecionado = tabela_veiculos.selection()

        # Verifica se algum veículo foi selecionado antes de continuar.
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um veículo!", parent=janela)
            return

        # Obtém os valores da linha selecionada na tabela de veículos.
        valores = tabela_veiculos.item(selecionado[0], "values")

        # O primeiro valor representa o ID do veículo no banco de dados.
        _id = valores[0]

        # Exibe uma caixa de diálogo de confirmação antes de excluir.
        confirmacao = messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja excluir este veículo?", parent=janela
        )

        # Se o usuário clicar em "Não", interrompe a execução da função.
        if not confirmacao:
            return

        # Remove o veículo permanentemente do banco de dados.
        colecao_veiculos.delete_one({"_id": ObjectId(_id)})

        # Exibe uma mensagem informando que o veículo foi removido com sucesso.
        messagebox.showinfo("Sucesso", "Veículo excluído do banco de dados!", parent=janela)

        # Atualiza a lista de veículos na interface gráfica para refletir as alterações.
        carregar_lista()

        # Limpa os campos do formulário após a exclusão para evitar confusão.
        limpar_campos()


    # Define uma função para limpar os campos do
    #       formulário de entrada de dados.
    def limpar_campos():

        # Remove qualquer texto digitado no campo de entrada da placa do veículo.
        # `campo_placa.delete(0, tk.END)` apaga todos os caracteres do campo.
        campo_placa.delete(0, tk.END)

        # Remove qualquer texto digitado no campo de entrada do modelo do veículo.
        # `campo_modelo.delete(0, tk.END)` apaga o conteúdo do campo.
        campo_modelo.delete(0, tk.END)

        # Remove qualquer texto digitado no campo de entrada da cor do veículo.
        # `campo_cor.delete(0, tk.END)` limpa o campo de entrada.
        campo_cor.delete(0, tk.END)

        # Redefine a seleção do campo de categoria para "Carro" como padrão.
        # `combo_categoria.set("Carro")` define o valor padrão no combobox.
        combo_categoria.set("Carro")

        # Limpa a seleção do proprietário do veículo.
        # `combo_proprietario.set("")` define o campo como vazio.
        combo_proprietario.set("")

        # Remove qualquer seleção feita na tabela de veículos.
        # `tabela_veiculos.selection()` retorna os itens selecionados.
        # `selection_remove(*tabela_veiculos.selection())` desmarca os itens selecionados.
        tabela_veiculos.selection_remove(*tabela_veiculos.selection())


    def historico():

        # Obtém a linha selecionada na `Treeview` chamada `tabela_veiculos`.
        # `selection()` retorna uma tupla contendo os identificadores das linhas selecionadas.
        selecionado = tabela_veiculos.selection()

        # Verifica se a seleção está vazia, ou seja, se nenhum veículo
        #       foi selecionado na tabela.
        # Se nada estiver selecionado, exibe uma mensagem de erro
        #       para o usuário e interrompe a execução da função.
        if not selecionado:
            messagebox.showerror("Erro",
                                 "Selecione um veículo!",
                                 parent=janela)

            # Sai da função sem executar mais nada.
            return

        # Obtém os valores do veículo selecionado na tabela.
        # `item(selecionado[0], "values")` retorna uma tupla com
        #       os valores da linha correspondente.
        valores = tabela_veiculos.item(selecionado[0], "values")

        # Extrai o **ID** do veículo da tupla de valores.
        # O **ID** é a chave primária no banco de dados.
        # O índice `0` representa o identificador único do veículo.
        _id = valores[0]

        # Extrai a **Placa** do veículo da tupla de valores.
        # A placa é um identificador importante para pesquisas e exibição.
        placa = valores[1]  # O índice `1` contém a placa do veículo.

        # Extrai o **Modelo** do veículo da tupla de valores.
        # O modelo ajuda a diferenciar veículos da mesma categoria.
        modelo = valores[2]  # O índice `2` contém o modelo do veículo.

        # Chama a função responsável por abrir a tela de histórico do veículo.
        # `tela_historico_veiculo_com_filtro` é uma função que
        #       exibe o histórico do veículo selecionado.
        # Essa função recebe como parâmetros:
        #  - `janela`: A janela principal, usada como janela mãe da nova tela.
        #  - `placa`: A placa do veículo selecionado.
        #  - `modelo`: O modelo do veículo selecionado.
        tela_historico_veiculo_com_filtro(janela, placa, modelo)



    # Define uma função chamada `preencher_campos` que será chamada
    #       quando o usuário selecionar um item na tabela de veículos.
    # Essa função tem o objetivo de preencher os campos do formulário
    #       com os dados do veículo selecionado.
    def preencher_campos(event):

        # Obtém a linha selecionada na `Treeview` chamada `tabela_veiculos`.
        # `selection()` retorna uma tupla com os identificadores dos itens selecionados.
        selecionado = tabela_veiculos.selection()

        # Verifica se a seleção está vazia, ou seja, se nenhum
        #       veículo foi selecionado.
        # Caso não tenha sido feita nenhuma seleção, a função
        #       simplesmente retorna e não executa nenhuma ação.
        if not selecionado:
            return

        # Obtém os valores do item selecionado na tabela.
        # `item(selecionado[0], "values")` retorna uma tupla com
        #       todos os valores da linha correspondente.
        # Os valores estão ordenados de acordo com as colunas da tabela.
        valores = tabela_veiculos.item(selecionado[0], "values")

        # Atualiza o campo de entrada da **Placa** do veículo:
        # Primeiro, apaga qualquer conteúdo existente no campo `campo_placa`
        #       para garantir que o novo valor não seja adicionado ao antigo.
        campo_placa.delete(0, tk.END)

        # Depois, insere a nova informação obtida da tabela,
        #       correspondente à **Placa** do veículo selecionado.
        # O índice `1` da tupla `valores` representa a placa do veículo.
        campo_placa.insert(0, valores[1])

        # Atualiza o campo de entrada do **Modelo** do veículo:
        # Primeiro, limpa qualquer valor antigo no campo `campo_modelo`.
        campo_modelo.delete(0, tk.END)

        # Depois, insere o novo valor correspondente ao **Modelo**
        #       do veículo selecionado.
        # O índice `2` da tupla `valores` representa o modelo do veículo.
        campo_modelo.insert(0, valores[2])

        # Atualiza o campo de entrada da **Cor** do veículo:
        # Primeiro, apaga qualquer valor antigo que esteja no campo `campo_cor`.
        campo_cor.delete(0, tk.END)

        # Depois, insere o novo valor correspondente à **Cor** do veículo selecionado.
        # O índice `3` da tupla `valores` representa a cor do veículo.
        campo_cor.insert(0, valores[3])

        # Atualiza o campo **Categoria** do veículo:
        # Define o valor do `Combobox` `combo_categoria` com a categoria
        #       do veículo selecionado na tabela.
        # O índice `4` da tupla `valores` representa a categoria do veículo.
        combo_categoria.set(valores[4])

        # Atualiza o campo **Proprietário (Cliente)** do veículo:
        # Define o valor do `Combobox` `combo_proprietario` com o nome do
        #       cliente associado ao veículo selecionado.
        # O índice `5` da tupla `valores` representa o proprietário do veículo.
        combo_proprietario.set(valores[5])


    # Define uma função para carregar a lista de veículos na tabela.
    def carregar_lista():

        # Remove todos os itens da tabela de veículos antes de recarregar os dados.
        # `tabela_veiculos.get_children()` retorna todos os itens presentes na tabela.
        # `tabela_veiculos.delete(*tabela_veiculos.get_children())` apaga todos os itens.
        tabela_veiculos.delete(*tabela_veiculos.get_children())

        # Busca todos os veículos no banco de dados que não estão marcados como "Removido".
        # `colecao_veiculos.find({"status": {"$ne": "Removido"}})` retorna apenas veículos ativos.
        veiculos = colecao_veiculos.find({"status": {"$ne": "Removido"}})

        # Percorre todos os veículos encontrados no banco de dados.
        for veiculo in veiculos:

            # Insere um novo veículo na tabela.
            # `tabela_veiculos.insert("", "end", values=(...))` adiciona
            #       uma nova linha com os dados do veículo.
            tabela_veiculos.insert(

                # Parâmetro indicando que o item será inserido na raiz da árvore (sem pai).
                "",

                # Adiciona o item ao final da lista.
                "end",
                values=(
                    str(veiculo["_id"]),  # Converte o ID do veículo para string para exibição na tabela.
                    veiculo["placa"],  # Exibe a placa do veículo.
                    veiculo["modelo"],  # Exibe o modelo do veículo.
                    veiculo.get("cor", ""),  # Obtém a cor do veículo, ou usa uma string vazia caso não exista.
                    veiculo.get("categoria", "Carro"),
                    # Obtém a categoria do veículo, padrão "Carro" se não estiver presente.
                    veiculo.get("proprietario", "")  # Obtém o proprietário do veículo, se houver.
                )
            )


    # Botões CRUD + Botão Histórico
    # Lista de botões com seus respectivos textos e funções associadas
    botoes = [
        ("✅ Cadastrar", cadastrar),  # Botão para cadastrar um novo veículo
        ("✏️ Alterar", alterar),  # Botão para alterar as informações de um veículo existente
        ("❌ Excluir", excluir),  # Botão para marcar um veículo como removido
        ("🧹 Limpar", limpar_campos),  # Botão para limpar os campos de entrada
        ("📜 Histórico", historico)  # Botão para exibir o histórico do veículo selecionado
    ]

    # Percorre a lista de botões, criando cada um deles e posicionando na tela
    for i, (texto, comando) in enumerate(botoes):

        # Cria um botão usando `ttk.Button`
        # `container_botoes` -> Frame onde os botões serão inseridos
        # `text=texto` -> Define o texto do botão (exemplo: "✅ Cadastrar")
        # `command=comando` -> Define a função que será executada ao clicar no botão
        # `width=15` -> Define a largura do botão para manter um tamanho padronizado
        botao = ttk.Button(container_botoes, text=texto, command=comando, width=15)

        # Posiciona o botão dentro do `container_botoes` usando `grid()`
        # `row=0` -> Todos os botões ficarão na mesma linha
        # `column=i` -> Cada botão será colocado em uma coluna
        #       diferente (índice `i` da lista)
        # `padx=8` -> Adiciona 8 pixels de espaçamento horizontal entre os botões
        # `pady=5` -> Adiciona 5 pixels de espaçamento vertical para melhor alinhamento
        botao.grid(row=0, column=i, padx=8, pady=5)

    # Tabela de Veículos
    # Definição das colunas da tabela (Treeview)
    # A tabela terá seis colunas: "ID", "Placa", "Modelo", "Cor", "Categoria" e "Proprietário"
    colunas = ("ID", "Placa", "Modelo", "Cor", "Categoria", "Proprietário")

    # Criação da tabela (Treeview) dentro do container principal
    # `container_principal` -> Frame onde a tabela será inserida
    # `columns=colunas` -> Define as colunas da tabela com base na tupla `colunas`
    # `show="headings"` -> Oculta a primeira coluna (índice) e exibe apenas os cabeçalhos definidos
    # `height=10` -> Define a altura da tabela para exibir
    #       até 10 linhas visíveis por vez
    tabela_veiculos = ttk.Treeview(container_principal,
                                   columns=colunas,
                                   show="headings",
                                   height=10)

    # Posicionamento da tabela na tela
    # `fill="both"` -> Faz com que a tabela se expanda para ocupar
    #       toda a largura e altura do container
    # `expand=True` -> Permite que a tabela aumente de tamanho
    #       quando a janela for redimensionada
    # `padx=10, pady=10` -> Adiciona um espaçamento de 10 pixels ao redor da tabela
    tabela_veiculos.pack(fill="both", expand=True, padx=10, pady=10)

    # Cabeçalhos da tabela
    # Percorre todas as colunas definidas na tabela
    for col in colunas:

        # Define o cabeçalho de cada coluna na Treeview
        # `tabela_veiculos.heading(col, text=col, anchor="center")`
        # `col` -> Nome da coluna atual no loop
        # `text=col` -> Define o texto do cabeçalho com o nome da coluna
        # `anchor="center"` -> Alinha o texto do cabeçalho ao centro
        tabela_veiculos.heading(col, text=col, anchor="center")

        # Define a largura e o alinhamento do conteúdo dentro de cada coluna
        # `tabela_veiculos.column(col, width=150, anchor="center")`
        # `width=150` -> Define a largura da coluna como 150 pixels
        # `anchor="center"` -> Alinha o conteúdo da célula ao centro
        tabela_veiculos.column(col, width=150, anchor="center")

    # Define a largura específica para a coluna "ID"
    # `tabela_veiculos.column("ID", width=50)`
    # "ID" -> Nome da coluna que será configurada
    # `width=50` -> Define a largura da coluna "ID" como 50 pixels (menor que as outras)
    # Isso é feito porque o ID é curto e não precisa de muito espaço
    tabela_veiculos.column("ID", width=50)

    # Associa um evento de duplo clique na tabela
    # `tabela_veiculos.bind("<Double-1>", preencher_campos)`
    # "<Double-1>" -> Representa o evento de **duplo clique** do mouse
    # `preencher_campos` -> Função que será chamada quando o usuário der duplo clique
    # Esse evento permite que, ao clicar duas vezes em um item da tabela,
    # os campos do formulário sejam preenchidos automaticamente
    #       com os dados do veículo selecionado
    tabela_veiculos.bind("<Double-1>", preencher_campos)

    # Carrega a lista de veículos ao abrir a tela
    # `carregar_lista()` é chamada para preencher a tabela
    #       assim que a janela for aberta
    # Essa função busca os veículos no banco de dados e os exibe na tabela
    carregar_lista()

    # Mantém a janela aberta em um loop contínuo
    # `janela.mainloop()`
    # `mainloop()` é um método do tkinter que mantém a interface gráfica ativa,
    # permitindo interação com os botões, campos e tabelas até que o usuário a feche
    janela.mainloop()



# Define a função `tela_historico_veiculo_com_filtro` para exibir o
#       histórico de um veículo específico
# `parent` -> Janela principal (janela pai) de onde essa tela será aberta
# `placa` -> Número da placa do veículo selecionado
# `modelo` -> Nome do modelo do veículo selecionado
def tela_historico_veiculo_com_filtro(parent, placa, modelo):

    # Cria uma nova janela secundária (janela filha) que será
    #       exibida sobre a janela principal
    # `Toplevel(parent)` cria uma nova janela vinculada à principal
    janela = Toplevel(parent)

    # Define o título da janela com base na placa do veículo
    # `title(f"Histórico do Veículo {placa}")`
    # O `f""` permite formatar a string, inserindo dinamicamente a
    #       placa do veículo no título da janela
    janela.title(f"Histórico do Veículo {placa}")

    # Centraliza a janela na tela e define seu tamanho (900x600 pixels)
    # `centralizar_janela(janela, 900, 600)`
    # A função `centralizar_janela` (deve existir no código)
    #       posiciona a janela no centro da tela
    # A largura é de 900 pixels e a altura é de 600 pixels para
    #       permitir exibição confortável do histórico
    centralizar_janela(janela, 900, 600)  # Janela mais larga

    # Aplica um estilo visual padronizado à janela
    # `criar_estilo_geral(janela)` (deve estar definida em
    #       outro trecho do código)
    # Essa função pode configurar cores, fontes e estilos visuais
    #       para tornar a interface mais agradável
    criar_estilo_geral(janela)

    # Cria um container (`frame_main`) que organiza os
    #       elementos dentro da janela
    # `ttk.Frame(janela)` -> Cria um quadro dentro da janela
    #       onde os componentes serão organizados
    frame_main = ttk.Frame(janela)

    # Empacota (`pack`) o frame principal para preencher
    #       toda a área disponível na janela
    # `fill="both"` -> Expande o frame tanto na largura quanto na altura
    # `expand=True` -> Permite que o frame cresça conforme o
    #       usuário redimensiona a janela
    # `padx=10, pady=10` -> Adiciona 10 pixels de espaçamento
    #       nas bordas para não deixar tudo grudado
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Cria um rótulo (`Label`) para exibir o título da
    #       tela de histórico do veículo
    lbl_title = ttk.Label(

        # Define o `frame_main` como o container onde o rótulo será inserido
        frame_main,

        # Define o texto do rótulo com o título personalizado do histórico do veículo
        # `f"Histórico de Reservas do Veículo {placa} ({modelo})"`
        # O `f""` permite formatar dinamicamente a string, inserindo a
        #       placa e o modelo do veículo
        text=f"Histórico de Reservas do Veículo {placa} ({modelo})",

        # Define a fonte do texto do rótulo
        # `("Arial", 16, "bold")` -> Usa a fonte Arial, tamanho 16, e texto em negrito
        font=("Arial", 16, "bold"),

        # Define a cor do texto do rótulo (`foreground`)
        # `"#3F51B5"` -> Azul escuro para destacar o título
        foreground="#3F51B5"

    )

    # Exibe o rótulo na interface
    # `pack(pady=10)` -> Usa o gerenciador de layout `pack`
    # `pady=10` -> Adiciona 10 pixels de espaçamento vertical
    #       entre o rótulo e os elementos acima/abaixo
    lbl_title.pack(pady=10)

    # ---------------------------------------------------------------------
    # Frame de Filtros Principais (Data Início, Data Fim, Status)
    # ---------------------------------------------------------------------

    # Cria um `Frame` (contêiner) para os filtros de pesquisa
    frame_filtros = ttk.Frame(frame_main)

    # Exibe o `Frame` na interface usando o gerenciador de layout `pack`
    # `pady=5` adiciona um espaçamento de 5 pixels na
    #       parte superior e inferior
    frame_filtros.pack(pady=5)

    # Data Início
    # Cria um rótulo para identificar o campo de data de início.
    # `frame_filtros` define o contêiner onde o rótulo será posicionado.
    # `text="Data Início:"` especifica o texto exibido no rótulo.
    # `grid(row=0, column=0, padx=5, pady=5, sticky="e")` posiciona o rótulo na grade.
    # `row=0, column=0` coloca o rótulo na primeira linha e primeira coluna.
    # `padx=5, pady=5` adiciona espaçamento horizontal e vertical para melhor estética.
    # `sticky="e"` alinha o texto à direita para melhor alinhamento com o campo de entrada.
    ttk.Label(frame_filtros,
              text="Data Início:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada do tipo DateEntry para selecionar a data de início.
    # `frame_filtros` define o contêiner onde o campo será posicionado.
    # `date_pattern="dd/MM/yyyy"` define o formato da data no padrão brasileiro (dia/mês/ano).
    # `width=12` define a largura do campo, garantindo espaço suficiente para exibir a data.
    date_ini = DateEntry(frame_filtros, date_pattern="dd/MM/yyyy", width=12)

    # Posiciona o campo de data de início na grade da interface.
    # `row=0, column=1` coloca o campo na primeira linha e segunda coluna.
    # `padx=5, pady=5` adiciona espaçamento para separar os elementos visualmente.
    date_ini.grid(row=0, column=1, padx=5, pady=5)

    # Data Fim
    # Cria um rótulo para identificar o campo de data de fim.
    # `frame_filtros` define o contêiner onde o rótulo será posicionado.
    # `text="Data Fim:"` especifica o texto exibido no rótulo.
    # `grid(row=0, column=2, padx=5, pady=5, sticky="e")` posiciona o rótulo na grade.
    # `row=0, column=2` coloca o rótulo na primeira linha e terceira coluna.
    # `padx=5, pady=5` adiciona espaçamento horizontal e vertical para melhor estética.
    # `sticky="e"` alinha o texto à direita para melhor alinhamento com o campo de entrada.
    ttk.Label(frame_filtros,
              text="Data Fim:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada do tipo DateEntry para selecionar a data de fim.
    # `frame_filtros` define o contêiner onde o campo será posicionado.
    # `date_pattern="dd/MM/yyyy"` define o formato da data no padrão brasileiro (dia/mês/ano).
    # `width=12` define a largura do campo, garantindo espaço
    #       suficiente para exibir a data.
    date_fim = DateEntry(frame_filtros, date_pattern="dd/MM/yyyy", width=12)

    # Posiciona o campo de data de fim na grade da interface.
    # `row=0, column=3` coloca o campo na primeira linha e quarta coluna.
    # `padx=5, pady=5` adiciona espaçamento para separar os elementos visualmente.
    date_fim.grid(row=0, column=3, padx=5, pady=5)

    # Status
    # Cria um rótulo para identificar o campo de status.
    # `frame_filtros` define o contêiner onde o rótulo será posicionado.
    # `text="Status:"` especifica o texto exibido no rótulo.
    # `grid(row=0, column=4, padx=5, pady=5, sticky="e")` posiciona o rótulo na grade.
    # `row=0, column=4` coloca o rótulo na primeira linha e quinta coluna.
    # `padx=5, pady=5` adiciona espaçamento horizontal e vertical para uma melhor organização.
    # `sticky="e"` alinha o texto à direita para manter alinhamento com os campos de entrada.
    ttk.Label(frame_filtros,
              text="Status:").grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Cria um campo de seleção (Combobox) para escolher o status do veículo.
    # `frame_filtros` define o contêiner onde o combobox será posicionado.
    # `values=["", "Reservado", "Finalizado", "Cancelado", "Ocupada"]`
    #       define as opções disponíveis no dropdown.
    # `""` como primeira opção permite que o campo fique vazio inicialmente.
    # `"Reservado", "Finalizado", "Cancelado", "Ocupada"` são os possíveis status de um veículo.
    # `state="readonly"` impede que o usuário digite valores personalizados, permitindo apenas seleção.
    # `width=12` define a largura do campo para garantir que os
    #       valores sejam exibidos corretamente.
    combo_st = ttk.Combobox(frame_filtros,
                            values=["", "Reservado", "Finalizado", "Cancelado", "Ocupada"],
                            state="readonly",
                            width=12)

    # Posiciona o combobox de status na grade da interface.
    # `row=0, column=5` coloca o campo na primeira linha e sexta coluna.
    # `padx=5, pady=5` adiciona espaçamento para melhorar a organização visual.
    combo_st.grid(row=0, column=5, padx=5, pady=5)

    # Define o valor padrão do combobox como vazio
    #       para evitar seleção automática.
    combo_st.set("")

    # ---------------------------------------------------------------------
    # Frame de filtros apenas para "bloco" e "vaga"
    # ---------------------------------------------------------------------

    # Cria um contêiner para os campos de filtro adicionais.
    # `ttk.Frame(frame_main)` cria um frame dentro do contêiner principal da janela.
    # Esse frame será usado para agrupar os campos de
    #       filtro, como bloco, vaga, carro e placa.
    frame_col_filtros = ttk.Frame(frame_main)

    # Posiciona o contêiner dos filtros na interface.
    # `pady=5` adiciona espaçamento vertical para separar
    #       visualmente os filtros de outros elementos.
    frame_col_filtros.pack(pady=5)

    # Cria um rótulo (label) para o campo de filtro de bloco.
    # `text="Filtrar Bloco:"` define o texto exibido no rótulo.
    # `ttk.Label(frame_col_filtros, text="Filtrar Bloco:")` cria o rótulo dentro do frame de filtros.
    # `.grid(row=0, column=0, padx=5, pady=5, sticky="e")` posiciona o rótulo na grade.
    # `row=0` define a linha na grade.
    # `column=0` define a coluna na grade.
    # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
    # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
    ttk.Label(frame_col_filtros,
              text="Filtrar Bloco:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (entry) para permitir que o
    #       usuário insira um filtro para o bloco.
    # `ttk.Entry(frame_col_filtros, width=12)` cria um campo
    #       de entrada dentro do frame de filtros.
    # `width=12` define a largura do campo em caracteres,
    #       permitindo até 12 caracteres visíveis.
    entry_filtro_bloco = ttk.Entry(frame_col_filtros, width=12)

    # Posiciona o campo de entrada dentro do frame de filtros usando a grade.
    # `row=0` posiciona o campo na mesma linha que o rótulo correspondente.
    # `column=1` posiciona o campo na coluna seguinte ao rótulo.
    # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do campo.
    entry_filtro_bloco.grid(row=0, column=1, padx=5, pady=5)

    # Cria um rótulo (label) para o campo de filtro da vaga.
    # `text="Filtrar Vaga:"` define o texto exibido no rótulo.
    # `ttk.Label(frame_col_filtros, text="Filtrar Vaga:")` cria o
    #       rótulo dentro do frame de filtros.
    # `.grid(row=0, column=2, padx=5, pady=5, sticky="e")` posiciona o rótulo na grade.
    # `row=0` define a linha na grade.
    # `column=2` define a coluna na grade, para que o rótulo
    #       fique ao lado do rótulo anterior.
    # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
    # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
    ttk.Label(frame_col_filtros,
              text="Filtrar Vaga:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (entry) para permitir que o
    #       usuário insira um filtro para a vaga.
    # `ttk.Entry(frame_col_filtros, width=12)` cria um campo de
    #       entrada dentro do frame de filtros.
    # `width=12` define a largura do campo em caracteres,
    #       permitindo até 12 caracteres visíveis.
    entry_filtro_vaga = ttk.Entry(frame_col_filtros, width=12)

    # Posiciona o campo de entrada dentro do frame de filtros usando a grade.
    # `row=0` posiciona o campo na mesma linha que o rótulo correspondente.
    # `column=3` posiciona o campo na coluna seguinte ao rótulo.
    # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do campo.
    entry_filtro_vaga.grid(row=0, column=3, padx=5, pady=5)

    # ---------------------------------------------------------------------
    # Treeview
    # ---------------------------------------------------------------------

    # Cria um frame para conter a tabela (Treeview).
    # `ttk.Frame(frame_main)` cria um frame dentro do
    #       frame principal da janela.
    frame_tv = ttk.Frame(frame_main)

    # Posiciona o frame na janela e o expande para preencher o espaço disponível.
    # `fill="both"` faz com que o frame se expanda tanto
    #       horizontal quanto verticalmente.
    # `expand=True` permite que o frame ocupe todo o espaço
    #       disponível dentro do frame principal.
    frame_tv.pack(fill="both", expand=True)

    # Define as colunas da tabela, incluindo o valor total.
    # Cada string representa o identificador de uma coluna na Treeview.
    # "id" - Identificação única do registro.
    # "data_entrada" - Data em que o veículo entrou.
    # "hora_entrada" - Hora exata da entrada.
    # "data_saida" - Data em que o veículo saiu.
    # "hora_saida" - Hora exata da saída.
    # "bloco" - Bloco onde a vaga está localizada.
    # "vaga" - Número da vaga onde o veículo foi estacionado.
    # "status" - Status atual da reserva (ex: Reservado,
    #       Finalizado, Cancelado, Ocupada).
    # "valor_total" - Valor total cobrado pela reserva do estacionamento.
    tv_colunas = (
        "id", "data_entrada", "hora_entrada", "data_saida", "hora_saida",
        "bloco", "vaga", "status", "valor_total"
    )

    # Cria uma tabela (Treeview) para exibir os dados do histórico de reservas do veículo.
    # `ttk.Treeview(frame_tv)` cria a tabela dentro do frame criado anteriormente.
    # `columns=tv_colunas` define as colunas que a tabela terá,
    #       usando a lista previamente definida.
    # `show="headings"` remove a primeira coluna padrão do Treeview e
    #       exibe apenas os cabeçalhos personalizados.
    # `height=15` define o número de linhas visíveis antes de precisar de rolagem.
    tv = ttk.Treeview(frame_tv,
                      columns=tv_colunas,
                      show="headings",
                      height=15)

    # Posiciona a tabela dentro do frame.
    # `fill="both"` permite que a tabela ocupe todo o espaço disponível no frame.
    # `expand=True` faz com que a tabela cresça quando a janela for redimensionada.
    tv.pack(fill="both", expand=True)

    # Percorre cada coluna definida na tabela para
    #       configurar os cabeçalhos e larguras.
    for c in tv_colunas:

        # Define o nome do cabeçalho da coluna, capitalizando a
        #       primeira letra do nome da coluna.
        # `tv.heading(c, text=c.capitalize())` configura o título da
        #       coluna para ser exibido no cabeçalho da tabela.
        tv.heading(c, text=c.capitalize())

        # Define a largura de cada coluna para 110 pixels.
        # `tv.column(c, width=110)` ajusta o espaço ocupado por cada coluna na tabela.
        tv.column(c, width=110)

    # Label para mostrar total de itens e soma
    # Cria um rótulo (Label) para exibir um resumo do total de itens e soma dos valores.
    # `ttk.Label(frame_main)` cria o rótulo dentro do frame principal da janela.
    # `text="Total de itens: 0   |   Soma Valor: R$ 0,00"`
    #       define o texto inicial exibido no rótulo.
    lbl_resumo = ttk.Label(frame_main,
                           text="Total de itens: 0   |   Soma Valor: R$ 0,00")

    # Posiciona o rótulo dentro do frame principal com um
    #       espaçamento vertical de 5 pixels.
    # `pady=5` adiciona um pequeno espaço acima e abaixo do
    #       rótulo para melhor organização visual.
    lbl_resumo.pack(pady=5)


    # ---------------------------------------------------------------------
    # Função filtrar
    # ---------------------------------------------------------------------

    # Define a função `filtrar()` que será responsável por
    #       buscar e exibir os dados filtrados na tabela.
    def filtrar():

        # Remove todos os itens da Treeview antes de exibir os novos resultados.
        # `tv.delete(*tv.get_children())` garante que a tabela
        #       seja limpa antes de inserir novos dados.
        tv.delete(*tv.get_children())

        # Obtém a data de início selecionada pelo usuário no DateEntry.
        # `date_ini.get_date()` retorna um objeto do tipo `datetime.date`,
        #       que representa a data escolhida.
        di_ = date_ini.get_date()

        # Obtém a data de fim selecionada pelo usuário no DateEntry.
        # `date_fim.get_date()` retorna um objeto `datetime.date`
        #       representando a data final para o filtro.
        df_ = date_fim.get_date()

        # Obtém o status selecionado no ComboBox de status, removendo espaços extras.
        # Se o usuário não selecionar um status, a string retornada será vazia ("").
        st_ = combo_st.get().strip()

        # Cria um dicionário `query` contendo os critérios para
        #       buscar os dados no banco de dados.
        # Aqui, o critério inicial é que o campo `veiculo_placa`
        #       deve ser igual à placa do veículo selecionado.
        query = {"veiculo_placa": placa}

        # Se o usuário selecionou um status, adiciona a condição de
        #       filtro pelo status na consulta.
        if st_:
            query["status"] = st_

        # Executa a consulta no banco de dados e armazena os
        #       resultados em uma lista `docs`.
        # `colecao_reservas.find(query)` busca os registros que
        #       atendem aos critérios definidos em `query`.
        # `list(colecao_reservas.find(query))` converte os resultados da
        #       consulta em uma lista para manipulação posterior.
        docs = list(colecao_reservas.find(query))

        # Cria uma lista vazia `final_results`, que armazenará os
        #       dados formatados para exibição na tabela.
        final_results = []

        # Percorre cada documento retornado na consulta ao banco de dados.
        for r in docs:

            # Obtém a string da data de entrada do documento.
            # Se o campo "data_entrada" não existir, retorna uma string vazia ("").
            dtent_str = r.get("data_entrada", "")

            # Tenta converter a string da data de entrada para um
            #       objeto do tipo `datetime.date`.
            try:

                # Usa `datetime.strptime(dtent_str, "%d/%m/%Y")` para interpretar a
                #       string como uma data no formato "dd/mm/yyyy".
                # O método `.date()` extrai apenas a parte da data,
                #       ignorando a informação de horário.
                dtent = datetime.strptime(dtent_str, "%d/%m/%Y").date()

            except:

                # Se houver erro na conversão (por exemplo, se a
                #       string estiver vazia ou em formato incorreto),
                # define `dtent` como `None`, indicando que a data
                #       não pôde ser processada.
                dtent = None

            # Define `ok = True` para indicar que, por padrão, o
            #       registro será incluído na lista final.
            ok = True

            # Se a data de entrada foi extraída corretamente (não é `None`),
            #       verifica se ela está dentro do intervalo desejado.
            if dtent:

                # Se a data de entrada for anterior à data de início do
                #       filtro, o registro será excluído (`ok = False`).
                if dtent < di_:
                    ok = False

                # Se a data de entrada for posterior à data de fim do filtro, o
                #       registro também será excluído (`ok = False`).
                if dtent > df_:
                    ok = False

            # Se a variável `ok` ainda for `True`, o registro será
            #       considerado válido e passará por mais verificações.
            if ok:

                # Obtém o valor do campo "bloco" do documento, ou uma string vazia se não existir.
                bloco_doc = r.get("bloco", "")

                # Obtém o valor do campo "numero_vaga" do documento, ou uma string vazia se não existir.
                vaga_doc = r.get("numero_vaga", "")

                # Captura o texto digitado no campo de filtro de bloco e converte
                #       para minúsculas para facilitar a comparação.
                filtro_bloco = entry_filtro_bloco.get().strip().lower()

                # Captura o texto digitado no campo de filtro de vaga e
                #       também converte para minúsculas.
                filtro_vaga = entry_filtro_vaga.get().strip().lower()

                # Se o usuário digitou algum valor no campo de filtro de bloco:
                if filtro_bloco:

                    # Verifica se o valor digitado não está presente no bloco do
                    #       documento (caso insensitivo).
                    # Se o bloco do documento não contém o valor digitado, então o
                    #       registro não será considerado (`ok = False`).
                    if filtro_bloco not in bloco_doc.lower():
                        ok = False

                # Se o usuário digitou algum valor no campo de filtro de vaga:
                if filtro_vaga:

                    # Verifica se o valor digitado não está presente na vaga
                    #       do documento (caso insensitivo).
                    # Se a vaga do documento não contém o valor digitado, então o
                    #       registro não será considerado (`ok = False`).
                    if filtro_vaga not in vaga_doc.lower():
                        ok = False

                # Após todas as verificações, se `ok` ainda for `True`, o
                #       registro será adicionado à lista final de resultados.
                if ok:
                    final_results.append(r)

        # Insere e soma
        # Inicializa a variável `soma_valor` com 0.0 para armazenar a
        #       soma total dos valores das reservas.
        soma_valor = 0.0

        # Percorre todos os documentos filtrados armazenados na
        #       lista `final_results`.
        for d in final_results:

            # Obtém o identificador único `_id` do documento e
            #       converte para string.
            val_id = str(d["_id"])

            # Obtém a data de entrada do documento, se não existir, retorna uma string vazia.
            val_de = d.get("data_entrada", "")

            # Obtém a hora de entrada do documento, se não existir, retorna uma string vazia.
            val_he = d.get("hora_entrada", "")

            # Obtém a data de saída do documento, se não existir, retorna uma string vazia.
            val_ds = d.get("data_saida", "")

            # Obtém a hora de saída do documento, se não existir, retorna uma string vazia.
            val_hs = d.get("hora_saida", "")

            # Obtém o bloco onde a vaga está localizada, se não existir, retorna uma string vazia.
            val_bl = d.get("bloco", "")

            # Obtém o número da vaga reservada, se não existir, retorna uma string vazia.
            val_vg = d.get("numero_vaga", "")

            # Obtém o status da reserva (ex.: "Reservado", "Finalizado"), se
            #       não existir, retorna uma string vazia.
            val_st = d.get("status", "")

            # Obtém o valor total da reserva, se não existir, retorna 0.
            val_vt = d.get("valor_total", 0)

            # Verifica se `val_vt` (valor total) é um número (int ou float).
            if isinstance(val_vt, (int, float)):

                # Formata o valor total para o padrão brasileiro (milhares
                #       com ponto e decimal com vírgula).
                # Primeiro, transforma o número no formato 1.234,56.
                # Depois, substitui as vírgulas por um marcador temporário "X".
                # Em seguida, troca os pontos por vírgulas.
                # Finalmente, troca os marcadores temporários "X" por pontos.
                valor_formatado = f"{val_vt:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                # Adiciona o valor total ao somatório geral das reservas.
                soma_valor += val_vt

            else:

                # Se `val_vt` não for um número válido, define o
                #       valor formatado como "0,00".
                valor_formatado = "0,00"

            # Insere uma nova linha na tabela `tv` com os dados formatados da reserva.
            # O primeiro argumento `""` indica que o item não tem um pai (entrada na raiz).
            # `END` indica que a nova linha será adicionada no final da tabela.
            # `values=` recebe uma tupla com os valores de cada coluna da tabela.
            tv.insert("",
                      END, values=(val_id,  # ID da reserva
                                   val_de,  # Data de entrada
                                   val_he,  # Hora de entrada
                                   val_ds,  # Data de saída
                                   val_hs,  # Hora de saída
                                   val_bl,  # Bloco da vaga
                                   val_vg,  # Número da vaga
                                   val_st,  # Status da reserva
                                   valor_formatado))  # Valor total formatado em reais

        # Obtém a quantidade total de registros
        #       filtrados na lista `final_results`
        qtd = len(final_results)

        # Formata a soma total dos valores para o padrão
        #       brasileiro (milhares com ponto e decimal com vírgula).
        # Primeiro, transforma o número no formato 1.234,56.
        # Depois, substitui as vírgulas por um marcador temporário "X".
        # Em seguida, troca os pontos por vírgulas.
        # Finalmente, troca os marcadores temporários "X" por pontos.
        soma_formatada = f"{soma_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # Atualiza o rótulo `lbl_resumo` com o número total de
        #       registros e a soma total formatada.
        lbl_resumo.config(text=f"Total de itens: {qtd}   |   Soma Valor: R$ {soma_formatada}")


    # Define a função `limpar_`, responsável por resetar os
    #       campos de filtro e limpar a tabela.
    def limpar_():

        # Importa a classe `datetime` do módulo `datetime` para obter a data atual.
        from datetime import datetime

        # Define o campo de data inicial (`date_ini`) para a data atual.
        date_ini.set_date(datetime.now())

        # Define o campo de data final (`date_fim`) para a data atual.
        date_fim.set_date(datetime.now())

        # Limpa a seleção do campo de status, deixando-o vazio.
        combo_st.set("")

        # Apaga qualquer texto digitado no campo de filtro do bloco.
        entry_filtro_bloco.delete(0, END)

        # Apaga qualquer texto digitado no campo de filtro da vaga.
        entry_filtro_vaga.delete(0, END)

        # Remove todos os itens exibidos na tabela (`tv`), deixando-a vazia.
        tv.delete(*tv.get_children())

        # Atualiza o rótulo `lbl_resumo` para exibir zero
        #       itens e um valor total de R$ 0,00.
        lbl_resumo.config(text="Total de itens: 0   |   Soma Valor: R$ 0,00")


    # ---------------------------------------------------------------------
    # Botões
    # ---------------------------------------------------------------------

    # Cria um frame (`frame_btn`) dentro de `frame_main` para
    #       organizar os botões na interface.
    frame_btn = ttk.Frame(frame_main)

    # Define o preenchimento vertical (`pady=5`) para espaçamento
    #       entre o frame de botões e outros elementos.
    frame_btn.pack(pady=5)

    # Cria um botão para filtrar os resultados na tabela.
    # `text="Filtrar"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=filtrar` associa a função `filtrar` ao clique do botão.
    # `pack(side="left", padx=10)` posiciona o botão no lado
    #       esquerdo do `frame_btn` com espaçamento horizontal de 10 pixels.
    ttk.Button(frame_btn,
               text="Filtrar",
               style="MyButton.TButton",
               command=filtrar).pack(side="left", padx=10)

    # Cria um botão para limpar os filtros e redefinir os campos da tabela.
    # `text="Limpar"` define o texto exibido no botão.
    # `style="MyButton.TButton"` aplica um estilo personalizado ao botão.
    # `command=limpar_` associa a função `limpar_` ao clique do botão.
    # `pack(side="left", padx=10)` posiciona o botão no lado
    #       esquerdo do `frame_btn` com espaçamento horizontal de 10 pixels.
    ttk.Button(frame_btn,
               text="Limpar",
               style="MyButton.TButton",
               command=limpar_).pack(side="left", padx=10)

    # Executa a função `filtrar()` imediatamente após a
    #       criação dos elementos, carregando os dados iniciais da tabela.
    filtrar()


# -------------------------------------------------------------------------
# CRUD de Clientes (com botão HISTÓRICO + FILTROS)
# -------------------------------------------------------------------------

# Define a função `tela_clientes_crud(janela_pai)` que cria a
#       tela de gerenciamento de clientes.
def tela_clientes_crud(janela_pai):

    # `janela = tk.Toplevel(janela_pai)` cria uma nova janela
    #       secundária dentro da janela principal.
    # `Toplevel` é usado para criar uma nova janela sobre a existente.
    janela = tk.Toplevel(janela_pai)

    # `janela.title("Gerenciamento de Clientes")` define o título da
    #       janela como "Gerenciamento de Clientes".
    # O título aparece na barra superior da janela.
    janela.title("Gerenciamento de Clientes")

    # `janela.state("zoomed")` faz com que a janela
    #       abra em tela cheia.
    # Isso melhora a visualização dos dados.
    janela.state("zoomed")

    # `janela.configure(bg="#F5F5F5")` define a cor
    #       de fundo da janela como cinza claro.
    # Isso dá um aspecto visual mais limpo e agradável.
    janela.configure(bg="#F5F5F5")

    # Criar o container principal que armazenará todos os
    #       componentes da interface.
    # `container_principal = tk.Frame(janela, bg="#F5F5F5")` cria
    #       um frame dentro da janela.
    # `bg="#F5F5F5"` define a cor de fundo do frame, como cinza claro.
    container_principal = tk.Frame(janela, bg="#F5F5F5")

    # `container_principal.pack(expand=True, fill="both")` faz com
    #       que o frame ocupe todo o espaço disponível.
    # `expand=True` permite que o frame cresça se a janela for redimensionada.
    # `fill="both"` garante que o frame ocupe toda a largura e altura possíveis.
    container_principal.pack(expand=True, fill="both")

    # Cria um rótulo (Label) que será o título da tela de gerenciamento de clientes.
    # `Cria o rótulo dentro do frame principal.
    # `text="📋 Gerenciar Clientes"` define o texto exibido no
    # ``título, incluindo um ícone para melhor visualização.
    # `font=("Arial", 22, "bold")` define a fonte do título com tamanho 22 e em negrito.
    # `foreground="#2E86C1"` define a cor do texto como **AZUL VIVO**.
    # `background="#F5F5F5"` define a cor de fundo como **CINZA CLARO**.
    rotulo_titulo = ttk.Label(container_principal,
                              text="📋 Gerenciar Clientes",
                              font=("Arial", 22, "bold"),
                              foreground="#2E86C1",
                              background="#F5F5F5")

    # Posiciona o rótulo na interface gráfica.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels
    #       acima e abaixo do título para melhor legibilidade.
    rotulo_titulo.pack(pady=10)

    # Criar formulário de entrada
    # Cria um container (Frame) para agrupar os campos do formulário.
    # Cria um frame dentro do container principal.
    container_formulario = ttk.Frame(container_principal)

    # Posiciona o container na interface gráfica.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels
    #       acima e abaixo do formulário para melhor organização visual.
    container_formulario.pack(pady=10)

    # Cria um rótulo para o campo "Nome".
    # `text="Nome:"` define o texto exibido no rótulo.
    # `font=("Arial", 12)` define a fonte usada no
    #       rótulo como Arial, tamanho 12.
    # `grid(row=0, column=0, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na linha 0, coluna 0 com 5 pixels de espaçamento
    #       horizontal e vertical, alinhado à direita.
    ttk.Label(container_formulario,
              text="Nome:",
              font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para o nome.
    # `width=35` define a largura do campo de entrada para 35 caracteres.
    # `font=("Arial", 12)` define a fonte usada no campo de
    #       entrada como Arial, tamanho 12.
    # `grid(row=0, column=1, padx=5, pady=5)` posiciona o campo de
    #       entrada na linha 0, coluna 1 com 5 pixels de
    #       espaçamento horizontal e vertical.
    campo_nome = ttk.Entry(container_formulario, width=35, font=("Arial", 12))
    campo_nome.grid(row=0, column=1, padx=5, pady=5)

    # Cria um rótulo para o campo "CPF".
    # `text="CPF:"` define o texto exibido no rótulo.
    # `font=("Arial", 12)` define a fonte do rótulo como Arial, tamanho 12.
    # `grid(row=1, column=0, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na linha 1, coluna 0 com 5 pixels de espaçamento
    #       horizontal e vertical, alinhado à direita.
    ttk.Label(container_formulario,
              text="CPF:",
              font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para o CPF.
    # `width=25` define a largura do campo de entrada para 25 caracteres.
    # `font=("Arial", 12)` define a fonte do campo de
    #       entrada como Arial, tamanho 12.
    # `grid(row=1, column=1, padx=5, pady=5)` posiciona o campo de
    #       entrada na linha 1, coluna 1 com 5 pixels de espaçamento horizontal e vertical.
    campo_cpf = ttk.Entry(container_formulario, width=25, font=("Arial", 12))
    campo_cpf.grid(row=1, column=1, padx=5, pady=5)

    # Cria um rótulo para o campo "Telefone:".
    # `text="Telefone:"` define o texto exibido no rótulo.
    # `font=("Arial", 12)` define a fonte do rótulo como Arial, tamanho 12.
    # `grid(row=2, column=0, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na linha 2, coluna 0 com 5 pixels de espaçamento
    #       horizontal e vertical, alinhado à direita.
    ttk.Label(container_formulario,
              text="Telefone:",
              font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada para o telefone.
    # `width=25` define a largura do campo de entrada para 25 caracteres.
    # `font=("Arial", 12)` define a fonte usada no campo de
    #       entrada como Arial, tamanho 12.
    # `grid(row=2, column=1, padx=5, pady=5)` posiciona o campo de
    #       entrada na linha 2, coluna 1 com 5 pixels de
    #       espaçamento horizontal e vertical.
    campo_telefone = ttk.Entry(container_formulario, width=25, font=("Arial", 12))
    campo_telefone.grid(row=2, column=1, padx=5, pady=5)

    # Criar botões
    # Cria um container para os botões.
    # `ttk.Frame(container_principal)` cria um frame
    #       dentro do container principal.
    container_botoes = ttk.Frame(container_principal)

    # Exibe o container dos botões na interface.
    # `pack(pady=10)` posiciona o container e adiciona 10
    #       pixels de espaçamento vertical ao redor.
    container_botoes.pack(pady=10)

    # Define uma lista de botões com seus respectivos textos e comandos.
    # Cada tupla contém:
    # - O texto do botão, incluindo um ícone para facilitar a identificação.
    # - Uma função lambda que chama a função associada ao botão quando clicado.
    botoes = [
        ("✅ Cadastrar", lambda: cadastrar()),
        ("✏️ Alterar", lambda: alterar()),
        ("❌ Excluir", lambda: excluir()),
        ("🧹 Limpar", lambda: limpar_campos()),
        ("📜 Histórico", lambda: abrir_historico())
    ]

    # Itera sobre a lista de botões para criar cada botão dinamicamente.
    # `enumerate(botoes)` retorna o índice e a tupla (texto, comando) de cada botão.
    for i, (texto, comando) in enumerate(botoes):

        # Cria um botão dentro do container de botões.
        # `text=texto` define o texto exibido no botão.
        # `style="TButton"` aplica o estilo previamente configurado para os botões.
        # `command=comando` associa a função que será executada ao clicar no botão.
        # `width=15` define a largura do botão.
        btn = ttk.Button(container_botoes,
                         text=texto,
                         style="TButton",
                         command=comando,
                         width=15)

        # Posiciona o botão na grade do container.
        # `row=0` posiciona o botão na linha 0.
        # `column=i` posiciona o botão na coluna correspondente ao seu índice.
        # `padx=8` adiciona 8 pixels de espaçamento horizontal ao redor do botão.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do botão.
        btn.grid(row=0, column=i, padx=8, pady=5)

    # Criar um container para a tabela dentro da janela principal
    # `ttk.Frame(container_principal)` cria um novo
    #       container (ou 'frame') que ficará dentro do container principal.
    # O 'container_principal' é o container maior onde
    #       todos os outros elementos serão posicionados.
    # `fill="both"` faz com que o frame ocupe tanto a largura
    #       quanto a altura do espaço disponível.
    # `expand=True` faz com que o frame se expanda para
    #       preencher qualquer espaço restante no layout.
    # `padx=10` e `pady=10` adicionam um espaçamento de 10 pixels
    #       nas direções horizontal e vertical, respectivamente, para
    #       evitar que o conteúdo fique muito colado nas bordas da janela.
    container_tabela = ttk.Frame(container_principal)
    container_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    # Define as colunas da tabela que será exibida
    # A variável `colunas` é uma tupla que define os títulos das colunas na tabela.
    # Cada elemento da tupla será uma coluna na tabela.
    # Neste caso, temos quatro colunas: "ID", "Nome", "CPF" e "Telefone".
    colunas = ("ID", "Nome", "CPF", "Telefone")

    # Cria a tabela para exibição dos dados dos clientes
    # `ttk.Treeview(container_tabela)` cria um widget Treeview
    #       dentro do `container_tabela`.
    # `columns=colunas` especifica quais colunas serão exibidas na
    #       tabela, utilizando os nomes definidos na variável `colunas`.
    # `show="headings"` faz com que a tabela mostre apenas os
    #       cabeçalhos das colunas, sem a coluna de índice (como
    #       uma numeração automática de linhas).
    # `height=10` define que a tabela exibirá até 10 linhas
    #       visíveis de uma vez (sem contar com a rolagem).
    tabela_clientes = ttk.Treeview(container_tabela,
                                   columns=colunas,
                                   show="headings", height=10)

    # Exibe a tabela no layout, ocupando o espaço disponível no container
    # `fill="both"` faz com que a tabela ocupe tanto a largura
    #       quanto a altura do espaço disponível.
    # `expand=True` faz com que a tabela se expanda para
    #       preencher o espaço restante dentro do `container_tabela`.
    tabela_clientes.pack(fill="both", expand=True)

    # Loop que percorre cada coluna definida na variável `colunas`
    # A variável `colunas` contém os títulos das colunas e, com o loop `for`,
    # será aplicada uma configuração em cada uma das colunas da tabela.
    for coluna in colunas:

        # Define o texto exibido no cabeçalho de cada coluna
        # `tabela_clientes.heading(coluna, text=coluna, anchor="center")`
        # configura o título de cada coluna. A variável `coluna` (que é
        #       cada um dos itens em `colunas`)
        #       será usada como título da coluna.
        # `text=coluna` define que o título será o nome da
        #       coluna, e `anchor="center"`
        #       alinha o texto do cabeçalho no centro.
        tabela_clientes.heading(coluna, text=coluna, anchor="center")

        # Define a largura e o alinhamento das colunas
        # Configura a largura das colunas.
        # `width=150` define a largura da coluna em pixels, e `anchor="center"`
        #       alinha o conteúdo da coluna ao centro.
        tabela_clientes.column(coluna, width=150, anchor="center")

    # Ajusta a largura da coluna "ID" para 50 pixels
    # `tabela_clientes.column("ID", width=50)` define
    #       especificamente a largura da coluna "ID".
    # A largura da coluna "ID" é configurada para 50 pixels, o
    #       que é uma largura mais estreita.
    tabela_clientes.column("ID", width=50)

    # Vincula um evento de duplo clique para chamar a
    #       função `ao_clicar` quando uma célula for clicada
    # `tabela_clientes.bind("<Double-1>", lambda event: ao_clicar(event))`
    # associa o evento de duplo clique em qualquer célula da tabela à função `ao_clicar`.
    # O parâmetro `<Double-1>` representa o evento de duplo
    #       clique com o botão esquerdo do mouse.
    # Quando o usuário faz um duplo clique, a função `ao_clicar(event)` será chamada.
    tabela_clientes.bind("<Double-1>", lambda event: ao_clicar(event))


    def carregar_lista():

        # Limpa todos os itens existentes na tabela antes de carregar novos dados
        # `tabela_clientes.delete(*tabela_clientes.get_children())` remove todos os itens
        # (linhas) que já estão na tabela. Isso é feito para garantir que a tabela
        # esteja vazia antes de inserir novos dados.
        tabela_clientes.delete(*tabela_clientes.get_children())

        # Obtém todos os clientes da coleção `colecao_clientes`
        # `colecao_clientes.find()` busca todos os documentos da coleção de clientes
        # no banco de dados. Isso retorna um cursor que pode ser iterado para acessar
        # os dados de cada cliente.
        clientes = colecao_clientes.find()

        # Itera sobre todos os clientes retornados pela consulta
        # A variável `cliente` armazena os dados de cada cliente no loop
        for cliente in clientes:

            # Insere os dados do cliente na tabela
            # `tabela_clientes.insert("", "end", values=(...))` adiciona uma nova linha
            # na tabela. O primeiro parâmetro é a chave do item (usando `""` indica que
            # é uma linha principal), o segundo `"end"` coloca a linha no final da tabela.
            # O parâmetro `values` define o conteúdo das colunas na nova linha.
            # Aqui, estamos inserindo:
            # - o ID do cliente como `str(cliente["_id"])` (convertido para string)
            # - o nome do cliente, acessado com `cliente["nome"]`
            # - o CPF do cliente, acessado com `cliente["cpf"]`
            # - o telefone, com `cliente.get("telefone", "")` (usando `get` para garantir que
            #   caso o telefone não exista, seja inserido uma string vazia ao invés de um erro)
            tabela_clientes.insert("",
                                   "end",
                                   values=(str(cliente["_id"]),
                                           cliente["nome"],
                                           cliente["cpf"],
                                           cliente.get("telefone", "")))


    # Definição da função que será chamada ao clicar em um item na tabela
    # O parâmetro `evento` é passado automaticamente pelo
    #       evento de clique na tabela,
    #       mas não é utilizado diretamente nesta função.
    def ao_clicar(evento):

        # Obtém o item selecionado na tabela
        # `tabela_clientes.selection()` retorna uma lista
        #       com a chave do item selecionado.
        # Se nenhum item for selecionado, essa lista estará vazia.
        selecionado = tabela_clientes.selection()

        # Verifica se algum item foi selecionado
        # Se a lista estiver vazia (nenhum item selecionado), a
        #       função retorna e não faz nada.
        if not selecionado:
            return

        # Obtém os valores da linha selecionada
        # `tabela_clientes.item(selecionado[0], "values")` retorna os
        #       valores da linha selecionada.
        # O `selecionado[0]` é a chave do item selecionado. A função `item`
        #       retorna os valores das colunas.
        valores = tabela_clientes.item(selecionado[0], "values")

        # Desempacota os valores da linha selecionada para as
        #       variáveis `_id`, `nome`, `cpf`, e `telefone`
        # Cada valor corresponde a uma coluna da tabela (ID, Nome, CPF, Telefone).
        _id, nome, cpf, telefone = valores

        # Preenche o campo de nome com o valor selecionado
        # `campo_nome.delete(0, tk.END)` limpa o conteúdo do
        #       campo de texto `campo_nome`.
        # `campo_nome.insert(0, nome)` insere o nome do cliente no
        #       campo de texto `campo_nome`.
        campo_nome.delete(0, tk.END)
        campo_nome.insert(0, nome)

        # Preenche o campo de CPF com o valor selecionado
        campo_cpf.delete(0, tk.END)
        campo_cpf.insert(0, cpf)

        # Preenche o campo de telefone com o valor selecionado
        campo_telefone.delete(0, tk.END)
        campo_telefone.insert(0, telefone)


    # Definição da função `cadastrar` que será responsável
    #       por cadastrar um novo cliente
    def cadastrar():

        # Obtém o nome do cliente a partir do campo de entrada de texto `campo_nome`
        # O método `get()` recupera o valor inserido no campo e `strip()`
        #       remove espaços extras no início e no final.
        nome = campo_nome.get().strip()

        # Obtém o CPF do cliente a partir do campo de entrada de texto `campo_cpf`
        cpf = campo_cpf.get().strip()

        # Obtém o telefone do cliente a partir do campo de
        #       entrada de texto `campo_telefone`
        telefone = campo_telefone.get().strip()

        # Verifica se o nome ou o CPF estão vazios
        # Caso algum dos dois esteja vazio, exibe uma mensagem de
        #       erro e a função é interrompida com `return`
        if not nome or not cpf:

            # `messagebox.showerror` exibe uma janela de erro com
            #       título "Erro" e a mensagem "Nome e CPF são obrigatórios!"
            # `parent=janela` faz com que a janela de erro seja modal, ou
            #       seja, ficará sobre a janela principal (`janela`)
            messagebox.showerror("Erro",
                                 "Nome e CPF são obrigatórios!",
                                 parent=janela)

            # A função retorna sem fazer mais nada, impedindo o
            #       cadastro de clientes com campos obrigatórios vazios
            return

        # Verifica se já existe um cliente com o CPF fornecido na coleção de clientes
        if colecao_clientes.find_one({"cpf": cpf}):

            # Se um cliente com o CPF já estiver cadastrado, exibe uma mensagem de erro
            # `messagebox.showerror` exibe uma janela com título "Erro" e
            #       a mensagem "CPF já cadastrado!"
            # `parent=janela` garante que a janela de erro será exibida
            #       sobre a janela principal (`janela`)
            messagebox.showerror("Erro",
                                 "CPF já cadastrado!",
                                 parent=janela)

            # A função retorna, impedindo o cadastro de um
            #       cliente com CPF já existente
            return

        # Se o CPF não estiver cadastrado, o código prossegue com o cadastro do cliente
        # `colecao_clientes.insert_one()` insere o novo cliente na coleção de clientes
        # O dicionário contém os dados do cliente: nome, CPF e telefone
        colecao_clientes.insert_one({"nome": nome, "cpf": cpf, "telefone": telefone})

        # Exibe uma janela de informação com título "Sucesso" e a
        #       mensagem "Cliente cadastrado com sucesso!"
        # `parent=janela` garante que a janela de sucesso será
        #       exibida sobre a janela principal (`janela`)
        messagebox.showinfo("Sucesso",
                            "Cliente cadastrado com sucesso!",
                            parent=janela)

        # Atualiza a tabela para refletir o cadastro do novo cliente
        carregar_lista()

        # Limpa os campos de entrada para preparar para
        #       um novo cadastro ou edição
        limpar_campos()


    # Função para alterar os dados de um cliente existente
    def alterar():

        # Verifica se algum cliente foi selecionado na tabela
        selecionado = tabela_clientes.selection()

        # Se nenhum cliente foi selecionado, exibe uma mensagem de erro
        # `messagebox.showerror` exibe uma janela de erro com
        #       título "Erro" e a mensagem "Selecione um cliente!"
        # `parent=janela` garante que a janela de erro será
        #       exibida sobre a janela principal (`janela`)
        if not selecionado:
            messagebox.showerror("Erro",
                                 "Selecione um cliente!",
                                 parent=janela)

            # Retorna para interromper a execução da função
            return

        # Se um cliente foi selecionado, obtém os dados do cliente da tabela
        valores = tabela_clientes.item(selecionado[0], "values")

        # O primeiro valor (ID do cliente) é armazenado na variável `_id`
        _id = valores[0]

        # Obtém os dados fornecidos nos campos de
        #       entrada (nome, CPF e telefone) e os limpa
        # `strip()` remove espaços em branco no início e no final dos valores
        nome = campo_nome.get().strip()
        cpf = campo_cpf.get().strip()
        telefone = campo_telefone.get().strip()

        # Verifica se o nome ou o CPF estão vazios.
        # `if not nome or not cpf:` retorna True se qualquer um
        #       dos campos obrigatórios estiver vazio.
        if not nome or not cpf:

            # Exibe uma janela de erro informando que nome e CPF são obrigatórios.
            # `messagebox.showerror("Erro", "Nome e CPF são
            #       obrigatórios!")` exibe a janela de erro.
            # `parent=janela` define que a janela de erro será
            #       exibida sobre a janela principal.
            messagebox.showerror("Erro",
                                 "Nome e CPF são obrigatórios!",
                                 parent=janela)

            # Interrompe a execução da função e não realiza o
            #       cadastro se houver campos obrigatórios vazios.
            return

        # Atualiza os dados do cliente no banco de dados.
        # `colecao_clientes.update_one(...)` atualiza um único documento no MongoDB.
        # `{"_id": ObjectId(_id)}` encontra o cliente pelo ID,
        #       onde `_id` é convertido para ObjectId.
        # `{"$set": {"nome": nome, "cpf": cpf, "telefone": telefone}}`
        #       define os novos valores para os campos.
        colecao_clientes.update_one(

            # Condição para encontrar o cliente pelo ID.
            {"_id": ObjectId(_id)},

            # Dados a serem atualizados.
            {"$set": {"nome": nome, "cpf": cpf, "telefone": telefone}})

        # Exibe uma janela de sucesso após atualizar os dados do cliente.
        # `messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")`
        #       exibe a mensagem de sucesso.
        # `parent=janela` define que a janela de sucesso será
        #       exibida sobre a janela principal.
        messagebox.showinfo("Sucesso",
                            "Cliente atualizado com sucesso!",
                            parent=janela)

        # Chama a função `carregar_lista()` para recarregar a tabela de clientes.
        # A tabela será atualizada com as informações mais recentes após a alteração.
        carregar_lista()

        # Chama a função `limpar_campos()` para limpar os campos de entrada.
        # Isso prepara os campos para o próximo uso, seja
        #       para cadastrar ou alterar outro cliente.
        limpar_campos()


    # Define a função 'excluir', que será chamada quando o
    #       usuário desejar excluir um cliente.
    def excluir():

        # Verifica se algum item foi selecionado na tabela.
        # `tabela_clientes.selection()` retorna a linha selecionada na
        #       tabela, se houver uma seleção.
        # Se nenhum item for selecionado, a lista ficará vazia.
        selecionado = tabela_clientes.selection()

        # Se não houver seleção (ou seja, a lista 'selecionado' está
        #       vazia), exibe uma mensagem de erro.
        # O usuário precisa selecionar um cliente antes de prosseguir.
        if not selecionado:

            # `messagebox.showerror()` exibe uma janela de erro com o
            #       título "Erro" e a mensagem fornecida.
            # `parent=janela` faz com que a janela de erro seja
            #       exibida sobre a janela principal da aplicação.
            messagebox.showerror("Erro",
                                 "Selecione um cliente!",
                                 parent=janela)

            # A função é interrompida com 'return' caso nenhum
            #       cliente tenha sido selecionado.
            return

        # Obtém os valores da linha selecionada na tabela.
        # `tabela_clientes.item(selecionado[0], "values")` retorna os
        #       valores (dados) da linha selecionada.
        # `selecionado[0]` é o identificador do item selecionado.
        valores = tabela_clientes.item(selecionado[0], "values")

        # O primeiro valor retornado pelos 'valores' é o ID do cliente,
        #       que é armazenado na variável `_id`.
        # Esse ID será utilizado para localizar o cliente no banco de
        #       dados e proceder com a exclusão.
        _id = valores[0]

        # Exibe uma caixa de confirmação perguntando se o usuário tem
        #       certeza de que deseja excluir o cliente.
        # `messagebox.askyesno()` cria uma janela com botões "Sim" e
        #       "Não" para o usuário escolher.
        # Se o usuário clicar em "Sim", a função retorna True,
        #       permitindo a execução do código de exclusão.
        if messagebox.askyesno("Confirmação",
                               "Tem certeza que deseja excluir este cliente?",
                               parent=janela):

            # Exclui o cliente da coleção do banco de dados usando `delete_one()`.
            # A função `ObjectId(_id)` converte o valor de `_id` (string)
            #       para o formato exigido pelo MongoDB (ObjectId).
            # `colecao_clientes.delete_one()` irá excluir o cliente que
            #       corresponde ao ID fornecido.
            colecao_clientes.delete_one({"_id": ObjectId(_id)})

            # Exibe uma janela de sucesso após a exclusão do cliente.
            # `messagebox.showinfo()` exibe uma caixa de mensagem com o
            #       título "Sucesso" e a mensagem informando que o cliente foi excluído.
            # `parent=janela` indica que a janela de sucesso será exibida
            #       sobre a janela principal da aplicação.
            messagebox.showinfo("Sucesso",
                                "Cliente excluído com sucesso!",
                                parent=janela)

            # Atualiza a lista exibida na tabela chamando a função `carregar_lista()`.
            # Essa função é responsável por recarregar a tabela
            #       com os dados mais recentes após a exclusão.
            carregar_lista()

            # Limpa os campos de entrada de texto após a exclusão do cliente.
            # A função `limpar_campos()` é chamada para garantir que os
            #       campos de nome, CPF e telefone fiquem vazios.
            limpar_campos()


    # Define a função `limpar_campos()`, que é responsável por
    #       limpar os campos de entrada de dados.
    def limpar_campos():

        # Limpa o conteúdo do campo de texto `campo_nome`:
        # `campo_nome.delete(0, tk.END)` remove qualquer texto
        #       presente no campo `campo_nome`.
        # O método `delete()` recebe dois parâmetros: o primeiro (`0`)
        #       indica o índice inicial (início do campo), e o
        #       segundo (`tk.END`) indica o índice final (final do campo), ou
        #       seja, apaga todo o conteúdo do campo.
        campo_nome.delete(0, tk.END)

        # Limpa o conteúdo do campo de texto `campo_cpf`:
        # Da mesma forma que o campo `campo_nome`, `campo_cpf.delete(0, tk.END)`
        #       apaga todo o texto do campo `campo_cpf`.
        campo_cpf.delete(0, tk.END)

        # Limpa o conteúdo do campo de texto `campo_telefone`:
        # Aqui, o mesmo processo é aplicado ao campo `campo_telefone`,
        #       removendo qualquer valor que o usuário tenha digitado.
        campo_telefone.delete(0, tk.END)

        # Remove qualquer seleção feita na tabela `tabela_clientes`:
        # `tabela_clientes.selection_remove(*tabela_clientes.selection())`
        #       remove a seleção atual na tabela de clientes.
        # `tabela_clientes.selection()` retorna uma lista de itens
        #       selecionados, e `selection_remove()` limpa a seleção.
        tabela_clientes.selection_remove(*tabela_clientes.selection())


    # Define a função `abrir_historico()` que é responsável
    #       por abrir a tela de histórico do cliente.
    def abrir_historico():

        # Obtém o item selecionado na tabela `tabela_clientes`:
        # `tabela_clientes.selection()` retorna uma lista com os
        #       IDs dos itens selecionados na tabela.
        # Se não houver nenhum item selecionado, `selecionado` será uma lista vazia.
        selecionado = tabela_clientes.selection()

        # Verifica se algum cliente foi selecionado na tabela:
        # Caso não haja nenhum item selecionado, exibe uma mensagem de erro.
        # `messagebox.showerror()` cria uma janela de erro com o
        #       título "Erro" e a mensagem "Selecione um cliente!".
        if not selecionado:
            messagebox.showerror("Erro",
                                 "Selecione um cliente!",
                                 parent=janela)

            # Se não houver seleção, a função é interrompida.
            return

        # Recupera os dados do cliente selecionado:
        # `tabela_clientes.item(selecionado[0], "values")` retorna os
        #       valores da linha selecionada.
        # O primeiro valor (`_id`) é o ID do cliente, seguido pelo nome, CPF e
        #       telefone (que são ignorados neste caso com `_`).
        valores = tabela_clientes.item(selecionado[0], "values")
        _id, nome, cpf, _ = valores

        # Chama a função `tela_historico_cliente_com_filtro()`, passando a
        #       janela, o CPF e o nome do cliente:
        # Esta função abre uma nova tela para exibir o
        #       histórico do cliente selecionado.
        tela_historico_cliente_com_filtro(janela, cpf, nome)

    # Chama a função `carregar_lista()` para atualizar a tabela
    #       com os dados mais recentes dos clientes.
    carregar_lista()

    # Inicia o loop principal da interface gráfica da janela:
    # `janela.mainloop()` mantém a janela aberta,
    #       aguardando a interação do usuário.
    janela.mainloop()


# Define a função 'tela_historico_cliente_com_filtro' que recebe três parâmetros:
# 'parent' é a janela principal que servirá de base para a nova janela,
# 'cpf_cliente' contém o CPF do cliente cujo histórico será exibido,
# 'nome_cliente' contém o nome do cliente para personalização do título da janela.
def tela_historico_cliente_com_filtro(parent, cpf_cliente, nome_cliente):

    # Cria uma nova instância de janela do tipo Toplevel, que é uma janela secundária
    # associada à janela principal (passada como 'parent'). Essa janela é independente,
    # permitindo que seja manipulada separadamente da janela principal.
    janela = Toplevel(parent)

    # Define o título da janela recém-criada. A mensagem utiliza o nome do cliente,
    # fornecendo um contexto personalizado para o usuário, por exemplo: "Histórico do Cliente João".
    janela.title(f"Histórico do Cliente {nome_cliente}")

    # Ajusta o estado da janela para "zoomed", o que faz com que ela seja maximizada,
    # ocupando toda a área de exibição disponível na tela do usuário.
    janela.state("zoomed")

    # Aplica um conjunto de estilos e configurações visuais à janela, utilizando
    # a função 'criar_estilo_geral'. Essa função, que deve ter sido definida previamente,
    # padroniza a aparência da interface, definindo fontes, cores, espaçamentos, etc.
    criar_estilo_geral(janela)

    # Cria um frame principal que servirá como contêiner para os componentes
    #      da interface dentro da janela.
    # `ttk.Frame(janela)` cria um novo frame dentro da janela principal `janela`,
    #      permitindo organizar os elementos de forma estruturada.
    # `frame_main.pack(fill="both", expand=True, padx=10, pady=10)` posiciona o frame
    #      dentro da janela e define suas propriedades de layout.
    # O parâmetro `fill="both"` permite que o frame ocupe todo o espaço
    #      disponível tanto na largura quanto na altura.
    # `expand=True` faz com que o frame se expanda conforme a janela é
    #      redimensionada, garantindo um ajuste dinâmico.
    # `padx=10` e `pady=10` adicionam 10 pixels de espaçamento ao redor do frame,
    #      criando uma margem para evitar que os elementos fiquem colados nas bordas.
    frame_main = ttk.Frame(janela)
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)

    # Título da tela, incluindo nome e CPF do cliente
    # Cria um rótulo (`Label`) que será utilizado como título da tela.
    # `ttk.Label(frame_main, ...)` cria um rótulo dentro do `frame_main`, garantindo
    #      que ele fique alinhado com os outros elementos da interface.
    # `text=f"Histórico de Reservas do Cliente {nome_cliente} (CPF: {cpf_cliente})"` define o texto do rótulo,
    # utilizando f-strings para inserir dinamicamente o nome e CPF do cliente,
    #      tornando o título personalizado.
    # `font=("Arial", 16, "bold")` define a fonte do texto como Arial,
    #      tamanho 16 e em negrito (`bold`),
    #      tornando o título mais destacado para facilitar a leitura.
    # `foreground="#3F51B5"` define a cor do texto como um tom de azul (`#3F51B5`),
    #      garantindo contraste e um visual profissional.
    # `lbl_title.pack(pady=10)` posiciona o rótulo na tela com `pack()`, utilizando `pady=10`
    # para adicionar um espaçamento vertical de 10 pixels entre o título e os elementos abaixo dele.
    lbl_title = ttk.Label(frame_main,
                          text=f"Histórico de Reservas do Cliente {nome_cliente} (CPF: {cpf_cliente})",
                          font=("Arial", 16, "bold"),
                          foreground="#3F51B5")
    lbl_title.pack(pady=10)

    # =========================================================================
    # Frame de Filtros (Data e Status)
    # =========================================================================

    # Cria um frame (`frame_filtros`) dentro do `frame_main`, que será
    #      responsável por organizar os campos de filtro.
    frame_filtros = ttk.Frame(frame_main)

    # Posiciona o frame na interface usando o método `pack()`,
    #      garantindo que ele seja exibido corretamente.
    # O parâmetro `pady=5` adiciona um espaçamento vertical de 5 pixels,
    #      separando este frame dos demais elementos da tela.
    frame_filtros.pack(pady=5)

    # ==================================================================
    # Filtro: Data Início
    # ==================================================================

    # Cria um rótulo (`Label`) para indicar o campo de filtro "Data Início".
    # Esse rótulo será exibido ao lado do campo de seleção de data,
    #      ajudando o usuário a identificar sua função.
    lbl_di = ttk.Label(frame_filtros, text="Data Início:")

    # Posiciona o rótulo na grade (`grid`) do `frame_filtros`.
    # `row=0` e `column=0` indicam que o rótulo será inserido na primeira
    #      linha e na primeira coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical de 5 pixels ao redor do rótulo.
    # `sticky="e"` alinha o texto do rótulo à direita dentro da célula,
    #      garantindo que ele fique próximo ao campo de entrada.
    lbl_di.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada de data (`DateEntry`) para permitir que o
    #      usuário selecione a data inicial do filtro.
    # O campo será posicionado ao lado do rótulo "Data Início".
    # `date_pattern="dd/MM/yyyy"` define o formato de exibição da data
    #      como "dia/mês/ano" (padrão brasileiro).
    # `width=12` define a largura do campo para comportar a data no
    #      formato especificado, garantindo uma boa apresentação.
    date_ini = DateEntry(frame_filtros, date_pattern="dd/MM/yyyy", width=12)

    # Posiciona o campo de entrada de data na grade (`grid`) dentro do `frame_filtros`.
    # `row=0` e `column=1` indicam que o campo será inserido na
    #      primeira linha e na segunda coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical
    #      de 5 pixels ao redor do campo, garantindo espaçamento adequado.
    date_ini.grid(row=0, column=1, padx=5, pady=5)

    # ==================================================================
    # Filtro: Data Fim
    # ==================================================================

    # Cria um rótulo (`Label`) para indicar o campo de filtro "Data Fim".
    # Esse rótulo será exibido ao lado do campo de seleção de data final,
    #      ajudando o usuário a identificar sua função.
    lbl_df = ttk.Label(frame_filtros, text="Data Fim:")

    # Posiciona o rótulo na grade (`grid`) dentro do `frame_filtros`.
    # `row=0` e `column=2` indicam que o rótulo será inserido na
    #      primeira linha e na terceira coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical de 5 pixels ao
    #      redor do rótulo, garantindo espaçamento adequado.
    # `sticky="e"` alinha o texto do rótulo à direita dentro da célula,
    #      posicionando-o próximo ao campo de entrada de data.
    lbl_df.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada de data (`DateEntry`) para permitir que o
    #      usuário selecione a data final do filtro.
    # O campo será posicionado ao lado do rótulo "Data Fim".
    # `date_pattern="dd/MM/yyyy"` define o formato de exibição da data
    #      como "dia/mês/ano" (padrão brasileiro).
    # `width=12` define a largura do campo para comportar a data no
    #      formato especificado, garantindo uma boa apresentação.
    date_fim = DateEntry(frame_filtros, date_pattern="dd/MM/yyyy", width=12)

    # Posiciona o campo de entrada de data na grade (`grid`) dentro do `frame_filtros`.
    # `row=0` e `column=3` indicam que o campo será inserido na primeira
    #      linha e na quarta coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical de 5 pixels ao
    #      redor do campo, garantindo espaçamento adequado.
    date_fim.grid(row=0, column=3, padx=5, pady=5)

    # ==================================================================
    # Filtro: Status
    # ==================================================================

    # Cria um rótulo (`Label`) para indicar o campo de filtro "Status".
    # Esse rótulo será exibido ao lado do menu suspenso (Combobox) para
    #      que o usuário possa selecionar o status desejado.
    lbl_st = ttk.Label(frame_filtros, text="Status:")

    # Posiciona o rótulo na grade (`grid`) dentro do `frame_filtros`.
    # `row=0` e `column=4` indicam que o rótulo será inserido na primeira
    #      linha e na quinta coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical de 5 pixels
    #      ao redor do rótulo, garantindo um espaçamento adequado.
    # `sticky="e"` alinha o texto do rótulo à direita dentro da célula,
    #      posicionando-o corretamente em relação ao campo de seleção.
    lbl_st.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Cria um menu suspenso (`Combobox`) para permitir a seleção do status da reserva.
    # O `Combobox` restringe as opções de entrada para evitar erros de digitação.
    # `values=["", "Reservado", "Finalizado", "Cancelado", "Ocupada"]` define a
    #      lista de opções disponíveis no menu suspenso.
    # A primeira opção é uma string vazia (`""`), permitindo que o usuário não
    #      selecione nenhum status caso deseje visualizar todos os registros.
    # `state="readonly"` impede que o usuário digite valores manualmente,
    #      limitando a escolha apenas às opções predefinidas.
    # `width=12` define a largura do `Combobox` para garantir que as
    #      opções sejam exibidas corretamente sem cortar o texto.
    combo_st = ttk.Combobox(frame_filtros,
                            values=["", "Reservado", "Finalizado", "Cancelado", "Ocupada"],
                            state="readonly",
                            width=12)

    # Posiciona o menu suspenso (`Combobox`) dentro da grade (`grid`) do `frame_filtros`.
    # `row=0` e `column=5` indicam que o `Combobox` será inserido na
    #      primeira linha e na sexta coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical
    #      de 5 pixels ao redor do `Combobox`,
    #      garantindo um alinhamento adequado e uma aparência organizada.
    combo_st.grid(row=0, column=5, padx=5, pady=5)

    # Define o valor inicial do `Combobox` como uma opção vazia.
    # Isso garante que, ao abrir a tela, o campo de status não esteja pré-selecionado,
    # permitindo que o usuário visualize todas as opções sem um filtro aplicado por padrão.
    combo_st.set("")

    # ==================================================================
    # Frame para Filtros Adicionais (Bloco, Vaga, Carro e Placa)
    # ==================================================================

    # Cria um novo frame (`frame_col_filtros`) dentro do `frame_main`.
    # Esse frame será responsável por organizar os filtros adicionais,
    #      como bloco, vaga, carro e placa.
    frame_col_filtros = ttk.Frame(frame_main)

    # Posiciona o `frame_col_filtros` dentro do `frame_main` utilizando o método `pack()`.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels entre
    #      este frame e os demais elementos,
    #      garantindo um layout bem distribuído.
    frame_col_filtros.pack(pady=5)

    # ==================================================================
    # Filtro: Bloco
    # ==================================================================

    # Cria um rótulo (`Label`) para indicar o campo de filtro "Bloco".
    # Esse rótulo será exibido ao lado do campo de entrada onde o
    #      usuário poderá digitar o bloco desejado.
    # `text="Filtrar Bloco:"` define o texto exibido no rótulo, tornando a
    #      funcionalidade clara para o usuário.
    ttk.Label(frame_col_filtros,
              text="Filtrar Bloco:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (`Entry`) para que o usuário possa inserir
    #      manualmente um valor para o filtro de bloco.
    # `frame_col_filtros` define o local onde o campo de entrada será
    #      posicionado dentro da interface.
    # `width=15` define a largura do campo de entrada, permitindo a
    #      digitação de textos de tamanho adequado.
    entry_filtro_bloco = ttk.Entry(frame_col_filtros, width=15)

    # Posiciona o campo de entrada na grade (`grid`) dentro do `frame_col_filtros`.
    # `row=0` e `column=1` indicam que o campo será inserido na primeira
    #      linha e na segunda coluna do frame.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical
    #      de 5 pixels ao redor do campo,
    #      garantindo um alinhamento adequado e um visual organizado.
    entry_filtro_bloco.grid(row=0, column=1, padx=5, pady=5)

    # ==================================================================
    # Filtro: Vaga
    # ==================================================================

    # Cria um rótulo (`Label`) dentro do frame `frame_col_filtros`
    #      para indicar o campo de filtro "Vaga".
    # Esse rótulo será exibido à esquerda do campo de entrada onde o
    #      usuário poderá digitar o número da vaga desejada.
    # `text="Filtrar Vaga:"` define o texto exibido no rótulo, deixando claro
    #      que este campo serve para filtrar vagas específicas.
    # O rótulo ajuda o usuário a entender qual tipo de informação
    #      deve ser inserida no campo ao lado.
    ttk.Label(frame_col_filtros,
              text="Filtrar Vaga:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (`Entry`) para que o usuário possa inserir
    #      manualmente um valor para o filtro de vaga.
    # O campo de entrada permitirá a digitação do número da vaga que o
    #      usuário deseja visualizar na tabela.
    # `frame_col_filtros` é o contêiner onde o campo será posicionado,
    #      garantindo que ele esteja dentro da seção de filtros.
    # `width=15` define a largura do campo de entrada, garantindo que
    #      ele tenha um tamanho adequado para acomodar números de vagas
    #      sem que fiquem cortados ou ultrapassem o limite de exibição.
    entry_filtro_vaga = ttk.Entry(frame_col_filtros, width=15)

    # Posiciona o campo de entrada na grade (`grid`) dentro do `frame_col_filtros`,
    #      garantindo uma organização estruturada.
    # `row=0` e `column=3` indicam que o campo será inserido na primeira
    #      linha e na quarta coluna do frame, garantindo o alinhamento
    #      correto ao lado do rótulo correspondente.
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical
    #      de 5 pixels ao redor do campo, garantindo que ele não fique muito
    #      próximo dos outros elementos e
    #      tenha um visual organizado.
    # O espaçamento melhora a usabilidade, facilitando a leitura e a
    #      interação do usuário com os filtros.
    entry_filtro_vaga.grid(row=0, column=3, padx=5, pady=5)

    # ==================================================================
    # Filtro: Carro (Modelo)
    # ==================================================================

    # Cria um rótulo (`Label`) dentro do frame `frame_col_filtros`
    #      para indicar o campo de filtro "Carro".
    # Esse rótulo será exibido à esquerda do campo de entrada, ajudando o
    #      usuário a entender que este filtro é destinado à busca de
    #      veículos com base no modelo do carro.
    # `text="Filtrar Carro:"` define o texto exibido no rótulo,
    #      deixando claro que o usuário deve inserir o nome ou parte do
    #      modelo do carro para realizar a filtragem na tabela.
    # O uso do rótulo melhora a acessibilidade e a experiência do
    #      usuário, tornando o layout mais intuitivo.
    ttk.Label(frame_col_filtros,
              text="Filtrar Carro:").grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (`Entry`) que permitirá ao usuário
    #      inserir manualmente um valor
    # para filtrar os registros de veículos com base no modelo do carro.
    # O usuário pode digitar um modelo completo ou parte do nome do
    #      carro para refinar os resultados na tabela.
    # `frame_col_filtros` define que esse campo pertence ao
    #      contêiner de filtros adicionais.
    # `width=15` define a largura do campo de entrada, garantindo
    #      espaço suficiente para a digitação de nomes de modelos de
    #      veículos sem comprometer a legibilidade.
    # Esse tamanho foi definido para balancear a usabilidade e o
    #      espaço disponível na interface.
    entry_filtro_carro = ttk.Entry(frame_col_filtros, width=15)

    # Posiciona o campo de entrada na grade (`grid`) dentro do `frame_col_filtros`,
    # garantindo uma organização estruturada do layout.
    # `row=0` e `column=5` indicam que o campo será inserido na primeira
    #      linha e na sexta coluna do frame, garantindo o alinhamento correto ao
    #      lado do rótulo correspondente "Filtrar Carro:".
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical
    #      de 5 pixels ao redor do campo, melhorando o espaçamento entre os
    #      elementos e evitando que fiquem muito próximos uns dos outros.
    # Esse espaçamento contribui para um layout mais organizado e fácil de usar.
    entry_filtro_carro.grid(row=0, column=5, padx=5, pady=5)

    # ==================================================================
    # Filtro: Placa
    # ==================================================================

    # Cria um rótulo (`Label`) dentro do frame `frame_col_filtros`
    #      para indicar o campo de filtro "Placa".
    # Esse rótulo será posicionado à esquerda do campo de entrada,
    #      permitindo que o usuário compreenda que esse filtro é
    #      destinado à busca de veículos com base na placa.
    # `text="Filtrar Placa:"` define o texto exibido no rótulo,
    #      deixando claro que o usuário deve inserir parte ou a placa
    #      completa do veículo para realizar a filtragem na tabela.
    # Esse rótulo melhora a usabilidade e torna a interface mais intuitiva.
    ttk.Label(frame_col_filtros,
              text="Filtrar Placa:").grid(row=0, column=6, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (`Entry`) que permitirá ao usuário
    #      inserir manualmente uma placa de veículo
    #      para filtrar os registros na tabela. O usuário pode digitar a
    #      placa completa ou apenas uma parte dela
    #      para encontrar veículos correspondentes.
    # `frame_col_filtros` define que esse campo pertence ao
    #      contêiner de filtros adicionais.
    # `width=15` define a largura do campo de entrada, garantindo
    #      espaço suficiente para a digitação de placas de veículos sem
    #      comprometer a visibilidade ou a experiência do usuário.
    # Esse tamanho foi ajustado para balancear o espaço disponível na
    #      interface e manter a harmonia do layout.
    entry_filtro_placa = ttk.Entry(frame_col_filtros, width=15)

    # Posiciona o campo de entrada na grade (`grid`) dentro do `frame_col_filtros`,
    # garantindo uma estrutura organizada e alinhada com os demais filtros.
    # `row=0` e `column=7` indicam que o campo será inserido na primeira
    #      linha e na oitava coluna do frame, garantindo seu correto
    #      alinhamento ao lado do rótulo "Filtrar Placa:".
    # `padx=5, pady=5` adicionam espaçamentos horizontal e vertical
    #      de 5 pixels ao redor do campo, evitando que ele fique muito
    #      próximo de outros elementos e melhorando a distribuição visual.
    # Esse espaçamento proporciona uma interface mais
    #      organizada e agradável para o usuário.
    entry_filtro_placa.grid(row=0, column=7, padx=5, pady=5)

    # ==================================================================
    # Criação da Área da Tabela (Treeview)
    # ==================================================================

    # Cria um frame (`frame_tv`) dentro do `frame_main`, que será responsável
    # por conter a tabela de exibição dos dados (Treeview).
    # Esse frame serve como um contêiner para melhor organização e
    #      manipulação da tabela na interface.
    frame_tv = ttk.Frame(frame_main)

    # Posiciona o frame da tabela (`frame_tv`) dentro do `frame_main`,
    #      utilizando o método `pack()`.
    # `fill="both"` faz com que o frame ocupe todo o espaço disponível,
    #      tanto na largura quanto na altura.
    # `expand=True` permite que o frame cresça conforme a janela for
    #      redimensionada, garantindo uma interface flexível.
    frame_tv.pack(fill="both", expand=True)

    # ==================================================================
    # Definição das Colunas da Tabela (Treeview)
    # ==================================================================

    # Cria uma tupla (`tv_colunas`) contendo os nomes das colunas que
    #      serão exibidas na tabela.
    # Cada string dentro da tupla representa uma coluna da tabela,
    #      permitindo a exibição estruturada dos dados.
    # As colunas incluem informações relevantes, como ID, datas,
    #      horários, veículo e status da reserva.
    tv_colunas = (
        "id", "data_entrada", "hora_entrada", "data_saida", "hora_saida",
        "bloco", "vaga", "veiculo", "tipo", "placa", "status", "valor_total"
    )

    # ==================================================================
    # Criação da Tabela (Treeview)
    # ==================================================================

    # Cria a tabela (`Treeview`) dentro do `frame_tv`, onde os
    #      dados serão exibidos de forma tabular.
    # `columns=tv_colunas` define que a tabela terá as colunas
    #      especificadas na tupla `tv_colunas`.
    # `show="headings"` garante que apenas os títulos das colunas
    #      sejam exibidos,
    # ocultando a primeira coluna padrão do Treeview, que normalmente
    #      exibe um índice hierárquico.
    # `height=20` define que a tabela exibirá até 20 linhas por vez,
    #      antes de precisar de rolagem vertical.
    tv = ttk.Treeview(frame_tv,
                      columns=tv_colunas,
                      show="headings",
                      height=20)

    # Posiciona a tabela (`tv`) dentro do `frame_tv` utilizando o método `pack()`.
    # `fill="both"` faz com que a tabela ocupe todo o espaço disponível,
    #      garantindo que os dados sejam exibidos corretamente.
    # `expand=True` permite que a tabela se ajuste ao redimensionamento da
    #      janela, garantindo flexibilidade na interface.
    tv.pack(fill="both", expand=True)

    # Dicionário com os títulos dos cabeçalhos para cada coluna
    cabecalhos = {
        "id": "ID",
        "data_entrada": "Data Entrada",
        "hora_entrada": "Hora Entrada",
        "data_saida": "Data Saída",
        "hora_saida": "Hora Saída",
        "bloco": "Bloco",
        "vaga": "Vaga",
        "veiculo": "Veículo",
        "tipo": "Tipo",
        "placa": "Placa",
        "status": "Status",
        "valor_total": "Valor Total (R$)"
    }

    # ==================================================================
    # Configuração das Colunas da Tabela (Treeview)
    # ==================================================================

    # Percorre todas as colunas definidas na tupla `tv_colunas`, aplicando
    #      configurações individuais para cada uma delas.
    # O objetivo desse laço `for` é definir os títulos (cabeçalhos) e
    #      ajustar a largura de cada coluna da tabela.
    for c in tv_colunas:

        # Define o título do cabeçalho da coluna, utilizando um
        #      dicionário chamado `cabecalhos`.
        # Esse dicionário contém os nomes formatados das colunas para
        #      melhor legibilidade na interface.
        # `tv.heading(c, text=cabecalhos[c])` configura o nome da
        #      coluna na interface, garantindo que
        #      o título correto seja exibido no cabeçalho da tabela.
        tv.heading(c, text=cabecalhos[c])

        # Define a largura padrão para cada coluna da tabela.
        # `tv.column(c, width=110)` ajusta o tamanho da coluna
        #      para 110 pixels, garantindo que os dados
        # fiquem visíveis sem ficarem muito espremidos ou muito espaçados.
        # Esse valor pode ser ajustado conforme necessário para
        #      diferentes resoluções de tela.
        tv.column(c, width=110)

    # ==================================================================
    # Rótulo de Resumo (Total de Itens e Soma dos Valores)
    # ==================================================================

    # Cria um rótulo (`Label`) que exibirá um resumo das informações filtradas na tabela.
    # O rótulo conterá o total de registros exibidos e a soma total dos valores, facilitando
    # a análise dos dados pelo usuário.
    # `text="Total de itens: 0   |   Soma Valor: R$ 0,00"` define um valor inicial para o rótulo,
    # indicando que nenhum item foi carregado ainda e que o total está zerado.
    lbl_resumo = ttk.Label(frame_main,
                           text="Total de itens: 0   |   Soma Valor: R$ 0,00")

    # Posiciona o rótulo de resumo (`lbl_resumo`) na interface
    #      utilizando o método `pack()`.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels, separando o
    #      rótulo dos demais elementos da tela,
    #      garantindo que ele fique bem visível e não colado na tabela.
    lbl_resumo.pack(pady=5)

    # ==================================================================
    # Função para Filtrar os Dados na Tabela
    # ==================================================================

    # Define a função `filtrar()`, que será responsável por aplicar os filtros
    # definidos pelo usuário e exibir os resultados filtrados na tabela (Treeview).
    def filtrar():

        # --------------------------------------------------------------
        # Limpeza da Tabela Antes da Inserção dos Novos Dados
        # --------------------------------------------------------------

        # Remove todos os itens atualmente exibidos na tabela
        #      antes de carregar novos resultados.
        # `tv.get_children()` retorna uma lista com todos os itens da tabela.
        # `tv.delete(*tv.get_children())` deleta todos os registros da tabela de uma vez,
        # garantindo que os novos dados exibidos sejam apenas aqueles
        #      que atendem aos filtros aplicados.
        tv.delete(*tv.get_children())

        # --------------------------------------------------------------
        # Captura dos Valores dos Filtros
        # --------------------------------------------------------------

        # Obtém os valores inseridos pelo usuário nos campos de filtro para
        #      serem utilizados na busca dos dados.
        # Esses valores serão comparados com os registros do banco de
        #      dados ou coleção de dados.

        # Captura as datas selecionadas nos widgets `DateEntry` para os
        #      filtros de intervalo de datas.
        # Os widgets `DateEntry` retornam um objeto do tipo `date`, que
        #      será utilizado para comparação com as datas dos registros.
        filtro_data_ini = date_ini.get_date()  # Data de início do filtro
        filtro_data_fim = date_fim.get_date()  # Data final do filtro

        # Captura o valor selecionado no `Combobox` de Status.
        # `combo_st.get().strip()` obtém o valor do filtro removendo
        #      espaços extras antes e depois do texto.
        filtro_status = combo_st.get().strip()  # Status do filtro (exemplo: "Reservado", "Finalizado")

        # Captura os valores digitados nos campos de texto para os filtros adicionais.
        # `strip().lower()` é aplicado para remover espaços extras e
        #      converter o texto para minúsculas, tornando a comparação
        #      entre valores insensível a maiúsculas e minúsculas.

        filtro_bloco = entry_filtro_bloco.get().strip().lower()  # Filtro pelo Bloco
        filtro_vaga = entry_filtro_vaga.get().strip().lower()  # Filtro pelo Número da Vaga
        filtro_carro = entry_filtro_carro.get().strip().lower()  # Filtro pelo Modelo do Veículo
        filtro_placa = entry_filtro_placa.get().strip().lower()  # Filtro pela Placa do Veículo

        # --------------------------------------------------------------
        # Consulta ao Banco de Dados para Buscar as Reservas do Cliente
        # --------------------------------------------------------------

        # Define o critério de consulta para buscar todas as reservas
        #      pertencentes ao cliente especificado.
        # O filtro é aplicado utilizando o CPF do cliente (`cpf_cliente`),
        #      garantindo que apenas as reservas
        #      desse cliente sejam recuperadas.
        query = {"cliente_cpf": cpf_cliente}

        # Executa a consulta no banco de dados para encontrar todas as
        #      reservas que correspondem ao CPF do cliente.
        # `colecao_reservas.find(query)` retorna um cursor com os registros encontrados.
        # `list(colecao_reservas.find(query))` converte esse cursor em
        #      uma lista de dicionários,
        #      onde cada dicionário representa uma reserva do cliente.
        docs = list(colecao_reservas.find(query))

        # Inicializa a variável `soma_valor` com 0.0 para acumular o valor
        #      total das reservas do cliente.
        # Essa variável será usada posteriormente para exibir o total dos
        #      valores das reservas filtradas.
        soma_valor = 0.0

        # --------------------------------------------------------------
        # Iteração Sobre os Registros Encontrados
        # --------------------------------------------------------------

        # Percorre cada documento (reserva) retornado pela consulta ao banco de dados.
        # Cada reserva contém diversas informações que serão extraídas e processadas.
        for d in docs:

            # Obtém o identificador único da reserva (ID).
            # O campo `_id` é uma chave primária no banco de dados MongoDB.
            # O `get("_id", "")` garante que, caso o campo não exista,
            #      seja retornada uma string vazia.
            # O valor é convertido para string (`str()`) para facilitar a
            #      exibição na interface.
            val_id = str(d.get("_id", ""))

            # Obtém as informações de data e hora de entrada da reserva.
            # `get("data_entrada", "")` retorna a data de entrada da reserva.
            # Caso o campo não exista, retorna uma string vazia (`""`).
            val_de = d.get("data_entrada", "")
            val_he = d.get("hora_entrada", "")

            # Obtém as informações de data e hora de saída da reserva.
            # `get("data_saida", "")` retorna a data de saída da reserva.
            # Caso o campo não exista, retorna uma string vazia (`""`).
            val_ds = d.get("data_saida", "")
            val_hs = d.get("hora_saida", "")

            # Obtém o bloco onde a reserva foi realizada.
            # `get("bloco", "")` retorna o bloco da reserva.
            # Caso o campo não exista, retorna uma string vazia (`""`).
            val_bl = d.get("bloco", "")

            # Obtém o número da vaga associada à reserva.
            # `get("numero_vaga", "")` retorna o número da vaga.
            # Caso o campo não exista, retorna uma string vazia (`""`).
            val_vg = d.get("numero_vaga", "")

            # Obtém o status da reserva.
            # `get("status", "")` retorna o status da reserva,
            #      como "Reservado", "Finalizado" ou "Cancelado".
            # Caso o campo não exista, retorna uma string vazia (`""`).
            val_st = d.get("status", "")

            # Obtém o valor total da reserva.
            # `get("valor_total", 0)` retorna o valor total da reserva.
            # Caso o campo não exista, o valor padrão será `0`.
            val_vt = d.get("valor_total", 0)

            # Obtém a placa do veículo associado à reserva.
            # `get("veiculo_placa", "")` retorna a placa do veículo.
            # Caso o campo não exista, retorna uma string vazia (`""`).
            veiculo_placa = d.get("veiculo_placa", "")

            # =========================================================================
            # Filtro por intervalo de datas
            # =========================================================================

            # --------------------------------------------------------------
            # Validação da Data de Entrada da Reserva
            # --------------------------------------------------------------

            # Verifica se o campo `val_de` (Data de Entrada) contém algum valor.
            # Isso é necessário para evitar erros ao tentar converter um
            #      valor nulo ou inválido.
            if val_de:

                try:

                    # Converte a string `val_de` (ex: "15/03/2028") para um objeto de data (`date`).
                    # `datetime.strptime(val_de, "%d/%m/%Y").date()` realiza a conversão utilizando o
                    # formato de data brasileiro (dia/mês/ano).
                    # Se a conversão for bem-sucedida, a variável `data_entrada_obj`
                    #      conterá um objeto de data válido.
                    data_entrada_obj = datetime.strptime(val_de, "%d/%m/%Y").date()

                except ValueError:

                    # Caso ocorra um erro na conversão (ex: formato inválido),
                    #      define `data_entrada_obj` como `None`.
                    # Isso evita que o código tente comparar uma data inválida
                    #      com os filtros, prevenindo falhas.
                    data_entrada_obj = None

                # --------------------------------------------------------------
                # Aplicação do Filtro de Data
                # --------------------------------------------------------------

                # Se a conversão da data foi bem-sucedida (`data_entrada_obj` não é `None`),
                # verifica se a data está dentro do intervalo selecionado pelo usuário nos filtros.
                if data_entrada_obj:

                    # Se a `data_entrada_obj` for menor que `filtro_data_ini` ou maior que `filtro_data_fim`,
                    # significa que a reserva não está dentro do intervalo especificado.
                    # O comando `continue` faz com que a reserva seja ignorada e o
                    #      loop avance para o próximo registro.
                    if data_entrada_obj < filtro_data_ini or data_entrada_obj > filtro_data_fim:
                        continue

            # =========================================================================
            # Filtro por Status
            # =========================================================================

            # Verifica se o usuário selecionou um status no filtro (`filtro_status`).
            # Se `filtro_status` não estiver vazio e for diferente do status da reserva (`val_st`),
            # significa que a reserva não corresponde ao critério de busca.
            # `filtro_status.lower() != val_st.lower()` é usado para garantir que a comparação
            # seja insensível a maiúsculas e minúsculas.
            # Se a reserva não atender ao critério, o comando `continue`
            #      faz com que ela seja ignorada
            #      e o loop passe para o próximo registro.
            if filtro_status and filtro_status.lower() != val_st.lower():
                continue

            # =========================================================================
            # Filtro por Bloco
            # =========================================================================

            # Verifica se o usuário digitou um bloco no filtro (`filtro_bloco`).
            # Se `filtro_bloco` não estiver vazio e o bloco da reserva (`val_bl`)
            #      não contiver o valor digitado, a reserva será ignorada.
            # `filtro_bloco not in val_bl.lower()` é utilizado para
            #      comparar os valores de forma insensível a
            #      maiúsculas e minúsculas, garantindo que qualquer
            #      ocorrência do bloco digitado seja considerada.
            if filtro_bloco and filtro_bloco not in val_bl.lower():
                continue

            # =========================================================================
            # Filtro por Vaga
            # =========================================================================

            # Verifica se o usuário digitou um número de vaga no filtro (`filtro_vaga`).
            # Se `filtro_vaga` não estiver vazio e o número da vaga na reserva (`val_vg`)
            # não contiver o valor digitado, a reserva será ignorada.
            # `str(val_vg).lower()` é utilizado para converter o
            #      número da vaga em string e evitar erros,
            #      permitindo que a comparação seja feita corretamente.
            if filtro_vaga and filtro_vaga not in str(val_vg).lower():
                continue

            # =========================================================================
            # Busca informações adicionais do veículo (modelo, categoria e placa)
            # =========================================================================

            # Realiza uma consulta na coleção de veículos (`colecao_veiculos`) para obter
            # mais informações sobre o veículo associado à reserva.
            # O critério de busca utiliza a placa do veículo (`veiculo_placa`) cadastrada na reserva.
            # `find_one({"placa": veiculo_placa})` retorna um único documento (registro) correspondente.
            doc_veiculo = colecao_veiculos.find_one({"placa": veiculo_placa})

            # =========================================================================
            # Verificação do Resultado da Consulta
            # =========================================================================

            # Se um documento correspondente for encontrado (`doc_veiculo` não for `None`),
            # extrai os detalhes do veículo a partir dos campos disponíveis no banco de dados.
            if doc_veiculo:

                # Obtém o modelo do veículo.
                # `get("modelo", "Desconhecido")` retorna o valor do campo `"modelo"` caso exista.
                # Se o campo não for encontrado, retorna `"Desconhecido"` como valor padrão.
                val_veiculo = doc_veiculo.get("modelo", "Desconhecido")

                # Obtém a categoria do veículo (exemplo: "Sedan", "SUV", "Hatch").
                # Se a categoria não for encontrada no banco de dados, o
                #      valor padrão `"Desconhecido"` será usado.
                val_tipo = doc_veiculo.get("categoria", "Desconhecido")

                # Obtém a placa do veículo.
                # Se o campo `"placa"` não existir no documento, retorna `"Desconhecido"`.
                val_placa = doc_veiculo.get("placa", "Desconhecido")

            # Caso o veículo não seja encontrado no banco de dados,
            #      define valores padrão indicando
            #      que a informação não está disponível.
            else:

                # Define `"Não Encontrado"` para o modelo do veículo.
                val_veiculo = "Não Encontrado"

                # Define `"Não Encontrado"` para a categoria do veículo.
                val_tipo = "Não Encontrado"

                # Como a placa já está armazenada na variável `veiculo_placa`, usa-se esse valor,
                # garantindo que, mesmo sem informações no banco de dados, a
                #      placa da reserva seja mantida.
                val_placa = veiculo_placa

            # =========================================================================
            # Filtro por Carro (modelo)
            # =========================================================================
            if filtro_carro and filtro_carro not in val_veiculo.lower():
                continue

            # =========================================================================
            # Filtro por Placa
            # =========================================================================
            if filtro_placa and filtro_placa not in val_placa.lower():
                continue

            # =========================================================================
            # Conversão e Formatação do Valor Total da Reserva
            # =========================================================================

            # Verifica se o valor total da reserva (`val_vt`) é um número válido.
            # `isinstance(val_vt, (int, float))` verifica se `val_vt` é do
            #      tipo `int` (inteiro) ou `float` (decimal).
            if isinstance(val_vt, (int, float)):

                # Adiciona o valor total da reserva à variável `soma_valor`,
                # que acumula o total de todas as reservas filtradas.
                soma_valor += val_vt

                # Formata o valor total para exibição na interface no formato monetário brasileiro (R$).
                # `f"{val_vt:,.2f}"` converte o número para string, separando milhares por vírgula
                # e usando ponto para indicar as casas decimais (exemplo: `1,234.56`).
                # `.replace(",", "X").replace(".", ",").replace("X", ".")` ajusta a formatação
                # para o padrão brasileiro, trocando a vírgula pelos pontos e vice-versa
                # (exemplo final: `1.234,56`).
                valor_formatado = f"{val_vt:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Se `val_vt` não for um número válido, define um valor
            #      padrão "0,00" para evitar erros.
            else:
                valor_formatado = "0,00"

            # =========================================================================
            # Inserção dos Dados na Tabela (Treeview)
            # =========================================================================

            # Insere uma nova linha na tabela (`Treeview`), adicionando os valores formatados
            # da reserva correspondente.
            # `tv.insert("", END, values=(...))` adiciona a linha no final da tabela.
            # Cada item dentro da tupla `values=(...)` representa uma coluna da tabela.
            tv.insert("", END, values=(
                val_id,  # Identificador único da reserva
                val_de,  # Data de entrada
                val_he,  # Hora de entrada
                val_ds,  # Data de saída
                val_hs,  # Hora de saída
                val_bl,  # Bloco da reserva
                val_vg,  # Número da vaga
                val_veiculo,  # Modelo do veículo associado à reserva
                val_tipo,  # Tipo do veículo (exemplo: Sedan, SUV)
                val_placa,  # Placa do veículo
                val_st,  # Status da reserva (exemplo: Reservado, Finalizado)
                valor_formatado  # Valor total formatado no padrão monetário brasileiro
            ))

        # =========================================================================
        # Atualização do Resumo (Total de Itens e Soma dos Valores)
        # =========================================================================

        # Atualiza o rótulo de resumo (`lbl_resumo`) com o número total de itens filtrados
        # e a soma total dos valores exibidos na tabela.

        # `len(tv.get_children())` retorna o número total de registros
        #      atualmente exibidos na `Treeview`.
        # Isso representa o número de reservas que atenderam aos
        #      filtros aplicados pelo usuário.

        # `soma_valor:,.2f` formata a soma total dos valores no padrão financeiro,
        # garantindo duas casas decimais e separação de milhares.
        # `.replace(".", ",")` ajusta a formatação para o padrão brasileiro,
        # onde a vírgula é usada como separador decimal.
        lbl_resumo.config(text=f"Total de itens: {len(tv.get_children())}   |   Soma Valor: R$ {soma_valor:,.2f}".replace(".", ","))

        # =========================================================================
        # Função para Limpar os Filtros e Restaurar os Valores Iniciais
        # =========================================================================


    # Define a função `limpar_()`, responsável por resetar os filtros e
    #      limpar os dados exibidos na tabela.
    def limpar_():

        # ---------------------------------------------------------------------
        # Resetando os Filtros de Data
        # ---------------------------------------------------------------------

        # Define os campos de data (`DateEntry`) para a data atual, garantindo que
        # ao limpar os filtros, o intervalo de datas seja reiniciado corretamente.

        # `date_ini.set_date(datetime.now())` ajusta a Data Início para a data do dia.
        date_ini.set_date(datetime.now())

        # `date_fim.set_date(datetime.now())` ajusta a Data Fim para a data do dia.
        date_fim.set_date(datetime.now())

        # ---------------------------------------------------------------------
        # Resetando o Filtro de Status
        # ---------------------------------------------------------------------

        # Define o campo de seleção de status (`Combobox`) como vazio.
        # `combo_st.set("")` garante que nenhuma opção de status fique selecionada.
        combo_st.set("")

        # ---------------------------------------------------------------------
        # Limpando os Campos de Texto dos Filtros
        # ---------------------------------------------------------------------

        # `entry_filtro_bloco.delete(0, END)` remove qualquer texto inserido
        #      no campo de filtro por bloco.
        entry_filtro_bloco.delete(0, END)

        # `entry_filtro_vaga.delete(0, END)` remove qualquer texto
        #      inserido no campo de filtro por vaga.
        entry_filtro_vaga.delete(0, END)

        # `entry_filtro_carro.delete(0, END)` remove qualquer texto
        #      inserido no campo de filtro por modelo de carro.
        entry_filtro_carro.delete(0, END)

        # `entry_filtro_placa.delete(0, END)` remove qualquer texto
        #      inserido no campo de filtro por placa do veículo.
        entry_filtro_placa.delete(0, END)

        # ---------------------------------------------------------------------
        # Limpando a Tabela (Treeview)
        # ---------------------------------------------------------------------

        # Remove todos os itens atualmente exibidos na `Treeview`.
        # `tv.get_children()` retorna uma lista com todos os registros da tabela.
        # `tv.delete(*tv.get_children())` deleta todos os registros,
        #      garantindo que a tabela fique vazia.
        tv.delete(*tv.get_children())

        # ---------------------------------------------------------------------
        # Resetando o Resumo de Itens e Valores
        # ---------------------------------------------------------------------

        # Atualiza o rótulo de resumo (`lbl_resumo`) para
        #      exibir "0" itens e "R$ 0,00" no total.
        # Isso garante que o resumo da tela seja reiniciado
        #      corretamente após a limpeza.
        lbl_resumo.config(text="Total de itens: 0   |   Soma Valor: R$ 0,00")



    # =========================================================================
    # Criação do Frame para os Botões de Ação (Filtrar e Limpar)
    # =========================================================================

    # Cria um frame (`frame_btn`) dentro do `frame_main` que
    #      conterá os botões de ação.
    # Esse frame é utilizado para organizar os botões e
    #      garantir um layout mais organizado.
    frame_btn = ttk.Frame(frame_main)

    # Posiciona o frame na interface utilizando `pack()`,
    #      garantindo espaçamento adequado.
    # `pady=5` adiciona um espaçamento vertical de 5 pixels,
    #      separando os botões dos outros elementos da tela.
    frame_btn.pack(pady=5)

    # =========================================================================
    # Botão para Aplicar o Filtro
    # =========================================================================

    # Cria um botão para acionar a função `filtrar()`, responsável por
    #      aplicar os filtros selecionados pelo usuário.
    # `text="Filtrar"` define o texto exibido no botão, informando sua funcionalidade.
    # `command=filtrar` associa o clique do botão à execução da função `filtrar()`.
    ttk.Button(frame_btn, text="Filtrar", command=filtrar).pack(

        # `side="left"` alinha o botão à esquerda dentro do `frame_btn`.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os botões.
        side="left", padx=10

    )

    # =========================================================================
    # Botão para Limpar os Filtros
    # =========================================================================

    # Cria um botão para acionar a função `limpar_()`, que redefine todos os
    #      filtros e limpa os resultados exibidos na tabela.
    # `text="Limpar"` define o texto exibido no botão, deixando claro que
    #      sua função é restaurar a tela ao estado inicial.
    # `command=limpar_` associa o clique do botão à execução da função `limpar_()`.
    ttk.Button(frame_btn, text="Limpar", command=limpar_).pack(

        # `side="left"` alinha o botão à esquerda dentro do `frame_btn`, ao
        #      lado do botão "Filtrar".
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels entre os
        #      botões para evitar que fiquem muito próximos.
        side="left", padx=10
    )

    # Chama a função filtrar ao iniciar a tela para
    #      exibir os dados iniciais
    filtrar()



# -------------------------------------------------------------------------
# CRUD de Usuários
# -------------------------------------------------------------------------

# Define a função para criar a tela de gerenciamento de usuários.
# `tela_usuarios_crud(janela_pai)` recebe a janela
#       principal como argumento.
def tela_usuarios_crud(janela_pai):

    # Cria uma nova janela para o CRUD de usuários.
    # `tk.Toplevel(janela_pai)` cria a janela como filha da
    #       janela principal, caso exista.
    # Se `janela_pai` for None, `tk.Tk()` cria
    #       uma nova janela independente.
    janela = tk.Toplevel(janela_pai) if janela_pai else tk.Tk()

    # Define o título da janela.
    # `title("Gerenciamento de Usuários")` exibe o nome da janela no topo.
    janela.title("Gerenciamento de Usuários")

    # Define as dimensões da janela.
    # `largura=850` define a largura da janela em 850 pixels.
    # `altura=550` define a altura da janela em 550 pixels.
    largura, altura = 850, 550

    # Chama a função para centralizar a janela na tela.
    # `centralizar_janela(janela, largura, altura)`
    #       posiciona a janela no centro da tela.
    centralizar_janela(janela, largura, altura)

    # Define a cor de fundo da janela.
    # `bg="#F5F5F5"` aplica um fundo cinza claro para um visual limpo.
    janela.configure(bg="#F5F5F5")

    # Cria o container principal da janela.
    # `tk.Frame(janela, bg="#F5F5F5")` cria um frame dentro da janela principal.
    # `bg="#F5F5F5"` define a cor de fundo do container como cinza claro.
    container_principal = tk.Frame(janela, bg="#F5F5F5")

    # Expande o container para preencher toda a janela.
    # `expand=True` faz com que o frame ocupe todo o espaço disponível.
    # `fill="both"` permite que ele seja redimensionado
    #       tanto na largura quanto na altura.
    container_principal.pack(expand=True, fill="both")

    # Cria um rótulo de título para a tela de gerenciamento de usuários.
    # `ttk.Label(container_principal, text="👤 Gerenciar Usuários")`
    #       cria um rótulo dentro do container principal.
    # `font=("Arial", 22, "bold")` define a fonte do texto
    #       como Arial, tamanho 22, em negrito.
    # `foreground="#2E86C1"` define a cor do texto como azul escuro.
    # `background="#F5F5F5"` mantém a cor de fundo igual à do container principal.
    rotulo_titulo = ttk.Label(container_principal,
                              text="👤 Gerenciar Usuários",
                              font=("Arial", 22, "bold"),
                              foreground="#2E86C1",
                              background="#F5F5F5")

    # Posiciona o rótulo de título na interface.
    # `pady=10` adiciona um espaçamento vertical de 10
    #       pixels acima e abaixo do rótulo.
    rotulo_titulo.pack(pady=10)

    # Cria um container para o formulário de entrada de dados.
    # `ttk.Frame(container_principal)` cria um frame dentro do
    #       container principal para organizar os elementos do formulário.
    container_formulario = ttk.Frame(container_principal)

    # Posiciona o container do formulário na interface.
    # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e
    #       abaixo do container para melhor organização visual.
    container_formulario.pack(pady=10)

    # Cria um rótulo (label) para identificar o campo de entrada do nome de usuário.
    # `text="Nome de Usuário:"` define o texto exibido ao lado do campo.
    # `font=("Arial", 12)` define a fonte do texto como Arial, tamanho 12.
    # `grid(row=0, column=0, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na linha 0, coluna 0 da grade,
    # adiciona um espaçamento horizontal (padx=5) e vertical (pady=5),
    # e alinha o rótulo à direita da célula com `sticky="e"` (east = leste = direita).
    ttk.Label(container_formulario,
              text="Nome de Usuário:",
              font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (entry) para o usuário digitar o nome.
    # `width=30` define a largura do campo para 30 caracteres.
    # `font=("Arial", 12)` aplica a fonte Arial tamanho 12 para o texto digitado.
    campo_usuario = ttk.Entry(container_formulario,
                              width=30,
                              font=("Arial", 12))

    # Posiciona o campo de entrada na interface.
    # `grid(row=0, column=1, padx=5, pady=5)` coloca o
    #       campo de entrada na linha 0, coluna 1 da grade,
    # adicionando um espaçamento horizontal (padx=5) e
    #       vertical (pady=5) para melhor organização.
    campo_usuario.grid(row=0, column=1, padx=5, pady=5)

    # Cria um rótulo (label) para identificar o campo de entrada da senha.
    # `text="Senha:"` define o texto exibido ao lado do campo.
    # `font=("Arial", 12)` define a fonte do texto como Arial, tamanho 12.
    # `grid(row=1, column=0, padx=5, pady=5, sticky="e")`
    #       posiciona o rótulo na linha 1, coluna 0 da grade,
    # adiciona um espaçamento horizontal (padx=5) e vertical (pady=5),
    #       e alinha o rótulo à direita da célula com `sticky="e"` (east = leste = direita).
    ttk.Label(container_formulario,
              text="Senha:",
              font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de entrada (entry) para o usuário digitar a senha.
    # `width=30` define a largura do campo para 30 caracteres.
    # `show="*"` oculta os caracteres digitados, exibindo asteriscos para proteger a senha.
    # `font=("Arial", 12)` aplica a fonte Arial tamanho 12 para o texto digitado.
    campo_senha = ttk.Entry(container_formulario,
                            width=30,
                            show="*",
                            font=("Arial", 12))

    # Posiciona o campo de entrada na interface.
    # `grid(row=1, column=1, padx=5, pady=5)` coloca o
    #       campo de entrada na linha 1, coluna 1 da grade,
    #       adicionando um espaçamento horizontal (padx=5) e
    #       vertical (pady=5) para melhor organização.
    campo_senha.grid(row=1, column=1, padx=5, pady=5)

    # Cria um rótulo (label) para indicar o campo de seleção do tipo de usuário.
    # `text="Tipo de Usuário:"` define o texto exibido ao lado do campo.
    # `font=("Arial", 12)` define a fonte do texto como Arial, tamanho 12.
    # `grid(row=2, column=0, padx=5, pady=5, sticky="e")` posiciona o
    #       rótulo na linha 2, coluna 0 da grade,
    #       adiciona um espaçamento horizontal (padx=5) e vertical (pady=5),
    #       e alinha o rótulo à direita da célula com
    #       `sticky="e"` (east = leste = direita).
    ttk.Label(container_formulario,
              text="Tipo de Usuário:",
              font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")

    # Cria um campo de seleção (Combobox) para escolher o tipo de usuário.
    # `values=["Administrador", "Atendente"]` define as opções
    #       disponíveis no menu suspenso.
    # `state="readonly"` impede a digitação manual e restringe a
    #       escolha apenas às opções fornecidas.
    # `width=28` define a largura da caixa de seleção para 28 caracteres.
    selecao_tipo = ttk.Combobox(container_formulario,
                                values=["Administrador", "Atendente"],
                                state="readonly",
                                width=28)

    # Posiciona a Combobox na interface.
    # `grid(row=2, column=1, padx=5, pady=5)` coloca a
    #       caixa de seleção na linha 2, coluna 1 da grade,
    #       adicionando um espaçamento horizontal (padx=5) e
    #       vertical (pady=5) para melhor organização.
    selecao_tipo.grid(row=2, column=1, padx=5, pady=5)

    # Define um valor padrão para a Combobox.
    # `set("Atendente")` seleciona automaticamente a
    #       opção "Atendente" ao abrir o formulário.
    selecao_tipo.set("Atendente")

    # Cria um contêiner (Frame) para organizar os botões na interface.
    # `ttk.Frame(container_principal)` cria um frame
    #       dentro do contêiner principal.
    container_botoes = ttk.Frame(container_principal)

    # Posiciona o frame na tela.
    # `pack(pady=10)` adiciona um espaçamento vertical
    #       de 10 pixels ao redor do frame,
    #       garantindo um melhor espaçamento entre os elementos.
    container_botoes.pack(pady=10)

    # Lista contendo os botões do CRUD (Cadastrar, Alterar, Excluir, Limpar).
    # Cada item da lista é uma tupla, onde:
    # - O primeiro elemento é o texto do botão (incluindo um
    #       emoji para melhor visualização).
    # - O segundo elemento é uma função `lambda` que chama a
    #       função correspondente ao clicar no botão.
    botoes = [
        ("✅ Cadastrar", lambda: cadastrar()),  # Botão para cadastrar um novo usuário.
        ("✏️ Alterar", lambda: alterar()),  # Botão para alterar os dados de um usuário existente.
        ("❌ Excluir", lambda: excluir()),  # Botão para excluir um usuário do banco de dados.
        ("🧹 Limpar", lambda: limpar_campos())  # Botão para limpar os campos do formulário.
    ]

    # Loop que percorre a lista de botões e os cria dinamicamente.
    # `enumerate(botoes)` percorre a lista de botões, retornando o
    #       índice (i) e os valores (texto, comando).
    for i, (texto, comando) in enumerate(botoes):

        # Cria um botão dentro do contêiner de botões.
        # `ttk.Button(container_botoes, text=texto, style="TButton",
        #       command=comando, width=15)`
        # - `container_botoes`: Define o frame onde o botão será colocado.
        # - `text=texto`: Define o texto do botão (exemplo: "✅ Cadastrar").
        # - `style="TButton"`: Aplica o estilo configurado anteriormente no ttk.Style().
        # - `command=comando`: Define a função que será executada
        #       quando o botão for pressionado.
        # - `width=15`: Define a largura do botão.
        btn = ttk.Button(container_botoes,
                         text=texto,
                         style="TButton",
                         command=comando,
                         width=15)

        # Posiciona o botão na grade (grid).
        # `row=0`: Todos os botões ficam na mesma linha.
        # `column=i`: Define a posição do botão com base no
        #       índice da lista (cada botão em uma coluna diferente).
        # `padx=8`: Adiciona um espaçamento horizontal
        #       de 8 pixels entre os botões.
        # `pady=5`: Adiciona um espaçamento vertical
        #       de 5 pixels ao redor dos botões.
        btn.grid(row=0, column=i, padx=8, pady=5)

    # Criar o contêiner onde a tabela de usuários será exibida.
    # `ttk.Frame(container_principal)`: Cria um
    #       frame dentro do contêiner principal.
    container_tabela = ttk.Frame(container_principal)

    # Posiciona o frame na tela.
    # `fill="both"`: O frame ocupará todo o espaço disponível na horizontal e vertical.
    # `expand=True`: Permite que o frame cresça automaticamente conforme o tamanho da janela.
    # `padx=10`: Adiciona um espaçamento de 10 pixels à esquerda e à direita do frame.
    # `pady=10`: Adiciona um espaçamento de 10 pixels acima e abaixo do frame.
    container_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    # Define os nomes das colunas da tabela de usuários.
    # `("ID", "Nome de Usuário", "Senha", "Tipo de Usuário")`: São
    #       as colunas que serão exibidas na tabela.
    colunas = ("ID", "Nome de Usuário", "Senha", "Tipo de Usuário")

    # Cria a tabela (Treeview) dentro do frame `container_tabela`.
    # `ttk.Treeview(container_tabela, columns=colunas, show="headings", height=10)`
    # - `container_tabela`: Define que a tabela será colocada dentro desse frame.
    # - `columns=colunas`: Define as colunas da tabela usando a tupla `colunas`.
    # - `show="headings"`: Remove a primeira coluna vazia
    #       padrão do Treeview e exibe apenas os cabeçalhos.
    # - `height=10`: Define o número de linhas visíveis da tabela.
    tabela_usuarios = ttk.Treeview(container_tabela,
                                   columns=colunas,
                                   show="headings",
                                   height=10)

    # Posiciona a tabela dentro do contêiner.
    # `fill="both"`: Faz a tabela ocupar todo o espaço
    #       horizontal e vertical disponível dentro do contêiner.
    # `expand=True`: Permite que a tabela cresça
    #       automaticamente conforme o tamanho da janela.
    tabela_usuarios.pack(fill="both", expand=True)

    # Percorre a lista de colunas para configurar cada uma delas na tabela.
    for coluna in colunas:

        # Define o texto exibido no cabeçalho da coluna.
        # `tabela_usuarios.heading(coluna, text=coluna, anchor="center")`
        # - `coluna`: Define o nome da coluna.
        # - `text=coluna`: Usa o próprio nome da coluna como rótulo no cabeçalho.
        # - `anchor="center"`: Centraliza o texto no cabeçalho da coluna.
        tabela_usuarios.heading(coluna, text=coluna, anchor="center")

        # Configura as propriedades de cada coluna.
        # `tabela_usuarios.column(coluna, width=150, anchor="center")`
        # - `width=150`: Define a largura da coluna como 150 pixels.
        # - `anchor="center"`: Centraliza o conteúdo dentro da coluna.
        tabela_usuarios.column(coluna, width=150, anchor="center")

    # Ajusta a largura da coluna "ID" separadamente.
    # `tabela_usuarios.column("ID", width=50)`: Define a
    #       largura da coluna "ID" como 50 pixels.
    tabela_usuarios.column("ID", width=50)

    # Adiciona um evento de duplo clique na tabela.
    # `tabela_usuarios.bind("<Double-1>", lambda event: ao_clicar(event))`
    # - `<Double-1>`: Especifica que o evento ocorre ao
    #       clicar duas vezes com o botão esquerdo do mouse.
    # - `lambda event: ao_clicar(event)`: Chama a
    #       função `ao_clicar(event)` quando um item for duplamente clicado.
    tabela_usuarios.bind("<Double-1>", lambda event: ao_clicar(event))


    # Função para carregar a lista de usuários na tabela.
    def carregar_lista():

        # Remove todos os itens da tabela antes de recarregar os dados.
        # `tabela_usuarios.delete(*tabela_usuarios.get_children())`
        # - `tabela_usuarios.get_children()`: Obtém todos os itens existentes na tabela.
        # - `*`: Expande a lista retornada para remover todos os itens de uma vez.
        tabela_usuarios.delete(*tabela_usuarios.get_children())

        # Obtém todos os usuários do banco de dados.
        # `colecao_usuarios.find()`: Retorna todos os
        #       documentos da coleção "usuarios".
        usuarios = colecao_usuarios.find()

        # Percorre a lista de usuários obtidos do banco de dados.
        for usuario in usuarios:

            # Insere os dados do usuário na tabela.
            # `tabela_usuarios.insert("", "end", values=(...))`
            # - `""`: Define que o item será inserido na raiz da hierarquia (sem pai).
            # - `"end"`: Insere o item na última posição da tabela.
            # - `values=(...)`: Define os valores que serão exibidos em cada coluna.
            #     - `str(usuario["_id"])`: Converte o `_id` (identificador
            #           único do MongoDB) para string.
            #     - `usuario["usuario"]`: Obtém o nome do usuário.
            #     - `usuario["senha"]`: Obtém a senha do usuário.
            #     - `usuario["tipo"]`: Obtém o tipo de usuário (Administrador/Atendente).
            tabela_usuarios.insert("",
                                   "end",
                                   values=(str(usuario["_id"]),
                                           usuario["usuario"],
                                           usuario["senha"],
                                           usuario["tipo"]))


    # Função chamada ao clicar duas vezes em um item da tabela de usuários.
    def ao_clicar(evento):

        # Obtém o item selecionado na tabela.
        # `tabela_usuarios.selection()`: Retorna uma lista com os
        #       identificadores dos itens selecionados.
        selecionado = tabela_usuarios.selection()

        # Verifica se algum item foi selecionado.
        # Caso não tenha sido, a função retorna sem fazer nada.
        if not selecionado:
            return

        # Obtém os valores do item selecionado.
        # `tabela_usuarios.item(selecionado[0], "values")`
        # - `selecionado[0]`: Pega o primeiro item
        #       selecionado (caso haja múltiplos, considera apenas um).
        # - `"values"`: Obtém os valores armazenados no item da tabela.
        valores = tabela_usuarios.item(selecionado[0], "values")

        # Desempacota os valores nas variáveis correspondentes.
        # `_id`: Identificador do usuário.
        # `nome`: Nome de usuário.
        # `senha`: Senha cadastrada.
        # `tipo`: Tipo de usuário (Administrador ou Atendente).
        _id, nome, senha, tipo = valores

        # Limpa o campo de entrada do nome de usuário
        #       antes de inserir um novo valor.
        # `campo_usuario.delete(0, tk.END)`: Remove
        #       todo o conteúdo do campo.
        campo_usuario.delete(0, tk.END)

        # Insere o nome do usuário selecionado no campo de entrada.
        # `campo_usuario.insert(0, nome)`: Define o nome do
        #       usuário no campo de entrada.
        campo_usuario.insert(0, nome)

        # Limpa o campo de entrada da senha antes de inserir um novo valor.
        campo_senha.delete(0, tk.END)

        # Insere a senha do usuário selecionado no campo de entrada.
        campo_senha.insert(0, senha)

        # Atualiza a seleção do tipo de usuário no combobox.
        # `selecao_tipo.set(tipo)`: Define a opção
        #       correspondente ao usuário selecionado.
        selecao_tipo.set(tipo)


    # Função para cadastrar um novo usuário no banco de dados.
    def cadastrar():

        # Obtém o valor do campo de entrada do nome do usuário.
        # `.get().strip()`: Recupera o texto digitado e remove
        #       espaços extras no início e no fim.
        nome = campo_usuario.get().strip()

        # Obtém o valor do campo de entrada da senha do usuário.
        senha = campo_senha.get().strip()

        # Obtém o valor selecionado no combobox do tipo de usuário.
        tipo = selecao_tipo.get().strip()

        # Verifica se o nome de usuário e a senha foram preenchidos.
        # Caso algum dos campos esteja vazio, exibe uma mensagem de
        #       erro e interrompe a execução.
        if not nome or not senha:
            messagebox.showerror("Erro", "Usuário e senha são obrigatórios!",
                                 parent=janela)

            # Sai da função sem cadastrar o usuário.
            return

        # Verifica se o nome de usuário já existe no banco de dados.
        # `colecao_usuarios.find_one({"usuario": nome})` busca um
        #       documento onde o campo "usuario" seja igual ao nome informado.
        if colecao_usuarios.find_one({"usuario": nome}):

            # Se um usuário com o mesmo nome for encontrado, exibe
            #       uma mensagem de erro e interrompe o cadastro.
            messagebox.showerror("Erro", "Usuário já cadastrado!",
                                 parent=janela)

            # Sai da função sem cadastrar o usuário.
            return

        # Insere o novo usuário na coleção do MongoDB.
        # `insert_one({})`: Insere um documento com os dados informados.
        colecao_usuarios.insert_one({"usuario": nome, "senha": senha, "tipo": tipo})

        # Exibe uma mensagem informando que o cadastro foi realizado com sucesso.
        messagebox.showinfo("Sucesso",
                            "Usuário cadastrado com sucesso!",
                            parent=janela)

        # Atualiza a lista de usuários na interface
        #       após a inserção do novo usuário.
        carregar_lista()

        # Limpa os campos do formulário após o cadastro bem-sucedido.
        limpar_campos()


    # Cria uma função para alterar os dados de um
    #       usuário selecionado na tabela.
    def alterar():

        # Obtém o item selecionado na tabela de usuários.
        # `tabela_usuarios.selection()` retorna uma tupla
        #       com os IDs dos itens selecionados.
        selecionado = tabela_usuarios.selection()

        # Verifica se nenhum usuário foi selecionado.
        # Se nenhum usuário estiver selecionado, exibe uma
        #       mensagem de erro e encerra a função.
        if not selecionado:

            # `messagebox.showerror()` exibe uma caixa de erro
            #       informando que o usuário deve ser selecionado.
            # `parent=janela` garante que a mensagem seja associada à janela principal.
            messagebox.showerror("Erro",
                                 "Selecione um usuário!",
                                 parent=janela)

            # Encerra a função.
            return

        # Obtém os valores do usuário selecionado na tabela.
        # `tabela_usuarios.item(selecionado[0], "values")`
        #       retorna uma tupla com os valores do item.
        valores = tabela_usuarios.item(selecionado[0], "values")

        # Obtém o ID do usuário que será alterado.
        # O ID está localizado na primeira posição da tupla retornada.
        _id = valores[0]

        # Obtém o novo nome digitado no campo de entrada do nome do usuário.
        # `.get().strip()` recupera o texto digitado e
        #       remove espaços extras antes e depois.
        nome = campo_usuario.get().strip()

        # Obtém a nova senha digitada no campo de
        #       entrada da senha do usuário.
        # `.get().strip()` garante que não haja espaços
        #       extras no início ou no final.
        senha = campo_senha.get().strip()

        # Obtém o novo tipo de usuário selecionado no combobox.
        # `.get().strip()` remove espaços adicionais para
        #       evitar problemas na validação.
        tipo = selecao_tipo.get().strip()

        # Verifica se os campos de nome ou senha estão vazios.
        # Se um dos campos estiver vazio, exibe uma mensagem de
        #       erro e encerra a função.
        if not nome or not senha:

            # `messagebox.showerror()` exibe um alerta informando
            #       que os campos são obrigatórios.
            # `parent=janela` associa a mensagem à janela principal.
            messagebox.showerror("Erro",
                                 "Usuário e senha são obrigatórios!",
                                 parent=janela)

            # Encerra a função.
            return

        # Atualiza o usuário no banco de dados.
        # `colecao_usuarios.update_one()` modifica apenas o
        #       documento que corresponde ao `_id` selecionado.
        # O filtro `{"_id": ObjectId(_id)}` encontra o usuário pelo ID.
        # `{"$set": {"usuario": nome, "senha": senha, "tipo": tipo}}`
        #       define os novos valores dos campos.
        colecao_usuarios.update_one({"_id": ObjectId(_id)},
                                    {"$set": {"usuario": nome, "senha": senha, "tipo": tipo}})

        # Exibe uma mensagem de sucesso informando que o usuário
        #       foi atualizado corretamente.
        # `messagebox.showinfo()` exibe uma caixa de diálogo com a
        #       confirmação da atualização.
        # `parent=janela` mantém a mensagem associada à janela principal.
        messagebox.showinfo("Sucesso",
                            "Usuário atualizado com sucesso!",
                            parent=janela)

        # Atualiza a tabela de usuários recarregando os
        #       dados do banco de dados.
        # Isso garante que a interface exiba os dados
        #       mais recentes após a alteração.
        carregar_lista()

        # Limpa os campos de entrada para permitir um
        #       novo cadastro ou edição.
        limpar_campos()


    # Função responsável por excluir um usuário do banco de
    #       dados e da interface gráfica.
    # É chamada quando o usuário seleciona um item na
    #       tabela e clica no botão "Excluir".
    def excluir():

        # Obtém o item selecionado na tabela de usuários.
        # `tabela_usuarios.selection()` retorna uma tupla
        #       com os itens selecionados.
        selecionado = tabela_usuarios.selection()

        # Verifica se algum usuário foi selecionado.
        # Se a tupla estiver vazia, exibe uma mensagem de erro e interrompe a função.
        if not selecionado:
            messagebox.showerror("Erro",
                                 "Selecione um usuário!",
                                 parent=janela)

            # Encerra a execução.
            return

        # Obtém os valores do usuário selecionado na tabela.
        # `tabela_usuarios.item(selecionado[0], "values")`
        #       retorna uma tupla com os dados do usuário.
        valores = tabela_usuarios.item(selecionado[0], "values")

        # Extrai o ID do usuário da tupla de valores.
        # O ID é armazenado na primeira posição (`index 0`).
        _id = valores[0]

        # Exibe uma caixa de diálogo para confirmar a exclusão do usuário.
        # `messagebox.askyesno()` retorna `True` se o usuário confirmar ou `False` se cancelar.
        # O parâmetro `parent=janela` mantém o alerta vinculado à janela principal.
        if messagebox.askyesno("Confirmação",
                               "Tem certeza que deseja excluir este usuário?",
                               parent=janela):

            # Se o usuário confirmou, exclui o usuário do
            #       banco de dados com base no ID.
            # `colecao_usuarios.delete_one({"_id": ObjectId(_id)})`
            #       remove apenas o registro correspondente.
            colecao_usuarios.delete_one({"_id": ObjectId(_id)})

            # Exibe uma mensagem informando que a exclusão foi bem-sucedida.
            # `messagebox.showinfo()` cria um alerta para o usuário.
            messagebox.showinfo("Sucesso",
                                "Usuário excluído com sucesso!",
                                parent=janela)

            # Atualiza a tabela para remover o usuário excluído da interface.
            # `carregar_lista()` recarrega os dados diretamente do banco de dados.
            carregar_lista()

            # Limpa os campos de entrada após a exclusão para evitar confusão.
            # `limpar_campos()` remove qualquer dado
            #       preenchido nos campos de entrada.
            limpar_campos()


    # Define a função `limpar_campos()` que será
    #       responsável por limpar os campos do formulário.
    def limpar_campos():

        # `""" Limpa os campos do formulário. """`
        # Esta função apaga qualquer informação digitada nos campos de entrada
        # e redefine a seleção do tipo de usuário para o valor padrão.

        # Remove o conteúdo do campo de entrada do nome do usuário.
        # `campo_usuario.delete(0, tk.END)` apaga o
        #       texto do campo, do início ao fim.
        campo_usuario.delete(0, tk.END)

        # Remove o conteúdo do campo de senha.
        # `campo_senha.delete(0, tk.END)` apaga qualquer senha digitada.
        campo_senha.delete(0, tk.END)

        # Reseta a seleção do tipo de usuário para o valor padrão "Atendente".
        # `selecao_tipo.set("Atendente")` altera o valor do
        #       campo de seleção (Combobox).
        selecao_tipo.set("Atendente")

        # Remove qualquer seleção existente na tabela de usuários.
        # selection_remove: Limpa a seleção atual.
        tabela_usuarios.selection_remove(*tabela_usuarios.selection())


    # Chama a função `carregar_lista()` para atualizar a
    #       tabela de usuários.
    # `carregar_lista()` recarrega os dados diretamente do banco de dados.
    carregar_lista()

    # Inicia o loop principal da interface gráfica.
    # `janela.mainloop()` mantém a janela aberta e
    #       aguardando interações do usuário.
    janela.mainloop()


# Inicia a tela de login ao executar o programa.
# A função `tela_login()` exibe a interface de login do sistema.
tela_login()