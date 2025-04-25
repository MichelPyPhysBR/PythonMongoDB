# Importa o módulo tkinter e renomeia como 'tk'. Este módulo é
#       usado para criar interfaces gráficas baseadas em janelas.
import tkinter as tk

# Importa submódulos específicos de 'tkinter'. 'ttk' é usado para
#       widgets com um estilo mais moderno. 'messagebox' é
#       utilizado para exibir mensagens ao usuário.
from tkinter import ttk, messagebox

# Importa o módulo 'MongoClient' de 'pymongo'. Este módulo é necessário
#       para se conectar e operar com um banco de dados MongoDB.
from pymongo import MongoClient

# Importa 'ObjectId' de 'bson.objectid', que é usado para manipular IDs
#       do MongoDB, que são utilizados para identificar documentos de forma única.
from bson.objectid import ObjectId

# Importa o módulo 'json', que permite a manipulação de dados em
#       formato JSON, uma forma comum de troca de dados na web.
import json

# Importa o módulo 'xlsxwriter', que permite criar arquivos em
#       formato Excel (.xlsx), possibilitando a escrita de dados em planilhas.
import xlsxwriter


# Importa 'letter' de 'reportlab.lib.pagesizes', que define o tamanho de
#       página padrão 'carta' para documentos PDF.
from reportlab.lib.pagesizes import letter

# Importa 'canvas' de 'reportlab.pdfgen', que é utilizado para criar
#       documentos PDF, permitindo desenhar textos, imagens e outros gráficos.
from reportlab.pdfgen import canvas

# Instalar o reportlab


# Importa o módulo 'os', que fornece funções para interagir com o
#       sistema operacional, incluindo funcionalidades para
#       manipular arquivos e diretórios.
import os

# Cria uma instância de 'MongoClient' para conectar ao servidor
#       MongoDB local na porta padrão 27017.
client = MongoClient("mongodb://localhost:27017/")

# Acessa o banco de dados chamado 'cinema_db' dentro do servidor MongoDB.
# Se não existir, ele será criado automaticamente ao inserir
#       dados pela primeira vez.
db = client["cinema_db"]

# Importa o PIL para trabalhar com imagens
from PIL import Image, ImageTk  # Para lidar com imagens


# ============================================================
# TELA GERENCIAR FILMES
# ============================================================

# Função para criar e configurar a janela de gerenciamento de filmes.
def tela_gerenciar_filmes(root, db):

    # Definição da largura e altura da janela que será aberta.
    largura_janela = 1100
    altura_janela = 450

    # Obtém a largura e altura da tela onde o programa está sendo executado.
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Calcula a posição X para centralizar a janela na tela.
    pos_x = (largura_tela - largura_janela) // 2

    # Calcula a posição Y para centralizar a janela na tela.
    pos_y = (altura_tela - altura_janela) // 2

    # Cria uma janela secundária (pop-up) utilizando a função
    #       auxiliar 'criar_janela_secundaria'.
    # Esta função configura a janela como modal, focando a
    #       interação do usuário com ela.
    janela = criar_janela_secundaria(root, "Gerenciar Filmes")

    # Configura a geometria da janela, definindo tamanho e posição.
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Configura a coluna 0 da grid da janela para ajustar seu
    #       tamanho automaticamente ao redimensionar.
    janela.columnconfigure(0, weight=1)

    # Configura a linha 0 da grid da janela para ajustar seu
    #       tamanho automaticamente ao redimensionar.
    janela.rowconfigure(0, weight=1)

    # Criação e configuração do frame principal dentro da
    #       janela de gerenciamento de filmes.
    frame_principal = ttk.Frame(janela, padding="10 10 10 10")

    # Posiciona o frame principal na janela usando o layout de grade (grid).
    # O frame é colocado na primeira linha (row=0) e primeira
    #       coluna (column=0) da janela.
    # A opção 'sticky="nsew"' faz com que o frame se expanda em todas as
    #       direções (Norte, Sul, Leste, Oeste) para preencher o espaço disponível.
    frame_principal.grid(row=0, column=0, sticky="nsew")

    # Configura a primeira coluna do frame principal para que ela
    #       expanda e ocupe o espaço disponível, adaptando-se ao
    #       redimensionamento da janela.
    frame_principal.columnconfigure(0, weight=1)

    # Configura a primeira linha do frame principal para expandir,
    #       permitindo que ela ocupe o espaço vertical disponível.
    frame_principal.rowconfigure(0, weight=1)

    # Configura a segunda linha do frame principal para não expandir, o
    #       que é útil para elementos que não devem esticar juntamente com a janela.
    frame_principal.rowconfigure(1, weight=0)

    # Criação e configuração do frame que conterá a Treeview,
    #       componente para listar os filmes existentes.
    frame_tree = ttk.Frame(frame_principal)

    # Posiciona o frame da Treeview dentro do frame principal usando o layout de grade.
    # O frame é colocado na primeira linha (row=0) e primeira
    #       coluna (column=0) do frame principal.
    # A opção 'sticky="nsew"' assegura que o frame da Treeview se
    #       expanda em todas as direções para ocupar todo o espaço do frame principal.
    frame_tree.grid(row=0, column=0, sticky="nsew")

    # Configura a única coluna dentro do frame da Treeview para expandir e
    #       ocupar o espaço disponível horizontalmente.
    frame_tree.columnconfigure(0, weight=1)

    # Configura a única linha dentro do frame da Treeview para expandir e
    #       ocupar o espaço disponível verticalmente.
    frame_tree.rowconfigure(0, weight=1)

    # Configuração da Treeview
    # Define as colunas que serão mostradas na Treeview. Cada elemento na
    #       tupla representa o nome de uma coluna no banco de dados.
    colunas = ("_id", "titulo", "duracao", "classificacao", "genero", "sinopse")

    # Cria o componente Treeview no frame destinado para ele. 'columns=colunas'
    #       especifica as colunas que devem ser exibidas.
    # 'show="headings"' faz com que apenas os cabeçalhos das colunas
    #       sejam mostrados, omitindo a coluna da árvore principal que normalmente é exibida.
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings")

    # Configura cada coluna da Treeview: define o texto do cabeçalho e a
    #       forma como o texto é alinhado, além de definir a largura padrão.
    for col in colunas:

        # 'capitalize()' é usado para garantir que o cabeçalho de
        #       cada coluna comece com letra maiúscula.
        tree.heading(col, text=col.capitalize())

        # Centraliza o texto nas colunas e define a largura de
        #       cada uma como 150 pixels.
        tree.column(col, anchor="center", width=150)

    # Cria uma barra de rolagem vertical e associa essa barra à
    #       Treeview para permitir rolagem vertical dos dados.
    scrollbar_vertical = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)

    # Cria uma barra de rolagem horizontal e associa essa barra à
    #       Treeview para permitir rolagem horizontal dos dados.
    scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=tree.xview)

    # Configura a Treeview para usar as barras de rolagem criadas. 'yscrollcommand' e
    #       'xscrollcommand' vinculam as barras de rolagem à Treeview.
    tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    # Posiciona a Treeview dentro do frame_tree utilizando o layout grid.
    # A Treeview é estendida para preencher o espaço disponível em todas as direções.
    tree.grid(row=0, column=0, sticky="nsew")

    # Posiciona a barra de rolagem vertical à direita da Treeview
    #       para permitir a rolagem vertical dos dados.
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")

    # Posiciona a barra de rolagem horizontal abaixo da Treeview para
    #       permitir a rolagem horizontal dos dados.
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew")


    # Cria um novo frame para abrigar campos de entrada e botões de ação,
    #       posicionado abaixo da Treeview no frame principal.
    frame_campos = ttk.Frame(frame_principal, padding="10 10 10 10")

    # Utiliza o layout grid para posicionar o frame_campos dentro do frame_principal.
    # A configuração sticky="ew" faz com que o frame se estenda horizontalmente.
    frame_campos.grid(row=1, column=0, sticky="ew")

    # Configura duas colunas dentro do frame_campos para expandir e ocupar o
    #       espaço disponível, garantindo que os campos de entrada e botões
    #       dentro dessas colunas se ajustem proporcionalmente ao redimensionar a janela.
    frame_campos.columnconfigure(1, weight=1)
    frame_campos.columnconfigure(3, weight=1)

    # Cria um rótulo (label) com o texto "Título:" e o adiciona ao
    #       layout grid do frame_campos.
    # A linha especifica a posição do rótulo na primeira linha (row=0) e
    #       primeira coluna (column=0) do grid.
    # O parâmetro 'sticky="e"' alinha o texto à direita (East) dentro do
    #       espaço da célula grid.
    # 'padx=5' e 'pady=5' adicionam um espaço de 5 pixels ao redor do
    #       rótulo para evitar que ele fique muito próximo dos outros componentes.
    ttk.Label(frame_campos, text="Título:").grid(row=0, column=0, sticky="e", padx=5, pady=5)

    # Cria um campo de entrada (Entry) para inserir o título do filme.
    #       Esse componente é associado ao frame_campos.
    entrada_titulo = ttk.Entry(frame_campos)

    # Posiciona o campo de entrada no layout grid do frame_campos.
    # A linha especifica a posição do campo na primeira linha (row=0) e
    #       segunda coluna (column=1) do grid.
    # 'sticky="ew"' faz com que o campo de entrada se expanda para preencher o
    #       espaço disponível horizontalmente (East-West) dentro da célula.
    # 'padx=5' e 'pady=5' adicionam um espaço de 5 pixels ao redor do campo de
    #       entrada para manter um espaçamento adequado dos outros componentes.
    entrada_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # ttk.Label: Cria um rótulo (Label) no frame 'frame_campos'
    # text="Duração (min):": Define o texto do rótulo como "Duração (min):"
    # grid: Configura o rótulo para se alinhar à direita na célula do grid (east)
    # row=0, column=2: Posiciona o rótulo na linha 0, coluna 2 do layout grid
    # sticky="e": Alinha à direita
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Duração (min):").grid(row=0, column=2, sticky="e", padx=5, pady=5)

    # ttk.Entry: Cria um campo de entrada (Entry) para receber
    #       texto no frame 'frame_campos'
    entrada_duracao = ttk.Entry(frame_campos)

    # grid: Configura a posição do campo de entrada no layout grid
    # row=0, column=3: Posiciona na linha 0, coluna 3 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    # sticky="ew": Define o campo de entrada para expandir e
    #       preencher o espaço horizontal disponível
    entrada_duracao.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    # classificacoes: Define uma lista de opções para classificação etária dos filmes
    classificacoes = ["Livre", "10 anos", "12 anos", "14 anos", "16 anos", "18 anos"]

    # ttk.Label: Cria um rótulo para o ComboBox no frame 'frame_campos'
    # text="Classificação:": Define o texto do rótulo como "Classificação:"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=0: Posiciona o rótulo na linha 1, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Classificação:").grid(row=1, column=0, sticky="e", padx=5, pady=5)

    # ttk.Combobox: Cria um ComboBox no frame 'frame_campos'
    # values=classificacoes: Define as opções do ComboBox com
    #       base na lista 'classificacoes'
    # state="readonly": Configura o ComboBox para ser apenas de
    #       leitura, impedindo a entrada de texto livre
    combo_classificacao = ttk.Combobox(frame_campos, values=classificacoes, state="readonly")

    # grid: Configura a posição do ComboBox no layout grid
    # row=1, column=1: Posiciona o ComboBox na linha 1, coluna 1 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    # sticky="ew": Expande o ComboBox para preencher horizontalmente a célula do grid
    combo_classificacao.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # generos: Define uma lista de opções para gêneros de filmes
    generos = ["Ação", "Comédia", "Drama", "Terror", "Ficção Científica", "Animação", "Romance"]

    # ttk.Label: Cria um rótulo para o ComboBox no frame 'frame_campos'
    # text="Gênero:": Define o texto do rótulo como "Gênero:"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=2: Posiciona o rótulo na linha 1, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Gênero:").grid(row=1, column=2, sticky="e", padx=5, pady=5)

    # ttk.Combobox: Cria um ComboBox no frame 'frame_campos'
    # values=generos: Define as opções do ComboBox com base na lista 'generos'
    # state="readonly": Configura o ComboBox para ser apenas de
    #       leitura, impedindo a entrada de texto livre
    combo_genero = ttk.Combobox(frame_campos, values=generos, state="readonly")

    # grid: Configura a posição do ComboBox no layout grid
    # row=1, column=3: Posiciona o ComboBox na linha 1, coluna 3 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    # sticky="ew": Expande o ComboBox para preencher horizontalmente a célula do grid
    combo_genero.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Sinopse:": Define o texto do rótulo como "Sinopse:"
    # grid: Posiciona o rótulo no layout grid
    # row=2, column=0: Posiciona o rótulo na linha 2, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Sinopse:").grid(row=2, column=0, sticky="e", padx=5, pady=5)

    # ttk.Entry: Cria uma caixa de texto para entrada de dados no frame 'frame_campos'
    # Esta caixa de texto é usada para inserir a sinopse do filme
    entrada_sinopse = ttk.Entry(frame_campos)

    # grid: Configura a posição da caixa de texto no layout grid
    # row=2, column=1: Posiciona a caixa de texto na linha 2, coluna 1 do layout grid
    # columnspan=3: Faz com que a caixa de texto ocupe o espaço de três colunas
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    # sticky="ew": Expande a caixa de texto para preencher horizontalmente a célula do grid
    entrada_sinopse.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

    # filme_id_em_edicao: Uma lista usada para armazenar
    #       temporariamente o ID do filme que está sendo editado
    # [None]: Inicializa com None indicando que nenhum filme
    #       está sendo editado inicialmente
    filme_id_em_edicao = [None]


    # def carregar_filmes(): Define uma função chamada 'carregar_filmes'
    #       que não recebe argumentos.
    def carregar_filmes():

        # for i in tree.get_children(): Itera sobre todos os itens (filhos)
        #       presentes no componente 'tree'.
        # tree.delete(i): Remove cada item (filme) do componente 'tree' para
        #       garantir que não haja duplicidade quando a função for chamada novamente.
        for i in tree.get_children():
            tree.delete(i)

        # for f in obter_filmes(db): Itera sobre a lista de filmes obtidos da
        #       função 'obter_filmes' que consulta o banco de dados.
        # tree.insert("", tk.END, ...): Insere um novo item no 'tree'
        #       para cada filme obtido.
        # values=(...): Define os valores que serão inseridos em cada
        #       coluna do 'tree' para o filme atual.
        # str(f["_id"]), ...: Converte o ObjectId do filme para string e
        #       inclui outros detalhes do filme como título, duração,
        #       classificação, gênero e sinopse.
        for f in obter_filmes(db):
            tree.insert("", tk.END, values=(
                str(f["_id"]), f["titulo"], f["duracao"], f["classificacao"], f["genero"], f["sinopse"]))


    # def cadastrar_novo(): Define uma função chamada 'cadastrar_novo'
    #       que não recebe argumentos.
    def cadastrar_novo():

        # titulo = entrada_titulo.get().strip(): Obtém o texto do campo de
        #       entrada 'entrada_titulo', removendo espaços em branco extras no início e no fim.
        titulo = entrada_titulo.get().strip()

        # duracao = entrada_duracao.get().strip(): Obtém o texto do campo de
        #       entrada 'entrada_duracao', removendo espaços em branco extras no início e no fim.
        duracao = entrada_duracao.get().strip()

        # classificacao = combo_classificacao.get().strip(): Obtém o valor
        #       selecionado no 'combo_classificacao', removendo espaços em
        #       branco extras no início e no fim.
        classificacao = combo_classificacao.get().strip()

        # genero = combo_genero.get().strip(): Obtém o valor selecionado
        #       no 'combo_genero', removendo espaços em branco extras no início e no fim.
        genero = combo_genero.get().strip()

        # sinopse = entrada_sinopse.get().strip(): Obtém o texto do campo de
        #       entrada 'entrada_sinopse', removendo espaços em branco
        #       extras no início e no fim.
        sinopse = entrada_sinopse.get().strip()

        # if not all([...]): Verifica se todos os campos (título, duração,
        #       classificação, gênero, sinopse) foram preenchidos.
        # messagebox.showerror(...): Mostra uma mensagem de erro se algum
        #       campo não estiver preenchido, indicando que todos os
        #       campos são obrigatórios.
        if not all([titulo, duracao, classificacao, genero, sinopse]):
            messagebox.showerror("Erro", "Preencha todos os campos!", parent=janela)
            return

        # try: Inicia um bloco de tentativa para converter a duração
        #       do filme de string para inteiro.
        try:

            # duracao = int(duracao): Tenta converter o valor
            #       de 'duracao' para um inteiro.
            duracao = int(duracao)

        # except ValueError: Captura o erro se a conversão para inteiro falhar,
        #       indicando que o input não é um número válido.
        except ValueError:

            # messagebox.showerror(...): Mostra uma mensagem de erro informando
            #       que o campo duração deve conter apenas números.
            messagebox.showerror("Erro", "Duração deve ser um número!", parent=janela)

            # return: Encerra a função para evitar que o código
            #       continue com um valor inválido.
            return

        # cadastrar_filme(...): Chama a função 'cadastrar_filme' para
        #       inserir os dados do novo filme no banco de dados.
        cadastrar_filme(db, titulo, duracao, classificacao, genero, sinopse)

        # messagebox.showinfo(...): Exibe uma mensagem de sucesso
        #       informando que o filme foi cadastrado.
        messagebox.showinfo("Sucesso", "Filme cadastrado!", parent=janela)

        # carregar_filmes(): Chama a função 'carregar_filmes' para
        #       atualizar a lista de filmes exibida.
        carregar_filmes()

        # limpar_campos([...]): Chama a função 'limpar_campos'
        #       para limpar os campos de entrada após o cadastro.
        limpar_campos([entrada_titulo, entrada_duracao, entrada_sinopse])

        # combo_classificacao.set(""): Limpa a seleção atual do
        #       combobox de classificação.
        combo_classificacao.set("")

        # combo_genero.set(""): Limpa a seleção atual do combobox de gênero.
        combo_genero.set("")

        # filme_id_em_edicao[0] = None: Reseta a variável que
        #       guarda o ID de um filme em edição.
        filme_id_em_edicao[0] = None


    def salvar_alteracoes():

        # if not filme_id_em_edicao[0]: Verifica se há um filme selecionado
        #       para edição verificando se o ID está armazenado na lista.
        if not filme_id_em_edicao[0]:

            # messagebox.showerror(...): Mostra uma mensagem de erro caso
            #       nenhum filme esteja selecionado para edição.
            messagebox.showerror("Erro", "Nenhum filme selecionado para edição!", parent=janela)

            # return: Sai da função sem executar as alterações, pois
            #       não há filme selecionado.
            return

        # titulo = entrada_titulo.get().strip(): Recupera o texto do campo de
        #       título, removendo espaços em branco excessivos.
        titulo = entrada_titulo.get().strip()

        # duracao = entrada_duracao.get().strip(): Recupera o texto do campo
        #       de duração, removendo espaços em branco excessivos.
        duracao = entrada_duracao.get().strip()

        # classificacao = combo_classificacao.get().strip(): Recupera o texto
        #       selecionado no combobox de classificação, removendo espaços
        #       em branco excessivos.
        classificacao = combo_classificacao.get().strip()

        # genero = combo_genero.get().strip(): Recupera o texto selecionado no
        #       combobox de gênero, removendo espaços em branco excessivos.
        genero = combo_genero.get().strip()

        # sinopse = entrada_sinopse.get().strip(): Recupera o texto do campo de
        #       sinopse, removendo espaços em branco excessivos.
        sinopse = entrada_sinopse.get().strip()

        # if not all([...]): Verifica se todos os campos (título, duração,
        #       classificação, gênero, sinopse) estão preenchidos.
        if not all([titulo, duracao, classificacao, genero, sinopse]):

            # messagebox.showerror(...): Exibe uma mensagem de erro se algum campo estiver vazio.
            messagebox.showerror("Erro", "Preencha todos os campos!", parent=janela)

            # return: Encerra a função sem salvar as alterações se
            #       algum campo estiver vazio.
            return

        # try: Tenta converter o valor de duração para um inteiro.
        try:

            duracao = int(duracao)

        # except ValueError: Captura o erro se a conversão
        #       falhar (quando o valor não é um número).
        except ValueError:

            # messagebox.showerror(...): Exibe uma mensagem de erro
            #       se a duração não for um número.
            messagebox.showerror("Erro", "Duração deve ser um número!", parent=janela)

            # return: Encerra a função sem salvar as alterações se a
            #       duração não for um número.
            return

        # atualizar_filme(...): Chama a função para atualizar o
        #       filme no banco de dados com os novos valores.
        atualizar_filme(db, filme_id_em_edicao[0], titulo, duracao, classificacao, genero, sinopse)

        # messagebox.showinfo(...): Exibe uma mensagem informando que o
        #       filme foi atualizado com sucesso.
        messagebox.showinfo("Sucesso", "Filme atualizado!", parent=janela)

        # carregar_filmes(): Recarrega a lista de filmes para
        #       refletir as alterações.
        carregar_filmes()

        # limpar_campos([...]): Limpa os campos de entrada para
        #       que estejam prontos para uma nova entrada.
        limpar_campos([entrada_titulo, entrada_duracao, entrada_sinopse])

        # combo_classificacao.set(""): Reseta o combobox de
        #       classificação para o estado inicial.
        combo_classificacao.set("")

        # combo_genero.set(""): Reseta o combobox de gênero para o estado inicial.
        combo_genero.set("")

        # filme_id_em_edicao[0] = None: Limpa a variável que
        #       armazena o ID do filme atualmente em edição.
        filme_id_em_edicao[0] = None


    def deletar_item():

        # sel = tree.selection(): Obtém a seleção atual na árvore (Treeview),
        #       que representa a linha selecionada.
        sel = tree.selection()

        # if not sel: Verifica se nenhum item foi selecionado.
        if not sel:

            # messagebox.showerror(...): Exibe uma mensagem de erro se
            #       nenhum filme estiver selecionado.
            messagebox.showerror("Erro", "Selecione um filme!", parent=janela)

            # return: Encerra a função se nenhum filme for selecionado.
            return

        # item = tree.item(sel): Obtém os dados do item selecionado na Treeview.
        item = tree.item(sel)

        # fid = item["values"][0]: Extrai o ID do filme da primeira
        #       coluna dos valores do item selecionado.
        fid = item["values"][0]

        # resp = messagebox.askyesno(...): Pergunta ao usuário se
        #       realmente deseja deletar o filme selecionado.
        resp = messagebox.askyesno("Confirmar", "Deseja deletar o filme?", parent=janela)

        # if resp: Verifica se o usuário confirmou a deleção.
        if resp:

            # deletar_filme(...): Chama a função para deletar o filme no
            #       banco de dados usando o ID do filme.
            deletar_filme(db, fid)

            # messagebox.showinfo(...): Exibe uma mensagem informando
            #       que o filme foi deletado com sucesso.
            messagebox.showinfo("Sucesso", "Filme deletado!", parent=janela)

            # carregar_filmes(): Recarrega a lista de filmes para refletir as
            #       alterações, atualizando a Treeview.
            carregar_filmes()


    def on_tree_select(event):

        # Obtém o item atualmente selecionado na Treeview.
        sel = tree.selection()

        # Verifica se nenhum item foi selecionado. Se não houver
        #       seleção, encerra a função.
        if not sel:
            return

        # Obtém o dicionário representando o item selecionado.
        item = tree.item(sel)

        # Extrai os valores associados ao item selecionado.
        vals = item["values"]

        # Atualiza o ID do filme atualmente em edição.
        filme_id_em_edicao[0] = vals[0]

        # Limpa o campo de entrada do título.
        entrada_titulo.delete(0, tk.END)

        # Preenche o campo de entrada do título com o valor
        #       correspondente do filme selecionado.
        entrada_titulo.insert(0, vals[1])

        # Limpa o campo de entrada da duração.
        entrada_duracao.delete(0, tk.END)

        # Preenche o campo de entrada da duração com o valor
        #       correspondente do filme selecionado.
        entrada_duracao.insert(0, vals[2])

        # Define a classificação no combobox com o valor
        #       correspondente do filme selecionado.
        combo_classificacao.set(vals[3])

        # Define o gênero no combobox com o valor correspondente do filme selecionado.
        combo_genero.set(vals[4])

        # Limpa o campo de entrada da sinopse.
        entrada_sinopse.delete(0, tk.END)

        # Preenche o campo de entrada da sinopse com o valor
        #       correspondente do filme selecionado.
        entrada_sinopse.insert(0, vals[5])


    # Associa o evento de seleção da Treeview com a função `on_tree_select`.
    # Isso significa que, quando o usuário clicar ou selecionar um item na tabela (Treeview),
    # a função `on_tree_select` será executada automaticamente para
    #       carregar as informações do item nos campos de edição.
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Botões de ação

    # Cria o botão "Cadastrar Novo".
    # Este botão é exibido na interface gráfica e, ao ser clicado, ele
    #       chama a função `cadastrar_novo`.
    # A função `cadastrar_novo` pega os dados dos campos de entrada e
    #       os insere no banco de dados como um novo filme.
    ttk.Button(
        frame_campos,  # Define o pai do botão, neste caso, o frame onde os campos e botões estão organizados.
        text="Cadastrar Novo",  # Define o texto que aparecerá no botão.
        command=cadastrar_novo  # Define qual função será executada ao clicar no botão.
    ).grid(
        row=3,  # Define a linha do grid onde o botão será colocado dentro do frame.
        column=0,  # Define a coluna do grid onde o botão será colocado dentro do frame.
        padx=5,  # Adiciona um espaço horizontal entre o botão e os elementos ao seu redor.
        pady=5  # Adiciona um espaço vertical entre o botão e os elementos ao seu redor.
    )

    # Cria o botão "Salvar Alterações".
    # Este botão chama a função `salvar_alteracoes` quando clicado,
    #       que salva as mudanças feitas nos campos
    #       em um filme já existente, atualizando o banco de dados.
    ttk.Button(frame_campos,
               text="Salvar Alterações",
               command=salvar_alteracoes).grid(row=3,  # Define a linha onde o botão será colocado dentro do frame.
                                               column=2,
                                               # Define a coluna onde o botão será colocado dentro do frame.
                                               padx=5,  # Adiciona espaço horizontal ao redor do botão.
                                               pady=5)  # Adiciona espaço vertical ao redor do botão.

    # Cria o botão "Deletar".
    # Este botão chama a função `deletar_item` ao ser clicado, que
    #       remove o filme selecionado na tabela (Treeview)
    #       do banco de dados e o atualiza na interface.
    ttk.Button(frame_campos,
               text="Deletar",
               command=deletar_item).grid(row=3,  # Define a linha onde o botão será colocado dentro do frame.
                                          column=3,  # Define a coluna onde o botão será colocado dentro do frame.
                                          padx=5,  # Adiciona espaço horizontal ao redor do botão.
                                          pady=5)  # Adiciona espaço vertical ao redor do botão.

    # Carrega os filmes já cadastrados no banco de dados e
    #       os exibe na tabela (Treeview).
    # Isso é útil para preencher a tabela com os dados existentes
    #       sempre que a tela é aberta ou atualizada.
    carregar_filmes()


# ============================================================
# FUNÇÕES AUXILIARES DE BANCO DE DADOS
# ============================================================

# FUNÇÕES RELACIONADAS A FILMES


# Função para deletar um filme específico da coleção 'filmes' no banco de dados.
def deletar_filme(db, filme_id):

    # db.filmes.delete_one() é usada para remover um único
    #       documento da coleção 'filmes'.
    # O documento a ser removido é identificado pelo seu ObjectId,
    #       que é passado para a função.
    # "ObjectId(filme_id)" converte o ID do filme, que é uma string, em um
    #       ObjectId do MongoDB para realizar a busca correta.
    db.filmes.delete_one({"_id": ObjectId(filme_id)})


