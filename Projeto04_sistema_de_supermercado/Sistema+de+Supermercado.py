# Importação de módulos necessários para o desenvolvimento
        # de interfaces gráficas.
import tkinter as tk

# Importação de componentes adicionais de 'tkinter', como estilos
        # personalizados, caixas de diálogo e formulários simples.
from tkinter import ttk, messagebox, simpledialog, Toplevel

# Importação do módulo 'datetime' para manipulação de datas e horários.
import datetime

from numpy.random import weibull
# Importação do módulo 'MongoClient' de 'pymongo', que permite a conexão e
        # manipulação de bancos de dados MongoDB.
from pymongo import MongoClient

# Importação da classe 'FPDF' da biblioteca 'fpdf', usada para criar arquivos PDF.
from fpdf import FPDF  # Biblioteca necessária para criar PDFs

"""Exporta os dados filtrados para um arquivo Excel."""
# Importa a biblioteca pandas para manipulação e exportação de dados.
import pandas as pd

############################################
# Conexão com o MongoDB
############################################

# String de conexão com o banco de dados MongoDB, apontando para o
        # MongoDB local na porta padrão (27017).
uri_mongo = "mongodb://localhost:27017"

# Criação de um objeto cliente que se conecta ao MongoDB usando a URI fornecida.
cliente_mongo = MongoClient(uri_mongo)

# Seleção do banco de dados chamado 'supermercado_db' dentro do MongoDB.
banco = cliente_mongo["supermercado_db"]

# Seleção de diferentes coleções dentro do banco de dados.
#       As coleções são como tabelas em bancos de dados relacionais.
colecao_produtos = banco["produtos"]  # Coleção para armazenar dados de produtos
colecao_clientes = banco["clientes"]  # Coleção para armazenar dados de clientes
colecao_funcionarios = banco["funcionarios"]  # Coleção para armazenar dados de funcionários
colecao_vendas = banco["vendas"]  # Coleção para armazenar dados de vendas
colecao_usuarios = banco["usuarios"]  # Coleção para armazenar dados de usuários (para controle de acesso)
colecao_fornecedores = banco["fornecedores"]  # Coleção para armazenar dados de fornecedores



# Define uma função que busca todos os funcionários registrados na base de dados.
def obter_funcionarios():

    # Utiliza o método 'find' para buscar todos os documentos na
    #       coleção 'funcionarios' sem nenhum filtro específico.
    return list(colecao_funcionarios.find({}))
    # O resultado do 'find' é convertido em uma lista antes de ser retornado.
    # Isso é necessário porque 'find' retorna um cursor do MongoDB e
    #       não uma lista diretamente.


# Define a função 'obter_clientes' que recupera todos os clientes cadastrados.
def obter_clientes():

    # Retorna uma lista com todos os clientes encontrados na coleção 'clientes'.
    return list(colecao_clientes.find({}))


# Define uma função que busca todos os fornecedores
#       registrados no banco de dados.
def obter_fornecedores():

    # Utiliza o método 'find' para buscar todos os documentos na
    #       coleção 'fornecedores' sem aplicar nenhum filtro específico.
    return list(colecao_fornecedores.find({}))
    # O resultado do 'find' é convertido em uma lista antes de ser
    #       retornado, pois 'find' retorna um cursor do MongoDB e não
    #       uma lista diretamente.



# Função para obter uma lista de todos os produtos cadastrados no banco de dados.
def obter_produtos():

    """
    Não há parâmetros para esta função.
    Retorna:
    - Uma lista de dicionários, cada um representando um produto no banco de dados.
    """

    # O método 'find({})' busca todos os documentos na coleção 'produtos' sem nenhum filtro.
    # 'list()' é usado para converter o cursor retornado
    #       por 'find()' em uma lista de documentos.
    return list(colecao_produtos.find({}))


# Define uma função para obter produtos com estoque abaixo de um limite especificado.
def obter_estoque_baixo(limite=5):

    # Usa o método 'find' para buscar documentos na coleção 'produtos' onde a
    #       quantidade está abaixo do limite especificado.
    # O operador '$lt' significa "menor que".
    return list(colecao_produtos.find({"quantidade": {"$lt": limite}}))
    # Converte o resultado (cursor) em uma lista antes de retornar.


# Define uma função para encontrar produtos com data de validade ultrapassada.
def obter_produtos_vencidos():

    # Obtém a data atual usando o método 'date' para remover a informação de hora.
    hoje = datetime.datetime.now().date()

    # Busca todos os produtos na coleção 'produtos' e converte o resultado em uma lista.
    produtos = list(colecao_produtos.find({}))

    # Inicia uma lista vazia para armazenar os produtos vencidos.
    vencidos = []

    # Itera sobre cada produto na lista de produtos.
    for p in produtos:

        # Tenta obter o campo 'validade' do produto. Se não existir,
        #       define como uma string vazia.
        validade_str = p.get("validade", "")

        # Se o campo 'validade' estiver vazio, pula para a próxima iteração do loop.
        if not validade_str:
            continue

        try:

            # Tenta converter a string de validade para um objeto de data.
            validade = datetime.datetime.strptime(validade_str, "%d/%m/%Y").date()

            # Compara a data de validade com a data atual. Se a validade for menor
            #       que hoje, adiciona o produto à lista de vencidos.
            if validade < hoje:
                vencidos.append(p)

        # Se a conversão de data falhar (por estar em formato incorreto),
        #       ignora o produto e continua o loop.
        except:
            pass

    # Retorna a lista de produtos vencidos.
    return vencidos



# Define uma função para verificar as credenciais de login de um usuário.
def verificar_login(usuario, senha):

    # Busca um único documento na coleção 'usuarios' que corresponda
    #       tanto ao usuário quanto à senha fornecidos.
    user = colecao_usuarios.find_one({"usuario": usuario, "senha": senha})

    # O método 'find_one' retorna o documento se um usuário com o nome de
    #       usuário e senha especificados for encontrado.
    return user
    # Se as credenciais estiverem corretas, retorna o documento do
    #       usuário; se não, retorna 'None'.


############################################
# Classe Base para Janelas
############################################

# Classe base para criar janelas no aplicativo. Serve como
#       template para outras janelas.
class JanelaBase:

    # Construtor da classe, que inicializa a janela com um título e
    #       configurações básicas.
    def __init__(self, master, titulo):

        # 'master' refere-se ao widget pai no qual esta janela será
        #       construída, tipicamente uma instância de Tk.
        self.master = master

        # Define o título da janela para o valor passado como parâmetro 'titulo'.
        self.master.title(titulo)

        # Configura a janela para exibir em tela cheia. Este método é útil
        #       para aplicações que devem ocupar toda a tela.
        self.master.state('zoomed')

        # Inicializa um objeto de estilo que permite a customização
        #       dos widgets ttk no Tkinter.
        self.estilo = ttk.Style()

        # Configura o estilo para todos os widgets do tipo Label dentro
        #       desta janela, definindo a fonte como Arial tamanho 14.
        self.estilo.configure("TLabel",
                              font=("Arial", 14))

        # Configura o estilo para todos os widgets do tipo Entry,
        #       ajustando a fonte para Arial tamanho 14.
        self.estilo.configure("TEntry",
                              font=("Arial", 14))

        # Configura o estilo para todos os botões (TButton),
        #       estabelecendo a fonte Arial tamanho 14.
        self.estilo.configure("TButton",
                              font=("Arial", 14))

        # Define o estilo para os cabeçalhos das colunas em uma Treeview,
        #       aplicando a fonte Arial, tamanho 14 e em negrito.
        self.estilo.configure("Treeview.Heading",
                              font=("Arial", 14, "bold"))

        # Configura o estilo geral das linhas na Treeview,
        #       usando a fonte Arial tamanho 12.
        self.estilo.configure("Treeview",
                              font=("Arial", 12))



############################################
# Funções Auxiliares
############################################


# Define a função para cadastrar um novo funcionário no sistema, recebendo
#       seus dados pessoais e credenciais de acesso.
def cadastrar_funcionario(id_func, nome, cargo, turno, salario, usuario, senha):

    # Cria um dicionário com as informações básicas do funcionário.
    funcionario = {
        "id_func": id_func,  # Identificador único do funcionário.
        "nome": nome,  # Nome do funcionário.
        "cargo": cargo,  # Cargo que o funcionário ocupa.
        "turno": turno,  # Turno de trabalho do funcionário.
        "salario": salario  # Salário do funcionário.
    }

    # Insere o dicionário com as informações do funcionário na coleção
    #       'funcionarios' do banco de dados.
    colecao_funcionarios.insert_one(funcionario)

    # Cria um dicionário com as credenciais de acesso do funcionário.
    colecao_usuarios.insert_one({
        "usuario": usuario,  # Nome de usuário para acesso ao sistema.
        "senha": senha,  # Senha para acesso ao sistema.
        "cargo": cargo,  # Cargo é replicado aqui para controle de acesso baseado em cargo.
        "id_func": id_func  # Identificador do funcionário vinculado às credenciais.
    })


# Define uma função para cadastrar um novo fornecedor no banco de dados.
def cadastrar_fornecedor(nome, endereco, telefone):

    # Cria um dicionário que representa o novo fornecedor,
    #       com seus dados essenciais.
    fornecedor = {

        "nome": nome,  # Nome do fornecedor.
        "endereco": endereco,  # Endereço do fornecedor.
        "telefone": telefone  # Número de telefone do fornecedor.

    }

    # Insere o dicionário do fornecedor como um novo documento
    #       na coleção 'fornecedores'.
    colecao_fornecedores.insert_one(fornecedor)

# Função para cadastrar um novo produto no banco de dados MongoDB.
# Essa função recebe várias informações sobre o produto como argumentos.
# Esses argumentos serão usados para criar um registro no banco de dados.
def cadastrar_produto(codigo, nome, categoria, quantidade, preco, fornecedor, validade, unidade):

    """
    Parâmetros:
    - codigo: Identificador único para o produto (string).
    - nome: Nome do produto (string).
    - categoria: Categoria do produto (exemplo: alimentos, bebidas) (string).
    - quantidade: Quantidade disponível no estoque (inteiro).
    - preco: Preço unitário do produto (número decimal).
    - fornecedor: Nome do fornecedor do produto (string).
    - validade: Data de validade do produto (string no formato "dd/mm/aaaa").
    - unidade: Unidade de medida (exemplo: kg, un) (string).
    """

    # Criação de um dicionário chamado 'produto'.
    # O dicionário é uma estrutura de dados que associa cada chave (por exemplo, "codigo") a
    #       um valor (o valor correspondente do produto).
    produto = {
        "codigo": codigo,  # O código único que identifica o produto.
        "nome": nome,  # Nome do produto.
        "categoria": categoria,  # Categoria a que o produto pertence.
        "quantidade": int(quantidade),  # Quantidade disponível no estoque (convertida para inteiro).
        "preco": float(preco),  # Preço unitário do produto (convertido para número decimal).
        "fornecedor": fornecedor,  # Nome do fornecedor do produto.
        "validade": validade,  # Data de validade do produto (no formato de string, como "01/12/2030").
        "unidade": unidade  # Unidade de medida do produto (exemplo: "kg", "un").
    }

    # Inserção do dicionário 'produto' na coleção 'produtos' do banco de dados MongoDB.
    # O método 'insert_one()' adiciona um único registro (documento) à coleção.
    colecao_produtos.insert_one(produto)



# Define a função para editar as informações de um funcionário já existente.
def editar_funcionario(id_func, nome, cargo, turno, salario):

    # Atualiza o documento do funcionário na coleção 'funcionarios' com novos valores.
    colecao_funcionarios.update_one(

         # Filtro para localizar o documento do funcionário pelo seu identificador único.
        {"id_func": id_func},
        {"$set": {  # Operador '$set' indica que os valores seguintes devem ser atualizados no documento.
            "nome": nome,  # Atualiza o nome do funcionário.
            "cargo": cargo,  # Atualiza o cargo do funcionário.
            "turno": turno,  # Atualiza o turno de trabalho do funcionário.
            "salario": salario  # Atualiza o salário do funcionário.
        }}

    )


# Define uma função para atualizar os detalhes de um fornecedor
#       existente no banco de dados.
def editar_fornecedor(nome_antigo, nome_novo, endereco, telefone):

    # Usa o método 'update_one' para atualizar um único documento na
    #       coleção 'fornecedores'.
    # O primeiro argumento especifica o critério de busca usando o nome antigo
    #       do fornecedor para encontrar o documento correto.
    colecao_fornecedores.update_one(

        {"nome": nome_antigo},

        # O segundo argumento usa '$set' para indicar quais campos devem ser atualizados.
        # Aqui, está atualizando o nome, endereço e telefone do fornecedor.
        {"$set": {"nome": nome_novo, "endereco": endereco, "telefone": telefone}}

    )


# Define a função 'editar_cliente' que atualiza as informações de um cliente existente.
def editar_cliente(codigo, nome, cpf_cnpj, telefone, endereco):

    # Atualiza um cliente na coleção 'clientes' com base em seu código.
    colecao_clientes.update_one(

        {"codigo": codigo},  # Usa o código do cliente como critério
                # para encontrar o documento correto.
        {"$set": {  # Define os campos que serão atualizados com seus novos valores.
            "nome": nome,  # Atualiza o nome do cliente.
            "cpf_cnpj": cpf_cnpj,  # Atualiza o CPF ou CNPJ do cliente.
            "telefone": telefone,  # Atualiza o telefone do cliente.
            "endereco": endereco  # Atualiza o endereço do cliente.
        }}
    )


# Função para editar os detalhes de um produto existente no banco de dados MongoDB.
# Essa função recebe os novos valores para as propriedades de um produto como argumentos,
# incluindo o código único do produto que não muda e é usado para
#       localizar o registro a ser atualizado.
def editar_produto(codigo, nome, categoria, quantidade, preco, fornecedor, validade, unidade):

    """
    Parâmetros:
    - codigo: Identificador único do produto que não muda (string).
    - nome: Novo nome para o produto (string).
    - categoria: Nova categoria do produto (string).
    - quantidade: Nova quantidade em estoque (inteiro).
    - preco: Novo preço unitário do produto (número decimal).
    - fornecedor: Nome atualizado do fornecedor do produto (string).
    - validade: Nova data de validade do produto (string no formato "dd/mm/aaaa").
    - unidade: Unidade de medida atualizada (exemplo: kg, un) (string).
    """

    # Atualização de um documento dentro da coleção 'produtos' no MongoDB.
    # 'update_one()' é o método usado para atualizar um único documento baseado em um filtro.
    # Aqui, o filtro é {"codigo": codigo}, que encontra o produto baseado no seu código único.
    colecao_produtos.update_one(
        {"codigo": codigo},  # Filtro para localizar o documento a ser atualizado.
        {"$set": {  # Operador '$set' usado para definir os novos valores dos campos.
            "nome": nome,  # Atualiza o nome do produto.
            "categoria": categoria,  # Atualiza a categoria do produto.
            "quantidade": int(quantidade),  # Atualiza a quantidade em estoque, convertendo para inteiro.
            "preco": float(preco),  # Atualiza o preço, convertendo para número decimal.
            "fornecedor": fornecedor,  # Atualiza o nome do fornecedor.
            "validade": validade,  # Atualiza a data de validade.
            "unidade": unidade  # Atualiza a unidade de medida.
        }}
    )


# Define uma função para remover um fornecedor do banco de dados.
def remover_fornecedor(nome):

    # Utiliza o método 'delete_one' para excluir um único
    #       documento da coleção 'fornecedores'.
    # O critério para exclusão é o nome do fornecedor.
    colecao_fornecedores.delete_one({"nome": nome})
    # Isso remove o documento cujo campo 'nome' corresponde ao valor fornecido.



# Função para remover um produto do banco de dados MongoDB.
# A função aceita um código de produto como argumento, que é usado para
#       identificar o produto a ser removido.
def remover_produto(codigo):

    """
    Parâmetro:
    - codigo: Identificador único do produto (string).
    """

    # A função 'delete_one()' é chamada sobre a coleção 'produtos'.
    # Ela remove o documento que corresponde ao filtro especificado,
    #       neste caso, o produto com o 'codigo' fornecido.
    colecao_produtos.delete_one({"codigo": codigo})
    # Se um produto com o código especificado existe, ele é removido.
    #       Caso contrário, nada acontece.




# Define a função 'cadastrar_cliente' com os parâmetros necessários
#       para registrar um cliente.
def cadastrar_cliente(codigo, nome, cpf_cnpj, telefone, endereco):

    # Cria um dicionário com as informações do cliente, incluindo um
    #       histórico de compras vazio.
    cliente = {

        "codigo": codigo,  # Armazena o código identificador do cliente.
        "nome": nome,  # Armazena o nome do cliente.
        "cpf_cnpj": cpf_cnpj,  # Armazena o CPF ou CNPJ do cliente.
        "telefone": telefone,  # Armazena o número de telefone do cliente.
        "endereco": endereco,  # Armazena o endereço do cliente.
        "historico_compras": []  # Inicializa uma lista vazia para o histórico de compras do cliente.

    }

    # Insere o dicionário criado na coleção 'clientes' no banco de dados MongoDB.
    colecao_clientes.insert_one(cliente)


