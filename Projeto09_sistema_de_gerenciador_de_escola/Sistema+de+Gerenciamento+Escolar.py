# ----------------------------------------------------------
# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
# ----------------------------------------------------------

# Importa a biblioteca Tkinter para criar a interface gráfica
import tkinter as tk

# Importa widgets específicos do Tkinter, incluindo:
# - ttk: Permite usar estilos modernos para widgets
# - messagebox: Exibe caixas de mensagem (alertas, confirmações, erros)
# - filedialog: Abre janelas para seleção de arquivos (salvar/abrir)
# - Toplevel: Cria novas janelas secundárias na interface gráfica
from tkinter import ttk, messagebox, filedialog, Toplevel

# Importa o módulo datetime para manipulação de datas e horários
import datetime

from PIL.ImageOps import expand
from Tools.scripts.make_ctype import values
# Importa a biblioteca PyMongo para conectar e interagir
#       com o banco de dados MongoDB
from pymongo import MongoClient

# Importa a classe ObjectId, usada para manipular identificadores únicos no MongoDB
from bson.objectid import ObjectId

import pandas as pd

# ----------------------------------------------------------
# CONFIGURAÇÃO DA CONEXÃO COM O BANCO DE DADOS MONGODB
# ----------------------------------------------------------

# Cria uma conexão com o servidor do MongoDB local (rodando na porta padrão 27017)
client = MongoClient('mongodb://localhost:27017/')

# Seleciona o banco de dados chamado "escola"
db = client['escola']

# ----------------------------------------------------------
# DEFINIÇÃO DAS COLEÇÕES DO BANCO DE DADOS
# ----------------------------------------------------------

# Acessa a coleção 'alunos', onde são armazenados os dados dos estudantes
col_alunos = db['alunos']

# Acessa a coleção 'professores', que armazena informações sobre os docentes
col_professores = db['professores']

# Acessa a coleção 'turmas', que contém os dados das turmas cadastradas
col_turmas = db['turmas']

# Acessa a coleção 'notas', onde são armazenadas as notas dos
#       alunos em diferentes disciplinas
col_notas = db['notas']

# Acessa a coleção 'faltas', que contém os registros de frequência dos alunos
col_faltas = db['faltas']



# Define a função para obter uma lista com todas as disciplinas
#       distintas cadastradas.
def obter_nomes_disciplinas():

    # Usa `distinct('disciplina')` para retornar apenas valores
    #       únicos do campo 'disciplina'.
    return col_professores.distinct('disciplina')



# Define a função para buscar um professor no banco de
#       dados pelo seu ID único.
def obter_professor_por_id(obj_id):

    # Converte o ID fornecido para `ObjectId` para garantir
    #       compatibilidade com o MongoDB.
    # `find_one({"_id": ...})` busca o primeiro documento onde o
    #       campo `_id` corresponda ao ID fornecido.
    return col_professores.find_one({"_id": ObjectId(obj_id)})


# Define a função para buscar uma turma no banco de
#       dados pelo seu ID único.
def obter_turma_por_id(obj_id):

    # Converte o ID fornecido para `ObjectId` para garantir
    #       compatibilidade com o MongoDB.
    # `find_one({"_id": ...})` busca o primeiro documento onde o
    #       campo `_id` corresponda ao ID fornecido.
    return col_turmas.find_one({"_id": ObjectId(obj_id)})


# Define a função para obter todos os turnos cadastrados ou
#       retornar um valor padrão caso não haja registros.
def obter_turnos():

    # Usa `distinct('turno')` para retornar apenas valores
    #       únicos do campo 'turno'.
    turnos = col_turmas.distinct('turno')

    # Se houver turnos cadastrados no banco, retorna a lista encontrada.
    # Caso contrário, retorna uma lista padrão contendo ["Manhã", "Tarde", "Noite"].
    return ["Manhã", "Tarde", "Noite"]



# Define a função para obter todas as séries cadastradas ou
#       retornar um valor padrão caso não haja registros.
def obter_series():

    # Usa `distinct('serie')` para retornar apenas valores únicos do campo 'serie'.
    series = col_turmas.distinct('serie')

    # Se houver séries cadastradas no banco, retorna a lista encontrada.
    # Caso contrário, retorna uma lista padrão contendo ["1ª", "2ª", "3ª", "4ª"].
    return ["1ª", "2ª", "3ª", "4ª", "5ª", "6ª", "7ª", "8ª"]


# Define a função para obter uma lista com os nomes dos
#       professores cadastrados.
def obter_nomes_professores():

    # Faz uma consulta no banco de dados e retorna todos os
    #       documentos da coleção 'professores'.
    # `find({})` busca todos os registros disponíveis.
    # `[p['nome'] for p in ...]` percorre os documentos retornados e
    #       extrai apenas o campo 'nome'.
    return [p['nome'] for p in col_professores.find({})]



# Define a função para obter uma lista com os nomes das
#       turmas cadastradas.
def obter_nomes_turmas():

    # Faz uma consulta no banco de dados e retorna todos os
    #       documentos da coleção 'turmas'.
    # `find({})` busca todos os registros disponíveis.
    # `[t['nome_turma'] for t in ...]` percorre os documentos
    #       retornados e extrai apenas o campo 'nome_turma'.
    return [t['nome_turma'] for t in col_turmas.find({})]


# Define a função para buscar um aluno no banco de dados
#       pelo seu ID único.
def obter_aluno_por_id(obj_id):

    # Converte o ID fornecido para `ObjectId` para garantir
    #       compatibilidade com o MongoDB.
    # `find_one({"_id": ...})` busca o primeiro documento onde o
    #       campo `_id` corresponda ao ID fornecido.
    return col_alunos.find_one({"_id": ObjectId(obj_id)})


def calcular_media_e_situacao(notas, total_faltas=0):

    """
    Essa função calcula a média das notas de um aluno e
            determina sua situação acadêmica.

    Regras de classificação:
    - Se o aluno tiver 10 ou mais faltas, é automaticamente reprovado por faltas.
    - Se não houver notas registradas, retorna 0 como média e a situação "Sem Notas".
    - Caso contrário, calcula a média e define a situação com base na seguinte lógica:
      - Média maior ou igual a 7 → "Aprovado"
      - Média entre 5 e 6.9 → "Recuperação"
      - Média abaixo de 5 → "Reprovado"

    Parâmetros:
    - notas (lista de float): Lista contendo as notas do aluno.
    - total_faltas (int, opcional): Número total de faltas do aluno (padrão: 0).

    Retorno:
    - (float, str): Retorna a média calculada e a situação do aluno.
    """

    # Se o número total de faltas for 10 ou mais, o aluno é
    #       automaticamente reprovado por faltas
    if total_faltas >= 10:

        # Calcula a média das notas apenas se houver notas, senão define como 0
        media = sum(notas) / len(notas) if notas else 0

        # Retorna a média e a situação "Reprovado por Faltas"
        return media, "Reprovado por Faltas"

    # Se não houver notas na lista, retorna média 0 e situação "Sem Notas"
    if len(notas) == 0:
        return 0, "Sem Notas"

    # Calcula a média das notas somando todos os valores e dividindo
    #       pela quantidade de notas
    media = sum(notas) / len(notas)

    # Define a situação do aluno com base na média obtida
    # Média maior ou igual a 7 → Aprovado
    if media >= 7:

        situacao = "Aprovado"

    # Média entre 5 e 6.9 → Recuperação
    elif media >= 5:

        situacao = "Recuperação"

    # Média abaixo de 5 → Reprovado
    else:

        situacao = "Reprovado"

    # Retorna a média calculada e a situação do aluno
    return media, situacao



# Define a função para centralizar uma janela na tela.
def centralizar_janela(janela, largura, altura):

    # Atualiza as tarefas pendentes do sistema de janelas para
    #       garantir que os cálculos sejam precisos.
    janela.update_idletasks()

    # Obtém a largura total da tela do usuário.
    largura_tela = janela.winfo_screenwidth()

    # Obtém a altura total da tela do usuário.
    altura_tela = janela.winfo_screenheight()

    # Calcula a posição X para centralizar a janela horizontalmente.
    # `(largura_tela - largura) // 2` coloca a janela no centro
    #       da tela em relação à largura.
    pos_x = (largura_tela - largura) // 2

    # Calcula a posição Y para centralizar a janela verticalmente.
    # `(altura_tela - altura) // 2` posiciona a janela no centro da
    #       tela em relação à altura.
    pos_y = (altura_tela - altura) // 2

    # Define a posição e o tamanho da janela usando a geometria
    #       formatada como "largura x altura + posição_x + posição_y".
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")



# ----------------------------------------------------------
# CLASSE DO SISTEMA DE GERENCIAMENTO ESCOLAR
# ----------------------------------------------------------