# Função para deletar uma sala específica da coleção 'salas' no banco de dados.
def deletar_sala(db, sala_id):


    # db.salas.delete_one() é usada para remover um único documento da coleção 'salas'.
    # O documento a ser removido é identificado pelo ObjectId fornecido, que é passado para a função.
    # "ObjectId(sala_id)" converte a string 'sala_id' em um ObjectId do
    #       MongoDB, necessário para encontrar o documento corretamente.
    db.salas.delete_one({"_id": ObjectId(sala_id)})


# Função para deletar uma sessão específica da coleção 'sessoes' e todas as
#       reservas associadas a essa sessão da coleção 'reservas'.
def deletar_sessao(db, sessao_id):

    # db.sessoes.delete_one() remove um único documento da
    #       coleção 'sessoes' baseado no ObjectId da sessão.
    # "ObjectId(sessao_id)" garante que o ID da sessão seja convertido
    #       para o formato apropriado para a consulta.
    db.sessoes.delete_one({"_id": ObjectId(sessao_id)})

    # db.reservas.delete_many() remove todos os documentos da coleção 'reservas'
    #       que correspondem ao ObjectId da sessão deletada.
    # Isso garante que todas as reservas associadas à sessão deletada sejam
    #       removidas, mantendo a consistência dos dados.
    db.reservas.delete_many({"sessao_id": ObjectId(sessao_id)})


# Função para atualizar um filme existente no banco de dados.
def atualizar_filme(db, filme_id, titulo, duracao, classificacao, genero, sinopse):

    # db.filmes.update_one() atualiza um único documento na coleção 'filmes'.
    # O primeiro parâmetro é o filtro para localizar o documento a ser atualizado,
    #       aqui usando o ObjectId do filme.
    # O segundo parâmetro, "$set", é usado para especificar os campos do documento
    #       que devem ser atualizados.
    # ObjectId(filme_id) converte a string 'filme_id' em um ObjectId para
    #       corresponder ao formato de identificação usado pelo MongoDB.
    db.filmes.update_one({"_id": ObjectId(filme_id)}, {"$set": {
        "titulo": titulo,
        "duracao": duracao,
        "classificacao": classificacao,
        "genero": genero,
        "sinopse": sinopse
    }})


# Função para atualizar os detalhes de uma sala existente na coleção 'salas' no banco de dados.
def atualizar_sala(db, sala_id, nome, fileiras, assentos_por_fileira, tipo_assento):

    # db.salas.update_one() atualiza um documento específico na coleção 'salas'.
    # O documento é identificado pelo seu ObjectId, que é fornecido pelo parâmetro 'sala_id'.
    # "ObjectId(sala_id)" converte a string 'sala_id' em um ObjectId, o
    #       identificador usado pelo MongoDB.
    # O segundo argumento, '$set', é um operador do MongoDB usado para
    #       especificar os campos que devem ser atualizados.
    # Cada chave dentro de '$set' corresponde a um campo do documento e o
    #       valor associado é o novo valor para esse campo.
    db.salas.update_one({"_id": ObjectId(sala_id)}, {"$set": {

        "nome": nome,  # Atualiza o nome da sala.
        "fileiras": fileiras,  # Atualiza o número de fileiras de assentos na sala.
        "assentos_por_fileira": assentos_por_fileira,  # Atualiza o número de assentos por fileira.
        "tipo_assento": tipo_assento  # Atualiza o tipo de assento, por exemplo, 'VIP' ou 'Comum'.

    }})


# Função para atualizar os detalhes de uma sessão existente na coleção 'sessoes' no banco de dados.
def atualizar_sessao(db, sessao_id, filme_id, sala_id, data_str, hora_str, valor_ingresso):

    # db.sessoes.update_one() é usada para atualizar um documento
    #       específico na coleção 'sessoes'.
    # O primeiro parâmetro, um dicionário, define o critério de busca do
    #       documento a ser atualizado, especificamente pelo ObjectId da sessão.
    # "ObjectId(sessao_id)" converte a string 'sessao_id' em um ObjectId do
    #       MongoDB, necessário para a busca correta do documento.
    # O segundo parâmetro, "$set", é um operador do MongoDB que especifica os
    #       campos do documento que devem ser atualizados com novos valores.
    db.sessoes.update_one({"_id": ObjectId(sessao_id)}, {"$set": {

        "filme_id": ObjectId(filme_id),
        # Atualiza o ID do filme associado à sessão, convertendo a string para ObjectId.
        "sala_id": ObjectId(sala_id),  # Atualiza o ID da sala associada à sessão.
        "data": data_str,  # Atualiza a data da sessão.
        "hora": hora_str,  # Atualiza a hora da sessão.
        "valor_ingresso": valor_ingresso  # Atualiza o valor do ingresso para a sessão.

    }})


# Função para obter uma lista de todos os filmes do banco de dados.
def obter_filmes(db):

    # db.filmes.find() consulta a coleção 'filmes' no banco de dados e
    #       recupera todos os documentos.
    # list() converte o cursor retornado pelo find() em uma lista para ser
    #       mais fácil de manipular e usar em outros lugares do código.
    return list(db.filmes.find())


# Função para criar dois dicionários mapeando os títulos dos
#       filmes aos seus IDs e vice-versa.
def obter_filmes_map(db):

    # Primeiro, obtemos todos os filmes do banco de dados
    #       chamando a função obter_filmes().
    filmes = obter_filmes(db)

    # Criamos um dicionário onde cada título de filme mapeia para seu ID correspondente.
    # A compreensão de dicionário é usada aqui para iterar sobre cada filme em 'filmes'.
    # 'f["titulo"]' é a chave, e 'str(f["_id"])' é o valor, convertendo o
    #       ObjectId para string para melhor manipulação.
    by_title = {f["titulo"]: str(f["_id"]) for f in filmes}

    # Criamos outro dicionário onde cada ID de filme mapeia para
    #       seu título correspondente.
    # Aqui também usamos uma compreensão de dicionário, mas
    #       invertendo as chaves e valores do dicionário anterior.
    by_id = {str(f["_id"]): f["titulo"] for f in filmes}

    # Retornamos ambos os dicionários.
    return by_title, by_id


# Função para obter uma lista de todas as salas do cinema
#       armazenadas no banco de dados.
def obter_salas(db):

    # db.salas.find() realiza uma busca na coleção 'salas', recuperando
    #       todos os documentos (salas).
    # list() é usado para converter o cursor retornado pelo find() em uma
    #       lista de documentos, tornando-a mais fácil de manipular.
    return list(db.salas.find())


# Função para criar dois dicionários mapeando os nomes das
#       salas aos seus IDs e vice-versa.
def obter_salas_map(db):

    # Primeiro, obtemos todas as salas do banco de dados
    #       chamando a função obter_salas().
    salas = obter_salas(db)

    # Criamos um dicionário onde cada nome de sala mapeia para seu ID correspondente.
    # A compreensão de dicionário é usada para iterar sobre cada sala em 'salas'.
    # 's["nome"]' é a chave, e 'str(s["_id"])' é o valor,
    #       convertendo o ObjectId para string.
    by_name = {s["nome"]: str(s["_id"]) for s in salas}

    # Criamos outro dicionário onde cada ID de sala mapeia
    #       para seu nome correspondente.
    # A lógica é a mesma que a anterior, mas invertendo as chaves e
    #       valores para facilitar buscas inversas.
    by_id = {str(s["_id"]): s["nome"] for s in salas}

    # Retornamos ambos os dicionários.
    return by_name, by_id


# SESSÕES
# Função para obter uma lista de todas as sessões armazenadas no banco de dados.
def obter_sessoes(db):

    # db.sessoes.find() busca na coleção 'sessoes' e recupera
    #       todos os documentos (sessões).
    # list() é usado para converter o cursor retornado pelo
    #       método find() em uma lista para fácil manipulação.
    return list(db.sessoes.find())


# Função para obter todas as sessões relacionadas a um filme específico.
def obter_sessoes_por_filme(db, filme_id):

    """
    Esta função busca todas as sessões que correspondem a um determinado filme.
    :param db: Instância da conexão com o banco de dados.
    :param filme_id: ID do filme, que é convertido para ObjectId,
            necessário para a consulta no MongoDB.
    :return: Retorna uma lista de sessões associadas ao filme especificado.
    """

    # db.sessoes.find() busca na coleção 'sessoes' por documentos
    #       onde o 'filme_id' corresponde ao ID fornecido.
    # ObjectId(filme_id) garante que o ID do filme seja no formato
    #       adequado para a consulta.
    return list(db.sessoes.find({"filme_id": ObjectId(filme_id)}))



# Função para obter os detalhes de uma sala específica a partir
#       do seu ID no banco de dados.
def obter_sala_por_id(db, sala_id):

    # db.salas.find_one() busca por um único documento na coleção 'salas'.
    # A busca é feita usando o '_id' da sala, onde 'ObjectId(sala_id)'
    #       garante que o ID passado seja tratado como um ObjectId.
    # Retorna os detalhes da sala, como nome, número de fileiras e
    #       assentos, ou None se nenhuma sala for encontrada com esse ID.
    return db.salas.find_one({"_id": ObjectId(sala_id)})



# Função para obter os detalhes de um filme específico a
#       partir do seu ID no banco de dados.
def obter_filme_por_id(db, filme_id):

    # db.filmes.find_one() é usado para buscar um único documento na coleção 'filmes'.
    # O critério de busca é especificado dentro das chaves, usando o '_id' e
    #       convertendo o 'filme_id' de string para ObjectId.
    # ObjectId(filme_id) converte a string do ID em um ObjectId, que é o
    #       formato de identificação utilizado pelo MongoDB.
    # A função retorna o documento encontrado, que contém os detalhes do
    #       filme, ou None se nenhum filme for encontrado com esse ID.
    return db.filmes.find_one({"_id": ObjectId(filme_id)})


# Função para obter os detalhes de uma sessão específica a
#       partir do seu ID no banco de dados.
def obter_sessao_por_id(db, sessao_id):

    # db.sessoes.find_one() realiza a busca por um único documento na coleção 'sessoes'.
    # A função utiliza 'ObjectId(sessao_id)' para converter o ID da
    #       sessão fornecido de string para ObjectId.
    # Retorna os detalhes da sessão, como o filme, a sala, a data, a
    #       hora e o valor do ingresso, ou None se não encontrar uma sessão com esse ID.
    return db.sessoes.find_one({"_id": ObjectId(sessao_id)})


# Função para limpar o conteúdo de uma lista de campos de entrada.
def limpar_campos(campos):

    # Itera sobre cada item na lista 'campos'.
    for c in campos:

        # isinstance() verifica se o objeto 'c' é uma instância de ttk.Entry, o
        #       que significa que é um campo de entrada.
        if isinstance(c, ttk.Entry):

            # c.delete(0, tk.END) limpa todo o conteúdo do campo, desde o
            #       início (0) até o final (tk.END).
            c.delete(0, tk.END)



# Função para cadastrar uma nova sala de cinema no banco de dados.
def cadastrar_sala(db, nome, fileiras, assentos_por_fileira, tipo_assento):

    # db.salas.insert_one() insere um novo documento na coleção 'salas'.
    # Cada parâmetro da função corresponde a um campo do documento a
    #       ser inserido, descrevendo as características da sala.
    # Retorna o resultado da operação de inserção, que pode incluir o ID
    #       da nova sala inserida entre outras informações úteis.
    return db.salas.insert_one({

        "nome": nome,  # Nome da sala, e.g., "Sala 1"
        "fileiras": fileiras,  # Número de fileiras de assentos na sala
        "assentos_por_fileira": assentos_por_fileira,  # Número de assentos por fileira
        "tipo_assento": tipo_assento  # Tipo de assento, e.g., "VIP", "Normal"

    })


# Função para cadastrar um novo filme no banco de dados.
def cadastrar_filme(db, titulo, duracao, classificacao, genero, sinopse):

    # db.filmes.insert_one() insere um novo documento na coleção 'filmes'.
    # Os parâmetros 'titulo', 'duracao', 'classificacao', 'genero' e 'sinopse'
    #       são usados para criar o documento.
    # Retorna o resultado da operação de inserção, que inclui, entre outras
    #       coisas, o ID do novo filme inserido.
    return db.filmes.insert_one({
        "titulo": titulo,
        "duracao": duracao,
        "classificacao": classificacao,
        "genero": genero,
        "sinopse": sinopse
    })


# Função para cadastrar uma nova sessão no banco de dados.
def cadastrar_sessao(db, filme_id, sala_id, data_str, hora_str, valor_ingresso):

    # db.sessoes.insert_one() insere um novo documento na coleção 'sessoes'.
    # O documento é formado por detalhes da sessão como IDs do
    #       filme e da sala, data, hora e valor do ingresso.
    db.sessoes.insert_one({
        "filme_id": ObjectId(filme_id),  # Converte o ID do filme para ObjectId e armazena.
        "sala_id": ObjectId(sala_id),  # Converte o ID da sala para ObjectId e armazena.
        "data": data_str,  # Armazena a data da sessão como uma string.
        "hora": hora_str,  # Armazena a hora da sessão como uma string.
        "valor_ingresso": valor_ingresso  # Armazena o valor do ingresso.
    })


# Função para criar uma nova janela secundária a partir de
#       uma janela principal.
def criar_janela_secundaria(root, titulo):

    # tk.Toplevel() cria uma nova janela topo de nível que é
    #       filha da janela principal 'root'.
    janela = tk.Toplevel(root)

    # janela.title() define o título da nova janela com o
    #       valor da variável 'titulo'.
    janela.title(titulo)

    # janela.grab_set() faz com que a janela secundária capture
    #       todos os eventos da aplicação, impedindo que outras partes da
    #       aplicação recebam entradas até que esta janela seja fechada.
    janela.grab_set()

    # janela.focus_force() força a janela a ganhar o foco, o que significa
    #       que ela estará imediatamente ativa para receber entradas do usuário.
    janela.focus_force()

    # janela.transient(root) define a janela principal como sua janela mãe,
    #       fazendo com que a janela secundária sempre apareça
    #       em cima da janela principal.
    janela.transient(root)

    # Retorna o objeto da janela criada para que possa ser utilizado
    #       em outras partes do código.
    return janela


# ============================================================
# TELA GERENCIAR SALAS
# ============================================================

def tela_gerenciar_salas(root, db):

    # Configurações para centralizar a janela
    # Define a largura da janela em pixels.
    largura_janela = 900

    # Define a altura da janela em pixels.
    altura_janela = 450

    # Obtém a largura total da tela do monitor.
    largura_tela = root.winfo_screenwidth()

    # Obtém a altura total da tela do monitor.
    altura_tela = root.winfo_screenheight()

    # Calcula a posição X para centralizar a janela na tela.
    pos_x = (largura_tela - largura_janela) // 2

    # Calcula a posição Y para centralizar a janela na tela.
    pos_y = (altura_tela - altura_janela) // 2

    # Cria uma nova janela secundária para gerenciar as salas.
    # O título da janela será "Gerenciar Salas".
    janela = criar_janela_secundaria(root, "Gerenciar Salas")

    # Configura o tamanho e a posição da janela na tela.
    # O tamanho é definido pelas variáveis `largura_janela` e `altura_janela`.
    # A posição é definida pelas variáveis `pos_x` e `pos_y`, centralizando a janela.
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Frame principal
    # Cria um frame principal dentro da janela para agrupar os componentes.
    # Define o preenchimento interno do frame com 10 pixels em cada lado.
    frame_principal = ttk.Frame(janela, padding="10 10 10 10")

    # Define que o frame ocupará todo o espaço disponível na
    #       janela e será redimensionável.
    frame_principal.pack(fill='both', expand=True)

    # Frame da Treeview
    # Cria um frame específico para conter a Treeview (tabela) e
    #       suas barras de rolagem.
    frame_tree = ttk.Frame(frame_principal)

    # Define a posição do frame na grade, ocupando a linha 0 e
    #       coluna 0, com ajuste automático.
    frame_tree.grid(row=0, column=0, sticky="nsew")

    # Configuração da Treeview
    # Define as colunas da Treeview. Cada coluna corresponde a uma propriedade dos dados.
    colunas = ("_id", "nome", "fileiras", "assentos_por_fileira", "tipo_assento")

    # Cria a Treeview com as colunas definidas e a opção "headings"
    #       para mostrar os cabeçalhos.
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings")

    # Itera sobre cada coluna para configurar o cabeçalho e o layout.
    for col in colunas:

        # Define o texto do cabeçalho da coluna como o nome da
        #       coluna com a primeira letra maiúscula.
        tree.heading(col, text=col.capitalize())

        # Define a centralização e largura padrão de cada coluna.
        tree.column(col, anchor="center", width=150)

    # ttk.Scrollbar: Cria uma barra de rolagem vertical no frame 'frame_tree'
    # frame_tree: Indica que a barra de rolagem pertence ao frame 'frame_tree'
    # orient=tk.VERTICAL: Define a orientação da barra como vertical
    # command=tree.yview: Liga a barra de rolagem ao movimento vertical da Treeview
    scrollbar_vertical = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)

    # ttk.Scrollbar: Cria uma barra de rolagem horizontal no frame 'frame_tree'
    # frame_tree: Indica que a barra de rolagem pertence ao frame 'frame_tree'
    # orient=tk.HORIZONTAL: Define a orientação da barra como horizontal
    # command=tree.xview: Liga a barra de rolagem ao movimento horizontal da Treeview
    scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=tree.xview)

    # tree.configure: Configura as barras de rolagem para serem controladas pela Treeview
    # yscrollcommand=scrollbar_vertical.set: Liga o movimento
    #       vertical da Treeview à barra de rolagem vertical
    # xscrollcommand=scrollbar_horizontal.set: Liga o movimento
    #       horizontal da Treeview à barra de rolagem horizontal
    tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    # tree.grid: Posiciona a Treeview no layout grid do frame 'frame_tree'
    # row=0, column=0: Posiciona a Treeview na linha 0, coluna 0 do layout grid
    # sticky="nsew": Faz a Treeview expandir para preencher todo o espaço disponível
    tree.grid(row=0, column=0, sticky="nsew")

    # scrollbar_vertical.grid: Posiciona a barra de rolagem
    #       vertical no layout grid do frame 'frame_tree'
    # row=0, column=1: Posiciona a barra na linha 0, coluna 1 do layout grid
    # sticky="ns": Faz a barra de rolagem vertical preencher todo o espaço vertical
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")

    # scrollbar_horizontal.grid: Posiciona a barra de rolagem
    #       horizontal no layout grid do frame 'frame_tree'
    # row=1, column=0: Posiciona a barra na linha 1, coluna 0 do layout grid
    # sticky="ew": Faz a barra de rolagem horizontal preencher todo o espaço horizontal
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

    # frame_tree.rowconfigure: Ajusta o layout do frame 'frame_tree'
    #       para permitir que o conteúdo da linha 0 se expanda
    # row=0: Define a linha 0 como ajustável
    # weight=1: Dá prioridade de expansão para a linha 0
    frame_tree.rowconfigure(0, weight=1)

    # frame_tree.columnconfigure: Ajusta o layout do frame 'frame_tree'
    #       para permitir que o conteúdo da coluna 0 se expanda
    # column=0: Define a coluna 0 como ajustável
    # weight=1: Dá prioridade de expansão para a coluna 0
    frame_tree.columnconfigure(0, weight=1)

    # ttk.Frame: Cria um frame para organizar os campos e botões de entrada
    # frame_principal: Define o frame pai onde este novo frame será adicionado
    # padding="10 10 10 10": Define espaçamento interno de 10
    #       pixels em todos os lados do frame
    frame_campos = ttk.Frame(frame_principal, padding="10 10 10 10")

    # frame_campos.grid: Posiciona o frame 'frame_campos' no
    #       layout grid do frame pai 'frame_principal'
    # row=1, column=0: Posiciona o frame na linha 1, coluna 0 do layout grid
    # sticky="ew": Faz o frame expandir horizontalmente
    #       para preencher o espaço disponível
    frame_campos.grid(row=1, column=0, sticky="ew")

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Nome:": Define o texto do rótulo como "Nome:"
    # grid: Posiciona o rótulo no layout grid
    # row=0, column=0: Posiciona o rótulo na linha 0, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)

    # ttk.Entry: Cria um campo de entrada de texto no frame 'frame_campos'
    # width=20: Define a largura do campo de entrada como 20 caracteres
    entrada_nome = ttk.Entry(frame_campos, width=20)

    # entrada_nome.grid: Posiciona o campo de entrada no layout grid
    # row=0, column=1: Posiciona o campo de entrada na linha 0, coluna 1 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Fileiras:": Define o texto do rótulo como "Fileiras:"
    # grid: Posiciona o rótulo no layout grid
    # row=0, column=2: Posiciona o rótulo na linha 0, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Fileiras:").grid(row=0, column=2, sticky="e", padx=5, pady=5)

    # ttk.Entry: Cria um campo de entrada de texto no frame 'frame_campos'
    # width=5: Define a largura do campo de entrada como 5 caracteres
    entrada_fileiras = ttk.Entry(frame_campos, width=5)

    # entrada_fileiras.grid: Posiciona o campo de entrada no layout grid
    # row=0, column=3: Posiciona o campo de entrada na linha 0, coluna 3 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    entrada_fileiras.grid(row=0, column=3, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Assentos/Fileira:": Define o texto do rótulo como "Assentos/Fileira:"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=0: Posiciona o rótulo na linha 1, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Assentos/Fileira:").grid(row=1, column=0, sticky="e", padx=5, pady=5)

    # ttk.Entry: Cria um campo de entrada de texto no frame 'frame_campos'
    # width=5: Define a largura do campo de entrada como 5 caracteres
    entrada_assentos_pf = ttk.Entry(frame_campos, width=5)

    # entrada_assentos_pf.grid: Posiciona o campo de entrada no layout grid
    # row=1, column=1: Posiciona o campo de entrada na linha 1, coluna 1 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    entrada_assentos_pf.grid(row=1, column=1, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de seleção do
    #       tipo de assento no frame 'frame_campos'
    # text="Tipo Assento:": Define o texto do rótulo como "Tipo Assento:"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=2: Posiciona o rótulo na linha 1, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Tipo Assento:").grid(row=1, column=2, sticky="e", padx=5, pady=5)

    # ttk.Frame: Cria um frame no 'frame_campos' para agrupar os
    #       botões ou opções relacionadas ao tipo de assento
    frame_tipo_assento = ttk.Frame(frame_campos)

    # frame_tipo_assento.grid: Posiciona o frame no layout grid
    # row=1, column=3: Posiciona o frame na linha 1, coluna 3 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    frame_tipo_assento.grid(row=1, column=3, padx=5, pady=5)

    # tipos_assento: Dicionário que armazena os tipos de assento
    #       disponíveis com suas variáveis de estado associadas
    # "VIP": Representa um tipo de assento especial
    # "Comum": Representa o tipo de assento padrão
    # tk.BooleanVar(): Cria uma variável booleana para armazenar o
    #       estado de cada tipo de assento (selecionado ou não)
    tipos_assento = {"VIP": tk.BooleanVar(), "Comum": tk.BooleanVar()}

    # for: Itera sobre cada tipo de assento no dicionário 'tipos_assento'
    # enumerate: Retorna o índice (idx) e o tipo de assento (tipo) durante a iteração
    for idx, tipo in enumerate(tipos_assento):

        # ttk.Checkbutton: Cria um botão de seleção (checkbox) no frame 'frame_tipo_assento'
        # text=tipo: Define o texto exibido no checkbox como o nome do tipo de assento
        # variable=tipos_assento[tipo]: Liga o estado do checkbox à
        #       variável booleana correspondente no dicionário
        # grid: Posiciona o checkbox no layout grid
        # row=0: Posiciona todos os checkboxes na linha 0
        # column=idx: Posiciona cada checkbox em uma coluna
        #       diferente, de acordo com o índice (idx)
        ttk.Checkbutton(frame_tipo_assento, text=tipo, variable=tipos_assento[tipo]).grid(row=0, column=idx)

    # sala_id_edicao: Lista que armazena o ID da sala que está
    #       sendo editada atualmente
    # [None]: Inicializa a lista com o valor 'None', indicando que
    #       nenhuma sala está em edição
    sala_id_edicao = [None]


    # carregar_salas: Função responsável por carregar as informações
    #       das salas e exibi-las na Treeview
    def carregar_salas():

        # for: Itera sobre todos os itens atualmente exibidos na Treeview
        # tree.get_children(): Obtém uma lista de todos os itens na Treeview
        # tree.delete(i): Remove cada item da Treeview
        for i in tree.get_children():
            tree.delete(i)

        # obter_salas: Função que retorna uma lista de salas do banco de dados
        # salas: Variável que armazena a lista de salas retornada
        salas = obter_salas(db)

        # for: Itera sobre cada sala na lista 'salas'
        for s in salas:

            # tipo_assento_str: Variável que formata os tipos de assento em
            #       uma string separada por vírgulas
            # .get("tipo_assento", {}): Obtém o dicionário de tipos de assento
            #       da sala, ou um dicionário vazio caso não exista
            # .items(): Obtém os pares chave-valor do dicionário de tipos de assento
            # if v: Inclui apenas os tipos de assento que estão marcados como True
            tipo_assento_str = ", ".join([f"{k}" for k, v in s.get("tipo_assento", {}).items() if v])

            # tree.insert: Insere uma nova linha na Treeview
            # "": Indica que o item será inserido na raiz da Treeview (sem pai)
            # tk.END: Adiciona o item no final da Treeview
            # values: Define os valores das colunas do item inserido
            # str(s["_id"]): Converte o ID da sala para string
            # s["nome"]: Nome da sala
            # s["fileiras"]: Quantidade de fileiras
            # s["assentos_por_fileira"]: Quantidade de assentos por fileira
            # tipo_assento_str: String formatada com os tipos de assento
            tree.insert("", tk.END,
                        values=(str(s["_id"]), s["nome"], s["fileiras"], s["assentos_por_fileira"], tipo_assento_str))


    # Função chamada ao selecionar um item na Treeview
    def on_tree_select(event):

        # Obtém a seleção atual da Treeview
        # tree.selection(): Retorna o ID do item selecionado
        sel = tree.selection()

        # Verifica se nenhum item foi selecionado
        # if not sel: Caso a seleção esteja vazia, a função retorna sem fazer nada
        if not sel:
            return

        # Obtém as informações do item selecionado na Treeview
        # tree.item(sel): Retorna os dados associados ao item selecionado
        item = tree.item(sel)

        # Extrai os valores do item selecionado
        # vals: Lista de valores do item selecionado na Treeview
        vals = item["values"]

        # Atualiza a variável global para armazenar o ID da
        #       sala que está sendo editada
        # sala_id_edicao[0]: Recebe o ID da sala (primeiro valor da lista)
        sala_id_edicao[0] = vals[0]

        # Atualiza o campo de entrada do nome da sala
        # entrada_nome.delete(0, tk.END): Remove o texto atual no campo
        # entrada_nome.insert(0, vals[1]): Insere o nome da sala no campo
        entrada_nome.delete(0, tk.END)
        entrada_nome.insert(0, vals[1])

        # Atualiza o campo de entrada do número de fileiras
        # entrada_fileiras.delete(0, tk.END): Remove o texto atual no campo
        # entrada_fileiras.insert(0, vals[2]): Insere o número de fileiras no campo
        entrada_fileiras.delete(0, tk.END)
        entrada_fileiras.insert(0, vals[2])

        # Atualiza o campo de entrada do número de assentos por fileira
        # entrada_assentos_pf.delete(0, tk.END): Remove o texto atual no campo
        # entrada_assentos_pf.insert(0, vals[3]): Insere o número
        #       de assentos por fileira no campo
        entrada_assentos_pf.delete(0, tk.END)
        entrada_assentos_pf.insert(0, vals[3])

        # Limpa as opções de tipos de assento selecionadas
        # limpar_tipo_assento(): Define todos os valores das checkboxes para False
        limpar_tipo_assento()

        # Atualiza os tipos de assento selecionados com base nos valores do item selecionado
        # vals[4]: Contém os tipos de assento como uma string separada por vírgulas
        # tipo in tipos_assento: Verifica se o tipo de assento está entre os tipos disponíveis
        # tipos_assento[tipo].set(True): Marca a checkbox correspondente ao tipo de assento
        for tipo in vals[4].split(", "):
            if tipo in tipos_assento:
                tipos_assento[tipo].set(True)


    # Função que retorna os tipos de assento selecionados
    def obter_tipos_assento():

        # {tipo: var.get() for tipo, var in tipos_assento.items()}:
        # Cria um dicionário com os tipos de assento (chave) e seus estados (valor)
        #   usando compreensão de dicionário.
        # tipo: Nome do tipo de assento (ex.: "VIP", "Comum").
        # var.get(): Obtém o estado atual (True ou False) da variável associada ao tipo.
        return {tipo: var.get() for tipo, var in tipos_assento.items()}


    # Função que cadastra uma nova sala no banco de dados
    def cadastrar_novo():

        # Obtém o valor do campo de entrada 'Nome' e remove espaços em branco extras
        nome = entrada_nome.get().strip()

        # Obtém o valor do campo de entrada 'Fileiras' e remove espaços em branco extras
        fileiras = entrada_fileiras.get().strip()

        # Obtém o valor do campo de entrada 'Assentos por Fileira' e
        #       remove espaços em branco extras
        assentos_pf = entrada_assentos_pf.get().strip()

        # Obtém os tipos de assento selecionados utilizando a função 'obter_tipos_assento'
        tipos_selecionados = obter_tipos_assento()

        # Verifica se os campos 'nome', 'fileiras' e 'assentos_pf' estão preenchidos
        # all: Retorna True se todos os valores na lista forem verdadeiros,
        #       caso contrário retorna False
        if not all([nome, fileiras, assentos_pf]):

            # messagebox.showerror: Exibe uma mensagem de erro caso
            #       algum campo não esteja preenchido
            # "Erro": Título da janela de mensagem
            # "Preencha todos os campos!": Mensagem de erro exibida ao usuário
            # parent=janela: Define que a janela 'janela' é o pai da mensagem de erro
            messagebox.showerror("Erro", "Preencha todos os campos!", parent=janela)
            return

        # Tenta converter os valores de 'fileiras' e 'assentos_pf' para inteiros
        try:

            # fileiras: Converte o valor do campo 'fileiras' para um número inteiro
            fileiras = int(fileiras)

            # assentos_pf: Converte o valor do campo 'assentos_pf' para um número inteiro
            assentos_pf = int(assentos_pf)

        # Trata exceção caso os valores fornecidos não sejam números inteiros válidos
        except ValueError:

            # messagebox.showerror: Exibe uma mensagem de erro informando
            #       que os campos devem ser números
            # "Erro": Título da janela de mensagem
            # "Fileiras e Assentos por fileira devem ser números!":
            #       Mensagem de erro exibida ao usuário
            # parent=janela: Define que a janela 'janela' é o pai da mensagem de erro
            messagebox.showerror("Erro",
                                 "Fileiras e Assentos por fileira devem ser números!",
                                 parent=janela)

            # return: Encerra a execução da função caso ocorra o erro
            return

        # cadastra_sala: Função que insere uma nova sala no banco de dados
        # db: Conexão com o banco de dados
        # nome: Nome da sala a ser cadastrada
        # fileiras: Número de fileiras da sala
        # assentos_pf: Número de assentos por fileira
        # tipos_selecionados: Dicionário indicando os tipos de assentos
        #       selecionados (ex.: {"VIP": True, "Comum": False})
        cadastrar_sala(db, nome, fileiras, assentos_pf, tipos_selecionados)

        # messagebox.showinfo: Exibe uma mensagem de sucesso
        #       informando que a sala foi cadastrada
        # "Sucesso": Título da mensagem de sucesso
        # "Sala cadastrada!": Mensagem exibida ao usuário
        # parent=janela: Define que a janela 'janela' é o pai da mensagem de sucesso
        messagebox.showinfo("Sucesso", "Sala cadastrada!", parent=janela)

        # carregar_salas: Função que atualiza a Treeview
        #       carregando as salas do banco de dados
        carregar_salas()

        # limpar_tipo_assento: Função que desmarca todas as opções de tipo de assento
        limpar_tipo_assento()

        # entrada_nome.delete: Limpa o campo de entrada de texto para 'nome'
        # 0, tk.END: Remove o texto desde o início até o fim do campo
        entrada_nome.delete(0, tk.END)

        # entrada_fileiras.delete: Limpa o campo de entrada de texto para 'fileiras'
        # 0, tk.END: Remove o texto desde o início até o fim do campo
        entrada_fileiras.delete(0, tk.END)

        # entrada_assentos_pf.delete: Limpa o campo de entrada de
        #       texto para 'assentos por fileira'
        # 0, tk.END: Remove o texto desde o início até o fim do campo
        entrada_assentos_pf.delete(0, tk.END)


    # Função que reseta todas as opções de tipos de assento para False
    def limpar_tipo_assento():

        # for: Itera sobre todas as variáveis associadas aos tipos de assento
        # tipos_assento.values(): Retorna os valores (variáveis BooleanVar) do
        #       dicionário 'tipos_assento'.
        # var.set(False): Define o valor de cada variável como False,
        #       desmarcando todos os checkboxes.
        for var in tipos_assento.values():
            var.set(False)


    # Função que salva as alterações feitas na sala selecionada
    def salvar_alteracoes():

        # Verifica se há uma sala em edição
        # sala_id_edicao[0]: Identificador da sala que está sendo editada
        # Caso não exista uma sala selecionada, exibe uma mensagem de erro e retorna
        if not sala_id_edicao[0]:

            # messagebox.showerror: Exibe uma mensagem de erro
            # "Erro": Título da mensagem de erro
            # "Nenhuma sala selecionada!": Mensagem exibida ao usuário
            # parent=janela: Define que a janela 'janela' é o pai da mensagem de erro
            messagebox.showerror("Erro", "Nenhuma sala selecionada!", parent=janela)
            return

        # Obtém o valor do campo de entrada 'nome' removendo espaços em branco extras
        # entrada_nome.get(): Pega o valor atual do campo de texto
        # strip(): Remove espaços antes e depois do texto
        nome = entrada_nome.get().strip()

        # Obtém o valor do campo de entrada 'fileiras'
        #       removendo espaços em branco extras
        fileiras = entrada_fileiras.get().strip()

        # Obtém o valor do campo de entrada 'assentos por fileira'
        #       removendo espaços em branco extras
        assentos_pf = entrada_assentos_pf.get().strip()

        # obter_tipos_assento: Retorna um dicionário indicando os
        #       tipos de assentos selecionados
        # Ex.: {"VIP": True, "Comum": False}
        tipos_selecionados = obter_tipos_assento()

        # Verifica se todos os campos obrigatórios estão preenchidos
        # all([nome, fileiras, assentos_pf]): Retorna True se todos os valores forem não vazios
        # Caso algum campo esteja vazio, exibe uma mensagem de erro e interrompe a função
        if not all([nome, fileiras, assentos_pf]):

            # messagebox.showerror: Exibe uma mensagem de erro para o usuário
            # "Erro": Título da mensagem
            # "Preencha todos os campos!": Texto informando o problema
            # parent=janela: Define a janela pai para a mensagem de erro
            messagebox.showerror("Erro", "Preencha todos os campos!", parent=janela)
            return

        # Tenta converter os valores de fileiras e assentos
        #       por fileira para inteiros
        try:

            # Converte o valor de 'fileiras' para inteiro
            fileiras = int(fileiras)

            # Converte o valor de 'assentos por fileira' para inteiro
            assentos_pf = int(assentos_pf)

        except ValueError:

            # Caso a conversão falhe, exibe uma mensagem de erro
            #       indicando que os valores devem ser números
            # "Erro": Título da mensagem
            # "Fileiras e Assentos por fileira devem ser
            #       números!": Texto informando o problema
            messagebox.showerror("Erro",
                                 "Fileiras e Assentos por fileira devem ser números!",
                                 parent=janela)
            return

        # Atualiza as informações da sala no banco de dados
        # atualizar_sala: Chama a função para atualizar uma sala no banco
        # db: Conexão com o banco de dados
        # sala_id_edicao[0]: ID da sala que está sendo editada
        # nome, fileiras, assentos_pf, tipos_selecionados: Novos valores para atualizar a sala
        atualizar_sala(db, sala_id_edicao[0], nome, fileiras, assentos_pf, tipos_selecionados)

        # Exibe uma mensagem informando que a sala foi atualizada com sucesso
        # messagebox.showinfo: Exibe uma mensagem de informação para o usuário
        # "Sucesso": Título da mensagem
        # "Sala atualizada!": Texto informando o sucesso da atualização
        # parent=janela: Define a janela pai para a mensagem de informação
        messagebox.showinfo("Sucesso", "Sala atualizada!", parent=janela)

        # Recarrega a lista de salas na Treeview para refletir a alteração
        carregar_salas()

        # Limpa as seleções dos tipos de assento
        limpar_tipo_assento()

        # Limpa o campo de entrada 'Nome'
        # delete(0, tk.END): Remove todo o texto do campo de entrada
        entrada_nome.delete(0, tk.END)

        # Limpa o campo de entrada 'Fileiras'
        entrada_fileiras.delete(0, tk.END)

        # Limpa o campo de entrada 'Assentos por fileira'
        entrada_assentos_pf.delete(0, tk.END)


    # Função para deletar a sala selecionada na Treeview
    def deletar_item():

        # Obtém a seleção atual da Treeview
        # tree.selection(): Retorna o ID do item selecionado
        sel = tree.selection()

        # Verifica se nenhuma sala foi selecionada
        # if not sel: Caso a seleção esteja vazia
        # messagebox.showerror: Exibe uma mensagem de erro informando
        #       que é necessário selecionar uma sala
        if not sel:
            messagebox.showerror("Erro", "Selecione uma sala!", parent=janela)
            return

        # Obtém as informações do item selecionado na Treeview
        # tree.item(sel): Retorna os dados associados ao item selecionado
        item = tree.item(sel)

        # Obtém o ID da sala a partir do item selecionado
        # item["values"][0]: O primeiro valor na lista de valores do item é o ID da sala
        sid = item["values"][0]

        # Solicita confirmação ao usuário antes de deletar a sala
        # messagebox.askyesno: Exibe uma mensagem de confirmação com as opções 'Sim' e 'Não'
        # resp: Variável que armazena o resultado da confirmação (True para 'Sim', False para 'Não')
        resp = messagebox.askyesno("Confirmar", "Deseja deletar a sala?", parent=janela)

        # Verifica se o usuário confirmou a exclusão
        if resp:

            # Chama a função para deletar a sala no banco de dados
            # deletar_sala: Remove a sala com o ID fornecido
            # db: Conexão com o banco de dados
            # sid: ID da sala a ser deletada
            deletar_sala(db, sid)

            # Recarrega a lista de salas na Treeview para refletir a exclusão
            carregar_salas()


    # Associa o evento de seleção na Treeview à função on_tree_select
    # tree.bind("<<TreeviewSelect>>", on_tree_select): Quando um
    #       item é selecionado na Treeview,
    # a função on_tree_select é chamada para atualizar os
    #       campos de entrada com os dados do item selecionado.
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Botão para cadastrar uma nova sala
    # ttk.Button: Cria um botão no frame 'frame_campos'
    # text="Cadastrar Novo": Define o texto exibido no botão
    # command=cadastrar_novo: Associa a função cadastrar_novo ao
    #       botão, chamada ao clicar
    # grid(row=2, column=0, padx=5, pady=5): Posiciona o botão na
    #       linha 2, coluna 0, com espaçamento de 5 pixels
    ttk.Button(frame_campos,
               text="Cadastrar Novo",
               command=cadastrar_novo).grid(row=2, column=0, padx=5, pady=5)

    # Botão para salvar alterações em uma sala existente
    # ttk.Button: Cria um botão no frame 'frame_campos'
    # text="Salvar Alterações": Define o texto exibido no botão
    # command=salvar_alteracoes: Associa a função salvar_alteracoes ao
    #       botão, chamada ao clicar
    # grid(row=2, column=2, padx=5, pady=5): Posiciona o botão na
    #       linha 2, coluna 2, com espaçamento de 5 pixels
    ttk.Button(frame_campos,
               text="Salvar Alterações",
               command=salvar_alteracoes).grid(row=2, column=2, padx=5, pady=5)

    # Botão para deletar uma sala selecionada
    # ttk.Button: Cria um botão no frame 'frame_campos'
    # text="Deletar": Define o texto exibido no botão
    # command=deletar_item: Associa a função deletar_item ao
    #       botão, chamada ao clicar
    # grid(row=2, column=3, padx=5, pady=5): Posiciona o botão na
    #       linha 2, coluna 3, com espaçamento de 5 pixels
    ttk.Button(frame_campos,
               text="Deletar",
               command=deletar_item).grid(row=2, column=3, padx=5, pady=5)

    # Chama a função carregar_salas para exibir as salas no início
    # carregar_salas(): Preenche a Treeview com os dados das
    #       salas armazenadas no banco de dados
    carregar_salas()