# Classe que gerencia a interface para operações
#       relacionadas a funcionários.
class JanelaFuncionarios(JanelaBase):

    # Método construtor que inicializa a janela e seus componentes.
    def __init__(self, master):

        # Chama o construtor da classe base (JanelaBase) e define o título da janela.
        super().__init__(master, "Gerenciamento de Funcionários")

        # Configura a janela para ser exibida em tela cheia.
        # O método `state('zoomed')` ajusta a janela para preencher toda a tela.
        self.master.state('zoomed')

        # Define a fonte padrão da interface para "Arial 14".
        # A função `option_add("*Font", ...)` aplica a fonte
        #       para todos os widgets da janela.
        self.master.option_add("*Font", "Arial 14")

        # Cria um frame (container) principal dentro da janela.
        # O frame é usado para organizar os componentes visuais da interface.
        self.frame = ttk.Frame(self.master, padding="10")

        # Adiciona o frame ao layout da janela principal.
        # O método `pack()` ajusta o frame para preencher o espaço disponível.
        # Os parâmetros `fill=tk.BOTH` permitem que o frame preencha largura e altura.
        # O parâmetro `expand=True` permite que o frame cresça conforme o tamanho da janela.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Criação de um rótulo (label) para o campo "ID Funcionário".
        # 'text="ID Funcionário:"' define o texto exibido no rótulo para
        #       identificar o campo onde o usuário deve inserir o ID do funcionário.
        # 'row=0' posiciona o rótulo na primeira linha da grade do frame (linha superior).
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="ID Funcionário:").grid(row=0,
                                               column=0,
                                               sticky="w",
                                               pady=5)

        # Criação de um campo de entrada (entry) para que o usuário
        #       possa digitar o ID do funcionário.
        # Este campo de entrada é armazenado na variável 'self.campo_id_func'.
        self.campo_id_func = ttk.Entry(self.frame)


        # Configuração do layout do campo de entrada "ID Funcionário" na grade.
        # 'row=0' posiciona o campo de entrada na mesma linha do rótulo "ID Funcionário".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_id_func.grid(row=0,
                                column=1,
                                sticky="we",
                                pady=5)

        # Criação de um rótulo (label) para o campo "Nome".
        # 'text="Nome:"' define o texto exibido no rótulo para identificar o
        #       campo onde o usuário deve inserir o nome do funcionário.
        # 'row=1' posiciona o rótulo na segunda linha da grade do frame.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Nome:").grid(row=1,
                                     column=0,
                                     sticky="w",
                                     pady=5)

        # Criação de um campo de entrada (entry) para que o usuário
        #       possa digitar o nome do funcionário.
        # Este campo de entrada é armazenado na variável 'self.campo_nome'.
        self.campo_nome = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada "Nome" na grade.
        # 'row=1' posiciona o campo de entrada na mesma linha do rótulo "Nome".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_nome.grid(row=1,
                             column=1,
                             sticky="we",
                             pady=5)

        # Criação de um rótulo (label) para o campo "Cargo".
        # 'text="Cargo:"' define o texto exibido no rótulo para identificar o
        #       campo onde o usuário deve inserir o cargo do funcionário.
        # 'row=2' posiciona o rótulo na terceira linha da grade do frame.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Cargo:").grid(row=2,
                                      column=0,
                                      sticky="w",
                                      pady=5)

        # Criação de um campo de entrada (entry) para que o usuário possa
        #       digitar o cargo do funcionário.
        # Este campo de entrada é armazenado na variável 'self.campo_cargo'.
        self.campo_cargo = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada "Cargo" na grade.
        # 'row=2' posiciona o campo de entrada na mesma linha do rótulo "Cargo".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_cargo.grid(row=2,
                              column=1,
                              sticky="we",
                              pady=5)

        # Criação de um rótulo (label) para o campo "Turno".
        # 'text="Turno:"' define o texto exibido no rótulo para identificar o
        #       campo onde o usuário deve inserir o turno do funcionário.
        # 'row=3' posiciona o rótulo na quarta linha da grade do frame.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Turno:").grid(row=3,
                                      column=0,
                                      sticky="w",
                                      pady=5)

        # Criação de um campo de entrada (entry) para que o usuário
        #       possa digitar o turno do funcionário.
        # Este campo de entrada é armazenado na variável 'self.campo_turno'.
        self.campo_turno = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada "Turno" na grade.
        # 'row=3' posiciona o campo de entrada na mesma linha do rótulo "Turno".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_turno.grid(row=3,
                              column=1,
                              sticky="we",
                              pady=5)

        # Criação de um rótulo (label) para o campo "Salário".
        # 'text="Salário:"' define o texto exibido no rótulo para identificar o
        #       campo onde o usuário deve inserir o salário do funcionário.
        # 'row=4' posiciona o rótulo na quinta linha da grade do frame.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Salário:").grid(row=4,
                                        column=0,
                                        sticky="w",
                                        pady=5)

        # Criação de um campo de entrada (entry) para que o usuário possa
        #       digitar o salário do funcionário.
        # Este campo de entrada é armazenado na variável 'self.campo_salario'.
        self.campo_salario = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada "Salário" na grade.
        # 'row=4' posiciona o campo de entrada na mesma linha do rótulo "Salário".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_salario.grid(row=4,
                                column=1,
                                sticky="we",
                                pady=5)

        # Criação de um rótulo (label) para o campo "Usuário (Login)".
        # 'text="Usuário (Login):"' define o texto exibido no rótulo para identificar o
        #       campo onde o usuário deve inserir o login do funcionário.
        # 'row=5' posiciona o rótulo na sexta linha da grade do frame.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Usuário (Login):").grid(row=5,
                                                column=0,
                                                sticky="w",
                                                pady=5)

        # Criação de um campo de entrada (entry) para que o usuário
        #       possa digitar o login do funcionário.
        # Este campo de entrada é armazenado na variável 'self.campo_usuario'.
        self.campo_usuario = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada "Usuário (Login)" na grade.
        # 'row=5' posiciona o campo de entrada na mesma linha do rótulo "Usuário (Login)".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_usuario.grid(row=5,
                                column=1,
                                sticky="we",
                                pady=5)

        # Criação de um rótulo (label) para o campo "Senha".
        # 'text="Senha:"' define o texto exibido no rótulo para identificar o
        #       campo onde o usuário deve inserir a senha do funcionário.
        # 'row=6' posiciona o rótulo na sétima linha da grade do frame.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Senha:").grid(row=6,
                                      column=0,
                                      sticky="w",
                                      pady=5)

        # Criação de um campo de entrada (entry) para que o usuário possa
        #       digitar a senha do funcionário.
        # O parâmetro 'show="*"' configura o campo de entrada para mascarar os
        #       caracteres digitados, exibindo apenas asteriscos, garantindo a segurança da senha.
        # Este campo de entrada é armazenado na variável 'self.campo_senha'.
        self.campo_senha = ttk.Entry(self.frame, show="*")

        # Configuração do layout do campo de entrada "Senha" na grade.
        # 'row=6' posiciona o campo de entrada na mesma linha do rótulo "Senha".
        # 'column=1' posiciona o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_senha.grid(row=6,
                              column=1,
                              sticky="we",
                              pady=5)

        # Criação de um frame adicional para organizar os botões.
        # Este frame é usado para alinhar os botões horizontalmente
        #       dentro do frame principal.
        # O frame é armazenado na variável 'self.botao_frame'.
        self.botao_frame = ttk.Frame(self.frame)

        # Configuração do layout do frame de botões na grade.
        # 'row=7' posiciona o frame na oitava linha da grade do frame principal.
        # 'column=0' posiciona o frame na primeira coluna da grade.
        # 'columnspan=2' faz com que o frame ocupe duas colunas, permitindo centralizar os botões.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo do frame.
        self.botao_frame.grid(row=7,
                              column=0,
                              columnspan=2,
                              pady=10)

        # Criação do botão "Cadastrar".
        # 'text="Cadastrar"' define o texto exibido no botão, que indica sua funcionalidade.
        # 'command=self.cadastrar_funcionario' associa o botão à
        #       função 'cadastrar_funcionario', que será executada quando o botão for clicado.
        # Este botão é armazenado na variável 'self.botao_cadastrar' e
        #       adicionado ao frame de botões.
        self.botao_cadastrar = ttk.Button(self.botao_frame,
                                          text="Cadastrar",
                                          command=self.cadastrar_funcionario)

        # Configuração do layout do botão "Cadastrar" dentro do frame de botões.
        # 'pack(side=tk.LEFT)' posiciona o botão à esquerda do frame,
        #       permitindo uma organização horizontal.
        # 'padx=10' adiciona um espaço horizontal de 10 pixels em ambos os
        #       lados do botão, criando separação visual.
        self.botao_cadastrar.pack(side=tk.LEFT, padx=10)

        # Criação do botão "Editar".
        # 'text="Editar"' define o texto exibido no botão, indicando que
        #       ele permite editar os dados de um funcionário.
        # 'command=self.editar_funcionario' associa o botão à função 'editar_funcionario',
        #       que será executada ao clicar no botão.
        # Este botão é armazenado na variável 'self.botao_editar' e
        #       adicionado ao frame de botões.
        self.botao_editar = ttk.Button(self.botao_frame,
                                       text="Editar",
                                       command=self.editar_funcionario)

        # Configuração do layout do botão "Editar" dentro do frame de botões.
        # 'pack(side=tk.LEFT)' posiciona o botão à esquerda do frame, próximo ao
        #       botão "Cadastrar", mantendo alinhamento horizontal.
        # 'padx=10' adiciona um espaço horizontal de 10 pixels em ambos os
        #       lados do botão para separação.
        self.botao_editar.pack(side=tk.LEFT, padx=10)

        # Criação do botão "Remover".
        # 'text="Remover"' define o texto exibido no botão, indicando que ele é
        #       usado para excluir um funcionário.
        # 'command=self.remover_funcionario' associa o botão à
        #       função 'remover_funcionario', que será chamada ao clicar no botão.
        # Este botão é armazenado na variável 'self.botao_remover' e
        #       adicionado ao frame de botões.
        self.botao_remover = ttk.Button(self.botao_frame,
                                        text="Remover",
                                        command=self.remover_funcionario)

        # Configuração do layout do botão "Remover" dentro do frame de botões.
        # 'pack(side=tk.LEFT)' posiciona o botão à esquerda do frame, próximo aos
        #       botões "Cadastrar" e "Editar", mantendo a organização horizontal.
        # 'padx=10' adiciona um espaço horizontal de 10 pixels em ambos os
        #       lados do botão para separação visual.
        self.botao_remover.pack(side=tk.LEFT, padx=10)

        # Tabela de funcionários
        # Criação da tabela Treeview.
        # 'self.tabela' é um widget Treeview que será usado para exibir
        #       os dados dos funcionários.
        # 'self.frame' define o frame onde a tabela será inserida.
        # 'columns' especifica as colunas da tabela com
        #       identificadores: "id_func", "nome", "cargo", "turno" e "salario".
        # 'show="headings"' configura a tabela para exibir apenas o cabeçalho das
        #       colunas, sem uma coluna extra de ícone padrão.
        self.tabela = ttk.Treeview(
            self.frame,
            columns=("id_func", "nome", "cargo", "turno", "salario"),
            show="headings"
        )

        # Configuração dos cabeçalhos da tabela.
        # O loop percorre cada coluna definida anteriormente.
        for col in ("id_func", "nome", "cargo", "turno", "salario"):

            # 'self.tabela.heading' define o texto que será exibido no
            #       cabeçalho de cada coluna.
            # 'text=col.capitalize()' ajusta o texto para que a
            #       primeira letra seja maiúscula.
            self.tabela.heading(col, text=col.capitalize())

        # Posicionamento da tabela Treeview no layout.
        # 'row=8' coloca a tabela na nona linha do grid (contagem começa em 0).
        # 'column=0' coloca a tabela na primeira coluna do grid.
        # 'columnspan=2' faz com que a tabela ocupe duas colunas horizontais,
        #       abrangendo o espaço necessário.
        # 'sticky="nsew"' faz com que a tabela se expanda para preencher
        #       todo o espaço disponível na célula, tanto vertical quanto horizontalmente.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels acima e abaixo da tabela.
        self.tabela.grid(row=8,
                         column=0,
                         columnspan=2,
                         sticky="nsew",
                         pady=10)

        # Configuração de layout responsivo para a linha 8 do grid.
        # 'rowconfigure(8, weight=1)' permite que a linha 8 expanda ou
        #       contraia conforme o redimensionamento da janela.
        self.frame.rowconfigure(8, weight=1)

        # Configuração de layout responsivo para a coluna 1 do grid.
        # 'columnconfigure(1, weight=1)' permite que a coluna 1 expanda ou
        #       contraia conforme o redimensionamento da janela.
        self.frame.columnconfigure(1, weight=1)

        # Associação de um evento à tabela Treeview.
        # 'bind("<<TreeviewSelect>>")' associa o evento de seleção na tabela à
        #       função 'self.selecionar_item'.
        # Isso permite que, ao selecionar uma linha na tabela, as informações
        #       correspondentes sejam carregadas em outros campos.
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_item)

        # Chamada da função para listar os funcionários na tabela.
        # 'self.listar_funcionarios()' popula a tabela com os dados de
        #       funcionários ao iniciar a janela.
        self.listar_funcionarios()


    # Função para cadastrar um novo funcionário no sistema.
    def cadastrar_funcionario(self):

        # Obtém o texto inserido no campo de ID do funcionário e remove
        #       espaços em branco no início e no final.
        i = self.campo_id_func.get().strip()

        # Obtém o texto inserido no campo de Nome do funcionário e remove
        #       espaços em branco no início e no final.
        n = self.campo_nome.get().strip()

        # Obtém o texto inserido no campo de Cargo do funcionário e remove
        #       espaços em branco no início e no final.
        c = self.campo_cargo.get().strip()

        # Obtém o texto inserido no campo de Turno do funcionário e remove
        #       espaços em branco no início e no final.
        t = self.campo_turno.get().strip()

        # Obtém o texto inserido no campo de Salário do funcionário e remove
        #       espaços em branco no início e no final.
        s = self.campo_salario.get().strip()

        # Obtém o texto inserido no campo de Usuário (login) do funcionário e
        #       remove espaços em branco no início e no final.
        u = self.campo_usuario.get().strip()

        # Obtém o texto inserido no campo de Senha do funcionário e remove
        #       espaços em branco no início e no final.
        pw = self.campo_senha.get().strip()

        # Verifica se os campos obrigatórios (ID, Usuário e Senha)
        #       foram preenchidos.
        if i and u and pw:

            # Chama a função 'cadastrar_funcionario' (fora da classe) para
            #       inserir o funcionário no banco de dados.
            cadastrar_funcionario(i, n, c, t, s, u, pw)

            # Exibe uma mensagem de sucesso ao usuário.
            messagebox.showinfo("Sucesso", "Funcionário cadastrado.", parent=self.master)

            # Atualiza a lista de funcionários exibida na tabela.
            self.listar_funcionarios()

            # Limpa os campos de entrada para que possam ser reutilizados.
            self.limpar_campos()

        else:

            # Exibe uma mensagem de erro caso os campos obrigatórios não
            #       tenham sido preenchidos.
            messagebox.showerror("Erro", "ID, Usuário e Senha são obrigatórios.", parent=self.master)


    # Função para editar as informações de um funcionário existente no sistema.
    def editar_funcionario(self):

        # Obtém o texto inserido no campo de ID do funcionário e remove
        #       espaços em branco no início e no final.
        i = self.campo_id_func.get().strip()

        # Obtém o texto inserido no campo de Nome do funcionário e
        #       remove espaços em branco no início e no final.
        n = self.campo_nome.get().strip()

        # Obtém o texto inserido no campo de Cargo do funcionário e remove
        #       espaços em branco no início e no final.
        c = self.campo_cargo.get().strip()

        # Obtém o texto inserido no campo de Turno do funcionário e remove
        #       espaços em branco no início e no final.
        t = self.campo_turno.get().strip()

        # Obtém o texto inserido no campo de Salário do funcionário e remove
        #       espaços em branco no início e no final.
        s = self.campo_salario.get().strip()

        # Verifica se o campo de ID do funcionário foi preenchido.
        if i:

            # Chama a função externa 'editar_funcionario' para
            #       atualizar as informações no banco de dados.
            editar_funcionario(i, n, c, t, s)

            # Exibe uma mensagem de sucesso para informar que as alterações foram salvas.
            messagebox.showinfo("Sucesso", "Funcionário editado.", parent=self.master)

            # Atualiza a lista de funcionários exibida na tabela
            #       para refletir as alterações.
            self.listar_funcionarios()

            # Limpa os campos de entrada para que possam ser reutilizados.
            self.limpar_campos()

        else:

            # Exibe uma mensagem de erro caso o campo de ID não tenha sido preenchido.
            messagebox.showerror("Erro", "Informe o ID do funcionário.", parent=self.master)


    # Função para remover um funcionário selecionado na tabela.
    def remover_funcionario(self):

        # Obtém a seleção atual da tabela (Treeview).
        selecao = self.tabela.selection()

        # Verifica se algum item foi selecionado na tabela.
        if not selecao:

            # Exibe uma mensagem de erro caso nenhum funcionário tenha
            #       sido selecionado.
            messagebox.showerror("Erro", "Selecione um funcionário para remover.", parent=self.master)

            # Encerra a função, já que não há seleção para processar.
            return

        # Obtém o item selecionado da tabela, que contém as
        #       informações do funcionário.
        item = self.tabela.item(selecao[0])

        # Extrai o ID do funcionário dos valores do item selecionado.
        # `str()` garante que o ID seja tratado como uma string,
        #       caso não esteja nesse formato.
        id_func = str(item["values"][0])

        # Exibe uma caixa de diálogo de confirmação para garantir que o
        #       usuário deseja remover o funcionário.
        confirmacao = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja remover o funcionário com ID '{id_func}'?",
            parent=self.master
        )

        # Verifica se o usuário confirmou a remoção.
        if confirmacao:

            # Remove o funcionário da coleção de funcionários.
            resultado_funcionario = colecao_funcionarios.delete_one({"id_func": id_func})

            # Remove o usuário associado ao funcionário da coleção de usuários.
            resultado_usuario = colecao_usuarios.delete_one({"id_func": id_func})

            # Verifica se a exclusão do funcionário foi bem-sucedida.
            if resultado_funcionario.deleted_count > 0:

                # Exibe mensagem de sucesso ao remover o funcionário e o usuário.
                messagebox.showinfo(
                    "Sucesso",
                    f"Funcionário ID {id_func} e o usuário associado foram removidos com sucesso.",
                    parent=self.master
                )

                # Atualiza a lista de funcionários na tabela.
                self.listar_funcionarios()

                # Limpa os campos de entrada.
                self.limpar_campos()

            else:

                # Exibe uma mensagem de erro caso o funcionário não tenha sido removido.
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível remover o funcionário ID {id_func}. Verifique se o ID existe.",
                    parent=self.master
                )


    def selecionar_item(self, event):

        # Itera sobre cada seleção na tabela. Normalmente, espera-se que
        #       apenas um item seja selecionado de cada vez.
        for sel in self.tabela.selection():

            # Obtém o item da tabela que foi selecionado.
            item = self.tabela.item(sel)

            # Extrai os valores (dados do funcionário) do item selecionado.
            valores = item["values"]

            # Limpa o campo de ID do funcionário e insere o novo
            #       valor do funcionário selecionado.
            self.campo_id_func.delete(0, tk.END)
            self.campo_id_func.insert(0, valores[0])

            # Limpa o campo de nome do funcionário e insere o novo valor.
            self.campo_nome.delete(0, tk.END)
            self.campo_nome.insert(0, valores[1])

            # Limpa o campo de cargo do funcionário e insere o novo valor.
            self.campo_cargo.delete(0, tk.END)
            self.campo_cargo.insert(0, valores[2])

            # Limpa o campo de turno do funcionário e insere o novo valor.
            self.campo_turno.delete(0, tk.END)
            self.campo_turno.insert(0, valores[3])

            # Limpa o campo de salário do funcionário e insere o novo valor.
            self.campo_salario.delete(0, tk.END)
            self.campo_salario.insert(0, valores[4])

            # Limpa o campo de usuário, pois não é adequado mostrar a senha
            #       ou o usuário automaticamente após seleção.
            # Por questões de segurança, esses campos são limpos para
            #       prevenir a exibição indevida de informações sensíveis.
            self.campo_usuario.delete(0, tk.END)
            self.campo_senha.delete(0, tk.END)


    def listar_funcionarios(self):

        # Limpa todos os itens existentes na tabela para preparar
        #       para uma nova inserção de dados.
        for x in self.tabela.get_children():
            self.tabela.delete(x)

        # Obtém a lista atualizada de funcionários do banco de dados.
        funcs = obter_funcionarios()

        # Itera sobre cada funcionário retornado pela função `obter_funcionarios`.
        for f in funcs:

            # Insere cada funcionário na tabela. Cada funcionário é
            #       representado como uma linha na tabela,
            #       e os valores inseridos correspondem às colunas
            #       configuradas para a tabela.
            self.tabela.insert("",
                               tk.END,
                               values=(f["id_func"], f["nome"], f["cargo"], f["turno"], f["salario"]))



    def limpar_campos(self):

        # Limpa o campo de entrada para o ID do funcionário.
        self.campo_id_func.delete(0, tk.END)

        # Limpa o campo de entrada para o nome do funcionário.
        self.campo_nome.delete(0, tk.END)

        # Limpa o campo de entrada para o cargo do funcionário.
        self.campo_cargo.delete(0, tk.END)

        # Limpa o campo de entrada para o turno do funcionário.
        self.campo_turno.delete(0, tk.END)

        # Limpa o campo de entrada para o salário do funcionário.
        self.campo_salario.delete(0, tk.END)

        # Limpa o campo de entrada para o usuário (nome de
        #       usuário usado para login).
        self.campo_usuario.delete(0, tk.END)

        # Limpa o campo de entrada para a senha.
        self.campo_senha.delete(0, tk.END)


############################################
# Janela Produtos
############################################

# Classe que define a janela de gerenciamento de produtos,
#       herda de JanelaBase.
class JanelaProdutos(JanelaBase):

    # Construtor da classe que inicializa a janela de gerenciamento de produtos.
    def __init__(self, master):

        # Chama o construtor da classe base para configurar a janela.
        super().__init__(master, "Gerenciamento de Produtos")

        # Cria um frame (painel) no widget pai (master) com um espaço de 10 pixels.
        self.frame = ttk.Frame(self.master, padding="10")

        # Adiciona o frame ao widget pai e configura para preencher
        #       todo o espaço disponível, permitindo expansão.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Define uma lista de categorias de produtos disponíveis para seleção.
        self.categorias = ["Perecíveis", "Não Perecíveis", "Bebidas", "Higiene", "Limpeza", "Frios"]

        # Obtém uma lista de fornecedores do banco de dados e extrai seus nomes.
        fornecedores = obter_fornecedores()

        # Cria uma lista contendo apenas os nomes dos fornecedores
        #       para uso em componentes da UI.
        self.lista_fornecedores = [f["nome"] for f in fornecedores]

        # Criação do rótulo (Label) que aparece na interface:
        # 'self.frame': especifica que o rótulo será adicionado ao frame principal da janela.
        # 'text="Código:": especifica o texto que será mostrado no rótulo.
        # 'row=0': coloca o rótulo na primeira linha do grid.
        # 'column=0': coloca o rótulo na primeira coluna do grid.
        # 'sticky="w"': alinha o rótulo à esquerda dentro da célula do grid.
        # 'pady=5': adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Código:").grid(row=0,
                                       column=0,
                                       sticky="w",
                                       pady=5)

        # Criação de um campo de entrada (Entry) para inserir dados:
        # 'self.frame': especifica que o campo de entrada será adicionado
        #       ao frame principal da janela.
        self.campo_codigo = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada usando o gerenciador de grid:
        # 'row=0': coloca o campo de entrada na primeira linha do grid.
        # 'column=1': coloca o campo de entrada na segunda coluna do grid.
        # 'sticky="we"': faz com que o campo de entrada se expanda
        #       para preencher a largura da célula.
        # 'pady=5': adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_codigo.grid(row=0,
                               column=1,
                               sticky="we",
                               pady=5)

        # Criação do rótulo (Label) que aparece na interface:
        # 'self.frame': especifica que o rótulo será adicionado ao
        #       frame principal da janela.
        # 'text="Nome:": especifica o texto que será mostrado no rótulo.
        # 'row=1': coloca o rótulo na segunda linha do grid.
        # 'column=0': coloca o rótulo na primeira coluna do grid.
        # 'sticky="w"': alinha o rótulo à esquerda dentro da célula do grid.
        # 'pady=5': adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Nome:").grid(row=1,
                                     column=0,
                                     sticky="w",
                                     pady=5)

        # Criação de um campo de entrada (Entry) para inserir dados:
        # 'self.frame': especifica que o campo de entrada será adicionado
        #       ao frame principal da janela.
        self.campo_nome = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada usando o gerenciador de grid:
        # 'row=1': coloca o campo de entrada na segunda linha do grid.
        # 'column=1': coloca o campo de entrada na segunda coluna do grid.
        # 'sticky="we"': faz com que o campo de entrada se expanda
        #       para preencher a largura da célula.
        # 'pady=5': adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_nome.grid(row=1,
                             column=1,
                             sticky="we",
                             pady=5)

        # Criação do rótulo (Label) "Categoria":
        # 'self.frame': indica que o rótulo será adicionado ao frame principal da janela.
        # 'text="Categoria:": define o texto do rótulo que identifica o
        #       campo para seleção de categoria.
        # 'row=2': posiciona o rótulo na terceira linha do grid.
        # 'column=0': posiciona o rótulo na primeira coluna do grid.
        # 'sticky="w"': alinha o rótulo à esquerda na célula do grid.
        # 'pady=5': adiciona um espaçamento vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Categoria:").grid(row=2,
                                          column=0,
                                          sticky="w",
                                          pady=5)

        # Criação de um ComboBox para seleção de categoria:
        # 'self.frame': indica que o ComboBox será adicionado ao
        #       frame principal da janela.
        # 'values=self.categorias': define as opções disponíveis no
        #       ComboBox, que são categorias de produtos.
        # 'font=("Arial",14)': define a fonte e tamanho do texto dentro do ComboBox.
        self.combo_categoria = ttk.Combobox(self.frame,
                                            values=self.categorias,
                                            font=("Arial", 14))

        # Configuração do layout do ComboBox usando o gerenciador de grid:
        # 'row=2': posiciona o ComboBox na terceira linha do grid.
        # 'column=1': posiciona o ComboBox na segunda coluna do grid.
        # 'sticky="we"': faz com que o ComboBox se expanda para preencher a largura da célula.
        # 'pady=5': adiciona um espaçamento vertical de 5 pixels acima e abaixo do ComboBox.
        self.combo_categoria.grid(row=2,
                                  column=1,
                                  sticky="we",
                                  pady=5)

        # Criação de um rótulo (label) com o texto "Quantidade", posicionado no frame.
        # 'row=3' indica que o rótulo será colocado na quarta linha da
        #       grade (grid) do frame (contagem começa em 0).
        # 'column=0' especifica que o rótulo será colocado na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Quantidade:").grid(row=3,
                                           column=0,
                                           sticky="w",
                                           pady=5)

        # Criação de um campo de entrada (entry) para que o usuário possa digitar a quantidade.
        # Este campo é armazenado na variável 'self.campo_quantidade'.
        self.campo_quantidade = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada na grade.
        # 'row=3' posiciona o campo de entrada na mesma linha do rótulo "Quantidade".
        # 'column=1' coloca o campo de entrada na segunda coluna da grade, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada expanda para preencher o
        #       espaço horizontal disponível na célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_quantidade.grid(row=3,
                                   column=1,
                                   sticky="we",
                                   pady=5)

        # Criação de um rótulo (label) com o texto "Preço", posicionado no frame.
        # 'row=4' indica que o rótulo será colocado na quinta linha da
        #       grade (grid) do frame (contagem começa em 0).
        # 'column=0' especifica que o rótulo será colocado na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Preço:").grid(row=4,
                                      column=0,
                                      sticky="w",
                                      pady=5)

        # Criação de um campo de entrada (entry) para que o usuário possa digitar o preço.
        # Este campo é armazenado na variável 'self.campo_preco'.
        self.campo_preco = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada na grade.
        # 'row=4' posiciona o campo de entrada na mesma linha do rótulo "Preço".
        # 'column=1' coloca o campo de entrada na segunda coluna da grade, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada expanda para
        #       preencher o espaço horizontal disponível na célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_preco.grid(row=4,
                              column=1,
                              sticky="we",
                              pady=5)

        # Criação de um rótulo (label) com o texto "Fornecedor", posicionado no frame.
        # 'row=5' indica que o rótulo será colocado na sexta linha da
        #       grade (grid) do frame (contagem começa em 0).
        # 'column=0' especifica que o rótulo será colocado na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Fornecedor:").grid(row=5,
                                           column=0,
                                           sticky="w",
                                           pady=5)

        # Criação de um combobox para seleção de fornecedor.
        # 'values=self.lista_fornecedores' carrega a lista de fornecedores
        #       obtida do banco de dados ou de uma lista pré-definida.
        # 'font=("Arial", 14)' define a fonte e o tamanho da fonte para o
        #       texto dentro do combobox.
        self.combo_fornecedor = ttk.Combobox(self.frame,
                                             values=self.lista_fornecedores,
                                             font=("Arial", 14))

        # Configuração do layout do combobox na grade.
        # 'row=5' posiciona o combobox na mesma linha do rótulo "Fornecedor".
        # 'column=1' coloca o combobox na segunda coluna da grade, ao lado do rótulo.
        # 'sticky="we"' faz com que o combobox expanda para preencher o espaço
        #       horizontal disponível na célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do combobox.
        self.combo_fornecedor.grid(row=5,
                                   column=1,
                                   sticky="we",
                                   pady=5)

        # Criação de um rótulo (label) com o texto "Validade (dd/mm/aaaa)", posicionado no frame.
        # 'row=6' indica que o rótulo será colocado na sétima linha da
        #       grade (grid) do frame (contagem começa em 0).
        # 'column=0' especifica que o rótulo será colocado na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Validade (dd/mm/aaaa):").grid(row=6,
                                                      column=0,
                                                      sticky="w",
                                                      pady=5)

        # Criação de um campo de entrada (entry) para que o usuário possa
        #       digitar a data de validade do produto.
        # Este campo é armazenado na variável 'self.campo_validade'.
        self.campo_validade = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada na grade.
        # 'row=6' posiciona o campo de entrada na mesma linha do rótulo "Validade (dd/mm/aaaa)".
        # 'column=1' coloca o campo de entrada na segunda coluna da grade, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada expanda para preencher o
        #       espaço horizontal disponível na célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_validade.grid(row=6,
                                 column=1,
                                 sticky="we",
                                 pady=5)

        # Criação de um rótulo (label) com o texto "Unidade (ex: Kg, un):", posicionado no frame.
        # 'row=7' indica que o rótulo será colocado na oitava linha da
        #       grade (grid) do frame (contagem começa em 0).
        # 'column=0' especifica que o rótulo será colocado na primeira coluna da grade.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Unidade (ex: Kg, un):").grid(row=7,
                                                     column=0,
                                                     sticky="w",
                                                     pady=5)

        # Criação de um campo de entrada (entry) para que o usuário
        #       possa digitar a unidade do produto.
        # Este campo é armazenado na variável 'self.campo_unidade'.
        self.campo_unidade = ttk.Entry(self.frame)

        # Configuração do layout do campo de entrada na grade.
        # 'row=7' posiciona o campo de entrada na mesma linha do
        #       rótulo "Unidade (ex: Kg, un)".
        # 'column=1' coloca o campo de entrada na segunda coluna da grade, ao lado do rótulo.
        # 'sticky="we"' faz com que o campo de entrada expanda para preencher o
        #       espaço horizontal disponível na célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_unidade.grid(row=7,
                                column=1,
                                sticky="we",
                                pady=5)

        # Criação de um botão chamado "Adicionar" que, quando clicado,
        #       chama o método 'adicionar_produto'.
        # Este botão é posicionado no frame.
        self.botao_adicionar = ttk.Button(self.frame,
                                          text="Adicionar",
                                          command=self.adicionar_produto)

        # Configuração do layout do botão "Adicionar" na grade.
        # 'row=8' posiciona o botão na nona linha do grid.
        # 'column=0' coloca o botão na primeira coluna do grid.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e
        #       abaixo do botão para separá-lo de outros elementos.
        self.botao_adicionar.grid(row=8,
                                  column=0,
                                  pady=10)

        # Criação de um botão chamado "Editar" que, quando clicado,
        #       chama o método 'editar_produto'.
        # Este botão é posicionado no frame.
        self.botao_editar = ttk.Button(self.frame,
                                       text="Editar",
                                       command=self.editar_produto)

        # Configuração do layout do botão "Editar" na grade.
        # 'row=8' posiciona o botão na nona linha do grid, na
        #       mesma linha do botão "Adicionar".
        # 'column=1' coloca o botão na segunda coluna do grid.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo do botão.
        self.botao_editar.grid(row=8,
                               column=1,
                               pady=10)

        # Criação de um botão chamado "Remover" que, quando clicado,
        #       chama o método 'remover_produto'.
        # Este botão é posicionado no frame.
        self.botao_remover = ttk.Button(self.frame,
                                        text="Remover",
                                        command=self.remover_produto)

        # Configuração do layout do botão "Remover" na grade.
        # 'row=9' posiciona o botão na décima linha do grid, abaixo
        #       dos botões "Adicionar" e "Editar".
        # 'column=0' coloca o botão na primeira coluna do grid.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo do botão.
        self.botao_remover.grid(row=9,
                                column=0,
                                pady=10)


        # Criação da tabela 'Treeview' dentro do 'self.frame'.
        # A tabela terá colunas identificadas por nomes específicos e mostrará
        #       apenas os cabeçalhos dessas colunas.
        self.tabela = ttk.Treeview(self.frame,
                                   columns=("codigo", "nome", "categoria", "quantidade", "preco", "fornecedor", "validade", "unidade"),
                                   show="headings")

        # Configuração dos cabeçalhos da tabela. Para cada coluna, o texto do
        #       cabeçalho é o nome da coluna com a primeira letra maiúscula.
        for col in ("codigo", "nome", "categoria", "quantidade", "preco", "fornecedor", "validade", "unidade"):
            self.tabela.heading(col, text=col.capitalize())

        # Configuração do layout da tabela na interface.
        # 'row=10' coloca a tabela na décima primeira linha do grid do frame.
        # 'column=0' inicia a tabela na primeira coluna do grid.
        # 'columnspan=2' faz com que a tabela se estenda por duas colunas.
        # 'sticky="nsew"' faz com que a tabela expanda em todas as
        #       direções (norte, sul, leste, oeste) para preencher o espaço disponível.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e
        #       abaixo da tabela para separá-la de outros elementos.
        self.tabela.grid(row=10,
                         column=0,
                         columnspan=2,
                         sticky="nsew",
                         pady=10)

        # Configuração da linha 10 do grid para que ela possa expandir e
        #       contrair, permitindo que a tabela mude de tamanho conforme a
        #       janela é redimensionada.
        self.frame.rowconfigure(10, weight=1)

        # Configuração da coluna 1 do grid para que ela possa expandir e contrair,
        #       garantindo que a tabela utilize eficientemente o espaço horizontal disponível.
        self.frame.columnconfigure(1, weight=1)

        # Associação de um evento de seleção de item na tabela com o método 'selecionar_item'.
        # Isso permite que ações específicas sejam executadas quando um
        #       item é selecionado pelo usuário.
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_item)

        # Chamada ao método 'listar_produtos' para preencher a tabela com os
        #       dados dos produtos ao inicializar a janela.
        self.listar_produtos()


    def adicionar_produto(self):

        # Obtém o texto do campo código e remove espaços extras.
        c = self.campo_codigo.get().strip()

        # Obtém o texto do campo nome e remove espaços extras.
        n = self.campo_nome.get().strip()

        # Obtém o texto selecionado na combobox de categoria e remove espaços extras.
        cat = self.combo_categoria.get().strip()

        # Obtém o texto do campo quantidade e remove espaços extras.
        q = self.campo_quantidade.get().strip()

        # Obtém o texto do campo preço e remove espaços extras.
        p = self.campo_preco.get().strip()

        # Obtém o texto selecionado na combobox de fornecedores e
        #       remove espaços extras.
        f = self.combo_fornecedor.get().strip()

        # Obtém o texto do campo validade e remove espaços extras.
        v = self.campo_validade.get().strip()

        # Obtém o texto do campo unidade e remove espaços extras.
        u = self.campo_unidade.get().strip()

        # Verifica se os campos de código e nome não estão vazios.
        if c and n:

            # Chama a função para cadastrar o produto com os dados fornecidos.
            cadastrar_produto(c, n, cat, q, p, f, v, u)

            # Exibe uma mensagem de sucesso.
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.",
                                parent=self.master)

            # Atualiza a lista de produtos exibida.
            self.listar_produtos()

            # Limpa todos os campos após o cadastro.
            self.limpar_campos()

        else:

            # Exibe uma mensagem de erro se código ou nome estiverem vazios.
            messagebox.showerror("Erro",
                                 "Código e Nome são obrigatórios.",
                                 parent=self.master)


    def editar_produto(self):

        # Obtém e limpa o texto do campo de código.
        c = self.campo_codigo.get().strip()

        # Obtém e limpa o texto do campo de nome.
        n = self.campo_nome.get().strip()

        # Obtém e limpa o valor selecionado da combobox de categoria.
        cat = self.combo_categoria.get().strip()

        # Obtém e limpa o texto do campo de quantidade.
        q = self.campo_quantidade.get().strip()

        # Obtém e limpa o texto do campo de preço.
        p = self.campo_preco.get().strip()

        # Obtém e limpa o valor selecionado da combobox de fornecedores.
        f = self.combo_fornecedor.get().strip()

        # Obtém e limpa o texto do campo de validade.
        v = self.campo_validade.get().strip()

        # Obtém e limpa o texto do campo de unidade.
        u = self.campo_unidade.get().strip()

        # Verifica se o código do produto foi fornecido.
        if c:

            # Chama a função para editar o produto com os valores fornecidos.
            editar_produto(c, n, cat, q, p, f, v, u)

            # Mostra uma mensagem de sucesso após a edição.
            messagebox.showinfo("Sucesso",
                                "Produto editado com sucesso.",
                                parent=self.master)

            # Atualiza a lista de produtos na interface.
            self.listar_produtos()

            # Limpa os campos após a edição.
            self.limpar_campos()

        else:

            # Mostra uma mensagem de erro se o código não for fornecido.
            messagebox.showerror("Erro",
                                 "É necessário informar o código do produto para editar.",
                                 parent=self.master)



    def remover_produto(self):

        # Obtém o texto do campo de código.
        c = self.campo_codigo.get().strip()

        # Verifica se o código do produto foi fornecido.
        if c:

            # Chama a função para remover o produto com o código especificado.
            remover_produto(c)

            # Exibe uma mensagem de sucesso informando que o produto foi removido.
            messagebox.showinfo("Sucesso", "Produto removido.", parent=self.master)

            # Atualiza a lista de produtos exibida na interface.
            self.listar_produtos()

            # Limpa os campos de entrada após a remoção do produto.
            self.limpar_campos()

        else:

            # Exibe uma mensagem de erro se o código do produto não for informado.
            messagebox.showerror("Erro", "Informe o código do produto para remover.")



    def listar_produtos(self):

        # Loop para percorrer todos os itens filhos presentes na
        #       tabela Treeview e deletar cada um.
        # Isso é necessário para limpar a tabela antes de inserir
        #       novos dados e evitar duplicidade.
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        # Chama a função obter_produtos para buscar todos os produtos
        #       cadastrados no banco de dados.
        # Esta função retorna uma lista de dicionários, onde cada
        #       dicionário representa um produto.
        produtos = obter_produtos()

        # Loop para percorrer cada produto obtido da função obter_produtos.
        # Para cada produto, ele insere na tabela os dados do produto.
        # Os dados incluem código, nome, categoria, quantidade, preço,
        #       fornecedor, validade e unidade.
        # 'tk.END' é usado para inserir cada novo item no final da lista na tabela.
        # 'values' recebe uma tupla com os dados do produto, correspondendo à
        #       ordem das colunas na definição da tabela.
        for p in produtos:
            self.tabela.insert("",
                               tk.END,
                               values=(p["codigo"], p["nome"], p["categoria"], p["quantidade"], p["preco"], p["fornecedor"], p["validade"], p["unidade"]))



    def selecionar_item(self, event):

        # Este loop percorre todos os itens selecionados na tabela Treeview.
        # 'self.tabela.selection()' retorna uma lista dos itens selecionados.
        for sel in self.tabela.selection():

            # 'self.tabela.item(sel)' retorna um dicionário contendo os detalhes
            #       do item selecionado, incluindo os valores.
            item = self.tabela.item(sel)

            # 'valores' é uma lista que contém os dados do item,
            #       correspondendo às colunas da tabela.
            valores = item["values"]

            # Limpa o campo de entrada 'campo_codigo' antes de inserir um novo valor.
            self.campo_codigo.delete(0, tk.END)

            # Insere o valor do código do produto no campo 'campo_codigo'.
            self.campo_codigo.insert(0, valores[0])

            # Limpa o campo de entrada 'campo_nome' antes de inserir um novo valor.
            self.campo_nome.delete(0, tk.END)

            # Insere o valor do nome do produto no campo 'campo_nome'.
            self.campo_nome.insert(0, valores[1])

            # Define o valor atual do combobox 'combo_categoria' para a
            #       categoria do produto selecionado.
            self.combo_categoria.set(valores[2])

            # Limpa o campo de entrada 'campo_quantidade' antes de inserir um novo valor.
            self.campo_quantidade.delete(0, tk.END)

            # Insere o valor da quantidade do produto no campo 'campo_quantidade'.
            self.campo_quantidade.insert(0, valores[3])

            # Limpa o campo de entrada 'campo_preco' antes de inserir um novo valor.
            self.campo_preco.delete(0, tk.END)

            # Insere o valor do preço do produto no campo 'campo_preco'.
            self.campo_preco.insert(0, valores[4])

            # Define o valor atual do combobox 'combo_fornecedor' para o
            #       fornecedor do produto selecionado.
            self.combo_fornecedor.set(valores[5])

            # Limpa o campo de entrada 'campo_validade' antes de inserir um novo valor.
            self.campo_validade.delete(0, tk.END)

            # Insere o valor da validade do produto no campo 'campo_validade'.
            self.campo_validade.insert(0, valores[6])

            # Limpa o campo de entrada 'campo_unidade' antes de inserir um novo valor.
            self.campo_unidade.delete(0, tk.END)

            # Insere o valor da unidade de medida do produto no campo 'campo_unidade'.
            self.campo_unidade.insert(0, valores[7])


    def limpar_campos(self):

        # Limpa o campo de entrada para o código do produto.
        # '0' e 'tk.END' especificam que o conteúdo será apagado
        #       desde o início até o fim do campo.
        self.campo_codigo.delete(0, tk.END)

        # Limpa o campo de entrada para o nome do produto.
        self.campo_nome.delete(0, tk.END)

        # Reseta o combobox de categorias para um estado vazio, sem seleção.
        self.combo_categoria.set("")

        # Limpa o campo de entrada para a quantidade do produto.
        self.campo_quantidade.delete(0, tk.END)

        # Limpa o campo de entrada para o preço do produto.
        self.campo_preco.delete(0, tk.END)

        # Reseta o combobox de fornecedores para um estado vazio, sem seleção.
        self.combo_fornecedor.set("")

        # Limpa o campo de entrada para a validade do produto.
        self.campo_validade.delete(0, tk.END)

        # Limpa o campo de entrada para a unidade de medida do produto.
        self.campo_unidade.delete(0, tk.END)



