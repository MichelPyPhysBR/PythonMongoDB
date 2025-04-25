# Importa o módulo Tkinter, que é a biblioteca padrão do Python
#       para criar interfaces gráficas (GUI).
import tkinter as tk
from gettext import textdomain

# Importa componentes específicos do Tkinter:
# `ttk` -> Contém widgets modernos e mais estilizados,
#       como botões e labels aprimorados.
# `messagebox` -> Usado para exibir caixas de mensagens (erros, avisos, confirmações).
# `Menu` -> Permite criar menus suspensos dentro da interface.
from tkinter import ttk, messagebox, Menu

# Importa a biblioteca `datetime`, que permite manipular
#       datas e horários no Python.
import datetime

# Importa a biblioteca `os`, que permite interagir com o sistema
#       operacional (ex.: manipular arquivos e diretórios).
import os

# Importa a biblioteca `sys`, que permite acessar funcionalidades do
#       sistema e manipular o interpretador Python.
import sys

from PIL.ImageOps import expand
from Tools.scripts.make_ctype import values
from pandas import date_range

# ==================================
# Verificando se o tkcalendar está disponível
# ==================================
# O `tkcalendar` é uma biblioteca que adiciona um widget de
#       calendário ao Tkinter.
# Como ele não está incluído por padrão no Python, é necessário
#       testar se está instalado.

try:

    # Importa o DateEntry do `tkcalendar`, que permite escolher datas em
    #   um calendário interativo.
    from tkcalendar import DateEntry

    # Se a importação for bem-sucedida, define uma variável para indicar
    #       que o tkcalendar está disponível.
    USANDO_TKCALENDAR = True

except ImportError:

    # Se o módulo `tkcalendar` não estiver instalado, essa exceção será capturada.
    # Define a variável como `False`, indicando que o recurso de
    #       calendário não poderá ser usado.
    USANDO_TKCALENDAR = False

# ==================================
# Conexão com o Banco de Dados MongoDB
# ==================================
# O MongoDB é um banco de dados NoSQL baseado em documentos JSON.
# Aqui, importamos os módulos necessários para interagir com ele.

# Importa `ObjectId` da biblioteca `bson`, usado para manipular
#       identificadores únicos (_id) do MongoDB.
from bson.objectid import ObjectId

# Importa `MongoClient` da biblioteca `pymongo`, que permite conectar-se ao
#       MongoDB e executar operações no banco de dados.
from pymongo import MongoClient

# ==================================
# Manipulação de Dados com Pandas
# ==================================
# O Pandas é uma biblioteca poderosa para análise e manipulação de
#       dados, especialmente planilhas e tabelas.

# Importa a biblioteca `pandas`, que será usada para trabalhar com
#       DataFrames (estruturas de dados tabulares).
import pandas as pd

# ===================== CONEXÃO COM O BANCO DE DADOS (MongoDB) ====================== #

# Cria uma conexão com o servidor MongoDB que está rodando localmente.
# O MongoDB é um banco de dados NoSQL que armazena informações em formato JSON.
# A URL "mongodb://localhost:27017" indica que o banco está
#       hospedado no próprio computador (localhost)
#       e está usando a porta padrão do MongoDB (27017).
client = MongoClient("mongodb://localhost:27017")

# Acessa o banco de dados chamado "gerenciamento_pousada".
# Se esse banco ainda não existir, ele será criado automaticamente ao inserir dados.
db = client["gerenciamento_pousada"]

# Criamos referências para diferentes coleções dentro do banco de dados.
# Coleções no MongoDB são equivalentes a tabelas em bancos SQL, mas
#       armazenam documentos JSON ao invés de registros estruturados.

# `usuarios_collection`: Armazena os dados dos usuários do
#       sistema (ex.: login, senha, permissões de acesso).
usuarios_collection = db["usuarios"]

# `quartos_collection`: Contém informações sobre os quartos disponíveis na pousada.
# Exemplo de dados armazenados: número do quarto, tipo (standard, suíte),
#       status (disponível, ocupado), preço da diária.
quartos_collection = db["quartos"]

# `reservas_collection`: Registra todas as reservas feitas pelos hóspedes.
# Inclui informações como o quarto reservado, período da estadia,
#       hóspede responsável e valor total da reserva.
reservas_collection = db["reservas"]

# `hospedes_collection`: Armazena dados dos hóspedes, como
#       nome, CPF, telefone, e-mail e endereço.
# Serve para identificar clientes recorrentes e facilitar o check-in.
hospedes_collection = db["hospedes"]

# `produtos_collection`: Contém informações sobre produtos vendidos na pousada.
# Exemplo: frigobar, café da manhã extra, passeios, itens de higiene pessoal.
produtos_collection = db["produtos"]


# =================================================================================== #

# ======================= APLICAÇÃO DE ESTILOS PERSONALIZADOS ========================= #
def aplicar_estilos(raiz):
    # Cria um objeto de estilo `Style` do `ttk`, que permite
    #       personalizar a aparência dos widgets da interface.
    estilo = ttk.Style(raiz)

    # Define o tema da interface gráfica como "clam".
    # Esse tema é escolhido porque tem um visual mais moderno e
    #       limpo em comparação com o padrão do Tkinter.
    estilo.theme_use('clam')

    # Personaliza a aparência dos botões (`TButton`).
    # `font=('Helvetica', 10, 'bold')` define a fonte como Helvetica,
    #       tamanho 10, em negrito.
    # `padding=6` adiciona um espaçamento interno de 6 pixels,
    #       tornando o botão maior e mais confortável para clicar.
    # `background='#4CAF50'` define a cor de fundo do botão como
    #       verde (código hexadecimal #4CAF50).
    # `foreground='white'` define a cor do texto como branco.
    estilo.configure('TButton',
                     font=('Helvetica', 10, 'bold'),
                     padding=6,
                     background='#4CAF50',
                     foreground='white')

    # Define o comportamento do botão (`TButton`) ao ser pressionado ou
    #       quando o mouse está sobre ele.
    # `foreground=[('pressed', 'white'), ('active', 'white')]` mantém a cor
    #       do texto branca quando o botão está pressionado ou ativo.
    # `background=[('pressed', '!disabled', '#388E3C'), ('active', '#43A047')]`
    #     - Quando pressionado (`pressed`), a cor de fundo muda para um
    #           tom de verde mais escuro (#388E3C).
    #     - Quando o mouse passa sobre o botão (`active`), a cor de fundo
    #           muda para um tom de verde médio (#43A047).
    estilo.map('TButton',
               foreground=[('pressed', 'white'), ('active', 'white')],
               background=[('pressed', '!disabled', '#388E3C'), ('active', '#43A047')])

    # Personaliza a aparência dos rótulos (`TLabel`), usados para
    #       exibir textos na interface.
    # `font=('Helvetica', 10)` define a fonte como Helvetica, tamanho 10.
    # `padding=4` adiciona um espaçamento interno de 4 pixels para
    #       evitar que o texto fique colado nas bordas do rótulo.
    estilo.configure('TLabel', font=('Helvetica', 10), padding=4)

    # Personaliza os campos de entrada de texto (`TEntry`), onde o
    #       usuário pode digitar informações.
    # `font=('Helvetica', 10)` define a fonte do texto digitado no campo de
    #       entrada como Helvetica, tamanho 10.
    estilo.configure('TEntry', font=('Helvetica', 10))

    # Personaliza os menus suspensos (`TCombobox`), que permitem ao
    #       usuário selecionar opções predefinidas.
    # `font=('Helvetica', 10)` define a fonte dos itens do menu
    #       suspenso como Helvetica, tamanho 10.
    estilo.configure('TCombobox', font=('Helvetica', 10))

    # Personaliza a aparência das tabelas (`Treeview`), usadas para
    #       exibir dados organizados em colunas e linhas.
    # `font=('Helvetica', 10)` define a fonte do texto dentro da
    #       tabela como Helvetica, tamanho 10.
    # `rowheight=25` define a altura de cada linha da tabela como 25
    #       pixels, tornando-a mais legível.
    estilo.configure('Treeview', font=('Helvetica', 10), rowheight=25)

    # Personaliza a aparência do cabeçalho da tabela (`Treeview.Heading`),
    #       onde ficam os títulos das colunas.
    # `font=('Helvetica', 10, 'bold')` define a fonte do cabeçalho como
    #       Helvetica, tamanho 10, em negrito.
    # `background="#e0e0e0"` define a cor de fundo do cabeçalho como
    #       cinza claro (#e0e0e0) para destacar os títulos das colunas.
    estilo.configure("Treeview.Heading",
                     font=('Helvetica', 10, 'bold'),
                     background="#e0e0e0")


# ==================================================================================== #


# =============================================================================
# ================ TELA DE GERENCIAMENTO DE QUARTOS (CRUD) ====================
# =============================================================================

class TelaGerenciarQuartos(tk.Frame):
    """
    Tela para Cadastrar, Alterar e Excluir quartos. Possui um
            Treeview para listar todos os quartos.
    Adicionamos um botão "Histórico" para ver quem usou o quarto.
    """

    def __init__(self, mestre, permissoes_usuario):

        # Inicializa a classe `tk.Frame`, que representa um
        #       container dentro da interface gráfica.
        # `super().__init__(mestre, bg="#f7f7f7")` chama o construtor
        #       da classe pai (`tk.Frame`), definindo `mestre` como o
        #       elemento pai e aplicando um fundo branco fumê (`#f7f7f7`).
        super().__init__(mestre, bg="#f7f7f7")

        # Armazena a referência para a janela principal (root).
        # `self.mestre = mestre` permite que a tela de gerenciamento de
        #       quartos interaja com a janela principal.
        self.mestre = mestre

        # Armazena as permissões do usuário autenticado.
        # `self.permissoes_usuario = permissoes_usuario` controla quais
        #       funcionalidades estarão disponíveis
        #       com base no nível de permissão do usuário logado.
        self.permissoes_usuario = permissoes_usuario

        # Exibe o frame `TelaGerenciarQuartos` na interface gráfica.
        # `.pack(fill="both", expand=True)` configura o comportamento do frame:
        # - `fill="both"` faz com que o frame ocupe todo o espaço
        #       disponível na largura e altura.
        # - `expand=True` permite que o frame se expanda conforme a
        #       janela principal for redimensionada.
        self.pack(fill="both", expand=True)

        # Cria um rótulo (Label) para exibir o título da tela de Gerenciamento de Quartos.
        # - `self`: O rótulo é inserido dentro da instância `TelaGerenciarQuartos`.
        # - `text="Gerenciamento de Quartos"`: Define o texto exibido no
        #       rótulo, informando o nome da tela.
        # - `font=("Helvetica", 16, "bold")`: Define a formatação do texto:
        #   - `"Helvetica"`: Fonte utilizada.
        #   - `16`: Tamanho da fonte, maior que o texto normal, para destacar o título.
        #   - `"bold"`: Deixa o texto em negrito para enfatizar o título.
        # - `bg="#f7f7f7"`: Define a cor de fundo do rótulo.
        #   - O código hexadecimal `#f7f7f7` representa a
        #           cor **branco fumê**, um tom muito claro de cinza.
        lbl_titulo = tk.Label(self,
                              text="Gerenciamento de Quartos",
                              font=("Helvetica", 16, "bold"),
                              bg="#f7f7f7")

        # Exibe o rótulo na tela utilizando o método `.pack()`.
        # `.pack(pady=10)` configura o posicionamento do rótulo dentro do layout:
        # - `pady=10`: Adiciona um espaçamento vertical de **10 pixels**
        #       acima e abaixo do rótulo.
        #   - Esse espaçamento melhora a organização visual e evita que o
        #       título fique muito próximo de outros elementos da tela.
        lbl_titulo.pack(pady=10)

        # Cria um frame (container) para agrupar os campos do formulário.
        # `ttk.Frame(self)` cria um frame dentro da `TelaGerenciarQuartos`,
        #       permitindo organizar os campos de entrada.
        frame_form = ttk.Frame(self)

        # Exibe o frame na interface gráfica.
        # `.pack(pady=10, padx=20)` configura o posicionamento do frame dentro do layout:
        # - `pady=10`: Adiciona um espaçamento vertical de **10 pixels** acima e abaixo do frame,
        #   garantindo uma separação entre o título e os campos do formulário.
        # - `padx=20`: Adiciona um espaçamento horizontal de **20 pixels**
        #       em ambos os lados do frame, melhorando a disposição dos
        #       elementos na tela e evitando que fiquem colados nas bordas.
        frame_form.pack(pady=10, padx=20)

        # `self.numero_quarto_var` armazena o número do quarto como uma string.
        # `tk.StringVar()` cria uma variável de texto para armazenar o número do quarto.
        self.numero_quarto_var = tk.StringVar()

        # `self.tipo_quarto_var` armazena o tipo do quarto como uma string.
        # `tk.StringVar()` permite que o valor seja alterado
        #       dinamicamente na interface.
        self.tipo_quarto_var = tk.StringVar()

        # `self.capacidade_var` armazena a quantidade de pessoas que o quarto comporta.
        # `tk.IntVar()` cria uma variável numérica do tipo inteiro
        #       para armazenar esse valor.
        self.capacidade_var = tk.IntVar()

        # `self.preco_diaria_var` armazena o preço da diária do quarto.
        # `tk.DoubleVar()` cria uma variável numérica do tipo ponto
        #       flutuante para permitir valores decimais.
        self.preco_diaria_var = tk.DoubleVar()

        # `self.status_var` armazena o status atual do quarto,
        #       como "Disponível" ou "Ocupado".
        # `tk.StringVar(value="Disponível")` cria uma variável de
        #       texto e define seu valor inicial como "Disponível".
        self.status_var = tk.StringVar(value="Disponível")

        # `self.quarto_em_edicao` armazena o ID do quarto que está sendo editado.
        # Inicialmente, a variável é definida como `None`, indicando
        #       que nenhum quarto está em edição no momento.
        self.quarto_em_edicao = None

        # Define uma lista de tipos de quartos predefinidos.
        # Essa lista será utilizada para preencher um menu
        #       suspenso (Combobox) com opções pré-definidas.
        tipos_predefinidos = ["Suíte Master", "Standard", "Quarto Compartilhado", "Quarto Família"]

        # Cria um rótulo (Label) para identificar o campo de entrada do número do quarto.
        # `ttk.Label(frame_form, text="Número do Quarto:")`
        # - `frame_form`: O rótulo é inserido dentro do frame que
        #       agrupa os campos do formulário.
        # - `text="Número do Quarto:"`: Define o texto exibido no rótulo,
        #       indicando que o campo ao lado é para inserir o número do quarto.
        # Configura o posicionamento do rótulo no layout `grid`:
        # - `row=0`: Posiciona o rótulo na **primeira linha** do grid dentro do frame.
        # - `column=0`: Posiciona o rótulo na **primeira coluna**, à
        #       esquerda do campo de entrada.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels** horizontal e
        #       vertical, evitando que o rótulo fique colado a outros elementos.
        # - `sticky="e"`: Alinha o rótulo à direita (`east`), garantindo
        #       que ele fique próximo ao campo de entrada.
        ttk.Label(frame_form,
                  text="Número do Quarto:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) para permitir que o
        #       usuário insira o número do quarto.
        # `ttk.Entry(frame_form, textvariable=self.numero_quarto_var)`
        # - `frame_form`: O campo de entrada é inserido dentro do
        #       mesmo frame dos outros elementos do formulário.
        # - `textvariable=self.numero_quarto_var`: Associa o campo de
        #       entrada à variável `self.numero_quarto_var`,
        #       permitindo que o valor digitado seja armazenado e
        #       recuperado dinamicamente.
        # Configura o posicionamento do campo de entrada no layout `grid`:
        # - `row=0`: Posiciona o campo na **primeira linha**, ao
        #       lado do rótulo "Número do Quarto".
        # - `column=1`: Posiciona o campo na **segunda coluna**,
        #       garantindo alinhamento ao lado do rótulo correspondente.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels**
        #       horizontal e vertical, garantindo um layout organizado.
        ttk.Entry(frame_form,
                  textvariable=self.numero_quarto_var).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) para identificar o campo de seleção do tipo de quarto.
        # `ttk.Label(frame_form, text="Tipo do Quarto:")`
        # - `frame_form`: O rótulo é inserido dentro do frame que
        #       agrupa os campos do formulário.
        # - `text="Tipo do Quarto:"`: Define o texto exibido no rótulo,
        #       informando que o campo ao lado é para selecionar o tipo de quarto.
        # Configura o posicionamento do rótulo no layout `grid`:
        # - `row=1`: Posiciona o rótulo na **segunda linha** do grid dentro do frame.
        # - `column=0`: Posiciona o rótulo na **primeira coluna**, à
        #       esquerda do campo de seleção.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels**
        #       horizontal e vertical, garantindo uma organização visual adequada.
        # - `sticky="e"`: Alinha o rótulo à direita (`east`), garantindo
        #       que fique próximo ao campo de seleção.
        ttk.Label(frame_form,
                  text="Tipo do Quarto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um menu suspenso (Combobox) para selecionar o tipo do quarto.
        # - `frame_form`: O Combobox é inserido dentro do frame que
        #       agrupa os campos do formulário.
        # - `textvariable=self.tipo_quarto_var`: Associa o Combobox à
        #       variável `self.tipo_quarto_var`,
        #   permitindo que a opção selecionada seja armazenada dinamicamente.
        # - `values=tipos_predefinidos`: Define as opções do Combobox
        #       usando a lista `tipos_predefinidos`,
        #       que contém os tipos de quartos predefinidos:
        #     - "Suíte Master"
        #     - "Standard"
        #     - "Quarto Compartilhado"
        #     - "Quarto Família"
        # - `state="readonly"`: Define que o usuário **só pode
        #       selecionar opções da lista**,
        #   impedindo a digitação de valores personalizados.
        # - `width=28`: Define a largura do Combobox para garantir
        #       uma exibição adequada do texto.
        combo_tipo = ttk.Combobox(frame_form,
                                  textvariable=self.tipo_quarto_var,
                                  values=tipos_predefinidos,
                                  state="readonly",
                                  width=28)

        # Posiciona o Combobox dentro do frame `frame_form` utilizando o sistema de layout `grid`.
        # `.grid(row=1, column=1, padx=5, pady=5)` define a posição do Combobox dentro do frame:
        # - `row=1`: Posiciona o Combobox na **segunda linha**, ao lado do
        #       rótulo "Tipo do Quarto".
        # - `column=1`: Posiciona o Combobox na **segunda coluna**, garantindo
        #       alinhamento ao lado do rótulo correspondente.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels**
        #       horizontal e vertical, garantindo um layout organizado.
        combo_tipo.grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) para identificar o campo de entrada da capacidade do quarto.
        # `ttk.Label(frame_form, text="Capacidade:")`
        # - `frame_form`: O rótulo é inserido dentro do frame que agrupa os
        #       campos do formulário.
        # - `text="Capacidade:"`: Define o texto exibido no rótulo, informando
        #       que o campo ao lado é para inserir a capacidade do quarto.
        # Configura o posicionamento do rótulo no layout `grid`:
        # - `row=2`: Posiciona o rótulo na **terceira linha** do grid dentro do frame.
        # - `column=0`: Posiciona o rótulo na **primeira coluna**, à
        #       esquerda do campo de entrada.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels**
        #       horizontal e vertical para melhorar o layout.
        # - `sticky="e"`: Alinha o rótulo à direita (`east`), garantindo que
        #       ele fique próximo ao campo de entrada.
        ttk.Label(frame_form,
                  text="Capacidade:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) para permitir que o usuário
        #       insira a capacidade do quarto.
        # `ttk.Entry(frame_form, textvariable=self.capacidade_var)`
        # - `frame_form`: O campo de entrada é inserido dentro do frame
        #       que agrupa os campos do formulário.
        # - `textvariable=self.capacidade_var`: Associa o campo de entrada à
        #       variável `self.capacidade_var`, permitindo que o valor
        #       digitado seja armazenado e recuperado dinamicamente.
        #   - `self.capacidade_var` é um `tk.IntVar()`, o que significa que
        #           este campo só aceitará números inteiros.
        # Configura o posicionamento do campo de entrada no layout `grid`:
        # - `row=2`: Posiciona o campo na **terceira linha**, ao lado
        #       do rótulo "Capacidade".
        # - `column=1`: Posiciona o campo na **segunda coluna**, garantindo
        #       alinhamento com o rótulo correspondente.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels**
        #       horizontal e vertical, garantindo um layout organizado.
        ttk.Entry(frame_form,
                  textvariable=self.capacidade_var).grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para identificar o campo de entrada do preço base por diária.
        # `text="Preço Base/Diária:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `sticky="e"` alinha o texto do rótulo à direita, garantindo
        #       que ele fique próximo ao campo de entrada.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e
        #       vertical ao redor do rótulo.
        ttk.Label(frame_form,
                  text="Preço Base/Diária:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para inserir o preço base da diária do quarto.
        # `textvariable=self.preco_diaria_var` associa o campo à variável `self.preco_diaria_var`,
        # garantindo que o valor inserido seja armazenado e possa ser recuperado dinamicamente.
        # `self.preco_diaria_var` é do tipo `tk.DoubleVar()`, permitindo a
        #       inserção de valores decimais.
        # O campo de entrada é posicionado ao lado do rótulo dentro do `frame_form`.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e
        #       vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.preco_diaria_var).grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo para identificar o campo de seleção do status do quarto.
        # `text="Status:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `sticky="e"` alinha o texto do rótulo à direita, garantindo que
        #       ele fique próximo ao campo de seleção.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e
        #       vertical ao redor do rótulo.
        ttk.Label(frame_form,
                  text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Cria um menu suspenso (Combobox) para selecionar o status do quarto.
        # `textvariable=self.status_var` associa o Combobox à variável `self.status_var`,
        # garantindo que o valor selecionado seja armazenado e possa ser recuperado dinamicamente.
        # `values=["Disponível", "Ocupado", "Manutenção"]` define as opções
        #       disponíveis no Combobox.
        # `state="readonly"` impede que o usuário digite valores manualmente,
        #       permitindo apenas a seleção das opções predefinidas.
        # `width=28` define a largura do Combobox, garantindo que o texto fique visível sem cortes.
        # O Combobox é posicionado ao lado do rótulo dentro do `frame_form`.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e
        #       vertical ao redor do Combobox.
        combo_status = ttk.Combobox(frame_form,
                                    textvariable=self.status_var,
                                    values=["Disponível", "Ocupado", "Manutenção"],
                                    state="readonly",
                                    width=28)
        combo_status.grid(row=4, column=1, padx=5, pady=5)

        # ---------------- FRAME para botões ---------------- #
        # Cria um frame para agrupar os botões de ação do formulário.
        # O frame é posicionado dentro do `frame_form`.
        # `columnspan=2` faz com que o frame ocupe as duas colunas do
        #       layout, garantindo centralização.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do frame.
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=10)

        # Cria um botão para cadastrar ou atualizar as informações do quarto.
        # `text="Cadastrar/Atualizar"` define o texto exibido no botão.
        # `width=15` define a largura do botão para manter um tamanho uniforme.
        # `command=self.cadastrar_quarto` associa o botão à função `self.cadastrar_quarto`,
        # garantindo que ao clicar, o quarto será cadastrado ou atualizado no banco de dados.
        # O botão é posicionado dentro do `frame_botoes`.
        # `.pack(side="left", padx=5)` posiciona o botão no lado esquerdo do frame e adiciona
        # um espaçamento horizontal de 5 pixels entre ele e outros elementos.
        btn_cadastrar = ttk.Button(frame_botoes,
                                   text="Cadastrar/Atualizar",
                                   width=15,
                                   command=self.cadastrar_quarto)
        btn_cadastrar.pack(side="left", padx=5)

        # Cria um botão para deletar um quarto cadastrado no sistema.
        # `text="Deletar"` define o texto exibido no botão.
        # `width=15` define a largura do botão para manter um tamanho
        #       uniforme com os demais botões.
        # `command=self.deletar_quarto` associa o botão à função `self.deletar_quarto`,
        # garantindo que ao clicar, o quarto selecionado será removido do banco de dados.
        # O botão é posicionado dentro do `frame_botoes`, agrupado com outros botões do formulário.
        btn_deletar = ttk.Button(frame_botoes,
                                 text="Deletar",
                                 width=15,
                                 command=self.deletar_quarto)

        # `.pack(side="left", padx=5)` posiciona o botão no lado esquerdo do frame.
        # `side="left"` garante que o botão fique alinhado à
        #       esquerda dentro do `frame_botoes`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre o botão e outros elementos.
        btn_deletar.pack(side="left", padx=5)

        # Cria um botão para exibir o histórico de uso do quarto.
        # `text="Histórico"` define o texto exibido no botão.
        # `width=15` define a largura do botão para manter um tamanho
        #       uniforme com os demais botões.
        # `command=self.abrir_historico_quarto` associa o botão à
        #       função `self.abrir_historico_quarto`,
        #       garantindo que ao clicar, será exibido o histórico de
        #       reservas e ocupação do quarto.
        # O botão é posicionado dentro do `frame_botoes`, agrupado
        #       com os outros botões do formulário.
        btn_historico = ttk.Button(frame_botoes,
                                   text="Histórico",
                                   width=15,
                                   command=self.abrir_historico_quarto)

        # `.pack(side="left", padx=5)` posiciona o botão no lado esquerdo do frame.
        # `side="left"` garante que o botão fique alinhado à
        #       esquerda dentro do `frame_botoes`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre o botão e outros elementos.
        btn_historico.pack(side="left", padx=5)

        # Treeview
        # Cria um widget Treeview para exibir a lista de quartos.
        # `ttk.Treeview(self, columns=(...), show="headings")` define
        #       uma tabela com colunas específicas.
        # - `self`: O Treeview é inserido dentro da tela de gerenciamento de quartos.
        # - `columns: Define as colunas que serão exibidas.
        # - `show="headings"` remove a primeira coluna padrão
        #       do Treeview, deixando apenas os cabeçalhos personalizados.
        self.tree_quartos = ttk.Treeview(self,
                                         columns=("numero", "tipo", "capacidade", "preco", "status", "id"),
                                         show="headings")

        # Define o cabeçalho da coluna "numero" no Treeview.
        # `heading("numero", text="Nº Quarto")` define o nome visível no
        #       cabeçalho da coluna "numero".
        self.tree_quartos.heading("numero", text="Nº Quarto")

        # Define o cabeçalho da coluna "tipo" no Treeview.
        # `heading("tipo", text="Tipo")` define o nome visível no
        #       cabeçalho da coluna "tipo".
        self.tree_quartos.heading("tipo", text="Tipo")

        # Define o cabeçalho da coluna "capacidade" no Treeview.
        # `heading("capacidade", text="Cap.")` define o nome visível no
        #       cabeçalho da coluna "capacidade".
        # O nome "Cap." foi utilizado para manter a interface mais compacta.
        self.tree_quartos.heading("capacidade", text="Cap.")

        # Define o cabeçalho da coluna "preco" no Treeview.
        # `heading("preco", text="Preço Base")` define o nome
        #       visível no cabeçalho da coluna "preco".
        self.tree_quartos.heading("preco", text="Preço Base")

        # Define o cabeçalho da coluna "status" no Treeview.
        # `heading("status", text="Status")` define o nome visível no
        #       cabeçalho da coluna "status".
        self.tree_quartos.heading("status", text="Status")

        # Define o cabeçalho da coluna "id" no Treeview.
        # `heading("id", text="ID(oculto)")` define o nome visível no
        #       cabeçalho da coluna "id".
        # Essa coluna armazena o ID do banco de dados, mas
        #       será oculta da visualização do usuário.
        self.tree_quartos.heading("id", text="ID(oculto)")

        # Ajusta a largura da coluna "id" para 0, tornando-a invisível na tabela.
        # `column("id", width=0, stretch=False)` esconde a coluna,
        #       pois o ID não precisa ser visível para o usuário.
        # - `width=0`: Define a largura como zero, ocultando o conteúdo.
        # - `stretch=False`: Impede que a coluna seja redimensionada pelo usuário.
        self.tree_quartos.column("id", width=0, stretch=False)

        # Exibe o Treeview na tela utilizando o método `.pack()`.
        # `fill="both"` faz com que o widget expanda tanto na largura quanto na
        #       altura, ocupando todo o espaço disponível.
        # `expand=True` permite que o Treeview se expanda quando a
        #       janela for redimensionada.
        # `padx=10, pady=10` adiciona 10 pixels de espaçamento
        #       horizontal e vertical ao redor do Treeview,
        #       garantindo um layout mais organizado.
        self.tree_quartos.pack(fill="both", expand=True, padx=10, pady=10)

        # Associa um evento ao Treeview para permitir a seleção de um
        #       quarto com um duplo clique.
        # `bind("<Double-1>", self.selecionar_quarto)` significa que ao
        #       dar um duplo clique em uma linha do Treeview,
        #       a função `self.selecionar_quarto` será chamada automaticamente.
        self.tree_quartos.bind("<Double-1>", self.selecionar_quarto)

        # Cria um botão para retornar ao Dashboard (tela principal).
        # `text="Voltar ao Dashboard"` define o texto exibido no botão.
        # `command=self.voltar_dashboard` associa o botão à função `self.voltar_dashboard`,
        # garantindo que ao ser clicado, a interface volte para a tela principal do sistema.
        btn_voltar = ttk.Button(self,
                                text="Voltar ao Dashboard",
                                command=self.voltar_dashboard)

        # Exibe o botão "Voltar ao Dashboard" na tela utilizando o método `.pack()`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels abaixo do botão,
        # evitando que ele fique muito próximo dos outros elementos da interface.
        btn_voltar.pack(pady=10)

        # Chama a função `listar_quartos()` para carregar os dados
        #       dos quartos e exibi-los no Treeview.
        # Essa função busca os quartos cadastrados no
        #       banco de dados e preenche a tabela automaticamente.
        self.listar_quartos()

    def listar_quartos(self):

        # Remove todos os itens existentes no Treeview antes de atualizar a lista.
        # `self.tree_quartos.get_children()` retorna todas as linhas da tabela.
        # O loop percorre cada item e o remove com `self.tree_quartos.delete(item)`,
        # garantindo que a tabela sempre exiba apenas os dados mais recentes.
        for item in self.tree_quartos.get_children():
            self.tree_quartos.delete(item)

        # Percorre todos os documentos (quartos) armazenados na
        #       coleção `quartos_collection` no banco de dados.
        # `quartos_collection.find()` retorna todos os registros
        #       cadastrados na base de dados.
        for q in quartos_collection.find():
            # Insere cada quarto recuperado no Treeview.
            # `self.tree_quartos.insert("", tk.END, values=(...))` adiciona uma nova linha na tabela.
            # - `""`: Indica que o item será inserido na raiz do Treeview (sem hierarquia).
            # - `tk.END`: Adiciona o novo item no final da lista.
            # - `values=(...)`: Define os valores que serão exibidos nas colunas do Treeview.
            self.tree_quartos.insert("",
                                     tk.END, values=(q["numero_quarto"],  # Número do quarto
                                                     q["tipo"],  # Tipo do quarto
                                                     q["capacidade"],  # Capacidade de hóspedes
                                                     q["preco_diaria"],  # Preço da diária
                                                     q["status"],  # Status do quarto
                                                     str(q["_id"])))  # ID do quarto (convertido para string)

        # Define `self.quarto_em_edicao` como `None`, indicando que
        #       nenhum quarto está sendo editado no momento.
        self.quarto_em_edicao = None

    def voltar_dashboard(self):

        # Oculta a tela atual de gerenciamento de quartos.
        # `self.pack_forget()` remove o frame da tela
        #       atual da interface gráfica,
        # permitindo que outra tela seja exibida no lugar sem destruí-la.
        self.pack_forget()

        # Cria e exibe a tela principal (Dashboard).
        # `TelaDashboard(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaDashboard`,
        #       que representa a tela principal do sistema.
        # - `self.mestre`: Passa a referência da janela principal para o Dashboard.
        # - `self.permissoes_usuario`: Mantém as permissões do usuário
        #       autenticado, garantindo que ele tenha acesso às funcionalidades adequadas.
        TelaDashboard(self.mestre, self.permissoes_usuario)

    def selecionar_quarto(self, event):

        # Obtém a seleção do usuário na tabela (`Treeview`).
        # `self.tree_quartos.selection()` retorna o identificador do item selecionado.
        sel = self.tree_quartos.selection()

        # Verifica se algum quarto foi selecionado.
        # Se `sel` estiver vazio, a função retorna imediatamente, evitando erros.
        if not sel:
            return

        # Obtém os valores da linha selecionada no `Treeview`.
        # `self.tree_quartos.item(sel, "values")` retorna uma tupla
        #       contendo os valores da linha selecionada.
        valores = self.tree_quartos.item(sel, "values")

        # Preenche o campo "Número do Quarto" com o valor selecionado.
        # `self.numero_quarto_var.set(valores[0])` define o valor
        #       da variável `numero_quarto_var`.
        self.numero_quarto_var.set(valores[0])

        # Preenche o campo "Tipo do Quarto" com o valor selecionado.
        # `self.tipo_quarto_var.set(valores[1])` define o valor
        #       da variável `tipo_quarto_var`.
        self.tipo_quarto_var.set(valores[1])

        # Preenche o campo "Capacidade" com o valor selecionado.
        # `self.capacidade_var.set(valores[2])` define o valor
        #       da variável `capacidade_var`.
        self.capacidade_var.set(valores[2])

        # Preenche o campo "Preço Base/Diária" com o valor selecionado.
        # `self.preco_diaria_var.set(valores[3])` define o
        #       valor da variável `preco_diaria_var`.
        self.preco_diaria_var.set(valores[3])

        # Preenche o campo "Status" com o valor selecionado.
        # `self.status_var.set(valores[4])` define o valor da variável `status_var`.
        self.status_var.set(valores[4])

        # Armazena o ID do quarto selecionado para edição futura.
        # `ObjectId(valores[5])` converte a string do ID para um
        #       formato compatível com o MongoDB.
        self.quarto_em_edicao = ObjectId(valores[5])

    def cadastrar_quarto(self):

        # Obtém o valor digitado no campo "Número do Quarto".
        # `.get().strip()` remove espaços extras no início e no final do texto.
        numero = self.numero_quarto_var.get().strip()

        # Obtém o valor selecionado no campo "Tipo do Quarto".
        # `.get().strip()` remove espaços extras para evitar problemas de formatação.
        tipo = self.tipo_quarto_var.get().strip()

        # Obtém o valor do campo "Capacidade", que representa o número
        #       de hóspedes que o quarto comporta.
        # Esse valor já está armazenado como um número inteiro (`IntVar()`),
        #       então não há necessidade de conversão.
        capacidade = self.capacidade_var.get()

        # Obtém o valor do campo "Preço Base/Diária", representando o
        #       valor da diária do quarto.
        # Esse valor já está armazenado como um número decimal (`DoubleVar()`),
        #       então não há necessidade de conversão.
        preco = self.preco_diaria_var.get()

        # Obtém o valor selecionado no campo "Status".
        # Como esse campo é um `StringVar()`, ele retorna uma string
        #       como "Disponível", "Ocupado" ou "Manutenção".
        status = self.status_var.get()

        # Verifica se o campo "Número do Quarto" foi preenchido.
        # Se estiver vazio, exibe uma mensagem de erro e interrompe a
        #       execução da função (`return`).
        if not numero:
            messagebox.showerror("Erro",
                                 "O campo 'Número do Quarto' é obrigatório.")
            return

        # Verifica se um quarto está em edição.
        # `self.quarto_em_edicao` contém o ID do quarto que está sendo editado.
        # Se for diferente de `None`, significa que um quarto já existente será atualizado.
        if self.quarto_em_edicao:

            # Atualiza os dados do quarto no banco de dados MongoDB.
            # `update_one({"_id": self.quarto_em_edicao}, {...})` busca o
            #       quarto pelo seu ID e atualiza os campos especificados.
            quartos_collection.update_one(
                {"_id": self.quarto_em_edicao},  # Filtra pelo ID do quarto em edição
                {"$set": {
                    "numero_quarto": numero,  # Atualiza o número do quarto
                    "tipo": tipo,  # Atualiza o tipo do quarto
                    "capacidade": capacidade,  # Atualiza a capacidade do quarto
                    "preco_diaria": preco,  # Atualiza o preço da diária
                    "status": status  # Atualiza o status do quarto
                }}
            )

            # Exibe uma mensagem informando que o quarto foi atualizado com sucesso.
            messagebox.showinfo("Sucesso",
                                f"Quarto '{numero}' atualizado com sucesso!")

        # Se `self.quarto_em_edicao` for `None`, significa
        #       que um novo quarto será cadastrado.
        else:

            # Verifica se já existe um quarto com o mesmo número no banco de dados.
            # `find_one({"numero_quarto": numero})` busca um quarto pelo número.
            if quartos_collection.find_one({"numero_quarto": numero}):
                # Exibe uma mensagem de erro se o quarto já estiver cadastrado e interrompe o cadastro.
                messagebox.showerror("Erro",
                                     f"O quarto '{numero}' já existe.")

                # Interrompe a execução da função
                return

            # Insere um novo quarto no banco de dados.
            # `insert_one({...})` adiciona um novo documento na coleção `quartos_collection`.
            quartos_collection.insert_one({
                "numero_quarto": numero,  # Número do quarto
                "tipo": tipo,  # Tipo do quarto
                "capacidade": capacidade,  # Capacidade do quarto
                "preco_diaria": preco,  # Preço base por diária
                "status": status  # Status do quarto
            })

            # Exibe uma mensagem informando que o quarto foi cadastrado com sucesso.
            messagebox.showinfo("Sucesso",
                                f"Quarto '{numero}' cadastrado com sucesso!")

        # Chama a função `limpar_campos()` para redefinir os valores dos campos do formulário.
        # Isso impede que os dados do último cadastro fiquem
        #       visíveis após a operação.
        self.limpar_campos()

        # Atualiza a lista de quartos no Treeview chamando `listar_quartos()`.
        # Isso garante que o novo quarto ou a atualização
        #       seja refletida na interface.
        self.listar_quartos()

    def limpar_campos(self):

        # Limpa o campo "Número do Quarto".
        # `self.numero_quarto_var.set("")` redefine o valor para uma
        #       string vazia, removendo qualquer entrada anterior.
        self.numero_quarto_var.set("")

        # Limpa o campo "Tipo do Quarto".
        # `self.tipo_quarto_var.set("")` redefine o valor para uma string vazia.
        self.tipo_quarto_var.set("")

        # Limpa o campo "Capacidade".
        # `self.capacidade_var.set(0)` redefine o valor para `0`,
        #       garantindo que não haja entrada residual.
        self.capacidade_var.set(0)

        # Limpa o campo "Preço Base/Diária".
        # `self.preco_diaria_var.set(0.0)` redefine o valor para `0.0`,
        #       garantindo que o campo fique zerado.
        self.preco_diaria_var.set(0.0)

        # Reseta o campo "Status" para o valor padrão "Disponível".
        # `self.status_var.set("Disponível")` garante que, ao limpar os
        #       campos, o status volte ao padrão inicial.
        self.status_var.set("Disponível")

        # Remove qualquer referência a um quarto que esteja sendo editado.
        # `self.quarto_em_edicao = None` significa que nenhuma
        #       edição está em andamento.
        self.quarto_em_edicao = None

    def deletar_quarto(self):

        # Obtém a seleção do usuário na tabela de quartos (`Treeview`).
        # `self.tree_quartos.selection()` retorna o identificador do item selecionado.
        sel = self.tree_quartos.selection()

        # Verifica se algum quarto foi selecionado.
        # Se `sel` estiver vazio, exibe uma mensagem de erro e
        #       interrompe a execução da função (`return`).
        if not sel:
            messagebox.showerror("Erro",
                                 "Selecione um quarto na lista para deletar.")
            return

        # Obtém os valores da linha selecionada na tabela (`Treeview`).
        # `self.tree_quartos.item(sel, "values")` retorna uma
        #       tupla contendo os valores da linha.
        valores = self.tree_quartos.item(sel, "values")

        # Obtém o ID do quarto que será deletado.
        # O ID está armazenado na **sexta coluna** da tabela (`valores[5]`).
        quarto_id_str = valores[5]

        # Exibe uma caixa de diálogo de confirmação antes de deletar o quarto.
        # `messagebox.askyesno("Confirmar Deleção", ...)` exibe uma
        #       janela com as opções "Sim" e "Não".
        # Se o usuário clicar em "Sim", a variável `confirm` será `True`,
        #       caso contrário, será `False`.
        confirm = messagebox.askyesno("Confirmar Deleção",
                                      f"Tem certeza que deseja deletar o quarto {valores[0]}?")

        # Verifica se o usuário confirmou a deleção do quarto.
        # Se `confirm` for `True`, significa que o usuário clicou
        #       em "Sim" na caixa de confirmação.
        if confirm:
            # Deleta o quarto do banco de dados MongoDB usando o ID.
            # `delete_one({"_id": ObjectId(quarto_id_str)})` busca e remove o
            #       quarto cujo ID corresponde ao selecionado.
            # `ObjectId(quarto_id_str)` converte o ID de string para
            #       um formato compatível com o MongoDB.
            quartos_collection.delete_one({"_id": ObjectId(quarto_id_str)})

            # Exibe uma mensagem informando que o quarto foi deletado com sucesso.
            # `{valores[0]}` representa o número do quarto que foi deletado.
            messagebox.showinfo("Sucesso", f"Quarto '{valores[0]}' deletado.")

            # Chama a função `limpar_campos()` para limpar os campos do formulário.
            # Isso evita que os dados do quarto deletado permaneçam visíveis na interface.
            self.limpar_campos()

            # Atualiza a lista de quartos no Treeview chamando `listar_quartos()`.
            # Isso garante que o quarto deletado desapareça da interface.
            self.listar_quartos()

    # -------------- Função para abrir o "Histórico" deste quarto -------------- #
    def abrir_historico_quarto(self):

        # Verifica se há um quarto selecionado para visualizar o histórico.
        # `self.quarto_em_edicao` contém o ID do quarto em edição.
        # Se for `None`, significa que nenhum quarto foi selecionado.
        if not self.quarto_em_edicao:
            # Exibe uma mensagem de erro informando que é necessário
            #       selecionar um quarto antes de abrir o histórico.
            messagebox.showerror("Erro",
                                 "Selecione um quarto para ver o histórico.")

            # Interrompe a execução da função.
            return

        # Obtém o número do quarto a partir do campo de entrada.
        # `.get().strip()` recupera o valor atual e remove espaços extras.
        numero_quarto = self.numero_quarto_var.get().strip()

        # Verifica se o número do quarto foi preenchido corretamente.
        # Se estiver vazio, exibe uma mensagem de erro e interrompe a execução da função.
        if not numero_quarto:
            messagebox.showerror("Erro",
                                 "Não há número de quarto definido.")

            # Interrompe a execução da função.
            return

        # Abre a nova janela para exibir o histórico do quarto selecionado.
        # `HistoricoQuartoWindow(self, numero_quarto)` instancia a
        #       classe `HistoricoQuartoWindow`,
        #       que é responsável por exibir as informações de ocupação e
        #       histórico do quarto selecionado.
        # - `self`: Passa a referência da tela atual como pai da nova janela.
        # - `numero_quarto`: Passa o número do quarto selecionado para que o
        #       histórico correto seja carregado.
        HistoricoQuartoWindow(self, numero_quarto)


class HistoricoQuartoWindow(tk.Toplevel):
    """
    Exibe o histórico de reservas de um determinado quarto,
    incluindo Data Início, Data Fim, Hóspedes, Valor Final, etc.
    Possui filtros de Data De/Até, Hóspede, e um botão para exportar em Excel.

    Ao dar duplo clique em uma linha do Treeview, abre a tela de edição/detalhe
    da reserva (JanelaEditarReserva)."""

    def __init__(self, pai, numero_quarto):

        # Chama o construtor da classe pai (`tk.Toplevel`), criando
        #       uma nova janela secundária.
        # `super().__init__(pai)` associa esta janela à janela principal (`pai`).
        super().__init__(pai)

        # Define o título da janela, exibindo o número do quarto.
        # `self.title(f"Histórico do Quarto: {numero_quarto}")` formata a
        #       string para exibir o número correto.
        self.title(f"Histórico do Quarto: {numero_quarto}")

        # Armazena a referência da janela principal (pai).
        # `self.pai = pai` permite que a janela de histórico se
        #       comunique com a interface principal.
        self.pai = pai

        # Armazena o número do quarto selecionado.
        # `self.numero_quarto = numero_quarto` permite que a tela
        #       saiba qual quarto exibir no histórico.
        self.numero_quarto = numero_quarto

        # Centraliza a janela na tela ao ser aberta.
        # `self.center_window(900, 600)` define a largura e altura da
        #       janela como 900x600 pixels e a posiciona no centro da tela.
        self.center_window(900, 600)

        # Define a cor de fundo da janela.
        # `self.configure(bg="#f7f7f7")` altera o fundo da janela para
        #       um tom de branco fumê (`#f7f7f7`).
        # Isso melhora a aparência da interface, tornando-a mais suave e
        #       agradável para leitura.
        self.configure(bg="#f7f7f7")

        # Impede que a janela seja redimensionada manualmente.
        # `self.resizable(False, False)` desativa a alteração do tamanho da janela.
        # - O primeiro `False` bloqueia a mudança de largura.
        # - O segundo `False` bloqueia a mudança de altura.
        self.resizable(False, False)

        # Cria uma variável para armazenar o valor do filtro "Data De".
        # `self.data_de_var = tk.StringVar()` define um campo de entrada de
        #       texto para a data inicial da pesquisa.
        # Esse valor será utilizado para filtrar reservas com data de
        #       check-in a partir desta data.
        self.data_de_var = tk.StringVar()

        # Cria uma variável para armazenar o valor do filtro "Data Até".
        # `self.data_ate_var = tk.StringVar()` define um campo de entrada de
        #       texto para a data final da pesquisa.
        # Esse valor será utilizado para filtrar reservas com data de
        #       check-out até esta data.
        self.data_ate_var = tk.StringVar()

        # Cria uma variável para armazenar o nome do hóspede no filtro de busca.
        # `self.filtro_hospede_var = tk.StringVar()` define um campo de
        #       entrada de texto para pesquisar por um hóspede específico.
        # Isso permite que o usuário filtre as reservas de um determinado hóspede pelo nome.
        self.filtro_hospede_var = tk.StringVar()

        # --------------- FRAME FILTROS (linha 1) --------------- #

        # Cria um frame para agrupar os filtros de pesquisa.
        # `ttk.Frame(self)` cria um container dentro da janela atual
        #       para organizar os campos de filtro.
        frame_filtros = ttk.Frame(self)

        # Exibe o frame na interface utilizando o método `.pack()`.
        # - `pady=5`: Adiciona 5 pixels de espaçamento vertical acima e abaixo do frame.
        # - `padx=10`: Adiciona 10 pixels de espaçamento horizontal em ambos os lados.
        # - `fill="x"`: Faz com que o frame ocupe toda a largura da
        #       janela, garantindo alinhamento adequado.
        frame_filtros.pack(pady=5, padx=10, fill="x")

        # Cria um rótulo (Label) para identificar o campo de entrada do filtro "Data De".
        # `ttk.Label(frame_filtros, text="Data De:")` define o texto
        #       do rótulo dentro do `frame_filtros`.
        ttk.Label(frame_filtros, text="Data De:").pack(

            # Posiciona o rótulo à esquerda dentro do frame.
            side="left",

            # Adiciona um espaçamento horizontal de 5 pixels entre o
            #       rótulo e outros elementos.
            padx=5

        )

        # Verifica se a biblioteca TkCalendar está sendo usada.
        # `USANDO_TKCALENDAR` é uma variável booleana que indica se o
        #       DateEntry pode ser utilizado.
        # Se `True`, será exibido um seletor de data (`DateEntry`).
        # Caso contrário, será utilizado um campo de entrada simples (`Entry`).
        if USANDO_TKCALENDAR:

            # Cria um campo de entrada de data utilizando `DateEntry` do TkCalendar.
            # `DateEntry(frame_filtros, textvariable=self.data_de_var,
            #       date_pattern="yyyy-MM-dd", width=12)`
            # - `frame_filtros`: O campo de data é inserido dentro do frame de filtros.
            # - `textvariable=self.data_de_var`: Associa o campo à
            #       variável `self.data_de_var`, permitindo que o valor
            #       selecionado seja armazenado.
            # - `date_pattern="yyyy-MM-dd"`: Define o formato de exibição da
            #       data como "Ano-Mês-Dia" (exemplo: 2024-02-12).
            # - `width=12`: Define a largura do campo para um tamanho adequado.
            self.date_de = DateEntry(frame_filtros,
                                     textvariable=self.data_de_var,
                                     date_pattern="yyyy-MM-dd",
                                     width=12)

            # Posiciona o `DateEntry` dentro do frame de filtros utilizando o método `.pack()`.
            # - `side="left"`: Alinha o campo à esquerda dentro do frame.
            # - `padx=5`: Adiciona um espaçamento horizontal de 5 pixels
            #       entre o campo de data e outros elementos.
            self.date_de.pack(side="left", padx=5)

        # Se `USANDO_TKCALENDAR` for `False`, cria um campo de
        #       entrada simples (`Entry`) para a data.
        else:

            # Cria um campo de entrada (`Entry`) para inserir manualmente a data.
            # `ttk.Entry(frame_filtros, textvariable=self.data_de_var, width=15)`:
            # - `frame_filtros`: O campo de entrada é inserido dentro do frame de filtros.
            # - `textvariable=self.data_de_var`: Associa o campo à variável `self.data_de_var`.
            # - `width=15`: Define uma largura adequada para inserção manual da data.
            # Posiciona o campo de entrada à esquerda dentro do frame.
            # Adiciona um espaçamento horizontal de 5 pixels entre o campo e outros elementos.
            ttk.Entry(frame_filtros,
                      textvariable=self.data_de_var,
                      width=15).pack(side="left",
                                     padx=5)

        # Cria um rótulo (Label) para identificar o campo de
        #       entrada do filtro "Data Até".
        # `ttk.Label(frame_filtros, text="Data Até:")` define o
        #       texto do rótulo dentro do `frame_filtros`.
        # Posiciona o rótulo à esquerda dentro do frame.
        # Adiciona um espaçamento horizontal de 5 pixels
        #       entre o rótulo e outros elementos.
        ttk.Label(frame_filtros,
                  text="Data Até:").pack(side="left",
                                         padx=5)

        # Verifica se a biblioteca TkCalendar está sendo usada.
        # `USANDO_TKCALENDAR` é uma variável booleana que indica se o
        #       DateEntry pode ser utilizado.
        # Se `True`, será exibido um seletor de data (`DateEntry`).
        # Caso contrário, será utilizado um campo de entrada simples (`Entry`).
        if USANDO_TKCALENDAR:

            # Cria um campo de entrada de data utilizando `DateEntry` do TkCalendar.
            # - `frame_filtros`: O campo de data é inserido dentro do frame de filtros.
            # - `textvariable=self.data_ate_var`: Associa o campo à
            #       variável `self.data_ate_var`, permitindo que o valor
            #       selecionado seja armazenado.
            # - `date_pattern="yyyy-MM-dd"`: Define o formato de exibição da
            #       data como "Ano-Mês-Dia" (exemplo: 2024-02-12).
            # - `width=12`: Define a largura do campo para um tamanho adequado.
            self.date_ate = DateEntry(frame_filtros,
                                      textvariable=self.data_ate_var,
                                      date_pattern="yyyy-MM-dd",
                                      width=12)

            # Posiciona o `DateEntry` dentro do frame de filtros utilizando o método `.pack()`.
            # - `side="left"`: Alinha o campo à esquerda dentro do frame.
            # - `padx=5`: Adiciona um espaçamento horizontal de 5 pixels
            #       entre o campo de data e outros elementos.
            self.date_ate.pack(side="left",
                               padx=5)

        # Se `USANDO_TKCALENDAR` for `False`, cria um campo de
        #       entrada simples (`Entry`) para a data.
        else:

            # Cria um campo de entrada (`Entry`) para inserir manualmente a data.
            # `ttk.Entry(frame_filtros, textvariable=self.data_ate_var, width=15)`:
            # - `frame_filtros`: O campo de entrada é inserido dentro do frame de filtros.
            # - `textvariable=self.data_ate_var`: Associa o campo à variável `self.data_ate_var`.
            # - `width=15`: Define uma largura adequada para inserção manual da data.
            # Posiciona o campo de entrada à esquerda dentro do frame.
            # Adiciona um espaçamento horizontal de 5 pixels entre o campo e outros elementos.
            ttk.Entry(frame_filtros,
                      textvariable=self.data_ate_var,
                      width=15).pack(side="left",
                                     padx=5)

        # Cria um rótulo para identificar o campo de entrada do filtro "Hóspede".
        # `text="Hóspede:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_filtros`.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(frame_filtros, text="Hóspede:").pack(side="left", padx=5)

        # Cria um campo de entrada para inserir o nome do hóspede a ser filtrado.
        # `textvariable=self.filtro_hospede_var` associa o campo à
        #       variável que armazenará o nome digitado.
        # `width=15` define a largura do campo para permitir a inserção
        #       de até 15 caracteres visíveis.
        # O campo de entrada é posicionado dentro do `frame_filtros`.
        # `side="left"` alinha o campo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        ttk.Entry(frame_filtros,
                  textvariable=self.filtro_hospede_var,
                  width=15).pack(side="left", padx=5)

        # Cria um botão para aplicar o filtro de pesquisa.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.aplicar_filtro` associa a ação de
        #       aplicar o filtro ao clicar no botão.
        btn_filtrar = ttk.Button(frame_filtros,
                                 text="Filtrar",
                                 command=self.aplicar_filtro)

        # Posiciona o botão dentro do `frame_filtros`.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        btn_filtrar.pack(side="left", padx=10)

        # --------------- TREEVIEW --------------- #

        # Define as colunas da tabela (Treeview).
        # `colunas` contém os nomes das colunas que serão exibidas na interface.
        colunas = ("data_inicio", "data_fim", "hospedes", "valor_final", "data_criacao", "idreserva")

        # Cria um Treeview para exibir o histórico de reservas.
        # `columns=colunas` define as colunas que serão usadas na tabela.
        # `show="headings"` oculta a primeira coluna padrão do Treeview,
        #       exibindo apenas os cabeçalhos personalizados.
        # `height=15` define a quantidade de linhas visíveis na tabela.
        self.tree_historico = ttk.Treeview(self,
                                           columns=colunas,
                                           show="headings",
                                           height=15)

        # Define o cabeçalho da coluna "data_inicio".
        # `text="Início"` define o nome visível no cabeçalho da coluna "data_inicio".
        self.tree_historico.heading("data_inicio", text="Início")

        # Define o cabeçalho da coluna "data_fim".
        # `text="Fim"` define o nome visível no cabeçalho da coluna "data_fim".
        self.tree_historico.heading("data_fim", text="Fim")

        # Define o cabeçalho da coluna "hospedes".
        # `text="Hóspedes"` define o nome visível no cabeçalho da coluna "hospedes".
        self.tree_historico.heading("hospedes", text="Hóspedes")

        # Define o cabeçalho da coluna "valor_final".
        # `text="Valor Final (R$)"` define o nome visível no
        #       cabeçalho da coluna "valor_final".
        self.tree_historico.heading("valor_final", text="Valor Final (R$)")

        # Define o cabeçalho da coluna "data_criacao".
        # `text="Data Criação"` define o nome visível no cabeçalho da coluna "data_criacao".
        self.tree_historico.heading("data_criacao", text="Data Criação")

        # Define o cabeçalho da coluna "idreserva".
        # `text="ID(oculto)"` define o nome visível no cabeçalho da coluna "idreserva".
        # Essa coluna é usada internamente para identificar a reserva,
        #       mas será oculta da interface do usuário.
        self.tree_historico.heading("idreserva", text="ID(oculto)")

        # Ajusta a largura da coluna "idreserva" para 0, tornando-a invisível na tabela.
        # `width=0`: Define a largura como zero, ocultando o conteúdo.
        # `stretch=False`: Impede que a coluna seja redimensionada pelo usuário.
        self.tree_historico.column("idreserva", width=0, stretch=False)

        # Exibe o Treeview na tela utilizando o método `.pack()`.
        # `fill="both"` permite que o widget expanda tanto na largura quanto na altura.
        # `expand=True` faz com que o Treeview ocupe todo o espaço disponível.
        # `padx=10, pady=10` adiciona um espaçamento horizontal e
        #       vertical de 10 pixels ao redor do Treeview.
        self.tree_historico.pack(fill="both", expand=True, padx=10, pady=10)

        # Vincula um evento de duplo clique ao Treeview.
        # `bind("<Double-1>", self.duplo_clique_reserva)` significa que ao
        #       dar um duplo clique em uma linha do Treeview,
        #       a função `self.duplo_clique_reserva` será chamada automaticamente.
        self.tree_historico.bind("<Double-1>", self.duplo_clique_reserva)

        # Cria um rótulo para exibir um resumo das informações do histórico de reservas.
        # `text=""` define um texto inicial vazio, que será atualizado dinamicamente.
        # `font=("Helvetica", 10, "bold")` define a fonte do texto
        #       como Helvetica, tamanho 10, e em negrito.
        self.lbl_resumo = ttk.Label(self,
                                    text="",
                                    font=("Helvetica", 10, "bold"))

        # Exibe o rótulo na tela utilizando o método `.pack()`.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do rótulo.
        self.lbl_resumo.pack(pady=5)

        # --------------- FRAME BOTÕES --------------- #
        # Cria um frame para agrupar os botões de ação.
        frame_botoes = ttk.Frame(self)

        # Exibe o frame na interface utilizando o método `.pack()`.
        # `pady=5` adiciona um espaçamento vertical
        #       de 5 pixels acima e abaixo do frame.
        frame_botoes.pack(pady=5)

        # Cria um botão para exportar os dados do histórico para um arquivo Excel.
        # `text="Exportar Excel"` define o texto exibido no botão.
        # `command=self.exportar_excel` associa a ação de
        #       exportar os dados ao clicar no botão.
        btn_exportar = ttk.Button(frame_botoes,
                                  text="Exportar Excel",
                                  command=self.exportar_excel)

        # Exibe o botão na tela utilizando o método `.pack()`.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels
        #       entre o botão e outros elementos.
        btn_exportar.pack(side="left", padx=10)

        # Cria um botão para fechar a janela.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar a janela ao clicar no botão.
        btn_fechar = ttk.Button(frame_botoes,
                                text="Fechar",
                                command=self.destroy)

        # Exibe o botão na tela utilizando o método `.pack()`.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal de
        #       10 pixels entre o botão e outros elementos.
        btn_fechar.pack(side="left", padx=10)

        # Chama a função para carregar os dados do histórico de reservas.
        # `self.carregar_historico()` busca e exibe os registros no Treeview.
        self.carregar_historico()

    # Define a função para carregar o histórico de reservas do quarto selecionado.
    # `data_de` e `data_ate` são parâmetros opcionais para aplicar um filtro de data.
    def carregar_historico(self, data_de=None, data_ate=None):

        # Remove todos os itens existentes no Treeview antes de carregar os novos dados.
        # `self.tree_historico.get_children()` retorna todas as linhas da tabela.
        # O loop percorre cada item e o remove com `self.tree_historico.delete(item)`,
        # garantindo que a tabela sempre exiba apenas os dados mais recentes.
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)

        # Define a consulta base para buscar as reservas no banco de dados.
        # O critério inicial é buscar apenas as reservas
        #       associadas ao quarto selecionado.
        query_base = {"numero_quarto": self.numero_quarto}

        # Aplica um filtro de datas para buscar reservas dentro do intervalo especificado.
        # Esse filtro verifica sobreposição de períodos, garantindo que qualquer reserva
        # que tenha pelo menos uma parte dentro do intervalo especificado seja incluída.

        # `if data_de or data_ate:` verifica se pelo menos um
        #       dos parâmetros de data foi passado.
        if data_de or data_ate:
            # Adiciona uma condição de expressão (`$expr`) para filtrar as
            #       reservas no MongoDB.
            # Utiliza operadores `$lte` (menor ou igual) e `$gte` (maior ou igual)
            #       para determinar se há sobreposição.
            query_base["$expr"] = {

                # Utiliza o operador `$and` para garantir que ambas as
                #       condições sejam atendidas.
                "$and": [

                    # Verifica se a data de início da reserva (`$data_inicio`) é
                    #       menor ou igual à data máxima (`data_ate`).
                    # Se `data_ate` não for especificado, assume-se "9999-12-31" como um limite alto.
                    {"$lte": ["$data_inicio", data_ate if data_ate else "9999-12-31"]},

                    # Verifica se a data de fim da reserva (`$data_fim`) é maior ou
                    #       igual à data mínima (`data_de`).
                    # Se `data_de` não for especificado, assume-se "0000-01-01"
                    #       como um limite baixo.
                    {"$gte": ["$data_fim", data_de if data_de else "0000-01-01"]}

                ]
            }

        # Executa a consulta no banco de dados para buscar as reservas filtradas.
        # `reservas_collection.find(query_base)` retorna todas as reservas
        #       que atendem aos critérios definidos em `query_base`.
        # `.sort("data_inicio", 1)` ordena os resultados pela coluna "data_inicio" em
        #       ordem crescente (`1` para ascendente, `-1` para descendente).
        reservas = reservas_collection.find(query_base).sort("data_inicio", 1)

        # Obtém o valor do campo de filtro de hóspede digitado pelo usuário.
        # `self.filtro_hospede_var.get().strip().lower()`:
        # - `.get()` obtém o texto digitado no campo.
        # - `.strip()` remove espaços extras no início e no final do texto.
        # - `.lower()` converte o texto para minúsculas para garantir que a
        #       busca seja case-insensitive (não diferencia maiúsculas de minúsculas).
        filtro_hospede = self.filtro_hospede_var.get().strip().lower()

        # Inicializa a variável `soma_valor` para armazenar a
        #       soma total dos valores finais das reservas.
        # Começa com 0.0, garantindo que a variável esteja no tipo float.
        soma_valor = 0.0

        # Inicializa a variável `contagem` para armazenar a
        #       quantidade total de reservas encontradas.
        # Começa com 0, pois ainda nenhuma reserva foi processada.
        contagem = 0

        # Percorre todas as reservas encontradas na consulta.
        for r in reservas:

            # Obtém a data de início da reserva.
            # `r.get("data_inicio", "")` tenta recuperar o valor da chave "data_inicio".
            # Se a chave não existir, retorna uma string vazia.
            data_inicio = r.get("data_inicio", "")

            # Obtém a data de fim da reserva.
            # `r.get("data_fim", "")` tenta recuperar o valor da chave "data_fim".
            # Se a chave não existir, retorna uma string vazia.
            data_fim = r.get("data_fim", "")

            # Obtém a lista de hóspedes da reserva.
            # `r.get("hospedes", [])` tenta recuperar o valor da chave "hospedes".
            # Se a chave não existir, retorna uma lista vazia `[]` como valor padrão.
            hospedes_list = r.get("hospedes", [])

            # Obtém o valor final da reserva e o converte para float.
            # `r.get("valor_final", 0.0)` tenta recuperar o valor da chave "valor_final".
            # Se a chave não existir, retorna `0.0` como valor padrão.
            valor_final = float(r.get("valor_final", 0.0))

            # Obtém a data de criação da reserva.
            # `r.get("data_criacao", "")` tenta recuperar o valor
            #       da chave "data_criacao".
            # Se a chave não existir, retorna uma string vazia.
            data_criacao = r.get("data_criacao", "")

            # Obtém o ID da reserva e o converte para string.
            # `str(r["_id"])` garante que o ID seja tratado como uma
            #       string para exibição no Treeview.
            reserva_id = str(r["_id"])

            # Converte a lista de hóspedes em uma string separada por vírgulas.
            # `", ".join(hospedes_list)` une os elementos da lista `hospedes_list` em
            #       uma única string separada por ", ".
            hospedes_str = ", ".join(hospedes_list)

            # Se houver um filtro de hóspede digitado pelo usuário, verifica se
            #       ele está presente na lista de hóspedes.
            if filtro_hospede:

                # Converte `hospedes_str` para minúsculas e verifica se contém o nome filtrado.
                # `filtro_hospede not in hospedes_str.lower()` verifica se o nome
                #       digitado pelo usuário aparece na lista de hóspedes.
                # Se não aparecer, a reserva é ignorada (`continue`).
                if filtro_hospede not in hospedes_str.lower():
                    continue

            # Insere a reserva na tabela (Treeview) com os valores extraídos.
            self.tree_historico.insert(

                # `""` indica que o item será inserido na raiz do Treeview (sem hierarquia).
                "",

                # `tk.END` adiciona o item no final da lista existente.
                tk.END,

                # `values=(...)` define os valores que serão exibidos nas colunas do Treeview.
                values=(

                    # Data de início da reserva.
                    data_inicio,

                    # Data de fim da reserva.
                    data_fim,

                    # Lista de hóspedes convertida para uma string separada por vírgulas.
                    hospedes_str,

                    # Valor final da reserva formatado com duas casas decimais.
                    f"{valor_final:.2f}",

                    # Data de criação da reserva.
                    data_criacao,

                    # ID da reserva (oculto).
                    reserva_id
                )
            )

            # Soma o valor final da reserva ao total acumulado.
            soma_valor += valor_final

            # Incrementa a contagem de reservas processadas.
            contagem += 1

        # Atualiza o rótulo de resumo com a quantidade total de
        #       reservas e a soma dos valores finais.
        self.lbl_resumo.config(

            # Define o texto exibido no rótulo.
            # Formata a string para mostrar a contagem de reservas e a
            #       soma total do valor final com duas casas decimais.
            text=f"Total de Registros: {contagem} | Soma do Valor Final: R$ {soma_valor:.2f}"

        )

    # Define a função para exportar os dados do histórico
    #       para um arquivo Excel.
    def exportar_excel(self):

        # Obtém todos os itens atualmente listados na tabela (Treeview).
        # `self.tree_historico.get_children()` retorna uma lista com
        #       os identificadores de cada linha exibida.
        itens = self.tree_historico.get_children()

        # Verifica se há registros na tabela antes de prosseguir com a exportação.
        if not itens:
            # Exibe uma mensagem informando que não há dados disponíveis para exportação.
            messagebox.showinfo("Informação",
                                "Não há dados para exportar.")

            # Retorna imediatamente, interrompendo a execução da função.
            return

        # Inicializa uma lista vazia para armazenar os dados
        #       das reservas a serem exportadas.
        linhas_data = []

        # Percorre todos os itens (reservas) exibidos no Treeview.
        for item_id in itens:
            # Obtém os valores da linha correspondente no Treeview.
            # `self.tree_historico.item(item_id, "values")` retorna uma
            #       tupla contendo os valores da reserva selecionada.
            valores = self.tree_historico.item(item_id, "values")

            # Os valores retornados na tupla seguem a estrutura:
            # (data_inicio, data_fim, hospedes, valor_final, data_criacao, idreserva)

            # Adiciona os valores extraídos à lista `linhas_data`.
            # Cada item da lista `linhas_data` representa uma reserva
            #       que será exportada para o Excel.
            linhas_data.append(valores)

        # Define os nomes das colunas que serão usadas no arquivo Excel.
        colunas_df = [

            # "Data Início" representa a data de início da reserva.
            "Data Início",

            # "Data Fim" representa a data de término da reserva.
            "Data Fim",

            # "Hóspedes" contém os nomes dos hóspedes da reserva.
            "Hóspedes",

            # "Valor Final (R$)" representa o valor total da reserva, formatado em reais.
            "Valor Final (R$)",

            # "Data Criação" indica quando a reserva foi registrada no sistema.
            "Data Criação",

            # "ID Reserva" armazena o identificador único da reserva no banco de dados.
            "ID Reserva"

        ]

        # Cria um DataFrame do Pandas contendo os dados das
        #       reservas extraídos do Treeview.
        # `linhas_data` contém todas as linhas processadas anteriormente.
        # `columns=colunas_df` define os nomes das colunas no
        #       DataFrame para melhor organização.
        df = pd.DataFrame(linhas_data, columns=colunas_df)

        # Define o caminho onde o arquivo Excel será salvo.
        # `os.getcwd()` retorna o diretório atual onde o script está sendo executado.
        # `os.path.join(os.getcwd(), "historico_quarto.xlsx")` cria o
        #       caminho completo para o arquivo "historico_quarto.xlsx".
        caminho = os.path.join(os.getcwd(), "historico_quarto.xlsx")

        # Tenta salvar o DataFrame em um arquivo Excel.
        try:

            # Exporta o DataFrame `df` para um arquivo Excel no caminho definido.
            # `df.to_excel(caminho, index=False)`:
            # - `index=False` garante que o Pandas não adicione uma
            #       coluna de índice extra no Excel.
            df.to_excel(caminho, index=False)

            # Exibe uma mensagem informando que a exportação foi concluída com sucesso.
            # `messagebox.showinfo("Sucesso", f"Histórico exportado para: {caminho}")`
            # Mostra um alerta com o caminho onde o arquivo foi salvo.
            messagebox.showinfo("Sucesso",
                                f"Histórico exportado para: {caminho}")

        # Se ocorrer um erro durante a exportação, captura a exceção.
        except Exception as e:

            # Exibe uma mensagem de erro informando o motivo da falha na exportação.
            # `str(e)` converte a exceção em texto para exibição.
            messagebox.showerror("Erro",
                                 f"Erro ao exportar: {str(e)}")

    # Define a função para tratar o evento de duplo clique em
    #       uma reserva no Treeview.
    def duplo_clique_reserva(self, event):

        # Obtém a seleção do usuário no Treeview (`self.tree_historico`).
        sel = self.tree_historico.selection()

        # Verifica se algum item foi selecionado.
        # Se `sel` estiver vazio, significa que o usuário clicou em um
        #       espaço em branco, então a função retorna.
        if not sel:
            return

        # Obtém os valores da linha selecionada no Treeview.
        # `self.tree_historico.item(sel, "values")` retorna uma tupla
        #       contendo os valores da reserva selecionada.
        valores = self.tree_historico.item(sel, "values")

        # Os valores retornados na tupla são:
        # (data_inicio, data_fim, hospedes_str, valor_final, data_criacao, reserva_id)

        # Obtém o ID da reserva selecionada.
        # `valores[5]` representa o sexto elemento da tupla, que
        #       corresponde ao ID da reserva.
        reserva_id_str = valores[5]

        # Verifica se o ID da reserva é válido.
        # Se `reserva_id_str` for uma string vazia ou `None`, a função retorna sem fazer nada.
        if not reserva_id_str:
            return

        # Busca o documento dessa reserva no banco de dados.
        # `reservas_collection.find_one({"_id": ObjectId(reserva_id_str)})` procura a
        #       reserva pelo seu ID único.
        # `ObjectId(reserva_id_str)` converte a string do ID em um objeto `ObjectId`,
        #       necessário para consultas no MongoDB.
        doc_reserva = reservas_collection.find_one({"_id": ObjectId(reserva_id_str)})

        # Verifica se a reserva foi encontrada no banco de dados.
        if doc_reserva:

            # Se a reserva existir, chama a tela de edição da reserva.
            # `JanelaEditarReserva(self, doc_reserva)` cria uma nova
            #       janela para exibir e editar os detalhes da reserva.
            # `self` passa a referência da tela atual como janela principal.
            # `doc_reserva` contém os detalhes da reserva extraídos do banco de dados.
            JanelaEditarReserva(self, doc_reserva)

        # Se a reserva não for encontrada no banco de dados,
        #       exibe uma mensagem de erro.
        else:

            # `messagebox.showerror("Erro", "Não encontrei essa reserva no banco de dados.")`
            # Mostra um alerta informando que a reserva não foi localizada no banco de dados.
            messagebox.showerror("Erro",
                                 "Não encontrei essa reserva no banco de dados.")

    # Define a função para aplicar filtros de data e
    #       atualizar a exibição do histórico.
    def aplicar_filtro(self):

        # Obtém a data inicial inserida pelo usuário.
        # `self.data_de_var.get().strip()` recupera o valor do
        #       campo e remove espaços extras.
        data_de_str = self.data_de_var.get().strip()

        # Obtém a data final inserida pelo usuário.
        # `self.data_ate_var.get().strip()` recupera o valor do
        #       campo e remove espaços extras.
        data_ate_str = self.data_ate_var.get().strip()

        # Inicializa as variáveis de data como `None`, indicando que
        #       nenhum filtro de data foi definido inicialmente.
        data_de = None
        data_ate = None

        # Tenta converter a data inicial (`data_de_str`) para
        #       garantir que está no formato correto.
        try:

            # Se o usuário inseriu uma data inicial, valida o formato "YYYY-MM-DD".
            if data_de_str:
                # Tenta converter a string para uma data válida.
                # Se não for possível, um erro será gerado e tratado no bloco `except`.
                datetime.datetime.strptime(data_de_str, "%Y-%m-%d")

                # Se a conversão for bem-sucedida, armazena `data_de_str`
                #       em `data_de` para ser usada no filtro.
                data_de = data_de_str

        # Se ocorrer um erro ao converter a data, ignora e
        #       mantém `data_de` como `None`.
        except:
            pass

        # Tenta converter a data final (`data_ate_str`) para
        #       garantir que está no formato correto.
        try:

            # Se o usuário inseriu uma data final, valida o formato "YYYY-MM-DD".
            if data_ate_str:
                # `datetime.datetime.strptime(data_ate_str, "%Y-%m-%d")` tenta
                #       converter a string para uma data válida.
                # Se a conversão falhar, um erro será gerado e tratado no bloco `except`.
                datetime.datetime.strptime(data_ate_str, "%Y-%m-%d")

                # Se a conversão for bem-sucedida, armazena `data_ate_str`
                #       em `data_ate` para ser usada no filtro.
                data_ate = data_ate_str

        # Se ocorrer um erro ao converter a data, ignora e
        #       mantém `data_ate` como `None`.
        except:
            pass

        # Chama a função `carregar_historico()` para atualizar a exibição do
        #       histórico com os filtros aplicados.
        # `data_de=data_de` e `data_ate=data_ate` garantem que apenas os
        #       registros dentro do intervalo especificado sejam carregados.
        self.carregar_historico(data_de=data_de, data_ate=data_ate)

    # Define um método chamado `center_window` que centraliza a
    #       janela na tela do usuário.
    # Esse método recebe dois parâmetros: `largura` e `altura`,
    #       que representam as dimensões da janela.
    def center_window(self, largura, altura):

        # Obtém a largura total da tela do usuário.
        # `winfo_screenwidth()` retorna a largura em pixels do monitor
        #       onde a aplicação está sendo executada.
        larg_tela = self.winfo_screenwidth()

        # Obtém a altura total da tela do usuário.
        # `winfo_screenheight()` retorna a altura em pixels do monitor.
        alt_tela = self.winfo_screenheight()

        # Calcula a posição X para centralizar a janela horizontalmente.
        # `(larg_tela - largura) / 2` pega a largura total da tela e
        #       subtrai a largura da janela.
        # Dividindo por 2, encontramos a posição exata para centralizar.
        # `int(...)` converte o valor para um número inteiro, pois `geometry`
        #       não aceita números decimais.
        x = int((larg_tela - largura) / 2)

        # Calcula a posição Y para centralizar a janela verticalmente.
        # `(alt_tela - altura) / 2` pega a altura total da tela e
        #       subtrai a altura da janela.
        # Dividindo por 2, encontramos a posição exata para que a
        #       janela fique centralizada verticalmente.
        y = int((alt_tela - altura) / 2)

        # Define o tamanho e a posição da janela usando `geometry()`.
        # O formato da string é: `"largura x altura + posição_x + posição_y"`.
        # Isso posiciona a janela no centro exato da tela.
        self.geometry(f"{largura}x{altura}+{x}+{y}")



# =============================================================================
# ============= JANELA PARA EDITAR/FINALIZAR RESERVA (TELA CHEIA) =============
# =============================================================================

class JanelaEditarReserva(tk.Toplevel):

    """
    Classe responsável por criar uma janela de edição de reserva.
    Permite visualizar e modificar informações de uma reserva existente.
    """

    def __init__(self, pai, reserva_doc):

        """
        Construtor da classe JanelaEditarReserva.
        Inicializa a janela de edição de uma reserva com base nos dados fornecidos.

        :param pai: Janela ou frame pai, de onde essa janela foi chamada.
        :param reserva_doc: Dicionário contendo os dados da reserva a ser editada.
        """

        # Chama o construtor da classe Toplevel (janela independente)
        #       para criar a janela de edição.
        super().__init__(pai)

        # Define o título da janela com o número do quarto da reserva em questão.
        # Exemplo de título: "Editar Reserva (Quarto 101)"
        self.title(f"Editar Reserva (Quarto {reserva_doc['numero_quarto']})")

        # Configura a janela para ser exibida em tela cheia.
        # Isso garante que o usuário tenha uma visão completa
        #       das informações da reserva.
        self.attributes("-fullscreen", True)

        # Armazena a referência ao frame ou janela pai.
        # Isso é necessário para futuras interações, como
        #       atualizar listas ao salvar alterações.
        self.pai = pai

        # Armazena o ID da reserva para identificar e atualizar o
        #       documento correto no banco de dados.
        # O "_id" é uma chave única gerada pelo MongoDB para
        #       cada documento na coleção.
        self.reserva_id = reserva_doc["_id"]

        # Armazena o número do quarto relacionado à reserva atual.
        # Isso permite exibir e modificar os detalhes do quarto nesta reserva.
        self.numero_quarto = reserva_doc["numero_quarto"]

        # Busca no banco de dados os detalhes do quarto associado a esta reserva.
        # Ele consulta a coleção de quartos para obter informações
        #       adicionais, como capacidade e preço.
        quarto_doc = quartos_collection.find_one({"numero_quarto": self.numero_quarto})

        # Obtém a capacidade máxima do quarto, ou define
        #       como 0 caso o quarto não seja encontrado.
        # A capacidade representa o número máximo de hóspedes permitidos no quarto.
        self.capacidade_quarto = quarto_doc["capacidade"] if quarto_doc else 0

        # Obtém o preço base da diária do quarto, ou define
        #       como 0.0 caso o quarto não seja encontrado.
        # O preço base é o valor padrão cobrado por dia de hospedagem neste quarto.
        self.preco_base_quarto = quarto_doc["preco_diaria"] if quarto_doc else 0.0

        # Cria uma variável do tipo StringVar para armazenar a data de início da reserva.
        # O valor padrão é extraído do documento da reserva;
        #       se não houver valor, define como uma string vazia.
        self.data_inicio_var = tk.StringVar(value=reserva_doc.get("data_inicio", ""))

        # Cria uma variável do tipo StringVar para armazenar a
        #       data de término da reserva.
        # O valor padrão é extraído do documento da reserva; se
        #       não houver valor, define como uma string vazia.
        self.data_fim_var = tk.StringVar(value=reserva_doc.get("data_fim", ""))

        # Cria uma variável do tipo StringVar para armazenar
        #       observações sobre a reserva.
        # Caso a reserva tenha sido criada com observações, elas
        #       são carregadas aqui; senão, a string fica vazia.
        self.observacoes_var = tk.StringVar(value=reserva_doc.get("observacoes", ""))

        # Lista de hóspedes registrados nesta reserva.
        # O valor é extraído diretamente do documento da reserva;
        #       caso não exista, uma lista vazia é usada.
        self.lista_hospedes_reserva = reserva_doc.get("hospedes", [])

        # Lista de produtos consumidos durante a estadia, extraída do banco de dados.
        # Essa lista contém dicionários com os produtos, suas
        #       quantidades e valores unitários.
        # Caso não haja consumo registrado, a lista fica vazia.
        self.lista_consumo = reserva_doc.get("produtos", [])

        # Cria uma variável do tipo DoubleVar para armazenar o valor total da reserva.
        # Esse valor representa o custo total da estadia, incluindo o
        #       preço da hospedagem e os produtos consumidos.
        # Caso o campo "valor_final" não exista no banco, o valor padrão será 0.0.
        self.valor_final_var = tk.DoubleVar(value=reserva_doc.get("valor_final", 0.0))

        # Cria um frame principal dentro da janela para organizar os elementos da interface.
        # O parâmetro `fill="both"` faz com que o frame expanda
        #       tanto na largura quanto na altura.
        # `padx=10, pady=10` adicionam um espaçamento de 10 pixels ao redor do frame.
        frame_principal = ttk.Frame(self)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Inicializa uma variável chamada `linha`, que será usada
        #       para organizar os elementos na grade.
        # A cada novo componente adicionado, essa variável será
        #       incrementada para garantir o alinhamento correto.
        linha = 0

        # Cria um rótulo (Label) que exibe o número do quarto sendo editado.
        # O texto do rótulo inclui o número do quarto armazenado em `self.numero_quarto`.
        # A fonte do texto é definida como Helvetica, tamanho 12 e
        #       negrito para destacar a informação.
        # O `columnspan=2` faz com que o rótulo ocupe duas colunas na grade.
        # O `sticky="w"` alinha o texto à esquerda da célula na grade.
        # O `pady=5` adiciona um espaçamento vertical de 5 pixels abaixo do rótulo.
        ttk.Label(frame_principal,
                  text=f"Quarto: {self.numero_quarto}",
                  font=("Helvetica", 12, "bold")).grid(row=linha,
                                                       column=0,
                                                       columnspan=2,
                                                       sticky="w",
                                                       pady=5)

        # Incrementa a variável `linha` para garantir que o
        #       próximo elemento da interface
        #       seja posicionado na linha seguinte da grade.
        linha += 1

        # Cria um rótulo (Label) para indicar o campo "Data Início".
        # Esse rótulo será posicionado na linha atual e na primeira coluna da grade.
        # O parâmetro `sticky="e"` alinha o texto à direita dentro da célula.
        # O `padx=5` adiciona um espaçamento horizontal de 5 pixels à
        #       esquerda e à direita do rótulo.
        # O `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       acima e abaixo do rótulo.
        ttk.Label(frame_principal,
                  text="Data Início:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (Entry) para exibir a data de início da reserva.
        # O campo está vinculado à variável `self.data_inicio_var`, que contém a data armazenada.
        # A largura do campo de entrada é definida como `width=15`, suficiente
        #       para exibir a data no formato "YYYY-MM-DD".
        # O parâmetro `state="disabled"` impede que o usuário edite manualmente
        #       esse campo, garantindo que a data seja fixa.
        # O `sticky="w"` alinha o campo à esquerda da célula na grade.
        # O `padx=5` adiciona um espaçamento horizontal de 5 pixels à
        #       esquerda e à direita do campo de entrada.
        # O `pady=5` adiciona um espaçamento vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        ttk.Entry(frame_principal,
                  textvariable=self.data_inicio_var,
                  width=15,
                  state="disabled").grid(row=linha, column=1, padx=5, pady=5, sticky="w")

        # Incrementa a variável `linha` para garantir que o
        #       próximo elemento da interface seja posicionado na
        #       linha seguinte da grade.
        linha += 1

        # Cria um rótulo (Label) para indicar o campo "Data Fim".
        # Esse rótulo exibe um texto informativo ao usuário e é
        #       posicionado na linha atual (`linha`),
        # e na primeira coluna (`column=0`) da grade de layout do `frame_principal`.
        # O `sticky="e"` alinha o texto à direita da célula, mantendo o
        #       padrão de alinhamento.
        # O `padx=5` adiciona um espaçamento horizontal de 5 pixels ao
        #       redor do rótulo para melhor espaçamento.
        # O `pady=5` adiciona um espaçamento vertical de 5 pixels,
        #       garantindo uma separação visual adequada.
        ttk.Label(frame_principal,
                  text="Data Fim:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (Entry) para exibir a data de fim da reserva.
        # Esse campo está vinculado à variável `self.data_fim_var`, que
        #       contém a data previamente armazenada no banco de dados.
        # O `width=15` define a largura do campo, permitindo a exibição da
        #       data no formato "YYYY-MM-DD".
        # O parâmetro `state="disabled"` impede que o usuário edite esse campo manualmente,
        # garantindo que a data de fim seja fixa e definida pelo sistema.
        # O `sticky="w"` alinha o campo à esquerda da célula na grade,
        #       mantendo um padrão de layout adequado.
        # O `padx=5` adiciona um espaçamento horizontal para evitar que o
        #       campo fique colado em outros elementos.
        # O `pady=5` adiciona um espaçamento vertical, garantindo uma
        #       distribuição uniforme dos elementos na interface.
        ttk.Entry(frame_principal,
                  textvariable=self.data_fim_var,
                  width=15,
                  state="disabled").grid(row=linha, column=1, padx=5, pady=5, sticky="w")

        # Incrementa a variável `linha` para que os próximos elementos da
        #       interface sejam posicionados na linha seguinte.
        # Isso garante que a organização dos campos siga um fluxo lógico e
        #       bem estruturado dentro da interface gráfica.
        linha += 1

        # Cria um rótulo (Label) para indicar o campo "Hóspedes".
        # Esse rótulo exibe um texto informativo ao usuário e é
        #       posicionado na linha atual (`linha`), e na primeira coluna (`column=0`) da
        #       grade de layout do `frame_principal`.
        # O `sticky="ne"` alinha o texto à direita e no topo da célula,
        #       garantindo um bom alinhamento com a lista de hóspedes.
        # O `padx=5` adiciona um espaçamento horizontal ao redor do rótulo
        #       para evitar que fique colado em outros elementos.
        # O `pady=5` adiciona um espaçamento vertical para manter um layout organizado.
        ttk.Label(frame_principal,
                  text="Hóspedes:").grid(row=linha, column=0, sticky="ne", padx=5, pady=5)

        # Cria uma lista (`Listbox`) que será usada para exibir os
        #       hóspedes associados à reserva.
        # O `width=40` define a largura da lista para que os nomes dos
        #       hóspedes fiquem visíveis sem cortes.
        # O `height=4` define a altura da lista, permitindo que até 4 hóspedes
        #       sejam exibidos antes da barra de rolagem ser necessária.
        self.lst_hospedes = tk.Listbox(frame_principal, width=40, height=4)

        # Posiciona a lista de hóspedes na interface gráfica.
        # `row=linha` mantém a organização do layout na linha atual.
        # `column=1` coloca a lista na segunda coluna, ao lado do rótulo "Hóspedes".
        # O `sticky="w"` alinha a lista à esquerda da célula para manter um design uniforme.
        # O `padx=5` adiciona um espaçamento horizontal entre a lista e os outros elementos.
        # O `pady=5` adiciona um espaçamento vertical para manter uma boa separação visual.
        self.lst_hospedes.grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Itera sobre a lista `self.lista_hospedes_reserva`, que
        #       contém os nomes dos hóspedes da reserva.
        # Para cada hóspede na lista, adiciona o nome na `Listbox`
        #       para exibição ao usuário.
        for h in self.lista_hospedes_reserva:
            self.lst_hospedes.insert(tk.END, h)

        # Incrementa a variável `linha` para garantir que os próximos elementos
        #       da interface sejam adicionados na linha seguinte.
        linha += 1

        # Cria um rótulo (Label) para indicar o campo "Produtos".
        # Esse rótulo serve para informar o usuário que abaixo haverá um espaço
        #       para visualizar ou adicionar produtos consumidos na reserva.
        # `row=linha` posiciona o rótulo na linha atual da grade de layout.
        # `column=0` define que ele ficará na primeira coluna da interface.
        # `sticky="e"` alinha o texto à direita dentro da célula, garantindo um
        #       melhor alinhamento com o campo ao lado.
        # `padx=5` adiciona um pequeno espaçamento horizontal para evitar
        #       que o rótulo fique colado nos elementos vizinhos.
        # `pady=5` adiciona um espaçamento vertical para manter uma
        #       separação clara entre os elementos.
        ttk.Label(frame_principal,
                  text="Produtos:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um frame (contêiner) que servirá como um agrupador de
        #       widgets relacionados aos produtos.
        # Esse frame será usado para organizar visualmente os componentes
        #       que permitem adicionar e visualizar os produtos consumidos na reserva.
        # Assim, facilita a organização da interface e melhora a experiência do usuário.
        frame_prod = ttk.Frame(frame_principal)

        # Posiciona o frame na interface gráfica na mesma
        #       linha (`row=linha`) onde está o rótulo "Produtos".
        # `column=1` define que ele ficará na segunda coluna, ao lado do rótulo.
        # `sticky="w"` alinha o frame à esquerda da célula,
        #       garantindo um design mais uniforme.
        frame_prod.grid(row=linha, column=1, sticky="w")

        # Cria uma variável de controle para armazenar o nome do produto selecionado.
        # `tk.StringVar()` permite que essa variável seja usada
        #       para interagir com widgets, como o Combobox.
        self.produto_var = tk.StringVar()

        # Cria uma variável de controle para armazenar a quantidade do
        #       produto que será consumido.
        # `tk.IntVar(value=1)` define que o valor inicial da variável será 1,
        #       garantindo que a reserva tenha pelo menos 1 unidade
        #       do produto por padrão.
        self.quantidade_var = tk.IntVar(value=1)

        # Consulta a coleção de produtos no banco de dados para obter uma
        #       lista dos nomes de todos os produtos cadastrados.
        # Isso permitirá que os produtos disponíveis sejam exibidos em um
        #       Combobox, facilitando a seleção pelo usuário.
        lista_produtos = [p["nome"] for p in produtos_collection.find()]

        # Cria um Combobox (caixa de seleção suspensa) para listar os
        #       produtos disponíveis no banco de dados.
        # O usuário poderá selecionar um produto da lista para adicioná-lo à reserva.
        # `frame_prod` define que o Combobox será adicionado dentro do
        #       frame específico para produtos.
        # `textvariable=self.produto_var` associa a variável `self.produto_var` ao
        #       Combobox, permitindo capturar e manipular o valor selecionado.
        # `values=lista_produtos` preenche o Combobox com os nomes dos
        #       produtos recuperados do banco de dados.
        # `width=20` define a largura do Combobox para que o
        #       texto dos produtos possa ser exibido adequadamente.
        combo_prod = ttk.Combobox(frame_prod,
                                  textvariable=self.produto_var,
                                  values=lista_produtos,
                                  width=20)

        # Posiciona o Combobox dentro do `frame_prod`, garantindo uma
        #       organização visual coerente.
        # `side="left"` alinha o widget à esquerda dentro do frame, permitindo
        #       que outros elementos fiquem ao lado dele.
        # `padx=3` adiciona um pequeno espaçamento horizontal entre os
        #       elementos, evitando que fiquem muito próximos um do outro.
        combo_prod.pack(side="left", padx=3)

        # Cria um widget Spinbox para permitir que o usuário selecione a
        #       quantidade do produto a ser adicionado.
        # `from_=1` define o valor mínimo como 1, garantindo que pelo
        #       menos uma unidade seja selecionada.
        # `to=999` define o valor máximo permitido como 999, limitando a
        #       quantidade a um número razoável.
        # `textvariable=self.quantidade_var` associa a variável `self.quantidade_var` ao
        #       Spinbox, permitindo capturar e manipular a quantidade selecionada.
        # `width=5` define a largura do Spinbox, garantindo que os números
        #       fiquem visíveis de forma adequada.
        spin_qtd = ttk.Spinbox(frame_prod,
                               from_=1,
                               to=999,
                               textvariable=self.quantidade_var,
                               width=5)

        # Posiciona o Spinbox dentro do `frame_prod`, garantindo um alinhamento
        #       adequado junto ao Combobox e botão de adicionar.
        # `side="left"` alinha o Spinbox à esquerda dentro do frame, permitindo
        #       que os outros elementos fiquem ao lado dele.
        # `padx=3` adiciona um pequeno espaçamento horizontal para evitar que os
        #       elementos fiquem muito próximos.
        spin_qtd.pack(side="left", padx=3)

        # Cria um botão que, ao ser clicado, adiciona o produto e a
        #       quantidade selecionada à reserva do cliente.
        # `text="Add"` define o texto exibido no botão, indicando sua funcionalidade.
        # `command=self.adicionar_produto` associa a função `adicionar_produto` ao
        #       botão, que será executada ao clicar nele.
        btn_add_p = ttk.Button(frame_prod,
                               text="Add",
                               command=self.adicionar_produto)

        # Posiciona o botão dentro do `frame_prod`, garantindo que ele
        #       fique alinhado corretamente com o Combobox e o Spinbox.
        # `side="left"` alinha o botão à esquerda dentro do frame,
        #       mantendo a organização visual.
        # `padx=3` adiciona um pequeno espaçamento horizontal, melhorando a
        #       legibilidade e a estética da interface.
        btn_add_p.pack(side="left", padx=3)

        # Incrementa o valor da variável `linha` para posicionar
        #       corretamente os próximos elementos na interface.
        # Isso garante que os próximos widgets sejam posicionados
        #       abaixo deste grupo de elementos.
        linha += 1

        # Cria um widget Treeview para exibir a lista de produtos consumidos na reserva.
        # `columns=("nome", "preco", "qtd", "subtotal")` define as colunas da tabela.
        # `"nome"` representa o nome do produto.
        # `"preco"` exibe o preço unitário do produto.
        # `"qtd"` mostra a quantidade consumida do produto.
        # `"subtotal"` exibe o valor total (preço x quantidade).
        # `show="headings"` esconde a primeira coluna padrão do Treeview,
        #       deixando visíveis apenas os cabeçalhos definidos.
        # `height=5` define o número de linhas visíveis, ajustando a
        #       altura do widget para exibir até 5 produtos simultaneamente.
        self.tree_produtos = ttk.Treeview(frame_principal,
                                          columns=("nome", "preco", "qtd", "subtotal"),
                                          show="headings",
                                          height=5)

        # Define o cabeçalho da coluna "nome" para que seja exibido como "Produto".
        self.tree_produtos.heading("nome", text="Produto")

        # Define o cabeçalho da coluna "preco" para que seja exibido como "Preço".
        self.tree_produtos.heading("preco", text="Preço")

        # Define o cabeçalho da coluna "qtd" para que seja exibido
        #       como "Qtde" (abreviação de Quantidade).
        self.tree_produtos.heading("qtd", text="Qtde")

        # Define o cabeçalho da coluna "subtotal" para que seja exibido
        #       como "Subtotal", mostrando o custo total do produto na reserva.
        self.tree_produtos.heading("subtotal", text="Subtotal")

        # Posiciona o Treeview na interface, dentro do `frame_principal`.
        # `row=linha` coloca o widget na linha atual, garantindo que ele
        #       seja inserido na posição correta na interface.
        # `column=1` posiciona o widget na segunda coluna do layout,
        #       alinhado ao restante dos elementos.
        # `sticky="w"` alinha o widget à esquerda dentro da célula da
        #       grade, garantindo um layout organizado.
        # `padx=5` adiciona um pequeno espaçamento horizontal para
        #       separar o widget de outros elementos ao seu redor.
        # `pady=5` adiciona um pequeno espaçamento vertical, melhorando a
        #       legibilidade e a organização da interface.
        self.tree_produtos.grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Percorre a lista de produtos consumidos na reserva (`self.lista_consumo`).
        # Para cada produto `p` na lista, insere uma nova linha
        #       no Treeview (`self.tree_produtos`).
        # `"nome"` → Nome do produto.
        # `"preco"` → Preço unitário formatado com duas casas decimais.
        # `"quantidade"` → Quantidade consumida do produto.
        # `"subtotal"` → Valor total (preço x quantidade), também
        #       formatado com duas casas decimais.
        for p in self.lista_consumo:
            self.tree_produtos.insert(
                "",  # Inserção na raiz da árvore (Treeview).
                tk.END,  # Adiciona o item no final da lista.
                values=(
                    p["nome"],  # Nome do produto.
                    f"{p['preco']:.2f}",  # Preço unitário formatado para duas casas decimais.
                    p["quantidade"],  # Quantidade consumida.
                    f"{p['subtotal']:.2f}"  # Valor total formatado.
                )
            )

        # Cria um botão para remover um produto da lista de consumo.
        # `text="Remover Produto"` define o texto exibido no botão.
        # `command=self.remover_produto` associa o botão à
        #       função `remover_produto`, que será chamada ao clicar.
        btn_rem_p = ttk.Button(frame_principal,
                               text="Remover Produto",
                               command=self.remover_produto)

        # Posiciona o botão "Remover Produto" na interface.
        # `row=linha` posiciona o botão na linha atual do layout.
        # `column=2` coloca o botão na terceira coluna da grade.
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       botão de outros elementos.
        # `pady=5` adiciona espaçamento vertical para manter um
        #       layout organizado.
        btn_rem_p.grid(row=linha, column=2, padx=5, pady=5)

        # Incrementa a variável `linha` para posicionar corretamente os
        #       próximos elementos na interface.
        linha += 1

        # Cria um rótulo (Label) indicando o campo "Valor Final"
        # `text="Valor Final:"` define o texto do rótulo.
        # `grid(row=linha, column=0, sticky="e", padx=5, pady=5)`
        #       posiciona o rótulo na interface:
        #   - `row=linha` define a linha atual (controlada pela variável `linha`).
        #   - `column=0` coloca o rótulo na primeira coluna.
        #   - `sticky="e"` alinha o texto à direita dentro da célula.
        #   - `padx=5, pady=5` adiciona espaçamento externo ao redor do rótulo.
        ttk.Label(frame_principal,
                  text="Valor Final:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (Entry) para exibir o valor final da reserva.
        # O campo exibe o valor total calculado da reserva (diárias + produtos consumidos).
        # `textvariable=self.valor_final_var` associa o campo a uma
        #       variável Tkinter (`self.valor_final_var`).
        # `width=20` define a largura do campo (20 caracteres).
        # `state="readonly"` impede a edição manual pelo usuário.
        # `grid(row=linha, column=1, sticky="w", padx=5, pady=5)` define a posição:
        #   - `row=linha` mantém o alinhamento com o rótulo.
        #   - `column=1` posiciona o campo na segunda coluna.
        #   - `sticky="w"` alinha o conteúdo à esquerda dentro da célula.
        #   - `padx=5, pady=5` adiciona espaçamento ao redor do campo.
        ttk.Entry(frame_principal,
                  textvariable=self.valor_final_var,
                  width=20,
                  state="readonly").grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Incrementa a variável `linha` para que os próximos
        #       elementos fiquem na linha abaixo.
        linha += 1

        # Cria um rótulo (Label) para o campo "Observações".
        # `text="Observações:"` define o texto exibido no rótulo.
        # `grid(row=linha, column=0, sticky="e", padx=5, pady=5)`
        #       define o posicionamento do rótulo:
        #   - `row=linha` coloca o rótulo na linha atual.
        #   - `column=0` define a primeira coluna como local do rótulo.
        #   - `sticky="e"` alinha o texto à direita dentro da célula.
        #   - `padx=5, pady=5` adiciona espaçamento externo para evitar que os elementos fiquem colados.
        ttk.Label(frame_principal,
                  text="Observações:").grid(row=linha,
                                            column=0,
                                            sticky="e",
                                            padx=5,
                                            pady=5)

        # Cria um campo de entrada (Entry) para digitação de observações da reserva.
        # Esse campo pode ser usado para inserir detalhes adicionais sobre a reserva.
        # `textvariable=self.observacoes_var` associa o campo a uma
        #       variável do Tkinter (`self.observacoes_var`),
        # permitindo que o valor seja armazenado e recuperado facilmente.
        # `width=30` define a largura do campo, permitindo a inserção de um texto mais longo.
        # `grid(row=linha, column=1, sticky="w", padx=5, pady=5)` define a posição do campo:
        #   - `row=linha` mantém o alinhamento com o rótulo.
        #   - `column=1` coloca o campo na segunda coluna, ao lado do rótulo.
        #   - `sticky="w"` alinha o conteúdo à esquerda dentro da célula.
        #   - `padx=5, pady=5` adiciona espaçamento ao redor do campo,
        #           garantindo um layout mais limpo.
        ttk.Entry(frame_principal,
                  textvariable=self.observacoes_var,
                  width=30).grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Incrementa a variável `linha`, garantindo que os
        #       próximos elementos sejam posicionados na linha abaixo.
        linha += 1

        # Cria um contêiner (Frame) para organizar os botões na interface gráfica.
        # `frame_principal` é o frame pai onde os elementos estão sendo organizados.
        # `ttk.Frame(frame_principal)` cria um novo frame dentro do principal.
        frame_btns = ttk.Frame(frame_principal)

        # Posiciona o frame na grade de layout da interface gráfica.
        # `grid(row=linha, column=0, columnspan=3, pady=10)` define:
        #   - `row=linha` coloca o frame na linha atual da grade.
        #   - `column=0` define que ele começa na primeira coluna.
        #   - `columnspan=3` faz com que o frame ocupe três colunas na grade.
        #   - `pady=10` adiciona 10 pixels de espaçamento vertical
        #           para separar o frame de outros elementos.
        frame_btns.grid(row=linha, column=0, columnspan=3, pady=10)

        # Cria um botão para salvar as alterações na reserva.
        # `text="Salvar Alterações"` define o texto exibido no botão.
        # `command=self.salvar_alteracoes` associa a
        #       função `salvar_alteracoes` ao botão, para que ao ser
        #       pressionado, o sistema processe e salve as mudanças
        #       feitas pelo usuário.
        btn_salvar = ttk.Button(frame_btns,
                                text="Salvar Alterações",
                                command=self.salvar_alteracoes)

        # Posiciona o botão dentro do frame `frame_btns`,
        #       garantindo um layout organizado.
        # `pack(side="left", padx=5)` define:
        #   - `side="left"` faz com que o botão seja posicionado à
        #       esquerda dentro do frame.
        #   - `padx=5` adiciona um espaçamento horizontal de 5 pixels ao
        #       redor do botão, evitando que fique colado a outros elementos.
        btn_salvar.pack(side="left", padx=5)

        # Cria um botão para finalizar a reserva.
        # `text="Finalizar Reserva"` define o texto exibido no botão.
        # `command=self.finalizar_reserva` associa a ação do botão à
        #       função `finalizar_reserva`, que será executada ao clicar no botão.
        #  Essa função marcará a reserva como concluída.
        btn_finalizar = ttk.Button(frame_btns,
                                   text="Finalizar Reserva",
                                   command=self.finalizar_reserva)

        # Posiciona o botão dentro do frame `frame_btns` para manter a
        #       organização do layout.
        # `pack(side="left", padx=5)` define:
        #   - `side="left"` alinha o botão à esquerda dentro do frame,
        #       garantindo que outros botões
        #     possam ser adicionados ao lado dele sem sobreposição.
        #   - `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre este botão e os demais elementos,
        #       evitando que fiquem colados.
        btn_finalizar.pack(side="left", padx=5)

        # Cria um botão para cancelar a reserva.
        # `text="Cancelar Reserva"` define o texto exibido no botão.
        # `command=self.cancelar_reserva` associa a ação do botão à
        #       função `cancelar_reserva`, que remove a
        #       reserva do sistema e devolve os itens ao estoque.
        btn_cancelar = ttk.Button(frame_btns,
                                  text="Cancelar Reserva",
                                  command=self.cancelar_reserva)

        # Posiciona o botão dentro do frame `frame_btns`, garantindo que
        #       ele fique ao lado do botão "Finalizar Reserva".
        # `pack(side="left", padx=5)` define:
        #   - `side="left"` posiciona o botão à esquerda dentro do
        #       frame, mantendo um layout organizado.
        #   - `padx=5` adiciona um espaçamento horizontal de 5 pixels,
        #       garantindo que o botão não fique colado ao outro,
        #       proporcionando melhor experiência visual ao usuário.
        btn_cancelar.pack(side="left", padx=5)

        # Cria um botão para fechar a janela.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.fechar_janela` associa a ação do botão à função `fechar_janela`,
        #       que será chamada quando o botão for pressionado. Essa
        #       função geralmente fecha a tela e pode atualizar dados na
        #       interface principal se necessário.
        btn_fechar = ttk.Button(frame_btns,
                                text="Fechar",
                                command=self.fechar_janela)

        # Posiciona o botão dentro do frame `frame_btns`, garantindo
        #       que fique organizado no layout.
        # `pack(side="left", padx=5)` define:
        #   - `side="left"` alinha o botão à esquerda dentro do frame,
        #       garantindo que outros botões
        #     fiquem ao lado dele sem sobreposição.
        #   - `padx=5` adiciona um espaçamento horizontal de 5 pixels,
        #       evitando que o botão fique
        #     muito colado aos outros elementos.
        btn_fechar.pack(side="left", padx=5)

        # Recalcula o total da reserva.
        # A função `recalcular_total` é chamada para atualizar o valor
        #       total da reserva com base nos produtos consumidos e no
        #       número de diárias do quarto.
        # Isso garante que qualquer modificação feita antes de fechar a
        #       janela seja refletida no valor final.
        self.recalcular_total()


    def adicionar_produto(self):

        # Obtém o nome do produto selecionado pelo usuário no campo 'produto_var'.
        # `strip()` remove espaços em branco extras antes e depois do nome.
        nome_prod = self.produto_var.get().strip()

        # Obtém a quantidade digitada pelo usuário no campo 'quantidade_var'.
        qtd = self.quantidade_var.get()

        # Verifica se o nome do produto está vazio ou se a
        #       quantidade é menor ou igual a zero.
        # Isso impede que produtos inválidos ou com quantidade
        #       negativa sejam adicionados.
        if not nome_prod or qtd <= 0:

            # Sai da função sem fazer nada se os dados não forem válidos.
            return

        # Busca o documento do produto no banco de dados `produtos_collection`
        #       que possui o nome igual ao `nome_prod`.
        # Isso serve para verificar se o produto realmente existe e
        #       obter informações adicionais, como o preço e estoque.
        prod_doc = produtos_collection.find_one({"nome": nome_prod})

        # Verifica se o produto não foi encontrado no banco de dados.
        # Se `prod_doc` for None, significa que não há um
        #       produto com esse nome no banco.
        if not prod_doc:

            # Exibe uma mensagem de erro informando que o
            #       produto não foi encontrado.
            messagebox.showerror("Erro",
                                 f"Produto '{nome_prod}' não encontrado.")

            # Sai da função sem continuar a execução.
            return

        # Obtém a quantidade disponível do produto no estoque.
        # Se o campo "quantidade" não existir no documento do
        #       produto, assume o valor padrão `0`.
        estoque_atual = prod_doc.get("quantidade", 0)

        # Verifica se a quantidade disponível no estoque é menor do
        #       que a quantidade solicitada pelo usuário.
        if estoque_atual < qtd:

            # Exibe uma mensagem de erro informando que o estoque é insuficiente.
            # Mostra ao usuário a quantidade real disponível no estoque.
            messagebox.showerror("Erro",
                                 f"Estoque insuficiente. Em estoque: {estoque_atual}")

            # Sai da função para evitar que o produto seja
            #       adicionado sem estoque suficiente.
            return

        # Obtém o preço unitário do produto a partir do banco de dados.
        # O campo "preco" deve existir no documento do produto.
        preco = prod_doc["preco"]

        # Calcula o subtotal do item consumido.
        # O subtotal é o preço unitário multiplicado pela
        #       quantidade desejada pelo usuário.
        subtotal = preco * qtd

        # Cria um dicionário representando o item consumido na reserva.
        # Ele armazena o nome do produto, o preço unitário, a
        #       quantidade consumida e o valor total do consumo.
        item_consumo = {
            "nome": nome_prod,  # Nome do produto selecionado
            "preco": preco,  # Preço unitário do produto
            "quantidade": qtd,  # Quantidade selecionada pelo usuário
            "subtotal": subtotal  # Valor total (preço unitário * quantidade)
        }

        # Adiciona o item consumido à lista de produtos consumidos da reserva.
        # Essa lista é mantida em memória e será usada para
        #       salvar a reserva posteriormente.
        self.lista_consumo.append(item_consumo)

        # Atualiza o estoque do produto no banco de dados.
        # Usa a operação `$inc` do MongoDB para subtrair a
        #       quantidade consumida do estoque.
        produtos_collection.update_one(
            {"_id": prod_doc["_id"]},  # Localiza o produto pelo ID
            {"$inc": {"quantidade": -qtd}}  # Diminui a quantidade no estoque
        )

        # Insere o item na Treeview (interface gráfica).
        # Isso atualiza a lista de produtos consumidos exibida na tela.
        # Formata os valores numéricos para exibição
        #       amigável (2 casas decimais para preços).
        self.tree_produtos.insert("",

                                  # Insere como um novo item no final da lista
                                  tk.END,

                                  # Valores que serão mostrados na UI
                                  values=(nome_prod, f"{preco:.2f}", qtd, f"{subtotal:.2f}"))

        # Recalcula o valor total da reserva considerando
        #       os produtos consumidos.
        # Esse método soma todos os produtos e diárias para
        #       atualizar o valor final da reserva.
        self.recalcular_total()



    def remover_produto(self):

        # Obtém a seleção atual da Treeview que exibe os
        #       produtos consumidos na reserva.
        # Se nenhum item estiver selecionado, a função
        #       simplesmente retorna e não faz nada.
        sel = self.tree_produtos.selection()

        # Verifica se algum item foi selecionado antes de continuar.
        # Caso contrário, sai da função imediatamente.
        if not sel:

            # Nenhum produto foi selecionado, então não há
            #       nada para remover.
            return

        # Obtém os valores do item selecionado na Treeview.
        # A função `item(sel, "values")` retorna uma tupla com os
        #       valores das colunas do item selecionado.
        item_valores = self.tree_produtos.item(sel, "values")

        # Extrai o nome do produto consumido que será removido.
        # Esse valor é armazenado na primeira posição da tupla `item_valores[0]`.
        nome = item_valores[0]  # Nome do produto selecionado para remoção.

        # Obtém a quantidade do produto consumido na reserva.
        # O valor da quantidade está na terceira posição da
        #       tupla `item_valores[2]` e precisa ser convertido para um inteiro.
        qtd = int(item_valores[2])  # Converte a quantidade de string para inteiro.

        # Obtém o subtotal gasto com esse produto na reserva.
        # O subtotal representa o valor total pago pelo número de
        #       unidades consumidas desse produto.
        # Ele está na quarta posição da tupla `item_valores[3]` e
        #       deve ser convertido para um número decimal (float).
        subtotal = float(item_valores[3])  # Converte o subtotal de string para float.

        # Percorre a lista de produtos consumidos na reserva (`self.lista_consumo`).
        # Utiliza `enumerate()` para obter tanto o índice (`i`) quanto o item (`it`).
        for i, it in enumerate(self.lista_consumo):

            # Verifica se o produto armazenado na lista corresponde ao
            #       nome do produto que será removido.
            # Também confere se a quantidade consumida e o subtotal são os mesmos.
            # A condição `abs(it["subtotal"] - subtotal) < 1e-9` é
            #       usada para evitar problemas com arredondamento de números decimais.
            if it["nome"] == nome and it["quantidade"] == qtd and abs(it["subtotal"] - subtotal) < 1e-9:

                # Remove o item correspondente da lista de produtos consumidos.
                self.lista_consumo.pop(i)

                # Após encontrar o item e removê-lo, interrompe o loop com `break`,
                # pois já não é necessário continuar procurando.
                break

        # Agora que o item foi removido da lista, devemos devolvê-lo ao estoque.

        # Busca o documento do produto no banco de dados MongoDB pelo nome.
        # Se o produto existir no banco, ele será atualizado no próximo passo.
        prod_doc = produtos_collection.find_one({"nome": nome})

        # Verifica se o produto foi encontrado no banco de dados.
        if prod_doc:

            # Atualiza a quantidade do produto no banco de dados,
            #       devolvendo a quantidade removida.
            # O operador `$inc` incrementa (ou decrementa, se negativo) o
            #   valor de um campo no MongoDB.
            produtos_collection.update_one({"_id": prod_doc["_id"]},
                                           {"$inc": {"quantidade": qtd}})

        # Remove o produto da interface gráfica (`Treeview`), garantindo que
        #       ele desapareça visualmente da reserva.
        self.tree_produtos.delete(sel)

        # Recalcula o total da reserva, pois a remoção do produto
        #       pode impactar o valor total.
        self.recalcular_total()



    def salvar_alteracoes(self):

        # Atualiza a reserva no banco de dados MongoDB usando o
        #       identificador único (self.reserva_id)
        reservas_collection.update_one(
            {"_id": self.reserva_id},  # Localiza a reserva pelo ID
            {
                "$set": {  # Define os novos valores para atualização
                    "produtos": self.lista_consumo,  # Atualiza a lista de produtos consumidos
                    "hospedes": self.lista_hospedes_reserva,  # Atualiza a lista de hóspedes na reserva
                    "valor_final": self.valor_final_var.get(),  # Atualiza o valor final da reserva
                    "observacoes": self.observacoes_var.get().strip()
                    # Atualiza as observações da reserva (removendo espaços extras)
                }
            }
        )

        # Exibe uma mensagem de sucesso para o usuário informando
        #       que as alterações foram salvas com sucesso.
        messagebox.showinfo("Sucesso", "Alterações salvas!")

        # Fecha a janela de edição da reserva, retornando à tela anterior.
        self.fechar_janela()


    def finalizar_reserva(self):

        # Exibe uma caixa de diálogo de confirmação para o usuário.
        # O usuário pode escolher "Sim" (True) ou "Não" (False).
        if messagebox.askyesno("Confirmar",
                               "Deseja realmente finalizar esta reserva?"):

            # Atualiza o status da reserva no banco de dados MongoDB.
            # Filtra a reserva específica pelo ID (_id) armazenado em self.reserva_id.
            reservas_collection.update_one(
                {"_id": self.reserva_id},  # Filtro para encontrar a reserva no banco de dados
                {
                    "$set": {  # Modifica apenas os campos especificados dentro deste dicionário

                        # Define o status da reserva como "Finalizada"
                        "status": "Finalizada",

                        # Registra a data de finalização da reserva no formato YYYY-MM-DD.
                        # Usa a data atual do sistema para garantir precisão no histórico.
                        "data_finalizacao": datetime.datetime.now().strftime("%Y-%m-%d")

                    }
                }
            )

            # Exibe uma mensagem informando ao usuário que a
            #       reserva foi finalizada com sucesso.
            # Essa confirmação garante que o usuário saiba que a
            #       ação foi concluída corretamente.
            messagebox.showinfo("Sucesso",
                                "Reserva finalizada!")

        # Fecha a janela atual após finalizar a reserva.
        # Isso garante que o usuário retorne à tela principal após a finalização.
        self.fechar_janela()


    def cancelar_reserva(self):

        # Busca a reserva no banco de dados utilizando
        #       o ID armazenado em self.reserva_id.
        # Isso garante que estamos operando na reserva correta.
        reserva_doc = reservas_collection.find_one({"_id": self.reserva_id})

        # Verifica se a reserva foi encontrada antes de prosseguir.
        if reserva_doc:

            # Percorre todos os produtos consumidos na reserva.
            for item in reserva_doc.get("produtos", []):

                # Obtém o nome do produto e a quantidade consumida.
                nome_prod = item["nome"]
                qtd = item["quantidade"]

                # Busca o documento do produto no banco de dados para garantir que ele existe.
                prod_doc = produtos_collection.find_one({"nome": nome_prod})

                # Se o produto foi encontrado no banco, devolvemos a quantidade ao estoque.
                if prod_doc:
                    produtos_collection.update_one(
                        {"_id": prod_doc["_id"]},  # Localiza o produto pelo ID no banco.
                        {"$inc": {"quantidade": qtd}}  # Adiciona de volta a quantidade consumida.
                    )

            # Remove a reserva do banco de dados, pois ela foi cancelada.
            reservas_collection.delete_one({"_id": self.reserva_id})

            # Exibe uma mensagem informando ao usuário que a reserva
            #       foi cancelada com sucesso.
            messagebox.showinfo("Cancelado",
                                "Reserva cancelada e itens devolvidos ao estoque.")

        # Fecha a janela após o cancelamento da reserva.
        self.fechar_janela()


    # Define um método para fechar a janela.
    def fechar_janela(self):

        # Verifica se o objeto pai possui o método 'atualizar_mapa'.
        # `hasattr(self.pai, 'atualizar_mapa')` verifica se o método existe.
        # `self.pai.atualizar_mapa()` chama o método para atualizar a exibição dos quartos.
        if hasattr(self.pai, 'atualizar_mapa'):
            self.pai.atualizar_mapa()

        # Verifica se o objeto pai possui o método 'atualizar_relatorio'.
        # `hasattr(self.pai, 'atualizar_relatorio')` verifica se o método existe.
        # `self.pai.atualizar_relatorio()` chama o método para
        #       atualizar a exibição do relatório geral.
        if hasattr(self.pai, 'atualizar_relatorio'):
            self.pai.atualizar_relatorio()

        # Fecha a janela atual.
        # `self.destroy()` fecha a janela e libera os
        #       recursos da interface gráfica.
        self.destroy()


    def recalcular_total(self):

        # Calcula o total dos produtos consumidos na reserva.
        # Utiliza a função `sum()` para somar o campo "subtotal" de
        #       cada item na lista `self.lista_consumo`.
        total_produtos = sum(it["subtotal"] for it in self.lista_consumo)

        try:

            # Obtém e converte a data de início da reserva do
            #       campo `self.data_inicio_var`.
            # Usa `strptime()` para transformar a string no
            #       formato "YYYY-MM-DD" em um objeto `datetime`.
            dt_ini = datetime.datetime.strptime(self.data_inicio_var.get(), "%Y-%m-%d")

            # Obtém e converte a data de fim da reserva.
            dt_fim = datetime.datetime.strptime(self.data_fim_var.get(), "%Y-%m-%d")

            # Calcula a quantidade de dias da reserva subtraindo a
            #       data de início da data de fim.
            dias = (dt_fim - dt_ini).days

            # Garante que a reserva tenha pelo menos 1 dia (caso a data
            #       de fim seja no mesmo dia da data de início).
            if dias < 1:

                # Uma reserva mínima de 1 diária
                dias = 1

        except:

            # Caso ocorra um erro ao converter as datas (exemplo:
            #       campo vazio ou formato inválido),
            #       assume-se um valor padrão de 1 diária para
            #       evitar falhas no cálculo.
            dias = 1

        # Calcula o total da hospedagem multiplicando o preço-base do
        #       quarto pela quantidade de dias da reserva.
        total_quarto = self.preco_base_quarto * dias

        # Atualiza o campo `self.valor_final_var` com o valor total da reserva.
        # O total inclui o custo da hospedagem (quarto) mais o
        #       custo dos produtos consumidos.
        self.valor_final_var.set(total_quarto + total_produtos)



# =============================================================================
# ================ TELA DE GERENCIAMENTO DE PRODUTOS (CRUD) ===================
# =============================================================================

# Define a classe `TelaGerenciarProdutos`, que representa a
#       interface para gerenciamento de produtos.
class TelaGerenciarProdutos(tk.Frame):

    """
    Tela para gerenciar Produtos (CRUD) e controlar estoque.
    """

    # Inicializa a interface de gerenciamento de produtos.
    def __init__(self, mestre, permissoes_usuario):

        # Chama o construtor da classe `tk.Frame`, passando o
        #       `mestre` como janela principal.
        # `bg="#f7f7f7"` define a cor de fundo da interface como cinza claro.
        super().__init__(mestre, bg="#f7f7f7")

        # Armazena a referência da janela principal.
        self.mestre = mestre

        # Armazena as permissões do usuário para controle de
        #       acesso às funcionalidades.
        self.permissoes_usuario = permissoes_usuario

        # Exibe a interface na tela.
        # `fill="both"` faz com que o frame ocupe todo o espaço
        #       disponível na largura e altura.
        # `expand=True` permite que o frame se expanda caso a
        #       janela seja redimensionada.
        self.pack(fill="both", expand=True)

        # Cria um rótulo (Label) para o título da tela de
        #       gerenciamento de estoque de produtos.
        lbl_titulo = tk.Label(self,

                              # `text="Controle de Estoque - Produtos"` define o
                              #         texto exibido no título da tela.
                              text="Controle de Estoque - Produtos",

                              # `font=("Helvetica", 16, "bold")` define a fonte do título
                              #         como Helvetica, tamanho 16, em negrito.
                              font=("Helvetica", 16, "bold"),

                              # `bg="#f7f7f7"` define a cor de fundo do rótulo como cinza claro.
                              bg="#f7f7f7")

        # Exibe o título na tela.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do rótulo.
        lbl_titulo.pack(pady=10)

        # Cria um frame (`Frame`) para agrupar os campos de entrada do formulário.
        frame_form = ttk.Frame(self)

        # Exibe o frame na interface.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do frame.
        # `padx=20` adiciona um espaçamento horizontal de 20 pixels para
        #       afastar os campos das bordas da tela.
        frame_form.pack(pady=10, padx=20)

        # Cria uma variável de controle para armazenar o nome do produto.
        # `tk.StringVar()` permite manipular strings dentro dos widgets do Tkinter.
        self.nome_var = tk.StringVar()

        # Cria uma variável de controle para armazenar a descrição do produto.
        # `tk.StringVar()` será usada para capturar e exibir descrições
        #       digitadas pelo usuário.
        self.descricao_var = tk.StringVar()

        # Cria uma variável de controle para armazenar o preço do produto.
        # `tk.DoubleVar()` permite armazenar valores numéricos com casas
        #       decimais, garantindo precisão nos preços.
        self.preco_var = tk.DoubleVar()

        # Cria uma variável de controle para armazenar a quantidade do produto em estoque.
        # `tk.IntVar()` permite manipular valores inteiros, garantindo
        #       que a quantidade seja sempre um número inteiro.
        self.quantidade_var = tk.IntVar()

        # Cria uma variável de controle para armazenar a categoria do produto.
        # `tk.StringVar()` será usada para permitir a seleção ou
        #       inserção de uma categoria para o produto.
        self.categoria_var = tk.StringVar()

        # Cria um rótulo para identificar o campo "Nome" do produto.
        # `text="Nome:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `row=0` posiciona o rótulo na primeira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula do grid.
        ttk.Label(frame_form,
                  text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para permitir que o usuário insira o nome do produto.
        # `textvariable=self.nome_var` associa o campo à variável `self.nome_var`.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # O campo de entrada é posicionado dentro do `frame_form`.
        # `row=0` posiciona o campo de entrada na mesma linha do rótulo "Nome".
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.nome_var,
                  width=30).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para identificar o campo "Descrição" do produto.
        # `text="Descrição:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `row=1` posiciona o rótulo na segunda linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula do grid.
        ttk.Label(frame_form,
                  text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para permitir que o usuário insira a descrição do produto.
        # `textvariable=self.descricao_var` associa o campo à variável `self.descricao_var`.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # O campo de entrada é posicionado dentro do `frame_form`.
        # `row=1` posiciona o campo de entrada na mesma linha do rótulo "Descrição".
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.descricao_var,
                  width=30).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para identificar o campo "Preço" do produto.
        # `text="Preço:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `row=2` posiciona o rótulo na terceira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula do grid.
        ttk.Label(frame_form,
                  text="Preço:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para permitir que o usuário insira o preço do produto.
        # `textvariable=self.preco_var` associa o campo à variável `self.preco_var`.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # O campo de entrada é posicionado dentro do `frame_form`.
        # `row=2` posiciona o campo de entrada na mesma linha do rótulo "Preço".
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.preco_var,
                  width=30).grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para identificar o campo "Quantidade em Estoque" do produto.
        # `text="Quantidade em Estoque:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `row=3` posiciona o rótulo na quarta linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula do grid.
        ttk.Label(frame_form,
                  text="Quantidade em Estoque:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para permitir que o usuário insira a
        #       quantidade do produto no estoque.
        # `textvariable=self.quantidade_var` associa o campo à variável `self.quantidade_var`.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # O campo de entrada é posicionado dentro do `frame_form`.
        # `row=3` posiciona o campo de entrada na mesma linha do rótulo "Quantidade em Estoque".
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.quantidade_var,
                  width=30).grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo para identificar o campo "Categoria" do produto.
        # `text="Categoria:"` define o texto exibido no rótulo.
        # O rótulo é posicionado dentro do `frame_form`.
        # `row=4` posiciona o rótulo na quinta linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula do grid.
        ttk.Label(frame_form,
                  text="Categoria:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para permitir que o usuário
        #       insira a categoria do produto.
        # `textvariable=self.categoria_var` associa o campo à variável `self.categoria_var`.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # O campo de entrada é posicionado dentro do `frame_form`.
        # `row=4` posiciona o campo de entrada na mesma linha do rótulo "Categoria".
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.categoria_var,
                  width=30).grid(row=4, column=1, padx=5, pady=5)

        # ---------------- FRAME para os botões, para alinhá-los lado a lado ---------------- #
        # Cria um frame para agrupar os botões de ação.
        # O frame será posicionado dentro do `frame_form`.
        frame_botoes = ttk.Frame(frame_form)

        # Exibe o frame na interface.
        # `row=5` posiciona o frame na sexta linha da grade.
        # `column=0` posiciona o frame na primeira coluna da grade.
        # `columnspan=2` faz com que o frame ocupe duas colunas, centralizando os botões.
        # `pady=10` adiciona um espaçamento vertical de
        #       10 pixels acima e abaixo do frame.
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=10)

        # Cria um botão para cadastrar ou atualizar um produto.
        # `text="Cadastrar/Atualizar"` define o texto exibido no botão.
        # `width=15` define a largura do botão para 15 caracteres.
        # `command=self.cadastrar_produto` associa a ação de
        #       cadastrar ou atualizar ao clicar no botão.
        btn_salvar = ttk.Button(frame_botoes,
                                text="Cadastrar/Atualizar",
                                width=15,
                                command=self.cadastrar_produto)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre o botão e outros elementos.
        btn_salvar.pack(side="left", padx=5)

        # Cria um botão para deletar um produto.
        # `text="Deletar"` define o texto exibido no botão.
        # `width=15` define a largura do botão para 15 caracteres.
        # `command=self.deletar_produto` associa a ação de
        #       deletar um produto ao clicar no botão.
        btn_deletar = ttk.Button(frame_botoes,
                                 text="Deletar",
                                 width=15,
                                 command=self.deletar_produto)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre o botão e outros elementos.
        btn_deletar.pack(side="left", padx=5)

        # Cria um botão para abrir o histórico do produto.
        # `text="Histórico"` define o texto exibido no botão.
        # `width=15` define a largura do botão para 15 caracteres.
        # `command=self.abrir_historico_produto` associa a ação de
        #       exibir o histórico do produto ao clicar no botão.
        btn_historico = ttk.Button(frame_botoes,
                                   text="Histórico",
                                   width=15,
                                   command=self.abrir_historico_produto)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de
        #       5 pixels entre o botão e outros elementos.
        btn_historico.pack(side="left", padx=5)

        # -------------------------------------------------------------- #

        # Treeview
        # Cria uma tabela (Treeview) para exibir a lista de produtos cadastrados.
        # columns=("nome", "descricao", "preco", "quantidade", "categoria", "id")
        #       define as colunas da tabela.
        # show="headings" oculta a primeira coluna vazia padrão e exibe
        #       apenas os cabeçalhos das colunas definidas.
        self.tree_produtos = ttk.Treeview(self,
                                          columns=("nome", "descricao", "preco", "quantidade", "categoria", "id"),
                                          show="headings")

        # Configura o cabeçalho da coluna "Nome".
        # text="Nome" define o texto exibido no cabeçalho.
        self.tree_produtos.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna "Descrição".
        # text="Descrição" define o texto exibido no cabeçalho.
        self.tree_produtos.heading("descricao", text="Descrição")

        # Configura o cabeçalho da coluna "Preço".
        # text="Preço" define o texto exibido no cabeçalho.
        self.tree_produtos.heading("preco", text="Preço")

        # Configura o cabeçalho da coluna "Qtd em Estoque".
        # text="Qtd em Estoque" define o texto exibido no cabeçalho.
        self.tree_produtos.heading("quantidade", text="Qtd em Estoque")

        # Configura o cabeçalho da coluna "Categoria".
        # text="Categoria" define o texto exibido no cabeçalho.
        self.tree_produtos.heading("categoria", text="Categoria")

        # Configura o cabeçalho da coluna "ID(oculto)".
        # text="ID(oculto)" define o texto exibido no cabeçalho.
        self.tree_produtos.heading("id", text="ID(oculto)")

        # Configura a largura da coluna "id" para 0 pixels e
        #       impede que ela seja redimensionada.
        # width=0 oculta a coluna ID.
        # stretch=False impede que a coluna seja ajustada automaticamente.
        self.tree_produtos.column("id", width=0, stretch=False)

        # Exibe a tabela na interface.
        # fill="both" faz com que a tabela expanda para ocupar todo o espaço disponível.
        # expand=True permite que a tabela se expanda conforme a interface for redimensionada.
        # padx=10 adiciona um espaçamento horizontal de 10 pixels ao redor da tabela.
        # pady=10 adiciona um espaçamento vertical de 10 pixels ao redor da tabela.
        self.tree_produtos.pack(fill="both", expand=True, padx=10, pady=10)

        # Associa um evento de duplo clique na tabela de produtos.
        # "<Double-1>" define que a ação será disparada ao clicar duas vezes em um item.
        # command=self.selecionar_produto associa a função que
        #       será chamada ao detectar o evento.
        self.tree_produtos.bind("<Double-1>", self.selecionar_produto)

        # Cria um botão para voltar ao dashboard.
        # text="Voltar ao Dashboard" define o texto exibido no botão.
        # command=self.voltar_dashboard associa a ação de retornar ao
        #       dashboard ao clicar no botão.
        btn_voltar = ttk.Button(self,
                                text="Voltar ao Dashboard",
                                command=self.voltar_dashboard)

        # Exibe o botão na interface.
        # pady=10 adiciona um espaçamento vertical de 10 pixels ao redor do botão.
        btn_voltar.pack(pady=10)

        # Inicializa a variável `produto_em_edicao` como `None`, indicando que
        #       nenhum produto está sendo editado no momento.
        self.produto_em_edicao = None

        # Chama a função `listar_produtos()` para carregar e exibir os
        #       produtos na tabela ao iniciar a tela.
        self.listar_produtos()

    # Define a função para selecionar um produto da tabela (Treeview).
    def selecionar_produto(self, event):

        # Obtém a seleção atual do usuário na tabela de produtos.
        # self.tree_produtos.selection() retorna o
        #       identificador da linha selecionada.
        sel = self.tree_produtos.selection()

        # Verifica se o usuário selecionou algum produto antes de prosseguir.
        if not sel:
            # Retorna imediatamente, interrompendo a execução da função.
            return

        # Obtém os valores da linha selecionada na tabela de produtos.
        # self.tree_produtos.item(sel, "values") retorna uma
        #       tupla contendo os dados do produto.
        valores = self.tree_produtos.item(sel, "values")

        # Define o nome do produto no campo de entrada correspondente.
        # valores[0] contém o nome do produto.
        self.nome_var.set(valores[0])

        # Define a descrição do produto no campo de entrada correspondente.
        # valores[1] contém a descrição do produto.
        self.descricao_var.set(valores[1])

        # Define o preço do produto no campo de entrada correspondente.
        # valores[2] contém o preço do produto.
        self.preco_var.set(valores[2])

        # Define a quantidade do produto no campo de entrada correspondente.
        # valores[3] contém a quantidade em estoque do produto.
        self.quantidade_var.set(valores[3])

        # Define a categoria do produto no campo de entrada correspondente.
        # valores[4] contém a categoria do produto.
        self.categoria_var.set(valores[4])

        # Define o ID do produto selecionado para edição.
        # valores[5] contém o ID do produto, que é convertido para ObjectId.
        self.produto_em_edicao = ObjectId(valores[5])

    # Define a função para cadastrar um novo produto ou atualizar um existente.
    def cadastrar_produto(self):

        # Obtém o nome do produto digitado pelo usuário.
        # self.nome_var.get().strip() recupera o valor do campo e
        #       remove espaços extras no início e no final.
        nome = self.nome_var.get().strip()

        # Obtém a descrição do produto digitada pelo usuário.
        # self.descricao_var.get().strip() recupera o valor do campo e
        #       remove espaços extras no início e no final.
        descricao = self.descricao_var.get().strip()

        # Tenta converter o preço digitado pelo usuário para um número decimal (float).
        try:

            # self.preco_var.get() obtém o valor do campo de preço.
            # float() converte a string para um número decimal.
            preco = float(self.preco_var.get())

        # Se ocorrer um erro na conversão (exemplo: usuário digitou um
        #       valor inválido), define o preço como 0.0.
        except:
            preco = 0.0

        # Tenta converter a quantidade digitada pelo usuário
        #       para um número inteiro.
        try:

            # self.quantidade_var.get() obtém o valor do campo de quantidade.
            # int() converte a string para um número inteiro.
            quantidade = int(self.quantidade_var.get())

        # Se ocorrer um erro na conversão (exemplo: usuário digitou um
        #       valor inválido), define a quantidade como 0.
        except:
            quantidade = 0

        # Obtém a categoria do produto digitada pelo usuário.
        # self.categoria_var.get().strip() recupera o valor do campo e
        #       remove espaços extras no início e no final.
        categoria = self.categoria_var.get().strip()

        # Verifica se o campo "Nome" foi preenchido.
        # Se `nome` estiver vazio, exibe uma mensagem de erro e
        #       interrompe o cadastro.
        if not nome:
            # messagebox.showerror("Erro", "O campo 'Nome' é
            #       obrigatório.") exibe um alerta de erro.
            messagebox.showerror("Erro",
                                 "O campo 'Nome' é obrigatório.")

            # Retorna imediatamente, interrompendo a execução da função.
            return

        # Verifica se um produto está sendo editado.
        if self.produto_em_edicao:

            # Atualiza os dados do produto no banco de dados.
            # produtos_collection.update_one({"_id": self.produto_em_edicao}, {"$set": {...}})
            # {"_id": self.produto_em_edicao} identifica qual produto será atualizado.
            # "$set" define os novos valores para os campos do produto.
            produtos_collection.update_one(
                {"_id": self.produto_em_edicao},
                {"$set": {
                    "nome": nome,
                    "descricao": descricao,
                    "preco": preco,
                    "quantidade": quantidade,
                    "categoria": categoria
                }}
            )

            # Exibe uma mensagem de sucesso informando que o produto foi atualizado.
            # f"Produto '{nome}' atualizado com sucesso!" exibe o nome do produto atualizado.
            messagebox.showinfo("Sucesso",
                                f"Produto '{nome}' atualizado com sucesso!")

        # Se não houver um produto em edição, significa que um
        #       novo produto será cadastrado.
        else:

            # Verifica se já existe um produto com o mesmo nome no banco de dados.
            # produtos_collection.find_one({"nome": nome}) retorna um
            #       documento se o produto já existir.
            if produtos_collection.find_one({"nome": nome}):
                # Exibe uma mensagem de erro informando que o produto já está cadastrado.
                # f"O produto '{nome}' já existe." exibe o nome do produto duplicado.
                messagebox.showerror("Erro",
                                     f"O produto '{nome}' já existe.")

                # Retorna imediatamente, interrompendo a execução da função.
                return

            # Insere um novo produto no banco de dados.
            # produtos_collection.insert_one({...}) adiciona o
            #       produto com os valores informados.
            produtos_collection.insert_one({
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "quantidade": quantidade,
                "categoria": categoria
            })

            # Exibe uma mensagem de sucesso informando que o produto foi cadastrado.
            # f"Produto '{nome}' cadastrado com sucesso!" exibe o nome do novo produto.
            messagebox.showinfo("Sucesso",
                                f"Produto '{nome}' cadastrado com sucesso!")

        # Chama a função limpar_campos() para redefinir os
        #       campos do formulário.
        self.limpar_campos()

        # Chama a função listar_produtos() para atualizar a
        #       lista de produtos exibida na tela.
        self.listar_produtos()

    # Define a função para limpar os campos do formulário.
    def limpar_campos(self):

        # Define o campo "Nome" como vazio.
        # self.nome_var.set("") remove qualquer texto digitado pelo usuário.
        self.nome_var.set("")

        # Define o campo "Descrição" como vazio.
        # self.descricao_var.set("") remove qualquer texto digitado pelo usuário.
        self.descricao_var.set("")

        # Define o campo "Preço" como 0.0.
        # self.preco_var.set(0.0) garante que o campo seja
        #       reiniciado com um valor padrão.
        self.preco_var.set(0.0)

        # Define o campo "Quantidade" como 0.
        # self.quantidade_var.set(0) reinicia o campo para
        #       evitar valores indesejados.
        self.quantidade_var.set(0)

        # Define o campo "Categoria" como vazio.
        # self.categoria_var.set("") remove qualquer texto digitado pelo usuário.
        self.categoria_var.set("")

        # Define que nenhum produto está sendo editado.
        # self.produto_em_edicao = None indica que não há um
        #       produto em edição no momento.
        self.produto_em_edicao = None

    # Define a função para listar os produtos na tabela (Treeview).
    def listar_produtos(self):

        # Remove todos os produtos atualmente exibidos na tabela.
        # self.tree_produtos.get_children() retorna todos os itens na tabela.
        # self.tree_produtos.delete(item) remove cada item encontrado.
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)

        # Percorre todos os produtos armazenados no banco de dados.
        # produtos_collection.find() retorna uma lista com
        #       todos os produtos cadastrados.
        for p in produtos_collection.find():
            # Insere um novo produto na tabela.
            # self.tree_produtos.insert("", tk.END, values=(...))
            #       adiciona uma nova linha ao Treeview.
            self.tree_produtos.insert("", tk.END, values=(

                # Obtém o nome do produto.
                # p.get("nome", "") retorna o nome do produto ou
                #       uma string vazia se não existir.
                p.get("nome", ""),

                # Obtém a descrição do produto.
                # p.get("descricao", "") retorna a descrição ou uma
                #       string vazia se não existir.
                p.get("descricao", ""),

                # Obtém o preço do produto.
                # p.get("preco", 0.0) retorna o preço ou 0.0 se não existir.
                p.get("preco", 0.0),

                # Obtém a quantidade em estoque do produto.
                # p.get("quantidade", 0) retorna a quantidade ou 0 se não existir.
                p.get("quantidade", 0),

                # Obtém a categoria do produto.
                # p.get("categoria", "") retorna a categoria ou uma
                #       string vazia se não existir.
                p.get("categoria", ""),

                # Obtém o ID do produto e o converte para string.
                # str(p["_id"]) garante que o ID seja exibido
                #       corretamente no formato de texto.
                str(p["_id"])

            ))

        # Define a variável `produto_em_edicao` como `None`, indicando que
        #       nenhum produto está sendo editado no momento.
        self.produto_em_edicao = None

    # Define a função para deletar um produto selecionado na tabela.
    def deletar_produto(self):

        # Obtém a seleção atual do usuário na tabela de produtos.
        # self.tree_produtos.selection() retorna a linha selecionada no Treeview.
        sel = self.tree_produtos.selection()

        # Verifica se o usuário selecionou algum produto antes
        #       de prosseguir com a exclusão.
        if not sel:
            # Exibe uma mensagem de erro informando que nenhuma seleção foi feita.
            # "Selecione um produto para deletar." orienta o
            #       usuário a selecionar um item antes de continuar.
            messagebox.showerror("Erro",
                                 "Selecione um produto para deletar.")

            # Retorna imediatamente, interrompendo a execução da função.
            return

        # Obtém os valores da linha selecionada na tabela de produtos.
        # self.tree_produtos.item(sel, "values") retorna uma
        #       tupla contendo os valores do produto.
        valores = self.tree_produtos.item(sel, "values")

        # Obtém o ID do produto selecionado.
        # valores[5] representa o sexto elemento da tupla, que
        #       corresponde ao ID do produto.
        produto_id_str = valores[5]

        # Exibe uma caixa de diálogo para confirmar a exclusão do produto.
        # askyesno retorna True se o usuário confirmar ou False se cancelar.
        if messagebox.askyesno("Confirmar",
                               f"Tem certeza que deseja deletar o produto '{valores[0]}'?"):
            # Deleta o produto do banco de dados.
            # produtos_collection.delete_one({"_id": ObjectId(produto_id_str)}) remove o produto pelo ID.
            produtos_collection.delete_one({"_id": ObjectId(produto_id_str)})

            # Exibe uma mensagem informando que o produto foi deletado com sucesso.
            messagebox.showinfo("Sucesso", "Produto deletado.")

            # Chama a função limpar_campos() para redefinir os campos do formulário.
            self.limpar_campos()

            # Chama a função listar_produtos() para atualizar a
            #       lista de produtos exibida na tela.
            self.listar_produtos()

    # ------------------- Função para abrir o "Histórico do Produto" ------------------- #

    # Define a função para abrir o histórico do produto selecionado.
    def abrir_historico_produto(self):

        # Verifica se há um produto selecionado para exibir o histórico.
        # Se `self.produto_em_edicao` for None, significa que
        #       nenhum produto foi selecionado.
        if not self.produto_em_edicao:
            # Exibe uma mensagem de erro informando que nenhum
            #       produto foi selecionado.
            # "Selecione um produto para ver o histórico." orienta o
            #       usuário a selecionar um item antes de continuar.
            messagebox.showerror("Erro",
                                 "Selecione um produto para ver o histórico.")

            # Retorna imediatamente, interrompendo a execução da função.
            return

        # Obtém o nome do produto digitado no campo correspondente.
        # self.nome_var.get().strip() recupera o valor do campo e
        #       remove espaços extras no início e no final.
        nome_produto = self.nome_var.get().strip()

        # Verifica se o campo "Nome" foi preenchido corretamente.
        # Se estiver vazio, o histórico não pode ser carregado.
        if not nome_produto:
            # Exibe uma mensagem de erro informando que o nome do
            #       produto não está preenchido.
            messagebox.showerror("Erro",
                                 "O nome do produto não está preenchido.")

            # Retorna imediatamente, interrompendo a execução da função.
            return

        # Abre a nova janela de histórico do produto.
        # HistoricoProdutoWindow(self, nome_produto) cria uma
        #       nova instância da janela de histórico,
        #       passando a tela atual (`self`) e o nome do produto como parâmetros.
        HistoricoProdutoWindow(self, nome_produto)

    # Define a função para voltar ao dashboard.
    def voltar_dashboard(self):

        # Oculta a tela atual de gerenciamento de produtos.
        # self.pack_forget() remove a interface da tela sem destruí-la,
        #       permitindo que seja reutilizada posteriormente.
        self.pack_forget()

        # Exibe a tela do dashboard.
        # TelaDashboard(self.mestre, self.permissoes_usuario) cria
        #       uma nova instância do dashboard,
        #       passando o mestre (janela principal) e as
        #       permissões do usuário como parâmetros.
        TelaDashboard(self.mestre, self.permissoes_usuario)


# Define a classe `HistoricoProdutoWindow`, que cria uma nova
#       janela para exibir o histórico do produto.
# `tk.Toplevel` indica que esta classe representa uma nova
#       janela secundária dentro da aplicação.
class HistoricoProdutoWindow(tk.Toplevel):

    # Define o método construtor (`__init__`) da classe,
    #       que inicializa a nova janela.
    # `pai` representa a janela principal (a partir da qual esta será aberta).
    # `nome_produto` é o nome do produto cujo histórico será exibido.
    def __init__(self, pai, nome_produto):

        # Chama o método construtor da classe `tk.Toplevel`
        #       para inicializar a janela corretamente.
        # `super().__init__(pai)` associa esta janela à janela principal (`pai`).
        super().__init__(pai)

        # Define o título da janela com o nome do produto selecionado.
        # f"Histórico do Produto: {nome_produto}" exibe dinamicamente o
        #       nome do produto no título da janela.
        self.title(f"Histórico do Produto: {nome_produto}")

        # Armazena a referência à janela principal.
        # `self.pai = pai` permite que a nova janela interaja
        #       com a janela principal.
        self.pai = pai

        # Armazena o nome do produto selecionado.
        # `self.nome_produto = nome_produto` permite que outras funções
        #       dentro desta classe acessem o nome do produto.
        self.nome_produto = nome_produto

        # Chama a função `center_window` para centralizar a janela na tela.
        # `center_window(900, 600)` define a largura como 900
        #       pixels e a altura como 600 pixels.
        self.center_window(900, 600)

        # Define a cor de fundo da janela.
        # bg="#f7f7f7" aplica um fundo na cor cinza claro.
        self.configure(bg="#f7f7f7")

        # Define que a janela não pode ser redimensionada.
        # resizable(False, False) impede que o usuário altere a
        #       largura e a altura da janela.
        self.resizable(False, False)

        # Cria variáveis de controle para os filtros da interface.

        # Cria uma variável para armazenar a data inicial do filtro.
        # `tk.StringVar()` permite armazenar um valor textual (string).
        self.data_de_var = tk.StringVar()

        # Cria uma variável para armazenar a data final do filtro.
        # `tk.StringVar()` será usada para capturar a data
        #       digitada ou selecionada pelo usuário.
        self.data_ate_var = tk.StringVar()

        # Cria uma variável para armazenar o filtro de hóspede.
        # `tk.StringVar()` será usada para pesquisar pelo
        #       nome do hóspede na lista de registros.
        self.filtro_hospede_var = tk.StringVar()

        # Cria uma variável para armazenar o filtro de quarto.
        # `tk.StringVar()` permitirá buscar registros de um quarto específico.
        self.filtro_quarto_var = tk.StringVar()

        # ---------------- FRAME FILTROS (linha 1) ---------------- #

        # Cria um frame para organizar a primeira linha de filtros.
        # `frame_filtros_linha1` será usado para agrupar os
        #       componentes de filtro na interface.
        frame_filtros_linha1 = ttk.Frame(self)

        # Exibe o frame na interface.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do frame.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do frame.
        # `fill="x"` faz com que o frame ocupe toda a largura disponível da tela.
        frame_filtros_linha1.pack(pady=5, padx=10, fill="x")

        # Cria um rótulo para identificar o campo "Data De".
        # `text="Data De:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` é o frame onde o rótulo será inserido.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(frame_filtros_linha1, text="Data De:").pack(side="left", padx=5)

        # Verifica se o módulo TKCalendar está sendo utilizado.
        # `USANDO_TKCALENDAR` é uma variável que indica se o DateEntry
        #       deve ser usado para seleção de datas.
        if USANDO_TKCALENDAR:

            # Cria um campo de entrada de data utilizando o DateEntry.
            # `frame_filtros_linha1` define o frame onde o campo será inserido.
            # `textvariable=self.data_de_var` associa a variável de controle ao campo.
            # `date_pattern="yyyy-MM-dd"` define o formato da data exibida.
            # `width=12` define a largura do campo de entrada.
            self.date_de = DateEntry(frame_filtros_linha1,
                                     textvariable=self.data_de_var,
                                     date_pattern="yyyy-MM-dd",
                                     width=12)

            # Exibe o campo de entrada de data na interface.
            # `side="left"` alinha o campo à esquerda dentro do frame.
            # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo.
            self.date_de.pack(side="left", padx=5)

        # Caso o TKCalendar não esteja disponível, usa um
        #       campo de entrada padrão (Entry).
        else:

            # Cria um campo de entrada de texto para digitar a data manualmente.
            # `frame_filtros_linha1` define o frame onde o campo será inserido.
            # `textvariable=self.data_de_var` associa a variável de controle ao campo.
            # `width=15` define a largura do campo de entrada.
            ttk.Entry(frame_filtros_linha1,
                      textvariable=self.data_de_var,
                      width=15).pack(side="left", padx=5)

        # Cria um rótulo para identificar o campo "Data Até".
        # `text="Data Até:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` é o frame onde o rótulo será inserido.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(frame_filtros_linha1,
                  text="Data Até:").pack(side="left", padx=5)

        # Verifica se o módulo TKCalendar está sendo utilizado.
        # `USANDO_TKCALENDAR` é uma variável que indica se o
        #       DateEntry deve ser usado para seleção de datas.
        if USANDO_TKCALENDAR:

            # Cria um campo de entrada de data utilizando o DateEntry.
            # `frame_filtros_linha1` define o frame onde o campo será inserido.
            # `textvariable=self.data_ate_var` associa a variável de controle ao campo.
            # `date_pattern="yyyy-MM-dd"` define o formato da data exibida.
            # `width=12` define a largura do campo de entrada.
            self.date_ate = DateEntry(frame_filtros_linha1,
                                      textvariable=self.data_ate_var,
                                      date_pattern="yyyy-MM-dd",
                                      width=12)

            # Exibe o campo de entrada de data na interface.
            # `side="left"` alinha o campo à esquerda dentro do frame.
            # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo.
            self.date_ate.pack(side="left", padx=5)

        # Caso o TKCalendar não esteja disponível, usa um
        #       campo de entrada padrão (Entry).
        else:

            # Cria um campo de entrada de texto para digitar a data manualmente.
            # `frame_filtros_linha1` define o frame onde o campo será inserido.
            # `textvariable=self.data_ate_var` associa a variável de controle ao campo.
            # `width=15` define a largura do campo de entrada.
            ttk.Entry(frame_filtros_linha1,
                      textvariable=self.data_ate_var,
                      width=15).pack(side="left", padx=5)

        # Cria um rótulo para identificar o campo "Hóspede".
        # `text="Hóspede:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` é o frame onde o rótulo será inserido.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(frame_filtros_linha1, text="Hóspede:").pack(side="left", padx=5)

        # Cria um campo de entrada para pesquisa de hóspede.
        # `frame_filtros_linha1` define o frame onde o campo será inserido.
        # `textvariable=self.filtro_hospede_var` associa a variável de controle ao campo.
        # `width=15` define a largura do campo de entrada.
        # `side="left"` alinha o campo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo.
        ttk.Entry(frame_filtros_linha1,
                  textvariable=self.filtro_hospede_var,
                  width=15).pack(side="left", padx=5)

        # Cria um rótulo para identificar o campo "Quarto".
        # `text="Quarto:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` é o frame onde o rótulo será inserido.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(frame_filtros_linha1,
                  text="Quarto:").pack(side="left", padx=5)

        # Cria um campo de entrada para pesquisa de número do quarto.
        # `frame_filtros_linha1` define o frame onde o campo será inserido.
        # `textvariable=self.filtro_quarto_var` associa a variável de controle ao campo.
        # `width=15` define a largura do campo de entrada.
        # `side="left"` alinha o campo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo.
        ttk.Entry(frame_filtros_linha1,
                  textvariable=self.filtro_quarto_var,
                  width=15).pack(side="left", padx=5)

        # Cria um botão para aplicar o filtro.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.aplicar_filtro` associa a ação de filtrar
        #       os resultados ao clicar no botão.
        # `frame_filtros_linha1` é o frame onde o botão será inserido.
        btn_filtrar = ttk.Button(frame_filtros_linha1,
                                 text="Filtrar",
                                 command=self.aplicar_filtro)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona 10 pixels de espaçamento
        #       horizontal ao redor do botão.
        btn_filtrar.pack(side="left", padx=10)

        # ---------------- TREEVIEW ---------------- #

        # Define as colunas da tabela (Treeview).
        # Cada string dentro da tupla representa o
        #       nome de uma coluna na tabela.
        colunas = (
            "data_inicio",  # Armazena a data de início da reserva.
            "data_fim",  # Armazena a data de término da reserva.
            "quarto",  # Identifica o número do quarto reservado.
            "hospedes",  # Lista os hóspedes da reserva.
            "quantidade",  # Quantidade de itens ou diárias reservadas.
            "total_item",  # Valor total da reserva para esse item.
            "data_criacao",  # Data em que a reserva foi cadastrada.
            "idreserva"  # ID único da reserva (oculto).
        )

        # Cria uma tabela (Treeview) para exibir os dados do histórico.
        # `self` indica que o Treeview pertence a essa classe.
        # `columns=colunas` define quais colunas serão exibidas na tabela.
        # `show="headings"` faz com que apenas os cabeçalhos das
        #       colunas sejam mostrados (sem a primeira coluna padrão).
        # `height=15` define a quantidade de linhas visíveis na
        #       tabela antes da rolagem.
        self.tree_historico = ttk.Treeview(self,
                                           columns=colunas,
                                           show="headings",
                                           height=15)

        # Define o título da coluna "data_inicio".
        # `text="Início"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("data_inicio", text="Início")

        # Define o título da coluna "data_fim".
        # `text="Fim"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("data_fim", text="Fim")

        # Define o título da coluna "quarto".
        # `text="Quarto"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("quarto", text="Quarto")

        # Define o título da coluna "hospedes".
        # `text="Hóspedes"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("hospedes", text="Hóspedes")

        # Define o título da coluna "quantidade".
        # `text="Qtd Consumida"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("quantidade", text="Qtd Consumida")

        # Define o título da coluna "total_item".
        # `text="Total (R$)"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("total_item", text="Total (R$)")

        # Define o título da coluna "data_criacao".
        # `text="Data Criação"` define o nome visível no cabeçalho da coluna.
        self.tree_historico.heading("data_criacao", text="Data Criação")

        # Define o título da coluna "idreserva".
        # `text="ID(oculto)"` define o nome visível no cabeçalho da
        #       coluna, mas a coluna pode ser oculta.
        self.tree_historico.heading("idreserva", text="ID(oculto)")

        # Oculta a coluna "idreserva" para que não seja exibida na interface.
        # `width=0` define a largura da coluna como zero, tornando-a invisível.
        # `stretch=False` impede que a coluna seja redimensionada pelo usuário.
        self.tree_historico.column("idreserva", width=0, stretch=False)

        # Exibe a tabela na interface.
        # `fill="both"` faz com que o Treeview expanda tanto em
        #       largura quanto em altura.
        # `expand=True` permite que o widget cresça junto com a janela.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor da tabela.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor da tabela.
        self.tree_historico.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria um rótulo para exibir um resumo das informações.
        # `text=""` inicializa o rótulo vazio, ele será preenchido dinamicamente.
        # `font=("Helvetica", 10, "bold")` define a fonte em Helvetica, tamanho 10, com negrito.
        self.lbl_resumo = ttk.Label(self,
                                    text="",
                                    font=("Helvetica", 10, "bold"))

        # Exibe o rótulo de resumo na interface.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        self.lbl_resumo.pack(pady=5)

        # ---------------- FRAME BOTÕES FINAIS ---------------- #

        # Cria um frame para organizar os botões finais da interface.
        # `frame_botoes_finais` será usado para agrupar os
        #       botões na parte inferior da tela.
        frame_botoes_finais = ttk.Frame(self)

        # Exibe o frame na interface.
        # `pady=5` adiciona 5 pixels de espaçamento vertical
        #       acima e abaixo do frame.
        frame_botoes_finais.pack(pady=5)

        # Cria um botão para exportar os dados para Excel.
        # `text="Exportar Excel"` define o texto exibido no botão.
        # `command=self.exportar_excel` associa a ação de exportação ao clicar no botão.
        btn_exportar = ttk.Button(frame_botoes_finais,
                                  text="Exportar Excel",
                                  command=self.exportar_excel)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        btn_exportar.pack(side="left", padx=10)

        # Cria um botão para fechar a janela.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar a
        #       janela ao clicar no botão.
        btn_fechar = ttk.Button(frame_botoes_finais,
                                text="Fechar",
                                command=self.destroy)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        btn_fechar.pack(side="left", padx=10)

        # Carrega o histórico inicial assim que a janela é aberta.
        # `self.carregar_historico()` chama a função responsável
        #       por buscar e exibir os dados na interface.
        self.carregar_historico()

    # Define a função para carregar o histórico de um produto específico.
    # `data_de` e `data_ate` são parâmetros opcionais para filtrar por período.
    def carregar_historico(self, data_de=None, data_ate=None):

        # Limpa todos os itens da tabela (Treeview) antes de carregar novos dados.
        # `self.tree_historico.get_children()` retorna todos os itens da tabela.
        # `self.tree_historico.delete(item)` remove cada item encontrado.
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)

        # Monta a query base para buscar os registros do produto no banco de dados.
        # `produtos.nome` é a chave que armazena o nome do produto dentro da coleção.
        # `self.nome_produto` contém o nome do produto selecionado.
        query_base = {"produtos.nome": self.nome_produto}

        # Aplica o filtro de datas (Data De/Até) para buscar apenas os
        #       registros dentro do período especificado.
        # A consulta usa um operador de sobreposição para verificar
        #       se o período da reserva se encaixa no intervalo desejado.
        if data_de or data_ate:
            # Adiciona uma condição de comparação na query base.
            # `$expr` permite realizar comparações dentro dos
            #       documentos do banco de dados.
            query_base["$expr"] = {

                # `$and` garante que ambas as condições de data sejam atendidas.
                "$and": [

                    # `$lte` (menor ou igual) verifica se a data de início da
                    #       reserva está antes ou igual à data final filtrada.
                    # Se `data_ate` for None, assume "9999-12-31" como valor padrão,
                    #       garantindo que todas as datas futuras sejam incluídas.
                    {"$lte": ["$data_inicio", data_ate if data_ate else "9999-12-31"]},

                    # `$gte` (maior ou igual) verifica se a data de fim da reserva
                    #       está depois ou igual à data inicial filtrada.
                    # Se `data_de` for None, assume "0000-01-01" como valor padrão,
                    #       garantindo que todas as datas passadas sejam incluídas.
                    {"$gte": ["$data_fim", data_de if data_de else "0000-01-01"]}
                ]
            }

        # Executa a busca no banco de dados aplicando a query base.
        # `reservas_collection.find(query_base)` busca todas as reservas
        #       que atendem aos critérios definidos.
        # `.sort("data_inicio", 1)` ordena os resultados pela data de início em ordem crescente.
        reservas = reservas_collection.find(query_base).sort("data_inicio", 1)

        # Lê valores dos filtros “hospede” e “quarto”

        # Obtém o valor do filtro de hóspede digitado pelo usuário.
        # `self.filtro_hospede_var.get()` captura o valor atual do campo de entrada.
        # `.strip()` remove espaços extras antes e depois do texto.
        # `.lower()` converte o texto para minúsculas para facilitar a comparação.
        filtro_hospede = self.filtro_hospede_var.get().strip().lower()

        # Obtém o valor do filtro de quarto digitado pelo usuário.
        # `self.filtro_quarto_var.get()` captura o valor atual do campo de entrada.
        # `.strip()` remove espaços extras antes e depois do texto.
        # `.lower()` converte o texto para minúsculas para garantir a
        #       busca sem diferenciação de maiúsculas e minúsculas.
        filtro_quarto = self.filtro_quarto_var.get().strip().lower()

        # Inicializa o contador de registros que atendem aos critérios de filtragem.
        # `contagem = 0` começa a contagem em zero e será incrementado
        #       conforme os registros forem adicionados à tabela.
        contagem = 0

        # Inicializa a variável para somar as quantidades dos itens filtrados.
        # `soma_quantidades = 0` armazena a soma total da quantidade de produtos consumidos.
        soma_quantidades = 0

        # Inicializa a variável para somar o valor total dos itens filtrados.
        # `soma_total = 0.0` começa em zero e será atualizado conforme os
        #       valores forem adicionados.
        soma_total = 0.0

        # Percorre a lista de reservas retornadas na consulta ao banco de dados.
        for r in reservas:

            # Obtém a data de início da reserva.
            # `.get("data_inicio", "")` retorna a data armazenada ou
            #       uma string vazia caso não exista.
            data_inicio = r.get("data_inicio", "")

            # Obtém a data de fim da reserva.
            # `.get("data_fim", "")` retorna a data armazenada ou
            #       uma string vazia caso não exista.
            data_fim = r.get("data_fim", "")

            # Obtém o número do quarto associado à reserva.
            # `.get("numero_quarto", "")` retorna o número do quarto ou
            #       uma string vazia caso não exista.
            quarto = r.get("numero_quarto", "")

            # Obtém a lista de hóspedes associados à reserva.
            # `.get("hospedes", [])` retorna uma lista de nomes ou
            #       uma lista vazia caso não exista.
            hospedes = r.get("hospedes", [])  # lista de nomes

            # Obtém a data de criação da reserva.
            # `.get("data_criacao", "")` retorna a data de criação ou
            #       uma string vazia caso não exista.
            data_criacao = r.get("data_criacao", "")

            # Inicializa a variável para armazenar a quantidade de
            #       unidades consumidas deste produto.
            # Começa em 0 e será atualizado caso haja informações no banco de dados.
            qtd_consumida = 0

            # Inicializa a variável para armazenar o valor total
            #       consumido deste item na reserva.
            # Começa em 0.0 e será atualizado caso o banco de dados
            #       contenha essa informação.
            subtotal_item = 0.0

            # Percorre a lista de produtos consumidos dentro da reserva.
            # `.get("produtos", [])` retorna a lista de produtos ou uma
            #       lista vazia caso não existam produtos registrados.
            for item_prod in r.get("produtos", []):

                # Verifica se o nome do produto no banco de dados corresponde ao
                #       produto selecionado pelo usuário.
                # `.get("nome", "")` obtém o nome do produto ou retorna uma
                #       string vazia caso a chave não exista.
                if item_prod.get("nome", "") == self.nome_produto:
                    # Adiciona a quantidade consumida do produto à variável `qtd_consumida`.
                    # `.get("quantidade", 0)` obtém o valor da chave "quantidade" ou
                    #       retorna 0 caso não exista.
                    qtd_consumida += item_prod.get("quantidade", 0)

                    # Obtém o valor total do item dentro da reserva, se estiver
                    #       salvo no banco de dados.
                    # `.get("subtotal", 0.0)` retorna o valor da chave "subtotal" ou 0.0 caso não exista.
                    # Caso o banco de dados não armazene "subtotal", o cálculo pode
                    #       ser feito com `item_prod["preco"] * item_prod["quantidade"]`.
                    valor_item = item_prod.get("subtotal", 0.0)

                    # Adiciona o valor do item ao subtotal acumulado.
                    # `float(valor_item)` converte o valor obtido para um
                    #       número de ponto flutuante.
                    subtotal_item += float(valor_item)

            # Monta string de hospedes
            # Converte a lista de hóspedes em uma string separada por vírgulas.
            # `", ".join(hospedes)` une todos os nomes da lista `hospedes` em
            #       uma única string, separados por vírgula.
            hospedes_str = ", ".join(hospedes)

            # ------------------ Aplica os filtros em Python (hóspede, quarto) ------------------

            # Verifica se há um filtro de hóspede ativo.
            # Se `filtro_hospede` contiver um valor, a condição será aplicada.
            if filtro_hospede:

                # Verifica se o hóspede digitado está presente na string formatada `hospedes_str`.
                # `.lower()` converte o texto para minúsculas para garantir
                #       que a busca não seja case-sensitive.
                if filtro_hospede not in hospedes_str.lower():
                    # Se o hóspede não for encontrado, a iteração
                    #       continua para o próximo registro.
                    continue

            # Verifica se há um filtro de quarto ativo.
            # Se `filtro_quarto` contiver um valor, a condição será aplicada.
            if filtro_quarto:

                # Verifica se o número do quarto digitado está presente na variável `quarto`.
                # `.lower()` converte o texto para minúsculas para garantir
                #       que a busca não seja case-sensitive.
                if filtro_quarto not in quarto.lower():
                    # Se o quarto não for encontrado, a iteração
                    #       continua para o próximo registro.
                    continue

            # Se passou nos filtros, insere
            # Insere os dados filtrados na tabela (Treeview).
            # `self.tree_historico.insert()` adiciona uma nova linha à tabela.
            # `""` indica que o item será inserido na raiz da árvore.
            # `tk.END` posiciona o novo item no final da lista.
            # `values=(...)` define os valores que serão exibidos
            #       em cada coluna da tabela.
            self.tree_historico.insert("", tk.END, values=(

                # `data_inicio` representa a data de início da reserva.
                data_inicio,

                # `data_fim` representa a data de término da reserva.
                data_fim,

                # `quarto` representa o número do quarto associado à reserva.
                quarto,

                # `hospedes_str` contém a lista de hóspedes formatada
                #       como uma string separada por vírgulas.
                hospedes_str,

                # `qtd_consumida` indica a quantidade do produto
                #       consumido dentro dessa reserva.
                qtd_consumida,

                # `subtotal_item` representa o valor total consumido do
                #       item dentro dessa reserva.
                # `f"{subtotal_item:.2f}"` formata o valor com duas casas decimais.
                f"{subtotal_item:.2f}",

                # `data_criacao` representa a data em que a reserva foi criada no sistema.
                data_criacao,

                # `str(r["_id"])` armazena o identificador único da
                #       reserva, convertido para string.
                str(r["_id"])

            ))

            # Incrementa o contador de registros adicionados à tabela.
            # `contagem += 1` aumenta o número total de registros exibidos.
            contagem += 1

            # Soma a quantidade total dos produtos consumidos nos registros exibidos.
            # `soma_quantidades += qtd_consumida` adiciona o valor
            #       da reserva atual ao total acumulado.
            soma_quantidades += qtd_consumida

            # Soma o valor total de todos os itens consumidos nos registros exibidos.
            # `soma_total += subtotal_item` adiciona o valor da
            #       reserva atual ao total acumulado.
            soma_total += subtotal_item

            # Exibe o resumo
            # Atualiza o rótulo de resumo com as informações calculadas.
            # `self.lbl_resumo.config()` modifica o texto exibido no rótulo da interface.
            self.lbl_resumo.config(

                # `text=(...)` define o novo texto do rótulo.
                text=(

                    # Exibe o total de registros filtrados e exibidos na tabela.
                    f"Total de Registros: {contagem} | "

                    # Exibe a soma total da quantidade consumida dos produtos 
                    #       nos registros filtrados.
                    f"Soma das Qtd Consumida: {soma_quantidades} | "

                    # Exibe a soma total dos valores dos produtos consumidos, 
                    #       formatada com duas casas decimais.
                    f"Soma Total (R$): {soma_total:.2f}"

                )
            )

    # Define a função para aplicar filtros na busca do histórico.
    def aplicar_filtro(self):

        # Obtém a data inicial inserida pelo usuário.
        # `.get().strip()` captura o valor do campo de entrada e
        #       remove espaços em branco extras.
        data_de_str = self.data_de_var.get().strip()

        # Obtém a data final inserida pelo usuário.
        # `.get().strip()` captura o valor do campo de entrada e
        #       remove espaços em branco extras.
        data_ate_str = self.data_ate_var.get().strip()

        # Inicializa as variáveis de data como `None`, caso não
        #       sejam preenchidas corretamente.
        data_de = None
        data_ate = None

        # ------------------ Validação das Datas ------------------

        # Tenta converter a data inicial para garantir que esteja no formato correto.
        try:

            if data_de_str:
                # `datetime.datetime.strptime(data_de_str, "%Y-%m-%d")` verifica
                #       se a data está no formato "YYYY-MM-DD".
                # Se a conversão for bem-sucedida, a data será armazenada na variável `data_de`.
                datetime.datetime.strptime(data_de_str, "%Y-%m-%d")
                data_de = data_de_str

        # Se houver um erro na conversão da data, a exceção é
        #       ignorada e `data_de` continua como `None`.
        except:
            pass

        # Tenta converter a data final para garantir que esteja no formato correto.
        try:

            if data_ate_str:
                # `datetime.datetime.strptime(data_ate_str, "%Y-%m-%d")` verifica
                #       se a data está no formato "YYYY-MM-DD".
                # Se a conversão for bem-sucedida, a data será
                #       armazenada na variável `data_ate`.
                datetime.datetime.strptime(data_ate_str, "%Y-%m-%d")
                data_ate = data_ate_str

        # Se houver um erro na conversão da data, a exceção é
        #       ignorada e `data_ate` continua como `None`.
        except:
            pass

        # Chama a função `carregar_historico()` para aplicar os
        #       filtros e exibir os resultados filtrados na tabela.
        # `data_de` e `data_ate` são passadas como argumentos para
        #       restringir os registros ao intervalo desejado.
        self.carregar_historico(data_de=data_de, data_ate=data_ate)

    # Define a função para exportar os dados da tabela para um arquivo Excel.
    def exportar_excel(self):

        # Obtém todos os itens da tabela (Treeview).
        # `self.tree_historico.get_children()` retorna uma lista
        #       com os identificadores das linhas exibidas na tabela.
        itens = self.tree_historico.get_children()

        # Verifica se há dados na tabela antes de exportar.
        # Se a lista de `itens` estiver vazia, exibe uma mensagem e encerra a função.
        if not itens:
            # Exibe uma caixa de mensagem informando que não há dados para exportar.
            messagebox.showinfo("Informação",
                                "Não há dados para exportar.")

            # Sai da função sem realizar a exportação.
            return

        # ------------------ Extração dos Dados da Treeview ------------------

        # Cria uma lista para armazenar os dados extraídos da tabela.
        linhas_data = []

        # Percorre todos os itens da tabela.
        for item_id in itens:
            # Obtém os valores da linha correspondente ao `item_id` na Treeview.
            # `self.tree_historico.item(item_id, "values")` retorna os
            #       valores de todas as colunas dessa linha.
            valores = self.tree_historico.item(item_id, "values")

            # Adiciona os valores extraídos à lista `linhas_data`.
            # As colunas incluem: data_inicio, data_fim, quarto, hóspedes,
            #       quantidade consumida, total do item, data de criação, e ID da reserva.
            linhas_data.append(valores)

        # Define os nomes das colunas do DataFrame para a exportação do Excel.
        # Cada string na lista representa um cabeçalho da planilha.
        colunas_df = [

            "Data Início",  # Coluna para a data de início da reserva.
            "Data Fim",  # Coluna para a data de término da reserva.
            "Quarto",  # Coluna que identifica o número do quarto associado à reserva.
            "Hóspedes",  # Coluna que lista os hóspedes da reserva.
            "Qtd Consumida",  # Coluna que mostra a quantidade do produto consumido na reserva.
            "Total (R$)",  # Coluna que exibe o valor total do consumo em reais.
            "Data Criação",  # Coluna que registra a data de criação da reserva no sistema.
            "ID Reserva"  # Coluna que contém o identificador único da reserva.

        ]

        # Cria um DataFrame do Pandas com os dados extraídos da tabela Treeview.
        # `linhas_data` contém todas as linhas extraídas da Treeview.
        # `columns=colunas_df` associa os dados extraídos aos nomes
        #       de colunas definidos anteriormente.
        df = pd.DataFrame(linhas_data, columns=colunas_df)

        # Define o caminho onde o arquivo Excel será salvo.
        # `os.getcwd()` obtém o diretório atual do programa.
        # `"historico_produto.xlsx"` é o nome do arquivo que será criado no diretório atual.
        caminho = os.path.join(os.getcwd(), "historico_produto.xlsx")

        # ------------------ Tentativa de Exportação para Excel ------------------
        try:

            # Exporta os dados do DataFrame para um arquivo Excel.
            # `df.to_excel(caminho, index=False)` salva os dados no
            #       arquivo especificado sem incluir o índice do DataFrame.
            df.to_excel(caminho, index=False)

            # Exibe uma mensagem informando que a exportação foi bem-sucedida.
            # `f"Histórico exportado para: {caminho}"` exibe o caminho completo do arquivo salvo.
            messagebox.showinfo("Sucesso",
                                f"Histórico exportado para: {caminho}")

        # Captura qualquer erro que possa ocorrer durante a exportação.
        except Exception as e:

            # Exibe uma mensagem de erro informando o problema ocorrido.
            # `str(e)` converte a exceção em texto para exibição ao usuário.
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

    # Define um método chamado `center_window` que centraliza a
    #       janela na tela do usuário.
    # Esse método recebe dois parâmetros: `largura` e `altura`,
    #       que representam as dimensões da janela.
    def center_window(self, largura, altura):

        # Obtém a largura total da tela do usuário.
        # `winfo_screenwidth()` retorna a largura em pixels do monitor
        #       onde a aplicação está sendo executada.
        larg_tela = self.winfo_screenwidth()

        # Obtém a altura total da tela do usuário.
        # `winfo_screenheight()` retorna a altura em pixels do monitor.
        alt_tela = self.winfo_screenheight()

        # Calcula a posição X para centralizar a janela horizontalmente.
        # `(larg_tela - largura) / 2` pega a largura total da tela e
        #       subtrai a largura da janela.
        # Dividindo por 2, encontramos a posição exata para centralizar.
        # `int(...)` converte o valor para um número inteiro, pois `geometry`
        #       não aceita números decimais.
        x = int((larg_tela - largura) / 2)

        # Calcula a posição Y para centralizar a janela verticalmente.
        # `(alt_tela - altura) / 2` pega a altura total da tela e
        #       subtrai a altura da janela.
        # Dividindo por 2, encontramos a posição exata para que a
        #       janela fique centralizada verticalmente.
        y = int((alt_tela - altura) / 2)

        # Define o tamanho e a posição da janela usando `geometry()`.
        # O formato da string é: `"largura x altura + posição_x + posição_y"`.
        # Isso posiciona a janela no centro exato da tela.
        self.geometry(f"{largura}x{altura}+{x}+{y}")


# =============================================================================
# ===================== TELA DE CADASTRO DE HÓSPEDES (CRUD) ===================
# =============================================================================

# Define a classe `TelaCadastroHospedes`, que representa a tela de cadastro de hóspedes.
# `tk.Frame` indica que esta classe herda de `Frame`, um contêiner da biblioteca Tkinter.
class TelaCadastroHospedes(tk.Frame):

    # Define o método construtor da classe.
    # `mestre` representa a janela principal onde esta tela será exibida.
    # `permissoes_usuario` armazena as permissões do usuário logado.
    def __init__(self, mestre, permissoes_usuario):

        # Chama o construtor da classe pai (`tk.Frame`).
        # `super().__init__(mestre, bg="#f7f7f7")` inicializa o
        #       frame com um fundo cinza-claro (#f7f7f7).
        super().__init__(mestre, bg="#f7f7f7")

        # Armazena a referência ao objeto `mestre`, que representa a janela principal.
        self.mestre = mestre

        # Armazena as permissões do usuário logado para controle de acessos na tela.
        self.permissoes_usuario = permissoes_usuario

        # Configura o layout do frame para preencher toda a área disponível.
        # `fill="both"` faz com que o frame expanda tanto na largura quanto na altura.
        # `expand=True` permite que o frame ocupe todo o espaço
        #       disponível dentro da janela.
        self.pack(fill="both", expand=True)

        # Cria um rótulo para o título da tela de cadastro de hóspedes.
        # `text="Cadastro de Hóspedes / Clientes"` define o texto exibido no rótulo.
        # `font=("Helvetica", 16, "bold")` define a fonte como Helvetica, tamanho 16, em negrito.
        # `bg="#f7f7f7"` define a cor de fundo como cinza claro (#f7f7f7).
        lbl_titulo = tk.Label(self,
                              text="Cadastro de Hóspedes / Clientes",
                              font=("Helvetica", 16, "bold"),
                              bg="#f7f7f7")

        # Exibe o rótulo na interface.
        # `pady=10` adiciona 10 pixels de espaçamento
        #       vertical acima e abaixo do rótulo.
        lbl_titulo.pack(pady=10)

        # Cria um frame para organizar os campos do formulário de cadastro.
        # `ttk.Frame(self)` cria um contêiner dentro da tela de cadastro.
        frame_form = ttk.Frame(self)

        # Exibe o frame na interface.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do frame.
        # `padx=20` adiciona 20 pixels de espaçamento horizontal ao redor do frame.
        frame_form.pack(pady=10, padx=20)

        # Cria uma variável para armazenar o nome do hóspede.
        # `tk.StringVar()` permite manipular e vincular o valor a um campo de entrada.
        self.nome_var = tk.StringVar()

        # Cria uma variável para armazenar o CPF do hóspede.
        # `tk.StringVar()` será usada para capturar e exibir o CPF no formulário.
        self.cpf_var = tk.StringVar()

        # Cria uma variável para armazenar o telefone do hóspede.
        # `tk.StringVar()` será usada para entrada e exibição do número de telefone.
        self.telefone_var = tk.StringVar()

        # Cria uma variável para armazenar o e-mail do hóspede.
        # `tk.StringVar()` permitirá que o usuário insira e visualize o e-mail do cliente.
        self.email_var = tk.StringVar()

        # Cria uma variável para armazenar o endereço do hóspede.
        # `tk.StringVar()` será utilizada para entrada e exibição do endereço do cliente.
        self.endereco_var = tk.StringVar()

        # Cria um rótulo para o campo "Nome".
        # `text="Nome:"` define o texto exibido no rótulo.
        # `frame_form` define o contêiner onde o rótulo será exibido.
        # `row=0` posiciona o rótulo na primeira linha do formulário.
        # `column=0` posiciona o rótulo na primeira coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        ttk.Label(frame_form,
                  text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o nome do hóspede.
        # `textvariable=self.nome_var` vincula a variável `self.nome_var` ao campo de entrada.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # `row=0` posiciona o campo de entrada na primeira linha do formulário.
        # `column=1` posiciona o campo de entrada na segunda coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.nome_var,
                  width=30).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "CPF".
        # `text="CPF:"` define o texto exibido no rótulo.
        # `frame_form` define o contêiner onde o rótulo será exibido.
        # `row=1` posiciona o rótulo na segunda linha do formulário.
        # `column=0` posiciona o rótulo na primeira coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        ttk.Label(frame_form,
                  text="CPF:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o CPF do hóspede.
        # `textvariable=self.cpf_var` vincula a variável `self.cpf_var` ao campo de entrada.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # `row=1` posiciona o campo de entrada na segunda linha do formulário.
        # `column=1` posiciona o campo de entrada na segunda coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.cpf_var,
                  width=30).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Telefone".
        # `text="Telefone:"` define o texto exibido no rótulo.
        # `frame_form` define o contêiner onde o rótulo será exibido.
        # `row=2` posiciona o rótulo na terceira linha do formulário.
        # `column=0` posiciona o rótulo na primeira coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        ttk.Label(frame_form,
                  text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o telefone do hóspede.
        # `textvariable=self.telefone_var` vincula a variável `self.telefone_var` ao campo de entrada.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # `row=2` posiciona o campo de entrada na terceira linha do formulário.
        # `column=1` posiciona o campo de entrada na segunda coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.telefone_var,
                  width=30).grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Email".
        # `text="Email:"` define o texto exibido no rótulo.
        # `frame_form` define o contêiner onde o rótulo será exibido.
        # `row=3` posiciona o rótulo na quarta linha do formulário.
        # `column=0` posiciona o rótulo na primeira coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        ttk.Label(frame_form,
                  text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o email do hóspede.
        # `textvariable=self.email_var` vincula a variável `self.email_var` ao campo de entrada.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # `row=3` posiciona o campo de entrada na quarta linha do formulário.
        # `column=1` posiciona o campo de entrada na segunda coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.email_var,
                  width=30).grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Endereço".
        # `text="Endereço:"` define o texto exibido no rótulo.
        # `frame_form` define o contêiner onde o rótulo será exibido.
        # `row=4` posiciona o rótulo na quinta linha do formulário.
        # `column=0` posiciona o rótulo na primeira coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        ttk.Label(frame_form,
                  text="Endereço:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o endereço do hóspede.
        # `textvariable=self.endereco_var` vincula a variável `self.endereco_var` ao campo de entrada.
        # `width=30` define a largura do campo de entrada para 30 caracteres.
        # `row=4` posiciona o campo de entrada na quinta linha do formulário.
        # `column=1` posiciona o campo de entrada na segunda coluna do formulário.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do campo de entrada.
        ttk.Entry(frame_form,
                  textvariable=self.endereco_var,
                  width=30).grid(row=4, column=1, padx=5, pady=5)

        # Cria um frame para organizar os botões na interface.
        # `ttk.Frame(frame_form)` cria um contêiner dentro do formulário principal.
        frame_botoes = ttk.Frame(frame_form)

        # Posiciona o frame na grade do formulário.
        # `row=5` posiciona o frame na sexta linha do formulário.
        # `column=0` posiciona o frame na primeira coluna do formulário.
        # `columnspan=3` faz com que o frame ocupe três colunas.
        # `pady=10` adiciona 10 pixels de espaçamento vertical abaixo do frame.
        frame_botoes.grid(row=5, column=0, columnspan=3, pady=10)

        # Cria um botão para cadastrar ou atualizar os dados do hóspede.
        # `text="Cadastrar/Atualizar"` define o texto exibido no botão.
        # `width=15` define a largura do botão para 15 caracteres.
        # `command=self.cadastrar_hospede` associa a função `self.cadastrar_hospede` ao clique do botão.
        btn_salvar = ttk.Button(frame_botoes,
                                text="Cadastrar/Atualizar",
                                width=15,
                                command=self.cadastrar_hospede)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal entre os botões.
        btn_salvar.pack(side="left", padx=5)

        # Cria um botão para deletar um hóspede.
        # `text="Deletar"` define o texto exibido no botão.
        # `width=15` define a largura do botão para 15 caracteres.
        # `command=self.deletar_hospede` associa a
        #       função `self.deletar_hospede` ao clique do botão.
        btn_deletar = ttk.Button(frame_botoes,
                                 text="Deletar",
                                 width=15,
                                 command=self.deletar_hospede)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal entre os botões.
        btn_deletar.pack(side="left", padx=5)

        # Cria um botão para abrir o histórico do hóspede.
        # `text="Histórico"` define o texto exibido no botão.
        # `width=15` define a largura do botão para 15 caracteres.
        # `command=self.abrir_historico` associa a
        #       função `self.abrir_historico` ao clique do botão.
        btn_historico = ttk.Button(frame_botoes,
                                   text="Histórico",
                                   width=15,
                                   command=self.abrir_historico)

        # Exibe o botão na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal entre os botões.
        btn_historico.pack(side="left", padx=5)

        # Treeview de Hóspedes
        # Cria uma Treeview para exibir a lista de hóspedes.
        # `self` define o frame onde a tabela será exibida.
        # `columns=(...)` define as colunas que serão exibidas na tabela.
        # `show="headings"` oculta a primeira coluna padrão da
        #       Treeview e exibe apenas os cabeçalhos personalizados.
        self.tree_hospedes = ttk.Treeview(self, columns=("nome", "cpf", "telefone", "email", "endereco", "id"),
                                          show="headings")

        # Define o cabeçalho da coluna "Nome".
        # `text="Nome"` define o texto exibido no cabeçalho.
        self.tree_hospedes.heading("nome", text="Nome")

        # Define o cabeçalho da coluna "CPF".
        # `text="CPF"` define o texto exibido no cabeçalho.
        self.tree_hospedes.heading("cpf", text="CPF")

        # Define o cabeçalho da coluna "Telefone".
        # `text="Telefone"` define o texto exibido no cabeçalho.
        self.tree_hospedes.heading("telefone", text="Telefone")

        # Define o cabeçalho da coluna "Email".
        # `text="Email"` define o texto exibido no cabeçalho.
        self.tree_hospedes.heading("email", text="Email")

        # Define o cabeçalho da coluna "Endereço".
        # `text="Endereço"` define o texto exibido no cabeçalho.
        self.tree_hospedes.heading("endereco", text="Endereço")

        # Define o cabeçalho da coluna "ID".
        # `text="ID(oculto)"` indica que a coluna de ID não
        #       será exibida visivelmente ao usuário.
        self.tree_hospedes.heading("id", text="ID(oculto)")

        # Oculta a coluna "ID" da exibição, mantendo-a apenas para controle interno.
        # `width=0` define a largura da coluna como zero, ocultando-a.
        # `stretch=False` impede que a coluna seja redimensionada.
        self.tree_hospedes.column("id", width=0, stretch=False)

        # Exibe a Treeview na interface.
        # `fill="both"` faz com que a tabela expanda para ocupar todo o espaço disponível.
        # `expand=True` permite que a tabela se ajuste automaticamente ao
        #       redimensionamento da janela.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor da tabela.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor da tabela.
        self.tree_hospedes.pack(fill="both", expand=True, padx=10, pady=10)

        # Associa um evento de duplo clique à função `selecionar_hospede`.
        # `<Double-1>` indica que a ação será acionada ao dar um
        #       duplo clique em um item da tabela.
        self.tree_hospedes.bind("<Double-1>", self.selecionar_hospede)

        # Cria um botão para voltar ao Dashboard.
        # `text="Voltar ao Dashboard"` define o texto exibido no botão.
        # `command=self.voltar_dashboard` associa a
        #       função `self.voltar_dashboard` ao clique do botão.
        btn_voltar = ttk.Button(self,
                                text="Voltar ao Dashboard",
                                command=self.voltar_dashboard)

        # Exibe o botão na interface.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
        btn_voltar.pack(pady=10)

        # Define a variável `hospede_em_edicao` como `None`, indicando
        #       que nenhum hóspede está sendo editado no momento.
        self.hospede_em_edicao = None

        # Chama a função `listar_hospedes()` para carregar e
        #       exibir a lista de hóspedes na tabela.
        self.listar_hospedes()

    # Define a função para listar os hóspedes na Treeview.
    def listar_hospedes(self):

        # Remove todos os itens da Treeview antes de carregar novos dados.
        # `self.tree_hospedes.get_children()` retorna todas as linhas da tabela.
        # `self.tree_hospedes.delete(item)` remove cada linha encontrada.
        for item in self.tree_hospedes.get_children():
            self.tree_hospedes.delete(item)

        # Busca todos os hóspedes no banco de dados e insere na Treeview.
        # `hospedes_collection.find()` retorna todos os
        #       documentos da coleção de hóspedes.
        for h in hospedes_collection.find():
            # Insere uma nova linha na Treeview com os dados do hóspede.
            # `"", tk.END` indica que a linha será adicionada no final da lista.
            # `h.get("chave", "")` obtém o valor do hóspede e, caso não
            #       exista, retorna uma string vazia.
            # `str(h["_id"])` converte o ID do hóspede para string antes de armazená-lo.
            self.tree_hospedes.insert("", tk.END, values=(
                h.get("nome", ""),  # Nome do hóspede.
                h.get("cpf", ""),  # CPF do hóspede.
                h.get("telefone", ""),  # Telefone do hóspede.
                h.get("email", ""),  # Email do hóspede.
                h.get("endereco", ""),  # Endereço do hóspede.
                str(h["_id"])  # ID do hóspede (convertido para string).
            ))

        # Define `self.hospede_em_edicao` como `None`, indicando
        #       que nenhum hóspede está sendo editado.
        self.hospede_em_edicao = None

    # Define a função para voltar ao Dashboard.
    def voltar_dashboard(self):

        # Oculta a tela atual removendo-a do layout.
        # `self.pack_forget()` faz com que a interface do
        #       cadastro de hóspedes desapareça.
        self.pack_forget()

        # Cria uma nova instância da tela do Dashboard.
        # `TelaDashboard(self.mestre, self.permissoes_usuario)`
        #       exibe novamente o Dashboard.
        TelaDashboard(self.mestre, self.permissoes_usuario)

    # Define a função para selecionar um hóspede da Treeview e
    #       carregar seus dados no formulário.
    def selecionar_hospede(self, event):

        # Obtém o item selecionado na Treeview.
        # `self.tree_hospedes.selection()` retorna a linha selecionada na tabela.
        sel = self.tree_hospedes.selection()

        # Verifica se algum hóspede foi selecionado.
        # Se não houver seleção, interrompe a execução da função.
        if not sel:
            return

        # Obtém os valores da linha selecionada na Treeview.
        # `self.tree_hospedes.item(sel, "values")` retorna os
        #       dados do hóspede selecionado.
        valores = self.tree_hospedes.item(sel, "values")

        # Define o valor do campo "Nome" com o valor da linha selecionada.
        self.nome_var.set(valores[0])

        # Define o valor do campo "CPF" com o valor da linha selecionada.
        self.cpf_var.set(valores[1])

        # Define o valor do campo "Telefone" com o valor da linha selecionada.
        self.telefone_var.set(valores[2])

        # Define o valor do campo "Email" com o valor da linha selecionada.
        self.email_var.set(valores[3])

        # Define o valor do campo "Endereço" com o valor da linha selecionada.
        self.endereco_var.set(valores[4])

        # Converte o ID do hóspede para um objeto `ObjectId` e
        #       armazena na variável `hospede_em_edicao`.
        self.hospede_em_edicao = ObjectId(valores[5])

    # Define a função para cadastrar ou atualizar um hóspede.
    def cadastrar_hospede(self):

        # Obtém o valor do campo "Nome".
        # `self.nome_var.get().strip()` remove espaços
        #       extras antes e depois do nome.
        nome = self.nome_var.get().strip()

        # Obtém o valor do campo "CPF".
        # `self.cpf_var.get().strip()` remove espaços extras antes e depois do CPF.
        cpf = self.cpf_var.get().strip()

        # Obtém o valor do campo "Telefone".
        # `self.telefone_var.get().strip()` remove espaços
        #       extras antes e depois do telefone.
        telefone = self.telefone_var.get().strip()

        # Obtém o valor do campo "Email".
        # `self.email_var.get().strip()` remove espaços
        #       extras antes e depois do email.
        email = self.email_var.get().strip()

        # Obtém o valor do campo "Endereço".
        # `self.endereco_var.get().strip()` remove espaços
        #       extras antes e depois do endereço.
        endereco = self.endereco_var.get().strip()

        # Verifica se o campo "Nome" está vazio.
        # Se estiver vazio, exibe uma mensagem de erro e
        #       interrompe a execução da função.
        if not nome:
            messagebox.showerror("Erro",
                                 "O campo 'Nome' é obrigatório.")
            return

        # Verifica se há um hóspede sendo editado.
        # Se `self.hospede_em_edicao` não for `None`, significa que o
        #       usuário está editando um hóspede existente.
        if self.hospede_em_edicao:

            # Atualiza os dados do hóspede no banco de dados.
            # `hospedes_collection.update_one(...)` localiza o
            #       hóspede pelo `_id` e atualiza os campos com os novos valores.
            hospedes_collection.update_one(
                {"_id": self.hospede_em_edicao},
                {"$set": {
                    "nome": nome,  # Atualiza o campo "nome" com o novo valor.
                    "cpf": cpf,  # Atualiza o campo "cpf" com o novo valor.
                    "telefone": telefone,  # Atualiza o campo "telefone" com o novo valor.
                    "email": email,  # Atualiza o campo "email" com o novo valor.
                    "endereco": endereco  # Atualiza o campo "endereco" com o novo valor.
                }}
            )

            # Exibe uma mensagem de sucesso informando que o hóspede foi atualizado.
            messagebox.showinfo("Sucesso",
                                f"Hóspede '{nome}' atualizado com sucesso!")

        # Se `self.hospede_em_edicao` for `None`, significa que o
        #       usuário está cadastrando um novo hóspede.
        else:

            # Insere um novo hóspede no banco de dados.
            # `hospedes_collection.insert_one(...)` adiciona um
            #       novo documento com os dados do hóspede.
            hospedes_collection.insert_one({
                "nome": nome,  # Insere o campo "nome" com o valor fornecido.
                "cpf": cpf,  # Insere o campo "cpf" com o valor fornecido.
                "telefone": telefone,  # Insere o campo "telefone" com o valor fornecido.
                "email": email,  # Insere o campo "email" com o valor fornecido.
                "endereco": endereco  # Insere o campo "endereco" com o valor fornecido.
            })

            # Exibe uma mensagem de sucesso informando
            #       que o hóspede foi cadastrado.
            messagebox.showinfo("Sucesso",
                                f"Hóspede '{nome}' cadastrado com sucesso!")

        # Chama a função `limpar_campos()` para limpar os campos do formulário.
        self.limpar_campos()

        # Chama a função `listar_hospedes()` para atualizar a
        #       lista de hóspedes na interface.
        self.listar_hospedes()

    # Define a função para limpar os campos do formulário de cadastro de hóspedes.
    def limpar_campos(self):

        # Define o campo "Nome" como uma string vazia, limpando seu conteúdo.
        self.nome_var.set("")

        # Define o campo "CPF" como uma string vazia, limpando seu conteúdo.
        self.cpf_var.set("")

        # Define o campo "Telefone" como uma string vazia, limpando seu conteúdo.
        self.telefone_var.set("")

        # Define o campo "Email" como uma string vazia, limpando seu conteúdo.
        self.email_var.set("")

        # Define o campo "Endereço" como uma string vazia, limpando seu conteúdo.
        self.endereco_var.set("")

        # Define `hospede_em_edicao` como `None`, indicando que
        #       nenhum hóspede está sendo editado.
        self.hospede_em_edicao = None

    # Define a função para deletar um hóspede da lista e do banco de dados.
    def deletar_hospede(self):

        # Obtém o item selecionado na Treeview.
        # `self.tree_hospedes.selection()` retorna a linha selecionada na tabela.
        sel = self.tree_hospedes.selection()

        # Verifica se algum hóspede foi selecionado.
        # Se não houver seleção, exibe uma mensagem de erro e
        #       interrompe a execução da função.
        if not sel:
            messagebox.showerror("Erro",
                                 "Selecione um hóspede para deletar.")
            return

        # Obtém os valores da linha selecionada na Treeview.
        # `self.tree_hospedes.item(sel, "values")` retorna os
        #       dados do hóspede selecionado.
        valores = self.tree_hospedes.item(sel, "values")

        # Obtém o ID do hóspede a partir da coluna de ID da tabela.
        # O ID está localizado na sexta posição da tupla de valores.
        hospede_id_str = valores[5]

        # Exibe uma caixa de diálogo de confirmação antes de deletar o hóspede.
        # `messagebox.askyesno(...)` pergunta ao usuário se deseja
        #       realmente excluir o hóspede.
        # `valores[0]` contém o nome do hóspede, que será exibido na mensagem.
        if messagebox.askyesno("Confirmar",
                               f"Tem certeza que deseja deletar o hóspede '{valores[0]}'?"):
            # Deleta o hóspede do banco de dados.
            # `hospedes_collection.delete_one({"_id": ObjectId(hospede_id_str)})`
            #       remove o hóspede pelo seu ID.
            hospedes_collection.delete_one({"_id": ObjectId(hospede_id_str)})

            # Exibe uma mensagem informando que o hóspede foi deletado com sucesso.
            messagebox.showinfo("Sucesso", "Hóspede deletado.")

            # Chama a função `limpar_campos()` para limpar os campos do formulário.
            self.limpar_campos()

            # Chama a função `listar_hospedes()` para atualizar a
            #       lista de hóspedes na interface.
            self.listar_hospedes()

    # ------------------ FUNÇÃO ABRIR HISTÓRICO------------------ #

    # Define a função para abrir a janela de histórico do hóspede.
    def abrir_historico(self):

        # Verifica se há um hóspede selecionado para exibir o histórico.
        # Se `self.hospede_em_edicao` for `None`, significa que
        #       nenhum hóspede foi selecionado.
        if not self.hospede_em_edicao:
            messagebox.showerror("Erro",
                                 "Selecione um hóspede na lista para ver o histórico.")
            return

        # Obtém o nome do hóspede selecionado no formulário.
        # `self.nome_var.get().strip()` remove espaços extras antes e depois do nome.
        nome_hospede = self.nome_var.get().strip()

        # Verifica se o campo "Nome" está vazio.
        # Se estiver vazio, exibe uma mensagem de erro e
        #       interrompe a execução da função.
        if not nome_hospede:
            messagebox.showerror("Erro",
                                 "Este hóspede não possui nome cadastrado.")
            return

        # Abre a janela de histórico do hóspede.
        # `HistoricoHospedeWindow(self, nome_hospede)` cria uma
        #       nova instância da janela de histórico.
        HistoricoHospedeWindow(self, nome_hospede)


# Define a classe para a janela de histórico do hóspede.
class HistoricoHospedeWindow(tk.Toplevel):

    # Inicializa a janela de histórico do hóspede.
    # `pai` é a janela principal que chamou esta subjanela.
    # `nome_hospede` é o nome do hóspede selecionado para exibição do histórico.
    def __init__(self, pai, nome_hospede):

        # Chama o construtor da classe `tk.Toplevel`, criando
        #       uma nova janela independente.
        super().__init__(pai)

        # Define o título da janela como "Histórico do Hóspede",
        #       exibindo o nome do hóspede selecionado.
        # `self.title(f"Histórico do Hóspede: {nome_hospede}")`
        #       personaliza o título com o nome do hóspede.
        self.title(f"Histórico do Hóspede: {nome_hospede}")

        # Armazena a referência para a janela principal.
        # `self.pai = pai` permite que a subjanela se comunique com a janela principal.
        self.pai = pai

        # Armazena o nome do hóspede selecionado.
        # `self.nome_hospede = nome_hospede` possibilita
        #       recuperar o nome posteriormente.
        self.nome_hospede = nome_hospede

        # Centraliza a janela na tela com largura de 900 pixels e altura de 600 pixels.
        # `self.center_window(900, 600)` posiciona a janela no centro da tela.
        self.center_window(900, 600)

        # Define a cor de fundo da janela.
        # `self.configure(bg="#f7f7f7")` define o fundo como
        #       branco acinzentado (#f7f7f7).
        self.configure(bg="#f7f7f7")

        # Impede que a janela seja redimensionada manualmente pelo usuário.
        # `self.resizable(False, False)` fixa o tamanho da janela,
        #       impedindo aumentos ou reduções.
        self.resizable(False, False)

        # Cria um botão para fechar a janela.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=10)

        # Define a cor de fundo da janela.
        # `self.configure(bg="#f7f7f7")` altera o fundo para a
        #       cor branco acinzentado (#f7f7f7).
        self.configure(bg="#f7f7f7")

        # Impede que a janela seja redimensionada manualmente pelo usuário.
        # `self.resizable(False, False)` fixa o tamanho da janela,
        #       impedindo aumentos ou reduções.
        self.resizable(False, False)

        # Cria uma variável para armazenar a data inicial do filtro.
        # `self.data_de_var = tk.StringVar()` permite que a data
        #       seja manipulada dinamicamente na interface.
        self.data_de_var = tk.StringVar()

        # Cria uma variável para armazenar a data final do filtro.
        # `self.data_ate_var = tk.StringVar()` permite que a data
        #       final seja definida e utilizada em consultas.
        self.data_ate_var = tk.StringVar()

        # Variáveis para filtro de Quarto e Produto

        # Cria uma variável para armazenar o filtro de quarto.
        # `self.filtro_quarto_var = tk.StringVar()` permite que o
        #       usuário filtre os resultados por quarto.
        self.filtro_quarto_var = tk.StringVar()

        # Cria uma variável para armazenar o filtro de produto.
        # `self.filtro_produto_var = tk.StringVar()` permite que o
        #       usuário filtre os resultados por produto.
        self.filtro_produto_var = tk.StringVar()

        # ---------------- FRAME DE FILTROS (linha 1) ---------------- #

        # Cria um frame para organizar os filtros na interface.
        # `frame_filtros_linha1 = ttk.Frame(self)` cria um container
        #       dentro da janela para armazenar os filtros.
        frame_filtros_linha1 = ttk.Frame(self)

        # Exibe o frame na interface.
        # `pady=5` adiciona 5 pixels de espaçamento vertical.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal.
        # `fill="x"` faz com que o frame ocupe toda a largura disponível.
        frame_filtros_linha1.pack(pady=5, padx=10, fill="x")

        # Cria um rótulo (Label) para a data inicial do filtro.
        # `text="Data De:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` define o container onde o rótulo será posicionado.
        ttk.Label(frame_filtros_linha1, text="Data De:").pack(side="left", padx=5)

        # Verifica se o módulo TKCalendar está sendo utilizado.
        # Se `USANDO_TKCALENDAR` for `True`, um campo de seleção
        #       de data (DateEntry) será utilizado.
        if USANDO_TKCALENDAR:

            # Cria um campo de entrada do tipo calendário (DateEntry) para selecionar a data inicial.
            # `frame_filtros_linha1` define o container onde o campo será posicionado.
            # `textvariable=self.data_de_var` associa a variável `self.data_de_var` ao campo de entrada.
            # `date_pattern="yyyy-MM-dd"` define o formato da data (Ano-Mês-Dia).
            # `width=12` define a largura do campo de entrada.
            self.date_de = DateEntry(frame_filtros_linha1,
                                     textvariable=self.data_de_var,
                                     date_pattern="yyyy-MM-dd",
                                     width=12)

            # Exibe o campo de entrada de data na interface.
            # `side="left"` alinha o campo à esquerda dentro do frame.
            # `padx=5` adiciona um espaçamento horizontal de 5 pixels.
            self.date_de.pack(side="left", padx=5)

        # Se `USANDO_TKCALENDAR` for `False`, utiliza um campo
        #       de entrada de texto normal para a data.
        else:

            # Cria um campo de entrada de texto para digitar a data inicial manualmente.
            # `frame_filtros_linha1` define o container onde o campo será posicionado.
            # `textvariable=self.data_de_var` associa a variável `self.data_de_var` ao campo de entrada.
            # `width=15` define a largura do campo de entrada.
            ttk.Entry(frame_filtros_linha1,
                      textvariable=self.data_de_var,
                      width=15).pack(side="left", padx=5)

        # Cria um rótulo (Label) para a data final do filtro.
        # `text="Data Até:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` define o container onde o
        #       rótulo será posicionado.
        # `pack(side="left", padx=5)` alinha o rótulo à esquerda e
        #       adiciona um espaçamento horizontal de 5 pixels.
        ttk.Label(frame_filtros_linha1,
                  text="Data Até:").pack(side="left", padx=5)

        # Verifica se o módulo TKCalendar está sendo utilizado.
        # Se `USANDO_TKCALENDAR` for `True`, um campo de seleção de
        #       data (DateEntry) será utilizado.
        if USANDO_TKCALENDAR:

            # Cria um campo de entrada do tipo calendário (DateEntry) para selecionar a data final.
            # `frame_filtros_linha1` define o container onde o campo será posicionado.
            # `textvariable=self.data_ate_var` associa a variável `self.data_ate_var` ao campo de entrada.
            # `date_pattern="yyyy-MM-dd"` define o formato da data (Ano-Mês-Dia).
            # `width=12` define a largura do campo de entrada.
            self.date_ate = DateEntry(frame_filtros_linha1,
                                      textvariable=self.data_ate_var,
                                      date_pattern="yyyy-MM-dd",
                                      width=12)

            # Exibe o campo de entrada de data na interface.
            # `side="left"` alinha o campo à esquerda dentro do frame.
            # `padx=5` adiciona um espaçamento horizontal de 5 pixels.
            self.date_ate.pack(side="left", padx=5)

        # Se `USANDO_TKCALENDAR` for `False`, utiliza um campo de
        #       entrada de texto normal para a data.
        else:

            # Cria um campo de entrada de texto para digitar a data final manualmente.
            # `frame_filtros_linha1` define o container onde o campo será posicionado.
            # `textvariable=self.data_ate_var` associa a
            #       variável `self.data_ate_var` ao campo de entrada.
            # `width=15` define a largura do campo de entrada.
            ttk.Entry(frame_filtros_linha1,
                      textvariable=self.data_ate_var,
                      width=15).pack(side="left", padx=5)

        # Cria um rótulo (Label) para o campo de filtro de quarto.
        # `text="Quarto:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` define o container onde o rótulo será posicionado.
        # `pack(side="left", padx=5)` alinha o rótulo à esquerda e
        #       adiciona um espaçamento horizontal de 5 pixels.
        ttk.Label(frame_filtros_linha1,
                  text="Quarto:").pack(side="left", padx=5)

        # Cria um campo de entrada de texto para o filtro de quarto.
        # `frame_filtros_linha1` define o container onde o
        #       campo será posicionado.
        # `textvariable=self.filtro_quarto_var` associa a
        #       variável `self.filtro_quarto_var` ao campo de entrada.
        # `width=15` define a largura do campo de entrada.
        # `pack(side="left", padx=5)` alinha o campo à esquerda e
        #       adiciona um espaçamento horizontal de 5 pixels.
        ttk.Entry(frame_filtros_linha1,
                  textvariable=self.filtro_quarto_var,
                  width=15).pack(side="left", padx=5)

        # Cria um rótulo (Label) para o campo de filtro de produto.
        # `text="Produto:"` define o texto exibido no rótulo.
        # `frame_filtros_linha1` define o container onde o rótulo será posicionado.
        # `pack(side="left", padx=5)` alinha o rótulo à esquerda e
        #       adiciona um espaçamento horizontal de 5 pixels.
        ttk.Label(frame_filtros_linha1,
                  text="Produto:").pack(side="left", padx=5)

        # Cria um campo de entrada de texto para o filtro de produto.
        # `frame_filtros_linha1` define o container onde o campo será posicionado.
        # `textvariable=self.filtro_produto_var` associa a
        #       variável `self.filtro_produto_var` ao campo de entrada.
        # `width=15` define a largura do campo de entrada.
        # `pack(side="left", padx=5)` alinha o campo à esquerda e
        #       adiciona um espaçamento horizontal de 5 pixels.
        ttk.Entry(frame_filtros_linha1,
                  textvariable=self.filtro_produto_var,
                  width=15).pack(side="left", padx=5)

        # ---------------- BOTÃO FILTRAR ---------------- #

        # Cria um botão para aplicar os filtros definidos pelo usuário.
        # `text="Filtrar"` define o texto exibido no botão.
        # `frame_filtros_linha1` define o container onde o botão será posicionado.
        # `command=self.aplicar_filtro` associa a função `aplicar_filtro` ao
        #       botão, que será executada quando o botão for clicado.
        btn_filtrar = ttk.Button(frame_filtros_linha1,
                                 text="Filtrar",
                                 command=self.aplicar_filtro)

        # Exibe o botão de filtro na interface.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels.
        btn_filtrar.pack(side="left", padx=10)

        # ---------------- TREEVIEW ---------------- #

        # Define as colunas da tabela (Treeview) para exibir o histórico de consumo.
        # Cada string dentro da tupla representa uma coluna da tabela.
        colunas = ("data_inicio", "data_fim", "quarto", "produtos", "valor_final", "data_criacao", "idreserva")

        # Cria um widget Treeview para exibir os dados históricos na interface gráfica.
        # `self` define o container onde a tabela será posicionada.
        # `columns=colunas` especifica as colunas da tabela.
        # `show="headings"` oculta a coluna padrão e exibe apenas os cabeçalhos definidos.
        # `height=15` define a altura da tabela, ou seja, quantas
        #       linhas serão exibidas antes da rolagem.
        self.tree_historico = ttk.Treeview(self,
                                           columns=colunas,
                                           show="headings",
                                           height=15)

        # ---------------- DEFINIÇÃO DOS CABEÇALHOS ---------------- #

        # Define o cabeçalho da coluna "data_inicio".
        # `text="Início"` define o nome visível da coluna como "Início".
        self.tree_historico.heading("data_inicio", text="Início")

        # Define o cabeçalho da coluna "data_fim".
        # `text="Fim"` define o nome visível da coluna como "Fim".
        self.tree_historico.heading("data_fim", text="Fim")

        # Define o cabeçalho da coluna "quarto".
        # `text="Quarto"` define o nome visível da coluna como "Quarto".
        self.tree_historico.heading("quarto", text="Quarto")

        # Define o cabeçalho da coluna "produtos".
        # `text="Produtos Consumidos"` define o nome visível da
        #       coluna como "Produtos Consumidos".
        self.tree_historico.heading("produtos", text="Produtos Consumidos")

        # Define o cabeçalho da coluna "valor_final".
        # `text="Valor Final"` define o nome visível da coluna como "Valor Final".
        self.tree_historico.heading("valor_final", text="Valor Final")

        # Define o cabeçalho da coluna "data_criacao".
        # `text="Data Criação"` define o nome visível da coluna como "Data Criação".
        self.tree_historico.heading("data_criacao", text="Data Criação")

        # Define o cabeçalho da coluna "idreserva".
        # `text="ID(oculto)"` define o nome visível da coluna como "ID(oculto)".
        self.tree_historico.heading("idreserva", text="ID(oculto)")

        # ---------------- CONFIGURAÇÃO DAS COLUNAS ---------------- #

        # Oculta a coluna de ID da reserva para que ela não seja exibida ao usuário.
        # `width=0` define a largura da coluna como 0 pixels.
        # `stretch=False` impede que a coluna seja redimensionada.
        self.tree_historico.column("idreserva",
                                   width=0,
                                   stretch=False)

        # Exibe a tabela (Treeview) na interface gráfica.
        # `fill="both"` faz com que a tabela expanda para ocupar todo o espaço disponível.
        # `expand=True` permite que a tabela cresça dinamicamente se a janela for redimensionada.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor da tabela.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor da tabela.
        self.tree_historico.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- LABEL DE RESUMO ---------------- #

        # Cria um rótulo (Label) para exibir um resumo dos dados na interface.
        # O rótulo pode exibir, por exemplo, a quantidade de reservas e o valor total.
        # `text=""` inicia o rótulo sem texto, que será atualizado posteriormente.
        # `font=("Helvetica", 10, "bold")` define a fonte do texto
        #       como Helvetica, tamanho 10, e negrito.
        self.lbl_resumo = ttk.Label(self, text="", font=("Helvetica", 10, "bold"))

        # Exibe o rótulo na interface gráfica.
        # `pady=5` adiciona 5 pixels de espaçamento vertical abaixo do rótulo.
        self.lbl_resumo.pack(pady=5)

        # ---------------- FRAME DE BOTÕES FINAIS ---------------- #

        # Cria um frame para organizar os botões na parte inferior da interface.
        # `self` define o container onde o frame será posicionado.
        frame_botoes_finais = ttk.Frame(self)

        # Exibe o frame na interface.
        # `pady=5` adiciona 5 pixels de espaçamento vertical entre o
        #       frame e os elementos acima.
        frame_botoes_finais.pack(pady=5)

        # ---------------- BOTÃO EXPORTAR EXCEL ---------------- #

        # Cria um botão para exportar os dados da tabela para um arquivo Excel.
        # `text="Exportar Excel"` define o texto exibido no botão.
        # `frame_botoes_finais` define o container onde o botão será posicionado.
        # `command=self.exportar_excel` associa a função `exportar_excel` ao
        #       botão, que será executada quando o botão for clicado.
        btn_exportar = ttk.Button(frame_botoes_finais,
                                  text="Exportar Excel",
                                  command=self.exportar_excel)

        # Exibe o botão de exportação na interface gráfica.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        btn_exportar.pack(side="left", padx=10)

        # ---------------- BOTÃO FECHAR ---------------- #

        # Cria um botão para fechar a janela atual.
        # `text="Fechar"` define o texto exibido no botão.
        # `frame_botoes_finais` define o container onde o botão será posicionado.
        # `command=self.destroy` associa a ação de fechar a janela ao botão.
        btn_fechar = ttk.Button(frame_botoes_finais,
                                text="Fechar",
                                command=self.destroy)

        # Exibe o botão de fechar na interface gráfica.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        btn_fechar.pack(side="left", padx=10)

        # ---------------- CARREGAR HISTÓRICO INICIALMENTE ---------------- #

        # Chama a função `carregar_historico()` ao iniciar a interface.
        # Isso garante que os dados sejam carregados automaticamente ao abrir a janela.
        self.carregar_historico()

    # Define uma função para carregar o histórico de reservas do hóspede.
    # `self` refere-se à instância da classe que contém a tabela de histórico.
    # `data_de` (opcional) representa a data inicial para o filtro das reservas.
    # `data_ate` (opcional) representa a data final para o filtro das reservas.
    def carregar_historico(self, data_de=None, data_ate=None):

        # ---------------- LIMPA A TREEVIEW ---------------- #

        # Remove todos os itens existentes na tabela de histórico
        #       antes de carregar novos dados.
        # `self.tree_historico.get_children()` retorna todos os
        #       elementos da tabela.
        for item in self.tree_historico.get_children():
            # `delete(item)` remove cada item encontrado na tabela.
            self.tree_historico.delete(item)

        # ---------------- MONTAGEM DA QUERY ---------------- #

        # Cria um dicionário para armazenar os critérios de busca no banco de dados.
        # Busca todas as reservas onde o nome do hóspede esteja presente no array 'hospedes'.
        # `self.nome_hospede` contém o nome do hóspede selecionado.
        query_base = {"hospedes": self.nome_hospede}

        # ---------------- FILTRO DE DATA (SE FORNECIDO) ---------------- #

        # Verifica se os filtros de data foram informados pelo usuário.
        if data_de or data_ate:
            # Aplica um filtro no banco de dados para buscar reservas
            #       dentro do intervalo de datas.
            # O filtro considera a sobreposição das datas no MongoDB.
            query_base["$expr"] = {

                "$and": [

                    # Busca todas as reservas onde a data de início seja menor
                    #       ou igual à data final do filtro.
                    {"$lte": ["$data_inicio", data_ate if data_ate else "9999-12-31"]},

                    # Busca todas as reservas onde a data de fim seja maior ou
                    #       igual à data inicial do filtro.
                    {"$gte": ["$data_fim", data_de if data_de else "0000-01-01"]}

                ]
            }

        # ---------------- BUSCA NO BANCO DE DADOS ---------------- #

        # Executa a busca no banco de dados MongoDB aplicando os filtros definidos.
        # `query_base` contém os critérios de busca, incluindo filtros de
        #       hóspede e, se aplicável, de data.
        # `.sort("data_inicio", 1)` ordena os resultados pela
        #       data de início em ordem crescente.
        reservas = reservas_collection.find(query_base).sort("data_inicio", 1)

        # ---------------- LER OS FILTROS DE QUARTO E PRODUTO ---------------- #

        # Obtém o valor do filtro de quarto digitado pelo usuário.
        # `.get()` pega o valor do campo de entrada e `.strip()` remove espaços extras.
        # `.lower()` converte o valor para minúsculas para facilitar a comparação.
        filtro_quarto = self.filtro_quarto_var.get().strip().lower()

        # Obtém o valor do filtro de produto digitado pelo usuário.
        # `.get()` pega o valor do campo de entrada e `.strip()` remove espaços extras.
        # `.lower()` converte o valor para minúsculas para facilitar a comparação.
        filtro_produto = self.filtro_produto_var.get().strip().lower()

        # ---------------- INICIALIZAÇÃO DAS VARIÁVEIS DE SOMA ---------------- #

        # Variável para armazenar a soma total dos
        #       valores das reservas filtradas.
        soma_total = 0.0

        # Variável para contar o número total de registros encontrados.
        contagem = 0

        # ---------------- PERCORRE TODAS AS RESERVAS ENCONTRADAS ---------------- #

        # Itera sobre cada reserva retornada pela
        #       consulta ao banco de dados.
        for r in reservas:

            # ---------------- OBTÉM DADOS BÁSICOS DA RESERVA ---------------- #

            # Obtém a data de início da reserva.
            # `.get("data_inicio", "")` pega o valor da chave "data_inicio" ou
            #       retorna uma string vazia se a chave não existir.
            data_inicio = r.get("data_inicio", "")

            # Obtém a data de fim da reserva.
            # `.get("data_fim", "")` pega o valor da chave "data_fim" ou retorna
            #       uma string vazia se a chave não existir.
            data_fim = r.get("data_fim", "")

            # Obtém o número do quarto associado à reserva.
            # `.get("numero_quarto", "")` pega o valor da chave "numero_quarto" ou
            #       retorna uma string vazia se a chave não existir.
            quarto = r.get("numero_quarto", "")

            # Obtém o valor final da reserva.
            # `.get("valor_final", 0.0)` pega o valor da chave "valor_final" ou
            #       retorna 0.0 se a chave não existir.
            valor_final = r.get("valor_final", 0.0)

            # Obtém a data de criação da reserva.
            # `.get("data_criacao", "")` pega o valor da chave "data_criacao" ou
            #       retorna uma string vazia se a chave não existir.
            data_criacao = r.get("data_criacao", "")

            # ---------------- OBTÉM LISTA DE PRODUTOS CONSUMIDOS ---------------- #

            # Obtém a lista de produtos consumidos na reserva.
            # `.get("produtos", [])` pega o valor da chave "produtos" ou retorna uma
            #       lista vazia se a chave não existir.
            lista_produtos = r.get("produtos", [])

            # ---------------- MONTA STRING DE PRODUTOS CONSUMIDOS ---------------- #

            # Gera uma string formatada contendo os produtos consumidos e suas quantidades.
            # Usa um loop `for` dentro do `.join()` para concatenar os
            #       produtos no formato "Produto(xQuantidade)".
            produtos_str = ", ".join(
                f"{item['nome']}(x{item['quantidade']})"
                for item in lista_produtos
            )

            # ---------------- FILTRO ADICIONAL (QUARTO E PRODUTO) EM PYTHON ---------------- #

            # Verifica se o usuário digitou um valor no campo de filtro de quarto.
            # Se o campo não estiver vazio, verifica se o texto digitado não
            #       está contido no nome do quarto.
            # Caso o nome do quarto não contenha o texto digitado, a
            #       reserva será ignorada (`continue`).
            if filtro_quarto:
                if filtro_quarto not in quarto.lower():
                    continue

            # Verifica se o usuário digitou um valor no campo de filtro de produto.
            # Se o campo não estiver vazio, verifica se o texto digitado não
            #       está contido na string de produtos consumidos.
            # Caso a string de produtos não contenha o texto digitado, a
            #       reserva será ignorada (`continue`).
            if filtro_produto:
                if filtro_produto not in produtos_str.lower():
                    continue

            # ---------------- INSERE OS DADOS FILTRADOS NO TREEVIEW ---------------- #

            # Se a reserva passou pelos filtros, insere os dados na
            #       tabela de histórico (`Treeview`).
            self.tree_historico.insert(
                "", tk.END,  # Insere um novo item no final da lista.
                values=(
                    data_inicio,  # Data de início da reserva.
                    data_fim,  # Data de fim da reserva.
                    quarto,  # Número do quarto reservado.
                    produtos_str,  # Produtos consumidos durante a estadia.
                    valor_final,  # Valor total da reserva.
                    data_criacao,  # Data de criação da reserva.
                    str(r["_id"])  # ID da reserva (convertido para string).
                )
            )

            # ---------------- ATUALIZAÇÃO DE CONTADORES ---------------- #

            # Adiciona o valor final da reserva ao total acumulado.
            soma_total += float(valor_final)

            # Incrementa o contador de registros para exibição posterior.
            contagem += 1

        # ---------------- ATUALIZA O RESUMO NA INTERFACE ---------------- #

        # Atualiza o texto da label de resumo (`self.lbl_resumo`) com a
        #       quantidade de reservas encontradas
        #       e a soma total dos valores das reservas filtradas.
        self.lbl_resumo.config(
            text=(

                # Exibe o número total de reservas encontradas.
                f"Total de Reservas: {contagem} | "

                # Exibe a soma total dos valores formatada com duas casas decimais.
                f"Soma dos Valores: R$ {soma_total:.2f}"

            )
        )

    # Define a função responsável por aplicar os filtros de
    #       data na pesquisa de reservas.
    def aplicar_filtro(self):

        # ---------------- OBTÉM OS VALORES DOS CAMPOS DE DATA ---------------- #

        # Obtém o valor digitado no campo "Data De" e remove espaços extras.
        data_de_str = self.data_de_var.get().strip()

        # Obtém o valor digitado no campo "Data Até" e remove espaços extras.
        data_ate_str = self.data_ate_var.get().strip()

        # ---------------- INICIALIZA AS VARIÁVEIS DE DATA ---------------- #

        # Inicializa `data_de` como `None`, indicando que o
        #       filtro pode não ser aplicado.
        data_de = None

        # Inicializa `data_ate` como `None`, indicando que o
        #       filtro pode não ser aplicado.
        data_ate = None

        # ---------------- CONVERSÃO DAS DATAS (SE VÁLIDAS) ---------------- #

        # Tenta converter a data inicial (`data_de_str`) para o
        #       formato correto (YYYY-MM-DD).
        try:

            if data_de_str:
                # `strptime` verifica se a string está no formato
                #       correto e retorna um objeto `datetime`.
                datetime.datetime.strptime(data_de_str, "%Y-%m-%d")

                # Se a conversão for bem-sucedida, armazena a data formatada.
                data_de = data_de_str

        except:

            # Se a conversão falhar, mantém `data_de` como `None`.
            pass

            # ---------------- TENTA CONVERTER A DATA FINAL (SE VÁLIDA) ---------------- #

        # Tenta converter a data final (`data_ate_str`) para o
        #       formato correto (YYYY-MM-DD).
        try:

            if data_ate_str:
                # `strptime` verifica se a string está no formato
                #       correto e retorna um objeto `datetime`.
                datetime.datetime.strptime(data_ate_str, "%Y-%m-%d")

                # Se a conversão for bem-sucedida, armazena a data formatada.
                data_ate = data_ate_str

        except:

            # Se a conversão falhar, mantém `data_ate` como `None`.
            pass

        # Chama a função `carregar_historico()` passando as datas
        #       filtradas (`data_de` e `data_ate`).
        # Se as datas forem inválidas, os valores permanecerão como `None`, e
        #       o histórico será carregado sem filtro de data.
        self.carregar_historico(data_de=data_de, data_ate=data_ate)

    # Define a função responsável por exportar os dados do
    #       Treeview para um arquivo Excel.
    def exportar_excel(self):

        # Obtém todos os itens (linhas) da tabela `self.tree_historico`.
        itens = self.tree_historico.get_children()

        # Se não houver itens na tabela, exibe uma mensagem informando
        #       que não há dados para exportar.
        if not itens:
            messagebox.showinfo("Informação", "Não há dados para exportar.")
            return  # Encerra a função.

        # Cria uma lista vazia para armazenar os valores das linhas da tabela.
        linhas_data = []

        # Itera sobre cada item presente na tabela `self.tree_historico`.
        for item_id in itens:
            # Obtém os valores das colunas do item atual.
            valores = self.tree_historico.item(item_id, "values")

            # `valores` retorna uma tupla contendo as informações de cada reserva:
            # (data_inicio, data_fim, quarto, produtos, valor_final,
            #       data_criacao, idreserva)

            # Adiciona os valores extraídos à lista `linhas_data`, que
            #       armazenará todas as reservas a serem exportadas.
            linhas_data.append(valores)

        # Define os nomes das colunas do DataFrame, correspondendo às
        #       informações extraídas do Treeview.
        colunas_df = [
            "Início",  # Data de início da reserva.
            "Fim",  # Data de fim da reserva.
            "Quarto",  # Número do quarto reservado.
            "Produtos Consumidos",  # Lista de produtos consumidos na reserva.
            "Valor Final",  # Valor total da reserva.
            "Data Criação",  # Data de criação da reserva no sistema.
            "ID Reserva"  # Identificador único da reserva no banco de dados.
        ]

        # Cria um DataFrame do Pandas com os dados extraídos e os
        #       nomes das colunas definidos acima.
        df = pd.DataFrame(linhas_data, columns=colunas_df)

        # Define o caminho onde o arquivo Excel será salvo.
        # `os.getcwd()` obtém o diretório atual do script e `os.path.join()`
        #       cria o caminho completo do arquivo.
        caminho = os.path.join(os.getcwd(), "historico_hospede.xlsx")

        try:

            # Salva o DataFrame `df` em um arquivo Excel no caminho especificado.
            # `index=False` remove a numeração automática do DataFrame no Excel.
            df.to_excel(caminho, index=False)

            # Exibe uma mensagem informando que a exportação foi bem-sucedida.
            messagebox.showinfo("Sucesso",
                                f"Relatório exportado para: {caminho}")

        except Exception as e:

            # Se ocorrer um erro durante a exportação, exibe uma
            #       mensagem com a descrição do erro.
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

    # Define um método chamado `center_window` que centraliza a
    #       janela na tela do usuário.
    # Esse método recebe dois parâmetros: `largura` e `altura`,
    #       que representam as dimensões da janela.
    def center_window(self, largura, altura):

        # Obtém a largura total da tela do usuário.
        # `winfo_screenwidth()` retorna a largura em pixels do monitor
        #       onde a aplicação está sendo executada.
        larg_tela = self.winfo_screenwidth()

        # Obtém a altura total da tela do usuário.
        # `winfo_screenheight()` retorna a altura em pixels do monitor.
        alt_tela = self.winfo_screenheight()

        # Calcula a posição X para centralizar a janela horizontalmente.
        # `(larg_tela - largura) / 2` pega a largura total da tela e
        #       subtrai a largura da janela.
        # Dividindo por 2, encontramos a posição exata para centralizar.
        # `int(...)` converte o valor para um número inteiro, pois `geometry`
        #       não aceita números decimais.
        x = int((larg_tela - largura) / 2)

        # Calcula a posição Y para centralizar a janela verticalmente.
        # `(alt_tela - altura) / 2` pega a altura total da tela e
        #       subtrai a altura da janela.
        # Dividindo por 2, encontramos a posição exata para que a
        #       janela fique centralizada verticalmente.
        y = int((alt_tela - altura) / 2)

        # Define o tamanho e a posição da janela usando `geometry()`.
        # O formato da string é: `"largura x altura + posição_x + posição_y"`.
        # Isso posiciona a janela no centro exato da tela.
        self.geometry(f"{largura}x{altura}+{x}+{y}")



# =============================================================================
# =========== TELA DE GERENCIAMENTO DE USUÁRIOS (FRAME DENTRO DO APP) =========
# =============================================================================
# ==========================

# Classe para Gerenciamento de Usuários Dentro do Sistema
# ==========================

# Define uma classe chamada `GerenciarUsuariosFrame`, que
#       representa um painel (Frame) para gerenciar usuários.
# Essa classe funciona de maneira semelhante à `GerenciarUsuariosWindow`,
#       mas em vez de abrir uma nova janela (`Toplevel`),
#       ela é carregada dentro da interface principal do
#       sistema (após o login bem-sucedido).
class GerenciarUsuariosFrame(tk.Frame):

    # ==========================
    # Inicializando o Frame
    # ==========================

    # O método `__init__` é chamado automaticamente quando uma nova
    #       instância de `GerenciarUsuariosFrame` é criada.
    # Ele recebe dois parâmetros:
    # `mestre` → Referência à janela principal do sistema, onde esse frame será exibido.
    # `permissoes_usuario` → Armazena as permissões do usuário
    #       logado (por exemplo, "gerente" ou "recepcionista").
    def __init__(self, mestre, permissoes_usuario):

        # Chama o método `__init__` da classe `tk.Frame`, garantindo
        #       que o frame seja inicializado corretamente.
        # Define `bg="#f7f7f7"` para configurar o fundo do frame
        #       com um tom claro de cinza.
        super().__init__(mestre, bg="#f7f7f7")

        # Armazena uma referência à janela principal do sistema.
        self.mestre = mestre

        # Armazena as permissões do usuário logado.
        # Isso será útil para definir quais funcionalidades ele
        #       pode acessar dentro do sistema.
        self.permissoes_usuario = permissoes_usuario

        # `pack(fill="both", expand=True)` → Faz com que o frame ocupe
        #       toda a área disponível dentro da janela principal.
        # `fill="both"` → Expande o frame tanto na largura quanto na altura.
        # `expand=True` → Permite que o frame cresça dinamicamente caso a
        #       janela principal seja redimensionada.
        self.pack(fill="both", expand=True)

        # Cria um rótulo (`Label`) chamado `lbl_titulo`, que será exibido
        #       no topo da tela para indicar o gerenciamento de usuários.
        # Esse rótulo exibe o texto "Gerenciamento de Usuários" em fonte grande e negrito.
        lbl_titulo = tk.Label(

            self,  # O rótulo será colocado dentro do próprio Frame `GerenciarUsuariosFrame`
            text="Gerenciamento de Usuários",  # Define o texto que será exibido no rótulo
            font=("Helvetica", 16, "bold"),  # Define a fonte como "Helvetica", tamanho 16 e em negrito
            bg="#f7f7f7"  # Define o fundo do rótulo com a mesma cor do Frame para harmonizar a interface

        )

        # Posiciona o rótulo na tela usando `pack()`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e
        #       abaixo do rótulo para não ficar colado nos elementos próximos.
        lbl_titulo.pack(pady=10)

        # Cria uma variável chamada `self.login_var` para armazenar o login do usuário.
        # `tk.StringVar()` cria uma variável que pode ser associada a
        #       um campo de entrada (`Entry`), garantindo que o valor digitado
        #       possa ser recuperado e manipulado posteriormente.
        self.login_var = tk.StringVar()

        # Cria uma variável chamada `self.senha_var` para armazenar a senha do usuário.
        # Assim como `login_var`, essa variável será associada ao campo de entrada da senha.
        self.senha_var = tk.StringVar()

        # Cria uma variável chamada `self.permissoes_var` para armazenar o
        #       nível de permissões do usuário.
        # `tk.StringVar(value="recepcionista")` define "recepcionista" como valor padrão.
        # Isso significa que, caso o usuário não escolha outra opção, ele
        #       será cadastrado como recepcionista.
        self.permissoes_var = tk.StringVar(value="recepcionista")

        # `self.usuario_em_edicao` é uma variável usada para
        #       armazenar o ID do usuário que está sendo editado.
        # Quando `None`, significa que um novo usuário será cadastrado.
        # Quando contém um ID, significa que o usuário está em modo de edição.
        self.usuario_em_edicao = None

        # Cria um frame (`ttk.Frame`) para organizar os campos do formulário.
        # `self` define que o frame será colocado dentro da tela
        #       principal do gerenciamento de usuários.
        frame_form = ttk.Frame(self)

        # Posiciona o frame dentro da interface.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels.
        # `padx=20` adiciona um espaçamento horizontal de 20 pixels,
        #       garantindo que os campos fiquem bem distribuídos.
        frame_form.pack(pady=10, padx=20)

        # Cria um rótulo (Label) dentro do frame_form para exibir o texto "Login:"
        # `text="Login:"` define o texto exibido no rótulo.
        # `frame_form` é o container onde o rótulo será colocado.
        # `.grid(row=0, column=0, padx=5, pady=5, sticky="e")` define o posicionamento:
        # - `row=0` coloca o rótulo na primeira linha.
        # - `column=0` coloca o rótulo na primeira coluna.
        # - `padx=5, pady=5` adiciona espaçamento de 5 pixels nas
        #       margens horizontal e vertical.
        # - `sticky="e"` alinha o rótulo à direita (east).
        ttk.Label(frame_form,
                  text="Login:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) dentro do frame_form
        #       para o usuário digitar o login.
        # `textvariable=self.login_var` associa o valor digitado a uma variável Tkinter (StringVar).
        # `.grid(row=0, column=1, padx=5, pady=5)` define o posicionamento:
        # - `row=0` coloca o campo de entrada na mesma linha do rótulo.
        # - `column=1` coloca o campo de entrada na segunda coluna, ao lado do rótulo.
        # - `padx=5, pady=5` adiciona espaçamento de 5 pixels nas margens horizontal e vertical.
        ttk.Entry(frame_form,
                  textvariable=self.login_var).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) dentro do `frame_form` para exibir o texto "Senha:"
        # `text="Senha:"` define o texto exibido no rótulo.
        # `frame_form` é o container onde o rótulo será colocado.
        # `.grid(row=1, column=0, padx=5, pady=5, sticky="e")` define o posicionamento:
        # - `row=1` coloca o rótulo na segunda linha da grade.
        # - `column=0` posiciona o rótulo na primeira coluna.
        # - `padx=5, pady=5` adiciona espaçamento de 5 pixels nas margens horizontal e vertical.
        # - `sticky="e"` alinha o rótulo à direita (east).
        ttk.Label(frame_form,
                  text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) dentro do `frame_form`
        #       para o usuário digitar a senha.
        # `textvariable=self.senha_var` associa o valor digitado a uma
        #       variável Tkinter (StringVar).
        # `show="*"` oculta os caracteres digitados, exibindo um asterisco (*)
        #       para cada caractere digitado, garantindo segurança na senha.
        # `.grid(row=1, column=1, padx=5, pady=5)` define o posicionamento:
        # - `row=1` posiciona o campo de entrada na segunda linha, alinhado ao rótulo "Senha".
        # - `column=1` coloca o campo de entrada na segunda coluna, ao lado do rótulo.
        # - `padx=5, pady=5` adiciona espaçamento de 5 pixels nas margens horizontal e vertical.
        ttk.Entry(frame_form,
                  textvariable=self.senha_var,
                  show="*").grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) dentro do `frame_form` para exibir o texto "Permissão:"
        # `text="Permissão:"` define o texto exibido no rótulo.
        # `frame_form` é o container onde o rótulo será posicionado.
        # `.grid(row=2, column=0, padx=5, pady=5, sticky="e")` define a posição do rótulo:
        # - `row=2` posiciona o rótulo na terceira linha da grade.
        # - `column=0` posiciona o rótulo na primeira coluna.
        # - `padx=5, pady=5` adiciona espaçamento de 5 pixels nas
        #       margens horizontal e vertical.
        # - `sticky="e"` alinha o rótulo à direita (east), garantindo
        #       alinhamento visual com os outros rótulos.
        ttk.Label(frame_form,
                  text="Permissão:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria uma caixa de seleção (Combobox) dentro do `frame_form`
        #       para escolher o nível de permissão do usuário.
        # `textvariable=self.permissoes_var` associa a opção selecionada a
        #       uma variável Tkinter (StringVar).
        # `values=["gerente", "recepcionista"]` define as opções disponíveis no menu suspenso:
        #    - "gerente": Usuário com permissões administrativas completas.
        #    - "recepcionista": Usuário com permissões limitadas ao atendimento.
        # `state="readonly"` impede que o usuário digite valores manuais,
        #       permitindo apenas a seleção das opções pré-definidas.
        # `width=28` define a largura da caixa de seleção, garantindo um
        #       tamanho adequado para exibir o texto das opções sem cortes.
        combo_perm = ttk.Combobox(frame_form,
                                  textvariable=self.permissoes_var,
                                  values=["gerente", "recepcionista"],
                                  state="readonly",
                                  width=28)

        # Define a posição da caixa de seleção (Combobox) dentro do layout da grade (grid).
        # `.grid(row=2, column=1, padx=5, pady=5)` configura o posicionamento do widget:
        # - `row=2` posiciona a caixa de seleção na terceira linha, ao lado do rótulo "Permissão".
        # - `column=1` coloca a caixa de seleção na segunda coluna.
        # - `padx=5, pady=5` adiciona espaçamento de 5 pixels nas margens
        #       horizontal e vertical, garantindo um layout espaçado e legível.
        combo_perm.grid(row=2, column=1, padx=5, pady=5)

        # Cria um botão para cadastrar ou atualizar um usuário no sistema.
        # `text="Cadastrar/Atualizar"` define o texto exibido no botão,
        #       indicando sua função dupla:
        #    - Se o usuário já existir, ele será atualizado.
        #    - Caso contrário, um novo usuário será cadastrado.
        # `command=self.cadastrar_ou_atualizar` associa a ação do
        #       botão ao método `self.cadastrar_ou_atualizar`,
        #       que será executado quando o botão for pressionado.
        btn_cadastrar = ttk.Button(frame_form,
                                   text="Cadastrar/Atualizar",
                                   command=self.cadastrar_ou_atualizar)

        # Define a posição do botão dentro do layout da grade (grid).
        # `.grid(row=3, column=0, pady=10, sticky="e")` configura a disposição do botão:
        # - `row=3` posiciona o botão na quarta linha da grade,
        #       abaixo dos campos de entrada.
        # - `column=0` posiciona o botão na primeira coluna, alinhado
        #       com os rótulos dos campos anteriores.
        # - `pady=10` adiciona um espaçamento de 10 pixels acima e abaixo
        #       do botão, criando um visual mais espaçado.
        # - `sticky="e"` alinha o botão à direita (east), garantindo um
        #       alinhamento mais organizado dentro do formulário.
        btn_cadastrar.grid(row=3, column=0, pady=10, sticky="e")

        # Cria um botão para excluir um usuário do sistema.
        # `text="Excluir"` define o texto exibido no botão, indicando sua função de remoção.
        # `command=self.excluir_usuario` associa a ação do botão ao
        #       método `self.excluir_usuario`,
        #       que será executado quando o botão for pressionado.
        btn_excluir = ttk.Button(frame_form, text="Excluir", command=self.excluir_usuario)

        # Define a posição do botão dentro do layout da grade (grid).
        # `.grid(row=3, column=1, pady=10, sticky="w")` configura a disposição do botão:
        # - `row=3` posiciona o botão na quarta linha da grade, abaixo
        #       dos campos de entrada.
        # - `column=1` posiciona o botão na segunda coluna, ao lado do
        #       botão "Cadastrar/Atualizar".
        # - `pady=10` adiciona um espaçamento de 10 pixels acima e abaixo do
        #       botão, criando um visual mais organizado.
        # - `sticky="w"` alinha o botão à esquerda (west), garantindo que
        #       fique alinhado dentro da célula da grade.
        btn_excluir.grid(row=3, column=1, pady=10, sticky="w")

        # Cria um widget Treeview para exibir a lista de usuários cadastrados.
        # `self.tree_usuarios = ttk.Treeview(self, ...)` cria o componente
        #       Treeview dentro do frame atual.
        # `columns=("login", "senha", "permissoes", "id")` define as colunas da tabela:
        #   - "login": Nome de usuário cadastrado.
        #   - "senha": Senha do usuário (geralmente não deveria ser exibida por questões de segurança).
        #   - "permissoes": Nível de permissão do usuário (ex.: gerente, recepcionista).
        #   - "id": Identificador único do usuário no banco de dados (oculto na interface).
        # `show="headings"` oculta a coluna extra que aparece por padrão no
        #       Treeview e exibe apenas os cabeçalhos das colunas definidas.
        self.tree_usuarios = ttk.Treeview(self,
                                          columns=("login", "senha", "permissoes", "id"),
                                          show="headings")

        # Define o título de cada coluna na tabela.
        # `self.tree_usuarios.heading("login", text="Login")` define o
        #       cabeçalho da coluna "login" com o texto "Login".
        self.tree_usuarios.heading("login", text="Login")

        # `self.tree_usuarios.heading("senha", text="Senha")` define o
        #       cabeçalho da coluna "senha" com o texto "Senha".
        self.tree_usuarios.heading("senha", text="Senha")

        # `self.tree_usuarios.heading("permissoes", text="Permissão")` define o
        #       cabeçalho da coluna "permissoes" com o texto "Permissão".
        self.tree_usuarios.heading("permissoes", text="Permissão")

        # `self.tree_usuarios.heading("id", text="ID (oculto)")` define o
        #       cabeçalho da coluna "id" com o texto "ID (oculto)".
        # O ID geralmente é usado internamente para manipulação dos usuários,
        #       mas não precisa ser visível para o usuário final.
        self.tree_usuarios.heading("id", text="ID (oculto)")

        # Define as configurações de exibição de cada coluna.
        # `self.tree_usuarios.column("id", width=0, stretch=False)` configura a coluna "id":
        #   - `width=0` define a largura da coluna como 0, tornando-a invisível.
        #   - `stretch=False` impede que a coluna seja redimensionada,
        #           garantindo que continue oculta.
        self.tree_usuarios.column("id", width=0, stretch=False)

        # Exibe a tabela (Treeview) dentro da interface gráfica.
        # `.pack(fill="both", expand=True, padx=10, pady=10)` configura a exibição da tabela:
        # - `fill="both"` permite que o widget se expanda horizontalmente e verticalmente.
        # - `expand=True` permite que o widget ocupe todo o espaço disponível na janela.
        # - `padx=10, pady=10` adiciona um espaçamento de 10 pixels nas
        #       margens horizontal e vertical,
        #   garantindo um layout mais espaçado e legível.
        self.tree_usuarios.pack(fill="both", expand=True, padx=10, pady=10)

        # Adiciona um evento de clique duplo na tabela (Treeview).
        # `.bind("<Double-1>", self.selecionar_usuario)` associa um evento à Treeview:
        # - `<Double-1>` significa que a ação será acionada ao dar um
        #       clique duplo do mouse sobre um item da tabela.
        # - `self.selecionar_usuario` é a função que será chamada quando um
        #       usuário der um clique duplo,
        #   permitindo que os dados do usuário selecionado sejam carregados para edição.
        self.tree_usuarios.bind("<Double-1>", self.selecionar_usuario)

        # Cria um botão para voltar ao painel principal (Dashboard).
        # `text="Voltar ao Dashboard"` define o texto exibido no botão.
        # `command=self.voltar_dashboard` associa a ação do botão ao método `self.voltar_dashboard`,
        #   que será executado ao clicar no botão, retornando o usuário à tela principal.
        btn_voltar = ttk.Button(self,
                                text="Voltar ao Dashboard",
                                command=self.voltar_dashboard)

        # Exibe o botão na interface gráfica.
        # `.pack(pady=10)` configura o posicionamento do botão:
        # - `pady=10` adiciona um espaçamento de 10 pixels na parte
        #       superior e inferior do botão,
        #       melhorando o layout e a disposição dos elementos na tela.
        btn_voltar.pack(pady=10)

        # Chama o método `listar_usuarios()`, que busca e
        #       exibe a lista de usuários cadastrados.
        # Esse método pode carregar os dados do banco de dados e
        #       exibir as informações na Treeview,
        #       garantindo que a tabela seja preenchida assim
        #       que a tela for carregada.
        self.listar_usuarios()

    def listar_usuarios(self):

        # Remove todos os itens atualmente exibidos na Treeview antes de carregar novos dados.
        # `self.tree_usuarios.get_children()` retorna todos os itens atualmente na tabela.
        # O loop percorre cada item e o remove com `self.tree_usuarios.delete(item)`.
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        # Percorre todos os documentos armazenados na coleção `usuarios_collection` do MongoDB.
        # `usuarios_collection.find()` busca todos os registros da coleção de usuários.
        for u in usuarios_collection.find():

            # Insere um novo item (linha) na Treeview com os dados do
            #       usuário recuperado do banco de dados.
            # `insert("", tk.END, values=(...))` adiciona um novo item ao final da lista.
            # `values=(...)` define os valores exibidos em cada coluna:
            #   - `u.get("login", "")` busca o valor do campo "login", retorna
            #           uma string vazia caso não exista.
            #   - `u.get("senha", "")` busca o valor do campo "senha", retorna
            #           uma string vazia caso não exista.
            #   - `u.get("permissoes", "")` busca o valor do campo "permissoes",
            #           retorna uma string vazia caso não exista.
            #   - `str(u["_id"])` converte o identificador único do usuário (`_id`) para string.
            self.tree_usuarios.insert("",
                                      tk.END,
                                      values=( u.get("login", ""),
                                            u.get("senha", ""),
                                            u.get("permissoes", ""),
                                            str(u["_id"])))

        # Define `self.usuario_em_edicao` como `None`, indicando que
        #       nenhum usuário está sendo editado no momento.
        # Esse atributo pode ser usado para controlar se um usuário está
        #       sendo atualizado ou se um novo será criado.
        self.usuario_em_edicao = None

    def cadastrar_ou_atualizar(self):

        # Obtém o valor do campo de login, removendo espaços em branco
        #       extras no início e no final.
        login_novo = self.login_var.get().strip()

        # Obtém o valor do campo de senha, também removendo
        #       espaços em branco extras.
        senha_nova = self.senha_var.get().strip()

        # Obtém o valor da permissão selecionada no combobox.
        permissao = self.permissoes_var.get()

        # Verifica se os campos obrigatórios 'Login' e 'Senha' foram preenchidos.
        # `if not login_novo or not senha_nova:` verifica se algum dos campos está vazio.
        if not login_novo or not senha_nova:

            # Exibe uma mensagem de erro para o usuário informando
            #       que os campos são obrigatórios.
            messagebox.showerror("Erro",
                                 "Campos 'Login' e 'Senha' são obrigatórios.")

            # Encerra a função, impedindo a continuação do
            #       cadastro ou atualização.
            return

        # Verifica se um usuário está sendo editado.
        # Se `self.usuario_em_edicao` não for `None`, significa que o
        #       usuário já existe e será atualizado.
        if self.usuario_em_edicao:

            # Atualiza os dados do usuário no banco de dados (MongoDB).
            # `usuarios_collection.update_one(...)` atualiza apenas um
            #       registro que corresponda ao filtro.
            usuarios_collection.update_one(
                {"_id": self.usuario_em_edicao},  # Filtro: busca o usuário pelo seu ID único.
                {"$set": {  # Define os novos valores a serem atualizados.
                    "login": login_novo,  # Atualiza o login.
                    "senha": senha_nova,  # Atualiza a senha.
                    "permissoes": permissao  # Atualiza a permissão do usuário.
                }}
            )

            # Exibe uma mensagem informando que o usuário foi atualizado com sucesso.
            messagebox.showinfo("Sucesso",
                                f"Usuário '{login_novo}' atualizado com sucesso!")

        # Se `self.usuario_em_edicao` for `None`, significa que
        #       um novo usuário será cadastrado.
        else:

            # Verifica se já existe um usuário com o mesmo login.
            # `usuarios_collection.find_one({"login": login_novo})`
            #       busca um usuário que tenha o mesmo login.
            if usuarios_collection.find_one({"login": login_novo}):

                # Se o usuário já existir, exibe uma mensagem de
                #       erro e interrompe o processo.
                messagebox.showerror("Erro", "Usuário já existe.")

                # Sai da função sem cadastrar um novo usuário.
                return

            # Insere um novo usuário no banco de dados (MongoDB).
            # `usuarios_collection.insert_one({...})` adiciona um
            #       novo registro à coleção.
            usuarios_collection.insert_one({
                "login": login_novo,  # Define o login do novo usuário.
                "senha": senha_nova,  # Define a senha do novo usuário.
                "permissoes": permissao  # Define a permissão do novo usuário.
            })

            # Exibe uma mensagem informando que o usuário
            #       foi cadastrado com sucesso.
            messagebox.showinfo("Sucesso",
                                f"Usuário '{login_novo}' cadastrado com sucesso!")

        # Após cadastrar ou atualizar o usuário, limpa os
        #       campos do formulário.
        self.limpar_campos()

        # Atualiza a lista de usuários na interface, garantindo que
        #       as alterações sejam refletidas na tela.
        self.listar_usuarios()

    def excluir_usuario(self):

        # Obtém a seleção atual da tabela (Treeview).
        # `self.tree_usuarios.selection()` retorna os itens selecionados na tabela.
        sel = self.tree_usuarios.selection()

        # Verifica se nenhum usuário foi selecionado.
        # `if not sel:` verifica se a seleção está vazia.
        if not sel:

            # Exibe uma mensagem de erro informando que a seleção é
            #       obrigatória para excluir um usuário.
            messagebox.showerror("Erro",
                                 "Selecione um usuário para excluir.")

            # Sai da função, impedindo a exclusão sem uma seleção válida.
            return

        # Obtém os valores do item selecionado na tabela.
        # `self.tree_usuarios.item(sel, "values")` retorna uma tupla
        #       com os valores da linha selecionada.
        valores = self.tree_usuarios.item(sel, "values")

        # Extrai o ID do usuário a partir da posição 3 da
        #       tupla (índice 3 corresponde à coluna "id").
        usuario_id_str = valores[3]

        # Extrai o login do usuário a partir da posição 0 da
        #       tupla (índice 0 corresponde à coluna "login").
        login_str = valores[0]

        # Impede a exclusão do usuário "admin" para evitar a remoção
        #       acidental da conta principal do sistema.
        # `if login_str.lower() == "admin":` verifica se o nome de
        #       usuário é "admin" (ignora maiúsculas/minúsculas).
        if login_str.lower() == "admin":

            # Exibe uma mensagem de erro informando que a exclusão
            #       do usuário "admin" não é permitida.
            messagebox.showerror("Erro",
                                 "Não é permitido excluir o usuário 'admin'.")

            # Sai da função, impedindo a exclusão do usuário "admin".
            return

        # Exibe uma caixa de diálogo perguntando ao usuário se ele
        #       deseja realmente excluir o usuário selecionado.
        # `messagebox.askyesno("Confirmar Exclusão", ...)` cria
        #       uma janela com botões "Sim" e "Não".
        # - O primeiro argumento `"Confirmar Exclusão"` define o
        #       título da janela de confirmação.
        # - O segundo argumento `f"Tem certeza que deseja
        #       excluir '{login_str}'?"` exibe a mensagem personalizada,
        #       onde `login_str` é o nome do usuário selecionado.
        # - A função retorna `True` se o usuário clicar
        #       em "Sim" e `False` se clicar em "Não".
        confirm = messagebox.askyesno("Confirmar Exclusão",
                                      f"Tem certeza que deseja excluir '{login_str}'?")

        # Se o usuário confirmou a exclusão (`confirm == True`), prossegue
        #       com a remoção do usuário do banco de dados.
        if confirm:

            # Exclui o usuário do banco de dados MongoDB usando seu ID único.
            # `usuarios_collection.delete_one({"_id": ObjectId(usuario_id_str)})`
            #       deleta o documento que possui o `_id` correspondente.
            # `ObjectId(usuario_id_str)` converte a string do ID
            #       para um formato reconhecido pelo MongoDB.
            usuarios_collection.delete_one({"_id": ObjectId(usuario_id_str)})

            # Exibe uma mensagem informando que a exclusão foi realizada com sucesso.
            messagebox.showinfo("Sucesso", "Usuário excluído.")

            # Limpa os campos do formulário, garantindo que nenhum
            #       dado do usuário excluído permaneça visível.
            self.limpar_campos()

            # Atualiza a lista de usuários na interface, removendo o
            #       usuário excluído da tabela.
            self.listar_usuarios()

    def selecionar_usuario(self, event):

        # Obtém a seleção atual da tabela (Treeview).
        # `self.tree_usuarios.selection()` retorna uma tupla com os
        #       identificadores dos itens selecionados.
        sel = self.tree_usuarios.selection()

        # Verifica se nenhum usuário foi selecionado.
        # Se `sel` estiver vazio, a função retorna imediatamente,
        #       sem executar o restante do código.
        if not sel:
            return  # Sai da função sem modificar os campos.

        # Obtém os valores da linha selecionada na tabela.
        # `self.tree_usuarios.item(sel, "values")` retorna uma
        #       tupla com os valores da linha correspondente.
        valores = self.tree_usuarios.item(sel, "values")

        # Define o campo de login com o valor selecionado.
        # `self.login_var.set(valores[0])` atribui ao campo de
        #       entrada o login do usuário selecionado.
        self.login_var.set(valores[0])

        # Define o campo de senha com o valor selecionado.
        # `self.senha_var.set(valores[1])` preenche o campo de
        #       senha com a senha do usuário selecionado.
        self.senha_var.set(valores[1])

        # Define o campo de permissão com o valor selecionado.
        # `self.permissoes_var.set(valores[2])` atualiza o combobox
        #       com a permissão do usuário selecionado.
        self.permissoes_var.set(valores[2])

        # Armazena o ID do usuário selecionado para edição.
        # `ObjectId(valores[3])` converte a string do ID para um
        #       formato reconhecido pelo MongoDB.
        # Isso indica que o usuário selecionado está sendo editado.
        self.usuario_em_edicao = ObjectId(valores[3])

    def limpar_campos(self):

        # Limpa o campo de login.
        # `self.login_var.set("")` define o valor da variável como uma string vazia,
        # garantindo que o campo de entrada de login fique em branco.
        self.login_var.set("")

        # Limpa o campo de senha.
        # `self.senha_var.set("")` remove qualquer senha previamente inserida,
        # deixando o campo de entrada vazio.
        self.senha_var.set("")

        # Reseta o campo de permissão para o valor padrão "recepcionista".
        # `self.permissoes_var.set("recepcionista")` define a
        #       permissão padrão para novos cadastros.
        self.permissoes_var.set("recepcionista")

        # Reseta a variável de controle do usuário em edição.
        # `self.usuario_em_edicao = None` indica que nenhum usuário
        #       está sendo editado no momento.
        self.usuario_em_edicao = None

    def voltar_dashboard(self):

        # Oculta a tela atual removendo-a do layout.
        # `self.pack_forget()` remove o frame da interface sem destruí-lo,
        # permitindo que ele possa ser exibido novamente se necessário.
        self.pack_forget()

        # Cria e exibe a tela do Dashboard.
        # `TelaDashboard(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaDashboard`,
        # passando como argumentos:
        # - `self.mestre`: A janela principal onde o Dashboard será exibido.
        # - `self.permissoes_usuario`: Permissões do usuário atual,
        #       garantindo que a nova tela saiba quais funcionalidades
        #       estão disponíveis para ele.
        TelaDashboard(self.mestre, self.permissoes_usuario)



# =============================================================================
# =================== TELA DE RELATÓRIO GERAL (FILTRAGEM) =====================
# =============================================================================
class TelaRelatorioGeral(tk.Frame):

    # Método construtor da classe, inicializa a tela de relatório geral.
    def __init__(self, mestre, permissoes_usuario):

        # Chama o construtor da classe `tk.Frame`, inicializando a interface gráfica.
        # `super().__init__(mestre, bg="#f7f7f7")` define a
        #       cor de fundo como cinza claro.
        super().__init__(mestre, bg="#f7f7f7")

        # Armazena a referência da janela principal (mestre)
        #       para futuras interações.
        self.mestre = mestre

        # Armazena as permissões do usuário, podendo ser utilizadas
        #       para restringir ações na interface.
        self.permissoes_usuario = permissoes_usuario

        # Expande a tela para ocupar todo o espaço disponível
        #       dentro da janela principal.
        # `self.pack(fill="both", expand=True)` garante que o
        #       frame se ajuste ao tamanho da janela.
        self.pack(fill="both", expand=True)

        # Cria um rótulo (label) para exibir o título da tela de Relatório Geral.
        # `text="Relatório Geral"` define o texto exibido no rótulo.
        # `font=("Helvetica", 16, "bold")` define a fonte como
        #       Helvetica, tamanho 16, e em negrito.
        # `bg="#f7f7f7"` define a cor de fundo como um cinza claro (#f7f7f7).
        lbl_titulo = tk.Label(self,
                              text="Relatório Geral",
                              font=("Helvetica", 16, "bold"),
                              bg="#f7f7f7")

        # Posiciona o título na interface.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       para melhor organização visual.
        lbl_titulo.pack(pady=10)

        # Cria um frame (container) para organizar os filtros ou opções no topo da tela.
        # `ttk.Frame(self)` define que o frame será filho do frame principal da tela.
        frame_top = ttk.Frame(self)

        # Posiciona o frame na interface.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels entre elementos.
        # `padx=20` adiciona um espaçamento horizontal de 20 pixels nas laterais.
        frame_top.pack(pady=5, padx=20)

        # Cria um rótulo que informa ao usuário a necessidade de selecionar uma entidade.
        # `text="Selecione a Entidade:"` define o texto que será exibido no rótulo.
        # `frame_top` define o local onde esse rótulo será posicionado,
        #       neste caso, dentro do frame superior.
        # `grid(row=0, column=0, padx=5, pady=5, sticky="e")` define a
        #       posição do rótulo na grade da interface.
        # - `row=0`: o rótulo será posicionado na primeira linha.
        # - `column=0`: o rótulo será posicionado na primeira coluna.
        # - `padx=5, pady=5`: adiciona um espaçamento de 5 pixels horizontal e
        #       verticalmente para melhor espaçamento.
        # - `sticky="e"`: alinha o rótulo à direita (east) da célula onde está posicionado.
        ttk.Label(frame_top,
                  text="Selecione a Entidade:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria uma variável do tipo `StringVar()` que armazenará o
        #       valor selecionado pelo usuário.
        # `self.entidade_var` será usada para capturar a entidade
        #       escolhida e pode ser usada em outras partes do código.
        # Essa variável permite que a interface reaja automaticamente
        #       quando o usuário altera sua seleção.
        self.entidade_var = tk.StringVar()

        # Cria um campo de seleção do tipo Combobox para permitir
        #       que o usuário escolha uma entidade.
        # `frame_top` define que esse Combobox será inserido no frame superior da interface.
        # `textvariable=self.entidade_var` associa a variável `self.entidade_var` ao Combobox,
        # permitindo que a seleção do usuário seja armazenada e utilizada posteriormente.
        # `values=["Reservas", "Produtos", "Hóspedes", "Quartos"]`
        #       define as opções disponíveis para seleção.
        # `state="readonly"` impede que o usuário digite valores
        #       manualmente, limitando-se às opções disponíveis.
        # `width=20` define a largura do Combobox para garantir
        #       que o texto fique legível e bem formatado.
        self.combo_entidade = ttk.Combobox(frame_top,
                                           textvariable=self.entidade_var,
                                           values=["Reservas", "Produtos", "Hóspedes", "Quartos"],
                                           state="readonly",
                                           width=20)

        # Define a posição do Combobox na grade da interface.
        # `row=0, column=1` posiciona o Combobox na primeira
        #       linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels ao
        #       redor do Combobox para melhorar a organização visual.
        self.combo_entidade.grid(row=0, column=1, padx=5, pady=5)

        # Adiciona um evento para detectar quando o usuário seleciona uma opção no Combobox.
        # `bind("<<ComboboxSelected>>", self.carregar_dados)`
        #       faz com que, ao selecionar uma opção, a função `self.carregar_dados`
        #       seja chamada automaticamente para atualizar os dados exibidos na interface.
        self.combo_entidade.bind("<<ComboboxSelected>>", self.carregar_dados)

        # Frames de filtros
        # Cria um frame para os filtros da primeira linha.
        # `self` define que o frame será um componente interno da interface principal.
        # `ttk.Frame(self)` cria um contêiner que pode conter
        #       outros elementos da interface.
        self.frame_filtros_linha1 = ttk.Frame(self)

        # Posiciona o frame na interface.
        # `padx=5, pady=3` adiciona um pequeno espaçamento
        #       horizontal (5 pixels) e vertical (3 pixels)
        #       para manter um layout mais organizado.
        self.frame_filtros_linha1.pack(padx=5, pady=3)

        # Cria um segundo frame para filtros adicionais.
        # Esse frame pode ser usado para distribuir os filtros em duas
        #       linhas para melhor organização visual.
        self.frame_filtros_linha2 = ttk.Frame(self)

        # Posiciona o segundo frame logo abaixo do primeiro.
        # Também recebe `padx=5, pady=3` para manter o espaçamento uniforme.
        self.frame_filtros_linha2.pack(padx=5, pady=3)

        # Cria um frame dedicado aos botões da interface.
        # Esse contêiner mantém os botões organizados e
        #       alinhados na interface gráfica.
        frame_botoes = ttk.Frame(self)

        # Posiciona o frame na interface principal.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels para
        #       separar os botões dos outros elementos.
        # `padx=20` aumenta o espaçamento horizontal para um melhor
        #       alinhamento e estética da interface.
        frame_botoes.pack(pady=5, padx=20)

        # Cria um botão para aplicar os filtros selecionados na interface.
        # `text="Aplicar Filtros"` define o texto exibido no botão.
        # `command=self.aplicar_filtros` associa a ação de
        #       chamar o método `aplicar_filtros`
        #       quando o botão for pressionado.
        btn_filtrar = ttk.Button(frame_botoes,
                                 text="Aplicar Filtros",
                                 command=self.aplicar_filtros)

        # Posiciona o botão dentro do frame de botões.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um pequeno espaçamento horizontal entre os botões.
        btn_filtrar.pack(side="left", padx=5)

        # Cria um botão para exportar os dados filtrados para um arquivo Excel.
        # `text="Exportar Excel"` define o rótulo exibido no botão.
        # `command=self.exportar_excel` define que, ao ser pressionado,
        # o botão chamará o método `exportar_excel` para gerar o arquivo.
        btn_exportar = ttk.Button(frame_botoes,
                                  text="Exportar Excel",
                                  command=self.exportar_excel)

        # Posiciona o botão dentro do frame de botões.
        # `side="left"` mantém o alinhamento com os outros botões à esquerda.
        # `padx=5` adiciona um pequeno espaçamento horizontal
        #       entre os botões para melhor organização.
        btn_exportar.pack(side="left", padx=5)

        # Cria um rótulo (label) para exibir um resumo dos dados filtrados.
        # `text=""` define inicialmente um texto vazio, que
        #       será atualizado dinamicamente.
        # `font=("Helvetica", 10, "bold")` define a fonte do texto
        #       como Helvetica, tamanho 10, e negrito.
        # `bg="#f7f7f7"` define o fundo do rótulo na cor
        #       cinza claro (#f7f7f7) para manter a harmonia visual da interface.
        self.lbl_resumo = tk.Label(frame_botoes,
                                   text="",
                                   font=("Helvetica", 10, "bold"),
                                   bg="#f7f7f7")

        # Posiciona o rótulo dentro do frame de botões.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=20` adiciona um espaçamento horizontal para evitar que o
        #       rótulo fique muito próximo dos botões.
        self.lbl_resumo.pack(side="left", padx=20)

        # Cria uma Treeview para exibir os dados do relatório de forma tabular.
        # `show="headings"` oculta a primeira coluna padrão da Treeview e
        #       exibe apenas os cabeçalhos das colunas definidas posteriormente.
        self.tree_relatorio = ttk.Treeview(self, show="headings")

        # Posiciona a Treeview na interface, permitindo que ela
        #       ocupe todo o espaço disponível.
        # `fill="both"` expande a tabela tanto horizontal quanto
        #       verticalmente para preencher o espaço do frame pai.
        # `expand=True` permite que a Treeview cresça quando a
        #       janela for redimensionada.
        # `padx=10, pady=10` adiciona espaçamento ao redor da
        #       tabela para melhor visualização.
        self.tree_relatorio.pack(fill="both",
                                 expand=True,
                                 padx=10,
                                 pady=10)

        # Associa um evento de duplo clique à Treeview.
        # `"<Double-1>"` significa que a ação será ativada quando o usuário
        #       der um duplo clique com o botão esquerdo do mouse em uma linha da tabela.
        # `self.duplo_clique_reserva` é o método que será chamado
        #       quando o evento ocorrer.
        self.tree_relatorio.bind("<Double-1>", self.duplo_clique_reserva)

        # Cria um botão para voltar ao Dashboard.
        # `text="Voltar ao Dashboard"` define o texto exibido no botão.
        # `command=self.voltar_dashboard` associa a ação de voltar ao
        #       Dashboard ao clicar no botão.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do
        #       botão para uma melhor disposição na interface.
        btn_voltar = ttk.Button(self, text="Voltar ao Dashboard", command=self.voltar_dashboard)
        btn_voltar.pack(pady=10)

        # Inicializa uma lista vazia para armazenar os
        #       nomes das colunas do relatório.
        self.colunas = []

        # Inicializa uma lista vazia para armazenar os dados
        #       carregados no relatório.
        self.dados = []

        # Dicionário que armazenará os filtros de texto
        #       aplicados nas colunas do relatório.
        self.filtros_text = {}

        # Variáveis para armazenar as datas de filtro "De" e "Até".
        self.data_de_var = None
        self.data_ate_var = None

        # Campos de entrada para permitir a inserção
        #       manual das datas nos filtros.
        self.data_de_entry = None
        self.data_ate_entry = None

        # Define a entidade padrão para exibição no relatório.
        # A entidade representa o conjunto de dados que será exibido
        #       na tabela (por exemplo, "Reservas", "Produtos", "Hóspedes", etc.).
        self.entidade_var.set("Reservas")

        # Chama a função `carregar_dados` para preencher os dados
        #       iniciais com base na entidade padrão ("Reservas").
        self.carregar_dados()


    # Carrega os dados para o relatório, ajustando a
    #       exibição com base na entidade selecionada.
    def carregar_dados(self, event=None):

        # Remove todas as linhas existentes na Treeview para
        #       evitar sobreposição de dados.
        self.tree_relatorio.delete(*self.tree_relatorio.get_children())

        # Limpa a lista de colunas para garantir que novas colunas
        #       possam ser definidas corretamente.
        self.colunas.clear()

        # Limpa a lista de dados para garantir que os novos
        #       registros sejam carregados corretamente.
        self.dados.clear()

        # Percorre todos os widgets (elementos gráficos) do
        #       primeiro painel de filtros e os remove.
        # Isso garante que os novos filtros sejam corretamente
        #       adicionados sem repetição.
        for w in self.frame_filtros_linha1.winfo_children():
            w.destroy()

        # Percorre todos os widgets do segundo painel de filtros e os remove.
        # Isso evita que filtros antigos permaneçam na interface ao mudar de entidade.
        for w in self.frame_filtros_linha2.winfo_children():
            w.destroy()

        # Dicionário que armazena os filtros inseridos pelo
        #       usuário, será redefinido.
        self.filtros_text.clear()

        # As variáveis de data (início e fim) são reiniciadas para
        #       evitar interferências com novos carregamentos.
        self.data_de_var = None
        self.data_ate_var = None

        # Os campos de entrada de data são redefinidos para que possam
        #       ser recriados corretamente ao carregar filtros.
        self.data_de_entry = None
        self.data_ate_entry = None

        # Obtém a entidade selecionada no combobox para definir
        #       quais dados devem ser carregados.
        # Essa entidade pode ser "Reservas", "Produtos", "Hóspedes" ou "Quartos".
        entidade = self.entidade_var.get()

        # Se a entidade selecionada for "Reservas",
        #       carregamos os dados das reservas.
        if entidade == "Reservas":

            # Define as colunas que serão exibidas no relatório de reservas.
            self.colunas = ["Quarto", "Hóspedes", "Valor Final", "Status", "Data Início", "Data Fim", "ID(oculto)"]

            # Configura a Treeview para utilizar essas
            #       colunas na exibição dos dados.
            self.tree_relatorio["columns"] = self.colunas

            # Define o cabeçalho para cada coluna da Treeview
            #       com os nomes definidos acima.
            for col in self.colunas:
                self.tree_relatorio.heading(col, text=col)

            # Percorre todas as reservas armazenadas no banco de
            #       dados e adiciona os dados ao relatório.
            for r in reservas_collection.find():

                # Monta a linha de dados com as informações da reserva atual.
                linha = [
                    r.get("numero_quarto", ""),  # Número do quarto reservado.
                    ", ".join(r.get("hospedes", [])),  # Lista de hóspedes separados por vírgula.
                    r.get("valor_final", 0.0),  # Valor total da reserva.
                    r.get("status", ""),  # Status da reserva (Aberta, Finalizada, etc.).
                    r.get("data_inicio", ""),  # Data de início da reserva.
                    r.get("data_fim", ""),  # Data de fim da reserva.
                    str(r["_id"])  # ID da reserva (campo oculto para identificação).
                ]

                # Adiciona a linha montada na lista de dados
                #       que será exibida na interface.
                self.dados.append(linha)

            # Filtros de texto
            # Cria um rótulo (Label) para indicar o campo de filtro "Quarto".
            # `text="Quarto:"` define o texto exibido no rótulo.
            # O rótulo será inserido na interface para identificação do campo de filtro.
            lbl_q = ttk.Label(self.frame_filtros_linha1, text="Quarto:")

            # Exibe o rótulo na interface, dentro do frame de filtros.
            # `side="left"` alinha o rótulo à esquerda dentro do frame.
            # `padx=3` adiciona um pequeno espaçamento lateral de 3 pixels.
            lbl_q.pack(side="left", padx=3)

            # Cria uma variável de controle do tipo StringVar para
            #       armazenar o valor digitado no campo de filtro.
            # Essa variável será usada para recuperar e aplicar o
            #       filtro digitado pelo usuário.
            self.filtros_text["Quarto"] = tk.StringVar()

            # Cria um campo de entrada de texto (Entry) para o filtro de "Quarto".
            # `textvariable=self.filtros_text["Quarto"]` vincula o campo à
            #       variável de controle, armazenando o valor digitado pelo usuário.
            # `width=12` define a largura do campo em 12 caracteres.
            ent_q = ttk.Entry(self.frame_filtros_linha1,
                              textvariable=self.filtros_text["Quarto"],
                              width=12)

            # Exibe o campo de entrada na interface, dentro do frame de filtros.
            # `side="left"` alinha o campo à esquerda dentro do frame.
            # `padx=5` adiciona um pequeno espaçamento lateral de 5 pixels.
            ent_q.pack(side="left", padx=5)

            # Cria um rótulo (Label) para indicar o campo de filtro "Hóspedes".
            # `text="Hóspedes:"` define o texto exibido no rótulo.
            # O rótulo será inserido na interface para identificação do campo de filtro.
            lbl_h = ttk.Label(self.frame_filtros_linha1, text="Hóspedes:")

            # Exibe o rótulo na interface, dentro do frame de filtros.
            # `side="left"` alinha o rótulo à esquerda dentro do frame.
            # `padx=3` adiciona um pequeno espaçamento lateral de 3 pixels.
            lbl_h.pack(side="left", padx=3)

            # Cria uma variável de controle do tipo StringVar para
            #       armazenar o valor digitado no campo de filtro "Hóspedes".
            # Essa variável permite que o valor seja recuperado e
            #       utilizado para filtragem posteriormente.
            self.filtros_text["Hóspedes"] = tk.StringVar()

            # Cria um campo de entrada de texto (Entry)
            #       para o filtro de "Hóspedes".
            # `textvariable=self.filtros_text["Hóspedes"]` vincula o
            #       campo à variável de controle, armazenando o valor
            #       digitado pelo usuário.
            # `width=12` define a largura do campo em 12 caracteres.
            ent_h = ttk.Entry(self.frame_filtros_linha1,
                              textvariable=self.filtros_text["Hóspedes"],
                              width=12)

            # Exibe o campo de entrada na interface, dentro do frame de filtros.
            # `side="left"` alinha o campo à esquerda dentro do frame.
            # `padx=5` adiciona um pequeno espaçamento lateral de 5 pixels.
            ent_h.pack(side="left", padx=5)

            # Cria um rótulo (Label) para identificar o campo de filtro "Status".
            # O rótulo será exibido dentro do frame de filtros da primeira linha.
            lbl_s = ttk.Label(self.frame_filtros_linha1, text="Status:")

            # Exibe o rótulo na interface.
            # `side="left"` alinha o rótulo à esquerda dentro do frame.
            # `padx=3` adiciona um pequeno espaçamento lateral
            #       de 3 pixels para separar do próximo elemento.
            lbl_s.pack(side="left", padx=3)

            # Cria uma variável de controle do tipo StringVar para
            #       armazenar o valor digitado no campo de filtro "Status".
            # Essa variável será utilizada posteriormente para
            #       aplicar os filtros na exibição dos dados.
            self.filtros_text["Status"] = tk.StringVar()

            # Cria um campo de entrada (Entry) para permitir que o
            #       usuário digite um valor para o filtro "Status".
            # Esse campo estará vinculado à variável `self.filtros_text["Status"]`,
            #       que armazenará o valor digitado.
            ent_s = ttk.Entry(self.frame_filtros_linha1,
                              textvariable=self.filtros_text["Status"],
                              width=12)

            # Exibe o campo de entrada na interface dentro do
            #       frame de filtros da primeira linha.
            # `side="left"` alinha o campo de entrada à esquerda.
            # `padx=5` adiciona um espaçamento lateral de 5 pixels
            #       para melhor organização visual.
            ent_s.pack(side="left", padx=5)

            # Cria um rótulo (Label) para identificar o campo de filtro "Valor Final".
            # Esse rótulo será exibido ao lado do campo de entrada correspondente.
            lbl_v = ttk.Label(self.frame_filtros_linha1, text="Valor Final:")

            # Exibe o rótulo na interface dentro do frame de filtros da primeira linha.
            # `side="left"` alinha o rótulo à esquerda.
            # `padx=3` adiciona um pequeno espaçamento lateral
            #       de 3 pixels para separar do próximo elemento.
            lbl_v.pack(side="left", padx=3)

            # Cria uma variável do tipo StringVar para armazenar o
            #       valor digitado no campo de filtro "Valor Final".
            # Essa variável permite a manipulação dinâmica do
            #       valor digitado no campo de entrada.
            self.filtros_text["Valor Final"] = tk.StringVar()

            # Cria um campo de entrada (Entry) onde o usuário poderá
            #       digitar um valor para o filtro "Valor Final".
            # Esse campo está vinculado à variável `self.filtros_text["Valor Final"]`,
            #       garantindo que o valor digitado possa ser recuperado posteriormente.
            # `width=10` define a largura do campo de entrada para
            #       comportar valores numéricos.
            ent_v = ttk.Entry(self.frame_filtros_linha1,
                              textvariable=self.filtros_text["Valor Final"],
                              width=10)

            # Exibe o campo de entrada na interface dentro do
            #       frame de filtros da primeira linha.
            # `side="left"` alinha o campo de entrada à esquerda.
            # `padx=5` adiciona um espaçamento lateral de 5 pixels
            #       para melhor organização visual.
            ent_v.pack(side="left", padx=5)

            # Filtros de data (opcional)
            # Cria um rótulo (Label) para indicar o filtro de
            #       período de data na segunda linha de filtros.
            # O rótulo exibirá o texto "Filtrar Período:", ajudando o
            #       usuário a entender a função do filtro.
            lbl_data = ttk.Label(self.frame_filtros_linha2,
                                 text="Filtrar Período:")

            # Posiciona o rótulo dentro do frame de filtros da segunda linha.
            # `side="left"` alinha o rótulo à esquerda dentro do frame.
            # `padx=3` adiciona um pequeno espaçamento lateral
            #       de 3 pixels para melhorar a organização visual.
            lbl_data.pack(side="left", padx=3)

            # Verifica se a biblioteca `tkcalendar` está instalada e sendo utilizada.
            # Isso permite que os widgets de seleção de data sejam criados corretamente.
            if USANDO_TKCALENDAR:

                # Cria uma variável de controle para armazenar a data inicial do filtro.
                self.data_de_var = tk.StringVar()

                # Cria uma variável de controle para armazenar a data final do filtro.
                self.data_ate_var = tk.StringVar()

                # Cria um campo de seleção de data (`DateEntry`) para a data inicial.
                # `self.frame_filtros_linha2` define onde o widget será posicionado.
                # `textvariable=self.data_de_var` associa a variável ao campo.
                # `date_pattern="yyyy-MM-dd"` define o formato da data como "Ano-Mês-Dia".
                # `width=10` especifica a largura do campo em caracteres.
                self.data_de_entry = DateEntry(self.frame_filtros_linha2,
                                               textvariable=self.data_de_var,
                                               date_pattern="yyyy-MM-dd",
                                               width=10)

                # Posiciona o campo de entrada de data inicial dentro do
                #       frame de filtros da segunda linha.
                # `side="left"` alinha o widget à esquerda dentro do frame.
                # `padx=5` adiciona um pequeno espaçamento lateral de 5 pixels
                #       para melhor organização visual.
                self.data_de_entry.pack(side="left", padx=5)

                # Cria um campo de seleção de data (`DateEntry`) para a data final.
                # Funciona da mesma forma que o campo anterior, mas
                #       vinculado à variável `self.data_ate_var`.
                self.data_ate_entry = DateEntry(self.frame_filtros_linha2,
                                                textvariable=self.data_ate_var,
                                                date_pattern="yyyy-MM-dd",
                                                width=10)

                # Posiciona o campo de entrada de data final dentro do
                #       frame de filtros da segunda linha.
                # As configurações são idênticas ao campo de data inicial.
                self.data_ate_entry.pack(side="left", padx=5)

            # Caso `tkcalendar` não esteja instalado ou ativado,
            #       exibe um aviso informando ao usuário.
            else:

                # Cria um rótulo (Label) que exibe o texto "tkcalendar não instalado".
                # Isso informa ao usuário que o recurso de calendário não está disponível.
                ttk.Label(self.frame_filtros_linha2,
                          text="tkcalendar não instalado").pack(side="left")


        # Verifica se a entidade selecionada é "Produtos".
        # Caso seja, define as colunas específicas para
        #       exibir informações sobre produtos.
        elif entidade == "Produtos":

            # Define a lista de colunas para o relatório de produtos.
            # Cada item da lista representa um campo que será exibido na tabela.
            self.colunas = ["Nome", "Descrição", "Preço", "Qtd", "Categoria"]

            # Configura as colunas da `Treeview` (tabela) com
            #       base na lista de colunas definida.
            self.tree_relatorio["columns"] = self.colunas

            # Percorre a lista de colunas e define o cabeçalho de cada uma na interface.
            # Isso permite que os títulos das colunas fiquem visíveis para o usuário.
            for col in self.colunas:
                self.tree_relatorio.heading(col, text=col)

            # Percorre todos os documentos da coleção de produtos no banco de dados.
            # Cada documento representa um produto cadastrado no sistema.
            for p in produtos_collection.find():

                # Cria uma lista `linha` contendo os valores
                #       extraídos do documento do banco de dados.
                # Utiliza `.get()` para evitar erros caso alguma
                #       chave não exista no documento.
                linha = [
                    p.get("nome", ""),  # Obtém o nome do produto. Se não existir, retorna uma string vazia.
                    p.get("descricao", ""),
                    # Obtém a descrição do produto. Se não existir, retorna uma string vazia.
                    p.get("preco", 0.0),  # Obtém o preço do produto. Se não existir, assume o valor 0.0.
                    p.get("quantidade", 0),  # Obtém a quantidade em estoque. Se não existir, assume 0.
                    p.get("categoria", "")
                    # Obtém a categoria do produto. Se não existir, retorna uma string vazia.
                ]

                # Adiciona a linha processada à lista `self.dados`, que
                #       contém todos os registros carregados.
                self.dados.append(linha)

            # Percorre a lista de colunas disponíveis no relatório atual.
            # Para cada coluna, será criado um campo de filtro correspondente na interface.
            for col in self.colunas:

                # Cria um rótulo (`Label`) para indicar qual campo está sendo filtrado.
                # O texto do rótulo é definido dinamicamente com base no nome da coluna.
                lbl = ttk.Label(self.frame_filtros_linha1, text=f"{col}:")

                # Adiciona o rótulo à interface, posicionando-o à esquerda
                #       com espaçamento horizontal de 3 pixels.
                lbl.pack(side="left", padx=3)

                # Cria uma variável de texto (`StringVar`) associada ao campo de filtro da coluna.
                # Essa variável armazenará o valor digitado pelo usuário.
                self.filtros_text[col] = tk.StringVar()

                # Cria um campo de entrada (`Entry`) para permitir que o usuário
                #       insira um valor para filtrar a coluna correspondente.
                # O campo de entrada está vinculado à variável `StringVar`,
                #       garantindo que o valor digitado possa ser recuperado dinamicamente.
                ent = ttk.Entry(self.frame_filtros_linha1,
                                textvariable=self.filtros_text[col],
                                width=12)

                # Adiciona o campo de entrada à interface, posicionando-o à
                #       esquerda com espaçamento horizontal de 5 pixels.
                ent.pack(side="left", padx=5)


        # Verifica se a entidade selecionada é "Hóspedes".
        elif entidade == "Hóspedes":

            # Define a lista de colunas que serão exibidas na tabela do relatório.
            # Estas colunas correspondem aos dados principais dos hóspedes cadastrados.
            self.colunas = ["Nome", "CPF", "Telefone", "Email", "Endereço"]

            # Atualiza as colunas da `Treeview` para refletir os dados dos hóspedes.
            self.tree_relatorio["columns"] = self.colunas

            # Para cada coluna definida, cria um cabeçalho correspondente na tabela.
            # O cabeçalho é exibido na interface para indicar o
            #       tipo de dado contido na coluna.
            for col in self.colunas:
                self.tree_relatorio.heading(col, text=col)

            # Percorre todos os registros da coleção `hospedes_collection` no banco de dados.
            # Cada registro representa um hóspede e será transformado em uma linha da tabela.
            for h in hospedes_collection.find():

                # Obtém os dados do hóspede atual e armazena em uma lista chamada `linha`.
                # Cada posição da lista corresponde a um campo da tabela (Nome, CPF, etc.).
                linha = [
                    h.get("nome", ""),  # Obtém o nome do hóspede ou retorna uma string vazia se não existir.
                    h.get("cpf", ""),  # Obtém o CPF do hóspede ou retorna uma string vazia se não existir.
                    h.get("telefone", ""),
                    # Obtém o telefone do hóspede ou retorna uma string vazia se não existir.
                    h.get("email", ""),  # Obtém o email do hóspede ou retorna uma string vazia se não existir.
                    h.get("endereco", "")  # Obtém o endereço do hóspede ou retorna uma string vazia se não existir.
                ]

                # Adiciona a linha contendo os dados do hóspede à lista `self.dados`.
                # Esta lista será posteriormente utilizada para popular a `Treeview`.
                self.dados.append(linha)

            # Percorre todas as colunas definidas para a entidade selecionada.
            # O objetivo é criar um campo de filtro para cada uma delas.
            for col in self.colunas:

                # Cria um rótulo (`Label`) para indicar qual é o
                #       campo de filtro correspondente.
                # O texto exibido no rótulo será o nome da coluna atual.
                lbl = ttk.Label(self.frame_filtros_linha1, text=f"{col}:")

                # Define a posição do rótulo dentro do frame de filtros da primeira linha.
                # O `side="left"` alinha os elementos à esquerda e `padx=3`
                #       adiciona um espaçamento lateral.
                lbl.pack(side="left", padx=3)

                # Cria uma variável de texto para armazenar o valor do
                #       filtro correspondente à coluna.
                # Essa variável será usada para capturar e armazenar o
                #       que o usuário digitar no campo de entrada.
                self.filtros_text[col] = tk.StringVar()

                # Cria um campo de entrada (`Entry`) associado à
                #       variável `self.filtros_text[col]`.
                # O usuário poderá digitar um valor neste campo para
                #       filtrar os dados exibidos na tabela.
                ent = ttk.Entry(self.frame_filtros_linha1,
                                textvariable=self.filtros_text[col],
                                width=12)

                # Define a posição do campo de entrada dentro do
                #       frame de filtros da primeira linha.
                # O `side="left"` alinha os elementos à esquerda e
                #       `padx=5` adiciona um espaçamento lateral.
                ent.pack(side="left", padx=5)


        # Verifica se a entidade selecionada é "Quartos".
        # Caso seja, define as colunas específicas para exibição na tabela.
        elif entidade == "Quartos":

            # Define os nomes das colunas que serão exibidas na Treeview.
            self.colunas = ["Número", "Tipo", "Capacidade", "Preço Base", "Status"]

            # Configura a Treeview para utilizar as colunas definidas acima.
            self.tree_relatorio["columns"] = self.colunas

            # Percorre cada coluna e define o nome que será
            #       exibido no cabeçalho da tabela.
            for col in self.colunas:
                self.tree_relatorio.heading(col, text=col)

            # Faz uma busca na coleção `quartos_collection` para
            #       recuperar todos os quartos cadastrados.
            for q in quartos_collection.find():

                # Para cada quarto encontrado no banco de dados, extrai os
                #       dados e armazena em uma lista.
                linha = [
                    q.get("numero_quarto", ""),  # Obtém o número do quarto, ou uma string vazia caso não exista.
                    q.get("tipo", ""),  # Obtém o tipo do quarto, como "Luxo", "Standard", etc.
                    q.get("capacidade", 0),  # Obtém a capacidade máxima de hóspedes no quarto.
                    q.get("preco_diaria", 0.0),  # Obtém o preço base da diária do quarto.
                    q.get("status", "")  # Obtém o status do quarto (ex.: "Disponível", "Ocupado").
                ]

                # Adiciona a linha com os dados do quarto à lista `self.dados`,
                #       que será usada para preencher a tabela.
                self.dados.append(linha)

            # Percorre todas as colunas definidas para a entidade selecionada.
            for col in self.colunas:

                # Cria um rótulo (Label) para cada coluna, que será
                #       exibido acima do campo de entrada do filtro.
                lbl = ttk.Label(self.frame_filtros_linha1, text=f"{col}:")

                # Adiciona o rótulo à interface gráfica, posicionando-o ao
                #       lado esquerdo e com espaçamento lateral.
                lbl.pack(side="left", padx=3)

                # Cria uma variável do tipo StringVar para armazenar os
                #       valores digitados no campo de filtro.
                self.filtros_text[col] = tk.StringVar()

                # Cria um campo de entrada (Entry) para permitir que o
                #       usuário insira um filtro para a coluna correspondente.
                ent = ttk.Entry(self.frame_filtros_linha1,
                                textvariable=self.filtros_text[col],
                                width=12)

                # Adiciona o campo de entrada à interface gráfica,
                #       posicionando-o ao lado esquerdo com espaçamento lateral.
                ent.pack(side="left", padx=5)


        # Após criar os filtros, chama o método para reinserir os
        #       dados na tabela, já filtrados conforme os critérios aplicados.
        self.reinserir_dados_filtrados(self.dados)



    def reinserir_dados_filtrados(self, lista):

        # Remove todas as linhas existentes da Treeview
        #       para inserir os dados filtrados.
        self.tree_relatorio.delete(*self.tree_relatorio.get_children())

        # Percorre a lista filtrada e insere cada linha na Treeview.
        for lin in lista:
            self.tree_relatorio.insert("", tk.END, values=lin)

        # Conta a quantidade total de registros filtrados.
        qtd = len(lista)

        # Verifica se a coluna "Valor Final" está presente na entidade exibida.
        if "Valor Final" in self.colunas:

            # Obtém o índice da coluna "Valor Final" dentro da lista de colunas.
            idx_val = self.colunas.index("Valor Final")

            # Inicializa a variável para armazenar a soma dos valores finais.
            soma_valor = 0.0

            # Percorre todas as linhas filtradas para somar os
            #       valores da coluna "Valor Final".
            for lin in lista:

                try:

                    # Converte o valor para float e adiciona à soma.
                    soma_valor += float(lin[idx_val])

                except:

                    # Se houver erro na conversão, ignora e mantém o valor acumulado.
                    pass

            # Atualiza o rótulo de resumo exibindo a quantidade de
            #       registros e o valor total formatado.
            self.lbl_resumo.config(text=f"Quantidade: {qtd} | Valor Total: R$ {soma_valor:.2f}")

        # Se a coluna "Valor Final" não existir, exibe apenas a
        #       quantidade de registros filtrados.
        else:
            self.lbl_resumo.config(text=f"Quantidade: {qtd}")


    # Define a função responsável por aplicar os filtros ao relatório.
    def aplicar_filtros(self):

        # Obtém a entidade selecionada no ComboBox (por exemplo,
        #       "Reservas", "Produtos", etc.)
        entidade = self.entidade_var.get()

        # Cria uma lista vazia para armazenar os resultados filtrados
        resultados = []

        # Inicializa as variáveis que armazenarão as datas de
        #       início e fim do filtro como None
        dt_de = dt_ate = None

        # Verifica se a entidade selecionada é "Reservas" e se o
        #       suporte ao tkcalendar está ativado.
        # Também checa se os campos de entrada de data ("De" e "Até")
        #       existem na interface.
        if entidade == "Reservas" and USANDO_TKCALENDAR and self.data_de_entry and self.data_ate_entry:

            # Obtém o valor digitado pelo usuário no campo "Data De" e
            #       remove espaços extras ao redor
            dt_de_str = self.data_de_var.get().strip()

            # Obtém o valor digitado pelo usuário no campo "Data Até" e
            #       remove espaços extras ao redor
            dt_ate_str = self.data_ate_var.get().strip()

            # Verifica se o usuário digitou alguma coisa no campo "Data De"
            if dt_de_str:

                try:

                    # Converte a string da data para um objeto de data do Python no formato "YYYY-MM-DD"
                    dt_de = datetime.datetime.strptime(dt_de_str, "%Y-%m-%d")

                except ValueError:

                    # Se a conversão falhar (por exemplo, se a data estiver em um
                    #       formato inválido), define como None
                    dt_de = None

            # Verifica se o usuário digitou alguma coisa no campo "Data Até"
            if dt_ate_str:

                try:

                    # Converte a string da data para um objeto de data
                    #       do Python no formato "YYYY-MM-DD"
                    dt_ate = datetime.datetime.strptime(dt_ate_str, "%Y-%m-%d")

                except ValueError:

                    # Se a conversão falhar, define a variável como
                    #       None para evitar erros
                    dt_ate = None

        # Percorre os dados e aplica os filtros
        # Percorre cada linha da lista `self.dados`, que contém todas as
        #       informações carregadas no relatório
        for linha in self.dados:

            # Assume que a linha deve ser incluída nos resultados filtrados
            # Caso algum filtro não seja atendido, essa variável será
            #       alterada para `False`
            incluir = True

            # Percorre todos os filtros de texto aplicados, ou seja, os
            #       campos de pesquisa digitados pelo usuário
            for chave, var in self.filtros_text.items():

                # Obtém o valor digitado pelo usuário no campo de filtro correspondente à `chave`
                # `.strip()` remove espaços extras no início e no fim
                # `.lower()` converte tudo para letras minúsculas para evitar
                #       problemas com maiúsculas/minúsculas
                filtro_valor = var.get().strip().lower()

                # Se o usuário digitou algo no filtro (se o campo não estiver vazio)
                if filtro_valor:

                    # Obtém o dado correspondente da linha na coluna especificada pela `chave`
                    # `self.colunas.index(chave)` encontra a posição da coluna na lista de colunas
                    # `.strip().lower()` garante que a comparação ignore espaços extras e
                    #       diferenças entre maiúsculas/minúsculas
                    dado_linha = str(linha[self.colunas.index(chave)]).strip().lower()

                    # Verifica se o valor digitado pelo usuário **não está contido** no dado da linha
                    # Isso significa que a linha **não atende** ao filtro e deve ser excluída
                    if filtro_valor not in dado_linha:

                        # Marca a linha como **não incluída**
                        incluir = False

                        # Sai do loop imediatamente para evitar verificações desnecessárias
                        break

            # Filtragem por data (aplicado apenas a "Reservas")
            # Verifica se a entidade selecionada é "Reservas" e se pelo menos
            #       uma das datas do filtro foi preenchida
            if entidade == "Reservas" and (dt_de or dt_ate):

                try:

                    # Obtém a data de início da reserva a partir da coluna correspondente
                    # Usa `strptime` para converter a string da data para um objeto `datetime`
                    data_inicio = datetime.datetime.strptime(linha[self.colunas.index("Data Início")], "%Y-%m-%d")

                    # Obtém a data de fim da reserva e converte para um objeto `datetime`
                    data_fim = datetime.datetime.strptime(linha[self.colunas.index("Data Fim")], "%Y-%m-%d")

                except ValueError:

                    # Se houver erro ao converter a data, a linha é
                    #       considerada inválida e não será incluída
                    incluir = False

                # Se a data de início do filtro foi preenchida e a reserva
                #       termina antes dela, a linha é excluída
                if dt_de and data_fim < dt_de:
                    incluir = False

                # Se a data de fim do filtro foi preenchida e a reserva
                #       começa depois dela, a linha é excluída
                if dt_ate and data_inicio > dt_ate:
                    incluir = False

            # Se a linha passou por todos os filtros (texto e data),
            #       ela é adicionada à lista de resultados
            if incluir:
                resultados.append(linha)

        # Atualiza a Treeview apenas com os dados filtrados
        self.reinserir_dados_filtrados(resultados)


    # Define a função responsável por exportar os dados da
    #       Treeview para um arquivo Excel.
    def exportar_excel(self):

        # Obtém todos os itens atualmente visíveis na
        #       Treeview (relatório exibido).
        itens = self.tree_relatorio.get_children()

        # Verifica se a Treeview está vazia, ou seja, se
        #       não há dados a serem exportados.
        if not itens:

            # Exibe uma mensagem informando ao usuário que
            #       não há dados disponíveis para exportação.
            messagebox.showinfo("Informação",
                                "Não há dados para exportar.")

            # Sai da função imediatamente, pois não há informações para processar.
            return

        # Inicializa uma lista vazia que será utilizada para
        #       armazenar os dados extraídos da Treeview.
        linhas = []

        # Percorre todos os itens presentes na Treeview para
        #       extrair os valores de cada linha.
        for item_id in itens:

            # Obtém os valores da linha correspondente ao item atual da Treeview.
            valores = self.tree_relatorio.item(item_id, "values")

            # Adiciona a tupla de valores da linha na lista de
            #       linhas que serão exportadas.
            linhas.append(valores)

        # Converte os dados extraídos da Treeview para um DataFrame do pandas.
        df = pd.DataFrame(linhas, columns=self.colunas)

        # Define o caminho onde o arquivo Excel será salvo.
        # `os.getcwd()` obtém o diretório atual do
        #       programa e "relatorio.xlsx" será o nome do arquivo.
        caminho = os.path.join(os.getcwd(), "relatorio.xlsx")

        try:

            # Tenta salvar o DataFrame como um arquivo Excel no caminho definido.
            # `index=False` significa que o índice da tabela não será salvo no arquivo.
            df.to_excel(caminho, index=False)

            # Se o processo for bem-sucedido, exibe uma mensagem de sucesso ao usuário,
            # informando o local onde o arquivo foi salvo.
            messagebox.showinfo("Sucesso",
                                f"Relatório exportado para: {caminho}")

        except Exception as e:

            # Caso ocorra um erro ao tentar exportar o arquivo Excel,
            # uma mensagem de erro é exibida contendo a descrição do problema.
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")


    # Manipula o evento de duplo clique na Treeview para
    #       abrir a edição de uma reserva.
    def duplo_clique_reserva(self, event):

        # Verifica se a entidade selecionada no combobox é "Reservas".
        # Caso contrário, a função não faz nada.
        if self.entidade_var.get() != "Reservas":
            return

        # Obtém a linha selecionada na Treeview.
        sel = self.tree_relatorio.selection()

        # Se nenhuma linha estiver selecionada, não há nada para processar.
        if not sel:
            return

        # Obtém os valores da linha selecionada.
        valores = self.tree_relatorio.item(sel, "values")

        # Verifica se a linha possui pelo
        #       menos 7 valores (garantindo que há um ID de reserva).
        if len(valores) < 7:
            return

        # Obtém o ID da reserva, que está armazenado na
        #       sétima coluna da Treeview.
        reserva_id_str = valores[6]

        # Converte o ID da reserva para um formato válido
        #       do MongoDB (ObjectId).
        reserva_id = ObjectId(reserva_id_str)

        # Busca a reserva correspondente no banco de dados pelo ID.
        reserva_doc = reservas_collection.find_one({"_id": reserva_id})

        # Se a reserva for encontrada, abre a janela de edição da reserva.
        if reserva_doc:

            JanelaEditarReserva(self, reserva_doc)

        else:

            # Se a reserva não for encontrada no banco de
            #       dados, exibe uma mensagem de erro.
            messagebox.showerror("Erro", "Reserva não encontrada no BD.")


    # Define o método responsável por retornar ao Dashboard principal.
    def voltar_dashboard(self):

        # Esconde a tela atual do relatório removendo-a da interface,
        # mas sem destruí-la completamente.
        # `self.pack_forget()` faz com que o frame desapareça da tela,
        # permitindo que outra interface ocupe o espaço.
        self.pack_forget()

        # Cria e exibe a tela principal do Dashboard novamente.
        # `TelaDashboard` é chamada, passando o mestre (janela principal)
        # e as permissões do usuário, para que o Dashboard funcione corretamente.
        TelaDashboard(self.mestre, self.permissoes_usuario)


# =============================================================================
# =================== TELA DE MAPA DE QUARTOS (CALENDÁRIO) ====================
# =============================================================================

# Define a classe `TelaMapaQuartos`, que herda de `tk.Frame`.
class TelaMapaQuartos(tk.Frame):

    # Inicializa a interface do mapa de quartos.
    def __init__(self, mestre, permissoes_usuario):

        # `super().__init__()` chama o construtor da
        #       classe `tk.Frame` para inicializar o frame.
        # `mestre` é a janela principal onde esse frame será inserido.
        # `bg="#f7f7f7"` define a cor de fundo como **cinza muito claro**.
        super().__init__(mestre, bg="#f7f7f7")

        # Armazena a referência da janela principal na variável `self.mestre`.
        self.mestre = mestre

        # Armazena as permissões do usuário, que podem ser
        #       usadas para definir acessos.
        self.permissoes_usuario = permissoes_usuario

        # Faz com que o frame ocupe todo o espaço disponível na janela principal.
        # `fill="both"` faz o frame expandir tanto horizontalmente
        #       quanto verticalmente.
        # `expand=True` permite que o frame se ajuste automaticamente ao
        #       redimensionar a janela.
        self.pack(fill="both", expand=True)

        # Cria um rótulo (`Label`) para exibir o título da tela.
        # `text="Mapa de Quartos"` define o texto exibido no rótulo.
        # `font=("Helvetica", 16, "bold")` define a fonte
        #       como **Helvetica, tamanho 16, em negrito**.
        # `bg="#f7f7f7"` define o fundo do rótulo como **cinza muito claro**.
        lbl_titulo = tk.Label(self,
                              text="Mapa de Quartos",
                              font=("Helvetica", 16, "bold"),
                              bg="#f7f7f7")

        # Exibe o rótulo na interface, centralizado na tela.
        # `pady=10` adiciona um espaçamento vertical de
        #       **10 pixels** acima e abaixo do rótulo.
        lbl_titulo.pack(pady=10)

        # Cria um frame (`ttk.Frame`) que será utilizado para
        #       organizar os elementos da parte superior da interface.
        frame_top = ttk.Frame(self)

        # Exibe o frame na tela, aplicando espaçamentos.
        # `pady=5` adiciona um espaçamento vertical de **5 pixels** acima e abaixo do frame.
        # `padx=20` adiciona um espaçamento horizontal de
        #       **20 pixels** nas laterais do frame.
        frame_top.pack(pady=5, padx=20)

        # Cria um rótulo (`Label`) dentro do `frame_top` para
        #       orientar o usuário a selecionar a data.
        # `text="Selecione a Data:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0, padx=5, pady=5, sticky="e")` posiciona o
        #       rótulo na **linha 0, coluna 0**, com espaçamentos
        #       horizontais (`padx=5`) e verticais (`pady=5`),
        #       alinhado à **direita** (`sticky="e"`).
        ttk.Label(frame_top,
                  text="Selecione a Data:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria uma variável `StringVar()` para armazenar a data
        #       selecionada pelo usuário.
        self.data_mapa_var = tk.StringVar()

        # Se a biblioteca `tkcalendar` estiver disponível, cria um
        #       seletor de data (`DateEntry`).
        if USANDO_TKCALENDAR:

            # Cria o campo de entrada de data (`DateEntry`) para
            #       permitir a seleção da data.
            # `textvariable=self.data_mapa_var` vincula a data selecionada à
            #       variável `self.data_mapa_var`.
            # `date_pattern="yyyy-MM-dd"` define o formato da data como **AAAA-MM-DD**.
            # `width=12` define a largura do campo como **12 caracteres**.
            self.date_mapa = DateEntry(frame_top,
                                       textvariable=self.data_mapa_var,
                                       date_pattern="yyyy-MM-dd",
                                       width=12)

            # Posiciona o seletor de data na **linha 0, coluna 1**,
            #       com espaçamento de **5 pixels** ao redor.
            self.date_mapa.grid(row=0, column=1, padx=5, pady=5)

        else:

            # Caso o `tkcalendar` não esteja instalado, exibe um
            #       aviso informando o usuário.
            # `text="tkcalendar não instalado."` exibe a mensagem na tela.
            # `grid(row=0, column=1)` posiciona o aviso na **linha 0, coluna 1**.
            tk.Label(frame_top,
                     text="tkcalendar não instalado.").grid(row=0, column=1)

        # Cria um botão (`Button`) dentro do `frame_top` para atualizar o mapa de quartos.
        # `text="Atualizar Mapa"` define o texto exibido no botão.
        # `command=self.atualizar_mapa` associa o botão à função `self.atualizar_mapa`,
        # que será executada ao clicar no botão.
        btn_atualizar = ttk.Button(frame_top,
                                   text="Atualizar Mapa",
                                   command=self.atualizar_mapa)

        # Posiciona o botão na **linha 0, coluna 2**, com espaçamentos:
        # `padx=10` adiciona **10 pixels** de espaçamento horizontal.
        # `pady=5` adiciona **5 pixels** de espaçamento vertical.
        btn_atualizar.grid(row=0, column=2, padx=10, pady=5)

        # Cria um frame (`ttk.Frame`) que será usado para exibir os quartos.
        # Esse frame servirá como um contêiner onde os quartos
        #       serão organizados visualmente.
        self.frame_quartos = ttk.Frame(self)

        # Exibe o frame na interface, permitindo que ele se
        #       expanda conforme necessário.
        # `fill="both"` faz com que o frame ocupe **todo o espaço
        #       disponível** horizontal e verticalmente.
        # `expand=True` permite que o frame aumente de tamanho quando a
        #       janela for redimensionada.
        # `padx=20` adiciona **20 pixels** de espaçamento horizontal.
        # `pady=20` adiciona **20 pixels** de espaçamento vertical.
        self.frame_quartos.pack(fill="both", expand=True, padx=20, pady=20)

        # Cria um botão (`Button`) dentro do frame principal para voltar ao Dashboard.
        # `text="Voltar ao Dashboard"` define o texto exibido no botão.
        # `command=self.voltar_dashboard` associa o botão à
        #       função `self.voltar_dashboard`, que será executada ao clicar no botão.
        btn_voltar = ttk.Button(self,
                                text="Voltar ao Dashboard",
                                command=self.voltar_dashboard)

        # Exibe o botão na interface, centralizado na tela.
        # `pady=10` adiciona **10 pixels** de espaçamento
        #       vertical ao redor do botão.
        btn_voltar.pack(pady=10)

        # Verifica se a biblioteca `tkcalendar` está disponível
        #       para definir a data inicial automaticamente.
        if USANDO_TKCALENDAR:
            # Obtém a data atual no formato **AAAA-MM-DD**.
            hoje_str = datetime.datetime.now().strftime("%Y-%m-%d")

            # Define a data inicial do seletor como a data de hoje.
            self.data_mapa_var.set(hoje_str)

        # Após configurar a interface, chama a função `self.atualizar_mapa()`
        # para carregar o estado inicial dos quartos na tela.
        self.atualizar_mapa()

    # ---------------- FUNÇÃO PARA ATUALIZAR O MAPA DE QUARTOS ---------------- #

    def atualizar_mapa(self):

        # Percorre todos os widgets dentro de `self.frame_quartos` e os remove.
        # Isso garante que o mapa de quartos seja atualizado
        #       corretamente sem sobreposição de elementos antigos.
        for widget in self.frame_quartos.winfo_children():
            widget.destroy()

        # Se o `tkcalendar` estiver instalado, obtém a data
        #       selecionada no formato de string.
        # Caso contrário, `data_str` será `None`.
        data_str = self.data_mapa_var.get().strip() if USANDO_TKCALENDAR else None

        # Se não houver uma data selecionada (ou `tkcalendar` não estiver instalado),
        # define `data_str` como a data atual no formato **AAAA-MM-DD**.
        if not data_str:
            data_str = datetime.datetime.now().strftime("%Y-%m-%d")

        # Obtém todos os quartos armazenados no banco de dados `quartos_collection`.
        # `find()` retorna todos os registros e `sort("numero_quarto", 1)` os
        #       ordena pelo número do quarto em ordem crescente.
        todos_quartos = list(quartos_collection.find().sort("numero_quarto", 1))

        # Define a quantidade de **colunas por linha** para exibir os
        #       quartos organizadamente.
        colunas_por_linha = 5

        # Inicializa os índices da **linha (`row_index`) e
        #       coluna (`col_index`)** onde os quartos serão posicionados.
        row_index = 0
        col_index = 0

        # PERCORRE TODOS OS QUARTOS PARA EXIBIÇÃO
        for quarto in todos_quartos:

            # Obtém o número do quarto no banco de dados.
            # Se não existir, define como `"???"` para indicar um
            #       erro ou dado ausente.
            numero_quarto = quarto.get("numero_quarto", "???")

            # Chama a função `self.verificar_ocupacao(quarto, data_str)`
            # para verificar se o quarto está ocupado na data selecionada.
            ocupado = self.verificar_ocupacao(quarto, data_str)

            # Se o quarto estiver ocupado, define as cores de fundo e do texto:
            # `cor_fundo = "yellow"` → Fundo **amarelo** indica
            #       que o quarto está **ocupado**.
            # `cor_texto = "black"` → Texto preto para melhor contraste.
            if ocupado:
                cor_fundo = "yellow"  # Amarelo
                cor_texto = "black"  # Preto

            # Se o quarto estiver disponível, define outras cores:
            # `cor_fundo = "green"` → Fundo **verde** indica que o quarto está **livre**.
            # `cor_texto = "white"` → Texto branco para melhor contraste.
            else:
                cor_fundo = "green"  # Verde
                cor_texto = "white"  # Branco

            # O texto do botão será no formato "Quarto {número do quarto}".
            texto_botao = f"Quarto {numero_quarto}"

            # Cria um botão (`Button`) dentro do `self.frame_quartos`
            #       para representar um quarto.
            # Esse botão permite visualizar ou interagir com o quarto ao clicar nele.
            btn = tk.Button(

                # O botão será posicionado dentro do frame `self.frame_quartos`.
                self.frame_quartos,

                # Define o texto exibido no botão, contendo o número do
                #       quarto (ex.: "Quarto 101").
                text=texto_botao,

                # Define a cor de fundo do botão:
                # - **"yellow"** se o quarto estiver ocupado.
                # - **"green"** se o quarto estiver disponível.
                bg=cor_fundo,

                # Define a cor do texto do botão:
                # - **"black"** para quartos ocupados (melhor contraste no fundo amarelo).
                # - **"white"** para quartos livres (melhor contraste no fundo verde).
                fg=cor_texto,

                # Define a **largura** do botão como **15 caracteres**.
                width=15,

                # Define a **altura** do botão como **2 linhas de texto**.
                height=2,

                # Associa o botão à função `self.on_quarto_click`, passando os parâmetros:
                # - `nq=numero_quarto` → Número do quarto clicado.
                # - `d=data_str` → Data selecionada.
                # - `oc=ocupado` → Indica se o quarto está ocupado (True) ou não (False).
                command=lambda nq=numero_quarto,
                               d=data_str,
                               oc=ocupado: self.on_quarto_click(nq, d, oc)

            )

            # Define a posição do botão dentro do `frame_quartos` usando `grid()`.
            # `row=row_index` → Define a **linha** do botão na grade.
            # `column=col_index` → Define a **coluna** do botão na grade.
            # `padx=5` → Adiciona **5 pixels** de espaçamento horizontal entre os botões.
            # `pady=5` → Adiciona **5 pixels** de espaçamento vertical entre os botões.
            btn.grid(row=row_index, column=col_index, padx=5, pady=5)

            # Aumenta o índice da coluna para posicionar o próximo botão ao lado.
            col_index += 1

            # Se a quantidade de colunas atingir o limite (`colunas_por_linha`),
            # reseta o índice da coluna (`col_index = 0`) e avança
            #       para a próxima linha (`row_index += 1`).
            if col_index >= colunas_por_linha:
                col_index = 0  # Reinicia a contagem de colunas.
                row_index += 1  # Passa para a próxima linha da grade.

    # FUNÇÃO PARA VERIFICAR A OCUPAÇÃO DO QUARTO
    def verificar_ocupacao(self, quarto_doc, data_str):

        # Obtém o número do quarto a partir do documento `quarto_doc` do banco de dados.
        # Se o campo `"numero_quarto"` não existir, ocorrerá um
        #       erro, pois esse dado é obrigatório.
        numero_quarto = quarto_doc["numero_quarto"]

        # CONVERTE A DATA SELECIONADA PARA OBJETO DATETIME
        try:

            # Converte a string `data_str` para um objeto `datetime`
            #       no formato **AAAA-MM-DD**.
            dt_ref = datetime.datetime.strptime(data_str, "%Y-%m-%d")

        except:

            # Se a conversão falhar (exemplo: data inválida),
            #       usa a data e hora atuais.
            dt_ref = datetime.datetime.now()

        # Realiza uma consulta na `reservas_collection` para
        #       encontrar reservas ativas no quarto.
        # `"$ne": "Finalizada"` significa que **não** queremos reservas finalizadas.
        reservas_ativas = reservas_collection.find({
            "numero_quarto": numero_quarto,  # Filtra pelo número do quarto.
            "status": {"$ne": "Finalizada"}  # Ignora reservas já finalizadas.
        })

        # Percorre todas as reservas ativas encontradas no banco de dados.
        for r in reservas_ativas:

            try:

                # Converte a string armazenada no campo "data_inicio" da
                #       reserva para um objeto `datetime`.
                # O formato esperado da data é "YYYY-MM-DD".
                r_dt_ini = datetime.datetime.strptime(r["data_inicio"], "%Y-%m-%d")

                # Converte a string armazenada no campo "data_fim" da
                #       reserva para um objeto `datetime`.
                # O formato esperado da data é "YYYY-MM-DD".
                r_dt_fim = datetime.datetime.strptime(r["data_fim"], "%Y-%m-%d")

                # Verifica se a data de referência `dt_ref` está dentro do período da reserva.
                # Se `dt_ref` for maior ou igual à data de início da reserva (`r_dt_ini`) e
                # menor ou igual à data de fim da reserva (`r_dt_fim`), significa que o quarto
                # está ocupado na data selecionada.
                if r_dt_ini <= dt_ref <= r_dt_fim:
                    # Retorna `True` indicando que o quarto está ocupado nessa data.
                    return True

            except:

                # Se ocorrer algum erro ao converter as datas da
                #       reserva (por exemplo, se os dados estiverem corrompidos ou
                #       fora do formato esperado), o erro será ignorado.
                pass

        # Se nenhuma reserva ativa foi encontrada para a data selecionada,
        #       significa que o quarto está disponível.
        # Retorna `False` indicando que o quarto **não está ocupado** nessa data.
        return False

    # Função chamada quando o usuário clica em um quarto no mapa.
    def on_quarto_click(self, numero_quarto, data_str, ocupado):

        # `numero_quarto` → Representa o número do quarto clicado.
        # `data_str` → Data selecionada para verificar a disponibilidade do quarto.
        # `ocupado` → Indica se o quarto está ocupado (`True`) ou disponível (`False`).
        if ocupado:

            # Se o quarto estiver ocupado (`True`), abre a tela para
            #       editar a reserva existente.
            # A função `abrir_janela_editar_reserva` receberá o número
            #       do quarto e a data selecionada.
            self.abrir_janela_editar_reserva(numero_quarto, data_str)

        else:

            # Se o quarto **não estiver ocupado** (`False`), abre a
            #       tela para criar uma nova reserva.
            # A função `abrir_janela_nova_reserva` receberá o número do
            #       quarto e a data selecionada.
            self.abrir_janela_nova_reserva(numero_quarto, data_str)

    # Função responsável por abrir a tela para criar uma nova reserva.
    def abrir_janela_nova_reserva(self, numero_quarto, data_inicio_str):

        # `numero_quarto` → Representa o número do quarto que será reservado.
        # `data_inicio_str` → Data selecionada como início da
        #       reserva, no formato "YYYY-MM-DD".

        # Chama a classe `JanelaNovaReserva`, passando como parâmetros:
        # - `self` → Referência da classe atual para manter a hierarquia correta.
        # - `numero_quarto` → Número do quarto a ser reservado.
        # - `data_inicio_str` → Data de início da nova reserva.
        JanelaNovaReserva(self, numero_quarto, data_inicio_str)


    # Função responsável por abrir a janela de edição de uma reserva existente.
    def abrir_janela_editar_reserva(self, numero_quarto, data_str):

        # `numero_quarto` → Número do quarto cuja reserva será editada.
        # `data_str` → Data selecionada no formato "YYYY-MM-DD".

        # Converte a string da data (`data_str`) para um objeto `datetime`.
        # Isso permite comparações precisas de datas no código.
        dt_ref = datetime.datetime.strptime(data_str, "%Y-%m-%d")

        # Busca todas as reservas ativas no banco de dados
        #       que não estejam finalizadas.
        # O critério de busca inclui apenas as reservas que
        #       pertencem ao quarto selecionado.
        reservas_ativas = list(reservas_collection.find({
            "numero_quarto": numero_quarto,  # Filtra as reservas pelo número do quarto.
            "status": {"$ne": "Finalizada"}  # Exclui reservas que já foram finalizadas.
        }))

        # Inicializa a variável que armazenará a reserva
        #       correspondente à data selecionada.
        reserva_encontrada = None

        # Itera sobre todas as reservas ativas encontradas
        #       para o quarto selecionado.
        for r in reservas_ativas:

            try:

                # Converte a data de início da reserva (string) para um objeto `datetime`.
                r_dt_ini = datetime.datetime.strptime(r["data_inicio"], "%Y-%m-%d")

                # Converte a data de fim da reserva (string) para um objeto `datetime`.
                r_dt_fim = datetime.datetime.strptime(r["data_fim"], "%Y-%m-%d")

                # Verifica se a data selecionada (`dt_ref`) está dentro
                #       do período da reserva atual.
                if r_dt_ini <= dt_ref <= r_dt_fim:

                    # Se a data estiver dentro do intervalo, atribui a
                    #       reserva à variável `reserva_encontrada`.
                    reserva_encontrada = r

                    # Encerra o loop, pois já encontramos a reserva correspondente.
                    break

            except:

                # Se houver um erro ao converter as datas, o loop
                #       continua sem interromper a execução.
                pass

        # Verifica se uma reserva foi encontrada para a data selecionada.
        if reserva_encontrada:

            # Se a reserva for encontrada, abre a janela de edição da reserva.
            # `JanelaEditarReserva` é chamada com os parâmetros:
            # - `self` → Referência da classe atual.
            # - `reserva_encontrada` → Dados da reserva que será editada.
            JanelaEditarReserva(self, reserva_encontrada)

        else:

            # Se nenhuma reserva for encontrada para a data selecionada,
            # exibe um aviso informando que não foi possível localizar a reserva.
            messagebox.showwarning("Aviso",
                                   "Não foi possível localizar a reserva para esta data.")



    # Função responsável por retornar à tela principal (Dashboard).
    def voltar_dashboard(self):

        # `self.pack_forget()` remove a tela atual da interface,
        # ocultando-a sem destruir completamente o frame.
        self.pack_forget()

        # Cria uma nova instância da classe `TelaDashboard`
        #       para exibir o menu principal.
        # Parâmetros passados:
        # - `self.mestre` → Referência à janela principal da aplicação.
        # - `self.permissoes_usuario` → Permissões do usuário logado,
        #       garantindo acesso adequado às funcionalidades.
        TelaDashboard(self.mestre, self.permissoes_usuario)


# =============================================================================
# ============= JANELA PARA NOVA RESERVA (TELA CHEIA / TOPLEVEL) ==============
# =============================================================================

# Classe responsável por criar uma janela modal para
#       cadastrar uma nova reserva.
class JanelaNovaReserva(tk.Toplevel):

    # Método construtor da classe `JanelaNovaReserva`.

    # `pai` → Referência à janela ou frame que chamou essa tela.
    # `numero_quarto` → Número do quarto onde será feita a reserva.
    # `data_inicio_str` → Data de início da reserva no formato de string (YYYY-MM-DD).
    def __init__(self, pai, numero_quarto, data_inicio_str):

        # Chama o construtor da classe `tk.Toplevel`, que cria
        #       uma nova janela independente.
        # `super().__init__(pai)` permite que a classe herde
        #       todas as propriedades e métodos
        #       da classe `tk.Toplevel`, garantindo que esta nova janela
        #       seja criada corretamente e esteja associada à
        #       janela ou frame pai (`pai`).
        super().__init__(pai)

        # Define o título da janela, exibido na barra de título da interface gráfica.
        # A formatação `f"Nova Reserva - Quarto {numero_quarto}"` insere dinamicamente
        # o número do quarto no título, tornando a interface mais
        #       informativa para o usuário.
        self.title(f"Nova Reserva - Quarto {numero_quarto}")

        # Configura a janela para abrir em modo tela cheia.
        # O atributo `"-fullscreen"` garante que a janela ocupará
        #       toda a tela do usuário, melhorando a experiência e
        #       evitando distrações com outras janelas.
        # Isso pode ser útil para aplicações que exigem total
        #       imersão ou controle total da interface.
        self.attributes("-fullscreen", True)

        # Armazena a referência ao objeto pai (geralmente a
        #       janela principal da aplicação).
        # Isso é útil para que a nova janela possa interagir com
        #       elementos da interface principal,
        # como atualizar informações ou fechar-se ao concluir uma ação.
        # A variável `self.pai` permite que métodos desta classe
        #       acessem atributos e funções da janela pai.
        self.pai = pai

        # Armazena o número do quarto na variável de instância `self.numero_quarto`.
        # Isso permite que o número do quarto esteja disponível em toda a classe,
        # sendo utilizado em diversos métodos para manipulação da reserva.
        self.numero_quarto = numero_quarto

        # Realiza uma busca no banco de dados (`quartos_collection`)
        #       para obter as informações do quarto.
        # A pesquisa é feita com base no número do quarto (`numero_quarto`),
        #       retornando um documento do MongoDB.
        # Caso o quarto não seja encontrado, `quarto_doc` recebe `None`.
        quarto_doc = quartos_collection.find_one({"numero_quarto": numero_quarto})

        # Obtém a capacidade máxima de pessoas que o quarto pode acomodar.
        # Se `quarto_doc` for encontrado no banco de dados, `quarto_doc["capacidade"]` é
        #       atribuído à variável `self.capacidade_quarto`.
        # Caso contrário, atribui-se `0`, indicando que o quarto não foi
        #       encontrado ou não possui capacidade registrada.
        self.capacidade_quarto = quarto_doc["capacidade"] if quarto_doc else 0

        # Obtém o preço base por diária do quarto.
        # Se `quarto_doc` existir, `quarto_doc["preco_diaria"]` é
        #       atribuído à variável `self.preco_base_quarto`.
        # Se o quarto não for encontrado, define-se `0.0`, garantindo que
        #       não haja erro ao tentar acessar a chave `preco_diaria`.
        self.preco_base_quarto = quarto_doc["preco_diaria"] if quarto_doc else 0.0

        # Cria uma variável de controle (`StringVar`) para armazenar a
        #       data de início da reserva.
        # O valor inicial da variável é definido como `data_inicio_str`,
        #       que representa a data selecionada
        #       pelo usuário ao clicar no quarto no mapa.
        self.data_inicio_var = tk.StringVar(value=data_inicio_str)

        # Cria uma variável de controle (`StringVar`) para armazenar a data de fim da reserva.
        # Inicialmente, a data de fim é definida como igual à data de início (`data_inicio_str`).
        # Posteriormente, o usuário pode modificar essa data conforme necessário.
        self.data_fim_var = tk.StringVar(value=data_inicio_str)

        # Cria uma variável de controle (`StringVar`) para armazenar o
        #       nome do hóspede principal da reserva.
        # Inicialmente, a variável está vazia, pois o usuário precisará
        #       selecionar ou digitar um nome.
        self.hospede_var = tk.StringVar()

        # Realiza uma consulta na coleção de hóspedes (`hospedes_collection.find()`).
        # Para cada documento encontrado, extrai o nome do
        #       hóspede (`h["nome"]`) e cria uma lista contendo
        #       todos os hóspedes cadastrados no banco de dados.
        # Essa lista será utilizada para facilitar a seleção do
        #       hóspede no momento da reserva.
        self.lista_hospedes_bd = [h["nome"] for h in hospedes_collection.find()]

        # Cria uma lista vazia para armazenar os hóspedes adicionados à reserva.
        # Durante o processo de reserva, o usuário poderá adicionar
        #       múltiplos hóspedes à lista.
        self.lista_hospedes_reserva = []

        # Cria uma lista vazia para armazenar os produtos ou serviços
        #       consumidos durante a estadia.
        # Durante o processo de reserva, o usuário poderá adicionar
        #       itens de consumo à reserva,
        #       como refeições, bebidas e outros serviços do hotel.
        self.lista_consumo = []

        # Cria uma variável de controle (`DoubleVar`) para armazenar o
        #       valor final da reserva.
        # O valor inicial é definido como `0.0`, pois a reserva ainda
        #       não possui custos associados.
        # Esse valor será atualizado automaticamente conforme o usuário
        #       adiciona diárias, produtos ou serviços.
        self.valor_final_var = tk.DoubleVar(value=0.0)

        # Cria uma variável de controle (`StringVar`) para armazenar
        #       observações sobre a reserva.
        # O usuário pode inserir informações adicionais, como
        #       solicitações especiais, preferências do hóspede
        #       ou quaisquer anotações relevantes para a estadia.
        self.observacoes_var = tk.StringVar()

        # Cria um frame principal dentro da janela de nova reserva.
        # O frame (`ttk.Frame`) serve como um contêiner para organizar os
        #       widgets (campos, botões, labels, etc.).
        self.frame_principal = ttk.Frame(self)

        # Posiciona (`pack()`) o frame na janela, ocupando todo o
        #       espaço disponível (`fill="both"`).
        # A opção `expand=True` permite que o frame se expanda caso a
        #       janela seja redimensionada.
        # `padx=10` e `pady=10` adicionam um espaçamento de 10 pixels
        #       nas bordas horizontal e vertical.
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Inicializa a variável `linha` com valor `0`.
        # Esta variável será usada para controlar o número da linha ao
        #       organizar os widgets dentro do frame.
        # Conforme adicionamos novos elementos, incrementamos essa
        #       variável para manter a organização vertical.
        linha = 0

        # Cria um rótulo (`Label`) dentro do frame principal para
        #       exibir o número do quarto.
        # `text=f"Quarto: {numero_quarto}"` define o texto do rótulo
        #       dinamicamente, incluindo o número do quarto.
        # `font=("Helvetica", 12, "bold")` define a fonte do texto
        #       como Helvetica, tamanho 12, em negrito.
        ttk.Label(self.frame_principal,
                  text=f"Quarto: {numero_quarto}",
                  font=("Helvetica", 12, "bold")).grid(

            # Define a posição do rótulo dentro do layout em grade (`grid`).
            # `row=linha` posiciona o rótulo na linha atual (definida
            #       anteriormente na variável `linha`).
            # `column=0` posiciona o rótulo na primeira coluna.
            # `columnspan=2` faz com que o rótulo ocupe duas colunas,
            #       garantindo um alinhamento visual melhor.
            # `sticky="w"` alinha o rótulo à esquerda (`west`), para que o
            #       texto fique alinhado com os demais elementos da tela.
            # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e
            #       abaixo do rótulo, melhorando a legibilidade.
            row=linha, column=0, columnspan=2, sticky="w", pady=5

        )

        # Incrementa a variável `linha` em 1, movendo para a próxima linha da grade.
        # Isso garante que os próximos elementos adicionados fiquem
        #       organizados abaixo deste rótulo.
        linha += 1

        # Cria um rótulo para exibir o campo "Data Início".
        # `text="Data Início:"` define o texto exibido no rótulo.
        # `row=linha` posiciona o rótulo na linha atual da grade.
        # `column=0` coloca o rótulo na primeira coluna.
        # `sticky="e"` alinha o rótulo à direita dentro da célula.
        # `padx=5, pady=5` adiciona espaçamentos horizontais e
        #       verticais para melhor organização.
        ttk.Label(self.frame_principal,
                  text="Data Início:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada para a data de início da reserva.
        # `textvariable=self.data_inicio_var` associa o
        #       campo à variável `self.data_inicio_var`.
        # `width=15` define a largura do campo como 15 caracteres.
        # `row=linha` posiciona o campo na mesma linha do rótulo correspondente.
        # `column=1` coloca o campo na segunda coluna.
        # `sticky="w"` alinha o campo à esquerda dentro da célula.
        # `padx=5, pady=5` adiciona espaçamentos horizontais e
        #       verticais para melhor organização.
        ttk.Entry(self.frame_principal,
                  textvariable=self.data_inicio_var,
                  width=15).grid(row=linha, column=1, padx=5, pady=5, sticky="w")

        # Incrementa a variável `linha` para que o próximo elemento da
        #       interface seja posicionado na linha seguinte.
        linha += 1

        # Cria um rótulo para exibir o campo "Data Fim".
        # `text="Data Fim:"` define o texto exibido no rótulo.
        # `row=linha` posiciona o rótulo na linha atual da grade.
        # `column=0` coloca o rótulo na primeira coluna.
        # `sticky="e"` alinha o rótulo à direita dentro da célula.
        # `padx=5, pady=5` adiciona espaçamentos horizontais e
        #       verticais para melhor organização.
        ttk.Label(self.frame_principal,
                  text="Data Fim:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada para a data de término da reserva.
        # `textvariable=self.data_fim_var` associa o campo à variável `self.data_fim_var`.
        # `width=15` define a largura do campo como 15 caracteres.
        # `row=linha` posiciona o campo na mesma linha do rótulo correspondente.
        # `column=1` coloca o campo na segunda coluna.
        # `sticky="w"` alinha o campo à esquerda dentro da célula.
        # `padx=5, pady=5` adiciona espaçamentos horizontais e
        #       verticais para melhor organização.
        ttk.Entry(self.frame_principal,
                  textvariable=self.data_fim_var,
                  width=15).grid(row=linha, column=1, padx=5, pady=5, sticky="w")

        # Incrementa a variável `linha` para que o próximo elemento da
        #       interface seja posicionado na linha seguinte.
        linha += 1

        # Cria um rótulo para indicar o campo "Hóspedes".
        # `text="Hóspedes:"` define o texto exibido no rótulo.
        # `row=linha` posiciona o rótulo na linha atual da grade.
        # `column=0` coloca o rótulo na primeira coluna.
        # `sticky="ne"` alinha o rótulo no canto superior direito da célula.
        # `padx=5, pady=5` adiciona espaçamentos horizontais e
        #       verticais para melhor disposição visual.
        ttk.Label(self.frame_principal,
                  text="Hóspedes:").grid(row=linha, column=0, sticky="ne", padx=5, pady=5)

        # Cria um frame para agrupar os elementos relacionados à seleção de hóspedes.
        # `frame_principal` define o frame principal como elemento pai.
        frame_hosp = ttk.Frame(self.frame_principal)

        # Posiciona o frame `frame_hosp` dentro da grade da interface.
        # `row=linha` coloca o frame na mesma linha do rótulo "Hóspedes".
        # `column=1` coloca o frame na segunda coluna.
        # `sticky="w"` alinha o frame à esquerda dentro da célula.
        frame_hosp.grid(row=linha, column=1, sticky="w")

        # Cria um combobox para selecionar um hóspede a partir da
        #       lista de hóspedes cadastrados.
        # `frame_hosp` define o frame como elemento pai, agrupando os
        #       elementos de seleção de hóspedes.
        # `textvariable=self.hospede_var` associa a variável `hospede_var` ao
        #       combobox, permitindo armazenar o valor selecionado.
        # `values=self.lista_hospedes_bd` define a lista de valores
        #       disponíveis, carregados a partir do banco de dados.
        # `state="readonly"` impede que o usuário digite valores
        #       manualmente, permitindo apenas seleção.
        # `width=25` define a largura do combobox para comportar os
        #       nomes dos hóspedes adequadamente.
        combo_hospede = ttk.Combobox(frame_hosp,
                                     textvariable=self.hospede_var,
                                     values=self.lista_hospedes_bd,
                                     state="readonly", width=25)

        # Posiciona o combobox dentro do `frame_hosp`.
        # `side="left"` alinha o combobox à esquerda do frame.
        # `padx=5` adiciona espaçamento horizontal para evitar
        #       sobreposição com outros elementos.
        combo_hospede.pack(side="left", padx=5)

        # Cria um botão para adicionar um hóspede à lista da reserva.
        # `frame_hosp` define o frame como elemento pai, agrupando os
        #       elementos relacionados à seleção de hóspedes.
        # `text="Add"` define o texto exibido no botão, indicando que
        #       sua função é adicionar um hóspede.
        # `command=self.adicionar_hospede` associa a ação do
        #       botão à função `adicionar_hospede`,
        #       permitindo que um hóspede selecionado no combobox seja
        #       incluído na lista de hóspedes da reserva.
        btn_add_h = ttk.Button(frame_hosp,
                               text="Add",
                               command=self.adicionar_hospede)

        # Posiciona o botão dentro do `frame_hosp`.
        # `side="left"` alinha o botão à esquerda do frame, logo
        #       após o combobox de seleção de hóspedes.
        # `padx=5` adiciona espaçamento horizontal entre o botão e o
        #       combobox para melhorar a organização visual.
        btn_add_h.pack(side="left", padx=5)

        # Incrementa o contador de linhas (`linha += 1`) para garantir que
        #       os próximos elementos sejam posicionados abaixo deste.
        linha += 1

        # Cria uma lista (`Listbox`) para exibir os hóspedes adicionados à reserva.
        # `frame_principal` define o frame como elemento pai, garantindo
        #       que a lista seja posicionada corretamente.
        # `width=40` define a largura da lista, permitindo visualizar
        #       nomes longos sem quebras desnecessárias.
        # `height=4` define a altura da lista, permitindo visualizar até
        #       quatro hóspedes antes da necessidade de rolagem.
        self.lst_hospedes = tk.Listbox(self.frame_principal, width=40, height=4)

        # Posiciona a `Listbox` na interface gráfica.
        # `row=linha` define que o widget será inserido na linha atual do layout.
        # `column=1` posiciona a lista na segunda coluna do frame.
        # `sticky="w"` alinha o widget à esquerda da célula para manter a organização visual.
        # `padx=5` adiciona espaçamento horizontal entre a lista e outros elementos.
        # `pady=5` adiciona espaçamento vertical entre a lista e outros elementos.
        self.lst_hospedes.grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Cria um botão para remover um hóspede selecionado da lista.
        # `frame_principal` define o frame como elemento pai,
        #       garantindo que o botão seja posicionado corretamente.
        # `text="Remover Hóspede"` define o texto exibido no botão,
        #       indicando sua função de remoção.
        # `command=self.remover_hospede` associa a ação do botão à
        #       função `remover_hospede`,
        # permitindo que um hóspede selecionado na `Listbox`
        #       seja removido da reserva.
        btn_rem_h = ttk.Button(self.frame_principal,
                               text="Remover Hóspede",
                               command=self.remover_hospede)

        # Posiciona o botão de remoção na interface gráfica.
        # `row=linha` posiciona o botão na mesma linha da `Listbox`,
        #       facilitando a interação do usuário.
        # `column=2` coloca o botão na terceira coluna do frame, ao
        #       lado da lista de hóspedes.
        # `padx=5` adiciona espaçamento horizontal entre o botão e a
        #       lista para melhor organização.
        # `pady=5` adiciona espaçamento vertical entre o botão e outros elementos.
        btn_rem_h.grid(row=linha, column=2, padx=5, pady=5)

        # Incrementa o contador de linhas (`linha += 1`) para garantir
        #       que os próximos elementos sejam posicionados abaixo deste.
        linha += 1

        # Cria um rótulo (`Label`) para indicar a seção de produtos
        #       consumidos na reserva.
        # `frame_principal` define o frame como elemento pai,
        #       garantindo que o rótulo seja posicionado corretamente.
        # `text="Produtos:"` define o texto exibido no rótulo para
        #       indicar a função da seção.
        # `row=linha` posiciona o rótulo na linha atual do layout.
        # `column=0` coloca o rótulo na primeira coluna do frame, alinhado à esquerda.
        # `sticky="e"` alinha o texto à direita dentro da célula para manter um visual organizado.
        # `padx=5` adiciona um espaçamento horizontal entre o rótulo e os outros elementos.
        # `pady=5` adiciona um espaçamento vertical entre o rótulo e os outros elementos.
        ttk.Label(self.frame_principal,
                  text="Produtos:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um frame (`Frame`) para organizar os elementos
        #       relacionados à seleção de produtos.
        # `frame_principal` define o frame como elemento pai, garantindo que
        #       este novo frame seja inserido corretamente.
        frame_prod = ttk.Frame(self.frame_principal)

        # Posiciona o frame de produtos na interface gráfica.
        # `row=linha` posiciona o frame na mesma linha do
        #       rótulo "Produtos:", mantendo a hierarquia visual.
        # `column=1` coloca o frame na segunda coluna do layout,
        #       alinhado corretamente com outros campos.
        # `sticky="w"` alinha o frame à esquerda dentro da célula,
        #       garantindo que os elementos internos fiquem alinhados.
        frame_prod.grid(row=linha, column=1, sticky="w")

        # Cria uma variável de controle do tipo `StringVar` para
        #       armazenar o nome do produto selecionado.
        # `tk.StringVar()` cria uma variável especial do Tkinter que
        #       pode ser vinculada a um widget, como `Combobox`.
        # Essa variável será usada para capturar e armazenar a seleção do
        #       usuário no menu suspenso de produtos.
        self.produto_var = tk.StringVar()

        # Cria uma variável de controle do tipo `IntVar` para armazenar a
        #       quantidade do produto a ser consumido.
        # `tk.IntVar(value=1)` cria uma variável inteira e define o valor inicial como 1.
        # Essa variável será usada em um campo de entrada (`Entry`)
        #       para que o usuário informe a quantidade desejada.
        self.quantidade_var = tk.IntVar(value=1)

        # Gera uma lista contendo os nomes de todos os produtos
        #       disponíveis no banco de dados (`produtos_collection`).
        # `produtos_collection.find()` faz uma consulta no banco de dados e
        #       retorna todos os documentos da coleção de produtos.
        # O laço `[p["nome"] for p in produtos_collection.find()]` percorre
        #       cada produto retornado e extrai apenas o nome dele.
        # O resultado é uma lista com os nomes de todos os produtos, que
        #       será usada para preencher um menu suspenso (`Combobox`).
        lista_produtos = [p["nome"] for p in produtos_collection.find()]

        # Cria um menu suspenso (`Combobox`) para seleção de produtos.
        # `frame_prod` é o contêiner onde este widget será inserido.
        # `textvariable=self.produto_var` vincula a seleção do usuário à
        #       variável `self.produto_var`, permitindo acessar o valor escolhido.
        # `values=lista_produtos` define a lista de produtos disponíveis
        #       como opções no menu suspenso.
        # `width=20` define a largura do campo de seleção para melhor
        #       exibição dos nomes dos produtos.
        combo_prod = ttk.Combobox(frame_prod,
                                  textvariable=self.produto_var,
                                  values=lista_produtos, width=20)

        # Posiciona o `Combobox` dentro do `frame_prod`.
        # `side="left"` alinha o widget à esquerda dentro do frame.
        # `padx=3` adiciona um espaçamento horizontal de 3 pixels para
        #       evitar que o widget fique muito colado em outros elementos.
        combo_prod.pack(side="left", padx=3)

        # Cria um campo numérico (`Spinbox`) para permitir que o
        #       usuário selecione a quantidade do produto consumido.
        # `frame_prod` é o contêiner onde o `Spinbox` será inserido.
        # `from_=1` define o valor mínimo permitido como 1, garantindo que a
        #       quantidade nunca seja zero ou negativa.
        # `to=999` define o valor máximo permitido como 999, evitando
        #       inserções excessivas de produtos.
        # `textvariable=self.quantidade_var` vincula o valor da quantidade à
        #       variável `self.quantidade_var`, permitindo acessá-lo facilmente no código.
        # `width=5` define a largura do campo numérico, ajustando o
        #       tamanho visualmente para números de até três dígitos.
        spin_qtd = ttk.Spinbox(frame_prod,
                               from_=1,
                               to=999,
                               textvariable=self.quantidade_var,
                               width=5)

        # Posiciona o `Spinbox` dentro do `frame_prod`.
        # `side="left"` alinha o widget à esquerda dentro do frame.
        # `padx=3` adiciona um espaçamento horizontal de 3 pixels para
        #       manter um layout organizado e legível.
        spin_qtd.pack(side="left", padx=3)

        # Cria um botão para adicionar o produto selecionado à
        #       lista de consumo da reserva.
        # `frame_prod` é o contêiner onde o botão será inserido.
        # `text="Add"` define o texto exibido no botão como "Add".
        # `command=self.adicionar_produto` associa a ação de
        #       adicionar o produto ao clicar no botão.
        btn_add_p = ttk.Button(frame_prod,
                               text="Add",
                               command=self.adicionar_produto)

        # Posiciona o botão dentro do `frame_prod`.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=3` adiciona um espaçamento horizontal de 3 pixels
        #       para evitar que o botão fique colado em outros elementos.
        btn_add_p.pack(side="left", padx=3)

        # Incrementa a variável `linha` para mover os próximos
        #       widgets para a linha seguinte do layout.
        linha += 1

        # Cria uma Treeview (tabela) para exibir os produtos adicionados à reserva.
        # `frame_principal` é o contêiner onde a tabela será inserida.
        # `columns=("nome", "preco", "qtd", "subtotal")` define as colunas da tabela.
        # `show="headings"` oculta a primeira coluna vazia padrão do Treeview.
        # `height=5` define que a tabela exibirá no máximo 5 linhas visíveis de cada vez.
        self.tree_produtos = ttk.Treeview(self.frame_principal,
                                          columns=("nome", "preco", "qtd", "subtotal"),
                                          show="headings",
                                          height=5)

        # Define o cabeçalho da coluna "nome" com o texto "Produto".
        self.tree_produtos.heading("nome", text="Produto")

        # Define o cabeçalho da coluna "preco" com o texto "Preço".
        self.tree_produtos.heading("preco", text="Preço")

        # Define o cabeçalho da coluna "qtd" com o texto "Qtde" (abreviação de quantidade).
        self.tree_produtos.heading("qtd", text="Qtde")

        # Define o cabeçalho da coluna "subtotal" com o texto "Subtotal".
        self.tree_produtos.heading("subtotal", text="Subtotal")

        # Posiciona a tabela dentro do `frame_principal` na linha correspondente.
        # `row=linha` define a linha onde a tabela será inserida.
        # `column=1` posiciona a tabela na segunda coluna do layout.
        # `sticky="w"` alinha a tabela à esquerda dentro da célula.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para separar dos outros elementos.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels para
        #       não ficar colada a outros componentes.
        self.tree_produtos.grid(row=linha,
                                column=1,
                                sticky="w",
                                padx=5,
                                pady=5)

        # Cria um botão para remover um produto da lista de produtos da reserva.
        # `text="Remover Produto"` define o texto exibido no botão.
        # `command=self.remover_produto` associa a função `remover_produto` ao botão,
        # de forma que quando o usuário clicar nele, o produto
        #       selecionado na lista será removido.
        btn_rem_p = ttk.Button(self.frame_principal,
                               text="Remover Produto",
                               command=self.remover_produto)

        # Posiciona o botão de remover produto dentro do `frame_principal`.
        # `row=linha` define a linha onde o botão será inserido,
        #       garantindo alinhamento com os outros elementos.
        # `column=2` posiciona o botão na terceira coluna do layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para
        #       separar o botão dos outros componentes.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels para
        #       evitar que o botão fique colado a outros elementos.
        btn_rem_p.grid(row=linha, column=2, padx=5, pady=5)

        # Incrementa a variável `linha` para que o próximo componente da
        #       interface seja posicionado na linha seguinte.
        linha += 1

        # Cria um rótulo (Label) para exibir o texto "Valor Final:" na interface.
        # `text="Valor Final:"` define o texto exibido no rótulo.
        # `frame_principal` define o contêiner onde o rótulo será posicionado.
        # `grid(row=linha, column=0, sticky="e", padx=5, pady=5)`
        #       define a posição do rótulo na grade.
        # `row=linha` posiciona o rótulo na linha atual.
        # `column=0` define a primeira coluna, alinhada à esquerda.
        # `sticky="e"` alinha o texto do rótulo à direita dentro da célula da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels para
        #       evitar que fique colado a outros elementos.
        # `pady=5` adiciona espaçamento vertical de 5 pixels para
        #       uma melhor organização visual.
        ttk.Label(self.frame_principal,
                  text="Valor Final:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (Entry) para exibir o valor final da reserva.
        # `textvariable=self.valor_final_var` associa a
        #       variável `valor_final_var` ao campo de entrada,
        # permitindo que o valor final seja atualizado dinamicamente
        #       conforme os produtos são adicionados ou removidos.
        # `width=20` define a largura do campo de entrada para acomodar
        #       valores numéricos de forma adequada.
        # `state="readonly"` impede que o usuário edite o valor manualmente,
        #       garantindo que ele seja atualizado apenas pelo sistema.
        # `grid(row=linha, column=1, sticky="w", padx=5, pady=5)` define a
        #       posição do campo de entrada na grade.
        # `row=linha` posiciona o campo na linha atual.
        # `column=1` coloca o campo na segunda coluna, ao lado do rótulo "Valor Final".
        # `sticky="w"` alinha o conteúdo à esquerda dentro da célula da grade.
        # `padx=5` e `pady=5` adicionam espaçamentos horizontal e vertical
        #       para uma organização mais clara na interface.
        ttk.Entry(self.frame_principal,
                  textvariable=self.valor_final_var,
                  width=20,
                  state="readonly").grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Incrementa a variável `linha` para garantir que os próximos
        #       elementos sejam adicionados na linha seguinte.
        linha += 1

        # Cria um rótulo (Label) para exibir o texto "Observações:" na interface.
        # `text="Observações:"` define o texto exibido no rótulo.
        # `frame_principal` define o contêiner onde o rótulo será posicionado.
        # `grid(row=linha, column=0, sticky="e", padx=5, pady=5)`
        #       define a posição do rótulo na grade.
        # `row=linha` posiciona o rótulo na linha atual.
        # `column=0` define a primeira coluna, alinhada à esquerda.
        # `sticky="e"` alinha o texto do rótulo à direita dentro da célula da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels para
        #       melhor separação dos elementos.
        # `pady=5` adiciona espaçamento vertical de 5 pixels para
        #       manter a organização visual da interface.
        ttk.Label(self.frame_principal,
                  text="Observações:").grid(row=linha, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (Entry) para permitir que o usuário
        #       insira observações sobre a reserva.
        # `textvariable=self.observacoes_var` associa a
        #       variável `observacoes_var` ao campo de entrada,
        # garantindo que o conteúdo digitado seja armazenado e possa ser
        #       acessado posteriormente no código.
        # `width=30` define a largura do campo de entrada, permitindo a
        #       exibição de textos mais longos sem precisar de rolagem.
        # `grid(row=linha, column=1, sticky="w", padx=5, pady=5)` define a
        #       posição do campo de entrada na grade.
        # `row=linha` posiciona o campo na linha atual.
        # `column=1` coloca o campo na segunda coluna, ao lado do rótulo "Observações".
        # `sticky="w"` alinha o campo de entrada à esquerda dentro da célula da grade.
        # `padx=5` adiciona espaçamento horizontal para evitar que o
        #       campo fique colado em outros elementos.
        # `pady=5` adiciona espaçamento vertical para manter uma melhor
        #       separação entre os elementos da interface.
        ttk.Entry(self.frame_principal,
                  textvariable=self.observacoes_var,
                  width=30).grid(row=linha, column=1, sticky="w", padx=5, pady=5)

        # Incrementa a variável `linha` para garantir que os
        #       próximos elementos sejam adicionados na linha seguinte.
        linha += 1

        # Cria um contêiner (Frame) para os botões de ação da reserva.
        # `frame_principal` define o contêiner pai onde esse Frame será posicionado.
        # `grid(row=linha, column=0, columnspan=3, pady=10)`
        #       define a posição do Frame na grade.
        # `row=linha` posiciona o Frame na linha atual.
        # `column=0` define que o Frame começa na primeira coluna.
        # `columnspan=3` faz com que o Frame ocupe três colunas,
        #       garantindo centralização dos botões.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels, criando
        #       uma separação visual entre os botões e os campos acima.
        frame_btns = ttk.Frame(self.frame_principal)
        frame_btns.grid(row=linha, column=0, columnspan=3, pady=10)

        # Cria um botão que salva a reserva ao ser clicado.
        # `text="Salvar Reserva"` define o texto exibido no botão.
        # `command=self.salvar_reserva` associa a ação de salvar a
        #       reserva ao ser pressionado.
        # `frame_btns` define que o botão será colocado dentro do
        #       Frame `frame_btns`, garantindo um layout organizado.
        # `pack(side="left", padx=5)` posiciona o botão dentro do Frame.
        # `side="left"` alinha o botão à esquerda dentro do Frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para
        #       evitar que o botão fique colado em outros elementos.
        btn_salvar = ttk.Button(frame_btns,
                                text="Salvar Reserva",
                                command=self.salvar_reserva)
        btn_salvar.pack(side="left", padx=5)

        # Cria um botão para cancelar a reserva.
        # `text="Cancelar Reserva"` define o texto exibido no botão.
        # `command=self.cancelar_reserva` associa a ação de
        #       cancelar a reserva ao ser pressionado.
        # `frame_btns` define que o botão será colocado dentro do
        #       Frame `frame_btns`, garantindo um layout organizado.
        # `pack(side="left", padx=5)` posiciona o botão dentro do Frame.
        # `side="left"` alinha o botão à esquerda dentro do Frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para
        #       evitar que o botão fique colado em outros elementos.
        btn_cancelar = ttk.Button(frame_btns,
                                  text="Cancelar Reserva",
                                  command=self.cancelar_reserva)
        btn_cancelar.pack(side="left", padx=5)

        # Cria um botão para fechar a janela.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.fechar_janela` associa a ação de fechar a
        #       janela ao ser pressionado.
        # `frame_btns` define que o botão será colocado dentro do
        #       Frame `frame_btns`, garantindo um layout organizado.
        # `pack(side="left", padx=5)` posiciona o botão dentro do Frame.
        # `side="left"` alinha o botão à esquerda dentro do Frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para
        #       manter um espaçamento adequado entre os botões.
        btn_fechar = ttk.Button(frame_btns,
                                text="Fechar",
                                command=self.fechar_janela)
        btn_fechar.pack(side="left", padx=5)

        # CHAMAMOS ESTE MÉTODO AQUI PARA CARREGAR O VALOR DO QUARTO
        self.recalcular_total()

    # Função para adicionar um hóspede à reserva.
    def adicionar_hospede(self):

        # Verifica se o número de hóspedes já atingiu a capacidade máxima do quarto.
        # `self.capacidade_quarto` contém o limite de pessoas permitido no quarto.
        # `len(self.lista_hospedes_reserva)` retorna a quantidade atual de hóspedes na lista.
        # Se a capacidade for maior que zero e já estiver cheia,
        #       exibe um erro e retorna.
        if len(self.lista_hospedes_reserva) >= self.capacidade_quarto and self.capacidade_quarto > 0:
            messagebox.showerror("Erro",
                                 f"O quarto tem capacidade para {self.capacidade_quarto} pessoas.")
            return

        # Obtém o nome do hóspede selecionado no combobox.
        # `self.hospede_var.get().strip()` captura o valor
        #       selecionado e remove espaços extras.
        nome = self.hospede_var.get().strip()

        # Verifica se o nome está vazio, caso esteja, interrompe a função.
        if not nome:
            return

        # Verifica se o hóspede já foi adicionado à lista da reserva.
        # Se o nome já estiver presente, a função é interrompida
        #       para evitar duplicação.
        if nome in self.lista_hospedes_reserva:
            return

        # Adiciona o hóspede à lista de hóspedes da reserva.
        self.lista_hospedes_reserva.append(nome)

        # Insere o nome do hóspede na lista de exibição (Listbox).
        # `tk.END` insere o novo nome no final da lista.
        self.lst_hospedes.insert(tk.END, nome)


    # Função para remover um hóspede da lista de hóspedes da reserva.
    def remover_hospede(self):

        # Obtém a seleção do usuário na lista de hóspedes.
        # `self.lst_hospedes.curselection()` retorna uma tupla
        #       contendo os índices dos itens selecionados.
        sel = self.lst_hospedes.curselection()

        # Verifica se nenhum hóspede foi selecionado.
        # Se a lista `sel` estiver vazia, significa que o usuário não
        #       selecionou nenhum item, então a função retorna.
        if not sel:
            return

        # Obtém o índice do hóspede selecionado.
        # `sel[0]` pega o primeiro índice da seleção (assumindo que
        #       apenas um item pode ser removido por vez).
        idx = sel[0]

        # Obtém o nome do hóspede baseado no índice selecionado.
        # `self.lst_hospedes.get(idx)` retorna o nome do hóspede na
        #       posição `idx` dentro da Listbox.
        nome = self.lst_hospedes.get(idx)

        # Remove o hóspede da lista exibida na interface gráfica (Listbox).
        # `self.lst_hospedes.delete(idx)` exclui o item da
        #       interface baseado no índice `idx`.
        self.lst_hospedes.delete(idx)

        # Remove o hóspede da lista interna da reserva.
        # `self.lista_hospedes_reserva.remove(nome)` remove o nome do
        #       hóspede da lista que armazena os hóspedes adicionados.
        self.lista_hospedes_reserva.remove(nome)


    # Função para adicionar um produto à lista de consumo da reserva.
    def adicionar_produto(self):

        # Obtém o nome do produto selecionado na interface.
        # `self.produto_var.get()` pega o valor do campo de entrada do produto.
        # `strip()` remove espaços extras no início e no final da string.
        nome_prod = self.produto_var.get().strip()

        # Obtém a quantidade do produto escolhida pelo usuário.
        # `self.quantidade_var.get()` retorna o valor selecionado no spinbox.
        qtd = self.quantidade_var.get()

        # Verifica se o nome do produto está vazio ou se a
        #       quantidade é menor ou igual a zero.
        # Se qualquer uma dessas condições for verdadeira, a
        #       função retorna sem adicionar o produto.
        if not nome_prod or qtd <= 0:
            return

        # Busca o documento do produto no banco de dados.
        # `produtos_collection.find_one({"nome": nome_prod})` busca o
        #       primeiro produto cujo nome seja igual ao selecionado.
        prod_doc = produtos_collection.find_one({"nome": nome_prod})

        # Verifica se o produto foi encontrado no banco de dados.
        # Caso não tenha sido encontrado, exibe uma mensagem de erro e interrompe a execução.
        if not prod_doc:
            messagebox.showerror("Erro",
                                 f"Produto '{nome_prod}' não encontrado.")
            return

        # Obtém a quantidade atual em estoque do produto.
        # `get("quantidade", 0)` retorna o valor da chave "quantidade" do produto.
        # Se a chave não existir, assume 0 como valor padrão.
        estoque_atual = prod_doc.get("quantidade", 0)

        # Verifica se a quantidade desejada pelo usuário é
        #       maior do que a disponível no estoque.
        # Se for maior, exibe uma mensagem de erro e interrompe a execução.
        if estoque_atual < qtd:
            messagebox.showerror("Erro",
                                 f"Estoque insuficiente para '{nome_prod}'. Estoque atual: {estoque_atual}")
            return

        # Obtém o preço unitário do produto.
        # `prod_doc["preco"]` acessa diretamente a chave "preco" no dicionário do produto.
        preco = prod_doc["preco"]

        # Calcula o subtotal do item, multiplicando o preço
        #       unitário pela quantidade solicitada.
        # Esse valor representa o custo total desse produto para a reserva.
        subtotal = preco * qtd

        # Cria um dicionário contendo as informações do produto consumido.
        # `nome` armazena o nome do produto.
        # `preco` guarda o valor unitário do produto.
        # `quantidade` representa a quantidade consumida.
        # `subtotal` é o valor total do consumo (preço unitário
        #       multiplicado pela quantidade).
        item_consumo = {"nome": nome_prod, "preco": preco, "quantidade": qtd, "subtotal": subtotal}

        # Adiciona o item consumido à lista de consumo da reserva.
        self.lista_consumo.append(item_consumo)

        # Atualiza o estoque no banco de dados, subtraindo a quantidade consumida.
        # `update_one` busca o produto pelo ID e reduz a quantidade disponível.
        produtos_collection.update_one({"_id": prod_doc["_id"]}, {"$inc": {"quantidade": -qtd}})

        # Insere o item consumido na Treeview para exibição na interface gráfica.
        # `nome_prod` é exibido na coluna do nome do produto.
        # `preco` é formatado para duas casas decimais e exibido
        #       na coluna do preço unitário.
        # `qtd` representa a quantidade consumida e é exibida na coluna correspondente.
        # `subtotal` mostra o valor total do item consumido, também
        #       formatado para duas casas decimais.
        self.tree_produtos.insert("",
                                  tk.END,
                                  values=(nome_prod, f"{preco:.2f}", qtd, f"{subtotal:.2f}"))

        # Atualiza o valor total da reserva recalculando
        #       todos os itens consumidos.
        self.recalcular_total()


    def remover_produto(self):

        # Obtém a seleção atual na Treeview.
        sel = self.tree_produtos.selection()

        # Verifica se algum item foi selecionado. Se não
        #       houver seleção, a função retorna.
        if not sel:
            return

        # Obtém os valores do item selecionado na Treeview.
        item_valores = self.tree_produtos.item(sel, "values")

        # Extrai o nome do produto do item selecionado.
        nome = item_valores[0]

        # Extrai a quantidade consumida do item selecionado e
        #       converte para inteiro.
        qtd = int(item_valores[2])

        # Extrai o valor subtotal do item selecionado e converte para float.
        subtotal = float(item_valores[3])

        # Percorre a lista de produtos consumidos na reserva.
        for i, it in enumerate(self.lista_consumo):

            # Verifica se o nome do produto no item da lista
            #       corresponde ao nome do item selecionado.
            if it["nome"] == nome:

                # Verifica se a quantidade do produto na lista corresponde à
                #       quantidade do item selecionado.
                if it["quantidade"] == qtd:

                    # Verifica se o subtotal armazenado na lista é praticamente
                    #       igual ao subtotal do item selecionado.
                    # A verificação de igualdade usa `abs(... - ...) < 1e-9`
                    #       para evitar erros de precisão de ponto flutuante.
                    if abs(it["subtotal"] - subtotal) < 1e-9:

                        # Remove o item da lista de consumo, garantindo que
                        #       ele não seja mais considerado.
                        self.lista_consumo.pop(i)

                        # Sai do loop após encontrar e remover o item correspondente,
                        #       evitando remoção de itens incorretos.
                        break

        # Devolve ao estoque
        # Busca no banco de dados o documento do produto removido,
        #       usando o nome como chave de pesquisa.
        prod_doc = produtos_collection.find_one({"nome": nome})

        # Se o produto for encontrado no banco de dados, significa
        #       que ele existe no estoque.
        if prod_doc:

            # Atualiza a quantidade do produto no banco de dados,
            #       adicionando de volta a quantidade removida.
            # O operador `$inc` incrementa a quantidade do produto no banco de dados.
            produtos_collection.update_one({"_id": prod_doc["_id"]}, {"$inc": {"quantidade": qtd}})

        # Remove a linha correspondente ao produto do `Treeview`,
        #       garantindo que ele não seja mais exibido na interface.
        self.tree_produtos.delete(sel)

        # Recalcula o valor total da reserva após a remoção do produto,
        #       garantindo que o preço final esteja correto.
        self.recalcular_total()


    def recalcular_total(self):

        # Calcula o total gasto com produtos consumidos.
        # Ele percorre todos os itens da lista de consumo (`self.lista_consumo`)
        # e soma os valores da chave "subtotal", que representa o
        #       preço total de cada produto adicionado.
        total_produtos = sum(it["subtotal"] for it in self.lista_consumo)

        try:

            # Converte a string da data de início para um objeto de
            #       data no formato 'YYYY-MM-DD'.
            # Isso permite realizar cálculos com a data.
            dt_ini = datetime.datetime.strptime(self.data_inicio_var.get(), "%Y-%m-%d")

            # Converte a string da data de fim para um objeto de
            #       data no formato 'YYYY-MM-DD'.
            dt_fim = datetime.datetime.strptime(self.data_fim_var.get(), "%Y-%m-%d")

            # Calcula a quantidade de dias entre a data de
            #       entrada e a data de saída.
            dias = (dt_fim - dt_ini).days

            # Garante que, caso o cálculo resulte em menos de 1 dia,
            #       seja considerado pelo menos 1 diária.
            # Isso é necessário porque uma reserva sempre tem, no
            #       mínimo, 1 dia de hospedagem.
            if dias < 1:
                dias = 1

        except:

            # Caso ocorra algum erro na conversão das datas (exemplo: usuário
            #       digitou a data errada ou está vazia),
            #       assume-se que a estadia tem pelo menos 1 dia.
            dias = 1

        # Calcula o valor total da hospedagem multiplicando o preço
        #       base da diária do quarto pelo número de dias.
        total_quarto = self.preco_base_quarto * dias

        # Define o valor total da reserva somando o valor da
        #       hospedagem (quarto) e o total de produtos consumidos.
        self.valor_final_var.set(total_quarto + total_produtos)


    def salvar_reserva(self):

        # Primeiro, verifica se o quarto está disponível para as datas escolhidas.
        # Se não estiver, a função é interrompida.
        if not self.verificar_disponibilidade():
            return

        # Cria um dicionário (estrutura que armazena dados organizados por "chave: valor")
        # contendo todas as informações da reserva que será salva no banco de dados.
        reserva_doc = {

            # Armazena o número do quarto escolhido na reserva.
            "numero_quarto": self.numero_quarto,

            # Lista com os nomes dos hóspedes cadastrados para esta reserva.
            "hospedes": self.lista_hospedes_reserva,

            # Lista com os produtos consumidos durante a hospedagem.
            "produtos": self.lista_consumo,

            # Valor total da reserva, incluindo o custo da
            #       hospedagem e dos produtos consumidos.
            "valor_final": self.valor_final_var.get(),

            # Define o status inicial da reserva como "Aberta".
            # (Pode ser alterado posteriormente para "Finalizada" ou outro estado).
            "status": "Aberta",

            # Observações adicionais que o usuário pode adicionar sobre a reserva.
            "observacoes": self.observacoes_var.get().strip(),

            # Data em que a reserva está sendo criada (data atual do sistema).
            "data_criacao": datetime.datetime.now().strftime("%Y-%m-%d"),

            # Campo vazio para armazenar futuramente a data
            #       de finalização da reserva.
            "data_finalizacao": "",

            # Data de início da reserva escolhida pelo usuário.
            "data_inicio": self.data_inicio_var.get().strip(),

            # Data de fim da reserva escolhida pelo usuário.
            "data_fim": self.data_fim_var.get().strip()

        }

        # Insere o documento (dicionário de dados da reserva)
        #       no banco de dados MongoDB.
        reservas_collection.insert_one(reserva_doc)

        # Exibe uma mensagem informando que a reserva foi criada com sucesso.
        messagebox.showinfo("Sucesso", "Reserva criada com sucesso!")

        # Fecha a janela de criação da reserva após a inserção bem-sucedida.
        self.fechar_janela()

    def verificar_disponibilidade(self):

        # Obtém as datas de início e fim da reserva inseridas pelo
        #       usuário e remove espaços em branco extras.
        dt_ini_str = self.data_inicio_var.get().strip()
        dt_fim_str = self.data_fim_var.get().strip()

        try:

            # Converte as datas de texto (string) para o
            #       formato de data do Python (datetime).
            dt_ini = datetime.datetime.strptime(dt_ini_str, "%Y-%m-%d")
            dt_fim = datetime.datetime.strptime(dt_fim_str, "%Y-%m-%d")

        except:

            # Se houver um erro na conversão (como datas inválidas ou formato incorreto),
            # exibe uma mensagem de erro e retorna False, interrompendo a função.
            messagebox.showerror("Erro", "Datas inválidas.")
            return False

        # Verifica se a data final da reserva é anterior à data inicial.
        # Isso não é permitido, pois a reserva deve sempre começar antes de terminar.
        if dt_fim < dt_ini:

            # Exibe uma mensagem de erro para o usuário informando o
            #       problema com as datas.
            messagebox.showerror("Erro",
                                 "Data final não pode ser antes da data inicial.")

            # Retorna False para indicar que a reserva não pode ser realizada.
            return False

        # Monta a query para buscar reservas ativas que envolvem o mesmo quarto.
        # O objetivo é verificar se já existe uma reserva em
        #       andamento para esse quarto.
        query = {

            # Filtra apenas as reservas que pertencem ao quarto
            #       que está sendo reservado.
            "numero_quarto": self.numero_quarto,

            # Exclui reservas que já foram finalizadas, pois não geram conflito.
            "status": {"$ne": "Finalizada"}

        }

        # Percorre todas as reservas ativas para o mesmo quarto
        #       buscando sobreposições de datas.
        for r in reservas_collection.find(query):

            try:

                # Converte a data de início da reserva armazenada no
                #       banco de dados para um formato de data válido.
                r_dt_ini = datetime.datetime.strptime(r["data_inicio"], "%Y-%m-%d")

                # Converte a data de fim da reserva armazenada no banco de
                #       dados para um formato de data válido.
                r_dt_fim = datetime.datetime.strptime(r["data_fim"], "%Y-%m-%d")

                # Verifica se há sobreposição entre a nova reserva e
                #       reservas já existentes.
                # Se a data inicial da nova reserva for menor ou igual à
                #       data final de uma reserva existente,
                # e a data final da nova reserva for maior ou igual à
                #       data inicial da reserva existente,
                # significa que há um conflito e o quarto já está
                #       ocupado nessas datas.
                if dt_ini <= r_dt_fim and dt_fim >= r_dt_ini:

                    # Exibe uma mensagem de erro informando ao usuário que o
                    #       quarto já está reservado no período.
                    messagebox.showerror(
                        "Erro",
                        f"O quarto {self.numero_quarto} já está reservado de {r['data_inicio']} a {r['data_fim']}."
                    )

                    # Retorna False indicando que a reserva não pode ser
                    #       feita devido ao conflito de datas.
                    return False

            except:

                # Se houver algum erro ao processar as datas (exemplo:
                #       dado corrompido no banco),
                # ignora essa reserva e segue para a próxima.
                pass

        # Se nenhuma reserva existente conflitar com as novas datas,
        #       retorna True, indicando que a reserva pode ser feita.
        return True


    # Inicia o processo de cancelamento da reserva.
    def cancelar_reserva(self):

        # Percorre a lista de produtos consumidos na reserva
        #       para devolvê-los ao estoque.
        for item in self.lista_consumo:

            # Obtém o nome do produto consumido na reserva.
            nome_prod = item["nome"]

            # Obtém a quantidade consumida do produto que
            #       precisa ser devolvida ao estoque.
            qtd = item["quantidade"]

            # Busca o documento do produto no banco de dados
            #       pelo nome para verificar se ele existe.
            prod_doc = produtos_collection.find_one({"nome": nome_prod})

            # Se o produto foi encontrado no banco de dados,
            #       devolve a quantidade ao estoque.
            if prod_doc:

                # Atualiza o estoque do produto, incrementando a
                #       quantidade devolvida.
                produtos_collection.update_one({"_id": prod_doc["_id"]}, {"$inc": {"quantidade": qtd}})

        # Exibe uma mensagem informando que a reserva foi cancelada e os
        #       itens foram devolvidos ao estoque.
        messagebox.showinfo("Cancelado",
                            "Reserva foi cancelada e itens devolvidos ao estoque.")

        # Fecha a janela da reserva após o cancelamento.
        self.fechar_janela()


    # Método responsável por fechar a janela atual e
    #       atualizar as telas que dependem dela.
    def fechar_janela(self):

        # Verifica se a janela pai (a partir da qual esta foi aberta)
        #       possui um método chamado 'atualizar_relatorio'.
        # Isso é útil, pois algumas telas podem precisar recarregar
        #       informações após a reserva ser criada, editada ou cancelada.
        if hasattr(self.pai, 'atualizar_relatorio'):

            # Se o método 'atualizar_relatorio' existir na tela pai, ele é chamado.
            # Esse método pode, por exemplo, atualizar tabelas de
            #       relatórios ou históricos no sistema.
            self.pai.atualizar_relatorio()

        # Verifica se a janela pai também possui um método chamado 'atualizar_mapa'.
        # Esse método pode ser necessário para atualizar o status de
        #       ocupação dos quartos no mapa visual.
        if hasattr(self.pai, 'atualizar_mapa'):

            # Se o método 'atualizar_mapa' existir, ele é chamado para
            #       refletir alterações no status dos quartos.
            # Exemplo: Se uma reserva foi criada, o quarto correspondente
            #       deve ser marcado como ocupado no mapa.
            self.pai.atualizar_mapa()

        # Após garantir que todas as atualizações necessárias
        #       foram feitas, a janela atual é fechada.
        self.destroy()


# =============================================================================
# =========================== TELA DASHBOARD ==================================
# =============================================================================

class TelaDashboard(tk.Frame):
    """
    Tela principal (Dashboard) visível após o login.
    Apresenta botões para as principais funcionalidades: Quartos,
            Produtos, Hóspedes, Relatórios e Mapa de Quartos.
    Mostra também um resumo (quantidade de Quartos e de Reservas).
    """

    # Inicializa a classe `tk.Frame`, que representa um
    #       container dentro da interface gráfica.
    def __init__(self, mestre, permissoes_usuario):
        # `super().__init__(mestre, bg="#f7f7f7")` chama o
        #       construtor da classe pai (`tk.Frame`),
        #       definindo `mestre` como o elemento pai e aplicando um
        #       fundo cinza claro (`#f7f7f7`).
        super().__init__(mestre, bg="#f7f7f7")

        # Define a referência para a janela principal (root).
        # `self.mestre = mestre` armazena a instância da janela
        #       principal para manipulação futura.
        self.mestre = mestre

        # Armazena as permissões do usuário autenticado.
        # `self.permissoes_usuario = permissoes_usuario` permite que o
        #       Dashboard controle quais funcionalidades
        #       estarão disponíveis com base no nível de permissão
        #       do usuário logado.
        self.permissoes_usuario = permissoes_usuario

        # Exibe o frame `TelaDashboard` na interface gráfica.
        # `.pack(fill="both", expand=True)` configura o comportamento do frame:
        # - `fill="both"` faz com que o frame ocupe todo o espaço
        #       disponível na largura e altura.
        # - `expand=True` permite que o frame expanda conforme a janela
        #       principal for redimensionada.
        self.pack(fill="both", expand=True)

        # Cria um rótulo (Label) para exibir o título do Dashboard.
        # - `self`: Define que o rótulo pertence à instância da classe `TelaDashboard`.
        # - `text="DASHBOARD - SISTEMA DE POUSADA"`: Define o texto exibido no
        #       rótulo, informando que a tela é o painel principal do sistema.
        # - `font=("Helvetica", 18, "bold")`: Define a fonte utilizada no rótulo:
        #   - `"Helvetica"`: Fonte do texto.
        #   - `18`: Tamanho da fonte.
        #   - `"bold"`: Deixa o texto em negrito para dar destaque ao título.
        # - `bg="#f7f7f7"`: Define a cor de fundo do rótulo.
        #   - O código hexadecimal `#f7f7f7` corresponde à
        #           cor **branco fumê**, que é um tom muito claro de cinza.
        lbl_titulo = tk.Label(self,
                              text="DASHBOARD - SISTEMA DE POUSADA",
                              font=("Helvetica", 18, "bold"),
                              bg="#f7f7f7")

        # Exibe o rótulo na tela utilizando o método `.pack()`.
        # `.pack(pady=20)` configura o posicionamento do rótulo dentro do layout:
        # - `pady=20`: Adiciona um espaçamento vertical de 20 pixels acima e abaixo do rótulo.
        #   - Esse espaçamento melhora a organização visual e evita que o
        #           título fique muito próximo de outros elementos da tela.
        lbl_titulo.pack(pady=20)

        # Cria um rótulo (Label) para exibir um resumo das informações do
        #       sistema (exemplo: número de quartos disponíveis e reservas ativas).
        # `tk.Label(self, text="", font=("Helvetica", 12), bg="#f7f7f7")`
        # - `self`: O rótulo pertence à instância da classe `TelaDashboard`.
        # - `text=""`: O rótulo é criado inicialmente sem texto, pois seu
        #       conteúdo será atualizado dinamicamente conforme os dados do sistema.
        # - `font=("Helvetica", 12)`: Define a formatação do texto:
        #   - `"Helvetica"`: Fonte utilizada.
        #   - `12`: Tamanho da fonte, um pouco menor que o título, para
        #           diferenciar os elementos visuais da interface.
        # - `bg="#f7f7f7"`: Define a cor de fundo do rótulo.
        #   - O código hexadecimal `#f7f7f7` representa a cor
        #           **branco fumê**, mantendo a mesma identidade visual do Dashboard.
        self.lbl_resumo = tk.Label(self,
                                   text="",
                                   font=("Helvetica", 12),
                                   bg="#f7f7f7")

        # Exibe o rótulo na tela utilizando o método `.pack()`.
        # `.pack(pady=10)` configura o posicionamento do rótulo dentro do layout:
        # - `pady=10`: Adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do rótulo.
        #   - Isso evita que o rótulo fique colado em outros elementos,
        #           tornando a interface mais organizada.
        self.lbl_resumo.pack(pady=10)

        # Cria um frame (container) para organizar os botões do Dashboard.
        # `ttk.Frame(self)` cria um frame dentro da instância `TelaDashboard`,
        #       servindo como um agrupador visual.
        frame_botoes = ttk.Frame(self)

        # Exibe o frame na interface gráfica.
        # `.pack(pady=10)` configura a disposição do frame:
        # - `pady=10`: Adiciona um espaçamento vertical de
        #       10 pixels acima e abaixo do frame.
        #   - Isso evita que os botões fiquem muito próximos dos outros
        #       elementos na tela, melhorando a organização visual.
        frame_botoes.pack(pady=10)

        # Cria um botão para acessar a tela de gerenciamento de quartos.
        # `ttk.Button(frame_botoes, text="Quartos", width=15, command=self.abrir_tela_quartos)`
        # - `frame_botoes`: O botão é inserido dentro do frame criado anteriormente.
        # - `text="Quartos"`: Define o texto exibido no botão, indicando
        #       que ele abrirá a tela de Quartos.
        # - `width=15`: Define a largura do botão, garantindo um tamanho
        #       uniforme e adequado para exibição do texto.
        # - `command=self.abrir_tela_quartos`: Associa a
        #       função `self.abrir_tela_quartos` ao botão,
        #       para que ao ser clicado, a tela correspondente seja aberta.
        btn_quartos = ttk.Button(frame_botoes,
                                 text="Quartos",
                                 width=15,
                                 command=self.abrir_tela_quartos)

        # Posiciona o botão dentro do frame `frame_botoes` utilizando o sistema de layout `grid`.
        # `.grid(row=0, column=0, padx=5, pady=5)` define a posição do botão dentro do frame:
        # - `row=0`: Posiciona o botão na primeira linha do grid dentro do frame.
        # - `column=0`: Posiciona o botão na primeira coluna do grid dentro do frame.
        # - `padx=5, pady=5`: Adiciona um espaçamento de 5 pixels nas
        #       margens horizontal (`padx`) e vertical (`pady`),
        #       evitando que o botão fique colado a outros elementos e
        #       garantindo um layout mais organizado.
        btn_quartos.grid(row=0, column=0, padx=5, pady=5)

        # Cria um botão para acessar a tela de gerenciamento de produtos.
        # `ttk.Button(frame_botoes, text="Produtos", width=15, command=self.abrir_tela_produtos)`
        # - `frame_botoes`: O botão é inserido dentro do frame `frame_botoes`,
        #       garantindo que todos os botões do Dashboard fiquem agrupados.
        # - `text="Produtos"`: Define o texto exibido no botão, indicando
        #       que ele abrirá a tela de Produtos.
        # - `width=15`: Define a largura do botão, garantindo que todos os
        #       botões do Dashboard tenham um tamanho uniforme.
        # - `command=self.abrir_tela_produtos`: Associa a função `self.abrir_tela_produtos` ao botão.
        #   - Isso significa que ao clicar no botão "Produtos", a
        #       tela correspondente será aberta.
        btn_produtos = ttk.Button(frame_botoes,
                                  text="Produtos",
                                  width=15,
                                  command=self.abrir_tela_produtos)

        # Posiciona o botão dentro do frame `frame_botoes` utilizando o sistema de layout `grid`.
        # `.grid(row=0, column=1, padx=5, pady=5)` define a posição do botão dentro do frame:
        # - `row=0`: Posiciona o botão na primeira linha do grid dentro do frame.
        # - `column=1`: Posiciona o botão na segunda coluna do grid
        #       dentro do frame, ao lado do botão "Quartos".
        # - `padx=5, pady=5`: Adiciona um espaçamento de 5 pixels nas
        #       margens horizontal (`padx`) e vertical (`pady`),
        #       garantindo que o botão não fique colado a outros elementos e
        #       mantendo um layout organizado.
        btn_produtos.grid(row=0, column=1, padx=5, pady=5)

        # Cria um botão para acessar a tela de gerenciamento de hóspedes.
        # `ttk.Button(frame_botoes, text="Hóspedes", width=15, command=self.abrir_tela_hospedes)`
        # - `frame_botoes`: O botão é inserido dentro do frame `frame_botoes`,
        #       garantindo que todos os botões do Dashboard fiquem agrupados.
        # - `text="Hóspedes"`: Define o texto exibido no botão, indicando que
        #       ele abrirá a tela de gerenciamento de hóspedes.
        # - `width=15`: Define a largura do botão, garantindo que todos os
        #       botões do Dashboard tenham um tamanho uniforme.
        # - `command=self.abrir_tela_hospedes`: Associa a
        #       função `self.abrir_tela_hospedes` ao botão.
        #   - Isso significa que ao clicar no botão "Hóspedes", a
        #       tela correspondente será aberta.
        btn_hospedes = ttk.Button(frame_botoes,
                                  text="Hóspedes",
                                  width=15,
                                  command=self.abrir_tela_hospedes)

        # Posiciona o botão dentro do frame `frame_botoes` utilizando o sistema de layout `grid`.
        # `.grid(row=1, column=0, padx=5, pady=5)` define a posição do botão dentro do frame:
        # - `row=1`: Posiciona o botão na **segunda linha** do grid dentro do frame.
        # - `column=0`: Posiciona o botão na **primeira coluna** do grid
        #       dentro do frame, abaixo do botão "Quartos".
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels** nas
        #       margens horizontal (`padx`) e vertical (`pady`),
        #   garantindo que o botão não fique colado a outros elementos e
        #       mantendo um layout organizado.
        btn_hospedes.grid(row=1, column=0, padx=5, pady=5)

        # Cria um botão para acessar a tela de relatório geral.
        # `ttk.Button(frame_botoes, text="Relatório Geral", width=15,
        #       command=self.abrir_tela_relatorio)`
        # - `frame_botoes`: O botão é inserido dentro do frame `frame_botoes`,
        #       agrupando-o com os outros botões do Dashboard.
        # - `text="Relatório Geral"`: Define o texto exibido no botão,
        #       indicando que ele abrirá a tela de relatórios.
        # - `width=15`: Define a largura do botão, garantindo que todos os
        #       botões do Dashboard tenham um tamanho uniforme.
        # - `command=self.abrir_tela_relatorio`: Associa a função `self.abrir_tela_relatorio` ao botão.
        #   - Isso significa que ao clicar no botão "Relatório Geral", a
        #       tela correspondente será aberta.
        btn_relatorio = ttk.Button(frame_botoes,
                                   text="Relatório Geral",
                                   width=15,
                                   command=self.abrir_tela_relatorio)

        # Posiciona o botão dentro do frame `frame_botoes` utilizando o sistema de layout `grid`.
        # `.grid(row=1, column=1, padx=5, pady=5)` define a posição do botão dentro do frame:
        # - `row=1`: Posiciona o botão na **segunda linha** do grid dentro do frame.
        # - `column=1`: Posiciona o botão na **segunda coluna** do grid
        #       dentro do frame, ao lado do botão "Hóspedes".
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels** nas
        #       margens horizontal (`padx`) e vertical (`pady`),
        #       garantindo que o botão não fique colado a outros
        #       elementos e mantendo um layout organizado.
        btn_relatorio.grid(row=1, column=1, padx=5, pady=5)

        # Cria um botão para acessar a tela do Mapa de Quartos.
        # - `frame_botoes`: O botão é inserido dentro do frame `frame_botoes`,
        #       agrupando-o com os outros botões do Dashboard.
        # - `text="Mapa de Quartos"`: Define o texto exibido no botão,
        #       indicando que ele abrirá a tela com a visualização dos quartos.
        # - `width=15`: Define a largura do botão, garantindo que todos os
        #       botões do Dashboard tenham um tamanho uniforme.
        # - `command=self.abrir_mapa_quartos`: Associa a função `self.abrir_mapa_quartos` ao botão.
        #   - Isso significa que ao clicar no botão "Mapa de Quartos", a
        #       tela correspondente será aberta.
        btn_mapa = ttk.Button(frame_botoes,
                              text="Mapa de Quartos",
                              width=15,
                              command=self.abrir_mapa_quartos)

        # Posiciona o botão dentro do frame `frame_botoes` utilizando o
        #       sistema de layout `grid`.
        # `.grid(row=2, column=0, columnspan=2, padx=5, pady=5)` define a
        #       posição do botão dentro do frame:
        # - `row=2`: Posiciona o botão na **terceira linha** do grid dentro do frame.
        # - `column=0`: Posiciona o botão na **primeira coluna** do grid dentro do frame.
        # - `columnspan=2`: Faz com que o botão ocupe duas colunas,
        #       centralizando-o no frame `frame_botoes`.
        # - `padx=5, pady=5`: Adiciona um espaçamento de **5 pixels** nas
        #       margens horizontal (`padx`) e vertical (`pady`),
        #       garantindo que o botão não fique colado a outros elementos e
        #       mantendo um layout organizado.
        btn_mapa.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Chama o método `atualizar_resumo()`, que
        #       atualiza o rótulo `self.lbl_resumo`
        #       com um resumo das informações do sistema, como a quantidade de
        #       quartos disponíveis e reservas ativas.
        self.atualizar_resumo()

    def atualizar_resumo(self):
        # Conta o total de quartos cadastrados no banco de dados.
        # `quartos_collection.count_documents({})` retorna o número
        #       total de documentos na coleção `quartos_collection`.
        # O uso de `{}` significa que a consulta está contando todos os
        #       documentos sem nenhum filtro específico.
        total_quartos = quartos_collection.count_documents({})

        # Conta o total de reservas cadastradas no banco de dados.
        # `reservas_collection.count_documents({})` retorna o número
        #       total de documentos na coleção `reservas_collection`.
        # Assim como na contagem de quartos, `{}` indica que todos os
        #       documentos estão sendo contados.
        total_reservas = reservas_collection.count_documents({})

        # Monta a string que será exibida no rótulo `lbl_resumo`.
        # Cria uma string formatada, onde os valores de `total_quartos` e
        #       `total_reservas` são inseridos dinamicamente.
        # - `\n` insere uma quebra de linha, separando as informações
        #       para melhor legibilidade.
        texto_resumo = (
            f"Total de Quartos: {total_quartos}\n"
            f"Total de Reservas: {total_reservas}"
        )

        # Atualiza o texto exibido no rótulo `lbl_resumo`, que mostra o
        #       resumo dos dados na interface.
        # `self.lbl_resumo.config(text=texto_resumo)` altera o
        #       atributo `text` do rótulo `lbl_resumo`,
        #       substituindo o texto atual pelos valores
        #       atualizados de quartos e reservas.
        self.lbl_resumo.config(text=texto_resumo)


    def abrir_tela_quartos(self):

        # Oculta a tela atual do Dashboard removendo-a temporariamente do layout.
        # `self.pack_forget()` remove o frame `TelaDashboard` da interface gráfica,
        # permitindo que outra tela seja exibida no lugar.
        # O frame não é destruído, apenas ocultado.
        self.pack_forget()

        # Cria e exibe a tela de gerenciamento de quartos.
        # `TelaGerenciarQuartos(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaGerenciarQuartos`,
        #       que é responsável por exibir a interface para
        #       adicionar, editar e excluir quartos.
        # - `self.mestre`: Passa a referência da janela principal (root) para a nova tela.
        # - `self.permissoes_usuario`: Mantém as permissões do usuário
        #       autenticado para controlar o acesso às funções da tela.
        TelaGerenciarQuartos(self.mestre, self.permissoes_usuario)

    def abrir_tela_produtos(self):

        # Oculta a tela atual do Dashboard removendo-a temporariamente do layout.
        # `self.pack_forget()` remove o frame `TelaDashboard` da interface gráfica,
        # permitindo que outra tela seja exibida no lugar.
        # O frame não é destruído, apenas ocultado.
        self.pack_forget()

        # Cria e exibe a tela de gerenciamento de produtos.
        # `TelaGerenciarProdutos(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaGerenciarProdutos`,
        #       que é responsável por exibir a interface para
        #       adicionar, editar e excluir produtos.
        # - `self.mestre`: Passa a referência da janela principal (root) para a nova tela.
        # - `self.permissoes_usuario`: Mantém as permissões do usuário autenticado
        #       para controlar o acesso às funções da tela.
        TelaGerenciarProdutos(self.mestre, self.permissoes_usuario)

    def abrir_tela_hospedes(self):

        # Oculta a tela atual do Dashboard removendo-a temporariamente do layout.
        # `self.pack_forget()` remove o frame `TelaDashboard` da interface gráfica,
        # permitindo que outra tela seja exibida no lugar sem destruir o frame.
        self.pack_forget()

        # Cria e exibe a tela de cadastro e gerenciamento de hóspedes.
        # `TelaCadastroHospedes(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaCadastroHospedes`,
        #       que exibe a interface para adicionar,
        #       editar e excluir hóspedes.
        # - `self.mestre`: Passa a referência da janela principal (root) para a nova tela.
        # - `self.permissoes_usuario`: Mantém as permissões do usuário
        #       autenticado para controlar o acesso às funções da tela.
        TelaCadastroHospedes(self.mestre, self.permissoes_usuario)


    def abrir_tela_relatorio(self):

        # Oculta a tela atual do Dashboard removendo-a temporariamente do layout.
        # `self.pack_forget()` remove o frame `TelaDashboard` da interface gráfica,
        # permitindo que outra tela seja exibida no lugar sem destruir o frame.
        self.pack_forget()

        # Cria e exibe a tela de relatórios gerais.
        # `TelaRelatorioGeral(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaRelatorioGeral`,
        #       que exibe estatísticas e informações sobre
        #       quartos, hóspedes e reservas.
        # - `self.mestre`: Passa a referência da janela principal (root) para a nova tela.
        # - `self.permissoes_usuario`: Mantém as permissões do usuário
        #       autenticado para controlar o acesso às funções da tela.
        TelaRelatorioGeral(self.mestre, self.permissoes_usuario)


    def abrir_mapa_quartos(self):

        # Oculta a tela atual do Dashboard removendo-a temporariamente do layout.
        # `self.pack_forget()` remove o frame `TelaDashboard` da interface gráfica,
        # permitindo que outra tela seja exibida no lugar sem destruir o frame.
        self.pack_forget()

        # Cria e exibe a tela do Mapa de Quartos.
        # `TelaMapaQuartos(self.mestre, self.permissoes_usuario)`
        #       instancia a classe `TelaMapaQuartos`,
        #       que exibe a ocupação dos quartos em um
        #       formato visual interativo.
        # - `self.mestre`: Passa a referência da janela principal (root) para a nova tela.
        # - `self.permissoes_usuario`: Mantém as permissões do usuário
        #       autenticado para controlar o acesso às funções da tela.
        TelaMapaQuartos(self.mestre, self.permissoes_usuario)


# =============================================================================
# ============================= TELA DE LOGIN =================================
# =============================================================================

# Criamos uma classe chamada `TelaLogin`, que representa a
#       tela de login do sistema.
# Essa classe herda da classe `tk.Toplevel`, que é usada para
#       criar uma nova janela separada da principal.
class TelaLogin(tk.Toplevel):

    """
    Tela de Login do sistema. Possui campos para inserir usuário e senha, além de:
     - Botão de Login (para autenticação do usuário).
     - Botão de Fechar (fecha o sistema).
     - Botão de Cadastro de Usuários (abre uma tela centralizada para gerenciar usuários).
    """

    # O método `__init__` é chamado automaticamente quando a
    #       classe `TelaLogin` é instanciada.
    # Ele define todas as configurações iniciais da tela de login.
    def __init__(self, mestre=None):

        # Chama o construtor da classe `tk.Toplevel`, garantindo que a
        #       nova janela seja inicializada corretamente.
        super().__init__(mestre)

        # Guarda uma referência à janela principal (caso tenha sido
        #       fornecida) para interações futuras.
        self.mestre = mestre

        # Define o título da janela, que será exibido na barra superior da interface.
        self.title("Sistema de Pousadas - Login")

        # Chama um método personalizado `center_window()` para
        #       centralizar a janela na tela do usuário.
        # Os argumentos `(400, 380)` definem a largura e a altura
        #       da janela em pixels.
        self.center_window(400, 380)

        # Define a cor de fundo da janela como um tom claro de cinza (#f7f7f7).
        self.configure(bg="#f7f7f7")

        # Impede que o usuário redimensione a janela manualmente (nem na
        #       largura nem na altura).
        self.resizable(False, False)

        # Desabilita o botão de fechar (X) no canto superior da janela de login.
        # Isso impede que o usuário feche a tela de login clicando no botão "X".
        # `WM_DELETE_WINDOW` é um evento do Tkinter que captura o fechamento da janela.
        # `self.desabilitar_fechar` é um método (ainda não definido) que será
        #       chamado quando o usuário tentar fechar a janela.
        self.protocol("WM_DELETE_WINDOW", self.desabilitar_fechar)

        # Cria uma variável de controle para armazenar o nome de
        #       usuário digitado no campo de login.
        # `tk.StringVar()` é um objeto do Tkinter que armazena e
        #       monitora mudanças em strings.
        self.login_var = tk.StringVar()

        # Cria uma variável de controle para armazenar a senha
        #       digitada no campo de senha.
        # Assim como `login_var`, essa variável ajudará a capturar a
        #       entrada do usuário e poderá ser usada para autenticação.
        self.senha_var = tk.StringVar()

        # Cria um frame (`ttk.Frame`) chamado `cont_principal`, que servirá
        #       como um contêiner para os elementos da tela de login.
        # Um `Frame` funciona como uma "caixa" que organiza e agrupa
        #       outros widgets dentro da interface.
        cont_principal = ttk.Frame(self)

        # Posiciona o frame `cont_principal` dentro da janela da tela de login.
        # `fill="both"` permite que o frame se expanda tanto na largura quanto na altura.
        # `expand=True` faz com que o frame ocupe todo o espaço disponível dentro da janela.
        # `padx=20, pady=20` adicionam um espaçamento de 20 pixels nas
        #       margens horizontais (esquerda/direita) e verticais (topo/baixo).
        cont_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Cria um rótulo (`Label`) chamado `lbl_titulo`, que exibirá o título da tela de login.
        # Esse rótulo serve para indicar que a tela é para acesso ao sistema.
        lbl_titulo = tk.Label(

            # Define que o rótulo será inserido dentro do frame `cont_principal`.
            cont_principal,

            # Define o texto que será exibido no rótulo.
            text="ACESSO AO SISTEMA",

            # Define a fonte do texto: Helvetica, tamanho 16, em negrito.
            font=("Helvetica", 16, "bold"),

            # Define a cor de fundo do rótulo como um tom claro de
            #       cinza (#f7f7f7), igual à cor da janela.
            bg="#f7f7f7"

        )

        # Posiciona o rótulo `lbl_titulo` dentro do frame `cont_principal`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do rótulo.
        lbl_titulo.pack(pady=10)

        # Cria um novo frame (`ttk.Frame`) chamado `frm_form` dentro do
        #       contêiner `cont_principal`.
        # Esse frame será usado para organizar os campos de entrada do
        #       formulário de login (Usuário e Senha).
        frm_form = ttk.Frame(cont_principal)

        # Posiciona o frame `frm_form` dentro do `cont_principal` usando o método `pack()`.
        # `pady=10` adiciona um espaçamento de 10 pixels acima e abaixo do frame.
        # `padx=10` adiciona um espaçamento de 10 pixels nas laterais
        #       esquerda e direita do frame.
        frm_form.pack(pady=10, padx=10)

        # Cria um rótulo (`Label`) dentro do frame `frm_form` com o texto "Usuário:".
        # Esse rótulo serve para indicar o campo onde o usuário deve
        #       inserir seu nome de login.
        # `grid(row=0, column=0)` posiciona o rótulo na **primeira linha (row=0) e
        #       primeira coluna (column=0)** da grade do frame.
        # `sticky="e"` alinha o rótulo à direita da célula, garantindo que ele
        #       fique encostado na caixa de entrada ao lado.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels em todas as direções
        #       para melhorar a organização dos elementos.
        ttk.Label(frm_form,
                  text="Usuário:").grid(row=0, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (`Entry`) onde o usuário digitará seu nome de login.
        # O argumento `textvariable=self.login_var` associa o campo à variável `self.login_var`,
        # garantindo que o texto digitado possa ser recuperado para validação do login.
        # `width=30` define a largura do campo de entrada
        #       como **30 caracteres**, tornando-o mais legível.
        # `grid(row=0, column=1)` posiciona o campo de entrada na **primeira
        #       linha (row=0) e segunda coluna (column=1)** da grade.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels para não
        #       deixar os elementos muito colados.
        ttk.Entry(frm_form,
                  textvariable=self.login_var,
                  width=30).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo (`Label`) dentro do frame `frm_form` com o texto "Senha:".
        # Esse rótulo serve para indicar o campo onde o usuário deve inserir sua senha.
        # `grid(row=1, column=0)` posiciona o rótulo na **segunda linha (row=1) e
        #       primeira coluna (column=0)** da grade.
        # `sticky="e"` alinha o rótulo à direita da célula, garantindo que ele
        #       fique próximo à caixa de entrada da senha.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao redor do
        #       rótulo para melhor organização.
        ttk.Label(frm_form,
                  text="Senha:").grid(row=1, column=0, sticky="e", padx=5, pady=5)

        # Cria um campo de entrada (`Entry`) onde o usuário digitará sua senha.
        # O argumento `textvariable=self.senha_var` associa o campo à variável `self.senha_var`,
        # permitindo que o valor digitado seja recuperado posteriormente para validação do login.
        # `show="*"` oculta os caracteres digitados, exibindo apenas
        #       asteriscos (*), para proteger a senha.
        # `width=30` define a largura do campo de entrada como **30 caracteres**,
        #       garantindo espaço suficiente para digitação.
        # `grid(row=1, column=1)` posiciona o campo de entrada na **segunda
        #       linha (row=1) e segunda coluna (column=1)** da grade.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao redor do campo
        #       para evitar que os elementos fiquem muito próximos.
        ttk.Entry(frm_form,
                  textvariable=self.senha_var,
                  show="*",
                  width=30).grid(row=1, column=1, padx=5, pady=5)

        # Cria um botão chamado `btn_login` dentro do frame `cont_principal`.
        # Esse botão será usado para que o usuário tente entrar no
        #       sistema após digitar login e senha.
        # `text="Entrar"` define o texto exibido no botão.
        # `width=20` define a largura do botão como 20 caracteres,
        #       garantindo um tamanho fixo.
        # `command=self.fazer_login` associa a ação de login ao botão.
        # Quando o usuário clicar no botão, o método `self.fazer_login`
        #       será executado para validar as credenciais.
        btn_login = ttk.Button(cont_principal,
                               text="Entrar",
                               width=20,
                               command=self.fazer_login)

        # Posiciona o botão `btn_login` dentro do frame `cont_principal`.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       acima e abaixo do botão, garantindo que ele não fique
        #       muito colado nos outros elementos.
        btn_login.pack(pady=5)

        # ==========================
        # Botão para abrir a tela de Gerenciamento de Usuários
        # ==========================

        # Cria um botão chamado `btn_cadastro_usuarios`, também
        #       dentro do frame `cont_principal`.
        # Esse botão permitirá que o usuário abra uma tela de cadastro e
        #       gerenciamento de usuários.
        # `text="Cadastrar Usuários"` define o texto exibido no botão.
        # `width=20` define a largura do botão como 20 caracteres, garantindo
        #       um tamanho consistente com o botão de login.
        # `command=self.abrir_tela_usuarios_no_login` associa a ação de
        #       abrir a tela de usuários ao botão.
        # Quando o usuário clicar, o método `self.abrir_tela_usuarios_no_login` será chamado.
        btn_cadastro_usuarios = ttk.Button(cont_principal,
                                           text="Cadastrar Usuários",
                                           width=20,
                                           command=self.abrir_tela_usuarios_no_login)

        # Posiciona o botão `btn_cadastro_usuarios` dentro do frame `cont_principal`.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do botão,
        # garantindo que ele não fique muito colado nos outros elementos.
        btn_cadastro_usuarios.pack(pady=5)

        # ==========================
        # Botão para Fechar o Sistema
        # ==========================

        # Cria um botão chamado `btn_fechar`, dentro do frame `cont_principal`.
        # Esse botão permitirá que o usuário feche o sistema de login.
        # `text="Fechar"` define o texto exibido no botão.
        # `width=20` define a largura do botão como 20 caracteres, garantindo um
        #       tamanho consistente com os outros botões.
        # `command=self.fechar_sistema` associa a ação de fechar o sistema ao botão.
        # Quando o usuário clicar, o método `self.fechar_sistema` será
        #       chamado para encerrar a aplicação.
        btn_fechar = ttk.Button(cont_principal,
                                text="Fechar",
                                width=20,
                                command=self.fechar_sistema)

        # Posiciona o botão `btn_fechar` dentro do frame `cont_principal`.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do botão,
        # garantindo que ele fique visualmente separado dos outros elementos da interface.
        btn_fechar.pack(pady=5)

    # Esse método verifica se os campos de login e senha estão preenchidos e
    #       busca o usuário no banco de dados.
    def fazer_login(self):

        # Obtém o valor digitado no campo de login.
        # `self.login_var.get()` pega o texto digitado pelo usuário.
        # `.strip()` remove espaços extras no início e no fim do texto.
        login_digitado = self.login_var.get().strip()

        # Obtém o valor digitado no campo de senha.
        # `self.senha_var.get()` pega o texto digitado pelo usuário.
        # `.strip()` remove espaços extras no início e no fim do texto.
        senha_digitada = self.senha_var.get().strip()

        # Verifica se os campos de login ou senha estão vazios.
        # Se o usuário não preencher algum dos campos, exibe uma
        #       mensagem de erro e interrompe o login.
        if not login_digitado or not senha_digitada:
            # Exibe uma mensagem de erro para o usuário usando `messagebox.showerror`.
            # "Erro" → Título da mensagem.
            # "Por favor, preencha os campos de usuário e senha." → Texto exibido no alerta.
            messagebox.showerror("Erro",
                                 "Por favor, preencha os campos de usuário e senha.")

            # `return` interrompe a execução da função para evitar que o
            #       sistema continue sem os dados necessários.
            return

        # Busca no banco de dados MongoDB um usuário cujo login seja igual ao digitado.
        # `usuarios_collection.find_one({"login": login_digitado})` faz uma
        #       consulta no banco e retorna o primeiro usuário encontrado.
        # Se nenhum usuário for encontrado, `usuario` receberá `None`.
        usuario = usuarios_collection.find_one({"login": login_digitado})

        # Verifica se o usuário foi encontrado no banco de dados.
        # Se `usuario` não for `None`, significa que o login digitado existe no sistema.
        if usuario:

            # Obtém a senha cadastrada para esse usuário no banco de dados.
            # `usuario.get("senha", "")` tenta pegar a senha do usuário no banco.
            # Se a chave "senha" não existir, retorna uma string vazia ("").
            senha_correta = usuario.get("senha", "")

            # Obtém o nível de permissões do usuário (ex.: administrador, recepcionista, etc.).
            # `usuario.get("permissoes", "recepcionista")` busca a chave "permissoes" no banco.
            # Se o usuário não tiver uma permissão definida, assume "recepcionista" como padrão.
            permissoes = usuario.get("permissoes", "recepcionista")

            # Verifica se a senha digitada pelo usuário corresponde à
            #       senha armazenada no banco.
            if senha_digitada == senha_correta:

                # Exibe uma mensagem informando que o login foi bem-sucedido.
                # O `messagebox.showinfo()` exibe uma janela de informação
                #       com uma mensagem de boas-vindas.
                # `f"Bem-vindo(a), {login_digitado}!"` personaliza a mensagem com o nome do usuário.
                messagebox.showinfo("Sucesso",
                                    f"Bem-vindo(a), {login_digitado}!")

                # Chama o método `exibir_dashboard()` da janela principal (`mestre`).
                # Passa as permissões do usuário para determinar quais
                #       funcionalidades ele pode acessar.
                self.mestre.exibir_dashboard(permissoes)

                # Fecha a janela de login após o login bem-sucedido.
                self.destroy()

            else:

                # Se a senha digitada estiver incorreta, exibe uma mensagem de erro.
                messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")

        # Caso o login não tenha sido encontrado no banco de dados,
        #       exibe uma mensagem de erro.
        else:
            messagebox.showerror("Erro",
                                 "Usuário não encontrado. Verifique os dados.")

    # Define um método chamado `abrir_tela_usuarios_no_login`.
    # Esse método será chamado quando o usuário clicar no
    #       botão "Cadastrar Usuários" na tela de login.
    def abrir_tela_usuarios_no_login(self):

        """
        Abre uma nova janela (Toplevel) para gerenciar usuários
                sem a necessidade de fazer login.
        Essa tela permite cadastrar, alterar e excluir usuários
                diretamente da tela de login.
        """

        # Cria uma instância da classe `GerenciarUsuariosWindow`, que
        #       representa a tela de gerenciamento de usuários.
        # `self` (a tela de login) é passado como argumento, tornando a
        #       tela de login a "janela mãe" da nova janela.
        GerenciarUsuariosWindow(self)

    # ==========================
    # Método para Fechar o Sistema
    # ==========================

    # Define um método chamado `fechar_sistema`, que encerra
    #       completamente o programa.
    def fechar_sistema(self):

        """Encerra totalmente o programa."""

        # `self.mestre.destroy()` fecha a janela principal do programa.
        # `mestre` representa a janela principal da aplicação (passada
        #       como argumento ao iniciar a tela de login).
        # Quando essa janela principal é destruída, todo o programa é encerrado.
        self.mestre.destroy()

    # ==========================
    # Método para Desabilitar o Botão Fechar (X)
    # ==========================

    # Define um método chamado `desabilitar_fechar`, que impede o
    #       fechamento da tela de login pelo botão "X".
    def desabilitar_fechar(self):

        """Bloqueia o botão de fechar (X) da janela de login."""

        # O método `pass` significa que essa função não faz nada quando chamada.
        # Isso impede que a janela seja fechada quando o usuário clica no botão "X".
        pass

    # Define um método chamado `center_window` que centraliza a
    #       janela na tela do usuário.
    # Esse método recebe dois parâmetros: `largura` e `altura`,
    #       que representam as dimensões da janela.
    def center_window(self, largura, altura):

        # Obtém a largura total da tela do usuário.
        # `winfo_screenwidth()` retorna a largura em pixels do monitor
        #       onde a aplicação está sendo executada.
        larg_tela = self.winfo_screenwidth()

        # Obtém a altura total da tela do usuário.
        # `winfo_screenheight()` retorna a altura em pixels do monitor.
        alt_tela = self.winfo_screenheight()

        # Calcula a posição X para centralizar a janela horizontalmente.
        # `(larg_tela - largura) / 2` pega a largura total da tela e
        #       subtrai a largura da janela.
        # Dividindo por 2, encontramos a posição exata para centralizar.
        # `int(...)` converte o valor para um número inteiro, pois `geometry`
        #       não aceita números decimais.
        x = int((larg_tela - largura) / 2)

        # Calcula a posição Y para centralizar a janela verticalmente.
        # `(alt_tela - altura) / 2` pega a altura total da tela e
        #       subtrai a altura da janela.
        # Dividindo por 2, encontramos a posição exata para que a
        #       janela fique centralizada verticalmente.
        y = int((alt_tela - altura) / 2)

        # Define o tamanho e a posição da janela usando `geometry()`.
        # O formato da string é: `"largura x altura + posição_x + posição_y"`.
        # Isso posiciona a janela no centro exato da tela.
        self.geometry(f"{largura}x{altura}+{x}+{y}")


# =============================================================================
# =========== TELA DE GERENCIAMENTO DE USUÁRIOS (JANELA TOPOLEVEL) ============
# =============================================================================
# ============================================
# Classe `GerenciarUsuariosWindow` - Tela de Gerenciamento de Usuários
# ============================================

# Define uma classe chamada `GerenciarUsuariosWindow`, que representa a
#       tela onde os usuários podem ser gerenciados.
# Essa classe herda de `tk.Toplevel`, o que significa que ela cria
#       uma nova janela independente da principal.
class GerenciarUsuariosWindow(tk.Toplevel):
    """
    Tela de Gerenciamento de Usuários (CRUD) aberta a partir da Tela de Login.
    Exibe um `Treeview` com todos os usuários e permite cadastrar,
            alterar e excluir usuários.
    """

    # O método `__init__` inicializa a janela de gerenciamento de usuários.
    # O parâmetro `mestre` representa a janela que chamou essa tela (pode
    #       ser a tela de login ou outra tela).
    def __init__(self, mestre=None):

        # Chama o construtor da classe `tk.Toplevel`, garantindo que a
        #       nova janela seja inicializada corretamente.
        super().__init__(mestre)

        # Define o título da janela, que será exibido na barra superior.
        self.title("Gerenciar Usuários")

        # Chama o método `center_window()` para centralizar a janela na tela do usuário.
        # Os argumentos `(600, 400)` definem a largura (600px) e a altura (400px) da janela.
        self.center_window(600, 400)

        # Define a cor de fundo da janela como um tom claro de cinza (#f7f7f7).
        # Isso melhora a aparência e a legibilidade da interface.
        self.configure(bg="#f7f7f7")

        # Impede que o usuário redimensione a janela manualmente.
        # `False, False` significa que a janela não pode ser
        #       redimensionada nem na largura nem na altura.
        self.resizable(False, False)

        # ==========================
        # Variáveis para armazenar os dados do formulário
        # ==========================

        # Cria uma variável de controle para armazenar o nome de login do usuário.
        # `tk.StringVar()` permite associar essa variável ao campo de entrada (`Entry`),
        # garantindo que o valor digitado seja armazenado e possa
        #       ser recuperado posteriormente.
        self.login_var = tk.StringVar()

        # Cria uma variável de controle para armazenar a senha do usuário.
        # Assim como `login_var`, essa variável será associada ao
        #       campo de entrada da senha.
        self.senha_var = tk.StringVar()

        # Cria uma variável de controle para armazenar o nível de permissões do usuário.
        # `tk.StringVar(value="recepcionista")` define "recepcionista" como valor padrão.
        # Isso significa que, caso o usuário não escolha outra opção,
        #       ele será cadastrado como recepcionista.
        self.permissoes_var = tk.StringVar(value="recepcionista")

        # ==========================
        # Criando um Frame para os campos de edição
        # ==========================

        # Cria um frame (`ttk.Frame`) chamado `frm_campos`, que será usado
        #       para agrupar os campos de entrada do formulário.
        # Esse frame ajuda a organizar a interface e mantém os
        #       elementos agrupados de forma mais estruturada.
        frm_campos = ttk.Frame(self)

        # Posiciona o frame `frm_campos` dentro da janela principal.
        # `pady=10` adiciona um espaçamento de 10 pixels acima e abaixo do frame.
        # `padx=10` adiciona um espaçamento de 10 pixels nas laterais,
        #       para evitar que os campos fiquem colados nas bordas da janela.
        # `fill="x"` faz com que o frame se expanda horizontalmente,
        #       ocupando toda a largura disponível.
        frm_campos.pack(pady=10, padx=10, fill="x")

        # Cria um rótulo (`Label`) dentro do frame `frm_campos` para identificar o campo de login.
        # O rótulo exibe o texto "Login (E-mail ou Nome):" para orientar o
        #       usuário sobre o que deve ser digitado.
        # `grid(row=0, column=0)` posiciona o rótulo na **primeira
        #       linha (row=0) e primeira coluna (column=0)** do frame.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao redor do
        #       rótulo para melhorar a organização da interface.
        # `sticky="e"` alinha o rótulo à direita da célula, garantindo
        #       que ele fique encostado na caixa de entrada ao lado.
        ttk.Label(frm_campos,
                  text="Login (E-mail ou Nome):").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) onde o usuário pode
        #       digitar seu login (e-mail ou nome).
        # `textvariable=self.login_var` associa o campo de entrada à variável `self.login_var`,
        #       garantindo que qualquer texto digitado seja armazenado e
        #       possa ser recuperado depois.
        # `width=25` define a largura do campo como **25 caracteres**,
        #       garantindo que o usuário tenha espaço suficiente para digitar.
        # `grid(row=0, column=1)` posiciona o campo de entrada na **primeira linha (row=0) e
        #       segunda coluna (column=1)** do frame.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao redor do
        #       campo para evitar que os elementos fiquem muito próximos.
        ttk.Entry(frm_campos,
                  textvariable=self.login_var,
                  width=25).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo (`Label`) dentro do frame `frm_campos` para indicar o campo de senha.
        # O rótulo exibe o texto "Senha:" para informar ao usuário
        #       onde deve digitar sua senha.
        # `grid(row=1, column=0)` posiciona o rótulo na **segunda linha (row=1) e
        #       primeira coluna (column=0)** do frame.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao redor do
        #       rótulo para manter um layout organizado.
        # `sticky="e"` alinha o rótulo à direita da célula, garantindo que
        #       ele fique encostado na caixa de entrada ao lado.
        ttk.Label(frm_campos,
                  text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) onde o usuário pode digitar sua senha.
        # `textvariable=self.senha_var` associa o campo de
        #       entrada à variável `self.senha_var`,
        #       garantindo que qualquer senha digitada seja armazenada corretamente.
        # `show="*"` oculta os caracteres digitados, exibindo apenas
        #       asteriscos (*), para proteger a senha.
        # `width=25` define a largura do campo como **25 caracteres**,
        #       garantindo um tamanho adequado.
        # `grid(row=1, column=1)` posiciona o campo de entrada
        #       na **segunda linha (row=1) e segunda coluna (column=1) do frame.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao
        #       redor do campo para garantir um layout organizado.
        ttk.Entry(frm_campos,
                  textvariable=self.senha_var,
                  show="*",
                  width=25).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo (`Label`) dentro do frame `frm_campos`
        #       para indicar o campo de permissões.
        # O rótulo exibe o texto "Permissão:" para informar ao
        #       usuário que ele pode selecionar um nível de acesso.
        # `grid(row=2, column=0)` posiciona o rótulo na terceira
        #       linha (row=2) e primeira coluna (column=0)** do frame.
        # `padx=5, pady=5` adicionam espaçamentos de 5 pixels ao redor do
        #       rótulo para manter o layout bem distribuído.
        # `sticky="e"` alinha o rótulo à direita da célula, garantindo
        #       que ele fique encostado no menu suspenso ao lado.
        ttk.Label(frm_campos,
                  text="Permissão:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um menu suspenso (`Combobox`) chamado `combo_perm`
        #       para selecionar o nível de permissão do usuário.
        # `frm_campos` → O Combobox será colocado dentro do
        #       frame `frm_campos`, que agrupa os campos do formulário.
        # `textvariable=self.permissoes_var` → Associa o Combobox à
        #       variável `self.permissoes_var`,
        #       garantindo que a opção selecionada seja armazenada
        #       corretamente e possa ser usada depois.
        # `values=["gerente", "recepcionista"]` → Define as opções
        #       disponíveis no menu suspenso:
        #     - "gerente" → Tem acesso total ao sistema.
        #     - "recepcionista" → Tem acesso limitado a algumas funções do sistema.
        # `state="readonly"` → Define que o usuário só pode escolher entre as
        #       opções fornecidas e não pode digitar manualmente um valor diferente.
        # `width=23` → Define a largura do Combobox como 23 caracteres,
        #       garantindo que ele se alinhe bem ao layout da interface.
        combo_perm = ttk.Combobox(frm_campos,
                                  textvariable=self.permissoes_var,
                                  values=["gerente", "recepcionista"],
                                  state="readonly",
                                  width=23)

        # Posiciona o Combobox `combo_perm` dentro do frame `frm_campos`.
        # `grid(row=2, column=1)` → Coloca o Combobox na **terceira
        #       linha (row=2) e segunda coluna (column=1)** do frame.
        # `padx=5, pady=5` → Adiciona um espaçamento de 5 pixels ao redor do
        #       Combobox para manter um layout organizado.
        combo_perm.grid(row=2, column=1, padx=5, pady=5)

        # Cria um frame (`ttk.Frame`) chamado `frm_botoes`, que será
        #       usado para organizar os botões de ação.
        # Esse frame será colocado dentro de `frm_campos`, onde já estão os
        #       outros campos do formulário.
        frm_botoes = ttk.Frame(frm_campos)

        # Posiciona o frame `frm_botoes` dentro do frame `frm_campos` usando `grid()`.
        # `row=3, column=0, columnspan=2` → Coloca o frame na **quarta linha (row=3),
        #       ocupando duas colunas (columnspan=2)**.
        # `pady=10` → Adiciona um espaçamento vertical de 10 pixels abaixo do
        #       frame, garantindo que os botões não fiquem colados nos campos acima.
        frm_botoes.grid(row=3, column=0, columnspan=2, pady=10)

        # Cria um botão chamado `btn_salvar`, que será usado para cadastrar
        #       ou atualizar um usuário.
        # `frm_botoes` → O botão será colocado dentro do frame `frm_botoes`,
        #       onde todos os botões de ação ficarão agrupados.
        # `text="Cadastrar / Atualizar"` → Define o texto exibido no botão,
        #       indicando sua funcionalidade dupla.
        # `command=self.cadastrar_ou_atualizar` → Define que, quando o botão for
        #       clicado, o método `cadastrar_ou_atualizar()` será chamado.
        # Esse método será responsável por cadastrar um novo usuário ou
        #       atualizar um usuário já existente no banco de dados.
        btn_salvar = ttk.Button(frm_botoes,
                                text="Cadastrar / Atualizar",
                                command=self.cadastrar_ou_atualizar)

        # Posiciona o botão `btn_salvar` dentro do frame `frm_botoes`.
        # `pack(side="left")` → Posiciona o botão no lado esquerdo do
        #       frame, garantindo um layout organizado.
        # `padx=5` → Adiciona um espaçamento horizontal de 5 pixels entre os
        #       botões para evitar que fiquem colados.
        btn_salvar.pack(side="left", padx=5)

        # Cria um botão chamado `btn_excluir`, que será usado para
        #       excluir um usuário do banco de dados.
        # `frm_botoes` → O botão será colocado dentro do frame `frm_botoes`, ao
        #       lado do botão de salvar.
        # `text="Excluir"` → Define o texto exibido no botão, indicando
        #       que ele remove um usuário.
        # `command=self.excluir_usuario` → Define que, quando o botão for clicado, o
        #       método `excluir_usuario()` será chamado.
        # Esse método será responsável por remover o usuário selecionado no banco de dados.
        btn_excluir = ttk.Button(frm_botoes,
                                 text="Excluir",
                                 command=self.excluir_usuario)

        # Posiciona o botão `btn_excluir` dentro do frame `frm_botoes`, ao
        #       lado do botão de salvar.
        # `pack(side="left")` → Posiciona o botão no lado esquerdo do
        #       frame, garantindo um layout alinhado.
        # `padx=5` → Adiciona um espaçamento horizontal de 5 pixels entre os
        #       botões para manter um layout organizado.
        btn_excluir.pack(side="left", padx=5)

        # Cria um `Treeview` chamado `tree_usuarios`, que será usado para
        #       exibir a lista de usuários cadastrados.
        # `self` → O Treeview será colocado diretamente dentro da
        #       janela `GerenciarUsuariosWindow`.
        # `columns=("login", "senha", "permissoes", "id")` → Define as colunas da tabela.
        #     - "login" → Armazena o e-mail ou nome de login do usuário.
        #     - "senha" → Armazena a senha do usuário (exibida como texto,
        #           mas idealmente deveria ser protegida).
        #     - "permissoes" → Armazena o nível de permissão do
        #           usuário (exemplo: "gerente" ou "recepcionista").
        #     - "id" → Identificador único do usuário (gerado pelo MongoDB).
        # `show="headings"` → Exibe apenas os cabeçalhos das colunas, sem uma
        #       coluna extra vazia na esquerda.
        self.tree_usuarios = ttk.Treeview(self,
                                          columns=("login", "senha", "permissoes", "id"),
                                          show="headings")

        # Define o título da coluna "login" como "Login".
        # Isso será exibido no cabeçalho da tabela.
        self.tree_usuarios.heading("login", text="Login")

        # Define o título da coluna "senha" como "Senha".
        # Como as senhas estão armazenadas em texto, elas ficarão visíveis na
        #       tabela (o ideal seria armazená-las de forma segura no banco).
        self.tree_usuarios.heading("senha", text="Senha")

        # Define o título da coluna "permissoes" como "Permissão".
        # Essa coluna exibirá os níveis de acesso de cada
        #       usuário (exemplo: "gerente", "recepcionista").
        self.tree_usuarios.heading("permissoes", text="Permissão")

        # Define o título da coluna "id" como "ID (oculto)".
        # O ID é um identificador único gerado pelo MongoDB para cada usuário.
        self.tree_usuarios.heading("id", text="ID (oculto)")

        # Define a largura da coluna "id" como 0 pixels e impede que
        #       ela seja redimensionada (`stretch=False`).
        # Isso garante que a coluna fique oculta, pois o ID não
        #       precisa ser visível na interface.
        self.tree_usuarios.column("id", width=0, stretch=False)

        # Posiciona o `Treeview` dentro da janela `GerenciarUsuariosWindow` usando `pack()`.
        # `fill="both"` → Expande o Treeview para ocupar todo o espaço
        #       disponível horizontal e verticalmente.
        # `expand=True` → Permite que o Treeview se ajuste ao tamanho da
        #       janela caso ela seja redimensionada.
        # `padx=10, pady=10` → Adiciona um espaçamento de 10 pixels ao
        #       redor da tabela para evitar que ela fique colada nas bordas.
        self.tree_usuarios.pack(fill="both", expand=True, padx=10, pady=10)

        # Associa um evento ao `Treeview`, que será ativado quando o
        #       usuário der um **duplo clique** em um item da tabela.
        # `"<Double-1>"` → Indica um evento de **duplo clique com o
        #       botão esquerdo do mouse**.
        # `self.selecionar_usuario` → Quando o duplo clique for detectado, o
        #       método `selecionar_usuario()` será chamado.
        self.tree_usuarios.bind("<Double-1>", self.selecionar_usuario)

        # Cria uma variável chamada `usuario_em_edicao` e define
        #       seu valor inicial como `None`.
        # Essa variável será usada para armazenar o usuário
        #       atualmente em edição na interface.
        self.usuario_em_edicao = None

        # Chama o método `listar_usuarios()`, que será responsável por
        #       carregar e exibir na tabela todos os usuários
        #       cadastrados no banco de dados.
        self.listar_usuarios()

    # Define um método chamado `listar_usuarios`, que busca todos os
    #       usuários do banco de dados
    #       e os exibe na tabela (`Treeview`).
    def listar_usuarios(self):

        # `self.tree_usuarios.get_children()` retorna todos os itens
        #       atualmente listados no Treeview.
        # Para evitar duplicações ao atualizar a lista de usuários, é necessário
        #       remover todos os itens antes de recarregar os dados.
        for item in self.tree_usuarios.get_children():
            # `self.tree_usuarios.delete(item)` remove cada item do Treeview.
            self.tree_usuarios.delete(item)

        # Faz uma consulta ao banco de dados MongoDB para obter todos os usuários cadastrados.
        # `usuarios_collection.find()` retorna todos os documentos da coleção "usuarios".
        for u in usuarios_collection.find():
            # Adiciona um novo usuário ao Treeview usando `insert()`.
            # O método `insert()` recebe os seguintes parâmetros:
            # `""` → Define que o item não terá um pai (pois estamos adicionando
            #       itens na raiz da árvore).
            # `tk.END` → Insere o novo item no final da lista.
            # `values=(...)` → Define os valores a serem exibidos nas colunas do Treeview.
            self.tree_usuarios.insert("", tk.END, values=(

                u.get("login", ""),  # Obtém o login do usuário (ou uma string vazia se não existir).
                u.get("senha", ""),  # Obtém a senha do usuário (exibida em texto, o ideal seria ocultar).
                u.get("permissoes", ""),  # Obtém a permissão do usuário (exemplo: "gerente", "recepcionista").
                str(u["_id"])

                # Converte o ID do usuário para string antes de inseri-lo
                #       (o ID geralmente é um ObjectId).
            ))

    # Define um método chamado `selecionar_usuario`, que permite
    #       carregar os dados de um usuário
    #       para edição ao dar um **duplo clique** em um item do Treeview.
    # O parâmetro `event` representa o evento de clique que acionou a função.
    def selecionar_usuario(self, event):

        # `self.tree_usuarios.selection()` → Retorna a seleção do usuário no `Treeview`.
        # Se nenhum usuário estiver selecionado, a variável `selecao` será uma tupla vazia.
        selecao = self.tree_usuarios.selection()

        # Se nenhum usuário foi selecionado, a função é encerrada sem fazer nada.
        if not selecao:
            return

        # `self.tree_usuarios.item(selecao, "values")` → Obtém os
        #       valores do usuário selecionado no Treeview.
        # O retorno é uma tupla contendo (login, senha, permissão, id).
        valores = self.tree_usuarios.item(selecao, "values")

        # `self.login_var.set(valores[0])` → Define o campo de login com o
        #       valor armazenado na primeira posição da tupla (`valores[0]`).
        self.login_var.set(valores[0])  # Login do usuário

        # `self.senha_var.set(valores[1])` → Define o campo de senha com o valor
        #       armazenado na segunda posição da tupla (`valores[1]`).
        # Senha do usuário (exibida como texto, idealmente deveria ser oculta)
        self.senha_var.set(valores[1])

        # `self.permissoes_var.set(valores[2])` → Define o campo de permissões
        #       com o valor armazenado na terceira posição da tupla (`valores[2]`).
        # Permissão do usuário (exemplo: "gerente", "recepcionista")
        self.permissoes_var.set(valores[2])

        # Converte a string do ID (`valores[3]`) para um `ObjectId`, que é
        #       o formato correto do MongoDB.
        # Isso permite que o usuário seja atualizado posteriormente no banco de dados.
        self.usuario_em_edicao = ObjectId(valores[3])

    # Define um método chamado `cadastrar_ou_atualizar`, que permite
    #       cadastrar um novo usuário ou atualizar os dados de um usuário já existente.
    def cadastrar_ou_atualizar(self):

        # `self.login_var.get().strip()` → Obtém o valor digitado no campo de
        #       login e remove espaços extras no início e no final.
        login_novo = self.login_var.get().strip()

        # `self.senha_var.get().strip()` → Obtém o valor digitado no campo de
        #       senha e remove espaços extras no início e no final.
        senha_nova = self.senha_var.get().strip()

        # `self.permissoes_var.get()` → Obtém a permissão selecionada no Combobox.
        permissao = self.permissoes_var.get()

        # Se o login ou a senha estiverem vazios, exibe uma mensagem de
        #       erro e interrompe o processo.
        if not login_novo or not senha_nova:
            # `messagebox.showerror("Erro", "Campos 'Login' e 'Senha' são obrigatórios.")`
            # Exibe uma caixa de erro informando que esses campos não podem estar vazios.
            messagebox.showerror("Erro",
                                 "Campos 'Login' e 'Senha' são obrigatórios.")

            # `return` interrompe a execução do método para evitar que o
            #       cadastro continue sem os dados necessários.
            return

        # Se `self.usuario_em_edicao` estiver preenchido, significa que o
        #       usuário está editando um cadastro existente.
        if self.usuario_em_edicao:

            # `usuarios_collection.update_one(...)` → Atualiza os dados do
            #       usuário no banco de dados MongoDB.
            # O método `update_one()` recebe dois argumentos:
            # **Filtro** → {"_id": self.usuario_em_edicao} → Filtra o usuário
            #       pelo ID armazenado na variável `self.usuario_em_edicao`.
            # **Atualização** → {"$set": {...}} → Define os novos
            #       valores para o usuário encontrado.
            usuarios_collection.update_one(

                # Filtra o usuário pelo ID armazenado na variável `self.usuario_em_edicao`
                {"_id": self.usuario_em_edicao},
                {
                    "$set": {  # Define os novos valores para atualizar no banco de dados
                        "login": login_novo,  # Atualiza o campo "login" com o novo valor digitado
                        "senha": senha_nova,  # Atualiza o campo "senha" com a nova senha digitada
                        "permissoes": permissao  # Atualiza o campo "permissoes" com a permissão selecionada
                    }
                }
            )

            # Exibe uma mensagem de sucesso informando que o usuário foi atualizado.
            messagebox.showinfo("Sucesso",
                                f"Usuário '{login_novo}' atualizado com sucesso.")

        else:

            # Antes de inserir, verifica se já existe um usuário com o mesmo login.
            # `usuarios_collection.find_one({"login": login_novo})` → Procura um usuário
            #       no banco de dados que tenha o mesmo login digitado.
            if usuarios_collection.find_one({"login": login_novo}):
                # Se o usuário já existir, exibe uma mensagem de
                #       erro e interrompe o cadastro.
                messagebox.showerror("Erro",
                                     f"Já existe um usuário com o login '{login_novo}'.")

                # `return` impede que o código continue executando, evitando um cadastro duplicado.
                return

            # Se o login não estiver cadastrado, insere um novo
            #       usuário no banco de dados.
            usuarios_collection.insert_one({

                # Salva o login digitado pelo usuário
                "login": login_novo,

                # Salva a senha digitada pelo usuário
                "senha": senha_nova,

                # Salva a permissão selecionada pelo usuário
                "permissoes": permissao

            })

            # Exibe uma mensagem informando que o usuário foi cadastrado com sucesso.
            messagebox.showinfo("Sucesso",
                                f"Usuário '{login_novo}' cadastrado com sucesso.")

        # Chama o método `limpar_campos()`, que remove os valores
        #       digitados no formulário após a operação.
        self.limpar_campos()

        # Chama o método `listar_usuarios()`, que recarrega a lista
        #       no `Treeview` para exibir os novos dados.
        self.listar_usuarios()

    # Define um método chamado `limpar_campos`, que é responsável por
    #       apagar os dados inseridos nos campos de entrada.
    # Esse método é útil após cadastrar, atualizar ou excluir um usuário.
    def limpar_campos(self):

        # `self.login_var.set("")` → Define o campo de login como uma string
        #       vazia (apaga qualquer texto digitado anteriormente).
        self.login_var.set("")  # Limpa o campo de login

        # `self.senha_var.set("")` → Define o campo de senha como uma string
        #       vazia (apaga qualquer senha digitada anteriormente).
        self.senha_var.set("")  # Limpa o campo de senha

        # `self.permissoes_var.set("recepcionista")` → Define o campo de
        #       permissões com o valor padrão "recepcionista".
        # Isso garante que sempre que o formulário for limpo, a permissão
        #       será redefinida para esse valor por padrão.
        # Redefine a permissão para "recepcionista"
        self.permissoes_var.set("recepcionista")

        # `self.usuario_em_edicao = None` → Remove qualquer usuário
        #       que estava sendo editado.
        # Isso garante que, após limpar os campos, o formulário volte
        #       para o modo de **cadastro de um novo usuário**,
        #       em vez de continuar editando um usuário antigo.
        self.usuario_em_edicao = None  # Remove o usuário em edição

    # Define um método chamado `excluir_usuario`, que permite
    #       remover um usuário do banco de dados
    #       e da lista exibida no `Treeview`.
    def excluir_usuario(self):

        # `self.tree_usuarios.selection()` → Retorna a seleção do usuário no `Treeview`.
        # Se nenhum usuário estiver selecionado, a variável `selecao` será uma tupla vazia.
        selecao = self.tree_usuarios.selection()

        # Se nenhum usuário foi selecionado, exibe uma mensagem de
        #       erro e interrompe o processo.
        if not selecao:
            # `messagebox.showerror("Erro", "Selecione um usuário para excluir.")`
            # Exibe um alerta informando que o usuário precisa selecionar
            #       um item antes de excluir.
            messagebox.showerror("Erro",
                                 "Selecione um usuário para excluir.")

            # `return` impede que o código continue executando
            #       sem uma seleção válida.
            return

        # `self.tree_usuarios.item(selecao, "values")`
        # Obtém os valores do usuário selecionado na tabela `Treeview`.
        # `values` retorna uma tupla com os dados do usuário (login, senha, permissões, ID).
        valores = self.tree_usuarios.item(selecao, "values")

        # O ID do usuário está na **quarta posição** da tupla de valores (`values[3]`).
        # Esse ID é necessário para identificar o usuário no banco
        #       de dados MongoDB e excluí-lo.
        usuario_id_str = valores[3]

        # O login do usuário está na **primeira posição** da
        #       tupla de valores (`values[0]`).
        # Esse valor será utilizado para exibir o nome do usuário
        #       na mensagem de confirmação.
        login_str = valores[0]

        # Verifica se o usuário selecionado tem o login "admin".
        # `login_str.lower()` → Converte o login para minúsculas para
        #       evitar variações como "Admin" ou "ADMIN".
        if login_str.lower() == "admin":
            # Exibe uma mensagem de erro informando que o usuário "admin"
            #       não pode ser excluído.
            messagebox.showerror("Erro",
                                 "Não é permitido excluir o usuário 'admin'.")

            # `return` interrompe a execução da função, impedindo a
            #       exclusão do usuário.
            return

        # `messagebox.askyesno("Confirmar", ...)` → Exibe uma caixa de
        #       confirmação com as opções "Sim" e "Não".
        # Se o usuário clicar em "Sim", `confirmar` será `True`, permitindo a exclusão.
        # Se clicar em "Não", `confirmar` será `False`, e a exclusão será cancelada.
        confirmar = messagebox.askyesno("Confirmar",
                                        f"Tem certeza que deseja excluir o usuário '{login_str}'?")

        # Se o usuário confirmar a exclusão (`confirmar == True`), o código continua.
        if confirmar:
            # `usuarios_collection.delete_one({"_id": ObjectId(usuario_id_str)})`
            # Remove do MongoDB o usuário cujo ID seja igual ao `usuario_id_str`.
            # `ObjectId(usuario_id_str)` → Converte a string do ID para o
            #       formato correto do MongoDB.
            usuarios_collection.delete_one({"_id": ObjectId(usuario_id_str)})

            # Exibe uma mensagem informando que a exclusão foi realizada com sucesso.
            messagebox.showinfo("Sucesso",
                                f"Usuário '{login_str}' excluído com sucesso.")

            # Chama o método `limpar_campos()` para limpar os campos de
            #       entrada da tela após a exclusão.
            self.limpar_campos()

            # Chama o método `listar_usuarios()` para atualizar a tabela
            #       do `Treeview` e remover o usuário excluído da interface.
            self.listar_usuarios()

    # Define um método chamado `center_window` que centraliza a
    #       janela na tela do usuário.
    # Esse método recebe dois parâmetros: `largura` e `altura`,
    #       que representam as dimensões da janela.
    def center_window(self, largura, altura):

        # Obtém a largura total da tela do usuário.
        # `winfo_screenwidth()` retorna a largura em pixels do monitor
        #       onde a aplicação está sendo executada.
        larg_tela = self.winfo_screenwidth()

        # Obtém a altura total da tela do usuário.
        # `winfo_screenheight()` retorna a altura em pixels do monitor.
        alt_tela = self.winfo_screenheight()

        # Calcula a posição X para centralizar a janela horizontalmente.
        # `(larg_tela - largura) / 2` pega a largura total da tela e
        #       subtrai a largura da janela.
        # Dividindo por 2, encontramos a posição exata para centralizar.
        # `int(...)` converte o valor para um número inteiro, pois `geometry`
        #       não aceita números decimais.
        x = int((larg_tela - largura) / 2)

        # Calcula a posição Y para centralizar a janela verticalmente.
        # `(alt_tela - altura) / 2` pega a altura total da tela e
        #       subtrai a altura da janela.
        # Dividindo por 2, encontramos a posição exata para que a
        #       janela fique centralizada verticalmente.
        y = int((alt_tela - altura) / 2)

        # Define o tamanho e a posição da janela usando `geometry()`.
        # O formato da string é: `"largura x altura + posição_x + posição_y"`.
        # Isso posiciona a janela no centro exato da tela.
        self.geometry(f"{largura}x{altura}+{x}+{y}")


# =============================================================================
# ================ CLASSE PRINCIPAL DA APLICAÇÃO (APP) ========================
# =============================================================================

# Define a classe principal da aplicação, que herda de `tk.Tk`,
# tornando-se a janela principal do programa.
class Aplicacao(tk.Tk):

    # Método construtor da classe `Aplicacao`
    def __init__(self):

        # Chama o construtor da classe `tk.Tk`, garantindo que a aplicação
        # seja inicializada corretamente como uma janela Tkinter.
        super().__init__()

        # Define o título da janela principal.
        # O texto "Sistema de Gerenciamento de Pousadas/Hostels"
        # será exibido na barra de título da janela.
        self.title("Sistema de Gerenciamento de Pousadas/Hostels")

        # Define a janela para abrir maximizada.
        # `self.state("zoomed")` faz com que a janela ocupe toda a tela.
        # Se estiver no Linux e isso não funcionar, pode
        #       usar `self.attributes('-zoomed', True)`.
        self.state("zoomed")

        # Define a cor de fundo da aplicação.
        # `bg="#f7f7f7"` aplica um tom de cinza claro como fundo.
        self.configure(bg="#f7f7f7")

        # Aplica os estilos personalizados à interface gráfica.
        # `aplicar_estilos(self)` é chamado para definir temas de botões,
        # cores de fontes e outros ajustes visuais.
        aplicar_estilos(self)

        # Cria a barra de menu da aplicação.
        # `Menu(self)` cria um menu principal associado à janela principal.
        self.menu_bar = Menu(self)

        # Configura a janela para utilizar a barra de menu recém-criada.
        # `self.config(menu=self.menu_bar)` garante que o menu
        #       fique fixo no topo da interface.
        self.config(menu=self.menu_bar)

        # Adiciona um item de menu chamado "Dashboard" à barra de menu.
        # `label="Dashboard"` define o nome do menu que será exibido.
        # `command=lambda: self._abrir_via_menu("dashboard")` especifica que,
        # quando o usuário clicar no menu "Dashboard", o método `_abrir_via_menu`
        # será chamado com o argumento `"dashboard"`, indicando que a tela do
        # Dashboard deve ser aberta.
        self.menu_bar.add_command(label="Dashboard",
                                  command=lambda: self._abrir_via_menu("dashboard"))

        # Menu "Sistema"
        # Cria um menu suspenso chamado "Sistema".
        # `Menu(self.menu_bar, tearoff=0)` cria um submenu
        #       dentro da barra de menu principal.
        # `tearoff=0` impede que o menu seja destacado da
        #       janela principal, garantindo
        #       que ele permaneça fixo no menu da aplicação.
        self.menu_sistema = Menu(self.menu_bar, tearoff=0)

        # Adiciona um comando chamado "Sair" ao menu "Sistema".
        # `label="Sair"` define o nome exibido no menu suspenso.
        # `command=self.destroy` associa a ação de fechar a
        #       aplicação ao clicar na opção "Sair".
        self.menu_sistema.add_command(label="Sair", command=self.destroy)

        # Adiciona o menu suspenso "Sistema" à barra de menus principal.
        # `label="Sistema"` define o nome que aparece na barra de menus.
        # `menu=self.menu_sistema` vincula o submenu "Sistema" à barra de menus principal.
        self.menu_bar.add_cascade(label="Sistema", menu=self.menu_sistema)

        # Menu "Cadastros"
        # Cria um menu suspenso chamado "Cadastros".
        # `Menu(self.menu_bar, tearoff=0)` cria um submenu
        #       dentro da barra de menus principal.
        # `tearoff=0` impede que o menu possa ser destacado da janela principal.
        self.menu_cadastros = Menu(self.menu_bar, tearoff=0)

        # Adiciona um comando "Quartos" ao menu "Cadastros".
        # `label="Quartos"` define o nome exibido no submenu.
        # `command=lambda: self._abrir_via_menu("quartos")`
        #       chama a função `_abrir_via_menu`
        #       e passa "quartos" como argumento ao clicar na opção.
        self.menu_cadastros.add_command(label="Quartos",
                                        command=lambda: self._abrir_via_menu("quartos"))

        # Adiciona um comando "Produtos" ao menu "Cadastros".
        # `label="Produtos"` define o nome exibido no submenu.
        # `command=lambda: self._abrir_via_menu("produtos")` chama a
        #       função `_abrir_via_menu` e passa "produtos" como
        #       argumento ao clicar na opção.
        self.menu_cadastros.add_command(label="Produtos",
                                        command=lambda: self._abrir_via_menu("produtos"))

        # Adiciona um comando "Hóspedes" ao menu "Cadastros".
        # `label="Hóspedes"` define o nome exibido no submenu.
        # `command=lambda: self._abrir_via_menu("hospedes")` chama a
        #       função `_abrir_via_menu`e passa "hospedes" como
        #       argumento ao clicar na opção.
        self.menu_cadastros.add_command(label="Hóspedes",
                                        command=lambda: self._abrir_via_menu("hospedes"))

        # Adiciona um comando "Usuários" ao menu "Cadastros".
        # `label="Usuários"` define o nome exibido no submenu.
        # `command=lambda: self._abrir_via_menu("usuarios")`
        #       chama a função `_abrir_via_menu`
        #       e passa "usuarios" como argumento ao clicar na opção.
        self.menu_cadastros.add_command(label="Usuários",
                                        command=lambda: self._abrir_via_menu("usuarios"))

        # Adiciona o menu suspenso "Cadastros" à barra de menus principal.
        # `label="Cadastros"` define o nome que aparece na barra de menus.
        # `menu=self.menu_cadastros` vincula o submenu "Cadastros" à barra de menus principal.
        self.menu_bar.add_cascade(label="Cadastros", menu=self.menu_cadastros)

        # Menu "Relatórios"
        # Cria um menu suspenso chamado "Relatórios".
        # `Menu(self.menu_bar, tearoff=0)` cria um submenu
        #       dentro da barra de menus principal.
        # `tearoff=0` impede que o menu possa ser destacado da janela principal.
        self.menu_relatorios = Menu(self.menu_bar, tearoff=0)

        # Adiciona um comando "Relatório Geral" ao menu "Relatórios".
        # `label="Relatório Geral"` define o nome exibido no submenu.
        # `command=lambda: self._abrir_via_menu("relatorio")`
        #       chama a função `_abrir_via_menu` e passa "relatorio" como
        #       argumento ao clicar na opção.
        self.menu_relatorios.add_command(label="Relatório Geral",
                                         command=lambda: self._abrir_via_menu("relatorio"))

        # Adiciona o menu suspenso "Relatórios" à barra de menus principal.
        # `label="Relatórios"` define o nome que aparece na barra de menus.
        # `menu=self.menu_relatorios` vincula o submenu "Relatórios" à
        #       barra de menus principal.
        self.menu_bar.add_cascade(label="Relatórios", menu=self.menu_relatorios)

        # Adiciona um comando direto "Mapa de Quartos" à barra de menus principal.
        # `label="Mapa de Quartos"` define o nome do comando na barra de menus.
        # `command=lambda: self._abrir_via_menu("mapa")` chama a função `_abrir_via_menu`
        # e passa "mapa" como argumento ao clicar na opção.
        self.menu_bar.add_command(label="Mapa de Quartos",
                                  command=lambda: self._abrir_via_menu("mapa"))

    # Define a função `_abrir_via_menu` que gerencia a troca de
    #       telas ao selecionar uma opção no menu.
    # `self` representa a instância da classe.
    # `opcao` é o argumento que indica qual tela deve ser aberta.
    def _abrir_via_menu(self, opcao):

        # Percorre todos os widgets dentro da janela principal (`self`).
        # `self.winfo_children()` retorna uma lista de todos os
        #       widgets filhos dentro da janela.
        for widget in self.winfo_children():

            # Verifica se o widget é um `tk.Frame`, ou seja, uma
            #       tela ou seção de interface.
            # Isso garante que apenas frames sejam destruídos ao trocar de tela.
            if isinstance(widget, tk.Frame):
                # Destroi o frame atual para liberar espaço para a nova tela.
                widget.destroy()

        # Verifica se o atributo `permissoes_atual` já foi definido na instância.
        # Caso o usuário não tenha permissões definidas (não esteja logado),
        # assume que ele possui o nível de acesso "recepcionista".
        if not hasattr(self, "permissoes_atual"):
            self.permissoes_atual = "recepcionista"

        # Verifica qual opção foi selecionada no menu e carrega a tela correspondente.
        # `opcao` contém o nome da tela a ser carregada.

        # Se a opção for "quartos", carrega a tela de gerenciamento de quartos.
        if opcao == "quartos":
            TelaGerenciarQuartos(self, self.permissoes_atual)

        # Se a opção for "produtos", carrega a tela de gerenciamento de produtos.
        elif opcao == "produtos":
            TelaGerenciarProdutos(self, self.permissoes_atual)

        # Se a opção for "hospedes", carrega a tela de cadastro de hóspedes.
        elif opcao == "hospedes":
            TelaCadastroHospedes(self, self.permissoes_atual)

        # Se a opção for "usuarios", carrega a tela de
        #       gerenciamento de usuários.
        elif opcao == "usuarios":

            GerenciarUsuariosFrame(self, self.permissoes_atual)

            # GerenciarUsuariosWindow(self)

        # Se a opção for "relatorio", carrega a tela de relatório geral.
        elif opcao == "relatorio":
            TelaRelatorioGeral(self, self.permissoes_atual)

        # Se a opção for "mapa", carrega a tela do mapa de quartos.
        elif opcao == "mapa":
            TelaMapaQuartos(self, self.permissoes_atual)

        # Se a opção for "dashboard", carrega a tela principal do dashboard.
        elif opcao == "dashboard":
            TelaDashboard(self, self.permissoes_atual)

        # Se nenhuma das opções anteriores for reconhecida,
        #       carrega o dashboard por padrão.
        else:
            TelaDashboard(self, self.permissoes_atual)

    # Define uma função para exibir a tela do Dashboard.
    # `self` refere-se à instância atual da classe.
    # `permissoes` recebe as permissões do usuário logado.
    def exibir_dashboard(self, permissoes):

        # Atualiza o atributo `permissoes_atual` com as permissões do usuário.
        # Isso garante que a aplicação reconheça o nível de acesso correto.
        self.permissoes_atual = permissoes

        # Cria e exibe a tela do Dashboard, passando as permissões do usuário.
        # `TelaDashboard(self, permissoes)` instancia a classe da tela principal.
        # `.tkraise()` garante que a tela do Dashboard fique visível sobre outras janelas.
        TelaDashboard(self, permissoes).tkraise()

    # Define uma função para iniciar a execução do sistema.
    # `self` refere-se à instância atual da classe Aplicacao.
    def executar(self):

        # Cria uma instância da Tela de Login.
        # A tela de login é a primeira interface exibida ao usuário.
        tela_login = TelaLogin(self)

        # Define a tela de login como "modal", impedindo interação
        #       com outras janelas até que seja fechada.
        # `grab_set()` captura todos os eventos do teclado e
        #       mouse para a tela de login.
        tela_login.grab_set()

        # Inicia o loop principal do Tkinter, mantendo a aplicação em execução.
        # `self.mainloop()` escuta eventos de interface
        #       gráfica e mantém a janela aberta.
        self.mainloop()


# =============================================================================
# ================================ MAIN ========================================
# =============================================================================

# Cria uma instância da classe Aplicacao.
# `app` será o objeto que gerencia toda a interface
#       gráfica e funcionalidades do sistema.
app = Aplicacao()

# Chama o método `executar()` da instância `app`, iniciando o sistema.
# Este método exibe a tela de login e mantém a
#       aplicação rodando até ser fechada.
app.executar()