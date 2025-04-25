# Importa o módulo tkinter, usado para criar interfaces gráficas no Python.
import tkinter as tk

# Importa o ttk (para widgets estilizados) e messagebox (para
# exibir caixas de mensagem).
from tkinter import ttk, messagebox

from pymongo.synchronous.network import command
# Importa o Calendar da biblioteca tkcalendar para exibir e selecionar datas.
from tkcalendar import Calendar

# Importa o MongoClient, usado para conectar e interagir com o banco de dados MongoDB.
from pymongo import MongoClient

# Importa ObjectId para manipular os identificadores únicos gerados pelo MongoDB.
from bson.objectid import ObjectId

# Importa o módulo datetime, usado para trabalhar com datas e horários no código.
import datetime


# Define a classe principal do sistema de agendamento de consultas.
class SistemaAgendamentoConsultas:

    # Método inicializador da classe, responsável por configurar a
    # janela principal e suas propriedades.
    def __init__(self, janela):

        # Define o atributo da janela principal como o parâmetro recebido.
        self.janela = janela

        # Define o título da janela principal.
        self.janela.title("Sistema de Agendamento de Consultas")

        # Define a janela para abrir maximizada na tela.
        self.janela.state('zoomed')

        # Configura o fundo da janela principal com uma cor padrão cinza claro (#f0f0f0).
        self.janela.configure(bg="#f0f0f0")

        # Conexão com MongoDB
        # Cria uma instância do cliente MongoDB para se conectar ao banco de dados local.
        self.cliente_mongo = MongoClient("mongodb://localhost:27017/")

        # Acessa o banco de dados chamado "agendamento_db" dentro do MongoDB.
        self.bd = self.cliente_mongo["agendamento_db"]

        # Acessa a coleção "clientes" dentro do banco de dados.
        self.colecao_clientes = self.bd["clientes"]

        # Acessa a coleção "medicos" dentro do banco de dados.
        self.colecao_medicos = self.bd["medicos"]

        # Acessa a coleção "consultas" dentro do banco de dados.
        self.colecao_consultas = self.bd["consultas"]

        # Criar Menus
        # Chama o método para criar os menus da aplicação.
        self.criar_menus()

        # Estilo ttk
        # Cria uma instância do estilo ttk para personalizar os widgets.
        style = ttk.Style()

        # Configura o estilo da Treeview (tabela) com fonte Arial de
        # tamanho 11 e altura das linhas 25.
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        # Configura o estilo do cabeçalho da Treeview com fonte Arial
        # de tamanho 12 e negrito.
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Configura o estilo dos botões ttk com fonte Arial de tamanho 11.
        style.configure("TButton", font=("Arial", 11))

        # Frame principal
        # Cria o frame principal que atuará como o contêiner principal da janela.
        # Define sua cor de fundo e o preenchimento.
        frame_principal = tk.Frame(self.janela, bg="#f0f0f0")

        # Configura o frame principal para preencher tanto vertical
        # quanto horizontalmente o espaço disponível e permitir expansão.
        frame_principal.pack(fill='both',
                             expand=True,
                             padx=20,
                             pady=20)

        # Frame esquerda
        # Cria um subframe à esquerda dentro do frame principal para
        # componentes específicos, como listas ou formulários.
        frame_esquerda = tk.Frame(frame_principal, bg="#f0f0f0")

        # Posiciona o frame esquerda no lado esquerdo, preenchendo verticalmente,
        # com um preenchimento horizontal e vertical especificado.
        frame_esquerda.pack(side=tk.LEFT,
                            fill='y',
                            padx=20)

        # Frame direita
        # Cria um subframe à direita dentro do frame principal para outros
        # componentes, para detalhamento ou entrada de dados.
        frame_direita = tk.Frame(frame_principal,
                                 bg="#f0f0f0")

        # Posiciona o frame direita no lado direito, permitindo que ele expanda e
        # preencha o espaço tanto horizontal quanto verticalmente.
        frame_direita.pack(side=tk.RIGHT,
                           fill='both',
                           expand=True,
                           padx=20)

        # Calendário principal
        # Obtém a data atual do sistema para usar como configuração padrão no calendário.
        hoje = datetime.date.today()

        # Cria uma instância de Calendar dentro do frame esquerda,
        # configurada para permitir a seleção de dias.
        # Configura o calendário para mostrar o ano, mês e dia atuais,
        # formatando a data como ano-mês-dia.
        self.calendario = Calendar(frame_esquerda,
                                   selectmode='day',
                                   year=hoje.year,
                                   month=hoje.month,
                                   day=hoje.day,
                                   date_pattern='y-mm-dd')

        # Posiciona o calendário dentro do frame esquerda
        # com um preenchimento específico.
        self.calendario.pack(pady=10, padx=10)

        # Botão para visualizar consultas
        # Cria um botão no frame esquerda que, quando clicado, executa a
        # função para visualizar as consultas do dia atual.
        botao_ver_consultas = ttk.Button(frame_esquerda,
                                         text="Ver Consultas do Dia",
                                         command=self.ver_consultas_dia)

        # Posiciona o botão com um preenchimento vertical para separá-lo
        # visualmente de outros componentes.
        botao_ver_consultas.pack(pady=10)

        # Label para título da lista de consultas
        # Cria e configura um rótulo no frame direita para identificar a
        # seção onde as consultas do dia selecionado serão exibidas.
        tk.Label(frame_direita,
                 text="Consultas do Dia Selecionado",
                 bg="#f0f0f0", font=("Arial", 14, "bold")).pack(pady=10)

        # Frame para lista de consultas
        # Cria um subframe dentro do frame direita para conter a lista de
        # consultas e sua barra de rolagem.
        frame_lista = tk.Frame(frame_direita, bg="#f0f0f0")

        # Configura o frame da lista para preencher tanto horizontal quanto
        # verticalmente o espaço disponível e permitir expansão.
        frame_lista.pack(fill='both', expand=True, pady=10)

        # Barra de rolagem para a lista
        # Adiciona uma barra de rolagem vertical ao frame da lista, que será
        # configurada mais tarde para interagir com a lista de consultas.
        barra_rolagem = tk.Scrollbar(frame_lista)

        # Posiciona a barra de rolagem à direita do frame da lista,
        # ocupando toda a altura do frame.
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuração da Treeview para exibir consultas
        # Cria uma tabela (Treeview) para exibir detalhes das consultas,
        # incluindo horários de início e final, médico, cliente e descrição.
        self.arvore_consultas_calendario = ttk.Treeview(frame_lista,
                                                        columns=(
                                                        "Hora Início", "Hora Final", "Médico", "Cliente", "Descrição"),
                                                        show="headings",
                                                        height=15,
                                                        yscrollcommand=barra_rolagem.set)

        # Configura os cabeçalhos da tabela com títulos apropriados para cada coluna.
        self.arvore_consultas_calendario.heading("Hora Início", text="Hora Início")
        self.arvore_consultas_calendario.heading("Hora Final", text="Hora Final")
        self.arvore_consultas_calendario.heading("Médico", text="Médico")
        self.arvore_consultas_calendario.heading("Cliente", text="Cliente")
        self.arvore_consultas_calendario.heading("Descrição", text="Descrição")

        # Define a largura de cada coluna na tabela para garantir que a
        # informação seja visível sem precisar de ajuste manual pelo usuário.
        self.arvore_consultas_calendario.column("Hora Início", width=100)
        self.arvore_consultas_calendario.column("Hora Final", width=100)
        self.arvore_consultas_calendario.column("Médico", width=200)
        self.arvore_consultas_calendario.column("Cliente", width=200)
        self.arvore_consultas_calendario.column("Descrição", width=400)

        # Empacotar a Treeview na interface para que ocupe todo o espaço
        # disponível, permitindo uma visualização expansível das consultas.
        self.arvore_consultas_calendario.pack(fill='both', expand=True)

        # Configurar a barra de rolagem para controlar a
        # visualização da Treeview de consultas.
        barra_rolagem.config(command=self.arvore_consultas_calendario.yview)

        # Vincular um evento que é disparado quando uma consulta é selecionada
        # na Treeview, chamando a função para tratar a seleção.
        self.arvore_consultas_calendario.bind("<<TreeviewSelect>>",
                                              self.selecionar_consulta_principal)

        # Inicializar uma variável para armazenar o ID da
        # consulta selecionada atualmente.
        self.id_consulta_selecionada_principal = None


        # Configuração do frame de ações, onde botões de ação estarão disponíveis.
        frame_acoes_principal = tk.Frame(frame_direita, bg="#f0f0f0")
        frame_acoes_principal.pack(pady=10)

        # Botões para alterar ou excluir a consulta selecionada. Estes chamam
        # funções correspondentes quando clicados.
        ttk.Button(frame_acoes_principal,
                   text="Alterar Consulta",
                   command=self.alterar_consulta_principal).grid(row=0,
                                                                 column=0,
                                                                 padx=10)

        ttk.Button(frame_acoes_principal,
                   text="Excluir Consulta",
                   command=self.excluir_consulta_principal).grid(row=0,
                                                                 column=1,
                                                                 padx=10)

        # Chamada de função que verifica e exibe um alerta de consultas para o
        # dia atual, ajudando na organização diária.
        self.exibir_alerta_consultas_hoje()


    def criar_menus(self):

        # Cria a barra de menu principal para a janela de aplicativo.
        menubar = tk.Menu(self.janela)

        # Configura a barra de menu na janela principal.
        self.janela.config(menu=menubar)

        # Cria um menu de arquivo com opções básicas.
        # 'tearoff=0' remove a opção de destacar o menu.
        menu_arquivo = tk.Menu(menubar, tearoff=0)

        # Adiciona o menu "Arquivo" à barra de menu com opções como "Sair".
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Adiciona uma opção para sair da aplicação ao menu "Arquivo".
        menu_arquivo.add_command(label="Sair", command=self.janela.destroy)

        # Cria um menu de cadastros para gerenciar entidades como
        # clientes, médicos e consultas.
        menu_cadastros = tk.Menu(menubar, tearoff=0)

        # Adiciona o menu "Cadastros" à barra de menu.
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)

        # Adiciona opções de cadastro de clientes, médicos, consultas e
        # uma pesquisa por médico ao menu "Cadastros".
        menu_cadastros.add_command(label="Clientes", command=self.janela_clientes)
        menu_cadastros.add_command(label="Médicos", command=self.janela_medicos)
        menu_cadastros.add_command(label="Consultas", command=self.janela_consultas)

        # Adiciona um separador visual no menu.
        menu_cadastros.add_separator()

        # Adiciona uma função para pesquisar consultas por médico.
        menu_cadastros.add_command(label="Pesquisar por Médico", command=self.janela_pesquisar_por_medico)


    def ver_consultas_dia(self):

        # Limpa todos os itens existentes na árvore de consultas (arvore_consultas_calendario)
        # antes de adicionar os novos.
        # Isso garante que a árvore exiba apenas as consultas
        # correspondentes à data selecionada.
        for item in self.arvore_consultas_calendario.get_children():
            self.arvore_consultas_calendario.delete(item)

        # Obtém a data selecionada no calendário (assumindo que o calendário está
        # configurado para selecionar uma data).
        data_selecionada = self.calendario.get_date()

        # Busca todas as consultas na coleção de consultas (colecao_consultas)
        # para a data selecionada e ordena por hora de início.
        consultas = self.colecao_consultas.find({"data": data_selecionada}).sort("hora_inicio", 1)

        # Itera sobre todas as consultas encontradas para aquela data.
        for c in consultas:

            # Busca o cliente correspondente ao 'cliente_id' da consulta no banco de dados.
            cliente = self.colecao_clientes.find_one({"_id": c["cliente_id"]})

            # Se o cliente não for encontrado, usa "Desconhecido".
            cliente_nome = cliente["nome"] if cliente else "Desconhecido"

            # Verifica se existe um médico associado à consulta, obtendo o 'medico_id'.
            medico_id = c.get("medico_id")
            if medico_id:

                # Se o 'medico_id' existir, faz uma consulta no banco de dados
                # para encontrar o médico correspondente.
                medico = self.colecao_medicos.find_one({"_id": medico_id})

                # Se o médico for encontrado, atribui seu nome à variável 'medico_nome',
                # caso contrário, define 'medico_nome' como "Desconhecido".
                medico_nome = medico["nome"] if medico else "Desconhecido"

            else:

                # Caso não exista o 'medico_id' associado à consulta, define o
                # 'medico_nome' como "Sem Médico".
                medico_nome = "Sem Médico"

            # Obtém a hora de início e a hora final da consulta.
            # Caso essas horas não estejam definidas no banco de dados,
            # são utilizados valores padrão.
            hora_ini = c.get("hora_inicio", c.get("hora", "00:00"))
            hora_fim = c.get("hora_final", "Sem Hora Final")

            # Insere as informações da consulta na árvore (arvore_consultas_calendario).
            # Cada consulta será representada por um item na árvore, onde as
            # informações são organizadas nas colunas:
            # - hora de início,
            # - hora final,
            # - nome do médico,
            # - nome do cliente,
            # - descrição da consulta.
            # O 'iid' é utilizado para garantir que cada item inserido
            # tenha um identificador único.
            self.arvore_consultas_calendario.insert("",
                                                    tk.END,
                                                    values=(hora_ini,
                                                            hora_fim,
                                                            medico_nome,
                                                            cliente_nome,
                                                            c["descricao"]),
                                                    iid=str(c["_id"]))


    def selecionar_consulta_principal(self, event):

        # Obtém o item selecionado na árvore de consultas (Treeview)
        selecionado = self.arvore_consultas_calendario.selection()

        # Verifica se algum item foi realmente selecionado na árvore
        if selecionado:

            # Caso haja uma seleção, armazena o ID da consulta selecionada (o
            # primeiro item da lista 'selecionado')
            self.id_consulta_selecionada_principal = selecionado[0]

        else:

            # Caso nenhum item tenha sido selecionado, armazena 'None'
            # indicando que não há consulta selecionada
            self.id_consulta_selecionada_principal = None

    def alterar_consulta_principal(self):

        # Verifica se existe uma consulta selecionada para alteração.
        if not self.id_consulta_selecionada_principal:

            # Se nenhuma consulta foi selecionada, exibe um aviso para o usuário.
            messagebox.showwarning("Aviso", "Nenhuma consulta selecionada para alterar.")
            return

        # Tenta buscar a consulta no banco de dados utilizando o ID da consulta selecionada.
        consulta = self.colecao_consultas.find_one({"_id": ObjectId(self.id_consulta_selecionada_principal)})

        # Verifica se a consulta foi encontrada no banco de dados.
        if not consulta:

            # Caso a consulta não tenha sido encontrada, exibe um erro.
            messagebox.showerror("Erro", "Consulta não encontrada no banco de dados.")
            return

        # Criação de uma nova janela para alterar os dados da consulta.
        # Essa janela será usada para exibir e permitir a alteração dos dados da consulta.
        janela_alt = tk.Toplevel(self.janela)
        janela_alt.title("Alterar Consulta")  # Definindo o título da janela.
        janela_alt.geometry("700x400")  # Definindo o tamanho da janela (700x400 pixels).
        janela_alt.configure(bg="#f0f0f0")  # Define a cor de fundo da janela como cinza claro (#f0f0f0).

        # Cria um LabelFrame dentro da janela 'janela_alt' com o título "Alterar Consulta",
        # definindo a cor de fundo como #f0f0f0 (cinza claro) e a fonte
        # como Arial, tamanho 12 e em negrito.
        # O 'LabelFrame' é um tipo de container que pode conter outros widgets,
        # neste caso, ele irá conter
        # os campos e botões relacionados à alteração de consulta.
        quadro_form = tk.LabelFrame(janela_alt,
                                    text="Alterar Consulta",
                                    bg="#f0f0f0",
                                    font=("Arial", 12, "bold"))

        # O método 'pack' é utilizado para posicionar o 'quadro_form' dentro
        # da janela, preenchendo o espaço horizontal ('fill="x"'),
        # com margens em cima e embaixo (pady=10) e nas laterais (padx=10).
        # Esse método faz com que o quadro preencha o espaço horizontal, e
        # também garante que o layout tenha um pouco de espaçamento.
        quadro_form.pack(fill='x', pady=10, padx=10)

        # Cria um rótulo (Label) dentro de 'quadro_form', com o texto "Cliente:",
        # cor de fundo #f0f0f0 (cinza claro) e a fonte definida como Arial, tamanho 11.
        # A posição do rótulo é configurada para a linha 0, coluna 0 da grade,
        # com margens de 5 pixels em todos os lados (padx=5, pady=5) e
        # alinhamento à direita (sticky='e').
        # O alinhamento 'sticky="e"' significa que o rótulo será posicionado à
        # direita dentro da célula da grade.
        tk.Label(quadro_form,
                 text="Cliente:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=0,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Define uma variável de string (tk.StringVar) que irá
        # armazenar o valor selecionado no combobox do cliente.
        # O combobox será usado para selecionar um cliente da lista.
        # Essa variável 'var_cliente_alt' é importante, pois o
        # valor selecionado no combobox será vinculado a ela.
        # O conteúdo da variável é atualizado automaticamente quando
        # o usuário seleciona um item.
        var_cliente_alt = tk.StringVar()

        # Cria um combobox dentro do 'quadro_form' que irá exibir os clientes.
        # O 'textvariable' é a variável associada ao combobox,
        # que irá manter o valor selecionado. O 'state="readonly"' impede
        # que o usuário digite algo diretamente no campo,
        # restringindo-o a selecionar apenas itens da lista.
        # A fonte é definida como Arial, tamanho 11 e a largura do combobox é 40.
        # O combobox será usado para listar os clientes e possibilitar a seleção de um deles.
        combo_cliente_alt = ttk.Combobox(quadro_form,
                                         textvariable=var_cliente_alt,
                                         state='readonly',
                                         font=("Arial", 11),
                                         width=40)

        # Posiciona o combobox na grade, na linha 0, coluna 1. As margens
        # são de 5 pixels nas laterais e no topo/embaixo.
        # O alinhamento é feito à esquerda (sticky='w').
        # O 'sticky' define a direção de alinhamento dentro da célula,
        # neste caso, à esquerda. O combobox será posicionado
        # ao lado do rótulo "Cliente:" na janela.
        combo_cliente_alt.grid(row=0,
                               column=1,
                               padx=5,
                               pady=5,
                               sticky='w')

        # Busca todos os clientes da coleção 'clientes' no banco de dados.
        # A função find() retorna um cursor com todos os
        # documentos (clientes) presentes na coleção.
        clientes = self.colecao_clientes.find()

        # Cria uma lista de strings formatadas, onde cada cliente é
        # representado pelo seu ID e nome.
        # A expressão f"{c['_id']} - {c['nome']}" formata os dados
        # de cada cliente para exibição no combobox.
        lista_clientes = [f"{c['_id']} - {c['nome']}" for c in clientes]

        # Atribui a lista de clientes ao atributo 'values' do
        # combobox, para que os clientes apareçam como opções.
        # O combobox será preenchido com a lista gerada, permitindo ao
        # usuário selecionar um cliente.
        combo_cliente_alt['values'] = lista_clientes

        # Cria um rótulo (Label) dentro do 'quadro_form', com o texto "Médico:",
        # cor de fundo #f0f0f0 (cinza claro) e a fonte definida como Arial,
        # tamanho 11. A posição do rótulo é configurada para a linha 1, coluna 0 da grade,
        # com margens de 5 pixels em todos os lados (padx=5, pady=5) e
        # alinhamento à direita (sticky='e').
        tk.Label(quadro_form,
                 text="Médico:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=1,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Define uma variável de string (tk.StringVar) que será
        # associada ao combobox de médicos.
        # O combobox exibirá os médicos e o valor selecionado
        # será armazenado nesta variável.
        var_medico_alt = tk.StringVar()

        # Cria um combobox dentro do 'quadro_form' que irá exibir os médicos.
        # O 'textvariable' é a variável associada ao combobox,
        # que irá manter o valor selecionado. O 'state="readonly"' impede
        # que o usuário digite algo diretamente no campo,
        # restringindo-o a selecionar apenas itens da lista.
        # A fonte é definida como Arial, tamanho 11 e a largura do combobox é 40.
        combo_medico_alt = ttk.Combobox(quadro_form,
                                        textvariable=var_medico_alt,
                                        state='readonly',
                                        font=("Arial", 11),
                                        width=40)

        # Posiciona o combobox na grade, na linha 1, coluna 1.
        # As margens são de 5 pixels nas laterais e no topo/embaixo.
        # O alinhamento é feito à esquerda (sticky='w').
        # O combobox será posicionado ao lado do rótulo "Médico:" na janela.
        combo_medico_alt.grid(row=1,
                              column=1,
                              padx=5,
                              pady=5,
                              sticky='w')

        # Busca todos os médicos da coleção 'medicos' no banco de dados.
        # A função find() retorna um cursor com todos os
        # documentos (médicos) presentes na coleção.
        medicos = self.colecao_medicos.find()

        # Cria uma lista de strings formatadas, onde cada médico é
        # representado pelo seu ID e nome.
        # A expressão f"{m['_id']} - {m['nome']}" formata os
        # dados de cada médico para exibição no combobox.
        lista_medicos = [f"{m['_id']} - {m['nome']}" for m in medicos]

        # Atribui a lista de médicos ao atributo 'values' do combobox,
        # para que os médicos apareçam como opções.
        # O combobox será preenchido com a lista gerada, permitindo ao
        # usuário selecionar um médico.
        combo_medico_alt['values'] = lista_medicos

        # Cria um rótulo (Label) dentro do 'quadro_form', com o
        # texto "Data:", cor de fundo #f0f0f0 (cinza claro)
        # e a fonte definida como Arial, tamanho 11. A posição do rótulo é
        # configurada para a linha 2, coluna 0 da grade,
        # com margens de 5 pixels em todos os lados (padx=5, pady=5) e
        # alinhamento à direita (sticky='e').
        tk.Label(quadro_form,
                 text="Data:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=2,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (Entry) dentro de 'quadro_form'
        # para que o usuário insira a data da consulta.
        # A largura do campo de entrada é 20, a fonte é definida como Arial, tamanho 11.
        entrada_data_alt = tk.Entry(quadro_form, width=20, font=("Arial", 11))

        # Posiciona o campo de entrada na grade, na linha 2, coluna 1.
        # As margens são de 5 pixels nas laterais e no topo/embaixo.
        # O alinhamento é feito à esquerda (sticky='w').
        entrada_data_alt.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Função para exibir a janela de seleção de data
        def selecionar_data_alt():

            # Cria uma nova janela chamada 'janela_data', sendo do
            # tipo 'Toplevel' (janela filha da janela principal 'janela_alt')
            # A janela Toplevel permite abrir uma janela separada,
            # mas dentro da mesma aplicação.
            janela_data = tk.Toplevel(janela_alt)

            # Define o título da janela 'janela_data' como "Selecionar Data"
            # Isso vai exibir o título na parte superior da janela
            janela_data.title("Selecionar Data")

            # Define o tamanho da janela 'janela_data' para 300x300 pixels
            # O tamanho é especificado na forma "largura x altura"
            janela_data.geometry("300x300")

            # Cria um widget Calendar dentro da janela, que permite ao
            # usuário selecionar uma data
            # 'selectmode="day"' significa que o usuário pode selecionar
            # apenas um único dia (não intervalo)
            # 'date_pattern="y-mm-dd"' define o formato da data que será exibido (ano-mês-dia)
            cal = Calendar(janela_data, selectmode='day', date_pattern='y-mm-dd')

            # Exibe o calendário na janela. O 'pady=10' adiciona um espaçamento
            # de 10 pixels acima e abaixo do calendário
            cal.pack(pady=10)

            # Função interna para ser chamada quando o botão "Confirmar" for pressionado
            def confirmar_data():

                # Obtém a data selecionada no calendário
                # A função get_date() retorna a data no formato definido,
                # por exemplo "2024-12-01"
                data_sel = cal.get_date()

                # Limpa o conteúdo atual do campo de entrada de data (entrada_data_alt)
                # A função delete(0, tk.END) exclui todos os caracteres no campo
                entrada_data_alt.delete(0, tk.END)

                # Insere a data selecionada no campo de entrada 'entrada_data_alt'
                # 'tk.END' faz com que a data seja inserida no final do campo
                entrada_data_alt.insert(tk.END, data_sel)

                # Fecha a janela 'janela_data' após o usuário confirmar a seleção
                janela_data.destroy()

            # Cria um botão "Confirmar" dentro da janela 'janela_data'
            # Quando o botão for pressionado, a função 'confirmar_data' será chamada
            ttk.Button(janela_data,
                       text="Confirmar",
                       command=confirmar_data).pack(pady=10)

        # Cria um botão "Selecionar Data" dentro do 'quadro_form', que, ao ser pressionado,
        # chama a função 'selecionar_data_alt' para abrir uma janela para
        # selecionar uma data.
        # O botão é posicionado na linha 2, coluna 2 da grade, com margens
        # de 5 pixels em ambos os lados (padx=5, pady=5).
        ttk.Button(quadro_form, text="Selecionar Data",
                   command=selecionar_data_alt).grid(row=2,
                                                     column=2,
                                                     padx=5,
                                                     pady=5)

        # --------------------------------------

        # Cria um rótulo (Label) dentro de 'quadro_form' com o texto "Hora Início (HH:MM):"
        # A cor de fundo do rótulo é #f0f0f0 (cinza claro) e a fonte é Arial, tamanho 11.
        # O rótulo é posicionado na linha 3, coluna 0 da grade, com margens
        # de 5 pixels em todos os lados (padx=5, pady=5) e
        # alinhamento à direita (sticky='e').
        tk.Label(quadro_form,
                 text="Hora Início (HH:MM):",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=3,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (Entry) para inserir a hora de início da consulta.
        # O campo tem uma largura de 20 caracteres e a fonte definida como Arial, tamanho 11.
        # O campo de entrada é posicionado na linha 3, coluna 1 da grade,
        # com margens de 5 pixels nas laterais e no topo/embaixo.
        # O alinhamento do campo de entrada é feito à esquerda (sticky='w').
        entrada_hora_alt_inicio = tk.Entry(quadro_form, width=20, font=("Arial", 11))
        entrada_hora_alt_inicio.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Cria um rótulo (Label) dentro de 'quadro_form' com o texto "Hora Final (HH:MM):"
        # A cor de fundo do rótulo é #f0f0f0 (cinza claro) e a fonte é Arial, tamanho 11.
        # O rótulo é posicionado na linha 4, coluna 0 da grade, com margens
        # de 5 pixels em todos os lados (padx=5, pady=5) e alinhamento à
        # direita (sticky='e').
        tk.Label(quadro_form,
                 text="Hora Final (HH:MM):",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=4,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (Entry) para inserir a hora final da consulta.
        # O campo tem uma largura de 20 caracteres e a fonte definida como Arial, tamanho 11.
        # O campo de entrada é posicionado na linha 4, coluna 1 da grade, com
        # margens de 5 pixels nas laterais e no topo/embaixo.
        # O alinhamento do campo de entrada é feito à esquerda (sticky='w').
        entrada_hora_alt_final = tk.Entry(quadro_form, width=20, font=("Arial", 11))
        entrada_hora_alt_final.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Cria um rótulo (Label) dentro de 'quadro_form' com o texto "Descrição:"
        # A cor de fundo do rótulo é #f0f0f0 (cinza claro) e a fonte é Arial, tamanho 11.
        # O rótulo é posicionado na linha 5, coluna 0 da grade, com margens de 5
        # pixels em todos os lados (padx=5, pady=5) e alinhamento ao norte (sticky='ne').
        tk.Label(quadro_form,
                 text="Descrição:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=5,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='ne')

        # Cria um campo de texto (Text) dentro de 'quadro_form' para inserir a
        # descrição da consulta.
        # O campo de texto tem uma largura de 50 caracteres e altura de 4
        # linhas, com a fonte definida como Arial, tamanho 11.
        # O campo de texto é posicionado na linha 5, coluna 1 da grade,
        # com margens de 5 pixels nas laterais e no topo/embaixo.
        # O alinhamento do campo de texto é feito à esquerda (sticky='w').
        texto_descricao_alt = tk.Text(quadro_form, width=50, height=4, font=("Arial", 11))
        texto_descricao_alt.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        # Preencher campos com a consulta atual
        # A linha abaixo consulta o banco de dados para encontrar o
        # cliente usando o 'cliente_id' da consulta.
        # 'self.colecao_clientes.find_one' busca um único cliente no
        # banco de dados pela chave '_id'.
        cliente = self.colecao_clientes.find_one({"_id": consulta["cliente_id"]})

        # A linha abaixo verifica se o cliente foi encontrado.
        # Se o cliente foi encontrado, a variável 'cliente_nome' recebe o nome do cliente.
        # Caso contrário, 'cliente_nome' recebe o valor "Desconhecido".
        cliente_nome = cliente["nome"] if cliente else "Desconhecido"

        # A linha abaixo atualiza o campo do ComboBox ou Entry com o nome do cliente e seu ID.
        # 'var_cliente_alt.set()' atualiza o valor associado à variável 'var_cliente_alt',
        # que é utilizada no ComboBox para exibir o nome e o ID do cliente selecionado.
        # O formato exibido será: "<ID do Cliente> - <Nome do Cliente>".
        var_cliente_alt.set(f"{consulta['cliente_id']} - {cliente_nome}")

        # Obtém o 'medico_id' da consulta atual
        # A linha abaixo obtém o ID do médico associado à consulta,
        # usando 'consulta.get("medico_id")'.
        # Se não houver médico associado, 'medico_id' será 'None'.
        medico_id = consulta.get("medico_id")

        # Se houver um médico associado à consulta
        if medico_id:

            # A linha abaixo consulta o banco de dados para encontrar o médico usando 'medico_id'.
            # 'self.colecao_medicos.find_one({"_id": medico_id})' busca um
            # único médico no banco de dados.
            medico = self.colecao_medicos.find_one({"_id": medico_id})

            # Se o médico foi encontrado, 'medico_nome' recebe o nome do médico.
            # Caso contrário, 'medico_nome' é atribuído como "Desconhecido".
            medico_nome = medico["nome"] if medico else "Desconhecido"

            # A linha abaixo atualiza o ComboBox ou Entry para exibir o
            # nome do médico e seu ID.
            # 'var_medico_alt.set(f"{medico_id} - {medico_nome}")' formata o
            # valor exibido como "<ID do Médico> - <Nome do Médico>".
            var_medico_alt.set(f"{medico_id} - {medico_nome}")

        else:

            # Caso não haja médico associado à consulta, o campo de
            # seleção de médico é limpo.
            var_medico_alt.set("")

        # A linha abaixo insere a data da consulta no campo de entrada de
        # data (entrada_data_alt).
        # O valor de 'consulta["data"]' é inserido no campo, que é
        # atualizado com a data da consulta.
        entrada_data_alt.insert(tk.END, consulta["data"])

        # Obtém as horas de início e fim da consulta.
        # Se a hora de início não estiver presente, o valor padrão será "00:00".
        # Se a hora final não estiver presente, o valor da hora de
        # início será usado como hora final.
        hora_ini = consulta.get("hora_inicio", consulta.get("hora", "00:00"))
        hora_fim = consulta.get("hora_final", hora_ini)

        # Insere a hora de início no campo de entrada de hora de
        # início (entrada_hora_alt_inicio).
        entrada_hora_alt_inicio.insert(tk.END, hora_ini)

        # Insere a hora de fim no campo de entrada de hora
        # final (entrada_hora_alt_final).
        entrada_hora_alt_final.insert(tk.END, hora_fim)

        # A linha abaixo insere a descrição da consulta no campo de
        # texto (texto_descricao_alt).
        # O valor de 'consulta["descricao"]' é inserido no campo de
        # texto, atualizando a descrição da consulta.
        texto_descricao_alt.insert(tk.END, consulta["descricao"])

        # Função que verifica se dois intervalos de tempo se sobrepõem.
        def intervalos_conflitam(inicio1, fim1, inicio2, fim2):

            # Função interna que converte o tempo no formato HH:MM para
            # minutos desde a meia-noite.
            # Ela divide o valor de hora e minuto da string, converte para
            # inteiro e retorna o total de minutos.
            def hm_para_min(hm):
                h, m = hm.split(':')  # Divide a string de tempo 'hm' em hora e minuto.
                return int(h) * 60 + int(m)  # Converte a hora para minutos e soma com os minutos.

            # Converte os horários de início e fim de cada intervalo para minutos.
            ini1 = hm_para_min(inicio1)  # Converte o início do primeiro intervalo para minutos.
            fi1 = hm_para_min(fim1)  # Converte o fim do primeiro intervalo para minutos.
            ini2 = hm_para_min(inicio2)  # Converte o início do segundo intervalo para minutos.
            fi2 = hm_para_min(fim2)  # Converte o fim do segundo intervalo para minutos.

            # Verifica se os intervalos se sobrepõem. A condição retorna
            # True se houver conflito de horários.
            # O primeiro intervalo começa antes do segundo terminar e
            # termina depois do segundo começar.
            return (ini1 < fi2) and (fi1 > ini2)

        # Função para salvar as alterações feitas em uma consulta
        def salvar_alteracoes():

            # Obtém o valor selecionado no campo de cliente e remove
            # espaços em branco antes e depois.
            cliente_sel = var_cliente_alt.get().strip()

            # Obtém o valor selecionado no campo de médico e remove
            # espaços em branco antes e depois.
            medico_sel = var_medico_alt.get().strip()

            # Obtém a data inserida no campo de data e remove espaços em branco.
            data_str = entrada_data_alt.get().strip()

            # Obtém a hora de início inserida no campo de hora inicial e
            # remove espaços em branco.
            hora_ini_str = entrada_hora_alt_inicio.get().strip()

            # Obtém a hora final inserida no campo de hora final e
            # remove espaços em branco.
            hora_fim_str = entrada_hora_alt_final.get().strip()

            # Obtém a descrição inserida no campo de descrição da consulta.
            descricao = texto_descricao_alt.get("1.0", tk.END).strip()

            # Verifica se algum campo obrigatório está vazio. Caso algum campo
            # esteja vazio, exibe uma mensagem de aviso e retorna.
            if not cliente_sel or not medico_sel or not data_str or not hora_ini_str or not hora_fim_str or not descricao:
                messagebox.showwarning("Aviso", "Preencha todos os campos.")
                return

            # A primeira parte tenta converter as informações selecionadas pelo
            # usuário para tipos válidos para o banco de dados
            try:

                # A linha abaixo separa a string 'cliente_sel' que contém o ID e
                # nome do cliente em duas partes.
                # O método split(" - ", 1) vai dividir a string onde houver " - ".
                # A primeira parte (ID) será salva em 'cliente_id_str' e a
                # segunda (nome) será ignorada com '_'.
                cliente_id_str, _ = cliente_sel.split(" - ", 1)

                # Agora que temos o 'cliente_id_str' (ID do cliente como string),
                # usamos o ObjectId() para convertê-lo em um tipo de dado especial
                # que o MongoDB usa para identificar documentos de forma única.
                cliente_id = ObjectId(cliente_id_str)

                # A mesma coisa é feita com a variável 'medico_sel' para obter o ID do médico.
                # Aqui, 'medico_sel' também é uma string com "ID - Nome".
                # Novamente, a primeira parte (ID) é extraída.
                medico_id_str, _ = medico_sel.split(" - ", 1)

                # O ID do médico é convertido em um ObjectId, como fizemos com o cliente.
                medico_id_novo = ObjectId(medico_id_str)

            # O bloco 'except' será executado caso ocorra algum erro nas operações acima.
            # Caso o usuário tenha selecionado algo incorretamente ou se o
            # formato dos dados estiver errado, um aviso será mostrado.
            except:

                # Se algo deu errado, mostramos uma mensagem de aviso para o usuário.
                # Isso ocorre se o formato da seleção de cliente ou médico
                # estiver errado, por exemplo.
                messagebox.showwarning("Aviso", "Selecione corretamente o cliente e médico.")

                # Após exibir o aviso, a função é interrompida com 'return'.
                # Nenhum outro código será executado.
                return

            # A segunda parte valida as datas e horários para garantir
            # que eles estão no formato correto
            try:

                # Verifica se a data inserida pelo usuário está no formato 'YYYY-MM-DD'.
                # O método strptime tenta converter a string da data para um
                # formato que o Python possa entender.
                # Se a data estiver no formato errado, uma exceção será gerada.
                datetime.datetime.strptime(data_str, "%Y-%m-%d")

                # Verifica se a hora de início está no formato 'HH:MM'.
                # Novamente, o strptime é usado para garantir que a hora esteja correta.
                datetime.datetime.strptime(hora_ini_str, "%H:%M")

                # Verifica se a hora final também está no formato 'HH:MM'.
                datetime.datetime.strptime(hora_fim_str, "%H:%M")

            # O bloco 'except ValueError' será executado se houver erro ao
            # tentar converter a data ou as horas.
            except ValueError:

                # Se ocorrer um erro (por exemplo, a data ou hora estiver em
                # formato incorreto), exibe uma mensagem de aviso para o usuário.
                messagebox.showwarning("Aviso", "Data, Hora Início ou Hora Final inválida.")

                # Após exibir o aviso, a função é interrompida com 'return'.
                return

            # Verificar conflitos
            # A consulta a seguir busca todas as consultas de um médico para o mesmo dia,
            # exceto a consulta que está sendo alterada (identificada pelo ID).
            # O operador "$ne" no MongoDB significa "não igual", então ele
            # garante que a consulta que está sendo alterada
            # não seja retornada nesta busca.
            consultas_medico_dia = self.colecao_consultas.find({
                "medico_id": medico_id_novo,  # Filtra consultas do médico selecionado.
                "data": data_str,  # Filtra consultas para o mesmo dia.
                "_id": {"$ne": ObjectId(self.id_consulta_selecionada_principal)}
                # Exclui a consulta sendo editada da busca.
            })

            # Agora, para cada consulta encontrada, a lógica abaixo verifica se
            # há algum conflito de horário.
            for c in consultas_medico_dia:

                # Obtém a hora de início da consulta atual. Caso não esteja
                # presente, usa o valor padrão "00:00".
                h_ini_exist = c.get("hora_inicio", c.get("hora", "00:00"))

                # Obtém a hora final da consulta atual. Caso não esteja presente,
                # usa a hora de início como valor padrão.
                h_fim_exist = c.get("hora_final", h_ini_exist)

                # Verifica se as horas da nova consulta (hora_ini_str, hora_fim_str)
                # entram em conflito com a consulta existente
                if intervalos_conflitam(hora_ini_str, hora_fim_str, h_ini_exist, h_fim_exist):

                    # Se houver conflito de horário, exibe uma mensagem de aviso.
                    messagebox.showwarning("Aviso", "Conflito de horário com outra consulta deste médico.")

                    # A execução da função é interrompida aqui, não permitindo
                    # que a consulta seja alterada.
                    return

            # Criação do dicionário 'dados_atualizacao' contendo os campos
            # que serão atualizados na consulta
            dados_atualizacao = {
                "$set": {  # "$set" é um operador do MongoDB que define novos valores para os campos especificados.
                    "cliente_id": cliente_id,  # Atualiza o ID do cliente na consulta com o novo valor.
                    "medico_id": medico_id_novo,  # Atualiza o ID do médico na consulta com o novo valor.
                    "data": data_str,  # Atualiza a data da consulta.
                    "hora_inicio": hora_ini_str,  # Atualiza a hora de início da consulta.
                    "hora_final": hora_fim_str,  # Atualiza a hora final da consulta.
                    "descricao": descricao  # Atualiza a descrição da consulta.
                }
            }

            # Atualiza a consulta no banco de dados usando o método 'update_one'.
            # O primeiro argumento é o filtro para localizar o documento da
            # consulta a ser atualizada, usando o ID da consulta.
            # O segundo argumento é o dicionário 'dados_atualizacao' com as
            # mudanças que devem ser aplicadas à consulta.
            self.colecao_consultas.update_one({"_id": ObjectId(self.id_consulta_selecionada_principal)},
                                              dados_atualizacao)

            # Fecha a janela de alteração após as alterações serem salvas.
            janela_alt.destroy()

            # Chama a função 'ver_consultas_dia' para atualizar a exibição
            # das consultas no calendário ou na lista.
            self.ver_consultas_dia()

            # Exibe uma mensagem de sucesso informando que a consulta foi atualizada corretamente.
            messagebox.showinfo("Sucesso", "Consulta atualizada com sucesso!")

        # Criação de um botão dentro da janela 'janela_alt' com o texto "Salvar Alterações"
        # O comando do botão, quando clicado, chama a função 'salvar_alteracoes'
        # para salvar as alterações feitas na consulta.
        ttk.Button(janela_alt, text="Salvar Alterações", command=salvar_alteracoes).pack(pady=10)


    # Função para excluir uma consulta selecionada
    def excluir_consulta_principal(self):

        # Verifica se uma consulta foi selecionada. Caso não tenha sido,
        # exibe uma mensagem de aviso.
        if not self.id_consulta_selecionada_principal:
            messagebox.showwarning("Aviso", "Nenhuma consulta selecionada para excluir.")
            return

        # Exibe uma janela de confirmação pedindo para o usuário
        # confirmar a exclusão da consulta.
        confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja excluir esta consulta?")

        # Se o usuário confirmar a exclusão (clicando em 'Sim')
        if confirmar:

            # Realiza a exclusão da consulta no banco de dados (MongoDB)
            # utilizando o '_id' da consulta selecionada.
            self.colecao_consultas.delete_one({"_id": ObjectId(self.id_consulta_selecionada_principal)})

            # Atualiza a visualização das consultas do dia após a exclusão
            self.ver_consultas_dia()

            # Reseta a variável que guarda o ID da consulta selecionada,
            # pois a consulta foi excluída.
            self.id_consulta_selecionada_principal = None

            # Exibe uma mensagem informando que a exclusão foi realizada com sucesso
            messagebox.showinfo("Sucesso", "Consulta excluída com sucesso!")


    def exibir_alerta_consultas_hoje(self):

        # Obtém a data de hoje no formato "YYYY-MM-DD"
        hoje = datetime.date.today().strftime("%Y-%m-%d")

        # Busca todas as consultas no banco de dados para o dia de hoje,
        # ordenando pelas horas de início
        consultas_hoje = list(self.colecao_consultas.find({"data": hoje}).sort("hora_inicio", 1))

        # Verifica se existem consultas agendadas para hoje
        if consultas_hoje:

            # Inicializa a variável 'texto' com o cabeçalho da mensagem
            texto = "Consultas agendadas para hoje:\n"

            # Itera sobre todas as consultas agendadas para hoje
            for c in consultas_hoje:

                # Busca o cliente associado à consulta usando o 'cliente_id' da consulta
                cliente = self.colecao_clientes.find_one({"_id": c["cliente_id"]})

                # Verifica se o cliente foi encontrado, se não, define o nome como "Desconhecido"
                cliente_nome = cliente["nome"] if cliente else "Desconhecido"

                # Obtém o 'medico_id' associado à consulta
                medico_id = c.get("medico_id")

                # Se o médico estiver associado à consulta, busca suas informações no banco
                if medico_id:
                    medico = self.colecao_medicos.find_one({"_id": medico_id})

                    # Verifica se o médico foi encontrado, se não, define o nome como "Desconhecido"
                    medico_nome = medico["nome"] if medico else "Desconhecido"

                else:

                    # Se não houver médico associado à consulta, define como "Sem Médico"
                    medico_nome = "Sem Médico"

                # Obtém a hora de início da consulta, se não estiver definida, utiliza "00:00"
                hora_ini = c.get("hora_inicio", c.get("hora", "00:00"))

                # Obtém a hora final da consulta, se não estiver definida, utiliza "Sem Hora Final"
                hora_fim = c.get("hora_final", "Sem Hora Final")

                # Concatena as informações da consulta para a variável 'texto'
                texto += f"{hora_ini}-{hora_fim} - {medico_nome} - {cliente_nome} - {c['descricao']}\n"

            # Exibe a mensagem com todas as consultas agendadas para hoje
            messagebox.showinfo("Alerta de Consultas", texto)


    def janela_clientes(self):

        # Abre uma nova janela sobre a janela principal do aplicativo. A nova
        # janela 'janela_cl' é usada para gerenciar clientes.
        janela_cl = tk.Toplevel(self.janela)

        # Define o título da nova janela que aparece na barra de título da janela.
        # 'Gerenciar Clientes' informa ao usuário sobre o propósito da janela.
        janela_cl.title("Gerenciar Clientes")

        # Define as dimensões da janela, onde '600x400' indica uma largura
        # de 600 pixels e altura de 400 pixels.
        janela_cl.geometry("600x400")

        # Configura a cor de fundo da janela para cinza claro ('#f0f0f0'), um
        # código de cor hexadecimal que define uma cor específica.
        janela_cl.configure(bg="#f0f0f0")

        # Define a janela para abrir maximizada na tela.
        janela_cl.state('zoomed')

        # Cria um contêiner dentro da janela para agrupar elementos
        # relacionados ao cadastro de clientes.
        quadro_form = tk.LabelFrame(janela_cl,
                                    text="Cadastro de Clientes",
                                    bg="#f0f0f0",
                                    font=("Arial", 12, "bold"))

        # Posiciona o quadro chamado 'quadro_form' no topo da janela principal.
        # 'side=tk.TOP' faz com que ele fique no topo da janela.
        # 'fill='x'' faz com que o quadro se expanda horizontalmente
        # para preencher o espaço disponível.
        # 'pady=10' adiciona 10 pixels de espaçamento vertical em cima e embaixo do quadro.
        # 'padx=10' adiciona 10 pixels de espaçamento horizontal nos
        # lados esquerdo e direito do quadro.
        quadro_form.pack(side=tk.TOP,
                         fill='x',
                         pady=10,
                         padx=10)

        # Cria um rótulo dentro do 'quadro_form' com o texto 'Nome:'.
        # 'bg="#f0f0f0"' define a cor de fundo do rótulo como
        # cinza claro, correspondendo à cor do quadro.
        # 'font=("Arial", 11)' define a fonte do texto como Arial tamanho 11.
        # 'grid(row=0, column=0, padx=5, pady=5, sticky='e')' posiciona o
        # rótulo na primeira linha (row=0) e primeira coluna (column=0).
        # 'padx=5' e 'pady=5' adicionam espaçamento de 5 pixels ao redor do rótulo.
        # 'sticky='e'' faz com que o rótulo fique alinhado à direita na célula da grade.
        tk.Label(quadro_form,
                 text="Nome:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=0,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria uma caixa de entrada para inserção do nome do cliente.
        # 'width=30' define que a caixa de entrada pode mostrar 30
        # caracteres de largura de uma vez.
        # 'font=("Arial", 11)' especifica que a fonte usada
        # dentro da caixa de entrada é Arial tamanho 11.
        entrada_nome_cliente = tk.Entry(quadro_form,
                                        width=30,
                                        font=("Arial", 11))

        # Posiciona a caixa de entrada na grade dentro do 'quadro_form'.
        # 'row=0' e 'column=1' colocam a caixa de entrada na
        # primeira linha e segunda coluna.
        # 'padx=5' e 'pady=5' estabelecem um espaçamento de 5 pixels
        # em todas as direções ao redor da caixa.
        entrada_nome_cliente.grid(row=0,
                                  column=1,
                                  padx=5,
                                  pady=5)

        # Cria um rótulo (label) para identificar o campo onde o
        # usuário deve inserir o e-mail. Configurações:
        # - 'text="E-mail:"' define o texto do rótulo.
        # - 'bg="#f0f0f0"' estabelece a cor de fundo do rótulo para se
        # integrar com o estilo do formulário.
        # - 'font=("Arial", 11)' aplica a fonte Arial tamanho 11 ao
        # texto, garantindo legibilidade.
        # - 'grid(...)' posiciona o rótulo na interface: na
        # segunda linha (row=1), primeira coluna (column=0),
        #   com margem de 5 pixels em todas as direções (padx=5, pady=5) e
        # alinhamento à direita (sticky='e').
        tk.Label(quadro_form,
                 text="E-mail:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=1,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria uma caixa de entrada (entry) para que o usuário
        # possa digitar seu e-mail. Configurações:
        # - 'width=30' define a largura do campo, permitindo que a
        # maior parte dos e-mails seja digitada sem cortes.
        # - 'font=("Arial", 11)' usa a fonte Arial tamanho 11,
        # mantendo consistência com o rótulo.
        # - 'grid(...)' posiciona a caixa de entrada na interface: na
        # segunda linha (row=1), segunda coluna (column=1),
        #   com margem de 5 pixels em todas as direções (padx=5, pady=5),
        # facilitando o acesso e a interação do usuário.
        entrada_email_cliente = tk.Entry(quadro_form,
                                         width=30,
                                         font=("Arial", 11))
        entrada_email_cliente.grid(row=1,
                                   column=1,
                                   padx=5,
                                   pady=5)

        # Cria um rótulo (label) para o campo de telefone, com configurações
        # semelhantes ao rótulo de e-mail, garantindo
        # uniformidade visual. Configurações:
        # - 'text="Telefone:"' especifica o texto do rótulo.
        # - 'bg="#f0f0f0"' e 'font=("Arial", 11)' mantêm a cor de
        # fundo e o estilo de fonte.
        # - 'grid(...)' posiciona o rótulo para o campo de telefone na
        # interface: na terceira linha (row=2), primeira coluna (column=0),
        #   com margem de 5 pixels e alinhamento à direita, padronizando a
        # localização dos rótulos nos formulários.
        tk.Label(quadro_form,
                 text="Telefone:", bg="#f0f0f0", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=5, sticky='e')

        # Cria uma caixa de entrada para o número de telefone, permitindo ao
        # usuário inserir seu contato telefônico. Configurações:
        # - 'width=30' permite a entrada de números de telefone comuns sem truncamento.
        # - 'font=("Arial", 11)' assegura que o texto dentro da caixa seja claramente legível.
        # - 'grid(...)' posiciona a caixa de entrada na interface: na terceira
        # linha (row=2), segunda coluna (column=1),
        # com margem de 5 pixels em todas as direções, facilitando a
        # digitação e o alinhamento com o campo de e-mail.
        entrada_telefone_cliente = tk.Entry(quadro_form, width=30, font=("Arial", 11))
        entrada_telefone_cliente.grid(row=2, column=1, padx=5, pady=5)

        # Função que define o comportamento para adicionar um cliente ao banco de dados.
        def adicionar_cliente():

            # Obtém e remove espaços desnecessários dos valores inseridos
            # nos campos de nome, e-mail e telefone.
            nome = entrada_nome_cliente.get().strip()
            email = entrada_email_cliente.get().strip()
            telefone = entrada_telefone_cliente.get().strip()

            # Verifica se algum dos campos está vazio. Se estiver, exibe uma
            # mensagem de aviso e interrompe a função.
            if not nome or not email or not telefone:
                messagebox.showwarning("Aviso", "Preencha todos os campos do cliente.", parent=janela_cl)
                return

            # Cria um dicionário com os dados coletados, que será usado
            # para inserir no banco de dados.
            novo_cliente = {
                "nome": nome,
                "email": email,
                "telefone": telefone
            }

            # Insere o novo cliente na coleção de clientes no MongoDB.
            self.colecao_clientes.insert_one(novo_cliente)

            # Limpa os campos de entrada após a inserção, preparando
            # para nova entrada de dados.
            entrada_nome_cliente.delete(0, tk.END)
            entrada_email_cliente.delete(0, tk.END)
            entrada_telefone_cliente.delete(0, tk.END)

            # Chama a função `carregar_clientes` para atualizar a lista de
            # clientes mostrada na interface.
            carregar_clientes()

            # Exibe uma mensagem informando que o cliente foi adicionado com sucesso.
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!", parent=janela_cl)

        # Cria um botão estilizado com o texto "Adicionar Cliente".
        # O botão, quando clicado, chama a função `adicionar_cliente`.
        # `quadro_form` é o contêiner onde o botão será posicionado.
        # `text="Adicionar Cliente"` define o texto exibido no botão.
        # `command=adicionar_cliente` associa a função `adicionar_cliente` ao
        # evento de clique no botão.
        # `.grid(row=3, column=0, columnspan=2, pady=10)` posiciona o botão:
        # - `row=3` coloca o botão na quarta linha da grade (índice começa em 0).
        # - `column=0` posiciona o botão na primeira coluna.
        # - `columnspan=2` faz o botão ocupar duas colunas, centralizando-o.
        # - `pady=10` adiciona 10 pixels de espaçamento vertical acima e abaixo do botão.
        ttk.Button(quadro_form,
                   text="Adicionar Cliente",
                   command=adicionar_cliente).grid(row=3,
                                                   column=0,
                                                   columnspan=2,
                                                   pady=10)


        # Cria um frame (contêiner) chamado `quadro_lista` dentro da
        # janela de clientes (`janela_cl`).
        # Este frame será usado para conter a lista de clientes e
        # uma barra de rolagem associada.
        # `bg="#f0f0f0"` define a cor de fundo como cinza claro,
        # consistente com o estilo geral.
        quadro_lista = tk.Frame(janela_cl, bg="#f0f0f0")

        # Posiciona o `quadro_lista` dentro da janela de clientes:
        # - `fill='both'` faz o frame expandir para preencher todo o
        # espaço disponível, tanto horizontal quanto verticalmente.
        # - `expand=True` permite que o frame se expanda dinamicamente
        # ao redimensionar a janela.
        # - `pady=10` e `padx=10` adicionam 10 pixels de margem em
        # todos os lados do frame.
        quadro_lista.pack(fill='both',
                          expand=True,
                          pady=10,
                          padx=10)

        # Cria uma barra de rolagem vertical associada ao `quadro_lista`.
        # A barra será configurada para controlar a rolagem de uma
        # tabela de clientes (Treeview).
        barra_rolagem = tk.Scrollbar(quadro_lista)

        # Posiciona a barra de rolagem à direita do frame `quadro_lista`:
        # - `side=tk.RIGHT` fixa a barra de rolagem ao lado
        # direito do contêiner.
        # - `fill=tk.Y` faz a barra ocupar toda a altura do contêiner,
        # permitindo rolagem vertical.
        barra_rolagem.pack(side=tk.RIGHT,
                           fill=tk.Y)

        # Cria um widget Treeview chamado `arvore_clientes`, que será usado como
        # uma tabela para exibir os dados dos clientes.
        # Parâmetros:
        # - `quadro_lista`: Define o contêiner pai onde a tabela será inserida.
        # - `columns=("Nome", "E-mail", "Telefone")`: Especifica as colunas que a
        # tabela terá. Cada nome no tuple é o identificador de uma coluna.
        # - `show="headings"`: Exibe apenas os cabeçalhos das colunas,
        # ocultando a coluna padrão de índice.
        # - `height=10`: Define o número de linhas visíveis na tabela.
        # - `yscrollcommand=barra_rolagem.set`: Associa a barra de rolagem vertical à
        # tabela, permitindo que ela funcione com o conteúdo exibido.
        arvore_clientes = ttk.Treeview(quadro_lista,
                                       columns=("Nome", "E-mail", "Telefone"),
                                       show="headings",
                                       height=10,
                                       yscrollcommand=barra_rolagem.set)

        # Configura os cabeçalhos das colunas da Treeview, especificando o
        # texto exibido no topo de cada coluna.
        # - `heading("Nome", text="Nome")`: Define o texto do cabeçalho da
        # coluna "Nome" como "Nome".
        # - `heading("E-mail", text="E-mail")`: Define o texto do cabeçalho da
        # coluna "E-mail" como "E-mail".
        # - `heading("Telefone", text="Telefone")`: Define o texto do cabeçalho
        # da coluna "Telefone" como "Telefone".
        arvore_clientes.heading("Nome", text="Nome")
        arvore_clientes.heading("E-mail", text="E-mail")
        arvore_clientes.heading("Telefone", text="Telefone")

        # Define a largura de cada coluna da tabela para garantir que o
        # conteúdo seja exibido de forma legível.
        # - `column("Nome", width=200)`: Configura a largura da coluna "Nome" como 200 pixels.
        # - `column("E-mail", width=200)`: Configura a largura da coluna "E-mail" como 200 pixels.
        # - `column("Telefone", width=120)`: Configura a largura da coluna "Telefone" como 120 pixels.
        arvore_clientes.column("Nome", width=200)
        arvore_clientes.column("E-mail", width=200)
        arvore_clientes.column("Telefone", width=120)

        # Posiciona a Treeview (`arvore_clientes`) dentro do frame `quadro_lista`.
        # - `fill='both'`: Faz com que o widget preencha todo o espaço
        # disponível no frame, tanto horizontal quanto verticalmente.
        # - `expand=True`: Permite que o widget seja redimensionado dinamicamente
        # quando o tamanho da janela for ajustado.
        arvore_clientes.pack(fill='both',
                             expand=True)

        # Configura a barra de rolagem para controlar a visualização da Treeview.
        # - `command=arvore_clientes.yview`: Vincula a barra de rolagem à
        # funcionalidade de rolagem vertical da Treeview.
        barra_rolagem.config(command=arvore_clientes.yview)

        # Inicializa uma variável `id_cliente_selecionado` como uma
        # lista contendo `None`.
        # Esta variável será usada para armazenar o ID do cliente
        # atualmente selecionado na Treeview.
        # Usar uma lista permite que a variável seja modificada dentro de
        # funções internas (closures) sem necessidade de usar `global`.
        id_cliente_selecionado = [None]

        # Define a função `carregar_clientes`, que será usada para carregar os
        # dados dos clientes armazenados no banco de dados e exibi-los na
        # Treeview (`arvore_clientes`).
        def carregar_clientes():

            # Remove todos os itens atualmente exibidos na Treeview.
            # `arvore_clientes.get_children()` retorna uma lista de todos os
            # itens (linhas) na Treeview.
            # `arvore_clientes.delete(item)` remove cada item individualmente.
            for item in arvore_clientes.get_children():
                arvore_clientes.delete(item)

            # Obtém todos os documentos da coleção `clientes` no banco de dados MongoDB.
            # `self.colecao_clientes.find()` retorna um cursor iterável
            # contendo todos os documentos na coleção.
            clientes = self.colecao_clientes.find()

            # Itera sobre os documentos retornados do banco de dados.
            for c in clientes:

                # Insere cada cliente como uma nova linha na Treeview.
                # Parâmetros:
                # - `""`: Indica que o item não possui um pai (nível superior na
                # hierarquia da Treeview).
                # - `tk.END`: Insere o novo item no final da lista de itens existentes.
                # - `values=(c["nome"], c["email"], c["telefone"])`: Define os
                # valores para as colunas da Treeview, extraídos do documento `c`.
                # - `iid=str(c["_id"])`: Define o identificador exclusivo da linha,
                # usando o `_id` do MongoDB convertido em string.
                arvore_clientes.insert("",
                                       tk.END,
                                       values=(c["nome"], c["email"], c["telefone"]), iid=str(c["_id"]))

            # Reseta a variável `id_cliente_selecionado` para `None`.
            # Isso é necessário para indicar que nenhum cliente está
            # selecionado após a atualização da lista.
            id_cliente_selecionado[0] = None


        # Define a função `selecionar_cliente`, que é executada quando um
        # item da Treeview `arvore_clientes` é selecionado.
        # A função recupera os dados do cliente correspondente ao item selecionado e
        # preenche os campos de entrada com essas informações.
        def selecionar_cliente(event):

            # Obtém os IDs dos itens selecionados na Treeview.
            # `arvore_clientes.selection()` retorna uma lista de IDs dos
            # itens atualmente selecionados.
            selecionado = arvore_clientes.selection()

            # Verifica se algum item foi selecionado.
            if selecionado:

                # Atualiza a variável `id_cliente_selecionado[0]` com o ID
                # do primeiro item selecionado.
                id_cliente_selecionado[0] = selecionado[0]

                # Busca o documento correspondente no banco de dados MongoDB
                # usando o ID selecionado.
                # `ObjectId(id_cliente_selecionado[0])` converte o ID selecionado para o
                # tipo ObjectId, necessário para consulta no MongoDB.
                cliente = self.colecao_clientes.find_one({"_id": ObjectId(id_cliente_selecionado[0])})

                # Verifica se o cliente foi encontrado no banco de dados.
                if cliente:

                    # Limpa o campo de entrada do nome e insere o nome do cliente.
                    entrada_nome_cliente.delete(0, tk.END)
                    entrada_nome_cliente.insert(tk.END, cliente["nome"])

                    # Limpa o campo de entrada do e-mail e insere o e-mail do cliente.
                    entrada_email_cliente.delete(0, tk.END)
                    entrada_email_cliente.insert(tk.END, cliente["email"])

                    # Limpa o campo de entrada do telefone e insere o telefone do cliente.
                    entrada_telefone_cliente.delete(0, tk.END)
                    entrada_telefone_cliente.insert(tk.END, cliente["telefone"])

            else:

                # Caso nenhum item esteja selecionado, reseta `id_cliente_selecionado[0]` para `None`.
                id_cliente_selecionado[0] = None

        # Associa o evento de seleção na Treeview (`<<TreeviewSelect>>`) à
        # função `selecionar_cliente`.
        # Quando o usuário seleciona um item na Treeview, a
        # função `selecionar_cliente` é chamada automaticamente.
        arvore_clientes.bind("<<TreeviewSelect>>", selecionar_cliente)

        # Cria um frame (`quadro_acoes`) para conter os botões de ação,
        # como atualizar ou excluir um cliente.
        # Parâmetros:
        # - `janela_cl`: Define o contêiner pai onde o frame será inserido.
        # - `bg="#f0f0f0"`: Define a cor de fundo do frame como
        # cinza claro, consistente com o estilo geral.
        quadro_acoes = tk.Frame(janela_cl, bg="#f0f0f0")

        # Posiciona o frame `quadro_acoes` abaixo da Treeview para
        # separar visualmente os botões de ação.
        # - `pady=10`: Adiciona 10 pixels de margem vertical ao redor do frame.
        quadro_acoes.pack(pady=10)

        # Define a função `atualizar_cliente`, que atualiza as informações de
        # um cliente no banco de dados com base nos dados
        # inseridos nos campos de entrada.
        def atualizar_cliente():

            # Verifica se existe um cliente selecionado.
            # `id_cliente_selecionado[0]` contém o ID do cliente atualmente selecionado.
            # Caso nenhum cliente esteja selecionado, exibe uma mensagem de
            # aviso e interrompe a execução da função.
            if not id_cliente_selecionado[0]:
                messagebox.showwarning("Aviso", "Nenhum cliente selecionado.", parent=janela_cl)
                return

            # Obtém os valores inseridos nos campos de entrada de
            # nome, e-mail e telefone, removendo espaços extras.
            nome = entrada_nome_cliente.get().strip()
            email = entrada_email_cliente.get().strip()
            telefone = entrada_telefone_cliente.get().strip()

            # Verifica se todos os campos de entrada estão preenchidos.
            # Caso algum campo esteja vazio, exibe uma mensagem de aviso e
            # interrompe a execução da função.
            if not nome or not email or not telefone:
                messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=janela_cl)
                return

            # Atualiza os dados do cliente no banco de dados MongoDB.
            # Parâmetros:
            # - `{"_id": ObjectId(id_cliente_selecionado[0])}`: Especifica o
            # cliente a ser atualizado, identificado pelo seu ID.
            # - `{"$set": {"nome": nome, "email": email, "telefone": telefone}}`:
            # Define os novos valores para os campos `nome`, `email` e `telefone`.
            self.colecao_clientes.update_one(
                {"_id": ObjectId(id_cliente_selecionado[0])},
                {"$set": {"nome": nome, "email": email, "telefone": telefone}}
            )

            # Chama a função `carregar_clientes` para atualizar a
            # lista de clientes exibida na Treeview.
            carregar_clientes()

            # Exibe uma mensagem de sucesso para informar que o
            # cliente foi atualizado com sucesso.
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!", parent=janela_cl)


        # Define a função `excluir_cliente`, que será usada para
        # remover um cliente selecionado do banco de dados.
        def excluir_cliente():

            # Verifica se há um cliente selecionado.
            # Caso contrário, exibe uma mensagem de aviso e
            # interrompe a execução da função.
            if not id_cliente_selecionado[0]:
                messagebox.showwarning("Aviso", "Nenhum cliente selecionado.", parent=janela_cl)
                return

            # Exibe uma caixa de diálogo de confirmação para o usuário.
            # `messagebox.askyesno` retorna `True` se o usuário clicar
            # em "Sim" e `False` caso contrário.
            confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja realmente excluir este cliente?", parent=janela_cl)

            # Verifica se o usuário confirmou a exclusão.
            if confirmar:

                # Procura no banco de dados consultas relacionadas ao cliente selecionado.
                # Caso existam consultas agendadas para o cliente,
                # impede a exclusão.
                consultas_existem = self.colecao_consultas.find_one(
                    {"cliente_id": ObjectId(id_cliente_selecionado[0])})

                if consultas_existem:

                    # Exibe um aviso informando que o cliente não pode ser
                    # excluído porque possui consultas agendadas.
                    messagebox.showwarning("Aviso",
                                           "Não é possível excluir um cliente que possui consultas agendadas.", parent=janela_cl)
                    return

                # Exclui o cliente da coleção de clientes no banco de dados MongoDB.
                # `delete_one` remove o documento identificado pelo `_id`
                # correspondente ao cliente selecionado.
                self.colecao_clientes.delete_one({"_id": ObjectId(id_cliente_selecionado[0])})

                # Recarrega a lista de clientes na interface gráfica
                # para refletir a exclusão.
                carregar_clientes()

                # Limpa os campos de entrada de nome, e-mail e telefone.
                entrada_nome_cliente.delete(0, tk.END)
                entrada_email_cliente.delete(0, tk.END)
                entrada_telefone_cliente.delete(0, tk.END)

                # Reseta a variável `id_cliente_selecionado` para indicar
                # que nenhum cliente está atualmente selecionado.
                id_cliente_selecionado[0] = None

                # Exibe uma mensagem informando que o cliente foi excluído com sucesso.
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!", parent=janela_cl)


        # Cria um botão estilizado chamado "Atualizar Cliente" dentro do frame `quadro_acoes`.
        # Parâmetros:
        # - `text="Atualizar Cliente"`: Define o texto exibido no botão.
        # - `command=atualizar_cliente`: Especifica a função `atualizar_cliente`
        # para ser executada ao clicar no botão.
        # `.grid(row=0, column=0, padx=10)` posiciona o botão na primeira
        # linha (índice 0) e primeira coluna do grid do frame,
        # com 10 pixels de espaçamento horizontal (padx).
        ttk.Button(quadro_acoes,
                   text="Atualizar Cliente",
                   command=atualizar_cliente).grid(row=0,
                                                   column=0,
                                                   padx=10)

        # Cria um botão estilizado chamado "Excluir Cliente" dentro
        # do frame `quadro_acoes`.
        # Parâmetros:
        # - `text="Excluir Cliente"`: Define o texto exibido no botão.
        # - `command=excluir_cliente`: Especifica a função `excluir_cliente`
        # para ser executada ao clicar no botão.
        # `.grid(row=0, column=1, padx=10)` posiciona o botão na primeira
        # linha (índice 0) e segunda coluna do grid do frame,
        # com 10 pixels de espaçamento horizontal (padx).
        ttk.Button(quadro_acoes,
                   text="Excluir Cliente",
                   command=excluir_cliente).grid(row=0,
                                                 column=1,
                                                 padx=10)

        # Chama a função `carregar_clientes` para inicializar a lista de
        # clientes na interface ao carregar o programa.
        carregar_clientes()


    # Define a função `janela_medicos`, que cria uma nova janela para
    # gerenciar os médicos no sistema.
    def janela_medicos(self):

        # Cria uma nova janela (janela filha) para gerenciar médicos.
        # `Toplevel` cria uma nova janela separada da janela principal.
        # `self.janela` é definida como a janela pai.
        janela_md = tk.Toplevel(self.janela)

        # Define o título da nova janela que será exibido na barra de título.
        janela_md.title("Gerenciar Médicos")

        # Define o tamanho inicial da janela como 600 pixels de
        # largura e 400 pixels de altura.
        janela_md.geometry("600x400")

        # Configura a cor de fundo da janela para cinza claro, usando o
        # código hexadecimal `#f0f0f0`.
        janela_md.configure(bg="#f0f0f0")

        # Define a janela para abrir maximizada na tela.
        janela_md.state('zoomed')

        # Cria um contêiner `LabelFrame` para agrupar os elementos do
        # formulário de cadastro de médicos.
        # Parâmetros:
        # - `janela_md`: Define a janela criada como o contêiner pai deste frame.
        # - `text="Cadastro de Médicos"`: Define o título exibido no contorno do frame.
        # - `bg="#f0f0f0"`: Define a cor de fundo do frame para manter a
        # consistência com a janela.
        # - `font=("Arial", 12, "bold")`: Define a fonte e o estilo do
        # texto do título do frame.
        quadro_form = tk.LabelFrame(janela_md,
                                    text="Cadastro de Médicos",
                                    bg="#f0f0f0",
                                    font=("Arial", 12, "bold"))

        # Posiciona o `quadro_form` na parte superior da janela.
        # - `side=tk.TOP`: Alinha o frame ao topo da janela.
        # - `fill='x'`: Faz o frame ocupar toda a largura da janela.
        # - `pady=10`: Adiciona 10 pixels de margem vertical acima e abaixo do frame.
        # - `padx=10`: Adiciona 10 pixels de margem horizontal nas laterais do frame.
        quadro_form.pack(side=tk.TOP, fill='x', pady=10, padx=10)

        # Cria um rótulo (`Label`) dentro do `quadro_form` para
        # identificar o campo "Nome do Médico".
        # Parâmetros:
        # - `text="Nome do Médico:"`: Define o texto exibido no rótulo.
        # - `bg="#f0f0f0"`: Define a cor de fundo para combinar com o frame.
        # - `font=("Arial", 11)`: Define a fonte e o tamanho do texto do rótulo.
        # - `.grid(row=0, column=0, padx=5, pady=5, sticky='e')`: Posiciona o
        # rótulo na primeira linha e primeira coluna da grade do frame,
        #   adicionando espaçamento de 5 pixels em todas as direções, e alinha o
        # texto à direita (sticky='e').
        tk.Label(quadro_form,
                 text="Nome do Médico:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=0,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (`Entry`) para que o usuário insira o nome do médico.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai onde o campo será inserido.
        # - `width=30`: Define a largura do campo, permitindo que até 30
        # caracteres sejam exibidos simultaneamente.
        # - `font=("Arial", 11)`: Define a fonte e o tamanho
        # do texto inserido no campo.
        entrada_nome_medico = tk.Entry(quadro_form,
                                       width=30,
                                       font=("Arial", 11))

        # Posiciona o campo de entrada na primeira linha e segunda coluna do `quadro_form`.
        # - `row=0`: Define que o campo estará na primeira linha da grade.
        # - `column=1`: Define que o campo estará na segunda coluna da grade.
        # - `padx=5`: Adiciona 5 pixels de espaçamento horizontal em ambos os lados.
        # - `pady=5`: Adiciona 5 pixels de espaçamento vertical acima e abaixo do campo.
        entrada_nome_medico.grid(row=0, column=1, padx=5, pady=5)

        # Define a função `adicionar_medico`, que é responsável por
        # adicionar um novo médico ao banco de dados.
        def adicionar_medico():

            # Obtém o texto inserido no campo de entrada `entrada_nome_medico` e
            # remove espaços extras ao redor.
            nome = entrada_nome_medico.get().strip()

            # Verifica se o campo `nome` está vazio.
            # Caso esteja, exibe uma mensagem de aviso e interrompe a
            # execução da função.
            if not nome:
                messagebox.showwarning("Aviso", "Informe o nome do médico.", parent=janela_md)
                return

            # Cria um dicionário com o nome do médico para ser inserido no banco de dados.
            # `{"nome": nome}`: Define a estrutura do documento a ser armazenado no MongoDB.
            novo_medico = {"nome": nome}

            # Insere o dicionário `novo_medico` na coleção de médicos (`colecao_medicos`) do MongoDB.
            # `insert_one` adiciona o novo médico como um documento na coleção.
            self.colecao_medicos.insert_one(novo_medico)

            # Limpa o campo de entrada para que o usuário possa adicionar outro médico facilmente.
            # `delete(0, tk.END)` remove todo o texto inserido no campo.
            entrada_nome_medico.delete(0, tk.END)

            # Atualiza a lista de médicos exibida na interface gráfica.
            # A função `carregar_medicos` recarrega os dados da coleção
            # `medicos` no MongoDB e exibe na interface.
            carregar_medicos()

            # Exibe uma mensagem de sucesso informando que o
            # médico foi adicionado com sucesso.
            messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!", parent=janela_md)

        # Cria um botão com o texto "Adicionar Médico" para inserir novos médicos no sistema.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner onde o botão será colocado.
        # - `text="Adicionar Médico"`: Define o texto exibido no botão.
        # - `command=adicionar_medico`: Especifica a função `adicionar_medico` a
        # ser chamada quando o botão for clicado.
        # `.grid(...)` posiciona o botão dentro do `quadro_form`:
        # - `row=1`: Coloca o botão na segunda linha do grid.
        # - `column=0`: Coloca o botão na primeira coluna do grid.
        # - `columnspan=2`: Faz o botão ocupar duas colunas, centralizando-o.
        # - `pady=10`: Adiciona 10 pixels de espaçamento vertical acima e abaixo do botão.
        ttk.Button(quadro_form,
                   text="Adicionar Médico",
                   command=adicionar_medico).grid(row=1,
                                                  column=0,
                                                  columnspan=2,
                                                  pady=10)


        # Cria um frame `quadro_lista` para conter a lista de médicos.
        # Parâmetros:
        # - `janela_md`: Define a janela `Gerenciar Médicos` como o contêiner pai.
        # - `bg="#f0f0f0"`: Define a cor de fundo do frame.
        quadro_lista = tk.Frame(janela_md, bg="#f0f0f0")

        # Posiciona o frame `quadro_lista` para ocupar todo o espaço restante da janela.
        # - `fill='both'`: Faz o frame preencher horizontal e verticalmente o espaço disponível.
        # - `expand=True`: Permite que o frame expanda caso a janela seja redimensionada.
        # - `pady=10`: Adiciona 10 pixels de margem vertical acima e abaixo do frame.
        # - `padx=10`: Adiciona 10 pixels de margem horizontal nas laterais do frame.
        quadro_lista.pack(fill='both', expand=True, pady=10, padx=10)

        # Cria uma barra de rolagem vertical para ser usada na lista de médicos.
        # Parâmetros:
        # - `quadro_lista`: Define o contêiner pai da barra de rolagem.
        barra_rolagem = tk.Scrollbar(quadro_lista)

        # Posiciona a barra de rolagem dentro do `quadro_lista`.
        # - `side=tk.RIGHT`: Alinha a barra de rolagem ao lado direito do frame.
        # - `fill=tk.Y`: Faz a barra de rolagem preencher toda a altura do frame.
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)

        # Cria uma tabela (Treeview) para exibir a lista de médicos.
        # Parâmetros:
        # - `quadro_lista`: Define o contêiner pai onde a tabela será inserida.
        # - `columns=("Nome",)`: Define as colunas da tabela; neste caso, apenas a coluna "Nome".
        # - `show="headings"`: Exibe apenas os cabeçalhos das colunas, sem coluna extra para seleção.
        # - `height=10`: Define a altura da tabela, permitindo exibir até 10 linhas simultaneamente.
        # - `yscrollcommand=barra_rolagem.set`: Vincula a barra de rolagem à tabela.
        arvore_medicos = ttk.Treeview(quadro_lista,
                                      columns=("Nome",),
                                      show="headings",
                                      height=10,
                                      yscrollcommand=barra_rolagem.set)

        # Configura o cabeçalho da coluna "Nome" com o texto "Nome".
        arvore_medicos.heading("Nome", text="Nome")

        # Define a largura da coluna "Nome" como 200 pixels para
        # garantir visibilidade suficiente.
        arvore_medicos.column("Nome", width=200)

        # Posiciona a tabela (Treeview) dentro do frame `quadro_lista`.
        # - `fill='both'`: Faz a tabela preencher horizontal e
        # verticalmente o espaço disponível no frame.
        # - `expand=True`: Permite que a tabela expanda caso o frame ou
        # a janela seja redimensionada.
        arvore_medicos.pack(fill='both', expand=True)

        # Configura a barra de rolagem para controlar a visualização vertical da tabela.
        # O método `yscrollcommand` da tabela é vinculado ao comando da barra de rolagem.
        barra_rolagem.config(command=arvore_medicos.yview)

        # Cria uma lista para armazenar o ID do médico atualmente selecionado.
        # - `[None]`: Inicializa a lista com o valor `None`, indicando que
        # nenhum médico está selecionado no início.
        id_medico_selecionado = [None]

        # Define a função `carregar_medicos`, responsável por carregar a
        # lista de médicos na tabela (Treeview) da interface gráfica.
        def carregar_medicos():

            # Remove todos os itens existentes na tabela `arvore_medicos`
            # antes de recarregar os dados.
            # O método `get_children` retorna todos os IDs das linhas atualmente na tabela.
            # `delete(item)` remove cada linha da tabela.
            for item in arvore_medicos.get_children():
                arvore_medicos.delete(item)

            # Busca todos os documentos na coleção `medicos` do MongoDB.
            # `self.colecao_medicos.find()` retorna um cursor que itera
            # sobre todos os médicos cadastrados.
            medicos = self.colecao_medicos.find()

            # Itera sobre os médicos retornados do banco de dados.
            for m in medicos:

                # Insere cada médico na tabela `arvore_medicos`.
                # Parâmetros:
                # - `""`: Indica que a nova linha será adicionada na
                # raiz da tabela (sem hierarquia).
                # - `tk.END`: Insere o item no final da tabela.
                # - `values=(m["nome"],)`: Define os valores exibidos nas colunas da
                # tabela. Neste caso, apenas o nome do médico.
                # - `iid=str(m["_id"])`: Define o identificador único da linha
                # como o `_id` do médico no MongoDB, convertido para string.
                arvore_medicos.insert("",
                                      tk.END,
                                      values=(m["nome"],), iid=str(m["_id"]))

            # Redefine a variável `id_medico_selecionado` para `None`, indicando
            # que nenhum médico está atualmente selecionado.
            id_medico_selecionado[0] = None


        # Define a função `selecionar_medico`, que será executada ao
        # selecionar um médico na tabela `arvore_medicos`.
        def selecionar_medico(event):

            # Obtém os IDs das linhas selecionadas na tabela `arvore_medicos`.
            # O método `selection()` retorna uma lista de IDs das
            # linhas atualmente selecionadas.
            selecionado = arvore_medicos.selection()

            # Verifica se existe alguma linha selecionada.
            if selecionado:

                # Atualiza a variável `id_medico_selecionado` com o ID da linha selecionada.
                # Como apenas um médico pode ser selecionado, é usado o
                # primeiro item da lista retornada.
                id_medico_selecionado[0] = selecionado[0]

                # Busca no banco de dados o médico correspondente ao ID selecionado.
                # `ObjectId(id_medico_selecionado[0])` converte o ID da linha
                # para o formato usado pelo MongoDB.
                medico = self.colecao_medicos.find_one({"_id": ObjectId(id_medico_selecionado[0])})

                # Verifica se o médico foi encontrado no banco de dados.
                if medico:

                    # Limpa o campo de entrada `entrada_nome_medico` antes de
                    # inserir o nome do médico selecionado.
                    # `delete(0, tk.END)` remove todo o texto existente no campo.
                    entrada_nome_medico.delete(0, tk.END)

                    # Insere o nome do médico no campo de entrada.
                    # `insert(tk.END, medico["nome"])` adiciona o nome do
                    # médico no final do campo.
                    entrada_nome_medico.insert(tk.END, medico["nome"])

            else:

                # Se nenhuma linha for selecionada, redefine `id_medico_selecionado` para `None`,
                # indicando que nenhum médico está atualmente selecionado.
                id_medico_selecionado[0] = None

        # Vincula a função `selecionar_medico` ao evento de seleção de uma
        # linha na tabela `arvore_medicos`.
        # O evento `<<TreeviewSelect>>` é disparado sempre que uma linha é
        # selecionada na tabela.
        arvore_medicos.bind("<<TreeviewSelect>>", selecionar_medico)

        # Cria um frame `quadro_acoes` para organizar os botões de ações, como
        # atualizar ou excluir médicos.
        # Parâmetros:
        # - `janela_md`: Define a janela `Gerenciar Médicos` como o contêiner pai.
        # - `bg="#f0f0f0"`: Define a cor de fundo do frame.
        quadro_acoes = tk.Frame(janela_md, bg="#f0f0f0")

        # Posiciona o frame `quadro_acoes` abaixo da tabela.
        # - `pady=10`: Adiciona 10 pixels de margem vertical acima e abaixo do frame.
        quadro_acoes.pack(pady=10)

        # Define a função `atualizar_medico`, que atualiza o nome de
        # um médico no banco de dados.
        def atualizar_medico():

            # Verifica se algum médico está selecionado na tabela.
            # Caso contrário, exibe uma mensagem de aviso e interrompe a execução da função.
            if not id_medico_selecionado[0]:
                messagebox.showwarning("Aviso", "Nenhum médico selecionado.", parent=janela_md)
                return

            # Obtém o nome digitado no campo `entrada_nome_medico` e
            # remove quaisquer espaços extras.
            nome = entrada_nome_medico.get().strip()

            # Verifica se o campo `nome` está vazio.
            # Se estiver, exibe uma mensagem de aviso e interrompe a execução da função.
            if not nome:
                messagebox.showwarning("Aviso", "Preencha o nome do médico.", parent=janela_md)
                return

            # Atualiza o registro do médico no banco de dados.
            # Parâmetros:
            # - `{"_id": ObjectId(id_medico_selecionado[0])}`: Filtro para
            # encontrar o médico pelo seu ID.
            # - `{"$set": {"nome": nome}}`: Atualiza o campo "nome" do médico
            # com o novo valor digitado.
            self.colecao_medicos.update_one({"_id": ObjectId(id_medico_selecionado[0])}, {"$set": {"nome": nome}})

            # Recarrega os médicos na tabela para refletir a alteração feita.
            carregar_medicos()

            # Exibe uma mensagem de sucesso informando que o médico foi atualizado com êxito.
            messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!", parent=janela_md)

        # Define a função `excluir_medico`, responsável por excluir um
        # médico selecionado do banco de dados.
        def excluir_medico():

            # Verifica se algum médico está selecionado na tabela.
            # Caso contrário, exibe uma mensagem de aviso e interrompe a execução da função.
            if not id_medico_selecionado[0]:
                messagebox.showwarning("Aviso", "Nenhum médico selecionado.", parent=janela_md)
                return

            # Exibe uma caixa de diálogo de confirmação para garantir que o
            # usuário realmente deseja excluir o médico.
            # Se o usuário confirmar (clicar em "Sim"), o valor de `confirmar` será `True`.
            confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja realmente excluir este médico?", parent=janela_md)

            # Verifica se o usuário confirmou a exclusão.
            if confirmar:

                # Verifica se o médico selecionado possui consultas agendadas.
                # Busca no banco de dados qualquer consulta associada
                # ao ID do médico selecionado.
                consultas_existem = self.colecao_consultas.find_one(
                    {"medico_id": ObjectId(id_medico_selecionado[0])})

                # Se houver consultas associadas ao médico, exibe um aviso e
                # interrompe a função.
                if consultas_existem:
                    messagebox.showwarning("Aviso",
                                           "Não é possível excluir um médico que possui consultas agendadas.", parent=janela_md)
                    return

                # Exclui o médico do banco de dados usando o ID selecionado.
                # `delete_one` remove o documento correspondente ao filtro especificado.
                self.colecao_medicos.delete_one({"_id": ObjectId(id_medico_selecionado[0])})

                # Atualiza a tabela de médicos para refletir a exclusão.
                carregar_medicos()

                # Limpa o campo de entrada `entrada_nome_medico` após a exclusão.
                entrada_nome_medico.delete(0, tk.END)

                # Redefine a variável `id_medico_selecionado` para `None`,
                # indicando que nenhum médico está selecionado.
                id_medico_selecionado[0] = None

                # Exibe uma mensagem de sucesso informando que o médico foi excluído com êxito.
                messagebox.showinfo("Sucesso", "Médico excluído com sucesso!", parent=janela_md)

        # Cria um botão "Atualizar Médico" para permitir a edição do médico selecionado.
        # Parâmetros:
        # - `quadro_acoes`: Contêiner onde o botão será inserido.
        # - `text="Atualizar Médico"`: Texto exibido no botão.
        # - `command=atualizar_medico`: Função chamada quando o botão é clicado.
        # `.grid(...)` posiciona o botão:
        # - `row=0`: Coloca o botão na primeira linha do grid.
        # - `column=0`: Coloca o botão na primeira coluna do grid.
        # - `padx=10`: Adiciona 10 pixels de margem horizontal.
        ttk.Button(quadro_acoes, text="Atualizar Médico", command=atualizar_medico).grid(row=0, column=0, padx=10)

        # Cria um botão "Excluir Médico" para excluir o médico selecionado.
        # Parâmetros:
        # - `quadro_acoes`: Contêiner onde o botão será inserido.
        # - `text="Excluir Médico"`: Texto exibido no botão.
        # - `command=excluir_medico`: Função chamada quando o botão é clicado.
        # `.grid(...)` posiciona o botão:
        # - `row=0`: Coloca o botão na primeira linha do grid.
        # - `column=1`: Coloca o botão na segunda coluna do grid.
        # - `padx=10`: Adiciona 10 pixels de margem horizontal.
        ttk.Button(quadro_acoes, text="Excluir Médico", command=excluir_medico).grid(row=0, column=1, padx=10)

        # Chama a função `carregar_medicos` para inicializar a tabela
        # com os dados de médicos do banco.
        carregar_medicos()


    # Define a função `janela_consultas`, responsável por abrir uma
    # nova janela para gerenciar consultas.
    def janela_consultas(self):

        # Cria uma nova janela (`Toplevel`) como filha da janela principal (`self.janela`).
        # Essa janela será usada para agendar e gerenciar consultas.
        janela_co = tk.Toplevel(self.janela)

        # Define o título da nova janela como "Agendar/Gerenciar Consultas".
        # Esse título aparece na barra de título da janela.
        janela_co.title("Agendar/Gerenciar Consultas")

        # Define o tamanho da janela como 1000x600 pixels (largura x altura).
        janela_co.geometry("1000x600")

        # Configura o fundo da janela com uma cor cinza claro (código hexadecimal `#f0f0f0`).
        janela_co.configure(bg="#f0f0f0")

        # Define a janela para abrir maximizada na tela.
        janela_co.state('zoomed')

        # Cria um `LabelFrame` chamado `quadro_form` dentro da janela.
        # O `LabelFrame` serve como um contêiner visual, com um título,
        # para agrupar widgets relacionados.
        # Parâmetros:
        # - `janela_co`: Define a janela `janela_co` como o contêiner pai.
        # - `text="Agendamento de Consultas"`: Título exibido no topo do quadro.
        # - `bg="#f0f0f0"`: Define a cor de fundo como cinza claro, para
        # harmonizar com o restante da interface.
        # - `font=("Arial", 12, "bold")`: Define a fonte do título do quadro
        # como Arial, tamanho 12, em negrito.
        quadro_form = tk.LabelFrame(
            janela_co,
            text="Agendamento de Consultas",
            bg="#f0f0f0",
            font=("Arial", 12, "bold")
        )

        # Posiciona o `quadro_form` no topo da janela (`side=tk.TOP`) e o faz
        # preencher horizontalmente o espaço disponível (`fill='x'`).
        # Adiciona margens:
        # - `pady=10`: Espaço vertical de 10 pixels acima e abaixo do quadro.
        # - `padx=10`: Espaço horizontal de 10 pixels à esquerda e à direita do quadro.
        quadro_form.pack(side=tk.TOP, fill='x', pady=10, padx=10)

        # Cria um rótulo (Label) dentro do `quadro_form` para identificar o campo do cliente.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai do rótulo como `quadro_form`.
        # - `text="Cliente:"`: Texto exibido no rótulo.
        # - `bg="#f0f0f0"`: Define a cor de fundo como cinza claro,
        # harmonizando com o fundo do quadro.
        # - `font=("Arial", 11)`: Define a fonte do texto como Arial tamanho 11.
        # - `.grid(...)`: Posiciona o rótulo na grade:
        #   - `row=0, column=0`: Na primeira linha e primeira coluna do `quadro_form`.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        #   - `sticky='e'`: Alinha o rótulo à direita dentro da célula da grade.
        tk.Label(quadro_form,
                 text="Cliente:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=0,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria uma variável do tipo `StringVar` para armazenar o
        # valor selecionado no campo de cliente.
        # Essa variável será vinculada ao `Combobox` para
        # facilitar a recuperação do valor.
        var_cliente_consulta = tk.StringVar()

        # Cria um widget `Combobox` para selecionar um cliente.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `textvariable=var_cliente_consulta`: Vincula a variável
        # `var_cliente_consulta` ao `Combobox`.
        # - `state='readonly'`: Torna o `Combobox` somente leitura,
        # permitindo apenas seleções das opções disponíveis.
        # - `font=("Arial", 11)`: Define a fonte como Arial tamanho 11.
        # - `width=40`: Define a largura do `Combobox` para exibir até 40 caracteres.
        combo_cliente_consulta = ttk.Combobox(quadro_form,
                                              textvariable=var_cliente_consulta,
                                              state='readonly',
                                              font=("Arial", 11),
                                              width=40)

        # Posiciona o `Combobox` na grade do `quadro_form`.
        # - `row=0, column=1`: Na primeira linha e segunda coluna.
        # - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        # - `sticky='w'`: Alinha o `Combobox` à esquerda dentro da célula da grade.
        combo_cliente_consulta.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Recupera a lista de clientes armazenados na coleção `clientes`
        # do banco de dados MongoDB.
        # `self.colecao_clientes.find()`: Retorna todos os
        # documentos da coleção de clientes.
        clientes = self.colecao_clientes.find()

        # Cria uma lista de strings com os dados dos clientes no formato "ID - Nome".
        # Para cada cliente (`c`) encontrado no banco:
        # - `c['_id']`: Obtém o ID único do cliente.
        # - `c['nome']`: Obtém o nome do cliente.
        # - `f"{c['_id']} - {c['nome']}"`: Formata os dados no formato desejado.
        lista_clientes = [f"{c['_id']} - {c['nome']}" for c in clientes]

        # Configura o `Combobox` para exibir a lista de clientes
        # como opções disponíveis para seleção.
        combo_cliente_consulta['values'] = lista_clientes

        # Cria um rótulo (Label) para identificar o campo de seleção de médicos.
        # Parâmetros:
        # - `quadro_form`: O contêiner pai onde o rótulo será exibido.
        # - `text="Médico:"`: Define o texto exibido no rótulo.
        # - `bg="#f0f0f0"`: Define a cor de fundo como cinza claro,
        # consistente com o restante do formulário.
        # - `font=("Arial", 11)`: Define a fonte como Arial tamanho 11.
        # - `.grid(...)`: Posiciona o rótulo na grade do `quadro_form`:
        #   - `row=1, column=0`: Na segunda linha e primeira coluna do quadro.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        #   - `sticky='e'`: Alinha o rótulo à direita dentro da célula da grade.
        tk.Label(quadro_form,
                 text="Médico:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=1,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria uma variável `StringVar` para armazenar o valor
        # selecionado no campo de médico.
        # Essa variável será vinculada ao `Combobox` para capturar o médico escolhido.
        var_medico_consulta = tk.StringVar()

        # Cria um widget `Combobox` para selecionar um médico da lista de opções.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `textvariable=var_medico_consulta`: Vincula a variável
        # `var_medico_consulta` ao `Combobox`.
        # - `state='readonly'`: Torna o `Combobox` somente leitura,
        # permitindo apenas seleções das opções disponíveis.
        # - `font=("Arial", 11)`: Define a fonte como Arial tamanho 11.
        # - `width=40`: Define a largura do `Combobox`, suficiente para
        # exibir nomes mais longos.
        combo_medico_consulta = ttk.Combobox(quadro_form,
                                             textvariable=var_medico_consulta,
                                             state='readonly',
                                             font=("Arial", 11),
                                             width=40)

        # Posiciona o `Combobox` na grade do `quadro_form`.
        # - `row=1, column=1`: Na segunda linha e segunda coluna do quadro.
        # - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        # - `sticky='w'`: Alinha o `Combobox` à esquerda dentro da célula da grade.
        combo_medico_consulta.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Recupera todos os médicos cadastrados na coleção `medicos`
        # do banco de dados MongoDB.
        # `self.colecao_medicos.find()`: Retorna todos os documentos da coleção de médicos.
        medicos = self.colecao_medicos.find()

        # Cria uma lista de strings formatadas para exibir os médicos no `Combobox`.
        # Para cada médico (`m`) encontrado no banco:
        # - `m['_id']`: Obtém o ID único do médico.
        # - `m['nome']`: Obtém o nome do médico.
        # - `f"{m['_id']} - {m['nome']}"`: Formata os dados no formato "ID - Nome".
        lista_medicos = [f"{m['_id']} - {m['nome']}" for m in medicos]

        # Configura o `Combobox` para exibir a lista de médicos como
        # opções disponíveis para seleção.
        combo_medico_consulta['values'] = lista_medicos

        # Cria um rótulo (Label) para identificar o campo de entrada de data.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `text="Data:"`: Define o texto exibido no rótulo, indicando que o
        # campo é para a entrada da data.
        # - `bg="#f0f0f0"`: Define a cor de fundo do rótulo como cinza claro,
        # consistente com o restante do formulário.
        # - `font=("Arial", 11)`: Define a fonte como Arial tamanho 11.
        # - `.grid(...)`: Posiciona o rótulo na grade do `quadro_form`:
        #   - `row=2, column=0`: Na terceira linha e primeira coluna do quadro.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        #   - `sticky='e'`: Alinha o rótulo à direita dentro da célula da grade.
        tk.Label(quadro_form,
                 text="Data:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=2,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (Entry) para o usuário inserir a data da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `width=20`: Define a largura do campo, suficiente para entradas no formato "YYYY-MM-DD".
        # - `font=("Arial", 11)`: Define a fonte do texto inserido no campo como Arial tamanho 11.
        entrada_data_consulta = tk.Entry(quadro_form,
                                         width=20,
                                         font=("Arial", 11))

        # Posiciona o campo de entrada de data na grade do `quadro_form`.
        # - `row=2, column=1`: Na terceira linha e segunda coluna do quadro.
        # - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        # - `sticky='w'`: Alinha o campo à esquerda dentro da célula da grade.
        entrada_data_consulta.grid(row=2,
                                   column=1,
                                   padx=5,
                                   pady=5,
                                   sticky='w')

        def selecionar_data():

            # Cria uma nova janela para selecionar a data.
            # `Toplevel` cria uma janela secundária sobre a principal (`janela_co`).
            janela_data = tk.Toplevel(janela_co)

            # Define o título da janela como "Selecionar Data".
            janela_data.title("Selecionar Data")

            # Define as dimensões da janela em 300x300 pixels.
            janela_data.geometry("300x300")

            # Cria um widget de calendário para permitir que o
            # usuário escolha uma data.
            # Parâmetros:
            # - `janela_data`: Define a janela pai como `janela_data`.
            # - `selectmode='day'`: Permite selecionar apenas um dia por vez.
            # - `date_pattern='y-mm-dd'`: Define o formato da data como ano-mês-dia.
            cal = Calendar(janela_data,
                           selectmode='day',
                           date_pattern='y-mm-dd')

            # Posiciona o calendário na janela e adiciona um
            # espaçamento vertical de 10 pixels.
            cal.pack(pady=10)

            # Define uma função interna para confirmar a seleção da data.
            def confirmar_data():

                # Obtém a data selecionada no calendário.
                data_sel = cal.get_date()

                # Remove o conteúdo atual do campo de entrada de
                # data (`entrada_data_consulta`).
                entrada_data_consulta.delete(0, tk.END)

                # Insere a data selecionada no campo de entrada de data.
                entrada_data_consulta.insert(tk.END, data_sel)

                # Fecha a janela de seleção de data.
                janela_data.destroy()

            # Cria um botão "Confirmar" para finalizar a seleção de data.
            # Parâmetros:
            # - `janela_data`: Define a janela pai como `janela_data`.
            # - `text="Confirmar"`: Define o texto do botão como "Confirmar".
            # - `command=confirmar_data`: Associa o clique do botão à função `confirmar_data`.
            ttk.Button(janela_data, text="Confirmar", command=confirmar_data).pack(pady=10)

        # Cria um botão "Selecionar Data" que abre a janela de
        # seleção de data ao ser clicado.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `text="Selecionar Data"`: Define o texto exibido no botão.
        # - `command=selecionar_data`: Vincula o clique do botão à
        # função `selecionar_data`, que abre a janela de calendário.
        # - `.grid(...)`: Posiciona o botão na grade do `quadro_form`:
        #   - `row=2, column=2`: Na terceira linha e terceira coluna do quadro.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais
        # de 5 pixels para espaçamento.
        ttk.Button(quadro_form,
                   text="Selecionar Data",
                   command=selecionar_data).grid(row=2,
                                                 column=2,
                                                 padx=5,
                                                 pady=5)

        # Cria um rótulo (Label) para identificar o campo de entrada
        # da hora de início da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `text="Hora Início (HH:MM):"`: Define o texto exibido no
        # rótulo, especificando o formato esperado.
        # - `bg="#f0f0f0"`: Define a cor de fundo como cinza claro,
        # consistente com o restante do formulário.
        # - `font=("Arial", 11)`: Define a fonte como Arial tamanho 11.
        # - `.grid(...)`: Posiciona o rótulo na grade do `quadro_form`:
        #   - `row=3, column=0`: Na quarta linha e primeira coluna do quadro.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        #   - `sticky='e'`: Alinha o rótulo à direita dentro da célula da grade.
        tk.Label(quadro_form,
                 text="Hora Início (HH:MM):",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=3,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (Entry) para o usuário inserir a
        # hora de início da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `width=20`: Define a largura do campo, suficiente para o formato de hora (HH:MM).
        # - `font=("Arial", 11)`: Define a fonte do texto inserido no campo como Arial tamanho 11.
        entrada_hora_inicio = tk.Entry(quadro_form, width=20, font=("Arial", 11))

        # Posiciona o campo de entrada da hora de início na grade do `quadro_form`.
        # - `row=3, column=1`: Na quarta linha e segunda coluna do quadro.
        # - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        # - `sticky='w'`: Alinha o campo à esquerda dentro da célula da grade.
        entrada_hora_inicio.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Cria um rótulo (Label) para identificar o campo de
        # entrada da hora final da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `text="Hora Final (HH:MM):"`: Define o texto exibido no rótulo,
        # especificando o formato esperado.
        # - `bg="#f0f0f0"`: Define a cor de fundo como cinza claro, mantendo consistência visual.
        # - `font=("Arial", 11)`: Define a fonte do texto como Arial tamanho 11.
        # - `.grid(...)`: Posiciona o rótulo na grade do `quadro_form`:
        #   - `row=4, column=0`: Na quinta linha e primeira coluna do quadro.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        #   - `sticky='e'`: Alinha o rótulo à direita dentro da célula da grade.
        tk.Label(quadro_form,
                 text="Hora Final (HH:MM):",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=4,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria um campo de entrada (Entry) para o usuário inserir a hora final da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `width=20`: Define a largura do campo, suficiente para o formato de hora (HH:MM).
        # - `font=("Arial", 11)`: Define a fonte do texto no campo como Arial tamanho 11.
        entrada_hora_final = tk.Entry(quadro_form,
                                      width=20,
                                      font=("Arial", 11))

        # Posiciona o campo de entrada da hora final na grade do `quadro_form`.
        # - `row=4, column=1`: Na quinta linha e segunda coluna do quadro.
        # - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        # - `sticky='w'`: Alinha o campo à esquerda dentro da célula da grade.
        entrada_hora_final.grid(row=4,
                                column=1,
                                padx=5,
                                pady=5,
                                sticky='w')

        # Cria um rótulo (Label) para identificar o campo de descrição da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `text="Descrição:"`: Define o texto exibido no rótulo,
        # indicando que o campo abaixo é para descrição.
        # - `bg="#f0f0f0"`: Define a cor de fundo como cinza claro.
        # - `font=("Arial", 11)`: Define a fonte como Arial tamanho 11.
        # - `.grid(...)`: Posiciona o rótulo na grade do `quadro_form`:
        #   - `row=5, column=0`: Na sexta linha e primeira coluna do quadro.
        #   - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        #   - `sticky='ne'`: Alinha o rótulo à direita e ao topo da
        # célula, pois o campo de texto associado ocupa mais de uma linha.
        tk.Label(quadro_form,
                 text="Descrição:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=5,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='ne')

        # Cria um campo de texto (Text) para o usuário inserir uma descrição da consulta.
        # Parâmetros:
        # - `quadro_form`: Define o contêiner pai como `quadro_form`.
        # - `width=50`: Define a largura do campo de texto, equivalente a 50 caracteres.
        # - `height=4`: Define a altura do campo, suficiente para 4 linhas de texto.
        # - `font=("Arial", 11)`: Define a fonte do texto no campo como Arial tamanho 11.
        texto_descricao_consulta = tk.Text(quadro_form,
                                           width=50,
                                           height=4,
                                           font=("Arial", 11))

        # Posiciona o campo de texto de descrição na grade do `quadro_form`.
        # - `row=5, column=1`: Na sexta linha e segunda coluna do quadro.
        # - `padx=5, pady=5`: Adiciona margens horizontais e verticais de 5 pixels.
        # - `sticky='w'`: Alinha o campo à esquerda dentro da célula da grade.
        texto_descricao_consulta.grid(row=5,
                                      column=1,
                                      padx=5,
                                      pady=5,
                                      sticky='w')

        # Função para verificar se dois intervalos de tempo (início e fim) se sobrepõem.
        def intervalos_conflitam(inicio1, fim1, inicio2, fim2):

            # Define uma função interna que converte um horário no
            # formato HH:MM para minutos do dia.
            # Parâmetros:
            # - `hm`: Uma string representando o horário (ex.: "14:30").
            # Retorna:
            # - O equivalente do horário em minutos desde 00:00 (ex.: "14:30" -> 870 minutos).
            def hm_para_min(hm):

                # Divide a string no formato HH:MM em duas partes: hora (h) e minuto (m).
                h, m = hm.split(':')

                # Converte as partes em inteiros e retorna o total em minutos.
                return int(h) * 60 + int(m)

            # Converte os horários de início e fim do primeiro intervalo para minutos.
            ini1 = hm_para_min(inicio1)  # Horário de início do primeiro intervalo.
            fi1 = hm_para_min(fim1)  # Horário de fim do primeiro intervalo.

            # Converte os horários de início e fim do segundo intervalo para minutos.
            ini2 = hm_para_min(inicio2)  # Horário de início do segundo intervalo.
            fi2 = hm_para_min(fim2)  # Horário de fim do segundo intervalo.

            # Verifica se os intervalos se sobrepõem:
            # Condição:
            # - Um intervalo começa antes do outro terminar (`ini1 < fi2`).
            # - Um intervalo termina depois do outro começar (`fi1 > ini2`).
            return (ini1 < fi2) and (fi1 > ini2)

        # Função responsável por agendar uma nova consulta após
        # validar os dados inseridos pelo usuário.
        def agendar_consulta():

            # Obtém e remove espaços extras dos valores
            # inseridos nos campos do formulário.
            # `cliente_selecionado`: Nome e ID do cliente selecionado no combo box.
            cliente_selecionado = var_cliente_consulta.get().strip()

            # `medico_selecionado`: Nome e ID do médico selecionado no combo box.
            medico_selecionado = var_medico_consulta.get().strip()

            # `data_str`: Data inserida pelo usuário no formato
            # esperado (yyyy-mm-dd).
            data_str = entrada_data_consulta.get().strip()

            # `hora_ini_str`: Horário de início da consulta no formato HH:MM.
            hora_ini_str = entrada_hora_inicio.get().strip()

            # `hora_fim_str`: Horário de término da consulta no formato HH:MM.
            hora_fim_str = entrada_hora_final.get().strip()

            # `descricao`: Detalhes da consulta inseridos na caixa de texto.
            descricao = texto_descricao_consulta.get("1.0", tk.END).strip()

            # Verifica se todos os campos obrigatórios estão preenchidos.
            # Caso algum campo esteja vazio, exibe uma mensagem de aviso ao
            # usuário e interrompe a execução da função.
            if not cliente_selecionado or not medico_selecionado or not data_str or not hora_ini_str or not hora_fim_str or not descricao:
                messagebox.showwarning("Aviso", "Preencha todos os campos da consulta.", parent=janela_co)
                return

            # Tenta obter o ID do cliente a partir do texto selecionado no combo box.
            try:

                # Divide o texto do cliente selecionado em ID e nome.
                cliente_id_str, _ = cliente_selecionado.split(" - ", 1)

                # Converte o ID do cliente para o tipo `ObjectId` utilizado pelo MongoDB.
                cliente_id = ObjectId(cliente_id_str)

            except:

                # Caso a conversão falhe, exibe uma mensagem de aviso informando que o
                # cliente deve ser selecionado corretamente.
                messagebox.showwarning("Aviso", "Selecione corretamente o cliente.", parent=janela_co)
                return

            try:

                # Tenta obter o ID do médico a partir do texto selecionado no combo box.
                # Divide o texto do médico selecionado em ID e nome.
                medico_id_str, _ = medico_selecionado.split(" - ", 1)

                # Converte o ID do médico para o tipo `ObjectId` usado no MongoDB.
                medico_id = ObjectId(medico_id_str)

            except:

                # Caso a conversão falhe, exibe uma mensagem de aviso informando que o
                # médico deve ser selecionado corretamente.
                messagebox.showwarning("Aviso", "Selecione corretamente o médico.", parent=janela_co)
                return

            try:

                # Verifica se a data fornecida está no formato correto "yyyy-mm-dd".
                # `datetime.datetime.strptime` valida e converte a string para
                # um objeto datetime.
                datetime.datetime.strptime(data_str, "%Y-%m-%d")

                # Verifica se o horário de início está no formato correto "HH:MM".
                datetime.datetime.strptime(hora_ini_str, "%H:%M")

                # Verifica se o horário de término está no formato correto "HH:MM".
                datetime.datetime.strptime(hora_fim_str, "%H:%M")

            except ValueError:

                # Caso algum dos valores (data, hora de início ou hora de
                # término) esteja em formato incorreto,
                # exibe uma mensagem de aviso ao usuário.
                messagebox.showwarning("Aviso", "Data, Hora Início ou Hora Final inválida(s). Formato HH:MM.", parent=janela_co)
                return

            # Verificar se existe conflito no mesmo dia com o mesmo médico
            # A consulta ao banco de dados encontra todas as consultas agendadas
            # para o mesmo médico e no mesmo dia
            # Isso é feito buscando no MongoDB, filtrando pelo
            # campo "medico_id" e "data".
            consultas_medico_dia = self.colecao_consultas.find({"medico_id": medico_id, "data": data_str})

            # Itera sobre todas as consultas do médico no mesmo dia
            for c in consultas_medico_dia:

                # Obtém o horário de início e fim da consulta já agendada.
                # Caso o horário não esteja presente, assume um valor
                # padrão "00:00" (utilizado como fallback).
                h_ini_exist = c.get("hora_inicio", c.get("hora", "00:00"))
                h_fim_exist = c.get("hora_final", h_ini_exist)

                # Verifica se existe conflito de horário entre a nova consulta e
                # as consultas já agendadas
                # A função `intervalos_conflitam` verifica se os horários se sobrepõem.
                if intervalos_conflitam(hora_ini_str, hora_fim_str, h_ini_exist, h_fim_exist):

                    # Caso exista um conflito de horário, exibe uma mensagem ao usuário
                    # Avisando sobre o conflito com outra consulta do mesmo médico no mesmo dia.
                    messagebox.showwarning("Aviso", "Conflito de horário com outra consulta deste médico.", parent=janela_co)

                    # Interrompe a execução da função caso haja um conflito
                    return

            # Caso não haja conflito de horários, prossegue com o agendamento da nova consulta
            # Define os dados da nova consulta em um dicionário.
            nova_consulta = {
                "cliente_id": cliente_id,  # ID do cliente
                "medico_id": medico_id,  # ID do médico
                "data": data_str,  # Data da consulta
                "hora_inicio": hora_ini_str,  # Horário de início da consulta
                "hora_final": hora_fim_str,  # Horário de término da consulta
                "descricao": descricao  # Descrição da consulta
            }

            # Inserir a nova consulta no banco de dados MongoDB
            # Após garantir que não há conflitos de horário e que todos os
            # campos estão preenchidos corretamente,
            # a nova consulta é inserida na coleção "consultas" do
            # banco de dados MongoDB.
            self.colecao_consultas.insert_one(nova_consulta)

            # Limpar os campos de entrada após o agendamento da consulta
            # O método `delete(0, tk.END)` é utilizado para limpar os campos de
            # texto e entradas, removendo qualquer valor digitado.
            entrada_data_consulta.delete(0, tk.END)  # Limpa o campo de entrada de data da consulta
            entrada_hora_inicio.delete(0, tk.END)  # Limpa o campo de entrada de hora de início
            entrada_hora_final.delete(0, tk.END)  # Limpa o campo de entrada de hora final
            texto_descricao_consulta.delete("1.0", tk.END)  # Limpa o campo de descrição da consulta

            # Resetar os valores selecionados nos combo boxes
            # `set("")` é utilizado para limpar o conteúdo dos combo
            # boxes, removendo a seleção anterior.
            var_cliente_consulta.set("")  # Limpa a seleção do cliente
            var_medico_consulta.set("")  # Limpa a seleção do médico

            # Atualizar a lista de consultas
            # Chama a função `atualizar_lista_consultas()` para garantir que a
            # lista de consultas exibida na interface
            # seja atualizada com a nova consulta agendada.
            atualizar_lista_consultas()

            # Exibir uma mensagem de sucesso ao usuário
            # Após o sucesso do agendamento, uma caixa de diálogo de
            # informação é exibida para o usuário,
            # informando que a consulta foi agendada corretamente.
            messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!", parent=janela_co)


        # Cria o botão "Agendar Consulta" que, quando pressionado, chama a
        # função agendar_consulta.
        # Esse botão é posicionado no quadro de formulário (quadro_form) com o
        # texto exibido como "Agendar Consulta".
        # O comando que será executado ao clicar no botão é a função agendar_consulta(),
        # que será responsável por agendar uma nova consulta.
        ttk.Button(quadro_form,
                   text="Agendar Consulta",
                   command=agendar_consulta).grid(row=6,
                                                  column=0,
                                                  columnspan=3,
                                                  pady=10)

        # Cria o frame 'quadro_lista' que será utilizado para armazenar a
        # lista de consultas agendadas.
        # O frame recebe a cor de fundo #f0f0f0, e o método 'pack' é utilizado
        # para posicioná-lo, permitindo que ele ocupe todo o espaço disponível na janela.
        # 'fill="both"' permite que o quadro se expanda tanto horizontal
        # quanto verticalmente, e 'expand=True' garante que o frame
        # preencha o espaço não utilizado.
        quadro_lista = tk.Frame(janela_co, bg="#f0f0f0")
        quadro_lista.pack(fill='both', expand=True, pady=10, padx=10)

        # Cria uma barra de rolagem (Scrollbar) dentro do quadro de
        # lista (quadro_lista), permitindo a rolagem vertical.
        # A barra de rolagem será associada à lista de consultas, para que o
        # usuário possa visualizar várias consultas, mesmo que a
        # lista ultrapasse o tamanho da tela.
        barra_rolagem = tk.Scrollbar(quadro_lista)
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)

        # Criação de uma Treeview (uma tabela) chamada arvore_consultas, que
        # será usada para exibir as consultas agendadas.
        # A Treeview será configurada com as colunas: "Data", "Hora Início", "Hora Final", "Médico", "Cliente", e "Descrição".
        # 'show="headings"' garante que a tabela mostre os títulos das colunas, mas
        # não mostre a coluna de identificação interna.
        # 'height=15' define o número de linhas visíveis na tabela por padrão.
        # A tabela pode ter rolagem se o número de entradas for superior a 15.
        # 'yscrollcommand=barra_rolagem.set' conecta a barra de rolagem à
        # Treeview, permitindo que a rolagem da tabela seja controlada pela barra.
        arvore_consultas = ttk.Treeview(quadro_lista,
                                        columns=(
                                        "Data", "Hora Início", "Hora Final", "Médico", "Cliente", "Descrição"),
                                        show="headings",
                                        height=15,
                                        yscrollcommand=barra_rolagem.set)

        # Configura os cabeçalhos das colunas da Treeview. O método 'heading' é
        # usado para definir o texto de cada coluna.
        # O título de cada coluna será visível na parte superior da tabela,
        # ajudando o usuário a identificar o que cada coluna representa.
        arvore_consultas.heading("Data", text="Data")
        arvore_consultas.heading("Hora Início", text="Hora Início")
        arvore_consultas.heading("Hora Final", text="Hora Final")
        arvore_consultas.heading("Médico", text="Médico")
        arvore_consultas.heading("Cliente", text="Cliente")
        arvore_consultas.heading("Descrição", text="Descrição")

        # Define a largura das colunas na Treeview para que cada
        # coluna tenha um tamanho fixo.
        # A largura é especificada em pixels, e a definição ajuda a
        # manter o layout organizado e legível.
        # A coluna "Data" será de 100 pixels de largura.
        arvore_consultas.column("Data", width=100)

        # A coluna "Hora Início" será de 80 pixels de largura.
        arvore_consultas.column("Hora Início", width=80)

        # A coluna "Hora Final" também terá 80 pixels de largura.
        arvore_consultas.column("Hora Final", width=80)

        # A coluna "Médico" terá 150 pixels de largura para acomodar
        # nomes mais longos dos médicos.
        arvore_consultas.column("Médico", width=150)

        # A coluna "Cliente" terá 150 pixels de largura, permitindo
        # mostrar o nome completo dos clientes.
        arvore_consultas.column("Cliente", width=150)

        # A coluna "Descrição" terá 300 pixels de largura, já que a
        # descrição das consultas pode ser mais longa.
        arvore_consultas.column("Descrição", width=300)

        # A função 'pack' é usada para posicionar o widget da Treeview
        # dentro do quadro de lista (quadro_lista).
        # O parâmetro 'fill="both"' permite que a tabela ocupe todo o espaço
        # disponível, tanto horizontal quanto verticalmente.
        # O parâmetro 'expand=True' garante que a tabela se expanda
        # conforme o tamanho da janela muda.
        arvore_consultas.pack(fill='both', expand=True)

        # Configura a barra de rolagem para que ela controle a visualização da Treeview.
        # O comando 'barra_rolagem.config(command=arvore_consultas.yview)'
        # vincula a barra de rolagem ao método de visualização da Treeview.
        # Isso permite que a rolagem da tabela seja controlada pela barra.
        barra_rolagem.config(command=arvore_consultas.yview)

        # Inicializa a variável 'id_consulta_selecionada' com um valor de 'None'.
        # Isso indica que inicialmente não há consulta selecionada na tabela.
        id_consulta_selecionada = [None]

        # A função 'atualizar_lista_consultas' atualiza a Treeview com as
        # consultas mais recentes da coleção 'consultas' no banco de dados.
        def atualizar_lista_consultas():

            # Remove todos os itens (linhas) existentes na Treeview para garantir
            # que a tabela seja limpa antes de adicionar os novos dados.
            for item in arvore_consultas.get_children():
                arvore_consultas.delete(item)

            # Busca todas as consultas na coleção 'consultas' do MongoDB e
            # ordena pelos campos 'data' e 'hora_inicio' (ascendente).
            consultas = self.colecao_consultas.find().sort([("data", 1), ("hora_inicio", 1)])

            # Para cada consulta encontrada, preenche os dados nas colunas da Treeview.
            for c in consultas:

                # Busca o cliente correspondente à consulta usando o
                # campo 'cliente_id' da consulta.
                cliente = self.colecao_clientes.find_one({"_id": c["cliente_id"]})

                # Se o cliente foi encontrado, usa o nome do cliente, caso
                # contrário, atribui "Desconhecido".
                cliente_nome = cliente["nome"] if cliente else "Desconhecido"

                # Busca o médico correspondente à consulta, se o campo 'medico_id' existir na consulta.
                medico_id = c.get("medico_id")

                if medico_id:

                    # Se o 'medico_id' existir, busca o médico correspondente no banco de dados.
                    medico = self.colecao_medicos.find_one({"_id": medico_id})

                    # Se o médico for encontrado, usa o nome do médico, caso
                    # contrário, atribui "Desconhecido".
                    medico_nome = medico["nome"] if medico else "Desconhecido"

                else:

                    # Se o 'medico_id' não existir na consulta, define "Sem Médico" como valor padrão.
                    medico_nome = "Sem Médico"

                # Obtém a hora de início da consulta, se não existir, usa o valor "00:00" como padrão.
                hora_ini = c.get("hora_inicio", c.get("hora", "00:00"))

                # Obtém a hora final da consulta, se não existir,
                # define "Sem Hora Final" como valor padrão.
                hora_fim = c.get("hora_final", "Sem Hora Final")

                # Insere uma nova linha na Treeview com os dados da consulta.
                # Cada coluna recebe um valor:
                # - 'data' da consulta.
                # - 'hora_inicio' e 'hora_final'.
                # - 'medico_nome' (nome do médico).
                # - 'cliente_nome' (nome do cliente).
                # - 'descricao' da consulta.
                arvore_consultas.insert("",
                                        tk.END,
                                        values=(c["data"],
                                                hora_ini,
                                                hora_fim,
                                                medico_nome,
                                                cliente_nome,
                                                c["descricao"]),
                                        iid=str(c["_id"]))

            # Após inserir todas as consultas, a variável 'id_consulta_selecionada' é
            # definida como None, indicando que nenhuma consulta está selecionada.
            id_consulta_selecionada[0] = None


        # Função que é chamada quando o usuário seleciona uma consulta na Treeview.
        def selecionar_consulta(event):

            # Obtém o item selecionado na Treeview.
            selecionado = arvore_consultas.selection()

            # Verifica se há algum item selecionado.
            if selecionado:

                # Armazena o ID da consulta selecionada (usando o ID do item na Treeview).
                id_consulta_selecionada[0] = selecionado[0]

                # Busca a consulta no banco de dados utilizando o ID da consulta selecionada.
                consulta = self.colecao_consultas.find_one({"_id": ObjectId(id_consulta_selecionada[0])})

                # Se a consulta for encontrada, preenche os campos da
                # interface com as informações da consulta.
                if consulta:

                    # Busca o cliente correspondente à consulta usando o 'cliente_id' da consulta.
                    cliente = self.colecao_clientes.find_one({"_id": consulta["cliente_id"]})

                    # Se o cliente for encontrado, usa o nome do cliente, caso
                    # contrário, atribui "Desconhecido".
                    cliente_nome = cliente["nome"] if cliente else "Desconhecido"

                    # Obtém o ID do médico da consulta, se existir.
                    medico_id = consulta.get("medico_id")

                    if medico_id:

                        # Se o 'medico_id' existir, busca o médico correspondente no banco de dados.
                        medico = self.colecao_medicos.find_one({"_id": medico_id})

                        # Se o médico for encontrado, usa o nome do médico, caso
                        # contrário, atribui "Desconhecido".
                        medico_nome = medico["nome"] if medico else "Desconhecido"

                    else:

                        # Se o 'medico_id' não existir na consulta, define "Sem Médico"
                        # como valor padrão.
                        medico_nome = "Sem Médico"

                    # Atualiza o campo 'var_cliente_consulta' com o cliente
                    # selecionado. Exibe o ID do cliente e o nome.
                    var_cliente_consulta.set(f"{consulta['cliente_id']} - {cliente_nome}")

                    if medico_id:

                        # Se o médico for selecionado, atualiza o campo 'var_medico_consulta'
                        # com o ID do médico e o nome.
                        var_medico_consulta.set(f"{medico_id} - {medico_nome}")

                    else:

                        # Caso contrário, limpa o campo do médico.
                        var_medico_consulta.set("")

                    # Atualiza o campo 'entrada_data_consulta' com a data da consulta.
                    entrada_data_consulta.delete(0, tk.END)
                    entrada_data_consulta.insert(tk.END, consulta["data"])

                    # Obtém a hora de início e fim da consulta, com valores padrão caso não existam.
                    hora_ini = consulta.get("hora_inicio", consulta.get("hora", "00:00"))
                    hora_fim = consulta.get("hora_final", hora_ini)

                    # Atualiza o campo 'entrada_hora_inicio' com a hora de início da consulta.
                    entrada_hora_inicio.delete(0, tk.END)
                    entrada_hora_inicio.insert(tk.END, hora_ini)

                    # Atualiza o campo 'entrada_hora_final' com a hora final da consulta.
                    entrada_hora_final.delete(0, tk.END)
                    entrada_hora_final.insert(tk.END, hora_fim)

                    # Atualiza o campo de texto para a descrição da consulta, se presente.
                    texto_descricao_consulta.delete("1.0", tk.END)
                    texto_descricao_consulta.insert(tk.END, consulta["descricao"])

            else:

                # Se nenhum item foi selecionado, limpa a seleção.
                id_consulta_selecionada[0] = None

        # Associa a função 'selecionar_consulta' ao evento de
        # seleção de item na Treeview.
        arvore_consultas.bind("<<TreeviewSelect>>", selecionar_consulta)


        # Função para verificar se dois intervalos de tempo se sobrepõem.
        def intervalos_conflitam(inicio1, fim1, inicio2, fim2):

            # Função interna para converter tempo em formato HH:MM para minutos.
            def hm_para_min(hm):
                h, m = hm.split(':')  # Separa as horas e minutos.
                return int(h) * 60 + int(m)  # Converte o tempo para minutos desde a meia-noite.

            # Converte os horários de início e fim dos dois intervalos para minutos.
            ini1 = hm_para_min(inicio1)  # Tempo de início do primeiro intervalo em minutos.
            fi1 = hm_para_min(fim1)  # Tempo de fim do primeiro intervalo em minutos.
            ini2 = hm_para_min(inicio2)  # Tempo de início do segundo intervalo em minutos.
            fi2 = hm_para_min(fim2)  # Tempo de fim do segundo intervalo em minutos.

            # Verifica se os intervalos se sobrepõem.
            return (ini1 < fi2) and (fi1 > ini2)

        # Criação de um quadro de ações na janela de agendamento de consultas.
        # Cria um novo frame para as ações com fundo cinza claro.
        quadro_acoes = tk.Frame(janela_co, bg="#f0f0f0")

        # Adiciona o frame na janela, com um padding de 10 pixels no eixo Y.
        quadro_acoes.pack(pady=10)

        # Função que será responsável por atualizar uma consulta existente.
        def atualizar_consulta():

            # Verifica se uma consulta foi selecionada. Se não, exibe um
            # aviso e interrompe a execução da função.
            if not id_consulta_selecionada[0]:

                # Exibe uma mensagem de alerta caso nenhuma consulta
                # tenha sido selecionada.
                messagebox.showwarning("Aviso", "Nenhuma consulta selecionada.", parent=janela_co)

                # Interrompe a execução da função se não houver uma
                # consulta selecionada.
                return

            # Obtém o valor selecionado do cliente, removendo espaços
            # extras no início e no final da string.
            cliente_selecionado = var_cliente_consulta.get().strip()

            # Obtém o valor selecionado do médico, removendo espaços
            # extras no início e no final da string.
            medico_selecionado = var_medico_consulta.get().strip()

            # Obtém o valor da data da consulta, removendo espaços extras.
            data_str = entrada_data_consulta.get().strip()

            # Obtém o valor da hora de início da consulta, removendo espaços extras.
            hora_ini_str = entrada_hora_inicio.get().strip()

            # Obtém o valor da hora final da consulta, removendo espaços extras.
            hora_fim_str = entrada_hora_final.get().strip()

            # Obtém a descrição da consulta, removendo espaços extras e
            # considerando o texto completo do campo.
            descricao = texto_descricao_consulta.get("1.0", tk.END).strip()

            # Verifica se algum campo obrigatório está vazio e exibe um
            # aviso se algum estiver.
            if not cliente_selecionado or not medico_selecionado or not data_str or not hora_ini_str or not hora_fim_str or not descricao:

                # Exibe uma mensagem de aviso caso algum campo obrigatório
                # não tenha sido preenchido.
                messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=janela_co)

                # Interrompe a execução da função se algum campo
                # obrigatório estiver vazio.
                return

            # Tenta extrair os IDs do cliente e do médico a partir das
            # strings selecionadas.
            try:

                # Separa o cliente selecionado em duas partes, pegando apenas a
                # primeira parte antes de " - ".
                cliente_id_str, _ = cliente_selecionado.split(" - ", 1)

                # Converte a string do ID do cliente para o formato ObjectId,
                # que é utilizado no MongoDB.
                cliente_id = ObjectId(cliente_id_str)

                # Separa o médico selecionado em duas partes, pegando apenas a
                # primeira parte antes de " - ".
                medico_id_str, _ = medico_selecionado.split(" - ", 1)

                # Converte a string do ID do médico para o formato ObjectId.
                medico_id = ObjectId(medico_id_str)

            # Caso ocorra algum erro ao tentar obter ou converter os IDs,
            # exibe um aviso para o usuário.
            except:

                # Exibe uma mensagem de aviso caso a conversão dos IDs falhe.
                messagebox.showwarning("Aviso", "Selecione corretamente o cliente e médico.", parent=janela_co)

                # Interrompe a execução da função se houver erro na conversão dos IDs.
                return

            # Tenta validar as entradas de data e horas para garantir
            # que estejam no formato correto.
            try:

                # Valida a data informada no formato "YYYY-MM-DD".
                datetime.datetime.strptime(data_str, "%Y-%m-%d")

                # Valida a hora de início informada no formato "HH:MM".
                datetime.datetime.strptime(hora_ini_str, "%H:%M")

                # Valida a hora final informada no formato "HH:MM".
                datetime.datetime.strptime(hora_fim_str, "%H:%M")

            # Caso algum formato de data ou hora seja inválido,
            # exibe um aviso de erro.
            except ValueError:

                # Exibe uma mensagem de aviso caso a data ou as
                # horas estejam no formato errado.
                messagebox.showwarning("Aviso", "Data, Hora Início ou Hora Final inválida.", parent=janela_co)

                # Interrompe a execução da função se houver erro no formato de data ou hora.
                return

            # Verificar conflito
            # A consulta busca as consultas do médico selecionado na data específica,
            # mas exclui a consulta que está sendo atualizada (id_consulta_selecionada).
            consultas_medico_dia = self.colecao_consultas.find({
                "medico_id": medico_id,  # Filtra as consultas do médico específico.
                "data": data_str,  # Filtra as consultas na data selecionada.
                "_id": {"$ne": ObjectId(id_consulta_selecionada[0])}
                # Exclui a consulta que está sendo atualizada (baseado no ID).
            })

            # Para cada consulta encontrada na busca acima
            for c in consultas_medico_dia:

                # Obtém a hora de início e hora final da consulta existente (caso
                # não exista, assume valores padrão).
                h_ini_exist = c.get("hora_inicio", c.get("hora", "00:00"))
                h_fim_exist = c.get("hora_final", h_ini_exist)

                # Verifica se há conflito entre o intervalo da consulta sendo
                # atualizada e a consulta existente
                if intervalos_conflitam(hora_ini_str, hora_fim_str, h_ini_exist, h_fim_exist):

                    # Exibe uma mensagem de aviso caso haja conflito de horário
                    messagebox.showwarning("Aviso", "Conflito de horário com outra consulta deste médico.", parent=janela_co)

                    # Interrompe a execução da função, impedindo a atualização da consulta
                    return

            # Se não houver conflito de horário, prepara os
            # dados para atualizar a consulta
            dados_atualizacao = {
                "$set": {  # Usando o operador "$set" para atualizar os campos da consulta
                    "cliente_id": cliente_id,  # Atualiza o ID do cliente
                    "medico_id": medico_id,  # Atualiza o ID do médico
                    "data": data_str,  # Atualiza a data da consulta
                    "hora_inicio": hora_ini_str,  # Atualiza a hora de início
                    "hora_final": hora_fim_str,  # Atualiza a hora final
                    "descricao": descricao  # Atualiza a descrição da consulta
                }
            }

            # Atualiza a consulta no banco de dados com os dados preparados anteriormente.
            # A função `update_one` é utilizada para encontrar a consulta com o ID especificado
            # e atualizar os campos com os dados fornecidos no dicionário `dados_atualizacao`.
            self.colecao_consultas.update_one({"_id": ObjectId(id_consulta_selecionada[0])}, dados_atualizacao)

            # Após a atualização da consulta, chamamos a função `atualizar_lista_consultas()`
            # para atualizar a lista exibida na interface, refletindo as
            # mudanças feitas no banco de dados.
            atualizar_lista_consultas()

            # Limpa os campos da interface para que o usuário possa ver que a
            # consulta foi atualizada com sucesso.
            var_cliente_consulta.set("")  # Limpa o campo de cliente selecionado.
            var_medico_consulta.set("")  # Limpa o campo de médico selecionado.
            entrada_data_consulta.delete(0, tk.END)  # Limpa o campo de data da consulta.
            entrada_hora_inicio.delete(0, tk.END)  # Limpa o campo de hora de início da consulta.
            entrada_hora_final.delete(0, tk.END)  # Limpa o campo de hora final da consulta.
            texto_descricao_consulta.delete("1.0", tk.END)  # Limpa o campo de descrição da consulta.

            # A variável `id_consulta_selecionada[0]` é definida como `None`,
            # indicando que nenhuma consulta está mais selecionada após a atualização.
            id_consulta_selecionada[0] = None

            # Exibe uma mensagem de sucesso para o usuário, informando que a
            # consulta foi atualizada com sucesso.
            messagebox.showinfo("Sucesso", "Consulta atualizada com sucesso!", parent=janela_co)


        # Função para excluir uma consulta
        def excluir_consulta():

            # Verifica se uma consulta foi selecionada antes de tentar excluí-la
            if not id_consulta_selecionada[0]:

                # Se nenhuma consulta foi selecionada, exibe um aviso
                messagebox.showwarning("Aviso", "Nenhuma consulta selecionada.", parent=janela_co)
                return

            # Pergunta ao usuário se ele tem certeza de que deseja excluir a consulta selecionada
            confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja excluir esta consulta?", parent=janela_co)

            if confirmar:

                # Se o usuário confirmar, a consulta será excluída do banco de dados
                self.colecao_consultas.delete_one({"_id": ObjectId(id_consulta_selecionada[0])})

                # Após a exclusão, a lista de consultas é atualizada
                atualizar_lista_consultas()

                # Limpa os campos de entrada na interface de usuário
                var_cliente_consulta.set("")  # Limpa o cliente selecionado
                var_medico_consulta.set("")  # Limpa o médico selecionado
                entrada_data_consulta.delete(0, tk.END)  # Limpa o campo de data
                entrada_hora_inicio.delete(0, tk.END)  # Limpa o campo de hora de início
                entrada_hora_final.delete(0, tk.END)  # Limpa o campo de hora final
                texto_descricao_consulta.delete("1.0", tk.END)  # Limpa o campo de descrição

                # Reseta a variável de ID da consulta selecionada
                id_consulta_selecionada[0] = None

                # Exibe uma mensagem de sucesso para o usuário
                messagebox.showinfo("Sucesso", "Consulta excluída com sucesso!", parent=janela_co)

        # Criação do botão de "Atualizar Consulta"
        ttk.Button(quadro_acoes,
                   text="Atualizar Consulta",
                   command=atualizar_consulta).grid(row=0,
                                                    column=0,
                                                    padx=10)

        # Criação do botão de "Excluir Consulta"
        ttk.Button(quadro_acoes,
                   text="Excluir Consulta",
                   command=excluir_consulta).grid(row=0,
                                                  column=1,
                                                  padx=10)

        # Atualiza a lista de consultas exibidas na interface
        atualizar_lista_consultas()


    # Função que cria uma janela para pesquisar agendamentos por médico
    def janela_pesquisar_por_medico(self):

        # Cria uma nova janela pop-up a partir da janela principal (self.janela)
        janela_pm = tk.Toplevel(self.janela)

        # Define o título da nova janela como "Pesquisar Agendamentos por Médico"
        janela_pm.title("Pesquisar Agendamentos por Médico")

        # Define o tamanho da janela para 900px de largura por 600px de altura
        janela_pm.geometry("900x600")

        # Configura o fundo da janela para a cor #f0f0f0, que é um cinza claro
        janela_pm.configure(bg="#f0f0f0")

        # Define a janela para abrir maximizada na tela.
        janela_pm.state('zoomed')

        # Cria um frame dentro da nova janela que servirá para conter os campos de pesquisa
        # O frame tem um título "Pesquisar por Médico" e usa a mesma cor de fundo da janela
        # A fonte utilizada é Arial, tamanho 12, e em negrito
        quadro_form = tk.LabelFrame(janela_pm,
                                    text="Pesquisar por Médico",
                                    bg="#f0f0f0",
                                    font=("Arial", 12, "bold"))

        # Adiciona o frame à janela, posicionando-o no topo da janela e fazendo
        # com que ele ocupe toda a largura (fill='x')
        # A margem (pady=10, padx=10) adiciona espaço de 10 pixels ao redor do frame
        quadro_form.pack(side=tk.TOP, fill='x', pady=10, padx=10)

        # Cria um rótulo (label) com o texto "Médico" para a interface gráfica
        # O parâmetro 'bg' define a cor de fundo do label, que é um cinza claro "#f0f0f0".
        # A fonte do texto é configurada para "Arial", com tamanho 11 e
        # negrito (não especificado mas é o padrão do tkinter).
        # O método 'grid' é usado para posicionar o label na interface, na
        # linha 0 e coluna 0, com margens de 5 pixels (padx=5, pady=5).
        # O 'sticky' com valor 'e' significa que o texto será alinhado à
        # direita da célula onde está posicionado no grid.
        tk.Label(quadro_form,
                 text="Médico:",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=0,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Cria uma variável do tipo StringVar, que será usada para
        # armazenar o valor do médico selecionado no ComboBox
        # Essa variável está ligada ao ComboBox, ou seja, o valor
        # escolhido no ComboBox será armazenado nela.
        var_medico_pesq = tk.StringVar()

        # Cria um ComboBox que permite ao usuário selecionar um médico da lista.
        # O ComboBox é configurado para ser somente leitura ('readonly'), o que
        # significa que o usuário só pode selecionar uma opção, não pode digitar.
        # O parâmetro 'textvariable' associa a variável 'var_medico_pesq' ao
        # ComboBox, para que o valor selecionado seja armazenado na variável.
        # O parâmetro 'font' define a fonte do texto dentro do ComboBox como "Arial", tamanho 11.
        # O parâmetro 'width' define a largura do ComboBox, neste caso, 40 caracteres de largura.
        # O 'grid' é usado para posicionar o ComboBox no layout da janela, na linha 0 e coluna 1.
        # 'padx' e 'pady' adicionam margens internas ao redor do ComboBox,
        # com 5 pixels de espaçamento em cada lado.
        # 'sticky="w"' faz com que o conteúdo do ComboBox se alinhe à
        # esquerda dentro da célula do grid.
        combo_medico_pesq = ttk.Combobox(quadro_form,
                                         textvariable=var_medico_pesq,
                                         state='readonly',
                                         font=("Arial", 11),
                                         width=40)

        # Coloca o ComboBox na janela, com as configurações de posição e
        # alinhamento já definidas.
        # O método 'grid' posiciona o ComboBox na interface, configurando as
        # propriedades de alinhamento e margens.
        # 'row=0' coloca o ComboBox na primeira linha (linha 0) do grid.
        # 'column=1' coloca o ComboBox na segunda coluna (coluna 1) do grid.
        # 'padx=5' e 'pady=5' adicionam 5 pixels de espaçamento interno na
        # horizontal (pontos a esquerda e a direita) e vertical (acima e
        # abaixo) ao redor do ComboBox.
        # 'sticky="w"' faz com que o conteúdo do ComboBox se alinhe à esquerda (west)
        # da célula do grid onde ele está posicionado.
        combo_medico_pesq.grid(row=0,
                               column=1,
                               padx=5,
                               pady=5,
                               sticky='w')

        # Consulta a coleção de médicos no banco de dados para preencher a
        # lista de médicos no ComboBox.
        # A função 'self.colecao_medicos.find()' retorna todos os
        # médicos cadastrados na base de dados.
        # 'medicos' recebe a lista de documentos de médicos retornada pela
        # consulta no banco de dados.
        medicos = self.colecao_medicos.find()

        # Cria uma lista 'lista_medicos' contendo strings no formato "ID - Nome",
        # com o nome e o ID de cada médico.
        # A expressão f"{m['_id']} - {m['nome']}" usa f-strings para criar a string
        # com a concatenação do ID e do nome de cada médico.
        # A lista 'lista_medicos' será usada para preencher as opções
        # disponíveis no ComboBox.
        lista_medicos = [f"{m['_id']} - {m['nome']}" for m in medicos]

        # Define as opções (valores) do ComboBox 'combo_medico_pesq' para a
        # lista de médicos recuperada.
        # Agora o ComboBox exibirá uma lista de médicos no formato "ID - Nome"
        # para o usuário selecionar.
        combo_medico_pesq['values'] = lista_medicos

        # Criação de um rótulo (label) "Data (opcional)" para a interface gráfica,
        # indicando que o campo de data é opcional.
        # O parâmetro 'bg="#f0f0f0"' define a cor de fundo do rótulo como cinza claro.
        # O parâmetro 'font=("Arial", 11)' define a fonte do texto como "Arial" no tamanho 11.
        # O método 'grid' posiciona o rótulo na interface, na linha 1 e coluna 0,
        # com margens internas de 5 pixels.
        # O parâmetro 'sticky="e"' alinha o texto à direita da célula
        # onde o rótulo está posicionado.
        tk.Label(quadro_form,
                 text="Data (opcional):",
                 bg="#f0f0f0",
                 font=("Arial", 11)).grid(row=1,
                                          column=0,
                                          padx=5,
                                          pady=5,
                                          sticky='e')

        # Criação de um campo de entrada de texto (Entry) onde o usuário
        # pode inserir a data para pesquisa.
        # O parâmetro 'width=20' define a largura do campo de entrada como 20 caracteres.
        # O parâmetro 'font=("Arial", 11)' define a fonte do texto dentro do
        # campo de entrada como "Arial", tamanho 11.
        # O método 'grid' posiciona o campo de entrada na interface, na
        # linha 1 e coluna 1, com margens internas de 5 pixels.
        # O parâmetro 'sticky="w"' alinha o conteúdo à esquerda (west) da
        # célula onde o campo de entrada está posicionado.
        entrada_data_pesq = tk.Entry(quadro_form, width=20, font=("Arial", 11))
        entrada_data_pesq.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Função para abrir uma janela adicional onde o usuário
        # pode selecionar uma data.
        def selecionar_data_pesq():

            # Cria uma nova janela Toplevel, que ficará sobre a janela principal.
            janela_data = tk.Toplevel(janela_pm)

            # Define o título da nova janela como "Selecionar Data".
            janela_data.title("Selecionar Data")

            # Define o tamanho da janela como 300x300 pixels.
            janela_data.geometry("300x300")

            # Cria o calendário (Calendar) na nova janela. O 'selectmode="day"'
            # permite a seleção de um único dia.
            # 'date_pattern="y-mm-dd"' define o formato da data como "ano-mês-dia".
            cal = Calendar(janela_data,
                           selectmode='day',
                           date_pattern='y-mm-dd')

            # Posiciona o calendário na janela, com 10 pixels de
            # espaçamento na parte superior e inferior (pady=10).
            cal.pack(pady=10)

            # Função para confirmar a seleção da data feita no calendário.
            def confirmar_data():

                # Obtém a data selecionada no calendário.
                data_sel = cal.get_date()

                # Limpa o campo de entrada de data para garantir que o
                # valor anterior seja apagado.
                entrada_data_pesq.delete(0, tk.END)

                # Insere a data selecionada no campo de entrada de data.
                entrada_data_pesq.insert(tk.END, data_sel)

                # Fecha a janela de seleção de data.
                janela_data.destroy()

            # Cria um botão "Confirmar" dentro da janela de data.
            # Quando o botão é clicado, chama a função confirmar_data
            # para confirmar a seleção.
            ttk.Button(janela_data,
                       text="Confirmar",
                       command=confirmar_data).pack(pady=10)

        # Cria o botão "Selecionar Data" dentro do quadro principal da interface
        # O texto do botão será "Selecionar Data" e ao ser clicado,
        # chama a função selecionar_data_pesq
        # Organiza o botão no layout utilizando grid
        # O botão ficará na linha 1 (segunda linha) e na coluna 2 (terceira coluna)
        # Com espaçamento horizontal e vertical de 5 pixels
        ttk.Button(quadro_form,
                   text="Selecionar Data",
                   command=selecionar_data_pesq).grid(row=1,
                                                      column=2,
                                                      padx=5,
                                                      pady=5)

        def pesquisar():

            # Obtém o valor selecionado no ComboBox de médicos e
            # remove espaços em branco ao redor
            medico_selecionado = var_medico_pesq.get().strip()

            # Obtém o valor da entrada de data para filtro, removendo espaços em branco
            data_filtro = entrada_data_pesq.get().strip()

            # Verifica se o médico foi selecionado, se não exibe um
            # aviso para selecionar um médico
            if not medico_selecionado:
                messagebox.showwarning("Aviso", "Selecione um médico.", parent=janela_pm)
                return

            # Tenta dividir o valor selecionado no ComboBox de médicos
            # para obter o ID do médico.
            # Se não conseguir, exibe uma mensagem de erro.
            try:

                # Divide a string do médico para pegar o ID
                medico_id_str, _ = medico_selecionado.split(" - ", 1)

                # Converte o ID do médico para ObjectId do MongoDB
                medico_id = ObjectId(medico_id_str)

            except:

                # Se houver erro na conversão, avisa o usuário
                messagebox.showwarning("Aviso", "Selecione corretamente o médico.", parent=janela_pm)
                return

            # Prepara a consulta no banco de dados, buscando consultas
            # com o ID do médico selecionado.
            query = {"medico_id": medico_id}

            # Verifica se o usuário inseriu um valor para o filtro de data
            if data_filtro:

                # Tenta converter a string da data fornecida para o
                # formato de data "YYYY-MM-DD".
                try:

                    # Usa datetime para verificar se a data fornecida está no formato correto.
                    datetime.datetime.strptime(data_filtro, "%Y-%m-%d")

                except ValueError:

                    # Se ocorrer um erro na conversão da data, significa que o formato está errado
                    # Exibe uma mensagem de aviso informando o usuário que a data é inválida
                    messagebox.showwarning("Aviso", "Data inválida.", parent=janela_pm)

                    # Interrompe a execução da função, pois a data não é válida
                    return

                # Se a data for válida, adiciona essa data no filtro da consulta
                query["data"] = data_filtro

            # Realiza a consulta no banco de dados, usando o filtro montado (incluindo o
            # médico e, se aplicável, a data)
            # A consulta será ordenada pela data e, em caso de empates, pela
            # hora de início da consulta
            consultas = self.colecao_consultas.find(query).sort([("data", 1), ("hora_inicio", 1)])

            # Limpa todas as entradas existentes na árvore de consultas do médico
            # para garantir que a lista será atualizada
            for item in arvore_consultas_medico.get_children():
                arvore_consultas_medico.delete(item)

            # Percorre todas as consultas retornadas pela consulta ao banco de dados
            for c in consultas:

                # Obtém o cliente associado à consulta usando o cliente_id
                cliente = self.colecao_clientes.find_one({"_id": c["cliente_id"]})

                # Se o cliente for encontrado, usa o nome, caso contrário,
                # define como "Desconhecido"
                cliente_nome = cliente["nome"] if cliente else "Desconhecido"

                # Obtém o médico associado à consulta usando o medico_id
                medico_id_c = c.get("medico_id")

                if medico_id_c:

                    # Se um médico foi encontrado, obtém as informações do médico
                    medico_c = self.colecao_medicos.find_one({"_id": medico_id_c})

                    # Se o médico for encontrado, usa o nome, caso contrário,
                    # define como "Desconhecido"
                    medico_nome = medico_c["nome"] if medico_c else "Desconhecido"

                else:

                    # Se não houver médico, define como "Sem Médico"
                    medico_nome = "Sem Médico"

                # Obtém a hora de início e de fim da consulta
                hora_ini = c.get("hora_inicio", c.get("hora", "00:00"))

                # Se a hora final não estiver definida, coloca "Sem Hora Final"
                hora_fim = c.get("hora_final", "Sem Hora Final")

                # Insere os dados da consulta na árvore de consultas do médico, com os
                # valores de data, hora de início, hora de fim, médico, cliente e descrição
                arvore_consultas_medico.insert("",
                                               tk.END,
                                               values=(c["data"],
                                                       hora_ini,
                                                       hora_fim,
                                                       medico_nome,
                                                       cliente_nome,
                                                       c["descricao"]))

        # Cria um botão "Pesquisar" que chama a função 'pesquisar' quando
        # clicado. Este botão é colocado no quadro de formulário da janela.
        # O botão será colocado na linha 2, coluna 0 da grid, ocupará as três
        # primeiras colunas e terá um espaçamento de 10 pixels para cima e para baixo.
        ttk.Button(quadro_form,
                   text="Pesquisar",
                   command=pesquisar).grid(row=2,
                                           column=0,
                                           columnspan=3,
                                           pady=10)

        # Cria um novo quadro (frame) para armazenar a lista de
        # resultados da pesquisa.
        # O quadro será inserido dentro da janela 'janela_pm', que é
        # uma janela pop-up ou nova janela.
        # A cor de fundo do quadro é definida como #f0f0f0, um tom de cinza claro.
        # O quadro será expandido para preencher todo o espaço disponível na
        # janela, tanto na direção horizontal quanto vertical.
        # O método 'pack' é utilizado para posicionar o quadro, com
        # espaçamento (padding) de 10 pixels ao redor (pady=10 e padx=10).
        # Isso cria um espaço extra em torno do quadro, para que ele não fique
        # colado nas bordas da janela ou em outros elementos.
        quadro_lista = tk.Frame(janela_pm, bg="#f0f0f0")  # Criação do frame
        quadro_lista.pack(fill='both', expand=True, pady=10, padx=10)  # Posicionamento do frame na janela

        # Cria uma barra de rolagem (Scrollbar) que estará associada ao quadro 'quadro_lista'.
        # A barra de rolagem será utilizada para permitir que o usuário role a
        # lista de resultados da pesquisa, caso seja muito longa para caber na tela.
        # O método 'pack' é novamente usado para posicionar a barra de rolagem no quadro.
        # 'side=tk.RIGHT' posiciona a barra de rolagem no lado direito do quadro,
        # onde normalmente são colocadas barras de rolagem verticais.
        # 'fill=tk.Y' faz com que a barra de rolagem ocupe toda a altura disponível do
        # quadro, permitindo que o usuário role por todos os itens da lista.
        barra_rolagem = tk.Scrollbar(quadro_lista)  # Criação da barra de rolagem
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)  # Posicionamento da barra de rolagem no lado direito do quadro

        # Cria um widget Treeview dentro do quadro 'quadro_lista' para exibir os
        # dados das consultas.
        # O Treeview vai exibir as colunas: "Data", "Hora Início", "Hora Final", "Médico", "Cliente", "Descrição".
        # As colunas são definidas pela tupla 'columns', e o
        # parâmetro 'show="headings"' faz com que as colunas sejam visíveis
        # sem a coluna de identificação interna.
        # 'height=15' define a altura inicial do Treeview, ou seja, quantas
        # linhas ele exibirá por padrão.
        # 'yscrollcommand=barra_rolagem.set' vincula o Treeview à barra de
        # rolagem, permitindo que o conteúdo da lista seja rolado.
        arvore_consultas_medico = ttk.Treeview(quadro_lista,
                                               columns=("Data", "Hora Início", "Hora Final", "Médico", "Cliente",
                                                        "Descrição"),
                                               show="headings",
                                               height=15,
                                               yscrollcommand=barra_rolagem.set)

        # Define os títulos das colunas do Treeview. Esses títulos são
        # exibidos no cabeçalho de cada coluna.
        # 'text' define o texto exibido como título da coluna.
        arvore_consultas_medico.heading("Data", text="Data")
        arvore_consultas_medico.heading("Hora Início", text="Hora Início")
        arvore_consultas_medico.heading("Hora Final", text="Hora Final")
        arvore_consultas_medico.heading("Médico", text="Médico")
        arvore_consultas_medico.heading("Cliente", text="Cliente")
        arvore_consultas_medico.heading("Descrição", text="Descrição")

        # Define a largura de cada coluna do Treeview. 'width' determina a
        # largura de cada coluna em pixels.
        # Cada coluna é ajustada para garantir que o conteúdo seja
        # exibido corretamente e de forma legível.
        arvore_consultas_medico.column("Data", width=100)
        arvore_consultas_medico.column("Hora Início", width=100)
        arvore_consultas_medico.column("Hora Final", width=100)
        arvore_consultas_medico.column("Médico", width=150)
        arvore_consultas_medico.column("Cliente", width=150)
        arvore_consultas_medico.column("Descrição", width=300)

        # Posiciona o Treeview dentro do quadro 'quadro_lista', fazendo com
        # que ele ocupe o espaço disponível.
        # 'fill="both"' faz com que o Treeview se expanda para preencher
        # tanto a largura quanto a altura do quadro.
        # 'expand=True' permite que o Treeview se redimensione conforme a
        # janela for ajustada.
        arvore_consultas_medico.pack(fill='both', expand=True)

        # Configura a barra de rolagem associada ao Treeview. 'command=arvore_consultas_medico.yview'
        # vincula a barra de rolagem ao Treeview,
        # permitindo que o conteúdo da lista seja rolado verticalmente.
        barra_rolagem.config(command=arvore_consultas_medico.yview)




# Inicializa a janela principal (root) utilizando a biblioteca tkinter.
root = tk.Tk()

# Cria uma instância do sistema de agendamento de consultas, passando a
        # janela principal (root) como parâmetro.
# Isso permite que o sistema de agendamento de consultas seja
        # exibido dentro da janela 'root'.
app = SistemaAgendamentoConsultas(root)

# Inicia o loop principal da interface gráfica (GUI), aguardando e
        # respondendo a interações do usuário.
# O 'mainloop' mantém a janela aberta e interativa, permitindo que o
        # usuário interaja com os componentes da GUI.
root.mainloop()