# ============================================================
# TELA GERENCIAR SESSÕES
# ============================================================

def tela_gerenciar_sessoes(root, db):

    # Configurações para centralizar a janela

    # largura_janela: Define a largura da janela como 900 pixels
    largura_janela = 900

    # altura_janela: Define a altura da janela como 450 pixels
    altura_janela = 450

    # largura_tela: Obtém a largura total da tela principal
    largura_tela = root.winfo_screenwidth()

    # altura_tela: Obtém a altura total da tela principal
    altura_tela = root.winfo_screenheight()

    # pos_x: Calcula a posição X para centralizar a janela na tela
    pos_x = (largura_tela - largura_janela) // 2

    # pos_y: Calcula a posição Y para centralizar a janela na tela
    pos_y = (altura_tela - altura_janela) // 2

    # janela: Cria uma nova janela secundária para gerenciar as sessões
    janela = criar_janela_secundaria(root, "Gerenciar Sessões")

    # geometry: Define o tamanho e a posição da janela
    # f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}":
    #       Especifica as dimensões e posição calculadas
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Frame principal

    # frame_principal: Cria um frame principal dentro da janela
    #       para organizar os elementos
    frame_principal = ttk.Frame(janela, padding="10 10 10 10")

    # pack: Posiciona o frame para preencher toda a janela (expandindo
    #       tanto em largura quanto em altura)
    frame_principal.pack(fill='both', expand=True)

    # Configuração da Treeview

    # colunas: Define as colunas da Treeview para exibir os dados das sessões
    colunas = ("_id", "filme_id", "sala_id", "data", "hora", "valor_ingresso")

    # frame_tree: Cria um frame dentro do frame principal para acomodar a Treeview
    frame_tree = ttk.Frame(frame_principal)

    # grid: Posiciona o frame da Treeview no layout grid
    # row=0, column=0: Define a posição na primeira linha e primeira coluna
    # sticky="nsew": Expande o frame para preencher o espaço disponível
    frame_tree.grid(row=0, column=0, sticky="nsew")

    # tree: Cria uma Treeview dentro do frame da Treeview
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings")

    # for col in colunas: Itera sobre cada coluna
    #       definida na variável colunas
    for col in colunas:

        # tree.heading: Define o cabeçalho de cada coluna
        # col: Define a coluna atual
        # text=col.capitalize(): Define o texto do cabeçalho com a
        #       primeira letra em maiúscula
        tree.heading(col, text=col.capitalize())

        # tree.column: Configura a coluna atual
        # col: Define a coluna a ser configurada
        # anchor="center": Centraliza o conteúdo da coluna
        # width=150: Define a largura da coluna em pixels
        tree.column(col, anchor="center", width=150)

    # Barras de rolagem

    # scrollbar_vertical: Cria uma barra de rolagem vertical
    # ttk.Scrollbar: Componente de barra de rolagem
    # frame_tree: Adiciona a barra ao frame_tree
    # orient=tk.VERTICAL: Define a orientação como vertical
    # command=tree.yview: Vincula a rolagem vertical à visualização da Treeview
    scrollbar_vertical = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)

    # scrollbar_horizontal: Cria uma barra de rolagem horizontal
    # orient=tk.HORIZONTAL: Define a orientação como horizontal
    # command=tree.xview: Vincula a rolagem horizontal à visualização da Treeview
    scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=tree.xview)

    # tree.configure: Configura as barras de rolagem para a Treeview
    # yscrollcommand=scrollbar_vertical.set: Vincula a barra vertical à Treeview
    # xscrollcommand=scrollbar_horizontal.set: Vincula a barra horizontal à Treeview
    tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    # tree.grid: Posiciona a Treeview no layout
    # row=0, column=0: Coloca a Treeview na linha 0, coluna 0 do grid
    # sticky="nsew": Expande a Treeview para preencher a célula
    tree.grid(row=0, column=0, sticky="nsew")

    # scrollbar_vertical.grid: Posiciona a barra de rolagem vertical no layout
    # row=0, column=1: Coloca a barra na linha 0, coluna 1
    # sticky="ns": Expande verticalmente (north-south)
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")

    # scrollbar_horizontal.grid: Posiciona a barra de rolagem horizontal no layout
    # row=1, column=0: Coloca a barra na linha 1, coluna 0
    # sticky="ew": Expande horizontalmente (east-west)
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

    # Ajuste de layout para expandir a Treeview

    # frame_tree.rowconfigure(0, weight=1): Configura a linha 0 do
    #       frame_tree para expandir dinamicamente
    # weight=1: Define que a linha recebe prioridade na expansão
    frame_tree.rowconfigure(0, weight=1)

    # frame_tree.columnconfigure(0, weight=1): Configura a
    #       coluna 0 do frame_tree para expandir dinamicamente
    # weight=1: Define que a coluna recebe prioridade na expansão
    frame_tree.columnconfigure(0, weight=1)

    # Frame de campos e botões

    # frame_campos: Cria um frame para organizar campos de entrada e botões
    # ttk.Frame: Widget do Tkinter para agrupar elementos
    # frame_principal: Define que o frame_campos será filho do frame_principal
    # padding="10 10 10 10": Adiciona espaçamento interno de 10 pixels em todos os lados
    frame_campos = ttk.Frame(frame_principal, padding="10 10 10 10")

    # frame_campos.grid: Posiciona o frame_campos no layout
    # row=1, column=0: Coloca o frame na linha 1, coluna 0 do grid
    # sticky="ew": Expande o frame horizontalmente para preencher a célula
    frame_campos.grid(row=1, column=0, sticky="ew")

    # Mapas de filmes e salas

    # filmes_by_title, filmes_by_id: Obtém dicionários mapeando
    #       títulos de filmes para IDs e vice-versa
    # obter_filmes_map: Função que retorna dois dicionários (título
    #       para ID, ID para título)
    # db: Conexão com o banco de dados para buscar os filmes
    filmes_by_title, filmes_by_id = obter_filmes_map(db)

    # salas_by_name, salas_by_id: Obtém dicionários mapeando nomes de
    #       salas para IDs e vice-versa
    # obter_salas_map: Função que retorna dois dicionários (nome
    #       para ID, ID para nome)
    # db: Conexão com o banco de dados para buscar as salas
    salas_by_name, salas_by_id = obter_salas_map(db)

    # Campos de entrada

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Filme:": Define o texto do rótulo como "Filme:"
    # grid: Posiciona o rótulo no layout grid
    # row=0, column=0: Posiciona o rótulo na linha 0, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Filme:").grid(row=0, column=0, sticky="e", padx=5, pady=5)

    # combo_filme: Cria uma caixa de seleção (combobox) para escolha de filmes
    # ttk.Combobox: Widget do Tkinter para criar um combobox
    # frame_campos: Define que o combobox será filho do frame_campos
    # values=list(filmes_by_title.keys()): Define os valores
    #       disponíveis na combobox como os títulos dos filmes
    # width=30: Define a largura do combobox como 30 caracteres
    combo_filme = ttk.Combobox(frame_campos, values=list(filmes_by_title.keys()), width=30)

    # combo_filme.grid: Posiciona o combobox no layout
    # row=0, column=1: Coloca o combobox na linha 0, coluna 1 do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    combo_filme.grid(row=0, column=1, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Sala:": Define o texto do rótulo como "Sala:"
    # grid: Posiciona o rótulo no layout grid
    # row=0, column=2: Posiciona o rótulo na linha 0, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Sala:").grid(row=0, column=2, sticky="e", padx=5, pady=5)

    # combo_sala: Cria uma caixa de seleção (combobox) para escolha de salas
    # ttk.Combobox: Widget do Tkinter para criar um combobox
    # frame_campos: Define que o combobox será filho do frame_campos
    # values=list(salas_by_name.keys()): Define os valores
    #       disponíveis na combobox como os nomes das salas
    # width=20: Define a largura do combobox como 20 caracteres
    combo_sala = ttk.Combobox(frame_campos, values=list(salas_by_name.keys()), width=20)

    # combo_sala.grid: Posiciona o combobox no layout
    # row=0, column=3: Coloca o combobox na linha 0, coluna 3 do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    combo_sala.grid(row=0, column=3, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Data (AAAA-MM-DD):": Define o texto do rótulo como "Data (AAAA-MM-DD):"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=0: Coloca o rótulo na linha 1, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Data (AAAA-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)

    # entrada_data: Cria um campo de entrada de texto para a data
    # ttk.Entry: Widget do Tkinter para criar um campo de entrada de texto
    # frame_campos: Define que o campo será filho do frame_campos
    # width=15: Define a largura do campo de entrada como 15 caracteres
    entrada_data = ttk.Entry(frame_campos, width=15)

    # entrada_data.grid: Posiciona o campo de entrada no layout grid
    # row=1, column=1: Coloca o campo de entrada na linha 1, coluna 1 do layout grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    entrada_data.grid(row=1, column=1, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Hora (HH:MM):": Define o texto do rótulo como "Hora (HH:MM):"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=2: Coloca o rótulo na linha 1, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos, text="Hora (HH:MM):").grid(row=1, column=2, sticky="e", padx=5, pady=5)

    # entrada_hora: Cria um campo de entrada de texto para a hora
    # ttk.Entry: Widget do Tkinter para criar um campo de entrada de texto
    # frame_campos: Define que o campo será filho do frame_campos
    # width=10: Define a largura do campo de entrada como 10 caracteres
    entrada_hora = ttk.Entry(frame_campos, width=10)

    # entrada_hora.grid: Posiciona o campo de entrada no layout grid
    # row=1, column=3: Coloca o campo de entrada na linha 1, coluna 3 do layout grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    entrada_hora.grid(row=1, column=3, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_campos'
    # text="Valor Ingresso:": Define o texto do rótulo como "Valor Ingresso:"
    # grid: Posiciona o rótulo no layout grid
    # row=2, column=0: Coloca o rótulo na linha 2, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_campos,
              text="Valor Ingresso:").grid(row=2, column=0, sticky="e", padx=5, pady=5)

    # entrada_valor: Cria um campo de entrada de texto para o valor do ingresso
    # ttk.Entry: Widget do Tkinter para criar um campo de entrada de texto
    # frame_campos: Define que o campo será filho do frame_campos
    # width=10: Define a largura do campo de entrada como 10 caracteres
    entrada_valor = ttk.Entry(frame_campos, width=10)

    # entrada_valor.grid: Posiciona o campo de entrada no layout grid
    # row=2, column=1: Coloca o campo de entrada na linha 2, coluna 1 do layout grid
    # padx=5, pady=5: Define espaçamento horizontal e vertical de 5 pixels
    entrada_valor.grid(row=2, column=1, padx=5, pady=5)

    # Variável para edição
    # sessao_id_edicao: Armazena o ID da sessão que está sendo editada atualmente
    # Inicializada com uma lista contendo None para facilitar a manipulação global
    sessao_id_edicao = [None]


    # Função para carregar sessões na Treeview
    def carregar_sessoes():

        # tree.get_children(): Obtém todos os itens atualmente exibidos na Treeview
        # tree.delete(i): Remove cada item da Treeview para recarregar os dados
        for i in tree.get_children():
            tree.delete(i)

        # obter_sessoes(db): Busca todas as sessões no banco de dados
        sessoes = obter_sessoes(db)

        # Itera sobre todas as sessões retornadas
        for s in sessoes:

            # filmes_by_id.get: Obtém o título do filme a partir do ID do filme na sessão
            # str(s["filme_id"]): Converte o ID do filme para string
            # Retorna "?" caso o ID do filme não seja encontrado
            filme_text = filmes_by_id.get(str(s["filme_id"]), "?")

            # salas_by_id.get: Obtém o nome da sala a partir do ID da sala na sessão
            # str(s["sala_id"]): Converte o ID da sala para string
            # Retorna "?" caso o ID da sala não seja encontrado
            sala_text = salas_by_id.get(str(s["sala_id"]), "?")

            # tree.insert: Adiciona uma nova linha na Treeview
            # "" como primeiro argumento significa que o item não tem pai (nível raiz)
            # tk.END: Insere o item no final da lista
            # values: Define os valores a serem exibidos nas colunas
            tree.insert("", tk.END, values=(
                str(s["_id"]),  # ID da sessão
                filme_text,  # Título do filme
                sala_text,  # Nome da sala
                s["data"],  # Data da sessão
                s["hora"],  # Hora da sessão
                s["valor_ingresso"]  # Valor do ingresso
            ))


    def on_tree_select(event):

        # Seleciona o item atualmente destacado na Treeview.
        sel = tree.selection()

        # Se nenhuma seleção for feita, a função será interrompida aqui.
        if not sel:
            return

        # Obtém o item selecionado a partir do identificador,
        #       incluindo os valores associados.
        item = tree.item(sel)

        # 'vals' contém todos os valores do item selecionado na
        #       Treeview (ID da sessão, filme, sala, data, hora, valor do ingresso).
        vals = item["values"]

        # Armazena o ID da sessão em uma variável para uso em operações de edição.
        sessao_id_edicao[0] = vals[0]

        # Ajusta o Combobox do filme para mostrar o filme atualmente selecionado na sessão.
        combo_filme.set(vals[1])

        # Ajusta o Combobox da sala para mostrar a sala atualmente selecionada na sessão.
        combo_sala.set(vals[2])

        # Limpa e insere a data da sessão no campo de entrada correspondente.
        entrada_data.delete(0, tk.END)
        entrada_data.insert(0, vals[3])

        # Limpa e insere a hora da sessão no campo de entrada correspondente.
        entrada_hora.delete(0, tk.END)
        entrada_hora.insert(0, vals[4])

        # Limpa e insere o valor do ingresso no campo de entrada correspondente.
        entrada_valor.delete(0, tk.END)
        entrada_valor.insert(0, vals[5])


    # Função para cadastrar uma nova sessão
    def cadastrar_novo():

        # combo_filme.get(): Obtém o filme selecionado no Combobox
        # strip(): Remove espaços extras no início e no final do texto
        # Atribui o valor à variável 'f' (filme)
        f = combo_filme.get().strip()

        # combo_sala.get(): Obtém a sala selecionada no Combobox
        # strip(): Remove espaços extras no início e no final do texto
        # Atribui o valor à variável 'sl' (sala)
        sl = combo_sala.get().strip()

        # entrada_data.get(): Obtém o valor inserido no campo de entrada para a data
        # strip(): Remove espaços extras no início e no final do texto
        # Atribui o valor à variável 'data_str'
        data_str = entrada_data.get().strip()

        # entrada_hora.get(): Obtém o valor inserido no campo de entrada para a hora
        # strip(): Remove espaços extras no início e no final do texto
        # Atribui o valor à variável 'hora_str'
        hora_str = entrada_hora.get().strip()

        # entrada_valor.get(): Obtém o valor inserido no campo de
        #       entrada para o valor do ingresso
        # strip(): Remove espaços extras no início e no final do texto
        # Atribui o valor à variável 'valor_str'
        valor_str = entrada_valor.get().strip()

        # all([f, sl, data_str, hora_str, valor_str]): Verifica se todos os
        #       campos possuem valores preenchidos
        # Caso algum campo esteja vazio, exibe uma mensagem de erro
        if not all([f, sl, data_str, hora_str, valor_str]):

            # messagebox.showerror(): Exibe uma janela de erro
            # "Erro": Título da janela
            # "Preencha todos os campos!": Mensagem exibida na janela
            # parent=janela: Define a janela principal como pai da mensagem
            messagebox.showerror("Erro", "Preencha todos os campos!", parent=janela)

            return  # Encerra a função sem continuar

        # Verifica se o filme selecionado é válido
        if f not in filmes_by_title:

            # messagebox.showerror(): Exibe uma janela de erro
            # "Erro": Título da janela
            # "Filme inválido!": Mensagem exibida informando que o filme não é válido
            # parent=janela: Define a janela principal como pai da mensagem
            messagebox.showerror("Erro", "Filme inválido!", parent=janela)

            return  # Encerra a função sem continuar

        # Verifica se a sala selecionada é válida
        if sl not in salas_by_name:

            # messagebox.showerror(): Exibe uma janela de erro
            # "Erro": Título da janela
            # "Sala inválida!": Mensagem exibida informando que a sala não é válida
            # parent=janela: Define a janela principal como pai da mensagem
            messagebox.showerror("Erro", "Sala inválida!", parent=janela)

            return  # Encerra a função sem continuar

        # Tenta converter o valor do ingresso para um número do tipo float
        try:

            # float(valor_str): Converte o texto inserido no campo de
            #       valor do ingresso para um número
            # Atribui o número à variável 'valor'
            valor = float(valor_str)

        except ValueError:

            # Caso a conversão falhe, exibe uma mensagem de erro
            # messagebox.showerror(): Exibe uma janela de erro
            # "Erro": Título da janela
            # "Valor ingresso deve ser número!": Mensagem exibida informando o erro
            # parent=janela: Define a janela principal como pai da mensagem
            messagebox.showerror("Erro",
                                 "Valor ingresso deve ser número!", parent=janela)

            # Encerra a função sem continuar
            return

        # Chama a função para cadastrar uma nova sessão no banco de dados
        # cadastrar_sessao(): Função que realiza o cadastro de uma sessão no banco
        # Passa os parâmetros:
        # db: O banco de dados
        # filmes_by_title[f]: Obtém o ID do filme a partir do título selecionado na combobox
        # salas_by_name[sl]: Obtém o ID da sala a partir do nome selecionado na combobox
        # data_str: A data da sessão fornecida pelo usuário
        # hora_str: A hora da sessão fornecida pelo usuário
        # valor: O valor do ingresso, que foi convertido para número
        cadastrar_sessao(db,
                         filmes_by_title[f], salas_by_name[sl], data_str, hora_str, valor)

        # Exibe uma mensagem informando que a sessão foi cadastrada com sucesso
        # messagebox.showinfo(): Exibe uma janela de informação
        # "Sucesso": Título da janela
        # "Sessão cadastrada!": Mensagem informando que a sessão foi cadastrada com sucesso
        # parent=janela: Define a janela principal como pai da mensagem
        messagebox.showinfo("Sucesso", "Sessão cadastrada!", parent=janela)

        # Chama a função para recarregar as sessões na Treeview
        # Isso atualiza a lista de sessões exibida para o usuário
        carregar_sessoes()

        # Limpa os campos de entrada após o cadastro da sessão
        # combo_filme.set(""): Limpa a seleção da combobox de filmes
        combo_filme.set("")

        # combo_sala.set(""): Limpa a seleção da combobox de salas
        combo_sala.set("")

        # entrada_data.delete(0, tk.END): Limpa o campo de entrada de data
        entrada_data.delete(0, tk.END)

        # entrada_hora.delete(0, tk.END): Limpa o campo de entrada de hora
        entrada_hora.delete(0, tk.END)

        # entrada_valor.delete(0, tk.END): Limpa o campo de
        #       entrada de valor do ingresso
        entrada_valor.delete(0, tk.END)


    def salvar_alteracoes():

        # Verifica se uma sessão está selecionada para edição
        # sessao_id_edicao[0]: Armazena o ID da sessão que está sendo editada
        # Se não houver uma sessão selecionada, exibe uma mensagem de erro
        if not sessao_id_edicao[0]:

            # messagebox.showerror(): Exibe uma caixa de erro
            # "Erro": Título da janela de erro
            # "Nenhuma sessão selecionada!": Mensagem de erro
            # parent=janela: Define a janela principal como a janela de erro
            messagebox.showerror("Erro",
                                 "Nenhuma sessão selecionada!", parent=janela)

            # Se não houver sessão selecionada, a função é encerrada
            return

        # Obtém os valores das entradas fornecidas pelo usuário
        # combo_filme.get(): Obtém o título do filme selecionado na combobox
        f = combo_filme.get().strip()

        # combo_sala.get(): Obtém o nome da sala selecionada na combobox
        sl = combo_sala.get().strip()

        # entrada_data.get(): Obtém a data fornecida pelo usuário
        data_str = entrada_data.get().strip()

        # entrada_hora.get(): Obtém a hora fornecida pelo usuário
        hora_str = entrada_hora.get().strip()

        # entrada_valor.get(): Obtém o valor do ingresso fornecido pelo usuário
        valor_str = entrada_valor.get().strip()

        # Verifica se todos os campos foram preenchidos
        # all(): Verifica se todas as condições são verdadeiras
        if not all([f, sl, data_str, hora_str, valor_str]):

            # messagebox.showerror(): Exibe uma caixa de erro
            # "Erro": Título da janela de erro
            # "Preencha todos os campos!": Mensagem de erro
            # parent=janela: Define a janela principal como a janela de erro
            messagebox.showerror("Erro",
                                 "Preencha todos os campos!", parent=janela)

            # Se algum campo não foi preenchido, a função é encerrada
            return

        # Verifica se o filme selecionado é válido
        # f not in filmes_by_title: Verifica se o filme selecionado
        #       não está na lista de filmes disponíveis
        if f not in filmes_by_title:

            # Exibe uma mensagem de erro informando que o filme selecionado é inválido
            messagebox.showerror("Erro", "Filme inválido!", parent=janela)
            return  # Se o filme for inválido, a função é encerrada

        # Verifica se a sala selecionada é válida
        # sl not in salas_by_name: Verifica se a sala selecionada
        #       não está na lista de salas disponíveis
        if sl not in salas_by_name:

            # Exibe uma mensagem de erro informando que a sala selecionada é inválida
            messagebox.showerror("Erro", "Sala inválida!", parent=janela)

            # Se a sala for inválida, a função é encerrada
            return

        # Tenta converter o valor do ingresso para um número (float)
        # Se não for possível converter (por exemplo, se o valor não
        #       for um número válido), exibe um erro
        try:

            # Tenta converter o valor para número
            valor = float(valor_str)

        except ValueError:

            # messagebox.showerror(): Exibe uma caixa de erro
            # "Erro": Título da janela de erro
            # "Valor ingresso deve ser número!": Mensagem de erro
            # parent=janela: Define a janela principal como a janela de erro
            messagebox.showerror("Erro",
                                 "Valor ingresso deve ser número!", parent=janela)

            # Se o valor não for um número, a função é encerrada
            return

        # Atualiza a sessão no banco de dados
        # Chama a função atualizar_sessao para atualizar a sessão com os novos dados
        # Passa os parâmetros necessários: banco de dados, ID da
        #       sessão, filme, sala, data, hora e valor do ingresso
        atualizar_sessao(db,
                         sessao_id_edicao[0],
                         filmes_by_title[f],
                         salas_by_name[sl],
                         data_str,
                         hora_str,
                         valor)

        # Exibe uma mensagem informando que a sessão foi atualizada com sucesso
        # messagebox.showinfo() é usado para exibir uma janela
        #       com a mensagem "Sessão atualizada!"
        messagebox.showinfo("Sucesso",
                            "Sessão atualizada!", parent=janela)

        # Recarrega a lista de sessões na interface
        # A função carregar_sessoes é chamada para atualizar a
        #       exibição da lista de sessões
        carregar_sessoes()

        # Limpa os campos de entrada
        # Deixa os campos de seleção (filme e sala) vazios
        combo_filme.set("")  # Limpa o campo de seleção de filmes
        combo_sala.set("")  # Limpa o campo de seleção de salas

        # Limpa os campos de texto (data, hora e valor)
        entrada_data.delete(0, tk.END)  # Limpa o campo de entrada de data
        entrada_hora.delete(0, tk.END)  # Limpa o campo de entrada de hora
        entrada_valor.delete(0, tk.END)  # Limpa o campo de entrada de valor

        # Reseta o ID da sessão em edição
        # Limpa o identificador da sessão em edição, permitindo
        #       que um novo item seja editado no futuro
        sessao_id_edicao[0] = None


    # Função responsável por deletar uma sessão de cinema
    #       selecionada na interface gráfica.
    def deletar_item():

        # Primeiro, acessa a Treeview para identificar qual sessão
        #       está selecionada atualmente pelo usuário.
        sel = tree.selection()

        # Verifica se alguma sessão foi realmente selecionada
        #       antes de tentar deletar.
        if not sel:

            # Caso nenhuma sessão tenha sido selecionada, informa ao
            #       usuário que é necessário selecionar uma sessão antes de deletar.
            messagebox.showerror("Erro",
                                 "Selecione uma sessão!", parent=janela)

            # Finaliza a execução da função aqui, pois não há
            #       sessão selecionada para deletar.
            return

        # Se houve uma seleção, extrai os detalhes dessa seleção
        #       para obter informações adicionais.
        item = tree.item(sel)

        # Extrai o ID da sessão, que é o primeiro valor armazenado nas
        #       informações do item selecionado.
        sid = item["values"][0]

        # Solicita uma confirmação do usuário para garantir que ele
        #       realmente deseja proceder com a exclusão.
        resp = messagebox.askyesno("Confirmar",
                                   "Deseja deletar a sessão?", parent=janela)

        # Processa a resposta do usuário à solicitação de confirmação.
        if resp:

            # Se o usuário confirmar que deseja deletar a sessão, a função abaixo é
            #       chamada para remover a sessão do banco de dados.
            deletar_sessao(db, sid)

            # Após a exclusão bem-sucedida da sessão, a lista de sessões é
            #       atualizada para refletir a mudança.
            # Isso é feito recarregando os dados das sessões do banco de
            #       dados e atualizando a Treeview.
            carregar_sessoes()


    # Associa o evento de seleção na Treeview (quando um item é
    #       selecionado) com a função 'on_tree_select'.
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # ttk.Button: Widget do Tkinter usado para criar um botão
    # frame_campos: Define que o botão será filho do frame_campos
    # text="Cadastrar Novo": Define o texto do botão como "Cadastrar Novo"
    # command=cadastrar_novo: Especifica que a função 'cadastrar_novo'
    #       será chamada ao clicar no botão
    # grid: Posiciona o botão no layout de grid
    # row=3, column=0: Define a posição do botão na linha 3, coluna 0
    # padx=5, pady=5: Adiciona um espaçamento interno horizontal e vertical de 5 pixels
    ttk.Button(frame_campos,
               text="Cadastrar Novo",
               command=cadastrar_novo).grid(row=3, column=0, padx=5, pady=5)

    # ttk.Button: Widget do Tkinter usado para criar um botão
    # text="Salvar Alterações": Define o texto do botão como "Salvar Alterações"
    # command=salvar_alteracoes: Especifica que a função 'salvar_alteracoes'
    #       será chamada ao clicar no botão
    # grid: Posiciona o botão no layout de grid
    # row=3, column=2: Define a posição do botão na linha 3, coluna 2
    ttk.Button(frame_campos,
               text="Salvar Alterações",
               command=salvar_alteracoes).grid(row=3, column=2, padx=5, pady=5)

    # ttk.Button: Widget do Tkinter usado para criar um botão
    # text="Deletar": Define o texto do botão como "Deletar"
    # command=deletar_item: Especifica que a função 'deletar_item'
    #       será chamada ao clicar no botão
    # grid: Posiciona o botão no layout de grid
    # row=3, column=3: Define a posição do botão na linha 3, coluna 3
    ttk.Button(frame_campos,
               text="Deletar",
               command=deletar_item).grid(row=3, column=3, padx=5, pady=5)

    # carregar_sessoes: Função que carrega as sessões do
    #       banco de dados e as exibe na interface
    carregar_sessoes()