############################################
# Janela Clientes
############################################

# Classe para gerenciar a interface de clientes, herda de JanelaBase
#           que configura a janela principal.
class JanelaClientes(JanelaBase):

    # Método construtor para inicializar a janela de clientes.
    def __init__(self, master):

        # Chama o construtor da classe base para configurar o título da
        #       janela e outras propriedades básicas.
        super().__init__(master, "Gerenciamento de Clientes")

        # Cria um frame (container) para organizar widgets dentro da
        #       janela principal, com 10 pixels de espaço interno.
        self.frame = ttk.Frame(self.master, padding="10")

        # Adiciona o frame ao layout principal, permitindo que ele
        #       expanda e preencha o espaço disponível.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Cria um rótulo para o campo 'Código' e posiciona no frame
        #       usando o gerenciador de geometria grid.
        # 'row=0' e 'column=0' posicionam o rótulo na primeira linha e coluna, respectivamente.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Código:").grid(row=0,
                                       column=0,
                                       sticky="w",
                                       pady=5)

        # Cria um campo de entrada para inserção do código do cliente.
        self.campo_codigo = ttk.Entry(self.frame)

        # Configura a posição do campo de entrada no grid.
        # 'row=0' e 'column=1' colocam o campo na primeira linha e segunda coluna.
        # 'sticky="we"' faz com que o campo de entrada expanda para preencher
        #       horizontalmente o espaço disponível na célula.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_codigo.grid(row=0,
                               column=1,
                               sticky="we",
                               pady=5)

        # Cria um rótulo (label) com o texto "Nome", posicionando-o no frame.
        # 'row=1' e 'column=0' colocam o rótulo na segunda linha e na primeira coluna do grid.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do
        #       rótulo para separá-lo visualmente dos outros componentes.
        ttk.Label(self.frame,
                  text="Nome:").grid(row=1,
                                     column=0,
                                     sticky="w",
                                     pady=5)

        # Cria um campo de entrada (Entry) para inserção do nome do cliente.
        self.campo_nome = ttk.Entry(self.frame)

        # Configura o campo de entrada no grid.
        # 'row=1' e 'column=1' posicionam o campo de entrada ao lado do
        #       rótulo "Nome", na segunda linha e segunda coluna.
        # 'sticky="we"' faz com que o campo de entrada expanda para
        #       preencher horizontalmente o espaço disponível na célula.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do
        #       campo de entrada para um layout mais limpo.
        self.campo_nome.grid(row=1,
                             column=1,
                             sticky="we",
                             pady=5)

        # Cria um rótulo (label) com o texto "CPF/CNPJ", posicionando-o no frame.
        # 'row=2' define que o rótulo será colocado na terceira linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna dessa linha.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do
        #       rótulo, melhorando o espaçamento visual.
        ttk.Label(self.frame,
                  text="CPF/CNPJ:").grid(row=2,
                                         column=0,
                                         sticky="w",
                                         pady=5)

        # Cria um campo de entrada (Entry) para que o usuário
        #       insira o CPF ou CNPJ do cliente.
        # Este campo é armazenado na variável 'self.campo_cpf_cnpj'.
        self.campo_cpf_cnpj = ttk.Entry(self.frame)

        # Configura o campo de entrada no grid para alinhá-lo corretamente no layout.
        # 'row=2' posiciona o campo de entrada na terceira linha, alinhado
        #       horizontalmente com o rótulo "CPF/CNPJ".
        # 'column=1' posiciona o campo na segunda coluna dessa linha, ao lado do rótulo.
        # 'sticky="we"' permite que o campo de entrada expanda horizontalmente,
        #       ocupando todo o espaço disponível na célula.
        # 'pady=5' adiciona um espaçamento vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_cpf_cnpj.grid(row=2,
                                 column=1,
                                 sticky="we",
                                 pady=5)

        # Cria um rótulo (label) com o texto "Telefone", posicionando-o no frame.
        # 'row=3' define que o rótulo será colocado na quarta linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna dessa linha.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do rótulo para melhorar o espaçamento.
        ttk.Label(self.frame,
                  text="Telefone:").grid(row=3,
                                         column=0,
                                         sticky="w",
                                         pady=5)

        # Cria um campo de entrada (Entry) para que o usuário insira o telefone do cliente.
        # Este campo é armazenado na variável 'self.campo_telefone'.
        self.campo_telefone = ttk.Entry(self.frame)

        # Configura o campo de entrada no grid para alinhá-lo corretamente no layout.
        # 'row=3' posiciona o campo de entrada na quarta linha, alinhado
        #       horizontalmente com o rótulo "Telefone".
        # 'column=1' posiciona o campo na segunda coluna dessa linha, ao lado do rótulo.
        # 'sticky="we"' permite que o campo de entrada expanda horizontalmente,
        #       ocupando todo o espaço disponível na célula.
        # 'pady=5' adiciona um espaçamento vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_telefone.grid(row=3,
                                 column=1,
                                 sticky="we",
                                 pady=5)

        # Cria um rótulo (label) com o texto "Endereço", posicionando-o no frame.
        # 'row=4' define que o rótulo será colocado na quinta linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna dessa linha.
        # 'sticky="w"' alinha o rótulo à esquerda dentro da célula do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do rótulo para melhorar o espaçamento.
        ttk.Label(self.frame,
                  text="Endereço:").grid(row=4,
                                         column=0,
                                         sticky="w",
                                         pady=5)

        # Cria um campo de entrada (Entry) para que o usuário insira o endereço do cliente.
        # Este campo é armazenado na variável 'self.campo_endereco'.
        self.campo_endereco = ttk.Entry(self.frame)

        # Configura o campo de entrada no grid para alinhá-lo corretamente no layout.
        # 'row=4' posiciona o campo de entrada na quinta linha, alinhado
        #       horizontalmente com o rótulo "Endereço".
        # 'column=1' posiciona o campo na segunda coluna dessa linha, ao lado do rótulo.
        # 'sticky="we"' permite que o campo de entrada expanda horizontalmente,
        #       ocupando todo o espaço disponível na célula.
        # 'pady=5' adiciona um espaçamento vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        self.campo_endereco.grid(row=4,
                                 column=1,
                                 sticky="we",
                                 pady=5)

        # Cria um botão para cadastrar um cliente.
        # O texto exibido no botão é "Cadastrar".
        # O parâmetro 'command=self.cadastrar_cliente' define a função a ser
        #       chamada quando o botão for clicado.
        self.botao_cadastrar = ttk.Button(self.frame,
                                          text="Cadastrar",
                                          command=self.cadastrar_cliente)

        # Configura o botão "Cadastrar" no grid.
        # 'row=5' posiciona o botão na sexta linha do grid.
        # 'column=0' posiciona o botão na primeira coluna dessa linha.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels
        #       acima e abaixo do botão.
        self.botao_cadastrar.grid(row=5,
                                  column=0,
                                  pady=10)

        # Cria um botão para editar um cliente.
        # O texto exibido no botão é "Editar".
        # O parâmetro 'command=self.editar_cliente' define a função a ser
        #       chamada quando o botão for clicado.
        self.botao_editar = ttk.Button(self.frame,
                                       text="Editar",
                                       command=self.editar_cliente)

        # Configura o botão "Editar" no grid.
        # 'row=5' posiciona o botão na sexta linha do grid, na mesma linha do botão "Cadastrar".
        # 'column=1' posiciona o botão na segunda coluna dessa linha.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels acima e abaixo do botão.
        self.botao_editar.grid(row=5,
                               column=1,
                               pady=10)

        # Cria um botão para remover um cliente.
        # O texto exibido no botão é "Remover".
        # O parâmetro 'command=self.remover_cliente' define a função a ser
        #       chamada quando o botão for clicado.
        self.botao_remover = ttk.Button(self.frame,
                                        text="Remover",
                                        command=self.remover_cliente)

        # Configura o botão "Remover" no grid.
        # 'row=6' posiciona o botão na sétima linha do grid.
        # 'column=0' posiciona o botão na primeira coluna dessa linha.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels acima e abaixo do botão.
        self.botao_remover.grid(row=6,
                                column=0,
                                pady=10)

        # Cria um botão para exibir o histórico de compras de um cliente.
        # O texto exibido no botão é "Histórico Compras".
        # O parâmetro 'command=self.exibir_historico' define a função a
        #       ser chamada quando o botão for clicado.
        self.botao_historico = ttk.Button(self.frame,
                                          text="Histórico Compras",
                                          command=self.exibir_historico)

        # Configura o botão "Histórico Compras" no grid.
        # 'row=6' posiciona o botão na sétima linha do grid, na mesma linha do botão "Remover".
        # 'column=1' posiciona o botão na segunda coluna dessa linha.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels acima e abaixo do botão.
        self.botao_historico.grid(row=6,
                                  column=1,
                                  pady=10)

        # Criação de uma tabela (Treeview) para exibir os dados dos clientes.
        # A tabela será exibida no frame principal.
        # 'columns' define as colunas que a tabela terá: "codigo", "nome", "cpf_cnpj", "telefone" e "endereco".
        # 'show="headings"' oculta a primeira coluna padrão e exibe
        #       apenas os cabeçalhos definidos.
        self.tabela = ttk.Treeview(
            self.frame,
            columns=("codigo", "nome", "cpf_cnpj", "telefone", "endereco"),
            show="headings"
        )

        # Configuração dos cabeçalhos (títulos) das colunas da tabela.
        # Itera sobre a lista de nomes das colunas e define o texto de cada cabeçalho.
        # 'col.capitalize()' transforma o nome da coluna para iniciar com letra maiúscula.
        for col in ("codigo", "nome", "cpf_cnpj", "telefone", "endereco"):
            self.tabela.heading(col, text=col.capitalize())

        # Configuração da tabela no layout usando o gerenciador de geometria 'grid'.
        # 'row=7' posiciona a tabela na oitava linha do grid.
        # 'column=0' coloca a tabela na primeira coluna.
        # 'columnspan=2' faz a tabela ocupar duas colunas no grid.
        # 'sticky="nsew"' permite que a tabela se expanda para preencher toda a célula no layout.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels acima e abaixo da tabela.
        self.tabela.grid(row=7,
                         column=0,
                         columnspan=2,
                         sticky="nsew",
                         pady=10)

        # Configuração do redimensionamento automático do layout do frame.
        # 'rowconfigure' faz com que a linha 7 do grid redimensione
        #       automaticamente ao redimensionar a janela.
        # 'weight=1' define o peso para priorizar o redimensionamento dessa linha.
        self.frame.rowconfigure(7, weight=1)

        # Configuração do redimensionamento automático para a coluna 1 do grid.
        # 'columnconfigure' faz com que a segunda coluna (índice 1) redimensione automaticamente.
        # 'weight=1' define o peso para priorizar o redimensionamento dessa coluna.
        self.frame.columnconfigure(1, weight=1)

        # Associação de um evento à tabela.
        # 'bind("<<TreeviewSelect>>")' captura o evento de seleção de um item na tabela.
        # 'self.selecionar_item' é o método chamado sempre que um item for selecionado.
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_item)

        # Chamada do método para listar os clientes na tabela.
        # 'self.listar_clientes()' preenche a tabela com os dados dos clientes existentes.
        self.listar_clientes()


    # Método que será chamado ao selecionar um item na tabela.
            # O evento `event` é passado automaticamente pelo bind ao disparar o evento.
    def selecionar_item(self, event):

        # Itera sobre os itens atualmente selecionados na tabela.
        for sel in self.tabela.selection():

            # Obtém os dados do item selecionado como um dicionário,
            #       incluindo valores e tags.
            item = self.tabela.item(sel)

            # Extrai os valores do item (cada coluna da linha
            #       selecionada) como uma lista.
            valores = item["values"]

            # Limpa o campo de entrada para o código do cliente.
            self.campo_codigo.delete(0, tk.END)

            # Insere o valor do código do cliente (primeiro valor da
            #       lista `valores`) no campo de entrada.
            self.campo_codigo.insert(0, valores[0])

            # Limpa o campo de entrada para o nome do cliente.
            self.campo_nome.delete(0, tk.END)

            # Insere o valor do nome do cliente (segundo valor da
            #       lista `valores`) no campo de entrada.
            self.campo_nome.insert(0, valores[1])

            # Limpa o campo de entrada para o CPF/CNPJ do cliente.
            self.campo_cpf_cnpj.delete(0, tk.END)

            # Insere o valor do CPF/CNPJ (terceiro valor da
            #       lista `valores`) no campo de entrada.
            self.campo_cpf_cnpj.insert(0, valores[2])

            # Limpa o campo de entrada para o telefone do cliente.
            self.campo_telefone.delete(0, tk.END)

            # Insere o valor do telefone (quarto valor da lista `valores`)
            #       no campo de entrada.
            self.campo_telefone.insert(0, valores[3])

            # Limpa o campo de entrada para o endereço do cliente.
            self.campo_endereco.delete(0, tk.END)

            # Insere o valor do endereço (quinto valor da lista `valores`)
            #       no campo de entrada.
            self.campo_endereco.insert(0, valores[4])


    # Método para cadastrar um cliente, utilizando os dados
    #       inseridos nos campos da interface.
    def cadastrar_cliente(self):

        # Obtém o valor do campo de entrada de código e remove
        #       espaços em branco das extremidades.
        c = self.campo_codigo.get().strip()

        # Obtém o valor do campo de entrada de nome e remove
        #       espaços em branco das extremidades.
        n = self.campo_nome.get().strip()

        # Obtém o valor do campo de entrada de CPF/CNPJ e remove
        #       espaços em branco das extremidades.
        cc = self.campo_cpf_cnpj.get().strip()

        # Obtém o valor do campo de entrada de telefone e remove
        #       espaços em branco das extremidades.
        t = self.campo_telefone.get().strip()

        # Obtém o valor do campo de entrada de endereço e remove
        #       espaços em branco das extremidades.
        e = self.campo_endereco.get().strip()

        # Verifica se os campos obrigatórios (código e nome) foram preenchidos.
        if c and n:

            # Chama a função `cadastrar_cliente` para inserir os
            #       dados do cliente no banco de dados.
            cadastrar_cliente(c, n, cc, t, e)

            # Exibe uma mensagem de sucesso em uma caixa de diálogo.
            messagebox.showinfo("Sucesso", "Cliente cadastrado.", parent=self.master)

            # Atualiza a tabela com a lista de clientes após o cadastro.
            self.listar_clientes()

            # Limpa os campos de entrada para permitir novos cadastros.
            self.limpar_campos()

        else:

            # Caso os campos obrigatórios não sejam preenchidos,
            #       exibe uma mensagem de erro.
            messagebox.showerror("Erro", "Código e Nome são obrigatórios.", parent=self.master)


    # Método para editar os dados de um cliente existente.
    def editar_cliente(self):

        # Obtém o valor do campo de entrada de código e remove
        #       espaços em branco das extremidades.
        c = self.campo_codigo.get().strip()

        # Obtém o valor do campo de entrada de nome e remove
        #       espaços em branco das extremidades.
        n = self.campo_nome.get().strip()

        # Obtém o valor do campo de entrada de CPF/CNPJ e remove
        #       espaços em branco das extremidades.
        cc = self.campo_cpf_cnpj.get().strip()

        # Obtém o valor do campo de entrada de telefone e remove
        #       espaços em branco das extremidades.
        t = self.campo_telefone.get().strip()

        # Obtém o valor do campo de entrada de endereço e remove
        #       espaços em branco das extremidades.
        e = self.campo_endereco.get().strip()

        # Verifica se o campo de código foi preenchido (obrigatório
        #       para editar o cliente).
        if c:

            # Chama a função `editar_cliente` para atualizar os
            #       dados do cliente no banco de dados.
            editar_cliente(c, n, cc, t, e)

            # Exibe uma mensagem de sucesso em uma caixa de diálogo.
            messagebox.showinfo("Sucesso", "Cliente editado.", parent=self.master)

            # Atualiza a tabela com a lista de clientes após a edição.
            self.listar_clientes()

            # Limpa os campos de entrada após a edição.
            self.limpar_campos()

        else:

            # Caso o campo de código não seja preenchido, exibe
            #       uma mensagem de erro.
            messagebox.showerror("Erro", "Informe o código do cliente.", parent=self.master)


    # Método para remover um cliente do banco de dados.
    def remover_cliente(self):

        # Obtém o valor do campo de entrada de código e remove
        #       espaços em branco das extremidades.
        c = self.campo_codigo.get().strip()

        # Verifica se o campo de código está vazio.
        if not c:

            # Caso o campo esteja vazio, exibe uma mensagem de erro
            #       em uma caixa de diálogo.
            messagebox.showerror("Erro", "Selecione um cliente para remover.", parent=self.master)

            # Interrompe a execução do método para evitar ações posteriores.
            return

        # Exibe uma caixa de diálogo de confirmação para o usuário,
        #       perguntando se deseja realmente remover o cliente.
        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este cliente?",
                                          parent=self.master)

        # Verifica se o usuário confirmou a ação de remoção.
        if confirmacao:

            # Remove o cliente do banco de dados usando o código como identificador.
            colecao_clientes.delete_one({"codigo": c})

            # Exibe uma mensagem informando que o cliente foi removido com sucesso.
            messagebox.showinfo("Sucesso", "Cliente removido.", parent=self.master)

            # Atualiza a tabela de clientes após a remoção.
            self.listar_clientes()

            # Limpa os campos de entrada para preparar a interface para novas ações.
            self.limpar_campos()


    # Método para exibir o histórico de compras de um cliente específico.
    def exibir_historico(self):

        # Obtém o valor do campo de código do cliente, removendo
        #       quaisquer espaços em branco antes ou depois.
        c = self.campo_codigo.get().strip()

        # Verifica se o campo de código está vazio.
        if not c:

            # Exibe uma mensagem de erro indicando que o código
            #       do cliente é necessário.
            messagebox.showerror("Erro", "Informe o código do cliente.", parent=self.master)
            return  # Encerra o método se o código não for informado.

        # Procura no banco de dados o cliente correspondente ao código informado.
        cliente = colecao_clientes.find_one({"codigo": c})

        # Verifica se o cliente não foi encontrado no banco de dados.
        if not cliente:

            # Exibe uma mensagem de erro indicando que o
            #       cliente não foi encontrado.
            messagebox.showerror("Erro", "Cliente não encontrado.", parent=self.master)
            return  # Encerra o método se o cliente não existir.

        # Obtém o histórico de compras do cliente a partir do campo "historico_compras".
        # Caso o campo não exista, retorna uma lista vazia como padrão.
        historico = cliente.get("historico_compras", [])

        # Verifica se o histórico de compras está vazio.
        if not historico:

            # Exibe uma mensagem informando que nenhuma compra foi
            #       encontrada para o cliente.
            messagebox.showinfo("Histórico", "Nenhuma compra encontrada para este cliente.", parent=self.master)
            return  # Encerra o método se não houver histórico.

        # Criação de uma nova janela (Toplevel) para exibir o
        #       histórico de compras do cliente.
        # Essa janela é filha da janela principal (`self.master`) e
        #       será exibida como uma janela separada.
        janela_historico = tk.Toplevel(self.master)

        # Define o título da janela com o nome do cliente para
        #       facilitar a identificação.
        # O título é formatado com a string "Histórico de
        #       Compras - " seguida do nome do cliente.
        janela_historico.title(f"Histórico de Compras - {cliente['nome']}")

        # Configura o tamanho da janela, definindo a largura
        #       como 800 pixels e a altura como 600 pixels.
        janela_historico.geometry("800x600")

        # Criação de um frame (container) dentro da nova janela
        #       para organizar os widgets.
        # O frame é criado com um padding de 10 pixels para
        #       adicionar um espaço interno.
        frame_historico = ttk.Frame(janela_historico, padding=10)

        # Adiciona o frame ao layout da nova janela.
        # O método `pack` é usado para preencher todo o espaço
        #       disponível na largura e altura da janela.
        # `fill=tk.BOTH` permite que o frame expanda em ambas as
        #       direções, enquanto `expand=True` garante a expansão dinâmica.
        frame_historico.pack(fill=tk.BOTH,
                             expand=True)

        # Criação de um rótulo (label) para o campo de filtro da coluna "Data".
        # O texto exibido será "Data:", indicando que este campo serve para filtrar pela data.
        # `row=0` posiciona o rótulo na primeira linha da grade (contagem começa em 0).
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `sticky="w"` alinha o rótulo à esquerda dentro da célula da grade.
        ttk.Label(frame_historico,
                  text="Data:").grid(row=0,
                                     column=0,
                                     sticky="w")

        # Criação de um campo de entrada (Entry) para que o usuário
        #       digite o valor a ser filtrado na coluna "Data".
        # Este campo será usado para filtrar registros no
        #       histórico com base na data.
        campo_filtro_data = ttk.Entry(frame_historico)

        # Configuração do layout do campo de entrada na grade.
        # `row=0` posiciona o campo de entrada na mesma linha do rótulo "Data".
        # `column=1` posiciona o campo de entrada na segunda
        #       coluna da grade, ao lado do rótulo.
        # `sticky="we"` faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível na célula.
        campo_filtro_data.grid(row=0,
                               column=1,
                               sticky="we")

        # Criação de um rótulo (label) para o campo de filtro da coluna "Produto".
        # O texto exibido será "Produto:", indicando que este campo
        #       serve para filtrar os registros pelo nome do produto.
        # `row=0` posiciona o rótulo na primeira linha da grade (grid).
        # `column=2` posiciona o rótulo na terceira coluna da grade.
        # `sticky="w"` alinha o rótulo à esquerda dentro da célula da grade.
        ttk.Label(frame_historico,
                  text="Produto:").grid(row=0,
                                        column=2,
                                        sticky="w")

        # Criação de um campo de entrada (Entry) para que o usuário digite o
        #       valor a ser filtrado na coluna "Produto".
        # Este campo será usado para filtrar registros no histórico
        #       com base no nome do produto.
        campo_filtro_produto = ttk.Entry(frame_historico)

        # Configuração do layout do campo de entrada na grade.
        # `row=0` posiciona o campo de entrada na mesma linha do rótulo "Produto".
        # `column=3` posiciona o campo de entrada na quarta coluna da
        #       grade, ao lado do rótulo.
        # `sticky="we"` faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível na célula.
        campo_filtro_produto.grid(row=0,
                                  column=3,
                                  sticky="we")

        # Criação de um rótulo (label) para o campo de filtro da
        #       coluna "Método de Pagamento".
        # O texto exibido será "Método de Pagamento:", indicando que este
        #       campo serve para filtrar os registros pelo método de pagamento utilizado.
        # `row=0` posiciona o rótulo na primeira linha da grade (grid).
        # `column=4` posiciona o rótulo na quinta coluna da grade.
        # `sticky="w"` alinha o rótulo à esquerda dentro da célula da grade.
        ttk.Label(frame_historico,
                  text="Método de Pagamento:").grid(row=0,
                                                    column=4,
                                                    sticky="w")

        # Criação de um campo de entrada (Entry) para que o usuário digite o
        #       valor a ser filtrado na coluna "Método de Pagamento".
        # Este campo será usado para filtrar registros no histórico com base no
        #       método de pagamento (por exemplo: "Cartão", "Dinheiro").
        campo_filtro_metodo = ttk.Entry(frame_historico)

        # Configuração do layout do campo de entrada na grade.
        # `row=0` posiciona o campo de entrada na mesma linha do
        #       rótulo "Método de Pagamento".
        # `column=5` posiciona o campo de entrada na sexta coluna da
        #       grade, ao lado do rótulo.
        # `sticky="we"` faz com que o campo de entrada se expanda
        #       horizontalmente para preencher o espaço disponível na célula.
        campo_filtro_metodo.grid(row=0,
                                 column=5,
                                 sticky="we")

        # Definição das colunas que serão exibidas na tabela.
        # As colunas representam as informações do histórico de compras: data,
        #       produto, método de pagamento, quantidade, preço unitário e total.
        colunas = ["data", "produto", "metodo_pagamento", "quantidade", "preco_unit", "total"]

        # Criação de uma tabela (Treeview) para exibir os registros do histórico de compras.
        # O widget `ttk.Treeview` é configurado com as colunas definidas acima.
        # A opção `show="headings"` exibe apenas os cabeçalhos das colunas,
        #       sem uma coluna adicional para ícones.
        tabela = ttk.Treeview(frame_historico,
                              columns=colunas,
                              show="headings")

        # Configuração da tabela para ocupar o espaço desejado na interface
        #       usando o gerenciador de geometria `grid`.
        # `row=1` posiciona a tabela na segunda linha da grade (abaixo dos campos de filtro).
        # `column=0` posiciona a tabela na primeira coluna.
        # `columnspan=6` faz com que a tabela ocupe seis colunas, alinhando
        #       com os campos de filtro acima.
        # `sticky="nsew"` permite que a tabela se expanda para preencher
        #       horizontalmente e verticalmente o espaço disponível.
        # `pady=10` adiciona 10 pixels de espaço vertical acima e abaixo da tabela.
        tabela.grid(row=1,
                    column=0,
                    columnspan=6,
                    sticky="nsew",
                    pady=10)

        # Configuração dos cabeçalhos das colunas da tabela.
        # Para cada coluna definida na lista `colunas`, é configurado um
        #       cabeçalho com um texto legível.
        # `col.replace("_", " ").capitalize()` substitui underscores (_) por
        #       espaços e coloca a primeira letra em maiúscula.
        for col in colunas:
            tabela.heading(col,
                           text=col.replace("_",
                                            " ").capitalize())

        # Configuração da largura e alinhamento de cada coluna da tabela.
        # `column("data")`: largura de 100 pixels, padrão de alinhamento à esquerda.
        tabela.column("data", width=100)

        # `column("produto")`: largura de 200 pixels, padrão de alinhamento à esquerda.
        tabela.column("produto", width=200)

        # `column("metodo_pagamento")`: largura de 150 pixels, padrão de
        #       alinhamento à esquerda.
        tabela.column("metodo_pagamento", width=150)

        # `column("quantidade")`: largura de 80 pixels, centralizado (`anchor="center"`).
        tabela.column("quantidade", width=80, anchor="center")

        # `column("preco_unit")`: largura de 100 pixels, alinhado à direita (`anchor="e"`).
        tabela.column("preco_unit", width=100, anchor="e")

        # `column("total")`: largura de 120 pixels, alinhado à direita (`anchor="e"`).
        tabela.column("total", width=120, anchor="e")

        # Barra de rolagem
        # Criação de uma barra de rolagem vertical associada à tabela.
        # O parâmetro `orient="vertical"` define a orientação da barra como vertical.
        # O comando `command=tabela.yview` conecta a barra de rolagem ao movimento vertical da tabela.
        scroll = ttk.Scrollbar(frame_historico,
                               orient="vertical",
                               command=tabela.yview)

        # Configuração da tabela para usar a barra de rolagem criada.
        # O parâmetro `yscrollcommand=scroll.set` garante que o movimento da
        #       barra sincronize com o conteúdo da tabela.
        tabela.configure(yscrollcommand=scroll.set)

        # Posicionamento da barra de rolagem no layout usando o
        #       gerenciador de geometria `grid`.
        # `row=1` coloca a barra de rolagem na mesma linha da tabela.
        # `column=6` posiciona a barra de rolagem na sétima coluna, ao
        #       lado direito da tabela.
        # `sticky="ns"` faz com que a barra se estenda de cima para
        #       baixo (norte a sul) dentro da célula.
        scroll.grid(row=1,
                    column=6,
                    sticky="ns")

        # Criação de um rótulo (label) para exibir o total das compras.
        # O texto inicial do rótulo é "Total: R$ 0,00", indicando o
        #       valor inicial como zero.
        # O parâmetro `font=("Arial", 16, "bold")` define a fonte
        #       como Arial, tamanho 16, com estilo negrito.
        label_total = ttk.Label(frame_historico,
                                text="Total: R$ 0,00",
                                font=("Arial", 16, "bold"))

        # Posicionamento do rótulo de total no layout usando o gerenciador de geometria `grid`.
        # `row=2` coloca o rótulo na terceira linha, abaixo da tabela.
        # `column=0` inicia o rótulo na primeira coluna.
        # `columnspan=6` faz com que o rótulo ocupe seis colunas, centralizando-o na interface.
        # `pady=10` adiciona um espaço vertical de 10 pixels acima e abaixo do rótulo.
        label_total.grid(row=2,
                         column=0,
                         columnspan=6,
                         pady=10)

        # Preenchendo a tabela
        # Define a função para atualizar os dados exibidos na tabela.
        def atualizar_tabela():

            # Remove todos os itens existentes na tabela.
            # `tabela.get_children()` retorna os identificadores de todos os
            #       itens, e `tabela.delete()` os remove.
            tabela.delete(*tabela.get_children())

            # Inicializa o total acumulado como zero.
            total = 0

            # Itera sobre cada compra no histórico de compras do cliente.
            for compra in historico:

                # Obtém a data da compra.
                data = compra["data"]

                # Itera sobre cada item na lista de itens comprados.
                for item in compra["itens"]:

                    # Calcula o total para o item atual (quantidade * preço unitário).
                    total_item = item["quantidade"] * item["preco_unit"]

                    # Insere os dados do item na tabela.
                    # `""` indica que o item será inserido na raiz da tabela.
                    # `"end"` adiciona o item no final da lista de itens da tabela.
                    # Os valores inseridos são:
                    # - `data`: Data da compra.
                    # - `item["nome"]`: Nome do produto.
                    # - `compra["metodo_pagamento"]`: Método de pagamento usado na compra.
                    # - `item["quantidade"]`: Quantidade do produto comprado.
                    # - `f"R$ {item['preco_unit']:.2f}"`: Preço unitário formatado
                    #       como moeda com 2 casas decimais.
                    # - `f"R$ {total_item:,.2f}"`: Total do item formatado como
                    #       moeda com separador de milhares.
                    tabela.insert("", "end", values=(
                        data,
                        item["nome"],
                        compra["metodo_pagamento"],
                        item["quantidade"],
                        f"R$ {item['preco_unit']:.2f}",
                        f"R$ {total_item:,.2f}",
                    ))

                    # Adiciona o total do item ao acumulador do total geral.
                    total += total_item

            # Atualiza o texto do rótulo que exibe o total acumulado.
            # O total é formatado como moeda com separador de milhares e 2 casas decimais.
            label_total.config(text=f"Total: R$ {total:,.2f}")

        # Chama a função `atualizar_tabela` para exibir todos os dados iniciais.
        atualizar_tabela()

        # Define a função `filtrar` para aplicar os filtros inseridos pelo usuário.
        def filtrar():

            # Remove todos os itens existentes na tabela antes de exibir
            #       os resultados filtrados.
            tabela.delete(*tabela.get_children())

            # Inicializa a variável para calcular o total filtrado como zero.
            total_filtrado = 0

            # Itera sobre cada compra no histórico de compras.
            for compra in historico:

                # Obtém a data da compra.
                data = compra["data"]

                # Verifica se o campo de filtro de data está preenchido.
                # Se estiver, apenas as compras que contêm o valor digitado
                #       na data serão consideradas.
                if campo_filtro_data.get().strip() and campo_filtro_data.get().strip() not in data:
                    continue

                # Itera sobre os itens comprados dentro de cada compra.
                for item in compra["itens"]:

                    # Verifica se o campo de filtro de produto está preenchido.
                    # Se estiver, apenas os itens cujo nome contém o texto
                    #       digitado (ignorando maiúsculas e minúsculas) serão considerados.
                    if campo_filtro_produto.get().strip() and campo_filtro_produto.get().strip().lower() not in \
                            item[
                                "nome"].lower():
                        continue

                    # Verifica se o campo de filtro de método de pagamento está preenchido.
                    # Se estiver, apenas as compras cujo método de pagamento contém o
                    #       texto digitado (ignorando maiúsculas e minúsculas) serão consideradas.
                    if campo_filtro_metodo.get().strip() and campo_filtro_metodo.get().strip().lower() not in \
                            compra[
                                "metodo_pagamento"].lower():
                        continue

                    # Calcula o total para o item atual (quantidade * preço unitário).
                    total_item = item["quantidade"] * item["preco_unit"]

                    # Insere os dados do item filtrado na tabela.
                    # `""` indica que o item será inserido na raiz da tabela.
                    # `"end"` adiciona o item no final da lista de itens da tabela.
                    # Os valores inseridos são:
                    # - `data`: Data da compra.
                    # - `item["nome"]`: Nome do produto.
                    # - `compra["metodo_pagamento"]`: Método de pagamento usado na compra.
                    # - `item["quantidade"]`: Quantidade do produto comprado.
                    # - `f"R$ {item['preco_unit']:.2f}"`: Preço unitário formatado
                    #       como moeda com 2 casas decimais.
                    # - `f"R$ {total_item:,.2f}"`: Total do item formatado como
                    #       moeda com separador de milhares.
                    tabela.insert("", "end", values=(
                        data,
                        item["nome"],
                        compra["metodo_pagamento"],
                        item["quantidade"],
                        f"R$ {item['preco_unit']:.2f}",
                        f"R$ {total_item:,.2f}",
                    ))

                    # Adiciona o total do item ao acumulador do total filtrado.
                    total_filtrado += total_item

            # Atualiza o texto do rótulo que exibe o total acumulado dos resultados filtrados.
            # O total é formatado como moeda com separador de milhares e 2 casas decimais.
            label_total.config(text=f"Total: R$ {total_filtrado:,.2f}")

        # Eventos para aplicar filtro
        # Associa o evento de pressionar uma tecla (KeyRelease) no campo
        #       de filtro de data à função `filtrar`.
        # Sempre que o usuário digitar ou apagar algo no campo, o
        #       filtro será aplicado automaticamente.
        campo_filtro_data.bind("<KeyRelease>", lambda e: filtrar())

        # Associa o evento de pressionar uma tecla (KeyRelease) no campo de
        #       filtro de produto à função `filtrar`.
        # Isso garante que o filtro seja aplicado imediatamente após
        #       alterações no campo de texto.
        campo_filtro_produto.bind("<KeyRelease>", lambda e: filtrar())

        # Associa o evento de pressionar uma tecla (KeyRelease) no campo de
        #       filtro de método de pagamento à função `filtrar`.
        # Isso permite que o filtro reaja dinamicamente às entradas do usuário.
        campo_filtro_metodo.bind("<KeyRelease>", lambda e: filtrar())

        # Configuração de pesos no gerenciador de layout da grade (grid)
        #       para tornar o layout responsivo.
        # Aqui, a linha 1 (onde a tabela está localizada) é configurada
        #       para expandir com o restante do espaço disponível.
        frame_historico.rowconfigure(1, weight=1)

        # Configuração de peso para a coluna 1 do frame, permitindo que ela
        #       expanda horizontalmente conforme necessário.
        frame_historico.columnconfigure(1, weight=1)

        # Configuração de peso para a coluna 3 do frame, permitindo que
        #       ela expanda horizontalmente de forma proporcional.
        frame_historico.columnconfigure(3, weight=1)

        # Configuração de peso para a coluna 5 do frame, garantindo que
        #       ela também possa expandir horizontalmente.
        frame_historico.columnconfigure(5, weight=1)

        # Inicia o loop principal da janela `janela_historico`, permitindo
        #       que a interface fique responsiva e interativa.
        janela_historico.mainloop()


    # Método para listar todos os clientes na tabela.
    def listar_clientes(self):

        # Itera sobre todos os filhos (linhas) da tabela atual.
        for i in self.tabela.get_children():

            # Remove cada linha da tabela para limpar os dados
            #       existentes antes de adicionar os novos.
            self.tabela.delete(i)

        # Chama a função `obter_clientes` para buscar todos os
        #       clientes do banco de dados.
        clientes = obter_clientes()

        # Itera sobre a lista de clientes retornada pela função.
        for cli in clientes:

            # Insere os dados de cada cliente como uma nova linha na tabela.
            # Os valores exibidos na tabela são: código, nome, CPF/CNPJ,
            #       telefone e endereço do cliente.
            self.tabela.insert(

                "",  # Define o item pai como vazio, indicando que
                # este é um item de nível superior.
                tk.END,  # Adiciona a nova linha no final da tabela.
                values=(  # Define os valores a serem exibidos na linha:
                    cli["codigo"],  # Código do cliente.
                    cli["nome"],  # Nome do cliente.
                    cli["cpf_cnpj"],  # CPF ou CNPJ do cliente.
                    cli["telefone"],  # Telefone do cliente.
                    cli["endereco"]  # Endereço do cliente.
                )

            )

    # Método que limpa todos os campos de entrada da janela de
    #       gerenciamento de clientes.
    def limpar_campos(self):

        # Limpa o campo de entrada para o código do cliente.
        # O método `delete(0, tk.END)` remove todo o texto do
        #       início (`0`) ao fim (`tk.END`) do campo.
        self.campo_codigo.delete(0, tk.END)

        # Limpa o campo de entrada para o nome do cliente.
        # Garantindo que qualquer valor previamente inserido seja removido.
        self.campo_nome.delete(0, tk.END)

        # Limpa o campo de entrada para o CPF/CNPJ do cliente.
        # Deixa o campo pronto para inserir um novo valor.
        self.campo_cpf_cnpj.delete(0, tk.END)

        # Limpa o campo de entrada para o telefone do cliente.
        # Este método é usado para redefinir o estado inicial do campo.
        self.campo_telefone.delete(0, tk.END)

        # Limpa o campo de entrada para o endereço do cliente.
        # Remove qualquer dado que possa estar preenchido neste campo.
        self.campo_endereco.delete(0, tk.END)