# Define a classe principal que gerencia o sistema escolar.
class GerenciamentoEscolar:

    # Método especial chamado automaticamente quando um objeto
    #       desta classe é criado.
    # O `__init__` é o construtor da classe, responsável por
    #       inicializar atributos e configurar a interface.
    # O parâmetro `root` representa a janela principal da aplicação Tkinter.
    def __init__(self, root):

        # Armazena a referência da janela principal dentro da classe.
        # Isso permite que possamos acessar e modificar a janela
        #       principal ao longo do código.
        self.root = root

        # Define o título da janela principal para "Sistema de Gerenciamento Escolar".
        # Esse título será exibido na barra de título da janela.
        self.root.title("Sistema de Gerenciamento Escolar")

        # Define a janela principal para abrir no modo maximizado automaticamente.
        # `state('zoomed')` expande a janela para ocupar toda a
        #       tela do usuário ao ser iniciada.
        # Esse método funciona no Windows e pode não ser suportado em
        #       alguns sistemas operacionais, como Linux e Mac.
        self.root.state('zoomed')

        # Cria um objeto de estilo (`ttk.Style()`) para
        #       personalizar a interface gráfica.
        style = ttk.Style()

        # Define o tema da interface como "clam".
        # O tema "clam" é um dos temas disponíveis no Tkinter e
        #       oferece uma aparência moderna.
        style.theme_use('clam')

        # Configura o estilo dos rótulos (`TLabel`).
        # Define a fonte como "Arial", tamanho 12.
        # Define a cor de fundo como `#f0f0f0`, um tom claro de cinza.
        style.configure('TLabel', font=('Arial', 12), background='#f0f0f0')

        # Configura o estilo dos botões (`TButton`).
        # Define a fonte como "Arial", tamanho 11.
        style.configure('TButton', font=('Arial', 11))

        # Configura o estilo dos campos de entrada (`TEntry`).
        # Define a fonte como "Arial", tamanho 11.
        style.configure('TEntry', font=('Arial', 11))

        # Configura o estilo dos menus suspensos (`TCombobox`).
        # Define a fonte como "Arial", tamanho 11.
        style.configure('TCombobox', font=('Arial', 11))

        # Configura o estilo das tabelas (`Treeview`), que são usadas
        #       para exibir listas e tabelas de dados.
        # Define a fonte como "Arial", tamanho 11.
        # Define a cor de fundo das células como branca (`background='white'`).
        # Define a cor do texto como preto (`foreground='black'`).
        style.configure('Treeview',
                        font=('Arial', 11),
                        background='white',
                        foreground='black')

        # Configura o estilo do cabeçalho das tabelas (`Treeview.Heading`).
        # Define a fonte como "Arial", tamanho 11, em negrito.
        # Define a cor de fundo do cabeçalho como `#d0d0d0`, um tom médio de cinza.
        style.configure('Treeview.Heading',
                        font=('Arial', 11, 'bold'),
                        background='#d0d0d0')

        # Define a cor de fundo de toda a janela principal (`self.root`).
        # A cor escolhida é `#f0f0f0`, um tom claro de cinza, para
        #       combinar com os rótulos (`TLabel`).
        self.root.configure(bg='#f0f0f0')

        # Cabeçalho
        # Cria um frame (área retangular) que servirá como cabeçalho na interface.
        # O cabeçalho será anexado à janela principal (`self.root`).
        # Define a cor de fundo como `#003366` (um azul escuro).
        header_frame = tk.Frame(self.root, bg='#003366')

        # Posiciona o frame do cabeçalho na parte superior da janela.
        # `fill='x'` faz com que o frame ocupe toda a largura disponível.
        header_frame.pack(fill='x')

        # Cria um rótulo (`Label`) dentro do cabeçalho para exibir o título do sistema.
        # O texto exibido será "Sistema de Gerenciamento Escolar".
        # A fonte utilizada será "Arial", tamanho 20, em negrito.
        # `fg='white'` define a cor do texto como branco.
        # `bg='#003366'` faz com que o fundo do rótulo tenha a mesma cor do cabeçalho.
        tk.Label(header_frame,
                 text="Sistema de Gerenciamento Escolar",
                 font=("Arial", 20, "bold"),
                 fg='white',
                 bg='#003366').pack(pady=10)

        # Cria o frame principal que conterá os elementos da interface.
        # `bg='#f0f0f0'` define a cor de fundo do frame como cinza claro.
        # `padx=20, pady=20` adiciona um espaçamento interno
        #       de 20 pixels nas bordas do frame.
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)

        # Posiciona o frame na interface.
        # `expand=True` faz com que o frame ocupe todo o espaço disponível na janela.
        # `fill='both'` permite que o frame seja expandido tanto
        #       na largura quanto na altura.
        main_frame.pack(expand=True, fill='both')

        # Cria a barra de menu principal.
        # `tk.Menu(self.root)` associa o menu à janela principal.
        menubar = tk.Menu(self.root)

        # Define a barra de menu como o menu principal da janela.
        # `self.root.config(menu=menubar)` configura a barra de menu na interface.
        self.root.config(menu=menubar)

        # Adiciona um item "Alunos" ao menu.
        # `label="Alunos"` define o nome do item no menu.
        # `command=self.abrir_janela_gerenciar_alunos` define a
        #       função chamada ao clicar nesse item.
        menubar.add_command(label="Alunos", command=self.abrir_janela_gerenciar_alunos)

        # Adiciona um item "Professores" ao menu.
        # `label="Professores"` define o nome do item no menu.
        # `command=self.abrir_janela_gerenciar_professores` define a
        #       função chamada ao clicar nesse item.
        menubar.add_command(label="Professores", command=self.abrir_janela_gerenciar_professores)

        # Adiciona um item "Turmas" ao menu.
        # `label="Turmas"` define o nome do item no menu.
        # `command=self.abrir_janela_gerenciar_turmas` define a função
        #       chamada ao clicar nesse item.
        menubar.add_command(label="Turmas", command=self.abrir_janela_gerenciar_turmas)

        # Adiciona um item "Notas" ao menu.
        # `label="Notas"` define o nome do item no menu.
        # `command=self.abrir_janela_notas` define a função chamada ao clicar nesse item.
        menubar.add_command(label="Notas", command=self.abrir_janela_notas)

        # Adiciona um item "Faltas" ao menu.
        # `label="Faltas"` define o nome do item no menu.
        # `command=self.abrir_janela_faltas` define a função chamada ao clicar nesse item.
        menubar.add_command(label="Faltas", command=self.abrir_janela_faltas)

        # Adiciona um item "Relatórios" ao menu.
        # `label="Relatórios"` define o nome do item no menu.
        # `command=self.abrir_janela_relatorio_geral` define a função
        #       chamada ao clicar nesse item.
        menubar.add_command(label="Relatórios", command=self.abrir_janela_relatorio_geral)

        # Adiciona um item "Sair" ao menu.
        # `label="Sair"` define o nome do item no menu.
        # `command=self.root.destroy` fecha a aplicação ao clicar nesse item.
        menubar.add_command(label="Sair", command=self.root.destroy)

        # Cria um rótulo de texto dentro do frame principal (`main_frame`).
        # `text="Bem-vindo ao Sistema de Gerenciamento Escolar"` define o texto exibido no rótulo.
        # `font=("Arial", 16, "bold")` define a fonte como Arial, tamanho 16, em negrito.
        # `bg='#f0f0f0'` define a cor de fundo como cinza claro para combinar com o layout.
        # `.pack(pady=20)` posiciona o rótulo e adiciona um espaçamento
        #       vertical de 20 pixels abaixo dele.
        tk.Label(main_frame,
                 text="Bem-vindo ao Sistema de Gerenciamento Escolar",
                 font=("Arial", 16, "bold"),
                 bg='#f0f0f0').pack(pady=20)

        # Cria um segundo rótulo de texto dentro do frame principal (`main_frame`).
        # `text="Use o menu superior para acessar as funcionalidades."`
        #       define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte como Arial, tamanho 14.
        # `bg='#f0f0f0'` mantém a cor de fundo como cinza claro para manter a identidade visual.
        # `.pack(pady=10)` posiciona o rótulo e adiciona um espaçamento
        #       vertical de 10 pixels abaixo dele.
        tk.Label(main_frame,
                 text="Use o menu superior para acessar as funcionalidades.",
                 font=("Arial", 14),
                 bg='#f0f0f0').pack(pady=10)

        # Cria um frame (`footer_frame`) que servirá como rodapé da interface.
        # `self.root` define que o frame será adicionado à janela principal.
        # `bg='#003366'` define a cor de fundo do rodapé como azul escuro.
        footer_frame = tk.Frame(self.root, bg='#003366')

        # Posiciona o frame do rodapé na parte inferior da janela.
        # `fill='x'` faz com que o rodapé ocupe toda a largura da tela.
        # `side='bottom'` posiciona o rodapé na parte inferior da interface.
        footer_frame.pack(fill='x', side='bottom')

        # Cria um rótulo de texto dentro do rodapé (`footer_frame`).
        # `text="© 2025 - Sua Escola - Todos os direitos reservados."`
        #       define o texto exibido no rodapé.
        # `font=("Arial", 10)` define a fonte como Arial, tamanho 10.
        # `fg='white'` define a cor do texto como branca para contrastar
        #       com o fundo azul escuro.
        # `bg='#003366'` mantém a cor de fundo do rótulo igual à do rodapé.
        # `.pack(pady=5)` adiciona um espaçamento vertical de 5 pixels para
        #       evitar que o texto fique colado nas bordas.
        tk.Label(footer_frame,
                 text="© 2025 - Sua Escola - Todos os direitos reservados.",
                 font=("Arial", 10),
                 fg='white',
                 bg='#003366').pack(pady=5)


    # ---------- Gerenciamento de Alunos ----------
    # Define um método para abrir a janela de gerenciamento de alunos.
    def abrir_janela_gerenciar_alunos(self):

        # Cria uma nova janela (`Toplevel`) que será independente da
        #       janela principal (`self.root`).
        # Essa janela permite interações sem bloquear a interface principal.
        janela = Toplevel(self.root)

        # Define o título da nova janela como "Gerenciamento de Alunos".
        # Esse título será exibido na barra de título da janela.
        janela.title("Gerenciamento de Alunos")

        # Maximiza automaticamente a nova janela para ocupar toda a tela do usuário.
        # `state('zoomed')` faz com que a janela inicie expandida,
        #       semelhante ao modo de tela cheia.
        janela.state('zoomed')

        # Define a cor de fundo da nova janela como cinza claro (`#f0f0f0`).
        # Isso mantém a identidade visual do sistema e melhora a legibilidade.
        janela.configure(bg='#f0f0f0')

        # Cria um frame (`top_frame`) dentro da janela para
        #       organizar os filtros de busca.
        # `janela` define que este frame será colocado dentro da
        #       janela de gerenciamento de alunos.
        # `bg='#f0f0f0'` define a cor de fundo como cinza claro, para
        #       manter o padrão visual do sistema.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       entre este frame e os outros elementos.
        top_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o `top_frame` na parte superior da janela.
        # `fill='x'` faz com que o frame ocupe toda a largura disponível,
        #       garantindo alinhamento.
        top_frame.pack(fill='x')

        # Cria um rótulo (`Label`) dentro do `top_frame` para indicar o campo de filtro por nome.
        # `text="Filtrar por Nome:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=0, padx=5, sticky='e')` posiciona o rótulo na linha 0, coluna 0,
        #       adicionando um espaçamento horizontal (`padx=5`) e alinhando-o à direita (`sticky='e'`).
        ttk.Label(top_frame,
                  text="Filtrar por Nome:").grid(row=0, column=0, padx=5, sticky='e')

        # Cria um campo de entrada (`Entry`) onde o usuário poderá
        #       digitar o nome do aluno para filtrar.
        # `top_frame` define que este campo será colocado dentro do frame superior.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        filtro_nome = ttk.Entry(top_frame, width=30)

        # Posiciona o campo de entrada na mesma linha (`row=0`), mas
        #       na próxima coluna (`column=1`).
        # `padx=5` adiciona um pequeno espaçamento horizontal para evitar
        #       que os elementos fiquem colados.
        filtro_nome.grid(row=0, column=1, padx=5)

        # Cria um rótulo (`Label`) dentro do `top_frame` para indicar o
        #       campo de filtro por matrícula.
        # `text="Filtrar por Matrícula:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=2, padx=5, sticky='e')` posiciona o rótulo na linha 0, coluna 2,
        #       adicionando um espaçamento horizontal (`padx=5`) e alinhando-o à direita (`sticky='e'`).
        ttk.Label(top_frame,
                  text="Filtrar por Matrícula:").grid(row=0, column=2, padx=5, sticky='e')

        # Cria um campo de entrada (`Entry`) onde o usuário poderá
        #       digitar a matrícula do aluno para filtrar.
        # `top_frame` define que este campo será colocado dentro do frame superior.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        filtro_matricula = ttk.Entry(top_frame, width=30)

        # Posiciona o campo de entrada na mesma linha (`row=0`), mas
        #       na próxima coluna (`column=3`).
        # `padx=5` adiciona um pequeno espaçamento horizontal para evitar
        #       que os elementos fiquem colados.
        filtro_matricula.grid(row=0, column=3, padx=5)

        # Cria um rótulo (`Label`) dentro do `top_frame` para indicar o
        #       campo de filtro por turma.
        # `text="Filtrar por Turma:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=4, padx=5, sticky='e')` posiciona o rótulo na linha 0, coluna 4,
        #       adicionando um espaçamento horizontal (`padx=5`) e alinhando-o à direita (`sticky='e'`).
        ttk.Label(top_frame,
                  text="Filtrar por Turma:").grid(row=0, column=4, padx=5, sticky='e')

        # Cria uma caixa de seleção (`Combobox`) onde o usuário pode
        #       escolher uma turma para filtrar.
        # `top_frame` define que este combobox será colocado dentro do frame superior.
        # `values=obter_nomes_turmas()` define a lista de opções disponíveis,
        #       obtida da função `obter_nomes_turmas()`.
        # `width=30` define a largura da caixa de seleção para caber até 30 caracteres.
        # `state="readonly"` impede que o usuário digite valores manualmente,
        #       permitindo apenas a seleção de uma opção existente.
        filtro_turma = ttk.Combobox(top_frame,
                                    values=obter_nomes_turmas(),
                                    width=30,
                                    state="readonly")

        # Posiciona a caixa de seleção na mesma linha (`row=0`), mas
        #       na próxima coluna (`column=5`).
        # `padx=5` adiciona um pequeno espaçamento horizontal para
        #       evitar que os elementos fiquem colados.
        filtro_turma.grid(row=0, column=5, padx=5)


        # Define uma função para atualizar a lista de alunos na interface.
        def atualizar_lista_alunos():

            # Cria um dicionário vazio (`query`) que armazenará os critérios de
            #       filtragem para a busca no banco de dados.
            query = {}

            # Verifica se há um valor digitado no campo de filtro por nome.
            # Se houver, adiciona um critério de busca que verifica se o nome contém esse valor.
            # `"$regex": filtro_nome.get()` aplica uma busca textual
            #       utilizando expressões regulares.
            # `"$options": "i"` torna a busca **case-insensitive**, ou seja, não
            #       diferencia maiúsculas de minúsculas.
            if filtro_nome.get():
                query["nome"] = {"$regex": filtro_nome.get(), "$options": "i"}

            # Verifica se há um valor digitado no campo de filtro por matrícula.
            # Se houver, adiciona um critério de busca que verifica
            #       se a matrícula contém esse valor.
            if filtro_matricula.get():
                query["matricula"] = {"$regex": filtro_matricula.get()}

            # Verifica se há uma turma selecionada no combobox de filtro de turma.
            # Se houver, adiciona um critério de busca para filtrar apenas
            #       alunos dessa turma específica.
            if filtro_turma.get():
                query["turma"] = filtro_turma.get()

            # Percorre todos os itens atualmente exibidos na árvore (`tree`).
            # `.get_children()` retorna todos os nós (linhas) existentes na tabela.
            # `.delete(i)` remove cada um deles, limpando a tabela antes de atualizar os dados.
            for i in tree.get_children():
                tree.delete(i)

            # Consulta o banco de dados MongoDB (`col_alunos.find(query)`) utilizando os
            #       critérios definidos no dicionário `query`.
            # Para cada aluno encontrado, insere uma nova linha (`item`) na tabela (`tree`).
            for aluno in col_alunos.find(query):
                tree.insert("",
                            "end",
                            values=(str(aluno["_id"]),  # Converte o ID do aluno para string para exibição.
                                    aluno["nome"],  # Exibe o nome do aluno.
                                    aluno["matricula"],  # Exibe a matrícula do aluno.
                                    aluno["turma"]))  # Exibe a turma do aluno.


        # Cria um botão que, ao ser clicado, aplica os filtros e atualiza a lista de alunos.
        # `top_frame` define que o botão será colocado dentro do frame superior.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=atualizar_lista_alunos` associa a ação de atualizar a
        #       lista de alunos ao clique no botão.
        # `.grid(row=0, column=6, padx=5)` posiciona o botão na linha 0,
        #       coluna 6, adicionando um espaçamento horizontal de 5 pixels.
        ttk.Button(top_frame,
                   text="Filtrar",
                   command=atualizar_lista_alunos).grid(row=0, column=6, padx=5)

        # Cria um botão que, ao ser clicado, limpa os filtros e recarrega a
        #       lista de alunos sem filtros aplicados.
        # `text="Limpar Filtros"` define o texto exibido no botão.
        # `command=lambda: [...]` usa uma função lambda para executar
        #       múltiplos comandos ao mesmo tempo.
        # `filtro_nome.delete(0, 'end')` limpa o campo de entrada de nome,
        #       removendo qualquer texto digitado.
        # `filtro_matricula.delete(0, 'end')` limpa o campo de entrada de
        #       matrícula, removendo qualquer texto digitado.
        # `filtro_turma.set('')` redefine a seleção do combobox de turma
        #       para vazio, removendo qualquer filtro aplicado.
        # `atualizar_lista_alunos()` chama a função que recarrega a lista de
        #       alunos, agora sem nenhum filtro ativo.
        # `.grid(row=0, column=7, padx=5)` posiciona o botão na linha 0,
        #       coluna 7, com um espaçamento horizontal de 5 pixels.
        ttk.Button(top_frame,
                   text="Limpar Filtros",
                   command=lambda: [filtro_nome.delete(0, 'end'),
                                    filtro_matricula.delete(0, 'end'),
                                    filtro_turma.set(''),
                                    atualizar_lista_alunos()]).grid(row=0, column=7, padx=5)

        # Cria um frame (`tree_frame`) que servirá como contêiner
        #       para a tabela de alunos.
        # `janela` define que este frame será colocado dentro da
        #       janela de gerenciamento de alunos.
        # `bg='#f0f0f0'` define a cor de fundo como cinza claro para
        #       manter a identidade visual do sistema.
        tree_frame = tk.Frame(janela, bg='#f0f0f0')

        # Posiciona o `tree_frame` na interface.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do frame.
        # `fill='both'` faz com que o frame ocupe toda a largura e altura disponíveis.
        # `expand=True` permite que o frame se expanda caso a janela seja redimensionada.
        tree_frame.pack(pady=10, fill='both', expand=True)

        # Define as colunas que serão exibidas na tabela (`Treeview`).
        # `("id", "Nome", "Matrícula", "Turma")` especifica as colunas da tabela:
        # - `"id"`: identificador único do aluno.
        # - `"Nome"`: nome completo do aluno.
        # - `"Matrícula"`: número de matrícula do aluno.
        # - `"Turma"`: turma à qual o aluno pertence.
        colunas = ("id", "Nome", "Matrícula", "Turma")

        # Cria a tabela (`Treeview`) dentro do `tree_frame` para exibir a lista de alunos.
        # `columns=colunas` define as colunas que serão exibidas na tabela.
        # `show="headings"` exibe apenas os cabeçalhos das
        #       colunas, ocultando a coluna padrão do índice.
        # `selectmode="browse"` permite que o usuário selecione apenas uma linha por vez.
        tree = ttk.Treeview(tree_frame,
                            columns=colunas,
                            show="headings",
                            selectmode="browse")

        # Percorre a lista de colunas definidas anteriormente para
        #       configurar os cabeçalhos da tabela.
        for col in colunas:

            # Define o título do cabeçalho para cada coluna.
            # `tree.heading(col, text=col)` faz com que o nome da coluna
            #       apareça no topo da tabela.
            tree.heading(col, text=col)

            # Define a largura da coluna na tabela (`Treeview`).
            # `width=220` define uma largura fixa de 220 pixels para cada coluna.
            tree.column(col, width=220)

        # Posiciona a tabela (`tree`) dentro do frame (`tree_frame`).
        # `fill='both'` faz com que a tabela ocupe toda a largura e
        #       altura disponíveis dentro do frame.
        # `expand=True` permite que a tabela se expanda ao redimensionar a janela.
        tree.pack(fill='both', expand=True)

        # Chama a função `atualizar_lista_alunos()` para carregar os
        #       dados dos alunos e exibi-los na tabela.
        atualizar_lista_alunos()


        # Define uma função para exibir o boletim do aluno quando o
        #       usuário interagir com a tabela.
        # O evento (`event`) será acionado ao clicar duas vezes em um aluno da lista.
        def exibir_boletim_aluno(event):

            # Obtém o identificador do item selecionado na tabela (`Treeview`).
            # `tree.focus()` retorna o identificador da linha atualmente selecionada.
            selecionado = tree.focus()

            # Verifica se algum aluno foi selecionado antes de prosseguir.
            # Se `selecionado` estiver vazio, a função simplesmente retorna sem fazer nada.
            if not selecionado:
                return

            # Obtém os valores da linha selecionada na tabela.
            # `tree.item(selecionado, "values")` retorna uma tupla
            #       com os valores da linha.
            valores = tree.item(selecionado, "values")

            # Desempacota os valores da tupla para obter os dados do aluno.
            # `aluno_id`: identificador único do aluno no banco de dados.
            # `aluno_nome`: nome do aluno.
            # `_`: ignoramos o terceiro valor, que seria a matrícula,
            #       pois não será usado aqui.
            # `aluno_turma`: turma do aluno.
            aluno_id, aluno_nome, _, aluno_turma = valores

            # Cria uma nova janela (`Toplevel`) para exibir o boletim do aluno.
            # `janela` define que essa nova janela será filha da
            #       janela de gerenciamento de alunos.
            boletim_win = Toplevel(janela)

            # Define o título da nova janela como "Boletim do Aluno: Nome do Aluno".
            # O `f"Boletim do Aluno: {aluno_nome}"` insere dinamicamente o
            #       nome do aluno no título.
            boletim_win.title(f"Boletim do Aluno: {aluno_nome}")

            # Maximiza automaticamente a nova janela do boletim para
            #       ocupar toda a tela do usuário.
            # `state('zoomed')` faz com que a janela inicie expandida,
            #       semelhante ao modo de tela cheia.
            boletim_win.state('zoomed')

            # Define a cor de fundo da nova janela do boletim como cinza claro (`#f0f0f0`).
            # Isso mantém a identidade visual do sistema e melhora a legibilidade.
            boletim_win.configure(bg='#f0f0f0')

            # Cria um frame (`boletim_frame`) dentro da janela do boletim
            #       para organizar os elementos internos.
            # `boletim_win` define que este frame será colocado dentro da janela do boletim.
            # `bg='#f0f0f0'` define a cor de fundo do frame para manter a padronização visual.
            # `padx=20` adiciona um espaçamento horizontal interno de 20 pixels dentro do frame.
            # `pady=20` adiciona um espaçamento vertical interno de 20 pixels dentro do frame.
            boletim_frame = tk.Frame(boletim_win, bg='#f0f0f0', padx=20, pady=20)

            # Posiciona o `boletim_frame` dentro da janela do boletim.
            # `fill='both'` faz com que o frame ocupe toda a largura e
            #       altura disponíveis na janela.
            # `expand=True` permite que o frame se expanda automaticamente
            #       caso a janela seja redimensionada.
            boletim_frame.pack(fill='both', expand=True)

            # Cria um rótulo (`Label`) dentro do `boletim_frame` para exibir o
            #       nome do aluno e sua turma.
            # `text=f"Aluno: {aluno_nome}    Turma: {aluno_turma}"` exibe
            #       dinamicamente o nome do aluno e sua turma.
            # `font=("Arial", 14, "bold")` define o estilo do texto
            #       como Arial, tamanho 14, em negrito.
            # `.pack(pady=10)` adiciona um espaçamento vertical de 10 pixels
            #       acima e abaixo do rótulo.
            ttk.Label(boletim_frame,
                      text=f"Aluno: {aluno_nome}    Turma: {aluno_turma}",
                      font=("Arial", 14, "bold")).pack(pady=10)

            # Cria um frame (`notas_frame`) dentro do `boletim_frame` para
            #       organizar a tabela de notas do aluno.
            # `boletim_frame` define que este frame será colocado
            #       dentro do frame principal do boletim.
            # `bg='#f0f0f0'` define a cor de fundo do frame para
            #       manter a padronização visual.
            notas_frame = tk.Frame(boletim_frame, bg='#f0f0f0')

            # Posiciona o `notas_frame` dentro do `boletim_frame`.
            # `fill='both'` faz com que o frame ocupe toda a largura e
            #       altura disponíveis.
            # `expand=True` permite que o frame se expanda automaticamente ao
            #       redimensionar a janela.
            notas_frame.pack(fill='both', expand=True)

            # Define as colunas da tabela que exibirá o boletim do aluno.
            # Cada item na tupla representa um cabeçalho da tabela:
            # - "Disciplina": nome da disciplina do aluno.
            # - "1º Bim", "2º Bim", "3º Bim", "4º Bim": notas dos quatro bimestres.
            # - "Média": média das notas do aluno.
            # - "Situação": status do aluno (Aprovado, Reprovado, Recuperação).
            # - "Faltas": quantidade total de faltas na disciplina.
            colunas_boletim = ("Disciplina", "1º Bim", "2º Bim", "3º Bim", "4º Bim", "Média", "Situação", "Faltas")

            # Cria uma tabela (`Treeview`) dentro do `notas_frame` para exibir o boletim do aluno.
            # `columns=colunas_boletim` define as colunas que serão exibidas na tabela.
            # `show="headings"` exibe apenas os cabeçalhos das colunas,
            #       ocultando a coluna de índice padrão.
            tree_boletim = ttk.Treeview(notas_frame,
                                        columns=colunas_boletim,
                                        show="headings")

            # Percorre a lista de colunas do boletim para configurar os
            #       cabeçalhos e larguras das colunas.
            for c in colunas_boletim:

                # Define o título do cabeçalho para cada coluna.
                # `tree_boletim.heading(c, text=c)` faz com que o nome da
                #       coluna apareça no topo da tabela.
                tree_boletim.heading(c, text=c)

                # Define a largura da coluna na tabela (`Treeview`).
                # `width=120` define uma largura fixa de 120 pixels para cada coluna.
                tree_boletim.column(c, width=120)

            # Posiciona a tabela (`tree_boletim`) dentro do `notas_frame`.
            # `fill='both'` faz com que a tabela ocupe toda a largura e
            #       altura disponíveis dentro do frame.
            # `expand=True` permite que a tabela se expanda ao
            #       redimensionar a janela.
            tree_boletim.pack(fill='both', expand=True)

            # Percorre todas as notas do aluno no banco de dados e exibe
            #       apenas as disciplinas com notas cadastradas.
            # `col_notas.find({"id_aluno": ObjectId(aluno_id)})` busca
            #       todas as notas associadas ao aluno selecionado.
            for nota in col_notas.find({"id_aluno": ObjectId(aluno_id)}):

                # Calcula o total de faltas do aluno na disciplina específica.
                # `col_faltas.find(...)` retorna todas as faltas do aluno na disciplina correspondente.
                # `sum(f.get("quantidade_faltas", 0) for f in ...)` soma todas as faltas registradas.
                total_faltas = sum(f.get("quantidade_faltas", 0)
                                   for f in col_faltas.find({"id_aluno": ObjectId(aluno_id),
                                                             "disciplina": nota["disciplina"]}))

                # Obtém a situação do aluno na disciplina (Aprovado, Reprovado, etc.).
                situacao = nota["situacao"]

                # Se o aluno tiver 10 ou mais faltas, ele será reprovado por
                #       faltas, independentemente da nota.
                if total_faltas >= 10:
                    situacao = "Reprovado por Faltas"

                # Formata a média para exibição com duas casas decimais.
                # `f"{nota['media']:.2f}"` converte a média para string e
                #       mantém duas casas decimais.
                # Se `nota["media"]` for `None`, exibe "0.00" como valor padrão.
                media_formatada = f"{nota['media']:.2f}" if nota.get("media") is not None else "0.00"

                # Insere uma nova linha na tabela (`tree_boletim`) com os
                #       dados do boletim do aluno.
                # Os valores são organizados conforme a ordem das colunas
                #       definidas anteriormente.
                tree_boletim.insert("", "end", values=(
                    nota["disciplina"],  # Nome da disciplina
                    nota["bimestre_1"],  # Nota do 1º bimestre
                    nota["bimestre_2"],  # Nota do 2º bimestre
                    nota["bimestre_3"],  # Nota do 3º bimestre
                    nota["bimestre_4"],  # Nota do 4º bimestre
                    media_formatada,  # Média final formatada com duas casas decimais
                    situacao,  # Situação do aluno na disciplina (Aprovado, Reprovado, etc.)
                    total_faltas  # Total de faltas registradas na disciplina
                ))

        # Associa a ação de duplo clique na tabela (`Treeview`)
        #       para exibir o boletim do aluno.
        # `"<Double-1>"` representa um clique duplo do mouse.
        # Quando o usuário der um duplo clique em uma linha da tabela, a
        #       função `exibir_boletim_aluno` será chamada.
        tree.bind("<Double-1>", exibir_boletim_aluno)

        # Cria um frame (`btn_frame`) dentro da `janela` para armazenar os botões de ação.
        # `bg='#f0f0f0'` define a cor de fundo do frame como cinza claro,
        #       para manter a identidade visual do sistema.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e
        #       abaixo do frame para melhor organização dos botões.
        btn_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o `btn_frame` dentro da `janela`.
        # Como nenhum argumento de `fill` ou `expand` foi passado, ele será
        #       centralizado automaticamente na interface.
        btn_frame.pack()


        # Define a função `adicionar_aluno()` que cria uma nova janela
        #       para cadastrar um aluno.
        def adicionar_aluno():

            # Cria uma nova janela (`Toplevel`) filha da janela principal (`janela`).
            # Essa janela será usada para inserir os dados do aluno.
            win = Toplevel(janela)

            # Define o título da nova janela como "Adicionar Aluno".
            win.title("Adicionar Aluno")

            # Centraliza a nova janela na tela com largura de 800
            #       pixels e altura de 500 pixels.
            # A função `centralizar_janela(win, 800, 500)` calcula
            #       automaticamente a posição para exibição centralizada.
            centralizar_janela(win, 800, 500)

            # Define a janela como uma janela transitória da `janela` principal.
            # Isso significa que a janela principal permanecerá ativa,
            #       mas a nova janela ficará acima dela.
            win.transient(janela)

            # Impede que o usuário interaja com outras janelas até que a
            #       ação na janela atual seja concluída.
            # `grab_set()` captura os eventos do mouse e teclado
            #       exclusivamente para esta janela.
            win.grab_set()

            # Cria um `LabelFrame` dentro da janela `win`, funcionando como um
            #       contêiner para os campos do formulário.
            # `text="Cadastro de Aluno"` define um título para o `LabelFrame`.
            # `padding=(20,10)` adiciona um espaçamento interno de 20 pixels na
            #       horizontal e 10 pixels na vertical.
            form_frame = ttk.LabelFrame(win,
                                        text="Cadastro de Aluno",
                                        padding=(20, 10))

            # Posiciona o `form_frame` dentro da janela `win`.
            # `fill='both'` faz com que ele ocupe toda a largura e altura disponíveis dentro da janela.
            # `expand=True` permite que ele se expanda caso a janela seja redimensionada.
            # `padx=20, pady=20` adiciona espaçamento externo de 20 pixels ao redor do `form_frame`.
            form_frame.pack(fill='both', expand=True, padx=20, pady=20)

            # Define os campos do formulário como uma lista de tuplas.
            # Cada tupla contém uma string com o nome do campo e uma
            #       string vazia representando o valor inicial.
            campos = [("Nome:", ""),
                      ("Data Nascimento (AAAA-MM-DD):", ""),
                      ("CPF:", ""),
                      ("Matrícula:", ""),
                      ("Endereço:", ""),
                      ("Telefone:", ""),
                      ("E-mail:", ""),
                      ("Turma:", "")]

            # Cria um dicionário (`entries`) para armazenar os widgets
            #       de entrada dos dados do aluno.
            entries = {}

            # Percorre a lista de campos do formulário para criar rótulos (`Label`) e
            #       caixas de entrada (`Entry` ou `Combobox`).
            # `enumerate(campos)` fornece o índice (`i`) e os valores da
            #       tupla (`lbl`, `_`), onde `lbl` é o nome do campo.
            for i, (lbl, _) in enumerate(campos):

                # Cria um rótulo (`Label`) dentro do `form_frame` com o texto
                #       correspondente ao nome do campo (`lbl`).
                # `row=i` posiciona o rótulo na linha correspondente ao índice `i`.
                # `column=0` coloca o rótulo na primeira coluna da grade do formulário.
                # `sticky='e'` alinha o rótulo à direita para ficar próximo ao campo de entrada.
                # `padx=10, pady=5` adiciona espaçamento horizontal e vertical para melhor organização.
                ttk.Label(form_frame,
                          text=lbl).grid(row=i, column=0, sticky='e', padx=10, pady=5)

                # Verifica se o campo atual é "Turma:", pois ele precisa de
                #       uma `Combobox` em vez de uma `Entry`.
                if lbl == "Turma:":

                    # Cria um menu suspenso (`Combobox`) para a seleção de turmas disponíveis.
                    # `values=obter_nomes_turmas()` preenche a lista com os nomes das turmas cadastradas.
                    # `width=30` define a largura da `Combobox`.
                    # `state="readonly"` impede que o usuário digite valores manuais,
                    #       permitindo apenas a seleção.
                    cb = ttk.Combobox(form_frame,
                                      values=obter_nomes_turmas(),
                                      width=30,
                                      state="readonly")

                    # Posiciona a `Combobox` na mesma linha do rótulo correspondente.
                    # `row=i` posiciona na linha correta do formulário.
                    # `column=1` coloca o campo na segunda coluna da grade do formulário.
                    # `sticky='w'` alinha o campo à esquerda.
                    # `padx=10, pady=5` adiciona espaçamento horizontal e vertical.
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena a `Combobox` no dicionário `entries` para acesso posterior.
                    entries[lbl] = cb

                else:

                    # Cria um campo de entrada (`Entry`) para os outros dados do
                    #       aluno (Nome, CPF, Matrícula, etc.).
                    # `width=30` define a largura da caixa de entrada.
                    ent = ttk.Entry(form_frame, width=30)

                    # Posiciona a `Entry` na mesma linha do rótulo correspondente.
                    # `row=i` posiciona na linha correta do formulário.
                    # `column=1` coloca o campo na segunda coluna da grade do formulário.
                    # `sticky='w'` alinha o campo à esquerda.
                    # `padx=10, pady=5` adiciona espaçamento horizontal e vertical.
                    ent.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena a `Entry` no dicionário `entries` para acesso posterior.
                    entries[lbl] = ent

            # Define a função `salvar_aluno()`, responsável por validar e
            #       salvar os dados do aluno no banco de dados.
            def salvar_aluno():

                # Obtém o nome da turma selecionada na `Combobox` do formulário.
                turma = entries["Turma:"].get()

                # Verifica se o campo de turma está vazio.
                # Se não houver uma turma selecionada, exibe uma mensagem de
                #       erro e interrompe a execução da função.
                if not turma:
                    messagebox.showerror("Erro", "Selecione a turma do aluno.")
                    return

                # Busca no banco de dados a turma correspondente ao nome selecionado.
                # `col_turmas.find_one({"nome_turma": turma})` retorna o
                #       documento da turma se ela existir.
                turma_doc = col_turmas.find_one({"nome_turma": turma})

                # Se a turma foi encontrada no banco de dados, verifica a
                #       quantidade de alunos já cadastrados nela.
                if turma_doc:

                    # Conta quantos alunos já estão matriculados na turma selecionada.
                    # `col_alunos.count_documents({"turma": turma})` retorna o
                    #       número total de alunos na turma.
                    total_alunos = col_alunos.count_documents({"turma": turma})

                    # Obtém a capacidade máxima da turma e verifica se ela foi atingida.
                    # `turma_doc.get("capacidade", 0)` obtém o valor da capacidade,
                    #       retornando 0 se o campo não existir.
                    # Se o número de alunos na turma for maior ou igual à capacidade
                    #       máxima, exibe um erro e interrompe a função.
                    if total_alunos >= turma_doc.get("capacidade", 0):
                        messagebox.showerror("Erro",
                                             "Esta turma atingiu sua capacidade máxima de alunos.")
                        return

                # Caso a turma não seja encontrada no banco de dados, exibe uma
                #       mensagem de erro e interrompe a execução.
                else:
                    messagebox.showerror("Erro", "Turma não encontrada.")
                    return

                # Cria um dicionário `doc` contendo os dados do aluno que
                #       serão salvos no banco de dados.
                # Cada chave do dicionário corresponde a um campo do banco de dados.
                doc = {

                    # Obtém o nome do aluno digitado no campo de entrada
                    #       correspondente e armazena no campo "nome".
                    "nome": entries["Nome:"].get(),

                    # Obtém a data de nascimento digitada e armazena no campo "data_nascimento".
                    "data_nascimento": entries["Data Nascimento (AAAA-MM-DD):"].get(),

                    # Obtém o CPF do aluno e armazena no campo "cpf".
                    "cpf": entries["CPF:"].get(),

                    # Obtém o número de matrícula do aluno e armazena no campo "matricula".
                    "matricula": entries["Matrícula:"].get(),

                    # Obtém o endereço digitado e armazena no campo "endereco".
                    "endereco": entries["Endereço:"].get(),

                    # Obtém o telefone digitado e armazena no campo "telefone".
                    "telefone": entries["Telefone:"].get(),

                    # Obtém o e-mail digitado e armazena no campo "email".
                    "email": entries["E-mail:"].get(),

                    # Armazena a turma selecionada no campo "turma".
                    "turma": turma

                }

                # Insere o documento `doc` na coleção `col_alunos`, salvando os
                #       dados do aluno no banco de dados MongoDB.
                col_alunos.insert_one(doc)

                # Exibe uma mensagem de sucesso informando que o aluno foi
                #       cadastrado corretamente.
                messagebox.showinfo("Sucesso",
                                    "Aluno cadastrado com sucesso!")

                # Fecha a janela de cadastro após a inserção dos dados no banco.
                win.destroy()

                # Atualiza a lista de alunos na interface para
                #       refletir o novo cadastro.
                atualizar_lista_alunos()

            # Cria um botão `Salvar` dentro do `form_frame`, responsável por
            #       chamar a função `salvar_aluno` ao ser clicado.
            # `text="Salvar"` define o texto exibido no botão.
            # `command=salvar_aluno` associa a função `salvar_aluno()` ao clique do botão.
            # `row=len(campos)` posiciona o botão na linha seguinte à última linha do formulário.
            # `column=0, columnspan=2` faz o botão ocupar duas colunas, centralizando-o
            #       abaixo dos campos do formulário.
            # `pady=20` adiciona um espaçamento vertical de 20 pixels acima e
            #       abaixo do botão para melhor visualização.
            ttk.Button(form_frame,
                       text="Salvar",
                       command=salvar_aluno).grid(row=len(campos), column=0, columnspan=2, pady=20)


        # Define a função `editar_aluno()`, responsável por permitir a
        #       edição dos dados de um aluno existente no sistema.
        def editar_aluno():

            # Obtém o item atualmente selecionado na `Treeview`.
            selecionado = tree.focus()

            # Se nenhum item estiver selecionado, exibe um alerta e interrompe a função.
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione um aluno para editar.")
                return

            # Obtém os valores do item selecionado na `Treeview`.
            # `tree.item(selecionado, "values")` retorna uma tupla
            #       com os valores da linha selecionada.
            valores = tree.item(selecionado, "values")

            # Obtém o ID do aluno a partir do primeiro valor da tupla `valores`.
            aluno_id = valores[0]

            # Busca no banco de dados o documento do aluno correspondente ao ID obtido.
            aluno = obter_aluno_por_id(aluno_id)

            # Se o aluno não for encontrado no banco de dados, exibe uma
            #       mensagem de erro e interrompe a função.
            if not aluno:
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return

            # Cria uma nova janela (`Toplevel`) para a edição dos dados do aluno.
            win = Toplevel(janela)

            # Define o título da janela como "Editar Aluno".
            win.title("Editar Aluno")

            # Centraliza a janela na tela com as dimensões 800x500 pixels.
            # A função `centralizar_janela(win, 800, 500)` calcula a posição
            #       para exibir a janela no centro da tela.
            centralizar_janela(win, 800, 500)

            # Define a janela de edição como uma janela modal, impedindo interações
            #       com a janela principal enquanto estiver aberta.
            win.transient(janela)

            # Faz com que a nova janela capture os eventos do usuário, garantindo
            #       que ela esteja em primeiro plano até ser fechada.
            win.grab_set()

            # Cria um `LabelFrame` para agrupar os campos de edição do aluno,
            #       com título "Editar Dados do Aluno".
            # O `padding=(20,10)` adiciona espaçamento interno de 20 pixels na
            #       horizontal e 10 na vertical.
            form_frame = ttk.LabelFrame(win,
                                        text="Editar Dados do Aluno",
                                        padding=(20, 10))

            # Exibe o `LabelFrame` na janela, permitindo que ele expanda e
            #       ocupe todo o espaço disponível.
            # `fill='both'` faz com que ele se ajuste tanto na largura quanto na altura.
            # `expand=True` permite que o frame cresça caso a janela seja redimensionada.
            # `padx=20, pady=20` adiciona espaçamento externo ao redor do
            #       frame para uma melhor organização visual.
            form_frame.pack(fill='both', expand=True, padx=20, pady=20)

            # Define uma lista de tuplas contendo os rótulos e os respectivos
            #       valores do aluno para edição.
            # Cada tupla contém o nome do campo e o valor atual armazenado no banco de dados.
            campos = [
                ("Nome:", aluno["nome"]),
                ("Data Nascimento (AAAA-MM-DD):", aluno["data_nascimento"]),
                ("CPF:", aluno["cpf"]),
                ("Matrícula:", aluno["matricula"]),
                ("Endereço:", aluno["endereco"]),
                ("Telefone:", aluno["telefone"]),
                ("E-mail:", aluno["email"]),
                ("Turma:", aluno["turma"])
            ]

            # Cria um dicionário `entries` para armazenar as referências dos
            #       campos de entrada (`Entry` e `Combobox`).
            entries = {}

            # Percorre a lista `campos`, onde `i` representa o índice, `lbl` é o nome
            #       do campo e `val` é o valor atual do aluno.
            for i, (lbl, val) in enumerate(campos):

                # Cria um rótulo (`Label`) com o nome do campo e o adiciona na
                #       coluna 0 da linha correspondente.
                # `sticky='e'` alinha o texto do rótulo à direita.
                # `padx=10, pady=5` adiciona espaçamento externo horizontal e
                #       vertical para melhorar a organização visual.
                ttk.Label(form_frame,
                          text=lbl).grid(row=i, column=0, sticky='e', padx=10, pady=5)

                # Verifica se o campo atual é "Turma:", pois ele será tratado de
                #       forma diferente dos demais.
                if lbl == "Turma:":

                    # Cria uma `Combobox` para permitir a seleção de uma turma existente.
                    # `values=obter_nomes_turmas()` define a lista de turmas
                    #       disponíveis no banco de dados.
                    # `width=30` define a largura da `Combobox`.
                    # `state="readonly"` impede que o usuário digite manualmente
                    #       uma opção, permitindo apenas a seleção.
                    cb = ttk.Combobox(form_frame,
                                      values=obter_nomes_turmas(),
                                      width=30,
                                      state="readonly")

                    # Define o valor atual da `Combobox` como a turma cadastrada do aluno.
                    cb.set(val)

                    # Posiciona a `Combobox` na coluna 1 da linha correspondente,
                    #       alinhando-a à esquerda (`sticky='w'`).
                    # `padx=10, pady=5` adiciona espaçamento ao redor do componente.
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena a referência da `Combobox` no dicionário `entries`,
                    #       associando-a ao nome do campo.
                    entries[lbl] = cb

                # Se o campo não for "Turma:", cria um campo de entrada (`Entry`).
                else:

                    # Cria um `Entry` (campo de entrada de texto) para
                    #       permitir a edição do valor do aluno.
                    # `width=30` define a largura do campo de entrada.
                    ent = ttk.Entry(form_frame, width=30)

                    # Insere o valor atual do aluno no campo de entrada.
                    ent.insert(0, val)

                    # Posiciona o campo de entrada na coluna 1 da linha correspondente,
                    #       alinhando-o à esquerda (`sticky='w'`).
                    # `padx=10, pady=5` adiciona espaçamento ao redor do campo
                    #       para melhor organização visual.
                    ent.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena a referência do campo de entrada no dicionário `entries`,
                    #       associando-a ao nome do campo.
                    entries[lbl] = ent

            # Define a função `atualizar_aluno()`, responsável por salvar as
            #       alterações feitas no cadastro do aluno.
            def atualizar_aluno():

                # Atualiza o registro do aluno na coleção `col_alunos` do MongoDB.
                # `update_one()` localiza o aluno pelo seu `_id` e atualiza os
                #       campos com os novos valores.
                col_alunos.update_one(
                    {"_id": ObjectId(aluno_id)},  # Filtra o aluno pelo seu identificador único (ObjectId).
                    {"$set": {  # Define os novos valores para os campos do aluno.
                        "nome": entries["Nome:"].get(),  # Obtém o nome atualizado do campo de entrada.
                        "data_nascimento": entries["Data Nascimento (AAAA-MM-DD):"].get(),
                        # Atualiza a data de nascimento.
                        "cpf": entries["CPF:"].get(),  # Atualiza o CPF do aluno.
                        "matricula": entries["Matrícula:"].get(),  # Atualiza o número de matrícula.
                        "endereco": entries["Endereço:"].get(),  # Atualiza o endereço do aluno.
                        "telefone": entries["Telefone:"].get(),  # Atualiza o telefone de contato.
                        "email": entries["E-mail:"].get(),  # Atualiza o e-mail do aluno.
                        "turma": entries["Turma:"].get()  # Atualiza a turma do aluno.
                    }}
                )

                # Exibe uma caixa de mensagem informando que o aluno foi atualizado com sucesso.
                messagebox.showinfo("Sucesso",
                                    "Aluno atualizado com sucesso!")

                # Fecha a janela de edição após a atualização dos dados.
                win.destroy()

                # Atualiza a lista de alunos na interface para refletir as
                #       mudanças feitas no banco de dados.
                atualizar_lista_alunos()

            # Cria um botão para salvar as alterações feitas no cadastro do aluno.
            # `text="Salvar Alterações"` define o texto exibido no botão.
            # `command=atualizar_aluno` associa a ação de atualizar os
            #       dados do aluno ao clicar no botão.
            # `grid(row=len(campos), column=0, columnspan=2, pady=20)` define a
            #       posição do botão na grade do layout.
            # - `row=len(campos)` posiciona o botão logo abaixo do último campo do formulário.
            # - `column=0` define a coluna onde o botão será inserido.
            # - `columnspan=2` faz com que o botão ocupe duas colunas, centralizando-o no formulário.
            # - `pady=20` adiciona um espaçamento vertical de 20 pixels ao redor do botão.
            ttk.Button(form_frame,
                       text="Salvar Alterações",
                       command=atualizar_aluno).grid(row=len(campos),
                                                     column=0,
                                                     columnspan=2,
                                                     pady=20)


        # Define a função para excluir um aluno da base de dados.
        def excluir_aluno():

            # Obtém o item atualmente selecionado na árvore (`Treeview`).
            selecionado = tree.focus()

            # Verifica se nenhum aluno foi selecionado.
            # Se não houver seleção, exibe um aviso e interrompe a execução da função.
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione um aluno para excluir.")
                return

            # Obtém os valores da linha selecionada na árvore.
            valores = tree.item(selecionado, "values")

            # Captura o ID do aluno a partir dos valores obtidos.
            aluno_id = valores[0]

            # Exibe uma caixa de diálogo de confirmação perguntando se o usuário deseja excluir o aluno.
            # Se o usuário clicar em "Sim", a exclusão será realizada.
            if messagebox.askyesno("Confirmação",
                                   "Deseja realmente excluir este aluno?"):

                # Remove o aluno do banco de dados usando seu ID.
                col_alunos.delete_one({"_id": ObjectId(aluno_id)})

                # Exibe uma mensagem informando que o aluno foi excluído com sucesso.
                messagebox.showinfo("Sucesso",
                                    "Aluno excluído!")

                # Atualiza a lista de alunos na interface
                #       para refletir a remoção.
                atualizar_lista_alunos()

                # Permanece na mesma tela após o clique em “OK” do messagebox.
                janela.lift()


        # Cria um botão para adicionar um novo aluno.
        # `text="Adicionar Aluno"` define o texto exibido no botão.
        # `command=adicionar_aluno` associa a ação de abrir o formulário de
        #       cadastro ao clicar no botão.
        # `grid(row=0, column=0, padx=10)` posiciona o botão na linha 0 e
        #       coluna 0, com espaçamento horizontal de 10 pixels.
        ttk.Button(btn_frame,
                   text="Adicionar Aluno",
                   command=adicionar_aluno).grid(row=0, column=0, padx=10)

        # Cria um botão para editar um aluno existente.
        # `text="Editar Aluno"` define o texto exibido no botão.
        # `command=editar_aluno` associa a ação de abrir o formulário de
        #       edição ao clicar no botão.
        # `grid(row=0, column=1, padx=10)` posiciona o botão na linha 0 e
        #       coluna 1, com espaçamento horizontal de 10 pixels.
        ttk.Button(btn_frame,
                   text="Editar Aluno",
                   command=editar_aluno).grid(row=0, column=1, padx=10)

        # Cria um botão para excluir um aluno.
        # `text="Excluir Aluno"` define o texto exibido no botão.
        # `command=excluir_aluno` associa a ação de remover um aluno da
        #       base de dados ao clicar no botão.
        # `grid(row=0, column=2, padx=10)` posiciona o botão na linha 0 e
        #       coluna 2, com espaçamento horizontal de 10 pixels.
        ttk.Button(btn_frame,
                   text="Excluir Aluno",
                   command=excluir_aluno).grid(row=0, column=2, padx=10)






    # ---------- Gerenciamento de Professores (inclui duplo clique para exibir turmas) ----------

    # Define a função para abrir a janela de gerenciamento de professores.
    def abrir_janela_gerenciar_professores(self):

        # Cria uma nova janela (`Toplevel`) dentro da
        #       janela principal (`self.root`).
        janela = Toplevel(self.root)

        # Define o título da nova janela.
        # `title("Gerenciamento de Professores")` exibe esse
        #       nome na barra superior da janela.
        janela.title("Gerenciamento de Professores")

        # Define o estado da janela como "maximizado".
        # `state('zoomed')` faz com que a janela seja aberta ocupando toda a tela.
        janela.state('zoomed')

        # Configura o fundo da janela com a cor cinza claro (`#f0f0f0`).
        # Isso mantém o estilo visual consistente com o restante do sistema.
        janela.configure(bg='#f0f0f0')

        # Cria um frame superior (`top_frame`) dentro da nova janela.
        # Esse frame será utilizado para organizar os filtros de pesquisa.
        # `bg='#f0f0f0'` mantém a mesma cor de fundo da janela.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        top_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Exibe o frame na janela, preenchendo toda a largura (`fill='x'`).
        top_frame.pack(fill='x')

        # Cria um rótulo (`Label`) para indicar o campo de filtro por nome.
        # `text="Filtrar por Nome:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0, padx=5, sticky='e')` posiciona o rótulo
        #       na primeira linha (`row=0`),
        #       na primeira coluna (`column=0`), com um espaçamento horizontal
        #       de 5 pixels (`padx=5`).
        # `sticky='e'` alinha o rótulo à direita (east).
        ttk.Label(top_frame,
                  text="Filtrar por Nome:").grid(row=0, column=0, padx=5, sticky='e')

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa digitar o nome a ser filtrado.
        # `width=30` define a largura do campo como 30 caracteres.
        filtro_nome = ttk.Entry(top_frame, width=30)

        # Posiciona o campo de entrada na primeira linha (`row=0`) e
        #       na segunda coluna (`column=1`),
        #       com um espaçamento horizontal de 5 pixels (`padx=5`).
        filtro_nome.grid(row=0, column=1, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de filtro por disciplina.
        # `text="Filtrar por Disciplina:"` define o texto exibido no rótulo.
        # `grid(row=0, column=2, padx=5, sticky='e')` posiciona o rótulo na primeira linha (`row=0`),
        #       na terceira coluna (`column=2`), com um espaçamento horizontal de 5 pixels (`padx=5`).
        # `sticky='e'` alinha o rótulo à direita (east), garantindo um alinhamento adequado.
        ttk.Label(top_frame,
                  text="Filtrar por Disciplina:").grid(row=0, column=2, padx=5, sticky='e')

        # Cria uma caixa de seleção (`Combobox`) para filtrar os
        #       professores por disciplina.
        # `values=obter_nomes_disciplinas()` preenche a caixa com a
        #       lista de disciplinas cadastradas.
        # `width=30` define a largura do campo como 30 caracteres.
        # `state="readonly"` impede que o usuário digite valores manuais,
        #       permitindo apenas a seleção.
        filtro_disciplina = ttk.Combobox(top_frame,
                                         values=obter_nomes_disciplinas(),
                                         width=30,
                                         state="readonly")

        # Posiciona a `Combobox` na primeira linha (`row=0`) e
        #       na quarta coluna (`column=3`),
        #       com um espaçamento horizontal de 5 pixels (`padx=5`).
        filtro_disciplina.grid(row=0, column=3, padx=5)


        # Define a função que atualizará a lista de professores
        #       com base nos filtros aplicados.
        def atualizar_lista_professores():

            # Cria um dicionário vazio para construir a
            #       consulta com os filtros.
            query = {}

            # Verifica se há texto no campo de filtro por nome.
            # Se houver, adiciona uma condição para buscar nomes que contenham o
            #       texto digitado, ignorando maiúsculas e minúsculas.
            if filtro_nome.get():
                query["nome"] = {"$regex": filtro_nome.get(), "$options": "i"}

            # Verifica se há uma disciplina selecionada no filtro de
            #       disciplina. Se houver, adiciona
            #       uma condição para buscar apenas professores daquela disciplina.
            if filtro_disciplina.get():
                query["disciplina"] = filtro_disciplina.get()

            # Remove todos os itens atualmente exibidos na árvore de
            #       visualização (`Treeview`) para que a lista possa ser
            #       recarregada com os dados atualizados.
            for i in tree.get_children():
                tree.delete(i)

            # Itera sobre todos os professores retornados pela
            #       consulta ao banco de dados.
            for prof in col_professores.find(query):

                # Adiciona cada professor como uma nova linha na árvore de visualização.
                # O primeiro argumento `""` indica que a linha será inserida na raiz.
                # `end` significa que o item será adicionado no final da lista de itens.
                # `values` define as colunas a serem exibidas: ID, nome, CPF, disciplina e telefone.
                tree.insert("",
                            "end",
                            values=(str(prof["_id"]),  # Converte o identificador único do MongoDB para string.
                                    prof["nome"],  # Nome do professor.
                                    prof["cpf"],  # CPF do professor.
                                    prof["disciplina"],  # Disciplina que o professor ensina.
                                    prof["telefone"]))  # Telefone do professor.


        # Cria um botão para aplicar os filtros na lista de professores.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=atualizar_lista_professores` chama a função responsável por
        #       atualizar a lista com base nos filtros.
        # `grid(row=0, column=4, padx=5)` posiciona o botão na linha 0,
        #       coluna 4, com um espaçamento horizontal de 5 pixels.
        ttk.Button(top_frame,
                   text="Filtrar",
                   command=atualizar_lista_professores).grid(row=0, column=4, padx=5)

        # Cria um botão para limpar os filtros.
        # `text="Limpar"` define o texto exibido no botão.
        # `command=lambda: [filtro_nome.delete(0, 'end'), filtro_disciplina.set(''),
        #       atualizar_lista_professores()]` limpa os campos de filtro e
        #       atualiza a lista de professores.
        # `grid(row=0, column=5, padx=5)` posiciona o botão na linha 0,
        #       coluna 5, com um espaçamento horizontal de 5 pixels.
        ttk.Button(top_frame,
                   text="Limpar",
                   command=lambda: [filtro_nome.delete(0,
                                                       'end'),
                                    filtro_disciplina.set(''),
                                    atualizar_lista_professores()]).grid(row=0,
                                                                         column=5,
                                                                         padx=5)

        # Cria um frame dentro da janela para conter o Treeview.
        # `bg='#f0f0f0'` define a cor de fundo do frame. (#f0f0f0 é um cinza claro)
        tree_frame = tk.Frame(janela, bg='#f0f0f0')

        # Empacota o frame na janela, com espaçamento vertical de 10 pixels,
        #       permitindo que ele preencha toda a largura e altura disponíveis.
        tree_frame.pack(pady=10, fill='both', expand=True)

        # Define os nomes das colunas do Treeview.
        colunas = ("id", "Nome", "CPF", "Disciplina", "Telefone")

        # Cria um Treeview dentro do frame.
        # `columns=colunas` especifica as colunas a serem exibidas.
        # `show="headings"` exibe apenas os cabeçalhos das colunas.
        # `selectmode="browse"` permite selecionar apenas uma linha por vez.
        tree = ttk.Treeview(tree_frame,
                            columns=colunas,
                            show="headings",
                            selectmode="browse")

        # Para cada coluna no Treeview:
        for col in colunas:

            # Define o texto do cabeçalho da coluna usando o nome da coluna.
            tree.heading(col, text=col)

            # Define a largura de cada coluna em 220 pixels.
            tree.column(col, width=220)

        # Empacota o Treeview dentro do frame.
        # `fill='both'` permite que ele se expanda horizontal e verticalmente.
        # `expand=True` faz com que o Treeview ocupe todo o
        #       espaço disponível no frame.
        tree.pack(fill='both', expand=True)

        # Atualiza a lista de professores exibida no Treeview.
        atualizar_lista_professores()


        # Duplo clique: exibe as turmas lecionadas pelo professor
        # Define a função chamada `exibir_turmas_professor`.
        # Essa função é chamada quando um evento ocorre (por exemplo, um
        #       clique em uma linha do Treeview).
        def exibir_turmas_professor(event):

            # Obtém a identificação do item atualmente selecionado no Treeview.
            selecionado = tree.focus()

            # Verifica se nenhum item foi selecionado.
            # Se não há item selecionado, a função simplesmente retorna sem fazer nada.
            if not selecionado:
                return

            # Obtém os valores associados ao item selecionado no Treeview.
            valores = tree.item(selecionado, "values")

            # O segundo valor (índice 1) contém o nome do professor.
            nome_prof = valores[1]

            # Cria uma nova janela (Toplevel) para exibir as turmas
            #       associadas ao professor selecionado.
            win_turmas = Toplevel(janela)

            # Define o título da janela criada anteriormente como "Turmas lecionadas por"
            #       seguido do nome do professor.
            win_turmas.title(f"Turmas lecionadas por {nome_prof}")

            # Define o estado da janela como "zoomed", ou seja, maximizada.
            win_turmas.state('zoomed')

            # Configura o fundo da janela para a cor #f0f0f0 (cinza claro).
            win_turmas.configure(bg='#f0f0f0')

            # Cria um novo frame dentro da janela `win_turmas` com fundo cinza claro.
            frame_t = tk.Frame(win_turmas, bg='#f0f0f0')

            # Adiciona o frame à janela e define um espaçamento vertical (`pady`) de 10 pixels.
            # Preenche todo o espaço horizontal e vertical disponível.
            frame_t.pack(pady=10, fill='both', expand=True)

            # Define as colunas que o Treeview conterá, cada uma
            #       representando um atributo das turmas.
            colunas_t = ("id_turma", "Nome Turma", "Ano", "Série", "Turno", "Capacidade")

            # Cria um Treeview, que é uma tabela interativa, dentro do frame `frame_t`.
            # As colunas são configuradas com base na lista `colunas_t`.
            # `show="headings"` indica que apenas os cabeçalhos das colunas e as
            #       células serão exibidos (sem a coluna de hierarquia padrão).
            tree_turmas = ttk.Treeview(frame_t, columns=colunas_t, show="headings")

            # Para cada coluna na lista `colunas_t`, define o texto exibido no
            #       cabeçalho e ajusta a largura.
            for c in colunas_t:

                # Define o texto do cabeçalho para a coluna atual.
                tree_turmas.heading(c, text=c)

                # Define a largura da coluna em 150 pixels.
                tree_turmas.column(c, width=150)

            # Adiciona o Treeview à interface, fazendo com que ele
            #       preencha o espaço disponível.
            tree_turmas.pack(fill='both', expand=True)

            # Consulta o banco de dados `col_turmas` para buscar todas as
            #       turmas associadas ao professor selecionado.
            for t in col_turmas.find({"professor_responsavel": nome_prof}):

                # Para cada turma encontrada, insere uma nova linha no
                #       Treeview com os valores correspondentes:
                # - ID da turma, convertido para string.
                # - Nome da turma.
                # - Ano da turma.
                # - Série da turma.
                # - Turno da turma.
                # - Capacidade da turma.
                tree_turmas.insert("",
                                   "end",
                                   values=(str(t["_id"]),
                                           t["nome_turma"],
                                           t["ano"],
                                           t["serie"],
                                           t["turno"],
                                           t["capacidade"]))

            # Função para executar ações quando uma turma for clicada.
            def ao_clicar_turma(event_turma):

                # Obtém a identificação do item selecionado na árvore de turmas.
                sel = tree_turmas.focus()

                # Se nenhum item estiver selecionado, a função retorna sem fazer nada.
                if not sel:
                    return

                # Obtém os valores do item selecionado. Esses valores estão em uma tupla,
                # onde a primeira posição corresponde ao ID da turma e a
                #       segunda ao nome da turma.
                vals = tree_turmas.item(sel, "values")
                turma_id, turma_nome = vals[0], vals[1]

                # Cria uma nova janela de nível superior para exibir os
                #       alunos da turma selecionada.
                win_alunos = Toplevel(win_turmas)

                # Define o título da janela com o nome da turma.
                win_alunos.title(f"Alunos da Turma {turma_nome}")

                # Configura a janela para abrir no estado maximizado,
                #       ocupando toda a tela.
                win_alunos.state('zoomed')

                # Define a cor de fundo da janela para um tom de cinza claro.
                win_alunos.configure(bg='#f0f0f0')  # Cor: cinza claro.

                # Cria um frame para exibir os alunos.
                # `bg='#f0f0f0'` define a cor de fundo como cinza claro.
                frame_alunos = tk.Frame(win_alunos, bg='#f0f0f0')

                # `pack(pady=10, fill='both', expand=True)` adiciona espaçamento
                #       vertical, preenche o espaço disponível e permite expansão.
                frame_alunos.pack(pady=10, fill='both', expand=True)

                # Define as colunas que aparecerão na árvore de alunos.
                # Cada entrada na tupla `colunas_a` é o nome de uma
                #       coluna: "id_aluno", "Nome", "Matrícula", "Turma".
                colunas_a = ("id_aluno", "Nome", "Matrícula", "Turma")

                # Cria uma Treeview para listar os alunos.
                # `columns=colunas_a` define as colunas na árvore.
                # `show="headings"` oculta a coluna raiz e exibe apenas os cabeçalhos definidos.
                tree_alunos = ttk.Treeview(frame_alunos, columns=colunas_a, show="headings")

                # Configura cada coluna da Treeview.
                for c in colunas_a:

                    # Define o texto do cabeçalho da coluna.
                    tree_alunos.heading(c, text=c)

                    # Define a largura da coluna para 200 pixels.
                    tree_alunos.column(c, width=200)

                # Adiciona a Treeview ao frame.
                # `fill='both'` permite que a Treeview preencha todo o espaço disponível no frame.
                # `expand=True` garante que o widget possa se expandir quando o frame crescer.
                tree_alunos.pack(fill='both', expand=True)

                # Busca o documento da turma correspondente ao `turma_id`.
                turma_doc = obter_turma_por_id(turma_id)

                # Se o documento da turma for encontrado, busca os alunos da turma.
                if turma_doc:

                    # Itera sobre os alunos encontrados na coleção `col_alunos`
                    #       cuja turma seja a mesma da turma selecionada.
                    for a in col_alunos.find({"turma": turma_doc["nome_turma"]}):

                        # Insere uma nova linha na Treeview para cada aluno encontrado.
                        # `values=()` define os valores das colunas para a linha inserida.
                        # `a["_id"]` representa o identificador único do aluno no banco de dados.
                        # `a["nome"]`, `a["matricula"]` e `a["turma"]` são os valores para
                        #       as colunas "Nome", "Matrícula" e "Turma", respectivamente.
                        tree_alunos.insert("", "end", values=(
                            str(a["_id"]),
                            a["nome"],
                            a["matricula"],
                            a["turma"]))

            # Liga o evento de clique duplo na tree_turmas à função ao_clicar_turma.
            # Quando o usuário der um duplo clique em um item da tree_turmas, a
            #       função ao_clicar_turma será chamada.
            tree_turmas.bind("<Double-1>", ao_clicar_turma)


        # Liga o evento de clique duplo na tree à função exibir_turmas_professor.
        # Quando o usuário der um duplo clique em um item da tree, a
        #       função exibir_turmas_professor será chamada.
        tree.bind("<Double-1>", exibir_turmas_professor)

        # Cria um frame para os botões na parte inferior da janela.
        # O frame terá um fundo cinza claro e um padding de
        #       10 pixels na parte inferior.
        btn_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o frame de botões na janela.
        # Este frame conterá os botões para adicionar, editar e
        #       excluir professores.
        btn_frame.pack()


        # Define a função que será chamada ao clicar no
        #       botão "Adicionar Professor".
        def adicionar_professor():

            # Cria uma nova janela modal para adicionar um professor.
            win = Toplevel(janela)

            # Define o título da nova janela.
            win.title("Adicionar Professor")

            # Configura o fundo da nova janela para cinza claro.
            win.configure(bg='#f0f0f0')

            # Centraliza a nova janela na tela, definindo suas dimensões.
            centralizar_janela(win, 500, 400)

            # Define a nova janela como modal, bloqueando a interação com a
            #       janela principal enquanto ela está aberta.
            win.transient(janela)

            # Impede que outras janelas recebam eventos enquanto
            #       esta janela está aberta.
            win.grab_set()

            # Cria um LabelFrame para conter o formulário de cadastro de professores.
            # O texto do LabelFrame é definido como "Cadastro de Professor".
            # O padding interno do LabelFrame é ajustado para 20 pixels
            #       horizontalmente e 10 pixels verticalmente.
            form = ttk.LabelFrame(win,
                                  text="Cadastro de Professor",
                                  padding=(20, 10))

            # Posiciona o LabelFrame na janela.
            # `fill='both'` faz com que o LabelFrame preencha todo o espaço
            #       disponível, tanto horizontal quanto verticalmente.
            # `expand=True` permite que o LabelFrame se expanda junto com a
            #       janela, se ela for redimensionada.
            # `padx=20` e `pady=20` adicionam 20 pixels de margem ao redor do
            #       LabelFrame, separando-o das bordas da janela.
            form.pack(fill='both', expand=True, padx=20, pady=20)

            # Define os campos do formulário.
            # Cada tupla contém o texto do rótulo (primeiro elemento) e o
            #       valor inicial do campo (segundo elemento).
            # Inicialmente, todos os campos estão vazios.
            campos = [
                ("Nome:", ""),  # Campo para o nome do professor.
                ("CPF:", ""),  # Campo para o CPF do professor.
                ("Disciplina:", ""),  # Campo para a disciplina que o professor leciona.
                ("Endereço:", ""),  # Campo para o endereço do professor.
                ("Telefone:", ""),  # Campo para o telefone de contato do professor.
                ("Email:", "")  # Campo para o endereço de email do professor.
            ]

            # Cria um dicionário vazio para armazenar as referências
            #       aos campos de entrada.
            # Cada chave do dicionário será o texto do rótulo do campo, e o
            #       valor será a referência ao widget correspondente.
            entries = {}

            # Percorre a lista de campos definidos anteriormente.
            # `enumerate(campos)` retorna o índice e o par (texto do
            #       rótulo, valor inicial) para cada campo.
            for i, (lbl, _) in enumerate(campos):

                # Cria um rótulo para o campo de entrada correspondente.
                # O texto do rótulo é obtido do primeiro elemento do par `lbl`.
                # `grid(row=i, column=0)` posiciona o rótulo na linha `i` e na primeira coluna.
                # `sticky='e'` alinha o rótulo à direita na célula.
                # `padx=10` e `pady=5` adicionam margens horizontais e verticais ao redor do rótulo.
                ttk.Label(form,
                          text=lbl).grid(row=i, column=0, sticky='e', padx=10, pady=5)

                # Cria um campo de entrada de texto simples (Entry).
                # `width=30` define a largura do campo de entrada.
                ent = ttk.Entry(form, width=30)

                # Posiciona o campo de entrada na linha `i` e na segunda coluna.
                # `sticky='w'` alinha o campo de entrada à esquerda na célula.
                # `padx=10` e `pady=5` adicionam margens horizontais e
                #       verticais ao redor do campo de entrada.
                ent.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                # Armazena a referência do campo de entrada no dicionário `entries`,
                #       usando o texto do rótulo como chave.
                entries[lbl] = ent

            def salvar_prof():

                # Cria um dicionário `doc` que representará o novo registro do professor.
                # Cada chave do dicionário corresponde a um campo do banco de dados (ex: "nome", "cpf").
                # O valor de cada chave é obtido do campo de entrada associado (em `entries`).
                doc = {

                    # Pega o texto do campo de entrada associado ao rótulo "Nome:" e
                    #       atribui ao campo "nome" do dicionário.
                    "nome": entries["Nome:"].get(),

                    # Pega o texto do campo de entrada associado ao rótulo "CPF:" e
                    #       atribui ao campo "cpf" do dicionário.
                    "cpf": entries["CPF:"].get(),

                    # Pega o texto do campo de entrada associado ao rótulo "Disciplina:" e
                    #       atribui ao campo "disciplina" do dicionário.
                    "disciplina": entries["Disciplina:"].get(),

                    # Pega o texto do campo de entrada associado ao rótulo "Endereço:" e
                    #       atribui ao campo "endereco" do dicionário.
                    "endereco": entries["Endereço:"].get(),

                    # Pega o texto do campo de entrada associado ao rótulo "Telefone:" e
                    #       atribui ao campo "telefone" do dicionário.
                    "telefone": entries["Telefone:"].get(),

                    # Pega o texto do campo de entrada associado ao rótulo "Email:" e
                    #       atribui ao campo "email" do dicionário.
                    "email": entries["Email:"].get()

                }

                # Insere o dicionário `doc` na coleção `col_professores` do banco de dados.
                # Isso efetivamente salva as informações do professor no banco de dados.
                col_professores.insert_one(doc)

                # Exibe uma mensagem de sucesso usando o `messagebox`.
                # Isso serve para informar ao usuário que o cadastro foi concluído com sucesso.
                messagebox.showinfo("Sucesso",
                                    "Professor cadastrado!")

                # Fecha a janela de cadastro do professor.
                # Assim, após o cadastro, o usuário volta à janela principal.
                win.destroy()

                # Atualiza a lista de professores na interface.
                # Garante que a nova entrada apareça imediatamente sem
                #       precisar reiniciar a aplicação.
                atualizar_lista_professores()

            # Cria um botão de salvar no formulário.
            # Quando clicado, ele executará a função `salvar_prof`
            #       para realizar as ações acima.
            ttk.Button(form,
                       text="Salvar",
                       command=salvar_prof).grid(row=len(campos),
                                                 # Posiciona o botão após todos os campos do formulário.
                                                 column=0,  # Define a coluna inicial do botão.
                                                 columnspan=2,
                                                 # O botão se estenderá por duas colunas para ficar centralizado.
                                                 pady=20)  # Adiciona espaçamento vertical ao redor do botão.


        # Define a função `editar_professor`, que será chamada quando o
        #       usuário quiser editar os dados de um professor.
        def editar_professor():

            # Obtém a linha selecionada na interface. `tree.focus()` retorna o
            #       identificador da linha selecionada.
            # Se nenhuma linha estiver selecionada, `tree.focus()`
            #       retornará uma string vazia.
            selecionado = tree.focus()

            # Verifica se nenhuma linha foi selecionada.
            # Se `selecionado` for vazio, exibe uma mensagem de aviso para o usuário
            #       indicando que é necessário selecionar um professor antes de tentar editar.
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione um professor para editar.")
                return

            # Obtém os valores associados à linha selecionada.
            # `tree.item(selecionado, "values")` retorna uma tupla com os
            #       valores das colunas da linha selecionada.
            # O primeiro valor da tupla (`valores[0]`) contém o
            #       identificador do professor.
            valores = tree.item(selecionado, "values")
            prof_id = valores[0]

            # Busca no banco de dados o professor correspondente ao identificador selecionado.
            # A função `obter_professor_por_id` retorna um dicionário com os dados do
            #       professor ou `None` se o professor não for encontrado.
            prof = obter_professor_por_id(prof_id)

            # Se o professor não for encontrado no banco de dados, exibe uma
            #       mensagem de erro para o usuário.
            if not prof:
                messagebox.showerror("Erro",
                                     "Professor não encontrado.")
                return

            # Cria uma nova janela para a edição do professor.
            # A função `Toplevel` cria uma nova janela em cima da
            #       janela principal (`janela`).
            win = Toplevel(janela)

            # Define o título da nova janela como "Editar Professor".
            win.title("Editar Professor")

            # Configura a cor de fundo da janela como '#f0f0f0' (cinza claro).
            win.configure(bg='#f0f0f0')

            # Centraliza a janela na tela do usuário.
            # `centralizar_janela` é uma função personalizada que posiciona a janela
            #       no centro da tela com a largura de 500 pixels e a altura de 400 pixels.
            centralizar_janela(win, 500, 400)

            # Faz com que a nova janela seja modal.
            # Isso impede que o usuário interaja com a janela principal
            #       enquanto a janela de edição está aberta.
            win.transient(janela)

            # Garante que a nova janela tenha o foco e bloqueie
            #       interações em outras janelas.
            win.grab_set()

            # Cria um frame com borda e título para o formulário de edição.
            # `text="Editar Professor"` define o título do frame.
            # `padding=(20,10)` adiciona um espaçamento interno (padding)
            #       de 20 pixels nas laterais e 10 pixels no topo e na base.
            form = ttk.LabelFrame(win, text="Editar Professor", padding=(20, 10))

            # Adiciona o frame ao layout da janela.
            # `fill='both'` faz com que o frame preencha a largura e a altura disponíveis.
            # `expand=True` permite que o frame cresça, se houver espaço adicional.
            # `padx=20` e `pady=20` adicionam espaçamento externo ao redor do frame.
            form.pack(fill='both', expand=True, padx=20, pady=20)

            # Define os campos do formulário e seus valores iniciais.
            # Cada campo é uma tupla no formato (rótulo, valor).
            campos = [
                ("Nome:", prof["nome"]),
                ("CPF:", prof["cpf"]),
                ("Disciplina:", prof["disciplina"]),
                ("Endereço:", prof["endereco"]),
                ("Telefone:", prof["telefone"]),
                ("Email:", prof["email"])
            ]

            # Cria um dicionário para armazenar os widgets de entrada.
            # As chaves serão os rótulos dos campos, e os valores
            #       serão os widgets correspondentes.
            entries = {}

            # Loop para criar os campos de formulário a partir da
            #       lista de campos e valores iniciais.
            # `enumerate(campos)` retorna o índice e a tupla (rótulo, valor) de cada campo.
            for i, (lbl, val) in enumerate(campos):

                # Cria um rótulo (Label) para o campo.
                # `text=lbl` define o texto exibido no rótulo.
                # `grid(row=i, column=0)` posiciona o rótulo na
                #       linha `i` e na primeira coluna (0).
                # `sticky='e'` alinha o rótulo à direita.
                # `padx=10` e `pady=5` adicionam espaçamento ao redor do rótulo.
                ttk.Label(form,
                          text=lbl).grid(row=i, column=0, sticky='e', padx=10, pady=5)

                # Verifica se o campo atual é o campo "Disciplina".
                if lbl == "Disciplina:":

                    # Cria uma caixa de seleção suspensa (Combobox) para as disciplinas.
                    # `values=obter_nomes_disciplinas()` define as opções disponíveis na caixa.
                    # `width=30` define a largura da caixa de seleção.
                    # `state="readonly"` torna a caixa apenas de leitura.
                    cb = ttk.Combobox(form,
                                      values=obter_nomes_disciplinas(),
                                      width=30,
                                      state="readonly")

                    # Define o valor inicial da caixa de seleção para a
                    #       disciplina correspondente.
                    cb.set(val)

                    # Posiciona a caixa de seleção na linha `i` e na segunda coluna (1).
                    # `sticky='w'` alinha a caixa à esquerda.
                    # `padx=10` e `pady=5` adicionam espaçamento ao redor da caixa.
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena a caixa de seleção no dicionário `entries`
                    #       com o rótulo como chave.
                    entries[lbl] = cb

                else:

                    # Cria uma caixa de texto (Entry) para os demais campos.
                    # `width=30` define a largura da caixa de texto.
                    ent = ttk.Entry(form, width=30)

                    # Insere o valor inicial no campo de texto.
                    ent.insert(0, val)

                    # Posiciona o campo de texto na linha `i` e na segunda coluna (1).
                    # `sticky='w'` alinha o campo à esquerda.
                    # `padx=10` e `pady=5` adicionam espaçamento ao redor do campo.
                    ent.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena o campo de texto no dicionário `entries`
                    #       com o rótulo como chave.
                    entries[lbl] = ent

            # Define a função que será chamada para salvar as
            #       alterações no banco de dados.
            def atualizar_prof():

                # Atualiza os dados do professor no banco de dados,
                #       utilizando a coleção `col_professores`.
                # A busca é feita pelo ID do professor: `{"_id": ObjectId(prof_id)}`.
                # Os novos valores são passados dentro de `{"$set": {...}}`.
                # Cada entrada é obtida diretamente do dicionário `entries`, que
                #       contém os campos do formulário.
                col_professores.update_one(
                    {"_id": ObjectId(prof_id)},

                    # Busca pelo ID do professor para identificar qual registro atualizar.
                    {"$set": {
                        "nome": entries["Nome:"].get(),  # Obtém o valor do campo "Nome".
                        "cpf": entries["CPF:"].get(),  # Obtém o valor do campo "CPF".
                        "disciplina": entries["Disciplina:"].get(),  # Obtém o valor do campo "Disciplina".
                        "endereco": entries["Endereço:"].get(),  # Obtém o valor do campo "Endereço".
                        "telefone": entries["Telefone:"].get(),  # Obtém o valor do campo "Telefone".
                        "email": entries["Email:"].get()  # Obtém o valor do campo "Email".
                    }}
                )

                # Exibe uma mensagem de sucesso ao usuário, indicando que o
                #       professor foi atualizado com sucesso.
                messagebox.showinfo("Sucesso", "Professor atualizado!")

                # Fecha a janela de edição.
                win.destroy()

                # Atualiza a lista de professores na interface principal,
                #       refletindo as alterações feitas.
                atualizar_lista_professores()

            # Cria um botão que, ao ser clicado, salva as alterações feitas no formulário.
            # O texto do botão é "Salvar Alterações".
            # Quando o botão é clicado, ele chama a função `atualizar_prof`,
            #       que realiza as alterações necessárias
            #       no banco de dados, atualiza a lista de professores na interface e fecha a janela de edição.
            # O botão é posicionado na última linha do formulário, utilizando `row=len(campos)`.
            # A configuração `column=0, columnspan=2` faz o botão ocupar duas colunas, centralizando-o visualmente.
            # `pady=20` adiciona um espaçamento vertical de 20 pixels acima e abaixo do botão, melhorando
            #       a organização visual do layout e separando o botão do restante dos campos.
            ttk.Button(form,
                       text="Salvar Alterações",
                       command=atualizar_prof).grid(row=len(campos), column=0, columnspan=2, pady=20)


        # Define a função `excluir_professor`, responsável por remover um
        #       professor do banco de dados.
        def excluir_professor():

            # Obtém o item atualmente selecionado na árvore (`tree`).
            selecionado = tree.focus()

            # Verifica se algum professor foi selecionado.
            # Se nenhum professor estiver selecionado, exibe um aviso ao
            #       usuário e interrompe a execução da função.
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione um professor para excluir.")
                return

            # Obtém os valores da linha correspondente ao professor selecionado.
            # A função `tree.item(selecionado, "values")` retorna uma tupla com os
            #       dados do professor na ordem definida nas colunas.
            valores = tree.item(selecionado, "values")

            # Extrai o ID do professor da tupla `valores`.
            # O ID é utilizado para identificar o professor no banco de dados MongoDB.
            prof_id = valores[0]

            # Exibe uma caixa de diálogo de confirmação para o usuário.
            # `askyesno` retorna `True` se o usuário clicar em "Sim" e `False` se clicar em "Não".
            if messagebox.askyesno("Confirmação",
                                   "Excluir este professor?"):

                # Se o usuário confirmar a exclusão, remove o professor do
                #       banco de dados MongoDB.
                # `delete_one({"_id": ObjectId(prof_id)})` busca e remove o
                #       documento cujo `_id` corresponde ao `prof_id`.
                col_professores.delete_one({"_id": ObjectId(prof_id)})

                # Exibe uma mensagem informando que o professor foi excluído com sucesso.
                messagebox.showinfo("Sucesso", "Professor excluído!")

                # Atualiza a lista de professores na interface
                #       gráfica para refletir a exclusão.
                atualizar_lista_professores()

                # Permanece na mesma tela após o clique em “OK” do messagebox.
                janela.lift()


        # Cria um botão para adicionar um novo professor.
        # `text="Adicionar Professor"` define o texto exibido no botão.
        # `command=adicionar_professor` associa a função `adicionar_professor` ao botão.
        # `grid(row=0, column=0, padx=5)` posiciona o botão na primeira
        #       linha e primeira coluna do frame, com espaçamento horizontal de 5 pixels.
        ttk.Button(btn_frame,
                   text="Adicionar Professor",
                   command=adicionar_professor).grid(row=0, column=0, padx=5)

        # Cria um botão para editar um professor existente.
        # `text="Editar Professor"` define o texto exibido no botão.
        # `command=editar_professor` associa a função `editar_professor` ao botão.
        # `grid(row=0, column=1, padx=5)` posiciona o botão na primeira
        #       linha e segunda coluna do frame, com espaçamento horizontal de 5 pixels.
        ttk.Button(btn_frame,
                   text="Editar Professor",
                   command=editar_professor).grid(row=0, column=1, padx=5)

        # Cria um botão para excluir um professor.
        # `text="Excluir Professor"` define o texto exibido no botão.
        # `command=excluir_professor` associa a função `excluir_professor` ao botão.
        # `grid(row=0, column=2, padx=5)` posiciona o botão na primeira linha e
        #       terceira coluna do frame, com espaçamento horizontal de 5 pixels.
        ttk.Button(btn_frame,
                   text="Excluir Professor",
                   command=excluir_professor).grid(row=0, column=2, padx=5)



    # ---------- Gerenciamento de Turmas ----------

    # Define um método para abrir a janela de gerenciamento de turmas.
    def abrir_janela_gerenciar_turmas(self):

        # Cria uma nova janela secundária para gerenciar turmas.
        # `Toplevel(self.root)` define a janela como um pop-up independente.
        janela = Toplevel(self.root)

        # Define o título da janela como "Gerenciamento de Turmas".
        janela.title("Gerenciamento de Turmas")

        # Expande a janela para ocupar toda a tela.
        janela.state('zoomed')

        # Define a cor de fundo da janela como cinza claro (#f0f0f0).
        janela.configure(bg='#f0f0f0')  # Cor: Cinza claro

        # Cria um frame superior para os filtros de busca de turmas.
        # `bg='#f0f0f0'` # Cor: Cinza claro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical interno.
        top_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Adiciona o frame superior na tela, ocupando
        #       toda a largura disponível.
        top_frame.pack(fill='x')

        # Cria um rótulo para o campo de filtro pelo nome da turma.
        # `text="Nome da Turma:"` define o texto do rótulo.
        # `grid(row=0, column=0, padx=5, sticky='e')` posiciona o
        #       rótulo na primeira linha e primeira coluna,
        #       adicionando 5 pixels de espaçamento horizontal e alinhando o
        #       texto à direita ('e' de 'east').
        ttk.Label(top_frame,
                  text="Nome da Turma:").grid(row=0, column=0, padx=5, sticky='e')

        # Cria um campo de entrada (Entry) para que o usuário possa
        #       digitar o nome da turma a ser filtrada.
        # `width=30` define a largura do campo de entrada.
        filtro_turma = ttk.Entry(top_frame, width=30)

        # Posiciona o campo de entrada na primeira linha e segunda coluna do frame.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels para separação visual.
        filtro_turma.grid(row=0, column=1, padx=5)


        # Define uma função para atualizar a lista de turmas
        #       exibida na interface.
        def atualizar_lista_turmas():

            # Inicializa um dicionário vazio para armazenar os
            #       critérios de busca.
            query = {}

            # Verifica se o campo de filtro de turma contém algum texto digitado pelo usuário.
            # Se sim, cria um critério de busca que filtra os nomes das
            #       turmas que contêm o texto digitado,
            #       utilizando expressão regular (`$regex`) e tornando a busca insensível a
            #       maiúsculas e minúsculas (`$options: "i"`).
            if filtro_turma.get():
                query["nome_turma"] = {"$regex": filtro_turma.get(), "$options": "i"}

            # Percorre todos os elementos atualmente exibidos na `Treeview` da interface.
            # `tree.get_children()` retorna todos os itens da lista.
            for i in tree.get_children():

                # Remove cada item encontrado para garantir que a lista
                #       seja atualizada corretamente.
                tree.delete(i)

            # Itera sobre todas as turmas encontradas no banco de dados que
            #       correspondem ao critério de busca.
            for turma in col_turmas.find(query):

                # Conta o número de alunos matriculados na turma atual.
                # `count_documents` retorna a quantidade de documentos na coleção `col_alunos`
                #       onde o campo "turma" corresponde ao nome da turma atual.
                count_alunos = col_alunos.count_documents({"turma": turma["nome_turma"]})

                # Insere os dados da turma na `Treeview`, criando uma nova
                #       linha com as informações da turma.
                # `"end"` adiciona o item no final da lista.
                # Os valores exibidos são:
                # - `str(turma["_id"])`: Converte o ID único da turma para string.
                # - `turma["nome_turma"]`: Nome da turma.
                # - `turma["ano"]`: Ano letivo da turma.
                # - `turma["serie"]`: Série da turma.
                # - `turma["turno"]`: Período em que a turma funciona (Manhã, Tarde ou Noite).
                # - `count_alunos`: Número de alunos matriculados na turma.
                tree.insert("", "end", values=(
                    str(turma["_id"]),
                    turma["nome_turma"],
                    turma["ano"],
                    turma["serie"],
                    turma["turno"],
                    count_alunos))


        # Cria um botão para aplicar o filtro e atualizar a lista de turmas.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=atualizar_lista_turmas` associa a função `atualizar_lista_turmas` ao
        #       botão, que será executada ao clicar.
        # `row=0, column=2` define a posição do botão na grade do `top_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(top_frame,
                   text="Filtrar",
                   command=atualizar_lista_turmas).grid(row=0, column=2, padx=5)

        # Cria um botão para limpar o filtro e recarregar a lista de turmas.
        # `text="Limpar"` define o texto exibido no botão.
        # `command=lambda: [filtro_turma.delete(0, 'end'), atualizar_lista_turmas()]`
        #       associa uma função anônima (lambda) ao botão.
        # Essa função executa duas ações ao clicar no botão:
        # 1. `filtro_turma.delete(0, 'end')` limpa o campo de entrada do filtro.
        # 2. `atualizar_lista_turmas()` recarrega a lista de turmas sem filtros.
        # `row=0, column=3` define a posição do botão na grade do `top_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(top_frame,
                   text="Limpar",
                   command=lambda: [filtro_turma.delete(0, 'end'),
                                    atualizar_lista_turmas()]).grid(row=0, column=3, padx=5)

        # Cria um frame para organizar e conter a árvore de visualização (`Treeview`).
        # `tk.Frame(janela, bg='#f0f0f0')` cria um frame dentro da janela
        #       principal com cor de fundo cinza claro (`#f0f0f0`).
        tree_frame = tk.Frame(janela, bg='#f0f0f0')

        # `pack(pady=10, fill='both', expand=True)` define a posição do frame na interface:
        # - `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do frame.
        # - `fill='both'` permite que o frame se expanda horizontal e verticalmente
        #       para ocupar todo o espaço disponível.
        # - `expand=True` faz com que o frame ocupe todo o espaço disponível
        #       quando a janela for redimensionada.
        tree_frame.pack(pady=10, fill='both', expand=True)

        # Define as colunas da tabela que será exibida na interface.
        # Cada elemento da tupla representa uma coluna na `Treeview`.
        colunas = ("id", "Nome Turma", "Ano", "Série", "Turno", "Qtd Alunos")

        # Cria a árvore de visualização (`Treeview`) para exibir os dados das turmas.
        # `tree_frame` define o frame onde a `Treeview` será inserida.
        # `columns=colunas` define as colunas que serão exibidas na tabela.
        # `show="headings"` remove a coluna padrão e exibe apenas os cabeçalhos das colunas.
        # `selectmode="browse"` permite selecionar apenas uma linha por vez.
        tree = ttk.Treeview(tree_frame, columns=colunas, show="headings", selectmode="browse")

        # Percorre a lista de colunas e configura os cabeçalhos e
        #       largura das colunas.
        for c in colunas:

            # `tree.heading(c, text=c)` define o nome do cabeçalho da
            #       coluna com o próprio nome da coluna.
            tree.heading(c, text=c)

            # `tree.column(c, width=220)` define a largura da coluna para 220 pixels.
            tree.column(c, width=220)

        # Exibe a árvore (`Treeview`) na interface.
        # `fill='both'` permite que o widget expanda tanto horizontal quanto verticalmente.
        # `expand=True` faz com que o widget ocupe todo o espaço disponível na interface.
        tree.pack(fill='both', expand=True)

        # Atualiza a lista de turmas carregando os dados do banco de dados.
        atualizar_lista_turmas()

        # Cria um frame para os botões de controle (Adicionar, Editar e Excluir turmas).
        # `tk.Frame(janela, bg='#f0f0f0', pady=10)` cria o frame com
        #       cor de fundo cinza claro (`#f0f0f0`).
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        btn_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # `pack()` adiciona o frame à interface.
        btn_frame.pack()

        # Define a função `adicionar_turma`, responsável por abrir uma
        #       nova janela para adicionar uma turma.
        def adicionar_turma():

            # Cria uma nova janela (`Toplevel`) para adicionar uma turma.
            win = Toplevel(janela)

            # Define o título da janela como "Adicionar Turma".
            win.title("Adicionar Turma")

            # Define a cor de fundo da janela como cinza claro (`#f0f0f0`).
            win.configure(bg='#f0f0f0')  # Cor: Cinza claro

            # Centraliza a janela na tela com dimensões de 500x450 pixels.
            centralizar_janela(win, 500, 450)

            # Define a nova janela como dependente da janela principal (`janela`).
            # Isso impede que o usuário interaja com a janela principal
            #       enquanto essa está aberta.
            win.transient(janela)

            # Bloqueia interações com outras janelas até que essa seja fechada.
            win.grab_set()

            # Cria um frame rotulado (`LabelFrame`) dentro da janela para
            #       conter o formulário de cadastro.
            # `text="Cadastro de Turma"` define o título do frame.
            # `padding=(20,10)` adiciona um espaçamento interno de 20 pixels
            #       nas laterais e 10 pixels no topo e na base.
            form = ttk.LabelFrame(win, text="Cadastro de Turma", padding=(20, 10))

            # Adiciona o frame à janela e expande para ocupar todo o espaço disponível.
            # `fill='both'` permite expansão horizontal e vertical.
            # `expand=True` garante que o frame preencha completamente a janela.
            # `padx=20, pady=20` adiciona 20 pixels de espaçamento externo
            #       nas laterais e no topo/base.
            form.pack(fill='both', expand=True, padx=20, pady=20)

            # Define uma lista de campos que serão usados no formulário
            #       para cadastrar uma turma.
            # Cada tupla contém o rótulo do campo e um valor inicial vazio.
            campos = [("Nome da Turma:", ""),
                      ("Ano:", ""),
                      ("Série:", ""),
                      ("Turno:", ""),
                      ("Professor Responsável:", ""),
                      ("Capacidade:", "")]

            # Cria um dicionário para armazenar as entradas do formulário.
            entries = {}

            # Percorre a lista de campos e cria os elementos de
            #       interface gráfica correspondentes.
            for i, (lbl, _) in enumerate(campos):

                # Cria um rótulo (`Label`) para cada campo do formulário.
                # `text=lbl` define o texto do rótulo.
                # `grid(row=i, column=0, sticky='e')` posiciona o rótulo na coluna 0, alinhado à direita.
                # `padx=10, pady=5` adiciona espaçamento externo ao rótulo para melhor visualização.
                ttk.Label(form,
                          text=lbl).grid(row=i, column=0, sticky='e', padx=10, pady=5)

                # Se o campo for "Professor Responsável:", cria um
                #       `Combobox` com os nomes dos professores.
                if lbl == "Professor Responsável:":

                    # Cria um `Combobox` preenchido com os nomes dos
                    #       professores cadastrados.
                    # `values=obter_nomes_professores()` preenche o combo com os
                    #       nomes retornados pela função.
                    # `width=30` define a largura do campo.
                    # `state="readonly"` impede que o usuário digite valores
                    #       manuais, permitindo apenas seleção.
                    cb = ttk.Combobox(form,
                                      values=obter_nomes_professores(),
                                      width=30,
                                      state="readonly")

                    # Posiciona o `Combobox` na grade da interface, na coluna 1.
                    # `sticky='w'` alinha o campo à esquerda.
                    # `padx=10, pady=5` adiciona espaçamento externo.
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena o campo no dicionário `entries` para futura referência.
                    entries[lbl] = cb

                # Se o campo for "Série:", cria um `Combobox` para
                #       seleção da série da turma.
                elif lbl == "Série:":

                    # `values=obter_series()` obtém a lista de séries disponíveis no banco de dados.
                    # Isso garante que apenas séries cadastradas possam ser selecionadas.
                    # `width=30` define a largura do campo de seleção para melhor visualização.
                    # `state="readonly"` impede que o usuário digite valores,
                    #       permitindo apenas escolher da lista.
                    cb = ttk.Combobox(form,
                                      values=obter_series(),
                                      width=30,
                                      state="readonly")

                    # Posiciona o `Combobox` na interface gráfica.
                    # `row=i` define que o campo será colocado na mesma linha
                    #       correspondente ao índice `i`.
                    # `column=1` posiciona o campo na segunda coluna da grade, ao
                    #       lado do rótulo correspondente.
                    # `sticky='w'` alinha o campo à esquerda da célula da grade.
                    # `padx=10, pady=5` adiciona um espaçamento de 10 pixels na
                    #       horizontal e 5 pixels na vertical
                    #       para melhorar o layout e a organização dos elementos.
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # O `Combobox` criado é armazenado no dicionário `entries` usando a
                    #       chave correspondente ao rótulo.
                    # Isso facilita a recuperação posterior do valor selecionado
                    #       quando o usuário preencher o formulário.
                    entries[lbl] = cb

                # Se o campo for "Turno:", cria um `Combobox` para
                #       seleção do turno da turma.
                elif lbl == "Turno:":

                    # `values=obter_turnos()` retorna uma lista de turnos
                    #       disponíveis (ex: Manhã, Tarde, Noite).
                    # Assim, o usuário pode escolher entre os turnos cadastrados.
                    # `width=30` mantém a largura do campo padrão do formulário.
                    # `state="readonly"` impede a entrada manual de texto, limitando as
                    #       escolhas à lista fornecida.
                    cb = ttk.Combobox(form,
                                      values=obter_turnos(),
                                      width=30,
                                      state="readonly")

                    # Posiciona o `Combobox` na interface, garantindo alinhamento adequado.
                    # `row=i, column=1` coloca o campo na linha correspondente e na segunda coluna.
                    # `sticky='w'` mantém o campo alinhado à esquerda da célula da grade.
                    # `padx=10, pady=5` adiciona espaçamento horizontal e vertical para melhor estética.
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # O `Combobox` é salvo no dicionário `entries` com a
                    #       chave correspondente ao rótulo do campo.
                    # Isso facilita a obtenção do valor posteriormente
                    #       para salvar no banco de dados.
                    entries[lbl] = cb

                # Para os demais campos do formulário, cria um campo de entrada (`Entry`).
                else:

                    # Cria um `Entry` (campo de entrada de texto) para os
                    #       campos que não são `Combobox`.
                    # `width=30` define uma largura adequada para facilitar a digitação.
                    ent = ttk.Entry(form, width=30)

                    # Posiciona o campo de entrada na interface gráfica.
                    # `row=i, column=1` coloca o campo na linha correta e na segunda coluna.
                    # `sticky='w'` alinha o campo à esquerda da célula da grade.
                    # `padx=10, pady=5` adiciona espaçamento horizontal e
                    #       vertical para melhor organização.
                    ent.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # O campo de entrada (`Entry`) é salvo no dicionário `entries`
                    #       usando o rótulo como chave.
                    # Isso facilita a recuperação dos dados digitados quando o
                    #       usuário preencher o formulário.
                    entries[lbl] = ent

            # Define a função `salvar_turma`, responsável por salvar uma
            #       nova turma no banco de dados.
            def salvar_turma():

                # Tenta converter os valores dos campos "Ano" e "Capacidade" para inteiros.
                try:

                    # `int(entries["Ano:"].get())` converte o valor digitado no
                    #       campo "Ano:" para um número inteiro.
                    # Isso garante que o ano seja armazenado corretamente como
                    #       um número e não como texto.
                    ano = int(entries["Ano:"].get())

                    # `int(entries["Capacidade:"].get())` converte o valor do
                    #       campo "Capacidade:" para inteiro.
                    # Isso evita que sejam inseridos valores inválidos, garantindo
                    #       que a capacidade seja um número.
                    capacidade = int(entries["Capacidade:"].get())

                # Captura o erro caso o usuário insira valores inválidos
                #       (exemplo: letras ou espaços em branco).
                except ValueError:

                    # Exibe uma mensagem de erro informando que os campos "Ano" e
                    #       "Capacidade" devem ser números inteiros.
                    messagebox.showerror("Erro",
                                         "Ano e Capacidade devem ser números inteiros.")

                    # Retorna imediatamente, impedindo que a turma seja
                    #       salva com valores inválidos.
                    return

                # Cria um dicionário `doc` que representa a nova turma a
                #       ser salva no banco de dados.
                doc = {

                    # Obtém o nome da turma digitado pelo usuário e armazena no
                    #       dicionário com a chave "nome_turma".
                    "nome_turma": entries["Nome da Turma:"].get(),

                    # Armazena o ano da turma, convertido para inteiro,
                    #       garantindo consistência nos dados.
                    "ano": ano,

                    # Obtém a série da turma selecionada no `Combobox` e armazena no dicionário.
                    "serie": entries["Série:"].get(),

                    # Obtém o turno selecionado no `Combobox` e armazena no dicionário.
                    "turno": entries["Turno:"].get(),

                    # Obtém o nome do professor responsável selecionado no `Combobox` e salva no dicionário.
                    "professor_responsavel": entries["Professor Responsável:"].get(),

                    # Armazena a capacidade máxima de alunos permitidos na
                    #       turma, convertida para inteiro.
                    "capacidade": capacidade

                }

                # Insere o dicionário `doc` no banco de dados na coleção `col_turmas`.
                # Isso salva a nova turma cadastrada com os dados informados pelo usuário.
                col_turmas.insert_one(doc)

                # Exibe uma mensagem informando que a turma foi cadastrada com sucesso.
                messagebox.showinfo("Sucesso", "Turma cadastrada!")

                # Fecha a janela de cadastro de turma após a inserção bem-sucedida.
                win.destroy()

                # Atualiza a lista de turmas na interface para incluir a
                #       nova turma cadastrada.
                atualizar_lista_turmas()

            # Cria um botão para salvar a turma cadastrada.
            # `text="Salvar"` define o texto exibido no botão.
            # `command=salvar_turma` associa a função `salvar_turma` ao botão.
            # `row=len(campos), column=0, columnspan=2` define a posição do
            #       botão na grade e o espaço que ele ocupa.
            # `pady=20` adiciona 20 pixels de espaçamento vertical ao redor do botão.
            ttk.Button(form,
                       text="Salvar",
                       command=salvar_turma).grid(row=len(campos), column=0, columnspan=2, pady=20)



        # Define a função para editar uma turma existente no banco de dados.
        def editar_turma():

            # Obtém o item selecionado na árvore (`Treeview`).
            selecionado = tree.focus()

            # Se nenhum item estiver selecionado, exibe um
            #       aviso e interrompe a função.
            if not selecionado:
                messagebox.showwarning("Atenção", "Selecione uma turma para editar.")
                return

            # Obtém os valores da linha selecionada na árvore.
            valores = tree.item(selecionado, "values")

            # O primeiro valor da linha representa o ID da turma.
            turma_id = valores[0]

            # Busca a turma no banco de dados utilizando o ID obtido.
            turma = obter_turma_por_id(turma_id)

            # Se a turma não for encontrada, exibe um
            #       erro e interrompe a função.
            if not turma:
                messagebox.showerror("Erro", "Turma não encontrada.")
                return

            # Cria uma nova janela para edição da turma.
            # `Toplevel(janela)` define a nova janela como uma
            #       subjanela da janela principal.
            win = Toplevel(janela)

            # Define o título da janela como "Editar Turma".
            # `title("Editar Turma")` exibe o nome da janela no topo.
            win.title("Editar Turma")

            # Configura a cor de fundo da janela.
            # `bg='#f0f0f0'` define a cor de fundo como cinza claro.
            win.configure(bg='#f0f0f0')  # Cor: Cinza Claro

            # Centraliza a janela na tela com tamanho fixo.
            # `centralizar_janela(win, 500, 450)` ajusta a posição da janela.
            centralizar_janela(win, 500, 450)

            # Define a janela como dependente da janela principal.
            # `transient(janela)` impede que a janela principal seja
            #       usada enquanto esta estiver aberta.
            win.transient(janela)

            # Bloqueia interações com outras janelas até que esta seja fechada.
            # `grab_set()` impede que o usuário clique fora da janela.
            win.grab_set()

            # Cria um contêiner com uma borda e um título para
            #       organizar os campos de edição da turma.
            # `text="Editar Turma"` define o título do quadro.
            # `padding=(20,10)` adiciona espaço interno ao redor dos campos.
            form = ttk.LabelFrame(win, text="Editar Turma", padding=(20, 10))

            # Posiciona o contêiner na janela.
            # `fill='both'` faz com que ele expanda na horizontal e vertical.
            # `expand=True` permite que ele ocupe todo o espaço disponível.
            # `padx=20, pady=20` adiciona espaço ao redor do contêiner.
            form.pack(fill='both', expand=True, padx=20, pady=20)

            # Define os campos do formulário de edição da turma.
            # Cada campo é uma tupla contendo o rótulo do campo e o
            #       valor correspondente da turma selecionada.
            campos = [("Nome da Turma:", turma["nome_turma"]),  # Nome da turma cadastrada
                      ("Ano:", turma["ano"]),  # Ano letivo da turma
                      ("Série:", turma["serie"]),  # Série correspondente à turma
                      ("Turno:", turma["turno"]),  # Turno (Manhã, Tarde ou Noite)
                      ("Professor Responsável:", turma["professor_responsavel"]),
                      # Nome do professor responsável pela turma
                      ("Capacidade:", turma["capacidade"])]  # Quantidade máxima de alunos na turma

            # Dicionário para armazenar as entradas dos campos do formulário.
            # As chaves são os rótulos dos campos e os valores
            #       são os widgets correspondentes.
            entries = {}

            # Percorre a lista de campos, criando os rótulos e os
            #       campos de entrada correspondentes
            for i, (lbl, val) in enumerate(campos):

                # Cria um rótulo (label) para cada campo do formulário
                # `text=lbl` define o texto do rótulo como o nome do campo
                # `grid(row=i, column=0, sticky='e', padx=10, pady=5)` posiciona o
                #       rótulo na grade, alinhado à direita
                ttk.Label(form,
                          text=lbl).grid(row=i, column=0, sticky='e', padx=10, pady=5)

                # Se o campo for "Professor Responsável:", cria um Combobox
                #       para selecionar um professor
                if lbl == "Professor Responsável:":

                    # Cria um Combobox preenchido com a lista de professores obtida do banco de dados
                    # `state="readonly"` impede a edição manual do campo,
                    #       permitindo apenas a seleção de um item da lista
                    cb = ttk.Combobox(form,
                                      values=obter_nomes_professores(),
                                      width=30, state="readonly")

                    # Define o valor atual do Combobox como o professor
                    #       responsável já cadastrado na turma
                    cb.set(val)

                    # Posiciona o Combobox na interface
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena o campo no dicionário `entries`
                    entries[lbl] = cb

                # Se o campo for "Série:", cria um Combobox para permitir que o
                #       usuário selecione a série da turma
                elif lbl == "Série:":

                    # Cria um Combobox (`ttk.Combobox`) preenchido com as
                    #       séries disponíveis no banco de dados
                    # `values=obter_series()` chama a função que retorna a lista de séries cadastradas
                    # `width=30` define a largura do Combobox
                    # `state="readonly"` impede a edição manual do campo, permitindo
                    #       apenas a seleção de um item da lista
                    cb = ttk.Combobox(form,
                                      values=obter_series(),
                                      width=30,
                                      state="readonly")

                    # Define o valor padrão do Combobox como a série já cadastrada na turma
                    cb.set(val)

                    # Posiciona o Combobox na interface utilizando o `grid()`
                    # `row=i` posiciona na mesma linha do rótulo correspondente
                    # `column=1` coloca o campo na segunda coluna, ao lado do rótulo
                    # `sticky='w'` alinha o campo à esquerda da célula
                    # `padx=10, pady=5` adiciona espaçamento horizontal e
                    #       vertical para melhor visualização
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena o campo no dicionário `entries`, associando o
                    #       rótulo ao Combobox
                    entries[lbl] = cb

                # Se o campo for "Turno:", cria um Combobox para permitir
                #       que o usuário selecione o turno da turma
                elif lbl == "Turno:":

                    # Cria um Combobox preenchido com a lista de turnos disponíveis
                    # `values=obter_turnos()` retorna os turnos cadastrados na base de dados
                    # `width=30` define a largura do Combobox
                    # `state="readonly"` impede a edição manual, permitindo apenas a
                    #       escolha entre as opções listadas
                    cb = ttk.Combobox(form,
                                      values=obter_turnos(),
                                      width=30,
                                      state="readonly")

                    # Define o valor inicial do Combobox como o turno
                    #       já cadastrado para a turma
                    cb.set(val)

                    # Posiciona o Combobox na interface utilizando o `grid()`
                    # `row=i` garante que o campo fique alinhado com o rótulo correspondente
                    # `column=1` posiciona o Combobox na segunda coluna, ao lado do rótulo
                    # `sticky='w'` alinha o campo à esquerda
                    # `padx=10, pady=5` adiciona espaçamento para uma
                    #       melhor organização visual
                    cb.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena o campo no dicionário `entries`, associando o rótulo ao Combobox
                    entries[lbl] = cb

                # Para os demais campos (não sendo "Série" nem "Turno"), cria
                #       um campo de entrada (`Entry`)
                else:

                    # Cria um campo de entrada de texto (`Entry`) para inserção manual de dados
                    # `width=30` define a largura do campo para manter uma boa legibilidade
                    ent = ttk.Entry(form, width=30)

                    # Define o valor inicial do campo como o valor já cadastrado na turma
                    # `insert(0, val)` insere o valor da turma na posição
                    #       inicial do campo de entrada
                    ent.insert(0, val)

                    # Posiciona o campo de entrada na interface utilizando o `grid()`
                    # `row=i` garante que o campo fique alinhado com o rótulo correspondente
                    # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo
                    # `sticky='w'` alinha o campo à esquerda da célula
                    # `padx=10, pady=5` adiciona espaçamento horizontal e vertical
                    ent.grid(row=i, column=1, sticky='w', padx=10, pady=5)

                    # Armazena o campo no dicionário `entries`, associando o
                    #       rótulo ao campo de entrada
                    entries[lbl] = ent

            # Define a função `atualizar_turma`, responsável por atualizar os
            #       dados de uma turma no banco de dados.
            def atualizar_turma():

                # Tenta converter os valores dos campos "Ano" e "Capacidade" para inteiros.
                try:

                    # Converte o valor do campo "Ano:" para um número inteiro.
                    # Se o usuário inserir um valor inválido (não numérico), a
                    #       conversão lançará um erro.
                    ano = int(entries["Ano:"].get())

                    # Converte o valor do campo "Capacidade:" para um número inteiro.
                    # Esse campo representa a quantidade máxima de alunos na turma.
                    capacidade = int(entries["Capacidade:"].get())

                # Se houver um erro na conversão (por exemplo, o usuário
                #       digitou letras em vez de números).
                except ValueError:

                    # Exibe uma mensagem de erro para o usuário informando que apenas
                    #       números inteiros são aceitos.
                    # `messagebox.showerror()` exibe uma janela de erro com um título e
                    #       uma mensagem explicativa.
                    messagebox.showerror("Erro",
                                         "Ano e Capacidade devem ser números inteiros.")

                    # Sai da função sem realizar mais nenhuma ação.
                    return

                # Atualiza o documento da turma no banco de dados com os novos
                #       valores inseridos pelo usuário.
                # O método `update_one` é utilizado para encontrar o registro
                #       correspondente e atualizar os campos necessários.
                col_turmas.update_one(

                    # Filtra a turma pelo seu identificador único (`_id`).
                    {"_id": ObjectId(turma_id)},

                    # Define os novos valores para os campos da turma.
                    {"$set": {

                        # Atualiza o nome da turma com o valor inserido no campo correspondente.
                        "nome_turma": entries["Nome da Turma:"].get(),

                        # Atualiza o ano da turma, que já foi convertido para
                        #       inteiro anteriormente.
                        "ano": ano,

                        # Atualiza a série da turma com o valor selecionado no `Combobox`.
                        "serie": entries["Série:"].get(),

                        # Atualiza o turno da turma com o valor selecionado no `Combobox`.
                        "turno": entries["Turno:"].get(),

                        # Atualiza o professor responsável pela turma com o nome
                        #       selecionado no `Combobox`.
                        "professor_responsavel": entries["Professor Responsável:"].get(),

                        # Atualiza a capacidade máxima de alunos, que já foi
                        #       convertida para inteiro anteriormente.
                        "capacidade": capacidade

                    }}
                )

                # Exibe uma mensagem informando que a atualização foi realizada com sucesso.
                # `messagebox.showinfo()` cria uma janela pop-up com título e mensagem de confirmação.
                messagebox.showinfo("Sucesso", "Turma atualizada!")

                # Fecha a janela de edição após a atualização dos dados.
                win.destroy()

                # Atualiza a lista de turmas na interface gráfica para refletir as
                #       mudanças no banco de dados.
                atualizar_lista_turmas()

            # Cria um botão para salvar as alterações feitas na turma.
            # `text="Salvar Alterações"` define o texto exibido no botão.
            # `command=atualizar_turma` associa a ação de chamar a
            #       função `atualizar_turma` quando o botão for clicado.
            # `row=len(campos)` posiciona o botão na última linha da grade,
            #       abaixo dos campos de entrada.
            # `column=0` posiciona o botão na primeira coluna da grade.
            # `columnspan=2` faz com que o botão ocupe duas colunas,
            #       centralizando-o na interface.
            # `pady=20` adiciona 20 pixels de espaçamento vertical ao
            #       redor do botão para melhorar a aparência.
            ttk.Button(form,
                       text="Salvar Alterações",
                       command=atualizar_turma).grid(row=len(campos),
                                                     column=0,
                                                     columnspan=2,
                                                     pady=20)


        # Define a função `excluir_turma` para remover uma
        #       turma do banco de dados.
        def excluir_turma():

            # Obtém a turma selecionada na interface.
            selecionado = tree.focus()

            # Verifica se alguma turma foi selecionada. Se não,
            #       exibe um alerta ao usuário.
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione uma turma para excluir.")
                return

            # Obtém os valores da turma selecionada na árvore de dados (`Treeview`).
            valores = tree.item(selecionado, "values")

            # Obtém o ID da turma a partir dos valores extraídos.
            turma_id = valores[0]

            # Exibe uma caixa de diálogo de confirmação para garantir
            #       que o usuário deseja excluir a turma.
            if messagebox.askyesno("Confirmação", "Excluir esta turma?"):

                # Remove a turma do banco de dados MongoDB com base no seu ID.
                col_turmas.delete_one({"_id": ObjectId(turma_id)})

                # Exibe uma mensagem informando que a exclusão foi bem-sucedida.
                messagebox.showinfo("Sucesso", "Turma excluída!")

                # Atualiza a lista de turmas exibida na interface
                #       para refletir a remoção.
                atualizar_lista_turmas()

                # Permanece na mesma tela após o clique em “OK” do messagebox.
                janela.lift()


        # Cria um botão para adicionar uma nova turma.
        # `text="Adicionar Turma"` define o texto exibido no botão.
        # `command=adicionar_turma` associa a função `adicionar_turma` ao botão.
        # `row=0, column=0` posiciona o botão na grade na primeira linha e primeira coluna.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal entre os botões.
        ttk.Button(btn_frame,
                   text="Adicionar Turma",
                   command=adicionar_turma).grid(row=0, column=0, padx=5)

        # Cria um botão para editar uma turma existente.
        # `text="Editar Turma"` define o texto exibido no botão.
        # `command=editar_turma` associa a função `editar_turma` ao botão.
        # `row=0, column=1` posiciona o botão na grade na primeira linha e segunda coluna.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal entre os botões.
        ttk.Button(btn_frame,
                   text="Editar Turma",
                   command=editar_turma).grid(row=0, column=1, padx=5)

        # Cria um botão para excluir uma turma selecionada.
        # `text="Excluir Turma"` define o texto exibido no botão.
        # `command=excluir_turma` associa a função `excluir_turma` ao botão.
        # `row=0, column=2` posiciona o botão na grade na primeira linha e terceira coluna.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal entre os botões.
        ttk.Button(btn_frame,
                   text="Excluir Turma",
                   command=excluir_turma).grid(row=0, column=2, padx=5)



    # ---------- Gerenciamento de Notas ----------
    # Define a função para abrir a janela de gerenciamento de notas.
    def abrir_janela_notas(self):

        # Cria uma nova janela para gerenciamento de notas.
        # `Toplevel(self.root)` cria uma janela secundária vinculada à janela principal.
        janela = Toplevel(self.root)

        # Define o título da janela como "Lançamento e Gerenciamento de Notas".
        janela.title("Lançamento e Gerenciamento de Notas")

        # Maximiza a janela para ocupar toda a tela.
        # `state('zoomed')` ajusta a janela para tela cheia automaticamente.
        janela.state('zoomed')

        # Define a cor de fundo da janela como um tom cinza claro.
        # `bg='#f0f0f0'` corresponde à cor cinza claro para um visual mais agradável.
        janela.configure(bg='#f0f0f0')

        # Cria um frame superior para conter os filtros de pesquisa.
        # `tk.Frame(janela, bg='#f0f0f0', pady=10)` define o frame com cor de
        #       fundo cinza claro e um espaçamento vertical de 10 pixels.
        top_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Expande o frame horizontalmente para ocupar toda a largura da janela.
        # `fill='x'` faz com que o frame se expanda apenas na horizontal.
        top_frame.pack(fill='x')

        # Cria um rótulo para identificar o campo de seleção de turma.
        # `text="Turma:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0, padx=5, sticky='e')` posiciona o
        #       rótulo na linha 0, coluna 0, com espaçamento horizontal
        #       de 5 pixels, alinhado à direita.
        ttk.Label(top_frame,
                  text="Turma:").grid(row=0, column=0, padx=5, sticky='e')

        # Cria um Combobox para selecionar uma turma.
        # `values=obter_nomes_turmas()` preenche a lista com os
        #       nomes das turmas obtidas da base de dados.
        # `width=30` define a largura do campo de seleção.
        # `state="readonly"` impede que o usuário digite valores
        #       manuais, permitindo apenas a seleção da lista.
        turma_combo = ttk.Combobox(top_frame,
                                   values=obter_nomes_turmas(),
                                   width=30,
                                   state="readonly")

        # Posiciona o Combobox na interface.
        # `grid(row=0, column=1, padx=5)` coloca o campo na linha 0,
        #       coluna 1, com espaçamento horizontal de 5 pixels.
        turma_combo.grid(row=0, column=1, padx=5)


        # Define a função para atualizar a lista de alunos na interface.
        def atualizar_alunos():

            # Remove todos os itens existentes na árvore antes de inserir novos dados.
            # `get_children()` retorna todos os itens da Treeview.
            # `delete(i)` remove cada item individualmente.
            for i in tree.get_children():
                tree.delete(i)

            # Inicializa um dicionário vazio para armazenar os critérios de busca.
            query = {}

            # Verifica se o usuário selecionou uma turma no Combobox.
            # Se uma turma foi selecionada, filtra os alunos dessa turma específica.
            if turma_combo.get():
                query["turma"] = turma_combo.get()

            # Percorre todos os alunos encontrados na coleção `col_alunos`
            #       com base na consulta `query`.
            for aluno in col_alunos.find(query):

                # Insere os dados do aluno na Treeview.
                # `str(aluno["_id"])` converte o ID do aluno para string.
                # `aluno["nome"]` representa o nome do aluno.
                # `aluno["matricula"]` representa o número de matrícula do aluno.
                tree.insert("",
                            "end",
                            values=(str(aluno["_id"]), aluno["nome"], aluno["matricula"]))


        # Cria um botão para listar os alunos da turma selecionada.
        # `text="Listar Alunos da Turma"` define o texto exibido no botão.
        # `command=atualizar_alunos` associa a função `atualizar_alunos` ao botão.
        # `row=0, column=2` define a posição do botão na grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(top_frame,
                   text="Listar Alunos da Turma",
                   command=atualizar_alunos).grid(row=0, column=2, padx=5)

        # Cria um frame para conter a tabela (Treeview) dos alunos.
        # `bg='#f0f0f0'` define a cor de fundo do frame como cinza claro.
        tree_frame = tk.Frame(janela, bg='#f0f0f0')

        # Adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        # `fill='both'` faz com que o frame expanda tanto em largura quanto em altura.
        # `expand=True` permite que o frame ocupe todo o espaço disponível dentro da janela.
        tree_frame.pack(pady=10, fill='both', expand=True)

        # Define as colunas da tabela.
        # `"id"` representa o identificador único do aluno no banco de dados.
        # `"Nome"` representa o nome completo do aluno.
        # `"Matrícula"` representa o número de matrícula do aluno.
        colunas = ("id", "Nome", "Matrícula")

        # Cria uma Treeview (tabela interativa) para exibir a lista de alunos.
        # `columns=colunas` define quais colunas estarão presentes na tabela.
        # `show="headings"` faz com que apenas os cabeçalhos das colunas
        #       sejam exibidos, sem a coluna de índice.
        # `selectmode="browse"` permite que apenas uma linha seja selecionada por vez.
        tree = ttk.Treeview(tree_frame,
                            columns=colunas,
                            show="headings",
                            selectmode="browse")

        # Percorre todas as colunas da Treeview e define o nome do
        #       cabeçalho e a largura das colunas.
        for c in colunas:

            # Define o nome do cabeçalho da coluna como o próprio nome da coluna.
            tree.heading(c, text=c)

            # Define a largura padrão de cada coluna como 220 pixels.
            tree.column(c, width=220)

        # Adiciona a tabela Treeview ao frame.
        # `fill='both'` faz com que a tabela expanda tanto na
        #       largura quanto na altura do frame.
        # `expand=True` permite que a tabela ocupe todo o
        #       espaço disponível no frame.
        tree.pack(fill='both', expand=True)

        # Cria um frame para os botões de ações relacionadas às notas.
        # `bg='#f0f0f0'` define a cor de fundo do frame como cinza claro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do frame.
        btn_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o frame na interface.
        btn_frame.pack()


        # Define uma função para cadastrar ou editar as notas de um aluno selecionado.
        def cadastrar_editar_notas():

            # Obtém o item atualmente selecionado na Treeview.
            selecionado = tree.focus()

            # Verifica se algum aluno foi selecionado.
            if not selecionado:

                # Exibe um aviso caso nenhum aluno tenha sido selecionado.
                messagebox.showwarning("Atenção", "Selecione um aluno.")
                return

            # Obtém os valores do item selecionado na Treeview.
            valores = tree.item(selecionado, "values")

            # Extrai o ID e o nome do aluno dos valores obtidos.
            aluno_id, aluno_nome = valores[0], valores[1]

            # Cria uma nova janela (`Toplevel`) para cadastrar ou editar as notas do aluno.
            win = Toplevel(janela)

            # Define o título da janela com o nome do aluno.
            win.title("Cadastrar/Editar Notas - " + aluno_nome)

            # Define o tamanho da janela como 500x500 pixels e posiciona a janela
            #       na tela (500px da esquerda, 200px do topo).
            win.geometry("500x500+500+200")

            # Define a janela como filha da janela principal para que não possa
            #       ser acessada enquanto estiver aberta.
            win.transient(janela)

            # Bloqueia a interação com a janela principal até que esta seja fechada.
            win.grab_set()

            # Define a cor de fundo da janela como cinza claro (`#f0f0f0`).
            win.configure(bg='#f0f0f0')

            # Cria um rótulo (`Label`) para exibir o nome do aluno na janela de edição de notas.
            # `text=f"Aluno: {aluno_nome}"` define o texto do rótulo com o nome do aluno.
            # `font=("Arial", 13, "bold")` define a fonte como Arial, tamanho 13 e em negrito.
            # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
            ttk.Label(win, text=f"Aluno: {aluno_nome}", font=("Arial", 13, "bold")).pack(pady=5)

            # Cria um frame (`Frame`) para organizar os campos do formulário dentro da janela.
            # `bg='#f0f0f0'` define a cor de fundo do frame como cinza claro.
            form_frame = tk.Frame(win, bg='#f0f0f0')

            # Posiciona o frame dentro da janela com espaçamento vertical de 10 pixels.
            form_frame.pack(pady=10)

            # Cria um rótulo (`Label`) para indicar o campo de seleção de disciplina.
            # `text="Disciplina:"` define o texto exibido no rótulo.
            # `grid(row=0, column=0, padx=5, pady=5, sticky='e')`
            #       posiciona o rótulo na linha 0, coluna 0,
            #       adiciona espaçamento de 5 pixels nas laterais e fixa o
            #       alinhamento à direita ('e' de 'east').
            ttk.Label(form_frame,
                      text="Disciplina:").grid(row=0, column=0, padx=5, pady=5, sticky='e')

            # Cria um combobox (`Combobox`) para seleção de disciplina.
            # `values=obter_nomes_disciplinas()` preenche a lista com as
            #       disciplinas obtidas do banco de dados.
            # `width=30` define a largura do combobox.
            # `state="readonly"` impede que o usuário digite manualmente no
            #       campo, permitindo apenas seleção na lista.
            disc_combo = ttk.Combobox(form_frame,
                                      values=obter_nomes_disciplinas(),
                                      width=30,
                                      state="readonly")

            # Posiciona o combobox na linha 0, coluna 1,
            #       alinhado à esquerda ('w' de 'west').
            # Adiciona 5 pixels de espaçamento nas laterais e na vertical.
            disc_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')

            # Define uma lista de rótulos para os campos de
            #       entrada das notas dos bimestres.
            notas_labels = ["1º Bimestre:", "2º Bimestre:", "3º Bimestre:", "4º Bimestre:"]

            # Cria um dicionário para armazenar os campos de entrada de notas.
            entries = {}

            # Loop para criar os rótulos e campos de entrada das notas dos bimestres.
            # `enumerate(notas_labels, start=1)` percorre a lista de
            #       rótulos começando do índice 1.
            for i, lbl in enumerate(notas_labels, start=1):

                # Cria um rótulo (`Label`) para indicar o campo de entrada de nota correspondente.
                # `text=lbl` define o texto exibido no rótulo, que varia de acordo com o bimestre.
                # `grid(row=i, column=0, padx=5, pady=5, sticky='e')` posiciona o
                #       rótulo na linha correspondente ao índice, na coluna 0,
                #       adicionando espaçamento de 5 pixels e alinhamento à direita ('e' de 'east').
                ttk.Label(form_frame,
                          text=lbl).grid(row=i, column=0, padx=5, pady=5, sticky='e')

                # Cria um campo de entrada (`Entry`) para digitação da
                #       nota do bimestre correspondente.
                # `width=30` define a largura do campo de entrada.
                ent = ttk.Entry(form_frame, width=30)

                # Posiciona o campo de entrada na linha correspondente ao índice, na coluna 1,
                #       alinhado à esquerda ('w' de 'west'), com espaçamento
                #       de 5 pixels nas laterais e na vertical.
                ent.grid(row=i, column=1, padx=5, pady=5, sticky='w')

                # Armazena o campo de entrada no dicionário `entries`,
                #       usando o rótulo como chave.
                entries[lbl] = ent


            # Define a função que será chamada ao selecionar uma disciplina no combobox.
            def ao_selecionar_disciplina(event=None):

                # Obtém a disciplina selecionada no combobox.
                disc = disc_combo.get()

                # Se nenhuma disciplina for selecionada, interrompe a função.
                if not disc:
                    return

                # Procura no banco de dados se já existe uma nota cadastrada
                #       para o aluno na disciplina selecionada.
                nota_exist = col_notas.find_one({"id_aluno": ObjectId(aluno_id), "disciplina": disc})

                # Se existir uma nota cadastrada para a disciplina:
                if nota_exist:

                    # Limpa os campos de entrada das notas para evitar valores residuais.
                    for lbl in notas_labels:
                        entries[lbl].delete(0, 'end')

                    # Preenche os campos de entrada com as notas do banco de dados.
                    # `get()` é usado para garantir que, se o valor não
                    #       existir, um valor vazio seja inserido.
                    entries["1º Bimestre:"].insert(0, nota_exist.get("bimestre_1", ""))
                    entries["2º Bimestre:"].insert(0, nota_exist.get("bimestre_2", ""))
                    entries["3º Bimestre:"].insert(0, nota_exist.get("bimestre_3", ""))
                    entries["4º Bimestre:"].insert(0, nota_exist.get("bimestre_4", ""))

                # Se não houver notas cadastradas para a disciplina, garante
                #       que os campos de entrada fiquem vazios.
                else:

                    # Percorre todos os rótulos dos bimestres.
                    for lbl in notas_labels:

                        # Limpa o conteúdo dos campos de entrada, removendo qualquer
                        #       valor digitado anteriormente.
                        entries[lbl].delete(0, 'end')

            # Associa a função `ao_selecionar_disciplina` ao evento de
            #       seleção no combobox de disciplinas.
            # Quando o usuário seleciona uma disciplina, a função é
            #       chamada automaticamente.
            disc_combo.bind("<<ComboboxSelected>>", ao_selecionar_disciplina)

            # Função para salvar as notas do aluno no banco de dados.
            def salvar_notas():

                # Obtém a disciplina selecionada no combobox.
                disc = disc_combo.get()

                # Verifica se a disciplina foi escolhida, se não, exibe um
                #       aviso ao usuário e interrompe a função.
                if not disc:
                    messagebox.showwarning("Atenção",
                                           "Selecione a disciplina antes de salvar.")
                    return

                # Inicializa uma lista vazia para armazenar as notas dos bimestres.
                notas = []

                # Percorre a lista de labels dos bimestres para obter os
                #       valores digitados pelo usuário.
                for lbl in notas_labels:

                    # Obtém o valor digitado no campo de entrada correspondente ao bimestre atual.
                    # O método `.get()` recupera o texto inserido no campo de entrada (`Entry`).
                    # `.strip()` remove quaisquer espaços em branco no
                    #       início e no final do valor inserido.
                    valor = entries[lbl].get().strip()

                    # Verifica se o campo não está vazio. Apenas valores
                    #       preenchidos serão processados.
                    if valor:

                        try:

                            # Converte o valor digitado para um número decimal (`float`).
                            # Isso é necessário para garantir que as notas sejam processadas
                            #       corretamente no banco de dados.
                            notas.append(float(valor))

                        # Se a conversão falhar (por exemplo, se o usuário digitou
                        #       letras ou caracteres inválidos),
                        #        uma exceção `ValueError` será gerada.
                        except ValueError:

                            # Exibe uma mensagem de erro informando ao usuário que o valor inserido não é válido.
                            # A mensagem especifica qual campo (bimestre) contém o erro para facilitar a correção.
                            messagebox.showerror("Erro",
                                                 f"Valor inválido no campo {lbl}. Certifique-se de digitar um número válido.")

                            # Interrompe a execução da função, impedindo que valores inválidos
                            #       sejam salvos no banco de dados.
                            return

                # Verifica se nenhuma nota foi informada.
                if len(notas) == 0:

                    # Exibe uma mensagem de erro informando que pelo menos uma
                    #       nota deve ser digitada.
                    messagebox.showerror("Erro",
                                         "Informe pelo menos uma nota antes de salvar.")

                    # Interrompe a execução da função para evitar que registros
                    #       vazios sejam inseridos no banco de dados.
                    return

                # Calcula o total de faltas do aluno para a disciplina selecionada.
                # `col_faltas.find()` realiza uma consulta no banco de dados,
                #       retornando todos os registros de faltas
                #       para o aluno identificado por `aluno_id` e correspondente à
                #       disciplina selecionada (`disc`).
                # O `sum()` percorre os resultados retornados pela consulta e
                #       soma o valor da chave "quantidade_faltas"
                #       de cada registro encontrado.
                total_faltas = sum(

                    # `f.get("quantidade_faltas", 0)` acessa o campo "quantidade_faltas" de
                    #       cada registro encontrado.
                    # Caso o campo não esteja presente no documento, retorna 0 para evitar erros.
                    f.get("quantidade_faltas", 0)

                    # Itera sobre todos os registros de faltas do aluno filtrados pela disciplina informada.
                    for f in col_faltas.find({"id_aluno": ObjectId(aluno_id), "disciplina": disc})

                )

                # Chama a função `calcular_media_e_situacao()` para calcular a média
                #       das notas informadas e determinar a situação do aluno.
                # A função recebe a lista de notas e o total de faltas como parâmetros.
                media, situacao = calcular_media_e_situacao(notas, total_faltas)

                # Verifica se o aluno ultrapassou o limite de faltas permitido.

                # Se o total de faltas do aluno for igual ou superior a 10, ele
                #       será automaticamente reprovado por faltas,
                #       independentemente da média obtida nas provas.
                if total_faltas >= 10:

                    # Define a situação do aluno como "Reprovado por Faltas".
                    situacao = "Reprovado por Faltas"

                # Verifica se já existe um registro de notas para o aluno na
                #       disciplina selecionada.

                # `col_notas.find_one()` busca no banco de dados um documento
                #       correspondente ao aluno (`id_aluno`) e à
                #       disciplina (`disc`). Se existir, ele retorna o documento; caso contrário, retorna `None`.
                nota_exist = col_notas.find_one({"id_aluno": ObjectId(aluno_id), "disciplina": disc})

                # Se o aluno já possui notas cadastradas para a disciplina
                #       selecionada, as notas serão atualizadas.
                if nota_exist:

                    # Atualiza o documento existente no banco de dados com as
                    #       novas notas e a situação calculada.
                    col_notas.update_one(

                        # Localiza o documento pelo ID.
                        {"_id": nota_exist["_id"]},
                        {"$set": {

                            # Atualiza cada bimestre com a nova nota digitada ou mantém a
                            #       nota anterior caso o campo esteja vazio.
                            "bimestre_1": entries["1º Bimestre:"].get() or nota_exist.get("bimestre_1", ""),
                            "bimestre_2": entries["2º Bimestre:"].get() or nota_exist.get("bimestre_2", ""),
                            "bimestre_3": entries["3º Bimestre:"].get() or nota_exist.get("bimestre_3", ""),
                            "bimestre_4": entries["4º Bimestre:"].get() or nota_exist.get("bimestre_4", ""),

                            # Atualiza a média calculada com base nas notas fornecidas.
                            "media": media,

                            # Atualiza a situação do aluno (Aprovado, Recuperação ou Reprovado).
                            "situacao": situacao

                        }}
                    )

                    # Exibe uma mensagem informando que as notas foram atualizadas com sucesso.
                    messagebox.showinfo("Sucesso", "Notas atualizadas!")

                # Caso contrário, se o aluno ainda não possui notas cadastradas para
                #       essa disciplina, um novo registro será criado.
                else:

                    # Cria um novo documento com as informações do aluno e suas notas.
                    doc = {

                        # Associa a nota ao aluno usando o ID.
                        "id_aluno": ObjectId(aluno_id),

                        # Armazena a disciplina correspondente às notas.
                        "disciplina": disc,

                        # Registra as notas digitadas para cada bimestre.
                        "bimestre_1": entries["1º Bimestre:"].get(),
                        "bimestre_2": entries["2º Bimestre:"].get(),
                        "bimestre_3": entries["3º Bimestre:"].get(),
                        "bimestre_4": entries["4º Bimestre:"].get(),

                        # Armazena a média calculada com base nas notas fornecidas.
                        "media": media,

                        # Define a situação do aluno de acordo com a média e o número de faltas.
                        "situacao": situacao

                    }

                    # Insere o novo registro de notas no banco de dados.
                    col_notas.insert_one(doc)

                    # Exibe uma mensagem informando que as notas foram cadastradas com sucesso.
                    messagebox.showinfo("Sucesso", "Notas cadastradas!")

                # Fecha a janela de cadastro/edição de notas após a
                #       operação ser concluída com sucesso.
                win.destroy()

            # Cria um botão para salvar as notas digitadas.
            # `text="Salvar Notas"` define o texto exibido no botão.
            # `command=salvar_notas` associa a função `salvar_notas` ao botão,
            #       garantindo que as notas sejam armazenadas ao ser pressionado.
            # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do
            #       botão para melhor organização visual.
            ttk.Button(win,
                       text="Salvar Notas",
                       command=salvar_notas).pack(pady=10)


        # Define a função `listar_notas`, responsável por
        #       exibir as notas do aluno selecionado.
        def listar_notas():

            # Obtém o item atualmente selecionado na árvore (`tree`).
            selecionado = tree.focus()

            # Se nenhum item estiver selecionado, exibe um alerta informando
            #       que é necessário selecionar um aluno.
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione um aluno para listar notas.")

                # Sai da função para evitar erros.
                return

            # Obtém os valores associados ao item selecionado na `Treeview`.
            valores = tree.item(selecionado, "values")

            # Extrai o ID e o nome do aluno a partir dos valores retornados.
            aluno_id, aluno_nome = valores[0], valores[1]

            # Cria uma nova janela (`Toplevel`) para exibir as notas do aluno.
            win = Toplevel(janela)

            # Define o título da janela, incluindo o nome do aluno.
            win.title("Notas do Aluno: " + aluno_nome)

            # Define a janela para abrir maximizada (modo tela cheia).
            win.state('zoomed')

            # Define a cor de fundo da janela para um tom de
            #       cinza claro (`#f0f0f0` - Cinza Claro).
            win.configure(bg='#f0f0f0')

            # Cria um frame (`nt_frame`) dentro da janela `win` para
            #       organizar a interface das notas.
            # `bg='#f0f0f0'` define o fundo do frame na cor cinza claro.
            nt_frame = tk.Frame(win, bg='#f0f0f0')

            # Posiciona o frame na janela, adicionando um espaçamento vertical (`pady=10`).
            # `fill='both'` permite que o frame expanda tanto na largura quanto na altura.
            # `expand=True` faz com que o frame ocupe todo o espaço disponível.
            nt_frame.pack(pady=10, fill='both', expand=True)

            # Define as colunas da `Treeview` que será usada para exibir as notas do aluno.
            # As colunas representam as disciplinas e os bimestres, além da
            #       média e situação final do aluno.
            colunas_nt = ("Disciplina", "1º Bim", "2º Bim", "3º Bim", "4º Bim", "Média", "Situação")

            # Cria um widget `Treeview` dentro do `nt_frame`, utilizando as colunas definidas.
            # `show="headings"` significa que não haverá uma coluna de
            #       índice (árvore), apenas cabeçalhos de colunas.
            tree_nt = ttk.Treeview(nt_frame, columns=colunas_nt, show="headings")

            # Percorre todas as colunas definidas para configurar os
            #       cabeçalhos e largura de cada uma.
            for c in colunas_nt:

                # Define o nome da coluna exibido no cabeçalho.
                tree_nt.heading(c, text=c)

                # Define a largura padrão de cada coluna como 120 pixels.
                tree_nt.column(c, width=120)

            # Posiciona a `Treeview` dentro do frame `nt_frame`, ocupando todo o espaço disponível.
            # `fill='both'` permite que a tabela expanda na largura e altura da interface.
            # `expand=True` faz com que a tabela cresça automaticamente conforme o tamanho da janela.
            tree_nt.pack(fill='both', expand=True)

            # Agora, exibimos apenas as disciplinas com pelo menos uma nota cadastrada.
            # Percorre todas as notas registradas para o aluno selecionado no banco de dados.
            # `col_notas.find({"id_aluno": ObjectId(aluno_id)})` busca todas
            #       as disciplinas e notas do aluno.
            for nota in col_notas.find({"id_aluno": ObjectId(aluno_id)}):

                # Calcula o total de faltas do aluno para a disciplina correspondente.
                # `col_faltas.find()` busca todos os registros de faltas desse
                #       aluno para a disciplina específica.
                # O `sum()` percorre os registros e soma a quantidade de faltas registradas.
                total_faltas = sum(
                    f.get("quantidade_faltas", 0)  # Obtém o número de faltas, assumindo 0 caso a chave não exista.
                    for f in col_faltas.find({"id_aluno": ObjectId(aluno_id), "disciplina": nota["disciplina"]})
                )

                # Obtém a situação do aluno na disciplina específica.
                # A situação é registrada no banco de dados na chave `"situacao"`,
                #       podendo ser "Aprovado", "Recuperação" etc.
                situacao = nota["situacao"]

                # Se o total de faltas for igual ou superior a 10, o aluno é
                #       automaticamente reprovado por faltas.
                if total_faltas >= 10:
                    situacao = "Reprovado por Faltas"

                # Formata a média do aluno para exibição com duas casas decimais.
                # Se a média não existir (`None`), define "0.00" como valor padrão.
                media_formatada = f"{nota['media']:.2f}" if nota.get("media") is not None else "0.00"

                # Insere uma nova linha na tabela `tree_nt` contendo todas as
                #       informações da disciplina do aluno.
                tree_nt.insert("", "end", values=(
                    nota["disciplina"],  # Nome da disciplina
                    nota["bimestre_1"],  # Nota do 1º bimestre
                    nota["bimestre_2"],  # Nota do 2º bimestre
                    nota["bimestre_3"],  # Nota do 3º bimestre
                    nota["bimestre_4"],  # Nota do 4º bimestre
                    media_formatada,  # Média formatada com duas casas decimais
                    situacao  # Situação final do aluno na disciplina
                ))

        # Cria um botão para cadastrar ou editar notas do aluno.
        # `text="Cadastrar/Editar Notas"` define o texto exibido no botão.
        # `command=cadastrar_editar_notas` associa a função `cadastrar_editar_notas` ao
        #       botão, que será chamada ao clicar nele.
        # `row=0, column=0` posiciona o botão na primeira linha e primeira coluna do `btn_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para separar os botões.
        ttk.Button(btn_frame,
                   text="Cadastrar/Editar Notas",
                   command=cadastrar_editar_notas).grid(row=0, column=0, padx=5)

        # Cria um botão para listar todas as notas do aluno selecionado.
        # `text="Listar Notas do Aluno"` define o texto exibido no botão.
        # `command=listar_notas` associa a função `listar_notas` ao botão,
        #       permitindo visualizar todas as notas do aluno ao clicar nele.
        # `row=0, column=1` posiciona o botão na primeira linha e na segunda
        #       coluna do `btn_frame`, ao lado do primeiro botão.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para manter uma
        #       distância visual adequada entre os botões.
        ttk.Button(btn_frame,
                   text="Listar Notas do Aluno",
                   command=listar_notas).grid(row=0, column=1, padx=5)


    # ---------- Gerenciamento de Faltas ----------

    # Define uma função para abrir a janela de controle de faltas.
    # Essa função cria uma nova janela (`Toplevel`), onde será possível
    #       gerenciar as faltas dos alunos.
    def abrir_janela_faltas(self):

        # Cria uma nova janela (`Toplevel`) vinculada à janela principal (`self.root`).
        # Essa janela será independente, mas ainda vinculada ao sistema principal.
        janela = Toplevel(self.root)

        # Define o título da janela como "Controle de Faltas".
        # Esse título será exibido na barra superior da janela.
        janela.title("Controle de Faltas")

        # Define a janela para iniciar no modo maximizado (ocupando toda a tela).
        # O método `state('zoomed')` faz com que a janela seja
        #       aberta no tamanho máximo disponível.
        janela.state('zoomed')

        # Configura a cor de fundo da janela como `#f0f0f0` (cinza claro).
        # Essa cor será aplicada a toda a área da janela, garantindo um visual uniforme.
        janela.configure(bg='#f0f0f0')  # Cor: Cinza Claro

        # Cria um `Frame` dentro da janela para organizar os elementos superiores.
        # O `Frame` é um contêiner que agrupa widgets dentro da interface gráfica.
        top_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o `top_frame` na janela e define que ele
        #       preencherá toda a largura (`fill='x'`).
        # O preenchimento horizontal garante que o frame ocupe
        #       toda a largura disponível.
        top_frame.pack(fill='x')

        # Cria um rótulo (`Label`) dentro do `top_frame` para indicar a seleção da turma.
        # `text="Turma:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0, padx=5, sticky='e')` posiciona o rótulo na grade.
        # - `row=0` coloca o rótulo na primeira linha.
        # - `column=0` posiciona o rótulo na primeira coluna.
        # - `padx=5` adiciona 5 pixels de espaçamento horizontal para
        #       melhor separação dos elementos.
        # - `sticky='e'` alinha o texto do rótulo à direita (East),
        #       para ficar próximo à caixa de seleção.
        ttk.Label(top_frame,
                  text="Turma:").grid(row=0, column=0, padx=5, sticky='e')

        # Cria um `Combobox` (caixa de seleção suspensa) para escolher
        #       uma turma disponível.
        # `values=obter_nomes_turmas()` define a lista de turmas disponíveis
        #       obtidas do banco de dados.
        # `width=30` define a largura da caixa de seleção para 30 caracteres.
        # `state="readonly"` bloqueia a edição manual, permitindo
        #       apenas a escolha de uma turma da lista.
        turma_combo = ttk.Combobox(top_frame,
                                   values=obter_nomes_turmas(),
                                   width=30,
                                   state="readonly")

        # Posiciona o `Combobox` dentro do `top_frame` utilizando o
        #       gerenciador de layout `grid()`.
        # `grid(row=0, column=1, padx=5)` posiciona a caixa de seleção ao lado do rótulo.
        # - `row=0` coloca a caixa na primeira linha da grade.
        # - `column=1` posiciona a caixa na segunda coluna, ao lado do rótulo "Turma:".
        # - `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre o rótulo e a caixa de seleção.
        turma_combo.grid(row=0, column=1, padx=5)

        # Cria um rótulo (`Label`) para indicar a seleção da disciplina.
        # `text="Disciplina:"` define o texto exibido no rótulo.
        # `grid(row=0, column=2, padx=5, sticky='e')` posiciona o rótulo na grade de layout.
        # - `row=0` coloca o rótulo na primeira linha da grade.
        # - `column=2` posiciona o rótulo na terceira coluna da grade (0,1,2).
        # - `padx=5` adiciona 5 pixels de espaçamento horizontal, garantindo
        #       que o rótulo não fique muito próximo dos outros elementos.
        # - `sticky='e'` alinha o rótulo à direita (East), para ficar
        #       próximo à caixa de seleção.
        ttk.Label(top_frame,
                  text="Disciplina:").grid(row=0, column=2, padx=5, sticky='e')

        # Cria um `Combobox` (caixa de seleção suspensa) para escolha da disciplina.
        # `values=obter_nomes_disciplinas()` preenche a caixa com a lista de
        #       disciplinas obtidas do banco de dados.
        # `width=30` define a largura da caixa para 30 caracteres, garantindo
        #       boa visibilidade do nome das disciplinas.
        # `state="readonly"` impede que o usuário digite manualmente,
        #       permitindo apenas a escolha de uma disciplina da lista.
        disc_combo = ttk.Combobox(top_frame,
                                  values=obter_nomes_disciplinas(),
                                  width=30,
                                  state="readonly")

        # Posiciona o `Combobox` na interface gráfica utilizando o gerenciador de layout `grid()`.
        # `grid(row=0, column=3, padx=5)` define a posição da caixa de seleção na grade.
        # - `row=0` mantém a caixa na primeira linha, alinhada com o rótulo "Disciplina:".
        # - `column=3` posiciona a caixa na quarta coluna, ao lado do rótulo "Disciplina:".
        # - `padx=5` adiciona espaçamento horizontal de 5 pixels entre o
        #       rótulo e a caixa de seleção.
        disc_combo.grid(row=0, column=3, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada da data.
        # `text="Data (AAAA-MM-DD):"` define o texto exibido no rótulo,
        #       orientando o usuário sobre o formato esperado.
        # `grid(row=0, column=4, padx=5, sticky='e')` posiciona o rótulo na grade de layout.
        # - `row=0` coloca o rótulo na primeira linha da grade.
        # - `column=4` posiciona o rótulo na quinta coluna da grade.
        # - `padx=5` adiciona 5 pixels de espaçamento horizontal para manter um
        #       bom espaçamento entre os elementos.
        # - `sticky='e'` alinha o rótulo à direita (East), para que fique
        #       próximo ao campo de entrada.
        ttk.Label(top_frame,
                  text="Data (AAAA-MM-DD):").grid(row=0, column=4, padx=5, sticky='e')

        # Cria um campo de entrada (`Entry`) para que o usuário possa
        #       inserir a data desejada.
        # `width=30` define a largura do campo para até 30 caracteres,
        #       garantindo espaço suficiente para o formato completo.
        data_entry = ttk.Entry(top_frame, width=30)

        # Insere automaticamente a data atual no formato `AAAA-MM-DD`
        #       assim que o campo de entrada é criado.
        # `datetime.date.today()` obtém a data de hoje e `str()` a converte
        #       para string antes de inseri-la no campo.
        data_entry.insert(0, str(datetime.date.today()))

        # Posiciona o campo de entrada na interface gráfica utilizando o
        #       gerenciador de layout `grid()`.
        # `grid(row=0, column=5, padx=5)` define a posição do campo na grade.
        # - `row=0` mantém o campo na primeira linha, alinhado com o rótulo "Data (AAAA-MM-DD):".
        # - `column=5` posiciona o campo na sexta coluna, ao lado do rótulo.
        # - `padx=5` adiciona espaçamento horizontal de 5 pixels
        #       para manter uma boa organização.
        data_entry.grid(row=0, column=5, padx=5)

        # Cria um frame (`Frame`) para conter a tabela (`Treeview`).
        # `janela` é a janela principal onde o frame será inserido.
        # `bg='#f0f0f0'` define a cor de fundo como cinza claro (#f0f0f0).
        tree_frame = tk.Frame(janela, bg='#f0f0f0')

        # Posiciona o frame na interface gráfica utilizando o gerenciador de layout `pack()`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do frame.
        # `fill='both'` faz com que o frame expanda para preencher o espaço
        #       disponível tanto horizontalmente quanto verticalmente.
        # `expand=True` permite que o frame cresça quando a janela for redimensionada.
        tree_frame.pack(pady=10, fill='both', expand=True)

        # Define as colunas da tabela (`Treeview`).
        # A tabela terá três colunas: "id" (identificador), "Nome" (nome
        #       do aluno) e "Presença" (registro de presença/faltas).
        colunas = ("id", "Nome", "Presença")

        # Cria a tabela (`Treeview`) dentro do frame `tree_frame`.
        # `columns=colunas` define as colunas da tabela.
        # `show="headings"` oculta a primeira coluna padrão do `Treeview` e
        #       exibe apenas os cabeçalhos definidos.
        # `selectmode="browse"` permite que o usuário selecione apenas uma linha por vez.
        tree = ttk.Treeview(tree_frame,
                            columns=colunas,
                            show="headings",
                            selectmode="browse")

        # Percorre todas as colunas definidas na variável `colunas`
        for c in colunas:

            # Define o cabeçalho da coluna na `Treeview`
            # `c` representa o nome da coluna e também será o texto exibido no cabeçalho
            tree.heading(c, text=c)

            # Define a largura padrão da coluna para 300 pixels
            tree.column(c, width=300)

        # Exibe a tabela (`Treeview`) na interface gráfica
        # `fill='both'` permite que a tabela se expanda horizontalmente e verticalmente
        # `expand=True` permite que a tabela aumente seu tamanho
        #       conforme a janela for redimensionada
        tree.pack(fill='both', expand=True)

        # Cria um dicionário vazio que armazenará o estado inicial das presenças
        # Este dicionário será usado para registrar o status de
        #       cada aluno antes de qualquer alteração
        estado_inicial = {}


        # Função para carregar os alunos da turma selecionada e exibir na `Treeview`
        def carregar_alunos():

            # Remove todos os itens atuais da `Treeview`
            # `tree.get_children()` retorna todos os itens existentes na árvore
            # `tree.delete(i)` remove cada item um por um
            for i in tree.get_children():
                tree.delete(i)

            # Verifica se os campos obrigatórios (turma, disciplina e
            #       data) foram preenchidos
            if not turma_combo.get() or not disc_combo.get() or not data_entry.get():

                # Exibe uma mensagem de erro caso algum campo esteja vazio
                messagebox.showerror("Erro",
                                     "Selecione a turma, disciplina e data.")

                # Interrompe a execução da função para evitar erros
                return

            # Obtém a data digitada no campo `data_entry`
            data_aula = data_entry.get()

            # Obtém a disciplina selecionada no `Combobox`
            disciplina = disc_combo.get()

            # Percorre todos os alunos da turma selecionada no `Combobox`
            for a in col_alunos.find({"turma": turma_combo.get()}):

                # Procura um registro de falta para o aluno na disciplina e data selecionadas
                falta_reg = col_faltas.find_one({
                    "id_aluno": a["_id"],  # Filtra pelo ID do aluno
                    "disciplina": disciplina,  # Filtra pela disciplina selecionada
                    "data_falta": data_aula  # Filtra pela data informada
                })

                # Define o estado de presença do aluno
                # Se um registro de falta foi encontrado, o aluno está "Falta"
                # Caso contrário, considera o aluno "Presente"
                presenca = "Falta" if falta_reg else "Presente"

                # Insere um novo item na `Treeview` com os valores:
                # - ID do aluno (`str(a["_id"])`) → Converte o ObjectId para string
                # - Nome do aluno (`a["nome"]`)
                # - Status de presença (`presenca`)
                item = tree.insert("",
                                   "end",
                                   values=(str(a["_id"]), a["nome"], presenca))

                # Armazena o estado inicial da presença do aluno no dicionário `estado_inicial`
                # O dicionário mapeia cada item da `Treeview` para seu status inicial
                estado_inicial[item] = presenca


        # Cria um botão para carregar os alunos da turma selecionada
        # `text="Carregar Alunos"` define o texto exibido no botão
        # `command=carregar_alunos` associa a função `carregar_alunos` ao
        #       botão, que busca e exibe os alunos na tabela
        # `grid(row=0, column=6, padx=5)` define a posição do botão na
        #       grade (linha 0, coluna 6) e adiciona um espaçamento horizontal de 5 pixels
        ttk.Button(top_frame,
                   text="Carregar Alunos",
                   command=carregar_alunos).grid(row=0, column=6, padx=5)

        # Cria um frame (`btn_frame`) para organizar os botões na interface
        # `tk.Frame(janela, bg='#f0f0f0', pady=10)` cria um container dentro da `janela`
        # `bg='#f0f0f0'` define a cor de fundo como **cinza claro**
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame
        btn_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o `btn_frame` na interface
        # `.pack()` exibe o frame na tela
        btn_frame.pack()


        # Função para alternar a presença de um aluno na lista
        def alternar_presenca():

            # Obtém o item atualmente selecionado na `Treeview`
            # `tree.focus()` retorna o identificador do item selecionado na tabela
            selecionado = tree.focus()

            # Se nenhum aluno estiver selecionado, exibe um alerta para o usuário
            # `messagebox.showwarning` exibe uma caixa de aviso com o título "Atenção"
            #       e a mensagem "Selecione um aluno na lista."
            if not selecionado:
                messagebox.showwarning("Atenção",
                                       "Selecione um aluno na lista.")

                # Sai da função sem executar as próximas linhas
                return

            # Obtém os valores do item selecionado na `Treeview`
            # `tree.item(selecionado, "values")` retorna uma tupla com os valores da linha
            vals = tree.item(selecionado, "values")

            # O terceiro valor da tupla corresponde ao status atual da
            #       presença ("Presente" ou "Falta")
            status_atual = vals[2]

            # Define o novo status invertendo o valor atual:
            # Se o status for "Presente", altera para "Falta"
            # Se for "Falta", altera para "Presente"
            novo_status = "Falta" if status_atual == "Presente" else "Presente"

            # Atualiza o valor na coluna "Presença" da `Treeview`
            # `tree.set(selecionado, column="Presença", value=novo_status)`
            # Encontra o item selecionado e modifica seu valor na coluna "Presença"
            tree.set(selecionado, column="Presença", value=novo_status)

        # Define a função que alterna a presença do aluno ao dar um
        #       duplo clique na linha da tabela
        def duplo_clique_toggle(event):

            # Obtém o item atualmente selecionado na `Treeview`
            # `tree.focus()` retorna o identificador do item que está selecionado
            selecionado = tree.focus()

            # Verifica se algum item foi selecionado na tabela antes de continuar
            if selecionado:

                # Obtém os valores da linha selecionada na `Treeview`
                # `tree.item(selecionado, "values")` retorna uma tupla
                #       com os valores de cada coluna
                vals = tree.item(selecionado, "values")

                # Obtém o terceiro valor da tupla, que representa o status
                #       atual da presença ("Presente" ou "Falta")
                status_atual = vals[2]

                # Alterna o status da presença:
                # Se o status for "Presente", muda para "Falta"
                # Se o status for "Falta", muda para "Presente"
                novo_status = "Falta" if status_atual == "Presente" else "Presente"

                # Atualiza o valor na coluna "Presença" da `Treeview` para o novo status
                tree.set(selecionado, column="Presença", value=novo_status)

        # Associa a função `duplo_clique_toggle` ao evento de duplo clique na tabela
        # Sempre que o usuário der um duplo clique em uma linha
        #       da `Treeview`, a função será chamada
        tree.bind("<Double-1>", duplo_clique_toggle)

        # Define a função para salvar as faltas no banco de dados
        def salvar_faltas():

            # Verifica se os campos obrigatórios (turma, disciplina e data) foram preenchidos
            if not turma_combo.get() or not disc_combo.get() or not data_entry.get():

                # Exibe uma mensagem de erro caso algum campo esteja vazio
                messagebox.showerror("Erro",
                                     "Selecione a turma, disciplina e data antes de salvar.")

                # Interrompe a execução da função para evitar erros
                return

            # Obtém a data da aula a partir do campo de entrada
            data_aula = data_entry.get()

            # Obtém a disciplina selecionada no combobox
            disciplina = disc_combo.get()

            # Inicializa um contador para armazenar quantas faltas foram
            #       inseridas no banco de dados
            faltas_inseridas = 0

            # Inicializa um contador para armazenar quantas faltas foram
            #       removidas do banco de dados
            faltas_removidas = 0

            # Percorre todas as linhas da árvore (`Treeview`) que
            #       representam os alunos da turma.
            for child in tree.get_children():

                # Obtém os valores armazenados na linha correspondente ao aluno selecionado.
                vals = tree.item(child, "values")

                # Converte o ID do aluno para o formato correto (`ObjectId`)
                #       para consulta no MongoDB.
                aluno_id = ObjectId(vals[0])

                # Obtém o status atual de presença/falta do aluno na interface gráfica.
                status_atual = vals[2]

                # Obtém o status original antes de qualquer modificação pelo usuário.
                # Se o status original não foi registrado, assume "Presente" como valor padrão.
                status_original = estado_inicial.get(child, "Presente")

                # Verifica no banco de dados se já existe um registro de falta
                #       para este aluno na disciplina e data informadas.
                falta_exist = col_faltas.find_one({
                    "id_aluno": aluno_id,  # Filtra pelo ID do aluno.
                    "disciplina": disciplina,  # Filtra pela disciplina selecionada.
                    "data_falta": data_aula  # Filtra pela data informada no campo de entrada.
                })

                # Verifica se o status foi alterado de "Presente" para "Falta"
                if status_atual == "Falta" and status_original == "Presente":

                    # Se não houver um registro de falta já existente no
                    #       banco de dados, cria um novo.
                    if not falta_exist:

                        # Define um dicionário contendo os dados da falta a serem armazenados.
                        doc = {
                            "id_aluno": aluno_id,  # ID do aluno que recebeu a falta.
                            "disciplina": disciplina,  # Disciplina na qual a falta foi registrada.
                            "data_falta": data_aula,  # Data da falta, no formato informado no campo de entrada.
                            "quantidade_faltas": 1  # Sempre inicia com 1 falta por dia letivo.
                        }

                        # Insere a falta no banco de dados MongoDB.
                        col_faltas.insert_one(doc)

                        # Incrementa o contador de faltas inseridas para exibição posterior.
                        faltas_inseridas += 1

                # Verifica se o status foi alterado de "Falta" para "Presente"
                elif status_atual == "Presente" and status_original == "Falta":

                    # Se existir um registro de falta no banco de dados, ele será removido.
                    if falta_exist:

                        # Remove a falta do banco de dados, pois o aluno
                        #       foi marcado como presente.
                        col_faltas.delete_one({"_id": falta_exist["_id"]})

                        # Incrementa o contador de faltas removidas para exibição posterior.
                        faltas_removidas += 1

            # Exibe uma mensagem informando o total de faltas inseridas e removidas.
            # `messagebox.showinfo()` cria um pop-up informativo para o usuário.
            # `f"Faltas inseridas: {faltas_inseridas}, faltas removidas: {faltas_removidas}"`
            #       exibe a quantidade de faltas processadas.
            messagebox.showinfo("Sucesso",
                                f"Faltas inseridas: {faltas_inseridas}, faltas removidas: {faltas_removidas}")

            # Permanece na mesma tela após o clique em “OK” do messagebox.
            janela.lift()


        # Cria um botão para alternar a presença/falta de um aluno na lista.
        # `text="Alternar Presença/Falta"` define o texto exibido no botão.
        # `command=alternar_presenca` associa a função `alternar_presenca` ao botão,
        #       que altera a presença do aluno selecionado.
        # `grid(row=0, column=0, padx=5)` posiciona o botão na linha 0, coluna 0, e
        #       adiciona 5 pixels de espaçamento horizontal (padding).
        ttk.Button(btn_frame,
                   text="Alternar Presença/Falta",
                   command=alternar_presenca).grid(row=0, column=0, padx=5)

        # Cria um botão para salvar os lançamentos de faltas.
        # `text="Salvar Lançamentos"` define o texto exibido no botão.
        # `command=salvar_faltas` associa a função `salvar_faltas` ao botão,
        #       que grava as alterações no banco de dados.
        # `grid(row=0, column=1, padx=5)` posiciona o botão na linha 0,
        #       coluna 1, e adiciona 5 pixels de espaçamento horizontal (padding).
        ttk.Button(btn_frame,
                   text="Salvar Lançamentos",
                   command=salvar_faltas).grid(row=0, column=1, padx=5)


        # Define a função para listar as faltas de um aluno
        #       selecionado na interface.
        def listar_faltas():

            # Obtém o item atualmente selecionado na árvore (`tree`).
            # `tree.focus()` retorna o identificador do item selecionado.
            selecionado = tree.focus()

            # Verifica se algum aluno foi selecionado na lista.
            # Se `selecionado` estiver vazio, exibe uma mensagem de
            #       aviso e encerra a função.
            if not selecionado:

                # `messagebox.showwarning()` exibe uma mensagem de
                #       alerta informando o usuário.
                messagebox.showwarning("Atenção",
                                       "Selecione um aluno para listar faltas.")

                # Sai da função sem executar as próximas linhas.
                return

            # Obtém os valores da linha correspondente ao item selecionado.
            # `tree.item(selecionado, "values")` retorna uma tupla contendo os dados do aluno.
            vals = tree.item(selecionado, "values")

            # Extrai o ID do aluno e o nome a partir dos valores obtidos.
            # `vals[0]` contém o ID do aluno armazenado no banco de dados (MongoDB).
            # `vals[1]` contém o nome do aluno exibido na interface.
            aluno_id, aluno_nome = vals[0], vals[1]

            # Cria uma nova janela (`Toplevel`) para exibir as
            #       faltas do aluno selecionado.
            win = Toplevel(janela)

            # Define o título da janela com o nome do aluno.
            # `"Faltas do Aluno: " + aluno_nome` cria um título
            #       dinâmico baseado no nome do aluno.
            win.title("Faltas do Aluno: " + aluno_nome)

            # Define a janela para abrir no modo maximizado (`zoomed`), ocupando toda a tela.
            win.state('zoomed')

            # Define a cor de fundo da janela como cinza claro (`#f0f0f0`).
            win.configure(bg='#f0f0f0')  # Cor: Cinza Claro

            # Cria um `Frame` (contêiner) dentro da janela para
            #       organizar os elementos da interface.
            ft_frame = tk.Frame(win, bg='#f0f0f0')  # Cor: Cinza Claro

            # Posiciona o `Frame` na interface com espaçamento vertical (`pady=10`).
            # `fill='both'` permite que o frame expanda para preencher todo o espaço disponível.
            # `expand=True` faz com que o frame cresça junto com a janela ao ser redimensionado.
            ft_frame.pack(pady=10, fill='both', expand=True)

            # Define as colunas da `Treeview` que exibirá as faltas do aluno.
            # "Disciplina" - Nome da disciplina em que a falta ocorreu.
            # "Data Falta" - Data em que a falta foi registrada.
            # "Quantidade" - Quantidade de faltas registradas para aquela disciplina e data.
            colunas_ft = ("Disciplina", "Data Falta", "Quantidade")

            # Cria uma `Treeview` (tabela interativa) dentro do frame `ft_frame`.
            # `columns=colunas_ft` define as colunas que a tabela terá.
            # `show="headings"` oculta a coluna padrão de índice e
            #       exibe apenas os cabeçalhos definidos.
            tree_ft = ttk.Treeview(ft_frame,
                                   columns=colunas_ft,
                                   show="headings")

            # Percorre todas as colunas da `Treeview` e configura
            #       seus cabeçalhos e larguras.
            for c in colunas_ft:

                # Define o nome visível no cabeçalho da coluna na `Treeview`.
                # O texto do cabeçalho será o mesmo nome da coluna definida em `colunas_ft`.
                tree_ft.heading(c, text=c)

                # Define a largura da coluna em pixels.
                # Todas as colunas terão largura fixa de 200 pixels.
                tree_ft.column(c, width=200)

            # Posiciona a `Treeview` dentro do `Frame` e a ajusta para
            #       preencher todo o espaço disponível.
            # `fill='both'` permite que a tabela se expanda tanto na largura quanto na altura.
            # `expand=True` faz com que a tabela cresça ao redimensionar a janela.
            tree_ft.pack(fill='both', expand=True)

            # Percorre todos os registros de faltas do aluno no banco de dados.
            # `col_faltas.find({"id_aluno": ObjectId(aluno_id)})` busca todas as
            #       faltas do aluno pelo seu `ObjectId`.
            for f in col_faltas.find({"id_aluno": ObjectId(aluno_id)}):

                # Insere um novo item na `Treeview` com os dados da falta.
                # `""` indica que os itens são adicionados na raiz da árvore (sem pai).
                # `"end"` adiciona cada novo item no final da lista.
                tree_ft.insert("", "end", values=(
                    f["disciplina"],  # Nome da disciplina onde a falta foi registrada.
                    f["data_falta"],  # Data da falta (formato: AAAA-MM-DD).
                    f["quantidade_faltas"]  # Número total de faltas registradas para essa disciplina e data.
                ))


        # Cria um botão para listar as faltas do aluno selecionado na `Treeview`.
        # `text="Listar Faltas do Aluno Selecionado"` define o texto exibido no botão.
        # `command=listar_faltas` associa a função `listar_faltas` ao botão, que
        #       será executada quando o botão for pressionado.
        # `row=0, column=2` posiciona o botão na linha 0 e coluna 2 do `btn_frame`,
        #       garantindo um alinhamento adequado.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do
        #       botão, melhorando a disposição dos elementos.
        ttk.Button(btn_frame,
                   text="Listar Faltas do Aluno Selecionado",
                   command=listar_faltas).grid(row=0, column=2, padx=5)


    # ---------- Gerenciamento de Relatório Geral ----------

    # Função para abrir a janela de Relatório Geral.
    def abrir_janela_relatorio_geral(self):

        # Cria uma nova janela (`Toplevel`) como filha da janela
        #       principal (`self.root`).
        janela = Toplevel(self.root)

        # Define o título da janela como "Relatório Geral".
        janela.title("Relatório Geral")

        # Define o estado da janela como `zoomed`, fazendo com que
        #       ela seja aberta em tela cheia.
        janela.state('zoomed')

        # Define a cor de fundo da janela como um tom de cinza claro (`#f0f0f0`).
        # Esse tom de cinza melhora a leitura e harmoniza o design da interface.
        janela.configure(bg='#f0f0f0')

        # Cria um frame (`top_frame`) dentro da janela `janela`, que servirá
        #       como o cabeçalho da tela de relatório.
        # Esse frame pode ser usado para conter filtros ou opções de navegação.
        # `bg='#f0f0f0'` define o fundo do frame na mesma cor da janela principal,
        #       garantindo uniformidade visual.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e
        #       abaixo do frame, melhorando o layout.
        top_frame = tk.Frame(janela, bg='#f0f0f0', pady=10)

        # Posiciona o `top_frame` na interface.
        # `fill='x'` faz com que o frame ocupe toda a largura da janela.
        # Isso é útil para garantir um alinhamento correto de elementos dentro do frame.
        top_frame.pack(fill='x')

        # Cria um rótulo (`Label`) para indicar o campo de filtro pelo nome do aluno.
        # `top_frame` é o frame onde o rótulo será inserido.
        # `text="Aluno (nome):"` define o texto que será exibido no rótulo.
        # `grid(row=0, column=0, padx=5, sticky='e')` posiciona o rótulo na
        #       primeira linha e primeira coluna,
        #       adicionando 5 pixels de espaçamento horizontal (`padx=5`) e
        #       alinhando-o à direita (`sticky='e'`).
        ttk.Label(top_frame,
                  text="Aluno (nome):").grid(row=0, column=0, padx=5, sticky='e')

        # Cria um campo de entrada (`Entry`) onde o usuário poderá digitar o
        #       nome do aluno para filtrar os dados.
        # `top_frame` é o frame onde o campo será inserido.
        # `width=30` define a largura do campo como 30 caracteres, garantindo
        #       espaço suficiente para nomes completos.
        # `grid(row=0, column=1, padx=5)` posiciona o campo ao lado do
        #       rótulo, na primeira linha e segunda coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`)
        #       para não ficar colado no rótulo.
        filtro_aluno = ttk.Entry(top_frame, width=30)
        filtro_aluno.grid(row=0, column=1, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de filtro pela turma do aluno.
        # `top_frame` é o frame onde o rótulo será inserido.
        # `text="Turma:"` define o texto que será exibido no rótulo, informando
        #       que o próximo campo é para selecionar uma turma.
        # `grid(row=0, column=2, padx=5, sticky='e')` posiciona o rótulo na
        #       primeira linha e terceira coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`) e
        #       alinhando-o à direita (`sticky='e'`).
        ttk.Label(top_frame, text="Turma:").grid(row=0, column=2, padx=5, sticky='e')

        # Cria um combobox (`ttk.Combobox`) para selecionar uma turma específica.
        # `top_frame` é o frame onde o combobox será inserido.
        # `values=obter_nomes_turmas()` obtém a lista de nomes das turmas do banco de dados.
        # `width=30` define a largura do combobox para exibir os nomes das turmas corretamente.
        # `state="readonly"` impede que o usuário digite valores manualmente,
        #       permitindo apenas a seleção de opções disponíveis.
        # `grid(row=0, column=3, padx=5)` posiciona o combobox na
        #       primeira linha e quarta coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`) para
        #       evitar que fique colado em outros elementos.
        filtro_turma = ttk.Combobox(top_frame,
                                    values=obter_nomes_turmas(),
                                    width=30,
                                    state="readonly")

        filtro_turma.grid(row=0, column=3, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de filtro pela disciplina.
        # `top_frame` é o frame onde o rótulo será inserido.
        # `text="Disciplina:"` define o texto exibido no rótulo, informando que o
        #       próximo campo é para selecionar uma disciplina.
        # `grid(row=0, column=4, padx=5, sticky='e')` posiciona o rótulo na
        #       primeira linha e quinta coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`) e
        #       alinhando o texto à direita (`sticky='e'`).
        ttk.Label(top_frame,
                  text="Disciplina:").grid(row=0, column=4, padx=5, sticky='e')

        # Cria um combobox (`ttk.Combobox`) para selecionar uma disciplina específica.
        # `top_frame` é o frame onde o combobox será inserido.
        # `values=obter_nomes_disciplinas()` preenche a lista com os nomes das
        #       disciplinas disponíveis no banco de dados.
        # `width=30` define a largura do combobox para exibir os nomes completos das disciplinas.
        # `state="readonly"` impede que o usuário insira texto manualmente,
        #       permitindo apenas a seleção de opções disponíveis.
        # `grid(row=0, column=5, padx=5)` posiciona o combobox na primeira linha e sexta coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`) para
        #       evitar que fique colado em outros elementos.
        filtro_disc = ttk.Combobox(top_frame,
                                   values=obter_nomes_disciplinas(),
                                   width=30,
                                   state="readonly")

        filtro_disc.grid(row=0, column=5, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de filtro pelo professor responsável.
        # `top_frame` é o frame onde o rótulo será inserido.
        # `text="Professor:"` define o texto exibido no rótulo, informando que o
        #       próximo campo será para selecionar um professor.
        # `grid(row=0, column=6, padx=5, sticky='e')` posiciona o rótulo na
        #       primeira linha e sétima coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`) e
        #       alinhando o texto à direita (`sticky='e'`),
        #       garantindo que o rótulo fique visualmente alinhado com os
        #       campos de entrada ao lado.
        ttk.Label(top_frame,
                  text="Professor:").grid(row=0, column=6, padx=5, sticky='e')

        # Cria um combobox (`ttk.Combobox`) para selecionar um professor responsável.
        # `top_frame` é o frame onde o combobox será inserido.
        # `values=obter_nomes_professores()` preenche a lista com os nomes dos
        #       professores cadastrados no banco de dados.
        # `width=30` define a largura do combobox para garantir que os nomes
        #       sejam exibidos completamente.
        # `state="readonly"` impede que o usuário insira texto manualmente,
        #       permitindo apenas a seleção das opções disponíveis.
        # `grid(row=0, column=7, padx=5)` posiciona o combobox na
        #       primeira linha e oitava coluna,
        #       adicionando um espaçamento horizontal de 5 pixels (`padx=5`)
        #       para evitar que fique colado em outros elementos.
        filtro_prof = ttk.Combobox(top_frame,
                                   values=obter_nomes_professores(),
                                   width=30,
                                   state="readonly")

        filtro_prof.grid(row=0, column=7, padx=5)

        # Cria um frame (`Frame`) que servirá como o contêiner para a
        #       tabela de dados (Treeview).
        # `janela` é a janela onde o frame será inserido.
        # `bg='#f0f0f0'` define a cor de fundo do frame para um
        #       tom de cinza claro (`#f0f0f0`).
        tree_frame = tk.Frame(janela, bg='#f0f0f0')

        # Posiciona o frame na interface gráfica.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do frame,
        #       garantindo um layout mais espaçado e organizado.
        # `fill='both'` faz com que o frame expanda para preencher a
        #       largura e a altura disponíveis.
        # `expand=True` permite que o frame cresça conforme o
        #       tamanho da janela muda.
        tree_frame.pack(pady=10, fill='both', expand=True)

        # Define as colunas que serão exibidas na tabela (`Treeview`).
        # Cada coluna representa um campo do relatório geral, incluindo
        #       informações do aluno, turma, disciplina, professor e notas.
        colunas = (
            "Aluno", "Turma", "Disciplina", "Professor", "1º Bim", "2º Bim", "3º Bim", "4º Bim", "Média",
            "Situação",
            "Faltas")

        # Cria a tabela (`Treeview`) dentro do `tree_frame` para
        #       exibir os dados dos alunos.
        # `columns=colunas` define as colunas que a tabela terá.
        # `show="headings"` faz com que apenas os cabeçalhos das colunas
        #       sejam exibidos, sem uma coluna extra de índice.
        tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")

        # Configura cada coluna da tabela (`Treeview`).
        # O loop percorre todas as colunas definidas anteriormente e
        #       ajusta suas propriedades.
        for c in colunas:

            # Define o nome visível da coluna no cabeçalho da tabela.
            # `heading(c, text=c)` faz com que o nome da coluna seja exibido no cabeçalho.
            tree.heading(c, text=c)

            # Define a largura padrão de cada coluna como 120 pixels.
            # Isso garante que todas as colunas tenham o mesmo tamanho e
            #       fiquem visíveis corretamente.
            tree.column(c, width=120)

        # Exibe a tabela (`Treeview`) dentro do `tree_frame`.
        # `fill='both'` faz com que a tabela se expanda para ocupar
        #       todo o espaço disponível dentro do frame.
        # `expand=True` permite que a tabela cresça dinamicamente
        #       se a janela for redimensionada.
        tree.pack(fill='both', expand=True)

        # Cria um rótulo (`Label`) para exibir o total de alunos na tabela.
        # O rótulo será atualizado dinamicamente à medida que os dados forem carregados.
        # `text="Total de Alunos exibidos: 0"` define o texto
        #       inicial do rótulo, começando com 0 alunos.
        # `bg='#f0f0f0'` define o fundo do rótulo como cinza claro para
        #       combinar com o layout da janela.
        # `font=("Arial", 12, "bold")` define a fonte do texto, tamanho 12, em negrito.
        lbl_total = tk.Label(janela,
                             text="Total de Alunos exibidos: 0",
                             bg='#f0f0f0',
                             font=("Arial", 12, "bold"))

        # Exibe o rótulo na interface.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do
        #       rótulo para evitar que fique muito colado aos outros elementos.
        lbl_total.pack(pady=5)


        # Função para gerar o relatório geral dos alunos.
        def gerar_relatorio():

            # Remove todos os dados atualmente exibidos na tabela (`Treeview`).
            # `tree.get_children()` retorna todos os itens da tabela.
            # O loop `for i in tree.get_children(): tree.delete(i)`
            #       percorre e apaga cada um dos itens existentes.
            for i in tree.get_children():
                tree.delete(i)

            # Consulta todas as notas armazenadas no banco de dados na coleção `col_notas`.
            # `col_notas.find({})` retorna todos os registros da coleção de notas.
            notas_cursor = col_notas.find({})

            # Cria um conjunto vazio para armazenar os alunos já
            #       exibidos no relatório.
            # Isso evita a duplicação de registros na tabela.
            alunos_exibidos = set()

            # Percorre cada documento de nota encontrado na
            #       consulta ao banco de dados.
            for nota_doc in notas_cursor:

                # Obtém o ID do aluno associado à nota atual.
                # O campo `id_aluno` no documento de notas armazena o
                #       identificador do aluno.
                aluno_id = nota_doc["id_aluno"]

                # Busca no banco de dados as informações do aluno pelo seu ID.
                # `obter_aluno_por_id(aluno_id)` retorna os detalhes do
                #       aluno, como nome e matrícula.
                aluno = obter_aluno_por_id(aluno_id)

                # Se o aluno não for encontrado no banco de dados, continua para o próximo item.
                # Isso pode acontecer se um aluno for removido do banco de
                #       dados, mas suas notas ainda existirem.
                if not aluno:
                    continue

                # Obtém o nome do aluno a partir do dicionário retornado pela consulta.
                # O campo "nome" contém o nome completo do aluno.
                nome_aluno = aluno["nome"]

                # Obtém a turma do aluno a partir do dicionário do banco de dados.
                # Usa `.get("turma", "")` para evitar erro caso o campo "turma" não exista.
                turma_aluno = aluno.get("turma", "")

                # Obtém a disciplina relacionada à nota atual.
                # Este campo é armazenado diretamente no documento da coleção `col_notas`.
                disciplina = nota_doc["disciplina"]

                # Obtém a nota do 1º Bimestre do aluno na disciplina correspondente.
                # O campo "bimestre_1" contém a nota do aluno para o primeiro bimestre.
                b1 = nota_doc["bimestre_1"]

                # Obtém a nota do 2º Bimestre do aluno na disciplina correspondente.
                # O campo "bimestre_2" contém a nota do aluno para o segundo bimestre.
                b2 = nota_doc["bimestre_2"]

                # Obtém a nota do 3º Bimestre do aluno na disciplina correspondente.
                # O campo "bimestre_3" contém a nota do aluno para o terceiro bimestre.
                b3 = nota_doc["bimestre_3"]

                # Obtém a nota do 4º Bimestre do aluno na disciplina correspondente.
                # O campo "bimestre_4" contém a nota do aluno para o quarto bimestre.
                b4 = nota_doc["bimestre_4"]

                # Obtém a média final do aluno na disciplina.
                # O campo "media" contém o cálculo da média das notas dos bimestres.
                media = nota_doc["media"]

                # Obtém a situação final do aluno na disciplina.
                # O campo "situacao" armazena se o aluno está "Aprovado", "Recuperação" ou "Reprovado".
                situacao = nota_doc["situacao"]

                # Calcula o total de faltas do aluno na disciplina selecionada.

                # `col_faltas.find({"id_aluno": aluno_id, "disciplina": disciplina})`
                # -> Esta consulta busca todos os registros de faltas na coleção `col_faltas`
                #    onde o `id_aluno` corresponde ao aluno atual e a `disciplina` é a selecionada.
                # -> Retorna um conjunto de documentos que representam cada falta registrada.

                # O `sum()` percorre todos os documentos retornados pela
                #       consulta e soma a quantidade de faltas.

                total_faltas = sum(

                    # Obtém o valor do campo `quantidade_faltas` dentro do documento.
                    # Se o campo não existir no documento (ou seja, se não houver registro),
                    # o método `.get("quantidade_faltas", 0)` retorna `0` por padrão,
                    # garantindo que a soma não falhe.
                    f.get("quantidade_faltas", 0)

                    # Itera sobre cada documento
                    # encontrado na coleção `col_faltas`
                    for f in col_faltas.find({"id_aluno": aluno_id, "disciplina": disciplina}))

                # Se o aluno acumulou 10 ou mais faltas na disciplina, altera sua
                #       situação para "Reprovado por Faltas".
                # Essa verificação garante que, independentemente das notas, um aluno
                #       com muitas faltas seja reprovado automaticamente.
                if total_faltas >= 10:
                    situacao = "Reprovado por Faltas"

                # Busca no banco de dados `col_professores` um professor que
                #       lecione a disciplina em questão.
                # O método `find_one()` retorna o primeiro documento encontrado onde a `disciplina`
                #       seja igual à variável `disciplina`.
                professor_doc = col_professores.find_one({"disciplina": disciplina})

                # Obtém o nome do professor a partir do documento encontrado.
                # Se `professor_doc` existir (ou seja, se foi encontrado um professor
                #       para a disciplina), o campo `nome` é acessado.
                # Caso contrário, atribui uma string vazia (`""`), garantindo que o
                #       código não falhe por tentar acessar um valor `None`.
                professor_nome = professor_doc["nome"] if professor_doc else ""

                # Se o campo de filtro "Aluno" estiver preenchido e o nome do aluno **não
                #       contiver** o termo buscado, ignora esse aluno.
                # - `filtro_aluno.get()` verifica se o usuário digitou algo no filtro.
                # - `filtro_aluno.get().lower()` converte o texto do filtro para
                #       minúsculas (evita problemas de diferenciação de maiúsculas/minúsculas).
                # - `nome_aluno.lower()` converte o nome do aluno para minúsculas.
                # - `not in` verifica se o nome do aluno **não contém** o termo buscado.
                # - Se a condição for verdadeira, o `continue` pula esse aluno e segue para o próximo.
                if filtro_aluno.get() and (filtro_aluno.get().lower() not in nome_aluno.lower()):
                    continue

                # Se o campo de filtro "Turma" estiver preenchido e a turma do aluno **não
                #       for exatamente igual** à turma selecionada no filtro, ignora esse aluno.
                # - `filtro_turma.get()` verifica se o usuário selecionou alguma turma no filtro.
                # - `turma_aluno != filtro_turma.get()` compara a turma do aluno
                #       com a turma escolhida no filtro.
                # - Se forem diferentes, o `continue` pula esse aluno e passa para o próximo.
                if filtro_turma.get() and (turma_aluno != filtro_turma.get()):
                    continue

                # Se o campo de filtro "Disciplina" estiver preenchido e a disciplina do
                #       aluno **não for exatamente igual** à disciplina selecionada no filtro, ignora esse aluno.
                # - `filtro_disc.get()` verifica se o usuário selecionou alguma disciplina no filtro.
                # - `disciplina != filtro_disc.get()` compara a disciplina do aluno com a escolhida no filtro.
                # - Se forem diferentes, o `continue` pula esse aluno e passa para o próximo.
                if filtro_disc.get() and (disciplina != filtro_disc.get()):
                    continue

                # Se o campo de filtro "Professor" estiver preenchido e o professor da
                #       disciplina **não for exatamente igual** ao professor selecionado
                #       no filtro, ignora esse aluno.
                # - `filtro_prof.get()` verifica se o usuário selecionou algum professor no filtro.
                # - `professor_nome != filtro_prof.get()` compara o nome do
                #       professor com o escolhido no filtro.
                # - Se forem diferentes, o `continue` pula esse aluno e passa para o próximo.
                if filtro_prof.get() and (professor_nome != filtro_prof.get()):
                    continue

                # Insere uma nova linha na Treeview com os dados do aluno, sua turma,
                #       disciplina, notas, média, situação e total de faltas.
                # - `tree.insert("", "end", values=...)` adiciona um novo item na tabela.
                # - `""` indica que esse item não tem um pai (é um item de nível principal na Treeview).
                # - `"end"` adiciona o novo item no final da lista.
                # - `values=(...)` define os valores de cada coluna do novo item na Treeview.
                tree.insert("", "end", values=(

                    # Nome do aluno.
                    nome_aluno,

                    # Turma à qual o aluno pertence.
                    turma_aluno,

                    # Disciplina para a qual as notas estão sendo lançadas.
                    disciplina,

                    # Nome do professor responsável pela disciplina.
                    professor_nome,

                    # Nota do 1º Bimestre.
                    b1,

                    # Nota do 2º Bimestre.
                    b2,

                    # Nota do 3º Bimestre.
                    b3,

                    # Nota do 4º Bimestre.
                    b4,

                    # Média final do aluno formatada com duas casas decimais.
                    f"{media:.2f}",

                    # Situação final do aluno (Aprovado, Recuperação ou Reprovado).
                    situacao,

                    # Quantidade total de faltas na disciplina.
                    total_faltas

                ))

                # Adiciona o ID do aluno no conjunto `alunos_exibidos` para evitar duplicações.
                # - `alunos_exibidos` é um conjunto (`set`) que armazena os
                #       IDs dos alunos já listados.
                # - Isso impede que o mesmo aluno apareça mais de uma vez no relatório.
                alunos_exibidos.add(aluno_id)

            # Atualiza o rótulo (`Label`) que exibe o total de alunos na tabela.
            # - `lbl_total.config(text=...)` altera o texto do rótulo dinamicamente.
            # - `len(alunos_exibidos)` conta quantos alunos foram listados no relatório.
            # - O f-string `f"Total de Alunos exibidos: {len(alunos_exibidos)}"`
            #       exibe o número total na interface.
            lbl_total.config(text=f"Total de Alunos exibidos: {len(alunos_exibidos)}")


        # Função para exportar os dados da Treeview para Excel
        def exportar_para_excel():

            # Inicializa uma lista vazia para armazenar os dados da Treeview.
            dados = []

            # Obtém os nomes das colunas da Treeview.
            # `tree["columns"]` retorna os identificadores das colunas.
            # `tree.heading(col)["text"]` acessa o nome visível da coluna.
            colunas = [tree.heading(col)["text"] for col in tree["columns"]]

            # Percorre todos os itens (linhas) da Treeview.
            for item in tree.get_children():

                # Obtém os valores da linha atual.
                valores = tree.item(item, "values")

                # Adiciona os valores obtidos à lista `dados`.
                dados.append(valores)

            # Verifica se há dados na lista `dados` antes de exportar.
            # Se a lista estiver vazia, interrompe a execução da função.
            if not dados:
                return

            # Cria um DataFrame do pandas contendo os dados extraídos da Treeview.
            # `dados` é uma lista de tuplas contendo os valores de cada linha.
            # `columns=colunas` define os nomes das colunas no DataFrame.
            df = pd.DataFrame(dados, columns=colunas)

            # Define o nome do arquivo onde os dados serão salvos no formato Excel.
            # O arquivo será criado ou sobrescrito no mesmo diretório do código-fonte.
            caminho_arquivo = "Relatorio_Geral.xlsx"

            # Salva o DataFrame no arquivo Excel.
            # `index=False` impede que o índice do DataFrame seja incluído no arquivo.
            # `engine='openpyxl'` define o motor de escrita necessário para manipular arquivos Excel.
            df.to_excel(caminho_arquivo, index=False, engine='openpyxl')

            # Exibe uma mensagem para o usuário informando que o relatório foi salvo com sucesso.
            # `messagebox.showinfo()` cria uma caixa de diálogo com um título e uma mensagem informativa.
            messagebox.showinfo("Exportação Concluída",
                                f"Relatório salvo com sucesso em:\n{caminho_arquivo}")

            # Permanece na mesma tela após o clique em “OK” do messagebox.
            janela.lift()


        # Cria um botão para gerar o relatório de alunos.
        # - `text="Gerar Relatório"` define o texto exibido no botão.
        # - `command=gerar_relatorio` associa a função `gerar_relatorio` ao
        #       botão, que será executada ao clicar.
        # - `row=0` posiciona o botão na primeira linha do `grid` layout.
        # - `column=8` posiciona o botão na coluna 8 do `grid`, ao lado dos filtros.
        # - `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(top_frame,
                   text="Gerar Relatório",
                   command=gerar_relatorio).grid(row=1, column=0, padx=5, pady=5)


        # Cria um botão para exportar os dados da Treeview para um arquivo Excel.
        # `top_frame` define que o botão será inserido no frame superior da interface.
        # `text="Exportar para Excel"` define o texto exibido no botão, indicando sua funcionalidade.
        # `command=exportar_para_excel` associa a função `exportar_para_excel` ao botão,
        #       que será executada ao clicar.
        btn_exportar = ttk.Button(top_frame,
                                  text="Exportar para Excel",
                                  command=exportar_para_excel)

        # Posiciona o botão na interface usando o layout grid.
        # `row=1` define que o botão será posicionado na segunda linha do grid (contagem começa em 0).
        # `column=1` define que o botão ficará na segunda coluna do grid.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal para evitar que o
        #       botão fique colado em outros elementos.
        # `pady=5` adiciona 5 pixels de espaçamento vertical para melhorar a organização visual.
        btn_exportar.grid(row=1, column=1, padx=5, pady=5)


# ----------------------------------------------------------
# EXECUÇÃO DO PROGRAMA
# ----------------------------------------------------------
# Cria a janela principal da aplicação.
# - `tk.Tk()` inicializa a interface gráfica do Tkinter.
root = tk.Tk()

# Cria uma instância da classe `GerenciamentoEscolar`, que
#       representa a aplicação.
# - `app = GerenciamentoEscolar(root)` instancia a classe e
#       vincula a janela `root` como sua base.
app = GerenciamentoEscolar(root)

# Mantém a aplicação em execução aguardando interações do usuário.
# - `root.mainloop()` inicia o loop principal do Tkinter,
#       mantendo a janela aberta.
root.mainloop()