# Função para gerar uma lista de identificadores para assentos de cinema.
def gerar_identificadores_assentos(fileiras, assentos_por_fileira):

    # Inicializa uma lista vazia para armazenar os
    #       identificadores dos assentos.
    assentos = []

    # Loop que percorre cada fileira. O índice 'i' representa o número da
    #       fileira, começando de 0 até o número de fileiras - 1.
    for i in range(fileiras):

        # Gera a letra correspondente à fileira atual. 'A' é a primeira
        #       letra para a primeira fileira, 'B' para a segunda, etc.
        # chr(ord('A') + i) converte 'A' em seu código ASCII e adiciona 'i'
        #       para obter o código ASCII da letra correspondente,
        #       e então converte de volta para o caractere.
        linha_letra = chr(ord('A') + i)

        # Loop interno que percorre os assentos em uma única fileira. 'j'
        #       começa em 1 e vai até o número de assentos por fileira.
        for j in range(1, assentos_por_fileira + 1):

            # Cria o identificador do assento combinando a letra da fileira
            #       com o número do assento e adiciona à lista de assentos.
            # Por exemplo, 'A1', 'A2', ..., 'A{n}', onde 'n' é o número de assentos na fileira.
            assentos.append(linha_letra + str(j))

    # Retorna a lista completa de identificadores de assentos após
    #       preencher todas as fileiras e todos os assentos em cada fileira.
    return assentos


# Função para obter um conjunto de assentos já ocupados em
#       uma sessão específica.
def obter_assentos_ocupados(db, sessao_id):

    # Consulta ao banco de dados para encontrar todas as reservas
    #       para a sessão específica.
    # ObjectId(sessao_id) é usado para converter o ID da sessão de
    #       string para ObjectId, conforme usado no MongoDB.
    reservas = db.reservas.find({"sessao_id": ObjectId(sessao_id)})

    # Inicializa um conjunto para armazenar os identificadores dos assentos ocupados.
    # Conjuntos são usados porque eles automaticamente evitam duplicatas e
    #       oferecem operações eficientes de verificação e inserção.
    assentos_ocupados = set()

    # Itera sobre cada objeto de reserva retornado pela consulta.
    for reserva in reservas:

        # Itera sobre cada assento reservado listado no documento da reserva.
        for a in reserva["assentos_reservados"]:

            # Adiciona cada assento ao conjunto de assentos ocupados.
            # Se o assento já estiver no conjunto, o Python automaticamente
            #       cuida para não adicionar duplicatas.
            assentos_ocupados.add(a)

    # Retorna o conjunto de assentos ocupados. Isso pode ser
    #       usado para verificar rapidamente se um assento está livre ou não.
    return assentos_ocupados


# Função para atualizar os detalhes de uma reserva específica na coleção 'reservas'.
def atualizar_reserva(db, reserva_id, sessao_id, assentos, nome_cliente, telefone_cliente):

    # db.reservas.update_one() é usada para atualizar um documento
    #       específico na coleção 'reservas'.
    # O primeiro parâmetro especifica o documento a ser atualizado,
    #       usando o '_id' da reserva convertido para ObjectId.
    # O segundo parâmetro, '$set', é um operador do MongoDB que especifica os
    #       campos do documento que devem ser atualizados com os novos valores fornecidos.
    db.reservas.update_one({"_id": ObjectId(reserva_id)}, {"$set": {

        # Atualiza o ID da sessão, convertendo o novo ID de string para ObjectId.
        "sessao_id": ObjectId(sessao_id),
        "assentos_reservados": assentos,  # Atualiza a lista de assentos reservados.
        "cliente": {  # Atualiza as informações do cliente.
            "nome": nome_cliente,  # Nome do cliente.
            "telefone": telefone_cliente  # Telefone do cliente.

        }
    }})


# Função para reservar assentos para uma sessão de cinema específica.
def reservar_assentos(db, sessao_id, assentos, nome_cliente, telefone_cliente):

    # Primeiramente, recuperamos todas as reservas já existentes para a sessão especificada.
    # A função ObjectId é usada para converter o sessao_id de string para ObjectId,
    #       que é o formato necessário para consultas no MongoDB.
    reservas_existentes = list(db.reservas.find({"sessao_id": ObjectId(sessao_id)}))

    # Lista para armazenar os assentos já reservados.
    assentos_ja_reservados = []

    # Iteramos sobre cada reserva encontrada para verificar se algum dos
    #       assentos que se deseja reservar já está ocupado.
    for reserva in reservas_existentes:

        # Iteramos sobre os assentos reservados em cada reserva existente.
        for a in reserva["assentos_reservados"]:

            # Se um assento já estiver reservado, ele é adicionado à
            #       lista de assentos já reservados.
            if a in assentos:
                assentos_ja_reservados.append(a)

    # Verifica se há assentos já reservados na lista.
    if assentos_ja_reservados:

        # Se houver assentos já reservados, uma exceção é levantada.
        # A exceção interrompe a execução da função e retorna uma mensagem de
        #       erro listando os assentos indisponíveis.
        # O método join() é usado para converter a lista de assentos em
        #       uma string separada por vírgulas.
        raise ValueError("Os seguintes assentos já estão reservados: " + ", ".join(assentos_ja_reservados))

    # Verifica se não há conflitos de assentos reservados.
    if not assentos_ja_reservados:

        # Se não houver conflitos, o sistema procede com a inserção da
        #       reserva no banco de dados.
        # db.reservas.insert_one() insere um novo documento na coleção 'reservas'.
        # O documento é um dicionário que contém os dados da reserva, incluindo:
        result = db.reservas.insert_one({

            # O ID da sessão, convertido para ObjectId, que é o formato usado
            #       pelo MongoDB para identificadores únicos.
            "sessao_id": ObjectId(sessao_id),
            "assentos_reservados": assentos,  # A lista de assentos que o cliente deseja reservar.
            "cliente": {  # Um dicionário contendo informações sobre o cliente que faz a reserva.
                "nome": nome_cliente,  # O nome do cliente.
                "telefone": telefone_cliente  # O telefone do cliente.
            }
        })

        # O resultado da inserção (incluindo o ID do documento inserido) é
        #       armazenado na variável 'result'.
        # Este ID pode ser usado para referência futura ou confirmação da reserva.

    # O método insert_one retorna um resultado que inclui o ID
    #       da nova reserva inserida.
    # Retornamos esse ID para confirmar que a reserva foi realizada com sucesso.
    return result.inserted_id


# Importa a biblioteca FPDF para geração de arquivos PDF
from fpdf import FPDF

# Importa a biblioteca threading para execução de processos em segundo plano
import threading

# Definição da função principal que gera o ingresso
def gerar_ingresso(nome_cliente, telefone_cliente, filme, sessao, assentos):

    """
    Gera um arquivo PDF representando um ingresso de cinema com as informações fornecidas.

    :param nome_cliente: Nome do cliente que comprou o ingresso.
    :param telefone_cliente: Telefone de contato do cliente.
    :param filme: Nome do filme que será assistido.
    :param sessao: Sessão do filme (data, hora e sala).
    :param assentos: Lista dos assentos reservados para o cliente.
    """

    # Definição da função interna que será responsável por gerar o arquivo PDF
    def gerar_pdf():

        """
        Gera e salva um arquivo PDF contendo as informações do ingresso.
        Essa função é executada dentro de uma thread separada para não travar a interface do usuário.
        """

        try:

            # Define o nome do arquivo PDF baseado no nome do cliente.
            # Substitui espaços no nome por "_" para evitar problemas com nomes de arquivos.
            nome_arquivo = f"Ingresso_{nome_cliente.replace(' ', '_')}.pdf"

            # Criação do objeto PDF
            # -----------------------------------
            # Aqui estamos criando um novo objeto da classe FPDF, que representa um documento PDF.
            # Essa classe é fornecida pela biblioteca FPDF, utilizada para criar documentos PDF a partir do Python.
            # O objeto "pdf" servirá como um manipulador do documento, permitindo
            #       adicionar páginas, definir fontes e inserir texto.
            pdf = FPDF()

            # Adiciona uma nova página ao documento PDF
            # -----------------------------------
            # O método "add_page()" adiciona uma nova página em branco ao documento.
            # Como os PDFs podem ter múltiplas páginas, este método é necessário sempre
            #       que formos criar um novo documento.
            # Por padrão, as páginas são adicionadas no formato "A4" (210x297mm).
            pdf.add_page()

            # Define a fonte que será usada para escrever no PDF
            # -----------------------------------
            # O método "set_font()" permite escolher a fonte do texto dentro do PDF.
            # Parâmetros:
            # - "Arial": Nome da fonte a ser utilizada.
            # - "size=12": Define o tamanho da fonte em pontos (pt). O tamanho 12 é padrão para textos legíveis.
            # Algumas opções de fontes disponíveis na FPDF: "Arial", "Courier", "Times", "Symbol", "ZapfDingbats".
            pdf.set_font("Arial", size=12)

            # Adiciona um título ao ingresso no PDF
            # -----------------------------------
            # O método "cell()" cria uma célula no PDF, que pode conter texto.
            # Parâmetros:
            # - "200": Define a largura da célula. Como a largura do A4 tem cerca de 210mm,
            #       usamos 200mm para cobrir quase toda a largura da página.
            # - "10": Define a altura da célula, geralmente usada para espaçamento vertical do texto.
            # - "txt='CINEMA - INGRESSO'": Define o texto que será inserido dentro da célula.
            # - "ln=True": Move o cursor para a próxima linha automaticamente após inserir o texto.
            # - "align='C'": Centraliza o texto horizontalmente dentro da célula (C = Center).
            pdf.cell(200, 10, txt="CINEMA - INGRESSO", ln=True, align="C")

            # Adiciona um espaçamento vertical antes das próximas informações
            # -----------------------------------
            # O método "ln(10)" adiciona uma nova linha com espaçamento de 10mm.
            # Isso cria um espaço entre o título e as próximas informações do ingresso.
            pdf.ln(10)

            # Adiciona os detalhes do cliente no ingresso
            # -----------------------------------
            # O método "cell()" é utilizado para inserir cada informação de forma separada.
            # Como o parâmetro "ln=True" está ativado, cada chamada do "cell()" cria uma nova linha automaticamente.
            pdf.cell(0, 10, txt=f"Cliente: {nome_cliente}", ln=True)  # Nome do cliente
            pdf.cell(0, 10, txt=f"Telefone: {telefone_cliente}", ln=True)  # Telefone do cliente

            # Adiciona os detalhes do filme e sessão no ingresso
            # -----------------------------------
            # O parâmetro "0" na largura significa que a célula ocupará toda a largura disponível.
            # O "ln=True" força o texto a ir para uma nova linha, organizando os dados verticalmente.
            pdf.cell(0, 10, txt=f"Filme: {filme}", ln=True)  # Nome do filme
            pdf.cell(0, 10, txt=f"Sessão: {sessao}", ln=True)  # Data, horário e sala do filme

            # Adiciona os assentos reservados
            # -----------------------------------
            # O método "join()" é usado para converter a lista de assentos em uma string separada por vírgulas.
            # Exemplo: Se "assentos" for ["A1", "A2", "B5"], ele será transformado em "A1, A2, B5".
            pdf.cell(0, 10, txt=f"Assentos: {', '.join(assentos)}", ln=True)

            # Adiciona um espaçamento extra antes das informações finais
            # -----------------------------------
            # O "ln(10)" adiciona um espaço de 10mm antes de inserir a mensagem final.
            pdf.ln(10)

            # Adiciona uma linha divisória no PDF para separar as informações
            # ---------------------------------------------------------------
            # O método "cell()" cria uma célula que ocupa toda a largura disponível no documento PDF.
            # Como não foi especificada uma largura fixa (0), a linha se estende até o final da página.
            # O texto "----------------------------------------" é apenas uma forma visual de
            #       criar um divisor dentro do PDF.
            # O parâmetro "ln=True" indica que, após esta célula, o cursor deve ir para a próxima linha.
            pdf.cell(0, 10, txt="----------------------------------------", ln=True)

            # Adiciona uma mensagem de instrução ao cliente
            # ---------------------------------------------------------------
            # Aqui, estamos adicionando uma mensagem importante no ingresso, informando que o cliente
            #       deve apresentar o ingresso na entrada do cinema.
            # O método "cell()" novamente cria uma célula que ocupa toda a largura do documento (0).
            # O texto "Apresente este ingresso na entrada do cinema." serve como uma instrução clara para o usuário.
            # O parâmetro "ln=True" força uma nova linha após essa célula, garantindo que a
            #       estrutura do documento fique organizada.
            pdf.cell(0, 10, txt="Apresente este ingresso na entrada do cinema.", ln=True)

            # Salvar o arquivo PDF gerado
            # ---------------------------------------------------------------
            # O método "output()" da classe FPDF é responsável por gerar e salvar o
            #       arquivo PDF no diretório atual.
            # O nome do arquivo é definido previamente na variável "nome_arquivo".
            # Se "nome_arquivo" for "Ingresso_Joao_Silva.pdf", o PDF será salvo como esse nome.
            pdf.output(nome_arquivo)

            # Abrir automaticamente o PDF gerado sem travar a interface gráfica
            # ---------------------------------------------------------------
            # O método "os.startfile()" abre um arquivo usando o programa padrão do sistema operacional.
            # No Windows, isso significa que o PDF será aberto automaticamente no
            #       leitor de PDF padrão (como Adobe Reader ou Edge).
            # Como essa operação pode ser bloqueante e causar travamento da interface
            #       gráfica, ela é executada dentro de uma **thread separada**.
            # A biblioteca "threading" permite executar processos em segundo plano, garantindo
            #       que a aplicação continue responsiva.
            # - "target=os.startfile" -> Define que a função "os.startfile()" será executada dentro da thread.
            # - "args=(nome_arquivo,)" -> Passa o nome do arquivo como argumento para "os.startfile()".
            # - "daemon=True" -> Define a thread como daemon, garantindo que ela será encerrada
            #       automaticamente quando o programa principal terminar.
            threading.Thread(target=os.startfile, args=(nome_arquivo,), daemon=True).start()


        # Captura e trata possíveis erros durante a geração do PDF
        # ---------------------------------------------------------------
        # A instrução "try" tenta executar o código dentro do bloco sem erros.
        # Se ocorrer um erro (exceção), o bloco "except" é ativado para capturar o erro.
        # O "Exception as e" captura qualquer tipo de erro e armazena a mensagem do erro na variável "e".
        except Exception as e:

            # Exibe uma mensagem de erro para o usuário caso ocorra uma falha na geração do PDF
            # ---------------------------------------------------------------
            # "messagebox.showerror()" é um método da biblioteca Tkinter utilizado para exibir
            #       mensagens de erro em uma janela pop-up.
            # Parâmetros:
            # - "Erro": Define o título da caixa de diálogo.
            # - f"Erro ao gerar PDF: {str(e)}" -> Exibe a mensagem de erro retornada
            #       pela exceção, convertida em string.
            # Isso permite que o usuário entenda o que deu errado e possa corrigir o problema.
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")


    # Criamos uma thread separada para evitar que a interface gráfica trave
    # ---------------------------------------------------------------
    # Quando um código executa uma operação demorada, como salvar um arquivo PDF,
    # ele pode bloquear a interface gráfica do usuário (GUI), impedindo interações.
    # Para evitar esse problema, utilizamos a biblioteca "threading" para executar
    #       essa operação em segundo plano.
    #
    # A função "threading.Thread()" cria uma nova thread (processo paralelo).
    # Parâmetros:
    # - "target=gerar_pdf" -> Define a função que será executada na thread (neste caso, a geração do PDF).
    # - "daemon=True" -> Define a thread como daemon, garantindo que ela seja
    #       encerrada automaticamente quando o programa principal for fechado.
    #
    # Em seguida, chamamos "start()" para iniciar a execução da thread.
    threading.Thread(target=gerar_pdf, daemon=True).start()


