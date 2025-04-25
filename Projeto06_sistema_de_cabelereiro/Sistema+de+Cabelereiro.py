# Importa o módulo tkinter e o renomeia como 'tk'
# O tkinter é usado para criar interfaces gráficas de
#       usuário (GUIs) em aplicações Python.
import tkinter as tk

# Importa o módulo ttk do tkinter
# O ttk é uma extensão do tkinter que fornece acesso a
#   widgets com um estilo mais moderno.
from tkinter import ttk

# Importa o módulo messagebox do tkinter
# O messagebox é usado para exibir caixas de diálogo e
#       alertas na interface gráfica.
from tkinter import messagebox

# Importa o módulo simpledialog do tkinter
# O simpledialog é usado para obter entradas simples do
#       usuário, como strings ou números.
from tkinter import simpledialog

# Importa o módulo pymongo
# O pymongo é uma biblioteca para trabalhar com MongoDB, um banco de dados NoSQL.
import pymongo

# Importa o módulo pandas e o renomeia como 'pd'
# O pandas é utilizado para análise e manipulação de dados, especialmente
#       útil para trabalhar com tabelas (DataFrames).
import pandas as pd

# Importa os módulos Image e ImageTk da biblioteca PIL (Python Imaging Library)
# Image é usado para manipular imagens (abrir, manipular, salvar).
# ImageTk é usado para trabalhar com imagens no tkinter,
#       permitindo inserir imagens em widgets.
from PIL import Image, ImageTk
from PIL.ImageOps import expand
from Tools.scripts.make_ctype import values

# Importa a classe ObjectId do módulo bson
# ObjectId é um identificador único usado no MongoDB, frequentemente
#       usado para referenciar documentos.
from bson import ObjectId

# Importa o módulo datetime
# O datetime é usado para manipular datas e horas em Python.
import datetime

from numpy.ma.core import resize
# O tkcalendar é uma biblioteca que fornece um widget de calendário para tkinter.
# Este widget pode ser usado para que o usuário selecione datas.
from tkcalendar import Calendar

# ------------------------------------------------------------
# Conexão com o MongoDB
# ------------------------------------------------------------

# O bloco 'try' inicia uma tentativa de executar o código que pode gerar uma exceção.
try:

    # Cria uma conexão com o cliente MongoDB local na porta padrão 27017.
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Acessa o banco de dados chamado 'salao_profissional_completo'.
    db = mongo_client["salao_profissional_completo"]

    # Cria ou acessa uma coleção chamada 'clientes' dentro do banco de dados.
    colecao_clientes = db["clientes"]

    # Cria ou acessa uma coleção chamada 'servicos'.
    colecao_servicos = db["servicos"]

    # Cria ou acessa uma coleção chamada 'produtos'.
    colecao_produtos = db["produtos"]

    # Cria ou acessa uma coleção chamada 'funcionarios'.
    colecao_funcionarios = db["funcionarios"]

    # Cria ou acessa uma coleção chamada 'agendamentos'.
    colecao_agendamentos = db["agendamentos"]

    # Cria ou acessa uma coleção chamada 'usuarios'.
    colecao_usuarios = db["usuarios"]

    # Cria ou acessa uma coleção chamada 'relatorios'.
    colecao_relatorios = db["relatorios"]

    # Cria ou acessa uma coleção chamada 'financeiro'
    colecao_financeiro = db["financeiro"]  # Exemplo, se quiser depois

# O bloco 'except' captura exceções que podem ser lançadas
#       pelo código no bloco 'try'.
except Exception as e:

    # Imprime uma mensagem de erro que descreve o problema ao tentar conectar ao MongoDB.
    print("Erro ao conectar ao MongoDB:", e)

    # Encerra o programa imediatamente se ocorrer algum erro durante a conexão.
    exit()


# Exemplo de categorias de produtos (poderia vir do BD ou
#       ser editável via tela)
CATEGORIAS_PRODUTOS = ["Shampoo", "Condicionador", "Coloração", "Tratamento", "Unhas", "Outros"]

# Exemplo de perfis de usuários para a tela de usuários
PERFIS_USUARIOS = ["Administrador", "Funcionário", "Recepcionista"]


# ------------------------------------------------------------
# Tela para Gerenciar Usuários
# ------------------------------------------------------------
class TelaUsuarios(tk.Toplevel):

    """
    Janela para adicionar, editar e excluir usuários do sistema.
    A partir desta tela, é possível criar novos usuários com login, senha e perfil.
    """
    def __init__(self, parent):

        # Chama o construtor da classe pai `tk.Toplevel`.
        super().__init__(parent)

        # Define o título da janela.
        self.title("Gerenciar Usuários")

        # Configura a janela para iniciar em modo tela cheia.
        # `zoomed` faz com que a janela ocupe toda a tela ao abrir.
        self.state('zoomed')

        # Define a cor de fundo da janela para branco.
        self.configure(bg="#FFFFFF")

        # Inicializa e configura o estilo para componentes `ttk`.
        # `self.style` permite personalizar o visual dos widgets.
        self.style = ttk.Style()

        # Define o tema "clam" para os widgets `ttk`.
        # O tema "clam" é escolhido por ser limpo e visualmente agradável.
        self.style.theme_use("clam")

        # Adiciona um título descritivo na janela.
        # O título "Gerenciamento de Usuários" será exibido no topo
        #       da janela, como cabeçalho principal.
        # Configuração de fonte:
        # - Fonte: Arial
        # - Tamanho: 20
        # - Estilo: Negrito ("bold"), para destacar o texto.
        # A cor de fundo do rótulo é branca (#FFFFFF), para manter
        #       consistência com o fundo da janela.
        # O parâmetro `pady=20` adiciona 20 pixels de espaço
        #       vertical acima e abaixo do rótulo.
        ttk.Label(self,
                text="Gerenciamento de Usuários",  # Define o texto que será exibido.
                font=("Arial", 20, "bold"),  # Estiliza a fonte do texto.
                background="#FFFFFF"  # Define o fundo do rótulo como branco.
                ).pack(pady=20)  # Adiciona espaçamento vertical ao redor do rótulo.


        # Cria um frame principal que será usado para organizar os
        #       widgets dentro da janela.
        # Esse frame serve como um contêiner para posicionar outros
        #       elementos, como campos e botões.
        main_frame = ttk.Frame(self,

                               # Define um preenchimento interno (padding) de
                               #        20 pixels ao redor do frame.
                               padding=20)

        # Posiciona o frame principal na janela.
        # `expand=True` faz com que o frame ocupe o máximo de espaço disponível.
        # `fill="both"` permite que o frame se expanda tanto na largura quanto na altura.
        main_frame.pack(expand=True, fill="both")

        # Criação de um frame para os campos de entrada e outros
        #       elementos à esquerda da interface.
        # Este frame será usado para organizar os campos de forma estruturada.

        # Define o frame dentro do `main_frame`, o container principal da janela.
        left_frame = ttk.Frame(main_frame)

        # Configuração de posicionamento do frame:
        # - `side="left"`: Posiciona o frame no lado esquerdo do container principal.
        # - `fill="y"`: Permite que o frame preencha toda a altura disponível dentro do container.
        # - `padx=20`: Adiciona um espaçamento horizontal de 20 pixels ao redor do frame.
        left_frame.pack(side="left",  # Posiciona o frame à esquerda.
                        fill="y",  # Preenche toda a altura do container.
                        padx=20)  # Adiciona espaçamento lateral.

        # Adiciona um rótulo descritivo para o campo de login.
        # O texto "Login:" indica que o campo ao lado será usado para o nome de usuário.
        # A fonte é definida como Arial, tamanho 12, e negrito para destaque.
        ttk.Label(left_frame,  # O rótulo é adicionado dentro do `left_frame`.
                text="Login:",  # Texto exibido no rótulo.
                font=("Arial", 12, "bold")  # Configuração de fonte: Arial, tamanho 12, negrito.
                ).grid( row=0,  # Posiciona o rótulo na linha 0.
                        column=0,  # Posiciona o rótulo na coluna 0.
                        sticky="w",  # Alinha o rótulo à esquerda da célula.
                        pady=5)  # Adiciona 5 pixels de espaçamento vertical.

        # Cria um campo de entrada de texto para o login.
        # O campo permite que o usuário digite o nome de usuário.
        self.login_entry = ttk.Entry(left_frame,  # O campo de entrada é adicionado dentro do `left_frame`.
                                    width=30)  # Define a largura do campo de entrada com 30 caracteres.

        # Posiciona o campo de entrada ao lado do rótulo de login.
        self.login_entry.grid( row=0,  # Posiciona o campo de entrada na mesma linha que o rótulo (linha 0).
                            column=1,  # Posiciona o campo na coluna 1, à direita do rótulo.
                            pady=5)  # Adiciona 5 pixels de espaçamento vertical.

        # Adiciona um rótulo descritivo para o campo de senha.
        # O texto "Senha:" indica que o campo ao lado será usado para a senha do usuário.
        # A fonte é definida como Arial, tamanho 12, e negrito para destacar o texto.
        ttk.Label(left_frame,  # O rótulo é adicionado dentro do `left_frame`.
                text="Senha:",  # Texto exibido no rótulo.
                font=("Arial", 12, "bold")  # Configuração da fonte: Arial, tamanho 12, e negrito.
                ).grid(
                    row=1,  # Posiciona o rótulo na linha 1 do `left_frame`.
                    column=0,  # Posiciona o rótulo na coluna 0, à esquerda.
                    sticky="w",  # Alinha o texto do rótulo à esquerda da célula.
                    pady=5  # Adiciona 5 pixels de espaçamento vertical.
                )

        # Cria um campo de entrada de texto para a senha.
        # O campo permite que o usuário digite a senha.
        # O parâmetro `show="*"` substitui os caracteres digitados por asteriscos para segurança.
        self.senha_entry = ttk.Entry(left_frame,  # O campo de entrada é adicionado dentro do `left_frame`.
                                    width=30,  # Define a largura do campo de entrada com 30 caracteres.
                                    show="*")  # Oculta os caracteres digitados, exibindo asteriscos.


        # Posiciona o campo de entrada ao lado do rótulo de senha.
        self.senha_entry.grid(row=1,  # Posiciona o campo na mesma linha que o rótulo de senha (linha 1).
                            column=1,  # Posiciona o campo na segunda coluna, à direita do rótulo.
                            pady=5)  # Adiciona 5 pixels de espaçamento vertical.


        # Adiciona um rótulo descritivo para o campo de "Nome Completo".
        # O texto "Nome Completo:" indica que o campo ao lado será
        #       usado para o nome completo do usuário.
        # A fonte é definida como Arial, tamanho 12, e negrito para destacar o texto.
        ttk.Label(left_frame,  # O rótulo é adicionado dentro do `left_frame`.
                text="Nome Completo:",  # Texto exibido no rótulo.
                font=("Arial", 12, "bold")  # Configuração da fonte: Arial, tamanho 12, e negrito.
                ).grid(row=2,  # Posiciona o rótulo na linha 2 do `left_frame`.
                        column=0,  # Posiciona o rótulo na coluna 0, à esquerda.
                        sticky="w",  # Alinha o texto do rótulo à esquerda da célula.
                        pady=5)  # Adiciona 5 pixels de espaçamento vertical.

        # Cria um campo de entrada de texto para o nome completo.
        # Este campo permitirá ao usuário inserir seu nome completo.
        self.nome_entry = ttk.Entry(left_frame,  # O campo de entrada é adicionado dentro do `left_frame`.
                                    width=30)  # Define a largura do campo de entrada com 30 caracteres.


        # Posiciona o campo de entrada ao lado do rótulo de "Nome Completo".
        self.nome_entry.grid(row=2,  # Posiciona o campo na mesma linha que o rótulo (linha 2).
                            column=1,  # Posiciona o campo na segunda coluna, à direita do rótulo.
                            pady=5)  # Adiciona 5 pixels de espaçamento vertical.

        # Adiciona um rótulo descritivo para o campo de "Perfil".
        # O texto "Perfil:" indica que o campo ao lado será
        #       usado para selecionar o perfil do usuário.
        # A fonte é definida como Arial, tamanho 12, e negrito
        #       para destacar o texto.
        ttk.Label(left_frame,  # O rótulo é adicionado dentro do `left_frame`.
                    text="Perfil:",  # Texto exibido no rótulo.
                    font=("Arial", 12, "bold")  # Configuração da fonte: Arial, tamanho 12, e negrito.
                    ).grid(row=3,  # Posiciona o rótulo na linha 3 do `left_frame`.
                        column=0,  # Posiciona o rótulo na coluna 0, à esquerda.
                        sticky="w",  # Alinha o texto do rótulo à esquerda da célula.
                        pady=5)  # Adiciona 5 pixels de espaçamento vertical.


        # Cria um campo do tipo combobox para selecionar o perfil do usuário.
        # O combobox permite ao usuário escolher uma das opções
        #       pré-definidas em `PERFIS_USUARIOS`.
        self.perfil_combo = ttk.Combobox(left_frame,  # O combobox é adicionado dentro do `left_frame`.
                                        values=PERFIS_USUARIOS,  # Lista de valores disponíveis para seleção.
                                        width=28)  # Define a largura do combobox com 28 caracteres.


        # Posiciona o combobox ao lado do rótulo de "Perfil".
        self.perfil_combo.grid(row=3,  # Posiciona o combobox na mesma linha que o rótulo (linha 3).
                                column=1,  # Posiciona o combobox na segunda coluna, à direita do rótulo.
                                pady=5)  # Adiciona 5 pixels de espaçamento vertical.


        # Botões de ação
        # Cria um frame para agrupar os botões de ação.
        botoes_frame = ttk.Frame(left_frame)

        # Posiciona o frame na linha 4 do layout do `left_frame`.
        # Ocupa duas colunas e adiciona espaçamento vertical de 10 pixels.
        botoes_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Cria o botão "Adicionar".
        # Este botão será responsável por adicionar novos usuários ao sistema.
        # Define o texto exibido no botão como "Adicionar", para
        #       que o usuário saiba sua funcionalidade.
        # O parâmetro `command=self.adicionar_usuario` associa o método `adicionar_usuario`
        #     para ser executado sempre que o botão for clicado.
        # O botão é posicionado dentro do `botoes_frame` usando o método `pack`.
        # `side="left"` posiciona o botão à esquerda do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Adicionar",
                   command=self.adicionar_usuario).pack(side="left",
                                                        padx=5)

        # Cria o botão "Editar".
        # Este botão será responsável por permitir a edição de
        #       informações de usuários existentes.
        # Define o texto exibido no botão como "Editar", indicando
        #       claramente sua funcionalidade.
        # O parâmetro `command=self.editar_usuario` associa o método `editar_usuario`
        #     para ser executado quando o botão for clicado.
        # O botão é posicionado dentro do `botoes_frame` usando o método `pack`.
        # `side="left"` posiciona o botão à esquerda dentro do frame, alinhado aos outros botões.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Editar",
                   command=self.editar_usuario).pack(side="left",
                                                     padx=5)

        # Cria o botão "Excluir".
        # Este botão será responsável por excluir usuários existentes do sistema.
        # Define o texto exibido no botão como "Excluir", indicando
        #       claramente sua funcionalidade.
        # O parâmetro `command=self.excluir_usuario` associa o método `excluir_usuario`
        #     para ser executado quando o botão for clicado.
        # O botão é posicionado dentro do `botoes_frame` usando o método `pack`.
        # `side="left"` posiciona o botão à esquerda dentro do
        #       frame, alinhado aos outros botões.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Excluir",
                   command=self.excluir_usuario).pack(side="left",
                                                      padx=5)

        # Frame da Treeview à direita.
        # Cria um container para a Treeview que exibirá a lista de usuários.
        # O frame é posicionado à direita do `main_frame` com o parâmetro `side="right"`.
        # `fill="both"` permite que o frame preencha a área disponível em largura e altura.
        # `expand=True` faz com que o frame cresça proporcionalmente
        #       quando a janela é redimensionada.
        # `padx=20` adiciona 20 pixels de espaçamento horizontal externo ao frame.
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        # Cria a Treeview dentro do `right_frame`.
        # A Treeview é usada para exibir uma tabela com as colunas especificadas.
        # As colunas "login", "nome" e "perfil" são criadas para
        #       organizar as informações dos usuários.
        # `show="headings"` faz com que apenas os cabeçalhos das colunas
        #       sejam exibidos, ocultando a coluna principal padrão.
        self.tree = ttk.Treeview(right_frame,
                                 columns=("login", "nome", "perfil"),
                                 show="headings")

        # Define o texto exibido no cabeçalho da coluna "login".
        # O cabeçalho ajuda a identificar que os valores dessa coluna
        #       correspondem ao login do usuário.
        self.tree.heading("login", text="Login")

        # Define o texto exibido no cabeçalho da coluna "nome".
        # O cabeçalho indica que os valores dessa coluna correspondem ao
        #       nome completo do usuário.
        self.tree.heading("nome", text="Nome Completo")

        # Define o texto exibido no cabeçalho da coluna "perfil".
        # O cabeçalho informa que os valores dessa coluna
        #       correspondem ao perfil do usuário.
        self.tree.heading("perfil", text="Perfil")

        # Cria uma barra de rolagem vertical para a Treeview.
        # `orient="vertical"` indica que a barra de rolagem será vertical.
        # O comando `command=self.tree.yview` associa a barra de
        #       rolagem ao movimento vertical da Treeview.
        scroll_usuarios = ttk.Scrollbar(right_frame,
                                        orient="vertical",
                                        command=self.tree.yview)

        # Configura a Treeview para utilizar a barra de rolagem criada.
        # O método `yscroll=scroll_usuarios.set` conecta a barra de rolagem
        #       vertical ao movimento do conteúdo na Treeview.
        self.tree.configure(yscroll=scroll_usuarios.set)

        # Posiciona a Treeview dentro do `right_frame`.
        # `side="left"` alinha a Treeview ao lado esquerdo do frame.
        # `fill="both"` permite que a Treeview preencha a largura e a
        #       altura disponíveis.
        # `expand=True` faz com que a Treeview cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem vertical dentro do `right_frame`.
        # `side="right"` alinha a barra de rolagem ao lado direito do frame.
        # `fill="y"` faz com que a barra de rolagem preencha apenas a altura disponível.
        scroll_usuarios.pack(side="right", fill="y")

        # Associa o evento de seleção de um item na Treeview ao
        #       método `selecionar_item_usuario`.
        # Esse método será chamado sempre que o usuário selecionar
        #       um item na Treeview.
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_usuario)

        # Carrega os dados dos usuários na Treeview ao iniciar.
        # O método `carregar_usuarios` é responsável por buscar e
        #       exibir os usuários na Treeview.
        self.carregar_usuarios()


    # Método para carregar os usuários na Treeview.
    def carregar_usuarios(self):

        # Remove todos os itens existentes na Treeview.
        # O método `get_children` retorna uma lista com os IDs de
        #       todos os itens na Treeview.
        # Para cada ID retornado, o método `delete` remove o
        #       item correspondente da Treeview.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca os dados de usuários na coleção `colecao_usuarios`.
        # O método `find` retorna todos os documentos da coleção.
        # `sort("login", pymongo.ASCENDING)` ordena os documentos
        #       pelo campo "login" em ordem crescente.
        for usuario in colecao_usuarios.find().sort("login",
                                                    pymongo.ASCENDING):

            # Insere cada usuário encontrado na Treeview.
            # O parâmetro `""` indica que o item será inserido na raiz da
            #       Treeview (sem pai).
            # `iid=str(usuario["_id"])` define o ID único do item como o
            #       valor do campo "_id" do documento.
            # `values=(...)` define os valores que serão exibidos nas colunas da
            #       Treeview, correspondendo aos campos "login", "nome" e "perfil".
            self.tree.insert("",
                             "end",
                             iid=str(usuario["_id"]),
                             values=(

                                 # Obtém o valor do campo "login", ou uma string vazia
                                 #       se o campo não existir.
                                 usuario.get("login", ""),

                                 # Obtém o valor do campo "nome", ou uma string vazia se o
                                 #       campo não existir.
                                 usuario.get("nome", ""),

                                 # Obtém o valor do campo "perfil", ou uma string vazia
                                 #       se o campo não existir.
                                 usuario.get("perfil", "")))


    # Método para selecionar um item na Treeview e carregar seus
    #       dados nos campos de entrada.
    def selecionar_item_usuario(self, event=None):

        # Tenta capturar o identificador único (ID) do item selecionado na Treeview.
        try:

            # Pega o primeiro item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Se nenhum item estiver selecionado, interrompe o método.
            return

        # Busca no banco de dados o usuário correspondente ao ID selecionado.
        # `ObjectId(selecionado)` é usado para converter o ID do
        #       formato string para o formato correto usado no MongoDB.
        usuario = colecao_usuarios.find_one({"_id": ObjectId(selecionado)})

        # Se um documento de usuário for encontrado no banco de dados:
        if usuario:

            # Limpa o campo de entrada do login, removendo qualquer texto anterior.
            self.login_entry.delete(0, "end")

            # Insere o login do usuário encontrado no banco de
            #       dados no campo de login.
            self.login_entry.insert(0, usuario.get("login", ""))

            # Limpa o campo de entrada da senha.
            # A senha não é exibida ou preenchida por razões de segurança.
            self.senha_entry.delete(0, "end")

            # Limpa o campo de entrada do nome, removendo qualquer texto anterior.
            self.nome_entry.delete(0, "end")

            # Insere o nome completo do usuário no campo de nome.
            self.nome_entry.insert(0, usuario.get("nome", ""))

            # Define o valor do combobox para refletir o perfil do usuário.
            # Caso o campo "perfil" não esteja definido no banco, o combobox será limpo.
            self.perfil_combo.set(usuario.get("perfil", ""))


    # Método para adicionar um novo usuário ao sistema.
    def adicionar_usuario(self):

        # Obtém o valor do campo de entrada para login.
        # O método `get()` recupera o texto digitado no campo.
        # O método `strip()` remove espaços em branco no início e no fim do texto.
        login = self.login_entry.get().strip()

        # Obtém o valor do campo de entrada para senha.
        # Funciona de forma semelhante ao campo de login.
        senha = self.senha_entry.get().strip()

        # Obtém o valor do campo de entrada para o nome completo.
        # Isso captura o nome do usuário a ser adicionado.
        nome = self.nome_entry.get().strip()

        # Obtém o valor selecionado no campo de perfil.
        # Garante que o perfil esteja definido corretamente.
        perfil = self.perfil_combo.get().strip()

        # Verifica se os campos obrigatórios (login e
        #       senha) estão preenchidos.
        if not login or not senha:

            # Exibe uma mensagem de erro se um dos campos estiver vazio.
            messagebox.showerror("Erro", "Login e Senha são obrigatórios.")
            return

        # Consulta o banco de dados para verificar se já existe um
        #      usuário com o mesmo login.
        existe = colecao_usuarios.find_one({"login": login})

        # Verifica se o login informado já está cadastrado
        #       no banco de dados.
        if existe:

            # Exibe uma mensagem de erro caso o login já exista.
            messagebox.showerror("Erro",
                                 "Já existe um usuário com este login.")
            return

        # Cria um dicionário com os dados do novo usuário.
        novo_usuario = {

            # Define o login do usuário.
            "login": login,

            # Define a senha do usuário.
            "senha": senha,

            # Define o nome completo do usuário.
            "nome": nome,

            # Define o perfil do usuário (ex.: administrador, operador).
            "perfil": perfil

        }

        # Insere o novo usuário na coleção de usuários no banco de dados.
        colecao_usuarios.insert_one(novo_usuario)

        # Recarrega os dados da tabela para incluir o novo usuário.
        self.carregar_usuarios()

        # Limpa os campos de entrada para evitar dados residuais.
        self.limpar_campos()

        # Exibe uma mensagem de sucesso informando que o
        #       usuário foi adicionado.
        messagebox.showinfo("Sucesso",
                            "Usuário adicionado com sucesso.")


    def editar_usuario(self):

        # Tenta obter o ID do usuário selecionado na Treeview.
        try:
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe uma mensagem de erro caso nenhum usuário esteja selecionado.
            messagebox.showerror("Erro",
                                 "Nenhum usuário selecionado.")
            return

        # Obtém e limpa o conteúdo do campo de login.
        login = self.login_entry.get().strip()

        # Obtém e limpa o conteúdo do campo de senha.
        senha = self.senha_entry.get().strip()

        # Obtém e limpa o conteúdo do campo de nome completo.
        nome = self.nome_entry.get().strip()

        # Obtém e limpa o valor selecionado no combobox de perfil.
        perfil = self.perfil_combo.get().strip()

        # Verifica se o campo de login está vazio.
        if not login:

            # Exibe uma mensagem de erro indicando que o login é obrigatório.
            messagebox.showerror("Erro", "Login é obrigatório.")

            # Interrompe a execução do método.
            return

        # Cria um dicionário contendo os dados que serão atualizados.
        atualizacao = {

            "login": login,  # Atualiza o login do usuário.
            "nome": nome,  # Atualiza o nome completo do usuário.
            "perfil": perfil  # Atualiza o perfil do usuário.

        }

        # Verifica se o campo de senha não está vazio.
        if senha:

            # Adiciona a nova senha ao dicionário de atualização.
            atualizacao["senha"] = senha

        # Atualiza os dados do usuário selecionado na coleção do banco de dados.
        # A busca é feita pelo ID do usuário (`_id`) convertido
        #       para o tipo `ObjectId`.
        # `"$set": atualizacao` indica que apenas os campos presentes no
        #       dicionário `atualizacao` serão modificados.
        colecao_usuarios.update_one({"_id": ObjectId(selecionado)},
                                    {"$set": atualizacao})

        # Recarrega a lista de usuários na interface para refletir as
        #       alterações feitas no banco de dados.
        self.carregar_usuarios()

        # Limpa os campos de entrada na interface para que o formulário
        #       esteja pronto para novas ações.
        self.limpar_campos()

        # Exibe uma mensagem de sucesso informando que o usuário foi editado com êxito.
        messagebox.showinfo("Sucesso",
                            "Usuário editado com sucesso.")


    def excluir_usuario(self):

        # Tenta capturar o ID do item atualmente selecionado na Treeview.
        try:
            selecionado = self.tree.selection()[0]

        # Se nada estiver selecionado, exibe uma mensagem de
        #       erro e interrompe a execução.
        except IndexError:
            messagebox.showerror("Erro",
                                 "Nenhum usuário selecionado.")
            return

        # Exibe uma mensagem de confirmação para o usuário, perguntando
        #       se deseja realmente excluir o item.
        resposta = messagebox.askyesno("Confirmar",
                                       "Deseja realmente excluir este usuário?")

        # Se o usuário confirmar a exclusão (clicar em "Sim"):
        if resposta:

            # Remove o documento correspondente ao ID selecionado da coleção `colecao_usuarios`.
            # A busca é feita pelo campo `_id` convertido para o
            #       formato `ObjectId` necessário pelo MongoDB.
            colecao_usuarios.delete_one({"_id": ObjectId(selecionado)})

            # Atualiza a Treeview para refletir a exclusão do usuário.
            self.carregar_usuarios()

            # Limpa os campos de entrada para que não fiquem com
            #       dados do usuário excluído.
            self.limpar_campos()

            # Exibe uma mensagem informando que o usuário foi excluído com sucesso.
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")


    # Método para limpar os campos do formulário de usuários.
    def limpar_campos(self):

        # Limpa o campo de entrada para o login.
        # O método `delete(0, "end")` remove todo o texto do campo de entrada.
        self.login_entry.delete(0, "end")

        # Limpa o campo de entrada para a senha.
        # Assim como no campo de login, todo o texto é removido.
        self.senha_entry.delete(0, "end")

        # Limpa o campo de entrada para o nome completo.
        # Remove qualquer texto que tenha sido inserido no campo.
        self.nome_entry.delete(0, "end")

        # Limpa o campo de seleção para o perfil.
        # O método `set("")` redefine o campo para uma string vazia,
        #       desmarcando qualquer seleção anterior.
        self.perfil_combo.set("")


# ------------------------------------------------------------
# Tela de Login
# ------------------------------------------------------------

# Define a classe Login, que herda de `tk.Tk`, representando a
#       janela principal do sistema.
class Login(tk.Tk):

    # Método construtor da classe, chamado automaticamente ao
    #       instanciar a classe Login.
    def __init__(self):

        # Chama o construtor da classe base `tk.Tk` para inicializar os
        #       componentes do Tkinter.
        # O super().__init__() chama o método __init__ da classe pai (tk.Tk).
        # Isso é necessário para que a classe Login herde todas as
        #       funcionalidades da janela Tkinter.
        # Assim, você não precisa reimplementar a lógica de criação de
        #       uma janela básica do Tkinter.
        super().__init__()

        # Define o título da janela como "Sistema de Cabeleireiro - Login".
        self.title("Sistema de Cabeleireiro - Login")

        # Configura a janela para iniciar em tela cheia.
        self.state('zoomed')

        # Configuração da imagem de fundo.
        # Carrega a imagem do arquivo "cabeleireiro_fundo.jpg".
        # Substitua "cabeleireiro_fundo.jpg" pelo caminho correto da imagem.
        self.background_image = Image.open("cabeleireiro_fundo.jpg")

        # Redimensiona a imagem de fundo para ocupar toda a tela.
        # `winfo_screenwidth()` e `winfo_screenheight()` obtêm a largura e
        #       altura da tela, respectivamente.
        self.background_image = self.background_image.resize((self.winfo_screenwidth(),
                                                              self.winfo_screenheight()))

        # Converte a imagem redimensionada para um formato compatível com Tkinter (PhotoImage).
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Cria um rótulo (`Label`) para exibir a imagem de fundo.
        # Define a imagem convertida como o conteúdo do rótulo.
        self.background_label = tk.Label(self, image=self.background_photo)

        # Posiciona o rótulo da imagem de fundo para preencher toda a janela.
        # `relwidth=1` faz o rótulo ter 100% da largura da janela.
        # `relheight=1` faz o rótulo ter 100% da altura da janela.
        self.background_label.place(relwidth=1, relheight=1)

        # Configurar estilo
        # Aqui é criado um objeto de estilo usando o módulo ttk (do Tkinter).
        # O objeto `style` permite modificar a aparência dos
        #       widgets da interface gráfica.
        self.style = ttk.Style()

        # Define o tema que será usado para os widgets da interface.
        # O método `theme_use("clam")` aplica o tema "clam" para a interface.
        # O "clam" é um tema leve do Tkinter, com um visual mais moderno e sem bordas.
        self.style.theme_use("clam")

        # Configura o estilo para o widget do tipo `TFrame`,
        #       definindo o fundo da tela para branco.
        # Isso significa que qualquer `TFrame` (frame do Tkinter)
        #       nesta aplicação terá o fundo branco.
        self.style.configure("TFrame", background="#ffffff")

        # Configura o estilo para o widget do tipo `TLabel`, que
        #       são os rótulos de texto (labels).
        # Aqui, o fundo é configurado como branco e a fonte é
        #       definida como Arial, com tamanho 11.
        self.style.configure("TLabel",
                             background="#ffffff",
                             font=("Arial", 11))

        # Configura o estilo para o widget do tipo `TButton`, que são os botões.
        # O estilo do botão é configurado com a fonte Arial, tamanho 11, e um
        # padding (espaçamento interno) de 6 pixels.
        self.style.configure("TButton",
                             font=("Arial", 11),
                             padding=6)

        # Frame principal transparente
        # Aqui criamos um frame (uma área de contenção) dentro da janela principal.
        # `bg="#ffffff"` define o fundo do frame como branco.
        # `bd=2` configura a largura da borda do frame em 2 pixels.
        # `relief="ridge"` define um estilo de borda elevada, com linhas que formam um "pico".
        # `place()` é usado para posicionar o frame na janela com base em coordenadas relativas.
        # `relx=0.5` e `rely=0.5` posicionam o frame no centro da janela.
        # `anchor="center"` garante que o centro do frame seja o ponto de referência para o posicionamento.
        # `width=400` e `height=300` definem a largura e altura do frame, respectivamente.
        main_frame = tk.Frame(self,
                              bg="#ffffff",
                              bd=2,
                              relief="ridge")

        main_frame.place(relx=0.5,
                         rely=0.5,
                         anchor="center",
                         width=400,
                         height=300)

        # Criação do rótulo (label) de título
        # `main_frame` é o frame onde o rótulo será adicionado.
        # `text="Bem-vindo(a)!"` define o texto exibido no rótulo
        #       como "Bem-vindo(a)".
        # `font=("Arial", 20, "bold")` define a fonte do texto como Arial,
        #       com tamanho 20 e em negrito (bold).
        # `bg="#ffffff"` define a cor de fundo do rótulo como branca,
        #       combinando com o fundo do frame.
        titulo_label = tk.Label(main_frame,
                                text="Bem-vindo(a)!",
                                font=("Arial", 20, "bold"),
                                bg="#ffffff")

        # Adiciona o rótulo ao frame `main_frame` e define o espaçamento vertical (pady).
        # `pady=20` cria um espaço de 20 pixels acima e abaixo do rótulo,
        #       proporcionando um afastamento visual.
        titulo_label.pack(pady=20)

        # Criação do frame que irá conter o formulário de login
        # `main_frame` é o frame principal que já foi criado anteriormente.
        # `bg="#ffffff"` define a cor de fundo do frame como branca,
        #       mantendo a consistência visual.
        # O frame será usado para agrupar os campos de entrada de
        #       dados (login e senha) e os botões.
        form_frame = tk.Frame(main_frame, bg="#ffffff")

        # Adiciona o frame `form_frame` dentro do `main_frame`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e
        #       abaixo do frame, criando um pequeno espaço entre os elementos.
        form_frame.pack(pady=10)

        # Criação de um rótulo (label) para o campo "Usuário"
        # O texto "Usuário:" será exibido no rótulo, informando ao usuário qual
        #       campo ele precisa preencher.
        # `font=("Arial", 13, "bold")` define a fonte do texto como Arial, tamanho 13, e
        #       em negrito, tornando-o mais visível.
        # `bg="#ffffff"` define a cor de fundo do rótulo como branca, mantendo a
        #       consistência visual com o fundo do formulário.
        # O método `grid()` é utilizado para posicionar o rótulo na posição (0, 0) da grade.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical de 5 pixels ao
        #       redor do rótulo, para garantir que o texto não fique colado nas bordas do campo.
        # `sticky="e"` alinha o texto do rótulo à direita dentro da célula da grade.
        tk.Label(form_frame,
                 text="Usuário:",
                 font=("Arial", 13, "bold"),
                 bg="#ffffff").grid(row=0,
                                    column=0,
                                    padx=5,
                                     pady=5,
                                    sticky="e")

        # Criação de uma caixa de entrada (Entry) para o campo "Usuário"
        # A caixa de entrada permitirá ao usuário digitar o nome de usuário.
        # `width=30` define a largura da caixa de entrada em termos de caracteres.
        # `form_frame` é o container onde a caixa de entrada será posicionada.
        self.usuario_entry = ttk.Entry(form_frame, width=30)

        # Posicionamento da caixa de entrada na grade.
        # `row=0, column=1` posiciona a caixa de entrada na primeira
        #       linha (0) e segunda coluna (1).
        # `padx=5, pady=5` adiciona espaçamento de 5 pixels nas direções
        #       horizontal (padx) e vertical (pady) para que o campo não
        #       fique colado nas bordas.
        self.usuario_entry.grid(row=0, column=1, padx=5, pady=5)

        # Insere o valor padrão "clevison" na caixa de entrada, permitindo que o
        #       campo seja preenchido com esse valor ao ser carregado.
        # Isso pode ser útil para sugerir um valor inicial ou deixar um
        #       valor de exemplo para o usuário.
        self.usuario_entry.insert(0, "clevison")

        # Criação de um rótulo (Label) para o campo "Senha".
        # O texto exibido será "Senha:", o que indica ao usuário que ele
        #       deve preencher esse campo com a senha.
        # A fonte do texto será Arial, com tamanho 13 e em negrito (bold).
        # O fundo do rótulo será branco, para combinar com o fundo da janela.
        tk.Label(form_frame,

                 text="Senha:",  # Define o texto exibido no rótulo.
                 font=("Arial", 13, "bold"),  # Define a fonte como Arial, tamanho 13 e estilo negrito.
                 bg="#ffffff"  # Define o fundo do rótulo como branco.
                 ).grid(row=1,
                        column=0,  # Coloca o rótulo na linha 1, coluna 0 da grade.
                        padx=5,  # Adiciona 5 pixels de espaçamento horizontal à esquerda e à direita.
                        pady=5,  # Adiciona 5 pixels de espaçamento vertical acima e abaixo.
                        sticky="e")  # Alinha o texto do rótulo à direita (leste, "east") da célula.

        # Criação de um campo de entrada (Entry) para a senha.
        # O campo de entrada terá 30 caracteres de largura e exibirá a
        #       senha com caracteres ocultos.
        # O parâmetro 'show="*"' faz com que os caracteres digitados sejam
        #       ocultados, sendo exibidos como asteriscos.
        self.senha_entry = ttk.Entry(form_frame,  # Cria um campo de entrada dentro do frame 'form_frame'.
                                     width=30,  # Define a largura do campo de entrada para 30 caracteres.
                                     show="*")  # Define que os caracteres digitados serão exibidos como asteriscos (*).


        # Coloca o campo de entrada na grade (grid) da interface.
        # Ele estará na linha 1, coluna 1 da grade.
        # O espaçamento horizontal e vertical é de 5 pixels.
        self.senha_entry.grid(row=1,  # Coloca o campo de entrada na linha 1 da grade.
                              column=1,  # Coloca o campo de entrada na coluna 1 da grade.
                              padx=5,  # Adiciona 5 pixels de espaçamento horizontal à esquerda e à direita.
                              pady=5)  # Adiciona 5 pixels de espaçamento vertical acima e abaixo.

        # Insere o valor padrão "555" no campo de entrada para a senha.
        # Isso é útil para demonstração ou testes, mas deve ser removido para produção.
        # Insere o texto "555" no campo de entrada, começando da posição 0 (início).
        self.senha_entry.insert(0, "555")

        # Botões
        # Cria o frame para os botões, dentro do `main_frame`, com fundo branco.
        # O `bg="#ffffff"` define a cor de fundo como branca.
        # O `pady=20` adiciona um espaçamento vertical de 20 pixels ao redor do frame.
        botoes_frame = tk.Frame(main_frame, bg="#ffffff")

        # Coloca o frame de botões dentro da interface.
        # `pady=20` garante que haverá um espaçamento de 20 pixels
        #       ao redor do frame verticalmente.
        botoes_frame.pack(pady=20)

        # Cria o botão "Entrar".
        # O texto do botão é "Entrar" e ao ser clicado, chamará o
        #       método `verificar_login`.
        # Cria o botão dentro do `botoes_frame`.
        btn_entrar = ttk.Button(botoes_frame,

                                # Define o texto do botão como "Entrar".
                                text="Entrar",

                                # Associa o método `verificar_login` ao evento de clique.
                                command=self.verificar_login)

        # Posiciona o botão "Entrar" dentro do `botoes_frame`.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento de 10 pixels à
        #       esquerda e à direita do botão.
        btn_entrar.pack(side="left", padx=10)

        # Cria o botão "Gerenciar Usuários".
        # O texto exibido no botão será "Gerenciar Usuários" e, ao ser
        #       clicado, chama o método `abrir_gerencia_usuarios`.
        btn_gerenciar_usuarios = ttk.Button(botoes_frame,  # Cria o botão dentro do `botoes_frame`.

                                            # Define o texto do botão como "Gerenciar Usuários".
                                            text="Gerenciar Usuários",

                                            # Associa o método `abrir_gerencia_usuarios` ao evento de clique.
                                            command=self.abrir_gerencia_usuarios)

        # Posiciona o botão "Gerenciar Usuários" dentro do `botoes_frame`.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=10` adiciona um espaçamento de 10 pixels à
        #       esquerda e à direita do botão.
        btn_gerenciar_usuarios.pack(side="left", padx=10)


    # Método que abre a tela de gerenciamento de usuários
    def abrir_gerencia_usuarios(self):

        # Cria uma nova instância da classe TelaUsuarios e
        #       passa `self` como o parâmetro,
        # o que significa que a tela de gerenciamento de usuários será
        #       aberta a partir da janela de login.
        TelaUsuarios(self)

    # Método que verifica o login do usuário
    def verificar_login(self):

        # Obtém o nome de usuário inserido no campo de entrada, removendo
        #       espaços em branco antes e depois do texto.
        usuario = self.usuario_entry.get().strip()

        # Obtém a senha inserida no campo de entrada, removendo espaços em
        #       branco antes e depois do texto.
        senha = self.senha_entry.get().strip()

        # Busca no banco de dados `colecao_usuarios` por um usuário que tenha o
        #       login e a senha correspondentes aos dados fornecidos.
        # O método `find_one` retorna o primeiro documento que
        #       corresponder aos critérios de pesquisa.
        user_db = colecao_usuarios.find_one({"login": usuario, "senha": senha})

        # Se o usuário for encontrado no banco de dados
        if user_db:

            # Exibe uma mensagem de sucesso com o nome do usuário,
            #       obtido do banco de dados.
            messagebox.showinfo("Sucesso", f"Login bem-sucedido! Bem-vindo, {user_db.get('nome', '')}")

            # Fecha a janela de login atual.
            self.destroy()

            # Abre a janela principal após o login bem-sucedido.
            MainWindow()

        else:

            # Se o usuário não for encontrado ou as credenciais forem
            #       inválidas, exibe uma mensagem de erro.
            messagebox.showerror("Erro", "Credenciais inválidas.")


# ------------------------------------------------------------
# Janela Principal (com Menu Lateral)
# ------------------------------------------------------------
class MainWindow(tk.Tk):

    """
    Janela principal com menu lateral e área de conteúdo.
    """

    # Método de inicialização (construtor) da classe, chamado
    #       automaticamente quando a classe é instanciada.
    def __init__(self):

        # Chama o construtor da classe pai (classe Tk).
        # `super()` é uma maneira de chamar métodos da classe base (no caso, tk.Tk)
        #       sem precisar especificar diretamente o nome da classe.
        super().__init__()

        # Define o título da janela.
        # `self.title()` configura o texto exibido na barra de título da janela.
        self.title("Sistema de Cabeleireiro - Profissional")

        # Define a janela como maximizada na inicialização.
        # `self.state('zoomed')` faz com que a janela ocupe a
        #       tela inteira assim que aberta.
        self.state('zoomed')

        # Configura o fundo da janela com a cor branca.
        # `self.configure(bg="#FFFFFF")` define a cor de
        #       fundo da janela como branco.
        self.configure(bg="#FFFFFF")

        # Inicializa o estilo dos widgets do Tkinter.
        # `self.style = ttk.Style()` cria um objeto de estilo para os widgets.
        self.style = ttk.Style()

        # Aplica o tema "clam" nos widgets.
        # `self.style.theme_use("clam")` seleciona o tema "clam", que é
        #       um tema simples e leve.
        self.style.theme_use("clam")

        # Configura o estilo do widget "TFrame"
        # `self.style.configure("TFrame", background="#FFFFFF")` define
        #       que o fundo de qualquer widget do tipo "TFrame"
        #       (que é um frame do ttk) será branco (#FFFFFF).
        self.style.configure("TFrame", background="#FFFFFF")

        # Configura o estilo do widget "TLabel"
        # `self.style.configure("TLabel", background="#FFFFFF",
        #       font=("Arial", 11))` define que qualquer rótulo
        # (label) do ttk terá o fundo branco (#FFFFFF) e a fonte Arial com tamanho 11.
        self.style.configure("TLabel", background="#FFFFFF", font=("Arial", 11))

        # Configura o estilo do widget "TButton"
        # `self.style.configure("TButton", font=("Arial", 11), padding=6)`
        #       define que os botões terão a fonte Arial com tamanho 11 e um
        #       preenchimento (padding) de 6 unidades em torno do texto do botão.
        self.style.configure("TButton", font=("Arial", 11), padding=6)

        # Configura o estilo personalizado para um botão com classe "SideButton.TButton"
        # `self.style.configure("SideButton.TButton", foreground="#FFFFFF",
        #       background="#444444")` define que os botões com a
        #       classe "SideButton.TButton" terão o texto na cor branca (#FFFFFF) e
        #       o fundo em cinza escuro (#444444).
        self.style.configure("SideButton.TButton",
                             foreground="#FFFFFF",
                             background="#444444")

        # Define a cor do fundo do botão da classe "SideButton.TButton"
        #       quando ele está ativo (pressionado).
        # `self.style.map("SideButton.TButton", background=[("active", "#666666")])`
        #       muda o fundo para cinza claro (#666666)
        #       quando o botão estiver ativo (quando o usuário
        #       clicar ou passar o mouse sobre ele).
        self.style.map("SideButton.TButton", background=[("active", "#666666")])

        # Header
        # Cria o frame para o cabeçalho da interface, com estilo "TFrame".
        # `self` se refere à instância da janela principal, que é o container do widget.
        # O `style="TFrame"` aplica o estilo configurado previamente para o TFrame.
        header_frame = ttk.Frame(self, style="TFrame")

        # Posiciona o `header_frame` no topo da janela, ocupando toda a largura disponível.
        # `side="top"` coloca o frame no topo da janela, e `fill="x"` faz com que o frame
        # ocupe toda a largura disponível horizontalmente.
        header_frame.pack(side="top", fill="x")

        # Cria o rótulo (label) que servirá como título da janela.
        # O texto exibido será "Sistema de Cabeleireiro", com
        #       fonte Arial em tamanho 20 e negrito.
        header_label = ttk.Label(header_frame,
                                 text="Sistema de Cabeleireiro",
                                 font=("Arial", 20, "bold"))

        # Posiciona o rótulo dentro do frame `header_frame` e
        #       aplica um espaçamento de 20 pixels
        #       acima e abaixo do rótulo.
        header_label.pack(pady=20)

        # Área principal
        # Cria o frame principal dentro da janela, aplicando o estilo "TFrame".
        # O `self` se refere à janela principal, e o `style="TFrame"`
        #       aplica o estilo configurado anteriormente.
        main_frame = ttk.Frame(self, style="TFrame")

        # Posiciona o `main_frame` no topo da janela e faz com que ele
        #       ocupe tanto a largura quanto a altura disponíveis.
        # `side="top"` coloca o frame no topo da janela, e `fill="both"` faz
        #       com que o frame ocupe tanto a largura quanto a altura.
        # `expand=True` permite que o frame se expanda conforme a
        #       janela é redimensionada.
        main_frame.pack(side="top", fill="both", expand=True)

        # Cria o frame para o menu lateral dentro do `main_frame`,
        #       com uma largura fixa de 220 pixels.
        # O `style="TFrame"` aplica o estilo configurado para o TFrame, e a
        #       largura do menu é configurada diretamente.
        self.sidebar_frame = ttk.Frame(main_frame, width=220, style="TFrame")

        # Posiciona o `sidebar_frame` no lado esquerdo da janela e faz com
        #       que ele preencha a altura disponível.
        # `side="left"` coloca o frame no lado esquerdo, e `fill="y"` faz
        #       com que o menu preencha toda a altura disponível.
        self.sidebar_frame.pack(side="left", fill="y")

        # Conteúdo
        # Cria o frame para o conteúdo principal da janela, aplicando o estilo "TFrame".
        # O frame será posicionado no lado direito do `main_frame` e ocupará o
        #       espaço restante disponível.
        # `side="right"` coloca o frame à direita do menu lateral, `fill="both"`
        #        faz com que ele ocupe tanto a largura quanto a altura.
        # `expand=True` permite que o conteúdo se expanda proporcionalmente
        #         ao redimensionar a janela.
        self.content_frame = ttk.Frame(main_frame, style="TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Cria o botão "Agendamentos" no menu lateral, aplicando o
        #       estilo "SideButton.TButton".
        # `text="Agendamentos"` define o texto exibido no botão.
        # `style="SideButton.TButton"` aplica um estilo personalizado
        #       para os botões do menu lateral.
        # `command=self.mostrar_agendamentos` define o método a ser
        #       chamado quando o botão for clicado.
        # O `pack(fill="x")` faz com que o botão ocupe toda a largura
        #       disponível horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Agendamentos",
                   style="SideButton.TButton",
                   command=self.mostrar_agendamentos).pack(fill="x",
                                                           padx=5,
                                                           pady=5)

        # Cria o botão "Clientes" no menu lateral, aplicando o estilo "SideButton.TButton".
        # O texto exibido no botão é "Clientes".
        # `style="SideButton.TButton"` aplica o estilo personalizado para os botões do menu lateral.
        # `command=self.mostrar_clientes` associa o método `mostrar_clientes` ao
        #       evento de clique no botão.
        # `fill="x"` faz com que o botão ocupe toda a largura disponível horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Clientes",
                   style="SideButton.TButton",
                   command=self.mostrar_clientes).pack(fill="x",
                                                       padx=5,
                                                       pady=5)

        # Cria o botão "Serviços" no menu lateral, aplicando o
        #       estilo "SideButton.TButton".
        # O texto exibido no botão é "Serviços".
        # `style="SideButton.TButton"` aplica o estilo personalizado
        #       para os botões do menu lateral.
        # `command=self.mostrar_servicos` associa o método `mostrar_servicos` ao
        #       evento de clique no botão.
        # `fill="x"` faz com que o botão ocupe toda a largura disponível horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Serviços",
                   style="SideButton.TButton",
                   command=self.mostrar_servicos).pack(fill="x",
                                                       padx=5,
                                                       pady=5)

        # Cria o botão "Produtos" no menu lateral, aplicando o
        #       estilo "SideButton.TButton".
        # O texto exibido no botão é "Produtos".
        # `style="SideButton.TButton"` aplica o estilo personalizado
        #       para os botões do menu lateral.
        # `command=self.mostrar_produtos` associa o método `mostrar_produtos` ao
        #       evento de clique no botão.
        # `fill="x"` faz com que o botão ocupe toda a largura disponível
        #       horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e
        #       vertical ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Produtos",
                   style="SideButton.TButton",
                   command=self.mostrar_produtos).pack(fill="x",
                                                       padx=5,
                                                       pady=5)

        # Cria o botão "Funcionários" no menu lateral, aplicando o
        #       estilo "SideButton.TButton".
        # O texto exibido no botão é "Funcionários".
        # `style="SideButton.TButton"` aplica o estilo personalizado
        #       para os botões do menu lateral.
        # `command=self.mostrar_funcionarios` associa o método
        #       `mostrar_funcionarios` ao evento de clique no botão.
        # `fill="x"` faz com que o botão ocupe toda a largura
        #       disponível horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Funcionários",
                   style="SideButton.TButton",
                   command=self.mostrar_funcionarios).pack(fill="x",
                                                           padx=5,
                                                           pady=5)

        # Cria o botão "Relatórios" no menu lateral, aplicando o
        #       estilo "SideButton.TButton".
        # O texto exibido no botão é "Relatórios".
        # `style="SideButton.TButton"` aplica o estilo personalizado
        #       para os botões do menu lateral.
        # `command=self.mostrar_relatorios` associa o método
        #       `mostrar_relatorios` ao evento de clique no botão.
        # `fill="x"` faz com que o botão ocupe toda a largura disponível horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Relatórios",
                   style="SideButton.TButton",
                   command=self.mostrar_relatorios).pack(fill="x",
                                                         padx=5,
                                                         pady=5)

        # Cria um rótulo em branco, usado como espaçamento visual.
        # O rótulo não possui texto (`text=""`), então ele serve apenas para
        #       adicionar um espaçamento entre os botões do menu.
        # `pady=20` adiciona um espaçamento vertical de 20 pixels ao redor do rótulo.
        ttk.Label(self.sidebar_frame, text="").pack(pady=20)

        # Cria o botão "Sair" no menu lateral, aplicando o estilo "SideButton.TButton".
        # O texto exibido no botão é "Sair".
        # `style="SideButton.TButton"` aplica o estilo personalizado
        #       para os botões do menu lateral.
        # `command=self.destroy` associa o método `self.destroy` ao
        #       evento de clique no botão.
        # O método `self.destroy` encerra a janela principal do Tkinter,
        #       fechando o aplicativo quando o botão for clicado.
        # `fill="x"` faz com que o botão ocupe toda a largura
        #       disponível horizontalmente no menu.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do botão.
        ttk.Button(self.sidebar_frame,
                   text="Sair",
                   style="SideButton.TButton",
                   command=self.destroy).pack(fill="x", padx=5, pady=5)

        # A variável `self.current_frame` é definida como `None`, que
        #       será usada para armazenar o frame atual.
        # Inicializa `self.current_frame` como `None` para garantir que
        #       não haja um frame ativo previamente.
        self.current_frame = None

        # Chama o método `mostrar_agendamentos` que irá exibir a
        #       tela de agendamentos.
        # Isso configura a tela inicial do aplicativo para mostrar os
        #       agendamentos assim que o programa é iniciado.
        self.mostrar_agendamentos()

        # Inicia o loop principal do Tkinter.
        # O `mainloop()` mantém a interface gráfica em execução,
        #       aguardando interações do usuário.
        self.mainloop()


    # Define o método `clear_content_frame` para limpar a área de conteúdo.
    # Esse método será utilizado para remover o frame atual (se houver)
    #       antes de carregar uma nova tela.
    def clear_content_frame(self):

        # Verifica se existe um frame atual para destruir.
        # `self.current_frame` armazena o frame atualmente exibido.
        # Se for diferente de None, significa que há um
        #       frame a ser removido.
        if self.current_frame is not None:

            # Chama o método `destroy()` no frame atual, removendo-o da interface.
            # Isso garante que o frame anterior seja apagado da tela
            #       antes de adicionar um novo.
            self.current_frame.destroy()

            # Define `self.current_frame` como `None` após destruir o frame.
            # Isso garante que não haverá referência a um frame
            #       antigo, preparando para um novo frame.
            self.current_frame = None

    # Navegação pelas telas:
    # Define o método `mostrar_agendamentos`, que será responsável
    #       por exibir a tela de agendamentos.
    # Este método será chamado para mostrar a interface relacionada
    #       aos agendamentos no sistema.
    def mostrar_agendamentos(self):

        # Chama o método `clear_content_frame` para limpar qualquer
        #       conteúdo anterior da área de conteúdo.
        # Isso é importante para garantir que, ao exibir uma nova tela, o
        #       conteúdo anterior seja removido.
        self.clear_content_frame()

        # Cria uma nova instância da tela de agendamentos,
        #       passando `self.content_frame` como o frame pai.
        # Isso significa que o conteúdo de agendamentos será
        #       exibido dentro do `content_frame`.
        self.current_frame = TelaAgendamentos(self.content_frame)

        # Após criar a instância da tela de agendamentos, usa o
        #       método `pack` para exibir o frame na interface.
        # `fill="both"` faz com que o frame ocupe tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente,
        #       ajustando-se ao tamanho da janela.
        self.current_frame.pack(fill="both", expand=True)


    # Define o método `mostrar_clientes`, responsável por
    #       exibir a tela de clientes.
    # Este método será chamado para mostrar a interface
    #       relacionada aos clientes no sistema.
    def mostrar_clientes(self):

        # Chama o método `clear_content_frame` para limpar qualquer
        #       conteúdo anterior da área de conteúdo.
        # Isso é importante para garantir que, ao exibir uma nova
        #       tela, o conteúdo anterior seja removido.
        self.clear_content_frame()

        # Cria uma nova instância da tela de clientes, passando
        #       `self.content_frame` como o frame pai.
        # Isso significa que o conteúdo de clientes será exibido
        #       dentro do `content_frame`.
        self.current_frame = TelaClientes(self.content_frame)

        # Após criar a instância da tela de clientes, usa o
        #       método `pack` para exibir o frame na interface.
        # `fill="both"` faz com que o frame ocupe tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente,
        #       ajustando-se ao tamanho da janela.
        self.current_frame.pack(fill="both", expand=True)


    # Define o método `mostrar_servicos`, responsável por
    #       exibir a tela de serviços.
    # Este método será chamado para mostrar a interface
    #       relacionada aos serviços no sistema.
    def mostrar_servicos(self):

        # Chama o método `clear_content_frame` para limpar qualquer
        #       conteúdo anterior da área de conteúdo.
        # Isso é importante para garantir que, ao exibir uma nova tela, o
        #       conteúdo anterior seja removido.
        self.clear_content_frame()

        # Cria uma nova instância da tela de serviços, passando
        #       `self.content_frame` como o frame pai.
        # Isso significa que o conteúdo de serviços será exibido
        #       dentro do `content_frame`.
        self.current_frame = TelaServicos(self.content_frame)

        # Após criar a instância da tela de serviços, usa o
        #       método `pack` para exibir o frame na interface.
        # `fill="both"` faz com que o frame ocupe tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente,
        #       ajustando-se ao tamanho da janela.
        self.current_frame.pack(fill="both", expand=True)


    # Define o método `mostrar_produtos`, responsável por
    #       exibir a tela de produtos.
    # Este método será chamado para mostrar a interface
    #       relacionada aos produtos no sistema.
    def mostrar_produtos(self):

        # Chama o método `clear_content_frame` para limpar qualquer
        #       conteúdo anterior da área de conteúdo.
        # Isso é importante para garantir que, ao exibir uma nova
        #       tela, o conteúdo anterior seja removido.
        self.clear_content_frame()

        # Cria uma nova instância da tela de produtos, passando
        #       `self.content_frame` como o frame pai.
        # Isso significa que o conteúdo de produtos será exibido
        #       dentro do `content_frame`.
        self.current_frame = TelaProdutos(self.content_frame)

        # Após criar a instância da tela de produtos, usa o método `pack`
        #       para exibir o frame na interface.
        # `fill="both"` faz com que o frame ocupe tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente,
        #       ajustando-se ao tamanho da janela.
        self.current_frame.pack(fill="both", expand=True)


    # Define o método `mostrar_funcionarios`, responsável por
    #       exibir a tela de funcionários.
    # Este método será chamado para mostrar a interface relacionada aos
    #       funcionários no sistema.
    def mostrar_funcionarios(self):

        # Chama o método `clear_content_frame` para limpar qualquer
        #       conteúdo anterior da área de conteúdo.
        # Isso é importante para garantir que, ao exibir uma nova tela, o
        #       conteúdo anterior seja removido.
        self.clear_content_frame()

        # Cria uma nova instância da tela de funcionários,
        #       passando `self.content_frame` como o frame pai.
        # Isso significa que o conteúdo de funcionários será
        #       exibido dentro do `content_frame`.
        self.current_frame = TelaFuncionarios(self.content_frame)

        # Após criar a instância da tela de funcionários, usa o
        #       método `pack` para exibir o frame na interface.
        # `fill="both"` faz com que o frame ocupe tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente,
        #       ajustando-se ao tamanho da janela.
        self.current_frame.pack(fill="both", expand=True)

    # Define o método `mostrar_relatorios`, responsável por
    #       exibir a tela de relatórios.
    # Este método será chamado para mostrar a interface
    #       relacionada aos relatórios no sistema.
    def mostrar_relatorios(self):

        # Chama o método `clear_content_frame` para limpar qualquer
        #       conteúdo anterior da área de conteúdo.
        # Isso é importante para garantir que, ao exibir uma nova
        #       tela, o conteúdo anterior seja removido.
        self.clear_content_frame()

        # Cria uma nova instância da tela de relatórios,
        #       passando `self.content_frame` como o frame pai.
        # Isso significa que o conteúdo de relatórios será exibido
        #       dentro do `content_frame`.
        self.current_frame = TelaRelatorios(self.content_frame)

        # Após criar a instância da tela de relatórios, usa o
        #       método `pack` para exibir o frame na interface.
        # `fill="both"` faz com que o frame ocupe tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente,
        #       ajustando-se ao tamanho da janela.
        self.current_frame.pack(fill="both", expand=True)


# ------------------------------------------------------------
# Tela de Agendamentos
# ------------------------------------------------------------

# Método construtor da classe `TelaAgendamentos`, chamado automaticamente ao
#       criar uma nova instância dessa classe.
# `parent` é o widget pai que vai conter essa tela, geralmente o
#       frame principal da aplicação.
class TelaAgendamentos(ttk.Frame):

    # Método construtor da classe `TelaAgendamentos`, chamado
    #       automaticamente ao criar uma nova instância dessa classe.
    # `parent` é o widget pai que vai conter essa tela o
    #       frame principal da aplicação.
    def __init__(self, parent):

        # Chama o construtor da classe pai (ttk.Frame) para inicializar a
        #       classe de forma apropriada.
        # Isso é necessário para garantir que a tela herde todos os
        #       comportamentos do widget base.
        # O `parent` é passado para o construtor da classe pai para que a
        #       tela seja corretamente inserida dentro do widget pai.
        super().__init__(parent)

        # Cria um rótulo (Label) com o texto "Agendamentos", utilizando a
        #       fonte Arial de tamanho 16 e em negrito.
        # O rótulo será exibido no topo da tela.
        # `anchor="w"` alinha o texto à esquerda dentro do rótulo.
        # `padx=10` e `pady=10` adicionam espaçamento ao redor do rótulo
        #       para garantir que não fique colado às bordas.
        ttk.Label(self, text="Agendamentos", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=10)

        # Cria o `main_frame`, que será o contêiner principal desta tela.
        # O parâmetro `padding=10` adiciona um espaçamento interno ao redor
        #       do conteúdo do frame.
        # O método `pack` posiciona o frame na tela, com `fill="both"` fazendo
        #       com que o frame ocupe tanto a largura quanto a altura disponíveis.
        # O `expand=True` faz com que o `main_frame` cresça proporcionalmente
        #       caso a tela seja redimensionada.
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Cria o `left_frame`, que vai ficar à esquerda do `main_frame` e
        #       irá conter o calendário e os formulários.
        # O método `pack` com `side="left"` alinha o `left_frame` à esquerda do `main_frame`.
        # O `fill="y"` faz com que o `left_frame` ocupe toda a altura
        #       disponível, mas não a largura.
        # `padx=10` e `pady=5` adicionam espaçamento extra nas
        #       margens do `left_frame`.
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=10, pady=5)

        # Calendário
        # Cria o widget `Calendar` chamado `calendario`, dentro do `left_frame`.
        # O parâmetro `selectmode="day"` define que o calendário permitirá a
        #       seleção de um único dia.
        # O parâmetro `date_pattern="dd/MM/yyyy"` define o formato de exibição da
        #       data, onde o dia vem primeiro, seguido do mês e ano (formato brasileiro).
        self.calendario = Calendar(left_frame, selectmode="day", date_pattern="dd/MM/yyyy")

        # Posiciona o calendário dentro do `left_frame` com o método `pack`.
        # O `anchor="n"` faz com que o calendário seja ancorado à parte
        #       superior do `left_frame` (ao norte).
        # `padx=5` adiciona um espaçamento horizontal extra (5 pixels) em
        #       relação ao `left_frame`.
        # `pady=5` adiciona um espaçamento vertical extra (5 pixels) em
        #       relação ao `left_frame`.
        self.calendario.pack(anchor="n", padx=5, pady=5)

        # Formulário de agendamentos
        # Cria um frame chamado `form_frame` dentro de `left_frame`, onde
        #       serão colocados os campos de entrada.
        # O `anchor="n"` faz com que o frame seja ancorado na parte
        #       superior do `left_frame`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels em
        #       relação ao topo do `left_frame`.
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(anchor="n", pady=10)

        # Cria um rótulo (Label) dentro de `form_frame` com o texto "Hora Início:".
        # `row=0, column=0` posiciona o rótulo na primeira linha (0) e
        #       primeira coluna (0) da grid.
        # `padx=5` e `pady=5` adicionam um pequeno espaçamento horizontal e
        #       vertical ao redor do rótulo.
        # `sticky="e"` faz com que o texto fique alinhado à direita (east)
        #       da célula da grid.
        ttk.Label(form_frame,
                  text="Hora Início:").grid(row=0,
                                            column=0,
                                            padx=5,
                                            pady=5,
                                            sticky="e")

        # Cria uma entrada de texto (`Entry`) dentro de `form_frame`, onde o
        #       usuário pode digitar a hora de início.
        # O parâmetro `width=10` define a largura da caixa de entrada como 10 caracteres.
        # A entrada será posicionada na primeira linha (0) e segunda coluna (1) da grid.
        # `padx=5` e `pady=5` adicionam espaçamento em torno da entrada.
        self.inicio_entry = ttk.Entry(form_frame, width=10)
        self.inicio_entry.grid(row=0, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) no `form_frame` com o texto "Hora Fim:".
        # O rótulo indica que o próximo campo é para inserir a hora de término.
        # `row=1` posiciona o rótulo na segunda linha (linha 1) da grid do `form_frame`.
        # `column=0` posiciona o rótulo na primeira coluna da grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do rótulo.
        # `sticky="e"` faz com que o texto do rótulo fique alinhado à
        #       direita (east) na célula da grid.
        ttk.Label(form_frame,
                  text="Hora Fim:").grid(row=1,
                                         column=0,
                                         padx=5,
                                         pady=5,
                                         sticky="e")

        # Cria uma entrada de texto (Entry) no `form_frame` onde o
        #       usuário pode inserir a hora de término.
        # `width=10` define a largura da caixa de entrada como 10 caracteres.
        # `row=1` posiciona a entrada de texto na segunda linha (linha 1)
        #       da grid do `form_frame`.
        # `column=1` posiciona a entrada na segunda coluna da grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta da entrada.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta da entrada.
        self.fim_entry = ttk.Entry(form_frame, width=10)
        self.fim_entry.grid(row=1, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) ao `form_frame` com o texto "Cliente:".
        # Esse rótulo serve para indicar ao usuário que o próximo
        #       campo é para selecionar o cliente.
        # `row=2` posiciona o rótulo na terceira linha (linha 2) da grid do `form_frame`.
        # `column=0` posiciona o rótulo na primeira coluna da grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do rótulo.
        # `sticky="e"` faz com que o texto do rótulo fique alinhado à
        #       direita (east) dentro da célula da grid.
        ttk.Label(form_frame,
                  text="Cliente:").grid(row=2,
                                        column=0,
                                        padx=5,
                                        pady=5,
                                        sticky="e")

        # Cria uma caixa de combinação (Combobox) dentro do `form_frame`
        #       para permitir a seleção de clientes.
        # `width=25` define a largura da caixa de seleção como 25 caracteres.
        # `values=self.listar_clientes()` preenche a lista de opções com os
        #       valores retornados pelo método `listar_clientes()`.
        # Esse método retorna uma lista de clientes
        #       cadastrados no sistema.
        self.cliente_combo = ttk.Combobox(form_frame,
                                          width=25,
                                          values=self.listar_clientes())

        # Posiciona a caixa de combinação na terceira linha (linha 2) e
        #       segunda coluna (column=1) da grid do `form_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em
        #       volta da caixa de seleção.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       em volta da caixa de seleção.
        self.cliente_combo.grid(row=2, column=1, padx=5, pady=5)

        # Cria um frame (`botoes_frame`) dentro do `left_frame`
        #       para organizar os botões.
        # O frame é usado para agrupar e alinhar os botões relacionados,
        #       mantendo o layout mais estruturado.
        botoes_frame = ttk.Frame(left_frame)

        # Posiciona o `botoes_frame` dentro do `left_frame` usando o método `pack`.
        # `anchor="n"` alinha o frame no topo (norte) do `left_frame`.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do frame.
        botoes_frame.pack(anchor="n", pady=10)

        # Botão para Selecionar Serviços
        # Cria um botão `btn_selecionar` dentro do frame `botoes_frame`.
        # O botão terá o texto "Selecionar Serviços" e, ao ser clicado,
        #       chamará o método `self.abrir_tela_selecao`.
        # Define o `botoes_frame` como contêiner pai do botão.
        btn_selecionar = ttk.Button(botoes_frame,

                                    # Define o texto exibido no botão.
                                    text="Selecionar Serviços",

                                    # Associa o método `self.abrir_tela_selecao` ao
                                    #       evento de clique do botão.
                                    command=self.abrir_tela_selecao)

        # Posiciona o botão `btn_selecionar` dentro do grid layout do `botoes_frame`.
        # `row=0` define a linha onde o botão será colocado.
        # `column=0` define a coluna onde o botão será colocado.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em ambos os lados do botão.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do botão.
        # `sticky="ew"` faz com que o botão se expanda horizontalmente para
        #       preencher completamente a célula.
        btn_selecionar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Aplica o estilo personalizado "Selecionar.TButton" ao botão `btn_selecionar`.
        # Esse estilo pode ser definido anteriormente no código para
        #       personalizar a aparência do botão.
        btn_selecionar.configure(style="Selecionar.TButton")

        # Botão para Agendar
        # Cria um botão `btn_agendar` dentro do frame `botoes_frame`.
        # O botão terá o texto "Agendar" e, ao ser clicado, chamará o método `self.agendar`.
        btn_agendar = ttk.Button(
            botoes_frame,  # Define o `botoes_frame` como contêiner pai do botão.
            text="Agendar",  # Define o texto exibido no botão como "Agendar".
            command=self.agendar  # Associa o método `self.agendar` ao evento de clique no botão.
        )

        # Posiciona o botão `btn_agendar` dentro do grid layout do `botoes_frame`.
        # `row=1` define que o botão será colocado na segunda linha (a contagem começa em 0).
        # `column=0` define que o botão estará na primeira coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em ambos os lados do botão.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do botão.
        # `sticky="ew"` faz com que o botão se expanda horizontalmente
        #       para preencher a largura da célula.
        btn_agendar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Aplica o estilo personalizado "Agendar.TButton" ao botão `btn_agendar`.
        # Este estilo pode ser configurado previamente para definir cores,
        #       bordas e outros aspectos visuais do botão.
        btn_agendar.configure(style="Agendar.TButton")

        # Botão para Finalizar Serviço
        # Cria um botão chamado `btn_finalizar` dentro do frame `botoes_frame`.
        # O texto do botão é "Finalizar Serviço" e ele está associado ao
        #       método `self.finalizar_servico`,
        #       que será chamado quando o botão for clicado.
        # Define `botoes_frame` como o contêiner pai do botão.
        btn_finalizar = ttk.Button(botoes_frame,

                                   # Define o texto exibido no botão.
                                    text="Finalizar Serviço",

                                   # Associa o método `self.finalizar_servico` ao evento de clique.
                                    command=self.finalizar_servico)

        # Posiciona o botão `btn_finalizar` dentro do layout em
        #       grade (grid layout) do frame `botoes_frame`.
        # `row=2` posiciona o botão na terceira linha (a contagem começa em 0).
        # `column=0` posiciona o botão na primeira coluna.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels em ambos os lados do botão.
        # `pady=5` adiciona espaçamento vertical de 5 pixels acima e abaixo do botão.
        # `sticky="ew"` faz com que o botão se expanda horizontalmente
        #       para preencher toda a largura da célula.
        btn_finalizar.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Aplica um estilo personalizado chamado "Finalizar.TButton" ao
        #       botão `btn_finalizar`.
        # Esse estilo pode ser previamente configurado
        #       usando o `ttk.Style` para personalizar
        #       a aparência visual, como cor de fundo, bordas ou fonte.
        btn_finalizar.configure(style="Finalizar.TButton")

        # Botão para Deletar Agendamento
        # Cria um botão chamado `btn_deletar` dentro do frame `botoes_frame`.
        # O texto do botão é "Deletar Agendamento" e ele está
        #       associado ao método `self.deletar_agendamento`,
        #       que será chamado quando o botão for clicado.
        # Define `botoes_frame` como o contêiner pai do botão.
        btn_deletar = ttk.Button(botoes_frame,

                                 # Define o texto exibido no botão.
                                text="Deletar Agendamento",

                                 # Associa o método `self.deletar_agendamento` ao evento de clique.
                                command=self.deletar_agendamento)

        # Posiciona o botão `btn_deletar` dentro do layout em
        #       grade (grid layout) do frame `botoes_frame`.
        # `row=3` posiciona o botão na quarta linha (a contagem começa em 0).
        # `column=0` posiciona o botão na primeira coluna.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels em ambos os lados do botão.
        # `pady=5` adiciona espaçamento vertical de 5 pixels acima e abaixo do botão.
        # `sticky="ew"` faz com que o botão se expanda horizontalmente
        #       para preencher toda a largura da célula.
        btn_deletar.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Aplica um estilo personalizado chamado "Deletar.TButton" ao botão `btn_deletar`.
        # Esse estilo pode ser configurado previamente usando o `ttk.Style` para personalizar
        # a aparência visual, como cor de fundo, bordas ou fonte.
        btn_deletar.configure(style="Deletar.TButton")

        # Adicionar estilos para os botões com cores diferentes
        # Cria uma instância de `ttk.Style` para configurar os
        #       estilos dos widgets personalizados.
        self.style = ttk.Style()

        # Configura o estilo "Selecionar.TButton".
        # `background="#FFD700"` define a cor de fundo como dourado.
        # `foreground="black"` define a cor do texto como preto.
        self.style.configure(
            "Selecionar.TButton",  # Nome do estilo.
            background="#FFD700",  # Cor de fundo (dourado).
            foreground="black"  # Cor do texto (preto).
        )

        # Configura o estilo "Agendar.TButton".
        # `background="#32CD32"` define a cor de fundo como verde.
        # `foreground="white"` define a cor do texto como branco.
        self.style.configure(
            "Agendar.TButton",  # Nome do estilo.
            background="#32CD32",  # Cor de fundo (verde).
            foreground="white"  # Cor do texto (branco).
        )

        # Configura o estilo "Finalizar.TButton".
        # `background="#1E90FF"` define a cor de fundo como azul.
        # `foreground="white"` define a cor do texto como branco.
        self.style.configure(
            "Finalizar.TButton",  # Nome do estilo.
            background="#1E90FF",  # Cor de fundo (azul).
            foreground="white"  # Cor do texto (branco).
        )

        # Configura o estilo "Deletar.TButton".
        # `background="#FF4500"` define a cor de fundo como vermelho.
        # `foreground="white"` define a cor do texto como branco.
        self.style.configure(
            "Deletar.TButton",  # Nome do estilo.
            background="#FF4500",  # Cor de fundo (vermelho).
            foreground="white"  # Cor do texto (branco).
        )

        # Frame direito (Mapa de horários + lista de agendamentos)
        # Cria um frame à direita do frame principal para conter os
        #       elementos do lado direito da interface.
        right_frame = ttk.Frame(main_frame)

        # Posiciona o frame à direita.
        # `side="right"` alinha o frame ao lado direito do frame principal.
        # `fill="both"` permite que o frame preencha a largura e altura disponíveis.
        # `expand=True` faz o frame crescer proporcionalmente se o layout for redimensionado.
        # `padx=10` adiciona espaçamento horizontal em ambos os lados do frame.
        # `pady=5` adiciona espaçamento vertical acima e abaixo do frame.
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        # Cria um LabelFrame dentro do `right_frame` para exibir o mapa de horários.
        # Um LabelFrame é um container com uma borda e um título, útil
        #       para agrupar elementos relacionados.
        mapa_frame = ttk.LabelFrame(
            right_frame,  # Define o `right_frame` como o pai do LabelFrame.
            text="Mapa de Horários",  # Define o título exibido no LabelFrame.
            padding=10  # Adiciona um preenchimento interno ao LabelFrame.
        )

        # Posiciona o `mapa_frame` dentro do `right_frame`.
        # `fill="x"` faz com que o LabelFrame preencha a largura disponível no layout.
        # `padx=10` adiciona espaçamento horizontal em ambos os lados do LabelFrame.
        # `pady=5` adiciona espaçamento vertical acima e abaixo do LabelFrame.
        mapa_frame.pack(fill="x", padx=10, pady=5)

        # Cria uma lista para armazenar os botões dos horários.
        # Esses botões serão criados dinamicamente e associados a
        #       horários específicos.
        self.botoes_horarios = []

        # Inicializa uma lista vazia para armazenar os horários
        #       formatados (como "08:00", "08:30", etc.).
        horarios = []

        # Define a hora inicial para a geração dos horários.
        hora = 8

        # Define o minuto inicial para a geração dos horários.
        minuto = 0

        # Loop para gerar os horários enquanto a hora for menor que 22
        # ou quando for exatamente 22:00 (limite superior dos horários).
        while hora < 22 or (hora == 22 and minuto == 0):

            # Formata a hora e o minuto no formato "HH:MM" e adiciona à lista de horários.
            # `{hora:02d}` garante que a hora tenha dois dígitos (ex.: 08 em vez de 8).
            # `{minuto:02d}` garante que o minuto tenha dois dígitos (ex.: 00 em vez de 0).
            horarios.append(f"{hora:02d}:{minuto:02d}")

            # Incrementa os minutos em 30 para gerar o próximo intervalo de horário.
            minuto += 30

            # Se os minutos ultrapassarem 59 (ex.: 08:60),
            #       ajusta para a próxima hora.
            if minuto >= 60:

                # Reseta os minutos para 0.
                minuto = 0

                # Incrementa a hora para o próximo horário.
                hora += 1

        # Loop que itera sobre os índices (i) e os horários (h) da lista `horarios`.
        for i, h in enumerate(horarios):

            # Define uma função `make_callback` que cria uma função de
            #       callback personalizada.
            # Essa função é necessária para capturar o horário
            #       associado ao botão atual.
            def make_callback(hora_str):

                # Retorna uma função lambda que chama o método `self.click_horario`
                # com o horário correspondente (`hora_str`) como argumento.
                return lambda: self.click_horario(hora_str)

            # Cria um botão para o horário atual (`h`) dentro do `mapa_frame`.
            # Define o texto do botão como o horário (`h`) no formato "HH:MM".
            # Define a largura do botão como 10.
            # Define a cor de fundo (`bg`) do botão como um cinza claro (`#d9d9d9`).
            # Define o comando do botão como o callback gerado pela função `make_callback(h)`.
            btn = tk.Button(mapa_frame,
                            text=h,
                            width=10,
                            bg="#d9d9d9",
                            command=make_callback(h))

            # Posiciona o botão na grade do `mapa_frame` com base em sua posição (`i`).
            # A linha (`row`) é calculada como `i // 5` (divide o índice
            #       por 5 para agrupar 5 botões por linha).
            # A coluna (`column`) é calculada como `i % 5` (resto da
            #       divisão para alternar entre as 5 colunas).
            # Adiciona espaçamento horizontal (`padx=2`) e vertical (`pady=2`) entre os botões.
            btn.grid(row=i // 5,
                     column=i % 5,
                     padx=2,
                     pady=2)

            # Adiciona uma tupla com o horário (`h`) e o botão (`btn`) à
            #       lista `self.botoes_horarios`.
            # Isso permite acessar e manipular os botões posteriormente, se necessário.
            self.botoes_horarios.append((h, btn))

        # Lista de agendamentos do dia
        # Cria um LabelFrame chamado `list_frame` dentro do `right_frame`.
        # O LabelFrame é usado para agrupar visualmente os widgets relacionados,
        #       com um rótulo na borda superior.
        # O texto exibido no LabelFrame é "Agendamentos do Dia".
        # O padding interno do frame é definido como 10 pixels
        #       para espaçamento interno.
        list_frame = ttk.LabelFrame(right_frame,
                                    text="Agendamentos do Dia",
                                    padding=10)

        # Posiciona o `list_frame` dentro do `right_frame` utilizando o método `pack`.
        # O `fill="both"` faz com que o `list_frame` preencha toda a
        #       largura e altura disponíveis.
        # O `expand=True` permite que o frame cresça proporcionalmente
        #       caso a janela seja redimensionada.
        # Adiciona espaçamento externo horizontal (`padx=10`) e
        #       vertical (`pady=5`) ao redor do frame.
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Cria uma Treeview chamada `self.tree` dentro do `list_frame`.
        # A Treeview é usada para exibir dados em formato tabular (semelhante a uma tabela).
        # Define as colunas como ("inicio", "fim", "cliente", "status").
        # O argumento `show="headings"` indica que apenas os cabeçalhos das
        #       colunas serão exibidos, sem uma coluna de ícones na lateral.
        self.tree = ttk.Treeview(list_frame,
                                 columns=("inicio", "fim", "cliente", "status"),
                                 show="headings")

        # Configura o cabeçalho da coluna "inicio".
        # Define o texto exibido no cabeçalho como "Hora Início".
        self.tree.heading("inicio", text="Hora Início")

        # Configura o cabeçalho da coluna "fim".
        # Define o texto exibido no cabeçalho como "Hora Fim".
        self.tree.heading("fim", text="Hora Fim")

        # Configura o cabeçalho da coluna "cliente".
        # Define o texto exibido no cabeçalho como "Cliente".
        self.tree.heading("cliente", text="Cliente")

        # Configura o cabeçalho da coluna "status".
        # Define o texto exibido no cabeçalho como "Status".
        self.tree.heading("status", text="Status")

        # Cria uma barra de rolagem vertical para a Treeview (`self.tree`).
        # A barra de rolagem será posicionada à direita do `list_frame`.
        # O argumento `orient="vertical"` define a orientação como vertical.
        # O parâmetro `command=self.tree.yview` conecta a barra de
        #       rolagem ao movimento vertical da Treeview.
        scrollbar = ttk.Scrollbar(list_frame,
                                  orient="vertical",
                                  command=self.tree.yview)

        # Configura a Treeview para usar a barra de rolagem.
        # O método `configure` ajusta a propriedade `yscroll` para
        #       conectar a barra de rolagem à Treeview.
        self.tree.configure(yscroll=scrollbar.set)

        # Posiciona a Treeview dentro do `list_frame`.
        # `side="left"` alinha a Treeview ao lado esquerdo do frame.
        # `fill="both"` faz com que a Treeview preencha tanto a
        #       largura quanto a altura disponíveis.
        # `expand=True` permite que a Treeview se expanda
        #       proporcionalmente ao redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem dentro do `list_frame`.
        # `side="right"` alinha a barra de rolagem ao lado direito do frame.
        # `fill="y"` faz com que a barra de rolagem preencha toda a altura disponível.
        scrollbar.pack(side="right", fill="y")

        # Inicializa a lista que armazenará os itens selecionados no agendamento.
        # Essa lista será usada para gerenciar e acessar os
        #       agendamentos que o usuário selecionar.
        self.itens_selecionados = []

        # Chama o método `carregar_agendamentos` para carregar os
        #       agendamentos atuais.
        # Isso garante que os agendamentos sejam exibidos assim
        #       que a interface é inicializada.
        self.carregar_agendamentos()

        # Associa o evento de seleção do calendário ao método `carregar_agendamentos`.
        # Quando o usuário seleciona uma nova data no calendário, o
        #       evento `<<CalendarSelected>>` é disparado.
        # Esse evento chama o método para atualizar os agendamentos
        #       exibidos de acordo com a nova data.
        self.calendario.bind("<<CalendarSelected>>", self.carregar_agendamentos)

        # Chama o método `atualizar_cores` para ajustar as cores
        #       dos botões de horários.
        # Esse método pode ser usado para indicar visualmente
        #       horários ocupados ou disponíveis.
        self.atualizar_cores()


    def atualizar_cores(self):

        # Obtém a data selecionada no calendário.
        data = self.calendario.get_date()

        # Busca todos os agendamentos do dia selecionado no banco de dados.
        agendamentos_dia = list(colecao_agendamentos.find({"data": data}))

        # Reseta as cores dos botões de horário.
        for (hora_str, btn) in self.botoes_horarios:

            # Configura a cor de fundo dos botões para o padrão cinza claro.
            btn.config(bg="#d9d9d9")

        # Atualizar cores
        # Itera sobre todos os agendamentos do dia selecionado.
        for ag in agendamentos_dia:

            # Converte o horário de início do agendamento para minutos.
            inicio_min = self.hora_em_minutos(ag.get("inicio", ""))

            # Converte o horário de fim do agendamento para minutos.
            fim_min = self.hora_em_minutos(ag.get("fim", ""))

            # Obtém o status do agendamento, padrão é "Pendente".
            status = ag.get("status", "Pendente")

            # Itera sobre todos os botões de horários disponíveis.
            for (hora_str, btn) in self.botoes_horarios:

                # Converte o horário do botão para minutos.
                hora_min = self.hora_em_minutos(hora_str)

                # Verifica se o horário do botão está dentro do
                #       intervalo do agendamento.
                if inicio_min <= hora_min <= fim_min:

                    # Se o agendamento estiver finalizado, define o botão como verde.
                    if status == "Finalizado":
                        btn.config(bg="#32CD32")  # Verde

                    # Caso contrário, define o botão como amarelo.
                    else:
                        btn.config(bg="#FFFF00")  # Amarelo



    # Define o método para tratar cliques nos horários
    #       exibidos no mapa de horários.
    def click_horario(self, hora_str):

        # Verifica se o campo de entrada de hora inicial está vazio.
        if not self.inicio_entry.get():

            # Insere o horário clicado no campo de hora inicial.
            self.inicio_entry.insert(0, hora_str)

        else:

            # Limpa o campo de hora final antes de inserir um novo horário.
            self.fim_entry.delete(0, "end")

            # Insere o horário clicado no campo de hora final.
            self.fim_entry.insert(0, hora_str)


    def deletar_agendamento(self):

        # Obtém o item selecionado na Treeview.
        # O método `selection` retorna uma lista com os IDs
        #       dos itens selecionados.
        selecionado = self.tree.selection()

        # Verifica se nenhum item foi selecionado na Treeview.
        # Caso a lista `selecionado` esteja vazia, exibe uma
        #       mensagem de erro ao usuário.
        if not selecionado:

            messagebox.showerror("Erro",
                                 "Nenhum agendamento selecionado.")

            # Interrompe a execução da função, pois não há item para deletar.
            return

        # Pega o primeiro item selecionado na Treeview.
        # Como é esperado que apenas um item seja selecionado,
        #       usa o índice 0 para acessar o ID.
        agendamento_id = selecionado[0]

        try:

            # Tenta deletar o agendamento selecionado no banco de dados MongoDB.
            # `delete_one` remove um único documento que atende ao critério especificado.
            # Aqui, o critério é `_id`, que deve ser igual ao `ObjectId` do `agendamento_id`.
            colecao_agendamentos.delete_one({"_id": ObjectId(agendamento_id)})

            # Atualiza a interface recarregando os agendamentos.
            # Isso garante que o agendamento deletado não seja
            #       mais exibido na Treeview.
            self.carregar_agendamentos()

            # Mostra uma mensagem de sucesso ao usuário informando
            #       que o agendamento foi deletado.
            messagebox.showinfo("Sucesso", "Agendamento deletado.")

        except Exception as e:

            # Captura qualquer erro que ocorra durante a operação de
            #       exclusão ou atualização.
            # Isso inclui falhas de conexão com o banco de dados ou
            #       problemas internos no MongoDB.
            # Exibe uma mensagem de erro ao usuário com detalhes
            #       sobre o problema.
            messagebox.showerror("Erro",
                                 f"Erro ao deletar o agendamento: {e}")


    def finalizar_servico(self):

        # Tenta obter o ID do agendamento selecionado na Treeview.
        try:
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Caso nenhum agendamento esteja selecionado, exibe
            #       uma mensagem de erro ao usuário.
            messagebox.showerror("Erro",
                                 "Nenhum agendamento selecionado.")
            return

        # Obtém o ID do agendamento selecionado.
        agendamento_id = selecionado

        # Busca o agendamento no banco de dados pelo seu ID.
        agendamento = colecao_agendamentos.find_one({"_id": ObjectId(agendamento_id)})
        if not agendamento:

            # Se o agendamento não for encontrado, exibe uma
            #       mensagem de erro ao usuário.
            messagebox.showerror("Erro",
                                 "Agendamento não encontrado.")
            return

        # Abre a janela para finalizar o serviço, passando o agendamento selecionado
        #       e o método para atualizar as cores da interface.
        janela_final = TelaFinalizarServico(self, agendamento, self.atualizar_cores)

        # Define a janela de finalização como modal, impedindo
        #       interações com a janela principal
        #       enquanto a janela de finalização está aberta.
        janela_final.grab_set()


    # Método responsável por agendar um serviço no sistema.
    def agendar(self):

        # Obtém a data selecionada no calendário.
        # `get_date()` retorna a data no formato definido na
        #       inicialização do calendário.
        data = self.calendario.get_date()

        # Obtém o horário de início preenchido pelo
        #       usuário no campo de entrada.
        # `get()` retorna o texto inserido no campo.
        # `strip()` remove espaços em branco extras.
        inicio = self.inicio_entry.get().strip()

        # Obtém o horário de fim preenchido pelo usuário no campo de entrada.
        # Assim como `inicio`, `strip()` garante que o valor seja
        #       processado sem espaços extras.
        fim = self.fim_entry.get().strip()

        # Obtém o nome do cliente selecionado no campo de combinação (ComboBox).
        # `get()` retorna o valor atualmente selecionado na ComboBox.
        cliente = self.cliente_combo.get().strip()

        # Verifica se todos os campos obrigatórios foram preenchidos.
        # Os campos obrigatórios são: data, horário de início,
        #       horário de fim e cliente.
        if not data or not inicio or not fim or not cliente:

            # Exibe uma mensagem de erro em uma janela pop-up.
            # `messagebox.showerror` é uma função do Tkinter que
            #       exibe mensagens de erro.
            # O título da mensagem é "Erro", e o conteúdo explica que campos
            #       obrigatórios estão ausentes.
            messagebox.showerror(
                "Erro",  # Título da mensagem de erro.
                "Data, Hora Início, Hora Fim e Cliente são obrigatórios."  # Detalhe do erro.
            )

            # Finaliza a execução do método, pois os dados necessários
            #       não foram fornecidos.
            return

        # Verifica se há conflitos de horário para o agendamento.

        # Converte o horário de início fornecido para minutos a
        #       partir de meia-noite.
        # O método `hora_em_minutos` transforma um horário no
        #       formato "HH:MM" em um valor numérico (minutos).
        inicio_min = self.hora_em_minutos(inicio)

        # Converte o horário de fim fornecido para minutos a partir de meia-noite.
        # Isso permite comparar intervalos de tempo de maneira mais simples.
        fim_min = self.hora_em_minutos(fim)

        # Recupera todos os agendamentos já existentes no dia selecionado.
        # A função `colecao_agendamentos.find` busca no banco de
        #       dados todos os agendamentos
        #       que possuem a mesma data que a selecionada no calendário.
        # O resultado é convertido em uma lista para facilitar a manipulação.
        agendamentos_dia = list(colecao_agendamentos.find({"data": data}))

        # Percorre cada agendamento existente no dia selecionado
        #       para verificar conflitos de horário.
        for ag in agendamentos_dia:

            # Converte o horário de início do agendamento existente para minutos.
            # A função `ag.get("inicio", "")` recupera o horário de início do agendamento,
            #       retornando uma string no formato "HH:MM". Caso o horário não
            #       exista, retorna uma string vazia.
            ag_inicio_min = self.hora_em_minutos(ag.get("inicio", ""))

            # Converte o horário de fim do agendamento existente para minutos.
            # A função `ag.get("fim", "")` recupera o horário de término do agendamento.
            ag_fim_min = self.hora_em_minutos(ag.get("fim", ""))

            # Verifica se há sobreposição de horários.
            # A condição `not (fim_min <= ag_inicio_min or inicio_min >= ag_fim_min)` significa:
            # - `fim_min <= ag_inicio_min`: O novo horário termina antes do
            #       início do agendamento existente.
            # - `inicio_min >= ag_fim_min`: O novo horário começa depois do
            #       término do agendamento existente.
            # Se nenhuma dessas condições for verdadeira, há sobreposição de horários.
            if not (fim_min <= ag_inicio_min or inicio_min >= ag_fim_min):

                # Exibe uma mensagem de erro informando que há um conflito de horários.
                # A função `messagebox.showerror` cria uma janela modal com
                #       uma mensagem de erro para o usuário.
                messagebox.showerror("Erro",
                                     "Conflito de horário com outro agendamento.")

                # Encerra o método sem concluir o agendamento,
                #       retornando ao fluxo principal.
                return

        # Cria um dicionário chamado `novo` que representa o agendamento
        #       que será adicionado ao banco de dados.
        novo = {

            # Armazena a data selecionada no calendário como uma
            #       string no formato "dd/MM/yyyy".
            "data": data,

            # Armazena o horário de início do agendamento, obtido do
            #       campo de entrada correspondente.
            "inicio": inicio,

            # Armazena o horário de término do agendamento, obtido do
            #       campo de entrada correspondente.
            "fim": fim,

            # Armazena o nome do cliente associado ao agendamento,
            #       selecionado na combobox de clientes.
            "cliente": cliente,

            # Armazena os itens selecionados para o agendamento.
            # `self.itens_selecionados` é uma lista de tuplas onde cada
            #       tupla contém informações sobre um item.
            # Por exemplo, pode incluir: o ID do item, o nome, o preço e
            #       o tipo (serviço ou produto).
            "itens": self.itens_selecionados,

            # Define o status inicial do agendamento como "Pendente".
            # Isso indica que o serviço ainda não foi realizado ou finalizado.
            "status": "Pendente"

        }

        # Insere o dicionário `novo` (contendo os detalhes do agendamento) na
        #       coleção `colecao_agendamentos` do MongoDB.
        # O método `insert_one` adiciona um único documento ao banco de dados.
        colecao_agendamentos.insert_one(novo)

        # Atualiza a interface carregando novamente todos os
        #       agendamentos para refletir o novo registro.
        # Isso é necessário para que a Treeview (ou qualquer outro
        #       componente) exiba o novo agendamento adicionado.
        self.carregar_agendamentos()

        # Limpa os campos de entrada na tela de agendamentos.
        # Garante que os campos de data, hora, cliente e outros sejam
        #       limpos após o agendamento ser salvo.
        self.limpar_campos()

        # Exibe uma mensagem de sucesso ao usuário indicando que o
        #       agendamento foi criado com sucesso.
        # Isso serve como feedback visual para informar que a
        #       operação foi concluída sem erros.
        messagebox.showinfo("Sucesso", "Agendamento criado.")


    def hora_em_minutos(self, hora_str):

        # Tenta dividir a string `hora_str` no
        #       formato "hh:mm" em horas e minutos.
        try:

            # Usa `split(":")` para separar horas (`h`) e minutos (`m`) na string.
            # Converte os valores separados para inteiros.
            h, m = map(int, hora_str.split(":"))

            # Calcula o total de minutos desde a meia-noite: (horas * 60) + minutos.
            return h * 60 + m

        # Captura erros no caso de formato inválido ou string vazia.
        except ValueError:

            # Retorna 0 como padrão para tratar casos
            #       onde `hora_str` não é válida.
            return 0


    def carregar_agendamentos(self, event=None):

        # Obtém a data selecionada no calendário.
        # A data será usada como filtro para carregar os agendamentos
        #       correspondentes no banco de dados.
        data = self.calendario.get_date()

        # Limpa a Treeview antes de carregar os agendamentos do dia.
        # `self.tree.get_children()` retorna todos os itens atualmente na Treeview.
        # Para cada item retornado, `self.tree.delete(item)` remove o item da Treeview.
        # Isso garante que a Treeview seja atualizada corretamente sem duplicações.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Itera sobre os agendamentos encontrados no banco de
        #       dados para a data selecionada.
        for ag in colecao_agendamentos.find({"data": data}).sort("inicio", pymongo.ASCENDING):

            # Obtém o status do agendamento. Caso o status não
            #       exista, define como "Pendente".
            status = ag.get("status", "Pendente")

            # Insere um novo item na Treeview com as informações do agendamento.
            # `""` indica que o item será inserido na raiz (sem hierarquia).
            # `"end"` posiciona o item no final da lista atual da Treeview.
            # `iid=str(ag["_id"])` usa o ID do documento como identificador único para o item.
            # `values` define as colunas visíveis: hora de início,
            #       hora de fim, cliente e status.
            self.tree.insert(
                "",
                "end",
                iid=str(ag["_id"]),
                values=(ag.get("inicio", ""),
                        ag.get("fim", ""),
                        ag.get("cliente", ""),
                        status)
            )

        # Atualiza as cores da Treeview, caso necessário.
        # A função `self.atualizar_cores` pode, por exemplo, alterar a
        #       cor dos itens com base no status.
        self.atualizar_cores()


    def limpar_campos(self):

        # Limpa o campo de entrada de texto para a hora de início,
        #       removendo qualquer valor digitado.
        self.inicio_entry.delete(0, "end")

        # Limpa o campo de entrada de texto para a hora de fim,
        #       removendo qualquer valor digitado.
        self.fim_entry.delete(0, "end")

        # Reseta a seleção no combobox de cliente, deixando-o vazio.
        self.cliente_combo.set("")

        # Reseta a lista de itens selecionados para um estado vazio.
        self.itens_selecionados = []



    # Método responsável por abrir uma nova janela
    #       para selecionar serviços.
    def abrir_tela_selecao(self):

        # Callback para processar os itens selecionados na tela de seleção.
        # `itens_selecionados` é uma lista de serviços escolhidos
        #       pelo usuário na nova janela.
        def callback_selecao(itens_selecionados):

            # Atualiza a variável `itens_selecionados` com os
            #       serviços escolhidos.
            self.itens_selecionados = itens_selecionados

            # Exibe no console os itens selecionados para depuração.
            print("Itens selecionados:", itens_selecionados)

        # Cria uma nova janela secundária (janela filha) a partir
        #       da janela principal.
        nova_janela = tk.Toplevel(self)

        # Instancia a tela de seleção de serviços dentro da nova janela.
        # Passa `callback_selecao` como argumento para que a seleção
        #       feita na nova janela seja processada aqui.
        TelaSelecaoServicos(nova_janela, callback_selecao)


    # Retorna uma lista contendo os nomes dos clientes
    #       cadastrados no banco de dados.
    # Usa uma expressão de lista (list comprehension) para percorrer os
    #       documentos encontrados na coleção `colecao_clientes`.
    def listar_clientes(self):

        # A função `colecao_clientes.find()` retorna todos os
        #       documentos da coleção de clientes.
        # O método `sort("nome", pymongo.ASCENDING)` ordena os documentos
        #       pelo campo "nome" em ordem alfabética ascendente.
        # `c.get("nome", "")` extrai o campo "nome" de cada documento; se o
        #       campo "nome" não existir, retorna uma string vazia.
        return [c.get("nome", "") for c in colecao_clientes.find().sort("nome", pymongo.ASCENDING)]


# ------------------------------------------------------------
# Janela para Finalizar/Editar Agendamento
# ------------------------------------------------------------
class TelaFinalizarServico(tk.Toplevel):

    # Método construtor da classe `TelaFinalizarServico`, chamado
    #       automaticamente ao criar uma nova instância dessa janela.
    def __init__(self, parent, agendamento, callback_atualizar_cores):

        # Chama o construtor da classe pai (`tk.Toplevel`) para inicializar a
        #       janela de forma apropriada.
        # Isso é essencial para herdar todas as funcionalidades do
        #       widget `tk.Toplevel`, como criação e gerenciamento de janelas.
        super().__init__(parent)

        # `self` refere-se à instância atual dessa classe, permitindo
        #       acesso a atributos e métodos internos.
        # É usado para definir e acessar propriedades
        #       exclusivas desta janela.

        # `parent` é a janela pai (normalmente a janela principal do
        #       sistema) que abriu esta janela.
        # Ele é necessário para estabelecer hierarquia e pode ser
        #       usado para referenciar a janela pai.

        # Define o título exibido na barra superior da janela.
        self.title("Finalizar Serviço")

        # Configura o tamanho inicial da janela para 700 pixels de
        #       largura por 550 pixels de altura.
        self.geometry("700x550")

        # Define a cor de fundo da janela como um tom claro de cinza (#f5f5f5).
        # Isso ajuda a criar um visual agradável e consistente
        #       com o design do sistema.
        self.configure(bg="#f5f5f5")

        # `agendamento` é um dicionário contendo os detalhes do
        #       agendamento selecionado.
        # Este atributo é armazenado para que possa ser usado em outras
        #       partes desta janela, como ao exibir informações do agendamento.
        self.agendamento = agendamento

        # `callback_atualizar_cores` é uma função passada pela janela pai.
        # Ela será chamada para atualizar a interface (como os horários)
        #       após o serviço ser finalizado.
        self.callback_atualizar_cores = callback_atualizar_cores

        # Centralizar a janela
        # Atualiza as tarefas pendentes do loop de eventos do Tkinter.
        # Isso é necessário para garantir que a janela tenha sido criada
        #       corretamente antes de calcular as dimensões.
        self.update_idletasks()

        # Define a largura fixa da janela como 700 pixels.
        largura_janela = 700

        # Define a altura fixa da janela como 550 pixels.
        altura_janela = 550

        # Obtém a largura total da tela do monitor do usuário.
        largura_tela = self.winfo_screenwidth()

        # Obtém a altura total da tela do monitor do usuário.
        altura_tela = self.winfo_screenheight()

        # Calcula a posição horizontal para centralizar a janela na tela.
        # Subtrai a largura da janela da largura total da tela e divide por 2.
        pos_x = (largura_tela - largura_janela) // 2

        # Calcula a posição vertical para centralizar a janela na tela.
        # Subtrai a altura da janela da altura total da tela e divide por 2.
        pos_y = (altura_tela - altura_janela) // 2

        # Define as dimensões e a posição da janela usando o formato
        #       largura x altura + pos_x + pos_y.
        # Isso posiciona a janela no centro da tela.
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Guardamos quem é o "parent" (TelaAgendamentos)
        # Armazena a referência do widget pai (janela que chamou essa janela).
        # Isso permite que a janela de finalização de serviço se
        #       comunique com a janela principal.
        self.parent = parent

        # Armazena os dados do agendamento recebido como argumento.
        # Isso inclui informações como cliente, horário, serviços, etc.
        self.agendamento = agendamento

        # Extrai e armazena o ID único do agendamento para facilitar
        #       consultas e atualizações no banco de dados.
        self.agendamento_id = agendamento["_id"]

        # Armazena a função de callback fornecida como argumento, que será
        #       usada para atualizar as cores dos botões
        #       na janela principal após finalizar ou modificar o agendamento.
        self.callback_atualizar_cores = callback_atualizar_cores

        # Obtém a lista de itens associados ao agendamento.
        # Essa lista geralmente contém os serviços selecionados no agendamento.
        # Se não houver itens, retorna uma lista vazia como valor padrão.
        self.itens = agendamento.get("itens", [])

        # Cria um rótulo para exibir o título da janela.
        # O texto "Finalização do Agendamento" é exibido em fonte Arial,
        #       tamanho 16, e em negrito.
        # O fundo do rótulo é configurado para combinar com o fundo da
        #       janela ("#f5f5f5").
        tk.Label(
            self,
            text="Finalização do Agendamento",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5"

        # Adiciona um espaçamento vertical (10 pixels) acima e abaixo do rótulo.
        ).pack(pady=10)

        # Cria um frame que servirá para organizar as informações
        #       do agendamento na janela.
        # O frame usa o mesmo fundo da janela principal ("#f5f5f5").
        info_frame = tk.Frame(self, bg="#f5f5f5")

        # Posiciona o `info_frame` no layout da janela.
        # `anchor="w"` alinha o frame ao lado esquerdo (west).
        # `padx=20` adiciona um espaçamento horizontal de 20 pixels nas bordas do frame.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels nas bordas do frame.
        # `fill="x"` faz o frame se expandir horizontalmente para
        #       preencher toda a largura disponível.
        info_frame.pack(anchor="w", padx=20, pady=5, fill="x")

        # Cria um rótulo dentro do `info_frame` para exibir o nome do
        #       cliente associado ao agendamento.
        # O texto é formatado como "Cliente: [nome do cliente]", onde o
        #       nome é obtido do dicionário `agendamento`.
        tk.Label(
            info_frame,

            # Define o texto a ser exibido, com o nome do cliente
            #       extraído do agendamento.
            text=f"Cliente: {agendamento.get('cliente', '')}",

            # Configura a fonte do texto para Arial, tamanho 12, e estilo negrito.
            font=("Arial", 12, "bold"),

            # Define o fundo do rótulo como a mesma cor do
            #       fundo da janela ("#f5f5f5").
            bg="#f5f5f5"

        ).pack(

            # Posiciona o rótulo alinhado ao lado esquerdo
            #       dentro do `info_frame` (west).
            anchor="w",

            # Adiciona um espaçamento vertical de 2 pixels entre este
            #       rótulo e outros elementos.
            pady=2)

        # Cria um rótulo dentro do `info_frame` para exibir o horário do agendamento.
        # O texto é formatado como "Horário: [hora início] - [hora fim]".
        tk.Label(
            info_frame,

            # Define o texto a ser exibido, que contém os horários de
            #       início e fim do agendamento.
            text=f"Horário: {agendamento.get('inicio', '')} - {agendamento.get('fim', '')}",

            # Configura a fonte do texto para Arial, tamanho 12, e estilo negrito.
            font=("Arial", 12, "bold"),

            # Define o fundo do rótulo como a mesma cor do
            #       fundo da janela ("#f5f5f5").
            bg="#f5f5f5"

        ).pack(

            # Posiciona o rótulo alinhado ao lado esquerdo dentro
            #       do `info_frame` (west).
            anchor="w",

            # Adiciona um espaçamento vertical de 2 pixels entre
            #       este rótulo e outros elementos.
            pady=2)

        # Selecionar o Funcionário que atendeu
        # Cria um frame chamado `func_frame` que serve como um contêiner
        #       para os elementos relacionados ao funcionário.
        func_frame = tk.Frame(

            # Referência ao frame pai, que é a janela atual.
            self,

            # Define a cor de fundo do frame como cinza claro (#f5f5f5) para
            #       combinar com o restante da janela.
            bg="#f5f5f5"

        )

        # Posiciona o frame dentro da janela atual.
        func_frame.pack(
            anchor="w",  # Alinha o frame ao lado esquerdo (west) da janela.
            padx=20,  # Adiciona 20 pixels de espaçamento horizontal ao redor do frame.
            pady=5,  # Adiciona 5 pixels de espaçamento vertical ao redor do frame.
            fill="x"  # Faz o frame preencher toda a largura disponível da janela.
        )

        # Adiciona um rótulo (`Label`) ao frame `func_frame` para
        #       indicar o campo "Funcionário que atendeu".
        tk.Label(
            func_frame,  # Define que o rótulo pertence ao frame `func_frame`.
            text="Funcionário que atendeu:",  # Texto que será exibido no rótulo.
            bg="#f5f5f5",  # Define a cor de fundo do rótulo para combinar com o frame.
            font=("Arial", 12, "bold")  # Define a fonte do texto como Arial, tamanho 12, e estilo negrito (bold).
        ).pack(
            side="left"  # Alinha o rótulo ao lado esquerdo do frame `func_frame`.
        )

        # Adiciona uma combobox (`Combobox`) ao `func_frame` para seleção do funcionário.
        # O elemento será utilizado para escolher o funcionário responsável pelo atendimento.
        # `func_frame` é o frame pai onde a combobox será posicionada.
        # `values=self.listar_funcionarios()` define os valores exibidos na combobox,
        #     que são obtidos através do método `listar_funcionarios`,
        #     retornando a lista de funcionários cadastrados.
        # `width=30` define a largura da combobox, configurando-a para exibir até 30 caracteres.
        self.funcionario_combo = ttk.Combobox(func_frame,
                                              values=self.listar_funcionarios(),
                                              width=30)

        # Posiciona a combobox no frame `func_frame`.
        # `side="left"` alinha a combobox ao lado esquerdo do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor da combobox.
        self.funcionario_combo.pack(side="left", padx=5)

        # Frame para Treeview
        # Cria um frame (`Frame`) dentro da janela atual (`self`) para conter a `Treeview`.
        # O frame será utilizado para organizar visualmente a tabela e seu conteúdo.
        # `bg="#f5f5f5"` define a cor de fundo do frame como um tom claro de cinza.
        tree_frame = tk.Frame(self, bg="#f5f5f5")

        # Posiciona o frame `tree_frame` dentro da janela atual.
        # `fill="both"` faz com que o frame ocupe todo o espaço
        #       disponível em largura e altura.
        # `expand=True` permite que o frame se expanda ao redimensionar a janela.
        # `padx=20` adiciona um espaçamento horizontal de 20 pixels ao redor do frame.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Define as colunas que serão exibidas na `Treeview`.
        # "nome", "preco" e "tipo" representam os nomes internos das colunas.
        colunas = ("nome", "preco", "tipo")

        # Cria a `Treeview` dentro do frame `tree_frame`.
        # A `Treeview` é uma tabela interativa usada para exibir dados.
        # `columns=colunas` define as colunas que a tabela irá conter.
        # `show="headings"` faz com que apenas os cabeçalhos das colunas
        #       sejam exibidos, sem uma coluna extra para o índice.
        self.tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")

        # Configura o cabeçalho da coluna "nome".
        # Define o texto exibido no cabeçalho como "Serviço/Produto".
        self.tree.heading("nome", text="Serviço/Produto")

        # Configura o cabeçalho da coluna "preco".
        # Define o texto exibido no cabeçalho como "Preço (R$)".
        self.tree.heading("preco", text="Preço (R$)")

        # Configura o cabeçalho da coluna "tipo".
        # Define o texto exibido no cabeçalho como "Tipo".
        self.tree.heading("tipo", text="Tipo")

        # Define a largura e alinhamento da coluna "nome".
        # `width=300` define que a largura da coluna será de 300 pixels.
        self.tree.column("nome", width=300)

        # Define a largura e alinhamento da coluna "preco".
        # `width=100` define que a largura da coluna será de 100 pixels.
        # `anchor="center"` alinha o texto dessa coluna ao centro.
        self.tree.column("preco", width=100, anchor="center")

        # Define a largura e alinhamento da coluna "tipo".
        # `width=100` define que a largura da coluna será de 100 pixels.
        # `anchor="center"` alinha o texto dessa coluna ao centro.
        self.tree.column("tipo", width=100, anchor="center")

        # Cria uma barra de rolagem vertical para a `Treeview`.
        # `orient="vertical"` especifica que a barra será vertical.
        # `command=self.tree.yview` conecta a barra de rolagem com a
        #       visão vertical da `Treeview`.
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)

        # Configura a `Treeview` para utilizar a barra de rolagem vertical.
        # A propriedade `yscroll` da `Treeview` é ajustada para que a
        #       barra funcione corretamente.
        self.tree.configure(yscroll=vsb.set)

        # Posiciona a `Treeview` dentro do `tree_frame`.
        # `side="left"` alinha a `Treeview` ao lado esquerdo do frame.
        # `fill="both"` faz com que a `Treeview` preencha toda a
        #       largura e altura disponíveis.
        # `expand=True` permite que a `Treeview` cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem vertical (`vsb`) dentro do `tree_frame`.
        # `side="right"` alinha a barra de rolagem ao lado direito do frame.
        # `fill="y"` faz com que a barra de rolagem preencha toda a altura disponível.
        vsb.pack(side="right", fill="y")

        # Carrega os itens na `Treeview`.
        # Este método será responsável por adicionar os dados à tabela.
        self.carregar_itens()

        # Cria um frame adicional para botões relacionados aos itens.
        # Este frame será usado para posicionar botões na interface.
        # `bg="#f5f5f5"` define a cor de fundo do frame como cinza claro.
        botoes_itens_frame = tk.Frame(self, bg="#f5f5f5")

        # Posiciona o frame de botões na interface.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       acima e abaixo do frame.
        botoes_itens_frame.pack(fill="x", pady=5)

        # Cria um botão no `botoes_itens_frame` com o texto "Adicionar Item".
        # `text="Adicionar Item"` define o texto exibido no botão.
        # `command=self.adicionar_item` associa o método `adicionar_item` ao clique do botão.
        ttk.Button(
            botoes_itens_frame,
            text="Adicionar Item",
            command=self.adicionar_item
        ).pack(

            # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
            side="left",

            # `padx=5` adiciona um espaçamento horizontal de 5
            #       pixels em volta do botão.
            padx=5)

        # Cria um botão no `botoes_itens_frame` com o texto "Remover Item".
        # `text="Remover Item"` define o texto exibido no botão.
        # `command=self.remover_item` associa o método `remover_item` ao clique do botão.
        ttk.Button(botoes_itens_frame,
                    text="Remover Item",
                    command=self.remover_item).pack(

                                                # `side="left"` posiciona o botão ao lado esquerdo dentro
                                                #       do frame, após o botão anterior.
                                                side="left",

                                                # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do botão.
                                                padx=5)

        # Adiciona um frame para botões de finalização chamado `botoes_final_frame`.
        # Este frame será usado para organizar os botões na parte inferior da janela.
        # `bg="#f5f5f5"` define a cor de fundo do frame como cinza claro.
        botoes_final_frame = tk.Frame(self, bg="#f5f5f5")

        # Posiciona o frame `botoes_final_frame` na interface.
        # `fill="x"` faz com que o frame preencha toda a largura disponível na janela.
        # `pady=10` adiciona 10 pixels de espaçamento vertical acima e abaixo do frame.
        # `padx=20` adiciona 20 pixels de espaçamento horizontal à
        #       esquerda e à direita do frame.
        botoes_final_frame.pack(fill="x", pady=10, padx=20)

        # Cria um botão no frame `botoes_final_frame` com o texto "Finalizar Serviço".
        # O botão é usado para finalizar o serviço associado ao agendamento atual.
        ttk.Button(botoes_final_frame,
                                text="Finalizar Serviço",  # Texto exibido no botão.
                                command=self.confirmar_finalizacao  # Função chamada ao clicar no botão.
                                ).pack(side="left",  # Posiciona o botão no lado esquerdo do frame.
                                       padx=5)  # Adiciona 5 pixels de espaçamento horizontal em ambos os lados do botão.


        # Cria um botão no frame `botoes_final_frame` com o texto "Cancelar".
        # O botão é usado para fechar a janela de finalização do
        #       serviço sem realizar nenhuma ação.
        ttk.Button(botoes_final_frame,
                    text="Cancelar",  # Texto exibido no botão.
                    command=self.destroy  # Função chamada ao clicar no botão para fechar a janela.
                    ).pack(
                        side="right",  # Posiciona o botão no lado direito do frame.
                        padx=5)  # Adiciona 5 pixels de espaçamento horizontal em ambos os lados do botão.



    def confirmar_finalizacao(self):

        # Verifica se um funcionário foi selecionado no combo box `funcionario_combo`.
        # Armazena o nome do funcionário selecionado na variável `funcionario_nome`.
        funcionario_nome = self.funcionario_combo.get().strip()

        # Caso nenhum funcionário tenha sido selecionado (campo vazio),
        # exibe uma mensagem de erro para o usuário e encerra o processo.
        if not funcionario_nome:
            messagebox.showerror("Erro",
                                 "Selecione o funcionário responsável.")
            return

        # 1.1) Buscar a comissão do funcionário no banco de
        #       dados na coleção `colecao_funcionarios`.
        # Busca o documento do funcionário com base no
        #       nome selecionado no combo box.
        funcionario_doc = colecao_funcionarios.find_one({"nome": funcionario_nome})

        # Verifica se o documento do funcionário foi encontrado.
        if funcionario_doc:

            # Obtém o valor da comissão do funcionário (em percentual) do
            #       documento encontrado.
            # Caso o campo "comissao" não exista ou seja inválido,
            #       assume o valor padrão de 10%.
            comissao_percentual = float(funcionario_doc.get("comissao", 10.0))

        else:

            # Caso o funcionário não seja encontrado no banco de dados,
            #       assume um valor padrão de 10% de comissão.
            comissao_percentual = 10.0

        # 2) Calcular o valor total dos itens incluídos no agendamento.
        valor_total = 0.0  # Inicializa o valor total com zero.

        # Percorre a lista de itens selecionados no agendamento.
        for (item_id, nome, preco, tipo) in self.itens:

            try:

                # Tenta converter o preço do item para um valor numérico (float).
                valor_total += float(preco)

            except ValueError:

                # Caso o preço não seja válido, ignora e continua o cálculo.
                pass

            # Verifica se o item é do tipo "produto", para atualizar o estoque.
            if tipo == "produto":

                try:

                    # Chama o método `atualizar_estoque` para abater o produto do estoque.
                    self.atualizar_estoque(item_id, tipo, abater=True)

                except Exception as e:

                    # Em caso de erro ao atualizar o estoque, exibe uma
                    #       mensagem de erro e interrompe o processo.
                    messagebox.showerror(
                        "Erro no Estoque",
                        f"Erro ao atualizar estoque para '{nome}': {e}"
                    )
                    return

        # 3) Calcular a comissão real do funcionário (ex.: 15% => 0.15)
        comissao_funcionario = round(valor_total * (comissao_percentual / 100.0), 2)

        # 4) Atualizar o status do agendamento no banco de dados para 'Finalizado'.
        try:

            colecao_agendamentos.update_one(

                # Filtro para encontrar o agendamento pelo ID.
                {"_id": ObjectId(self.agendamento_id)},
                {
                    "$set": {  # Atualizações a serem realizadas.
                        "status": "Finalizado",  # Define o status como 'Finalizado'.
                        "itens": self.itens,  # Atualiza os itens do agendamento.
                        "funcionario_nome": funcionario_nome,  # Adiciona o nome do funcionário responsável.
                        "valor_total": valor_total,  # Registra o valor total calculado.
                        "comissao_funcionario": comissao_funcionario  # Calcula e salva a comissão do funcionário.
                    }
                }
            )

            # Após atualizar o banco de dados, salva o relatório financeiro.
            # Isso inclui a comissão do funcionário e o valor total da venda.
            self.salvar_relatorio(funcionario_nome, valor_total, comissao_funcionario)

        except Exception as e:

            # Caso ocorra algum erro ao atualizar o banco, exibe
            #       uma mensagem de erro detalhada.
            messagebox.showerror(
                "Erro",
                f"Falha ao atualizar no banco:\n{e}"
            )
            return

        # 5) Exibir mensagem de sucesso após a finalização do serviço.
        # A mensagem inclui o valor total do serviço e a comissão do funcionário.
        messagebox.showinfo(
            "Sucesso",  # Título da mensagem.
            f"Serviço finalizado!\n"  # Texto da mensagem.
            f"Valor total: R${valor_total:.2f}\n"  # Mostra o valor total com duas casas decimais.
            f"Comissão: R${comissao_funcionario:.2f}"  # Mostra a comissão calculada com duas casas decimais.
        )

        # 6) AGORA VAMOS ATUALIZAR A TELA DE AGENDAMENTOS

        # 6.1) Atualizar a TreeView (somente a linha correspondente ao
        #       agendamento finalizado)
        agendamento_id_str = str(self.agendamento_id)

        # Recupera o agendamento atual do banco de dados,
        #       utilizando o ID do agendamento.
        agendamento_atual = colecao_agendamentos.find_one({"_id": ObjectId(self.agendamento_id)})

        # Verifica se o agendamento foi encontrado no banco de dados.
        if agendamento_atual:

            # Obtém os dados do agendamento atual, com valores
            #       padrão caso não estejam disponíveis.
            inicio = agendamento_atual.get("inicio", "")  # Hora de início do agendamento.
            fim = agendamento_atual.get("fim", "")  # Hora de fim do agendamento.
            cliente = agendamento_atual.get("cliente", "")  # Nome do cliente associado ao agendamento.
            status = agendamento_atual.get("status", "Finalizado")  # Status atual do agendamento.

            # Atualiza a linha correspondente na TreeView para refletir o
            #       novo status e os dados do agendamento.
            self.parent.tree.item(
                agendamento_id_str,  # Identificador único da linha na TreeView.
                values=(inicio, fim, cliente, status)  # Novos valores a serem exibidos nas colunas da TreeView.
            )

        # 6.2) Atualizar cores dos botões do mapa de horários
        # Obtém a data do agendamento atual a partir do banco de dados.
        data_do_agendamento = agendamento_atual.get("data", "")

        # Percorre todos os botões de horários associados ao agendamento e
        #       redefine suas cores para o padrão.
        for (hora_str, btn) in self.parent.botoes_horarios:

            # `hora_str` é o horário associado ao botão.
            # `btn` é o próprio botão que será atualizado.
            # Define a cor de fundo do botão como o cinza padrão (#d9d9d9).
            btn.config(bg="#d9d9d9")

        # Pegar todos agendamentos do dia (salvos no BD)
        # Obtém todos os agendamentos do dia específico
        #       armazenados no banco de dados.
        agendamentos_dia = list(colecao_agendamentos.find({"data": data_do_agendamento}))

        # Itera por cada agendamento encontrado para atualizar as
        #       cores dos botões de horários.
        for ag in agendamentos_dia:

            # Obtém o status do agendamento, padrão sendo "Pendente".
            ag_status = ag.get("status", "Pendente")

            # Converte o horário de início do agendamento em minutos
            #       para facilitar a comparação.
            inicio_min = self.parent.hora_em_minutos(ag.get("inicio", ""))

            # Converte o horário de término do agendamento em minutos
            #       para facilitar a comparação.
            fim_min = self.parent.hora_em_minutos(ag.get("fim", ""))

            # Itera pelos botões de horários disponíveis no calendário da interface.
            for (hora_str, btn) in self.parent.botoes_horarios:

                # Converte o horário do botão em minutos para comparação
                #       com os horários dos agendamentos.
                hora_min = self.parent.hora_em_minutos(hora_str)

                # Verifica se o horário do botão está dentro do
                #       intervalo do agendamento.
                if inicio_min <= hora_min <= fim_min:

                    # Se o status do agendamento for "Finalizado", altera a
                    #       cor do botão para verde.
                    if ag_status == "Finalizado":
                        btn.config(bg="#32CD32")  # Verde representa finalizado.

                    # Caso contrário, altera a cor do botão para amarelo,
                    #       indicando agendamento pendente.
                    else:
                        btn.config(bg="#FFFF00")  # Amarelo representa pendente.

        # 7) Fecha a janela de finalização
        self.destroy()

    def salvar_relatorio(self, funcionario_nome, valor_total, comissao_funcionario):

        """
        Salva os dados de um agendamento finalizado no
                relatório do banco de dados.
        Verifica a comissão real do funcionário antes de salvar.
        """
        try:

            # Verifica se a coleção `colecao_agendamentos` está configurada.
            # Isso garante que o código não falhe devido à falta de inicialização.
            if 'colecao_agendamentos' not in globals():
                messagebox.showerror(
                    "Erro",
                    "A coleção 'colecao_agendamentos' não está configurada."
                )
                return

            # Verifica se a coleção `colecao_relatorios` está configurada.
            # Isso garante que o código não falhe caso o banco de dados
            #       ou a coleção esteja mal configurada.
            if 'colecao_relatorios' not in globals():
                messagebox.showerror(
                    "Erro",
                    "A coleção 'colecao_relatorios' não está configurada."
                )
                return

            # Verifica se a coleção `colecao_produtos` está configurada.
            # Essa verificação é necessária para evitar erros caso o
            #       banco de dados esteja incompleto.
            if 'colecao_produtos' not in globals():
                messagebox.showerror(
                    "Erro",
                    "A coleção 'colecao_produtos' não está configurada."
                )
                return

            # Verifica se a coleção `colecao_funcionarios` está configurada.
            # Essa verificação garante que o acesso ao banco de dados dos
            #       funcionários funcione corretamente.
            if 'colecao_funcionarios' not in globals():
                messagebox.showerror(
                    "Erro",
                    "A coleção 'colecao_funcionarios' não está configurada."
                )
                return

            # Busca o documento do funcionário na coleção `colecao_funcionarios`
            #       pelo nome do funcionário.
            funcionario_doc = colecao_funcionarios.find_one({"nome": funcionario_nome})

            if funcionario_doc:

                # Caso o documento do funcionário seja encontrado, tenta
                #       obter o valor da comissão.
                # Se o campo `comissao` não existir, assume 10% como valor padrão.
                porcentagem_comissao = float(funcionario_doc.get("comissao", 10))

            else:

                # Se o funcionário não for encontrado no banco de dados,
                #       assume 10% como valor padrão.
                porcentagem_comissao = 10.0

            # Itera pelos itens associados ao agendamento, como
            #       produtos ou serviços.
            for item in self.itens:

                # Verifica se o item é uma lista e contém pelo menos 3
                #       elementos (ex: ID, nome, preço).
                if isinstance(item, list) and len(item) >= 3:

                    # Obtém o nome do produto ou serviço a partir do
                    #       segundo elemento da lista.
                    produto_servico_nome = item[1]

                    try:

                        # Tenta converter o preço ou valor do serviço para um número decimal.
                        # Isso garante que valores inválidos (como strings) não causem falhas.
                        valor_item = float(item[2])

                    except ValueError:

                        # Caso ocorra um erro ao converter o preço,
                        #       atribui 0.0 como valor padrão.
                        valor_item = 0.0

                    # Tenta buscar no banco de dados o preço de compra do
                    #       produto, caso o item seja um produto.
                    # Isso permite calcular a comissão com base no custo
                    #       real do produto ou serviço.
                    produto = colecao_produtos.find_one({"nome": produto_servico_nome})
                    if produto and "preco_compra" in produto:

                        # Se o produto for encontrado e tiver o campo "preco_compra",
                        # converte esse valor para um número decimal para cálculo posterior.
                        custo_item = float(produto["preco_compra"])

                    else:

                        # Caso o produto não seja encontrado ou não tenha o preço de compra,
                        # assume que o item é um serviço, e o custo será zero.
                        custo_item = 0.0

                    # Calcular comissão do item com base na porcentagem do funcionário
                    # Ex: se funcionario_doc["comissao"] = 15 => comissao_item = valor_item * 0.15
                    comissao_item = round(valor_item * (porcentagem_comissao / 100), 2)

                    # Determina o lucro do item, levando em consideração o valor do item, o
                    #       custo do item e a comissão do funcionário.
                    # Se o custo do item for maior que zero, o lucro é calculado subtraindo o
                    #       custo e a comissão do valor do item.
                    # Caso contrário, o lucro será apenas o valor do item menos a comissão.
                    lucro = valor_item - custo_item - comissao_item if custo_item > 0 else valor_item - comissao_item

                    # Cria o dicionário que será salvo no banco de dados como um relatório.
                    # O dicionário inclui todas as informações relevantes sobre o
                    #       agendamento e o serviço/produto realizado.
                    relatorio_item = {
                        "data": self.agendamento.get("data", ""),  # Data do agendamento
                        "hora_inicio": self.agendamento.get("inicio", ""),  # Hora de início do agendamento
                        "hora_fim": self.agendamento.get("fim", ""),  # Hora de fim do agendamento
                        "cliente": self.agendamento.get("cliente", ""),  # Nome do cliente
                        "funcionario": funcionario_nome,  # Nome do funcionário responsável
                        "produto_servico": produto_servico_nome,  # Nome do produto ou serviço realizado
                        "valor": valor_item,  # Valor do produto ou serviço
                        "custo": custo_item,  # Custo do produto ou serviço
                        "lucro": lucro,  # Lucro do item (valor - custo - comissão)
                        "comissao_funcionario": comissao_item,  # Comissão do funcionário sobre esse item
                        "status": "Finalizado"  # Status do item após a finalização do serviço
                    }

                    # Inserir o relatório individual na coleção de relatórios
                    colecao_relatorios.insert_one(relatorio_item)

            # Cria o dicionário 'relatorio' contendo as informações do
            #       agendamento e o cálculo das comissões.
            # Esses dados serão salvos no banco de dados de relatórios.
            relatorio = {
                "data": self.agendamento.get("data", ""),  # Data do agendamento.
                "hora_inicio": self.agendamento.get("inicio", ""),  # Hora de início do agendamento.
                "hora_fim": self.agendamento.get("fim", ""),  # Hora de fim do agendamento.
                "cliente": self.agendamento.get("cliente", ""),  # Nome do cliente do agendamento.
                "funcionario": funcionario_nome,  # Nome do funcionário responsável pelo serviço.
                "itens": self.itens,  # Lista de itens (produtos/serviços) associados ao agendamento.
                "valor_total": valor_total,  # Valor total do agendamento (soma dos itens).
                # Calcula a comissão do funcionário com base no valor total e na porcentagem de comissão.
                # O valor da comissão é arredondado para duas casas decimais.
                "comissao_funcionario": round(valor_total * (porcentagem_comissao / 100), 2),
                "status": "Finalizado"  # Marca o status do agendamento como "Finalizado".
            }

            # Atualiza o agendamento no banco de dados com as informações do relatório.
            # Usamos a função 'update_one' para modificar o agendamento
            #       específico com o ID fornecido.
            # A operação de atualização usa o método "$set" para substituir ou
            #       adicionar os campos de relatório no agendamento.
            resultado_atualizacao = colecao_agendamentos.update_one(
                {"_id": ObjectId(self.agendamento_id)},  # Filtra pelo ID do agendamento.
                {"$set": relatorio}  # Atualiza o agendamento com as informações do relatório.
            )

            # Verifica se algum documento foi realmente modificado.
            # A função `modified_count` retorna o número de documentos
            #       modificados pela operação.
            # Se o valor for 0, significa que o agendamento não foi
            #       atualizado corretamente, então exibe um erro.
            if resultado_atualizacao.modified_count == 0:
                messagebox.showerror("Erro",
                                     "Nenhum documento foi atualizado na coleção de agendamentos.")
                return



        except Exception as e:

            # Captura qualquer exceção que possa ocorrer durante o
            #       processo de salvar o relatório.
            # Exibe uma mensagem de erro detalhando o problema para o usuário.
            messagebox.showerror("Erro", f"Erro ao salvar relatório: {e}")
            return



    # Define o método `remover_item` para remover itens
    #       selecionados do agendamento.
    def remover_item(self):

        # Obtém o item selecionado na Treeview.
        selecionado = self.tree.selection()

        # Verifica se nenhum item foi selecionado.
        if not selecionado:

            # Exibe uma mensagem de aviso caso nenhum item esteja selecionado.
            messagebox.showwarning("Aviso", "Nenhum item selecionado.")

            # Interrompe a execução do método, pois não há itens para remover.
            return

        # Itera sobre os itens selecionados na Treeview.
        for sel in selecionado:

            # Obtém os valores do item selecionado, retornando uma
            #       tupla com (nome, preço, tipo).
            valores = self.tree.item(sel, "values")  # (nome, preco, tipo)

            # Extrai o nome do item a partir do primeiro valor da tupla.
            nome = valores[0]

            # Converte o segundo valor (preço) para um número de ponto flutuante.
            preco = float(valores[1])

            # Armazena o tipo do item, que é o terceiro valor da tupla.
            tipo = valores[2]

            # Inicializa uma lista para armazenar itens que permanecerão após a remoção.
            nova_lista = []

            # Marca para rastrear se o item foi removido uma vez.
            removido_uma_vez = False

            # Itera sobre a lista de itens atuais para encontrar o
            #       item correspondente.
            for it in self.itens:

                # `it` contém (_id, nome_item, preco_item, tipo_item)
                # Verifica se o item não foi removido ainda e corresponde ao selecionado.
                if (not removido_uma_vez and it[1] == nome and it[2] == preco and it[3] == tipo):

                    # Marca que o item foi removido para evitar duplicação de remoções.
                    removido_uma_vez = True

                    # Atualiza o estoque para reverter o abate ao excluir o item.
                    self.atualizar_estoque(it[0], tipo, abater=False)

                else:

                    # Adiciona o item à nova lista, mantendo os não removidos.
                    nova_lista.append(it)

            # Atualiza a lista de itens com a nova lista após a remoção.
            self.itens = nova_lista

            # Remove o item selecionado da Treeview.
            self.tree.delete(sel)


    # Define o método `adicionar_item` para adicionar novos itens ao agendamento.
    def adicionar_item(self):

        # Define uma função de callback que será chamada quando os
        #       itens forem selecionados na tela de seleção.
        def callback(itens_selecionados):

            # Itera sobre os itens selecionados na tela de seleção.
            for (id_str, nome, preco, tipo) in itens_selecionados:

                # Chama o método `atualizar_estoque` para abater o estoque
                #       imediatamente, caso o item seja um produto ou serviço.
                # `id_str` é o identificador único do item.
                # `tipo` indica se é produto ou serviço.
                # `abater=True` sinaliza que o estoque deve ser reduzido.
                self.atualizar_estoque(id_str, tipo, abater=True)

                # Adiciona o item à lista `self.itens`, que contém os itens do agendamento.
                # Cada item é representado por uma tupla contendo: (_id, nome, preco, tipo).
                self.itens.append((id_str, nome, preco, tipo))

            # Atualiza a Treeview para exibir os itens adicionados.
            self.carregar_itens()

        # Cria uma nova janela (Toplevel) para a tela de
        #       seleção de serviços/produtos.
        win = tk.Toplevel(self)

        # Instancia a `TelaSelecaoServicos`, passando a nova
        #       janela (`win`) e a função de callback como parâmetros.
        # A tela de seleção permitirá escolher itens que serão
        #       retornados para o callback.
        TelaSelecaoServicos(win, callback)


    def atualizar_estoque(self, item_id, tipo, abater=True):

        """
        Atualiza o estoque (quantidade) de um produto/serviço no banco de dados.

        - Se `abater=True`, subtrai 1 do estoque.
        - Se `abater=False`, adiciona 1 ao estoque.

        Parâmetros:
        - `item_id`: O ID do item no banco de dados (produto/serviço).
        - `tipo`: O tipo do item, usado para verificar se é aplicável ao estoque.
        - `abater`: Indica se o estoque será decrementado (True) ou incrementado (False).
        """

        # Verifica se o tipo é "produto", que possui controle de estoque.
        if tipo == "produto":

            # Define a coleção no banco de dados que será atualizada.
            colecao = colecao_produtos

        else:

            # Exibe um aviso caso o tipo seja desconhecido ou não aplicável ao estoque.
            messagebox.showwarning("Estoque", f"Tipo desconhecido: {tipo}.")
            return

        # Busca o documento (produto) correspondente no banco de dados pelo ID fornecido.
        doc = colecao.find_one({"_id": ObjectId(item_id)})

        # Verifica se o documento correspondente foi encontrado no banco de dados.
        if not doc:

            # Exibe um aviso se o item não foi localizado, informando o tipo e ID.
            messagebox.showwarning("Estoque",
                                   f"{tipo.capitalize()} (ID={item_id}) não encontrado.")
            return

        try:

            # Obtém a quantidade atual do documento e a converte para um número inteiro.
            # Caso a quantidade não esteja no formato esperado, ocorre um ValueError.
            qtd_atual = int(doc.get("quantidade", 0))  # Certifique-se de que é um número inteiro

        except ValueError:

            # Exibe um erro se a quantidade no banco de dados não é válida.
            messagebox.showerror("Estoque",
                                 f"Quantidade inválida no banco de dados para {doc.get('nome', 'desconhecido')}.")
            return

        # Define o valor de incremento ou decremento no estoque
        #       com base no parâmetro `abater`.
        # Se `abater=True`, delta será positivo para subtração;
        #       caso contrário, será negativo.
        delta = 1 if abater else -1

        # Calcula a nova quantidade no estoque.
        # Se abater=True, subtrai delta; caso contrário, adiciona delta.
        nova_qtd = qtd_atual - delta if abater else qtd_atual + abs(delta)

        # Verifica se a nova quantidade no estoque seria negativa.
        # Caso a nova quantidade seja menor que zero, exibe um
        #       erro e interrompe o processo.
        if nova_qtd < 0:
            messagebox.showerror("Estoque",
                                 f"Estoque insuficiente de '{doc.get('nome', '')}'.")
            return

        # Atualiza o documento no banco de dados para refletir a
        #       nova quantidade no estoque.
        # Usa o método `update_one` para alterar apenas o
        #       campo "quantidade" do item correspondente.
        colecao.update_one(
            {"_id": doc["_id"]},  # Localiza o documento pelo ID.
            {"$set": {"quantidade": nova_qtd}}  # Atualiza o campo "quantidade" com o novo valor.
        )



    # Define o método `carregar_itens` para exibir os itens
    #       associados ao agendamento na `Treeview`.
    def carregar_itens(self):

        # Itera sobre todos os itens da Treeview atual e os remove.
        for i in self.tree.get_children():

            # Remove cada item usando seu identificador.
            self.tree.delete(i)

        # Itera sobre os itens armazenados na lista `self.itens`.
        for item in self.itens:

            # Cada item é representado por uma tupla contendo: (_id, nome, preco, tipo).
            nome = item[1]  # Obtém o nome do item, que está na posição 1 da tupla.
            preco = item[2]  # Obtém o preço do item, que está na posição 2 da tupla.
            tipo = item[3]  # Obtém o tipo do item, que está na posição 3 da tupla.

            # Insere o item na Treeview. O valor de cada coluna é
            #       definido pelos campos da tupla.
            self.tree.insert(
                "",  # O item será inserido na raiz da Treeview (sem hierarquia).
                "end",  # Insere o item no final da lista.
                values=(nome, preco, tipo)  # Define os valores das colunas: Nome, Preço e Tipo.
            )


    # Define o método `listar_funcionarios` para obter os nomes dos
    #       funcionários cadastrados no banco de dados.
    def listar_funcionarios(self):

        """
        Retorna uma lista contendo o nome de todos os funcionários cadastrados.
        Os nomes são obtidos a partir da coleção `colecao_funcionarios` no banco de dados.
        Os funcionários são retornados em ordem alfabética pelo campo "nome".
        """

        return [

            # Obtém o valor associado à chave "nome". Caso não exista,
            #       retorna uma string vazia.
            f.get("nome", "")

            # Consulta os funcionários e ordena por nome.
            for f in colecao_funcionarios.find().sort("nome", pymongo.ASCENDING)

        ]


# ------------------------------------------------------------
# Tela Selecao Servicos
# ------------------------------------------------------------
class TelaSelecaoServicos:

    """
    Classe responsável por criar uma janela para seleção de serviços ou produtos.
    """

    # Método construtor da classe `TelaSelecaoServicos`, chamado
    #       automaticamente ao instanciar a classe.
    def __init__(self, master, callback_selecao=None):

        # Armazena a referência ao widget pai (a janela
        #       principal ou outro widget).
        # `master` é usado como o widget pai para posicionar esta janela.
        self.master = master

        # Callback opcional, uma função que será chamada quando a seleção for concluída.
        # Permite retornar os itens selecionados para quem instanciou esta tela.
        self.callback_selecao = callback_selecao


        # Configurar a janela principal
        # Define o título da janela como "Selecionar Serviços/Produtos".
        self.master.title("Selecionar Serviços/Produtos")

        # Configurações adicionais para a janela principal:
        # Define o fundo da janela como cinza claro (#f5f5f5) para um visual limpo.
        self.master.configure(bg="#f5f5f5")

        # Ajusta a janela para o estado maximizado (ocupando toda a tela).
        self.master.state('zoomed')

        # Inicializa uma lista vazia para armazenar os itens selecionados.
        self.itens_selecionados = []

        # Cria um frame principal dentro da janela para organizar os widgets.
        # Este frame servirá como contêiner para outros elementos da interface.
        self.frame_principal = tk.Frame(self.master)

        # Posiciona o frame principal na interface.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels nas bordas do frame.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels nas bordas do frame.
        # `fill="both"` faz com que o frame preencha toda a largura e altura disponíveis.
        # `expand=True` permite que o frame cresça proporcionalmente ao redimensionamento da janela.
        self.frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

        # Adiciona um rótulo (Label) ao `frame_principal` com o
        #       texto "Selecione os itens desejados:".
        # `text="Selecione os itens desejados:"` define o texto exibido no rótulo.
        # `font=("Arial", 14, "bold")` configura a fonte do texto
        #       como Arial, tamanho 14, com estilo negrito.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       acima e abaixo do rótulo.
        tk.Label(self.frame_principal,
                 text="Selecione os itens desejados:",
                 font=("Arial", 14, "bold")).pack(pady=5)

        # Cria um frame para organizar os Treeviews dentro do `frame_principal`.
        # O `frame_treeviews` será usado para agrupar e organizar a
        #       exibição das tabelas de dados (Treeviews).
        self.frame_treeviews = tk.Frame(self.frame_principal)

        # Posiciona o `frame_treeviews` dentro do `frame_principal`.
        # `fill="x"` faz com que o frame preencha toda a largura
        #       disponível no eixo horizontal.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       acima e abaixo do frame.
        self.frame_treeviews.pack(fill="x", pady=5)

        # Treeview para Serviços
        # Cria um Treeview chamado `tree_servicos` dentro do `frame_treeviews`.
        # Este Treeview será usado para exibir os serviços disponíveis.
        # Define o frame pai como `frame_treeviews`.
        self.tree_servicos = ttk.Treeview(self.frame_treeviews,

                                        # Define as colunas exibidas no Treeview.
                                        columns=("_id", "nome", "preco", "tipo"),

                                        # Exibe apenas os cabeçalhos das colunas (sem a coluna de ícones padrão).
                                        show="headings",

                                        # Define a altura do Treeview para exibir 8 linhas de itens por vez.
                                        height=8)

        # Define o texto do cabeçalho da coluna "_id" como "ID".
        self.tree_servicos.heading("_id", text="ID")

        # Define o texto do cabeçalho da coluna "nome" como "Serviço".
        self.tree_servicos.heading("nome", text="Serviço")

        # Define o texto do cabeçalho da coluna "preco" como "Preço (R$)".
        self.tree_servicos.heading("preco", text="Preço (R$)")

        # Define o texto do cabeçalho da coluna "tipo" como "Tipo".
        self.tree_servicos.heading("tipo", text="Tipo")

        # Define a largura da coluna "_id" como 0 e impede que ela se expanda.
        # Isso é útil para ocultar a coluna "_id" na interface,
        #       pois ela não é necessária para o usuário.
        self.tree_servicos.column("_id", width=0, stretch=tk.NO)

        # Define a largura da coluna "nome" como 200 pixels.
        # Esta coluna exibe o nome do serviço e precisa de
        #       espaço suficiente para o texto.
        self.tree_servicos.column("nome", width=200)

        # Define a largura da coluna "preco" como 80 pixels.
        # Alinha o conteúdo da coluna ao centro para uma melhor organização visual.
        self.tree_servicos.column("preco", width=80, anchor="center")

        # Define a largura da coluna "tipo" como 80 pixels.
        # Alinha o conteúdo da coluna ao centro para uma melhor organização visual.
        self.tree_servicos.column("tipo", width=80, anchor="center")

        # Posiciona o Treeview `self.tree_servicos` no lado esquerdo do `frame_treeviews`.
        # Adiciona um espaçamento horizontal (padding) de 5 pixels em volta do Treeview.
        self.tree_servicos.pack(side="left", padx=5)

        # Cria um botão `btn_servico` para adicionar serviços selecionados na Treeview.
        # Define o texto exibido no botão como "Adicionar Serviço".
        # Atribui o método `self.adicionar_item_servico` para ser
        #       executado quando o botão for clicado.
        btn_servico = tk.Button(self.frame_treeviews,
                                text="Adicionar Serviço",
                                command=self.adicionar_item_servico)

        # Posiciona o botão `btn_servico` no lado esquerdo do `frame_treeviews`.
        # Adiciona um espaçamento horizontal (padding) de 5 pixels
        #       entre o botão e os outros elementos.
        btn_servico.pack(side="left", padx=5)

        # Cria um Treeview chamado `self.tree_produtos` dentro do `frame_treeviews`.
        # Este Treeview exibirá informações de produtos, como ID, Nome, Preço e Tipo.
        # `columns` define as colunas: "_id", "nome", "preco" e "tipo".
        # `show="headings"` faz com que apenas os cabeçalhos e colunas
        #       especificados sejam exibidos (sem a coluna padrão).
        # `height=8` define que o Treeview exibirá até 8 linhas
        #       visíveis antes de precisar de rolagem.
        self.tree_produtos = ttk.Treeview( self.frame_treeviews,
                                            columns=("_id", "nome", "preco", "tipo"),
                                            show="headings",
                                            height=8)

        # Define o cabeçalho da coluna "_id" no Treeview `self.tree_produtos`.
        # O texto do cabeçalho será "ID".
        self.tree_produtos.heading("_id", text="ID")

        # Define o cabeçalho da coluna "nome" no Treeview `self.tree_produtos`.
        # O texto do cabeçalho será "Produto".
        self.tree_produtos.heading("nome", text="Produto")

        # Define o cabeçalho da coluna "preco" no Treeview `self.tree_produtos`.
        # O texto do cabeçalho será "Preço (R$)".
        self.tree_produtos.heading("preco", text="Preço (R$)")

        # Define o cabeçalho da coluna "tipo" no Treeview `self.tree_produtos`.
        # O texto do cabeçalho será "Tipo".
        self.tree_produtos.heading("tipo", text="Tipo")

        # Configura a coluna "_id" no Treeview `self.tree_produtos`.
        # Define a largura da coluna como 0 para ocultá-la.
        # `stretch=tk.NO` impede que a coluna seja redimensionada pelo usuário.
        self.tree_produtos.column("_id", width=0, stretch=tk.NO)

        # Configura a coluna "nome" no Treeview `self.tree_produtos`.
        # Define a largura da coluna como 200 pixels.
        self.tree_produtos.column("nome", width=200)

        # Configura a coluna "preco" no Treeview `self.tree_produtos`.
        # Define a largura da coluna como 80 pixels.
        # `anchor="center"` alinha os valores da coluna ao centro.
        self.tree_produtos.column("preco", width=80, anchor="center")

        # Configura a coluna "tipo" no Treeview `self.tree_produtos`.
        # Define a largura da coluna como 80 pixels.
        # `anchor="center"` alinha os valores da coluna ao centro.
        self.tree_produtos.column("tipo", width=80, anchor="center")

        # Posiciona o Treeview `self.tree_produtos` no lado
        #       esquerdo do `frame_treeviews`.
        # Adiciona um espaçamento horizontal (padding) de 5 pixels
        #       entre o Treeview e os outros elementos.
        self.tree_produtos.pack(side="left", padx=5)

        # Cria o botão "Adicionar Produto" no frame `self.frame_treeviews`.
        # Este botão será usado para adicionar itens à lista de produtos.
        # `text="Adicionar Produto"` define o texto exibido no botão.
        # `command=self.adicionar_item_produto` associa o clique do
        #       botão ao método `self.adicionar_item_produto`.
        btn_produto = tk.Button(self.frame_treeviews,
                                text="Adicionar Produto",
                                command=self.adicionar_item_produto)

        # Posiciona o botão no lado esquerdo do frame `self.frame_treeviews`.
        # `side="left"` alinha o botão ao lado esquerdo do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        btn_produto.pack(side="left", padx=5)

        # Frame de itens selecionados
        # Cria um frame para exibir os itens selecionados.
        # Este frame será usado para organizar os elementos
        #       relacionados aos itens que foram selecionados.
        self.frame_selecionados = tk.Frame(self.frame_principal)

        # Posiciona o frame `self.frame_selecionados` dentro de `self.frame_principal`.
        # `fill="both"` faz com que o frame ocupe toda a largura disponível.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        self.frame_selecionados.pack(fill="both", pady=10)

        # Adiciona um rótulo (Label) no frame `self.frame_selecionados`
        #       com o texto "Itens Selecionados:".
        # O rótulo indica a lista de itens que já foram adicionados pelo usuário.
        # `font=("Arial", 12, "bold")` define a fonte do
        #       texto com tamanho 12 e estilo negrito.
        tk.Label(self.frame_selecionados,

                 # `anchor="w"` alinha o texto à esquerda (west) dentro do frame.
                 text="Itens Selecionados:",

                 # `pady=2` adiciona um espaçamento vertical de 2
                 #      pixels ao redor do rótulo.
                 font=("Arial", 12, "bold")).pack(anchor="w",
                                                  pady=2)

        # Cria uma Treeview para exibir os itens selecionados.
        # `self.frame_selecionados` é o frame pai onde a Treeview será posicionada.
        # `columns=("nome", "preco", "tipo")` define as colunas
        #       que a Treeview terá, sendo elas:
        #   - "nome": Nome do serviço/produto.
        #   - "preco": Preço associado ao item.
        #   - "tipo": Indica se é um serviço ou produto.
        # `show="headings"` remove a coluna extra que geralmente é
        #       exibida à esquerda da Treeview.
        # `height=8` define a quantidade de linhas visíveis na Treeview.
        self.tree_selecionados = ttk.Treeview( self.frame_selecionados,
                                               columns=("nome", "preco", "tipo"),
                                               show="headings",
                                               height=8 )

        # Configura o cabeçalho da coluna "nome" com o texto "Item".
        self.tree_selecionados.heading("nome", text="Item")

        # Configura o cabeçalho da coluna "preco" com o texto "Preço (R$)".
        self.tree_selecionados.heading("preco", text="Preço (R$)")

        # Configura o cabeçalho da coluna "tipo" com o texto "Tipo".
        self.tree_selecionados.heading("tipo", text="Tipo")

        # Define a largura da coluna "nome" como 200 pixels.
        self.tree_selecionados.column("nome", width=200)

        # Define a largura da coluna "preco" como 80 pixels e centraliza o conteúdo.
        self.tree_selecionados.column("preco", width=80, anchor="center")

        # Define a largura da coluna "tipo" como 80 pixels e centraliza o conteúdo.
        self.tree_selecionados.column("tipo", width=80, anchor="center")

        # Posiciona a Treeview dentro do `frame_selecionados`.
        # `fill="both"` faz com que a Treeview preencha tanto a largura
        #       quanto a altura disponíveis no frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta da Treeview.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta da Treeview.
        # `expand=True` permite que a Treeview cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree_selecionados.pack(fill="both", padx=5, pady=5, expand=True)

        # Adiciona um botão no `frame_selecionados` com o texto "Remover Item".
        # Associa o método `remover_item` ao evento de clique do botão.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do botão.
        tk.Button(self.frame_selecionados,
                  text="Remover Item",
                  command=self.remover_item).pack(pady=5)

        # Cria um rótulo (`Label`) dentro do `frame_principal` para exibir o total.
        # Define o texto inicial como "Total (R$): 0.00".
        # Estiliza o texto com fonte Arial, tamanho 12 e em negrito.
        self.total_label = tk.Label(self.frame_principal,
                                    text="Total (R$): 0.00",
                                    font=("Arial", 12, "bold"))

        # Posiciona o rótulo no `frame_principal`.
        # `anchor="e"` alinha o rótulo à direita (east) dentro do frame.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       acima e abaixo do rótulo.
        self.total_label.pack(anchor="e", pady=5)

        # Cria um frame (`Frame`) dentro do `frame_principal` para
        #       conter os botões de confirmação.
        # Este frame será usado para organizar e alinhar os botões de forma consistente.
        self.frame_confirmar = tk.Frame(self.frame_principal)

        # Posiciona o frame no `frame_principal`.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do frame.
        self.frame_confirmar.pack(fill="x", pady=5)

        # Adiciona um botão de "Cancelar" dentro do `frame_confirmar`.
        # O texto do botão é "Cancelar" e ao ser clicado, ele fecha a
        #       janela atual chamando `self.master.destroy`.
        # `side="left"` posiciona o botão no lado esquerdo do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do botão.
        tk.Button(self.frame_confirmar,
                  text="Cancelar",
                  command=self.master.destroy).pack(side="left",
                                                    padx=5)

        # Adiciona um botão de "Confirmar" dentro do `frame_confirmar`.
        # O texto do botão é "Confirmar" e ao ser clicado, ele
        #       executa a função `self.confirmar_selecao`.
        # `side="right"` posiciona o botão no lado direito do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do botão.
        tk.Button(self.frame_confirmar,
                  text="Confirmar",
                  command=self.confirmar_selecao).pack(side="right",
                                                       padx=5)

        # Carrega os serviços do banco de dados e os exibe na interface.
        self.carregar_servicos_do_bd()

        # Carrega os produtos do banco de dados e os exibe na interface.
        self.carregar_produtos_do_bd()


    def carregar_servicos_do_bd(self):

        # Itera sobre os serviços armazenados na coleção `colecao_servicos`,
        #       ordenando-os pelo campo "nome" em ordem ascendente.
        for servico in colecao_servicos.find().sort("nome", pymongo.ASCENDING):

            # Converte o identificador único do serviço (_id) para uma
            #       string para evitar problemas de manipulação.
            _id_str = str(servico["_id"])

            # Obtém o nome do serviço, ou uma string vazia caso o campo não exista.
            nome = servico.get("nome", "")

            # Obtém o preço do serviço, ou define como 0.0 caso o
            #       campo não esteja presente ou seja inválido.
            preco = servico.get("preco", 0.0)

            # Insere o serviço como uma nova linha na TreeView `tree_servicos`.
            # O valor "servico" é adicionado à coluna "tipo" para
            #       diferenciá-lo de outros itens.
            self.tree_servicos.insert("",
                                      "end",
                                      values=(_id_str, nome, preco, "servico"))



    def carregar_produtos_do_bd(self):

        # Itera sobre os produtos armazenados na coleção `colecao_produtos`,
        #       ordenando-os pelo campo "nome" em ordem ascendente.
        for produto in colecao_produtos.find().sort("nome", pymongo.ASCENDING):

            # Converte o identificador único do produto (_id) para uma string.
            _id_str = str(produto["_id"])

            # Obtém o nome do produto, ou uma string vazia caso o campo não exista.
            nome = produto.get("nome", "")

            # Obtém o preço de venda do produto.
            # Verifica se o campo "preco_venda" está presente no produto.
            # Se o campo não existir ou estiver vazio, será atribuído o valor padrão 0.0.
            preco_venda = produto.get("preco_venda", 0.0)

            # Caso o preço de venda seja 0 (ou não definido), tenta obter o preço de compra.
            # Isso é útil para garantir que um valor válido seja atribuído ao produto.
            if not preco_venda:
                preco_venda = produto.get("preco_compra", 0.0)

            # Insere o produto como uma nova linha na TreeView `tree_produtos`.
            # O valor "produto" é adicionado à coluna "tipo" para
            #       diferenciá-lo de outros itens.
            self.tree_produtos.insert("",
                                      "end",
                                      values=(_id_str, nome, preco_venda, "produto"))


    def confirmar_selecao(self):

        # Verifica se a lista de itens selecionados está vazia.
        if not self.itens_selecionados:

            # Exibe uma mensagem de aviso caso nenhum item tenha sido selecionado.
            messagebox.showwarning("Aviso", "Nenhum item selecionado.")
            return

        # Verifica se foi fornecido um callback para lidar com a seleção.
        if self.callback_selecao:

            # Chama o callback, passando os itens selecionados como argumento.
            self.callback_selecao(self.itens_selecionados)

        else:

            # Caso não haja callback, exibe uma mensagem informativa
            #       com os itens selecionados.
            messagebox.showinfo("Seleção Confirmada",
                                f"Itens:\n{self.itens_selecionados}")

        # Fecha a janela após confirmar a seleção.
        self.master.destroy()


    # Define o método para remover itens da lista de itens selecionados.
    def remover_item(self):

        # Obtém o item atualmente selecionado na Treeview de itens selecionados.
        selecionado = self.tree_selecionados.selection()

        # Verifica se há algum item selecionado para remover.
        if selecionado:

            # Itera sobre cada item selecionado.
            for sel in selecionado:

                # Obtém os valores associados ao item selecionado na Treeview.
                # Os valores representam (nome, preco, tipo).
                valores = self.tree_selecionados.item(sel, "values")

                # Extrai os valores do item selecionado.
                nome_remover = valores[0]  # Nome do item a ser removido.
                preco_remover = float(valores[1])  # Preço do item a ser removido.
                tipo_remover = valores[2]  # Tipo do item a ser removido.

                # Cria uma nova lista para armazenar os itens
                #       que permanecem após a remoção.
                nova_lista = []

                # Flag para controlar a remoção de um único item.
                removido_uma_vez = False

                # Itera sobre os itens na lista de itens selecionados.
                # `item_tuple` representa um item no formato (_id, nome, preco, tipo).
                for item_tuple in self.itens_selecionados:

                    # Verifica se o item atual corresponde ao
                    #       item que deve ser removido.
                    if (
                            not removido_uma_vez  # Garante que apenas um item seja removido por vez.
                            and item_tuple[1] == nome_remover  # Compara o nome do item.
                            and float(item_tuple[2]) == preco_remover  # Compara o preço do item.
                            and item_tuple[3] == tipo_remover  # Compara o tipo do item.
                    ):

                        # Marca o item como removido para evitar
                        #       múltiplas remoções do mesmo.
                        removido_uma_vez = True

                    else:

                        # Adiciona o item à nova lista se não for o item a ser removido.
                        nova_lista.append(item_tuple)

                # Atualiza a lista de itens selecionados com os
                #       itens que não foram removidos.
                self.itens_selecionados = nova_lista

                # Remove o item selecionado da Treeview de itens selecionados.
                self.tree_selecionados.delete(sel)

            # Atualiza o valor total exibido no rótulo,
            #       refletindo a remoção do item.
            self.atualizar_total()

        # Caso nenhum item tenha sido selecionado para remoção,
        #       exibe um aviso ao usuário.
        else:

            # Mostra uma caixa de diálogo com a mensagem "Selecione um item para remover."
            messagebox.showwarning("Aviso", "Selecione um item para remover.")



    # Define o método para adicionar um serviço à lista de itens selecionados.
    def adicionar_item_servico(self):

        # Obtém o item atualmente selecionado na Treeview de serviços.
        selecionado = self.tree_servicos.selection()

        # Verifica se há algum item selecionado.
        if selecionado:

            # Obtém os valores associados ao item selecionado na Treeview.
            # Os valores representam (_id, nome, preco, tipo).
            valores = self.tree_servicos.item(selecionado, "values")

            # Insere o item selecionado na Treeview de itens selecionados.
            # Os valores exibidos são: nome, preco, tipo.
            self.tree_selecionados.insert("",
                                          "end",
                                          values=(valores[1], valores[2], valores[3]))

            # Adiciona os valores do item à lista de itens selecionados.
            self.itens_selecionados.append(valores)

            # Atualiza o valor total exibido com base nos itens selecionados.
            self.atualizar_total()

        else:

            # Exibe uma mensagem de aviso caso nenhum serviço tenha sido selecionado.
            messagebox.showwarning("Aviso",
                                   "Selecione um serviço para adicionar.")



    def atualizar_total(self):

        # Inicializa o total com 0.0 para calcular a soma
        #       dos preços dos itens selecionados.
        total = 0.0

        # Itera sobre a lista de itens selecionados para somar os preços.
        for item_tuple in self.itens_selecionados:

            try:

                # Adiciona o preço do item ao total. O preço está na
                #       terceira posição do tuple (índice 2).
                total += float(item_tuple[2])

            except ValueError:

                # Ignora itens cujo preço não seja um número válido.
                pass

        # Atualiza o texto do rótulo exibindo o valor total
        #       formatado com duas casas decimais.
        self.total_label.config(text=f"Total (R$): {total:.2f}")



    # Define o método para adicionar um produto à lista de itens selecionados.
    def adicionar_item_produto(self):

        # Obtém o item atualmente selecionado na Treeview de produtos.
        selecionado = self.tree_produtos.selection()

        # Verifica se há algum item selecionado.
        if selecionado:

            # Obtém os valores associados ao item selecionado na Treeview.
            # Os valores representam (_id, nome, preco, tipo).
            valores = self.tree_produtos.item(selecionado, "values")

            # Insere o item selecionado na Treeview de itens selecionados.
            # Os valores exibidos são: nome, preco, tipo.
            self.tree_selecionados.insert("",
                                          "end",
                                          values=(valores[1], valores[2], valores[3]))

            # Adiciona os valores do item à lista de itens selecionados.
            self.itens_selecionados.append(valores)

            # Atualiza o valor total exibido com base nos itens selecionados.
            self.atualizar_total()

        else:

            # Exibe uma mensagem de aviso caso nenhum produto tenha sido selecionado.
            messagebox.showwarning("Aviso",
                                   "Selecione um produto para adicionar.")



# ------------------------------------------------------------
# TelaProdutos
# ------------------------------------------------------------
# Define a classe `TelaProdutos`, que herda de `ttk.Frame`.
# Essa classe é responsável por criar a interface para
#       gerenciamento de produtos.
class TelaProdutos(ttk.Frame):

    # Método construtor da classe, chamado automaticamente ao
    #       criar uma instância de `TelaProdutos`.
    def __init__(self, parent):

        # `parent` é o widget pai, ou seja, o componente onde esta tela será inserida.
        #       é o frame principal da aplicação ou uma janela secundária.
        # O método `super()` é usado para chamar o construtor da classe base (`ttk.Frame`).
        # Isso garante que todos os métodos e atributos do frame
        #       sejam inicializados corretamente.
        super().__init__(parent)

        # Cria um rótulo (Label) para o título da tela.
        # O texto exibido será "Produtos e Estoque", indicando a funcionalidade da tela.
        # `font=("Arial", 14, "bold")` define a fonte como Arial, tamanho 14, em negrito.
        # `side="top"` posiciona o rótulo no topo do frame principal.
        # `anchor="w"` alinha o rótulo à esquerda (west) no frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels.
        titulo_label = ttk.Label(self,
                                 text="Produtos e Estoque",
                                 font=("Arial", 14, "bold"))

        titulo_label.pack(side="top", anchor="w", padx=10, pady=10)

        # Cria um frame (`campos_frame`) para organizar os campos de entrada.
        # `self` indica que o frame pertence à instância atual da classe.
        # `padding=10` adiciona um espaçamento interno de 10 pixels em
        #       todas as direções dentro do frame.
        campos_frame = ttk.Frame(self, padding=10)

        # Posiciona o `campos_frame` no topo do frame principal.
        # `side="top"` coloca o frame na parte superior do layout.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        campos_frame.pack(side="top", fill="x")

        # Adiciona um rótulo (`Label`) para identificar o campo de
        #       entrada do nome do produto.
        # `text="Nome do Produto:"` define o texto exibido no rótulo.
        # `row=0` posiciona o rótulo na primeira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula.
        ttk.Label(campos_frame,
                  text="Nome do Produto:").grid(row=0,
                                                column=0,
                                                padx=5,
                                                pady=5,
                                                sticky="w")

        # Cria um campo de entrada (`Entry`) para o nome do produto.
        # `width=30` define a largura do campo como 30 caracteres.
        self.nome_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=0` posiciona o campo na primeira linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do campo.
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # Adiciona um rótulo (`Label`) para identificar o campo
        #       de entrada da marca do produto.
        # `text="Marca:"` define o texto exibido no rótulo.
        # `row=1` posiciona o rótulo na segunda linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula.
        ttk.Label(campos_frame,
                  text="Marca:").grid(row=1,
                                      column=0,
                                      padx=5,
                                      pady=5,
                                      sticky="w")

        # Cria um campo de entrada (`Entry`) para a marca do produto.
        # `width=30` define a largura do campo como 30 caracteres.
        self.marca_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=1` posiciona o campo na segunda linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do campo.
        self.marca_entry.grid(row=1, column=1, padx=5, pady=5)

        # Adiciona um rótulo (`Label`) para identificar o campo de
        #       entrada da quantidade de produto.
        # `text="Quantidade:"` define o texto exibido no rótulo.
        # `row=2` posiciona o rótulo na terceira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula.
        ttk.Label(campos_frame,
                  text="Quantidade:").grid(row=2,
                                           column=0,
                                           padx=5,
                                           pady=5,
                                           sticky="w")

        # Cria um campo de entrada (`Entry`) para a quantidade do produto.
        # `width=10` define a largura do campo como 10 caracteres.
        self.quantidade_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=2` posiciona o campo na terceira linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do campo.
        # `sticky="w"` alinha o campo à esquerda (west) na célula.
        self.quantidade_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Adiciona um rótulo (`Label`) para identificar o campo de
        #       entrada do preço de compra do produto.
        # `text="Preço de Compra:"` define o texto exibido no rótulo.
        # `row=3` posiciona o rótulo na quarta linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula.
        ttk.Label(campos_frame,
                  text="Preço de Compra:").grid(row=3,
                                                column=0,
                                                padx=5,
                                                pady=5,
                                                sticky="w")

        # Cria um campo de entrada (`Entry`) para o preço de compra do produto.
        # `width=10` define a largura do campo como 10 caracteres.
        self.preco_compra_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=3` posiciona o campo na quarta linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do campo.
        # `sticky="w"` alinha o campo à esquerda (west) na célula.
        self.preco_compra_entry.grid(row=3,
                                     column=1,
                                     padx=5,
                                     pady=5,
                                     sticky="w")

        # Adiciona um rótulo (`Label`) para identificar o campo de
        #       entrada do preço de venda do produto.
        # `text="Preço de Venda:"` define o texto exibido no rótulo.
        # `row=4` posiciona o rótulo na quinta linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula.
        ttk.Label(campos_frame,
                  text="Preço de Venda:").grid(row=4,
                                               column=0,
                                               padx=5,
                                               pady=5,
                                               sticky="w")

        # Cria um campo de entrada (`Entry`) para o preço de venda do produto.
        # `width=10` define a largura do campo como 10 caracteres.
        self.preco_venda_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=4` posiciona o campo na quinta linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do campo.
        # `sticky="w"` alinha o campo à esquerda (west) na célula.
        self.preco_venda_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Adiciona um rótulo (`Label`) para identificar o campo de
        #       seleção da categoria do produto.
        # `text="Categoria:"` define o texto exibido no rótulo.
        # `row=5` posiciona o rótulo na sexta linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula.
        ttk.Label(campos_frame,
                  text="Categoria:").grid(row=5,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky="w")

        # Cria um campo de seleção (`Combobox`) para escolher a categoria do produto.
        # `values=CATEGORIAS_PRODUTOS` define a lista de opções disponíveis na combobox.
        # `width=20` define a largura da combobox como 20 caracteres.
        self.categoria_combo = ttk.Combobox(campos_frame,
                                            values=CATEGORIAS_PRODUTOS,
                                            width=20)

        # Posiciona o campo de seleção na grade do `campos_frame`.
        # `row=5` posiciona a combobox na sexta linha da grade.
        # `column=1` posiciona a combobox na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em volta da combobox.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em volta da combobox.
        # `sticky="w"` alinha a combobox à esquerda (west) na célula.
        self.categoria_combo.grid(row=5,
                                  column=1,
                                  padx=5,
                                  pady=5,
                                  sticky="w")

        # Cria um frame (`Frame`) para agrupar os botões de ação
        #       relacionados ao gerenciamento de produtos.
        # Este frame é útil para organizar os botões em uma linha separada no layout.
        botoes_frame = ttk.Frame(campos_frame)

        # Posiciona o frame de botões na grade do `campos_frame`.
        # `row=6` posiciona o frame na sétima linha da grade (index começa em 0).
        # `column=0` posiciona o frame na primeira coluna da grade.
        # `columnspan=2` faz com que o frame ocupe duas colunas, centralizando os botões.
        # `pady=10` adiciona 10 pixels de espaçamento vertical acima e abaixo do frame.
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Cria um botão chamado "Adicionar" no `botoes_frame`.
        # `text="Adicionar"` define o texto exibido no botão.
        # `command=self.novo_produto` vincula o método `novo_produto`
        #       para ser executado quando o botão for clicado.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Adicionar",
                   command=self.novo_produto).pack(side="left",
                                                   padx=5)

        # Cria um botão chamado "Editar" no `botoes_frame`.
        # `text="Editar"` define o texto exibido no botão.
        # `command=self.editar_produto` vincula o método `editar_produto`
        #       para ser executado quando o botão for clicado.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Editar",
                   command=self.editar_produto).pack(side="left",
                                                     padx=5)

        # Cria um botão chamado "Excluir" no `botoes_frame`.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir_produto` vincula o método `excluir_produto`
        #       para ser executado quando o botão for clicado.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Excluir",
                   command=self.excluir_produto).pack(side="left", padx=5)

        # Cria um botão chamado "Add Estoque" no `botoes_frame`.
        # `text="Add Estoque"` define o texto exibido no botão.
        # `command=self.adicionar_estoque` vincula o método `adicionar_estoque`
        #       para ser executado quando o botão for clicado.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Add Estoque",
                   command=self.adicionar_estoque).pack(side="left",
                                                        padx=5)

        # Cria um frame chamado `table_frame` dentro da tela principal.
        # Este frame será usado para posicionar e organizar a tabela de exibição de produtos.
        # `side="top"` posiciona o frame na parte superior da tela principal.
        # `fill="both"` faz com que o frame preencha tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o frame expanda proporcionalmente quando a janela for redimensionada.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do frame.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do frame.
        table_frame = ttk.Frame(self)
        table_frame.pack(side="top",
                         fill="both",
                         expand=True,
                         padx=10,
                         pady=10)

        # Cria uma Treeview chamada `self.tree` dentro do frame `table_frame`.
        # A Treeview será usada para exibir os dados dos produtos em formato de tabela.
        # O frame onde a Treeview será posicionada.
        self.tree = ttk.Treeview(table_frame,

                                 # Define as colunas da tabela.
                                columns=("nome", "marca", "quantidade", "compra", "venda", "categoria"),

                                 # Mostra apenas o cabeçalho das colunas, sem a
                                 #      coluna de hierarquia padrão.
                                show="headings")


        # Configura o cabeçalho da coluna "nome".
        # Define o texto exibido como "Nome".
        self.tree.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna "marca".
        # Define o texto exibido como "Marca".
        self.tree.heading("marca", text="Marca")

        # Configura o cabeçalho da coluna "quantidade".
        # Define o texto exibido como "Qtd" (abreviação de Quantidade).
        self.tree.heading("quantidade", text="Qtd")

        # Configura o cabeçalho da coluna "compra".
        # Define o texto exibido como "Compra" (preço de compra do produto).
        self.tree.heading("compra", text="Compra")

        # Configura o cabeçalho da coluna "venda".
        # Define o texto exibido como "Venda" (preço de venda do produto).
        self.tree.heading("venda", text="Venda")

        # Configura o cabeçalho da coluna "categoria".
        # Define o texto exibido como "Categoria" (categoria do produto).
        self.tree.heading("categoria", text="Categoria")

        # Cria um scrollbar vertical associado à Treeview `self.tree`.
        # `orient="vertical"` indica que o scrollbar será vertical.
        # O comando `self.tree.yview` permite que o scrollbar mova o conteúdo da Treeview.
        scrollbar = ttk.Scrollbar(table_frame,  # O frame onde o scrollbar será posicionado.
                                orient="vertical",  # Define a orientação como vertical.
                                command=self.tree.yview)  # Associa o comando para mover o conteúdo da Treeview.


        # Configura a Treeview `self.tree` para utilizar o scrollbar criado.
        self.tree.configure(yscroll=scrollbar.set)

        # Posiciona a Treeview `self.tree` no frame.
        # `side="left"` alinha a Treeview no lado esquerdo do frame.
        # `fill="both"` faz com que a Treeview preencha tanto a
        #       largura quanto a altura disponíveis.
        # `expand=True` permite que a Treeview cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona o scrollbar no lado esquerdo do frame, ao lado da Treeview.
        # `fill="y"` faz com que o scrollbar preencha toda a altura do frame.
        scrollbar.pack(side="left", fill="y")

        # Configura uma tag chamada `estoque_baixo` para destacar
        #       produtos com estoque baixo.
        # Define a cor de fundo dos itens com esta tag como um vermelho claro (#ff9999).
        self.tree.tag_configure("estoque_baixo", background="#ff9999")

        # Vincula o evento de seleção de itens na Treeview ao
        #       método `selecionar_item_tree`.
        # Este método será chamado sempre que um item for selecionado na Treeview.
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_tree)

        # Vincula o evento de duplo clique ("<Double-1>") na Treeview a uma função chamada `abrir_historico_vendas`
        # `self.tree` representa a Treeview principal onde os produtos estão exibidos
        # `bind("<Double-1>", ...)` associa um evento ao widget. Neste caso:
        # - "<Double-1>" significa "clique duplo com o botão esquerdo do mouse"
        # - `self.abrir_historico_vendas` é a função que será executada quando o evento ocorrer
        self.tree.bind("<Double-1>", self.abrir_historico_vendas)

        # Carrega os dados dos produtos no banco de dados
        #       para exibição na Treeview.
        self.carregar_produtos()


    def abrir_historico_vendas(self, event):

        """
        Função que abre uma janela com o histórico de vendas de um produto selecionado.
        É acionada quando um evento (como um clique duplo) ocorre na Treeview.
        """

        try:

            # Obtém o ID do item selecionado na Treeview (o usuário precisa ter selecionado algo)
            item_selecionado = self.tree.selection()[0]

            # Converte o ID do item selecionado para um ObjectId (usado pelo MongoDB para identificar documentos)
            produto_id = ObjectId(item_selecionado)

            # Busca no banco de dados (coleção `colecao_produtos`) o documento correspondente ao ID do produto
            produto = colecao_produtos.find_one({"_id": produto_id})

            # Verifica se o produto existe. Se não for encontrado, exibe uma mensagem de erro para o usuário
            if not produto:

                # Exibe uma caixa de diálogo com a mensagem de erro
                messagebox.showerror("Erro", "Produto não encontrado.")

                # Sai da função, pois não faz sentido continuar sem um produto válido
                return


            # Função para carregar os dados na Treeview com base nos filtros aplicados
            def carregar_dados():

                # Limpa todos os itens atualmente exibidos na Treeview
                # `tree_vendas.get_children()` retorna todos os IDs dos itens na Treeview
                # `tree_vendas.delete(item)` remove cada item um por um
                for item in tree_vendas.get_children():
                    tree_vendas.delete(item)

                # Inicializa a variável `total` com o valor 0
                # Essa variável será usada para somar os valores pagos (preços) dos itens exibidos
                total = 0

                # Obtém o valor digitado no campo de entrada de data inicial
                # `filtro_data_inicio.get()` pega o texto do campo, e `.strip()` remove espaços extras
                data_inicio = filtro_data_inicio.get().strip()

                # Obtém o valor digitado no campo de entrada de data final
                # Segue o mesmo processo do campo de data inicial
                data_fim = filtro_data_fim.get().strip()

                # Obtém o valor digitado no campo de entrada de nome do cliente
                # `filtro_cliente.get()` pega o texto digitado no campo, e `.lower()` converte para letras minúsculas
                # Isso é feito para que a busca no banco de dados não seja sensível a letras maiúsculas ou minúsculas
                nome_cliente = filtro_cliente.get().strip().lower()

                # Define a consulta inicial (query) para buscar os documentos no banco de dados MongoDB
                query = {

                    # Apenas registros com o status "Finalizado"
                    "status": "Finalizado",

                    # Verifica se o produto_id está nos itens
                    "itens": {"$elemMatch": {"0": str(produto_id)}},
                }

                # Adiciona o filtro de datas na consulta, se a data inicial for preenchida
                if data_inicio:

                    # Adiciona um critério de busca: busca registros com data maior ou igual à data_inicio
                    query["data"] = {"$gte": data_inicio}

                # Adiciona o filtro de datas na consulta, se a data final for preenchida
                if data_fim:

                    # Atualiza a condição de busca para incluir registros com data menor ou igual à data_fim
                    # Se "data" já existir na consulta, ele mantém os critérios anteriores e adiciona "$lte"
                    query["data"] = query.get("data", {})  # Garante que a chave "data" já existe
                    query["data"]["$lte"] = data_fim  # Adiciona o critério "menor ou igual" à data_fim

                # Adiciona o filtro de nome do cliente, se o campo for preenchido
                if nome_cliente:

                    # Usa uma expressão regular (regex) para buscar clientes cujo nome contenha o texto digitado
                    # "$options": "i" torna a busca insensível a letras maiúsculas ou minúsculas
                    query["cliente"] = {"$regex": nome_cliente, "$options": "i"}

                # Consulta os agendamentos no banco de dados
                agendamentos = colecao_agendamentos.find(query)

                # Preenche a Treeview com os dados retornados da consulta no banco de dados
                # O loop percorre todos os agendamentos encontrados
                for agendamento in agendamentos:

                    # Obtém o nome do cliente do agendamento. Se não existir, usa "Desconhecido" como valor padrão
                    cliente = agendamento.get("cliente", "Desconhecido")

                    # Obtém a data do agendamento. Se não existir, usa "N/A" (não disponível) como valor padrão
                    data = agendamento.get("data", "N/A")

                    # Percorre os itens do agendamento (lista de produtos relacionados ao agendamento)
                    for item in agendamento.get("itens", []):

                        # Verifica se o produto atual corresponde ao produto selecionado pelo usuário
                        # `item[0]` contém o ID do produto, que é comparado com o `produto_id` selecionado
                        if item[0] == str(produto_id):

                            # Converte o valor pago para um número de ponto flutuante (float)
                            valor_pago = float(item[2])

                            # Adiciona o valor pago ao total acumulado (somando todos os valores pagos exibidos)
                            total += valor_pago

                            # Insere os dados na Treeview
                            # `insert()` adiciona uma nova linha na tabela
                            # `""` significa que a linha será inserida na raiz (sem hierarquia)
                            # `"end"` adiciona a nova linha no final da tabela
                            # `values=()` define os valores das colunas na ordem especificada ao criar a Treeview
                            tree_vendas.insert(
                                "",
                                "end",
                                values=(
                                    data,  # Data do agendamento
                                    cliente,  # Nome do cliente
                                    item[1],  # Nome do produto
                                    f"R$ {valor_pago:.2f}"  # Valor pago formatado como moeda
                                ),
                            )

                # Atualiza o total no label
                label_total.config(text=f"Total: R$ {total:.2f}")


            # Cria uma nova janela como uma sub-janela (Toplevel) para exibir o histórico de vendas
            # `Toplevel` é usado para criar janelas secundárias na interface Tkinter
            janela_historico = tk.Toplevel(self)

            # Define o título da janela, exibindo "Histórico de Vendas" seguido do nome do produto
            # `produto.get('nome', 'Produto')` tenta obter o nome do produto. Caso não exista,
            #       usa o texto "Produto" como padrão
            janela_historico.title(f"Histórico de Vendas - {produto.get('nome', 'Produto')}")

            # Define o tamanho da janela (largura e altura em pixels)
            largura, altura = 800, 600

            # Obtém a largura total da tela onde a janela será exibida
            largura_tela = self.winfo_screenwidth()

            # Obtém a altura total da tela onde a janela será exibida
            altura_tela = self.winfo_screenheight()

            # Calcula a posição X para centralizar a janela horizontalmente na tela
            # `(largura_tela // 2)` é o meio da tela, subtraindo metade da largura da
            #       janela posiciona ela no centro
            pos_x = (largura_tela // 2) - (largura // 2)

            # Calcula a posição Y para centralizar a janela verticalmente na tela
            # `(altura_tela // 2)` é o meio da tela, subtraindo metade da altura da
            #       janela posiciona ela no centro
            pos_y = (altura_tela // 2) - (altura // 2)

            # Define a geometria da janela (tamanho e posição inicial)
            # O formato é "largura x altura + posição_x + posição_y"
            # Isso garante que a janela seja exibida centralizada na tela
            janela_historico.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

            # Frame de filtros
            # Cria um frame para agrupar os filtros
            # `ttk.Frame` é um contêiner que organiza widgets (elementos da interface) em um espaço delimitado
            # Aqui, ele será usado para organizar os filtros na parte superior da janela
            frame_filtros = ttk.Frame(janela_historico)

            # Exibe o frame na janela histórica, ajustando sua largura para ocupar todo o espaço horizontal
            # `fill="x"` faz com que o frame se expanda horizontalmente para preencher o espaço disponível
            # `padx=10` e `pady=10` adicionam um espaçamento interno de 10 pixels nas
            #       margens horizontal e vertical
            frame_filtros.pack(fill="x", padx=10, pady=10)

            # Adiciona um rótulo (label) ao frame para indicar o campo de "Data Início"
            # `text="Data Início:"` define o texto exibido no rótulo
            # `row=0` e `column=0` posicionam o rótulo na primeira linha e na primeira coluna do grid
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do rótulo
            # `sticky="w"` alinha o texto do rótulo à esquerda (West)
            ttk.Label(frame_filtros, text="Data Início:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

            # Cria um campo de entrada (Entry) para o usuário digitar a data de início
            # `ttk.Entry` é um campo de texto que permite entrada de dados
            # `frame_filtros` define que o campo de entrada será exibido dentro do frame de filtros
            # `width=15` define a largura do campo de entrada como 15 caracteres
            filtro_data_inicio = ttk.Entry(frame_filtros, width=15)

            # Posiciona o campo de entrada na mesma linha que o rótulo, mas na próxima coluna (coluna 1)
            # `row=0` e `column=1` indicam a posição no grid
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do campo de entrada
            filtro_data_inicio.grid(row=0, column=1, padx=5, pady=5)

            # Adiciona um rótulo (label) ao frame de filtros para indicar o campo de "Data Fim"
            # `text="Data Fim:"` define o texto exibido no rótulo
            # `row=0` e `column=2` posicionam o rótulo na primeira linha e na terceira coluna do grid
            # `padx=5` e `pady=5` adicionam um espaçamento interno ao redor do rótulo
            # `sticky="w"` alinha o texto do rótulo à esquerda (West)
            ttk.Label(frame_filtros, text="Data Fim:").grid(row=0, column=2, padx=5, pady=5, sticky="w")

            # Cria um campo de entrada (Entry) para o usuário digitar a data de fim
            # `ttk.Entry` é um widget que permite a entrada de texto pelo usuário
            # `frame_filtros` define que o campo será exibido dentro do frame de filtros
            # `width=15` define a largura do campo de entrada, permitindo até 15 caracteres
            filtro_data_fim = ttk.Entry(frame_filtros, width=15)

            # Posiciona o campo de entrada na mesma linha que o rótulo "Data Fim", mas
            #       na próxima coluna (coluna 3)
            # `row=0` e `column=3` posicionam o campo de entrada na primeira linha e na quarta coluna do grid
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do campo para melhorar a estética
            filtro_data_fim.grid(row=0, column=3, padx=5, pady=5)

            # Adiciona um rótulo (label) ao frame de filtros para indicar o campo de "Cliente"
            # `text="Cliente:"` define o texto exibido no rótulo
            # `row=0` e `column=4` posicionam o rótulo na primeira linha e na quinta coluna do grid
            # `padx=5` e `pady=5` adicionam um espaçamento interno ao redor do rótulo
            # `sticky="w"` alinha o texto do rótulo à esquerda (West)
            ttk.Label(frame_filtros, text="Cliente:").grid(row=0, column=4, padx=5, pady=5, sticky="w")

            # Cria um campo de entrada (Entry) para o usuário digitar o nome do cliente
            # `ttk.Entry` é um widget que permite a entrada de texto pelo usuário
            # `frame_filtros` define que o campo será exibido dentro do frame de filtros
            # `width=20` define a largura do campo de entrada, permitindo até 20 caracteres
            filtro_cliente = ttk.Entry(frame_filtros, width=20)

            # Posiciona o campo de entrada na mesma linha que o rótulo "Cliente",
            #       mas na próxima coluna (coluna 5)
            # `row=0` e `column=5` posicionam o campo de entrada na primeira linha e na sexta coluna do grid
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do campo para melhorar a estética
            filtro_cliente.grid(row=0, column=5, padx=5, pady=5)

            # Cria um botão para aplicar os filtros definidos pelo usuário
            # `ttk.Button` é usado para criar um botão
            # `frame_filtros` define que o botão será exibido dentro do frame de filtros
            # `text="Filtrar"` define o texto exibido no botão
            # `command=carregar_dados` associa o botão à função `carregar_dados`, que será executada ao clicar
            btn_filtrar = ttk.Button(frame_filtros, text="Filtrar", command=carregar_dados)

            # Posiciona o botão no grid
            # `row=0` coloca o botão na mesma linha dos filtros
            # `column=6` coloca o botão na sétima coluna, à direita do campo "Cliente"
            # `padx=10` adiciona espaçamento horizontal ao redor do botão
            # `pady=5` adiciona espaçamento vertical ao redor do botão
            btn_filtrar.grid(row=0, column=6, padx=10, pady=5)

            # Cria um label (rótulo) para exibir o total das vendas filtradas
            # `ttk.Label` é usado para criar o rótulo
            # `janela_historico` define que o rótulo será exibido na janela principal (fora do frame de filtros)
            # `text="Total: R$ 0.00"` define o texto inicial do rótulo, exibindo o valor total como 0.00
            # `font=("Arial", 12, "bold")` define a fonte do texto: Arial, tamanho 12, em negrito
            label_total = ttk.Label(janela_historico, text="Total: R$ 0.00", font=("Arial", 12, "bold"))

            # Posiciona o rótulo para exibição na janela
            # `pack(anchor="e")` posiciona o rótulo no canto direito (east) da janela
            # `padx=10` adiciona um espaçamento horizontal ao redor do rótulo
            # `pady=5` adiciona um espaçamento vertical ao redor do rótulo
            label_total.pack(anchor="e", padx=10, pady=5)

            # Cria um frame para organizar a Treeview (tabela de dados) e a barra de rolagem
            # `ttk.Frame` cria um contêiner para esses widgets
            # `janela_historico` define que o frame será exibido dentro da janela principal
            frame_historico = ttk.Frame(janela_historico)

            # Exibe o frame na janela e faz com que ele preencha o espaço disponível
            # `fill="both"` faz com que o frame se expanda tanto horizontalmente quanto verticalmente
            # `expand=True` permite que o frame ocupe todo o espaço restante disponível
            frame_historico.pack(fill="both", expand=True)

            # Cria uma Treeview para exibir os dados do histórico
            # `ttk.Treeview` é usado para criar uma tabela interativa para exibir dados tabulares
            # `frame_historico` define que a Treeview será exibida dentro do frame destinado à tabela
            # `columns=("data", "cliente", "produto", "valor")` define as colunas da tabela com identificadores
            # `show="headings"` indica que apenas os cabeçalhos das colunas serão exibidos,
            #       sem uma coluna de índice extra
            tree_vendas = ttk.Treeview(
                frame_historico,
                columns=("data", "cliente", "produto", "valor"),
                show="headings",
            )

            # Define o cabeçalho para a coluna "data"
            # O texto exibido no cabeçalho será "Data"
            tree_vendas.heading("data", text="Data")

            # Define o cabeçalho para a coluna "cliente"
            # O texto exibido no cabeçalho será "Cliente"
            tree_vendas.heading("cliente", text="Cliente")

            # Define o cabeçalho para a coluna "produto"
            # O texto exibido no cabeçalho será "Produto"
            tree_vendas.heading("produto", text="Produto")

            # Define o cabeçalho para a coluna "valor"
            # O texto exibido no cabeçalho será "Valor Pago"
            tree_vendas.heading("valor", text="Valor Pago")

            # Configura o layout da Treeview para exibição
            # `pack()` posiciona o widget na interface
            # `side="left"` posiciona a tabela à esquerda dentro do frame
            # `fill="both"` faz com que a tabela preencha todo o espaço disponível horizontal e verticalmente
            # `expand=True` permite que a tabela se expanda se o tamanho da janela for alterado
            tree_vendas.pack(side="left", fill="both", expand=True)

            # Configura a barra de rolagem
            scrollbar = ttk.Scrollbar(frame_historico, orient="vertical", command=tree_vendas.yview)
            tree_vendas.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Carrega os dados inicialmente
            carregar_dados()

        # Trata a exceção IndexError
        # Isso acontece quando o usuário tenta abrir o histórico sem selecionar um produto na Treeview
        except IndexError:

            # Exibe uma mensagem de erro para o usuário informando que nenhum produto foi selecionado
            # `messagebox.showerror()` cria uma caixa de diálogo de erro com o título "Erro" e
            #       uma mensagem explicativa
            messagebox.showerror("Erro", "Nenhum produto selecionado.")

        # Trata qualquer outra exceção genérica que possa ocorrer no código
        # O nome da exceção será armazenado na variável `e`
        except Exception as e:

            # Exibe uma mensagem de erro genérica informando que houve um problema ao abrir o histórico
            # A mensagem inclui o texto da exceção (`f"Erro ao abrir histórico: {e}"`), útil para depuração
            messagebox.showerror("Erro", f"Erro ao abrir histórico: {e}")



    def carregar_produtos(self):

        # Remove todos os itens existentes na Treeview `self.tree`.
        # Isso é necessário para garantir que os dados não
        #       sejam duplicados ao recarregar.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Itera sobre os produtos encontrados na coleção `colecao_produtos`.
        # Os produtos são ordenados pelo campo `nome` em ordem crescente.
        for p in colecao_produtos.find().sort("nome", pymongo.ASCENDING):

            # Extrai o ID do produto como uma string para uso
            #       como identificador na Treeview.
            _id = str(p["_id"])

            # Obtém o nome do produto. Caso não exista, define como uma string vazia.
            nome = p.get("nome", "")

            # Obtém a marca do produto. Caso não exista, define como uma string vazia.
            marca = p.get("marca", "")

            # Obtém a quantidade disponível no estoque. Caso não exista, define como 0.
            quantidade = p.get("quantidade", 0)

            # Obtém o preço de compra do produto. Caso não exista, define como 0.0.
            preco_compra = p.get("preco_compra", 0.0)

            # Obtém o preço de venda do produto. Caso não exista, define como 0.0.
            preco_venda = p.get("preco_venda", 0.0)

            # Obtém a categoria do produto. Caso não exista,
            #       define como uma string vazia.
            categoria = p.get("categoria", "")

            # Insere o produto na Treeview `self.tree`.
            # Os valores a serem exibidos nas colunas são
            #       fornecidos pela tupla `values`.
            # O `iid` é o identificador exclusivo para o item, baseado
            #       no `_id` do produto no banco de dados.
            novo_id = self.tree.insert(
                "",
                "end",  # Insere o item no final da Treeview.
                iid=_id,  # Identificador exclusivo do item.
                values=(nome, marca, quantidade, preco_compra, preco_venda, categoria)  # Valores exibidos nas colunas.
            )

            # Verifica se o estoque do produto é inferior a 5 unidades.
            # Caso seja, adiciona a tag "estoque_baixo" ao item para estilização.
            if quantidade < 5:
                self.tree.item(novo_id, tags=("estoque_baixo",))



    # Define o método para selecionar um item na TreeView.
    # `event` é o evento que dispara o método, mas é opcional e
    #       pode não ser usado diretamente.
    def selecionar_item_tree(self, event=None):

        try:

            # Obtém o identificador do item selecionado na TreeView.
            # `self.tree.selection()` retorna uma lista de IDs selecionados.
            # `[0]` pega o primeiro item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Se nenhum item estiver selecionado, `selection()[0]` causará um erro.
            # Nesse caso, o método retorna sem fazer nada.
            return

        # Busca no banco de dados o documento do produto com o ID selecionado.
        # `ObjectId(selecionado)` converte o ID da TreeView para um
        #       formato que o MongoDB entende.
        # O método `find_one` retorna o primeiro documento que corresponde ao filtro.
        p = colecao_produtos.find_one({"_id": ObjectId(selecionado)})

        # Verifica se o produto foi encontrado no banco de dados.
        if p:

            # Limpa o campo de entrada de "Nome do Produto" antes de
            #       inserir o novo valor.
            self.nome_entry.delete(0, "end")

            # Insere o valor do campo "nome" do produto no campo de entrada.
            self.nome_entry.insert(0, p.get("nome", ""))

            # Limpa o campo de entrada de "Marca" antes de inserir o novo valor.
            self.marca_entry.delete(0, "end")

            # Insere o valor do campo "marca" do produto no campo de entrada.
            self.marca_entry.insert(0, p.get("marca", ""))

            # Limpa o campo de entrada de "Quantidade" antes de inserir o novo valor.
            self.quantidade_entry.delete(0, "end")

            # Insere o valor do campo "quantidade" do produto no campo de entrada.
            self.quantidade_entry.insert(0, str(p.get("quantidade", 0)))

            # Limpa o campo de entrada de "Preço de Compra" antes de inserir o novo valor.
            self.preco_compra_entry.delete(0, "end")

            # Insere o valor do campo "preco_compra" do produto no campo de entrada.
            self.preco_compra_entry.insert(0, str(p.get("preco_compra", 0.0)))

            # Limpa o campo de entrada de "Preço de Venda" antes de inserir o novo valor.
            self.preco_venda_entry.delete(0, "end")

            # Insere o valor do campo "preco_venda" do produto no campo de entrada.
            self.preco_venda_entry.insert(0, str(p.get("preco_venda", 0.0)))

            # Define o valor da combo box "Categoria" com base no
            #       campo "categoria" do produto.
            self.categoria_combo.set(p.get("categoria", ""))


    # Define o método `novo_produto`, responsável por adicionar um
    #       novo produto ao banco de dados.
    def novo_produto(self):

        # Obtém o valor do campo de entrada para o nome do
        #       produto e remove espaços extras.
        nome = self.nome_entry.get().strip()

        # Obtém o valor do campo de entrada para a marca do
        #       produto e remove espaços extras.
        marca = self.marca_entry.get().strip()

        # Obtém o valor do campo de entrada para a quantidade do
        #       produto e remove espaços extras.
        quantidade = self.quantidade_entry.get().strip()

        # Obtém o valor do campo de entrada para o preço de compra do
        #       produto e remove espaços extras.
        preco_compra = self.preco_compra_entry.get().strip()

        # Obtém o valor do campo de entrada para o preço de venda do
        #       produto e remove espaços extras.
        preco_venda = self.preco_venda_entry.get().strip()

        # Obtém o valor selecionado na lista de categorias e remove espaços extras.
        categoria = self.categoria_combo.get().strip()

        # Verifica se o nome e a quantidade foram preenchidos, pois são obrigatórios.
        if not nome or not quantidade:

            # Exibe uma mensagem de erro se o nome ou a quantidade estiverem em branco.
            messagebox.showerror("Erro", "Nome e Quantidade são obrigatórios.")
            return

        try:

            # Tenta converter a quantidade para um número inteiro.
            quantidade = int(quantidade)

            # Tenta converter o preço de compra para um número decimal.
            # Se o campo estiver vazio, define como 0.0.
            preco_compra = float(preco_compra) if preco_compra else 0.0

            # Tenta converter o preço de venda para um número decimal.
            # Se o campo estiver vazio, define como 0.0.
            preco_venda = float(preco_venda) if preco_venda else 0.0

        # Captura qualquer erro de conversão de valores (se os
        #       campos não forem numéricos).
        except ValueError:

            # Exibe uma mensagem de erro informando que os valores
            #       devem ser numéricos.
            messagebox.showerror("Erro",
                                 "Quantidade e preços devem ser valores numéricos.")
            return

        # Cria um dicionário contendo as informações do novo produto.
        novo = {
            "nome": nome,  # Nome do produto.
            "marca": marca,  # Marca do produto.
            "quantidade": quantidade,  # Quantidade disponível em estoque.
            "preco_compra": preco_compra,  # Preço de compra do produto.
            "preco_venda": preco_venda,  # Preço de venda do produto.
            "categoria": categoria  # Categoria do produto.
        }

        # Insere o novo produto na coleção do banco de dados.
        colecao_produtos.insert_one(novo)

        # Atualiza a TreeView carregando todos os produtos novamente.
        self.carregar_produtos()

        # Limpa os campos do formulário para entrada de novos dados.
        self.limpar_campos()

        # Exibe uma mensagem de sucesso para informar que o produto foi adicionado.
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")



    # Define o método `limpar_campos`, responsável por limpar
    #       todos os campos do formulário de entrada.
    def limpar_campos(self):

        # Limpa o campo de entrada de texto para o nome do produto.
        self.nome_entry.delete(0, "end")

        # Limpa o campo de entrada de texto para a marca do produto.
        self.marca_entry.delete(0, "end")

        # Limpa o campo de entrada de texto para a quantidade do produto.
        self.quantidade_entry.delete(0, "end")

        # Limpa o campo de entrada de texto para o preço de compra do produto.
        self.preco_compra_entry.delete(0, "end")

        # Limpa o campo de entrada de texto para o preço de venda do produto.
        self.preco_venda_entry.delete(0, "end")

        # Reseta o campo de seleção da categoria para o estado inicial.
        self.categoria_combo.set("")



    def editar_produto(self):

        # Tenta obter o item selecionado na TreeView.
        try:

            # Obtém o ID do item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Caso nenhum item esteja selecionado, exibe uma mensagem de erro.
            messagebox.showerror("Erro", "Nenhum produto selecionado.")

            # Sai do método se não houver seleção.
            return

        # Obtém o nome do produto a partir do campo de entrada,
        #       removendo espaços extras nas extremidades.
        nome = self.nome_entry.get().strip()

        # Obtém a marca do produto a partir do campo de entrada,
        #       removendo espaços extras nas extremidades.
        marca = self.marca_entry.get().strip()

        # Obtém a quantidade do produto a partir do campo de entrada,
        #       removendo espaços extras nas extremidades.
        quantidade = self.quantidade_entry.get().strip()

        # Obtém o preço de compra do produto a partir do campo de entrada,
        #       removendo espaços extras nas extremidades.
        preco_compra = self.preco_compra_entry.get().strip()

        # Obtém o preço de venda do produto a partir do campo de entrada,
        #       removendo espaços extras nas extremidades.
        preco_venda = self.preco_venda_entry.get().strip()

        # Obtém a categoria do produto selecionada no campo de
        #       seleção (Combobox), removendo espaços extras.
        categoria = self.categoria_combo.get().strip()

        # Verifica se os campos "nome" e "quantidade" foram preenchidos.
        if not nome or not quantidade:

            # Exibe uma mensagem de erro se os campos obrigatórios estiverem vazios.
            messagebox.showerror("Erro",
                                 "Nome e Quantidade são obrigatórios.")

            # Sai do método sem continuar a execução se os campos
            #       obrigatórios estiverem ausentes.
            return

        try:

            # Tenta converter a quantidade para um número inteiro.
            # Se a conversão falhar, será lançada uma exceção ValueError.
            quantidade = int(quantidade)

            # Tenta converter o preço de compra para um número float.
            # Caso o campo esteja vazio, define o valor como 0.0.
            preco_compra = float(preco_compra) if preco_compra else 0.0

            # Tenta converter o preço de venda para um número float.
            # Caso o campo esteja vazio, define o valor como 0.0.
            preco_venda = float(preco_venda) if preco_venda else 0.0

        except ValueError:

            # Exibe uma mensagem de erro se a conversão de "quantidade",
            #       "preco_compra" ou "preco_venda" falhar.
            messagebox.showerror("Erro",
                                 "Quantidade e preços devem ser numéricos.")

            # Sai do método sem continuar a execução se ocorrer uma exceção.
            return

        # Atualiza o documento na coleção de produtos do banco de dados MongoDB.
        # A pesquisa é feita pelo campo "_id", utilizando o ID do produto selecionado.
        # O operador "$set" atualiza apenas os campos especificados,
        #       mantendo os demais inalterados.
        colecao_produtos.update_one(
            {"_id": ObjectId(selecionado)},  # Filtro para encontrar o produto pelo ID.
            {
                "$set": {  # Define os novos valores para os campos especificados.
                    "nome": nome,  # Atualiza o nome do produto.
                    "marca": marca,  # Atualiza a marca do produto.
                    "quantidade": quantidade,  # Atualiza a quantidade em estoque.
                    "preco_compra": preco_compra,  # Atualiza o preço de compra.
                    "preco_venda": preco_venda,  # Atualiza o preço de venda.
                    "categoria": categoria  # Atualiza a categoria do produto.
                }
            }
        )

        # Recarrega a lista de produtos para refletir as
        #       alterações feitas no banco de dados.
        self.carregar_produtos()

        # Limpa os campos de entrada para que fiquem prontos para novos dados.
        self.limpar_campos()

        # Exibe uma mensagem informando que o produto foi editado com sucesso.
        messagebox.showinfo("Sucesso", "Produto editado com sucesso.")



    # Define o método para excluir um produto selecionado na interface.
    def excluir_produto(self):

        try:

            # Tenta obter o ID do item selecionado na Treeview.
            # Pega o primeiro item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Caso nenhum item esteja selecionado, exibe uma mensagem de erro.
            messagebox.showerror("Erro", "Nenhum produto selecionado.")

            # Sai do método sem fazer nada.
            return

        # Exibe uma mensagem de confirmação ao usuário perguntando se
        #       deseja realmente excluir o produto.
        resposta = messagebox.askyesno("Confirmar",
                                       "Deseja realmente excluir este produto?")

        # Verifica se o usuário clicou em "Sim".
        if resposta:

            # Remove o documento do banco de dados correspondente
            #       ao ID do item selecionado.
            colecao_produtos.delete_one({"_id": ObjectId(selecionado)})

            # Atualiza a lista de produtos exibida na interface.
            self.carregar_produtos()

            # Limpa os campos de entrada para evitar inconsistências.
            self.limpar_campos()

            # Informa o usuário que o produto foi excluído com sucesso.
            messagebox.showinfo("Sucesso",
                                "Produto excluído com sucesso.")



    # Define o método para adicionar estoque a um produto selecionado.
    def adicionar_estoque(self):

        # Tenta obter o item selecionado na Treeview.
        try:
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe um erro caso nenhum item tenha sido selecionado.
            messagebox.showerror("Erro",
                                 "Nenhum produto selecionado.")
            return

        # Solicita ao usuário a quantidade a adicionar por
        #       meio de uma caixa de diálogo.
        adicionar = simpledialog.askinteger("Adicionar Estoque",
                                            "Quantidade a adicionar:")

        # Verifica se o valor informado é inválido (None ou menor/igual a zero).
        if adicionar is None or adicionar <= 0:

            # Retorna sem fazer nada caso o valor seja inválido.
            return

        # Busca o documento correspondente ao produto no banco de
        #       dados usando o ID selecionado.
        # O método `find_one` retorna o documento que corresponde ao filtro.
        produto = colecao_produtos.find_one({"_id": ObjectId(selecionado)})

        # Calcula a nova quantidade do produto somando a quantidade
        #       atual à quantidade adicionada.
        # `produto["quantidade"]` é o valor atual no banco de dados.
        nova_quantidade = produto["quantidade"] + adicionar

        # Atualiza o documento do produto no banco de dados para refletir a nova quantidade.
        # Usa o método `update_one` com `$set` para modificar apenas o campo `quantidade`.
        colecao_produtos.update_one({"_id": ObjectId(selecionado)},  # Filtro: identifica o produto pelo seu ID.
                                    {"$set": {
                                        "quantidade": nova_quantidade}})  # Define o novo valor para `quantidade`.

        # Exibe uma mensagem de sucesso para o usuário indicando a
        #       nova quantidade no estoque.
        messagebox.showinfo("Sucesso",
                            f"Estoque atualizado. Nova quantidade: {nova_quantidade}")

        # Recarrega a lista de produtos na interface para
        #       refletir as alterações feitas.
        self.carregar_produtos()



# ------------------------------------------------------------
# Tela de Serviços
# ------------------------------------------------------------

# Define a classe `TelaServicos`, que herda de `ttk.Frame`.
# Esta classe será usada para criar a interface gráfica da tela de serviços.
class TelaServicos(ttk.Frame):

    # Documentação da classe, explicando seu propósito e campos.

    """
    Tela de cadastro/gerenciamento de serviços.
    Cada serviço terá: nome, descrição, preço e quantidade (para
            controle de "estoque" ou capacidade).
    """

    # Método construtor da classe, com `self` referenciando a instância da classe,
    #       e `parent` sendo o widget pai no qual esse frame será colocado.
    def __init__(self, parent):

        # Chama o construtor da classe pai `ttk.Frame`.
        super().__init__(parent)

        # Cria e configura um widget `Label` para ser o título da tela de serviços.
        # `text` define o texto exibido, e `font` define a fonte do texto.
        titulo_label = ttk.Label(self, text="Serviços", font=("Arial", 14, "bold"))

        # Posiciona o `titulo_label` na tela usando o método `pack`, que é
        #       um gerenciador de geometria.
        # `side='top'` posiciona o widget no topo do frame.
        # `anchor='w'` ancora o widget à esquerda dentro do espaço disponível.
        # `padx` e `pady` adicionam padding no eixo x e y, respectivamente.
        titulo_label.pack(side="top",
                          anchor="w",
                          padx=10,
                          pady=10)

        # Cria um frame para conter os campos de entrada, utilizando a
        #       classe `Frame` do módulo `ttk`.
        # `padding=10` adiciona uma margem interna de 10 pixels ao redor
        #       dos elementos dentro do frame.
        campos_frame = ttk.Frame(self, padding=10)

        # Posiciona o `campos_frame` usando o método `pack`, que é um gerenciador de geometria.
        # `side="top"` coloca o frame no topo do widget pai.
        # `fill="x"` faz com que o frame se expanda horizontalmente para
        #       preencher o espaço disponível.
        campos_frame.pack(side="top", fill="x")

        # Cria um widget `Label` dentro do `campos_frame` para identificar o
        #       campo de entrada do nome do serviço.
        # `text="Nome do Serviço:"` define o texto que aparecerá ao
        #       lado do campo de entrada.
        # `.grid(row=0, column=0, padx=5, pady=5, sticky="w")` posiciona o label na
        #       primeira linha e primeira coluna,
        #       com um padding de 5 pixels em todas as direções e alinhado à
        #       esquerda (`sticky="w"`).
        ttk.Label(campos_frame,
                  text="Nome do Serviço:").grid(row=0,
                                                column=0,
                                                padx=5,
                                                pady=5,
                                                sticky="w")

        # Cria um widget `Entry` para entrada de texto, permitindo ao usuário
        #       digitar o nome do serviço.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        self.nome_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o `nome_entry` usando o método `grid`, que permite um
        #       posicionamento mais preciso dentro do `campos_frame`.
        # `row=0, column=1` coloca o campo de entrada na primeira linha e
        #       segunda coluna, alinhado com o label acima.
        # `padx=5, pady=5` adiciona um padding de 5 pixels ao redor do
        #       campo de entrada para espaçamento.
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Descrição".
        # `text="Descrição:"` define o texto exibido no rótulo.
        # `campos_frame` é o frame pai onde o rótulo será colocado.
        # Posiciona o rótulo no grid layout do frame, na linha 1 e coluna 0.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical.
        # `sticky="w"` alinha o rótulo à esquerda da célula.
        ttk.Label(campos_frame,
                  text="Descrição:").grid(row=1,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky="w")

        # Cria uma entrada de texto para o campo "Descrição".
        # `width=30` define a largura da entrada de texto.
        self.descricao_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona a entrada no grid layout do frame.
        # `row=1` define que o elemento será posicionado na linha 1.
        # `column=1` define que o elemento será posicionado na coluna 1.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do elemento.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do elemento.
        self.descricao_entry.grid(row=1, column=1, padx=5, pady=5)

        # Adiciona um rótulo ao frame `campos_frame` para indicar o
        #       campo de "Quantidade (Estoque)".
        # `text="Quantidade (Estoque):"` define o texto exibido no rótulo.
        # `grid(row=2, column=0, padx=5, pady=5, sticky="w")` posiciona o
        #       rótulo na linha 2, coluna 0.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical.
        # `sticky="w"` alinha o texto do rótulo à esquerda (West).
        ttk.Label(campos_frame,
                  text="Quantidade (Estoque):").grid(row=2,
                                                     column=0,
                                                     padx=5,
                                                     pady=5,
                                                     sticky="w")

        # Adiciona um campo de entrada para inserir a quantidade ou o estoque do serviço.
        # `width=10` define a largura do campo de entrada.
        self.quantidade_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada no frame `campos_frame`.
        # `grid(row=2, column=1, padx=5, pady=5, sticky="w")` posiciona o
        #       campo na linha 2, coluna 1.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical.
        # `sticky="w"` alinha o campo de entrada à esquerda.
        self.quantidade_entry.grid(row=2,
                                   column=1,
                                   padx=5,
                                   pady=5,
                                   sticky="w")

        # Adiciona um rótulo ao frame `campos_frame` para indicar o campo de "Preço (R$)".
        # `text="Preço (R$):"` define o texto exibido no rótulo.
        # `grid(row=3, column=0, padx=5, pady=5, sticky="w")` posiciona o
        #       rótulo na linha 3, coluna 0.
        # `padx=5` adiciona espaçamento horizontal ao redor do rótulo.
        # `pady=5` adiciona espaçamento vertical ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda.
        ttk.Label(campos_frame,
                  text="Preço (R$):").grid(row=3,
                                           column=0,
                                           padx=5,
                                           pady=5,
                                           sticky="w")

        # Cria um campo de entrada para inserir o preço do serviço.
        # `width=10` define a largura do campo de entrada.
        self.preco_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada no frame `campos_frame`.
        # `grid(row=3, column=1, padx=5, pady=5, sticky="w")` posiciona o
        #       campo na linha 3, coluna 1.
        # `padx=5` adiciona espaçamento horizontal ao redor do campo de entrada.
        # `pady=5` adiciona espaçamento vertical ao redor do campo de entrada.
        # `sticky="w"` alinha o campo de entrada à esquerda.
        self.preco_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Cria um frame para os botões dentro do frame `campos_frame`.
        # Isso permite agrupar os botões em uma área específica.
        botoes_frame = ttk.Frame(campos_frame)

        # Posiciona o frame dos botões no grid layout do `campos_frame`.
        # `row=4` posiciona o frame na linha 4.
        # `column=0` posiciona o frame na primeira coluna.
        # `columnspan=2` faz com que o frame ocupe duas colunas.
        # `pady=10` adiciona espaçamento vertical acima e abaixo do frame.
        botoes_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Cria o botão "Adicionar" dentro do frame dos botões.
        # `text="Adicionar"` define o texto exibido no botão.
        # `command=self.novo_servico` associa a função `novo_servico` ao clique do botão.
        # O botão é posicionado usando o método `pack`:
        # `side="left"` alinha o botão ao lado esquerdo do frame.
        # `padx=5` adiciona espaçamento horizontal entre os botões.
        ttk.Button(botoes_frame,
                   text="Adicionar",
                   command=self.novo_servico).pack(side="left",
                                                   padx=5)

        # Cria o botão "Editar" dentro do frame dos botões.
        # `text="Editar"` define o texto exibido no botão.
        # `command=self.editar_servico` associa a função
        #       `editar_servico` ao clique do botão.
        # O botão é posicionado ao lado do botão "Adicionar".
        ttk.Button(botoes_frame,
                   text="Editar",
                   command=self.editar_servico).pack(side="left",
                                                     padx=5)

        # Cria o botão "Excluir" dentro do frame dos botões.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir_servico` associa a função
        #       `excluir_servico` ao clique do botão.
        # O botão é posicionado ao lado do botão "Editar".
        ttk.Button(botoes_frame,
                   text="Excluir",
                   command=self.excluir_servico).pack(side="left",
                                                      padx=5)

        # Cria um frame para conter a Treeview.
        # `self` refere-se ao frame pai onde este frame será inserido.
        # `table_frame` será usado para posicionar a tabela de exibição dos dados.
        table_frame = ttk.Frame(self)

        # Posiciona o `table_frame` no layout.
        # `side="top"` alinha o frame ao topo do frame pai.
        # `fill="both"` faz com que o frame preencha tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame cresça proporcionalmente ao
        #       redimensionamento do frame pai.
        # `padx=10` adiciona espaçamento horizontal ao redor do frame.
        # `pady=10` adiciona espaçamento vertical ao redor do frame.
        table_frame.pack(side="top",
                         fill="both",
                         expand=True,
                         padx=10,
                         pady=10)

        # Cria uma Treeview para exibir os dados.
        # `table_frame` é o frame pai onde a Treeview será posicionada.
        # `self.tree` será o objeto Treeview que armazenará e exibirá os dados.
        self.tree = ttk.Treeview(

            # Define o frame pai onde a Treeview será inserida.
            table_frame,

            # Define as colunas da Treeview.
            # Cada valor na tupla corresponde a uma coluna
            #       identificada por um nome único.
            columns=("nome", "descricao", "quantidade", "preco"),

            # Define que apenas os cabeçalhos serão exibidos,
            #       sem uma coluna de índice padrão.
            show="headings"

        )

        # Define o cabeçalho da coluna "nome".
        # O texto exibido será "Nome".
        self.tree.heading("nome", text="Nome")

        # Define o cabeçalho da coluna "descricao".
        # O texto exibido será "Descrição".
        self.tree.heading("descricao", text="Descrição")

        # Define o cabeçalho da coluna "quantidade".
        # O texto exibido será "Qtd".
        self.tree.heading("quantidade", text="Qtd")

        # Define o cabeçalho da coluna "preco".
        # O texto exibido será "Preço".
        self.tree.heading("preco", text="Preço")

        # Cria uma barra de rolagem vertical para a Treeview.
        # `orient="vertical"` define a orientação vertical.
        # `command=self.tree.yview` conecta a barra de rolagem ao
        #       movimento vertical da Treeview.
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient="vertical",
                                  command=self.tree.yview)

        # Configura a Treeview para usar a barra de rolagem.
        # `yscroll=scrollbar.set` conecta o movimento da barra à Treeview.
        self.tree.configure(yscroll=scrollbar.set)

        # Posiciona a Treeview no frame.
        # `side="left"` posiciona a Treeview à esquerda do frame.
        # `fill="both"` permite que a Treeview preencha a largura e altura disponíveis.
        # `expand=True` faz a Treeview expandir quando o frame for redimensionado.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem no frame.
        # `side="left"` alinha a barra de rolagem à esquerda da Treeview.
        # `fill="y"` faz com que a barra preencha toda a altura disponível.
        scrollbar.pack(side="left", fill="y")

        # Configura uma tag para destacar visualmente as linhas com estoque baixo.
        # A tag "estoque_baixo" define o fundo das linhas como vermelho
        #       claro (`background="#ff9999"`).
        self.tree.tag_configure("estoque_baixo", background="#ff9999")

        # Associa um evento à Treeview para capturar a seleção de um item.
        # `"<<TreeviewSelect>>"` é acionado quando uma linha é selecionada.
        # `self.selecionar_item_tree` é o método que será chamado ao selecionar um item.
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_tree)

        # Associa um evento de clique duplo à Treeview

        # `self.tree.bind("<Double-1>", self.abrir_historico_servicos)`
        # - `self.tree`: É o widget Treeview onde os dados dos serviços estão exibidos.
        # - `bind`: Método usado para associar um evento a uma função.
        # - `"<Double-1>"`: Representa o evento de clique duplo com o botão esquerdo do mouse:
        #   - `"Double"` indica o clique duplo.
        #   - `"1"` representa o botão esquerdo do mouse.
        # - `self.abrir_historico_servicos`: É a função que será chamada sempre que o evento de clique duplo ocorrer.
        self.tree.bind("<Double-1>", self.abrir_historico_servicos)

        # Carrega os serviços na Treeview.
        # Este método adiciona os dados à Treeview ao iniciar a aplicação.
        self.carregar_servicos()

    def abrir_historico_servicos(self, event):

        """
        Função que abre uma janela com o histórico de serviços de um serviço selecionado.
        É acionada quando um evento (como um clique duplo) ocorre na Treeview.
        """

        try:

            # Obtém o ID do item selecionado na Treeview
            # `self.tree.selection()` retorna uma lista de itens selecionados na Treeview.
            # `[0]` pega o primeiro item selecionado (supondo que apenas um item está selecionado).
            item_selecionado = self.tree.selection()[0]

            # Converte o ID do item selecionado em um ObjectId.
            # `ObjectId` é usado pelo MongoDB para identificar documentos de forma única.
            # Ele converte o identificador de string para o formato esperado pelo banco de dados.
            servico_id = ObjectId(item_selecionado)

            # Função para carregar os dados na Treeview com base nos filtros aplicados
            def carregar_dados():

                # Limpa todos os itens atualmente exibidos na Treeview
                # `tree_servicos.get_children()` retorna uma lista de todos os IDs dos itens na Treeview.
                # O loop percorre cada ID e remove os itens um por um usando `tree_servicos.delete(item)`.
                for item in tree_servicos.get_children():
                    tree_servicos.delete(item)

                # Inicializa a variável `total` com o valor 0.
                # Essa variável será usada para acumular os valores dos serviços exibidos.
                total = 0

                # Obtém o valor digitado no campo de entrada para a data inicial.
                # `filtro_data_inicio.get()` obtém o texto do campo de entrada.
                # `.strip()` remove espaços em branco no início e no final do texto.
                data_inicio = filtro_data_inicio.get().strip()

                # Obtém o valor digitado no campo de entrada para a data final.
                # Segue o mesmo processo da data inicial: obtém o texto e remove espaços extras.
                data_fim = filtro_data_fim.get().strip()

                # Obtém o valor digitado no campo de entrada para o nome do cliente.
                # `.lower()` converte o texto para letras minúsculas para que a busca
                #       não seja sensível a maiúsculas/minúsculas.
                nome_cliente = filtro_cliente.get().strip().lower()

                # Define a consulta inicial (query) para buscar os agendamentos no banco de dados
                query = {

                    # Apenas registros com o status "Finalizado".
                    "status": "Finalizado",

                    # Verifica se o ID do serviço corresponde ao `servico_id` e se o tipo é "servico".
                    # "$elemMatch" busca um elemento na lista `itens` que atende a ambas as condições:
                    # - O ID do serviço (campo "0") deve ser igual ao `servico_id`.
                    # - O tipo do item (campo "3") deve ser "servico".
                    "itens": {"$elemMatch": {"0": str(servico_id), "3": "servico"}},

                }

                # Adiciona o filtro de data inicial, se preenchido
                if data_inicio:

                    # Se o campo de data inicial foi preenchido, adiciona uma condição para buscar registros
                    # cuja data seja maior ou igual à data informada (`$gte` = "greater than or equal").
                    query["data"] = {"$gte": data_inicio}

                # Adiciona o filtro de data final, se preenchido
                if data_fim:

                    # Verifica se já existe uma condição de data na query.
                    # Se não existir, adiciona um dicionário vazio para o campo "data".
                    query["data"] = query.get("data", {})

                    # Adiciona uma condição para buscar registros cuja data seja menor ou
                    #       igual à data final fornecida.
                    # "$lte" significa "less than or equal" (menor ou igual).
                    query["data"]["$lte"] = data_fim

                # Adiciona o filtro de nome do cliente, se preenchido
                if nome_cliente:

                    # Adiciona uma condição para buscar registros onde o nome do
                    #       cliente contenha o texto fornecido.
                    # "$regex" permite fazer buscas parciais, como "contém".
                    # "$options": "i" torna a busca insensível a maiúsculas ou minúsculas.
                    query["cliente"] = {"$regex": nome_cliente, "$options": "i"}

                # Consulta os agendamentos no banco de dados
                # `colecao_agendamentos.find(query)` executa a consulta no MongoDB com
                #       os critérios definidos na query.
                # Retorna todos os documentos que atendem às condições especificadas.
                agendamentos = colecao_agendamentos.find(query)

                # Preenche a Treeview com os dados retornados da consulta
                for agendamento in agendamentos:

                    # Obtém o nome do cliente do agendamento. Se não houver, usa "Desconhecido" como valor padrão.
                    cliente = agendamento.get("cliente", "Desconhecido")

                    # Obtém a data do agendamento. Se não houver, usa "N/A" como valor padrão.
                    data = agendamento.get("data", "N/A")

                    # Percorre os itens do agendamento para encontrar os serviços
                    # `agendamento.get("itens", [])` obtém a lista de itens do agendamento.
                    # Se não houver itens, retorna uma lista vazia como valor padrão.
                    for item in agendamento.get("itens", []):

                        # Verifica se o ID do serviço corresponde ao `servico_id` e se o tipo é "servico".
                        if item[0] == str(servico_id) and item[3] == "servico":

                            # Converte o valor do serviço para float (garantindo que seja um número).
                            valor_pago = float(item[2])

                            # Adiciona o valor do serviço ao total acumulado.
                            total += valor_pago

                            # Insere os dados do serviço na Treeview
                            # `insert()` adiciona uma nova linha na tabela.
                            # O primeiro argumento `""` indica que a linha será adicionada
                            #       na raiz (sem hierarquia).
                            # `"end"` insere a nova linha no final da tabela.
                            # `values=()` define os valores a serem exibidos nas colunas da Treeview.
                            tree_servicos.insert(
                                "",
                                "end",
                                values=(
                                    data,  # Data do agendamento (coluna "Data").
                                    cliente,  # Nome do cliente (coluna "Cliente").
                                    item[1],  # Nome do serviço (coluna "Serviço").
                                    f"R$ {valor_pago:.2f}"  # Valor pago formatado como moeda (coluna "Valor Pago").
                                ),
                            )

                # Atualiza o total no label
                # O `label_total` exibe o total acumulado dos serviços mostrados na Treeview.
                # O texto é atualizado com o valor formatado em moeda (duas casas decimais).
                label_total.config(text=f"Total: R$ {total:.2f}")


            # Cria a janela para exibir o histórico de serviços
            # `tk.Toplevel(self)` cria uma nova janela independente (sub-janela) a partir da janela principal.
            # Essa sub-janela pode ser usada para exibir informações adicionais.
            janela_historico = tk.Toplevel(self)

            # Define o título da janela para exibição no cabeçalho da sub-janela.
            # Nesse caso, o título será "Histórico de Serviços".
            janela_historico.title("Histórico de Serviços")

            # Centraliza a janela na tela

            # Define a largura e a altura da janela.
            # Aqui, a largura é definida como 800 pixels e a altura como 600 pixels.
            largura, altura = 800, 600

            # Obtém a largura total da tela do monitor onde o programa está sendo executado.
            # `self.winfo_screenwidth()` retorna a largura total da tela em pixels.
            largura_tela = self.winfo_screenwidth()

            # Obtém a altura total da tela do monitor onde o programa está sendo executado.
            # `self.winfo_screenheight()` retorna a altura total da tela em pixels.
            altura_tela = self.winfo_screenheight()

            # Calcula a posição X para centralizar a janela horizontalmente.
            # Divide a largura total da tela por 2 (para encontrar o centro) e subtrai metade da largura da janela.
            pos_x = (largura_tela // 2) - (largura // 2)

            # Calcula a posição Y para centralizar a janela verticalmente.
            # Divide a altura total da tela por 2 (para encontrar o centro) e subtrai metade da altura da janela.
            pos_y = (altura_tela // 2) - (altura // 2)

            # Define a geometria da janela, especificando largura, altura e posição inicial.
            # O formato utilizado é: "largura x altura + posição_x + posição_y".
            # Isso garante que a janela será exibida centralizada na tela.
            janela_historico.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

            # Frame de filtros
            # Cria um container (frame) para organizar os campos de filtro.
            # `ttk.Frame` é um widget do Tkinter usado para agrupar outros elementos em uma área delimitada.
            # Aqui, o frame será usado para organizar os campos de entrada e rótulos (labels) de filtro.
            frame_filtros = ttk.Frame(janela_historico)

            # Posiciona o frame na sub-janela (`janela_historico`) utilizando o método `pack`.
            # `fill="x"` faz com que o frame ocupe toda a largura disponível na sub-janela.
            # `padx=10` e `pady=10` adicionam um espaçamento interno de 10 pixels nas bordas horizontal e vertical.
            frame_filtros.pack(fill="x", padx=10, pady=10)

            # Campo para filtro de data inicial

            # Cria um rótulo (label) para identificar o campo "Data Início".
            # `text="Data Início:"` define o texto exibido no rótulo.
            # `frame_filtros` define que o rótulo será exibido dentro do frame de filtros.
            # `grid(row=0, column=0)` posiciona o rótulo na primeira linha (linha 0) e na primeira coluna (coluna 0).
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do rótulo.
            # `sticky="w"` alinha o texto do rótulo à esquerda (West).
            ttk.Label(frame_filtros, text="Data Início:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

            # Cria um campo de entrada (Entry) para que o usuário digite a data inicial.
            # `ttk.Entry` é um widget que permite entrada de texto pelo usuário.
            # `frame_filtros` define que o campo será exibido dentro do frame de filtros.
            # `width=15` define a largura do campo de entrada (15 caracteres).
            filtro_data_inicio = ttk.Entry(frame_filtros, width=15)

            # Posiciona o campo de entrada ao lado do rótulo "Data Início".
            # `grid(row=0, column=1)` coloca o campo de entrada na mesma linha (linha 0) e na próxima coluna (coluna 1).
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do campo de entrada.
            filtro_data_inicio.grid(row=0, column=1, padx=5, pady=5)

            # Campo para filtro de data final

            # Cria um rótulo (label) para identificar o campo "Data Fim".
            # `text="Data Fim:"` define o texto exibido no rótulo.
            # `frame_filtros` indica que o rótulo será exibido dentro do frame de filtros.
            # `grid(row=0, column=2)` posiciona o rótulo na primeira linha (linha 0) e na terceira coluna (coluna 2) do grid.
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do rótulo.
            # `sticky="w"` alinha o texto do rótulo à esquerda (West) dentro da célula.
            ttk.Label(frame_filtros, text="Data Fim:").grid(row=0, column=2, padx=5, pady=5, sticky="w")

            # Cria um campo de entrada (Entry) para que o usuário digite a data final.
            # `ttk.Entry` é um widget que permite entrada de texto pelo usuário.
            # `frame_filtros` define que o campo será exibido dentro do frame de filtros.
            # `width=15` define a largura do campo de entrada (15 caracteres).
            filtro_data_fim = ttk.Entry(frame_filtros, width=15)

            # Posiciona o campo de entrada ao lado do rótulo "Data Fim".
            # `grid(row=0, column=3)` posiciona o campo de entrada na mesma linha (linha 0) e na quarta coluna (coluna 3) do grid.
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do campo de entrada.
            filtro_data_fim.grid(row=0, column=3, padx=5, pady=5)

            # Campo para filtro por cliente

            # Cria um rótulo (label) para identificar o campo "Cliente".
            # `text="Cliente:"` define o texto exibido no rótulo.
            # `frame_filtros` define que o rótulo será exibido dentro do frame de filtros.
            # `grid(row=0, column=4)` posiciona o rótulo na primeira linha (linha 0) e na quinta coluna (coluna 4) do grid.
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do rótulo.
            # `sticky="w"` alinha o texto do rótulo à esquerda (West) dentro da célula.
            ttk.Label(frame_filtros, text="Cliente:").grid(row=0, column=4, padx=5, pady=5, sticky="w")

            # Cria um campo de entrada (Entry) para que o usuário digite o nome do cliente.
            # `ttk.Entry` é um widget que permite a entrada de texto pelo usuário.
            # `frame_filtros` define que o campo será exibido dentro do frame de filtros.
            # `width=20` define a largura do campo de entrada como 20 caracteres.
            filtro_cliente = ttk.Entry(frame_filtros, width=20)

            # Posiciona o campo de entrada ao lado do rótulo "Cliente".
            # `grid(row=0, column=5)` posiciona o campo de entrada na mesma linha (linha 0) e na sexta coluna (coluna 5) do grid.
            # `padx=5` e `pady=5` adicionam espaçamento interno ao redor do campo de entrada.
            filtro_cliente.grid(row=0, column=5, padx=5, pady=5)

            # Botão para aplicar os filtros

            # Cria um botão para aplicar os filtros definidos pelo usuário.
            # `text="Filtrar"` define o texto exibido no botão.
            # `command=carregar_dados` associa o botão à função `carregar_dados`, que será executada ao clicar.
            btn_filtrar = ttk.Button(frame_filtros, text="Filtrar", command=carregar_dados)

            # Posiciona o botão ao lado do campo "Cliente".
            # `grid(row=0, column=6)` posiciona o botão na mesma linha (linha 0) e na sétima coluna (coluna 6) do grid.
            # `padx=10` adiciona mais espaçamento horizontal ao redor do botão, separando-o dos campos anteriores.
            # `pady=5` adiciona espaçamento vertical ao redor do botão.
            btn_filtrar.grid(row=0, column=6, padx=10, pady=5)

            # Label para exibir o total

            # Cria um rótulo (label) para exibir o total dos valores calculados.
            # `text="Total: R$ 0.00"` define o texto inicial do rótulo, exibindo o total como R$ 0.00.
            # `font=("Arial", 12, "bold")` define a fonte do texto:
            # - "Arial" é o nome da fonte,
            # - 12 é o tamanho da fonte,
            # - "bold" indica que o texto será exibido em negrito.
            label_total = ttk.Label(janela_historico, text="Total: R$ 0.00", font=("Arial", 12, "bold"))

            # Posiciona o rótulo na janela.
            # `pack()` organiza o widget de forma automática no espaço disponível.
            # `anchor="e"` alinha o rótulo à direita (east) da janela.
            # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do rótulo.
            # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
            label_total.pack(anchor="e", padx=10, pady=5)

            # Frame para a Treeview

            # Cria um frame que será usado para organizar e exibir a Treeview (tabela de dados).
            # `ttk.Frame` é um contêiner que agrupa widgets, como a Treeview e sua barra de rolagem.
            frame_historico = ttk.Frame(janela_historico)

            # Posiciona o frame na sub-janela (`janela_historico`).
            # `pack(fill="both", expand=True)` faz com que o frame ocupe todo o espaço restante da janela.
            # - `fill="both"` expande o frame tanto horizontal quanto verticalmente.
            # - `expand=True` garante que o frame se ajuste automaticamente ao redimensionamento da janela.
            frame_historico.pack(fill="both", expand=True)

            # Cria a Treeview para exibir os serviços
            # Cria a Treeview para exibir os dados do histórico

            # `ttk.Treeview` é um widget usado para criar tabelas interativas, ideal para exibir dados tabulares.
            # `frame_historico` define que a Treeview será exibida dentro do frame destinado ao histórico.
            # `columns=("data", "cliente", "servico", "valor")` define as colunas da tabela.
            # Cada identificador da lista ("data", "cliente", "servico", "valor") representa uma coluna.
            # `show="headings"` indica que apenas os cabeçalhos das colunas serão exibidos, sem uma coluna de índice extra.
            tree_servicos = ttk.Treeview(
                frame_historico,
                columns=("data", "cliente", "servico", "valor"),
                show="headings",
            )

            # Configura o cabeçalho da coluna "data".
            # `tree_servicos.heading("data", text="Data")` define:
            # - `"data"` como identificador da coluna.
            # - `"Data"` como o texto exibido no cabeçalho.
            tree_servicos.heading("data", text="Data")

            # Configura o cabeçalho da coluna "cliente".
            # `tree_servicos.heading("cliente", text="Cliente")` define:
            # - `"cliente"` como identificador da coluna.
            # - `"Cliente"` como o texto exibido no cabeçalho.
            tree_servicos.heading("cliente", text="Cliente")

            # Configura o cabeçalho da coluna "servico".
            # `tree_servicos.heading("servico", text="Serviço")` define:
            # - `"servico"` como identificador da coluna.
            # - `"Serviço"` como o texto exibido no cabeçalho.
            tree_servicos.heading("servico", text="Serviço")

            # Configura o cabeçalho da coluna "valor".
            # `tree_servicos.heading("valor", text="Valor Pago")` define:
            # - `"valor"` como identificador da coluna.
            # - `"Valor Pago"` como o texto exibido no cabeçalho.
            tree_servicos.heading("valor", text="Valor Pago")

            # Posiciona a Treeview no frame.
            # `pack()` organiza o widget na interface.
            # `side="left"` posiciona a tabela à esquerda dentro do frame.
            # `fill="both"` faz com que a tabela preencha todo o espaço disponível horizontal e verticalmente.
            # `expand=True` permite que a tabela se ajuste automaticamente ao tamanho do frame ao redimensionar a janela.
            tree_servicos.pack(side="left", fill="both", expand=True)

            # Barra de rolagem para a Treeview

            # Cria uma barra de rolagem vertical associada à Treeview.
            # `ttk.Scrollbar` é um widget usado para adicionar barras de rolagem.
            # `frame_historico` define que a barra de rolagem será exibida dentro do frame do histórico.
            # `orient="vertical"` especifica que a barra será vertical.
            # `command=tree_servicos.yview` conecta a barra de rolagem ao método de rolagem vertical da Treeview.
            scrollbar = ttk.Scrollbar(frame_historico, orient="vertical", command=tree_servicos.yview)

            # Configura a Treeview para usar a barra de rolagem.
            # `yscroll=scrollbar.set` associa a barra de rolagem vertical à Treeview.
            # Isso garante que ao rolar a barra, os dados na Treeview sejam exibidos corretamente.
            tree_servicos.configure(yscroll=scrollbar.set)

            # Posiciona a barra de rolagem no frame.
            # `pack()` organiza o widget na interface.
            # `side="right"` posiciona a barra de rolagem no lado direito do frame.
            # `fill="y"` faz com que a barra de rolagem preencha toda a altura do frame.
            scrollbar.pack(side="right", fill="y")

            # Carrega os dados inicialmente

            # Chama a função `carregar_dados` para preencher a Treeview com os dados assim que a janela é aberta.
            # Isso garante que a Treeview não fique vazia inicialmente e exiba os dados correspondentes ao serviço selecionado.
            carregar_dados()


        except IndexError:

            # Caso nenhum serviço tenha sido selecionado
            # Essa exceção ocorre quando o usuário tenta abrir o histórico sem selecionar um item na Treeview.
            # `IndexError` é levantado porque a tentativa de acessar um índice inexistente (como [0]) falha.
            messagebox.showerror("Erro", "Nenhum serviço selecionado.")

        # Caso outro erro genérico ocorra
        # `Exception` captura qualquer outro tipo de erro que possa acontecer no código.
        # A variável `e` armazena o detalhe do erro, como mensagem ou tipo de exceção.
        except Exception as e:

            # `messagebox.showerror` exibe uma caixa de diálogo de erro com:
            # - "Erro" como título.
            # - Uma mensagem que inclui o detalhe da exceção (`{e}`), útil para depuração.
            messagebox.showerror("Erro", f"Erro ao abrir histórico: {e}")


    def carregar_servicos(self):

        # Remove todos os itens existentes na Treeview.
        for item in self.tree.get_children():

            # `self.tree.get_children()` retorna todos os itens atualmente na Treeview.
            # `self.tree.delete(item)` remove cada item encontrado.
            self.tree.delete(item)

        # Itera sobre todos os serviços na coleção `colecao_servicos`.
        # `colecao_servicos.find()` retorna todos os documentos armazenados na coleção.
        # `.sort("nome", pymongo.ASCENDING)` ordena os documentos pelo
        #       campo "nome" em ordem alfabética crescente.
        for s in colecao_servicos.find().sort("nome", pymongo.ASCENDING):

            # Obtém o campo "nome" do serviço.
            # Se o campo não existir, retorna uma string vazia como padrão.
            nome = s.get("nome", "")

            # Obtém o campo "descricao" do serviço.
            # Se o campo não existir, retorna uma string vazia como padrão.
            descricao = s.get("descricao", "")

            # Obtém o campo "quantidade" do serviço.
            # Se o campo não existir, retorna 0 como padrão.
            quantidade = s.get("quantidade", 0)

            # Obtém o campo "preco" do serviço.
            # Se o campo não existir, retorna 0.0 como padrão.
            preco = s.get("preco", 0.0)

            # Insere um novo item na Treeview.
            item_id = self.tree.insert(

                # `""` indica que o item será inserido na raiz da Treeview.
                "",

                # `"end"` posiciona o item no final da lista.
                "end",

                # `iid=str(s["_id"])` define um identificador único baseado no
                #       campo `_id` do serviço no banco.
                iid=str(s["_id"]),

                # `values=(nome, descricao, quantidade, preco)` define os
                #       valores das colunas para o item.
                values=(nome, descricao, quantidade, preco)

            )

            # Verifica se a quantidade de estoque é menor que 5.
            if quantidade < 5:

                # Se a quantidade for baixa, aplica a tag `estoque_baixo` ao item.
                # Essa tag estiliza a linha da Treeview (ex.: pinta de vermelho).
                self.tree.item(item_id, tags=("estoque_baixo",))



    def selecionar_item_tree(self, event=None):

        """
        Manipula a seleção de um item na Treeview.
        Ao selecionar um serviço na lista, os detalhes desse serviço são carregados
                nos campos de entrada para edição ou exclusão.
        """

        # Tenta capturar o item selecionado na Treeview.
        try:

            # Obtém o ID único do item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Caso nenhum item esteja selecionado, encerra a função sem erros.
            return

        # Busca o serviço correspondente no banco de dados MongoDB.
        servico = colecao_servicos.find_one({"_id": ObjectId(selecionado)})

        # Verifica se o serviço foi encontrado no banco.
        if servico:

            # Preenche o campo de entrada "Nome do Serviço"
            #       com o valor correspondente.
            # Primeiro, limpa o conteúdo existente no campo.
            self.nome_entry.delete(0, "end")

            # Insere o nome do serviço recuperado do banco.
            self.nome_entry.insert(0, servico.get("nome", ""))

            # Preenche o campo de entrada "Descrição" com o valor correspondente.
            self.descricao_entry.delete(0, "end")
            self.descricao_entry.insert(0, servico.get("descricao", ""))

            # Preenche o campo de entrada "Quantidade" com o valor correspondente.
            # Converte o valor para string antes de inseri-lo no campo.
            self.quantidade_entry.delete(0, "end")
            self.quantidade_entry.insert(0, str(servico.get("quantidade", 0)))

            # Preenche o campo de entrada "Preço" com o valor correspondente.
            # Converte o valor para string antes de inseri-lo no campo.
            self.preco_entry.delete(0, "end")
            self.preco_entry.insert(0, str(servico.get("preco", 0.0)))



    # Define o método `novo_servico` para adicionar um novo
    #       serviço ao banco de dados.
    def novo_servico(self):

        # Obtém o texto inserido no campo de entrada do nome e remove
        #       espaços em branco no início e no final.
        nome = self.nome_entry.get().strip()

        # Obtém o texto inserido no campo de entrada da descrição e remove
        #       espaços em branco no início e no final.
        descricao = self.descricao_entry.get().strip()

        # Obtém o texto inserido no campo de entrada da quantidade e remove
        #       espaços em branco no início e no final.
        quantidade = self.quantidade_entry.get().strip()

        # Obtém o texto inserido no campo de entrada do preço e remove
        #       espaços em branco no início e no final.
        preco = self.preco_entry.get().strip()

        # Verifica se o campo de nome está vazio.
        if not nome:

            # Exibe uma mensagem de erro se o nome não foi preenchido.
            messagebox.showerror("Erro", "Nome do serviço é obrigatório.")

            # Sai do método sem continuar.
            return

        try:

            # Converte o valor do campo de quantidade para um número
            #       inteiro, ou 0 caso esteja vazio.
            quantidade = int(quantidade) if quantidade else 0

            # Converte o valor do campo de preço para um número decimal,
            #       ou 0.0 caso esteja vazio.
            preco = float(preco) if preco else 0.0

        except ValueError:

            # Exibe uma mensagem de erro se os valores de quantidade ou
            #       preço não forem numéricos.
            messagebox.showerror("Erro",
                                 "Quantidade e preço devem ser numéricos.")

            # Sai do método sem continuar.
            return

        # Cria um dicionário com os dados do novo serviço.
        novo = {

            "nome": nome,  # Nome do serviço.
            "descricao": descricao,  # Descrição do serviço.
            "quantidade": quantidade,  # Quantidade em estoque.
            "preco": preco  # Preço do serviço.

        }

        # Insere o novo serviço na coleção de serviços do banco de dados.
        colecao_servicos.insert_one(novo)

        # Recarrega a lista de serviços na interface para incluir o novo serviço.
        self.carregar_servicos()

        # Limpa os campos de entrada para permitir adicionar outro serviço.
        self.limpar_campos()

        # Exibe uma mensagem informando que o serviço foi adicionado com sucesso.
        messagebox.showinfo("Sucesso",
                            "Serviço adicionado com sucesso.")


    # Define o método `limpar_campos` para limpar os campos de entrada do formulário.
    def limpar_campos(self):

        # Limpa o conteúdo do campo de entrada do nome.
        # `delete(0, "end")` remove o texto desde o início até o final do campo.
        self.nome_entry.delete(0, "end")

        # Limpa o conteúdo do campo de entrada da descrição.
        self.descricao_entry.delete(0, "end")

        # Limpa o conteúdo do campo de entrada da quantidade.
        self.quantidade_entry.delete(0, "end")

        # Limpa o conteúdo do campo de entrada do preço.
        self.preco_entry.delete(0, "end")


    # Define o método para editar um serviço existente.
    def editar_servico(self):

        # Tenta obter o item selecionado na Treeview.
        try:

            # Recupera o identificador do item selecionado na Treeview.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Caso nenhum item esteja selecionado, exibe uma mensagem de erro.
            messagebox.showerror("Erro",
                                 "Nenhum serviço selecionado.")

            # Sai do método sem continuar.
            return

        # Obtém e remove os espaços em branco do campo de entrada do nome.
        nome = self.nome_entry.get().strip()

        # Obtém e remove os espaços em branco do campo de entrada da descrição.
        descricao = self.descricao_entry.get().strip()

        # Obtém e remove os espaços em branco do campo de entrada da quantidade.
        quantidade = self.quantidade_entry.get().strip()

        # Obtém e remove os espaços em branco do campo de entrada do preço.
        preco = self.preco_entry.get().strip()

        # Verifica se o campo "nome" está vazio.
        if not nome:

            # Exibe uma mensagem de erro se o campo "nome" não for preenchido.
            messagebox.showerror("Erro", "Nome do serviço é obrigatório.")

            # Sai do método sem continuar.
            return

        # Tenta converter os valores de quantidade e preço
        #       para os tipos numéricos corretos.
        try:

            # Converte a quantidade para um número inteiro, se for preenchida.
            # Caso contrário, define como 0.
            quantidade = int(quantidade) if quantidade else 0

            # Converte o preço para um número decimal (float), se for preenchido.
            # Caso contrário, define como 0.0.
            preco = float(preco) if preco else 0.0

        except ValueError:

            # Exibe uma mensagem de erro caso os valores de quantidade ou
            #       preço não sejam numéricos.
            messagebox.showerror("Erro",
                                 "Quantidade e preço devem ser numéricos.")

            # Sai do método sem continuar.
            return

        # Atualiza o documento correspondente na coleção "colecao_servicos".
        colecao_servicos.update_one(

            # Localiza o documento pelo campo "_id" usando o ID selecionado na Treeview.
            {"_id": ObjectId(selecionado)},

            {

                # Define os campos que serão atualizados no documento.
                "$set": {

                    "nome": nome,  # Atualiza o campo "nome" com o valor fornecido.
                    "descricao": descricao,  # Atualiza o campo "descricao" com o valor fornecido.
                    "quantidade": quantidade,  # Atualiza o campo "quantidade" com o valor fornecido.
                    "preco": preco  # Atualiza o campo "preco" com o valor fornecido.

                }
            }
        )

        # Recarrega os serviços na Treeview para refletir as alterações feitas.
        self.carregar_servicos()

        # Limpa os campos de entrada no formulário.
        self.limpar_campos()

        # Exibe uma mensagem de sucesso informando que o serviço foi editado.
        messagebox.showinfo("Sucesso", "Serviço editado com sucesso.")


    def excluir_servico(self):

        # Tenta obter o item selecionado na Treeview.
        try:

            # Obtém o ID do item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe um erro caso nenhum serviço esteja selecionado.
            messagebox.showerror("Erro", "Nenhum serviço selecionado.")

            # Encerra a execução da função.
            return

        # Exibe uma mensagem de confirmação para o usuário.
        resposta = messagebox.askyesno("Confirmar",
                                       "Deseja realmente excluir este serviço?")

        # Se o usuário confirmar a exclusão:
        if resposta:

            # Remove o documento correspondente na coleção "colecao_servicos" pelo "_id".
            colecao_servicos.delete_one({"_id": ObjectId(selecionado)})

            # Atualiza a Treeview carregando novamente os serviços.
            self.carregar_servicos()

            # Limpa os campos de entrada no formulário.
            self.limpar_campos()

            # Exibe uma mensagem de sucesso informando que o serviço foi excluído.
            messagebox.showinfo("Sucesso",
                                "Serviço excluído com sucesso.")


# ------------------------------------------------------------
# Tela Clientes
# ------------------------------------------------------------
class TelaClientes(ttk.Frame):

    # Método construtor da classe `TelaClientes`,
    #       chamado ao criar uma instância.
    def __init__(self, parent):

        # `parent` é o widget pai que conterá este frame, o
        #       frame principal da aplicação.
        # Chama o construtor da classe base `ttk.Frame` para herdar e
        #       inicializar corretamente o frame.
        super().__init__(parent)

        # Cria um rótulo (Label) para exibir o título "Clientes".
        # Define o texto do rótulo como "Clientes".
        # Aplica a fonte Arial, tamanho 14, com estilo em negrito (bold).
        titulo_label = ttk.Label(self, text="Clientes", font=("Arial", 14, "bold"))

        # Posiciona o rótulo no topo do frame.
        # `side="top"` alinha o rótulo na parte superior.
        # `anchor="w"` alinha o texto à esquerda dentro do espaço disponível.
        # `padx=10` e `pady=10` adicionam espaçamento horizontal e
        #       vertical, respectivamente.
        titulo_label.pack(side="top", anchor="w", padx=10, pady=10)

        # Cria um frame (container) para agrupar os campos de entrada de dados.
        # `padding=10` adiciona um espaçamento interno de 10
        #       pixels em todos os lados do frame.
        campos_frame = ttk.Frame(self, padding=10)

        # Posiciona o frame no topo do frame principal.
        # `side="top"` alinha o frame na parte superior.
        # `fill="x"` faz com que o frame se expanda horizontalmente
        #       para preencher o espaço disponível.
        campos_frame.pack(side="top", fill="x")

        # Adiciona um rótulo (Label) ao `campos_frame` com o texto "Nome Completo:".
        # `row=0` posiciona o rótulo na primeira linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(campos_frame,
                  text="Nome Completo:").grid(row=0,
                                              column=0,
                                              padx=5,
                                              pady=5,
                                              sticky="w")

        # Cria um campo de entrada de texto (Entry) para o nome completo.
        # `width=30` define a largura do campo de entrada em caracteres.
        self.nome_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=0` posiciona o campo na primeira linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e
        #       vertical ao redor do campo.
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) ao `campos_frame` com o texto "Telefone:".
        # `row=1` posiciona o rótulo na segunda linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west)
        #       dentro da célula da grade.
        ttk.Label(campos_frame,
                  text="Telefone:").grid(row=1,
                                         column=0,
                                         padx=5,
                                         pady=5,
                                         sticky="w")

        # Cria um campo de entrada de texto (Entry) para o número de telefone.
        # `width=30` define a largura do campo de entrada em caracteres.
        self.telefone_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=1` posiciona o campo na segunda linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e
        #       vertical ao redor do campo.
        self.telefone_entry.grid(row=1, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) ao `campos_frame` com o texto "E-mail:".
        # `row=2` posiciona o rótulo na terceira linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(campos_frame,
                  text="E-mail:").grid(row=2,
                                       column=0,
                                       padx=5,
                                       pady=5,
                                       sticky="w")

        # Cria um campo de entrada de texto (Entry) para o e-mail.
        # `width=30` define a largura do campo de entrada em caracteres.
        self.email_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=2` posiciona o campo na terceira linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) ao `campos_frame` com o texto "Endereço:".
        # `row=3` posiciona o rótulo na quarta linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(campos_frame,
                  text="Endereço:").grid(row=3,
                                         column=0,
                                         padx=5,
                                         pady=5,
                                         sticky="w")

        # Cria um campo de entrada de texto (Entry) para o endereço.
        # `width=30` define a largura do campo de entrada em caracteres.
        self.endereco_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=3` posiciona o campo na quarta linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        self.endereco_entry.grid(row=3, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) ao `campos_frame` com o texto "Data Nasc (dd/mm/aaaa):".
        # `row=4` posiciona o rótulo na quinta linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(campos_frame,
                  text="Data Nasc (dd/mm/aaaa):").grid(row=4,
                                                       column=0,
                                                       padx=5,
                                                       pady=5,
                                                       sticky="w")

        # Cria um campo de entrada de texto (Entry) para a data de nascimento.
        # `width=30` define a largura do campo de entrada em caracteres.
        self.nasc_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na grade do `campos_frame`.
        # `row=4` posiciona o campo na quinta linha da grade.
        # `column=1` posiciona o campo na segunda coluna da grade.
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e
        #       vertical ao redor do campo.
        self.nasc_entry.grid(row=4, column=1, padx=5, pady=5)

        # Cria um frame (`botoes_frame`) dentro do `campos_frame`
        #       para organizar os botões de ação.
        # Este frame será usado para agrupar e alinhar os botões
        #       de forma centralizada.
        botoes_frame = ttk.Frame(campos_frame)

        # Posiciona o `botoes_frame` na grade do `campos_frame`.
        # `row=5` posiciona o frame na sexta linha da grade.
        # `column=0` posiciona o frame na primeira coluna da grade.
        # `columnspan=2` faz com que o frame ocupe duas colunas na
        #       grade, centralizando os botões.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do frame.
        botoes_frame.grid(row=5, column=0, columnspan=2, pady=10)

        # Adiciona um botão "Adicionar" ao `botoes_frame`.
        # O texto exibido no botão é "Adicionar".
        # O botão é associado ao método `self.novo_cliente`, que será
        #       chamado quando o botão for clicado.
        # `side="left"` posiciona o botão à esquerda dentro do `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Adicionar",
                   command=self.novo_cliente).pack(side="left",
                                                   padx=5)

        # Adiciona um botão "Editar" ao `botoes_frame`.
        # O texto exibido no botão é "Editar".
        # O botão é associado ao método `self.editar_cliente`, que será
        #       chamado quando o botão for clicado.
        # `side="left"` posiciona o botão à esquerda do próximo botão dentro do `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Editar",
                   command=self.editar_cliente).pack(side="left",
                                                     padx=5)

        # Adiciona um botão "Excluir" ao `botoes_frame`.
        # O texto exibido no botão é "Excluir".
        # O botão é associado ao método `self.excluir_cliente`, que será
        #       chamado quando o botão for clicado.
        # `side="left"` posiciona o botão à esquerda do próximo botão dentro do `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Excluir",
                   command=self.excluir_cliente).pack(side="left",
                                                      padx=5)

        # Botão para ver o histórico do Cliente
        # Adiciona um botão "Ver Histórico" ao `botoes_frame`.
        # O texto exibido no botão é "Ver Histórico".
        # O botão é associado ao método `self.ver_historico_cliente`, que
        #       será chamado quando o botão for clicado.
        # `side="left"` posiciona o botão à esquerda dentro do `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Ver Histórico",
                   command=self.ver_historico_cliente).pack(side="left",
                                                            padx=5)

        # Cria um frame `table_frame` dentro do widget principal.
        # Esse frame será usado para conter a tabela com os dados dos clientes.
        # `side="top"` posiciona o frame na parte superior do layout.
        # `fill="both"` faz com que o frame preencha tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame se expanda proporcionalmente ao
        #       redimensionamento da janela principal.
        # `padx=10` e `pady=10` adicionam espaçamento horizontal e
        #       vertical ao redor do frame.
        table_frame = ttk.Frame(self)
        table_frame.pack(side="top",
                         fill="both",
                         expand=True,
                         padx=10,
                         pady=10)

        # Cria uma Treeview dentro do `table_frame` para exibir os dados dos clientes.
        # `columns` define as colunas que serão exibidas na Treeview.
        # Cada coluna representa um campo: "nome", "telefone", "email", "endereco" e "nascimento".
        # `show="headings"` faz com que apenas os cabeçalhos das colunas
        #       sejam exibidos, sem a coluna de árvore padrão.
        self.tree = ttk.Treeview(table_frame,
                                columns=("nome", "telefone", "email", "endereco", "nascimento"),
                                show="headings")

        # Define os títulos das colunas da Treeview.
        # Cada coluna recebe um texto descritivo que será exibido no cabeçalho.
        # "nome" é exibido como "Nome".
        self.tree.heading("nome", text="Nome")

        # "telefone" é exibido como "Telefone".
        self.tree.heading("telefone", text="Telefone")

        # "email" é exibido como "E-mail".
        self.tree.heading("email", text="E-mail")

        # "endereco" é exibido como "Endereço".
        self.tree.heading("endereco", text="Endereço")

        # "nascimento" é exibido como "Data Nasc.".
        self.tree.heading("nascimento", text="Data Nasc.")

        # Cria uma barra de rolagem vertical para a Treeview.
        # `table_frame` é o frame pai que contém a Treeview e a barra de rolagem.
        # A orientação é definida como "vertical" para rolar verticalmente.
        # O comando da barra de rolagem é configurado para controlar a visualização da Treeview.
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient="vertical",
                                  command=self.tree.yview)

        # Configura a Treeview para associá-la à barra de rolagem.
        # Isso permite que a barra de rolagem funcione
        #       corretamente com a Treeview.
        self.tree.configure(yscroll=scrollbar.set)

        # Posiciona a Treeview dentro do `table_frame`.
        # `side="left"` alinha a Treeview ao lado esquerdo do frame.
        # `fill="both"` faz com que a Treeview preencha tanto a
        #       largura quanto a altura disponíveis.
        # `expand=True` permite que a Treeview cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem dentro do `table_frame`.
        # `side="left"` alinha a barra de rolagem ao lado esquerdo do frame.
        # `fill="y"` faz com que a barra de rolagem preencha
        #       toda a altura disponível.
        scrollbar.pack(side="left", fill="y")

        # Associa o evento de seleção da Treeview a um método.
        # Quando um item é selecionado na Treeview, o
        #       método `selecionar_item_tree` é chamado.
        # `"<<TreeviewSelect>>"` é o evento padrão para seleção de itens na Treeview.
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_tree)

        # Chama o método para carregar os clientes na Treeview.
        # Esse método busca os dados do banco de dados e
        #       preenche a Treeview com os registros.
        self.carregar_clientes()


    # Método para selecionar e exibir os dados de um cliente ao
    #       clicar em uma linha na TreeView.
    def selecionar_item_tree(self, event=None):

        # Tenta obter o ID do item selecionado na TreeView.
        try:

            # Obtém o identificador do item selecionado na TreeView.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Caso nenhuma linha esteja selecionada, interrompe a execução do método.
            return

        # Busca no banco de dados os detalhes do cliente usando o ID selecionado.
        cliente = colecao_clientes.find_one({"_id": ObjectId(selecionado)})

        # Verifica se o cliente foi encontrado no banco de dados.
        if cliente:

            # Limpa o campo de entrada para o nome do cliente.
            self.nome_entry.delete(0, "end")

            # Insere o nome do cliente recuperado do banco de dados no campo de entrada.
            self.nome_entry.insert(0, cliente.get("nome", ""))

            # Limpa o campo de entrada para o telefone do cliente.
            self.telefone_entry.delete(0, "end")

            # Insere o telefone do cliente recuperado do banco de
            #       dados no campo de entrada.
            self.telefone_entry.insert(0, cliente.get("telefone", ""))

            # Limpa o campo de entrada para o e-mail do cliente.
            self.email_entry.delete(0, "end")

            # Insere o e-mail do cliente recuperado do banco de
            #       dados no campo de entrada.
            self.email_entry.insert(0, cliente.get("email", ""))

            # Limpa o campo de entrada para o endereço do cliente.
            self.endereco_entry.delete(0, "end")

            # Insere o endereço do cliente recuperado do banco de
            #       dados no campo de entrada.
            self.endereco_entry.insert(0, cliente.get("endereco", ""))

            # Limpa o campo de entrada para a data de nascimento do cliente.
            self.nasc_entry.delete(0, "end")

            # Insere a data de nascimento do cliente recuperado do
            #       banco de dados no campo de entrada.
            self.nasc_entry.insert(0, cliente.get("nascimento", ""))


    # Método para carregar clientes na Treeview.
    # Remove todos os itens existentes na Treeview antes de
    #       adicionar novos registros.
    def carregar_clientes(self):

        # Itera sobre os itens atualmente exibidos na Treeview.
        # Remove cada um deles para garantir que a Treeview seja
        #       atualizada corretamente.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Consulta todos os clientes no banco de dados, ordenando pelo nome.
        # `colecao_clientes.find()` retorna todos os documentos da coleção.
        # `.sort("nome", pymongo.ASCENDING)` organiza os resultados em ordem
        #       alfabética crescente com base no campo "nome".
        for c in colecao_clientes.find().sort("nome", pymongo.ASCENDING):

            # Insere um novo item na Treeview para cada cliente.
            # `iid=str(c["_id"])` define um identificador exclusivo para o
            #       item na Treeview, usando o ID do cliente.
            # `values=(...)` preenche as colunas da Treeview com os dados do cliente.
            self.tree.insert("",
                             "end",  # Adiciona o item como filho da raiz (sem pai).
                             iid=str(c["_id"]),
                             values=(
                                 c.get("nome", ""),  # Obtém o nome do cliente, ou uma string vazia se não existir.
                                 c.get("telefone", ""),
                                 # Obtém o telefone do cliente, ou uma string vazia se não existir.
                                 c.get("email", ""),
                                 # Obtém o e-mail do cliente, ou uma string vazia se não existir.
                                 c.get("endereco", ""),
                                 # Obtém o endereço do cliente, ou uma string vazia se não existir.
                                 c.get("nascimento",
                                       "")))  # Obtém a data de nascimento do cliente, ou uma string vazia se não existir.



    # Método para adicionar um novo cliente ao banco de dados.
    def novo_cliente(self):

        # Obtém o valor do campo de entrada "Nome" e remove espaços
        #       em branco nas extremidades.
        nome = self.nome_entry.get().strip()

        # Obtém o valor do campo de entrada "Telefone" e remove
        #       espaços em branco nas extremidades.
        telefone = self.telefone_entry.get().strip()

        # Obtém o valor do campo de entrada "E-mail" e remove
        #       espaços em branco nas extremidades.
        email = self.email_entry.get().strip()

        # Obtém o valor do campo de entrada "Endereço" e remove
        #       espaços em branco nas extremidades.
        endereco = self.endereco_entry.get().strip()

        # Obtém o valor do campo de entrada "Data de Nascimento" e
        #       remove espaços em branco nas extremidades.
        nasc = self.nasc_entry.get().strip()

        # Verifica se os campos "Nome" e "Telefone" estão preenchidos.
        # Caso estejam vazios, exibe uma mensagem de erro e interrompe a execução.
        if not nome or not telefone:
            messagebox.showerror("Erro", "Nome e Telefone são obrigatórios.")
            return

        # Cria um dicionário chamado `novo` contendo as informações do
        #       cliente que será adicionado.
        # Cada chave do dicionário corresponde a um campo no banco de dados.
        novo = {
            "nome": nome,  # Nome completo do cliente.
            "telefone": telefone,  # Telefone de contato do cliente.
            "email": email,  # Endereço de e-mail do cliente.
            "endereco": endereco,  # Endereço residencial ou comercial do cliente.
            "nascimento": nasc  # Data de nascimento do cliente (no formato fornecido).
        }

        # Insere o dicionário `novo` na coleção `colecao_clientes`
        #       do banco de dados.
        colecao_clientes.insert_one(novo)

        # Atualiza a lista de clientes exibida na interface carregando
        #       novamente os dados do banco.
        self.carregar_clientes()

        # Limpa os campos de entrada do formulário para
        #       que possam ser usados novamente.
        self.limpar_campos()

        # Exibe uma mensagem informando que o cliente foi
        #       adicionado com sucesso.
        messagebox.showinfo("Sucesso",
                            "Cliente adicionado com sucesso.")


    # Método para limpar os campos do formulário de entrada.
    def limpar_campos(self):

        # Limpa o campo de entrada de nome, removendo qualquer texto existente.
        self.nome_entry.delete(0, "end")

        # Limpa o campo de entrada de telefone, removendo qualquer texto existente.
        self.telefone_entry.delete(0, "end")

        # Limpa o campo de entrada de e-mail, removendo qualquer texto existente.
        self.email_entry.delete(0, "end")

        # Limpa o campo de entrada de endereço, removendo qualquer texto existente.
        self.endereco_entry.delete(0, "end")

        # Limpa o campo de entrada de data de nascimento, removendo
        #       qualquer texto existente.
        self.nasc_entry.delete(0, "end")


    # Define o método `editar_cliente` para editar as informações
    #       de um cliente selecionado.
    def editar_cliente(self):

        # Tenta obter o cliente selecionado na TreeView.
        try:

            # Obtém o ID do cliente selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe uma mensagem de erro se nenhum cliente estiver selecionado.
            messagebox.showerror("Erro", "Nenhum cliente selecionado.")
            return

        # Recupera as informações dos campos de entrada.
        nome = self.nome_entry.get().strip()  # Remove espaços desnecessários do início e do fim.
        telefone = self.telefone_entry.get().strip()  # Telefones não podem ser deixados em branco.
        email = self.email_entry.get().strip()  # O e-mail pode ser deixado vazio.
        endereco = self.endereco_entry.get().strip()  # Endereço pode ser deixado vazio.
        nasc = self.nasc_entry.get().strip()  # Data de nascimento pode ser deixada vazia.

        # Verifica se os campos obrigatórios `nome` e `telefone`
        #       estão preenchidos.
        if not nome or not telefone:

            # Exibe uma mensagem de erro se os campos obrigatórios estiverem vazios.
            messagebox.showerror("Erro", "Nome e Telefone são obrigatórios.")
            return

        # Atualiza as informações do cliente no banco de dados.
        colecao_clientes.update_one(

            # Localiza o cliente pelo ID selecionado.
            {"_id": ObjectId(selecionado)},
            {

                # Define os novos valores para os campos editados.
                "$set": {
                    "nome": nome,  # Atualiza o nome do cliente.
                    "telefone": telefone,  # Atualiza o telefone do cliente.
                    "email": email,  # Atualiza o e-mail do cliente.
                    "endereco": endereco,  # Atualiza o endereço do cliente.
                    "nascimento": nasc  # Atualiza a data de nascimento do cliente.
                }
            }
        )

        # Recarrega os dados dos clientes na interface
        #       após a atualização.
        self.carregar_clientes()

        # Limpa os campos de entrada após a edição.
        self.limpar_campos()

        # Exibe uma mensagem informando que a edição foi realizada com sucesso.
        messagebox.showinfo("Sucesso", "Cliente editado com sucesso.")


    def excluir_cliente(self):

        # Tenta obter o cliente selecionado na TreeView.
        try:

            # Obtém o ID do item selecionado na TreeView.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe uma mensagem de erro se nenhum cliente estiver selecionado.
            messagebox.showerror("Erro", "Nenhum cliente selecionado.")

            # Encerra o método, já que não há cliente para excluir.
            return

        # Exibe uma caixa de diálogo de confirmação para o usuário.
        resposta = messagebox.askyesno(

            # Título da janela de confirmação.
            "Confirmar",

            # Mensagem exibida na janela.
            "Deseja realmente excluir este cliente?"

        )

        # Prossegue com a exclusão apenas se o usuário confirmar.
        # Exibe uma caixa de diálogo de confirmação para o usuário
        #       com a mensagem e título apropriados.
        resposta = messagebox.askyesno("Confirmar",  # Título da janela de confirmação.
                                        "Deseja realmente excluir este cliente?")  # Mensagem exibida na janela.


        # Verifica se o usuário confirmou a exclusão.
        if resposta:

            # Remove o cliente do banco de dados utilizando o ID selecionado.
            colecao_clientes.delete_one({"_id": ObjectId(selecionado)})

            # Recarrega a lista de clientes exibida na TreeView
            #       para refletir a exclusão.
            self.carregar_clientes()

            # Limpa os campos de entrada para evitar dados residuais.
            self.limpar_campos()

            # Exibe uma mensagem informando que a exclusão foi bem-sucedida.
            messagebox.showinfo( "Sucesso",  # Título da mensagem de sucesso.
                                "Cliente excluído com sucesso.")  # Mensagem exibida ao usuário.


    # Define o método para visualizar o histórico de um
    #       cliente selecionado na Treeview.
    def ver_historico_cliente(self):

        # Tenta obter o item selecionado na Treeview.
        try:

            # Obtém o identificador do cliente selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe uma mensagem de erro caso nenhum cliente esteja selecionado.
            messagebox.showerror("Erro", "Nenhum cliente selecionado.")
            return

        # Busca no banco de dados o documento do cliente correspondente ao ID selecionado.
        cliente = colecao_clientes.find_one({"_id": ObjectId(selecionado)})

        # Verifica se o cliente foi encontrado no banco de dados.
        if cliente:

            # Abre a tela de histórico do cliente, passando o nome
            #       do cliente como parâmetro.
            TelaHistoricoCliente(self, cliente.get("nome", ""))



# ------------------------------------------------------------
# Tela Historico de Cliente
# ------------------------------------------------------------
# Define uma classe chamada `TelaHistoricoCliente` que herda de `tk.Toplevel`.
class TelaHistoricoCliente(tk.Toplevel):

    # Método construtor da classe, inicializa a janela de histórico do cliente.
    # Método construtor da classe `TelaHistoricoCliente`.
    # `parent` é a janela principal que chama esta janela.
    # `nome_cliente` é uma string com o nome do cliente cujo histórico será exibido.
    def __init__(self, parent, nome_cliente):

        # Chama o construtor da classe pai (`tk.Toplevel`) para configurar a janela.
        # Chama o construtor da classe pai (`tk.Toplevel`), passando o argumento `parent`.
        # Isso assegura que a nova janela seja vinculada à janela principal que a criou.
        super().__init__(parent)

        # Define o título da janela com o nome do cliente passado como argumento.
        self.title(f"Histórico de {nome_cliente}")

        # Configura a janela para abrir no estado maximizado.
        self.state("zoomed")

        # Define a cor de fundo da janela como branca.
        self.configure(bg="#FFFFFF")

        # Armazena o nome do cliente passado como argumento
        #       em um atributo da classe.
        self.nome_cliente = nome_cliente

        # Cria um rótulo (`Label`) que exibirá o título da janela com o nome do cliente.
        # `text`: Define o texto a ser exibido, incluindo o nome do cliente.
        # `font`: Define a fonte como Arial, tamanho 20 e estilo negrito ("bold").
        titulo_label = ttk.Label(self,
                                 text=f"Histórico de {nome_cliente}",
                                 font=("Arial", 20, "bold"))

        # Posiciona o rótulo na janela, centralizado verticalmente com
        #       um espaçamento vertical (pady) de 20 pixels.
        titulo_label.pack(pady=20)

        # Cria um frame (`botoes_frame`) para agrupar os botões e filtros.
        # O frame será utilizado para posicionar elementos de controle na interface.
        botoes_frame = ttk.Frame(self)

        # Posiciona o frame na parte superior da janela.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        # `pady=10` adiciona um espaçamento vertical de 10
        #       pixels acima e abaixo do frame.
        botoes_frame.pack(fill="x", pady=10)

        # Adiciona um rótulo (`Label`) dentro do `botoes_frame`
        #       para indicar a seção de filtros.
        # O texto "Filtrar por:" será exibido como um indicativo de funcionalidade.
        # `side="left"` alinha o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        ttk.Label(botoes_frame,
                  text="Filtrar por:").pack(side="left",
                                            padx=5)

        # Cria um campo de entrada (`Entry`) dentro do `botoes_frame`
        #       para que o usuário possa inserir filtros.
        # O campo será utilizado para digitar termos de busca.
        # `width=30` define a largura do campo de entrada.
        self.filtro_entry = ttk.Entry(botoes_frame, width=30)

        # Posiciona o campo de entrada (`Entry`) à esquerda no `botoes_frame`.
        # `side="left"` alinha o campo à esquerda.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        self.filtro_entry.pack(side="left", padx=5)

        # Adiciona um botão (`Button`) dentro do `botoes_frame` para aplicar o filtro.
        # O botão possui o texto "Filtrar" e executa o método `atualizar_lista` ao ser clicado.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Filtrar",
                   command=self.atualizar_lista).pack(side="left",
                                                      padx=5)

        # Adiciona outro botão (`Button`) dentro do `botoes_frame`
        #       para limpar os filtros.
        # O botão possui o texto "Limpar" e executa o método `limpar_filtro` ao ser clicado.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Limpar",
                   command=self.limpar_filtro).pack(side="left",
                                                    padx=5)

        # Cria um rótulo (`Label`) dentro do `botoes_frame` para exibir o valor total.
        # O texto do rótulo começa como "Total: R$ 0.00".
        # `font=("Arial", 12, "bold")` define a fonte como Arial, tamanho 12, e em negrito.
        # `side="right"` alinha o rótulo à direita dentro do `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        self.total_label = ttk.Label(botoes_frame,
                                     text="Total: R$ 0.00",
                                     font=("Arial", 12, "bold"))
        self.total_label.pack(side="right", padx=5)

        # Cria um frame (`Frame`) dentro do objeto atual (`self`)
        #       para a tabela de dados.
        # `fill="both"` faz com que o frame preencha tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame cresça proporcionalmente ao
        #       redimensionamento da janela.
        # `padx=20` adiciona um espaçamento horizontal de 20 pixels ao redor do frame.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Cria uma Treeview dentro do `table_frame` para exibir os dados em formato tabular.
        # As colunas são definidas por `columns=("data", "hora", "itens", "funcionario")`.
        # `show="headings"` garante que as colunas sejam exibidas como cabeçalhos.
        self.tree = ttk.Treeview(table_frame,
                                columns=("data", "hora", "itens", "funcionario"),
                                show="headings")

        # Define o cabeçalho para a coluna "data" com o texto "Data".
        self.tree.heading("data", text="Data")

        # Define o cabeçalho para a coluna "hora" com o texto "Hora".
        self.tree.heading("hora", text="Hora")

        # Define o cabeçalho para a coluna "itens" com o texto "Itens".
        self.tree.heading("itens", text="Itens")

        # Define o cabeçalho para a coluna "funcionario" com o texto "Funcionário".
        self.tree.heading("funcionario", text="Funcionário")

        # Define a largura da coluna "data" como 100 pixels.
        self.tree.column("data", width=100)

        # Define a largura da coluna "hora" como 100 pixels.
        self.tree.column("hora", width=100)

        # Define a largura da coluna "itens" como 300 pixels.
        self.tree.column("itens", width=300)

        # Define a largura da coluna "funcionario" como 200 pixels.
        self.tree.column("funcionario", width=200)

        # Cria uma barra de rolagem vertical para a Treeview.
        # A orientação é "vertical" e a função `yscroll` é
        #       associada ao método `tree.yview`.
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient="vertical",
                                  command=self.tree.yview)

        # Configura a Treeview para usar a barra de rolagem vertical.
        self.tree.configure(yscroll=scrollbar.set)

        # Posiciona a Treeview dentro do `table_frame`.
        # `side="left"` faz com que a Treeview seja alinhada à esquerda do frame.
        # `fill="both"` faz com que a Treeview preencha tanto a
        #       largura quanto a altura disponíveis.
        # `expand=True` permite que a Treeview cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem à direita da Treeview.
        # `fill="y"` faz com que a barra de rolagem preencha a altura disponível.
        scrollbar.pack(side="right", fill="y")

        # Associa o evento de clique duplo (<Double-1>) para abrir os
        #       detalhes do atendimento.
        # Quando o usuário der um duplo clique na Treeview, o
        #       método `abrir_detalhes_atendimento` será chamado.
        self.tree.bind("<Double-1>", self.abrir_detalhes_atendimento)

        # Atualiza a lista de atendimentos na interface, chamando o
        #       método para carregar os dados.
        self.atualizar_lista()


    # Define o método `atualizar_lista`, que é responsável por
    #       atualizar a lista de atendimentos na interface.
    def atualizar_lista(self):

        # Obtém o texto inserido no campo de filtro e remove espaços extras (strip),
        #       além de converter o texto para minúsculas (lower) para facilitar a busca.
        filtro = self.filtro_entry.get().strip().lower()

        # Remove todos os itens atualmente exibidos na Treeview,
        #       limpando a lista de atendimentos.
        # `self.tree.delete(*self.tree.get_children())` exclui todas as
        #       entradas existentes na Treeview.
        self.tree.delete(*self.tree.get_children())

        # Inicializa o total em zero. Este valor será utilizado para
        #       somar os valores dos atendimentos filtrados.
        total = 0.0

        # Inicia um loop que percorre todos os agendamentos encontrados na
        #       coleção `colecao_agendamentos`
        # A pesquisa é feita filtrando pelo nome do cliente e ordenando os
        #       resultados pela data em ordem decrescente.
        for ag in colecao_agendamentos.find({"cliente": self.nome_cliente}).sort("data", pymongo.DESCENDING):

            # Obtém a data do agendamento. Caso não exista, atribui uma
            #       string vazia como valor padrão.
            data = ag.get("data", "")

            # Obtém a hora de início do agendamento. Caso não exista,
            #       atribui uma string vazia como valor padrão.
            hora = ag.get("inicio", "")

            # Obtém o nome do funcionário que atendeu o agendamento.
            # Se o nome do funcionário não estiver presente,
            # a variável `funcionario` receberá "Desconhecido" como valor padrão.
            funcionario = ag.get("funcionario_nome", "Desconhecido")

            # Obtém a lista de itens do agendamento (serviços/produtos).
            # Se não houver itens, a lista ficará vazia.
            itens = ag.get("itens", [])

            # Cria uma lista vazia para armazenar os itens convertidos
            #       para string de forma mais legível.
            itens_str = []

            # Verificação de consistência dos itens
            # Inicia um loop para percorrer todos os itens do agendamento.
            # `itens` é uma lista que contém os serviços/produtos
            #       relacionados ao agendamento.
            for it in itens:

                try:

                    # Verifica se o item possui pelo menos 2 elementos (nome e preço).
                    # Caso o nome do item não esteja presente, atribui "Item desconhecido".
                    nome_item = it[1] if len(it) > 1 else "Item desconhecido"

                    # Tenta obter o preço do item. Se não houver preço ou o valor
                    #       for inválido, define o preço como 0.0.
                    preco_item = float(it[2]) if len(it) > 2 and it[2] else 0.0

                    # Adiciona o nome e o preço formatado do item na lista `itens_str`.
                    # O preço é formatado com 2 casas decimais (R$xx.xx).
                    itens_str.append(f"{nome_item} (R${preco_item:.2f})")

                    # Adiciona o preço do item ao total acumulado.
                    total += preco_item

                except (IndexError, ValueError):

                    # Se ocorrer um erro ao acessar os dados do item (por exemplo,
                    #       índice fora do limite ou valor inválido),
                    #       adiciona "Item inválido" à lista de itens.
                    itens_str.append("Item inválido")

            # Junta os itens da lista `itens_str` em uma única string,
            #       separada por ponto e vírgula e espaço.
            # Cada item na lista representa um produto ou serviço do agendamento.
            # O método `join()` é utilizado para unir os elementos da lista em uma string.
            # `itens_str` é a lista contendo os nomes dos itens e seus preços.
            itens_resumo = "; ".join(itens_str)

            # Verifica se o filtro inserido pelo usuário está presente
            #       em `itens_resumo` ou no nome do `funcionario`.
            # O filtro é convertido para minúsculas para garantir que a busca
            #       seja insensível a maiúsculas/minúsculas.
            # Se o filtro for encontrado no resumo dos itens ou no nome
            #       do funcionário, o agendamento é adicionado à TreeView.
            if filtro in itens_resumo.lower() or filtro in funcionario.lower():

                # Insere um novo item na Treeview com os dados do agendamento.
                # A árvore é preenchida com os valores dos campos: data, hora,
                #       resumo dos itens e nome do funcionário.
                self.tree.insert("",
                                 "end",
                                 values=(data, hora, itens_resumo, funcionario))

        # Atualiza o texto do rótulo `total_label` para exibir o valor total calculado.
        # O texto é formatado para mostrar o valor como moeda brasileira, com 2 casas decimais.
        # A string f"Total: R$ {total:.2f}" é uma f-string, que insere o
        #       valor da variável `total` com 2 casas decimais.
        # O método `config` é usado para alterar a configuração do widget,
        #       neste caso, o texto do rótulo.
        self.total_label.config(text=f"Total: R$ {total:.2f}")


    # Define o método `limpar_filtro`, responsável por limpar os
    #       filtros aplicados na interface.
    def limpar_filtro(self):

        # Remove o conteúdo da entrada de filtro, deixando-a vazia.
        # `self.filto_entrry.delete(0, "end")` deleta o texto atual no campo de filtro.
        self.filtro_entry.delete(0, "end")

        # Atualiza a lista de atendimentos, refletindo a remoção dos filtros.
        # `self.atualizar_lista()` recarrega os dados na
        #       interface sem os filtros aplicados.
        self.atualizar_lista()


    def abrir_detalhes_atendimento(self, event):

        # Obter o item selecionado
        selecionado = self.tree.selection()

        # Verifica se nenhum item foi selecionado na TreeView
        if not selecionado:

            # Exibe um aviso caso nenhum atendimento tenha sido selecionado
            messagebox.showwarning("Aviso",
                                   "Nenhum atendimento selecionado.")
            return

        # Obter os valores do item selecionado
        # Obtém os valores do item selecionado na Treeview.
        # `selecionado[0]` refere-se ao identificador do item selecionado.
        # O método `self.tree.item()` retorna os valores do item
        #       selecionado na forma de uma tupla.
        # `"values"` obtém os dados associados ao item na Treeview,
        #       como a data, hora, itens e outros.
        item = self.tree.item(selecionado[0], "values")

        try:

            # Extrai os valores dos campos "data", "hora_inicio" e "itens_resumo" da tupla `item`.
            # Estes dados são usados para buscar o atendimento
            #       completo no banco de dados.
            data = item[0]
            hora_inicio = item[1]
            itens_resumo = item[2]

            # Ajustar a lógica para obter detalhes adicionais
            # Realiza uma consulta no banco de dados (`colecao_agendamentos`)
            #       para buscar um atendimento
            #       correspondente à data e hora de início do item selecionado.
            # O método `find_one` retorna o primeiro atendimento que
            #       corresponde aos parâmetros dados.
            atendimento = colecao_agendamentos.find_one({"data": data, "inicio": hora_inicio})

            # Verifica se o atendimento foi encontrado.
            # Caso contrário, exibe uma mensagem de erro informando o usuário.
            if not atendimento:
                messagebox.showerror("Erro",
                                     "Não foi possível localizar os detalhes do atendimento.")
                return

            # Dados adicionais
            # Calcula o valor total somando os preços de todos os itens no atendimento.
            # A expressão `sum()` é usada para somar os preços de cada item.
            # Para cada item, se o item possui pelo menos 3 elementos (verificado com `len(it) > 2`),
            # o preço do item (posição 2) é convertido para float. Caso contrário, o valor será 0.0.
            # O valor total é a soma dos preços de todos os itens.
            valor_total = sum(float(it[2]) if len(it) > 2 and it[2] else 0.0 for it in atendimento.get("itens", []))

            # Calcula a comissão total com base no valor total.
            # A comissão é calculada como 10% do valor total (valor_total * 0.10).
            # A função `round()` é usada para arredondar o valor da comissão para 2 casas decimais.
            comissao_total = round(valor_total * 0.10, 2)

            # Obtém o valor de "hora_fim" do atendimento. Caso não exista esse valor, o
            #       valor padrão será "Desconhecido".
            # A função `get()` é usada para acessar o valor da chave "fim", e
            #       retorna o valor padrão "Desconhecido" se a chave não for encontrada.
            hora_fim = atendimento.get("fim", "Desconhecido")

            # Obtém o nome do funcionário responsável pelo atendimento.
            # Caso não exista esse valor, o valor padrão será "Desconhecido".
            # A função `get()` é usada para acessar o valor da chave "funcionario_nome", e
            #       retorna "Desconhecido" se a chave não for encontrada.
            funcionario = atendimento.get("funcionario_nome", "Desconhecido")

            # Abrir a tela de detalhes
            # Cria uma nova instância da tela de detalhes do histórico do funcionário.
            # A tela exibirá as informações detalhadas do atendimento, incluindo:
            # - `self`: Passa o próprio objeto atual como o argumento pai da nova tela.
            # - `data`: Data do atendimento.
            # - `hora_inicio`: Hora de início do atendimento.
            # - `hora_fim`: Hora de término do atendimento.
            # - `funcionario`: Nome do funcionário responsável pelo atendimento.
            # - `itens_resumo`: Resumo dos itens envolvidos no atendimento.
            # - `valor_total`: Valor total do atendimento.
            # - `comissao_total`: Comissão calculada com base no valor total.
            TelaDetalhesHistoricoFuncionario(
                self,
                data,
                hora_inicio,
                hora_fim,
                funcionario,
                itens_resumo,
                valor_total,
                comissao_total,
            )


        # O bloco `except` captura dois tipos de exceções que podem
        #       ocorrer durante o processamento:
        # 1. `IndexError`: Caso a lista `itens` não tenha o índice esperado.
        # 2. `ValueError`: Caso haja um erro ao tentar converter ou processar os valores.
        #
        # Quando qualquer uma dessas exceções for levantada, o programa irá:
        # - Mostrar uma mensagem de erro com detalhes do tipo da
        #       exceção (utilizando `f"Erro ao processar detalhes: {e}"`).
        # - O `return` interrompe a execução da função ou método,
        #       impedindo que o fluxo continue após o erro.
        except (IndexError, ValueError) as e:
            messagebox.showerror("Erro", f"Erro ao processar detalhes: {e}")
            return



class TelaDetalhesHistoricoFuncionario(tk.Toplevel):

    """
    Exibe os detalhes completos de um atendimento de um funcionário.
    """

    def __init__(self, parent, data, hora_inicio, hora_fim, cliente, itens_resumo, valor, comissao):

        """
        Construtor da classe TelaDetalhesHistoricoFuncionario.

        Este método inicializa a janela de detalhes do
                atendimento de um funcionário.

        Parâmetros:
        - parent: Referência para a janela principal ou pai que chamou esta janela.
        - data: Data do atendimento.
        - hora_inicio: Horário de início do atendimento.
        - hora_fim: Horário de término do atendimento.
        - cliente: Nome do cliente associado ao atendimento.
        - itens_resumo: Resumo dos itens (produtos/serviços) relacionados ao atendimento.
        - valor: Valor total do atendimento.
        - comissao: Comissão total gerada para o funcionário.
        """

        # Chama o construtor da classe base `tk.Toplevel` para inicializar a janela
        # como filha da janela `parent` recebida no parâmetro. Isso garante que esta
        # janela seja criada como uma janela modal ou associada à principal.
        super().__init__(parent)

        # Define o título da janela com o nome "Detalhes do Atendimento".
        self.title("Detalhes do Atendimento")

        # Ajusta o tamanho da janela para preencher a tela inteira.
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Define o fundo da janela com a cor branca.
        self.configure(bg="#FFFFFF")

        # Título da Janela
        # Cria um `ttk.Label` com o texto "Detalhes do Atendimento".
        # `font=("Arial", 20, "bold")` define a fonte como Arial, tamanho 20, e em negrito.
        # `pady=20` adiciona um espaçamento vertical de 20 pixels ao redor do rótulo.
        titulo_label = ttk.Label(self, text="Detalhes do Atendimento", font=("Arial", 20, "bold"))
        titulo_label.pack(pady=20)  # Posiciona o rótulo na parte superior da janela.

        # Frame de Detalhes Gerais
        # Cria um frame para agrupar os elementos de detalhes do atendimento.
        # `padding=10` adiciona um espaçamento interno de 10 pixels em todos os lados do frame.
        # `fill="both"` faz com que o frame preencha a largura e altura disponíveis na janela.
        # `expand=True` permite que o frame se expanda proporcionalmente ao redimensionamento da janela.
        detalhes_frame = ttk.Frame(self, padding=10)
        detalhes_frame.pack(fill="both", expand=True)

        # Informações principais
        # Exibe a data do atendimento
        # Cria um `ttk.Label` para mostrar a data, utilizando o valor de `data`.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `anchor="w"` alinha o texto à esquerda do frame.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        ttk.Label(detalhes_frame,
                  text=f"Data: {data}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)

        # Exibe a hora de início do atendimento
        # Cria um `ttk.Label` para mostrar a hora de início, utilizando o valor de `hora_inicio`.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `anchor="w"` alinha o texto à esquerda do frame.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        ttk.Label(detalhes_frame,
                  text=f"Hora Início: {hora_inicio}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)

        # Exibe a hora de fim do atendimento
        # Cria um `ttk.Label` para mostrar a hora de término, utilizando o valor de `hora_fim`.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `anchor="w"` alinha o texto à esquerda do frame.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        ttk.Label(detalhes_frame,
                  text=f"Hora Fim: {hora_fim}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)

        # Exibe o nome do cliente
        # Cria um `ttk.Label` para mostrar o cliente, utilizando o valor de `cliente`.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `anchor="w"` alinha o texto à esquerda do frame.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        ttk.Label(detalhes_frame,
                  text=f"Atendimento: {cliente}",
                  font=("Arial", 12)).pack(anchor="w", pady=5)

        # Itens do atendimento
        # Exibe o título "Itens"
        # Cria um `ttk.Label` para indicar que a seção a seguir
        #       lista os itens do atendimento.
        # `text="Itens:"` define o texto exibido no rótulo.
        # `font=("Arial", 12, "bold")` utiliza a fonte Arial, tamanho 12, em
        #       negrito para destacar o título.
        # `anchor="w"` alinha o texto à esquerda do frame.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels abaixo do rótulo.
        ttk.Label(detalhes_frame,
                  text="Itens:",
                  font=("Arial", 12, "bold")).pack(anchor="w", pady=10)

        # Cria um frame para conter os itens do atendimento
        # O `itens_frame` será utilizado para organizar os elementos
        #       relacionados à listagem de itens.
        # `fill="both"` faz com que o frame preencha toda a largura e altura disponíveis.
        # `expand=True` permite que o frame seja redimensionado proporcionalmente ao
        #       redimensionamento do frame pai.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels em ambos os lados do frame.
        itens_frame = ttk.Frame(detalhes_frame)
        itens_frame.pack(fill="both", expand=True, padx=10)

        # TreeView para os itens
        # Cria um `Treeview` dentro do `itens_frame` para listar os itens do atendimento.
        # `columns=("nome", "preco")` define as colunas: uma para o nome do item e outra para o preço.
        # `show="headings"` exibe apenas os cabeçalhos das colunas, ocultando a
        #       coluna de identificação padrão.
        treeview = ttk.Treeview(itens_frame,
                                columns=("nome", "preco"), show="headings")

        # Configura o cabeçalho da coluna "nome".
        # `heading("nome", text="Nome do Item")` define o texto do
        #       cabeçalho como "Nome do Item".
        treeview.heading("nome", text="Nome do Item")

        # Configura o cabeçalho da coluna "preco".
        # `heading("preco", text="Preço")` define o texto do cabeçalho como "Preço".
        treeview.heading("preco", text="Preço")

        # Define a largura e o alinhamento da coluna "nome".
        # `column("nome", width=400)` define a largura da coluna como 400 pixels.
        treeview.column("nome", width=400)

        # Define a largura e o alinhamento da coluna "preco".
        # `column("preco", width=150, anchor="center")` define a largura
        #       como 150 pixels e centraliza o texto.
        treeview.column("preco", width=150, anchor="center")

        # Adiciona os itens na TreeView
        # Itera sobre cada item da lista de itens separados por "; ".
        # `itens_resumo.split("; ")` divide os itens em uma lista usando "; " como delimitador.
        for item in itens_resumo.split("; "):

            try:

                # Separa o nome do item e o preço do item.
                # `rsplit(" (R$", 1)` divide a string em duas partes: o nome do item e o preço.
                nome_item, preco_item = item.rsplit(" (R$", 1)

                # Remove o parêntese final do preço e adiciona "R$" como prefixo.
                # `strip(')')` remove o parêntese final do preço.
                preco_item = f"R$ {preco_item.strip(')')}"

                # Insere o item e o preço formatado na `Treeview`.
                # `insert("", "end", values=(nome_item, preco_item))` adiciona
                #       uma nova linha com os valores.
                treeview.insert("", "end", values=(nome_item, preco_item))

            except ValueError:

                # Se houver erro na formatação do item, insere "R$ 0.00" como preço padrão.
                # Adiciona uma linha com o item original e o preço padrão.
                treeview.insert("", "end", values=(item, "R$ 0.00"))

        # Posiciona a `Treeview` dentro do `itens_frame`.
        # `fill="both"` faz com que a `Treeview` preencha a largura e altura disponíveis.
        # `expand=True` permite que a `Treeview` se expanda conforme o
        #       redimensionamento do frame.
        treeview.pack(fill="both", expand=True)

        # Preço total e comissão - Labels destacados
        # Cria um frame para exibir o total do atendimento.
        # `ttk.Frame(detalhes_frame, padding=10)` cria um frame com
        #       espaçamento interno de 10 pixels.
        total_frame = ttk.Frame(detalhes_frame, padding=10)

        # Posiciona o frame total abaixo do `detalhes_frame`.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        # `pady=10` adiciona espaçamento vertical acima e abaixo do frame.
        total_frame.pack(fill="x", pady=10)

        # Cria um rótulo para exibir o valor total do atendimento.
        # `text=f"Valor Total do Atendimento: R$ {valor}"` exibe o
        #       texto com o valor total formatado.
        # `font=("Arial", 14, "bold")` define a fonte como
        #       Arial, tamanho 14, e em negrito.
        # `foreground="green"` altera a cor do texto para verde.
        total_label = ttk.Label(total_frame,
                                text=f"Valor Total do Atendimento: R$ {valor}",
                                font=("Arial", 14, "bold"),
                                foreground="green")

        # Posiciona o rótulo dentro do `total_frame`.
        # `side="left"` alinha o rótulo à esquerda do frame.
        # `padx=20` adiciona espaçamento horizontal de 20 pixels ao
        #       lado esquerdo e direito do rótulo.
        total_label.pack(side="left", padx=20)

        # Cria um rótulo para exibir o valor da comissão.
        # `text=f"Comissão: R$ {comissao}"` exibe o texto com o valor da comissão formatado.
        # `font=("Arial", 14, "bold")` define a fonte como Arial, tamanho 14, e em negrito.
        # `foreground="blue"` altera a cor do texto para azul.
        comissao_label = ttk.Label(total_frame,
                                    text=f"Comissão: R$ {comissao}",
                                    font=("Arial", 14, "bold"),
                                    foreground="blue")

        # Posiciona o rótulo da comissão no lado direito do frame total.
        # `side="right"` alinha o rótulo ao lado direito do frame.
        # `padx=20` adiciona 20 pixels de espaçamento horizontal ao redor do rótulo.
        comissao_label.pack(side="right", padx=20)

        # Cria um botão para fechar a janela.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=10)


# ------------------------------------------------------------
# Tela Relatorios
# ------------------------------------------------------------
class TelaRelatorios(ttk.Frame):

    """
    Classe que representa a tela de relatórios.
    Herda de `ttk.Frame` para criar uma interface gráfica dentro do frame pai.
    """

    def __init__(self, parent):

        """
        Método construtor da classe `TelaRelatorios`.

        Args:
            parent: O widget pai que contém esta tela (geralmente a
                    janela principal ou outro frame).
        """
        # Inicializa o construtor da classe pai (`ttk.Frame`).
        super().__init__(parent)

        # Configura o frame para preencher toda a área disponível.
        # `fill="both"` faz com que o frame preencha tanto a largura
        #       quanto a altura do espaço disponível.
        # `expand=True` permite que o frame cresça proporcionalmente ao
        #       redimensionamento do widget pai.
        self.pack(fill="both", expand=True)

        # Título
        # Adiciona um rótulo (`Label`) no topo do frame principal.
        # `text="Relatórios"` define o texto exibido.
        # `font=("Arial", 16, "bold")` define a fonte como Arial, tamanho 16, em negrito.
        # `side="top"` posiciona o rótulo na parte superior do frame.
        # `anchor="center"` alinha o rótulo no centro horizontal do frame.
        # `pady=10` adiciona 10 pixels de espaçamento vertical acima e abaixo do rótulo.
        titulo_label = ttk.Label(self, text="Relatórios", font=("Arial", 16, "bold"))
        titulo_label.pack(side="top", anchor="center", pady=10)

        # Cria um frame para filtros e organiza sua posição dentro do frame principal.
        # `padding=10` adiciona um preenchimento interno de 10 pixels dentro do frame.
        # `side="top"` posiciona o frame de filtros na parte superior.
        # `fill="x"` faz com que o frame preencha toda a largura do frame principal.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal em ambos os lados do frame.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do frame.
        filtros_frame = ttk.Frame(self, padding=10)
        filtros_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Adiciona um rótulo (`Label`) ao frame de filtros.
        # `text="Cliente:"` define o texto exibido pelo rótulo.
        # `row=0` posiciona o rótulo na primeira linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do rótulo.
        # `sticky="w"` alinha o rótulo ao lado esquerdo (west) da célula na grade.
        ttk.Label(filtros_frame,
                  text="Cliente:").grid(row=0,
                                        column=0,
                                        padx=5,
                                        pady=5,
                                        sticky="w")

        # Cria um campo de entrada (`Entry`) para inserir o nome do cliente.
        # `width=20` define a largura do campo de entrada em aproximadamente 20 caracteres.
        # `row=0` posiciona o campo de entrada na primeira linha da grade do frame.
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do campo.
        self.cliente_entry = ttk.Entry(filtros_frame, width=20)
        self.cliente_entry.grid(row=0, column=1, padx=5, pady=5)

        # Adiciona um rótulo (`Label`) ao frame de filtros para
        #       indicar o campo de "Data Inicial".
        # `text="Data Inicial:"` define o texto exibido pelo rótulo.
        # `row=0` posiciona o rótulo na primeira linha da grade do frame.
        # `column=2` posiciona o rótulo na terceira coluna da grade (contando a partir de 0).
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do rótulo.
        # `sticky="w"` alinha o rótulo ao lado esquerdo (west) da célula na grade.
        ttk.Label(filtros_frame,
                  text="Data Inicial:").grid(row=0,
                                             column=2,
                                             padx=5,
                                             pady=5,
                                             sticky="w")

        # Cria um campo de entrada (`Entry`) para inserir a data inicial.
        # `width=12` define a largura do campo de entrada em aproximadamente 12 caracteres.
        # `row=0` posiciona o campo de entrada na primeira linha da grade do frame.
        # `column=3` posiciona o campo de entrada na quarta coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do campo.
        self.data_inicial_entry = ttk.Entry(filtros_frame, width=12)
        self.data_inicial_entry.grid(row=0, column=3, padx=5, pady=5)

        # Adiciona um rótulo (`Label`) ao frame de filtros para
        #       indicar o campo de "Data Final".
        # `text="Data Final:"` define o texto exibido pelo rótulo.
        # `row=0` posiciona o rótulo na primeira linha da grade do frame.
        # `column=4` posiciona o rótulo na quinta coluna da grade (contando a partir de 0).
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do rótulo.
        # `sticky="w"` alinha o rótulo ao lado esquerdo (west) da célula na grade.
        ttk.Label(filtros_frame,
                  text="Data Final:").grid(row=0,
                                           column=4,
                                           padx=5,
                                           pady=5,
                                           sticky="w")

        # Cria um campo de entrada (`Entry`) para inserir a data final.
        # `width=12` define a largura do campo de entrada em aproximadamente 12 caracteres.
        # `row=0` posiciona o campo de entrada na primeira linha da grade do frame.
        # `column=5` posiciona o campo de entrada na sexta coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do campo.
        self.data_final_entry = ttk.Entry(filtros_frame, width=12)
        self.data_final_entry.grid(row=0, column=5, padx=5, pady=5)

        # Adiciona um rótulo (`Label`) ao frame de filtros para
        #       indicar o campo de "Funcionário".
        # `text="Funcionário:"` define o texto exibido pelo rótulo.
        # `row=1` posiciona o rótulo na segunda linha da grade do frame.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do rótulo.
        # `sticky="w"` alinha o rótulo ao lado esquerdo (west) da célula na grade.
        ttk.Label(filtros_frame,
                  text="Funcionário:").grid(row=1,
                                            column=0,
                                            padx=5,
                                            pady=5,
                                            sticky="w")

        # Cria um campo de entrada (`Entry`) para inserir o nome do funcionário.
        # `width=20` define a largura do campo de entrada em aproximadamente 20 caracteres.
        # `row=1` posiciona o campo de entrada na segunda linha da grade do frame.
        # `column=1` posiciona o campo de entrada na segunda coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do campo.
        self.funcionario_entry = ttk.Entry(filtros_frame, width=20)
        self.funcionario_entry.grid(row=1, column=1, padx=5, pady=5)

        # Adiciona um rótulo (`Label`) ao frame de filtros para
        #       indicar o campo de "Produto/Serviço".
        # `text="Produto/Serviço:"` define o texto exibido pelo rótulo.
        # `row=1` posiciona o rótulo na segunda linha da grade do frame.
        # `column=2` posiciona o rótulo na terceira coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do rótulo.
        # `sticky="w"` alinha o rótulo ao lado esquerdo (west) da célula na grade.
        ttk.Label(filtros_frame,
                  text="Produto/Serviço:").grid(row=1,
                                                column=2,
                                                padx=5,
                                                pady=5,
                                                sticky="w")

        # Cria um campo de entrada (`Entry`) para inserir o nome do produto ou serviço.
        # `width=20` define a largura do campo de entrada em aproximadamente 20 caracteres.
        # `row=1` posiciona o campo de entrada na segunda linha da grade do frame.
        # `column=3` posiciona o campo de entrada na quarta coluna da grade.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal em torno do campo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do campo.
        self.item_entry = ttk.Entry(filtros_frame, width=20)
        self.item_entry.grid(row=1, column=3, padx=5, pady=5)

        # Cria um botão (`Button`) no frame de filtros para
        #       aplicar o filtro nos dados.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar_dados` associa o clique no botão à
        #       execução do método `self.filtrar_dados`.
        # `row=1` posiciona o botão na segunda linha da grade do frame.
        # `column=5` posiciona o botão na sexta coluna da grade.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal em torno do botão.
        # `pady=5` adiciona 5 pixels de espaçamento vertical em torno do botão.
        # `sticky="e"` alinha o botão ao lado direito (east) da célula na grade.
        ttk.Button(filtros_frame,
                   text="Filtrar",
                   command=self.filtrar_dados).grid(row=1,
                                                    column=5,
                                                    padx=10,
                                                    pady=5,
                                                    sticky="e")

        # Cria um frame (`Frame`) para conter a TreeView e a barra de rolagem,
        #       onde os dados filtrados serão exibidos.
        # `padding=10` adiciona 10 pixels de espaçamento interno em torno do frame.
        # `side="top"` posiciona o frame no topo do container principal.
        # `fill="both"` faz com que o frame preencha tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o frame cresça proporcionalmente ao
        #       redimensionamento do container principal.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal em torno do frame.
        # `pady=10` adiciona 10 pixels de espaçamento vertical em torno do frame.
        table_frame = ttk.Frame(self, padding=10)
        table_frame.pack(side="top",
                         fill="both",
                         expand=True,
                         padx=10,
                         pady=10)

        # Cria uma TreeView para exibir os dados dos relatórios no frame `table_frame`.
        # `columns` define as colunas exibidas, especificando seus identificadores.
        # `show="headings"` exibe apenas os cabeçalhos, ocultando a
        #       coluna de hierarquia (índice).
        self.tree = ttk.Treeview(table_frame,
                                columns=("data", "hora", "cliente", "funcionario", "produto", "valor", "custo", "lucro", "comissao"),
                                show="headings")


        # Define o cabeçalho de cada coluna na TreeView.
        # `heading` especifica o identificador da coluna e o
        #       texto exibido no cabeçalho.

        # Define o cabeçalho para a coluna "data" com o texto "Data".
        self.tree.heading("data", text="Data")

        # Define o cabeçalho para a coluna "hora" com o texto "Hora".
        self.tree.heading("hora", text="Hora")

        # Define o cabeçalho para a coluna "cliente" com o texto "Cliente".
        self.tree.heading("cliente", text="Cliente")

        # Define o cabeçalho para a coluna "funcionario" com o texto "Funcionário".
        self.tree.heading("funcionario", text="Funcionário")

        # Define o cabeçalho para a coluna "produto" com o texto "Produto/Serviço".
        self.tree.heading("produto", text="Produto/Serviço")

        # Define o cabeçalho para a coluna "valor" com o texto "Valor (R$)".
        self.tree.heading("valor", text="Valor (R$)")

        # Define o cabeçalho para a coluna "custo" com o texto "Custo (R$)".
        self.tree.heading("custo", text="Custo (R$)")

        # Define o cabeçalho para a coluna "lucro" com o texto "Lucro (R$)".
        self.tree.heading("lucro", text="Lucro (R$)")

        # Define o cabeçalho para a coluna "comissao" com o texto "Comissão (R$)".
        self.tree.heading("comissao", text="Comissão (R$)")

        # Configura as colunas da TreeView, definindo largura e
        #       alinhamento para cada uma delas.

        # Configura a largura da coluna "data" como 100 pixels e
        #       alinha o texto ao centro.
        self.tree.column("data", width=100, anchor="center")

        # Configura a largura da coluna "hora" como 80 pixels e
        #       alinha o texto ao centro.
        self.tree.column("hora", width=80, anchor="center")

        # Configura a largura da coluna "cliente" como 150 pixels e
        #       alinha o texto à esquerda.
        self.tree.column("cliente", width=150, anchor="w")

        # Configura a largura da coluna "funcionario" como 150
        #       pixels e alinha o texto à esquerda.
        self.tree.column("funcionario", width=150, anchor="w")

        # Configura a largura da coluna "produto" como 250 pixels e alinha o texto à esquerda.
        self.tree.column("produto", width=250, anchor="w")

        # Configura a largura da coluna "valor" como 100 pixels e alinha o texto ao centro.
        self.tree.column("valor", width=100, anchor="center")

        # Configura a largura da coluna "custo" como 100 pixels e alinha o texto ao centro.
        self.tree.column("custo", width=100, anchor="center")

        # Configura a largura da coluna "lucro" como 100 pixels e alinha o texto ao centro.
        self.tree.column("lucro", width=100, anchor="center")

        # Configura a largura da coluna "comissao" como 100 pixels e alinha o texto ao centro.
        self.tree.column("comissao", width=100, anchor="center")

        # Cria uma barra de rolagem vertical para a TreeView e a
        #       associa à sua funcionalidade de rolagem.
        # `orient="vertical"` define a orientação como vertical.
        # `command=self.tree.yview` conecta a barra de rolagem ao
        #       movimento vertical da TreeView.
        tree_scroll = ttk.Scrollbar(table_frame,
                                    orient="vertical",
                                    command=self.tree.yview)

        # Configura a TreeView para usar a barra de rolagem criada.
        self.tree.configure(yscroll=tree_scroll.set)

        # Posiciona a TreeView no lado esquerdo do frame `table_frame`.
        # `side="left"` posiciona a TreeView à esquerda.
        # `fill="both"` faz com que a TreeView preencha tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que a TreeView expanda proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem no lado direito do frame `table_frame`.
        # `side="right"` posiciona a barra de rolagem vertical à direita.
        # `fill="y"` faz com que a barra de rolagem preencha toda a altura do frame.
        tree_scroll.pack(side="right", fill="y")

        # Cria um frame para exibir os totais (valores consolidados) na parte inferior da tela.
        # `padding=10` adiciona espaçamento interno de 10 pixels em todas as direções.
        totais_frame = ttk.Frame(self, padding=10)

        # Posiciona o frame dos totais na parte inferior do layout principal.
        # `side="bottom"` posiciona o frame dos totais na parte inferior.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        # `padx=10` adiciona um espaçamento horizontal externo de 10 pixels.
        # `pady=5` adiciona um espaçamento vertical externo de 5 pixels.
        totais_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        # Cria um rótulo (Label) para exibir o valor total consolidado dos registros.
        # `totais_frame` é o frame pai onde o rótulo será inserido.
        # `text="Valor Total: R$ 0.00"` define o texto inicial exibido pelo rótulo.
        # `font=("Arial", 12, "bold")` define a fonte do texto como
        #       Arial, tamanho 12 e em negrito.
        self.label_total_valor = ttk.Label(totais_frame,
                                           text="Valor Total: R$ 0.00",
                                           font=("Arial", 12, "bold"))

        # Posiciona o rótulo dentro do frame `totais_frame`.
        # `side="left"` alinha o rótulo ao lado esquerdo dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal externo de 10 pixels.
        self.label_total_valor.pack(side="left", padx=10)

        # Cria um rótulo (Label) para exibir o custo total consolidado dos registros.
        # `totais_frame` é o frame pai onde o rótulo será inserido.
        # `text="Custo Total: R$ 0.00"` define o texto inicial exibido pelo rótulo.
        # `font=("Arial", 12, "bold")` define a fonte do texto
        #       como Arial, tamanho 12 e em negrito.
        self.label_total_custo = ttk.Label(totais_frame,
                                           text="Custo Total: R$ 0.00",
                                           font=("Arial", 12, "bold"))

        # Posiciona o rótulo dentro do frame `totais_frame`.
        # `side="left"` alinha o rótulo ao lado esquerdo dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal externo de 10 pixels.
        self.label_total_custo.pack(side="left", padx=10)

        # Cria um rótulo (Label) para exibir o lucro total consolidado dos registros.
        # `totais_frame` é o frame pai onde o rótulo será inserido.
        # `text="Lucro Total: R$ 0.00"` define o texto inicial exibido pelo rótulo.
        # `font=("Arial", 12, "bold")` define a fonte do texto
        #       como Arial, tamanho 12 e em negrito.
        self.label_total_lucro = ttk.Label(totais_frame,
                                           text="Lucro Total: R$ 0.00",
                                           font=("Arial", 12, "bold"))

        # Posiciona o rótulo dentro do frame `totais_frame`.
        # `side="left"` alinha o rótulo ao lado esquerdo dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal externo de 10 pixels.
        self.label_total_lucro.pack(side="left", padx=10)

        # Cria um rótulo (Label) para exibir o valor total de comissão
        #       consolidado dos registros.
        # `totais_frame` é o frame pai onde o rótulo será inserido.
        # `text="Comissão Total: R$ 0.00"` define o texto inicial exibido pelo rótulo.
        # `font=("Arial", 12, "bold")` define a fonte do texto
        #       como Arial, tamanho 12 e em negrito.
        self.label_total_comissao = ttk.Label(totais_frame,
                                              text="Comissão Total: R$ 0.00",
                                              font=("Arial", 12, "bold"))

        # Posiciona o rótulo dentro do frame `totais_frame`.
        # `side="left"` alinha o rótulo ao lado esquerdo dentro do frame.
        # `padx=10` adiciona um espaçamento horizontal externo de 10 pixels.
        self.label_total_comissao.pack(side="left", padx=10)

        # Cria um botão (Button) para exportar os dados do relatório para um arquivo Excel.
        # `totais_frame` é o frame pai onde o botão será inserido.
        # `text="Exportar para Excel"` define o texto exibido no botão.
        # `command=self.exportar_excel` associa a função `self.exportar_excel` ao clique no botão.
        ttk.Button(totais_frame,
                   text="Exportar para Excel",
                   command=self.exportar_excel
                    ).pack(

                        # Posiciona o botão dentro do frame `totais_frame`.
                        # `side="right"` alinha o botão ao lado direito do frame.
                        # `padx=10` adiciona um espaçamento horizontal externo de 10 pixels.
                        side="right",
                        padx=10)

        # Carrega os dados iniciais no TreeView e nos totais do relatório.
        # `self.carregar_dados_iniciais()` chama o método responsável por
        #       preencher os dados da interface ao iniciar.
        self.carregar_dados_iniciais()


    def limpar_tree(self):

        """
        Remove todos os itens atualmente exibidos no TreeView.
        Este método é útil para limpar os dados antes de carregar novos,
        garantindo que informações duplicadas ou obsoletas não sejam exibidas.
        """

        # Itera sobre todos os itens filhos no TreeView.
        # `self.tree.get_children()` retorna uma lista de IDs de
        #       todos os itens no TreeView.
        for item in self.tree.get_children():

            # Remove o item atual do TreeView usando o ID retornado.
            self.tree.delete(item)

    def carregar_dados_iniciais(self):

        """
        Carrega os dados iniciais para o TreeView assim
                que a tela de relatórios é aberta.
        Este método busca todos os registros da coleção de relatórios no
                banco de dados e os exibe no TreeView.
        """

        # Chama o método `limpar_tree` para remover qualquer dado existente no TreeView.
        # Isso garante que o TreeView esteja vazio antes de adicionar novos dados.
        self.limpar_tree()

        # Busca todos os documentos da coleção `colecao_relatorios`.
        # `find({})` retorna um cursor com todos os registros.
        relatorios_cursor = colecao_relatorios.find({})

        # Passa o cursor retornado para o método `_popular_treeview`
        #       que será responsável por preencher o TreeView com os dados.
        self._popular_treeview(relatorios_cursor)



    def _popular_treeview(self, relatorios_cursor):

        """
        Popula o TreeView com os dados obtidos do cursor `relatorios_cursor`
                retornado pela consulta no banco de dados.
        Calcula e exibe os totais de valor, custo, lucro e comissão
                dos registros exibidos.
        """

        # Inicializa variáveis para os totais que serão exibidos nos labels de totais.
        total_valor = 0.0  # Total acumulado de valores de venda.
        total_custo = 0.0  # Total acumulado dos custos dos produtos ou serviços.
        total_lucro = 0.0  # Total acumulado do lucro (valor - custo - comissão).
        total_comissao = 0.0  # Total acumulado das comissões pagas.

        # Itera sobre cada documento retornado pelo cursor `relatorios_cursor`.
        # Cada documento representa um relatório ou registro de serviço/produto.
        for rel in relatorios_cursor:

            # Obtém a data do relatório ou serviço. Retorna uma
            #       string vazia se não for encontrada.
            data = rel.get("data", "")

            # Obtém a hora de início do serviço. Retorna uma string
            #       vazia se não for encontrada.
            hora_inicio = rel.get("hora_inicio", "")

            # Obtém o nome do cliente associado ao serviço ou produto.
            # Retorna uma string vazia se não for encontrado.
            cliente = rel.get("cliente", "")

            # Obtém o nome do funcionário responsável pelo serviço.
            # Retorna uma string vazia se não for encontrado.
            funcionario = rel.get("funcionario", "")

            # Obtém o nome do produto ou serviço relacionado ao relatório.
            # Retorna uma string vazia se não for encontrado.
            produto = rel.get("produto_servico", "")

            # Obtém o valor total do item ou serviço. Converte para `float`,
            #       com valor padrão 0.0 caso não seja encontrado.
            valor = float(rel.get("valor", 0.0))

            # Obtém o custo associado ao item ou serviço. Converte para `float`,
            #       com valor padrão 0.0 caso não seja encontrado.
            custo = float(rel.get("custo", 0.0))

            # Obtém o lucro do item ou serviço. Converte para `float`, com
            #       valor padrão 0.0 caso não seja encontrado.
            lucro = float(rel.get("lucro", 0.0))

            # Obtém a comissão paga ao funcionário. Converte para `float`,
            #       com valor padrão 0.0 caso não seja encontrado.
            comissao = float(rel.get("comissao_funcionario", 0.0))

            # Incrementa o valor total com o valor do item ou serviço atual.
            total_valor += valor

            # Incrementa o custo total com o custo do item ou serviço atual.
            total_custo += custo

            # Incrementa o lucro total com o lucro do item ou serviço atual.
            total_lucro += lucro

            # Incrementa o total de comissão com o valor da
            #       comissão do item ou serviço atual.
            total_comissao += comissao

            # Insere os dados do relatório atual na `TreeView`.
            # Os valores são formatados para duas casas decimais, onde aplicável.
            self.tree.insert(
                "",  # Inserção no nível raiz da `TreeView`.
                "end",  # Insere como último filho na hierarquia.
                values=(
                    data,  # Data do serviço/produto.
                    hora_inicio,  # Hora de início do serviço/produto.
                    cliente,  # Nome do cliente.
                    funcionario,  # Nome do funcionário responsável.
                    produto,  # Nome do produto/serviço.
                    f"{valor:.2f}",  # Valor formatado para duas casas decimais.
                    f"{custo:.2f}",  # Custo formatado para duas casas decimais.
                    f"{lucro:.2f}",  # Lucro formatado para duas casas decimais.
                    f"{comissao:.2f}"  # Comissão formatada para duas casas decimais.
                )
            )

        # Atualiza o texto do rótulo que exibe o valor total.
        # Formata o valor total acumulado para exibição em
        #       reais, com duas casas decimais.
        self.label_total_valor.config(text=f"Valor Total: R$ {total_valor:.2f}")

        # Atualiza o texto do rótulo que exibe o custo total.
        # Formata o custo total acumulado para exibição em reais,
        #       com duas casas decimais.
        self.label_total_custo.config(text=f"Custo Total: R$ {total_custo:.2f}")

        # Atualiza o texto do rótulo que exibe o lucro total.
        # Formata o lucro total acumulado para exibição em reais,
        #       com duas casas decimais.
        self.label_total_lucro.config(text=f"Lucro Total: R$ {total_lucro:.2f}")

        # Atualiza o texto do rótulo que exibe o total de comissão.
        # Formata o total de comissão acumulado para exibição em
        #       reais, com duas casas decimais.
        self.label_total_comissao.config(text=f"Comissão Total: R$ {total_comissao:.2f}")



    def filtrar_dados(self):

        """
        Filtra os dados do TreeView com base nos critérios especificados
                nos campos de entrada de filtros.
        Cada campo de filtro é opcional e, caso preenchido, adiciona uma
                condição ao filtro do banco de dados.
        """

        # Limpa os dados existentes no TreeView para evitar
        #       sobreposição de resultados.
        self.limpar_tree()

        # Inicia um dicionário vazio para construir a consulta de
        #       filtro no banco de dados.
        query = {}

        # Adiciona um filtro para o campo "cliente" se o usuário
        #       preencheu a entrada correspondente.
        # Utiliza regex para buscar clientes contendo o texto
        #       digitado (ignora maiúsculas e minúsculas).
        if self.cliente_entry.get():
            query["cliente"] = {"$regex": self.cliente_entry.get(), "$options": "i"}

        # Adiciona um filtro para o campo "funcionário" de forma
        #       similar ao filtro de cliente.
        if self.funcionario_entry.get():
            query["funcionario"] = {"$regex": self.funcionario_entry.get(), "$options": "i"}

        # Adiciona um filtro para a data inicial, garantindo que os
        #       resultados sejam posteriores ou iguais.
        if self.data_inicial_entry.get():
            query["data"] = {"$gte": self.data_inicial_entry.get()}

        # Adiciona um filtro para a data final, atualizando o
        #       dicionário "data" existente ou criando um novo.
        if self.data_final_entry.get():
            query.setdefault("data", {}).update({"$lte": self.data_final_entry.get()})

        # Adiciona um filtro para o campo "produto/serviço" usando
        #       regex para busca parcial.
        if self.item_entry.get():
            query["produto_servico"] = {"$regex": self.item_entry.get(), "$options": "i"}

        # Realiza a consulta no banco de dados com os critérios de
        #       filtro definidos no dicionário `query`.
        relatorios_cursor = colecao_relatorios.find(query)

        # Preenche o TreeView com os resultados retornados pela consulta.
        self._popular_treeview(relatorios_cursor)


    # Define o método para exportar os dados da TreeView
    #       para um arquivo Excel.
    def exportar_excel(self):

        # Coleta todos os dados da TreeView, transformando cada
        #       linha em uma lista de valores.
        # Utiliza o método `self.tree.get_children()` para obter os IDs de todas as linhas.
        dados = [self.tree.item(item, "values") for item in self.tree.get_children()]

        # Verifica se há dados na TreeView. Se a lista `dados` estiver vazia:
        if not dados:

            # Exibe uma mensagem de aviso informando que não há dados para exportar.
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")

            # Interrompe a execução do método retornando `None`.
            return

        # Cria um DataFrame do pandas com os dados coletados da TreeView.
        # As colunas do DataFrame são definidas com nomes descritivos que
        #       representam os dados exibidos na TreeView.
        df = pd.DataFrame(dados, columns=[

            "Data",  # Coluna para a data do registro.
            "Hora",  # Coluna para a hora do registro.
            "Cliente",  # Coluna para o nome do cliente.
            "Funcionário",  # Coluna para o nome do funcionário responsável.
            "Produto/Serviço",  # Coluna para o produto ou serviço relacionado.
            "Valor (R$)",  # Coluna para o valor do item em reais.
            "Custo (R$)",  # Coluna para o custo do item em reais.
            "Lucro (R$)",  # Coluna para o lucro gerado.
            "Comissão (R$)"  # Coluna para a comissão do funcionário em reais.

        ])

        # Salva o DataFrame em um arquivo Excel chamado "relatorio.xlsx".
        # `index=False` evita que a coluna de índices seja incluída no arquivo.
        df.to_excel("relatorio.xlsx", index=False)

        # Exibe uma mensagem de sucesso informando que o relatório
        #       foi exportado com êxito.
        messagebox.showinfo("Sucesso",
                            "Relatório exportado com sucesso.")


# ------------------------------------------------------------
# Tela Funcionarios
# ------------------------------------------------------------
class TelaFuncionarios(ttk.Frame):

    """
    Classe que representa a tela de gerenciamento de funcionários.
    """

    def __init__(self, parent):

        # Chama o construtor da classe pai (`ttk.Frame`) para garantir a
        #       inicialização correta do widget.
        # `super().__init__(parent)` inicializa os atributos
        #       herdados da classe `ttk.Frame`.
        super().__init__(parent)

        # Cria um rótulo (Label) no frame para exibir o título "Funcionários".
        # O texto do rótulo é "Funcionários", formatado com
        #       fonte Arial de tamanho 14 e em negrito.
        # `self` refere-se à instância atual do frame, onde o rótulo será posicionado.
        # `side="top"` posiciona o rótulo na parte superior do frame.
        # `anchor="w"` alinha o texto do rótulo à esquerda (west)
        #       dentro da célula onde está inserido.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal em torno do rótulo.
        # `pady=10` adiciona 10 pixels de espaçamento vertical em torno do rótulo.
        titulo_label = ttk.Label(self, text="Funcionários", font=("Arial", 14, "bold"))
        titulo_label.pack(side="top", anchor="w", padx=10, pady=10)

        # Cria um frame (contêiner) dentro do frame principal
        #       para agrupar os campos de entrada.
        # `self` indica que o frame será criado como um elemento
        #       filho do frame principal.
        # `padding=10` adiciona 10 pixels de espaçamento interno em
        #       todas as direções no frame.
        campos_frame = ttk.Frame(self, padding=10)

        # Posiciona o frame de campos na parte superior do frame principal.
        # `side="top"` alinha o frame no topo do frame principal.
        # `fill="x"` faz com que o frame preencha toda a largura
        #       disponível horizontalmente.
        campos_frame.pack(side="top", fill="x")

        # Adiciona um rótulo (Label) no frame `campos_frame` com o texto "Nome Completo:".
        # Este rótulo serve para identificar o campo de entrada de
        #       texto para o nome completo do funcionário.
        # `row=0` posiciona o rótulo na primeira linha do grid layout.
        # `column=0` posiciona o rótulo na primeira coluna do grid layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula do grid.
        ttk.Label(campos_frame,
                  text="Nome Completo:").grid(row=0,
                                              column=0,
                                              padx=5,
                                              pady=5,
                                              sticky="w")

        # Cria um campo de entrada de texto (Entry) dentro do frame `campos_frame`.
        # `self.nome_entry` permite acessar o campo em outras partes da classe,
        #       como para recuperar ou limpar o texto inserido.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        self.nome_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na primeira linha e segunda
        #       coluna do grid layout no frame `campos_frame`.
        # `row=0` posiciona o campo de entrada na mesma linha que o rótulo correspondente.
        # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo "Nome Completo:".
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)


        # Adiciona um rótulo (Label) no frame `campos_frame` com o texto "Cargo:".
        # Este rótulo serve para identificar o campo de entrada de
        #       texto destinado ao cargo do funcionário.
        # `row=1` posiciona o rótulo na segunda linha do grid layout.
        # `column=0` posiciona o rótulo na primeira coluna do grid layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula do grid.
        ttk.Label(campos_frame,
                  text="Cargo:").grid(row=1,
                                      column=0,
                                      padx=5,
                                      pady=5,
                                      sticky="w")

        # Cria um campo de entrada de texto (Entry) dentro do frame `campos_frame`.
        # `self.cargo_entry` permite acessar o campo em outras partes da
        #       classe, como para recuperar ou limpar o texto inserido.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        self.cargo_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na segunda linha e segunda coluna do
        #       grid layout no frame `campos_frame`.
        # `row=1` posiciona o campo de entrada na mesma linha que o rótulo correspondente.
        # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo "Cargo:".
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        self.cargo_entry.grid(row=1, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) no frame `campos_frame` com o texto "Telefone:".
        # Este rótulo serve para identificar o campo de entrada de
        #       texto destinado ao telefone do funcionário.
        # `row=2` posiciona o rótulo na terceira linha do grid layout.
        # `column=0` posiciona o rótulo na primeira coluna do grid layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula do grid.
        ttk.Label(campos_frame,
                  text="Telefone:").grid(row=2,
                                         column=0,
                                         padx=5,
                                         pady=5,
                                         sticky="w")

        # Cria um campo de entrada de texto (Entry) dentro do frame `campos_frame`.
        # `self.telefone_entry` permite acessar o campo em outras partes da
        #       classe, como para recuperar ou limpar o texto inserido.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        self.telefone_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na terceira linha e segunda
        #       coluna do grid layout no frame `campos_frame`.
        # `row=2` posiciona o campo de entrada na mesma linha
        #       que o rótulo correspondente.
        # `column=1` posiciona o campo na segunda coluna, ao
        #       lado do rótulo "Telefone:".
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e
        #       vertical ao redor do campo.
        self.telefone_entry.grid(row=2, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) no frame `campos_frame` com o texto "E-mail:".
        # Este rótulo serve para identificar o campo de entrada de
        #       texto destinado ao e-mail do funcionário.
        # `row=3` posiciona o rótulo na quarta linha do grid layout.
        # `column=0` posiciona o rótulo na primeira coluna do grid layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula do grid.
        ttk.Label(campos_frame,
                  text="E-mail:").grid(row=3,
                                       column=0,
                                       padx=5,
                                       pady=5,
                                       sticky="w")

        # Cria um campo de entrada de texto (Entry) dentro do frame `campos_frame`.
        # `self.email_entry` permite acessar o campo em outras partes da classe,
        #       como para recuperar ou limpar o texto inserido.
        # `width=30` define a largura do campo de entrada como 30 caracteres.
        self.email_entry = ttk.Entry(campos_frame, width=30)

        # Posiciona o campo de entrada na quarta linha e segunda coluna do
        #       grid layout no frame `campos_frame`.
        # `row=3` posiciona o campo de entrada na mesma linha que o rótulo correspondente.
        # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo "E-mail:".
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) no frame `campos_frame` com o texto "Salário:".
        # Este rótulo serve para identificar o campo de entrada de texto
        #       destinado ao salário do funcionário.
        # `row=4` posiciona o rótulo na quinta linha do grid layout.
        # `column=0` posiciona o rótulo na primeira coluna do grid layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula do grid.
        ttk.Label(campos_frame,
                  text="Salário:").grid(row=4,
                                        column=0,
                                        padx=5,
                                        pady=5,
                                        sticky="w")

        # Cria um campo de entrada de texto (Entry) dentro do frame `campos_frame`.
        # `self.salario_entry` permite acessar o campo em outras partes da
        #       classe, como para recuperar ou limpar o texto inserido.
        # `width=10` define a largura do campo de entrada como 10 caracteres.
        self.salario_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada na quinta linha e segunda coluna do
        #       grid layout no frame `campos_frame`.
        # `row=4` posiciona o campo de entrada na mesma linha que o rótulo correspondente.
        # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo "Salário:".
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        # `sticky="w"` alinha o campo de entrada à esquerda dentro da célula.
        self.salario_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Adiciona um rótulo (Label) no frame `campos_frame` com o texto "Comissão (%):".
        # Este rótulo serve para identificar o campo de entrada destinado ao
        #       percentual de comissão do funcionário.
        # `row=5` posiciona o rótulo na sexta linha do grid layout.
        # `column=0` posiciona o rótulo na primeira coluna do grid layout.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) na célula do grid.
        ttk.Label(campos_frame,
                  text="Comissão (%):").grid(row=5,
                                             column=0,
                                             padx=5,
                                             pady=5,
                                             sticky="w")

        # Cria um campo de entrada de texto (Entry) dentro do frame `campos_frame`.
        # `self.comissao_entry` permite acessar o campo em outras partes da classe,
        #       como para recuperar ou limpar o texto inserido.
        # `width=10` define a largura do campo de entrada como 10 caracteres.
        self.comissao_entry = ttk.Entry(campos_frame, width=10)

        # Posiciona o campo de entrada na sexta linha e segunda coluna do
        #       grid layout no frame `campos_frame`.
        # `row=5` posiciona o campo de entrada na mesma linha que o rótulo correspondente.
        # `column=1` posiciona o campo na segunda coluna, ao lado do rótulo "Comissão (%):".
        # `padx=5` e `pady=5` adicionam espaçamento horizontal e vertical ao redor do campo.
        # `sticky="w"` alinha o campo de entrada à esquerda dentro da célula.
        self.comissao_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Cria um frame para os botões e o posiciona dentro de `campos_frame`.
        # Este frame agrupa os botões de ação para gerenciar funcionários.
        # `row=6` posiciona o frame na sétima linha do grid layout de `campos_frame`.
        # `column=0` posiciona o frame na primeira coluna.
        # `columnspan=2` permite que o frame ocupe duas colunas,
        #       alinhando os botões centralizados.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do frame.
        botoes_frame = ttk.Frame(campos_frame)
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Cria um botão com o texto "Adicionar" e o associa ao método `self.novo_funcionario`.
        # Este botão é usado para adicionar um novo funcionário ao sistema.
        # `side="left"` posiciona o botão à esquerda dentro do `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Adicionar",
                   command=self.novo_funcionario).pack(side="left",
                                                       padx=5)

        # Cria um botão com o texto "Editar" e o associa ao método `self.editar_funcionario`.
        # Este botão é usado para editar os dados de um funcionário selecionado.
        # `side="left"` posiciona o botão à esquerda, ao lado do botão "Adicionar".
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Editar",
                   command=self.editar_funcionario).pack(side="left",
                                                         padx=5)

        # Cria um botão com o texto "Excluir" e o associa ao método `self.excluir_funcionario`.
        # Este botão é usado para excluir um funcionário selecionado do sistema.
        # `side="left"` posiciona o botão à esquerda, ao lado do botão "Editar".
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Excluir",
                   command=self.excluir_funcionario).pack(side="left",
                                                          padx=5)

        # Botão para ver o histórico do Funcionário
        # Cria um botão com o texto "Ver Histórico" e o associa ao
        #       método `self.ver_historico_funcionario`.
        # Este botão é usado para visualizar o histórico do funcionário selecionado.
        # `side="left"` posiciona o botão à esquerda, ao lado dos outros botões no `botoes_frame`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        ttk.Button(botoes_frame,
                   text="Ver Histórico",
                   command=self.ver_historico_funcionario).pack(side="left",
                                                                padx=5)

        # Cria um frame para conter a tabela (Treeview) e o posiciona dentro do layout principal.
        # Este frame organiza visualmente a tabela de funcionários na interface.
        # `side="top"` posiciona o frame no topo do layout principal da tela.
        # `fill="both"` faz com que o frame preencha toda a largura e altura disponíveis.
        # `expand=True` permite que o frame cresça proporcionalmente ao
        #       redimensionamento da janela principal.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do frame.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels ao redor do frame.
        table_frame = ttk.Frame(self)
        table_frame.pack(side="top",
                         fill="both",
                         expand=True,
                         padx=10,
                         pady=10)

        # Cria uma Treeview dentro do `table_frame` para exibir a lista de funcionários.
        # A Treeview utiliza as colunas especificadas para organizar os dados.
        # `columns` define os nomes internos das colunas que serão exibidas.
        # `show="headings"` indica que somente os cabeçalhos das colunas
        #       serão exibidos (sem coluna de índice).
        self.tree = ttk.Treeview(table_frame,
                                columns=("nome", "cargo", "telefone", "email", "salario", "comissao"),
                                show="headings")

        # Configura o cabeçalho da coluna "nome" com o texto exibido "Nome".
        # Esse cabeçalho será exibido no topo da Treeview para
        #       identificar os dados na coluna.
        self.tree.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna "cargo" com o texto exibido "Cargo".
        # Essa configuração segue a mesma lógica para as demais colunas.
        self.tree.heading("cargo", text="Cargo")

        # Configura o cabeçalho da coluna "telefone" com o texto exibido "Telefone".
        self.tree.heading("telefone", text="Telefone")

        # Configura o cabeçalho da coluna "email" com o texto exibido "E-mail".
        self.tree.heading("email", text="E-mail")

        # Configura o cabeçalho da coluna "salario" com o texto exibido "Salário".
        self.tree.heading("salario", text="Salário")

        # Configura o cabeçalho da coluna "comissao" com o texto exibido "Comissão(%)".
        self.tree.heading("comissao", text="Comissão(%)")

        # Cria uma barra de rolagem (Scrollbar) vertical para a Treeview.
        # `orient="vertical"` define que a barra de rolagem será na direção vertical.
        # `command=self.tree.yview` associa a barra de rolagem à
        #       Treeview, permitindo rolar a lista de funcionários.
        scrollbar = ttk.Scrollbar(table_frame,
                                  orient="vertical",
                                  command=self.tree.yview)

        # Configura a Treeview para usar a barra de rolagem vertical criada acima.
        # `yscroll=scrollbar.set` conecta a Treeview à barra de rolagem,
        #       permitindo que o movimento de rolagem seja controlado.
        self.tree.configure(yscroll=scrollbar.set)

        # Posiciona a Treeview dentro do `table_frame` no lado esquerdo.
        # `fill="both"` faz com que a Treeview ocupe tanto a
        #       largura quanto a altura disponíveis.
        # `expand=True` permite que a Treeview cresça proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem vertical ao lado esquerdo da Treeview.
        # `fill="y"` faz com que a barra de rolagem ocupe toda a altura
        #       disponível, permitindo rolar a Treeview.
        scrollbar.pack(side="left", fill="y")

        # Associa o evento de seleção de um item da Treeview à
        #       função `selecionar_item_tree`.
        # Quando o usuário selecionar uma linha na Treeview, a
        #       função `selecionar_item_tree` será chamada.
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item_tree)

        # Carrega os dados dos funcionários no Treeview.
        # A função `carregar_funcionarios` é responsável por preencher a
        #       Treeview com os dados do banco de dados.
        self.carregar_funcionarios()


    def carregar_funcionarios(self):

        # Itera sobre todos os itens atualmente na Treeview.
        # `self.tree.get_children()` retorna uma lista de IDs
        #       dos itens existentes na Treeview.
        for item in self.tree.get_children():

            # Remove cada item da Treeview, garantindo que ela fique
            #       vazia antes de recarregar os dados.
            self.tree.delete(item)

        # Itera sobre todos os documentos da coleção `colecao_funcionarios` no banco de dados.
        # Os resultados são ordenados pelo campo "nome" em ordem alfabética ascendente.
        for f in colecao_funcionarios.find().sort("nome", pymongo.ASCENDING):

            # Insere cada funcionário encontrado no banco de dados na Treeview.
            # `iid=str(f["_id"])` define o ID do item como a string do ObjectId do funcionário.
            # `values=(...)` define os valores que serão exibidos nas colunas da Treeview.
            self.tree.insert(

                "",  # Indica que o item não terá um pai (será inserido na raiz).
                "end",  # Insere o item no final da lista atual de itens.
                iid=str(f["_id"]),  # Define o identificador único do item na Treeview.
                values=(
                    f.get("nome", ""),  # Obtém o nome do funcionário ou uma string vazia se não estiver definido.
                    f.get("cargo", ""),  # Obtém o cargo do funcionário.
                    f.get("telefone", ""),  # Obtém o telefone do funcionário.
                    f.get("email", ""),  # Obtém o e-mail do funcionário.
                    f.get("salario", ""),  # Obtém o salário do funcionário.
                    f.get("comissao", "")  # Obtém a comissão do funcionário.
                )
            )


    # Método que é acionado quando um item da Treeview é selecionado.
    def selecionar_item_tree(self, event=None):

        # Tenta obter o ID do item selecionado na Treeview.
        try:

            # `self.tree.selection()[0]` retorna o primeiro item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Se nenhum item estiver selecionado, sai do
            #       método sem realizar ações.
            return

        # Busca o documento correspondente ao funcionário selecionado no banco de dados.
        f = colecao_funcionarios.find_one({"_id": ObjectId(selecionado)})

        # Se o funcionário for encontrado, preenche os campos com as informações.
        if f:

            # Limpa o campo de nome e insere o nome do funcionário encontrado.
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, f.get("nome", ""))

            # Limpa o campo de cargo e insere o cargo do funcionário encontrado.
            self.cargo_entry.delete(0, "end")
            self.cargo_entry.insert(0, f.get("cargo", ""))

            # Limpa o campo de telefone e insere o telefone do funcionário encontrado.
            self.telefone_entry.delete(0, "end")
            self.telefone_entry.insert(0, f.get("telefone", ""))

            # Limpa o campo de e-mail e insere o e-mail do funcionário encontrado.
            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, f.get("email", ""))

            # Limpa o campo de salário e insere o salário do funcionário
            #       encontrado, formatado como texto.
            self.salario_entry.delete(0, "end")
            self.salario_entry.insert(0, str(f.get("salario", 0.0)))

            # Limpa o campo de comissão e insere a comissão do
            #       funcionário encontrado, formatada como texto.
            self.comissao_entry.delete(0, "end")
            self.comissao_entry.insert(0, str(f.get("comissao", 0.0)))


    # Método para adicionar um novo funcionário ao sistema.
    # Captura os dados inseridos nos campos e os salva no banco de dados.
    def novo_funcionario(self):

        # Obtém o nome do funcionário digitado e remove espaços desnecessários.
        nome = self.nome_entry.get().strip()

        # Obtém o cargo do funcionário digitado e remove espaços desnecessários.
        cargo = self.cargo_entry.get().strip()

        # Obtém o telefone do funcionário digitado e remove espaços desnecessários.
        telefone = self.telefone_entry.get().strip()

        # Obtém o e-mail do funcionário digitado e remove espaços desnecessários.
        email = self.email_entry.get().strip()

        # Obtém o salário do funcionário digitado e remove espaços desnecessários.
        salario = self.salario_entry.get().strip()

        # Obtém a comissão do funcionário digitado e remove espaços desnecessários.
        comissao = self.comissao_entry.get().strip()

        # Verifica se o campo de nome está vazio, exibindo
        #       um erro se necessário.
        if not nome:
            messagebox.showerror("Erro", "Nome do funcionário é obrigatório.")
            return

        # Tenta converter os valores de salário e comissão para float.
        # Se estiver vazio, atribui 0.0 como valor padrão.
        try:

            salario = float(salario) if salario else 0.0
            comissao = float(comissao) if comissao else 0.0

        # Captura erros caso os valores não sejam numéricos e
        #       exibe uma mensagem de erro.
        except ValueError:
            messagebox.showerror("Erro",
                                 "Salário e Comissão devem ser numéricos.")
            return

        # Cria um dicionário `novo` com os dados do funcionário
        #       para ser adicionado ao banco de dados.
        novo = {

            "nome": nome,  # Nome do funcionário.
            "cargo": cargo,  # Cargo do funcionário.
            "telefone": telefone,  # Telefone do funcionário.
            "email": email,  # E-mail do funcionário.
            "salario": salario,  # Salário do funcionário, já convertido para float.
            "comissao": comissao  # Comissão do funcionário em percentual, já convertido para float.

        }

        # Insere o dicionário `novo` na coleção de funcionários no banco de dados.
        colecao_funcionarios.insert_one(novo)

        # Atualiza a exibição da Treeview carregando novamente todos os
        #       funcionários do banco de dados.
        self.carregar_funcionarios()

        # Limpa os campos de entrada para facilitar o
        #       cadastro de novos funcionários.
        self.limpar_campos()

        # Exibe uma mensagem informando que o funcionário foi
        #       adicionado com sucesso.
        messagebox.showinfo("Sucesso",
                            "Funcionário adicionado com sucesso.")


    def limpar_campos(self):

        # Limpa o campo de entrada para o nome do funcionário,
        #       removendo qualquer texto digitado.
        self.nome_entry.delete(0, "end")

        # Limpa o campo de entrada para o cargo do funcionário.
        self.cargo_entry.delete(0, "end")

        # Limpa o campo de entrada para o telefone do funcionário.
        self.telefone_entry.delete(0, "end")

        # Limpa o campo de entrada para o e-mail do funcionário.
        self.email_entry.delete(0, "end")

        # Limpa o campo de entrada para o salário do funcionário.
        self.salario_entry.delete(0, "end")

        # Limpa o campo de entrada para a comissão do funcionário.
        self.comissao_entry.delete(0, "end")


    # Define o método para editar as informações de um
    #       funcionário selecionado na Treeview.
    def editar_funcionario(self):

        try:

            # Obtém o ID do funcionário selecionado na Treeview.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe uma mensagem de erro caso nenhum funcionário esteja selecionado.
            messagebox.showerror("Erro", "Nenhum funcionário selecionado.")
            return

        # Obtém o nome do funcionário a partir do campo de entrada.
        # Utiliza o método strip() para remover quaisquer espaços em
        #       branco extras no início ou no fim.
        nome = self.nome_entry.get().strip()

        # Obtém o cargo do funcionário do campo de entrada, removendo espaços extras.
        cargo = self.cargo_entry.get().strip()

        # Obtém o telefone do funcionário do campo de entrada, removendo espaços extras.
        telefone = self.telefone_entry.get().strip()

        # Obtém o e-mail do funcionário do campo de entrada, removendo espaços extras.
        email = self.email_entry.get().strip()

        # Obtém o salário do funcionário do campo de entrada e remove espaços extras.
        salario = self.salario_entry.get().strip()

        # Obtém a comissão do funcionário do campo de entrada e remove espaços extras.
        comissao = self.comissao_entry.get().strip()

        # Verifica se o nome do funcionário foi informado.
        # Caso o campo esteja vazio, exibe uma mensagem de
        #       erro e encerra o método.
        if not nome:
            messagebox.showerror("Erro",
                                 "Nome do funcionário é obrigatório.")
            return

        try:

            # Converte o valor do salário para um número de ponto flutuante (float).
            # Se o campo estiver vazio, define o valor padrão como 0.0.
            salario = float(salario) if salario else 0.0

            # Converte o valor da comissão para um número de ponto flutuante (float).
            # Se o campo estiver vazio, define o valor padrão como 0.0.
            comissao = float(comissao) if comissao else 0.0

        except ValueError:

            # Caso ocorra um erro ao converter os valores para números,
            # exibe uma mensagem de erro e encerra o método.
            messagebox.showerror("Erro",
                                 "Salário e Comissão devem ser numéricos.")
            return

        # Atualiza as informações do funcionário no banco de dados.
        # O método `update_one` é utilizado para modificar um único documento na coleção.
        # O primeiro argumento é um filtro que localiza o documento pelo `_id`
        #       correspondente ao item selecionado na Treeview.
        # O segundo argumento é um dicionário que contém o operador `$set`,
        #       que define os campos a serem atualizados no documento encontrado.
        colecao_funcionarios.update_one(
            {"_id": ObjectId(selecionado)},  # Localiza o documento pelo `_id`.
            {
                "$set": {  # Define os campos e os valores que serão atualizados no documento.
                    "nome": nome,  # Atualiza o nome do funcionário.
                    "cargo": cargo,  # Atualiza o cargo do funcionário.
                    "telefone": telefone,  # Atualiza o telefone do funcionário.
                    "email": email,  # Atualiza o e-mail do funcionário.
                    "salario": salario,  # Atualiza o salário do funcionário.
                    "comissao": comissao  # Atualiza a comissão do funcionário.
                }
            }
        )

        # Recarrega a lista de funcionários na interface.
        # O método `carregar_funcionarios` é chamado para atualizar a Treeview
        #       com as informações atualizadas do banco de dados.
        self.carregar_funcionarios()

        # Limpa os campos de entrada após a edição.
        # O método `limpar_campos` remove os dados preenchidos nos campos de texto
        #       para que fiquem prontos para uma nova operação ou entrada.
        self.limpar_campos()

        # Exibe uma mensagem informativa para o usuário indicando
        #       que a operação foi bem-sucedida.
        # O `messagebox.showinfo` mostra um alerta modal com o
        #       título "Sucesso" e o texto correspondente.
        messagebox.showinfo("Sucesso",
                            "Funcionário editado com sucesso.")


    # Define o método `excluir_funcionario` que lida com a
    #       exclusão de funcionários selecionados.
    def excluir_funcionario(self):

        # Tenta obter o ID do funcionário selecionado na Treeview.
        # `self.tree.selection()[0]` retorna o primeiro item selecionado.
        try:

            selecionado = self.tree.selection()[0]

        # Caso nenhum item esteja selecionado, captura a exceção `IndexError`.
        except IndexError:

            # Mostra uma mensagem de erro informando que nenhum
            #       funcionário foi selecionado.
            # O método retorna imediatamente, evitando que a execução continue.
            messagebox.showerror("Erro",
                                 "Nenhum funcionário selecionado.")
            return

        # Exibe uma caixa de diálogo de confirmação ao usuário.
        # `messagebox.askyesno` retorna `True` se o usuário clicar
        #       em "Sim" e `False` em "Não".
        resposta = messagebox.askyesno("Confirmar",
                                       "Deseja realmente excluir este funcionário?")

        # Verifica se o usuário confirmou a exclusão.
        if resposta:

            # Deleta o funcionário selecionado da coleção no banco de dados.
            # O ID do funcionário é usado como critério de busca para a exclusão.
            colecao_funcionarios.delete_one({"_id": ObjectId(selecionado)})

            # Atualiza a Treeview para refletir a exclusão do funcionário.
            self.carregar_funcionarios()

            # Limpa os campos de entrada para evitar inconsistências após a exclusão.
            self.limpar_campos()

            # Mostra uma mensagem informando que o funcionário foi excluído com sucesso.
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso.")


    def ver_historico_funcionario(self):

        # Tenta obter o ID do funcionário selecionado na Treeview.
        try:

            # Obtém o identificador do item selecionado.
            selecionado = self.tree.selection()[0]

        except IndexError:

            # Exibe uma mensagem de erro se nenhum funcionário estiver selecionado.
            messagebox.showerror("Erro", "Nenhum funcionário selecionado.")

            # Sai da função caso não haja seleção.
            return

        # Busca no banco de dados o funcionário com o ID selecionado.
        funcionario = colecao_funcionarios.find_one({"_id": ObjectId(selecionado)})

        if funcionario:

            # Se o funcionário for encontrado, abre a tela de histórico.
            # `funcionario.get("nome", "")` obtém o nome do funcionário,
            #       com valor padrão "" se não existir.
            TelaHistoricoFuncionario(self, funcionario.get("nome", ""))


# ------------------------------------------------------------
# Tela Historico Funcionário
# ------------------------------------------------------------
# Define uma classe para a tela de histórico de um funcionário.
# A classe herda de `tk.Toplevel`, que cria uma nova janela na aplicação.
class TelaHistoricoFuncionario(tk.Toplevel):

    # Método construtor da classe.
    # `parent`: Janela ou widget pai.
    # `nome_funcionario`: Nome do funcionário cujo histórico será exibido.
    def __init__(self, parent, nome_funcionario):

        # Chama o construtor da classe pai `tk.Toplevel`.
        super().__init__(parent)

        # Define o título da janela, incluindo o nome do funcionário.
        self.title(f"Histórico do Funcionário: {nome_funcionario}")

        # Define o tamanho da janela para preencher a tela inteira.
        # `winfo_screenwidth` e `winfo_screenheight` obtêm a largura e
        #       altura da tela, respectivamente.
        # `+0+0` posiciona a janela no canto superior esquerdo da tela.
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Configura a cor de fundo da janela para um tom de cinza claro.
        self.configure(bg="#f0f0f0")

        # Armazena o nome do funcionário em um atributo da classe.
        # Isso facilita o acesso ao nome em outros métodos dentro da classe.
        self.nome_funcionario = nome_funcionario

        # Cria um frame para os filtros na parte superior da janela.
        # `ttk.Frame` é um container usado para agrupar widgets relacionados.
        # O frame será usado para inserir campos de filtro e botões.
        # `padding=10` adiciona um espaçamento interno de 10 pixels ao redor do frame.
        filtros_frame = ttk.Frame(self, padding=10)

        # Posiciona o frame na parte superior da janela.
        # `side="top"` posiciona o frame na parte superior.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do frame.
        filtros_frame.pack(side="top", fill="x", pady=10)

        # Adiciona um rótulo (Label) no frame de filtros com o texto "Data Inicial (dd/mm/aaaa):".
        # O rótulo informa ao usuário que o próximo campo é para inserir a data inicial.
        # `row=0` posiciona o rótulo na primeira linha da grade (grid) dentro do frame.
        # `column=0` posiciona o rótulo na primeira coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(filtros_frame,
                  text="Data Inicial (dd/mm/aaaa):").grid(row=0,
                                                          column=0,
                                                          padx=5,
                                                          pady=5,
                                                          sticky="w")

        # Cria uma entrada de texto (`Entry`) no frame de filtros para que o
        #       usuário insira a data inicial.
        # `width=15` define a largura do campo como 15 caracteres.
        self.data_inicial_entry = ttk.Entry(filtros_frame, width=15)

        # Posiciona o campo de entrada na grade do frame de filtros.
        # `row=0` posiciona o campo na primeira linha.
        # `column=1` posiciona o campo na segunda coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do campo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do campo.
        self.data_inicial_entry.grid(row=0, column=1, padx=5, pady=5)

        # Adiciona um rótulo (Label) no frame de filtros com o
        #       texto "Data Final (dd/mm/aaaa):".
        # O rótulo informa ao usuário que o próximo campo é para inserir a data final.
        # `row=0` posiciona o rótulo na primeira linha da grade (grid) dentro do frame.
        # `column=2` posiciona o rótulo na terceira coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(filtros_frame,
                  text="Data Final (dd/mm/aaaa):").grid(row=0,
                                                        column=2,
                                                        padx=5,
                                                        pady=5,
                                                        sticky="w")

        # Cria uma entrada de texto (`Entry`) no frame de filtros para
        #       que o usuário insira a data final.
        # `width=15` define a largura do campo como 15 caracteres.
        self.data_final_entry = ttk.Entry(filtros_frame, width=15)

        # Posiciona o campo de entrada na grade do frame de filtros.
        # `row=0` posiciona o campo na primeira linha.
        # `column=3` posiciona o campo na quarta coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do campo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do campo.
        self.data_final_entry.grid(row=0, column=3, padx=5, pady=5)

        # Adiciona um rótulo (Label) no frame de filtros com o texto "Produto/Serviço:".
        # O rótulo informa ao usuário que o próximo campo é para inserir um produto ou serviço.
        # `row=0` posiciona o rótulo na primeira linha da grade (grid) dentro do frame.
        # `column=4` posiciona o rótulo na quinta coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(filtros_frame,
                  text="Produto/Serviço:").grid(row=0,
                                                column=4,
                                                padx=5,
                                                pady=5,
                                                sticky="w")

        # Cria uma entrada de texto (`Entry`) no frame de filtros para que o
        #       usuário insira o nome do produto ou serviço.
        # `width=20` define a largura do campo como 20 caracteres.
        self.item_entry = ttk.Entry(filtros_frame, width=20)

        # Posiciona o campo de entrada na grade do frame de filtros.
        # `row=0` posiciona o campo na primeira linha.
        # `column=5` posiciona o campo na sexta coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do campo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do campo.
        self.item_entry.grid(row=0, column=5, padx=5, pady=5)

        # Adiciona um rótulo (Label) no frame de filtros com o texto "Cliente:".
        # O rótulo informa ao usuário que o próximo campo é destinado para inserir o nome do cliente.
        # `row=0` posiciona o rótulo na primeira linha da grade (grid) dentro do frame.
        # `column=6` posiciona o rótulo na sétima coluna (considerando índice zero).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do rótulo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do rótulo.
        # `sticky="w"` alinha o texto do rótulo à esquerda (west) dentro da célula da grade.
        ttk.Label(filtros_frame,
                  text="Cliente:").grid(row=0,
                                        column=6,
                                        padx=5,
                                        pady=5,
                                        sticky="w")

        # Cria uma entrada de texto (`Entry`) no frame de filtros para
        #       que o usuário insira o nome do cliente.
        # `width=20` define a largura do campo como 20 caracteres.
        self.cliente_entry = ttk.Entry(filtros_frame, width=20)

        # Posiciona o campo de entrada na grade do frame de filtros.
        # `row=0` posiciona o campo na primeira linha.
        # `column=7` posiciona o campo na oitava coluna.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels em volta do campo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do campo.
        self.cliente_entry.grid(row=0, column=7, padx=5, pady=5)

        # Adiciona um botão (Button) no frame de filtros com o texto "Buscar".
        # O botão executa o comando `self.atualizar_lista` quando clicado.
        # `row=0` posiciona o botão na primeira linha da grade dentro do frame de filtros.
        # `column=8` posiciona o botão na nona coluna.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels em volta do botão.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels em volta do botão.
        ttk.Button(filtros_frame,
                   text="Buscar",
                   command=self.atualizar_lista).grid(row=0,
                                                      column=8,
                                                      padx=10,
                                                      pady=5)

        # Cria um frame para conter a TreeView (tabela) onde serão exibidos os dados.
        # `self` indica que o frame será filho do frame principal da janela atual.
        tree_frame = ttk.Frame(self)

        # Posiciona o frame da TreeView na interface.
        # `fill="both"` faz com que o frame preencha tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que o frame cresça proporcionalmente ao
        #       redimensionamento da janela.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels em volta do frame.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels em volta do frame.
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria uma TreeView (tabela) dentro do frame `tree_frame` para
        #       exibir os dados de histórico.
        # `columns` define as colunas da tabela com os respectivos
        #       identificadores ("data", "hora", etc.).
        # `show="headings"` remove a coluna inicial padrão e exibe
        #       apenas os cabeçalhos das colunas definidas.
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("data", "hora", "cliente", "itens", "valor", "comissao"),
                                 show="headings")

        # Define o texto do cabeçalho da coluna "data" como "Data".
        self.tree.heading("data", text="Data")

        # Define o texto do cabeçalho da coluna "hora" como "Hora".
        self.tree.heading("hora", text="Hora")

        # Define o texto do cabeçalho da coluna "cliente" como "Cliente".
        self.tree.heading("cliente", text="Cliente")

        # Define o texto do cabeçalho da coluna "itens" como "Itens (Produtos/Serviços)".
        self.tree.heading("itens", text="Itens (Produtos/Serviços)")

        # Define o texto do cabeçalho da coluna "valor" como "Valor (R$)".
        self.tree.heading("valor", text="Valor (R$)")

        # Define o texto do cabeçalho da coluna "comissao" como "Comissão (R$)".
        self.tree.heading("comissao", text="Comissão (R$)")

        # Define a largura e o alinhamento do conteúdo da coluna "data".
        # `width=100` especifica a largura da coluna em pixels.
        # `anchor="center"` alinha o conteúdo da coluna ao centro.
        self.tree.column("data", width=100, anchor="center")

        # Define a largura e o alinhamento do conteúdo da coluna "hora".
        # `width=80` especifica a largura da coluna em pixels.
        # `anchor="center"` alinha o conteúdo da coluna ao centro.
        self.tree.column("hora", width=80, anchor="center")

        # Define a largura e o alinhamento do conteúdo da coluna "cliente".
        # `width=150` especifica a largura da coluna em pixels.
        # `anchor="center"` alinha o conteúdo da coluna ao centro.
        self.tree.column("cliente", width=150, anchor="center")

        # Define a largura e o alinhamento do conteúdo da coluna "itens".
        # `width=400` especifica a largura da coluna em pixels.
        # `anchor="w"` alinha o conteúdo da coluna à esquerda (west).
        self.tree.column("itens", width=400, anchor="w")

        # Define a largura e o alinhamento do conteúdo da coluna "valor".
        # `width=100` especifica a largura da coluna em pixels.
        # `anchor="center"` alinha o conteúdo da coluna ao centro.
        self.tree.column("valor", width=100, anchor="center")

        # Define a largura e o alinhamento do conteúdo da coluna "comissao".
        # `width=100` especifica a largura da coluna em pixels.
        # `anchor="center"` alinha o conteúdo da coluna ao centro.
        self.tree.column("comissao", width=100, anchor="center")

        # Cria uma barra de rolagem vertical para a TreeView.
        # `tree_frame` é o frame que contém a TreeView.
        # `orient="vertical"` define a orientação da barra de rolagem como vertical.
        # `command=self.tree.yview` associa a barra de rolagem ao
        #       movimento vertical da TreeView.
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)

        # Configura a TreeView para utilizar a barra de rolagem.
        # `yscroll=tree_scroll.set` conecta a barra de rolagem vertical à TreeView.
        self.tree.configure(yscroll=tree_scroll.set)

        # Posiciona a TreeView dentro do frame `tree_frame`.
        # `side="left"` alinha a TreeView à esquerda do frame.
        # `fill="both"` faz com que a TreeView preencha a largura e
        #       altura disponíveis.
        # `expand=True` permite que a TreeView expanda proporcionalmente ao
        #       redimensionamento do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Posiciona a barra de rolagem vertical no frame `tree_frame`.
        # `side="right"` alinha a barra de rolagem à direita do frame.
        # `fill="y"` faz com que a barra de rolagem preencha toda a altura do frame.
        tree_scroll.pack(side="right", fill="y")

        # Frame para os totais
        # Cria um frame para exibir os totais de informações no rodapé.
        # `self` refere-se à janela principal onde o frame será posicionado.
        # `padding=10` adiciona um espaçamento interno de 10 pixels em
        #       todos os lados do frame.
        totais_frame = ttk.Frame(self, padding=10)

        # Posiciona o frame `totais_frame` na parte inferior da janela.
        # `side="bottom"` alinha o frame na parte inferior.
        # `fill="x"` faz com que o frame preencha toda a largura disponível.
        totais_frame.pack(side="bottom", fill="x")

        # Cria um rótulo para exibir a quantidade de atendimentos.
        # `totais_frame` é o frame onde o rótulo será adicionado.
        # `text="Atendimentos: 0"` define o texto inicial do rótulo.
        # `font=("Arial", 12, "bold")` aplica uma fonte Arial, tamanho 12, em negrito.
        self.label_qtde = ttk.Label(totais_frame, text="Atendimentos: 0", font=("Arial", 12, "bold"))

        # Posiciona o rótulo `self.label_qtde` dentro do frame `totais_frame`.
        # `side="left"` alinha o rótulo à esquerda do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels em
        #       ambos os lados do rótulo.
        self.label_qtde.pack(side="left", padx=10)

        # Cria um rótulo para exibir o valor total de todos os atendimentos.
        # `totais_frame` é o frame onde o rótulo será posicionado.
        # `text="Total: R$ 0.00"` define o texto inicial do rótulo.
        # `font=("Arial", 12, "bold")` aplica a fonte Arial, tamanho 12, em negrito.
        # `foreground="green"` altera a cor do texto para verde, indicando destaque positivo.
        self.label_total = ttk.Label(totais_frame,
                                    text="Total: R$ 0.00",
                                    font=("Arial", 12, "bold"),
                                    foreground="green")

        # Posiciona o rótulo `self.label_total` no frame `totais_frame`.
        # `side="right"` alinha o rótulo à direita do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do rótulo.
        self.label_total.pack(side="right", padx=10)

        # Cria um rótulo para exibir o valor total das comissões.
        # `totais_frame` é o frame onde o rótulo será posicionado.
        # `text="Comissão Total: R$ 0.00"` define o texto inicial do rótulo.
        # `font=("Arial", 12, "bold")` aplica a fonte Arial, tamanho 12, em negrito.
        # `foreground="blue"` altera a cor do texto para azul,
        #       destacando o valor das comissões.
        self.label_comissao = ttk.Label(totais_frame,
                                        text="Comissão Total: R$ 0.00",
                                        font=("Arial", 12, "bold"),
                                        foreground="blue")

        # Posiciona o rótulo `self.label_comissao` no frame `totais_frame`.
        # `side="right"` alinha o rótulo à direita do frame.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do rótulo.
        self.label_comissao.pack(side="right", padx=10)

        # Evento de duplo clique na TreeView
        # Associa um evento ao TreeView `self.tree` para detectar cliques duplos.
        # `<Double-1>` é o evento de clique duplo do botão esquerdo do mouse.
        # `self.abrir_detalhes_atendimento` é o método que será
        #       executado ao detectar o evento.
        # Isso permite que o usuário visualize os detalhes de um
        #       atendimento clicando duas vezes em uma linha.
        self.tree.bind("<Double-1>", self.abrir_detalhes_atendimento)

        # Atualiza a lista inicial de atendimentos no TreeView.
        # `self.atualizar_lista()` carrega e exibe os dados
        #       disponíveis na interface.
        # Esse método é chamado para garantir que o TreeView seja
        #       preenchido logo ao abrir a tela.
        self.atualizar_lista()


    # Define o método para abrir detalhes de um atendimento
    #       selecionado na TreeView.
    def abrir_detalhes_atendimento(self, event):

        # Obtém o item atualmente selecionado na TreeView.
        selecionado = self.tree.selection()

        # Verifica se algum item foi selecionado. Caso contrário,
        #       exibe um aviso ao usuário.
        if not selecionado:

            # Exibe uma mensagem de aviso se nenhum atendimento estiver selecionado.
            messagebox.showwarning("Aviso", "Nenhum atendimento selecionado.")

            # Retorna imediatamente para interromper a execução do método.
            return

        # Obter valores do item selecionado
        # Obtém os valores do item selecionado na TreeView.
        item = self.tree.item(selecionado[0], "values")

        try:

            # Extrai a data do atendimento a partir do item selecionado.
            data = item[0]

            # Extrai a hora de início do atendimento.
            hora_inicio = item[1]

            # Obtém o nome do cliente associado ao atendimento.
            cliente = item[2]

            # Coleta o resumo dos itens atendidos (produtos/serviços).
            itens_resumo = item[3]

            # Converte o valor total do atendimento para um
            #       número de ponto flutuante.
            valor = float(item[4])

            # Converte a comissão associada ao atendimento para ponto flutuante.
            comissao = float(item[5])

        # Tratamento de exceções para índices fora do intervalo.
        except IndexError:

            # Exibe uma mensagem de erro ao usuário caso os dados do
            #       atendimento sejam incompletos.
            messagebox.showerror("Erro",
                                 "Dados incompletos no atendimento selecionado.")

            # Interrompe a execução do método.
            return

        # Tratamento de exceções para erros de conversão de valores numéricos.
        except ValueError:

            # Exibe uma mensagem de erro ao usuário caso ocorra um
            #       problema ao converter valores.
            messagebox.showerror("Erro",
                                 "Erro ao converter valores numéricos.")

            # Interrompe a execução do método.
            return

        # Buscar a hora de fim no banco de dados
        # Consulta o banco de dados para buscar o atendimento com
        #       base na data e hora de início.
        atendimento = colecao_agendamentos.find_one({"data": data, "inicio": hora_inicio})

        # Verifica se o atendimento foi encontrado no banco.
        if not atendimento:

            # Exibe uma mensagem de erro caso os detalhes do atendimento
            #       não sejam localizados.
            messagebox.showerror("Erro",
                                 "Não foi possível localizar os detalhes do atendimento.")

            # Interrompe a execução do método.
            return

        # Obtém a hora de término do atendimento. Caso não esteja
        #       disponível, retorna "Desconhecido".
        hora_fim = atendimento.get("fim", "Desconhecido")

        # Exibe os detalhes completos
        # Inicializa uma nova janela do tipo `TelaDetalhesHistoricoFuncionario`
        #       para exibir os detalhes do atendimento.
        TelaDetalhesHistoricoFuncionario(

            self,  # Define a janela atual como pai da nova janela.
            data,  # Passa a data do atendimento para a nova janela.
            hora_inicio,  # Passa a hora de início do atendimento.
            hora_fim,  # Passa a hora de fim do atendimento.
            cliente,  # Passa o nome do cliente associado ao atendimento.
            itens_resumo,  # Passa o resumo dos itens atendidos (produtos/serviços).
            valor,  # Passa o valor total do atendimento.
            comissao  # Passa o valor da comissão correspondente.

        )


    def atualizar_lista(self):

        # Limpa todos os itens da TreeView para que novos dados possam ser carregados.
        # `self.tree.get_children()` retorna uma lista de todos os itens na TreeView.
        # O loop itera sobre esses itens e os remove com `self.tree.delete(i)`.
        # Isso evita que dados duplicados sejam exibidos na interface.
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Ler filtros
        # Obtém a data inicial inserida no campo de texto, removendo
        #       espaços extras no início e no final.
        # O método `strip()` é usado para garantir que não haja
        #       espaços em branco indesejados.
        data_inicial = self.data_inicial_entry.get().strip()

        # Obtém a data final inserida no campo de texto, aplicando o mesmo
        #       tratamento de remoção de espaços extras.
        data_final = self.data_final_entry.get().strip()

        # Obtém o filtro de item/produto inserido no campo de texto.
        # Converte o texto para letras minúsculas usando `lower()` para
        #       facilitar comparações insensíveis a maiúsculas/minúsculas.
        item_filtro = self.item_entry.get().strip().lower()

        # Obtém o filtro de cliente inserido no campo de texto.
        # Também converte para letras minúsculas para garantir
        #       comparações consistentes.
        cliente_filtro = self.cliente_entry.get().strip().lower()

        # Exibe no console as datas inicial e final fornecidas pelo
        #       usuário para fins de depuração.
        # Isso ajuda a confirmar os valores obtidos dos campos de entrada.
        print(f"Data Inicial: {data_inicial}, Data Final: {data_final}")

        # Define uma consulta (query) para buscar os agendamentos
        #       relacionados ao funcionário selecionado.
        # A consulta inclui o nome do funcionário (`funcionario_nome`) e
        #       o status "Finalizado".
        query = {

            # Filtra os agendamentos pelo nome do funcionário.
            "funcionario_nome": self.nome_funcionario,

            # Garante que apenas agendamentos finalizados sejam considerados.
            "status": "Finalizado"

        }

        # Executa a consulta na coleção `colecao_agendamentos` e
        #       converte os resultados em uma lista.
        # Isso permite manipular os dados facilmente em memória.
        agendamentos = list(colecao_agendamentos.find(query))

        # Verifica se o campo `data_inicial` possui algum valor preenchido.
        if data_inicial:

            try:

                # Tenta converter a string fornecida para um objeto `date` no formato dd/mm/aaaa.
                data_inicial = datetime.datetime.strptime(data_inicial, "%d/%m/%Y").date()

            except ValueError:

                # Exibe uma mensagem de erro caso o valor informado não
                #       esteja no formato esperado.
                messagebox.showerror("Erro", "Data inicial inválida. Use o formato dd/mm/aaaa.")

                # Interrompe a execução da função para evitar erros subsequentes.
                return

        # Verifica se o campo `data_final` possui algum valor preenchido.
        if data_final:

            try:

                # Tenta converter a string fornecida para um objeto `date` no formato dd/mm/aaaa.
                data_final = datetime.datetime.strptime(data_final, "%d/%m/%Y").date()

            except ValueError:

                # Exibe uma mensagem de erro caso o valor informado não esteja no formato esperado.
                messagebox.showerror("Erro", "Data final inválida. Use o formato dd/mm/aaaa.")

                # Interrompe a execução da função para evitar erros subsequentes.
                return

        # Lista para armazenar os agendamentos que atendem aos critérios de filtro.
        agendamentos_filtrados = []

        # Itera sobre cada agendamento recuperado da consulta no banco de dados.
        for ag in agendamentos:

            try:

                # Tenta converter a string de data do agendamento no
                #       formato dd/mm/yyyy para um objeto `date`.
                ag_data = datetime.datetime.strptime(ag["data"], "%d/%m/%Y").date()

                # Verifica se a data do agendamento é anterior à `data_inicial`
                #       fornecida. Se for, pula para o próximo.
                if data_inicial and ag_data < data_inicial:
                    continue

                # Verifica se a data do agendamento é posterior à `data_final`
                #       fornecida. Se for, pula para o próximo.
                if data_final and ag_data > data_final:
                    continue

                # Adiciona o agendamento à lista filtrada caso
                #       passe pelas validações.
                agendamentos_filtrados.append(ag)

            except (ValueError, KeyError):

                # Em caso de erro de conversão de data ou chave ausente,
                #       registra o problema e ignora o agendamento.
                print(f"Data inválida em agendamento: {ag}")
                continue

        # Lista para armazenar os resultados finais após os filtros.
        resultados = []

        # Itera sobre cada agendamento que passou pelos filtros de data.
        for ag in agendamentos_filtrados:

            # Obtém os itens do agendamento ou inicializa como uma
            #       lista vazia, caso não existam.
            itens = ag.get("itens", [])

            # Converte o nome do cliente para letras minúsculas
            #       para facilitar a comparação.
            cliente = ag.get("cliente", "").lower()

            # Verifica se o filtro de item foi fornecido e se corresponde a pelo menos um item.
            # Utiliza `any` para verificar se `item_filtro` está contido no nome de algum item.
            if item_filtro and not any(item_filtro in it[1].lower() for it in itens):

                # Se nenhum item corresponder, pula para o próximo agendamento.
                continue

            # Verifica se o filtro de cliente foi fornecido e se
            #       corresponde ao nome do cliente.
            if cliente_filtro and cliente_filtro not in cliente:

                # Se o cliente não corresponder, pula para o próximo agendamento.
                continue

            # Se todos os filtros forem atendidos, adiciona o
            #       agendamento à lista de resultados.
            resultados.append(ag)

        # Inicializa variáveis para armazenar os totais gerais.
        total_geral = 0.0  # Total do valor dos agendamentos.
        total_comissao = 0.0  # Total da comissão dos funcionários.

        # Itera sobre os agendamentos que passaram por todos os filtros.
        for ag in resultados:

            # Obtém a data do agendamento como string ou usa
            #       uma string vazia como padrão.
            data_str = ag.get("data", "")

            # Obtém a hora de início do agendamento como string ou
            #       usa uma string vazia como padrão.
            hora_str = ag.get("inicio", "")

            # Obtém o nome do cliente ou usa "Desconhecido" como padrão.
            cliente_nome = ag.get("cliente", "Desconhecido")

            # Obtém o valor total do agendamento como um float ou usa 0.0 como padrão.
            valor_total = float(ag.get("valor_total", 0.0))

            # Obtém a comissão do funcionário como um float ou usa 0.0 como padrão.
            comissao = float(ag.get("comissao_funcionario", 0.0))

            # Acumula o valor total no total geral.
            total_geral += valor_total

            # Acumula a comissão no total de comissões.
            total_comissao += comissao

            # Converte a lista de itens do agendamento em uma string formatada.
            # Cada item é exibido no formato "nome do item (R$ preço)".
            itens_str = "; ".join([f"{it[1]} (R${it[2]})" for it in ag.get("itens", [])])

            # Insere os valores do agendamento na TreeView.
            # A TreeView exibe uma linha com as seguintes colunas:
            # - Data do agendamento.
            # - Hora do início do agendamento.
            # - Nome do cliente.
            # - Lista de itens comprados no agendamento.
            # - Valor total do agendamento, formatado como moeda.
            # - Comissão associada ao agendamento, formatada como moeda.
            self.tree.insert("", "end", values=(
                data_str,  # Data do agendamento.
                hora_str,  # Hora do início do agendamento.
                cliente_nome,  # Nome do cliente.
                itens_str,  # Lista de itens no agendamento.
                f"{valor_total:.2f}",  # Valor total, formatado.
                f"{comissao:.2f}"  # Comissão, formatada.
            ))

        # Atualizar labels
        # Obtém a quantidade de atendimentos filtrados.
        qtde = len(resultados)

        # Atualiza o texto do rótulo que exibe a quantidade de atendimentos.
        # Formato: "Atendimentos: {qtde}".
        self.label_qtde.config(text=f"Atendimentos: {qtde}")

        # Atualiza o texto do rótulo que exibe o total geral dos atendimentos.
        # O total geral é formatado como moeda (R$ {valor:.2f}).
        self.label_total.config(text=f"Total: R$ {total_geral:.2f}")

        # Atualiza o texto do rótulo que exibe a soma total das comissões.
        # A comissão total é formatada como moeda (R$ {valor:.2f}).
        self.label_comissao.config(text=f"Comissão Total: R$ {total_comissao:.2f}")








# ------------------------------------------------------------
# Execução do Sistema
# ------------------------------------------------------------

# Instancia a classe `Login`, que representa a janela inicial do aplicativo.
# A variável `app` agora contém a referência ao objeto da classe `Login`.
app = Login()

# Inicia o loop principal da interface gráfica.
# `mainloop()` mantém a janela aberta, processando eventos
#       do usuário (como cliques e teclas).
app.mainloop()