############################################
# Janela Fornecedores
############################################

# Esta classe 'JanelaFornecedores' é responsável por criar uma
#       interface gráfica para gerenciar fornecedores.
# Ela herda características de 'JanelaBase', uma classe que já
#       define elementos comuns de uma janela.
class JanelaFornecedores(JanelaBase):

    # Método construtor, chamado automaticamente quando uma
    #       instância desta classe é criada.
    def __init__(self, master):

        # 'super()' é usado para chamar o método __init__ da classe pai,
        #       'JanelaBase', que configura a janela.
        # Isso inclui definir o título da janela para "Gerenciamento de Fornecedores".
        super().__init__(master, "Gerenciamento de Fornecedores")

        # 'ttk.Frame' cria um contêiner dentro da janela onde outros
        #       elementos (como botões, textos) podem ser adicionados.
        # 'padding="10"' adiciona um espaço de 10 pixels em todas as direções
        #       dentro do frame, entre a borda e os elementos internos.
        self.frame = ttk.Frame(self.master, padding="10")

        # 'pack' é um gerenciador de geometria que define como o frame se ajusta na janela.
        # 'fill=tk.BOTH' faz com que o frame expanda tanto na vertical quanto na horizontal.
        # 'expand=True' permite que o frame se ajuste à medida que a janela é redimensionada.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Cria um rótulo (texto estático) no frame que serve como etiqueta
        #       para o campo de entrada do nome do fornecedor.
        # 'text="Nome do Fornecedor:"' define o texto que aparece no rótulo.
        # 'grid' é outro gerenciador de geometria que coloca o rótulo em uma grade dentro do frame.
        # 'row=0, column=0' posiciona o rótulo na primeira linha e coluna da grade.
        # 'sticky="w"' faz com que o rótulo alinhe à esquerda dentro do espaço alocado para ele.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        ttk.Label(self.frame,
                  text="Nome do Fornecedor:").grid(row=0,
                                                   column=0,
                                                   sticky="w",
                                                   pady=5)

        # Cria um campo de entrada onde os usuários podem digitar o nome do fornecedor.
        self.campo_nome = ttk.Entry(self.frame)

        # 'grid' posiciona o campo de entrada na grade, diretamente ao
        #       lado do rótulo do nome do fornecedor.
        # 'column=1' coloca o campo na segunda coluna (ao lado do rótulo).
        # 'sticky="we"' faz com que o campo de entrada expanda para preencher
        #       horizontalmente o espaço disponível na célula da grade.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        self.campo_nome.grid(row=0,
                             column=1,
                             sticky="we",
                             pady=5)

        # Cria um rótulo (Label) para o campo 'Endereço' dentro do frame.
        # 'text="Endereço:"' define o texto exibido no rótulo para orientar o
        #       usuário a inserir o endereço do fornecedor.
        ttk.Label(self.frame,
                  text="Endereço:").grid(row=1,
                                         column=0,
                                         sticky="w",
                                         pady=5)
        # ↑ Usamos ttk.Label para criar o rótulo e o método .grid para posicioná-lo no grid do frame.
        # ↑ 'row=1' coloca o rótulo na segunda linha do grid (a contagem de linhas começa em 0).
        # ↑ 'column=0' coloca o rótulo na primeira coluna do grid.
        # ↑ 'sticky="w"' alinha o rótulo à esquerda da célula grid.
        # ↑ 'pady=5' adiciona um espaçamento vertical de 5 pixels acima e abaixo do rótulo.

        # Cria um campo de entrada (Entry) para o endereço do fornecedor.
        self.campo_endereco = ttk.Entry(self.frame)
        # ↑ ttk.Entry é usado para criar uma caixa de texto onde o
        #       usuário pode digitar o endereço.

        # Posiciona o campo de entrada para endereço no layout,
        #       definindo sua localização e comportamento.
        self.campo_endereco.grid(row=1,
                                 column=1,
                                 sticky="we",
                                 pady=5)
        # ↑ 'row=1' posiciona o campo de entrada na mesma linha do rótulo de endereço.
        # ↑ 'column=1' coloca o campo de entrada na segunda coluna, ao lado do rótulo.
        # ↑ 'sticky="we"' faz com que o campo de entrada expanda para
        #       preencher a largura da célula no grid.
        # ↑ 'pady=5' adiciona um espaçamento vertical de 5 pixels acima e
        #       abaixo do campo de entrada.

        # Cria um rótulo para o campo 'Telefone' no frame.
        # 'text="Telefone:"' especifica o texto do rótulo para guiar o
        #       usuário a inserir o telefone do fornecedor.
        ttk.Label(self.frame,
                  text="Telefone:").grid(row=2,
                                         column=0,
                                         sticky="w",
                                         pady=5)
        # ↑ Posiciona o rótulo para o telefone na terceira linha e na
        #       primeira coluna, alinhado à esquerda.

        # Cria um campo de entrada para o telefone do fornecedor.
        self.campo_telefone = ttk.Entry(self.frame)
        # ↑ Uma nova caixa de texto para inserção do número de telefone.

        # Configura a posição e o comportamento do campo de telefone na interface.
        self.campo_telefone.grid(row=2,
                                 column=1,
                                 sticky="we",
                                 pady=5)
        # ↑ 'row=2' posiciona o campo na terceira linha do grid, abaixo do campo de endereço.
        # ↑ 'column=1' alinha este campo com o campo de endereço, na segunda coluna.
        # ↑ 'sticky="we"' permite que o campo de entrada se expanda horizontalmente.
        # ↑ 'pady=5' mantém o espaçamento vertical consistente com outros campos.

        # Cria um botão para a ação de cadastrar um fornecedor.
        # 'self.frame' indica que o botão será colocado dentro do frame já definido.
        # 'text="Cadastrar"' define o texto que aparece no botão.
        # 'command=self.cadastrar_fornecedor' associa este botão à função
        #       que executa a ação de cadastrar um fornecedor.
        self.botao_cadastrar = ttk.Button(self.frame,
                                          text="Cadastrar",
                                          command=self.cadastrar_fornecedor)

        # Posiciona o botão 'Cadastrar' no grid (grade de layout).
        # 'row=3' coloca o botão na quarta linha do grid (contagem começa em 0).
        # 'column=0' coloca o botão na primeira coluna.
        # 'pady=10' adiciona 10 pixels de espaço vertical acima e abaixo do
        #       botão para separação visual.
        self.botao_cadastrar.grid(row=3,
                                  column=0,
                                  pady=10)

        # Cria um botão para a ação de editar um fornecedor.
        # 'self.frame' indica que o botão será colocado dentro do frame já definido.
        # 'text="Editar"' define o texto que aparece no botão.
        # 'command=self.editar_fornecedor' associa este botão à função que
        #       executa a ação de editar um fornecedor.
        self.botao_editar = ttk.Button(self.frame,
                                       text="Editar",
                                       command=self.editar_fornecedor)

        # Posiciona o botão 'Editar' no grid.
        # 'row=3' coloca o botão na quarta linha.
        # 'column=1' coloca o botão na segunda coluna.
        # 'pady=10' adiciona 10 pixels de espaço vertical acima e abaixo do
        #       botão para separação visual.
        self.botao_editar.grid(row=3,
                               column=1,
                               pady=10)

        # Cria um botão para a ação de remover um fornecedor.
        # 'self.frame' indica que o botão será colocado dentro do frame já definido.
        # 'text="Remover"' define o texto que aparece no botão.
        # 'command=self.remover_fornecedor_cmd' associa este botão à função
        #       que executa a ação de remover um fornecedor.
        self.botao_remover = ttk.Button(self.frame,
                                        text="Remover",
                                        command=self.remover_fornecedor_cmd)

        # Posiciona o botão 'Remover' no grid.
        # 'row=4' coloca o botão na quinta linha.
        # 'column=0' coloca o botão na primeira coluna.
        # 'pady=10' adiciona 10 pixels de espaço vertical acima e abaixo do
        #       botão para separação visual.
        self.botao_remover.grid(row=4,
                                column=0,
                                pady=10)


        # Cria uma tabela (Treeview) para exibir os dados dos fornecedores.
        # 'self.frame' indica que a tabela será colocada dentro do frame já definido.
        # 'columns=("nome", "endereco", "telefone")' define as colunas da
        #       tabela com seus identificadores.
        # 'show="headings"' configura a tabela para mostrar apenas os cabeçalhos das
        #       colunas, sem exibir a coluna da árvore padrão.
        self.tabela = ttk.Treeview(
            self.frame,
            columns=("nome", "endereco", "telefone"),
            show="headings"
        )

        # Configura o cabeçalho da coluna "nome" e o texto que será
        #       exibido nesse cabeçalho.
        self.tabela.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna "endereco" e o texto que será
        #       exibido nesse cabeçalho.
        self.tabela.heading("endereco", text="Endereço")

        # Configura o cabeçalho da coluna "telefone" e o texto que
        #       será exibido nesse cabeçalho.
        self.tabela.heading("telefone", text="Telefone")

        # Posiciona a tabela na interface usando o gerenciador de geometria 'grid'.
        # 'row=5' coloca a tabela na sexta linha.
        # 'column=0' inicia a tabela na primeira coluna.
        # 'columnspan=2' faz com que a tabela se estenda por duas colunas.
        # 'sticky="nsew"' faz com que a tabela expanda para preencher o
        #       espaço disponível em todas as direções (norte, sul, leste, oeste).
        # 'pady=10' adiciona 10 pixels de espaço vertical acima e abaixo
        #       da tabela para separação visual.
        self.tabela.grid(row=5,
                         column=0,
                         columnspan=2,
                         sticky="nsew",
                         pady=10)

        # Configura a linha 5 do frame para que ela expanda e acomode dinamicamente o
        #       tamanho da tabela conforme a janela é redimensionada.
        self.frame.rowconfigure(5, weight=1)

        # Configura a segunda coluna do frame para que ela expanda, permitindo que a
        #       tabela ocupe mais espaço horizontalmente conforme a janela é redimensionada.
        self.frame.columnconfigure(1, weight=1)

        # Associa um evento à tabela que será acionado quando um item é selecionado.
        # '<<TreeviewSelect>>' é o evento que é disparado quando a seleção da tabela muda.
        # 'self.selecionar_item' é a função que será chamada quando o evento ocorrer.
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar_item)

        # Chama a função 'listar_fornecedores' que preenche a
        #       tabela com os dados dos fornecedores.
        self.listar_fornecedores()


    # Define a função 'cadastrar_fornecedor' para o objeto atual.
    def cadastrar_fornecedor(self):

        # Obtém o valor do campo de nome, remove espaços em branco
        #       extras com 'strip()'.
        nome = self.campo_nome.get().strip()

        # Obtém o valor do campo de endereço, remove espaços em
        #       branco extras com 'strip()'.
        endereco = self.campo_endereco.get().strip()

        # Obtém o valor do campo de telefone, remove espaços em
        #       branco extras com 'strip()'.
        telefone = self.campo_telefone.get().strip()

        # Verifica se o campo 'nome' foi preenchido.
        if nome:

            # Chama a função 'cadastrar_fornecedor' definida globalmente
            #       para registrar os dados.
            cadastrar_fornecedor(nome, endereco, telefone)

            # Exibe uma caixa de mensagem informando que o cadastro foi um sucesso.
            messagebox.showinfo("Sucesso",
                                "Fornecedor cadastrado.",
                                parent=self.master)

            # Atualiza a lista de fornecedores para refletir o novo cadastro.
            self.listar_fornecedores()

            # Limpa os campos de entrada após o cadastro ser concluído.
            self.limpar_campos()

        else:

            # Se o campo 'nome' não estiver preenchido, exibe uma mensagem de erro.
            messagebox.showerror("Erro",
                                 "O campo Nome do fornecedor é obrigatório.",
                                 parent=self.master)

    # Define a função 'editar_fornecedor' para o objeto atual.
    def editar_fornecedor(self):

        # Obtém a seleção atual na tabela de fornecedores.
        selecao = self.tabela.selection()

        # Verifica se algum fornecedor foi selecionado.
        if not selecao:

            # Exibe uma mensagem de erro se nenhum fornecedor for selecionado.
            messagebox.showerror("Erro",
                                 "Selecione um fornecedor para editar.",
                                 parent=self.master)

            return

        # Obtém o novo nome do campo de entrada, removendo espaços extras.
        nome_novo = self.campo_nome.get().strip()

        # Obtém o novo endereço do campo de entrada, removendo espaços extras.
        endereco_novo = self.campo_endereco.get().strip()

        # Obtém o novo telefone do campo de entrada, removendo espaços extras.
        telefone_novo = self.campo_telefone.get().strip()

        # Verifica se o campo de nome novo está preenchido.
        if not nome_novo:

            # Exibe uma mensagem de erro se o campo de nome novo estiver vazio.
            messagebox.showerror("Erro",
                                 "O campo Nome é obrigatório.",
                                 parent=self.master)
            return

        # Obtém o item selecionado na tabela.
        item = self.tabela.item(selecao[0])

        # Extrai o nome antigo do fornecedor do item selecionado.
        nome_antigo = item["values"][0]

        # Chama a função global 'editar_fornecedor' para atualizar os dados no banco.
        editar_fornecedor(nome_antigo, nome_novo, endereco_novo, telefone_novo)

        # Exibe uma mensagem de sucesso após a edição.
        messagebox.showinfo("Sucesso", "Fornecedor editado.", parent=self.master)

        # Atualiza a lista de fornecedores na interface.
        self.listar_fornecedores()

        # Limpa os campos de entrada após a edição.
        self.limpar_campos()


    # Define a função 'remover_fornecedor_cmd' para o objeto atual.
    def remover_fornecedor_cmd(self):

        # Obtém a seleção atual na tabela de fornecedores.
        selecao = self.tabela.selection()

        # Verifica se algum fornecedor foi selecionado.
        if not selecao:

            # Exibe uma mensagem de erro se nenhum fornecedor for selecionado.
            messagebox.showerror("Erro",
                                 "Selecione um fornecedor para remover.",
                                 parent=self.master)
            return

        # Obtém o item selecionado na tabela.
        item = self.tabela.item(selecao[0])

        # Extrai o nome do fornecedor do item selecionado.
        nome = item["values"][0]

        # Pede confirmação do usuário antes de remover o fornecedor.
        confirmacao = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja remover o fornecedor '{nome}'?",
            parent=self.master
        )

        # Verifica se o usuário confirmou a remoção.
        if confirmacao:

            # Chama a função global 'remover_fornecedor' para
            #       remover os dados no banco.
            remover_fornecedor(nome)

            # Exibe uma mensagem de sucesso após a remoção.
            messagebox.showinfo("Sucesso",
                                "Fornecedor removido.",
                                parent=self.master)

            # Atualiza a lista de fornecedores na interface.
            self.listar_fornecedores()

            # Limpa os campos de entrada após a remoção.
            self.limpar_campos()


    # Define a função 'listar_fornecedores' para o objeto atual.
    def listar_fornecedores(self):

        # Itera sobre todos os itens (filhos) presentes na tabela de fornecedores.
        for i in self.tabela.get_children():

            # Remove cada item da tabela, limpando todos os dados visuais existentes.
            self.tabela.delete(i)

        # Chama a função global 'obter_fornecedores' que busca os
        #       fornecedores do banco de dados.
        fornecedores = obter_fornecedores()

        # Itera sobre a lista de fornecedores obtida.
        for f in fornecedores:

            # Obtém o endereço do fornecedor, retorna uma string vazia
            #       se não estiver disponível.
            endereco = f.get("endereco", "")

            # Obtém o telefone do fornecedor, retorna uma string
            #       vazia se não estiver disponível.
            telefone = f.get("telefone", "")

            # Insere um novo item na tabela com os dados do fornecedor.
            self.tabela.insert("",
                               tk.END,
                               values=(f["nome"], endereco, telefone))

    # Define a função 'selecionar_item' que é acionada quando um
    #       item é selecionado na tabela.
    def selecionar_item(self, event):

        # Itera sobre os itens selecionados na tabela.
        for sel in self.tabela.selection():

            # Obtém o item atual com base na seleção.
            item = self.tabela.item(sel)

            # Extrai os valores associados ao item selecionado.
            valores = item["values"]

            # Limpa o conteúdo atual do campo de entrada para o nome do fornecedor.
            self.campo_nome.delete(0, tk.END)

            # Insere o nome do fornecedor no campo de entrada correspondente.
            self.campo_nome.insert(0, valores[0])

            # Limpa o conteúdo atual do campo de entrada para o endereço do fornecedor.
            self.campo_endereco.delete(0, tk.END)

            # Insere o endereço do fornecedor no campo de entrada correspondente.
            self.campo_endereco.insert(0, valores[1])

            # Limpa o conteúdo atual do campo de entrada para o telefone do fornecedor.
            self.campo_telefone.delete(0, tk.END)

            # Insere o telefone do fornecedor no campo de entrada correspondente.
            self.campo_telefone.insert(0, valores[2])


    # Define a função 'limpar_campos' que limpa os campos de
    #       entrada na interface do usuário.
    def limpar_campos(self):

        # Limpa o conteúdo do campo de entrada para o nome do fornecedor.
        self.campo_nome.delete(0, tk.END)

        # Limpa o conteúdo do campo de entrada para o endereço do fornecedor.
        self.campo_endereco.delete(0, tk.END)

        # Limpa o conteúdo do campo de entrada para o telefone do fornecedor.
        self.campo_telefone.delete(0, tk.END)