# ============================================================
# TELA RESERVAR ASSENTOS COM MAPA
# ============================================================

def tela_reserva_assentos(root, db):

    # janela: Cria uma nova janela secundária para a reserva de assentos.
    # criar_janela_secundaria: Função que configura uma nova janela a
    #       partir da janela principal (root).
    janela = criar_janela_secundaria(root, "Reservar Assentos")

    # Determinar as dimensões da janela e centralizá-la
    # largura_janela: Define a largura da janela como 600 pixels.
    largura_janela = 600

    # altura_janela: Define a altura da janela como 500 pixels.
    altura_janela = 500

    # largura_tela: Obtém a largura total da tela do sistema.
    largura_tela = root.winfo_screenwidth()

    # altura_tela: Obtém a altura total da tela do sistema.
    altura_tela = root.winfo_screenheight()

    # Cálculo para centralizar a janela na tela
    # pos_x: Calcula a posição horizontal inicial da janela para centralizá-la.
    pos_x = (largura_tela - largura_janela) // 2

    # pos_y: Calcula a posição vertical inicial da janela para centralizá-la.
    pos_y = (altura_tela - altura_janela) // 2

    # janela.geometry: Configura o tamanho e a posição da janela no
    #       formato largura x altura + pos_x + pos_y.
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # frame: Cria um frame para organizar os widgets da janela.
    # ttk.Frame: Widget do Tkinter para criar um contêiner para outros elementos.
    # janela: Define a janela criada anteriormente como pai do frame.
    # padding="10 10 10 10": Adiciona espaçamento interno (padding) ao
    #       redor do frame em todos os lados.
    frame = ttk.Frame(janela, padding="10 10 10 10")

    # frame.pack: Posiciona o frame para preencher o espaço disponível na janela.
    # fill='both': Faz com que o frame expanda tanto na largura quanto na altura.
    # expand=True: Permite que o frame se expanda para ocupar o espaço disponível na janela.
    frame.pack(fill='both', expand=True)

    # Primeiro, o usuário escolhe o filme
    # filmes: Obtém a lista de filmes do banco de dados.
    # list(obter_filmes(db)): Converte o resultado da função obter_filmes em
    #       uma lista de dicionários contendo os filmes.
    filmes = list(obter_filmes(db))

    # ttk.Label: Cria um rótulo para guiar o usuário na seleção do filme.
    # frame: Define que o rótulo será filho do frame criado anteriormente.
    # text="Selecione o Filme:": Define o texto exibido no rótulo como "Selecione o Filme:".
    # grid: Posiciona o rótulo no layout de grade.
    # row=0, column=0: Define a posição do rótulo na linha 0, coluna 0.
    # sticky='e': Alinha o rótulo à direita (east) dentro da célula do grid.
    # padx=5, pady=5: Adiciona espaçamento horizontal e vertical de 5 pixels ao redor do rótulo.
    ttk.Label(frame,
              text="Selecione o Filme:").grid(row=0, column=0, sticky='e', padx=5, pady=5)

    # combo_filmes: Cria um combobox para o usuário selecionar um filme.
    # ttk.Combobox: Widget do Tkinter para criar uma caixa de seleção com opções.
    # frame: Define que o combobox será filho do frame criado anteriormente.
    # values=[f["titulo"] for f in filmes]: Define as opções do combobox com os
    #       títulos dos filmes extraídos da lista de filmes.
    # width=30: Define a largura do combobox como 30 caracteres.
    combo_filmes = ttk.Combobox(frame,
                                values=[f["titulo"] for f in filmes], width=30)

    # grid: Posiciona o combobox no layout de grade.
    # row=0, column=1: Define a posição do combobox na linha 0, coluna 1.
    # padx=5, pady=5: Adiciona espaçamento horizontal e vertical
    #       de 5 pixels ao redor do combobox.
    combo_filmes.grid(row=0, column=1, padx=5, pady=5)

    # Depois, após selecionar o filme, carregamos as sessões desse filme.

    # ttk.Label: Cria um rótulo para guiar o usuário na seleção da sessão.
    # frame: Define que o rótulo será filho do frame criado anteriormente.
    # text="Selecione a Sessão:": Define o texto exibido no
    #       rótulo como "Selecione a Sessão:".
    # grid: Posiciona o rótulo no layout de grade.
    # row=1, column=0: Define a posição do rótulo na linha 1, coluna 0.
    # sticky='e': Alinha o rótulo à direita (east) dentro da célula do grid.
    # padx=5, pady=5: Adiciona espaçamento horizontal e vertical de 5 pixels ao redor do rótulo.
    ttk.Label(frame,
              text="Selecione a Sessão:").grid(row=1, column=0, sticky='e', padx=5, pady=5)

    # combo_sessoes: Cria um combobox para o usuário selecionar uma sessão.
    # ttk.Combobox: Widget do Tkinter para criar uma caixa de seleção com opções.
    # frame: Define que o combobox será filho do frame criado anteriormente.
    # width=50: Define a largura do combobox como 50 caracteres,
    #       proporcionando espaço para descrever a sessão.
    combo_sessoes = ttk.Combobox(frame, width=50)

    # grid: Posiciona o combobox no layout de grade.
    # row=1, column=1: Define a posição do combobox na linha 1, coluna 1.
    # padx=5, pady=5: Adiciona espaçamento horizontal e vertical
    #       de 5 pixels ao redor do combobox.
    combo_sessoes.grid(row=1, column=1, padx=5, pady=5)

    # frame_mapa: Cria um frame para exibir o mapa de assentos.
    # ttk.Frame: Widget do Tkinter para criar um contêiner para outros elementos.
    # frame: Define que o frame será filho do frame principal.
    frame_mapa = ttk.Frame(frame)

    # grid: Posiciona o frame no layout de grade.
    # row=3, column=0: Define a posição do frame na linha 3, começando na coluna 0.
    # columnspan=2: Faz o frame ocupar duas colunas, centralizando o mapa de assentos.
    # pady=10: Adiciona espaçamento vertical de 10 pixels acima e abaixo do frame.
    frame_mapa.grid(row=3, column=0, columnspan=2, pady=10)

    # selected_assentos: Cria um conjunto para armazenar os
    #       assentos selecionados pelo usuário.
    # set(): Um conjunto vazio para gerenciar os assentos
    #       selecionados sem duplicatas.
    selected_assentos = set()


    def atualizar_sessoes():

        """Atualiza o combobox de sessões com base no filme selecionado."""

        # Limpa a seleção atual do combobox de sessões.
        # combo_sessoes.set(''): Remove qualquer valor atualmente
        #       exibido no combobox de sessões.
        combo_sessoes.set('')

        # Obtém o título do filme atualmente selecionado no combobox de filmes.
        # combo_filmes.get(): Retorna o texto atualmente selecionado no combobox de filmes.
        filme_selecionado = combo_filmes.get()

        # Verifica se nenhum filme foi selecionado.
        # Se o filme_selecionado estiver vazio, a função retorna imediatamente.
        if not filme_selecionado:
            return

        # Busca o documento do filme correspondente ao título selecionado.
        # next((f for f in filmes if f["titulo"] == filme_selecionado), None):
        # Encontra o primeiro filme na lista 'filmes' cujo título
        #       corresponde ao filme selecionado.
        # Caso nenhum filme seja encontrado, retorna 'None'.
        filme_doc = next((f for f in filmes if f["titulo"] == filme_selecionado), None)

        # Verifica se o filme não foi encontrado no banco de dados.
        # Caso não seja encontrado, a função retorna imediatamente.
        if not filme_doc:
            return

        # Obtém todas as sessões associadas ao filme selecionado.
        # obter_sessoes_por_filme(db, filme_doc["_id"]): Retorna as
        #       sessões para o filme cujo ID é fornecido.
        sessoes_filme = list(obter_sessoes_por_filme(db, filme_doc["_id"]))

        # Lista para armazenar as informações das sessões formatadas.
        valores = []

        # Itera sobre cada sessão associada ao filme selecionado.
        for s in sessoes_filme:

            # Obtém os detalhes da sala correspondente à sessão.
            # obter_sala_por_id(db, s["sala_id"]): Retorna o documento da
            #       sala com base no ID fornecido.
            sala_doc = obter_sala_por_id(db, s["sala_id"])

            # Formata o texto da sessão com data, hora e nome da sala.
            texto_sessao = f"{s['data']} {s['hora']} - {sala_doc['nome']}"

            # Adiciona o ID da sessão e o texto formatado à lista de valores.
            valores.append((str(s["_id"]), texto_sessao))

        # Atualiza o combobox de sessões com os novos valores.
        # combo_sessoes.values_map: Armazena o mapeamento entre
        #       IDs de sessão e texto de exibição.
        combo_sessoes.values_map = valores

        # combo_sessoes["values"]: Define as opções exibidas no combobox
        #       de sessões como os textos formatados.
        combo_sessoes["values"] = [v[1] for v in valores]



    def abrir_caixa_reserva(sessao_id, assento):

        """Exibe uma janela com informações detalhadas da reserva e
                permite alterações ou exclusões."""

        # Busca a reserva no banco de dados com base no ID da sessão e
        #       no assento específico.
        # db.reservas.find_one: Retorna o primeiro documento correspondente à
        #       consulta ou None se não houver correspondência.
        # {"sessao_id": ObjectId(sessao_id), "assentos_reservados": assento}: Filtro
        #       que combina a sessão e o assento específico.
        reserva = db.reservas.find_one({"sessao_id": ObjectId(sessao_id), "assentos_reservados": assento})

        # Verifica se a reserva não foi encontrada.
        # Se não houver reserva correspondente, a função retorna imediatamente.
        if not reserva:
            return

        # Cria uma nova janela secundária para exibir os detalhes da reserva.
        # criar_janela_secundaria: Função personalizada para criar uma janela modal.
        # "Detalhes da Reserva": Define o título da nova janela.
        janela_reserva = criar_janela_secundaria(janela, "Detalhes da Reserva")

        # Dimensões da tela
        largura_tela = janela_reserva.winfo_screenwidth()
        altura_tela = janela_reserva.winfo_screenheight()

        #Definir dimensões da janela
        largura_janela = 400
        altura_janela = 250

        # Calcular posição centralizada
        x_posicao = (largura_tela // 2) - (largura_janela // 2)
        y_posicao = (altura_tela // 2) - (altura_janela // 2)

        # Aplicar tamanho e posição
        janela_reserva.geometry(f"{largura_janela}x{altura_janela}+{x_posicao}+{y_posicao}")


        # Exibe um rótulo para o campo do nome do cliente.
        # ttk.Label: Cria um widget de rótulo no Tkinter.
        # text="Nome do Cliente:": Define o texto exibido no rótulo.
        # grid(row=0, column=0, padx=5, pady=5, sticky="e"): Posiciona o rótulo
        #       na célula (0,0) com espaçamento e alinhamento à direita.
        ttk.Label(janela_reserva,
                  text="Nome do Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para o nome do cliente.
        # ttk.Entry: Widget para entrada de texto no Tkinter.
        # width=30: Define a largura do campo de entrada como 30 caracteres.
        entrada_nome = ttk.Entry(janela_reserva, width=30)

        # Posiciona o campo de entrada na janela.
        # grid(row=0, column=1, padx=5, pady=5): Posiciona o
        #       campo na célula (0,1) com espaçamento.
        entrada_nome.grid(row=0, column=1, padx=5, pady=5)

        # Preenche o campo de entrada com o nome do cliente da reserva.
        # insert(0, reserva["cliente"]["nome"]): Insere o nome do
        #       cliente no início do campo de entrada.
        entrada_nome.insert(0, reserva["cliente"]["nome"])

        # Exibe um rótulo para o campo do telefone do cliente.
        # ttk.Label: Este é um widget da biblioteca ttk, usado para criar um
        #       rótulo de texto que pode ser exibido em uma interface gráfica.
        # frame_pai=janela_reserva: Indica que o rótulo será exibido dentro da
        #       janela 'janela_reserva', que é o pai deste widget.
        # text="Telefone do Cliente:": Define o texto que será exibido no rótulo,
        #       que neste caso é "Telefone do Cliente:", indicando ao usuário o
        #       propósito do campo associado.
        # grid(row=1, column=0): Posiciona o rótulo na célula (linha 1, coluna 0)
        #       de um layout do tipo grid.
        # padx=5, pady=5: Adiciona um espaçamento interno (padding) de 5 pixels ao
        #       redor do rótulo, tanto horizontal quanto verticalmente, para evitar
        #       que ele fique colado em outros elementos.
        # sticky="e": Alinha o rótulo à direita (east) dentro da célula do
        #       layout grid, garantindo que ele se posicione próximo ao campo associado.
        ttk.Label(janela_reserva,
                  text="Telefone do Cliente:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para o telefone do cliente.
        # ttk.Entry: Este é um widget da biblioteca ttk usado para criar
        #       campos onde o usuário pode digitar texto.
        # frame_pai=janela_reserva: Indica que o campo de entrada será exibido
        #       dentro da janela 'janela_reserva', que é o pai deste widget.
        # width=20: Define a largura do campo de entrada em 20 caracteres, permitindo
        #       que o texto digitado se ajuste de forma visível nesse espaço.
        entrada_telefone = ttk.Entry(janela_reserva, width=20)

        # Posiciona o campo de entrada na janela.
        # grid(row=1, column=1): Posiciona o campo na célula (linha 1, coluna 1)
        #       de um layout do tipo grid.
        # padx=5, pady=5: Adiciona um espaçamento interno de 5 pixels ao
        #       redor do campo de entrada, tanto horizontal quanto verticalmente,
        #       para manter uma boa separação visual entre os elementos.
        entrada_telefone.grid(row=1, column=1, padx=5, pady=5)

        # Preenche o campo de entrada com o telefone do cliente da reserva.
        # insert(index, texto): É um método usado para inserir texto em um
        #       campo de entrada. Aqui, '0' significa que o texto será
        #       inserido no início do campo.
        # reserva["cliente"]["telefone"]: Obtém o telefone do cliente da
        #       reserva selecionada no banco de dados e o insere como texto
        #       inicial no campo de entrada.
        entrada_telefone.insert(0, reserva["cliente"]["telefone"])

        # Exibe um rótulo para identificar o campo de assento na interface.
        # ttk.Label: Widget da biblioteca ttk usado para exibir texto
        #       fixo na interface gráfica.
        # frame_pai=janela_reserva: Define que o rótulo será exibido dentro da
        #       janela 'janela_reserva', que é o pai do widget.
        # text="Assento:": Define o texto exibido no rótulo como "Assento:",
        #       indicando ao usuário que o campo relacionado exibe os assentos reservados.
        # grid(row=2, column=0): Posiciona o rótulo na linha 2, coluna 0, no
        #       layout de grade da janela.
        # padx=5, pady=5: Define um espaçamento horizontal (padding x) e
        #       vertical (padding y) de 5 pixels ao redor do rótulo.
        # sticky="e": Alinha o rótulo à direita (east) dentro da célula onde
        #       ele está posicionado, ajustando sua posição para um alinhamento
        #       mais natural com o conteúdo ao lado.
        ttk.Label(janela_reserva,
                  text="Assento:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Exibe o(s) assento(s) reservado(s) na interface.
        # ttk.Label: Widget da biblioteca ttk usado para exibir texto fixo na interface gráfica.
        # frame_pai=janela_reserva: Define que o rótulo será exibido dentro da
        #       janela 'janela_reserva', que é o pai do widget.
        # text=", ".join(reserva["assentos_reservados"]): Junta os assentos
        #       reservados em uma única string, separados por vírgulas, para exibição.
        #   reserva["assentos_reservados"]: Obtém a lista de assentos
        #       reservados para a reserva em questão.
        label_assento = ttk.Label(janela_reserva,
                                  text=", ".join(reserva["assentos_reservados"]))

        # Posiciona o rótulo de assentos na interface.
        # grid(row=2, column=1): Posiciona o rótulo na linha 2, coluna 1, ao
        #       lado do rótulo "Assento:".
        # padx=5, pady=5: Define um espaçamento horizontal e vertical
        #       de 5 pixels ao redor do rótulo.
        label_assento.grid(row=2, column=1, padx=5, pady=5)


        # Define a função para deletar uma reserva.
        # deletar_reserva(): Função que solicita a confirmação do usuário e, se
        #       confirmada, exclui a reserva do banco de dados.
        def deletar_reserva():

            # Solicita a confirmação do usuário antes de excluir a reserva.
            # messagebox.askyesno(): Exibe uma janela de confirmação com as opções "Sim" e "Não".
            # "Confirmar": Título da janela de confirmação.
            # "Deseja realmente deletar esta reserva?": Mensagem exibida ao usuário.
            # parent=janela_reserva: Define a janela de confirmação como filha da janela atual.
            resposta = messagebox.askyesno("Confirmar",
                                           "Deseja realmente deletar esta reserva?",
                                           parent=janela_reserva)

            # Verifica se o usuário confirmou a exclusão.
            if resposta:

                # Tenta excluir a reserva no banco de dados.
                try:

                    # Exclui a reserva do banco de dados MongoDB.
                    # db.reservas.delete_one(): Função do MongoDB para excluir um único documento.
                    # {"_id": reserva["_id"]}: Filtro para identificar a reserva a
                    #       ser excluída usando o ID da reserva.
                    db.reservas.delete_one({"_id": reserva["_id"]})

                    # Exibe uma mensagem informando que a reserva foi deletada com sucesso.
                    # messagebox.showinfo(): Exibe uma janela informativa com a mensagem de sucesso.
                    # parent=janela_reserva: Define a janela informativa como filha da janela atual.
                    messagebox.showinfo("Sucesso",
                                        "Reserva deletada com sucesso!",
                                        parent=janela_reserva)

                    # Fecha a janela de detalhes da reserva após a exclusão.
                    # destroy(): Fecha a janela 'janela_reserva'.
                    janela_reserva.destroy()

                    # Atualiza o mapa de assentos após a exclusão da reserva.
                    # exibir_mapa(): Função chamada para refletir a
                    #       mudança no mapa de assentos.
                    exibir_mapa()

                # Captura e trata qualquer exceção que possa ocorrer
                #       durante o processo de exclusão.
                except Exception as e:

                    # Exibe uma mensagem de erro caso ocorra uma exceção durante a exclusão.
                    # messagebox.showerror(): Exibe uma janela de erro com a mensagem do erro capturado.
                    # str(e): Converte o objeto da exceção em uma string descritiva.
                    # parent=janela_reserva: Define a janela de erro como filha da janela atual.
                    messagebox.showerror("Erro", str(e), parent=janela_reserva)


        # Define a função para salvar alterações na reserva.
        # salvar_alteracoes(): Função que coleta os dados alterados pelo usuário,
        #       valida as entradas e atualiza a reserva no banco de dados.
        def salvar_alteracoes():

            # Obtém o nome atualizado inserido pelo usuário.
            # entrada_nome.get(): Coleta o valor atual do campo de entrada de nome.
            # strip(): Remove espaços em branco no início e no final do texto.
            novo_nome = entrada_nome.get().strip()

            # Obtém o telefone atualizado inserido pelo usuário.
            # entrada_telefone.get(): Coleta o valor atual do campo de entrada de telefone.
            # strip(): Remove espaços em branco no início e no final do texto.
            novo_telefone = entrada_telefone.get().strip()

            # Valida se os campos obrigatórios foram preenchidos.
            # all([novo_nome, novo_telefone]): Verifica se todos os
            #       valores (nome e telefone) não estão vazios.
            # Se qualquer campo estiver vazio, exibe uma mensagem de erro.
            if not all([novo_nome, novo_telefone]):

                # messagebox.showerror(): Exibe uma janela de erro com a
                #       mensagem "Preencha todos os campos!".
                # parent=janela_reserva: Define a janela de erro como
                #       filha da janela atual.
                messagebox.showerror("Erro",
                                     "Preencha todos os campos!", parent=janela_reserva)

                # Interrompe a execução da função.
                return

            # Tenta atualizar os dados no banco de dados.
            try:

                # Atualiza a reserva no banco de dados.
                # atualizar_reserva(): Função para atualizar uma reserva existente.
                # reserva["_id"]: ID da reserva que será atualizada.
                # sessao_id: ID da sessão relacionado à reserva (não alterado aqui).
                # reserva["assentos_reservados"]: Lista de assentos reservados (não alterado aqui).
                # novo_nome: Nome atualizado do cliente.
                # novo_telefone: Telefone atualizado do cliente.
                atualizar_reserva(db,
                                  reserva["_id"],
                                  sessao_id,
                                  reserva["assentos_reservados"],
                                  novo_nome,
                                  novo_telefone)

                # Exibe uma mensagem de sucesso ao concluir a atualização.
                # messagebox.showinfo(): Exibe uma janela informativa com a
                #       mensagem "Reserva alterada com sucesso!".
                # parent=janela_reserva: Define a janela informativa
                #       como filha da janela atual.
                messagebox.showinfo("Sucesso",
                                    "Reserva alterada com sucesso!",
                                    parent=janela_reserva)

                # Fecha a janela de detalhes da reserva após salvar as alterações.
                # destroy(): Fecha a janela 'janela_reserva'.
                janela_reserva.destroy()

                # Reexibe o mapa de assentos atualizado.
                # exibir_mapa(): Função chamada para atualizar a
                #       exibição do mapa de assentos.
                exibir_mapa()

            # Captura e trata qualquer exceção que possa ocorrer
            #       durante o processo de atualização.
            except Exception as e:

                # Exibe uma mensagem de erro caso ocorra uma exceção.
                # messagebox.showerror(): Exibe uma janela de erro com a mensagem do erro capturado.
                # str(e): Converte o objeto da exceção em uma string descritiva.
                # parent=janela_reserva: Define a janela de erro como filha da janela atual.
                messagebox.showerror("Erro", str(e), parent=janela_reserva)



        # Cria um botão para salvar alterações feitas na reserva.
        # ttk.Button: Cria um botão utilizando a biblioteca ttk do Tkinter.
        # janela_reserva: Define que o botão será filho da janela atual 'janela_reserva'.
        # text="Salvar Alterações": Define o texto exibido no botão como "Salvar Alterações".
        # command=salvar_alteracoes: Associa a função 'salvar_alteracoes' ao
        #       botão, que será executada quando o botão for clicado.
        # grid(row=3, column=0, padx=5, pady=10): Posiciona o botão na célula (3,0) do
        #       layout grid, com espaçamento horizontal de 5 pixels e vertical de 10 pixels.
        ttk.Button(janela_reserva,
                   text="Salvar Alterações",
                   command=salvar_alteracoes).grid(row=3, column=0, padx=5, pady=10)

        # Cria um botão para deletar a reserva atual.
        # ttk.Button: Cria um botão utilizando a biblioteca ttk do Tkinter.
        # janela_reserva: Define que o botão será filho da janela atual 'janela_reserva'.
        # text="Deletar": Define o texto exibido no botão como "Deletar".
        # command=deletar_reserva: Associa a função 'deletar_reserva' ao
        #       botão, que será executada quando o botão for clicado.
        # grid(row=3, column=1, padx=5, pady=10): Posiciona o botão na
        #       célula (3,1) do layout grid, com espaçamento horizontal de 5 pixels e
        #       vertical de 10 pixels.
        ttk.Button(janela_reserva,
                   text="Deletar",
                   command=deletar_reserva).grid(row=3, column=1, padx=5, pady=10)


    # Define a função para exibir o mapa de assentos da sessão selecionada.
    def exibir_mapa():

        # Remove todos os widgets existentes no frame_mapa antes de redesenhar o mapa.
        # frame_mapa.winfo_children(): Retorna uma lista de todos os widgets filhos no frame_mapa.
        # widget.destroy(): Remove o widget da interface gráfica.
        for widget in frame_mapa.winfo_children():
            widget.destroy()

        # Limpa o conjunto de assentos selecionados, preparando-o para a nova seleção.
        # selected_assentos.clear(): Remove todos os itens do
        #       conjunto de assentos selecionados.
        selected_assentos.clear()

        # Obtém o texto da sessão selecionada no combobox.
        # combo_sessoes.get(): Retorna o texto da sessão atualmente selecionada.
        sessao_txt = combo_sessoes.get()

        # Verifica se nenhuma sessão foi selecionada ou se o combobox
        #       não possui mapeamento de valores.
        # hasattr(combo_sessoes, "values_map"): Verifica se o combobox
        #       possui um atributo chamado values_map.
        if not sessao_txt or not hasattr(combo_sessoes, "values_map"):
            return

        # Inicializa a variável sessao_id como None, que será utilizada
        #       para armazenar o ID da sessão selecionada.
        sessao_id = None

        # Itera sobre o mapeamento de valores do combobox de sessões
        #       para encontrar o ID da sessão selecionada.
        # combo_sessoes.values_map: Lista de tuplas contendo os IDs das
        #       sessões e os textos correspondentes.
        # sid: ID da sessão, texto: Descrição da sessão.
        for sid, texto in combo_sessoes.values_map:

            # Compara o texto da sessão selecionada com o texto
            #       armazenado no mapeamento.
            if texto == sessao_txt:

                # Armazena o ID da sessão correspondente na variável sessao_id.
                sessao_id = sid

                # Sai do loop após encontrar o ID correspondente.
                break

        # Verifica se nenhum ID foi encontrado para a sessão selecionada.
        # Isso pode acontecer se a sessão selecionada não estiver no mapeamento.
        if not sessao_id:
            return

        # Obtém os detalhes da sessão utilizando o ID encontrado.
        # obter_sessao_por_id(db, sessao_id): Função que retorna os dados da
        #       sessão a partir do banco de dados.
        sessao = obter_sessao_por_id(db, sessao_id)

        # Obtém os detalhes da sala associada à sessão.
        # obter_sala_por_id(db, sessao["sala_id"]): Retorna os dados da sala
        #       utilizando o ID armazenado na sessão.
        sala = obter_sala_por_id(db, sessao["sala_id"])

        # Gera a lista completa de identificadores de assentos com base
        #       na configuração da sala.
        # sala["fileiras"]: Número de fileiras na sala.
        # sala["assentos_por_fileira"]: Número de assentos em cada fileira.
        # gerar_identificadores_assentos(): Retorna uma lista de identificadores de
        #       assentos (ex.: A1, A2, B1, etc.).
        assentos_totais = gerar_identificadores_assentos(sala["fileiras"], sala["assentos_por_fileira"])

        ###### PAREI AQUI FAZER A FUNCAO gerar_identificadores_assentos e depois as outras duas que faltam...

        # Obtém os assentos que já estão ocupados para a sessão selecionada.
        # obter_assentos_ocupados(db, sessao_id): Retorna um conjunto contendo os
        #       identificadores de assentos ocupados.
        assentos_ocupados = obter_assentos_ocupados(db, sessao_id)

        # Armazena o número total de fileiras da sala.
        # sala["fileiras"]: Obtém o número de fileiras na sala a partir do banco de dados.
        fileiras = sala["fileiras"]

        # Armazena o número de assentos por fileira na sala.
        # sala["assentos_por_fileira"]: Obtém o número de assentos por
        #       fileira a partir do banco de dados.
        assentos_por_fileira = sala["assentos_por_fileira"]

        # Inicializa uma lista vazia para armazenar a matriz de assentos.
        # A matriz será uma lista de listas, onde cada sublista
        #       representa uma fileira de assentos.
        matriz_assentos = []

        # Itera sobre o número total de fileiras para dividir os
        #       assentos em fileiras individuais.
        # range(fileiras): Gera índices de 0 até fileiras-1
        #       para iterar sobre cada fileira.
        for i in range(fileiras):

            # Calcula o índice inicial dos assentos para a fileira atual.
            # i * assentos_por_fileira: Multiplica o índice da fileira
            #       pelo número de assentos por fileira.
            start = i * assentos_por_fileira

            # Calcula o índice final dos assentos para a fileira atual.
            # start + assentos_por_fileira: Determina o final da fatia
            #       correspondente à fileira.
            end = start + assentos_por_fileira

            # Adiciona à matriz a lista de assentos correspondente à fileira atual.
            # assentos_totais[start:end]: Extrai os assentos da fileira
            #       atual da lista completa de assentos.
            matriz_assentos.append(assentos_totais[start:end])

        # Define uma função para alternar o estado de um assento quando clicado.
        # toggle_assento: Gerencia a seleção ou deseleção de um assento no mapa.
        def toggle_assento(assento, btn):

            # Verifica se o assento já está reservado.
            # assento in assentos_ocupados: Confirma se o assento
            #       está na lista de ocupados.
            if assento in assentos_ocupados:

                # Se o assento estiver reservado, abre a caixa de detalhes da reserva.
                # abrir_caixa_reserva: Função que exibe os detalhes da
                #       reserva para edição ou exclusão.
                # sessao_id, assento: Passa o ID da sessão e o assento para exibição.
                abrir_caixa_reserva(sessao_id, assento)
                return

            # Verifica se o assento está na lista de assentos selecionados pelo usuário.
            # assento in selected_assentos: Confirma se o assento já foi clicado anteriormente.
            if assento in selected_assentos:

                # Remove o assento da lista de selecionados se ele já estiver nela.
                # selected_assentos.remove: Remove o assento específico da lista de selecionados.
                selected_assentos.remove(assento)

                # Atualiza a aparência do botão para indicar que o assento foi desmarcado.
                # btn.config(bg="green", relief="raised"): Define a cor do
                #       botão como verde e estilo de relevo normal.
                btn.config(bg="green", relief="raised")

            else:

                # Adiciona o assento à lista de selecionados se ele ainda não estiver nela.
                # selected_assentos.add: Adiciona o assento à lista de selecionados.
                selected_assentos.add(assento)

                # Atualiza a aparência do botão para indicar que o assento foi marcado.
                # btn.config(bg="blue", relief="sunken"): Define a cor do
                #       botão como azul e estilo afundado.
                btn.config(bg="blue", relief="sunken")

        # Itera sobre a matriz de assentos para criar os botões no mapa.
        # for i, linha in enumerate(matriz_assentos): Itera sobre cada
        #       linha (fileira) da matriz de assentos.
        for i, linha in enumerate(matriz_assentos):

            # Itera sobre cada assento na linha.
            # for j, assento in enumerate(linha): Itera sobre os assentos na fileira atual.
            for j, assento in enumerate(linha):

                # Define a cor de fundo do botão com base na disponibilidade do assento.
                # bg_color: A cor do botão é cinza (reservado) ou verde (disponível).
                # "gray": Indica que o assento está ocupado (reservado).
                # "green": Indica que o assento está disponível.
                bg_color = "gray" if assento in assentos_ocupados else "green"

                # Cria o botão para representar o assento.
                # tk.Button: Cria um botão no mapa com o texto do identificador do assento.
                # frame_mapa: Define que o botão é filho do frame onde o mapa está localizado.
                # text=assento: Exibe o identificador do assento no botão.
                # bg=bg_color: Define a cor de fundo do botão com base na disponibilidade.
                # width=4: Define a largura do botão para caber o identificador do assento.
                btn = tk.Button(frame_mapa, text=assento, bg=bg_color, width=4)

                # Posiciona o botão no grid correspondente.
                # grid(row=i, column=j, padx=2, pady=2): Coloca o botão na
                #       célula da linha i e coluna j com espaçamento.
                btn.grid(row=i, column=j, padx=2, pady=2)

                # Configura o comando a ser executado ao clicar no botão.
                # btn.config: Define o comando do botão.
                # lambda b=btn, a=assento: toggle_assento(a, b): Cria uma função que
                #       alterna o estado do assento ao clicar.
                # b=btn: Passa o botão atual como argumento.
                # a=assento: Passa o identificador do assento como argumento.
                btn.config(command=lambda b=btn, a=assento: toggle_assento(a, b))


    # Associa um evento ao combo_filmes para atualizar as sessões ao selecionar um filme.
    # combo_filmes.bind: Liga o evento de seleção no combobox.
    # "<<ComboboxSelected>>": Evento disparado ao selecionar um item no combobox.
    # lambda e: atualizar_sessoes(): Chama a função
    #       atualizar_sessoes quando o evento ocorre.
    combo_filmes.bind("<<ComboboxSelected>>", lambda e: atualizar_sessoes())

    # Associa um evento ao combo_sessoes para exibir o mapa de
    #       assentos ao selecionar uma sessão.
    # combo_sessoes.bind: Liga o evento de seleção no combobox.
    # "<<ComboboxSelected>>": Evento disparado ao selecionar um item no combobox.
    # lambda e: exibir_mapa(): Chama a função exibir_mapa quando o evento ocorre.
    combo_sessoes.bind("<<ComboboxSelected>>", lambda e: exibir_mapa())


    # Exibe um rótulo para o campo do nome do cliente.
    # ttk.Label: Cria um widget de rótulo no Tkinter.
    # frame: Define que o rótulo é filho do frame principal.
    # text="Nome do Cliente:": Define o texto exibido no rótulo.
    # grid(row=4, column=0, sticky='e', padx=5, pady=5): Posiciona o
    #       rótulo na célula (4,0) com espaçamento e alinhamento à direita.
    ttk.Label(frame,
              text="Nome do Cliente:").grid(row=4, column=0, sticky='e', padx=5, pady=5)

    # Cria um campo de entrada de texto para o nome do cliente.
    # ttk.Entry: Widget para entrada de texto no Tkinter.
    # frame: Define que o campo é filho do frame principal.
    # width=30: Define a largura do campo de entrada como 30 caracteres.
    entrada_cliente_nome = ttk.Entry(frame, width=30)

    # Posiciona o campo de entrada na janela.
    # grid(row=4, column=1, padx=5, pady=5): Posiciona o
    #       campo na célula (4,1) com espaçamento.
    entrada_cliente_nome.grid(row=4, column=1, padx=5, pady=5)

    # Exibe um rótulo para o campo do telefone do cliente.
    # ttk.Label: Cria um widget de rótulo no Tkinter para exibir um texto fixo.
    # frame: Define que o rótulo será exibido dentro do frame principal da janela.
    # text="Telefone do Cliente:": Define o texto que será exibido no
    #       rótulo, indicando que o campo se refere ao telefone do cliente.
    # grid(row=5, column=0, sticky='e', padx=5, pady=5): Posiciona o rótulo
    #       na linha 5 e coluna 0 da grade (grid layout),
    #   com alinhamento à direita (sticky='e') dentro da célula. Adiciona
    #       espaçamento horizontal (padx=5) e vertical (pady=5) ao redor do rótulo.
    ttk.Label(frame,
              text="Telefone do Cliente:").grid(row=5, column=0, sticky='e', padx=5, pady=5)

    # Cria um campo de entrada de texto para o telefone do cliente.
    # ttk.Entry: Widget que permite a entrada de texto no Tkinter,
    #       utilizado aqui para o telefone do cliente.
    # frame: Define que o campo de entrada será exibido dentro do frame principal da janela.
    # width=20: Configura o campo de entrada com uma largura suficiente para
    #       até 20 caracteres, adequado para a maioria dos formatos de número de telefone.
    entrada_cliente_telefone = ttk.Entry(frame, width=20)

    # Posiciona o campo de entrada na janela.
    # grid(row=5, column=1, padx=5, pady=5): Posiciona o campo na
    #       linha 5 e coluna 1 da grade (grid layout).
    #   Adiciona espaçamento horizontal (padx=5) e vertical (pady=5) ao
    #       redor do campo de entrada.
    entrada_cliente_telefone.grid(row=5, column=1, padx=5, pady=5)

    # Inicia o processo para confirmar a reserva de assentos.
    def confirmar_reserva():

        # Obtém o texto da sessão selecionada no combobox.
        # combo_sessoes.get(): Retorna o texto da sessão atualmente
        #       selecionada no combobox `combo_sessoes`.
        sessao_txt = combo_sessoes.get()

        # Obtém o texto do filme selecionado no combobox.
        # combo_filmes.get(): Retorna o texto do filme atualmente
        #       selecionado no combobox `combo_filmes`.
        filme_txt = combo_filmes.get()

        # Obtém o nome do cliente inserido no campo de entrada.
        # entrada_cliente_nome.get(): Retorna o texto digitado no
        #       campo de entrada `entrada_cliente_nome`.
        # .strip(): Remove quaisquer espaços em branco extras no
        #       início e no final do texto.
        nome = entrada_cliente_nome.get().strip()

        # Obtém o telefone do cliente inserido no campo de entrada.
        # entrada_cliente_telefone.get(): Retorna o texto digitado no
        #       campo de entrada `entrada_cliente_telefone`.
        # .strip(): Remove quaisquer espaços em branco extras no
        #       início e no final do texto.
        telefone = entrada_cliente_telefone.get().strip()

        # Verifica se o texto do filme está vazio, indicando que nenhum filme foi selecionado.
        # if not filme_txt: Avalia como verdadeiro se `filme_txt` estiver vazio ou None.
        if not filme_txt:

            # Exibe uma mensagem de erro informando que é necessário selecionar um filme.
            # messagebox.showerror: Mostra uma caixa de diálogo de erro.
            # "Erro": Define o título da caixa de diálogo.
            # "Selecione um filme!": Define a mensagem de erro exibida ao usuário.
            # parent=janela: Define `janela` como a janela pai para a caixa de diálogo.
            messagebox.showerror("Erro", "Selecione um filme!", parent=janela)

            # Retorna imediatamente da função, interrompendo o processo de reserva.
            return

        # Verifica se o texto da sessão está vazio, indicando que
        #       nenhuma sessão foi selecionada.
        # if not sessao_txt: Avalia como verdadeiro se `sessao_txt`
        #       estiver vazio ou None.
        if not sessao_txt:

            # Exibe uma mensagem de erro informando que é necessário
            #       selecionar uma sessão.
            # messagebox.showerror: Mostra uma caixa de diálogo de erro.
            # "Erro": Define o título da caixa de diálogo.
            # "Selecione uma sessão!": Define a mensagem de erro exibida ao usuário.
            # parent=janela: Define `janela` como a janela pai para a caixa de diálogo.
            messagebox.showerror("Erro", "Selecione uma sessão!", parent=janela)

            # Retorna imediatamente da função, interrompendo o processo de reserva.
            return

        # Verifica se os campos de nome ou telefone do cliente estão vazios.
        # if not nome or not telefone: Avalia como verdadeiro
        #       se `nome` ou `telefone` estiverem vazios ou None.
        if not nome or not telefone:

            # Exibe uma mensagem de erro informando que é necessário preencher o
            #       nome e o telefone do cliente.
            # messagebox.showerror: Mostra uma caixa de diálogo de erro.
            # "Erro": Define o título da caixa de diálogo.
            # "Preencha nome e telefone do cliente!": Define a mensagem de
            #       erro exibida ao usuário.
            # parent=janela: Define `janela` como a janela pai
            #       para a caixa de diálogo.
            messagebox.showerror("Erro",
                                 "Preencha nome e telefone do cliente!", parent=janela)

            # Retorna imediatamente da função, interrompendo o processo de reserva.
            return

        # Verifica se nenhum assento foi selecionado.
        # if not selected_assentos: Avalia como verdadeiro
        #       se `selected_assentos` estiver vazio.
        if not selected_assentos:

            # Exibe uma mensagem de erro informando que é necessário
            #       selecionar pelo menos um assento.
            # messagebox.showerror: Mostra uma caixa de diálogo de erro.
            # "Erro": Define o título da caixa de diálogo.
            # "Selecione pelo menos um assento!": Define a mensagem de erro exibida ao usuário.
            # parent=janela: Define `janela` como a janela pai para a caixa de diálogo.
            messagebox.showerror("Erro", "Selecione pelo menos um assento!", parent=janela)

            # Retorna imediatamente da função, interrompendo o processo de reserva.
            return

        # Inicializa a variável `sessao_id` como None.
        # Essa variável será utilizada para armazenar o ID da sessão
        #       correspondente ao texto selecionado.
        sessao_id = None

        # Itera sobre os pares de IDs e textos das sessões armazenados no
        #       atributo `values_map` do combobox de sessões.
        # getattr: Obtém o atributo `values_map` de `combo_sessoes`, retornando
        #       uma lista vazia se o atributo não existir.
        for sid, texto in getattr(combo_sessoes, "values_map", []):

            # Compara o texto da sessão atual com o texto selecionado no combobox.
            # Se corresponder, define o `sessao_id` como o ID da sessão atual.
            if texto == sessao_txt:

                # Atribui o ID da sessão correspondente à variável `sessao_id`.
                sessao_id = sid

                # Interrompe o loop porque a sessão correspondente foi encontrada.
                break

        # Verifica se `sessao_id` ainda é None após a iteração, indicando
        #       que nenhuma sessão válida foi encontrada.
        # if not sessao_id: Avalia como verdadeiro se `sessao_id` for None ou vazio.
        if not sessao_id:

            # Exibe uma mensagem de erro informando que a sessão selecionada é inválida.
            # messagebox.showerror: Mostra uma caixa de diálogo de erro.
            # "Erro": Define o título da caixa de diálogo.
            # "Sessão inválida.": Define a mensagem de erro exibida ao usuário.
            # parent=janela: Define `janela` como a janela pai para a caixa de diálogo.
            messagebox.showerror("Erro", "Sessão inválida.", parent=janela)

            # Retorna imediatamente da função, interrompendo o processo de reserva.
            return

        try:

            # Tenta reservar os assentos selecionados para a sessão
            #       especificada no banco de dados.
            # `reservar_assentos`: Função que realiza a lógica de reserva no banco.
            # `db`: Conexão com o banco de dados.
            # `sessao_id`: ID da sessão selecionada.
            # `list(selected_assentos)`: Lista dos assentos selecionados pelo usuário.
            # `nome`: Nome do cliente.
            # `telefone`: Telefone do cliente.
            reservar_assentos(db, sessao_id, list(selected_assentos), nome, telefone)

            # Mostra uma mensagem de sucesso se os assentos forem reservados com sucesso.
            # messagebox.showinfo: Mostra uma caixa de diálogo de informação.
            # "Sucesso": Define o título da caixa de diálogo.
            # "Assentos reservados com sucesso!": Define a mensagem exibida ao usuário.
            # parent=janela: Define `janela` como a janela pai para a caixa de diálogo.
            messagebox.showinfo("Sucesso",
                                "Assentos reservados com sucesso!", parent=janela)

            # Após reservar os assentos, gera o ingresso correspondente.
            # `gerar_ingresso`: Função que cria um arquivo PDF com os dados do ingresso.
            # `nome_cliente`: Nome do cliente que reservou os assentos.
            # `telefone_cliente`: Telefone do cliente que reservou os assentos.
            # `filme`: Nome do filme da sessão reservada.
            # `sessao`: Texto representando a sessão reservada.
            # `assentos`: Lista dos assentos reservados.
            gerar_ingresso(nome_cliente=nome,
                           telefone_cliente=telefone,
                           filme=filme_txt,
                           sessao=sessao_txt,
                           assentos=list(selected_assentos), )

            # Limpa o campo de nome do cliente.
            # delete(0, tk.END): Remove o texto existente no campo.
            entrada_cliente_nome.delete(0, tk.END)

            # Limpa o campo de telefone do cliente.
            # delete(0, tk.END): Remove o texto existente no campo.
            entrada_cliente_telefone.delete(0, tk.END)

            # Limpa a seleção de assentos.
            # clear(): Remove todos os itens da variável `selected_assentos`.
            selected_assentos.clear()

            # Atualiza o mapa de assentos para refletir as alterações.
            # `exibir_mapa`: Função que redesenha os botões de assentos com base nas reservas.
            exibir_mapa()


        except ValueError as e:

            # Captura erros específicos de valor durante a reserva de assentos.
            # Exibe uma mensagem de erro com o texto da exceção levantada.
            # messagebox.showerror: Mostra uma caixa de diálogo de erro.
            # "Erro": Define o título da caixa de diálogo.
            # str(e): Converte a exceção para texto e exibe a mensagem ao usuário.
            # parent=janela: Define `janela` como a janela pai para a caixa de diálogo.
            messagebox.showerror("Erro", str(e), parent=janela)


    # Cria um botão para confirmar a reserva.
    # ttk.Button: Widget para criar botões no Tkinter com estilos modernos.
    # frame: Define que o botão será filho do frame principal.
    # text="Confirmar Reserva": Define o texto exibido no botão.
    # command=confirmar_reserva: Especifica a função a ser executada quando o botão for clicado.
    ttk.Button(frame, text="Confirmar Reserva", command=confirmar_reserva).grid(
        row=6,  # Define a linha na grade onde o botão será posicionado.
        column=0,  # Define a coluna na grade onde o botão será posicionado.
        columnspan=2,  # O botão ocupará duas colunas, centralizando-o no layout.
        pady=(10, 0)  # Define um espaçamento superior de 10 pixels e nenhum espaçamento inferior.
    )

    # Atualiza as sessões disponíveis no combobox assim que a tela é carregada.
    # `atualizar_sessoes`: Função que preenche o combobox de
    #       sessões com os dados disponíveis.
    atualizar_sessoes()



# Função para criar mapeamentos entre os detalhes textuais
#       das sessões e seus IDs, e vice-versa.
def obter_sessoes_map(db):

    # Primeiro, obtemos todas as sessões chamando a função obter_sessoes(),
    #       que retorna uma lista de todas as sessões armazenadas no banco de dados.
    sessoes = obter_sessoes(db)

    # Inicializamos uma lista vazia para armazenar os detalhes
    #       formatados das sessões junto com seus IDs.
    values = []

    # Iteramos sobre cada sessão na lista de sessões.
    for s in sessoes:

        # Obtemos os detalhes do filme chamando obter_filme_por_id(),
        #       passando o ID do filme da sessão.
        filme = obter_filme_por_id(db, s["filme_id"])

        # Obtemos os detalhes da sala chamando obter_sala_por_id(),
        #       passando o ID da sala da sessão.
        sala = obter_sala_por_id(db, s["sala_id"])

        # Formatamos uma string que contém o título do filme, a data e
        #       a hora da sessão, e o nome da sala.
        texto = f"{filme['titulo']} - {s['data']} {s['hora']} ({sala['nome']})"

        # Adicionamos uma tupla contendo o ID da sessão e o texto
        #       formatado à lista values.
        values.append((str(s["_id"]), texto))

    # Criamos um dicionário que mapeia os textos formatados das sessões
    #       para seus IDs, usando uma compreensão de dicionário.
    by_text = {v[1]: v[0] for v in values}

    # Criamos um dicionário que mapeia os IDs das sessões para seus textos
    #       formatados, também usando uma compreensão de dicionário.
    by_id = {v[0]: v[1] for v in values}

    # Retornamos ambos os dicionários.
    return by_text, by_id


# Função para obter uma lista de todas as reservas
#       armazenadas no banco de dados.
def obter_reservas(db):

    # db.reservas.find() busca todos os documentos na coleção 'reservas'.
    # list() converte o cursor retornado pelo método find() em uma lista de documentos,
    # facilitando a manipulação e a iteração sobre os dados retornados.
    return list(db.reservas.find())


# Função para deletar uma reserva específica da coleção 'reservas'.
def deletar_reserva(db, reserva_id):

    # db.reservas.delete_one() remove um único documento da coleção 'reservas'.
    # O documento a ser removido é identificado pelo '_id', que é
    #       convertido de uma string para ObjectId.
    # Isso garante que o documento correto seja identificado e removido.
    db.reservas.delete_one({"_id": ObjectId(reserva_id)})


# ============================================================
# TELA GERENCIAR RESERVAS (CRUD)
# ============================================================

def tela_gerenciar_reservas(root, db):

    # criar_janela_secundaria: Função para criar uma janela secundária
    # root: Passa a janela principal como referência para a criação da janela secundária
    # "Gerenciar Reservas (CRUD)": Define o título da janela secundária
    janela = criar_janela_secundaria(root, "Gerenciar Reservas (CRUD)")

    # largura_janela: Define a largura da janela secundária
    # altura_janela: Define a altura da janela secundária
    largura_janela = 900
    altura_janela = 600

    # largura_tela: Obtém a largura total da tela do dispositivo
    # altura_tela: Obtém a altura total da tela do dispositivo
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # pos_x: Calcula a posição horizontal para centralizar a janela
    # pos_y: Calcula a posição vertical para centralizar a janela
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    # geometry: Define a geometria da janela, incluindo dimensões e posição inicial
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Frame principal
    # frame_principal: Cria um frame principal na janela secundária
    #       para organizar os widgets
    # ttk.Frame: Utiliza o widget Frame do ttk para melhorar a aparência dos frames
    # janela: Define que o frame_principal será filho da janela secundária
    # padding="10 10 10 10": Aplica um espaçamento interno
    #       uniforme de 10 pixels em todas as direções
    frame_principal = ttk.Frame(janela, padding="10 10 10 10")

    # pack: Gerencia a geometria do frame principal para preencher e
    #       expandir dentro da janela secundária
    # fill="both": Permite que o frame se expanda tanto horizontal
    #       quanto verticalmente
    # expand=True: Habilita a expansão do frame para ocupar qualquer espaço extra
    frame_principal.pack(fill="both", expand=True)

    # grid_rowconfigure e grid_columnconfigure: Configurações para a
    #       expansão automática das linhas e colunas do frame
    # weight: Define a prioridade de expansão para linhas e colunas (maior peso = maior expansão)
    frame_principal.grid_rowconfigure(0, weight=1)  # Filtros
    frame_principal.grid_rowconfigure(2, weight=10)  # Treeview (área principal)
    frame_principal.grid_columnconfigure(0, weight=1)  # Colunas principais

    # Definição das colunas do Treeview

    # colunas: Define as colunas da tabela (Treeview)
    # Tupla contendo os nomes das colunas: "_id", "sessao", "assentos", "cliente_nome", "cliente_telefone"
    colunas = ("_id", "sessao", "assentos", "cliente_nome", "cliente_telefone")

    # Criação do Treeview
    # ttk.Treeview: Widget do Tkinter para exibir tabelas com múltiplas colunas
    # frame_principal: Define que o Treeview será filho do frame principal
    # columns=colunas: Define as colunas do Treeview
    # show="headings": Exibe apenas os cabeçalhos das colunas (sem
    #       uma coluna extra para expandir)
    # height=10: Define a altura da tabela (número de linhas visíveis)
    tree = ttk.Treeview(frame_principal, columns=colunas, show="headings", height=10)

    # Configuração das colunas
    # Itera por cada coluna definida em "colunas"
    for c in colunas:

        # heading: Define o cabeçalho de cada coluna
        # c: Nome da coluna (chave da coluna)
        # text=c.capitalize(): Exibe o texto do cabeçalho com a primeira letra maiúscula
        tree.heading(c, text=c.capitalize())

        # column: Configura a aparência e alinhamento de cada coluna
        # c: Nome da coluna
        # anchor="center": Alinha o conteúdo da coluna ao centro
        tree.column(c, anchor="center")

    # grid: Posiciona a Treeview no layout grid do frame principal
    # row=2: Posiciona na terceira linha (indexado a partir do zero)
    # column=0: Posiciona na primeira coluna
    # columnspan=5: Estende a Treeview para ocupar 5 colunas
    # sticky="nsew": Expande a Treeview para preencher todo o
    #       espaço disponível na célula do grid
    tree.grid(row=2, column=0, columnspan=5, sticky="nsew")

    # Scrollbar vertical
    # scrollbar: Cria uma barra de rolagem vertical para a Treeview
    # ttk.Scrollbar: Utiliza o widget Scrollbar do ttk para garantir uma
    #       aparência consistente com o restante da interface
    # frame_principal: Define o frame principal como o contêiner para a scrollbar
    # orient=tk.VERTICAL: Define a orientação da barra de rolagem como vertical
    scrollbar = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=tree.yview)

    # grid: Posiciona a scrollbar no layout grid do frame principal
    # row=2: Posiciona a scrollbar na mesma linha da Treeview
    # column=5: Posiciona a scrollbar na sexta coluna, ao lado direito da Treeview
    # sticky="ns": Faz com que a scrollbar se expanda verticalmente para
    #       preencher o espaço disponível entre o topo e o fundo do container
    scrollbar.grid(row=2, column=5, sticky="ns")

    # configure: Configura a Treeview para interagir com a scrollbar
    # yscrollcommand=scrollbar.set: Define o comando que será chamado
    #       pela Treeview quando a scrollbar for movida
    tree.configure(yscrollcommand=scrollbar.set)

    # frame_filtros: Cria um frame para conter os campos de filtro
    # ttk.Frame: Utiliza o widget Frame do ttk para a criação de
    #       um subcontainer no frame principal
    frame_filtros = ttk.Frame(frame_principal)

    # grid: Posiciona o frame_filtros no layout grid do frame principal
    # row=0: Posiciona no topo do frame principal
    # column=0: Inicia na primeira coluna
    # columnspan=5: Estende o frame de filtros para cobrir as mesmas 5 colunas da Treeview
    # sticky="nsew": Permite que o frame de filtros se expanda nas direções
    #       norte, sul, leste e oeste para preencher o espaço disponível
    # pady=5: Adiciona um espaçamento vertical de 5 pixels acima e
    #       abaixo do frame de filtros
    frame_filtros.grid(row=0, column=0, columnspan=5, sticky="nsew", pady=5)

    # filtros: Dicionário para armazenar as variáveis associadas a cada filtro
    # colunas: Lista de colunas definidas para a Treeview; cada
    #       uma terá um filtro associado
    # tk.StringVar(): Cria uma instância de StringVar para cada
    #       coluna, que armazenará o texto do filtro
    filtros = {col: tk.StringVar() for col in colunas}

    # entradas_filtro: Dicionário para armazenar os widgets de
    #       entrada de texto para os filtros
    entradas_filtro = {}

    # Loop para configurar os filtros e campos de entrada para
    #       cada coluna na Treeview
    for i, col in enumerate(colunas):

        # Configura cada coluna do frame de filtros para expandir igualmente
        # grid_columnconfigure: Ajusta a configuração da coluna para que ela
        #       se expanda quando a janela for redimensionada
        # i: Índice da coluna atual
        # weight=1: Atribui um peso igual para todas as colunas, permitindo que
        #       elas cresçam uniformemente conforme a janela se expande
        frame_filtros.grid_columnconfigure(i, weight=1)

        # Cria um rótulo para cada campo de filtro
        # ttk.Label: Cria um widget de rótulo no frame de filtros
        # text=col.capitalize(): Define o texto do rótulo com o nome da coluna capitalizado
        # grid: Posiciona o rótulo no grid
        # row=0: Posiciona na primeira linha do frame de filtros
        # column=i: Posiciona na coluna correspondente ao índice da coluna atual
        # padx=5: Define um preenchimento horizontal de 5 pixels para separar os rótulos
        # sticky="w": Alinha o rótulo à esquerda (west) dentro da célula do grid
        ttk.Label(frame_filtros, text=col.capitalize()).grid(row=0, column=i, padx=5, sticky="w")

        # Cria um campo de entrada para cada filtro
        # ttk.Entry: Cria um widget de entrada de texto no frame de filtros
        # textvariable=filtros[col]: Associa o campo de entrada à variável StringVar
        #       correspondente para armazenar e manipular o texto de filtro
        # entradas_filtro[col]: Armazena o widget de entrada no dicionário
        #       entradas_filtro usando a chave da coluna
        # grid: Posiciona o campo de entrada no grid
        # row=1: Posiciona na segunda linha do frame de filtros
        # column=i: Posiciona na coluna correspondente ao índice da coluna atual
        # padx=5: Define um preenchimento horizontal de 5 pixels para
        #       separar os campos de entrada
        # sticky="ew": Faz com que o campo de entrada se expanda horizontalmente
        #       para preencher a célula do grid
        entradas_filtro[col] = ttk.Entry(frame_filtros, textvariable=filtros[col])
        entradas_filtro[col].grid(row=1, column=i, padx=5, sticky="ew")

    # Variável global reservas_cache para armazenar temporariamente as reservas
    # reservas_cache: Lista vazia inicializada para armazenar os dados das
    #       reservas carregadas ou manipuladas durante a sessão
    reservas_cache = []


    def carregar_reservas():

        # Descrição da função para carregar as reservas
        """Carrega as reservas do banco e as insere no TreeView."""

        # A palavra-chave nonlocal é usada para trabalhar com a variável
        #       reservas_cache que é definida fora desta função.
        nonlocal reservas_cache

        # Limpa a lista reservas_cache para garantir que apenas as
        #       reservas atualizadas estejam na cache.
        reservas_cache.clear()

        # Loop para remover todos os itens existentes no TreeView,
        #       garantindo que não haja duplicação de dados ao recarregar.
        for i in tree.get_children():
            tree.delete(i)

        # Obtém um mapeamento dos IDs das sessões para seus textos
        #       descritivos para exibição amigável no TreeView.
        sessoes_map = obter_sessoes_map(db)[1]

        # Busca todas as reservas no banco de dados e itera sobre cada uma.
        for r in obter_reservas(db):

            # Busca o texto descritivo da sessão usando o ID da sessão da
            #       reserva, se não encontrado, usa "Sessão desconhecida".
            sessao_texto = sessoes_map.get(str(r["sessao_id"]), "Sessão desconhecida")

            # Compila os valores da reserva em uma tupla para inserção no TreeView.
            valores = (
                str(r["_id"]),  # ID da reserva
                sessao_texto,  # Texto descritivo da sessão
                ",".join(r["assentos_reservados"]),  # Assentos reservados, listados e separados por vírgulas
                r["cliente"]["nome"],  # Nome do cliente
                r["cliente"]["telefone"],  # Telefone do cliente
            )

            # Adiciona a tupla de valores ao cache de reservas.
            reservas_cache.append(valores)

            # Insere a reserva no TreeView.
            tree.insert("", "end", values=valores)



    def aplicar_filtros(event=None):

        # Descrição da função para aplicar filtros
        """Aplica os filtros dinamicamente no TreeView."""

        # Loop para remover todos os itens existentes no TreeView
        #       antes de aplicar os filtros.
        for i in tree.get_children():
            tree.delete(i)

        # Itera sobre cada reserva armazenada no cache
        for reserva in reservas_cache:

            # Aplica os filtros dinamicamente:
            # Utiliza uma compreensão de lista para verificar se todos os filtros
            #       especificados estão presentes nos valores da reserva.
            # `filtros[col].get().lower()` obtém o valor do filtro para a coluna,
            #       convertido para minúsculas, para comparação insensível a maiúsculas.
            # `reserva[idx].lower()` obtém o valor correspondente da reserva, também em minúsculas.
            # `enumerate(colunas)` é usado para obter o índice e o nome da coluna ao
            #       mesmo tempo, permitindo acessar o valor correto na reserva.
            if all(filtros[col].get().lower() in reserva[idx].lower() for idx, col in enumerate(colunas)):

                # Se todos os filtros correspondem, insere a reserva no TreeView.
                tree.insert("", "end", values=reserva)

    # Associar o evento de filtro ao KeyRelease
    for col in colunas:

        # Associa o evento de liberação de tecla ao campo de entrada
        #       para cada coluna de filtro
        # <KeyRelease> é um evento que ocorre quando uma tecla é solta
        # aplicar_filtros é chamado sempre que uma tecla é liberada, atualizando os
        #       itens visíveis baseados no filtro de entrada
        entradas_filtro[col].bind("<KeyRelease>", aplicar_filtros)


    # Chama a função carregar_reservas para popular inicialmente o
    #       TreeView com dados de reservas
    carregar_reservas()

    # Frame de Edição
    # Cria um frame para conter os widgets de edição de reservas
    frame_edicao = ttk.Frame(frame_principal, padding="10 10 10 10")

    # Configura o layout do frame de edição na janela principal
    # grid posiciona o frame na linha 3, coluna 0 e se estende por 5 colunas
    # sticky="ew" faz com que o frame se expanda horizontalmente
    #       para preencher o espaço disponível
    frame_edicao.grid(row=3, column=0, columnspan=5, sticky="ew")

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_edicao'
    # text="Sessão:": Define o texto do rótulo como "Sessão:"
    # grid: Posiciona o rótulo no layout grid
    # row=0, column=0: Posiciona o rótulo na linha 0, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_edicao,
              text="Sessão:").grid(row=0, column=0, sticky="e", padx=5, pady=5)

    # combo_sessao: Cria um campo de seleção dropdown para escolher
    #       entre as sessões disponíveis
    # ttk.Combobox: Widget do Tkinter para criar um campo de seleção dropdown
    # frame_edicao: Define que o combobox será filho do frame_edicao
    # width=40: Define a largura do combobox como 40 unidades, adequado
    #       para exibir informações da sessão
    combo_sessao = ttk.Combobox(frame_edicao, width=40)

    # grid: Posiciona o combobox no layout grid
    # row=0, column=1: Posiciona o combobox na linha 0,
    #       coluna 1 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e
    #       vertical de 5 pixels para o combobox
    combo_sessao.grid(row=0, column=1, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_edicao'
    # text="Assentos:": Define o texto do rótulo como "Assentos:"
    # grid: Posiciona o rótulo no layout grid
    # row=0, column=2: Posiciona o rótulo na linha 0, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_edicao,
              text="Assentos:").grid(row=0, column=2, sticky="e", padx=5, pady=5)

    # entrada_assentos: Cria um campo de entrada de texto para
    #       inserir a quantidade de assentos ou a lista de assentos
    # ttk.Entry: Widget do Tkinter para criar um campo de entrada de texto
    # frame_edicao: Define que o campo será filho do frame_edicao
    # width=30: Define a largura do campo de entrada como 30 caracteres,
    #       adequado para inserir uma lista de assentos
    entrada_assentos = ttk.Entry(frame_edicao, width=30)

    # grid: Posiciona o campo de entrada no layout grid
    # row=0, column=3: Posiciona o campo de entrada na linha 0, coluna 3 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e
    #       vertical de 5 pixels para o campo de entrada
    entrada_assentos.grid(row=0, column=3, padx=5, pady=5)

    # ttk.Label: Cria um rótulo para o campo de entrada no frame 'frame_edicao'
    # text="Nome do Cliente:": Define o texto do rótulo como "Nome do Cliente:"
    # grid: Posiciona o rótulo no layout grid
    # row=1, column=0: Posiciona o rótulo na linha 1, coluna 0 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels
    ttk.Label(frame_edicao,
              text="Nome do Cliente:").grid(row=1, column=0, sticky="e", padx=5, pady=5)

    # entrada_nome: Cria um campo de entrada de texto para o nome do cliente
    # ttk.Entry: Widget do Tkinter para criar um campo de entrada de texto
    # frame_edicao: Define que o campo será filho do frame_edicao
    # width=30: Define a largura do campo de entrada como 30 caracteres
    entrada_nome = ttk.Entry(frame_edicao, width=30)

    # grid: Posiciona o campo de entrada no layout grid
    # row=1, column=1: Posiciona o campo de entrada na linha 1,
    #       coluna 1 do layout grid
    # padx=5, pady=5: Define um espaçamento horizontal e vertical
    #       de 5 pixels para o campo de entrada
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    # ttk.Label para o telefone: Cria um rótulo para o campo de entrada
    #       de telefone no frame 'frame_edicao'
    # text="Telefone:": Define o texto do rótulo como "Telefone", informando o
    #       usuário sobre a finalidade do campo adjacente
    # grid: Posiciona o rótulo no layout grid do Tkinter
    # row=1, column=2: Posiciona o rótulo na linha 1, coluna 2 do layout grid
    # sticky="e": Alinha o rótulo à direita (east) dentro da célula do grid,
    #       assegurando alinhamento com outros rótulos
    # padx=5, pady=5: Define um espaçamento horizontal e vertical de 5 pixels,
    #       mantendo uma distância adequada entre elementos para uma interface organizada
    ttk.Label(frame_edicao,
              text="Telefone:").grid(row=1, column=2, sticky="e", padx=5, pady=5)

    # entrada_telefone: Cria um campo de entrada de texto onde o usuário
    #       pode digitar o número de telefone do cliente
    # ttk.Entry: Utiliza o widget Entry do Tkinter que permite a entrada de
    #       uma única linha de texto
    # frame_edicao: Especifica que este campo de entrada é um elemento filho do
    #       frame_edicao, garantindo que herde estilos e comportamentos
    # width=20: Estabelece a largura do campo de entrada para 20 caracteres, o
    #       que é adequado para acomodar a maioria dos formatos de
    #       número de telefone sem truncamento
    entrada_telefone = ttk.Entry(frame_edicao, width=20)

    # grid: Posiciona o campo de entrada no grid
    # row=1, column=3: Posiciona o campo na linha 1, coluna 3, diretamente ao
    #       lado do seu rótulo correspondente para fácil associação visual pelo usuário
    # padx=5, pady=5: Aplica um espaçamento horizontal e vertical de 5 pixels
    #       em torno do campo de entrada, contribuindo para uma interface
    #       visualmente agradável e fácil de usar
    entrada_telefone.grid(row=1, column=3, padx=5, pady=5)


    # reserva_id_edicao: Lista contendo None inicialmente, utilizado
    #       para armazenar o ID da reserva sendo editada
    reserva_id_edicao = [None]

    # Definição da função carregar_sessoes_combo
    # Descrição: Carrega todas as sessões disponíveis no banco de
    #       dados e as exibe no combobox para seleção.
    def carregar_sessoes_combo():

        """Carrega as sessões no combobox de edição."""

        # Chama a função obter_sessoes para buscar todas as sessões
        #       armazenadas no banco de dados.
        sessoes = obter_sessoes(db)

        # Inicializa uma lista vazia para armazenar os mapeamentos
        #       entre ID da sessão e sua descrição formatada.
        sessoes_map = []

        # Itera sobre cada sessão obtida da base de dados.
        for sessao in sessoes:

            # Busca o filme correspondente ao ID do filme da sessão atual.
            filme = obter_filme_por_id(db, sessao["filme_id"])

            # Busca a sala correspondente ao ID da sala da sessão atual.
            sala = obter_sala_por_id(db, sessao["sala_id"])

            # Formata a descrição da sessão para incluir título do
            #       filme, data, hora e nome da sala.
            texto_sessao = f"{filme['titulo']} - {sessao['data']} {sessao['hora']} ({sala['nome']})"

            # Adiciona uma tupla contendo o ID da sessão e sua
            #       descrição formatada à lista sessoes_map.
            sessoes_map.append((str(sessao["_id"]), texto_sessao))

        # Armazena o mapeamento entre ID da sessão e descrição no
        #       atributo values_map do combobox.
        combo_sessao.values_map = sessoes_map

        # Atualiza os valores exibíveis no combobox para apenas as
        #       descrições das sessões.
        combo_sessao["values"] = [v[1] for v in sessoes_map]


    # Definição da função carregar_dados_edicao
    # Descrição: Carrega os dados da reserva selecionada nos campos de
    #       edição para permitir alterações.
    def carregar_dados_edicao(event):

        """Carrega os dados da reserva selecionada para os campos de edição."""

        # Obtém a seleção atual do Treeview, que lista todas as reservas.
        sel = tree.selection()

        # Verifica se há algum item selecionado. Se não, a função
        #       retorna e não faz nada.
        if not sel:
            return

        # Obtém os dados do item selecionado no Treeview.
        item = tree.item(sel)

        # Extrai os valores dos dados da reserva selecionada (ID, sessão,
        #       assentos, nome do cliente, telefone do cliente).
        vals = item["values"]

        # Armazena o ID da reserva no array global reserva_id_edicao
        #       para uso em operações de atualização ou deleção.
        reserva_id_edicao[0] = vals[0]

        # Sessão: Define o valor do combobox de sessões para a
        #       sessão da reserva selecionada.
        sessao_texto = vals[1]
        combo_sessao.set(sessao_texto)

        # Assentos: Limpa o campo de entrada dos assentos e
        #       insere os assentos reservados.
        entrada_assentos.delete(0, tk.END)
        entrada_assentos.insert(0, vals[2])

        # Nome do Cliente: Limpa o campo de entrada do nome e
        #       insere o nome do cliente da reserva.
        entrada_nome.delete(0, tk.END)
        entrada_nome.insert(0, vals[3])

        # Telefone: Limpa o campo de entrada do telefone e
        #       insere o telefone do cliente.
        entrada_telefone.delete(0, tk.END)
        entrada_telefone.insert(0, vals[4])


    def deletar_reserva_selecionada():

        """Deleta a reserva selecionada."""

        # Verifica se existe uma reserva selecionada para deletar.
        # 'reserva_id_edicao[0]' contém o ID da reserva em edição. Se
        #       for None, nenhuma reserva está selecionada.
        if not reserva_id_edicao[0]:

            # Exibe uma mensagem de erro caso nenhuma reserva esteja selecionada.
            messagebox.showerror("Erro",
                                 "Nenhuma reserva selecionada para deletar!",
                                 parent=janela)
            return

        # Pergunta ao usuário se ele realmente deseja deletar a reserva selecionada.
        # Exibe uma caixa de diálogo com as opções 'Sim' e 'Não'.
        resposta = messagebox.askyesno("Confirmar",
                                       "Deseja realmente deletar a reserva?", parent=janela)

        # Verifica se o usuário confirmou a exclusão.
        if resposta:

            try:

                # Tenta deletar a reserva do banco de dados.
                # Parâmetro passado:
                # - db: Conexão com o banco de dados.
                # - reserva_id_edicao[0]: ID da reserva a ser deletada.
                deletar_reserva(db, reserva_id_edicao[0])

                # Exibe uma mensagem de sucesso informando que a reserva foi deletada.
                messagebox.showinfo("Sucesso", "Reserva deletada com sucesso!", parent=janela)

                # Recarrega a lista de reservas no Treeview para refletir a exclusão.
                carregar_reservas()

                # Limpa os campos de entrada relacionados à reserva, como assentos, nome e telefone.
                limpar_campos([entrada_assentos, entrada_nome, entrada_telefone])

                # Reseta o ID da reserva em edição para None, indicando que
                #       nenhuma reserva está atualmente selecionada.
                reserva_id_edicao[0] = None

            except Exception as e:

                # Captura qualquer erro ocorrido durante a tentativa de deletar a reserva.
                # Exibe uma mensagem de erro detalhada com o motivo do erro.
                messagebox.showerror("Erro",
                                     f"Erro ao deletar reserva: {str(e)}", parent=janela)



    def salvar_alteracoes_reserva():

        """Salva as alterações feitas na reserva selecionada,
                atualizando os dados no banco de dados."""

        # Verifica se uma reserva está realmente selecionada para
        #       edição. Caso não esteja, exibe uma mensagem de erro.
        if not reserva_id_edicao[0]:
            messagebox.showerror("Erro",
                                 "Nenhuma reserva selecionada para edição!",
                                 parent=janela)
            return

        # Obtém o texto do combo box que indica a sessão selecionada.
        sessao_texto = combo_sessao.get()

        # Obtém o texto que lista os assentos reservados, removendo espaços desnecessários.
        assentos_texto = entrada_assentos.get().strip()

        # Obtém o nome do cliente da reserva, removendo espaços desnecessários.
        nome_cliente = entrada_nome.get().strip()

        # Obtém o telefone do cliente da reserva, removendo espaços desnecessários.
        telefone_cliente = entrada_telefone.get().strip()

        # Verifica se todos os campos necessários (sessão, assentos,
        #       nome do cliente e telefone) estão preenchidos.
        if not all([sessao_texto, assentos_texto, nome_cliente, telefone_cliente]):

            # Se algum campo não estiver preenchido, exibe uma mensagem de erro
            #       indicando que todos os campos devem ser preenchidos.
            messagebox.showerror("Erro",
                                 "Preencha todos os campos!",
                                 parent=janela)
            return

        # Inicializa a variável 'sessao_id' como None para verificar
        #       se a sessão escolhida é válida.
        sessao_id = None

        # Itera sobre o mapeamento de sessões disponíveis para
        #       encontrar o ID correspondente ao texto selecionado.
        for sid, texto in combo_sessao.values_map:

            # Se o texto do combo box corresponde a uma das sessões,
            #       atribui o ID desta sessão à variável 'sessao_id'.
            if texto == sessao_texto:
                sessao_id = sid

                # Sai do loop após encontrar o ID correto, otimizando o processo.
                break

        # Verifica se o ID da sessão foi encontrado.
        if not sessao_id:

            # Se o ID não foi encontrado, exibe uma mensagem de erro
            #       informando que a sessão é inválida.
            messagebox.showerror("Erro",
                                 "Sessão inválida!", parent=janela)
            return

        # Processa o texto dos assentos, dividindo a string por vírgulas e
        #       removendo espaços desnecessários.
        # Isso é necessário porque os assentos podem ser inseridos como
        #       uma lista separada por vírgulas no campo de texto.
        assentos = [a.strip() for a in assentos_texto.split(",")]

        try:

            # Tenta atualizar a reserva no banco de dados usando a
            #       função 'atualizar_reserva'.
            # Parâmetros passados:
            # - db: Conexão com o banco de dados.
            # - reserva_id_edicao[0]: ID da reserva que está sendo editada.
            # - sessao_id: ID da sessão selecionada no combobox.
            # - assentos: Lista de assentos reservados.
            # - nome_cliente: Nome do cliente fornecido no campo de entrada.
            # - telefone_cliente: Telefone do cliente fornecido no campo de entrada.
            atualizar_reserva(db,
                              reserva_id_edicao[0], sessao_id, assentos, nome_cliente, telefone_cliente)

            # Exibe uma mensagem informando que a reserva foi atualizada com sucesso.
            messagebox.showinfo("Sucesso", "Reserva atualizada!", parent=janela)

            # Recarrega a lista de reservas no Treeview para refletir as alterações feitas.
            carregar_reservas()

            # Limpa os campos de entrada para que fiquem prontos
            #       para uma nova inserção ou edição.
            limpar_campos([entrada_assentos, entrada_nome, entrada_telefone])

            # Reseta o ID da reserva em edição para None, indicando que nenhuma
            #       reserva está atualmente selecionada para edição.
            reserva_id_edicao[0] = None

        except Exception as e:

            # Captura qualquer exceção que possa ocorrer durante o
            #       processo de atualização.
            # Exibe uma mensagem de erro detalhando o problema encontrado,
            #       incluindo a mensagem da exceção (str(e)).
            messagebox.showerror("Erro",
                                 f"Erro ao salvar alterações: {str(e)}", parent=janela)



    # carregar_sessoes_combo: Carrega as sessões disponíveis no combobox.
    # Função responsável por buscar todas as sessões no banco de dados e
    #       preenchê-las no combobox `combo_sessao` no formato adequado.
    carregar_sessoes_combo()

    # Botão "Salvar Alterações"
    # ttk.Button: Cria um botão para salvar as alterações feitas em uma reserva.
    # frame_edicao: Define o botão como filho do frame de edição.
    # text="Salvar Alterações": Define o texto exibido no botão.
    # command=salvar_alteracoes_reserva: Associa o botão à função `salvar_alteracoes_reserva`,
    #       que será executada ao clicar no botão.
    # grid: Posiciona o botão no layout da grade (row=2, column=2).
    # padx=5, pady=10: Adiciona espaçamento horizontal (5) e vertical (10) ao redor do botão.
    ttk.Button(frame_edicao,
               text="Salvar Alterações",
               command=salvar_alteracoes_reserva).grid(row=2, column=2, padx=5, pady=10)

    # Botão "Deletar"
    # ttk.Button: Cria um botão para deletar a reserva selecionada.
    # frame_edicao: Define o botão como filho do frame de edição.
    # text="Deletar": Define o texto exibido no botão.
    # command=deletar_reserva_selecionada: Associa o botão à função `deletar_reserva_selecionada`,
    #       que será executada ao clicar no botão.
    # grid: Posiciona o botão no layout da grade (row=2, column=3).
    # padx=5, pady=10: Adiciona espaçamento horizontal (5) e vertical (10) ao redor do botão.
    ttk.Button(frame_edicao,
               text="Deletar",
               command=deletar_reserva_selecionada).grid(row=2, column=3, padx=5, pady=10)

    # tree.bind: Associa um evento ao Treeview.
    # "<<TreeviewSelect>>": Evento gerado sempre que uma linha do Treeview é selecionada.
    # carregar_dados_edicao: Função que será executada quando o evento de
    #       seleção ocorrer. Essa função carrega os dados da reserva selecionada
    #       nos campos de edição.
    tree.bind("<<TreeviewSelect>>", carregar_dados_edicao)

    # Botão "Recarregar"
    # ttk.Button: Cria um botão para recarregar as reservas exibidas no Treeview.
    # frame_principal: Define o botão como filho do frame principal.
    # text="Recarregar": Define o texto exibido no botão como "Recarregar".
    # command=carregar_reservas: Associa o botão à função `carregar_reservas`, que
    #       será executada ao clicar no botão. Essa função recarrega os
    #       dados das reservas no Treeview.
    # grid: Posiciona o botão no layout da grade (row=4, column=0).
    # pady=10: Adiciona um espaçamento vertical de 10 pixels ao redor do botão.
    ttk.Button(frame_principal,
               text="Recarregar",
               command=carregar_reservas).grid(row=4, column=0, pady=10)


# ============================================================
# RELATÓRIO
# ============================================================
def tela_relatorio_lucro(root, db):

    """
    Função para criar e exibir a janela de Relatório de Lucro.
    """

    # Cria uma nova janela secundária com o título especificado.
    # root: Define a janela principal como pai desta nova janela.
    # "Relatório de Lucro": Título exibido na barra de título da nova janela.
    janela = criar_janela_secundaria(root, "Relatório de Lucro")

    # Define as dimensões fixas para a nova janela.
    # largura_janela: Largura da janela em pixels.
    # altura_janela: Altura da janela em pixels.
    largura_janela = 1100  # Define a largura como 1100 pixels.
    altura_janela = 450  # Define a altura como 450 pixels.

    # Obtém as dimensões da tela principal.
    # largura_tela: Largura total da tela do monitor em pixels.
    # altura_tela: Altura total da tela do monitor em pixels.
    largura_tela = root.winfo_screenwidth()  # Largura da tela principal.
    altura_tela = root.winfo_screenheight()  # Altura da tela principal.

    # Calcula as coordenadas para centralizar a janela na tela.
    # pos_x: Coordenada horizontal para posicionar a janela no centro da tela.
    # pos_y: Coordenada vertical para posicionar a janela no centro da tela.
    # Subtrai a largura da janela da largura da tela e divide por 2.
    pos_x = (largura_tela - largura_janela) // 2

    # Subtrai a altura da janela da altura da tela e divide por 2.
    pos_y = (altura_tela - altura_janela) // 2

    # Define as dimensões e a posição inicial da janela.
    # f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}": String formatada
    #       para configurar largura, altura e posição.
    janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    # Criação do frame principal que abrigará todo o conteúdo da janela.
    # ttk.Frame: Cria um contêiner para agrupar widgets.
    # janela: Define que o frame será um elemento filho da janela principal.
    # padding="10 10 10 10": Define um espaçamento interno (padding)
    #       de 10 pixels em todos os lados.
    frame_principal = ttk.Frame(janela, padding="10 10 10 10")

    # Posiciona o frame principal dentro da janela.
    # pack: Gerenciador de geometria que organiza os widgets no contêiner.
    # fill='both': Permite que o frame se expanda tanto horizontal quanto verticalmente.
    # expand=True: Permite que o frame ocupe o máximo de espaço disponível.
    frame_principal.pack(fill='both', expand=True)

    # Criação do frame de filtros para adicionar elementos de entrada ou seleção.
    # ttk.Frame: Cria um contêiner para widgets relacionados a filtros.
    # frame_principal: Define o frame principal como pai deste frame de filtros.
    frame_filtros = ttk.Frame(frame_principal)

    # Posiciona o frame de filtros dentro do frame principal.
    # grid(row=0, column=0, columnspan=6): Posiciona o frame na
    #       linha 0 e faz com que ele se estenda por 6 colunas.
    # sticky="ew": Permite que o frame se expanda horizontalmente (leste-oeste).
    # pady=5: Adiciona um espaçamento vertical de 5 pixels ao redor do frame.
    frame_filtros.grid(row=0, column=0, columnspan=6, sticky="ew", pady=5)

    # Dicionário para armazenar as variáveis associadas aos filtros.
    # Cada chave representa um filtro específico (sessão, filme, sala, etc.).
    # tk.StringVar(): Cria uma variável Tkinter que será vinculada aos campos de entrada.
    filtros = {
        "sessao": tk.StringVar(),
        "filme": tk.StringVar(),
        "sala": tk.StringVar(),
        "data": tk.StringVar(),
        "hora": tk.StringVar()
    }

    # Loop para criar rótulos e campos de entrada para cada filtro.
    # enumerate: Retorna o índice (i) e o nome do filtro (filtro) no dicionário.
    for i, filtro in enumerate(filtros.keys()):

        # Criação de um rótulo para cada filtro.
        # ttk.Label: Widget que cria um rótulo no Tkinter.
        # frame_filtros: Define o frame de filtros como o pai do rótulo.
        # text=filtro.capitalize(): Define o texto do rótulo com o nome do
        #       filtro em maiúscula inicial.
        # grid(row=0, column=i, padx=5): Posiciona o rótulo na linha 0 e na
        #       coluna correspondente ao índice.
        # padx=5: Adiciona um espaçamento horizontal de 5 pixels entre os rótulos.
        ttk.Label(frame_filtros, text=filtro.capitalize()).grid(row=0, column=i, padx=5)

        # Criação de um campo de entrada de texto para cada filtro.
        # ttk.Entry: Widget que cria um campo de entrada no Tkinter.
        # frame_filtros: Define o frame de filtros como o pai do campo de entrada.
        # textvariable=filtros[filtro]: Vincula o campo à variável
        #       correspondente no dicionário filtros.
        # width=15: Define a largura do campo de entrada como 15 caracteres.
        # grid(row=1, column=i, padx=5): Posiciona o campo na linha 1 e
        #       na coluna correspondente ao índice.
        # padx=5: Adiciona um espaçamento horizontal de 5 pixels entre os campos.
        ttk.Entry(frame_filtros,
                  textvariable=filtros[filtro], width=15).grid(row=1, column=i, padx=5)


    # Criação de um botão para aplicar os filtros configurados.
    # ttk.Button: Widget para criar um botão no Tkinter.
    # frame_filtros: Define o frame de filtros como o pai do botão.
    # text="Aplicar Filtro": Define o texto exibido no botão.
    # command=lambda: aplicar_filtros(filtros): Associa a ação de
    #       clique do botão à função aplicar_filtros,
    # passando o dicionário filtros como argumento.
    # grid(row=1, column=len(filtros), padx=5): Posiciona o botão na
    #       linha 1 e na coluna seguinte à última
    # coluna de filtros, com espaçamento horizontal de 5 pixels.
    ttk.Button(frame_filtros,
               text="Aplicar Filtro",
               command=lambda: aplicar_filtros(filtros)
               ).grid(row=1, column=len(filtros), padx=5)

    # Criação de um frame para acomodar a tabela (Treeview) e suas barras de rolagem.
    # ttk.Frame: Widget para criar um container de layout no Tkinter.
    # frame_principal: Define o frame principal como o pai do frame_tree.
    # grid(row=2, column=0, columnspan=6, sticky="nsew"): Posiciona o frame na linha 2,
    # ocupando todas as 6 colunas, com expansão automática para preencher todo o espaço disponível.
    frame_tree = ttk.Frame(frame_principal)
    frame_tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

    # Configuração das colunas da tabela que exibirá os resultados.
    # Lista contendo os nomes das colunas a serem exibidas na tabela.
    colunas = ["Sessão", "Filme", "Sala", "Data", "Hora", "Assentos Reservados", "Valor Total"]

    # Criação da tabela de resultados (Treeview).
    # ttk.Treeview: Widget utilizado para criar tabelas no Tkinter.
    # frame_tree: Define o frame_tree como o pai da tabela.
    # columns=colunas: Define as colunas da tabela com base na lista 'colunas'.
    # show="headings": Exibe apenas os cabeçalhos das colunas, sem
    #       uma coluna de identificação extra.
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings")

    # Configuração de cada coluna da tabela.
    # Itera sobre a lista de colunas para configurar o cabeçalho e
    #       os atributos de cada coluna.
    for col in colunas:

        # Define o texto exibido no cabeçalho da coluna.
        # heading: Configura o texto do cabeçalho da coluna.
        tree.heading(col, text=col)

        # Configura o alinhamento e a largura de cada coluna.
        # anchor="center": Centraliza o conteúdo das células dentro da coluna.
        # width=150: Define a largura inicial de cada coluna como 150 pixels.
        tree.column(col, anchor="center", width=150)

    # Configuração das barras de rolagem para a tabela.

    # Criação da barra de rolagem vertical.
    # ttk.Scrollbar: Widget utilizado para criar barras de rolagem no Tkinter.
    # frame_tree: Define o frame_tree como o pai da barra de rolagem.
    # orient=tk.VERTICAL: Configura a barra para rolar verticalmente.
    # command=tree.yview: Conecta a barra de rolagem à funcionalidade de rolagem vertical da tabela.
    scrollbar_vertical = ttk.Scrollbar(frame_tree,
                                       orient=tk.VERTICAL,
                                       command=tree.yview)

    # Criação da barra de rolagem horizontal.
    # orient=tk.HORIZONTAL: Configura a barra para rolar horizontalmente.
    # command=tree.xview: Conecta a barra de rolagem à funcionalidade de rolagem horizontal da tabela.
    scrollbar_horizontal = ttk.Scrollbar(frame_tree,
                                         orient=tk.HORIZONTAL,
                                         command=tree.xview)

    # Configuração da tabela para sincronizar com as barras de rolagem.
    # tree.configure: Define os parâmetros de configuração da tabela.
    # yscrollcommand=scrollbar_vertical.set: Configura a tabela para responder à rolagem vertical.
    # xscrollcommand=scrollbar_horizontal.set: Configura a tabela para responder à rolagem horizontal.
    tree.configure(yscrollcommand=scrollbar_vertical.set,
                   xscrollcommand=scrollbar_horizontal.set)

    # Posicionamento da tabela no layout do frame_tree.

    # tree.grid: Posiciona a tabela no layout usando o método grid.
    # row=0, column=0: Define a posição da tabela na linha 0 e coluna 0 do grid.
    # sticky="nsew": Faz com que a tabela se expanda para preencher todo o
    #       espaço disponível nas direções norte, sul, leste e oeste.
    tree.grid(row=0, column=0, sticky="nsew")

    # Posicionamento da barra de rolagem vertical no layout do frame_tree.

    # scrollbar_vertical.grid: Posiciona a barra de rolagem vertical no layout.
    # row=0, column=1: Define a posição na linha 0 e coluna 1.
    # sticky="ns": Faz com que a barra de rolagem vertical se expanda
    #        para preencher toda a altura (norte-sul) do espaço disponível.
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")

    # Posicionamento da barra de rolagem horizontal no layout do frame_tree.

    # scrollbar_horizontal.grid: Posiciona a barra de rolagem horizontal no layout.
    # row=1, column=0: Define a posição na linha 1 e coluna 0.
    # sticky="ew": Faz com que a barra de rolagem horizontal se expanda para
    #       preencher toda a largura (leste-oeste) do espaço disponível.
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

    # Configuração do layout do frame_tree para expandir com a janela.

    # frame_tree.rowconfigure: Configura as linhas do frame_tree
    #       para se ajustar ao redimensionamento.
    # row=0, weight=1: Define que a linha 0 pode se expandir
    #       proporcionalmente com peso 1.
    frame_tree.rowconfigure(0, weight=1)

    # frame_tree.columnconfigure: Configura as colunas do frame_tree
    #       para se ajustar ao redimensionamento.
    # column=0, weight=1: Define que a coluna 0 pode se expandir
    #       proporcionalmente com peso 1.
    frame_tree.columnconfigure(0, weight=1)

    # Criação de um rótulo para exibir o total arrecadado.

    # total_arrecadado_label: Cria um widget de rótulo para exibir o
    #       valor total arrecadado.
    # ttk.Label: Widget do Tkinter para exibir texto estático.
    # frame_principal: Define que o rótulo será filho do frame_principal.
    # text="Total Arrecadado: R$ 0.00": Define o texto inicial do rótulo,
    #       indicando que o valor arrecadado começa em R$ 0.00.
    # font=("Arial", 12, "bold"): Define a fonte usada no texto com
    #       estilo Arial, tamanho 12, e em negrito.
    total_arrecadado_label = ttk.Label(frame_principal,
                                       text="Total Arrecadado: R$ 0.00",
                                       font=("Arial", 12, "bold"))

    # Posicionamento do rótulo no layout.

    # grid(row=3, column=0, columnspan=6, pady=10): Posiciona o
    #       rótulo na linha 3, coluna 0, ocupando 6 colunas.
    # pady=10: Adiciona um espaçamento vertical de 10 pixels acima e abaixo do rótulo.
    total_arrecadado_label.grid(row=3, column=0, columnspan=6, pady=10)

    # Criação de uma lista para armazenar informações das reservas.

    # reservas: Variável que armazena uma lista vazia para controle
    #       dos dados das reservas carregadas.
    # Esta variável será usada para manipular e exibir as reservas no relatório.
    reservas = []

    # Define a função para carregar os dados e exibi-los na tabela.
    def carregar_dados():

        # Indica que a variável `reservas` será manipulada dentro do escopo da função.
        nonlocal reservas

        # Limpa a lista de reservas armazenadas.
        # reservas.clear(): Garante que os dados anteriores sejam
        #       removidos antes de carregar novos.
        reservas.clear()

        # Remove todas as linhas existentes na tabela do TreeView.
        # tree.get_children(): Retorna todos os identificadores de linhas na tabela.
        # tree.delete(i): Remove cada linha identificada por `i`.
        for i in tree.get_children():
            tree.delete(i)

        # Cria dicionários para mapear IDs às informações de sessões, filmes e salas.

        # sessoes: Dicionário que mapeia o ID da sessão para o documento completo da sessão.
        # obter_sessoes(db): Recupera todas as sessões do banco de dados.
        sessoes = {str(s["_id"]): s for s in obter_sessoes(db)}

        # filmes: Dicionário que mapeia o ID do filme para o título do filme.
        # obter_filmes(db): Recupera todos os filmes do banco de dados.
        filmes = {str(f["_id"]): f["titulo"] for f in obter_filmes(db)}

        # salas: Dicionário que mapeia o ID da sala para o nome da sala.
        # obter_salas(db): Recupera todas as salas do banco de dados.
        salas = {str(s["_id"]): s["nome"] for s in obter_salas(db)}

        # Inicializa a variável para calcular o total arrecadado.

        # total_arrecadado: Variável que acumula o valor total de todas as reservas.
        total_arrecadado = 0.0

        # Itera sobre todas as reservas obtidas do banco de dados.
        for reserva in obter_reservas(db):

            # Obtém os dados da sessão associada à reserva usando o ID da sessão.
            # sessoes.get(): Procura pelo ID da sessão no
            #       dicionário `sessoes` e retorna os dados completos da sessão.
            # Retorna um dicionário vazio se a sessão não for encontrada.
            sessao = sessoes.get(str(reserva["sessao_id"]), {})

            # Obtém o título do filme associado à sessão.
            # filmes.get(): Procura pelo ID do filme no dicionário `filmes` e
            #       retorna o título do filme.
            # Retorna "Desconhecido" se o filme não for encontrado.
            filme = filmes.get(str(sessao.get("filme_id")), "Desconhecido")

            # Obtém o nome da sala associada à sessão.
            # salas.get(): Procura pelo ID da sala no dicionário `salas` e
            #       retorna o nome da sala.
            # Retorna "Desconhecida" se a sala não for encontrada.
            sala = salas.get(str(sessao.get("sala_id")), "Desconhecida")

            # Calcula o valor total arrecadado pela reserva.
            # len(reserva["assentos_reservados"]): Conta o número de assentos reservados.
            # sessao.get("valor_ingresso", 0.0): Obtém o valor do ingresso da
            #       sessão, retornando 0.0 se não existir.
            valor_total = len(reserva["assentos_reservados"]) * sessao.get("valor_ingresso", 0.0)

            # Adiciona o valor total da reserva ao total acumulado.
            total_arrecadado += valor_total

            # Cria uma lista com os dados formatados da reserva para exibição na tabela.
            reserva_data = [
                f"{filme} - {sessao.get('data', '')} {sessao.get('hora', '')}",  # Sessão (Filme, Data e Hora)
                filme,  # Nome do filme
                sala,  # Nome da sala
                sessao.get("data", ""),  # Data da sessão
                sessao.get("hora", ""),  # Hora da sessão
                ", ".join(reserva["assentos_reservados"]),  # Lista de assentos reservados (formatada como string)
                f"R$ {valor_total:.2f}"  # Valor total formatado como moeda brasileira
            ]

            # Adiciona os dados formatados à lista global de reservas.
            reservas.append(reserva_data)

            # Insere os dados da reserva na tabela (TreeView).
            # tree.insert(): Adiciona uma nova linha na tabela com os valores de `reserva_data`.
            tree.insert("", "end", values=reserva_data)

        # Atualiza o rótulo do total arrecadado com o valor calculado.
        # total_arrecadado_label.config(): Altera o texto do rótulo para exibir o total acumulado.
        total_arrecadado_label.config(text=f"Total Arrecadado: R$ {total_arrecadado:.2f}")


    # Função para aplicar filtros dinamicamente na tabela de reservas.
    def aplicar_filtros(filtros):

        # Remove todas as linhas existentes no TreeView.
        # tree.get_children(): Retorna uma lista de todos os itens na tabela.
        # tree.delete(i): Remove cada item do TreeView.
        for i in tree.get_children():
            tree.delete(i)

        # Inicializa a variável que irá acumular o total
        #       arrecadado para as reservas filtradas.
        total_arrecadado_filtrado = 0.0

        # Itera sobre todas as reservas disponíveis na lista global `reservas`.
        for reserva in reservas:

            # Verifica se todos os filtros são compatíveis com os dados da reserva.
            # enumerate(filtros.keys()): Associa o índice da
            #       coluna (idx) à chave do filtro (key).
            # filtros[key].get().lower(): Obtém o valor do filtro em letras minúsculas.
            # reserva[idx].lower(): Obtém o valor correspondente da coluna da
            #       reserva em letras minúsculas.
            # Verifica se o valor do filtro está contido no valor da coluna.
            if all(filtros[key].get().lower() in reserva[idx].lower() for idx, key in enumerate(filtros.keys())):

                # Adiciona a reserva ao TreeView se passar pelos filtros.
                tree.insert("", "end", values=reserva)

                # Obtém o valor total da reserva da última coluna (index -1).
                # replace("R$", "").strip(): Remove o prefixo "R$" e espaços em branco.
                valor = reserva[-1].replace("R$", "").strip()

                # Converte o valor para float e adiciona ao total acumulado dos filtrados.
                total_arrecadado_filtrado += float(valor)

        # Atualiza o rótulo do total arrecadado com o valor acumulado
        #       para as reservas filtradas.
        # total_arrecadado_label.config(): Altera o texto exibido no rótulo.
        total_arrecadado_label.config(text=f"Total Arrecadado: R$ {total_arrecadado_filtrado:.2f}")


    # Função para obter os dados filtrados exibidos no TreeView.
    def obter_dados_filtrados():

        # Retorna uma lista de valores das linhas exibidas atualmente no TreeView.
        # tree.get_children(): Retorna todos os identificadores das linhas do TreeView.
        # tree.item(item_id)["values"]: Para cada linha, obtém os valores associados a ela.
        return [tree.item(item_id)["values"] for item_id in tree.get_children()]


    # Função para exportar os dados visíveis no TreeView para um arquivo Excel.
    def exportar_para_excel(dados):

        try:

            # Importa o módulo xlsxwriter para manipular arquivos Excel.
            import xlsxwriter

            # Define o nome do arquivo Excel que será gerado.
            arquivo = "Relatorio_Lucro.xlsx"

            # Cria uma nova pasta de trabalho (workbook) e uma
            #       planilha (worksheet) dentro dela.
            workbook = xlsxwriter.Workbook(arquivo)
            worksheet = workbook.add_worksheet("Relatório de Lucro")

            # Escreve os nomes das colunas no cabeçalho (linha 0) do arquivo Excel.
            for col_idx, col_nome in enumerate(colunas):

                # `col_idx`: Índice da coluna.
                # `col_nome`: Nome da coluna.
                worksheet.write(0, col_idx, col_nome)

            # Escreve os dados filtrados a partir da segunda linha do arquivo Excel.
            for row_idx, linha in enumerate(dados, start=1):

                # `row_idx`: Índice da linha no arquivo Excel, começando em 1.
                # `linha`: Dados da linha correspondente do TreeView.
                for col_idx, valor in enumerate(linha):

                    # `col_idx`: Índice da coluna dentro da linha.
                    # `valor`: Valor correspondente à célula atual.
                    worksheet.write(row_idx, col_idx, valor)

            # Fecha o arquivo Excel para garantir que ele seja salvo corretamente.
            workbook.close()

            # Exibe uma mensagem de sucesso ao usuário.
            messagebox.showinfo("Sucesso",
                                f"Relatório exportado para '{arquivo}' com sucesso!")

        except Exception as e:

            # Em caso de erro, exibe uma mensagem com a descrição do erro.
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")


    # Chama a função para carregar os dados no TreeView e inicializar o estado.
    carregar_dados()

    # Cria um botão para exportar os dados visíveis no TreeView para um arquivo Excel.
    # ttk.Button: Widget do Tkinter para criar botões.
    # frame_principal: Define o frame pai onde o botão será exibido.
    # text="Exportar para Excel": Define o texto exibido no botão.
    # command=lambda: exportar_para_excel(obter_dados_filtrados()):
    #       Define a ação executada ao clicar no botão.
    # - `obter_dados_filtrados()`: Obtém os dados atualmente exibidos no TreeView.
    # - `exportar_para_excel`: Função que exporta os dados filtrados para um arquivo Excel.
    # grid(row=4, column=0, columnspan=6, pady=10): Posiciona o botão na
    #       linha 4, ocupando 6 colunas e define o espaçamento vertical.
    ttk.Button(frame_principal,
               text="Exportar para Excel",
               command=lambda: exportar_para_excel(obter_dados_filtrados())
               ).grid(row=4, column=0, columnspan=6, pady=10)





# ============================================================
# JANELA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    """
    Verifica se o script está sendo executado diretamente e não importado como módulo.
    Abaixo está a configuração para conexão com o MongoDB.
    """

    # Importa o cliente do MongoDB.
    from pymongo import MongoClient

    # Configurar conexão com o MongoDB.
    try:

        # Tenta conectar ao servidor do MongoDB na porta e endereço padrão.
        client = MongoClient("mongodb://localhost:27017/")

        # Seleciona o banco de dados `cinema_db` para uso.
        # Substitua "cinema_db" pelo nome correto do banco de dados se necessário.
        db = client["cinema_db"]

    except Exception as e:

        # Captura qualquer erro que ocorrer durante a conexão com o MongoDB.
        # Exibe o erro e encerra o programa com status de erro.
        print(f"Erro ao conectar ao MongoDB: {e}")
        exit(1)

    # Criação da janela principal
    root = tk.Tk()

    # Define o título da janela principal
    # "Sistema de Reserva de Cinema - Completo" é o título que
    #       será exibido na barra de título da janela.
    root.title("Sistema de Reserva de Cinema - Completo")

    # Define a janela para iniciar maximizada
    # `root.state('zoomed')` faz a janela ocupar toda a tela ao abrir.
    root.state('zoomed')

    # Tenta carregar a imagem de fundo
    try:

        # Abre a imagem de fundo chamada "fundo.jpg"
        # Substitua "fundo.jpg" pelo caminho completo ou
        #       relativo da sua imagem de fundo
        imagem_fundo = Image.open("fundo.jpg")

        # Redimensiona a imagem para o tamanho exato da janela principal
        # `root.winfo_screenwidth()` retorna a largura da tela em pixels
        # `root.winfo_screenheight()` retorna a altura da tela em pixels
        imagem_fundo = imagem_fundo.resize(

            # Define as dimensões para o redimensionamento
            (root.winfo_screenwidth(), root.winfo_screenheight()),

            # Aplica o algoritmo LANCZOS para redimensionar a
            #       imagem com alta qualidade
            Image.Resampling.LANCZOS

        )

        # Converte a imagem redimensionada para um formato compatível com o Tkinter
        # `ImageTk.PhotoImage` cria um objeto de imagem que
        #       pode ser usado como fundo no `Canvas`
        imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)

    # Caso ocorra algum erro durante o carregamento ou processamento da imagem
    except Exception as e:

        # Exibe uma mensagem de erro no console com os detalhes do problema
        print(f"Erro ao carregar a imagem de fundo: {e}")

        # Define `imagem_fundo_tk` como `None` para evitar erros
        #       subsequentes caso a imagem não seja carregada
        imagem_fundo_tk = None

    # Cria um canvas para exibir a imagem de fundo
    # O canvas é uma área na janela onde objetos gráficos, como
    #       imagens e formas, podem ser desenhados
    canvas = tk.Canvas(

        # Define que o canvas será filho da janela principal (root)
        root,

        # Define a largura do canvas igual à largura da tela principal
        width=root.winfo_screenwidth(),

        # Define a altura do canvas igual à altura da tela principal
        height=root.winfo_screenheight()

    )

    # Adiciona o canvas na janela principal
    # `pack()` é usado para gerenciar o layout do canvas dentro da janela
    # `fill="both"` faz o canvas ocupar todo o espaço disponível,
    #       tanto horizontal quanto verticalmente
    # `expand=True` permite que o canvas expanda quando a
    #       janela for redimensionada
    canvas.pack(fill="both", expand=True)

    # Verifica se a imagem foi carregada corretamente
    # A variável `imagem_fundo_tk` será `None` caso o carregamento
    #       da imagem tenha falhado
    if imagem_fundo_tk:

        # Adiciona a imagem ao canvas
        # `create_image(x, y, image=imagem_fundo_tk, anchor="nw")` desenha a imagem no canvas:
        # - `x=0, y=0`: A posição inicial da imagem será no canto superior esquerdo do canvas
        # - `image=imagem_fundo_tk`: A imagem carregada no formato compatível com Tkinter
        # - `anchor="nw"`: Define que o ponto de ancoragem da imagem
        #       será o canto superior esquerdo ("northwest")
        canvas.create_image(0, 0, image=imagem_fundo_tk, anchor="nw")

    # Criação de um estilo personalizado para os widgets no Tkinter
    # Instancia um objeto de estilo que será usado para configurar os widgets
    style = ttk.Style()

    # Define o tema visual padrão para o estilo
    # "clam" é um tema moderno e simples fornecido pelo
    #       Tkinter que suporta personalizações
    style.theme_use('clam')

    # Define uma fonte padrão para todos os widgets
    # `fonte_padrao` especifica que a fonte será "Arial", tamanho 12
    fonte_padrao = ("Arial", 12)

    # Aplica a configuração de fonte padrão a todos os widgets
    # O ponto ('.') indica que o estilo será aplicado globalmente
    style.configure('.', font=fonte_padrao)

    # Configura um estilo personalizado para botões do tipo `ttk.Button`
    style.configure(
        "Custom.TButton",  # Nome do estilo (identificador) que será aplicado aos botões
        font=("Arial", 14, "bold"),  # Define a fonte como Arial, tamanho 14, em negrito
        background="#1a73e8",  # Cor de fundo do botão, definida em hexadecimal (um azul específico)
        foreground="white",  # Cor do texto dentro do botão (branca)
        borderwidth=2,  # Largura da borda do botão (2 pixels)
        padding=10,  # Padding interno, para adicionar espaçamento ao conteúdo do botão (10 pixels)
        relief="raised",  # Define o relevo do botão como "raised" (elevado), criando um efeito 3D
    )

    # Configura os estados dinâmicos do estilo personalizado "Custom.TButton"
    style.map(

        # Aplica as configurações ao estilo identificado como "Custom.TButton"
        "Custom.TButton",

        # Configurações de cores de fundo (background) para diferentes estados do botão
        background=[

            # Quando o botão está ativo (mouse hover), a cor muda para um azul mais escuro
            ("active", "#0c47a1"),

            # Quando o botão é pressionado, a cor muda para um azul ainda mais escuro
            ("pressed", "#0b3c87"),

        ],

        # Configurações de cores do texto (foreground) para diferentes estados do botão
        foreground=[

            # Quando o botão está ativo (mouse hover), o texto permanece branco
            ("active", "white"),

        ],
    )

    # Criação de um frame principal que será colocado sobre o canvas
    frame_main = ttk.Frame(

        # Define que o frame é filho da janela principal (root)
        root,

        # Adiciona 20 pixels de espaçamento interno (padding) em todos os lados do frame
        padding="20 20 20 20",

        # Aplica o estilo padrão do tema atual para frames
        style="TFrame"

    )

    # Posiciona o frame principal no centro da janela usando coordenadas relativas
    frame_main.place(

        # Define a posição horizontal relativa como 50% (centro horizontal da janela)
        relx=0.5,

        # Define a posição vertical relativa como 50% (centro vertical da janela)
        rely=0.5,

        # Define que o ponto de ancoragem é o centro do frame
        anchor="center"

    )

    # Adicionando título
    # Criação de um rótulo (label) para o título principal da aplicação
    titulo_label = ttk.Label(

        # Define que o rótulo será colocado dentro do frame_main
        frame_main,

        # Texto que será exibido no rótulo
        text="Sistema de Reserva de Cinema",

        font=("Arial", 28, "bold"),  # Configura a fonte do texto:
        # "Arial" é a família de fonte
        # 28 é o tamanho da fonte
        # "bold" aplica o estilo negrito

        # Centraliza o texto no rótulo (horizontal e verticalmente)
        anchor="center",

        # Define a cor do texto como preto
        foreground="black"

    )

    # Posiciona o rótulo no layout da interface usando o gerenciador de layout `grid`
    titulo_label.grid(

        # Posiciona o rótulo na linha 0 do grid
        row=0,

        # Posiciona o rótulo na coluna 0 do grid
        column=0,

        # Faz com que o rótulo ocupe 3 colunas no grid,
        #       centralizando-o em relação aos widgets
        columnspan=3,

        # Adiciona um espaçamento vertical de 30 pixels abaixo do rótulo
        # O primeiro valor (0) é o espaçamento acima, o
        #       segundo (30) é o espaçamento abaixo
        pady=(0, 30))

    # Configuração de botões com estilo customizado

    # botoes: Lista contendo tuplas com o texto a ser exibido no
    #       botão e a função a ser chamada ao clicar.
    # Cada tupla segue o formato: (texto_do_botao, funcao_associada).
    botoes = [
        ("Gerenciar Filmes", lambda: tela_gerenciar_filmes(root, db)),  # Botão para gerenciar filmes.
        ("Gerenciar Salas", lambda: tela_gerenciar_salas(root, db)),  # Botão para gerenciar salas.
        ("Gerenciar Sessões", lambda: tela_gerenciar_sessoes(root, db)),  # Botão para gerenciar sessões.
        ("Reservar Assentos", lambda: tela_reserva_assentos(root, db)),  # Botão para reservar assentos.
        ("Gerenciar Reservas", lambda: tela_gerenciar_reservas(root, db)),  # Botão para gerenciar reservas.
        ("Relatório de Lucro", lambda: tela_relatorio_lucro(root, db)),  # Botão para acessar o relatório de lucro.
    ]

    # Loop para criar e posicionar os botões dinamicamente
    for i, (texto, comando) in enumerate(botoes):

        # ttk.Button: Cria um botão estilizado.
        # frame_main: Define que o botão será filho do frame principal.
        # text=texto: Define o texto exibido no botão.
        # style="Custom.TButton": Aplica o estilo customizado definido anteriormente para botões.
        # command=comando: Associa o comando (função) a ser executado ao clicar no botão.
        ttk.Button(frame_main,
                   text=texto,
                   style="Custom.TButton",
                   command=comando).grid(

                                        # grid: Posiciona o botão no layout de grade.
                                        # row=1 + i // 3: Define a linha do botão com base no índice; 3 botões por linha.
                                        # column=i % 3: Define a coluna do botão com base no índice; começa uma nova linha após 3 botões.
                                        # padx=20, pady=20: Define espaçamento horizontal (20px) e vertical (20px) ao redor de cada botão.
                                        # sticky="ew": Faz o botão expandir horizontalmente para ocupar o espaço disponível.
                                        row=1 + i // 3, column=i % 3, padx=20, pady=20, sticky="ew")

    # Adicionando um rodapé na interface principal

    # rodape_label: Cria um rótulo (label) para exibir informações do rodapé.
    # ttk.Label: Widget de rótulo no Tkinter, usado para exibir texto estático.
    # frame_main: Define que o rótulo será filho do frame principal da interface.
    rodape_label = ttk.Label(frame_main,  # Especifica que o rótulo pertence ao frame principal.

                            # text="Desenvolvido por Clevison Santos": Define o texto exibido no rótulo.
                            text="Desenvolvido por Clevison Santos",

                            # font=("Arial", 10, "italic"): Configura a fonte do texto
                             #      como Arial, tamanho 10, em estilo itálico.
                            font=("Arial", 10, "italic"),

                            # anchor="center": Alinha o texto no centro do rótulo.
                            anchor="center",

                            # foreground="#808080": Define a cor do texto como cinza (#808080).
                            foreground="#808080", )

    # Posiciona o rótulo no layout de grade
    rodape_label.grid(

        # row=4: Posiciona o rótulo na linha 4 da grade.
        row=4,

        # column=0: Posiciona o rótulo na coluna 0.
        column=0,

        # columnspan=3: Faz com que o rótulo ocupe três colunas, centralizando-o
        #       em relação aos botões acima.
        columnspan=3,

        # pady=(30, 0): Adiciona espaçamento vertical de 30px na parte
        #       superior e nenhum na parte inferior.
        pady=(30, 0),

    )

    # Configuração do layout grid no frame principal

    # Configura o comportamento das colunas no grid
    for col in range(3):  # Itera pelas três colunas da interface principal

        # columnconfigure: Define configurações para cada coluna no frame_main
        # col: Identifica a coluna que está sendo configurada
        # weight=1: Permite que cada coluna se expanda igualmente ao
        #       redimensionar a janela
        frame_main.columnconfigure(col, weight=1)

    # Configura o comportamento das linhas no grid
    # rowconfigure: Define configurações para as linhas no frame_main
    # row=0: Configura a linha que contém o título principal
    frame_main.rowconfigure(0, weight=1)  # Linha do título

    # row=1: Configura a linha que contém a primeira linha de botões
    frame_main.rowconfigure(1, weight=1)  # Primeira linha de botões

    # row=2: Configura a linha que contém a segunda linha de botões
    frame_main.rowconfigure(2, weight=1)  # Segunda linha de botões

    # row=3: Configura a linha que contém o rodapé
    frame_main.rowconfigure(3, weight=1)  # Linha do rodapé

    # root.mainloop(): Mantém a aplicação em execução,
    #       aguardando eventos do usuário
    root.mainloop()