############################################
# Janela Estoque (Produtos Baixo Estoque e Vencidos)
############################################

# A classe JanelaEstoque é uma extensão da classe JanelaBase, o que
#       significa que ela herda todas as propriedades e métodos de JanelaBase.
class JanelaEstoque(JanelaBase):

    # A função __init__ é um método especial chamado de construtor,
    #       que é chamado automaticamente quando uma nova
    #       instância desta classe é criada.
    def __init__(self, master):

        # A palavra 'super' é usada para chamar o construtor da classe pai,
        #       neste caso, JanelaBase. Isso é necessário para inicializar a
        #       classe pai corretamente.
        # 'master' refere-se ao widget pai no qual esta janela será construída,
        #       tipicamente é uma janela Tk principal ou outra janela de nível superior.
        # "Gerenciamento de Estoque" é o título que será exibido na barra de título da janela.
        super().__init__(master, "Gerenciamento de Estoque")

        # Cria um frame (quadro) dentro da janela principal. Um frame é um
        #       contêiner que pode armazenar outros widgets.
        # 'padding="10"' adiciona uma margem interna de 10 pixels para
        #       separar os elementos internos das bordas do frame.
        self.frame = ttk.Frame(self.master, padding="10")

        # Faz com que o frame preencha todo o espaço disponível na
        #       janela tanto na largura (BOTH) quanto na altura.
        # 'expand=True' faz com que o frame expanda para preencher qualquer
        #       espaço extra na janela principal.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Cria um Notebook dentro do frame. Um Notebook é um widget que
        #       permite a criação de abas para organização do conteúdo.
        self.notebook = ttk.Notebook(self.frame)

        # Configura o notebook para preencher completamente o espaço
        #       disponível no frame que o contém.
        # Isso significa que o notebook se ajustará ao tamanho do
        #       frame principal quando este for redimensionado.
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Cria outro frame que será usado como uma das abas dentro do notebook.
        # Este frame específico será usado para listar produtos
        #       que estão com o estoque baixo.
        self.frame_baixo = ttk.Frame(self.notebook)

        # Adiciona o frame criado para a aba 'Estoque Baixo' ao notebook.
        # 'text="Estoque Baixo"' é o título da aba que aparecerá na
        #       interface do usuário.
        self.notebook.add(self.frame_baixo, text="Estoque Baixo")

        # Cria uma tabela (Treeview) no frame designado para a aba de "Estoque Baixo".
        # 'columns=("codigo","nome","quantidade")' define as colunas da
        #       tabela com os identificadores especificados.
        self.tabela_baixo = ttk.Treeview(self.frame_baixo,
                                         columns=("codigo", "nome", "quantidade"),
                                         show="headings")

        # Configura o cabeçalho da coluna "codigo" com o texto "Código".
        # 'heading("codigo", text="Código")' especifica o título do
        #       cabeçalho para a coluna de código.
        self.tabela_baixo.heading("codigo", text="Código")

        # Configura o cabeçalho da coluna "nome" com o texto "Nome".
        # Isso define o que será exibido como o título para a coluna que
        #       mostra os nomes dos itens no estoque.
        self.tabela_baixo.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna "quantidade" com o texto "Quantidade".
        # Esta configuração destina-se a exibir a quantidade de itens em
        #       estoque para cada entrada listada.
        self.tabela_baixo.heading("quantidade", text="Quantidade")

        # 'pack(fill=tk.BOTH, expand=True)' diz ao gestor de geometria "pack"
        #       para expandir o widget para preencher todo o espaço disponível.
        # 'tk.BOTH' indica que o widget deve expandir tanto
        #       verticalmente quanto horizontalmente.
        self.tabela_baixo.pack(fill=tk.BOTH,
                               expand=True)

        # Aba Vencidos
        # Cria um frame para a aba "Produtos Vencidos" dentro do notebook.
        # Este frame servirá como container para os elementos que
        #       mostram produtos vencidos.
        self.frame_vencidos = ttk.Frame(self.notebook)

        # Adiciona o frame recém-criado ao notebook e define o título
        #       da aba como "Produtos Vencidos".
        self.notebook.add(self.frame_vencidos,
                          text="Produtos Vencidos")

        # Cria uma tabela (Treeview) dentro do frame destinado aos produtos vencidos.
        # 'columns=("codigo","nome","validade","quantidade")'
        #       especifica as colunas da tabela.
        self.tabela_vencidos = ttk.Treeview(self.frame_vencidos,
                                            columns=("codigo", "nome", "validade", "quantidade"),
                                            show="headings")

        # Configura o cabeçalho da coluna "codigo" com o texto "Código",
        #       que exibirá os códigos dos produtos.
        self.tabela_vencidos.heading("codigo", text="Código")

        # Configura o cabeçalho da coluna "nome" com o texto "Nome",
        #       destinado a mostrar os nomes dos produtos vencidos.
        self.tabela_vencidos.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna "validade" com o texto "Validade",
        #       para exibir a data de validade dos produtos.
        self.tabela_vencidos.heading("validade", text="Validade")

        # Configura o cabeçalho da coluna "quantidade" com o texto "Quantidade",
        #       que mostrará a quantidade dos produtos vencidos em estoque.
        self.tabela_vencidos.heading("quantidade", text="Quantidade")

        # Empacota a tabela dentro do frame, configurando-a para preencher
        #   todo o espaço disponível tanto horizontal quanto verticalmente.
        # 'fill=tk.BOTH' faz com que a tabela se expanda em ambas as
        #       direções e 'expand=True' permite que a tabela aproveite
        #       todo o espaço extra disponível.
        self.tabela_vencidos.pack(fill=tk.BOTH,
                                  expand=True)

        # Cria um frame para a aba "Todos os Produtos" dentro do notebook.
        # Este frame servirá como container para os elementos que
        #       mostram todos os produtos em estoque.
        self.frame_todos = ttk.Frame(self.notebook)

        # Adiciona o frame recém-criado ao notebook com a
        #       etiqueta "Todos os Produtos".
        # Isso cria uma nova aba no notebook.
        self.notebook.add(self.frame_todos,
                          text="Todos os Produtos")

        # Cria uma tabela (Treeview) dentro do frame destinado a mostrar todos os produtos.
        # As colunas são definidas para mostrar informações detalhadas de cada produto.
        self.tabela_todos = ttk.Treeview(self.frame_todos,
                                         columns=("codigo", "nome", "categoria", "quantidade", "preco", "fornecedor", "validade", "unidade"),
                                         show="headings")

        # Configura os cabeçalhos das colunas da tabela para
        #       cada atributo do produto.
        # O loop percorre cada coluna definida, configurando o
        #       cabeçalho para ter a primeira letra em maiúscula (capitalize()).
        for col in ("codigo", "nome", "categoria", "quantidade", "preco", "fornecedor", "validade", "unidade"):
            self.tabela_todos.heading(col, text=col.capitalize())

        # Empacota a tabela dentro do frame. A configuração 'fill=tk.BOTH' e 'expand=True'
        #       faz com que a tabela expanda para preencher todo o
        #       espaço disponível no frame, tanto horizontal quanto verticalmente.
        self.tabela_todos.pack(fill=tk.BOTH, expand=True)

        # Chamada de método para atualizar as listas de produtos exibidas nas tabelas.
        # Este método consulta o banco de dados ou uma fonte de
        #       dados para obter informações atualizadas
        #       e exibir na interface.
        self.atualizar_listas()


    def atualizar_listas(self):

        # Este loop remove todos os itens da tabela 'Estoque Baixo'.
        # Utiliza 'get_children()' para obter uma lista de todos os
        #       identificadores das linhas presentes na tabela.
        for i in self.tabela_baixo.get_children():

            # Remove cada item identificado por 'i' da tabela para
            #       garantir que ela esteja vazia antes da atualização.
            self.tabela_baixo.delete(i)

        # Este loop remove todos os itens da tabela 'Produtos Vencidos'.
        # Como no loop anterior, 'get_children()' é usado para
        #       encontrar todos os itens na tabela.
        for i in self.tabela_vencidos.get_children():

            # Cada item é removido pela chamada de 'delete(i)', preparando a
            #       tabela para receber novos dados atualizados.
            self.tabela_vencidos.delete(i)

        # Este loop limpa todos os itens da tabela 'Todos os Produtos'.
        # A função 'get_children()' retorna uma lista de todos os
        #       itens que serão removidos.
        for i in self.tabela_todos.get_children():

            # 'delete(i)' é chamado para cada item na tabela, garantindo que
            #       nenhum dado antigo permaneça antes da atualização.
            self.tabela_todos.delete(i)

        # A função 'obter_estoque_baixo' é chamada com o parâmetro 5, o que
        #       significa que ela retornará todos os produtos
        #       cuja quantidade em estoque é inferior a 5 unidades.
        # Este valor é armazenado na variável 'baixo'.
        baixo = obter_estoque_baixo(5)

        # Este loop percorre cada produto na lista 'baixo'. Cada produto 'p' na
        #       lista tem detalhes como código, nome e quantidade.
        for p in baixo:

            # Para cada produto com estoque baixo, este comando insere uma
            #       nova linha na tabela 'Estoque Baixo'.
            # As informações inseridas na tabela são o 'código', 'nome' e
            #       'quantidade' de cada produto,
            #       ajudando na visualização rápida do estoque que
            #       necessita de atenção.
            self.tabela_baixo.insert("",
                                     tk.END,
                                     values=(p["codigo"], p["nome"], p["quantidade"]))

        # Consulta todos os produtos que estão vencidos utilizando a
        #       função 'obter_produtos_vencidos'.
        # Esta função retorna uma lista de produtos cuja
        #       data de validade já passou.
        vencidos = obter_produtos_vencidos()

        # Este loop itera sobre cada produto 'p' na lista de produtos vencidos.
        for p in vencidos:

            # Insere cada produto vencido na tabela 'Produtos Vencidos'.
            # A linha inserida inclui o código, nome,
            #       validade e quantidade do produto, permitindo uma visualização
            #       clara dos itens que precisam ser retirados do estoque.
            self.tabela_vencidos.insert("",
                                        tk.END,
                                        values=(p["codigo"], p["nome"], p["validade"], p["quantidade"]))

        # Consulta todos os produtos em estoque utilizando a função 'obter_produtos'.
        # Esta função retorna uma lista com todos os produtos disponíveis no inventário.
        todos = obter_produtos()

        # Este loop itera sobre cada produto 'p' na lista de todos os produtos.
        for p in todos:

            # Insere cada produto na tabela 'Todos os Produtos'. A linha inserida
            #       inclui o código, nome, categoria, quantidade, preço, fornecedor,
            #       validade e unidade de cada produto, oferecendo uma
            #       visão completa do inventário.
            self.tabela_todos.insert("",
                                     tk.END,
                                     values=( p["codigo"], p["nome"], p["categoria"],
                                              p["quantidade"], p["preco"], p["fornecedor"],
                                              p["validade"], p["unidade"]))



############################################
# Janela Relatórios
############################################

# Define a classe JanelaRelatorios, que herda funcionalidades de JanelaBase.
# Esta classe cria a interface gráfica para exibir relatórios de vendas.
class JanelaRelatorios(JanelaBase):

    # Método construtor da classe. É chamado automaticamente
    #       quando a classe é instanciada.
    # O parâmetro `master` é a janela principal ou o container no
    #       qual esta janela será inserida.
    def __init__(self, master):

        # Chama o método construtor da classe base `JanelaBase` para inicializar a janela.
        # Configura o título da janela como "Relatórios de Vendas".
        super().__init__(master, "Relatórios de Vendas")

        # Criação de um frame principal
        # Cria um widget do tipo `Frame` para agrupar e organizar outros
        #       componentes da interface gráfica.
        # O parâmetro `padding="10"` adiciona um espaçamento de 10 pixels
        #       em todos os lados do frame.
        # `self.master` define que o frame será inserido na janela principal.
        self.frame = ttk.Frame(self.master,
                               padding="10")

        # Posiciona o frame dentro da janela principal usando o método `pack`.
        # `fill=tk.BOTH` permite que o frame expanda para preencher todo o
        #       espaço disponível, tanto na horizontal quanto na vertical.
        # `expand=True` garante que o frame será redimensionado automaticamente
        #       se a janela for redimensionada.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Filtros
        # Cria um rótulo (label) com o texto "Filtrar por:" dentro do frame principal.
        # Este rótulo indica que a seção abaixo permitirá aplicar filtros nos relatórios.
        # 'row=0' posiciona o rótulo na primeira linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        # 'sticky="w"' alinha o texto à esquerda dentro da célula do grid.
        ttk.Label(self.frame,
                  text="Filtrar por:").grid(row=0,
                                            column=0,
                                            pady=5,
                                            sticky="w")

        # Cria outro rótulo (label) com o texto "Data Inicial (dd/mm/aaaa):"
        #       dentro do frame principal.
        # Este rótulo serve para identificar o campo onde o usuário pode
        #       inserir a data inicial do filtro.
        # 'row=1' posiciona o rótulo na segunda linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna do grid, alinhado
        #       verticalmente com o rótulo anterior.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        # 'sticky="w"' alinha o texto à esquerda dentro da célula do grid.
        ttk.Label(self.frame,
                  text="Data Inicial (dd/mm/aaaa):").grid(row=1,
                                                          column=0,
                                                          pady=5,
                                                          sticky="w")

        # Cria um campo de entrada (Entry) onde o usuário pode
        #       digitar a data inicial do filtro.
        # Este campo é armazenado na variável 'self.campo_data_inicial'
        #       para permitir acesso posterior.
        self.campo_data_inicial = ttk.Entry(self.frame)

        # Posiciona o campo de entrada na interface utilizando o gerenciador de layout 'grid'.
        # 'row=1' posiciona o campo na mesma linha do rótulo "Data Inicial".
        # 'column=1' posiciona o campo na segunda coluna, ao lado do rótulo correspondente.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        # 'sticky="we"' faz com que o campo de entrada se expanda para
        #       preencher o espaço disponível na horizontal.
        self.campo_data_inicial.grid(row=1,
                                     column=1,
                                     pady=5,
                                     sticky="we")

        # Cria um rótulo (label) com o texto "Data Final (dd/mm/aaaa):"
        #       dentro do frame principal.
        # Este rótulo serve para indicar ao usuário onde inserir a data
        #       final para o filtro dos relatórios.
        # 'row=2' posiciona o rótulo na terceira linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        # 'sticky="w"' alinha o texto à esquerda dentro da célula do grid.
        ttk.Label(self.frame,
                  text="Data Final (dd/mm/aaaa):").grid(row=2,
                                                        column=0,
                                                        pady=5,
                                                        sticky="w")

        # Cria um campo de entrada (Entry) onde o usuário pode
        #       digitar a data final do filtro.
        # Este campo é armazenado na variável 'self.campo_data_final'
        #       para ser utilizado posteriormente.
        self.campo_data_final = ttk.Entry(self.frame)

        # Posiciona o campo de entrada na interface utilizando o gerenciador de layout 'grid'.
        # 'row=2' posiciona o campo na mesma linha do rótulo "Data Final".
        # 'column=1' posiciona o campo na segunda coluna do grid, ao lado do rótulo correspondente.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        # 'sticky="we"' faz com que o campo de entrada se expanda para
        #       preencher o espaço horizontal disponível dentro da célula.
        self.campo_data_final.grid(row=2,
                                   column=1,
                                   pady=5,
                                   sticky="we")

        # Cria um rótulo (label) com o texto "Produto:" dentro do frame principal.
        # Este rótulo serve para indicar ao usuário onde inserir o nome
        #       do produto para o filtro dos relatórios.
        # 'row=3' posiciona o rótulo na quarta linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        # 'sticky="w"' alinha o texto à esquerda dentro da célula do grid.
        ttk.Label(self.frame,
                  text="Produto:").grid(row=3,
                                        column=0,
                                        pady=5,
                                        sticky="w")

        # Cria um campo de entrada (Entry) onde o usuário pode
        #       digitar o nome do produto para o filtro.
        # Este campo é armazenado na variável 'self.campo_produto'
        #       para ser utilizado posteriormente.
        self.campo_produto = ttk.Entry(self.frame)

        # Posiciona o campo de entrada na interface utilizando o
        #       gerenciador de layout 'grid'.
        # 'row=3' posiciona o campo na mesma linha do rótulo "Produto".
        # 'column=1' posiciona o campo na segunda coluna do grid, ao
        #       lado do rótulo correspondente.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e
        #       abaixo do campo de entrada.
        # 'sticky="we"' faz com que o campo de entrada se expanda para
        #       preencher o espaço horizontal disponível dentro da célula.
        self.campo_produto.grid(row=3,
                                column=1,
                                pady=5,
                                sticky="we")

        # Cria um rótulo (label) com o texto "Fornecedor:" dentro do frame principal.
        # Este rótulo serve para indicar ao usuário onde inserir o nome do
        #       fornecedor para o filtro dos relatórios.
        # 'row=4' posiciona o rótulo na quinta linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        # 'sticky="w"' alinha o texto à esquerda dentro da célula do grid.
        ttk.Label(self.frame,
                  text="Fornecedor:").grid(row=4,
                                           column=0,
                                           pady=5,
                                           sticky="w")

        # Cria um campo de entrada (Entry) onde o usuário pode digitar o
        #       nome do fornecedor para o filtro.
        # Este campo é armazenado na variável 'self.campo_fornecedor'
        #       para ser utilizado posteriormente.
        self.campo_fornecedor = ttk.Entry(self.frame)

        # Posiciona o campo de entrada na interface utilizando o gerenciador de layout 'grid'.
        # 'row=4' posiciona o campo na mesma linha do rótulo "Fornecedor".
        # 'column=1' posiciona o campo na segunda coluna do grid, ao
        #       lado do rótulo correspondente.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        # 'sticky="we"' faz com que o campo de entrada se expanda para
        #       preencher o espaço horizontal disponível dentro da célula.
        self.campo_fornecedor.grid(row=4,
                                   column=1,
                                   pady=5,
                                   sticky="we")

        # Cria um rótulo (label) com o texto "Método de Pagamento:" dentro do frame principal.
        # Este rótulo serve para indicar ao usuário onde inserir o método de
        #       pagamento para o filtro dos relatórios.
        # 'row=5' posiciona o rótulo na sexta linha do grid.
        # 'column=0' posiciona o rótulo na primeira coluna do grid.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do rótulo.
        # 'sticky="w"' alinha o texto à esquerda dentro da célula do grid.
        ttk.Label(self.frame,
                  text="Método de Pagamento:").grid(row=5,
                                                    column=0,
                                                    pady=5,
                                                    sticky="w")

        # Cria um campo de entrada (Entry) onde o usuário pode digitar o
        #       método de pagamento para o filtro.
        # Este campo é armazenado na variável 'self.campo_metodo' para
        #       ser utilizado posteriormente.
        self.campo_metodo = ttk.Entry(self.frame)

        # Posiciona o campo de entrada na interface utilizando o gerenciador de layout 'grid'.
        # 'row=5' posiciona o campo na mesma linha do rótulo "Método de Pagamento".
        # 'column=1' posiciona o campo na segunda coluna do grid, ao lado do rótulo correspondente.
        # 'pady=5' adiciona um espaço vertical de 5 pixels acima e abaixo do campo de entrada.
        # 'sticky="we"' faz com que o campo de entrada se expanda para
        #       preencher o espaço horizontal disponível dentro da célula.
        self.campo_metodo.grid(row=5,
                               column=1,
                               pady=5,
                               sticky="we")

        # Cria um botão (Button) com o texto "Aplicar Filtros" que será
        #       usado para aplicar os filtros selecionados.
        # O botão é armazenado na variável 'self.botao_filtrar' e ao ser
        #       clicado executará a função 'self.aplicar_filtros'.
        self.botao_filtrar = ttk.Button(self.frame,
                                        text="Aplicar Filtros",
                                        command=self.aplicar_filtros)

        # Posiciona o botão na interface utilizando o gerenciador de layout 'grid'.
        # 'row=6' posiciona o botão na sétima linha do grid.
        # 'column=0' e 'columnspan=2' fazem com que o botão ocupe as
        #       duas primeiras colunas da linha.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo do botão.
        self.botao_filtrar.grid(row=6,
                                column=0,
                                columnspan=2,
                                pady=10)

        # Cria um rótulo (label) com o texto "Total: R$ 0,00" para
        #       exibir o total calculado dos relatórios.
        # O rótulo é estilizado com a fonte "Arial", tamanho 16, e em negrito ("bold").
        # 'row=7' posiciona o rótulo na oitava linha do grid.
        # 'column=0' e 'columnspan=2' fazem com que o rótulo ocupe as duas primeiras colunas da linha.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo do rótulo.
        self.label_total = ttk.Label(self.frame, text="Total: R$ 0,00", font=("Arial", 16, "bold"))
        self.label_total.grid(row=7,
                              column=0,
                              columnspan=2,
                              pady=10)

        # Cria um botão (Button) com o texto "Exportar para Excel" para permitir a
        #       exportação dos dados filtrados para um arquivo Excel.
        # O botão é armazenado na variável 'self.botao_exportar' e ao ser
        #       clicado executará a função 'self.exportar_excel'.
        self.botao_exportar = ttk.Button(self.frame,
                                         text="Exportar para Excel",
                                         command=self.exportar_excel)

        # Posiciona o botão na interface utilizando o gerenciador de layout 'grid'.
        # 'row=8' posiciona o botão na nona linha do grid.
        # 'column=0' e 'columnspan=2' fazem com que o botão ocupe as
        #       duas primeiras colunas da linha.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo do botão.
        self.botao_exportar.grid(row=8,
                                 column=0,
                                 columnspan=2,
                                 pady=10)

        # Cria uma tabela (Treeview) para exibir os dados filtrados ou todas as vendas.
        # A tabela possui as colunas "data", "produto", "fornecedor",
        #       "quantidade", "preco_unit", "total", "pagamento".
        # 'self.frame' é o container onde a tabela será exibida.
        self.tabela = ttk.Treeview(

            self.frame,  # Adiciona a tabela ao frame principal.
            columns=("data", "produto", "fornecedor", "quantidade", "preco_unit", "total", "pagamento"),

            # Define as colunas da tabela.
            # Exibe apenas os cabeçalhos das colunas, sem a coluna de identificador padrão.
            show="headings"

        )

        # Define o título das colunas e exibe os cabeçalhos.
        self.tabela.heading("data", text="Data")  # Cabeçalho para a coluna "Data".
        self.tabela.heading("produto", text="Produto")  # Cabeçalho para a coluna "Produto".
        self.tabela.heading("fornecedor", text="Fornecedor")  # Cabeçalho para a coluna "Fornecedor".
        self.tabela.heading("quantidade", text="Quantidade")  # Cabeçalho para a coluna "Quantidade".
        self.tabela.heading("preco_unit", text="Preço Unitário")  # Cabeçalho para a coluna "Preço Unitário".
        self.tabela.heading("total", text="Total")  # Cabeçalho para a coluna "Total".
        self.tabela.heading("pagamento", text="Pagamento")  # Cabeçalho para a coluna "Pagamento".

        # Posiciona a tabela na interface utilizando o gerenciador de layout 'grid'.
        # 'row=9' posiciona a tabela na décima linha do grid.
        # 'column=0' e 'columnspan=2' fazem com que a tabela ocupe as duas
        #       primeiras colunas da linha.
        # 'sticky="nsew"' faz com que a tabela se expanda para preencher o
        #       espaço disponível na célula do grid.
        # 'pady=10' adiciona um espaço vertical de 10 pixels acima e abaixo da tabela.
        self.tabela.grid(row=9,
                         column=0,
                         columnspan=2,
                         sticky="nsew",
                         pady=10)

        # Configura a linha onde está a tabela para se ajustar ao tamanho da janela.
        # 'rowconfigure(9, weight=1)' permite que a nona linha se expanda
        #       quando a janela é redimensionada.
        self.frame.rowconfigure(9, weight=1)

        # Configura a segunda coluna do frame para se ajustar ao tamanho da janela.
        # 'columnconfigure(1, weight=1)' permite que a segunda coluna se
        #       expanda quando a janela é redimensionada.
        self.frame.columnconfigure(1, weight=1)

        # Chama o método para listar todas as vendas na tabela.
        # Este método será responsável por preencher os dados na tabela.
        self.listar_todas_vendas()



    def aplicar_filtros(self):

        # Coleta a data inicial do campo de entrada, removendo espaços em branco extras
        data_inicial = self.campo_data_inicial.get().strip()

        # Coleta a data final do campo de entrada, removendo espaços em branco extras
        data_final = self.campo_data_final.get().strip()

        # Coleta o nome do produto do campo de entrada, removendo espaços em branco extras
        produto = self.campo_produto.get().strip()

        # Coleta o nome do fornecedor do campo de entrada, removendo espaços em branco extras
        fornecedor = self.campo_fornecedor.get().strip()

        # Coleta o método de pagamento do campo de entrada, removendo
        #       espaços em branco extras
        pagamento = self.campo_metodo.get().strip()

        # Inicializa um dicionário vazio para construir a consulta de
        #       filtro ao banco de dados
        query = {}

        # =======================
        # Filtro entre datas
        # =======================
        # Caso o usuário tenha preenchido tanto data_inicial quanto data_final
        # Verifica se os campos de data inicial e data final estão preenchidos.
        if data_inicial and data_final:

            try:

                # Tenta converter as strings de data inicial e final para objetos
                #       datetime utilizando o formato especificado.
                data_inicial_obj = datetime.datetime.strptime(data_inicial, "%d/%m/%Y")
                data_final_obj = datetime.datetime.strptime(data_final, "%d/%m/%Y")

                # Configura a hora do objeto datetime da data inicial para o
                #       início do dia (00:00:00) para incluir todos os eventos desse dia.
                data_inicial_obj = data_inicial_obj.replace(hour=0, minute=0, second=0, microsecond=0)

                # Configura a hora do objeto datetime da data final para o final
                #       do dia (23:59:59.999999) para incluir todos os eventos até o final desse dia.
                data_final_obj = data_final_obj.replace(hour=23, minute=59, second=59, microsecond=999999)

                # Adiciona ao dicionário de consulta uma condição que busca
                #       registros com datas entre as especificadas, incluindo os limites.
                query["data"] = {"$gte": data_inicial_obj, "$lte": data_final_obj}

            # Captura um erro de valor, que ocorre se a conversão da
            #       data falhar devido a formato incorreto.
            except ValueError:

                print("Datas inválidas. Formato deve ser dd/mm/aaaa.")


        # Verifica se apenas a data inicial foi preenchida, permitindo o
        #       filtro de vendas a partir dessa data específica.
        elif data_inicial:

            try:

                # Converte a string da data inicial para um objeto datetime, usando o formato dia/mês/ano.
                data_inicial_obj = datetime.datetime.strptime(data_inicial,
                                                              "%d/%m/%Y")

                # Configura a hora do objeto datetime para o início do dia (00:00:00).
                # Isso é feito para garantir que todas as vendas
                #       a partir do início do dia especificado sejam incluídas
                #       nos resultados da consulta.
                data_inicial_obj = data_inicial_obj.replace(hour=0,
                                                            minute=0,
                                                            second=0,
                                                            microsecond=0)

                # Adiciona ao dicionário de consulta ('query') uma condição que
                #       especifica que os registros devem ter uma data maior ou igual ('$gte' -
                #       greater than or equal) à data inicial. Isso filtra os dados
                #       para mostrar todas as vendas a partir dessa data.
                query["data"] = {"$gte": data_inicial_obj}

            # Captura e trata o erro caso a data inicial não esteja no formato
            #       correto, evitando interrupções no programa.
            # Um erro de 'ValueError' ocorrerá se a data não puder ser convertida
            #       para datetime devido a um formato inadequado.
            except ValueError:

                print("Data inicial inválida.")


        # Se só preencheu data_final
        # Verifica se apenas a data final foi preenchida, permitindo o filtro
        #       de vendas até essa data específica.
        elif data_final:

            try:

                # Converte a string da data final para um objeto datetime,
                #       usando o formato dia/mês/ano.
                data_final_obj = datetime.datetime.strptime(data_final, "%d/%m/%Y")

                # Configura a hora do objeto datetime para o final do dia (23:59:59.999999).
                # Isso é feito para garantir que todas as vendas
                #       até o final do dia especificado sejam incluídas nos
                #       resultados da consulta.
                data_final_obj = data_final_obj.replace(hour=23,
                                                        minute=59,
                                                        second=59,
                                                        microsecond=999999)

                # Adiciona ao dicionário de consulta ('query') uma condição que especifica
                #       que os registros devem ter uma data
                # menor ou igual ('$lte' - less than or equal) à data final. Isso filtra os
                #       dados para mostrar todas as vendas até essa data.
                query["data"] = {"$lte": data_final_obj}

            # Captura e trata o erro caso a data final não esteja no formato correto,
            #       evitando interrupções no programa.
            # Um erro de 'ValueError' ocorrerá se a data não puder ser convertida para
            #       datetime devido a um formato inadequado.
            except ValueError:
                print("Data final inválida.")

        # =======================
        # Filtros adicionais
        # =======================

        # Se o campo produto estiver preenchido, adiciona um filtro de busca no
        #       dicionário de consultas 'query'.
        # Utiliza uma expressão regular ('$regex') para buscar por qualquer registro que
        #       contenha a string fornecida, ignorando diferenças entre maiúsculas e
        #       minúsculas ('$options': 'i').
        if produto:
            query["produto_nome"] = {"$regex": produto, "$options": "i"}

        # Se o campo fornecedor estiver preenchido, adiciona um filtro semelhante ao de produto.
        # Busca por registros que contenham a string de fornecedor, também utilizando
        #       expressão regular para ignorar maiúsculas e minúsculas.
        if fornecedor:
            query["fornecedor"] = {"$regex": fornecedor, "$options": "i"}

        # Se o campo método de pagamento estiver preenchido, adiciona outro filtro
        #       usando expressão regular.
        # Permite buscar por registros que contenham a string do método de pagamento
        #       especificado, também de forma insensível a maiúsculas.
        if pagamento:
            query["pagamento"] = {"$regex": pagamento, "$options": "i"}

        # Executa a consulta no banco de dados com os filtros aplicados, se houver, e
        #       armazena os resultados em 'vendas_filtradas'.
        # 'colecao_vendas.find(query)' retorna todos os documentos que correspondem ao
        #       critério de pesquisa definido no dicionário 'query'.
        vendas_filtradas = colecao_vendas.find(query)

        # Antes de adicionar novos dados, limpa todos os itens existentes na
        #       tabela para evitar duplicações.
        # '*self.tabela.get_children()' retorna uma lista de todos os elementos
        #       atuais na Treeview, que são então deletados.
        self.tabela.delete(*self.tabela.get_children())

        # Inicializa a variável que irá acumular o total dos valores filtrados
        #       para exibição futura.
        total_filtrado = 0

        # Itera sobre cada documento de venda obtido na consulta
        #       filtrada à base de dados.
        for venda in vendas_filtradas:

            # Extrai o campo 'data' do documento de venda.
            data_venda = venda.get("data")

            # Verifica se o campo 'data' é um dicionário que contém a chave '$date', o
            #       que indica um formato específico de data.
            # Isso é comum em bases de dados que armazenam datas em um
            #       formato especial para serialização.
            if isinstance(data_venda, dict) and "$date" in data_venda:

                # Converte esse formato específico para um objeto de data.
                data_venda = data_venda["$date"]

            # Verifica se existe uma 'data_venda' válida para formatar.
            if data_venda:

                # Formata a data para o formato 'Dia/Mês/Ano'.
                data_formatada = data_venda.strftime("%d/%m/%Y")

            else:

                # Se não houver uma data válida, define a string 'Data desconhecida'
                #       para representar esse valor na tabela.
                data_formatada = "Data desconhecida"

            # Extrai o nome do produto da venda ou usa um valor padrão
            #       se não estiver disponível.
            produto_nome = venda.get("produto_nome", "Produto Desconhecido")

            # Extrai o nome do fornecedor da venda ou usa um valor padrão
            #       se não estiver disponível.
            fornecedor_nome = venda.get("fornecedor", "Fornecedor Desconhecido")

            # Extrai a quantidade do produto vendido ou atribui zero se
            #       não estiver disponível.
            quantidade = venda.get("quantidade", 0)

            # Extrai o preço unitário do produto ou atribui zero se
            #       não estiver disponível.
            preco_unitario = venda.get("preco_unit", 0)

            # Extrai o total do item ou atribui zero se não estiver disponível.
            total_item = float(venda.get("total_item", 0) or 0)

            # Extrai o método de pagamento usado na venda ou usa um
            #       valor padrão se não estiver disponível.
            forma_pagamento = venda.get("pagamento", "Método Desconhecido")

            # Acumula o valor total dos itens filtrados.
            total_filtrado += total_item

            # Insere uma nova linha na tabela 'self.tabela'. Esta ação adiciona os
            #       dados formatados de cada venda filtrada.
            self.tabela.insert("", "end", values=(
                data_formatada,  # Data da venda formatada como "dd/mm/aaaa".
                produto_nome,  # Nome do produto vendido.
                fornecedor_nome,  # Nome do fornecedor do produto.
                quantidade,  # Quantidade do produto vendido.
                f"R$ {preco_unitario:.2f}",  # Preço unitário do produto formatado como moeda.
                f"R$ {total_item:.2f}",  # Total pago pelo item, também formatado como moeda.
                forma_pagamento  # Método de pagamento utilizado na venda.
            ))

        # Atualiza o texto do rótulo 'self.label_total' para mostrar o
        #       valor total dos itens filtrados.
        # O valor 'total_filtrado' é formatado como um valor monetário em
        #       reais, incluindo duas casas decimais e separador de milhares.
        self.label_total.config(text=f"Total: R$ {total_filtrado:,.2f}")



    def exportar_excel(self):



        # Inicializa uma lista para armazenar os dados da tabela.
        dados = []

        # Itera sobre cada item na Treeview para extrair seus valores.
        for item in self.tabela.get_children():

            # Obtém os valores de cada linha da tabela e os adiciona à lista 'dados'.
            valores = self.tabela.item(item, "values")
            dados.append(valores)

        # Define os nomes das colunas para o DataFrame.
        colunas = ["Data", "Produto", "Fornecedor", "Quantidade", "Preço Unitário", "Total", "Pagamento"]

        # Cria um DataFrame a partir dos dados extraídos da tabela.
        df = pd.DataFrame(dados, columns=colunas)

        try:

            # Tenta exportar o DataFrame para um arquivo Excel chamado "relatorio_vendas.xlsx".
            df.to_excel("relatorio_vendas.xlsx", index=False)

            # Exibe uma mensagem informando que a exportação foi concluída com sucesso.
            messagebox.showinfo(
                "Exportação Concluída",
                "Os dados foram exportados para 'relatorio_vendas.xlsx'.",
                parent=self.master
            )

        except Exception as e:

            # Em caso de erro durante a exportação, exibe uma mensagem de
            #       erro com a descrição do problema.
            messagebox.showerror(
                "Erro na Exportação",
                f"Erro ao exportar os dados: {e}",
                parent=self.master
            )



    def listar_todas_vendas(self):

        # Limpa a tabela antes de inserir novos dados.
        # '*self.tabela.get_children()' retorna todos os itens da
        #       tabela, que são deletados.
        self.tabela.delete(*self.tabela.get_children())

        # Obtém todas as vendas armazenadas no banco de dados.
        vendas = colecao_vendas.find()

        # Variável para somar o total geral de todas as vendas.
        total_geral = 0

        # Itera por cada venda recuperada do banco de dados.
        for venda in vendas:

            # Obtém a data da venda, tratando casos onde a data pode
            #       estar formatada como um dicionário.
            data_venda = venda.get("data")
            if isinstance(data_venda, dict) and "$date" in data_venda:

                # Extrai o valor da chave "$date" se a data estiver no
                #       formato de dicionário.
                data_venda = data_venda["$date"]

            # Formata a data em um formato legível (dd/mm/aaaa). Caso a data
            #       seja inexistente, usa "Data desconhecida".
            data_formatada = data_venda.strftime("%d/%m/%Y") if data_venda else "Data desconhecida"

            # Obtém o nome do produto. Caso o campo esteja ausente,
            #       exibe "Produto Desconhecido".
            produto = venda.get("produto_nome", "Produto Desconhecido")

            # Obtém o fornecedor. Caso o campo esteja ausente, exibe "Fornecedor Desconhecido".
            fornecedor = venda.get("fornecedor", "Fornecedor Desconhecido")

            # Obtém a quantidade vendida. Caso o campo esteja ausente, usa o valor padrão 0.
            quantidade = venda.get("quantidade", 0)

            # Obtém o preço unitário do produto. Caso o campo esteja ausente, usa o valor padrão 0.
            preco_unitario = venda.get("preco_unit", 0)

            # Obtém o total do item vendido. Caso o campo esteja ausente, usa o valor padrão 0.
            total = venda.get("total_item", 0)

            # Obtém o método de pagamento utilizado na venda. Caso o campo
            #       esteja ausente, exibe "Método Desconhecido".
            pagamento = venda.get("pagamento", "Método Desconhecido")

            # Soma o total geral
            total_geral += total

            # Adiciona os dados de cada venda na tabela da interface.
            # Os valores são adicionados em uma nova linha ("end") e
            #       organizados em colunas correspondentes.
            self.tabela.insert(

                "",  # Especifica que a nova linha será inserida como um nó raiz na Treeview.
                "end",  # Adiciona a linha no final da tabela.
                values=(
                    data_formatada,  # Data da venda formatada no formato dd/mm/aaaa.
                    produto,  # Nome do produto vendido.
                    fornecedor,  # Nome do fornecedor do produto.
                    quantidade,  # Quantidade do produto vendido.
                    f"R$ {preco_unitario:.2f}",  # Preço unitário formatado como moeda (exemplo: R$ 10,00).
                    f"R$ {total:.2f}",  # Total do item formatado como moeda.
                    pagamento  # Método de pagamento utilizado (exemplo: Dinheiro, Cartão).
                )
            )

        # Atualiza o label do total
        self.label_total.config(text=f"Total: R$ {total_geral:,.2f}")



############################################
# Janela Admin
############################################

# Definição da classe JanelaAdmin que herda de JanelaBase.
# Esta herança permite que JanelaAdmin utilize
#       todas as funcionalidades definidas na classe JanelaBase.
class JanelaAdmin(JanelaBase):

    # Construtor da classe, responsável por inicializar a
    #       janela do painel administrativo.
    def __init__(self, master):

        # Chama o construtor da classe pai, JanelaBase, passando
        #       'master' (o widget pai) e o título da janela.
        super().__init__(master, "Painel Administrativo")

        # Criação de um frame principal que funcionará como o contêiner
        #       para os outros widgets na janela.
        # 'padding="20"' adiciona um espaçamento interno de 20 pixels em
        #       todas as direções dentro do frame.
        self.frame = ttk.Frame(self.master, padding="20")

        # Configuração do frame para preencher completamente o espaço
        #       disponível no widget pai e permitir expansão.
        # 'fill=tk.BOTH' faz com que o frame expanda tanto vertical
        #       quanto horizontalmente.
        # 'expand=True' permite que o frame expanda além do seu tamanho
        #       mínimo para ocupar qualquer espaço extra disponível.
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Criação de um rótulo (label) que serve como título ou
        #       cabeçalho dentro do frame.
        # O rótulo exibe o texto "Selecione o que deseja gerenciar:".
        # 'font=("Arial", 20, "bold")' configura a fonte do texto
        #       para Arial, tamanho 20, em negrito,
        #       melhorando a legibilidade e dando destaque ao título.
        ttk.Label(  self.frame,
                    text="Selecione o que deseja gerenciar:",
                    font=("Arial", 20, "bold")).pack(pady=40)

        # O método .pack() adiciona o rótulo ao layout do frame.
        # 'pady=40' adiciona um espaçamento vertical de 40 pixels acima e
        #       abaixo do rótulo, ajudando a separar visualmente
        #       o título dos outros elementos da interface.

        # Criação de um frame adicional dentro do frame principal
        #       para organizar visualmente os botões.
        # Este frame secundário é chamado de 'botoes_frame'.
        self.botoes_frame = ttk.Frame(self.frame)

        # A função pack() é usada para adicionar este frame secundário ao frame principal.
        # O método pack é uma forma de gerenciar o layout dos widgets,
        #       fazendo-os preencher o espaço disponível.
        self.botoes_frame.pack()

        # Lista de tuplas, onde cada tupla contém um texto representando o
        #       nome do botão e uma função que é chamada quando o botão é clicado.
        # Essa lista é usada para criar vários botões de forma dinâmica.
        botoes = [
            ("Produtos", self.abrir_produtos),  # Botão para abrir a janela de gerenciamento de produtos.
            ("Clientes", self.abrir_clientes),  # Botão para abrir a janela de gerenciamento de clientes.
            ("Funcionários", self.abrir_funcionarios),  # Botão para abrir a janela de gerenciamento de funcionários.
            ("Fornecedores", self.abrir_fornecedores),  # Botão para abrir a janela de gerenciamento de fornecedores.
            ("Estoque", self.abrir_estoque),  # Botão para abrir a janela de gerenciamento de estoque.
            ("Relatórios", self.abrir_relatorios)  # Botão para abrir a janela de relatórios.
        ]

        # Itera sobre a lista de tuplas 'botoes', onde cada tupla contém o
        #       texto do botão e a função correspondente a ser chamada quando o botão é clicado.
        for texto, comando in botoes:

            # Cria um botão dentro do frame 'botoes_frame'.
            # 'text=texto' define o texto que será exibido no botão,
            #       como "Produtos", "Clientes", etc.
            # 'command=comando' associa a função que será executada ao
            #       clicar no botão, como 'self.abrir_produtos', 'self.abrir_clientes', etc.
            # 'width=20' define a largura do botão para garantir
            #       uma aparência uniforme.
            ttk.Button(
                self.botoes_frame,
                text=texto,
                command=comando,
                width=20

                # 'pack' organiza o botão no frame 'botoes_frame'. 'pady=10'
                #       adiciona espaço vertical acima e abaixo do botão. 'ipadx=20' e
                #       'ipady=10' aumentam a área interna do botão horizontalmente e
                #       verticalmente, tornando-o mais fácil de clicar.
            ).pack(pady=10,
                   ipadx=20,
                   ipady=10)

    # Define o método para abrir a janela de gerenciamento de produtos.
    def abrir_produtos(self):

        # Cria uma nova janela para produtos usando 'tk.Toplevel' que faz com
        #       que a janela de produtos seja uma sub-janela da janela
        #       principal ('self.master').
        JanelaProdutos(tk.Toplevel(self.master))

    # Define o método para abrir a janela de gerenciamento de clientes.
    def abrir_clientes(self):

        # Cria uma nova janela para clientes usando 'tk.Toplevel'.
        JanelaClientes(tk.Toplevel(self.master))

    # Define o método para abrir a janela de gerenciamento de funcionários.
    def abrir_funcionarios(self):

        # Cria uma nova janela para funcionários usando 'tk.Toplevel'.
        JanelaFuncionarios(tk.Toplevel(self.master))

    # Define o método para abrir a janela de gerenciamento de fornecedores.
    def abrir_fornecedores(self):

        # Cria uma nova janela para fornecedores usando 'tk.Toplevel'.
        JanelaFornecedores(tk.Toplevel(self.master))

    # Define o método para abrir a janela de gerenciamento de estoque.
    def abrir_estoque(self):

        # Cria uma nova janela para estoque usando 'tk.Toplevel'.
        JanelaEstoque(tk.Toplevel(self.master))

    # Define o método para abrir a janela de relatórios.
    def abrir_relatorios(self):

        # Cria uma nova janela para relatórios usando 'tk.Toplevel'.
        JanelaRelatorios(tk.Toplevel(self.master))



############################################
# Janela Nota Fiscal
############################################

# Classe para gerenciar a exibição e operações relacionadas à nota fiscal.
class JanelaNotaFiscal:

    # Construtor da classe, inicializa a janela e configura seu layout.
    def __init__(self, master, venda):

        # 'master' é o widget pai no qual a janela será criada.
        self.master = master

        # Define o título da janela para "Nota Fiscal".
        self.master.title("Nota Fiscal")

        # Ajusta a janela para o modo de tela cheia.
        # self.master.state('zoomed')

        # Cria um frame dentro da janela principal para organizar outros widgets.
        frame = ttk.Frame(self.master,
                          padding="10")

        # Configura o frame para preencher o espaço disponível na janela,
        #       tanto horizontal quanto verticalmente.
        frame.pack(fill=tk.BOTH, expand=True)

        # Botão que permite ao usuário exportar e imprimir a nota fiscal em formato PDF.
        exportar_btn = ttk.Button(frame,
                                  text="Exportar e Imprimir PDF",
                                  command=lambda: self.exportar_pdf(venda))

        # Posiciona o botão na janela e ajusta seu padding vertical.
        exportar_btn.pack(pady=10)

        # Inicia a variável 'texto' com a linha de cabeçalho da nota fiscal,
        #       indicando o nome do supermercado.
        texto = "===== Supermercado Exemplo =====\n"

        # Adiciona a data da venda ao texto, convertendo o objeto de data
        #       para uma string formatada com dia, mês, ano e hora.
        texto += f"Data: {venda['data'].strftime('%d/%m/%Y %H:%M')}\n"

        # Inclui o CPF do cliente na nota fiscal.
        texto += f"CPF Cliente: {venda['cpf_cliente']}\n"

        # Insere uma linha de separação para demarcar o início da
        #       listagem dos itens comprados.
        texto += "--------------------------------\n"

        # Define os títulos das colunas para os itens listados na nota,
        #       especificando código, nome, quantidade, preço e total.
        texto += "Cód   Nome             Qtd    Preço     Total\n"

        # Adiciona outra linha de separação abaixo dos títulos das colunas.
        texto += "--------------------------------\n"

        # Define a variável 'total_final' para acumular o valor total da compra.
        total_final = 0.0

        # Itera sobre cada item na lista de itens da venda.
        for item in venda["itens"]:

            # Calcula o subtotal multiplicando a quantidade do item
            #       pelo seu preço unitário.
            subtotal = item["quantidade"] * item["preco_unit"]

            # Adiciona o subtotal ao total final da compra.
            total_final += subtotal

            # Formata e adiciona cada item da compra ao texto da nota fiscal. O formato especifica:
            # - Código do produto alinhado e com espaço para até 5 caracteres.
            # - Nome do produto cortado para caber em 15 caracteres e alinhado à esquerda.
            # - Quantidade com espaço para 3 caracteres e alinhada à direita.
            # - Preço unitário precedido por "R$" e formatado para ter duas casas
            #       decimais, com espaço para 7 caracteres e alinhado à direita.
            # - Subtotal precedido por "R$" e formatado para ter duas casas
            #       decimais, com espaço para 7 caracteres e alinhado à direita.
            texto += f"{item['codigo']:5}  {item['nome'][:15]:15}  {item['quantidade']:3}  R${item['preco_unit']:7.2f}  R${subtotal:7.2f}\n"

        # Verifica se existe um desconto aplicado na venda e, se houver, adiciona a
        #       linha do desconto no texto da nota fiscal.
        if venda["desconto_total"] > 0:
            texto += f"\nDesconto: R${venda['desconto_total']:.2f}\n"

        # Adiciona uma linha de separação após a listagem dos itens ou desconto.
        texto += "--------------------------------\n"

        # Calcula o total final subtraindo o desconto do total bruto
        #       acumulado e adiciona esta informação ao texto.
        texto += f"Total: R${total_final - venda['desconto_total']:.2f}\n"

        # Adiciona outra linha de separação após o total.
        texto += "--------------------------------\n"

        # Adiciona uma mensagem de agradecimento ao final da nota.
        texto += "Obrigado pela preferência!\n"

        # Cria um widget de texto para exibir a nota fiscal formatada.
        text_widget = tk.Text(frame, wrap="word", font=("Courier", 20))

        # Insere o texto da nota fiscal no widget de texto a partir da
        #       posição "1.0" (linha 1, coluna 0).
        text_widget.insert("1.0", texto)

        # Configura o widget de texto para ser somente leitura, impedindo
        #       que o usuário edite o conteúdo.
        text_widget.config(state="disabled")

        # Configura o widget de texto para preencher o espaço disponível na
        #       interface, expandindo conforme necessário.
        text_widget.pack(fill=tk.BOTH, expand=True)

    def exportar_pdf(self, venda):

        # Cria um objeto PDF, que será usado para construir o documento.
        pdf = FPDF()

        # Adiciona uma página ao documento PDF, que será a base para
        #       adicionar textos e outros conteúdos.
        pdf.add_page()

        # Define o tipo e o tamanho da fonte que será usada no documento.
        # 'Courier' é uma fonte de largura fixa.
        pdf.set_font("Courier", size=12)

        # Cabeçalho
        # Muda a fonte para negrito ('B') e aumenta o tamanho
        #      para 14 para destacar o cabeçalho.
        pdf.set_font("Courier", style="B", size=14)

        # Cria uma célula no PDF que contém o título do supermercado,
        #       centralizado ('C') e com uma quebra de linha automática (ln=True).
        pdf.cell(190, 10, txt="===== Supermercado Exemplo =====", ln=True, align='C')

        # Volta para a fonte normal, tamanho 12, para as informações subsequentes.
        pdf.set_font("Courier", size=12)

        # Adiciona a data da venda ao PDF, também centralizada e com quebra de linha.
        pdf.cell(190, 8, txt=f"Data: {venda['data'].strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')

        # Adiciona o CPF do cliente ao PDF, formatado da mesma maneira que a data.
        pdf.cell(190, 8, txt=f"CPF Cliente: {venda['cpf_cliente']}", ln=True, align='C')

        # Adiciona um espaço adicional antes de listar os itens da venda.
        pdf.ln(8)

        # Define o estilo e o tamanho da fonte para os cabeçalhos da
        #       tabela de itens. 'B' indica negrito.
        pdf.set_font("Courier", style="B", size=12)

        # Cria uma célula para o cabeçalho "Cód", com borda,
        #       largura de 25 e altura de 8.
        pdf.cell(25, 8, "Cód", 1)

        # Cria uma célula para o cabeçalho "Nome", com borda,
        #       largura de 70 e altura de 8.
        pdf.cell(70, 8, "Nome", 1)

        # Cria uma célula para o cabeçalho "Qtd" (Quantidade),
        #       com borda, largura de 25 e altura de 8.
        pdf.cell(25, 8, "Qtd", 1)

        # Cria uma célula para o cabeçalho "Preço", com borda,
        #       largura de 30 e altura de 8.
        pdf.cell(30, 8, "Preço", 1)

        # Cria uma célula para o cabeçalho "Total", com borda,
        #       largura de 30 e altura de 8.
        pdf.cell(30, 8, "Total", 1)

        # Move para a próxima linha na tabela para começar a adicionar os itens.
        pdf.ln()

        # Volta para a fonte normal (sem negrito) para a listagem dos itens da venda.
        pdf.set_font("Courier", size=12)

        # Inicializa a variável que vai acumular o total final da nota.
        total_final = 0.0

        # Itera sobre cada item na lista de itens da venda.
        for item in venda["itens"]:

            # Calcula o subtotal para cada item multiplicando a
            #       quantidade pelo preço unitário.
            subtotal = item["quantidade"] * item["preco_unit"]

            # Acumula o subtotal de cada item ao total final da nota fiscal.
            total_final += subtotal

            # Cria uma célula no PDF para o código do item, configurando a
            #       largura, altura e borda da célula.
            pdf.cell(25, 8, str(item["codigo"]), 1)

            # Cria uma célula para o nome do item. Limita o nome a 20 caracteres
            #       para evitar sobreposição.
            pdf.cell(70, 8, item["nome"][:20], 1)

            # Cria uma célula para a quantidade do item, convertendo o valor para string.
            pdf.cell(25, 8, str(item["quantidade"]), 1)

            # Cria uma célula para o preço unitário do item, formatando o
            #       número para duas casas decimais com o símbolo de real.
            pdf.cell(30, 8, f"R${item['preco_unit']:.2f}", 1)

            # Cria uma célula para o subtotal do item, também formatado
            #       com duas casas decimais.
            pdf.cell(30, 8, f"R${subtotal:.2f}", 1)

            # Move para a próxima linha no PDF para começar a adicionar o próximo item.
            pdf.ln()

        # Adiciona um pequeno espaço antes de começar a parte do desconto e
        #       total para melhor visualização.
        pdf.ln(5)

        # Verifica se existe um desconto aplicado na venda.
        if venda["desconto_total"] > 0:

            # Cria uma célula no PDF para mostrar o desconto aplicado,
            #       alinhado à direita.
            pdf.cell(190,
                     8,
                     f"Desconto: R${venda['desconto_total']:.2f}",
                     ln=True,
                     align='R')

        # Cria uma célula para mostrar o total final da compra já com o desconto
        #       aplicado, se houver, alinhado à direita.
        pdf.cell(190,
                 8,
                 f"Total: R${total_final - venda['desconto_total']:.2f}",
                 ln=True,
                 align='R')

        # Adiciona um espaço antes de exibir a mensagem de agradecimento.
        pdf.ln(10)

        # Exibe a mensagem de agradecimento ao cliente, centrada no documento.
        pdf.cell(190,
                 10,
                 txt="Obrigado pela preferência!",
                 ln=True,
                 align='C')

        # Define o nome do arquivo PDF a ser salvo.
        arquivo_pdf = "nota_fiscal.pdf"

        # Salva o arquivo PDF no diretório local.
        pdf.output(arquivo_pdf)

        # Exibe uma caixa de mensagem informando que a nota fiscal
        #       foi exportada com sucesso.
        messagebox.showinfo("Sucesso", f"Nota fiscal exportada como {arquivo_pdf}", parent=self.master)



############################################
# Janela Caixa (POS)
############################################

class JanelaCaixa:

    # Construtor da classe JanelaCaixa. Ele é chamado automaticamente quando
    #       uma instância desta classe é criada.
    def __init__(self, root, dados_usuario):

        # 'self.root' é uma variável de instância que armazena o objeto root,
        #       que representa a janela principal do Tkinter.
        # O parâmetro 'root' é passado quando uma instância da classe JanelaCaixa é criada.
        # Isso permite que todas as funções dentro da classe JanelaCaixa
        #       interajam com a janela principal do aplicativo.
        self.root = root

        # 'self.dados_usuario' é uma variável de instância que armazena
        #       informações sobre o usuário atual.
        # O parâmetro 'dados_usuario' é passado ao criar uma instância da classe e
        #       geralmente contém informações como nome de usuário, permissões, etc.
        # Esses dados são utilizados para personalizar a experiência do usuário e
        #       controlar acessos dentro da aplicação.
        self.dados_usuario = dados_usuario

        # Define o título da janela principal. Este método configura o texto
        #       que aparece na barra de título da janela.
        # Neste caso, está configurado para mostrar que esta janela é
        #       dedicada ao "Sistema de Supermercado - Caixa".
        self.root.title("Sistema de Supermercado - Caixa")

        # Configura a janela para ser exibida em tela cheia.
        # O método 'attributes' com o argumento "-fullscreen", True faz com
        #       que a janela ocupe toda a tela, melhorando a visibilidade e
        #       acessibilidade para o usuário final.
        self.root.attributes("-fullscreen", True)

        # Cria e configura o estilo visual para diferentes widgets (componentes de
        #       interface) que serão utilizados na janela.
        # 'ttk.Style()' cria um objeto de estilo que pode ser usado para
        #       configurar a aparência global dos widgets ttk.
        estilo = ttk.Style()

        # Configura os rótulos (labels) para usar a fonte Arial tamanho 16.
        # Isso ajuda a garantir que os rótulos sejam claramente legíveis,
        #       mantendo a interface amigável.
        estilo.configure("TLabel", font=("Arial", 16))

        # Configura as entradas de texto (entries) para usar a mesma fonte,
        #       garantindo uma consistência visual na interface.
        estilo.configure("TEntry", font=("Arial", 16))

        # Configura os botões para também usar Arial tamanho 16, mantendo a
        #       uniformidade com outros elementos de texto.
        estilo.configure("TButton", font=("Arial", 16))

        # Especifica o estilo para os cabeçalhos das tabelas (Treeview.Heading),
        #       usando negrito para destacá-los visualmente.
        estilo.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        # Aplica um tamanho de fonte ligeiramente menor para o conteúdo das
        #       tabelas (Treeview), garantindo que mais dados caibam na tela
        #       sem sacrificar a legibilidade.
        estilo.configure("Treeview", font=("Arial", 14))

        # Cria um frame chamado 'frame_top' no topo da janela principal 'root'.
        # O 'padding=10' adiciona um espaçamento interno de 10 pixels em todos os
        #       lados dentro do frame, o que ajuda a evitar que os widgets
        #       fiquem muito juntos.
        self.frame_top = ttk.Frame(self.root, padding=10)

        # Empacota o 'frame_top' na parte superior da janela ('side=tk.TOP') e
        #       faz com que ele preencha toda a largura disponível ('fill=tk.X').
        # Isso assegura que o frame se estenda horizontalmente ao longo da parte
        #       superior da janela, criando uma área distinta para outros
        #       controles ou informações.
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        # Cria um rótulo dentro de 'frame_top' que exibe o texto "Supermercado Exemplo".
        # 'font=("Arial", 24, "bold")' configura a fonte do texto para Arial,
        #       tamanho 24, em negrito, tornando o rótulo visualmente
        #       proeminente como um cabeçalho.
        self.label_supermercado = ttk.Label(self.frame_top,
                                            text="Supermercado Exemplo",
                                            font=("Arial", 24, "bold"))

        # Empacota o rótulo 'label_supermercado' à esquerda dentro
        #       do 'frame_top' ('side=tk.LEFT').
        # Isso posiciona o rótulo no lado esquerdo do frame, fazendo-o
        #       aparecer no canto superior esquerdo da janela.
        self.label_supermercado.pack(side=tk.LEFT)

        # Cria outro rótulo chamado 'label_data_hora' dentro de 'frame_top',
        #       inicialmente sem texto.
        # 'font=("Arial", 16)' configura a fonte para Arial, tamanho 16,
        #       adequado para exibir informações menores como data e hora.
        self.label_data_hora = ttk.Label(self.frame_top,
                                         font=("Arial", 16))

        # Empacota o rótulo 'label_data_hora' à direita dentro do
        #       'frame_top' ('side=tk.RIGHT').
        # Isso faz com que ele apareça no canto superior direito,
        #       geralmente usado para informações como data e hora atuais.
        self.label_data_hora.pack(side=tk.RIGHT)

        # Cria um botão chamado 'botao_admin' no 'frame_top', com o rótulo "Admin".
        # O comando 'self.abrir_admin' é associado a este botão, que será
        #       executado quando o botão for clicado, abrindo a interface administrativa.
        self.botao_admin = ttk.Button(self.frame_top,
                                      text="Admin",
                                      command=self.abrir_admin)

        # Empacota o 'botao_admin' no lado direito do 'frame_top',
        #       com um espaçamento horizontal ('padx') de 10 pixels.
        # Isso adiciona um espaço entre este botão e outros elementos ou
        #       margens, melhorando a estética da disposição.
        self.botao_admin.pack(side=tk.RIGHT, padx=10)

        # Cria um botão chamado 'botao_sair', também no 'frame_top', com o rótulo "Sair".
        # O comando 'self.root.destroy' é vinculado a este botão, que
        #       fecha a aplicação quando clicado.
        self.botao_sair = ttk.Button(self.frame_top,
                                     text="Sair",
                                     command=self.root.destroy)

        # Empacota o 'botao_sair' no lado direito, próximo ao 'botao_admin',
        #       com um espaçamento horizontal ('padx') de 10 pixels.
        # Isso mantém a uniformidade visual entre os botões.
        self.botao_sair.pack(side=tk.RIGHT,
                             padx=10)

        # Chama a função 'self.atualizar_data_hora', que atualiza continuamente a
        #       data e a hora exibidas no 'label_data_hora'.
        self.atualizar_data_hora()

        # Cria um frame principal chamado 'frame_main' para conter os
        #       principais widgets da aplicação.
        # O 'padding=20' adiciona um espaçamento interno ao frame,
        #       aumentando a legibilidade e atração visual.
        self.frame_main = ttk.Frame(self.root,
                                    padding=20)

        # Empacota o 'frame_main' para preencher tanto a largura quanto a
        #       altura disponíveis ('fill=tk.BOTH'), e permite que ele
        #       expanda ('expand=True').
        # Isso assegura que o 'frame_main' ocupe todo o espaço disponível na
        #       janela, adequando-se à dinâmica da interface.
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # Cria uma tabela 'Treeview' dentro do 'frame_main' com colunas específicas.
        # 'columns' define as colunas pelo nome. 'show="headings"' configura a
        #       tabela para mostrar apenas os cabeçalhos das colunas, sem
        #       uma coluna de índice à esquerda.
        # 'height=20' define a altura da tabela para mostrar 20 linhas de uma vez.
        # 'selectmode='browse'' permite a seleção de uma única linha por vez.
        self.tabela = ttk.Treeview(
            self.frame_main,
            columns=("codigo", "nome", "qtd", "preco_unit", "subtotal"),
            show="headings",
            height=20,
            selectmode='browse'
        )

        # Configura o cabeçalho da coluna 'codigo' com o texto "Código".
        self.tabela.heading("codigo", text="Código")

        # Configura o cabeçalho da coluna 'nome' com o texto "Nome".
        self.tabela.heading("nome", text="Nome")

        # Configura o cabeçalho da coluna 'qtd' (quantidade) com o texto "Qtd".
        self.tabela.heading("qtd", text="Qtd")

        # Configura o cabeçalho da coluna 'preco_unit' com o texto "Preço Unit.".
        self.tabela.heading("preco_unit", text="Preço Unit.")

        # Configura o cabeçalho da coluna 'subtotal' com o texto "Subtotal".
        self.tabela.heading("subtotal", text="Subtotal")

        # Define a largura da coluna 'codigo' como 100 pixels.
        self.tabela.column("codigo", width=100)

        # Define a largura da coluna 'nome' como 200 pixels.
        self.tabela.column("nome", width=200)

        # Define a largura da coluna 'qtd' como 50 pixels.
        self.tabela.column("qtd", width=50)

        # Define a largura da coluna 'preco_unit' como 100 pixels.
        self.tabela.column("preco_unit", width=100)

        # Define a largura da coluna 'subtotal' como 100 pixels.
        self.tabela.column("subtotal", width=100)

        # Empacota a tabela no lado esquerdo do 'frame_main', preenchendo tanto a
        #       largura quanto a altura disponíveis e permitindo expansão.
        # 'side=tk.LEFT' coloca a tabela à esquerda dentro de seu container.
        # 'fill=tk.BOTH' e 'expand=True' permitem que a tabela expanda para
        #       preencher o espaço disponível horizontal e verticalmente.
        self.tabela.pack(side=tk.LEFT,
                         fill=tk.BOTH,
                         expand=True)

        # Inicializa a lista 'self.carrinho' que armazenará os itens
        #       adicionados ao carrinho de compras.
        self.carrinho = []

        # Cria um frame à direita no frame principal para organizar
        #       elementos específicos do processo de checkout.
        # 'padding=10' adiciona um espaçamento interno de 10 pixels em
        #       todos os lados dentro do frame.
        self.frame_side = ttk.Frame(self.frame_main, padding=10)

        # Empacota o frame lateral no lado direito da tela principal,
        #       preenchendo o espaço vertical disponível (fill=tk.Y).
        self.frame_side.pack(side=tk.RIGHT, fill=tk.Y)

        # Cria e configura um rótulo com o texto "Código de Barras:" no
        #       frame lateral usando fonte Arial tamanho 16.
        # 'pack(pady=5)' posiciona o rótulo com um espaçamento
        #       vertical de 5 pixels para separação visual.
        ttk.Label(self.frame_side,
                  text="Código de Barras:",
                  font=("Arial", 16)).pack(pady=5)

        # Cria um campo de entrada para que o usuário possa inserir os
        #       códigos de barras dos produtos.
        # Usa a mesma fonte do rótulo para consistência visual.
        self.campo_codigo = ttk.Entry(self.frame_side,
                                      font=("Arial", 16))

        # Empacota o campo de entrada com um espaçamento vertical de 5 pixels,
        #       similar ao do rótulo, para alinhamento e organização visual.
        self.campo_codigo.pack(pady=5)

        # Associa o evento de pressionar a tecla Enter (Return) no campo de
        #       entrada ao método 'self.adicionar_item'.
        # Isso permite que um item seja adicionado ao carrinho imediatamente
        #       após o código ser digitado e Enter pressionado.
        self.campo_codigo.bind("<Return>",
                               self.adicionar_item)

        # Cria um rótulo para exibir o total das compras com
        #       fonte Arial tamanho 24 e em negrito.
        # O texto inicial é 'Total: R$ 0.00', mostrando o total inicial
        #       do carrinho como R$0,00.
        self.label_total = ttk.Label(self.frame_side,
                                     text="Total: R$ 0.00",
                                     font=("Arial", 24, "bold"))

        # Empacota o rótulo do total no frame lateral com um
        #       espaçamento vertical de 20 pixels,
        #       proporcionando uma separação visual adequada entre os
        #       elementos na interface.
        self.label_total.pack(pady=20)

        # Cria um rótulo para indicar onde o usuário pode inserir um
        #       desconto, se aplicável, utilizando fonte Arial tamanho 14.
        # O texto 'Desconto (opcional):' orienta o usuário de que
        #       pode aplicar um desconto nas compras.
        ttk.Label(self.frame_side,
                  text="Desconto (opcional):",
                  font=("Arial", 14)).pack(pady=5)

        # Cria um campo de entrada onde o usuário pode digitar um
        #       valor de desconto para a compra.
        # Usa a mesma fonte do rótulo para consistência visual.
        self.campo_desconto = ttk.Entry(self.frame_side,
                                        font=("Arial", 14))

        # Empacota o campo de desconto no frame lateral com um
        #       espaçamento vertical de 5 pixels,
        #       mantendo a consistência do layout com o espaçamento
        #       entre os outros elementos.
        self.campo_desconto.pack(pady=5)

        # Cria um rótulo para indicar onde o usuário deve inserir o método de pagamento.
        # Utiliza fonte Arial tamanho 14 para manter a consistência
        #       visual com outros elementos de entrada.
        # O texto "Método Pagamento:" serve como um guia visual para o
        #       usuário saber onde inserir essa informação.
        ttk.Label(self.frame_side,
                  text="Método Pagamento:",
                  font=("Arial", 14)).pack(pady=5)

        # Cria um campo de entrada para que o usuário possa digitar o
        #       método de pagamento utilizado.
        # Configura a fonte do campo de entrada para Arial tamanho 14,
        #       alinhando-se ao estilo dos outros campos de entrada.
        self.campo_pagamento = ttk.Entry(self.frame_side,
                                         font=("Arial", 14))

        # Insere o texto padrão "Dinheiro" no campo de entrada como valor inicial,
        # indicando que esta é a opção de pagamento padrão, mas pode
        #       ser alterada pelo usuário.
        self.campo_pagamento.insert(0, "Dinheiro")

        # Empacota o campo de entrada no frame lateral com um espaçamento
        #       vertical de 5 pixels,
        #       assegurando que haja um espaço adequado acima e abaixo deste
        #       campo para evitar uma interface visualmente congestionada.
        self.campo_pagamento.pack(pady=5)

        # Cria um rótulo no frame lateral para indicar onde o usuário
        #       pode inserir um CPF para nota fiscal.
        # Utiliza a fonte Arial tamanho 14, mantendo a consistência com
        #       outros rótulos na interface.
        # O texto "CPF na Nota (opcional):" informa ao usuário que ele
        #       pode, mas não é obrigatório, inserir o CPF.
        ttk.Label(self.frame_side,
                  text="CPF na Nota (opcional):",
                  font=("Arial", 14)).pack(pady=5)

        # Cria um campo de entrada para que o usuário possa digitar o CPF.
        # Configura a fonte do campo para Arial tamanho 14, assim como os
        #       outros campos de entrada da interface.
        self.campo_cpf = ttk.Entry(self.frame_side,
                                   font=("Arial", 14))

        # Empacota o campo de entrada no frame lateral, com um
        #       espaçamento vertical de 5 pixels, garantindo um espaçamento
        #       adequado para evitar uma interface visualmente congestionada.
        self.campo_cpf.pack(pady=5)

        # Cria um botão para finalizar a venda. Este botão executa a
        #       função 'finalizar_venda' quando clicado.
        # O texto "Finalizar Venda" é autoexplicativo, indicando a
        #       ação que será realizada ao clicar.
        # bg="yellow",  # Cor de fundo do botão.
        # fg="white",  # Cor do texto do botão.
        # font=("Arial", 12, "bold")  # Configuração da fonte.
        self.botao_finalizar = tk.Button(self.frame_side,
                                         text="Finalizar Venda",
                                         command=self.finalizar_venda,
                                         bg="yellow",
                                         fg="black",
                                         font=("Arial", 16, "bold"))

        # Empacota o botão no frame lateral com um preenchimento em eixo x (fill=tk.X) e
        #       um espaçamento vertical (pady) de 10 pixels,
        #       tornando o botão mais largo e mais fácil de clicar, além
        #       de visualmente mais atraente.
        self.botao_finalizar.pack(pady=10, fill=tk.X)

        # Cria um botão para cancelar a venda atual. Este botão executa a
        #       função 'cancelar_venda' quando clicado.
        # "Cancelar Venda" é o texto exibido no botão, comunicando
        #       claramente sua função.
        self.botao_cancelar = ttk.Button(self.frame_side,
                                         text="Cancelar Venda",
                                         command=self.cancelar_venda)

        # Empacota o botão de cancelar no frame lateral com preenchimento em
        #       eixo x (fill=tk.X) e um espaçamento vertical (pady) de 10 pixels,
        #       tornando o botão mais acessível e visualmente consistente
        #       com outros botões da interface.
        self.botao_cancelar.pack(pady=10, fill=tk.X)

        # Cria um botão para remover um produto selecionado na lista de compras.
        # "Remover Produto Selecionado" é o texto no botão, explicando
        #       explicitamente sua funcionalidade.
        # A função 'remover_item_selecionado' é chamada quando o botão é
        #       clicado, removendo o item atualmente selecionado na tabela.
        self.botao_remover_item = ttk.Button(self.frame_side,
                                             text="Remover Produto Selecionado",
                                             command=self.remover_item_selecionado)

        # Empacota o botão de remover produto da mesma maneira que os outros,
        #       garantindo uniformidade e facilitando a navegação do usuário.
        self.botao_remover_item.pack(pady=10,
                                     fill=tk.X)

        # Cria um botão para alterar a quantidade de um produto selecionado.
        # "Alterar Quantidade Selecionada" indica que o usuário pode modificar a
        #       quantidade do item escolhido.
        # Este botão aciona a função 'alterar_quantidade_item', permitindo ao
        #       usuário ajustar a quantidade do produto diretamente na interface.
        self.botao_alterar_qtd = ttk.Button(self.frame_side,
                                            text="Alterar Quantidade Selecionada",
                                            command=self.alterar_quantidade_item)

        # O empacotamento é realizado com as mesmas opções dos botões anteriores
        #       para manter a consistência visual e de layout.
        self.botao_alterar_qtd.pack(pady=10, fill=tk.X)

        # Configura o estilo dos botões destacados com a cor de
        #       fundo azul (#007BFF) e texto branco.
        # A fonte Arial, tamanho 16 e negrito é usada para realçar
        #       ainda mais esses botões importantes.
        estilo.configure("Accent.TButton",
                         foreground="white",
                         background="#007BFF",
                         font=("Arial", 16, "bold"))


    # Função para abrir a janela de administração quando o
    #       botão "Admin" é pressionado.
    def abrir_admin(self):

        # Cria uma nova janela de nível superior, que é usada
        #       para abrir uma nova instância de JanelaAdmin.
        JanelaAdmin(tk.Toplevel(self.root))


    # Função para atualizar a data e a hora exibidas na interface do usuário.
    def atualizar_data_hora(self):

        # Obtém o momento atual, formata para o formato de data e hora
        #       brasileiro (dia, mês, ano, horas, minutos, segundos).
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Atualiza o texto do rótulo `label_data_hora` com a string formatada 'agora'.
        self.label_data_hora.config(text=agora)

        # Agendamento para que esta função seja chamada novamente
        #       após 1000 milissegundos (1 segundo),
        #       garantindo que a hora exibida seja atualizada a cada segundo.
        self.root.after(1000, self.atualizar_data_hora)


    # Função chamada ao pressionar 'Enter' no campo de código de
    #       barras ou ao disparar outro evento associado.
    def adicionar_item(self, event=None):

        # Primeiro, garante que o carrinho exibido na interface gráfica
        #       esteja sincronizado com a lista interna do carrinho.
        self.sincronizar_carrinho_com_treeview()

        # Obtém o código digitado no campo de entrada de código de barras,
        #       removendo espaços extras antes e depois do texto.
        cod = self.campo_codigo.get().strip()

        # Se o campo estiver vazio (sem código), a função retorna imediatamente,
        #       evitando processamento adicional.
        if not cod:
            return

        # Procura no banco de dados do produto pelo código fornecido.
        produto = colecao_produtos.find_one({"codigo": cod})

        # Se não encontrar um produto com o código fornecido, exibe uma
        #       mensagem de erro e interrompe a função.
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.", parent=self.root)
            return

        # Verifica se a quantidade disponível do produto é menor que 1.
        # Se for, exibe uma mensagem de erro.
        if produto["quantidade"] < 1:
            messagebox.showerror("Erro", "Estoque insuficiente.", parent=self.root)
            return

        # Adiciona o novo produto ao carrinho com quantidade inicial definida como 1.
        qtd = 1  # Define a quantidade inicial do produto a ser adicionada ao carrinho.
        preco = produto["preco"]  # Obtém o preço do produto do banco de dados.
        nome = produto["nome"]  # Obtém o nome do produto do banco de dados.

        # Insere uma tupla representando o item do carrinho na lista `self.carrinho`.
        # Cada tupla contém o código, quantidade, preço e nome do produto.
        self.carrinho.append((cod, qtd, preco, nome))

        # Insere o produto na interface gráfica, especificamente na tabela Treeview.
        # Adiciona uma nova linha com o código do produto, nome,
        #       quantidade e preço formatado.
        self.tabela.insert("",
                           tk.END,
                           values=(cod, nome, qtd, f"R${preco:.2f}", f"R${qtd * preco:.2f}"))

        # Chama a função para atualizar o total geral devido à adição de um novo produto.
        self.atualizar_total_geral()

        # Limpa o campo de entrada do código de barras após o produto ser
        #       adicionado, preparando para a próxima entrada.
        self.campo_codigo.delete(0, tk.END)


    def atualizar_tabela(self):

        # Limpa a Treeview removendo todos os itens existentes para
        #       evitar duplicações ao reexibir os dados.
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        # Inicializa uma variável `total` que vai acumular o
        #       valor total dos itens no carrinho.
        total = 0.0

        # Itera sobre cada item no carrinho, que é uma lista de tuplas
        #       contendo código, quantidade, preço e nome do produto.
        for (cod, qtd, preco, nome) in self.carrinho:

            # Calcula o subtotal do item multiplicando a quantidade pelo preço.
            subtotal = qtd * preco

            # Adiciona o subtotal ao total geral.
            total += subtotal

            # Insere cada item do carrinho na Treeview, mostrando código,
            #       nome, quantidade, preço unitário e subtotal,
            # formatando os valores de preço para incluir o símbolo de
            #       real e duas casas decimais.
            self.tabela.insert("",
                               tk.END,
                               values=(cod, nome, qtd, f"R${preco:.2f}", f"R${subtotal:.2f}"))

        # Atualiza o label que mostra o total geral de todos os itens no carrinho,
        # formatando o valor total para incluir o símbolo de real e duas casas decimais.
        self.label_total.config(text=f"Total: R$ {total:.2f}")


    def finalizar_venda(self):

        # Verifica se existem produtos no carrinho, checando
        #       se a tabela está vazia.
        if not self.tabela.get_children():

            # Exibe uma mensagem de erro se o carrinho estiver vazio e
            #       interrompe a execução da função.
            messagebox.showerror("Erro", "Carrinho vazio.", parent=self.root)

            return  # Sai da função se não houver itens para processar.

        # Obtém o CPF inserido no campo de entrada, removendo espaços desnecessários.
        cpf_cliente = self.campo_cpf.get().strip()

        # Cria uma lista para armazenar os detalhes dos itens que serão vendidos.
        itens_venda = []

        # Tenta converter o texto do campo de desconto para float.
        # Se estiver vazio, assume-se 0.0.
        desconto = float(self.campo_desconto.get() or 0.0)

        # Inicializa o cálculo do total dos itens no carrinho antes
        #       do desconto ser aplicado.
        # Itera sobre cada item na Treeview do carrinho para somar seus subtotais.
        # O valor em 'values[4]' representa o subtotal de cada item, que
        #       está formatado como string no formato de moeda, por exemplo, "R$100,00".
        # Este valor é primeiramente limpo de caracteres monetários e de
        #       formatação ("R$" e vírgulas) para permitir a correta conversão para float,
        #       que é necessário para realizar operações matemáticas.
        # A função 'sum()' soma todos os subtotais após a conversão,
        #       resultando no total dos preços dos produtos antes de
        #       qualquer desconto ser aplicado.
        total_sem_desconto = sum(
            float(self.tabela.item(item,
                                   "values")[4].replace("R$", "").replace(",", "."))
            for item in self.tabela.get_children()
        )

        # Calcula a porcentagem do desconto com base no total sem
        #       desconto, evitando divisão por zero.
        desconto_porcentagem = desconto / total_sem_desconto if total_sem_desconto > 0 else 0

        # Itera sobre cada item na Treeview que representa o carrinho de compras.
        for item in self.tabela.get_children():

            # Extrai os valores associados ao item selecionado da Treeview.
            valores = self.tabela.item(item, "values")

            # O código do produto está na primeira posição dos
            #       valores e é extraído diretamente.
            cod = valores[0]

            # Extrai o nome do produto da segunda coluna (índice 1) da linha no Treeview.
            nome = valores[1]  # Exemplo: "Arroz"

            # A quantidade é extraída da terceira posição dos valores,
            #       convertida para inteiro.
            qtd = int(valores[2])

            # Extrai o preço unitário da quarta coluna (índice 3), que está formatado como moeda (ex.: "R$ 10,00").
            # Remove o símbolo "R$" e substitui vírgulas por pontos para converter o valor para float.
            preco_unit = float(valores[3].replace("R$", "").replace(",", "."))  # Exemplo: 10.00

            # Calcula o subtotal multiplicando a quantidade pelo preço unitário.
            subtotal = preco_unit * qtd

            # Calcula o subtotal com o desconto aplicado, usando a
            #       porcentagem de desconto calculada anteriormente.
            subtotal_com_desconto = subtotal * (1 - desconto_porcentagem)

            # Busca o fornecedor no banco de dados, se necessário
            produto = colecao_produtos.find_one({"codigo": cod})

            # Verifica se o produto foi encontrado no banco de dados.
            if not produto:

                # Se o produto não for encontrado, define "Fornecedor Desconhecido" como valor padrão.
                fornecedor = "Fornecedor Desconhecido"

            else:

                # Se o produto for encontrado, extrai o fornecedor do campo correspondente no banco de dados.
                # Caso o campo "fornecedor" não exista, define "Fornecedor Desconhecido" como padrão.
                fornecedor = produto.get("fornecedor", "Fornecedor Desconhecido").strip()  # Remove espaços extras

            # Adiciona um dicionário com os detalhes do produto e o
            #       subtotal com desconto à lista de itens da venda.
            itens_venda.append({
                "codigo": cod,
                "nome": nome,
                "quantidade": qtd,
                "preco_unit": preco_unit,
                "subtotal_com_desconto": subtotal_com_desconto,
                "total_item": subtotal_com_desconto,
                "fornecedor": fornecedor,
            })

        # Calcula o total da venda somando os subtotais com
        #       desconto de cada item vendido.
        total = sum(item["subtotal_com_desconto"] for item in itens_venda)

        # Obtém o método de pagamento fornecido pelo usuário ou
        #       usa "Dinheiro" como padrão se nenhum foi especificado.
        metodo_pagamento = self.campo_pagamento.get() or "Dinheiro"

        # Registra a data e hora atuais da venda.
        data_venda = datetime.datetime.now()

        # Se o cliente forneceu um CPF, tenta atualizar o
        #       histórico de compras desse cliente.
        if cpf_cliente:

            # Busca o cliente pelo CPF/CNPJ fornecido no banco de dados.
            cliente = colecao_clientes.find_one({"cpf_cnpj": cpf_cliente})

            # Se encontrou um cliente com esse CPF/CNPJ:
            if cliente:

                # Obtém o histórico de compras do cliente ou cria uma
                        # lista vazia se não existir.
                historico = cliente.get("historico_compras", [])

                # Cria um dicionário com os detalhes da compra atual.
                nova_compra = {
                    "data": data_venda.strftime("%d/%m/%Y %H:%M"),  # Formata a data e hora da compra.
                    "itens": itens_venda,  # Lista de itens comprados.
                    "total": total,  # Total pago, considerando descontos.
                    "metodo_pagamento": metodo_pagamento,  # Método de pagamento utilizado.
                    "desconto": desconto,  # Valor do desconto aplicado.
                }

                # Adiciona a nova compra ao histórico do cliente.
                historico.append(nova_compra)

                # Atualiza o documento do cliente no banco de dados,
                #       definindo o novo histórico de compras.
                colecao_clientes.update_one(
                    {"cpf_cnpj": cpf_cliente},
                    {"$set": {"historico_compras": historico}}
                )

        # Atualizar o estoque
        # Itera sobre cada item vendido para atualizar a
        #       quantidade de produtos em estoque.
        for item in itens_venda:

            # Busca o produto correspondente no banco de dados pela chave 'codigo'.
            produto = colecao_produtos.find_one({"codigo": item["codigo"]})

            # Se o produto for encontrado:
            if produto:

                # Calcula a nova quantidade do produto subtraindo a quantidade
                #       vendida da quantidade atual em estoque.
                nova_quantidade = produto["quantidade"] - item["quantidade"]

                # Verifica se a nova quantidade é negativa, o que indicaria estoque insuficiente.
                if nova_quantidade < 0:

                    # Mostra uma mensagem de erro informando que há estoque
                    #       insuficiente para o produto e cancela a venda.
                    messagebox.showerror(
                        "Erro",
                        f"Estoque insuficiente para o produto {produto['nome']}. Venda cancelada.",
                        parent=self.root
                    )

                    # Encerra a função para não proceder com a atualização do estoque.
                    return

                # Se a quantidade é suficiente, atualiza a quantidade do
                #       produto no banco de dados.
                colecao_produtos.update_one(
                    {"codigo": item["codigo"]},
                    {"$set": {"quantidade": nova_quantidade}}
                )

        # Salva cada item da venda como um registro individual no banco de dados.
        for item in itens_venda:

            # Cria um dicionário com todos os detalhes relevantes da
            #       venda para ser armazenado.
            venda = {
                "data": data_venda,  # A data e hora da venda.
                "cliente_codigo": cpf_cliente if cpf_cliente else None,  # O CPF do cliente, se fornecido.
                "produto_codigo": item["codigo"],  # O código do produto vendido.
                "produto_nome": item["nome"],  # O nome do produto vendido.
                "quantidade": item["quantidade"],  # A quantidade do produto vendido.
                "preco_unit": item["preco_unit"],  # O preço unitário do produto.
                "subtotal_com_desconto": item["subtotal_com_desconto"],  # O subtotal após aplicar descontos.
                "total_item": item["subtotal_com_desconto"],
                "pagamento": metodo_pagamento,  # O método de pagamento usado.
                "desconto_total": desconto,  # O valor total de desconto aplicado à venda.
                "fornecedor": item["fornecedor"], # Salva o nome do fornecedor do produto, como especificado no banco de dados.
            }

            # Insere o registro da venda na coleção de vendas do banco de dados.
            colecao_vendas.insert_one(venda)

        # Criação da nota fiscal
        JanelaNotaFiscal(tk.Toplevel(self.root), {
            "data": data_venda,  # Data da venda, formatada adequadamente.
            "itens": itens_venda,  # Lista dos itens vendidos, incluindo detalhes como código, nome, quantidade, etc.
            "cpf_cliente": cpf_cliente if cpf_cliente else "Não informado",
            # CPF do cliente, ou indicativo de não fornecido.
            "total": total,  # Total da venda já com descontos aplicados.
            "desconto_total": desconto  # Total de desconto dado na venda.
        })

        # Limpa os campos
        self.campo_cpf.delete(0, tk.END)  # Limpa o campo de CPF.
        self.campo_codigo.delete(0, tk.END)  # Limpa o campo de código de barras.
        self.campo_desconto.delete(0, tk.END)  # Limpa o campo de desconto.
        self.campo_pagamento.delete(0, tk.END)  # Limpa o campo de método de pagamento.
        self.campo_pagamento.insert(0, "Dinheiro")  # Reinicia o campo de pagamento com o valor padrão "Dinheiro".

        self.carrinho.clear()  # Limpa a lista do carrinho de compras.
        self.tabela.delete(*self.tabela.get_children())  # Limpa todos os itens da tabela na interface gráfica.

        self.label_total.config(text="Total: R$ 0.00")  # Reseta o texto do total para R$0.00.

        # Exibe uma mensagem de sucesso ao finalizar a venda.
        # messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!", parent=self.root)


    def cancelar_venda(self):

        # Reseta o carrinho de compras, removendo todos os itens
        #       adicionados anteriormente.
        self.carrinho = []

        # Atualiza a tabela na interface gráfica para refletir o carrinho vazio.
        self.atualizar_tabela()

        # Limpa o campo de código de barras onde o usuário insere os códigos dos produtos.
        self.campo_codigo.delete(0, tk.END)

        # Limpa o campo de desconto, removendo qualquer valor que tenha sido inserido.
        self.campo_desconto.delete(0, tk.END)

        # Limpa o campo de método de pagamento.
        self.campo_pagamento.delete(0, tk.END)

        # Reinserindo o valor padrão "Dinheiro" no campo de método de pagamento.
        self.campo_pagamento.insert(0, "Dinheiro")

        # Exibe uma mensagem informando que a venda foi cancelada,
        #       utilizando um messagebox para a interação com o usuário.
        messagebox.showinfo("Cancelado", "A venda foi cancelada.", parent=self.root)


    def remover_item_selecionado(self):

        # Verifica se há algum item selecionado na tabela (carrinho).
        selecao = self.tabela.selection()
        if not selecao:

            # Exibe uma mensagem de erro se nenhum item for selecionado.
            messagebox.showerror("Erro", "Selecione um produto no carrinho.")
            return

        # Remove o item selecionado da Treeview, que visualmente
        #       representa o carrinho de compras.
        self.tabela.delete(selecao[0])

        # Chama a função para atualizar o total geral após a remoção do item.
        self.atualizar_total_geral()

        # Exibe uma mensagem informando que o produto foi removido com sucesso.
        messagebox.showinfo("Sucesso", "Produto removido do carrinho.")


    def alterar_quantidade_item(self):

        # Obter a seleção atual na Treeview, que contém os
        #       produtos no carrinho.
        selecao = self.tabela.selection()

        # Verificar se algum produto foi realmente selecionado.
        if not selecao:

            # Caso nenhum produto seja selecionado, exibir mensagem de erro.
            messagebox.showerror("Erro", "Selecione um produto no carrinho.", parent=self.root)
            return

        # Obter o item atualmente selecionado para manipulação.
        item = self.tabela.item(selecao[0])

        # Extrair os valores atuais do item selecionado na tabela.
        valores = item["values"]  # Pega os valores da linha selecionada
        cod = valores[0]  # Código do produto
        nome = valores[1]  # Nome do produto
        preco_unitario = float(

            # Converte o preço unitário para float após remover o símbolo de moeda
            valores[3].replace("R$", ""))

        # Solicita ao usuário uma nova quantidade para o produto selecionado.
        nova_qtd_str = simpledialog.askstring("Alterar Quantidade", "Informe a nova quantidade:")

        # Verifica se o usuário cancelou a entrada ou deixou o campo vazio.
        if not nova_qtd_str:

            # Sai da função sem fazer alterações.
            return

        try:

            # Tenta converter a entrada do usuário em um número inteiro.
            nova_qtd = int(nova_qtd_str)

            # Verifica se a nova quantidade é válida (maior que zero).
            if nova_qtd <= 0:

                # Exibe uma mensagem de erro se a quantidade for inválida.
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero.", parent=self.root)

                return  # Sai da função sem alterar a quantidade.

        except ValueError:

            # Exibe uma mensagem de erro se a entrada não puder ser
            #       convertida para um número inteiro.
            messagebox.showerror("Erro", "Quantidade inválida.")

            # Sai da função sem fazer alterações.
            return

        # Calcula o novo subtotal multiplicando a nova
        #       quantidade pelo preço unitário.
        subtotal = nova_qtd * preco_unitario

        # Atualiza a linha correspondente na Treeview com os novos valores.
        # 'selecao[0]' identifica a linha selecionada na tabela (Treeview).
        # 'values=(...)' substitui os valores antigos pelos novos, incluindo a
        #       nova quantidade e o subtotal atualizado.
        self.tabela.item(selecao[0], values=(

            cod,  # Código do produto, que permanece o mesmo.
            nome,  # Nome do produto, que também não muda.
            nova_qtd,  # Nova quantidade fornecida pelo usuário.
            f"R${preco_unitario:.2f}",  # Preço unitário formatado como moeda.
            f"R${subtotal:.2f}"  # Subtotal calculado e formatado como moeda.

        ))

        # Chama a função para atualizar o total geral da compra na interface.
        # Isso garante que o valor exibido no rótulo de total
        #       seja atualizado após a alteração.
        self.atualizar_total_geral()

        # Exibe uma mensagem de sucesso informando que a
        #       quantidade foi alterada com sucesso.
        messagebox.showinfo("Sucesso", "Quantidade alterada com sucesso.")


    def atualizar_total_geral(self):

        # Inicializa a variável total com 0.0, que será
        #       usada para somar os subtotais.
        total = 0.0

        # Itera sobre cada item presente na tabela (Treeview).
        # 'self.tabela.get_children()' retorna os IDs de todas as linhas da tabela.
        for item in self.tabela.get_children():

            # Obtém os valores de uma linha específica da tabela.
            # 'self.tabela.item(item, "values")' retorna os valores como uma tupla.
            valores = self.tabela.item(item, "values")

            # Extrai o subtotal do produto (5ª coluna) e converte de string para float.
            # Remove "R$" e substitui vírgulas por pontos para que a conversão funcione.
            subtotal = float(valores[4].replace("R$", "").replace(",", "."))

            # Adiciona o subtotal ao total acumulado.
            total += subtotal

        # Atualiza o texto do rótulo que exibe o total geral.
        # 'text=f"Total: R$ {total:.2f}"' formata o total com duas
        #       casas decimais no formato monetário.
        self.label_total.config(text=f"Total: R$ {total:.2f}")


    def sincronizar_carrinho_com_treeview(self):

        # Limpa o carrinho atual.
        # Remove todos os itens da lista `self.carrinho` para
        #       garantir que a sincronização com a Treeview seja feita
        #       de forma precisa e sem duplicações.
        self.carrinho.clear()

        # Itera sobre todas as linhas da tabela (Treeview).
        # `self.tabela.get_children()` retorna uma lista de IDs de
        #       todas as linhas na Treeview.
        for item in self.tabela.get_children():

            # Obtém os valores da linha correspondente usando o ID retornado pelo `get_children`.
            # `self.tabela.item(item, "values")` retorna os valores das colunas como uma tupla.
            valores = self.tabela.item(item, "values")

            # Extrai o código do produto (1ª coluna) da tupla de valores.
            cod = valores[0]

            # Extrai o nome do produto (2ª coluna) da tupla de valores.
            nome = valores[1]

            # Extrai a quantidade do produto (3ª coluna) da tupla e
            #       converte para inteiro.
            qtd = int(valores[2])

            # Extrai o preço unitário (4ª coluna) da tupla, remove "R$" e converte para float.
            preco_unit = float(valores[3].replace("R$", ""))

            # Adiciona os dados do produto ao carrinho na forma de uma tupla.
            # Cada item do carrinho contém: código, quantidade, preço unitário e nome.
            self.carrinho.append((cod, qtd, preco_unit, nome))





############################################
# Janela de Login
############################################

# Define a classe `JanelaLogin`, responsável por gerenciar a
#       tela de login do sistema.
class JanelaLogin:

    # Método construtor que inicializa a janela de login.
    def __init__(self, root):

        # Recebe o objeto `root` (janela principal) do Tkinter e o
        #       atribui a `self.root`.
        self.root = root

        # Configura o título da janela principal para "Login - Sistema de Supermercado".
        self.root.title("Login - Sistema de Supermercado")

        # Define o estado da janela principal como "zoomed", fazendo
        #       com que a janela abra em tela cheia.
        self.root.state('zoomed')

        # Configuração de estilos para os widgets da interface gráfica.
        estilo = ttk.Style()  # Cria uma instância de estilo para aplicar aos widgets.

        # Configura o estilo para os rótulos (`TLabel`), definindo a
        #       fonte como Arial de tamanho 16.
        estilo.configure("TLabel",
                         font=("Arial", 16))

        # Configura o estilo para os campos de entrada (`TEntry`),
        #       definindo a fonte como Arial de tamanho 16.
        estilo.configure("TEntry",
                         font=("Arial", 16))

        # Configura o estilo para os botões (`TButton`), definindo a
        #       fonte como Arial de tamanho 16 em negrito e aplicando um
        #       preenchimento (padding) de 10 pixels.
        estilo.configure("TButton",
                         font=("Arial", 16, "bold"),
                         padding=10)

        # Frame principal
        # Cria um frame principal dentro da janela principal (`root`)
        #       para organizar os elementos da interface.
        # O frame tem um padding de 20 pixels ao redor para espaçamento interno.
        self.frame = ttk.Frame(root,
                               padding=20)

        # Posiciona o frame principal para preencher todo o espaço disponível,
        #       expandindo tanto na largura quanto na altura.
        self.frame.pack(expand=True,
                        fill=tk.BOTH)

        # Fundo colorido
        # Configura a cor de fundo da janela principal (`root`) para um
        #       tom claro de cinza (#F0F0F0).
        self.root.configure(bg="#F0F0F0")

        # Subframe centralizado
        # Cria um subframe dentro do frame principal para agrupar elementos
        #       específicos, como campos de entrada e botões.
        # O subframe possui um padding interno de 20 pixels, bordas com
        #       estilo "ridge" (relevo) e estilo `TFrame`.
        self.subframe = ttk.Frame(self.frame,
                                  padding=20,
                                  relief="ridge",
                                  style="TFrame")

        # Posiciona o subframe no centro da janela, utilizando coordenadas
        #       relativas (`relx=0.5` e `rely=0.5`) e alinhando-o pelo
        #       centro com o parâmetro `anchor="center"`.
        self.subframe.place(relx=0.5,
                            rely=0.5,
                            anchor="center")

        # Criação do rótulo de boas-vindas
        # Adiciona um rótulo (label) no subframe com a mensagem "Bem-vindo
        #       ao Sistema de Supermercado".
        # O texto está formatado com a fonte Arial, tamanho 24, em negrito.
        # O rótulo é centralizado (`anchor="center"`) e ocupa duas colunas (`columnspan=2`).
        # O espaçamento vertical inferior do rótulo é configurado para 20 pixels com `pady=(0, 20)`.
        ttk.Label(
            self.subframe,
            text="Bem-vindo ao Sistema de Supermercado",
            font=("Arial", 24, "bold"),
            anchor="center",
        ).grid(row=0,
               column=0,
               columnspan=2,
               pady=(0, 20))

        # Rótulo para o campo "Usuário"
        # Adiciona um rótulo no subframe indicando onde o usuário deve
        #       digitar seu nome de usuário.
        # O rótulo está posicionado na segunda linha (`row=1`) e na primeira coluna (`column=0`) da grade.
        # Um espaçamento horizontal de 10 pixels é adicionado em ambos os lados com `padx=10`.
        # Um espaçamento vertical de 10 pixels é adicionado em cima e embaixo com `pady=10`.
        # O texto é alinhado à direita dentro da célula com `sticky="e"`.
        ttk.Label(self.subframe,
                  text="Usuário:").grid(row=1,
                                        column=0,
                                        padx=10,
                                        pady=10,
                                        sticky="e")

        # Campo de entrada para o "Usuário"
        # Cria um campo de entrada (Entry) no subframe para o usuário digitar seu nome de usuário.
        # O campo é armazenado na variável de instância `self.campo_usuario` para referência posterior.
        # O campo está posicionado na segunda linha (`row=1`) e na segunda coluna (`column=1`) da grade.
        # Um espaçamento horizontal de 10 pixels é adicionado em ambos os lados com `padx=10`.
        # Um espaçamento vertical de 10 pixels é adicionado em cima e embaixo com `pady=10`.
        # O campo é configurado para se expandir horizontalmente dentro da célula com `sticky="we"`.
        self.campo_usuario = ttk.Entry(self.subframe)
        self.campo_usuario.grid(row=1,
                                column=1,
                                padx=10,
                                pady=10,
                                sticky="we")

        # Rótulo para o campo "Senha"
        # Adiciona um rótulo no subframe indicando onde o usuário deve digitar sua senha.
        # O texto "Senha:" serve como orientação para o campo de entrada.
        # Este rótulo está posicionado na terceira linha (`row=2`) e na
        #       primeira coluna (`column=0`) da grade.
        # Um espaçamento horizontal de 10 pixels é adicionado com `padx=10`, e
        #       um espaçamento vertical de 10 pixels com `pady=10`.
        # O texto é alinhado à direita dentro da célula com `sticky="e"`.
        ttk.Label(self.subframe,
                  text="Senha:").grid(row=2,
                                      column=0,
                                      padx=10,
                                      pady=10,
                                      sticky="e")

        # Campo de entrada para "Senha"
        # Cria um campo de entrada (Entry) no subframe para o usuário digitar sua senha.
        # O atributo `show="*"` substitui os caracteres digitados por asteriscos,
        #       ocultando a senha do usuário.
        # Este campo é armazenado na variável de instância `self.campo_senha`
        #       para referência posterior.
        # O campo está posicionado na terceira linha (`row=2`) e na
        #       segunda coluna (`column=1`) da grade.
        # Um espaçamento horizontal de 10 pixels é adicionado com `padx=10`, e um
        #       espaçamento vertical de 10 pixels com `pady=10`.
        # O campo é configurado para se expandir horizontalmente
        #       dentro da célula com `sticky="we"`.
        self.campo_senha = ttk.Entry(self.subframe, show="*")
        self.campo_senha.grid(row=2,
                              column=1,
                              padx=10,
                              pady=10,
                              sticky="we")

        # Botão "Login"
        # Cria um botão no subframe com o texto "Login", que executa o
        #       método `self.fazer_login` quando clicado.
        # Este botão está posicionado na quarta linha (`row=3`) e ocupa
        #       duas colunas (`columnspan=2`) da grade.
        # Um espaçamento vertical de 20 pixels é adicionado abaixo do botão com `pady=20`.
        self.botao_login = ttk.Button(self.subframe,
                                      text="Login",
                                      command=self.fazer_login)
        self.botao_login.grid(row=3,
                              column=0,
                              columnspan=2,
                              pady=20)

        # Botão "Cadastro"
        # Cria um botão no subframe com o texto "Não tem conta? Cadastre-se",
        #       que redireciona o usuário para a tela de cadastro ao ser clicado.
        # O método `self.ir_para_cadastro` é executado quando o botão é pressionado.
        # O botão utiliza o estilo "Accent.TButton" para um design diferenciado.
        # Está posicionado na quinta linha (`row=4`) e ocupa duas colunas (`columnspan=2`) da grade.
        # Um espaçamento vertical de 10 pixels é adicionado abaixo do botão com `pady=10`.
        self.botao_cadastro = ttk.Button(
            self.subframe,
            text="Não tem conta? Cadastre-se",
            command=self.ir_para_cadastro,
            style="Accent.TButton",
        )

        # Configuração do botão "Cadastro"
        # Posiciona o botão "Não tem conta? Cadastren-se" no subframe.
        # O botão é colocado na quinta liha (`row=4`) e ocupa duas
        #       colunas (`columnspan=2`), centralizando-o na interface.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels abaixo do botão.
        self.botao_cadastro.grid(row=4,
                                 column=0,
                                 columnspan=2,
                                 pady=10)

        # Configuração da coluna no subframe
        # Configura a segunda coluna (`column=1`) do subframe para expandir
        #       proporcionalmente, garantindo alinhamento e responsividade.
        # O peso (`weight=1`) determina que esta coluna ocupará mais
        #       espaço quando o tamanho do subframe for ajustado.
        self.subframe.columnconfigure(1,
                                      weight=1)


    def fazer_login(self):

        # Obtém o valor do campo de entrada do usuário e remove
        #       espaços em branco das extremidades.
        usuario = self.campo_usuario.get().strip()

        # Obtém o valor do campo de entrada da senha e remove espaços
        #       em branco das extremidades.
        senha = self.campo_senha.get().strip()

        # Verifica as credenciais do usuário através da função `verificar_login`,
        #       que retorna os dados do usuário se forem válidos.
        u = verificar_login(usuario, senha)

        # Se as credenciais forem válidas (usuário encontrado):
        if u:

            # Exibe uma mensagem de sucesso com o nome do usuário logado.
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario}!", parent=self.root)

            # Fecha a janela de login.
            self.root.destroy()

            # Cria a janela principal do sistema (caixa).
            root_caixa = tk.Tk()

            # Inicializa a janela do caixa, passando os dados do usuário logado.
            JanelaCaixa(root_caixa, u)

            # Inicia o loop principal da interface gráfica para a janela do caixa.
            root_caixa.mainloop()

        else:

            # Exibe uma mensagem de erro caso o login não seja
            #       válido (usuário ou senha incorretos).
            messagebox.showerror("Erro", "Usuário ou senha inválidos.", parent=self.root)




    """Abre a tela de gerenciamento de funcionários para cadastro."""

    def ir_para_cadastro(self):

        # Exibe uma mensagem informando ao usuário que ele será
        #       redirecionado para a tela de funcionários.
        messagebox.showinfo(
            "Cadastro",
            "Você será redirecionado para a tela de funcionários.",
            parent=self.root
        )

        # Cria uma nova janela principal para o cadastro de funcionários.
        root_cadastro = tk.Tk()

        # Inicializa a janela de gerenciamento de funcionários para o cadastro.
        JanelaFuncionarios(root_cadastro)

        # Inicia o loop principal da interface gráfica para a nova janela.
        root_cadastro.mainloop()



# Cria a janela principal para o login.
login_root = tk.Tk()

# Inicializa a interface de login.
JanelaLogin(login_root)

# Inicia o loop principal da interface gráfica.
login_root.mainloop()