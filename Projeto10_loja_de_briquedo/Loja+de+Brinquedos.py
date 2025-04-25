# Importa a biblioteca Tkinter para criar interfaces gráficas
import tkinter as tk
from mailbox import mboxMessage

# Importa componentes avançados do Tkinter:
# ttk -> permite usar widgets mais modernos como Treeview e Combobox
# messagebox -> fornece caixas de diálogo para exibir mensagens ao usuário
from tkinter import ttk, messagebox

import pandas as pd

# Importa a biblioteca pymongo para se conectar ao banco de dados MongoDB
import pymongo
from PIL.ImageOps import expand

# Importa a classe ObjectId do módulo bson, usada para manipular
#       identificadores únicos (_id) do MongoDB
from bson.objectid import ObjectId

# Importa o módulo datetime para trabalhar com datas e horários
import datetime

# Importa o módulo hashlib, que permite gerar hash de senhas
#       para armazenamento seguro
import hashlib

# Importa a configuração de páginas do ReportLab, usada para
#       gerar PDFs no tamanho A4
from reportlab.lib.pagesizes import A4
from reportlab.lib.randomtext import verbs

# Importa a classe canvas do ReportLab, que permite desenhar e
#       criar documentos PDF
from reportlab.pdfgen import canvas

# Importa a unidade de medida 'cm' do ReportLab para facilitar a
#       formatação de espaçamentos e margens no PDF
from reportlab.lib.units import cm
from urllib3 import proxy_from_url


###############################################################################
# FUNÇÕES AUXILIARES PARA DATAS (FORMATO BRASILEIRO)
###############################################################################

# Função para converter uma string de data/hora no formato ISO 8601
#       (usado no MongoDB) para um objeto de data (datetime.date)
def converter_iso_para_date(iso_str):

    """
    Esta função recebe uma string no formato ISO 8601, por exemplo:
    '2023-08-27T14:35:22.000Z', onde:
        - '2023-08-27' representa a data (ano-mês-dia)
        - 'T' é apenas um separador entre a data e a hora
        - '14:35:22.000Z' representa a hora, minutos, segundos e milissegundos (que serão ignorados)

    O objetivo da função é extrair apenas a data e convertê-la para um objeto `datetime.date`.

    Retorna:
        - Um objeto `datetime.date(ano, mês, dia)` se a conversão for bem-sucedida.
        - `None` se a string for vazia ou inválida.
    """

    # Verifica se a string recebida é vazia ou None (nula).
    # Caso seja, retorna None, pois não há nada para converter.
    if not iso_str:
        return None

    # Divide a string no caractere 'T', separando a parte da data da parte do horário.
    # Exemplo: '2023-08-27T14:35:22.000Z' -> ['2023-08-27', '14:35:22.000Z']
    # Pegamos apenas a primeira parte, que contém a data: '2023-08-27'
    parte_data = iso_str.split("T")[0]

    try:

        # Divide a string da data no caractere '-' para separar ano, mês e dia
        # Exemplo: '2023-08-27' -> ['2023', '08', '27']
        ano, mes, dia = parte_data.split("-")

        # Converte as partes para inteiros e cria um objeto datetime.date
        return datetime.date(int(ano), int(mes), int(dia))

    # Se houver erro (por exemplo, se a string não estiver no
    #       formato esperado), captura a exceção
    except:

        # Retorna None indicando que a conversão falhou
        return None


# Função para converter um objeto `datetime.date` para uma
#       string no formato brasileiro 'dd/mm/aaaa'
def converter_date_para_str_br(data_obj):

    """
    Converte um objeto `datetime.date` para uma string formatada no
            padrão brasileiro 'dd/mm/aaaa'.

    Entrada:
        - data_obj: Um objeto do tipo `datetime.date`.

    Retorno:
        - Uma string formatada como 'dd/mm/aaaa' se `data_obj` for válido.
        - Uma string vazia ("") se `data_obj` for None.
    """

    # Verifica se `data_obj` não é nulo (None)
    # Se for None, retorna uma string vazia (""), pois não há data para converter
    if not data_obj:
        return ""

    # Retorna a data formatada no estilo brasileiro 'dd/mm/aaaa'
    # Usamos f-strings para formatar os valores:
    # - `data_obj.day:02d` garante que o dia sempre tenha 2 dígitos (ex: 01, 02, ..., 31)
    # - `data_obj.month:02d` garante que o mês sempre tenha 2 dígitos (ex: 01, 02, ..., 12)
    # - `data_obj.year` exibe o ano com 4 dígitos (ex: 2025)
    return f"{data_obj.day:02d}/{data_obj.month:02d}/{data_obj.year}"


# Função que converte uma string de data no formato
#       brasileiro 'dd/mm/aaaa' para um objeto `datetime.date`
def analisar_data_br(data_str):

    """
    Recebe uma string de data no formato brasileiro 'dd/mm/aaaa' e
            a converte para um objeto `datetime.date`.

    Entrada:
        - data_str: Uma string representando a data no
                formato 'dd/mm/aaaa' (ex: "27/08/2023").

    Retorno:
        - Um objeto `datetime.date` correspondente à data
                fornecida, se a conversão for bem-sucedida.
        - None, caso a string esteja vazia ou tenha um formato inválido.
    """

    # Remove espaços em branco extras no início e no final da
    #       string, garantindo que ela esteja limpa.
    data_str = data_str.strip()

    # Verifica se a string está vazia após a remoção dos espaços.
    # Se estiver vazia, retorna `None`, pois não há data para converter.
    if not data_str:
        return None

    try:

        # Divide a string nos três componentes da data: dia, mês e ano.
        # A string "27/08/2023" será separada em ["27", "08", "2023"].
        dia, mes, ano = data_str.split("/")

        # Converte cada parte para um número inteiro e cria um objeto `datetime.date`.
        return datetime.date(int(ano), int(mes), int(dia))

    except:

        # Se houver um erro (exemplo: a string não estiver no formato correto),
        #       a função retorna `None`, indicando que a conversão falhou.
        return None



###############################################################################
# CLASSE DE GERENCIAMENTO DO BANCO DE DADOS (MongoDB)
###############################################################################

# Importa a biblioteca pymongo para conectar e interagir com o MongoDB
class GerenciadorBanco:

    """
    Classe para gerenciar a conexão e interação com um banco de dados MongoDB.

    - Conecta ao banco de dados MongoDB usando pymongo.
    - Define coleções para armazenar diferentes tipos de dados, como
            usuários, fornecedores, produtos, clientes e vendas.

    Parâmetros:
    ----------
    - uri (str): URI do MongoDB para conexão (padrão: "mongodb://localhost:27017").
    - nome_banco (str): Nome do banco de dados a ser utilizado (padrão: "loja_brinquedos").
    """

    def __init__(self, uri="mongodb://localhost:27017", nome_banco="loja_brinquedos"):

        """
        Método construtor da classe.

        Parâmetros:
        ----------
        - uri (str): Endereço do MongoDB (padrão: "mongodb://localhost:27017").
        - nome_banco (str): Nome do banco de dados (padrão: "loja_brinquedos").
        """

        # Cria uma conexão com o servidor MongoDB usando a URI fornecida.
        # Se o MongoDB estiver rodando localmente, a URI
        #       padrão "mongodb://localhost:27017" será usada.
        self.cliente = pymongo.MongoClient(uri)

        # Acessa o banco de dados com o nome especificado.
        # Se o banco não existir, o MongoDB criará automaticamente
        #       quando um dado for inserido.
        self.banco = self.cliente[nome_banco]

        # Define coleções dentro do banco de dados para armazenar
        #       diferentes tipos de informações.

        # Coleção para armazenar dados dos usuários do sistema.
        self.col_usuarios = self.banco["usuarios"]

        # Coleção para armazenar informações dos fornecedores de brinquedos.
        self.col_fornecedores = self.banco["fornecedores"]

        # Coleção para armazenar os produtos disponíveis na loja.
        self.col_produtos = self.banco["produtos"]

        # Coleção para armazenar informações dos clientes.
        self.col_clientes = self.banco["clientes"]

        # Coleção para armazenar as vendas realizadas pela loja.
        self.col_vendas = self.banco["vendas"]

    # Converte a senha para um formato seguro usando SHA-256.
    # O algoritmo SHA-256 gera um hash de 256 bits, tornando a
    #       senha ilegível para terceiros.
    def gerar_hash_senha(self, senha):

        # `senha.encode("utf-8")` transforma a string em bytes,
        #       pois o SHA-256 requer entrada binária.
        # UTF-8 é um formato de codificação de caracteres que
        #       suporta caracteres especiais.
        hash_objeto = hashlib.sha256(senha.encode("utf-8"))

        # `.hexdigest()` converte o hash gerado para uma string hexadecimal legível.
        # Isso facilita o armazenamento e a comparação do hash.
        return hash_objeto.hexdigest()

    # Autentica um usuário no sistema.
    # `usuario` é uma string contendo o nome do usuário.
    # `senha` é uma string contendo a senha fornecida pelo usuário.
    # Retorna o documento do usuário se a autenticação for
    #       bem-sucedida, ou `None` se falhar.
    def autenticar_usuario(self, usuario, senha):

        # Converte a senha fornecida em um hash SHA-256.
        # `self.gerar_hash_senha(senha)` transforma a senha em um
        #       código seguro antes da verificação.
        senha_hash = self.gerar_hash_senha(senha)

        # Busca no banco de dados um usuário que tenha o nome de usuário e a
        #       senha criptografada correspondente.
        # `self.col_usuarios.find_one({...})` consulta a coleção "usuarios" no banco MongoDB.
        # O filtro `{"usuario": usuario, "senha": senha_hash}` verifica se
        #       existe um usuário com essas credenciais.
        doc_usuario = self.col_usuarios.find_one({"usuario": usuario, "senha": senha_hash})

        # Retorna o documento do usuário caso encontrado.
        # Se nenhum usuário correspondente for encontrado, retorna `None`.
        return doc_usuario

    # Cria um novo usuário no banco de dados.
    # `nome` é uma string contendo o nome completo do usuário.
    # `usuario` é uma string contendo o nome de usuário que será usado para login.
    # `senha` é uma string contendo a senha fornecida pelo usuário.
    # `permissao` é uma string que define o nível de acesso do usuário.
    # Retorna uma tupla `(True, "Usuário criado com sucesso!")` se o
    #       usuário for cadastrado corretamente.
    # Se o nome de usuário já existir no banco, retorna `(False, "Usuário já existe!")`.
    def criar_usuario(self, nome, usuario, senha, permissao):

        # Verifica se o nome de usuário já existe no banco de dados.
        # `self.col_usuarios.find_one({"usuario": usuario})` busca um
        #       documento com o mesmo nome de usuário.
        if self.col_usuarios.find_one({"usuario": usuario}):

            # Se já existir um usuário com esse nome, retorna `False` e
            #       uma mensagem de erro.
            return False, "Usuário já existe!"

        # Gera um hash seguro para a senha antes de armazená-la no banco de dados.
        # `self.gerar_hash_senha(senha)` converte a senha em um
        #       formato criptografado (SHA-256).
        senha_cripto = self.gerar_hash_senha(senha)

        # Insere o novo usuário na coleção `usuarios` do MongoDB.
        # `insert_one({...})` adiciona um documento com os dados do novo usuário.
        self.col_usuarios.insert_one({
            "nome": nome,  # Armazena o nome completo do usuário.
            "usuario": usuario,  # Armazena o nome de usuário.
            "senha": senha_cripto,  # Armazena a senha criptografada.
            "permissao": permissao  # Armazena a permissão do usuário.
        })

        # Retorna `True` e uma mensagem informando que o usuário
        #       foi criado com sucesso.
        return True, "Usuário criado com sucesso!"

    # Recupera todos os usuários cadastrados no banco de dados.
    # Retorna uma lista contendo todos os documentos armazenados
    #       na coleção `usuarios`.
    def listar_usuarios(self):

        # `self.col_usuarios.find({})` busca todos os documentos na coleção.
        # `list(...)` converte o cursor do MongoDB em uma lista de dicionários.
        return list(self.col_usuarios.find({}))

    # Remove um usuário do banco de dados com base no seu ID.
    # `id_usuario` é uma string contendo o identificador único do usuário no banco.
    # Essa função não retorna nenhum valor.
    def remover_usuario(self, id_usuario):

        # `self.col_usuarios.delete_one(...)` remove um documento
        #       específico da coleção `usuarios`.
        # `{"_id": ObjectId(id_usuario)}` define o critério de busca
        #       para remover apenas o usuário com o ID correspondente.
        self.col_usuarios.delete_one({"_id": ObjectId(id_usuario)})

    # Atualiza as informações de um usuário no banco de dados.
    # `id_usuario` é o identificador único do usuário no banco (em formato string).
    # `nome` é o novo nome do usuário.
    # `usuario` é o novo nome de usuário (login).
    # `nova_senha` é a nova senha, caso o usuário deseje alterá-la.
    # `permissao` define o nível de acesso do usuário.
    def atualizar_usuario(self, id_usuario, nome, usuario, nova_senha, permissao):

        # Cria um dicionário contendo os campos a serem atualizados.
        campos = {
            "nome": nome,  # Atualiza o nome do usuário.
            "usuario": usuario,  # Atualiza o nome de usuário (login).
            "permissao": permissao  # Atualiza a permissão do usuário.
        }

        # Verifica se a nova senha foi informada (não está vazia).
        if nova_senha.strip():

            # Se a senha foi informada, ela é criptografada e
            #       adicionada ao dicionário de atualização.
            campos["senha"] = self.gerar_hash_senha(nova_senha)

        # Atualiza o usuário no banco de dados.
        # `update_one` busca pelo usuário com o `_id` fornecido e aplica as alterações.
        # O operador `$set` garante que apenas os campos especificados sejam atualizados.
        self.col_usuarios.update_one(

            # Filtro para encontrar o usuário pelo ID.
            {"_id": ObjectId(id_usuario)},

            # Campos que serão atualizados no documento correspondente.
            {"$set": campos}

        )


    # -------------------------------------------------------------------------
    # CRUD Fornecedores
    # -------------------------------------------------------------------------

    # Cadastra um novo fornecedor no banco de dados.
    # `nome` representa o nome do fornecedor.
    # `cnpj` é o Cadastro Nacional de Pessoa Jurídica do fornecedor.
    # `telefone` é o número de contato do fornecedor.
    # `email` é o endereço de e-mail do fornecedor.
    # `endereco` é o local onde o fornecedor está localizado.
    def cadastrar_fornecedor(self, nome, cnpj, telefone, email, endereco):

        # Insere um novo fornecedor na coleção 'fornecedores' do banco de dados.
        # Os dados são armazenados como um documento JSON contendo os seguintes campos:
        self.col_fornecedores.insert_one({
            "nome": nome,  # Nome do fornecedor.
            "cnpj": cnpj,  # CNPJ do fornecedor.
            "telefone": telefone,  # Número de telefone do fornecedor.
            "email": email,  # Endereço de e-mail do fornecedor.
            "endereco": endereco  # Endereço físico do fornecedor.
        })

    # Define um método para listar todos os fornecedores
    #       cadastrados no banco de dados.
    # Retorna uma lista de dicionários contendo os fornecedores.
    def listar_fornecedores(self):

        # Executa a consulta no banco de dados para buscar todos os
        #       fornecedores cadastrados.
        return list(self.col_fornecedores.find({}))

    # Atualiza os dados de um fornecedor existente no banco de dados.
    # `id_forn`: Identificador único do fornecedor a ser atualizado.
    # `nome`: Novo nome do fornecedor.
    # `cnpj`: Novo CNPJ do fornecedor.
    # `telefone`: Novo número de telefone do fornecedor.
    # `email`: Novo endereço de e-mail do fornecedor.
    # `endereco`: Novo endereço físico do fornecedor.
    def atualizar_fornecedor(self, id_forn, nome, cnpj, telefone, email, endereco):

        # Atualiza o fornecedor na coleção 'fornecedores' do banco de dados.
        self.col_fornecedores.update_one(
            {"_id": ObjectId(id_forn)},  # Filtra pelo ID único do fornecedor.
            {"$set": {  # Define os novos valores dos campos do fornecedor.
                "nome": nome,  # Atualiza o nome do fornecedor.
                "cnpj": cnpj,  # Atualiza o CNPJ do fornecedor.
                "telefone": telefone,  # Atualiza o telefone do fornecedor.
                "email": email,  # Atualiza o e-mail do fornecedor.
                "endereco": endereco  # Atualiza o endereço do fornecedor.
            }}
        )

    # Define um método para excluir um fornecedor do banco de dados.
    # Recebe o ID do fornecedor como parâmetro e remove o registro correspondente.
    def excluir_fornecedor(self, id_forn):

        # Converte o ID fornecido para ObjectId e executa a exclusão
        #       do fornecedor no banco de dados.
        self.col_fornecedores.delete_one({"_id": ObjectId(id_forn)})

    # -------------------------------------------------------------------------
    # CRUD Produtos
    # -------------------------------------------------------------------------

    # Define um método para cadastrar um novo produto no banco de dados.
    # Recebe os detalhes do produto como parâmetros e insere no banco de dados.
    def cadastrar_produto(self, codigo, nome, descricao, categoria, preco_compra, preco_venda, quantidade, id_forn):

        # Insere um novo produto na coleção de produtos do banco de dados.
        self.col_produtos.insert_one({

            # Código único do produto.
            "codigo": codigo,

            # Nome do produto.
            "nome": nome,

            # Descrição detalhada do produto.
            "descricao": descricao,

            # Categoria a que o produto pertence.
            "categoria": categoria,

            # Preço de compra do produto.
            "preco_compra": preco_compra,

            # Preço de venda do produto.
            "preco_venda": preco_venda,

            # Quantidade do produto disponível no estoque.
            "quantidade_estoque": quantidade,

            # Identificador do fornecedor associado ao produto,
            #       convertido para ObjectId.
            "fornecedor_id": ObjectId(id_forn)

        })


    # Define um método para listar produtos do banco de dados.
    # Permite opcionalmente aplicar um filtro para buscar produtos
    #       pelo nome, categoria ou código.
    def listar_produtos(self, filtro=None):

        # Inicializa um dicionário vazio para a consulta.
        consulta = {}

        # Se um filtro for passado, cria uma expressão regular para
        #       busca parcial e case insensitive.
        if filtro:
            rgx = {"$regex": filtro, "$options": "i"}

            # Define a consulta para buscar produtos cujo nome, categoria ou
            #       código correspondam ao filtro.
            consulta = {
                "$or": [
                    {"nome": rgx},  # Busca pelo nome do produto.
                    {"categoria": rgx},  # Busca pela categoria do produto.
                    {"codigo": rgx}  # Busca pelo código do produto.
                ]
            }

        # Retorna uma lista com os produtos encontrados na
        #       coleção 'produtos' do banco de dados.
        return list(self.col_produtos.find(consulta))


    # Define um método para atualizar as informações de um produto no banco de dados.
    # Requer o ID do produto e os novos valores para os campos do produto.
    def atualizar_produto(self, id_prod, codigo, nome, descricao, categoria,
                          preco_compra, preco_venda, quantidade, id_forn):

        # Executa a atualização no banco de dados, identificando o produto pelo seu ID.
        self.col_produtos.update_one(

            # Filtra pelo ID do produto.
            {"_id": ObjectId(id_prod)},

            # Define os novos valores para os campos do produto.
            {"$set": {
                "codigo": codigo,  # Atualiza o código do produto.
                "nome": nome,  # Atualiza o nome do produto.
                "descricao": descricao,  # Atualiza a descrição do produto.
                "categoria": categoria,  # Atualiza a categoria do produto.
                "preco_compra": preco_compra,  # Atualiza o preço de compra do produto.
                "preco_venda": preco_venda,  # Atualiza o preço de venda do produto.
                "quantidade_estoque": quantidade,  # Atualiza a quantidade em estoque.
                "fornecedor_id": ObjectId(id_forn)  # Atualiza o ID do fornecedor do produto.
            }}
        )

    # Define um método para excluir um produto do banco de dados.
    # Requer o ID do produto que será removido.
    def excluir_produto(self, id_prod):

        # Exclui um produto do banco de dados.
        # `id_prod` é o identificador único do produto a ser removido.
        self.col_produtos.delete_one({"_id": ObjectId(id_prod)})


    # -------------------------------------------------------------------------
    # CRUD Clientes
    # -------------------------------------------------------------------------

    # Define um método para cadastrar um novo cliente no banco de dados.
    # Recebe os dados do cliente (nome, CPF, telefone, e-mail e endereço) como parâmetros.
    def cadastrar_cliente(self, nome, cpf, telefone, email, endereco):

        # Insere um novo cliente na coleção 'clientes' do banco de dados.f
        # O cliente será armazenado com nome, CPF, telefone, e-mail e endereço.
        self.col_clientes.insert_one({
            "nome": nome,  # Define o nome do cliente.
            "cpf": cpf,  # Define o CPF do cliente.
            "telefone": telefone,  # Define o telefone do cliente.
            "email": email,  # Define o e-mail do cliente.
            "endereco": endereco  # Define o endereço do cliente.
        })

    # Retorna uma lista com todos os clientes cadastrados no banco de dados.
    # Não recebe parâmetros e retorna uma lista de dicionários contendo os clientes.
    def listar_clientes(self):

        # Retorna uma lista contendo todos os clientes encontrados no banco de dados.
        return list(self.col_clientes.find({}))

    # Atualiza os dados de um cliente existente no banco de dados.
    # Recebe o ID do cliente, nome, CPF, telefone, e-mail e endereço como parâmetros.
    def atualizar_cliente(self, id_cl, nome, cpf, telefone, email, endereco):

        # Realiza a atualização dos dados do cliente no banco
        #       com base no ID fornecido.
        self.col_clientes.update_one(
            {"_id": ObjectId(id_cl)},  # Filtra o cliente pelo ID.
            {"$set": {
                "nome": nome,  # Atualiza o nome do cliente.
                "cpf": cpf,  # Atualiza o CPF do cliente.
                "telefone": telefone,  # Atualiza o telefone do cliente.
                "email": email,  # Atualiza o e-mail do cliente.
                "endereco": endereco  # Atualiza o endereço do cliente.
            }}
        )

    # Exclui um cliente do banco de dados com base no ID fornecido.
    # Recebe o ID do cliente como parâmetro e remove o registro correspondente.
    def excluir_cliente(self, id_cl):

        # Executa a exclusão do cliente no banco de dados pelo seu ID único.
        self.col_clientes.delete_one({"_id": ObjectId(id_cl)})



    # -------------------------------------------------------------------------
    # OPERAÇÕES DE VENDAS
    # -------------------------------------------------------------------------


    # Registra uma nova venda no banco de dados.
    # `itens` é uma lista contendo os produtos vendidos e suas quantidades.
    # `total` representa o valor total da venda.
    # `forma_pagamento` indica como o cliente pagou (ex.: dinheiro, cartão).
    # `id_vendedor` é o identificador do vendedor responsável pela venda.
    # `id_cliente` é o identificador do cliente que realizou a compra.
    def registrar_venda(self, itens, total, forma_pagamento, id_vendedor, id_cliente):

        # Obtém a data e hora atuais no formato ISO 8601.
        # Isso permite registrar quando a venda foi feita com precisão.
        data_e_hora = datetime.datetime.now().isoformat()

        # Percorre a lista de itens vendidos para atualizar o estoque.
        # Cada item contém um 'produto_id' e a quantidade vendida.
        for item in itens:

            # Atualiza o banco de dados reduzindo a quantidade do
            #       produto vendido no estoque.
            # `"_id": ObjectId(item["produto_id"])` encontra o produto
            #       pelo seu identificador.
            # `"$inc": {"quantidade_estoque": -item["quantidade"]}`
            #       subtrai a quantidade vendida do estoque.
            self.col_produtos.update_one(
                {"_id": ObjectId(item["produto_id"])},
                {"$inc": {"quantidade_estoque": -item["quantidade"]}}
            )

        # Cria um dicionário contendo os detalhes da venda.
        # "data_hora" armazena a data e hora da venda no formato ISO 8601.
        # "itens" guarda a lista de produtos vendidos com suas quantidades.
        # "total" representa o valor total da compra.
        # "forma_pagamento" indica o método de pagamento utilizado pelo cliente.
        # "vendedor_id" guarda o identificador do vendedor responsável pela venda.
        # "cliente_id" armazena o identificador do cliente, caso exista.
        # Se não houver cliente cadastrado, armazena `None`.
        doc_venda = {
            "data_hora": data_e_hora,
            "itens": itens,
            "total": total,
            "forma_pagamento": forma_pagamento,
            "vendedor_id": ObjectId(id_vendedor),
            "cliente_id": ObjectId(id_cliente) if id_cliente else None
        }

        # Insere a venda no banco de dados na coleção "vendas".
        # `insert_one(doc_venda)` adiciona os detalhes da venda ao banco.
        # O método retorna um objeto contendo o ID do documento inserido.
        resultado = self.col_vendas.insert_one(doc_venda)

        # Retorna o ID da venda recém-registrada para possíveis usos futuros.
        return resultado.inserted_id


    # Define um método para buscar uma venda específica no banco de dados.
    # `id_venda` é o identificador único da venda a ser consultada.
    def obter_venda_por_id(self, id_venda):

        # Realiza a busca na coleção de vendas utilizando o `_id` da venda.
        # `ObjectId(id_venda)` converte o ID fornecido para o
        #       formato correto do MongoDB.
        # A função `find_one()` retorna um dicionário com os
        #       detalhes da venda, ou `None` se não encontrar.
        return self.col_vendas.find_one({"_id": ObjectId(id_venda)})


###############################################################################
# FUNÇÃO PARA CENTRALIZAR JANELAS
###############################################################################

# Função para centralizar uma janela do Tkinter na tela
def centralizar_janela(janela):

    """
    Centraliza a janela do Tkinter no meio da tela.

    Entrada:
        - janela: O objeto da janela principal do Tkinter (tk.Tk() ou tk.Toplevel()).

    Funcionamento:
        - Obtém as dimensões da janela e da tela.
        - Calcula a posição central.
        - Define a nova posição da janela para que ela fique centralizada.

    Retorno:
        - Nenhum. A função apenas altera a posição da janela.
    """

    # Atualiza as informações da janela antes de obter suas dimensões.
    # Isso garante que o Tkinter tenha processado todas as
    #       configurações da janela antes de pegar os valores.
    janela.update_idletasks()

    # Obtém a largura atual da janela
    w = janela.winfo_width()

    # Obtém a altura atual da janela
    h = janela.winfo_height()

    # Obtém a largura da tela do monitor
    sw = janela.winfo_screenwidth()

    # Obtém a altura da tela do monitor
    sh = janela.winfo_screenheight()

    # Calcula a posição x para centralizar a janela na tela
    x = (sw - w) // 2

    # Calcula a posição y para centralizar a janela na tela
    y = (sh - h) // 2

    # Define o tamanho da janela e sua posição na tela.
    # O formato f"{w}x{h}+{x}+{y}" define:
    # - Largura (w)
    # - Altura (h)
    # - Posição X (x)
    # - Posição Y (y)
    janela.geometry(f"{w}x{h}+{x}+{y}")


###############################################################################
# QUADRO DE LOGIN (COM CADASTRO)
###############################################################################

# Cria a classe `QuadroLogin`, que representa a interface
#       de login do sistema.
# Esta classe herda de `tk.Frame`, que é um contêiner
#       para organizar os elementos gráficos.
class QuadroLogin(tk.Frame):

    # Define o método construtor `__init__`, que é executado ao
    #       criar uma instância da classe.
    # `pai` representa o elemento onde o quadro será inserido.
    # `db` é a referência ao banco de dados.
    # `aplicacao` é a referência à aplicação principal para interação após o login.
    def __init__(self, pai, db, aplicacao):

        # Chama o construtor da classe `tk.Frame` para
        #       inicializar corretamente o quadro.
        # `pai` define onde este quadro será inserido.
        # `bg="#eaeaea"` define a cor de fundo como um tom claro de cinza.
        super().__init__(pai, bg="#eaeaea")

        # Armazena a referência ao banco de dados para
        #       verificar as credenciais do usuário.
        self.db = db

        # Armazena a referência à aplicação principal para
        #       permitir interações pós-login.
        self.aplicacao = aplicacao

        # Expande o quadro `QuadroLogin` para ocupar todo o espaço disponível na janela.
        # `expand=True` permite que o quadro cresça caso a janela seja redimensionada.
        # `fill="both"` faz com que o quadro ocupe toda a largura e altura disponíveis.
        self.pack(expand=True, fill="both")

        # Cria um `Frame` chamado `quadro_form` dentro do `QuadroLogin`
        #       para conter os elementos do formulário.
        # `bd=3` define uma borda de 3 pixels.
        # `relief="ridge"` cria um efeito tridimensional na borda.
        # `padx=40` e `pady=40` adicionam espaçamento interno ao
        #       redor dos elementos dentro do quadro.
        # `bg="white"` define o fundo do quadro como branco.
        quadro_form = tk.Frame(self,
                               bd=3,
                               relief="ridge",
                               padx=40,
                               pady=40,
                               bg="white")

        # Posiciona o `quadro_form` no centro da tela usando `place()`.
        # `relx=0.5` e `rely=0.5` posicionam o centro do quadro no meio da tela.
        # `anchor="center"` garante que o ponto de referência seja o centro do quadro.
        quadro_form.place(relx=0.5, rely=0.5, anchor="center")

        # Cria um rótulo (`Label`) chamado `titulo` que
        #       exibe uma mensagem de boas-vindas.
        # `quadro_form` é o pai deste rótulo.
        # `text="Bem-vindo(a) à Loja de Brinquedos"` define o texto exibido.
        # `font=("Arial", 18, "bold")` define a fonte como Arial, tamanho 18, e em negrito.
        # `bg="white"` define o fundo branco para combinar com o quadro.
        # `fg="#333333"` define a cor do texto como um tom escuro de cinza.
        titulo = tk.Label(quadro_form,
                          text="Bem-vindo(a) à Loja de Brinquedos",
                          font=("Arial", 18, "bold"),
                          bg="white",
                          fg="#333333")

        # Posiciona o rótulo `titulo` na primeira linha e ocupa
        #       duas colunas (`columnspan=2`).
        # `row=0` define que o rótulo será inserido na primeira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna.
        # `columnspan=2` faz com que o rótulo ocupe duas colunas, centralizando o texto.
        # `pady=(0, 20)` adiciona um espaço de 20 pixels abaixo do rótulo.
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))


        # Rótulo e Entry de Usuário
        # Cria um rótulo (`Label`) para identificar o campo de entrada do usuário.
        # `quadro_form` é o pai deste rótulo.
        # `text="Usuário:"` define o texto exibido ao lado do campo de entrada.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `bg="white"` mantém o fundo branco, combinando com o `quadro_form`.
        tk.Label(quadro_form,
                 text="Usuário:",
                 font=("Arial", 12),
                 bg="white").grid(row=1,  # Posiciona o rótulo na segunda linha (índice 1) da grade.
                                  column=0,  # Coloca o rótulo na primeira coluna.
                                  padx=10,  # Adiciona um espaçamento horizontal de 10 pixels.
                                  pady=5,  # Adiciona um espaçamento vertical de 5 pixels.
                                  sticky="e")  # Alinha o rótulo à direita dentro da célula da grade.

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa digitar o nome de usuário.
        # `quadro_form` é o pai deste campo de entrada.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        self.ent_usuario = tk.Entry(quadro_form, font=("Arial", 12))

        # Posiciona o campo de entrada na grade do `quadro_form`.
        self.ent_usuario.grid(row=1,  # Posiciona o campo na segunda linha (índice 1).
                              column=1,  # Coloca o campo na segunda coluna.
                              padx=10,  # Adiciona um espaçamento horizontal de 10 pixels.
                              pady=5)  # Adiciona um espaçamento vertical de 5 pixels.
        self.ent_usuario.insert(0, "clevison")

        # Rótulo e Entry de Senha
        # Cria um rótulo (`Label`) para identificar o campo de entrada da senha.
        # `quadro_form` é o pai deste rótulo.
        # `text="Senha:"` define o texto exibido ao lado do campo de entrada.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `bg="white"` mantém o fundo branco, combinando com o `quadro_form`.
        tk.Label(quadro_form,
                 text="Senha:",
                 font=("Arial", 12),
                 bg="white").grid(row=2,  # Posiciona o rótulo na terceira linha (índice 2) da grade.
                                  column=0,  # Coloca o rótulo na primeira coluna.
                                  padx=10,  # Adiciona um espaçamento horizontal de 10 pixels.
                                  pady=5,  # Adiciona um espaçamento vertical de 5 pixels.
                                  sticky="e")  # Alinha o rótulo à direita dentro da célula da grade.

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa digitar a senha.
        # `quadro_form` é o pai deste campo de entrada.
        # `show="*"` oculta os caracteres digitados, exibindo apenas asteriscos.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        self.ent_senha = tk.Entry(quadro_form, show="*", font=("Arial", 12))

        # Posiciona o campo de entrada da senha na grade do `quadro_form`.
        self.ent_senha.grid(row=2,  # Posiciona o campo na terceira linha (índice 2).
                            column=1,  # Coloca o campo na segunda coluna.
                            padx=10,  # Adiciona um espaçamento horizontal de 10 pixels.
                            pady=5)  # Adiciona um espaçamento vertical de 5 pixels.
        self.ent_senha.insert(0, "555")

        # Quadro de botões (Entrar / Sair)
        # Cria um frame (`Frame`) para agrupar os botões de ação
        #       dentro do formulário de login.
        # `quadro_form` é o pai deste frame.
        # `bg="white"` mantém o fundo branco, combinando com o `quadro_form`.
        quadro_btn = tk.Frame(quadro_form, bg="white")

        # Posiciona o `quadro_btn` na grade do `quadro_form`.
        quadro_btn.grid(row=3,  # Posiciona o frame na quarta linha (índice 3).
                        column=0,  # Coloca o frame na primeira coluna.
                        columnspan=2,  # O frame ocupa duas colunas, centralizando os botões.
                        pady=15)  # Adiciona um espaçamento vertical de 15 pixels.

        # Cria um botão (`Button`) para a ação de login.
        # `quadro_btn` é o pai deste botão.
        # `text="Entrar"` define o texto exibido no botão.
        # `width=10` define a largura do botão para comportar o texto de forma equilibrada.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        # `bg="#4CAF50"` define a cor de fundo do botão como verde (#4CAF50).
        # `fg="white"` define a cor do texto do botão como branco.
        # `activebackground="#45a049"` altera a cor do botão quando pressionado.
        # `command=self.fazer_login` associa a ação de chamar `self.fazer_login` ao clicar no botão.
        btn_entrar = tk.Button(quadro_btn,
                               text="Entrar",
                               width=10,
                               font=("Arial", 12),
                               bg="#4CAF50",
                               fg="white",
                               activebackground="#45a049",
                               command=self.fazer_login)

        # Posiciona o botão `btn_entrar` dentro do `quadro_btn`.
        # `side="left"` alinha o botão à esquerda dentro do `quadro_btn`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre os elementos dentro do frame.
        btn_entrar.pack(side="left", padx=5)

        # Cria um botão (`Button`) para a ação de sair do aplicativo.
        # `quadro_btn` é o pai deste botão.
        # `text="Sair"` define o texto exibido no botão.
        # `width=10` define a largura do botão, garantindo que
        #       fique proporcional ao botão "Entrar".
        # `font=("Arial", 12)` define a fonte do texto do botão como Arial, tamanho 12.
        # `bg="#f44336"` define a cor de fundo do botão como vermelho intenso (#f44336).
        # `fg="white"` define a cor do texto do botão como branco, garantindo contraste.
        # `activebackground="#e53935"` altera a cor de fundo do
        #       botão para um vermelho mais escuro (#e53935) quando pressionado.
        # `command=self.aplicacao.destroy` define que ao clicar no
        #       botão, o aplicativo será fechado.
        btn_sair = tk.Button(quadro_btn,
                             text="Sair",
                             width=10,
                             font=("Arial", 12),
                             bg="#f44336",
                             fg="white",
                             activebackground="#e53935",
                             command=self.aplicacao.destroy)

        # Posiciona o botão `btn_sair` dentro do `quadro_btn`.
        # `side="left"` alinha o botão à esquerda dentro do `quadro_btn`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre os botões "Entrar" e "Sair".
        btn_sair.pack(side="left", padx=5)

        # Botão adicional: Cadastrar Usuário
        # Cria um botão (`Button`) para a ação de cadastrar um novo usuário.
        # `quadro_form` é o pai deste botão, garantindo que ele fique no
        #       mesmo quadro do formulário de login.
        # `text="Cadastrar Usuário"` define o texto exibido no botão.
        # `font=("Arial", 10)` define a fonte do texto do botão como Arial, tamanho 10.
        # `bg="#2196F3"` define a cor de fundo do botão como azul vibrante (#2196F3).
        # `fg="white"` define a cor do texto do botão como branco, garantindo
        #       contraste com o fundo azul.
        # `activebackground="#1976D2"` altera a cor de fundo do botão para um azul
        #       mais escuro (#1976D2) quando pressionado.
        # `command=self.abrir_cadastro_usuario` define que ao clicar no botão, a
        #       função `abrir_cadastro_usuario` será executada.
        btn_cadastro = tk.Button(quadro_form,
                                 text="Cadastrar Usuário",
                                 font=("Arial", 10),
                                 bg="#2196F3",
                                 fg="white",
                                 activebackground="#1976D2",
                                 command=self.abrir_cadastro_usuario)

        # Posiciona o botão `btn_cadastro` dentro do `quadro_form`.
        # `row=4` posiciona o botão na quarta linha do `quadro_form`.
        # `column=0, columnspan=2` faz com que o botão ocupe duas
        #       colunas, centralizando-o.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels abaixo do
        #       botão, para melhor organização visual.
        btn_cadastro.grid(row=4, column=0, columnspan=2, pady=10)

        # Este método centraliza a janela principal (caso queira)
        self.after(100, lambda: centralizar_janela(self.master))


    # Define o método `fazer_login` que será chamado quando o
    #       usuário tentar realizar o login.
    # Esse método verifica as credenciais inseridas e
    #       autentica o usuário no sistema.
    def fazer_login(self):

        # Obtém o nome de usuário digitado no campo de entrada `self.ent_usuario`.
        # `get()` captura o texto digitado, e `strip()` remove
        #       espaços extras antes e depois do texto.
        usuario = self.ent_usuario.get().strip()

        # Obtém a senha digitada no campo de entrada `self.ent_senha`.
        # `get()` captura o texto digitado, e `strip()` remove
        #       espaços extras antes e depois do texto.
        senha = self.ent_senha.get().strip()

        # Chama a função `autenticar_usuario` do banco de dados,
        #       passando `usuario` e `senha`.
        # Se o usuário for encontrado no banco, `doc` conterá os
        #       dados do usuário; caso contrário, será `None`.
        doc = self.db.autenticar_usuario(usuario, senha)

        # Verifica se a autenticação foi bem-sucedida.
        if doc:

            # Se o usuário foi autenticado com sucesso, exibe uma
            #       mensagem de boas-vindas com o nome do usuário.
            messagebox.showinfo("Login",
                                f"Bem-vindo(a), {doc['nome']}!")

            # Salva os dados do usuário autenticado dentro da aplicação.
            self.aplicacao.usuario_logado = doc

            # Chama a função `mostrar_painel_principal` para
            #       exibir a tela principal do sistema.
            self.aplicacao.mostrar_painel_principal()

        else:

            # Se a autenticação falhar, exibe uma mensagem de erro
            #       informando que o usuário ou senha são inválidos.
            messagebox.showerror("Erro",
                                 "Usuário ou senha inválidos.")


    # Define o método `abrir_cadastro_usuario`, que cria
    #       uma nova janela para o cadastro de usuários.
    def abrir_cadastro_usuario(self):

        # Cria uma nova janela `Toplevel`, que será uma janela
        #       separada dentro da aplicação.
        # `self` indica que a nova janela será filha da janela principal.
        janela_cad = tk.Toplevel(self)

        # Define o título da nova janela como "Cadastrar Novo Usuário".
        janela_cad.title("Cadastrar Novo Usuário")

        # Define o tamanho da janela para 320 pixels de
        #       largura por 250 pixels de altura.
        janela_cad.geometry("320x250")

        # Configura a cor de fundo da janela para um tom de branco (#fafafa).
        janela_cad.configure(bg="#fafafa")  # Branco gelo

        # Define que a nova janela será modal, impedindo interações
        #       com a janela principal enquanto estiver aberta.
        janela_cad.transient(self)

        # Bloqueia a interação com outras janelas da aplicação
        #       enquanto esta estiver aberta.
        janela_cad.grab_set()

        # Centraliza a nova janela na tela do usuário,
        #       chamando a função `centralizar_janela`.
        centralizar_janela(janela_cad)

        # Cria um rótulo para o campo de entrada do nome completo.
        # `text="Nome Completo:"` define o texto exibido no rótulo.
        # `bg="#fafafa"` define a cor de fundo como cinza claro para combinar com a janela.
        # `row=0` posiciona o rótulo na primeira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        tk.Label(janela_cad,
                 text="Nome Completo:",
                 bg="#fafafa").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o usuário digitar o nome completo.
        # Este campo permitirá que o usuário insira o texto do nome completo.
        ent_nome = tk.Entry(janela_cad)

        # Posiciona o campo de entrada na grade da janela.
        # `row=0` coloca o campo na mesma linha do rótulo.
        # `column=1` coloca o campo na segunda coluna, ao lado do rótulo.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels ao
        #       redor do campo de entrada.
        ent_nome.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de entrada do nome de usuário.
        # `text="Usuário:"` define o texto exibido no rótulo.
        # `bg="#fafafa"` define a cor de fundo como cinza claro
        #       para combinar com a janela.
        # `row=1` posiciona o rótulo na segunda linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        tk.Label(janela_cad,
                 text="Usuário:",
                 bg="#fafafa").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o usuário digitar o nome de usuário.
        # Este campo permitirá que o usuário insira um nome de usuário único.
        ent_user = tk.Entry(janela_cad)

        # Posiciona o campo de entrada na grade da janela.
        # `row=1` coloca o campo na mesma linha do rótulo.
        # `column=1` coloca o campo na segunda coluna, ao lado do rótulo.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels
        #       ao redor do campo de entrada.
        ent_user.grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de entrada da senha.
        # `text="Senha:"` define o texto exibido no rótulo.
        # `bg="#fafafa"` define a cor de fundo como cinza claro
        #       para combinar com a janela.
        # `row=2` posiciona o rótulo na terceira linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        tk.Label(janela_cad,
                 text="Senha:",
                 bg="#fafafa").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para a senha do usuário.
        # O parâmetro `show="*"` oculta os caracteres digitados para segurança.
        ent_senha = tk.Entry(janela_cad, show="*")

        # Posiciona o campo de entrada da senha na grade da janela.
        # `row=2` coloca o campo na mesma linha do rótulo.
        # `column=1` coloca o campo na segunda coluna, ao lado do rótulo.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels
        #       ao redor do campo de entrada.
        ent_senha.grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para indicar o campo de seleção da permissão do usuário.
        # `text="Permissão:"` define o texto exibido no rótulo.
        # `bg="#fafafa"` define a cor de fundo como cinza claro
        #       para manter a harmonia visual.
        # `row=3` posiciona o rótulo na quarta linha da grade.
        # `column=0` posiciona o rótulo na primeira coluna da grade.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita dentro da célula da grade.
        tk.Label(janela_cad,
                 text="Permissão:",
                 bg="#fafafa").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria uma variável de controle do tipo StringVar para
        #       armazenar a permissão do usuário.
        # `value="vendedor"` define o valor inicial da
        #       variável como "vendedor".
        var_perm = tk.StringVar(value="vendedor")

        # Cria uma caixa de seleção (Combobox) para permitir a
        #       escolha da permissão do usuário.
        # `janela_cad` define que o Combobox pertence à janela de cadastro.
        # `textvariable=var_perm` vincula a seleção do usuário à variável var_perm.
        # `values=["admin", "gerente", "vendedor"]` define as
        #       opções disponíveis no menu suspenso.
        # `state="readonly"` impede que o usuário digite valores
        #       manualmente, permitindo apenas a seleção.
        combo_perm = ttk.Combobox(janela_cad,
                                  textvariable=var_perm,
                                  values=["admin", "gerente", "vendedor"],
                                  state="readonly")

        # Define a posição do Combobox na grade da janela de cadastro.
        # `row=3` posiciona a caixa de seleção na quarta linha da grade.
        # `column=1` posiciona a caixa de seleção na segunda coluna da grade.
        # `padx=5, pady=5` adiciona um espaçamento de 5 pixels
        #       ao redor da caixa de seleção.
        combo_perm.grid(row=3, column=1, padx=5, pady=5)


        # Define a função `confirmar_cadastro` que será chamada
        #       ao clicar no botão de cadastro.
        def confirmar_cadastro():

            # Obtém e remove espaços extras do nome digitado pelo usuário.
            nome_c = ent_nome.get().strip()

            # Obtém e remove espaços extras do nome de usuário digitado.
            user_c = ent_user.get().strip()

            # Obtém e remove espaços extras da senha digitada.
            senha_c = ent_senha.get().strip()

            # Obtém e remove espaços extras da permissão selecionada.
            perm_c = var_perm.get().strip()

            # Verifica se todos os campos obrigatórios foram preenchidos.
            # Se algum campo estiver vazio, exibe uma mensagem de
            #       erro e interrompe o cadastro.
            if not nome_c or not user_c or not senha_c:
                messagebox.showerror("Erro",
                                     "Preencha todos os campos!")
                return

            # Chama o método `criar_usuario` do banco de dados para cadastrar o novo usuário.
            # Retorna `status` como True ou False e `msg` como a mensagem de resposta.
            status, msg = self.db.criar_usuario(nome_c, user_c, senha_c, perm_c)

            # Se o cadastro for bem-sucedido, exibe uma mensagem de
            #       sucesso e fecha a janela de cadastro.
            if status:
                messagebox.showinfo("Sucesso", msg)
                janela_cad.destroy()

            # Se o cadastro falhar (exemplo: usuário já existente),
            #       exibe uma mensagem de erro.
            else:
                messagebox.showerror("Erro", msg)


        # Cria um botão chamado "Salvar" para confirmar o cadastro do usuário.
        # `text="Salvar"` define o texto exibido no botão.
        # `bg="#4CAF50"` define o fundo do botão na cor verde (#4CAF50).
        # `fg="white"` define a cor do texto do botão como branco.
        # `activebackground="#45a049"` define o fundo do botão ao ser
        #       pressionado, um tom de verde mais escuro (#45a049).
        # `command=confirmar_cadastro` define que, ao clicar no botão, a
        #       função `confirmar_cadastro` será chamada.
        # `row=4, column=0, columnspan=2` posiciona o botão na quarta
        #       linha e faz com que ocupe duas colunas.
        # `pady=15` adiciona um espaçamento vertical de 15 pixels abaixo do botão.
        tk.Button(janela_cad,
                  text="Salvar",
                  bg="#4CAF50",
                  fg="white",
                  activebackground="#45a049",
                  command=confirmar_cadastro).grid(row=4, column=0, columnspan=2, pady=15)


###############################################################################
# CLASSE PRINCIPAL DA APLICAÇÃO
###############################################################################

# Cria a classe `Aplicacao` que herda de `tk.Tk`, a classe principal do
#       Tkinter para janelas.
class Aplicacao(tk.Tk):

    # Define o método inicializador `__init__`, chamado
    #       quando a classe é instanciada.
    def __init__(self):

        # Chama o inicializador da classe pai (`tk.Tk`) para
        #       configurar a janela principal.
        super().__init__()

        # Define o título da janela principal como "Loja de Brinquedos".
        self.title("Loja de Brinquedos")

        # Ajusta a janela para iniciar maximizada, preenchendo toda a tela.
        self.state("zoomed")

        # Cria uma instância do gerenciador do banco de dados, `GerenciadorBanco`,
        #       para interagir com os dados da loja.
        self.db = GerenciadorBanco()

        # Inicializa a variável `usuario_logado` como `None`, indicando que
        #       nenhum usuário está autenticado inicialmente.
        self.usuario_logado = None

        # Inicializa a variável `quadro_atual` como `None`, que
        #       armazenará o quadro visível na interface.
        self.quadro_atual = None

        # Chama o método `exibir_login()` para exibir a
        #       tela de login ao iniciar a aplicação.
        self.exibir_login()

    # Define o método `exibir_login` que exibe a tela de login da aplicação.
    def exibir_login(self):

        # Verifica se já há um quadro ativo na
        #       interface (por exemplo, outra tela aberta).
        if self.quadro_atual is not None:

            # Se houver, ele é destruído para remover a tela
            #       anterior e evitar sobreposição.
            self.quadro_atual.destroy()

        # Cria uma nova instância da classe `QuadroLogin`, que é a
        #       tela de login da aplicação.
        # Passa `self` (a aplicação principal), `self.db` (o banco
        #       de dados) e `self` novamente
        #       para que a tela de login tenha acesso à aplicação.
        self.quadro_atual = QuadroLogin(self, self.db, self)

        # Exibe a tela de login preenchendo toda a janela e
        #       permitindo que ela se expanda automaticamente.
        self.quadro_atual.pack(fill="both", expand=True)


    # Define o método `mostrar_painel_principal`, responsável por
    #       exibir o painel principal da aplicação.
    def mostrar_painel_principal(self):

        # Verifica se há um quadro ativo na interface (como a tela de login).
        if self.quadro_atual is not None:

            # Se houver, ele é destruído para remover a tela
            #       anterior e evitar sobreposição.
            self.quadro_atual.destroy()

        # Cria uma barra de menu na interface principal.
        barra_menu = tk.Menu(self)

        # Configura a barra de menu criada como a barra de
        #       menu principal da aplicação.
        self.config(menu=barra_menu)

        # Cria um menu suspenso chamado 'Sistema' dentro da barra de menu principal.
        # `tearoff=0` impede que o menu seja destacado da janela principal.
        menu_sistema = tk.Menu(barra_menu, tearoff=0)

        # Adiciona uma opção chamada 'Sair' dentro do menu 'Sistema'.
        # `label="Sair"` define o nome visível da opção no menu.
        # `command=self.destroy` associa a ação de fechar a
        #       aplicação ao clicar nesta opção.
        menu_sistema.add_command(label="Sair", command=self.destroy)

        # Adiciona o menu suspenso 'Sistema' à barra de menus principal.
        # `label="Sistema"` define o nome do menu na barra de menus.
        barra_menu.add_cascade(label="Sistema", menu=menu_sistema)

        # Obtém o nível de permissão do usuário logado.
        # `self.usuario_logado["permissao"]` armazena a
        #       permissão do usuário autenticado.
        permissao = self.usuario_logado["permissao"]

        # Cria um componente `Notebook`, que permite a exibição
        #       de várias abas na interface.
        # Este componente será usado para organizar diferentes seções do sistema.
        abas = ttk.Notebook(self)

        # Aba de Vendas
        # Cria um quadro específico para gerenciar vendas dentro do sistema.
        # `QuadroVendas` representa a interface gráfica relacionada ao
        #       gerenciamento de vendas.
        # `abas` é o container onde o quadro será inserido.
        # `self.db` é a conexão com o banco de dados, permitindo
        #       operações de consulta e inserção.
        # `self.usuario_logado` contém informações do usuário autenticado,
        #       usadas para definir permissões e ações.
        quadro_vendas = QuadroVendas(abas, self.db, self.usuario_logado)

        # Adiciona a aba 'Vendas' dentro do `Notebook` (interface de múltiplas abas).
        # `abas.add` insere o quadro de vendas dentro do conjunto de abas da aplicação.
        # `text="Vendas"` define o nome da aba visível ao usuário.
        abas.add(quadro_vendas, text="Vendas")

        # Cria um quadro específico para gerenciar os clientes do sistema.
        # `QuadroClientes` representa a interface gráfica relacionada ao
        #       cadastro e consulta de clientes.
        # `abas` é o container onde o quadro será inserido.
        # `self.db` é a conexão com o banco de dados para buscar e
        #       armazenar informações dos clientes.
        quadro_clientes = QuadroClientes(abas, self.db)

        # Adiciona a aba 'Clientes' dentro do `Notebook`, permitindo
        #       que todos os usuários a acessem.
        # `abas.add` insere o quadro de clientes dentro do
        #       conjunto de abas da aplicação.
        # `text="Clientes"` define o nome da aba visível ao usuário.
        abas.add(quadro_clientes, text="Clientes")

        # Fornecedores e Produtos (somente admin ou gerente)
        # Verifica se o usuário tem permissão de "admin" ou "gerente".
        # Somente esses níveis de permissão podem acessar as
        #       abas de Fornecedores e Produtos.
        if permissao in ["admin", "gerente"]:

            # Cria o quadro para gerenciamento de fornecedores.
            # `QuadroFornecedores` é a interface gráfica que permite
            #       adicionar, editar e excluir fornecedores.
            # `abas` é o container onde o quadro será inserido.
            # `self.db` é a conexão com o banco de dados, permitindo
            #       operações nos dados dos fornecedores.
            quadro_forn = QuadroFornecedores(abas, self.db)

            # Adiciona a aba 'Fornecedores' dentro do `Notebook` para que o
            #       usuário possa acessar essas informações.
            # `abas.add` insere o quadro de fornecedores dentro do
            #       conjunto de abas da aplicação.
            # `text="Fornecedores"` define o nome da aba visível ao usuário.
            abas.add(quadro_forn, text="Fornecedores")

            # Cria o quadro para gerenciamento de produtos.
            # `QuadroProdutos` é a interface gráfica que permite
            #       adicionar, editar e excluir produtos.
            # `abas` é o container onde o quadro será inserido.
            # `self.db` é a conexão com o banco de dados, permitindo
            #       operações nos dados dos produtos.
            quadro_prod = QuadroProdutos(abas, self.db)

            # Adiciona a aba 'Produtos' dentro do `Notebook` para que o
            #       usuário possa acessar essas informações.
            # `abas.add` insere o quadro de produtos dentro do conjunto de abas da aplicação.
            # `text="Produtos"` define o nome da aba visível ao usuário.
            abas.add(quadro_prod, text="Produtos")

        # Aba Admin (somente admin)
        # Verifica se o usuário tem permissão de "admin".
        # Somente usuários com permissão de administrador podem acessar esta aba.
        if permissao == "admin":

            # Cria o quadro de administrador.
            # `QuadroAdmin` é a interface gráfica para gerenciar
            #       recursos exclusivos de administradores.
            # `abas` é o container onde o quadro será inserido.
            # `self.db` é a conexão com o banco de dados.
            # `self.usuario_logado` passa informações do usuário atualmente logado.
            quadro_adm = QuadroAdmin(abas, self.db, self.usuario_logado)

            # Adiciona a aba 'Admin' dentro do `Notebook` para que o
            #       administrador possa acessar essas ferramentas.
            # `abas.add` insere o quadro de administrador dentro do
            #       conjunto de abas da aplicação.
            # `text="Admin"` define o nome da aba visível ao usuário.
            abas.add(quadro_adm, text="Admin")

        # Posiciona o conjunto de abas na interface.
        # `fill="both"` faz com que as abas ocupem todo o espaço disponível.
        # `expand=True` permite que o conjunto de abas se
        #       expanda conforme a janela é redimensionada.
        abas.pack(fill="both", expand=True)

        # Define o quadro atual da aplicação como o conjunto de abas.
        # Isso garante que a referência à interface ativa seja atualizada.
        self.quadro_atual = abas


###############################################################################
# QUADRO DE VENDAS
###############################################################################

# Define a classe `QuadroVendas` como um container
#       gráfico que herda de `tk.Frame`.
class QuadroVendas(tk.Frame):

    # Define o método inicializador da classe.
    #  Ele configura o quadro e seus atributos.
    # `pai` é o componente pai onde o quadro será inserido.
    # `db` é uma instância de `GerenciadorBanco` que gerencia o banco de dados.
    # `usuario` é o usuário atualmente logado na aplicação.
    def __init__(self, pai, db: GerenciadorBanco, usuario):

        # Inicializa o `Frame` base com o pai especificado.
        super().__init__(pai)

        # Atribui a instância do banco de dados à variável de instância `self.db`.
        # Isso permite que o quadro acesse métodos para manipular os dados.
        self.db = db

        # Salva as informações do usuário logado na variável `self.usuario`.
        self.usuario = usuario

        # Inicializa uma lista vazia para o carrinho de compras.
        # `self.carrinho` será usado para armazenar os
        #       itens selecionados pelo cliente.
        self.carrinho = []

        # Cria um cache dos clientes listados no banco de dados.
        # Isso melhora o desempenho ao evitar consultas repetidas.
        # `self.lista_clientes_cache` conterá os clientes disponíveis.
        self.lista_clientes_cache = self.db.listar_clientes()

        # Parte de busca de produto
        # Cria um frame horizontal para agrupar os widgets de busca.
        frm_busca = tk.Frame(self)

        # Posiciona o frame de busca na parte superior e faz
        #       com que ele ocupe toda a largura.
        frm_busca.pack(fill="x")

        # Adiciona um rótulo para o campo de busca.
        # `text="Buscar Produto:"` define o texto exibido no rótulo.
        # `side="left"` posiciona o rótulo à esquerda dentro do frame.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor.
        tk.Label(frm_busca,
                 text="Buscar Produto:").pack(side="left", padx=5)

        # Cria um campo de entrada onde o usuário pode digitar o nome do produto.
        # `side="left"` posiciona o campo à esquerda, logo após o rótulo.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor.
        self.ent_busca = tk.Entry(frm_busca)
        self.ent_busca.pack(side="left", padx=5)

        # Adiciona um botão que, ao ser clicado, chama a função `self.buscar_produto`.
        # `text="Buscar"` define o texto exibido no botão.
        # `command=self.buscar_produto` define a ação executada ao clicar no botão.
        # `side="left"` posiciona o botão à esquerda, logo após o campo de entrada.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor.
        tk.Button(frm_busca,
                  text="Buscar",
                  command=self.buscar_produto).pack(side="left", padx=5)

        # Cria um Scrollbar vertical para navegar pelos produtos.
        # `orient="vertical"` indica que o scrollbar será vertical.
        scroll_p = tk.Scrollbar(self, orient="vertical")

        # Cria um Treeview que exibirá os produtos em uma lista
        #       organizada por colunas.
        # `columns= define as colunas da tabela.
        # `show="headings"` oculta a coluna de índice padrão e
        #       mostra apenas os cabeçalhos definidos.
        # `yscrollcommand=scroll_p.set` vincula o scrollbar
        #       vertical ao Treeview, para que ele role ao arrastar.
        self.lista_produtos = ttk.Treeview( self,
                                            columns=("Código", "Nome", "Categoria", "PreçoVenda", "Estoque"),
                                            show="headings",
                                            yscrollcommand=scroll_p.set)

        # Configura o comando do scrollbar para ajustar a visualização do Treeview.
        scroll_p.config(command=self.lista_produtos.yview)

        # Posiciona o scrollbar no lado direito e o ajusta para
        #       ocupar todo o comprimento.
        scroll_p.pack(side="right", fill="y")

        # Define os cabeçalhos e larguras das colunas do Treeview.
        # O loop percorre cada nome de coluna definido anteriormente.
        for c in ("Código", "Nome", "Categoria", "PreçoVenda", "Estoque"):

            # Configura o cabeçalho de cada coluna com o nome correspondente.
            # `heading(c, text=c)` define o texto exibido no cabeçalho da coluna.
            self.lista_produtos.heading(c, text=c)

            # Configura a largura de cada coluna.
            # `column(c, width=120)` define a largura da coluna como 120 pixels.
            self.lista_produtos.column(c, width=120)

        # Exibe o Treeview, permitindo que ele ocupe todo o espaço disponível.
        # `fill="both"` faz com que o Treeview seja redimensionado para
        #       preencher o espaço horizontal e vertical.
        # `expand=True` garante que o Treeview se expanda junto com o container.
        self.lista_produtos.pack(fill="both", expand=True)

        # Cria um botão para adicionar produtos ao carrinho.
        # `text="Adicionar ao Carrinho"` define o texto exibido no botão.
        # `command=self.adicionar_carrinho` associa a função que
        #       será chamada ao clicar no botão.
        # `pady=5` adiciona um espaçamento vertical ao redor do botão.
        tk.Button(self,
                  text="Adicionar ao Carrinho",
                  command=self.adicionar_carrinho).pack(pady=5)

        # Lista do carrinho
        # Cria um scrollbar vertical para a lista de carrinho.
        # `orient="vertical"` especifica que a barra de rolagem é vertical.
        scroll_c = tk.Scrollbar(self, orient="vertical")

        # Cria um Treeview para exibir os itens do carrinho.
        # `columns=(...)` define as colunas que serão exibidas: Nome do
        #       produto, Quantidade, Preço Unitário e Subtotal.
        # `show="headings"` exibe apenas os cabeçalhos das colunas, sem a coluna de índice.
        # `yscrollcommand=scroll_c.set` conecta a barra de rolagem ao Treeview.
        self.lista_carrinho = ttk.Treeview(self,
                                            columns=("Nome", "Qtd", "Preço Unitário", "Subtotal"),
                                            show="headings",
                                            yscrollcommand=scroll_c.set)

        # Configura a barra de rolagem para controlar a
        #       visualização do Treeview do carrinho.
        # `command=self.lista_carrinho.yview` estabelece a
        #       conexão entre a barra de rolagem e o Treeview.
        scroll_c.config(command=self.lista_carrinho.yview)

        # Posiciona a barra de rolagem no lado direito da tela.
        # `side="right"` alinha a barra à direita.
        # `fill="y"` faz com que a barra se estenda verticalmente.
        # `in_=self` garante que a barra esteja dentro do frame atual.
        scroll_c.pack(side="right", fill="y", in_=self)

        # Define os cabeçalhos e larguras das colunas do Treeview do carrinho.
        # Para cada coluna (Nome, Quantidade, Preço Unitário, Subtotal):
        for cc in ("Nome", "Qtd", "Preço Unitário", "Subtotal"):

            # Define o texto do cabeçalho.
            self.lista_carrinho.heading(cc, text=cc)

            # Ajusta a largura de cada coluna para 120 pixels.
            self.lista_carrinho.column(cc, width=120)

        # Posiciona o Treeview do carrinho para ocupar todo o espaço disponível.
        # `fill="both"` faz com que ele se ajuste horizontal e verticalmente.
        # `expand=True` permite que ele cresça junto com a janela.
        self.lista_carrinho.pack(fill="both", expand=True)

        # Cria um frame para organizar os elementos de seleção do cliente.
        # Este frame será posicionado horizontalmente e se ajustará à largura disponível.
        frm_cli = tk.Frame(self)
        frm_cli.pack(fill="x")

        # Adiciona uma etiqueta para indicar a funcionalidade de seleção de cliente.
        # `text="Selecionar Cliente (opcional):"` fornece uma breve descrição.
        # `pack(side="left", padx=5)` posiciona a etiqueta à esquerda
        #       com 5 pixels de espaçamento horizontal.
        tk.Label(frm_cli,
                 text="Selecionar Cliente (opcional):").pack(side="left", padx=5)

        # Define uma variável para armazenar a seleção do cliente.
        # `self.var_cli` será vinculada aos widgets relacionados a clientes.
        self.var_cli = tk.StringVar()

        # Cria um combobox (menu suspenso) para selecionar um cliente.
        # O widget será posicionado dentro do frame criado anteriormente.
        self.combo_cli = ttk.Combobox(

            # O combobox será adicionado no frame 'frm_cli'.
            frm_cli,

            # Vincula a seleção ao StringVar 'self.var_cli'.
            textvariable=self.var_cli,

            # Popula o combobox com os nomes dos clientes armazenados
            #       em 'self.lista_clientes_cache'.
            values=[c["nome"] for c in self.lista_clientes_cache],

            # Define que o combobox só permite selecionar valores
            #       predefinidos, desativando a edição direta do texto.
            state="readonly"

        )

        # Posiciona o combobox ao lado esquerdo com um
        #       pequeno espaçamento horizontal.
        self.combo_cli.pack(side="left", padx=5)

        # Cria um botão para atualizar a lista de clientes.
        # `text="Atualizar Clientes"` define o texto exibido no botão.
        # `command=self.atualizar_clientes` associa a ação de atualizar a
        #       lista de clientes ao clicar no botão.
        # `side="left", padx=5` posiciona o botão à esquerda
        #       com espaçamento horizontal.
        tk.Button(frm_cli,
                  text="Atualizar Clientes",
                  command=self.atualizar_clientes).pack(side="left", padx=5)

        # Cria um frame para organizar os elementos relacionados à forma de pagamento.
        # `fill="x"` faz o frame ocupar toda a largura disponível na janela.
        frm_pag = tk.Frame(self)
        frm_pag.pack(fill="x")

        # Adiciona um rótulo indicando a forma de pagamento.
        # `text="Forma de Pagamento:"` define o texto exibido no rótulo.
        # `side="left", padx=5` posiciona o rótulo à esquerda com espaçamento horizontal.
        tk.Label(frm_pag, text="Forma de Pagamento:").pack(side="left", padx=5)

        # Cria uma variável para armazenar a forma de pagamento escolhida.
        # `value="Dinheiro"` define o valor inicial como "Dinheiro".
        self.var_forma = tk.StringVar(value="Dinheiro")

        # Cria um combobox para selecionar a forma de pagamento.
        # `textvariable=self.var_forma` associa o combobox à
        #       variável da forma de pagamento.
        # `values= Define as opções disponíveis.
        # `state="readonly"` restringe o combobox apenas para
        #       seleção, sem permitir edição direta.
        # `side="left", padx=5` posiciona o combobox à esquerda
        #       com espaçamento horizontal.
        ttk.Combobox(frm_pag,
                    textvariable=self.var_forma,
                    values=["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Todos"],
                    state="readonly").pack(side="left", padx=5)

        # Cria um botão para finalizar a venda.
        # `text="Finalizar Venda"` define o texto exibido no botão.
        # `command=self.finalizar_venda` associa a ação de finalizar a venda ao botão.
        # `bg="green", fg="white"` define o fundo verde e o texto branco do botão.
        # `side="right", padx=5` posiciona o botão à direita com espaçamento horizontal.
        tk.Button(frm_pag,
                  text="Finalizar Venda",
                  command=self.finalizar_venda,
                  bg="green",
                  fg="white").pack(side="right", padx=5)

        # Cria um rótulo para exibir o total da venda.
        # `text="Total: R$ 0,00"` define o texto inicial do rótulo.
        # `font=("Arial", 14, "bold")` define a fonte, tamanho e estilo do texto.
        # `pady=5` adiciona espaçamento vertical ao redor do rótulo.
        self.lbl_total = tk.Label(self, text="Total: R$ 0,00", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=5)


    # Método para buscar produtos no banco de dados e
    #       exibi-los na lista de produtos.
    def buscar_produto(self):

        # Obtém o texto digitado na barra de busca.
        # `self.ent_busca.get().strip()` remove espaços extras ao
        #       redor do texto digitado.
        texto = self.ent_busca.get().strip()

        # Consulta a base de dados para obter os produtos.
        # Se `texto` não estiver vazio, usa o texto como filtro; caso
        #       contrário, busca todos os produtos.
        # `produtos` armazena a lista de produtos retornada pela
        #       função `self.db.listar_produtos`.
        produtos = self.db.listar_produtos(texto if texto else None)

        # Limpa os itens atualmente exibidos na lista de produtos.
        # `self.lista_produtos.get_children()` retorna todos os
        #       identificadores de itens da lista.
        # `self.lista_produtos.delete(i)` remove cada item da
        #       lista com base em seu identificador.
        for i in self.lista_produtos.get_children():
            self.lista_produtos.delete(i)

        # Adiciona os produtos encontrados à lista visual de produtos.
        # Para cada produto na lista de produtos retornados pela consulta:
        for p in produtos:

            # Insere uma nova linha no Treeview `self.lista_produtos`.
            # A função `insert()` requer os seguintes parâmetros:
            # - parent: o identificador do nó pai. Aqui, usamos uma
            #       string vazia (`""`) para adicionar o item à raiz,
            #   já que não há subnós (é uma lista simples, não hierárquica).
            # - index: onde inserir o novo item. Usamos `"end"` para
            #       adicionar no final da lista existente.
            # - values: uma tupla contendo os valores das colunas da tabela.
            # - iid: identificador único da linha inserida. Usamos o campo `_id` do produto,
            #   que é o identificador único no banco de dados, convertido para string.
            #   Este identificador é útil para, futuramente, localizar ou referenciar esta linha.
            self.lista_produtos.insert("",  # Insere o item diretamente na raiz da árvore.
                                       "end",  # Adiciona no final da lista.
                                       values=(p["codigo"], p["nome"], p["categoria"], p["preco_venda"],
                                               p["quantidade_estoque"]),
                                       iid=str(p["_id"]))  # Usa o identificador único do produto como iid.


    def adicionar_carrinho(self):

        # Adiciona o produto selecionado à lista de itens do carrinho.
        sel = self.lista_produtos.selection()

        # Verifica se algum produto foi selecionado na
        #       lista `self.lista_produtos` antes de continuar.
        if not sel:

            # Exibe uma mensagem de aviso caso nenhum produto esteja selecionado.
            # A função `messagebox.showwarning` mostra uma caixa de
            #       diálogo com um título e uma mensagem.
            # Título: "Aviso".
            # Mensagem: "Selecione um produto para adicionar."
            messagebox.showwarning("Aviso",
                                   "Selecione um produto para adicionar.")

            # Sai da função sem fazer nada se não houver seleção.
            return

        # Obtém o ID do produto selecionado.
        # A seleção retornada por `self.lista_produtos.selection()` é
        #       uma lista de IDs das linhas selecionadas.
        # Aqui pegamos o primeiro (e geralmente único) item selecionado.
        id_prod = sel[0]

        # Busca os detalhes do produto no banco de dados.
        # A consulta é feita na coleção de produtos `self.db.col_produtos`
        #       usando o `_id` correspondente.
        # O identificador `id_prod` é convertido para um objeto `ObjectId`
        #       porque o MongoDB usa este tipo para armazenar identificadores únicos.
        doc_p = self.db.col_produtos.find_one({"_id": ObjectId(id_prod)})

        # Define a função que será executada ao confirmar a quantidade do produto.
        def confirmar():

            # Obtém o texto digitado na entrada de quantidade.
            # Usa o método `strip()` para remover espaços em
            #       branco antes e depois do valor.
            qt_str = ent_qt.get().strip()

            # Verifica se o texto digitado é um número válido.
            # A função `isdigit()` retorna `True` se todos os
            #       caracteres da string forem dígitos.
            # Caso contrário, exibe uma mensagem de erro informando
            #       que a quantidade é inválida.
            if not qt_str.isdigit():

                # Mostra uma caixa de mensagem com o título "Erro" e a
                #       mensagem "Quantidade inválida!".
                # A função `messagebox.showerror` é usada para exibir erros.
                messagebox.showerror("Erro", "Quantidade inválida!")

                # Interrompe a função se o valor não for um número válido.
                return

            # Converte o texto digitado (string) para um número inteiro.
            qt_int = int(qt_str)

            # Verifica se a quantidade está fora dos limites aceitáveis.
            # Se a quantidade for menor ou igual a zero, ou maior do
            #       que a quantidade disponível em estoque,
            #       exibe uma mensagem de erro correspondente.
            if qt_int <= 0 or qt_int > doc_p["quantidade_estoque"]:

                # Mostra uma mensagem de erro com o título "Erro" e a
                #       mensagem "Quantidade fora do estoque!".
                messagebox.showerror("Erro", "Quantidade fora do estoque!")

                # Interrompe a função se a quantidade estiver
                #       fora do intervalo permitido.
                return

            # Obtém o preço unitário do produto a partir do documento
            #       do banco de dados.
            # O valor `preco_venda` é usado para calcular o subtotal ou
            #       outros valores no próximo passo.
            preco_uni = doc_p["preco_venda"]

            # Adiciona os dados do produto selecionado ao carrinho.
            # O carrinho é uma lista de dicionários, cada um representando um item.
            self.carrinho.append({

                # `produto_id` é o identificador único do produto, convertido para string.
                "produto_id": str(doc_p["_id"]),

                # `nome` é o nome do produto.
                "nome": doc_p["nome"],

                # `quantidade` é a quantidade selecionada pelo usuário.
                "quantidade": qt_int,

                # `preco_unitario` é o preço unitário do produto,
                #       obtido diretamente do documento do banco.
                "preco_unitario": preco_uni

            })

            # Atualiza a exibição do carrinho na interface do usuário.
            # Essa função insere os itens no
            #       componente de lista do carrinho e recalcula o total.
            self.atualizar_carrinho()

            # Fecha a janela de entrada de quantidade após a adição ao carrinho.
            # `janela_qt.destroy()` remove essa janela da tela.
            janela_qt.destroy()

        # Cria uma nova janela pop-up para que o usuário
        #       insira a quantidade desejada.
        # `tk.Toplevel(self)` cria uma janela filha associada à janela principal.
        janela_qt = tk.Toplevel(self)

        # Define o título da nova janela como "Quantidade".
        janela_qt.title("Quantidade")

        # Configura a janela para estar sempre acima da
        #       janela principal, para maior visibilidade.
        janela_qt.transient(self)

        # Coloca a nova janela em modo modal, o que impede
        #       interação com outras janelas
        #       enquanto esta estiver aberta. O usuário precisa
        #       fechar esta janela para voltar à janela principal.
        janela_qt.grab_set()

        # Adiciona um rótulo informando ao usuário o nome do
        #       produto e a quantidade em estoque.
        # `text= mostra o nome do produto e o estoque atual.
        # `pack(pady=10, padx=10)` centraliza o texto e adiciona
        #       espaçamento vertical e horizontal.
        tk.Label(janela_qt,
                 text=f"Quantidade para {doc_p['nome']} (Estoque: {doc_p['quantidade_estoque']}):") \
                 .pack(pady=10, padx=10)

        # Cria um campo de entrada de texto para digitar a quantidade.
        # `pady=5` adiciona 5 pixels de espaço vertical.
        # `padx=10` adiciona 10 pixels de espaço horizontal.
        ent_qt = tk.Entry(janela_qt)
        ent_qt.pack(pady=5, padx=10)

        # Cria um botão com o texto "OK".
        # `command=confirmar` faz com que o botão execute a
        #       função `confirmar` ao ser clicado.
        # `pady=5` adiciona 5 pixels de espaço vertical.
        tk.Button(janela_qt, text="OK", command=confirmar).pack(pady=5)

        # Centraliza a janela ao carregá-la.
        # `after(0, lambda: centralizar_janela(janela_qt))` agenda a
        #       chamada da função para centralizar a janela.
        janela_qt.after(0, lambda: centralizar_janela(janela_qt))


    # Define a função que atualiza o conteúdo da lista de itens no carrinho.
    def atualizar_carrinho(self):

        # Remove todas as linhas atuais da árvore `lista_carrinho`
        #       para evitar duplicatas.
        # A função `get_children()` retorna todos os itens da árvore,
        #       que são deletados em seguida.
        for i in self.lista_carrinho.get_children():
            self.lista_carrinho.delete(i)

        # Inicializa a soma total dos valores dos itens no carrinho.
        # O valor `0.0` será usado como ponto de partida para
        #       acumular os subtotais dos produtos.
        soma = 0.0

        # Itera sobre cada item presente no carrinho para exibi-los na
        #       lista e calcular o total.
        for item in self.carrinho:

            # Calcula o subtotal de cada item multiplicando a
            #       quantidade pelo preço unitário.
            # Esse subtotal será exibido na coluna de subtotal da
            #       árvore e também somado ao total geral.
            subt = item["quantidade"] * item["preco_unitario"]

            # Adiciona o subtotal do item à soma total do carrinho.
            # O valor da soma acumula os subtotais de todos os itens,
            #       resultando no valor total.
            soma += subt

            # Insere uma nova linha na árvore `lista_carrinho` para
            #       exibir os detalhes do item.
            # Os valores exibidos incluem o nome do produto, quantidade, preço
            #       unitário formatado com duas casas decimais e o subtotal formatado da mesma forma.
            self.lista_carrinho.insert("",  # Insere o item na raiz da árvore (sem pai).
                                 "end",  # Adiciona o item ao final da lista.
                                        values=( item["nome"],  # Nome do produto.
                                                item["quantidade"],  # Quantidade do produto.
                                                f"{item['preco_unitario']:.2f}",  # Preço unitário formatado.
                                                f"{subt:.2f}"))  # Subtotal formatado.


        # Atualiza o texto do rótulo `lbl_total` para exibir o valor total calculado.
        # A formatação assegura que o valor total seja exibido com duas casas decimais.
        self.lbl_total.config(text=f"Total: R$ {soma:.2f}")


    # Define o método para atualizar a lista de
    #       clientes disponíveis no cache.
    def atualizar_clientes(self):

        # Obtém a lista atualizada de clientes do banco de dados.
        # Armazena os dados dos clientes no cache.
        self.lista_clientes_cache = self.db.listar_clientes()

        # Atualiza os valores exibidos na combobox de clientes.
        #       extrai os nomes dos clientes e define como valores da combobox.
        self.combo_cli["values"] = [cli["nome"] for cli in self.lista_clientes_cache]


    # Função para finalizar a venda
    def finalizar_venda(self):

        # Verifica se o carrinho está vazio
        # Caso não tenha itens no carrinho, exibe um erro e interrompe o processo.
        if not self.carrinho:
            messagebox.showerror("Erro", "Carrinho vazio!")
            return

        # Inicializa a variável `cliente_id` com `None`
        # Caso o cliente selecionado não seja encontrado,
        #       `cliente_id` permanecerá como `None`.
        cliente_id = None

        # Obtém o nome do cliente selecionado na interface
        # A partir da variável associada ao combobox de clientes.
        nome_cli = self.var_cli.get()

        # Caso um nome de cliente tenha sido selecionado
        if nome_cli:

            # Percorre a lista de clientes armazenada em cache
            for cc in self.lista_clientes_cache:

                # Verifica se o nome do cliente atual corresponde ao nome selecionado
                if cc["nome"] == nome_cli:

                    # Armazena o identificador do cliente em `cliente_id`
                    cliente_id = str(cc["_id"])

                    # Encerra a busca após encontrar o cliente correspondente
                    break

        # Obtém a forma de pagamento selecionada na interface
        forma = self.var_forma.get()

        # Inicializa uma lista para armazenar os itens da venda
        itens = []

        # Inicializa uma variável para calcular o total da venda
        total_final = 0

        # Itera sobre todos os itens atualmente no carrinho.
        for c_item in self.carrinho:

            # Multiplica a quantidade do item pelo preço unitário para obter o subtotal.
            # Por exemplo, se o cliente comprou 3 unidades a R$ 10,00 cada,
            # o subtotal será 3 * 10 = R$ 30,00.
            st = c_item["quantidade"] * c_item["preco_unitario"]

            # Incrementa o subtotal calculado ao valor total da venda.
            # Cada item do carrinho vai acumulando no total_final,
            #       que será o valor total da venda.
            total_final += st

            # Cria um dicionário com os detalhes do item que será
            #       registrado na venda.
            # - "produto_id": o identificador único do produto, necessário para
            #       registrar qual item foi vendido.
            # - "quantidade": a quantidade vendida desse produto.
            # - "preco_unitario": o preço de uma unidade do produto.
            # O `ObjectId(c_item["produto_id"])` é usado porque os IDs no
            #       banco de dados MongoDB são do tipo ObjectId.
            itens.append({"produto_id": ObjectId(c_item["produto_id"]),
                          "quantidade": c_item["quantidade"],
                          "preco_unitario": c_item["preco_unitario"]})

        # Registra a venda no banco de dados.
        # A função registrar_venda recebe os seguintes parâmetros:
        # - itens: uma lista contendo os itens vendidos.
        # - total_final: o valor total da venda.
        # - forma: a forma de pagamento escolhida.
        # - self.usuario["_id"]: o ID do usuário (vendedor) que está realizando a venda.
        # - cliente_id: o ID do cliente, se informado.
        id_venda = self.db.registrar_venda(itens,
                                           total_final,
                                           forma,
                                           self.usuario["_id"], cliente_id)

        # Mostra uma mensagem indicando que a venda foi registrada com sucesso.
        messagebox.showinfo("Sucesso",
                            "Venda registrada com sucesso!")

        # Limpa o carrinho, removendo todos os itens.
        self.carrinho.clear()

        # Atualiza a interface do carrinho para refletir que ele está vazio.
        self.atualizar_carrinho()

        # Atualiza a lista de clientes, caso haja alterações
        #       (como um novo cliente cadastrado).
        self.atualizar_clientes()

        # Cria uma nova janela para exibir a nota fiscal da venda.
        # A JanelaNotaFiscal exibe os detalhes da venda com
        #       base no id_venda recém-gerado.
        JanelaNotaFiscal(self, self.db, id_venda)



###############################################################################
# FUNÇÃO PARA GERAR PDF DA NOTA FISCAL
###############################################################################

# Define uma função para gerar um PDF da nota fiscal de uma venda.
# `venda`: dicionário contendo os dados da venda.
# `db`: instância da classe `GerenciadorBanco` para acessar dados adicionais.
# `nome_arquivo`: nome do arquivo PDF gerado (padrão: "nota_fiscal.pdf").
def gerar_pdf_nota_fiscal(venda, db: GerenciadorBanco, nome_arquivo="nota_fiscal.pdf"):

    # Cria um objeto `canvas` para gerar o PDF.
    # `pagesize=A4` define o tamanho da página como padrão A4.
    cnv = canvas.Canvas(nome_arquivo, pagesize=A4)

    # Obtém as dimensões da página A4 (largura e altura).
    largura, altura = A4

    # Define a margem esquerda da nota fiscal, com um
    #       espaço de 2 centímetros.
    margem_esq = 2 * cm

    # Define a posição inicial do topo da página, deixando 2
    #       centímetros de margem superior.
    topo = altura - 2 * cm

    # Define a altura de cada linha do texto dentro do PDF,
    #       espaçando 0.5 cm entre as linhas.
    alt_linha = 0.5 * cm

    # Define a fonte e o tamanho do texto para o título da nota fiscal.
    # `Helvetica-Bold, 16`: fonte em negrito com tamanho 16.
    cnv.setFont("Helvetica-Bold", 16)

    # Desenha o título da nota fiscal no PDF na posição especificada.
    # `margem_esq, topo`: define a posição do texto no canto superior da página.
    cnv.drawString(margem_esq, topo, "Loja de Brinquedos - Nota Fiscal")

    # Define a fonte e o tamanho do texto para os detalhes da venda.
    # `Helvetica, 10`: fonte padrão com tamanho 10.
    cnv.setFont("Helvetica", 10)

    # Desenha a data e hora da venda abaixo do título.
    # `topo - alt_linha`: move o texto uma linha para baixo.
    cnv.drawString(margem_esq,
                   topo - alt_linha,
                   f"Data/Hora da Venda: {venda['data_hora']}")

    # Define a posição inicial para os próximos textos,
    #       deixando um espaço adicional abaixo da data/hora.
    desloc = topo - 2 * alt_linha

    #  Verifica se há um cliente associado à venda.
    # `venda.get("cliente_id")`: tenta obter o ID do cliente,
    #       retorna None se não existir.
    if venda.get("cliente_id"):

        # Busca no banco de dados as informações do cliente com base no ID.
        doc_cli = db.col_clientes.find_one({"_id": venda["cliente_id"]})

        # Se o cliente foi encontrado no banco de dados, exibe
        #       seus dados na nota fiscal.
        if doc_cli:

            # Escreve o nome do cliente e o CPF/CNPJ na nota fiscal.
            # `margem_esq, desloc`: define a posição do texto na página.
            cnv.drawString(margem_esq,
                           desloc, f"Cliente: {doc_cli['nome']} - CPF/CNPJ: {doc_cli['cpf']}")

            # Reduz a posição vertical para evitar sobreposição de textos.
            desloc -= alt_linha

            # Escreve o endereço do cliente logo abaixo do nome e CPF/CNPJ.
            cnv.drawString(margem_esq,
                           desloc, f"Endereço: {doc_cli['endereco']}")

            # Reduz a posição novamente para manter espaçamento adequado.
            desloc -= alt_linha

    # Caso a venda não tenha um cliente associado,
    #       exibe "Cliente: Não informado" na nota fiscal.
    else:

        cnv.drawString(margem_esq, desloc, "Cliente: Não informado")

        # Reduz a posição vertical para evitar sobreposição de textos.
        desloc -= alt_linha

    # Busca no banco de dados as informações do vendedor responsável pela venda.
    doc_vend = db.col_usuarios.find_one({"_id": venda["vendedor_id"]})

    # Se o vendedor for encontrado no banco de dados,
    #       exibe seu nome na nota fiscal.
    if doc_vend:

        # Escreve o nome do vendedor na nota fiscal.
        cnv.drawString(margem_esq, desloc, f"Vendedor: {doc_vend['nome']}")

        # Reduz a posição vertical para evitar sobreposição de textos.
        desloc -= alt_linha

    # Escreve a forma de pagamento utilizada na venda.
    cnv.drawString(margem_esq, desloc,
                   f"Forma de Pagamento: {venda['forma_pagamento']}")

    # Reduz a posição vertical para evitar sobreposição de textos.
    desloc -= alt_linha

    # Desenha uma linha horizontal para separar as
    #       informações do cabeçalho dos itens vendidos.
    cnv.line(margem_esq, desloc, largura - margem_esq, desloc)

    # Reduz a posição vertical para continuar imprimindo as
    #       informações abaixo da linha.
    desloc -= alt_linha

    # Define a fonte em negrito tamanho 12 para destacar o
    #       título da seção de itens da venda.
    cnv.setFont("Helvetica-Bold", 12)

    # Escreve o título "Itens da Venda:" no PDF para
    #       indicar a lista de produtos vendidos.
    cnv.drawString(margem_esq, desloc, "Itens da Venda:")

    # Reduz a posição vertical para evitar sobreposição do próximo texto.
    desloc -= alt_linha

    # Define a fonte em negrito tamanho 10 para os
    #       cabeçalhos da tabela de itens.
    cnv.setFont("Helvetica-Bold", 10)

    # Adiciona os títulos das colunas da tabela no PDF
    #       para organizar os itens da venda.
    # Isso facilita a leitura e compreensão dos dados na nota fiscal.

    # Escreve o título da primeira coluna como "Produto", que
    #       representa o nome do item vendido.
    # Esta coluna conterá os nomes de cada produto listado na venda.
    cnv.drawString(margem_esq, desloc, "Produto")

    # Escreve o título da segunda coluna como "Qtd", que
    #       representa a quantidade do produto vendido.
    # Esta coluna mostrará quantas unidades do produto foram compradas.
    cnv.drawString(margem_esq + 6 * cm, desloc, "Qtd")

    # Escreve o título da terceira coluna como "Preço", que
    #       representa o valor unitário do produto.
    # Essa informação ajuda o cliente a entender o
    #       custo individual de cada item.
    cnv.drawString(margem_esq + 8 * cm, desloc, "Preço")

    # Escreve o título da quarta coluna como "Subtotal", que
    #       representa o valor total do item.
    # O subtotal é calculado multiplicando a quantidade
    #       pelo preço unitário do produto.
    cnv.drawString(margem_esq + 11 * cm, desloc, "Subtotal")

    # Reduz a posição vertical para começar a adicionar os
    #       itens vendidos na tabela.
    desloc -= alt_linha

    # Define a fonte normal tamanho 10 para os valores dos itens da venda.
    cnv.setFont("Helvetica", 10)

    # Inicializa a variável que armazenará o total geral da venda.
    total_geral = 0

    # Itera sobre a lista de itens vendidos para exibir
    #       cada um na nota fiscal.
    for item in venda["itens"]:

        # Busca no banco de dados o produto correspondente ao
        #       ID armazenado no item da venda.
        doc_p = db.col_produtos.find_one({"_id": item["produto_id"]})

        # Se o produto for encontrado no banco, armazena seu
        #       nome na variável 'nome_prod'.
        # Caso contrário, define o nome como "Desconhecido" para
        #       evitar erros caso o produto tenha sido removido.
        nome_prod = doc_p["nome"] if doc_p else "Desconhecido"

        # Calcula o subtotal do item, multiplicando a quantidade
        #       comprada pelo preço unitário do produto.
        subtotal = item["quantidade"] * item["preco_unitario"]

        # Adiciona o subtotal do item ao total geral da venda.
        total_geral += subtotal

        # Adiciona o nome do produto na coluna "Produto" da nota fiscal.
        # Para evitar sobreposição de texto, limita o nome a 25 caracteres.
        cnv.drawString(margem_esq, desloc, nome_prod[:25])

        # Adiciona a quantidade comprada do produto na coluna "Qtd".
        cnv.drawString(margem_esq + 6 * cm,
                       desloc,
                       str(item["quantidade"]))

        # Adiciona o preço unitário do produto na coluna "Preço",
        #       formatando como moeda (R$ XX.XX).
        cnv.drawString(margem_esq + 8 * cm,
                       desloc,
                       f"R$ {item['preco_unitario']:.2f}")

        # Adiciona o subtotal do item na coluna "Subtotal",
        #       formatando como moeda (R$ XX.XX).
        cnv.drawString(margem_esq + 11 * cm,
                       desloc,
                       f"R$ {subtotal:.2f}")

        # Move a posição vertical para a próxima linha da
        #       tabela, garantindo que os itens fiquem organizados.
        desloc -= alt_linha

    # Move a posição vertical para a próxima linha,
    #       separando os itens do total da venda.
    desloc -= alt_linha

    # Define a fonte do texto para negrito e tamanho 12,
    #       destacando o total da venda.
    cnv.setFont("Helvetica-Bold", 12)

    # Adiciona a linha com o total geral da venda,
    #       formatando o valor como moeda (R$ XX.XX).
    cnv.drawString(margem_esq, desloc, f"Total: R$ {venda['total']:.2f}")

    # Finaliza a página do PDF para que todos os
    #       conteúdos fiquem registrados corretamente.
    cnv.showPage()

    # Salva o arquivo PDF gerado, garantindo que os dados da
    #       nota fiscal sejam armazenados corretamente.
    cnv.save()


###############################################################################
# JANELA DE NOTA FISCAL
###############################################################################

# Define uma nova classe chamada JanelaNotaFiscal, que herda de tk.Toplevel.
# Essa classe será usada para exibir uma janela separada com informações
#       da nota fiscal de uma venda específica.
class JanelaNotaFiscal(tk.Toplevel):

    # O método __init__ inicializa a janela. Ele é chamado automaticamente
    # quando a classe é instanciada.
    def __init__(self, pai, db: GerenciadorBanco, id_venda):

        # Chama o método __init__ da classe pai (tk.Toplevel) para garantir
        # que a janela seja configurada corretamente.
        # `pai` é o widget pai da janela. Ele serve como a "base" na qual
        # essa nova janela será colocada.
        super().__init__(pai)

        # Define o título da janela como "Nota Fiscal - Loja de Brinquedos".
        # Isso será exibido na barra de título da janela.
        self.title("Nota Fiscal - Loja de Brinquedos")

        # Armazena a instância do GerenciadorBanco recebida como parâmetro na
        # variável self.db. Isso permite que outros métodos da classe acessem
        # o banco de dados diretamente.
        self.db = db

        # Obtém os dados da venda correspondente ao id_venda fornecido.
        # A função obter_venda_por_id é chamada no banco de dados para recuperar
        # todos os detalhes necessários para exibir a nota fiscal.
        self.dados_venda = db.obter_venda_por_id(id_venda)

        # Define a janela como não redimensionável. Isso significa que o usuário
        # não poderá alterar o tamanho da janela.
        self.resizable(False, False)

        # Define a janela como "transient" em relação à janela pai.
        # Isso garante que a nova janela ficará sempre acima da janela principal
        # e será fechada automaticamente se a janela principal for fechada.
        self.transient(pai)

        # Torna a janela modal, o que significa que o usuário não poderá interagir
        # com a janela principal enquanto esta estiver aberta.
        self.grab_set()

        # Define as dimensões iniciais da janela. O formato é "LARGURAxALTURA".
        # No caso, 700 pixels de largura por 600 pixels de altura.
        self.geometry("700x600")

        # Centraliza a janela na tela, chamando uma função auxiliar que calcula
        # as posições corretas e ajusta a posição da janela.
        centralizar_janela(self)

        # Cria um rótulo para exibir o nome da loja.
        # `text="Loja de Brinquedos"` define o texto exibido no rótulo.
        # `font=("Arial", 16, "bold")` define a fonte do texto
        #       como Arial, tamanho 16, em negrito.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
        tk.Label(self,
                 text="Loja de Brinquedos",
                 font=("Arial", 16, "bold")).pack(pady=5)

        # Cria outro rótulo para exibir o título "Nota Fiscal".
        # `text="Nota Fiscal"` define o texto exibido no rótulo.
        # `font=("Arial", 12, "bold")` define a fonte do texto
        #       como Arial, tamanho 12, em negrito.
        # Este rótulo aparece abaixo do primeiro, indicando que a
        #       nota fiscal está sendo exibida.
        tk.Label(self,
                 text="Nota Fiscal",
                 font=("Arial", 12, "bold")).pack()

        # Cria um quadro com borda para agrupar informações da nota fiscal.
        # `bd=1` define uma borda com 1 pixel de largura.
        # `relief="groove"` aplica um estilo de borda rebaixada.
        # `padx=10` e `pady=10` adicionam 10 pixels de
        #       espaçamento interno horizontal e vertical.
        frm_info = tk.Frame(self,
                            bd=1,
                            relief="groove",
                            padx=10,
                            pady=10)

        # Posiciona o quadro na janela principal.
        # `fill="x"` faz o quadro ocupar toda a largura disponível.
        # `pady=5` adiciona 5 pixels de espaçamento vertical ao redor do quadro.
        frm_info.pack(fill="x", pady=5)

        # Obtém a data e hora da venda dos dados carregados.
        data_hora = self.dados_venda["data_hora"]

        # Cria um rótulo dentro do quadro para exibir a data e hora da venda.
        # O texto é formatado com `f"Data/Hora: {data_hora}"` para
        #       incluir a data e hora no rótulo.
        # `anchor="w"` alinha o texto do rótulo à esquerda dentro do quadro.
        tk.Label(frm_info, text=f"Data/Hora: {data_hora}").pack(anchor="w")

        # Verifica se existe um cliente associado à venda.
        # `get("cliente_id")` retorna o ID do cliente se disponível,
        #       caso contrário, retorna `None`.
        if self.dados_venda.get("cliente_id"):

            # Busca o cliente no banco de dados utilizando o ID do cliente.
            # `find_one({"_id": self.dados_venda["cliente_id"]})` retorna o
            #       documento do cliente correspondente.
            doc_c = self.db.col_clientes.find_one({"_id": self.dados_venda["cliente_id"]})

            # Se o cliente for encontrado no banco de dados:
            if doc_c:

                # Exibe o nome e o CPF/CNPJ do cliente.
                # `f"Cliente: {doc_c['nome']} (CPF/CNPJ: {doc_c['cpf']})"`
                #       monta a string a ser exibida.
                # `anchor="w"` alinha o texto à esquerda dentro do quadro.
                tk.Label(frm_info,
                         text=f"Cliente: {doc_c['nome']} (CPF/CNPJ: {doc_c['cpf']})").pack(anchor="w")

                # Exibe o endereço do cliente.
                # `f"Endereço: {doc_c['endereco']}"` monta a string
                #       com o endereço do cliente.
                tk.Label(frm_info, text=f"Endereço: {doc_c['endereco']}").pack(anchor="w")

        # Caso não exista cliente associado à venda:
        else:

            # Exibe uma mensagem indicando que o cliente não foi informado.
            # `text="Cliente: Não informado"` define o texto do rótulo.
            # `anchor="w"` alinha o texto à esquerda dentro do quadro.
            tk.Label(frm_info, text="Cliente: Não informado").pack(anchor="w")

        # Busca o vendedor no banco de dados utilizando o ID armazenado na venda.
        # `find_one({"_id": self.dados_venda["vendedor_id"]})` retorna o
        #       documento do vendedor correspondente.
        doc_v = self.db.col_usuarios.find_one({"_id": self.dados_venda["vendedor_id"]})

        # Se o vendedor for encontrado no banco de dados:
        if doc_v:

            # Exibe o nome do vendedor responsável pela venda.
            # `f"Vendedor: {doc_v['nome']}"` monta a string a ser exibida.
            # `anchor="w"` alinha o texto à esquerda dentro do quadro.
            tk.Label(frm_info, text=f"Vendedor: {doc_v['nome']}").pack(anchor="w")

        # Cria um rótulo (Label) para exibir a forma de pagamento utilizada na venda.
        # `f"Forma de Pagamento: {self.dados_venda['forma_pagamento']}"`
        #       exibe a forma de pagamento selecionada.
        # `anchor="w"` alinha o texto à esquerda dentro do quadro de informações.
        tk.Label(frm_info,
                 text=f"Forma de Pagamento: {self.dados_venda['forma_pagamento']}").pack(anchor="w")

        # Cria um frame (quadro) para conter a tabela de itens vendidos.
        # `tk.Frame(self)` cria um novo quadro dentro da janela da nota fiscal.
        frm_itens = tk.Frame(self)

        # `pack(fill="both", expand=True, padx=10)` configura o layout do frame:
        # - `fill="both"` faz com que o quadro se expanda tanto na
        #       horizontal quanto na vertical.
        # - `expand=True` permite que o quadro ocupe todo o espaço disponível.
        # - `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do quadro.
        frm_itens.pack(fill="both", expand=True, padx=10)

        # Define as colunas da tabela que exibirá os itens da venda.
        # `("Produto", "Qtd", "Preço Unit.", "Subtotal")` são os títulos das colunas.
        colunas = ("Produto", "Qtd", "Preço Unit.", "Subtotal")

        # Cria um widget Treeview para exibir a lista de itens vendidos na nota fiscal.
        # `ttk.Treeview(frm_itens, columns=colunas, show="headings")`:
        # - `frm_itens` define o quadro onde a tabela será inserida.
        # - `columns=colunas` define as colunas da tabela.
        # - `show="headings"` oculta a coluna de índice padrão e
        #       exibe apenas os cabeçalhos das colunas definidas.
        self.tree = ttk.Treeview(frm_itens, columns=colunas, show="headings")

        # Configura cada coluna da tabela, definindo o nome e o tamanho.
        for c in colunas:

            # Define o cabeçalho da coluna com o nome correspondente.
            self.tree.heading(c, text=c)

            # Define a largura padrão da coluna como 100 pixels.
            self.tree.column(c, width=100)

        # Exibe a tabela na interface, posicionando-a corretamente no frame.
        # `side="left"` alinha a tabela à esquerda dentro do frame.
        # `fill="both"` permite que a tabela ocupe todo o espaço disponível.
        # `expand=True` faz com que o widget se ajuste
        #       automaticamente ao tamanho do frame.
        self.tree.pack(side="left", fill="both", expand=True)

        # Cria uma barra de rolagem vertical para a tabela de itens.
        # `tk.Scrollbar(frm_itens, orient="vertical", command=self.tree.yview)`:
        # - `frm_itens` define o quadro onde a barra de rolagem será inserida.
        # - `orient="vertical"` define a orientação da barra de rolagem como vertical.
        # - `command=self.tree.yview` associa a rolagem da barra à exibição da tabela.
        scroll_y = tk.Scrollbar(frm_itens,
                                orient="vertical",
                                command=self.tree.yview)

        # Configura a tabela para usar a barra de rolagem.
        # `yscrollcommand=scroll_y.set` permite que a barra de
        #       rolagem controle o deslocamento da tabela.
        self.tree.configure(yscrollcommand=scroll_y.set)

        # Exibe a barra de rolagem no lado direito do frame `frm_itens`.
        # `side="right"` posiciona a barra de rolagem à direita da tabela.
        # `fill="y"` faz com que a barra de rolagem preencha toda a altura do frame.
        scroll_y.pack(side="right", fill="y")

        # Inicializa a variável `total_venda`, que armazenará o
        #       valor total da venda.
        total_venda = 0

        # Percorre a lista de itens da venda para exibição na tabela (Treeview).
        for it in self.dados_venda["itens"]:

            # Busca o documento do produto no banco de dados pelo ID armazenado.
            # Caso o produto não seja encontrado, exibe "Desconhecido" como nome.
            prod_doc = self.db.col_produtos.find_one({"_id": it["produto_id"]})
            nome_p = prod_doc["nome"] if prod_doc else "Desconhecido"

            # Calcula o subtotal do item multiplicando a
            #       quantidade pelo preço unitário.
            subt = it["quantidade"] * it["preco_unitario"]

            # Adiciona o valor do subtotal ao total geral da venda.
            total_venda += subt

            # Insere o item na tabela de exibição (Treeview).
            # O nome do produto, a quantidade comprada, o preço unitário e o subtotal
            # são formatados corretamente para exibição no relatório da nota fiscal.
            self.tree.insert(

                "",  # Adiciona como um item raiz (sem pai).
                "end",  # Insere no final da tabela.
                values=(
                    nome_p,  # Nome do produto.
                    it["quantidade"],  # Quantidade adquirida.
                    f"{it['preco_unitario']:.2f}",  # Preço unitário formatado.
                    f"{subt:.2f}"  # Subtotal formatado.
                )
            )

        # Cria um frame na parte inferior da janela para exibir
        #       informações adicionais e botões.
        frm_bot = tk.Frame(self)

        # Expande horizontalmente e adiciona um espaçamento vertical.
        frm_bot.pack(fill="x", pady=5)

        # Adiciona um rótulo (Label) dentro do frame para exibir o valor total da venda.
        # O texto mostra "Total: R$" seguido do valor total
        #       formatado com duas casas decimais.
        # A fonte é Arial, tamanho 14 e em negrito para dar destaque.
        # A cor do texto é azul para ressaltar a informação na interface.
        tk.Label(

            frm_bot,  # O rótulo pertence ao frame frm_bot.
            text=f"Total: R$ {self.dados_venda['total']:.2f}",  # Exibe o valor total da venda.
            font=("Arial", 14, "bold"),  # Define a fonte como Arial, tamanho 14 e em negrito.
            fg="blue"  # Define a cor do texto como azul.

        # Alinha o rótulo à esquerda com um espaçamento horizontal de 10 pixels.
        ).pack(side="left", padx=10)

        # Cria um botão para exportar a nota fiscal para um arquivo PDF.
        # `text="Exportar PDF"` define o texto exibido no botão.
        # `command=self.exportar_pdf` associa a ação de exportar a
        #       nota fiscal para PDF ao clicar no botão.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
        ttk.Button(self,
                   text="Exportar PDF",
                   command=self.exportar_pdf).pack(pady=10)

        # Cria um botão para fechar a janela da nota fiscal.
        # `text="Fechar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do botão.
        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=10)


    # Define a função para exportar a nota fiscal para um arquivo PDF.
    def exportar_pdf(self):

        # `gerar_pdf_nota_fiscal(self.dados_venda, self.db)` chama a
        #       função responsável por gerar o PDF da nota fiscal.
        # Após a geração do PDF, exibe uma mensagem informando ao
        #       usuário que a nota fiscal foi exportada com sucesso.
        gerar_pdf_nota_fiscal(self.dados_venda, self.db)

        # Exibe uma mensagem informando que a nota fiscal foi exportada.
        # `messagebox.showinfo("PDF", "...")` cria uma caixa de
        #       diálogo com a informação da exportação.
        messagebox.showinfo("PDF",
                            "Nota Fiscal exportada em 'nota_fiscal.pdf'!")


###############################################################################
# QUADRO DE CLIENTES
###############################################################################

# Cria a classe `QuadroClientes`, responsável por exibir e
#       gerenciar os clientes cadastrados no sistema.
class QuadroClientes(tk.Frame):

    # Inicializa o quadro de clientes.
    # `pai` representa o container (janela ou aba) onde esse
    #       quadro será inserido.
    # `db` é a instância do banco de dados `GerenciadorBanco`,
    #       utilizada para acessar e manipular os dados dos clientes.
    def __init__(self, pai, db: GerenciadorBanco):

        # Chama o construtor da classe `tk.Frame` para
        #       garantir a correta inicialização do quadro.
        super().__init__(pai)

        # Armazena a referência ao banco de dados para acessar os clientes.
        self.db = db

        # Cria um scrollbar (barra de rolagem) vertical para a lista de clientes.
        # `self` refere-se ao quadro onde será inserida a barra de rolagem.
        # `orient="vertical"` define a orientação como vertical.
        scroll_y = tk.Scrollbar(self, orient="vertical")

        # Cria a lista de clientes usando um Treeview (tabela com cabeçalhos).
        # `self` refere-se ao quadro onde será inserida a lista de clientes.
        # `columns=(...)` define as colunas da tabela: Nome, CPF, Telefone, Email e Endereço.
        # `show="headings"` oculta a primeira coluna oculta do
        #       Treeview, exibindo apenas os cabeçalhos definidos.
        # `yscrollcommand=scroll_y.set` conecta a barra de rolagem
        #       vertical à lista para permitir rolagem quando houver muitos clientes.
        self.lista_clientes = ttk.Treeview(self,
                                            columns=("Nome", "CPF", "Telefone", "Email", "Endereço"),
                                            show="headings",
                                            yscrollcommand=scroll_y.set)

        # Configura a barra de rolagem para controlar a rolagem
        #       vertical da lista de clientes.
        # O `command=self.lista_clientes.yview` conecta a barra de
        #       rolagem à visualização vertical da Treeview,
        #       permitindo que a rolagem funcione corretamente ao movimentar a barra.
        scroll_y.config(command=self.lista_clientes.yview)

        # Posiciona a barra de rolagem à direita da lista de clientes dentro do frame.
        # `side="right"` indica que a barra de rolagem será posicionada
        #       no lado direito do widget Treeview.
        # `fill="y"` faz com que a barra ocupe toda a altura do widget,
        #       garantindo uma rolagem completa.
        scroll_y.pack(side="right", fill="y")

        # Configura os cabeçalhos e as colunas da lista de clientes.
        # Percorre a tupla contendo os nomes das colunas para definir suas propriedades.
        for c in ("Nome", "CPF", "Telefone", "Email", "Endereço"):

            # Define o nome exibido no cabeçalho da coluna correspondente na Treeview.
            # Isso permite que o usuário veja os títulos das colunas.
            self.lista_clientes.heading(c, text=c)

            # Define a largura padrão da coluna em 120 pixels para
            #       garantir um layout uniforme.
            # Isso evita que o conteúdo das colunas fique muito
            #       espremido ou desalinhado.
            self.lista_clientes.column(c, width=120)

        # Adiciona o widget Treeview ao frame para exibição da lista de clientes.
        # `fill="both"` faz com que o widget ocupe toda a largura e altura disponíveis no frame.
        # `expand=True` permite que o widget se expanda
        #       automaticamente se o frame for redimensionado.
        self.lista_clientes.pack(fill="both", expand=True)

        # Cria um frame (`frm_b`) que servirá como um contêiner para os botões da interface.
        # Isso permite organizar melhor os botões e manter um layout estruturado.
        frm_b = tk.Frame(self)

        # Posiciona o frame no layout principal.
        # `fill="x"` faz com que o frame ocupe toda a
        #       largura disponível da janela.
        frm_b.pack(fill="x")

        # Cria um botão para cadastrar um novo cliente.
        # `text="Cadastrar"` define o texto exibido no botão.
        # `command=self.cadastrar` vincula a função `cadastrar` ao botão,
        #       permitindo que a ação de cadastro seja executada quando o botão for pressionado.
        botao_cadastrar = tk.Button(frm_b, text="Cadastrar", command=self.cadastrar)

        # Posiciona o botão dentro do frame `frm_b`.
        # `side="left"` faz com que o botão fique alinhado à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       para melhorar a disposição visual.
        botao_cadastrar.pack(side="left", padx=5, pady=5)

        # Cria um botão para editar um cliente existente.
        # `text="Editar"` define o texto exibido no botão.
        # `command=self.editar` associa a função `editar` ao botão,
        # permitindo que a ação de edição seja executada ao pressioná-lo.
        botao_editar = tk.Button(frm_b, text="Editar", command=self.editar)

        # Posiciona o botão dentro do frame `frm_b`.
        # `side="left"` faz com que o botão fique alinhado à esquerda.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels entre os elementos.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       para uma melhor disposição.
        botao_editar.pack(side="left", padx=5, pady=5)

        # Cria um botão para excluir um cliente selecionado.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir` vincula a função `excluir` ao botão,
        # permitindo que a ação de exclusão seja executada quando pressionado.
        botao_excluir = tk.Button(frm_b, text="Excluir", command=self.excluir)

        # Posiciona o botão dentro do frame `frm_b`.
        # `side="left"` mantém o alinhamento à esquerda.
        # `padx=5` e `pady=5` garantem espaçamento adequado
        #       entre os elementos da interface.
        botao_excluir.pack(side="left", padx=5, pady=5)

        # Cria um botão para atualizar a lista de clientes.
        # `text="Atualizar"` define o texto exibido no botão.
        # `command=self.atualizar_lista` vincula a função `atualizar_lista` ao botão,
        #       permitindo que a lista de clientes seja recarregada e exibida corretamente.
        botao_atualizar = tk.Button(frm_b, text="Atualizar", command=self.atualizar_lista)

        # Posiciona o botão dentro do frame `frm_b`.
        # `side="left"` mantém o alinhamento à esquerda.
        # `padx=5` e `pady=5` mantêm a organização visual e evitam que
        #       os botões fiquem muito próximos.
        botao_atualizar.pack(side="left", padx=5, pady=5)

        # Associa um evento de duplo clique na lista de clientes.
        # Quando um cliente for clicado duas vezes na interface gráfica,
        #       a função `abrir_produtos_comprados` será chamada.
        # Isso permite visualizar os produtos comprados pelo cliente selecionado.
        self.lista_clientes.bind("<Double-1>", self.abrir_produtos_comprados)

        # Chama a função `atualizar_lista` para carregar os dados dos clientes
        #        assim que o quadro for criado, garantindo que a
        #       lista esteja sempre atualizada.
        self.atualizar_lista()


    # Define a função responsável por atualizar a lista de
    #       clientes exibida na interface.
    def atualizar_lista(self):

        # Remove todos os itens da `Treeview` de clientes antes de atualizar a lista.
        # Isso evita duplicação de dados ao carregar novas informações do banco.
        for i in self.lista_clientes.get_children():
            self.lista_clientes.delete(i)

        # Obtém a lista de clientes do banco de dados chamando `listar_clientes()`.
        # O banco retorna uma lista de dicionários contendo os dados de cada cliente.
        lista = self.db.listar_clientes()

        # Percorre a lista de clientes retornada pelo banco de dados.
        for c in lista:

            # Insere uma nova linha na `Treeview` para cada cliente
            #       encontrado no banco.
            # Cada linha representa um cliente e contém informações como
            #       nome, CPF, telefone, e-mail e endereço.
            self.lista_clientes.insert(

                # Insere a linha na raiz da `Treeview`, sem hierarquia.
                "",

                # Adiciona o item ao final da lista.
                "end",

                # Define os valores das colunas.
                values=(c["nome"], c["cpf"], c["telefone"], c["email"], c["endereco"]),

                # Converte o `_id` do MongoDB para string e usa como
                #       identificador único da linha.
                iid=str(c["_id"])

            )

    # Define a função responsável por abrir o formulário de
    #       cadastro de um novo cliente.
    def cadastrar(self):

        # Define uma função de callback que será chamada ao
        #       confirmar o cadastro do cliente.
        def cb(n, cp, tel, em, end):

            # Chama a função `cadastrar_cliente` do banco de dados
            #       para salvar os dados informados.
            self.db.cadastrar_cliente(n, cp, tel, em, end)

            # Atualiza a lista de clientes para exibir o novo cliente
            #       cadastrado na interface.
            self.atualizar_lista()

        # Cria e exibe a janela do formulário de cadastro de clientes,
        #       passando a função `cb` como callback.
        FormCliente(self, cb)


    # Define a função responsável por editar os dados de
    #       um cliente já cadastrado.
    def editar(self):

        # Obtém a seleção do usuário na lista de clientes.
        sel = self.lista_clientes.selection()

        # Verifica se algum cliente foi selecionado.
        if not sel:

            # Se nenhum cliente foi selecionado, exibe uma mensagem de
            #       aviso para o usuário.
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")

            return  # Sai da função sem fazer nada.

        # Obtém o ID do cliente selecionado na lista.
        id_c = sel[0]

        # Busca os dados do cliente selecionado no banco de
        #       dados utilizando seu ID.
        doc_c = self.db.col_clientes.find_one({"_id": ObjectId(id_c)})

        # Define uma função de callback que será chamada quando o
        #       usuário confirmar a edição do cliente.
        def cb(n, cp, tel, em, end):

            # Chama a função `atualizar_cliente` para modificar os
            #       dados do cliente no banco de dados.
            self.db.atualizar_cliente(id_c, n, cp, tel, em, end)

            # Atualiza a lista de clientes para refletir as alterações feitas.
            self.atualizar_lista()

        # Cria e exibe a janela do formulário de edição de clientes,
        #       passando a função `cb` como callback e os dados do cliente a ser editado.
        FormCliente(self, cb, doc_c)


    # Define a função responsável por excluir um cliente da base de dados.
    def excluir(self):

        # Obtém a seleção do usuário na lista de clientes.
        sel = self.lista_clientes.selection()

        # Verifica se algum cliente foi selecionado na lista.
        if not sel:

            # Se nenhum cliente foi selecionado, exibe um aviso ao usuário.
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")

            # Sai da função sem fazer nada.
            return

        # Obtém o ID do cliente selecionado.
        id_c = sel[0]

        # Exibe uma caixa de diálogo de confirmação para evitar exclusões acidentais.
        # Se o usuário confirmar a exclusão (clicar em "Sim"), o cliente será excluído.
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?"):

            # Chama a função `excluir_cliente` para remover o
            #       cliente do banco de dados.
            self.db.excluir_cliente(id_c)

            # Atualiza a lista de clientes na interface para
            #       refletir a exclusão do cliente.
            self.atualizar_lista()


    # Define a função que abre uma nova janela para exibir os
    #       produtos comprados por um cliente.
    def abrir_produtos_comprados(self, event):

        # Obtém a seleção do usuário na lista de clientes.
        sel = self.lista_clientes.selection()

        # Se nenhum cliente foi selecionado, a função retorna sem
        #       executar nenhuma ação.
        if not sel:
            return

        # Obtém o ID do cliente selecionado.
        id_c = sel[0]

        # Busca no banco de dados os detalhes do cliente usando o ID.
        doc_c = self.db.col_clientes.find_one({"_id": ObjectId(id_c)})

        # Se o cliente foi encontrado no banco de dados, abre a
        #       janela de produtos comprados.
        if doc_c:


            # Cria uma nova instância da classe `JanelaProdutosPorCliente`
            #       para exibir os produtos do cliente.
            # Passa a referência da janela atual (`self`), o banco de dados (`self.db`),
            #        o ID do cliente e o nome do cliente como parâmetros.
            JanelaProdutosPorCliente(self, self.db, str(doc_c["_id"]), doc_c["nome"])



###############################################################################
# JANELA PRODUTOS COMPRADOS POR CLIENTE (FILTRANDO POR DATA dd/mm/aaaa, ETC.)
###############################################################################

# Cria uma nova janela para exibir os produtos comprados
#       por um cliente específico.
class JanelaProdutosPorCliente(tk.Toplevel):

    # Método construtor (__init__) da classe JanelaProdutosPorCliente.
    # Inicializa a janela, recebendo:
    # - `pai`: a janela principal que chamou esta janela.
    # - `db`: uma instância de `GerenciadorBanco` para acessar os dados.
    # - `id_cliente`: o identificador único do cliente no banco de dados.
    # - `nome_cli`: o nome do cliente, para exibição na interface.
    def __init__(self, pai, db: GerenciadorBanco, id_cliente, nome_cli):

        # Chama o método __init__ da classe pai (tk.Toplevel),
        #       garantindo que a janela seja criada corretamente.
        super().__init__(pai)

        # Define o título da janela com o nome do cliente.
        self.title(f"Produtos de {nome_cli}")

        # Armazena a referência do banco de dados para acessar as informações.
        self.db = db

        # Armazena o ID do cliente para buscar seus produtos comprados.
        self.id_cl = id_cliente

        # Define o tamanho da janela como 800x400 pixels.
        self.geometry("1150x400")

        # Define esta janela como dependente da janela principal (`pai`).
        # Isso impede que o usuário interaja com a janela
        #       principal enquanto esta estiver aberta.
        self.transient(pai)

        # Impede que o usuário interaja com outras janelas
        #       até que esta seja fechada.
        self.grab_set()

        # Centraliza a janela na tela do usuário para melhor usabilidade.
        centralizar_janela(self)

        # Cria um frame para conter os filtros de pesquisa.
        # Este frame será utilizado para organizar os campos de entrada das datas.
        frm_filtro = tk.Frame(self)

        # Exibe o frame na interface gráfica.
        # `fill="x"` faz com que o frame ocupe toda a largura disponível da janela.
        # `padx=5` adiciona espaçamento lateral para melhor estética.
        # `pady=5` adiciona espaçamento vertical para separar
        #       dos outros elementos da interface.
        frm_filtro.pack(fill="x", padx=5, pady=5)

        # Cria um rótulo (Label) para indicar o campo de entrada da data inicial.
        # `text="Data Inicial (dd/mm/aaaa):"` define o texto exibido no rótulo.
        # `grid(row=0, column=0, padx=5)` posiciona o rótulo na primeira
        #       linha e primeira coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels para melhor alinhamento.
        tk.Label(frm_filtro,
                 text="Data Inicial (dd/mm/aaaa):").grid(row=0, column=0, padx=5)

        # Cria um campo de entrada (Entry) para que o usuário possa digitar a data inicial.
        # `width=10` define a largura do campo como 10 caracteres.
        self.ent_data_ini = tk.Entry(frm_filtro, width=10)

        # Exibe o campo de entrada na interface gráfica.
        # `grid(row=0, column=1, padx=5)` posiciona o campo na
        #       primeira linha e segunda coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels para
        #       evitar que fique muito colado ao rótulo.
        self.ent_data_ini.grid(row=0, column=1, padx=5)

        # Cria um rótulo (Label) para indicar o campo de entrada da data final.
        # `text="Data Final:"` define o texto exibido no rótulo.
        # `grid(row=0, column=2, padx=5)` posiciona o rótulo na
        #       primeira linha e terceira coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels
        #       para melhor alinhamento visual.
        tk.Label(frm_filtro,
                 text="Data Final:").grid(row=0, column=2, padx=5)

        # Cria um campo de entrada (Entry) para que o usuário
        #       possa digitar a data final.
        # `width=10` define a largura do campo como 10 caracteres,
        #       garantindo que a entrada fique compacta e alinhada.
        self.ent_data_fim = tk.Entry(frm_filtro, width=10)

        # Exibe o campo de entrada na interface gráfica.
        # `grid(row=0, column=3, padx=5)` posiciona o campo na primeira
        #       linha e quarta coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels
        #       para evitar que fique muito colado ao rótulo.
        self.ent_data_fim.grid(row=0, column=3, padx=5)

        # Cria um rótulo (Label) para indicar o campo de entrada do nome do produto.
        # `text="Produto:"` define o texto exibido no rótulo.
        # `grid(row=0, column=4, padx=5)` posiciona o rótulo na primeira
        #       linha e quinta coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels
        #       para uma melhor organização visual.
        tk.Label(frm_filtro,
                 text="Produto:").grid(row=0, column=4, padx=5)

        # Cria um campo de entrada (Entry) para que o usuário possa
        #       digitar o nome do produto desejado.
        # `width=15` define a largura do campo como 15 caracteres, garantindo
        #       espaço suficiente para nomes curtos e médios.
        self.ent_produto = tk.Entry(frm_filtro, width=15)

        # Exibe o campo de entrada na interface gráfica.
        # `grid(row=0, column=5, padx=5)` posiciona o campo na
        #       primeira linha e sexta coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels
        #       para evitar que fique muito colado ao rótulo.
        self.ent_produto.grid(row=0, column=5, padx=5)

        # Cria um rótulo para indicar o campo de entrada da forma de pagamento.
        # `text="Forma:"` define o texto exibido no rótulo.
        # `grid(row=0, column=6, padx=5)` posiciona o rótulo na
        #       primeira linha e sétima coluna do frame `frm_filtro`,
        #       garantindo um alinhamento correto e adicionando um
        #       espaçamento lateral de 5 pixels.
        tk.Label(frm_filtro, text="Forma:").grid(row=0, column=6, padx=5)

        # Cria um campo de entrada para que o usuário possa digitar a
        #       forma de pagamento desejada.
        # `width=10` define a largura do campo como 10 caracteres,
        #       adequado para opções como "Dinheiro" ou "Cartão".
        self.ent_forma = tk.Entry(frm_filtro, width=10)

        # Exibe o campo de entrada na interface gráfica.
        # `grid(row=0, column=7, padx=5)` posiciona o campo na primeira
        #       linha e oitava coluna do frame `frm_filtro`,
        #       adicionando um espaçamento lateral de 5 pixels
        #       para manter uma organização visual adequada.
        self.ent_forma.grid(row=0, column=7, padx=5)

        # Cria um rótulo para indicar o campo de entrada do subtotal.
        # `text="Subtotal:"` define o texto exibido no rótulo.
        # `grid(row=0, column=8, padx=5)` posiciona o rótulo na primeira
        #       linha e nona coluna do frame `frm_filtro`,
        #       garantindo um alinhamento correto e adicionando um
        #       espaçamento lateral de 5 pixels.
        tk.Label(frm_filtro, text="Subtotal:").grid(row=0, column=8, padx=5)

        # Cria um campo de entrada para que o usuário possa
        #       digitar o valor do subtotal.
        # `width=10` define a largura do campo como 10 caracteres,
        #       suficiente para exibir valores numéricos adequados.
        self.ent_subt = tk.Entry(frm_filtro, width=10)

        # Exibe o campo de entrada na interface gráfica.
        # `grid(row=0, column=9, padx=5)` posiciona o campo na primeira
        #       linha e décima coluna do frame `frm_filtro`,
        #       garantindo um espaçamento lateral de 5 pixels para
        #       manter uma organização visual apropriada.
        self.ent_subt.grid(row=0, column=9, padx=5)

        # Cria um botão para aplicar os filtros e buscar os produtos
        #       conforme os critérios informados.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a função `filtrar` ao botão, que
        #       será chamada quando o usuário clicar.
        # `grid(row=0, column=10, padx=5)` posiciona o botão na primeira
        #       linha e décima primeira coluna do frame `frm_filtro`,
        #       garantindo um espaçamento lateral de 5 pixels
        #       para um layout organizado.
        tk.Button(frm_filtro,
                  text="Filtrar",
                  command=self.filtrar).grid(row=0, column=10, padx=5)

        # Define as colunas da tabela que será usada para exibir os
        #       produtos comprados pelo cliente.
        # As colunas incluem "Data" (data da compra), "Produto" (nome do produto),
        # "Forma" (forma de pagamento) e "Subtotal" (valor total da compra do item).
        colunas = ("Data", "Produto", "Forma", "Subtotal")

        # Cria uma tabela `Treeview` para exibir os produtos
        #       filtrados na interface gráfica.
        # `columns=colunas` define as colunas a serem exibidas na tabela.
        # `show="headings"` indica que apenas os cabeçalhos das
        #       colunas devem ser exibidos,
        #       ocultando a primeira coluna padrão da `Treeview`.
        self.tree = ttk.Treeview(self,
                                 columns=colunas,
                                 show="headings")

        # Percorre a lista de colunas e define o cabeçalho e a
        #       largura de cada uma na tabela.
        # `self.tree.heading(c, text=c)` define o nome do cabeçalho da coluna.
        # `self.tree.column(c, width=120)` ajusta a largura de
        #       cada coluna para 120 pixels.
        for c in colunas:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)

        # Adiciona a tabela `Treeview` ao layout da janela,
        #       ocupando todo o espaço disponível.
        # `fill="both"` permite que a tabela se expanda horizontalmente e verticalmente.
        # `expand=True` faz com que o widget ocupe todo o espaço extra disponível.
        self.tree.pack(fill="both", expand=True)

        # Chama a função `_carregar_dados()` para buscar os dados no
        #       banco de dados e armazená-los na variável `self.dados`.
        self.dados = self._carregar_dados()

        # Chama a função `_exibir()` para preencher a tabela
        #       com os dados carregados.
        self._exibir(self.dados)


    # Define um método privado `_carregar_dados` responsável por buscar e
    #       organizar os dados de vendas do cliente.
    def _carregar_dados(self):

        # Inicializa uma lista vazia `lista` para armazenar os
        #       dados das vendas do cliente.
        lista = []

        # Busca todas as vendas associadas ao cliente específico no banco de dados.
        # `self.db.col_vendas.find({"cliente_id": ObjectId(self.id_cl)})`
        #       retorna um cursor com todas as vendas cujo `cliente_id`
        #       corresponde ao ID do cliente selecionado.
        docs_vendas = self.db.col_vendas.find({"cliente_id": ObjectId(self.id_cl)})

        # Itera sobre cada venda encontrada no banco de dados.
        for vd in docs_vendas:

            # Converte a data da venda do formato ISO (ex.: "2023-08-27T14:35:22")
            #       para um objeto `datetime.date`.
            data_obj = converter_iso_para_date(vd["data_hora"])

            # Converte a data do objeto `datetime.date` para o
            #       formato brasileiro "dd/mm/aaaa".
            data_br = converter_date_para_str_br(data_obj)

            # Obtém a forma de pagamento utilizada na venda.
            forma = vd["forma_pagamento"]

            # Percorre cada item da venda para obter os detalhes do produto vendido.
            for it in vd["itens"]:

                # Busca no banco de dados o documento do produto com base
                #       no ID armazenado na venda.
                prod_doc = self.db.col_produtos.find_one({"_id": it["produto_id"]})

                # Se o produto for encontrado, obtém o nome dele, caso
                #       contrário, define como "Desconhecido".
                nome_prod = prod_doc["nome"] if prod_doc else "Desconhecido"

                # Calcula o subtotal do item, multiplicando a quantidade
                #       comprada pelo preço unitário do produto.
                subt = it["quantidade"] * it["preco_unitario"]

                # Adiciona os dados estruturados do item da venda na
                #       lista que será retornada.
                lista.append({
                    "data_obj": data_obj,  # Data da venda como objeto datetime.date.
                    "data_br": data_br,  # Data da venda formatada no padrão "dd/mm/aaaa".
                    "produto": nome_prod,  # Nome do produto vendido.
                    "forma": forma,  # Forma de pagamento utilizada na venda.
                    "subt_str": f"{subt:.2f}",  # Subtotal formatado como string para exibição.
                    "subt_val": subt  # Subtotal como valor numérico para cálculos.
                })

        # Retorna a lista contendo os produtos vendidos, suas
        #       respectivas datas, formas de pagamento e subtotais.
        return lista

    # Método responsável por exibir os dados na tabela (Treeview).
    def _exibir(self, lista_dados):

        # Remove todas as linhas existentes na tabela antes de inserir novos dados.
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Percorre a lista de dados e insere cada item como
        #       uma nova linha na tabela.
        for d in lista_dados:
            self.tree.insert(
                "",  # Define que a linha será inserida na raiz da árvore (sem hierarquia).
                "end",  # Adiciona a linha no final da lista.
                values=(
                    d["data_br"],  # Exibe a data da venda no formato "dd/mm/aaaa".
                    d["produto"],  # Exibe o nome do produto vendido.
                    d["forma"],  # Exibe a forma de pagamento utilizada na venda.
                    d["subt_str"]  # Exibe o subtotal formatado da venda.
                )
            )

    # Método responsável por filtrar os dados exibidos na tabela
    #       com base nos critérios informados.
    def filtrar(self):

        # Obtém e converte a data inicial inserida no campo para o formato correto.
        dt_ini = analisar_data_br(self.ent_data_ini.get())

        # Obtém e converte a data final inserida no campo para o formato correto.
        dt_fim = analisar_data_br(self.ent_data_fim.get())

        # Obtém o texto digitado no campo de produto e converte
        #       para minúsculas para facilitar a busca.
        prod_f = self.ent_produto.get().lower().strip()

        # Obtém a forma de pagamento digitada e converte para
        #       minúsculas para facilitar a busca.
        forma_f = self.ent_forma.get().lower().strip()

        # Obtém o valor do subtotal digitado e converte para
        #       minúsculas para facilitar a busca.
        subt_f = self.ent_subt.get().lower().strip()

        # Lista onde serão armazenados os resultados filtrados.
        filtrados = []

        # Percorre todos os dados carregados para aplicar os filtros
        for d in self.dados:

            # Verifica se a data do item é menor que a data inicial filtrada
            if dt_ini and d["data_obj"] and d["data_obj"] < dt_ini:

                # Se for menor, pula para o próximo item
                continue

            # Verifica se a data do item é maior que a data final filtrada
            if dt_fim and d["data_obj"] and d["data_obj"] > dt_fim:

                # Se for maior, pula para o próximo item
                continue

            # Verifica se o nome do produto contém o texto digitado no filtro
            # Converte para minúsculas para garantir que a busca não
            #       seja sensível a maiúsculas/minúsculas
            if prod_f and prod_f not in d["produto"].lower():

                # Se não contém, pula para o próximo item
                continue

            # Verifica se a forma de pagamento corresponde ao filtro digitado
            # Converte para minúsculas para garantir que a busca não
            #       seja sensível a maiúsculas/minúsculas
            if forma_f and forma_f not in d["forma"].lower():

                # Se não contém, pula para o próximo item
                continue

            # Verifica se o subtotal contém o valor digitado no filtro
            # Converte para minúsculas para evitar erros de correspondência
            if subt_f and subt_f not in d["subt_str"].lower():

                # Se não contém, pula para o próximo item
                continue

            # Se o item passou por todos os filtros,
            #       adiciona à lista de itens filtrados
            filtrados.append(d)

        # Exibe na interface apenas os itens que passaram pelo filtro
        self._exibir(filtrados)



# Cria uma nova janela do tipo `Toplevel`, que será utilizada
#       para cadastro ou edição de clientes.
# `class FormCliente(tk.Toplevel)` define uma nova classe
#       que herda de `tk.Toplevel`.
class FormCliente(tk.Toplevel):

    # Método construtor da classe `FormCliente`.
    # `__init__` inicializa a janela de formulário de cliente e recebe os parâmetros:
    # - `pai`: a janela principal ou pai que chamou este formulário.
    # - `func_cb`: uma função de callback que será chamada ao confirmar o cadastro ou edição.
    # - `dados`: um dicionário opcional contendo os dados do cliente, caso seja uma edição.
    def __init__(self, pai, func_cb, dados=None):

        # Chama o construtor da classe `Toplevel` para inicializar a nova janela.
        super().__init__(pai)

        # Define o título da janela como "Cadastro/Editar Cliente".
        # Isso permite que o usuário saiba se está cadastrando um
        #       novo cliente ou editando um existente.
        self.title("Cadastro/Editar Cliente")

        # Armazena a função de callback `func_cb` para ser
        #       utilizada ao salvar os dados do cliente.
        # Essa função será chamada ao confirmar o cadastro ou edição.
        self.func_cb = func_cb

        # Impede que a janela seja redimensionada pelo usuário.
        # `False, False` indica que a largura e altura não podem ser alteradas.
        self.resizable(False, False)

        # Define esta janela como dependente da janela principal (`pai`).
        # Isso impede que o usuário interaja com a janela
        #       principal enquanto esta está aberta.
        self.transient(pai)

        # Captura o foco da janela, garantindo que o usuário não
        #       possa interagir com outras janelas
        #       até que esta seja fechada.
        self.grab_set()

        # Cria um rótulo (label) com o texto "Nome:" para indicar ao usuário
        #       qual informação deve ser preenchida no campo ao lado.
        # `row=0, column=0` posiciona o rótulo na primeira linha e primeira coluna.
        # `padx=5, pady=5` adiciona espaçamento interno para melhor legibilidade.
        # `sticky="e"` alinha o texto à direita dentro da célula da grade.
        tk.Label(self, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (Entry) onde o usuário pode digitar o nome do cliente.
        # O campo é posicionado na linha 0 e coluna 1, ao lado do rótulo "Nome:".
        # `padx=5, pady=5` garante espaçamento para melhor aparência e organização.
        self.ent_nome = tk.Entry(self)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo (label) com o texto "CPF/CNPJ:" para indicar ao usuário
        #       que ele deve inserir o CPF ou CNPJ do cliente.
        # `row=1, column=0` posiciona o rótulo na segunda linha e primeira coluna.
        # `padx=5, pady=5` adiciona espaçamento interno para melhor legibilidade.
        # `sticky="e"` alinha o texto à direita dentro da célula da grade.
        tk.Label(self,
                 text="CPF/CNPJ:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (Entry) onde o usuário pode
        #       digitar o CPF ou CNPJ do cliente.
        # O campo é posicionado na linha 1 e coluna 1, ao lado do rótulo "CPF/CNPJ:".
        # `padx=5, pady=5` garante espaçamento para melhor aparência e organização.
        self.ent_cpf = tk.Entry(self)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo (label) com o texto "Telefone:" para indicar ao usuário
        #       que ele deve inserir o telefone do cliente.
        # `row=2, column=0` posiciona o rótulo na terceira linha e primeira coluna.
        # `padx=5, pady=5` adiciona espaçamento interno para melhor legibilidade.
        # `sticky="e"` alinha o texto à direita dentro da célula da grade.
        tk.Label(self,
                 text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (Entry) onde o usuário pode digitar o telefone do cliente.
        # O campo é posicionado na linha 2 e coluna 1, ao lado do rótulo "Telefone:".
        # `padx=5, pady=5` garante espaçamento para melhor aparência e organização.
        self.ent_tel = tk.Entry(self)
        self.ent_tel.grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo (label) com o texto "Email:" para indicar ao usuário
        #       que ele deve inserir o email do cliente.
        # `row=3, column=0` posiciona o rótulo na quarta linha e primeira coluna.
        # `padx=5, pady=5` adiciona espaçamento interno para melhor legibilidade.
        # `sticky="e"` alinha o texto à direita dentro da célula da grade.
        tk.Label(self,
                 text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (Entry) onde o usuário pode digitar o email do cliente.
        # O campo é posicionado na linha 3 e coluna 1, ao lado do rótulo "Email:".
        # `padx=5, pady=5` garante espaçamento para melhor aparência e organização.
        self.ent_email = tk.Entry(self)
        self.ent_email.grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo (label) com o texto "Endereço:" para indicar ao usuário
        #       que ele deve inserir o endereço do cliente.
        # `row=4, column=0` posiciona o rótulo na quinta linha e primeira coluna.
        # `padx=5, pady=5` adiciona espaçamento interno para melhor organização e legibilidade.
        # `sticky="e"` alinha o texto à direita dentro da célula da grade.
        tk.Label(self,
                 text="Endereço:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (Entry) onde o usuário pode digitar o endereço do cliente.
        # O campo é posicionado na linha 4 e coluna 1, ao lado do rótulo "Endereço:".
        # `padx=5, pady=5` garante espaçamento ao redor do campo
        #       para uma melhor organização.
        self.ent_end = tk.Entry(self)
        self.ent_end.grid(row=4, column=1, padx=5, pady=5)

        # Cria um frame (quadro) para organizar os botões "Salvar" e "Cancelar".
        # `row=5, column=0, columnspan=2` posiciona o frame na sexta
        #       linha e faz com que ele ocupe duas colunas.
        # `pady=10` adiciona um espaçamento vertical para
        #       separar os botões dos campos de entrada.
        frm_b = tk.Frame(self)
        frm_b.grid(row=5, column=0, columnspan=2, pady=10)

        # Cria um botão para salvar os dados inseridos pelo usuário.
        # `text="Salvar"` define o texto exibido no botão.
        # `command=self.ao_salvar` associa a ação de salvar os dados ao clicar no botão.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal entre os botões.
        tk.Button(frm_b,
                  text="Salvar",
                  command=self.ao_salvar).pack(side="left", padx=5)

        # Cria um botão para cancelar e fechar a janela de cadastro.
        # `text="Cancelar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `side="left"` alinha o botão à esquerda dentro do frame.
        # `padx=5` adiciona um espaçamento horizontal entre os botões.
        tk.Button(frm_b,
                  text="Cancelar",
                  command=self.destroy).pack(side="left", padx=5)

        # Verifica se há dados do cliente para edição.
        # Caso existam, preenche automaticamente os campos de
        #       entrada com as informações do cliente selecionado.
        if dados:

            # Insere o nome do cliente no campo correspondente.
            self.ent_nome.insert(0, dados["nome"])

            # Insere o CPF/CNPJ do cliente no campo correspondente.
            self.ent_cpf.insert(0, dados["cpf"])

            # Insere o telefone do cliente no campo correspondente.
            self.ent_tel.insert(0, dados["telefone"])

            # Insere o email do cliente no campo correspondente.
            self.ent_email.insert(0, dados["email"])

            # Insere o endereço do cliente no campo correspondente.
            self.ent_end.insert(0, dados["endereco"])

        # Após a criação da janela, centraliza automaticamente na tela.
        # `self.after(0, lambda: centralizar_janela(self))`
        #       chama a função `centralizar_janela`
        #       assim que possível, garantindo que a janela apareça
        #       centralizada no monitor.
        self.after(0, lambda: centralizar_janela(self))


    # Define a função que será chamada ao clicar no botão "Salvar".
    def ao_salvar(self):

        # Obtém e remove espaços em branco no início e no
        #       fim do texto digitado no campo "Nome".
        n = self.ent_nome.get().strip()

        # Obtém e remove espaços em branco no início e no fim do
        #       texto digitado no campo "CPF/CNPJ".
        cp = self.ent_cpf.get().strip()

        # Obtém e remove espaços em branco no início e no fim do
        #       texto digitado no campo "Telefone".
        t = self.ent_tel.get().strip()

        # Obtém e remove espaços em branco no início e no fim do
        #       texto digitado no campo "Email".
        e = self.ent_email.get().strip()

        # Obtém e remove espaços em branco no início e no fim do
        #       texto digitado no campo "Endereço".
        end = self.ent_end.get().strip()

        # Verifica se o campo "Nome" está vazio.
        # Se estiver vazio, exibe uma mensagem de erro e
        #       interrompe a execução da função.
        if not n:
            messagebox.showerror("Erro", "Campo 'Nome' é obrigatório!")
            return

        # Chama a função `func_cb`, passando os valores obtidos
        #       dos campos de entrada.
        # Essa função é responsável por salvar ou atualizar os
        #       dados do cliente no banco de dados.
        self.func_cb(n, cp, t, e, end)

        # Fecha a janela de cadastro/edição após a execução
        #       da função de callback.
        self.destroy()



###############################################################################
# QUADRO DE FORNECEDORES
###############################################################################

# Cria um quadro (Frame) para gerenciar os
#       fornecedores dentro da interface gráfica
class QuadroFornecedores(tk.Frame):

    # Método construtor da classe QuadroFornecedores
    # `pai` representa o componente pai ao qual esse quadro será vinculado
    # `db` é uma instância do GerenciadorBanco para acesso ao banco de dados
    def __init__(self, pai, db: GerenciadorBanco):

        # Chama o construtor da classe pai (tk.Frame) para
        #       inicializar corretamente o quadro
        super().__init__(pai)

        # Armazena a referência ao banco de dados para operações futuras
        self.db = db

        # Cria uma barra de rolagem vertical para a lista de fornecedores
        scroll_y = tk.Scrollbar(self, orient="vertical")

        # Cria uma tabela (Treeview) para exibir os fornecedores cadastrados
        self.lista = ttk.Treeview(

            self,  # Define que a tabela pertence ao quadro atual
            columns=("Nome", "CNPJ", "Telefone", "Email", "Endereço"),  # Define as colunas da tabela
            show="headings",  # Oculta a primeira coluna de índice (por padrão, o Treeview tem uma coluna extra)
            yscrollcommand=scroll_y.set  # Conecta a barra de rolagem vertical à tabela

        )

        # Configura a barra de rolagem para controlar a visualização da tabela
        scroll_y.config(command=self.lista.yview)

        # Posiciona a barra de rolagem no lado direito do quadro e
        #       permite que ela preencha toda a altura
        scroll_y.pack(side="right", fill="y")

        # Percorre todas as colunas definidas para a tabela de fornecedores
        for c in ("Nome", "CNPJ", "Telefone", "Email", "Endereço"):

            # Define o cabeçalho da coluna, ou seja, o nome exibido na interface
            self.lista.heading(c, text=c)

            # Define a largura de cada coluna para melhor visualização dos dados
            self.lista.column(c, width=120)

        # Empacota a lista de fornecedores para ocupar todo o
        #       espaço disponível na janela.
        # `fill="both"` faz com que a lista se expanda tanto
        #       horizontalmente quanto verticalmente.
        # `expand=True` permite que a lista utilize todo o espaço
        #       disponível conforme a janela for redimensionada.
        self.lista.pack(fill="both", expand=True)

        # Cria um contêiner (frame) para organizar os botões abaixo da lista.
        # Isso facilita o layout e a organização dos elementos na interface.
        frm_b = tk.Frame(self)

        # Empacota o frame de botões para que ele ocupe toda a largura da janela.
        # `fill="x"` faz com que o frame se estenda horizontalmente.
        frm_b.pack(fill="x")

        # Cria um botão para cadastrar um novo fornecedor.
        # `text="Cadastrar"` define o texto exibido no botão.
        # `command=self.cadastrar` associa a ação de abrir o
        #       formulário de cadastro ao clicar no botão.
        # `side="left"` posiciona o botão no lado esquerdo do frame.
        # `padx=5, pady=5` adiciona espaçamento ao redor do
        #       botão para melhor organização visual.
        tk.Button(frm_b,
                  text="Cadastrar",
                  command=self.cadastrar).pack(side="left", padx=5, pady=5)

        # Cria um botão para editar um fornecedor existente.
        # `text="Editar"` define o texto exibido no botão.
        # `command=self.editar` associa a ação de abrir o
        #       formulário de edição ao clicar no botão.
        # `side="left"` posiciona o botão no lado esquerdo do frame.
        # `padx=5, pady=5` adiciona espaçamento ao redor do botão
        #       para manter o alinhamento adequado.
        tk.Button(frm_b,
                  text="Editar",
                  command=self.editar).pack(side="left", padx=5, pady=5)

        # Cria um botão para excluir um fornecedor.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir` associa a ação de exclusão ao clicar no botão.
        # `side="left"` posiciona o botão no lado esquerdo do frame.
        # `padx=5, pady=5` adiciona espaçamento ao redor do botão
        #       para melhor organização visual.
        tk.Button(frm_b,
                  text="Excluir",
                  command=self.excluir).pack(side="left", padx=5, pady=5)

        # Cria um botão para atualizar a lista de fornecedores.
        # `text="Atualizar"` define o texto exibido no botão.
        # `command=self.atualizar_lista` associa a ação de
        #       recarregar a lista ao clicar no botão.
        # `side="left"` posiciona o botão no lado esquerdo do frame.
        # `padx=5, pady=5` adiciona espaçamento ao redor do botão
        #       para manter o alinhamento adequado.
        tk.Button(frm_b,
                  text="Atualizar",
                  command=self.atualizar_lista).pack(side="left", padx=5, pady=5)

        # Associa o evento de clique duplo em uma linha da lista
        #       para abrir as vendas do fornecedor.
        # `<Double-1>` significa o primeiro botão do mouse clicado duas vezes.
        # `self.abrir_vendas_fornecedor` é a função chamada ao detectar o clique duplo.
        self.lista.bind("<Double-1>", self.abrir_vendas_fornecedor)

        # Atualiza a lista de fornecedores, preenchendo-a com
        #       dados atualizados do banco de dados.
        # Chama o método `atualizar_lista` para reatualizar os
        #       elementos exibidos na Treeview.
        self.atualizar_lista()


    # Define o método `abrir_vendas_fornecedor`, que será chamado quando o usuário
    # clicar duas vezes em um fornecedor da lista.
    def abrir_vendas_fornecedor(self, event):

        # Obtém os itens selecionados na lista.
        # `self.lista.selection()` retorna os identificadores
        #       dos itens selecionados.
        sel = self.lista.selection()

        # Caso nenhum fornecedor esteja selecionado, o
        #       método retorna sem fazer nada.
        if not sel:
            return

        # `id_f` é o identificador único do fornecedor selecionado.
        # Estamos assumindo o primeiro item (index 0) como o fornecedor em foco.
        id_f = sel[0]

        # Busca os dados do fornecedor no banco de dados utilizando o identificador.
        # `self.db.col_fornecedores.find_one()` retorna um
        #       documento (dicionário) correspondente
        #       ao fornecedor com o ID fornecido.
        doc_f = self.db.col_fornecedores.find_one({"_id": ObjectId(id_f)})

        # Se um documento válido foi encontrado no banco,
        #       abre uma nova janela de vendas
        #       relacionadas a este fornecedor. Esta janela é instanciada
        #       com os dados do fornecedor,
        #       como o ID e o nome, para exibir as vendas correspondentes.
        if doc_f:
            JanelaVendasFornecedor(self,
                                   self.db, str(doc_f["_id"]), doc_f["nome"])


    # Define um método chamado `cadastrar` na classe.
    # Esse método será usado para iniciar o processo de
    #       cadastro de um novo fornecedor.
    def cadastrar(self):

        # Define uma função de callback `cb` que será chamada quando os
        #       dados do fornecedor forem confirmados.
        # Essa função:
        # - Recebe os dados do fornecedor (nome, cnpj, telefone, email, endereço).
        # - Chama o método `cadastrar_fornecedor` do banco para salvar os dados.
        # - Atualiza a lista de fornecedores exibida.
        def cb(n, c, t, e, end):

            self.db.cadastrar_fornecedor(n, c, t, e, end)
            self.atualizar_lista()

        # Cria uma instância da classe `FormFornecedor`, passando:
        # - `self` como pai para a nova janela.
        # - `cb` como a função de callback a ser chamada após a
        #       confirmação do cadastro.
        FormFornecedor(self, cb)


    # Define o método `editar`, que permitirá modificar os dados
    #       de um fornecedor existente.
    def editar(self):

        # Obtém os itens selecionados na lista.
        # `self.lista.selection()` retorna os identificadores dos itens selecionados.
        sel = self.lista.selection()

        # Caso nenhum fornecedor esteja selecionado, exibe uma
        #       mensagem de alerta e interrompe o processo.
        if not sel:
            messagebox.showwarning("Aviso",
                                   "Selecione um fornecedor para editar.")
            return

        # `id_f` é o identificador único do fornecedor selecionado.
        # O método `selection()` retorna uma lista, mas como o
        #       Treeview permite selecionar múltiplos itens,
        #       estamos assumindo o primeiro item (index 0) como o selecionado.
        id_f = sel[0]

        # Consulta no banco de dados o documento do fornecedor correspondente ao ID selecionado.
        # `find_one` retorna um dicionário com os dados do fornecedor.
        doc_f = self.db.col_fornecedores.find_one({"_id": ObjectId(id_f)})

        # Define uma função de callback chamada `cb`.
        # Essa função será chamada quando o formulário for confirmado.
        # Recebe os dados atualizados do fornecedor, atualiza o banco de dados
        #       e chama `atualizar_lista` para refletir as mudanças na interface.
        def cb(n, c, t, em, end):

            # Atualiza o documento do fornecedor no banco de dados.
            self.db.atualizar_fornecedor(id_f, n, c, t, em, end)

            # Atualiza a lista de fornecedores exibida.
            self.atualizar_lista()

        # Cria uma instância de `FormFornecedor`.
        # Passa a si mesmo (`self`) como pai para a nova janela.
        # Passa `cb` como a função a ser chamada após o envio do formulário.
        # Passa `doc_f` (os dados atuais do fornecedor) para
        #       preencher o formulário com os valores existentes.
        FormFornecedor(self, cb, doc_f)


    # Define o método `excluir`, que será responsável por
    #       remover um fornecedor da lista.
    def excluir(self):

        # Obtém os itens selecionados na lista.
        # `self.lista.selection()` retorna os identificadores
        #       dos itens selecionados.
        sel = self.lista.selection()

        # Caso nenhum fornecedor esteja selecionado, exibe uma
        #       mensagem de alerta e interrompe o processo.
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um fornecedor para excluir.")
            return

        # `id_f` é o identificador único do fornecedor selecionado.
        # O método `selection()` retorna uma lista, mas como o
        #       Treeview permite selecionar múltiplos itens,
        # o primeiro item (index 0) como o selecionado.
        id_f = sel[0]

        # Exibe uma caixa de diálogo de confirmação.
        # Caso o usuário confirme a exclusão, o retorno será `True`.
        # Se o usuário cancelar, nada será feito.
        if messagebox.askyesno("Confirmação",
                               "Deseja excluir este fornecedor?"):

            # Remove o fornecedor do banco de dados usando o identificador único.
            self.db.excluir_fornecedor(id_f)

            # Atualiza a lista de fornecedores exibida, refletindo a exclusão.
            self.atualizar_lista()


    # Define um método chamado `atualizar_lista` dentro da classe.
    # Esse método será usado para atualizar os dados exibidos na Treeview.
    def atualizar_lista(self):

        # Limpa a Treeview removendo todas as entradas atuais.
        # Garante que a Treeview exibirá apenas informações atualizadas.
        for i in self.lista.get_children():
            self.lista.delete(i)

        # Obtém a lista mais recente de fornecedores do banco de dados.
        # Chama o método `listar_fornecedores` no banco para recuperar os dados.
        forn_list = self.db.listar_fornecedores()

        # Insere os fornecedores recuperados na Treeview.
        # Para cada fornecedor na lista:
        # - Adiciona uma nova linha na Treeview com as informações do fornecedor.
        # - Usa o `_id` do fornecedor como `iid` (identificador da linha).
        for f in forn_list:
            self.lista.insert("",
                              "end",
                              values=(f["nome"], f["cnpj"], f["telefone"], f["email"], f["endereco"]),
                              iid=str(f["_id"]))


# Define a classe `FormFornecedor`, que cria uma janela
#       para cadastrar ou editar um fornecedor.
class FormFornecedor(tk.Toplevel):

    # Define o método especial `__init__`, que é chamado
    #       quando a classe é instanciada.
    # Parâmetros:
    # - `pai`: a janela ou quadro principal que "possui" este formulário.
    # - `func_cb`: uma função de callback que será chamada
    #       quando o fornecedor for salvo.
    # - `dados`: um dicionário com os dados do fornecedor (se for
    #       edição); caso contrário, é `None`.
    def __init__(self, pai, func_cb, dados=None):

        # Chama o construtor da classe base `tk.Toplevel`, inicializando a janela.
        super().__init__(pai)

        # Define o título da janela como "Cadastro/Editar Fornecedor".
        self.title("Cadastro/Editar Fornecedor")

        # Armazena a função de callback que será chamada ao
        #       salvar o fornecedor.
        self.func_cb = func_cb

        # Desativa a capacidade de redimensionar a janela,
        #       mantendo um tamanho fixo.
        self.resizable(False, False)

        # Define que esta janela será modal em relação ao pai, ou seja, o
        #       usuário não poderá interagir com a janela principal
        #       enquanto esta estiver aberta.
        self.transient(pai)

        # Garante que o foco do teclado está nesta janela, bloqueando
        #       interações com a janela principal até que ela seja fechada.
        self.grab_set()

        # Cria um rótulo para exibir o texto "Nome:"
        # `text="Nome:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 0 e coluna 0.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        # `sticky="e"` alinha o rótulo à direita.
        tk.Label(self,
                 text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) para permitir
        #       que o usuário insira o nome.
        # `grid(row=0, column=1, padx=5, pady=5)` posiciona o campo de
        #       entrada na linha 0 e coluna 1.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        self.ent_nome = tk.Entry(self)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para exibir o texto "CNPJ:"
        # `text="CNPJ:"` define o texto exibido no rótulo.
        # `grid(row=1, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 1 e coluna 0.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        # `sticky="e"` alinha o rótulo à direita.
        tk.Label(self,
                 text="CNPJ:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) para permitir
        #       que o usuário insira o CNPJ.
        # `grid(row=1, column=1, padx=5, pady=5)` posiciona o campo de
        #       entrada na linha 1 e coluna 1.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        self.ent_cnpj = tk.Entry(self)
        self.ent_cnpj.grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para exibir o texto "Telefone:"
        # `text="Telefone:"` define o texto exibido no rótulo.
        # `grid(row=2, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 2 e coluna 0.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        # `sticky="e"` alinha o rótulo à direita.
        tk.Label(self,
                 text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) para permitir que o
        #       usuário insira o número de telefone.
        # `grid(row=2, column=1, padx=5, pady=5)` posiciona o campo de
        #       entrada na linha 2 e coluna 1.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        self.ent_tel = tk.Entry(self)
        self.ent_tel.grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para exibir o texto "Email:"
        # `text="Email:"` define o texto exibido no rótulo.
        # `grid(row=3, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 3 e coluna 0.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        # `sticky="e"` alinha o rótulo à direita.
        tk.Label(self, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) para permitir
        #       que o usuário insira o email.
        # `grid(row=3, column=1, padx=5, pady=5)` posiciona o campo de
        #       entrada na linha 3 e coluna 1.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        self.ent_email = tk.Entry(self)
        self.ent_email.grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo para exibir o texto "Endereço:"
        # `text="Endereço:"` define o texto exibido no rótulo.
        # `grid(row=4, column=0, padx=5, pady=5, sticky="e")` posiciona o
        #       rótulo na linha 4 e coluna 0.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        # `sticky="e"` alinha o rótulo à direita.
        tk.Label(self,
                 text="Endereço:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto (Entry) para permitir
        #       que o usuário insira o endereço.
        # `grid(row=4, column=1, padx=5, pady=5)` posiciona o
        #       campo de entrada na linha 4 e coluna 1.
        # `padx=5, pady=5` adiciona 5 pixels de espaçamento horizontal e vertical.
        self.ent_end = tk.Entry(self)
        self.ent_end.grid(row=4, column=1, padx=5, pady=5)

        # Cria um frame para organizar os botões de controle.
        frm_b = tk.Frame(self)

        # Posiciona o frame na linha 5, abrangendo duas colunas e
        # adicionando um espaçamento vertical (pady) de 10 pixels.
        frm_b.grid(row=5, column=0, columnspan=2, pady=10)

        # Cria um botão de "Salvar".
        # `text="Salvar"` define o texto que aparece no botão.
        # `command=self.ao_salvar` associa a ação de salvar ao clicar no botão.
        # `pack(side="left", padx=5)` posiciona o botão à esquerda
        #       com um espaçamento horizontal de 5 pixels.
        tk.Button(frm_b,
                  text="Salvar", command=self.ao_salvar).pack(side="left", padx=5)

        # Cria um botão de "Cancelar".
        # `text="Cancelar"` define o texto que aparece no botão.
        # `command=self.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `pack(side="left", padx=5)` posiciona o botão à esquerda, ao
        #       lado do botão "Salvar", com um espaçamento horizontal de 5 pixels.
        tk.Button(frm_b,
                  text="Cancelar",
                  command=self.destroy).pack(side="left", padx=5)

        # Verifica se foram passados dados de entrada.
        # Caso existam, insere esses dados nos campos apropriados.
        if dados:

            # Insere o nome do fornecedor no campo correspondente.
            self.ent_nome.insert(0, dados["nome"])

            # Insere o CNPJ do fornecedor no campo correspondente.
            self.ent_cnpj.insert(0, dados["cnpj"])

            # Insere o telefone do fornecedor no campo correspondente.
            self.ent_tel.insert(0, dados["telefone"])

            # Insere o e-mail do fornecedor no campo correspondente.
            self.ent_email.insert(0, dados["email"])

            # Insere o endereço do fornecedor no campo correspondente.
            self.ent_end.insert(0, dados["endereco"])

        # Agendamento de um ajuste de layout.
        # Após 0 milissegundos, chama a função `centralizar_janela`
        #       para ajustar a posição da janela na tela.
        self.after(0, lambda: centralizar_janela(self))

    # Função que é chamada ao clicar no botão "Salvar".
    def ao_salvar(self):

        # Captura o texto do campo de nome e remove espaços
        #       em branco nas extremidades.
        n = self.ent_nome.get().strip()

        # Captura o texto do campo de CNPJ e remove espaços em
        #       branco nas extremidades.
        c = self.ent_cnpj.get().strip()

        # Captura o texto do campo de telefone e remove espaços
        #       em branco nas extremidades.
        t = self.ent_tel.get().strip()

        # Captura o texto do campo de e-mail e remove espaços em
        #       branco nas extremidades.
        e = self.ent_email.get().strip()

        # Captura o texto do campo de endereço e remove espaços em
        #       branco nas extremidades.
        end = self.ent_end.get().strip()

        # Verifica se os campos "nome" e "CNPJ" estão preenchidos.
        # Se um ou ambos estiverem vazios, exibe uma mensagem de
        #       erro e interrompe a função.
        if not n or not c:
            messagebox.showerror("Erro",
                                 "Nome e CNPJ são obrigatórios!")
            return

        # Caso os campos obrigatórios estejam preenchidos, chama a função de callback,
        #       passando os valores capturados como argumentos.
        self.func_cb(n, c, t, e, end)

        # Fecha a janela após salvar.
        self.destroy()


###############################################################################
# JANELA DE VENDAS POR FORNECEDOR (FILTRA DATAS dd/mm/aaaa, ETC.)
###############################################################################

# Classe que cria uma janela para exibir as vendas de um fornecedor específico.
class JanelaVendasFornecedor(tk.Toplevel):

    # Método inicializador da janela, chamado ao criar uma instância da classe.
    # Recebe o objeto pai, a conexão com o banco de dados, o ID do
    #       fornecedor e o nome do fornecedor.
    def __init__(self, pai, db: GerenciadorBanco, id_forn, nome_forn):

        # Chama o construtor da classe base tk.Toplevel,
        #       passando o objeto pai como argumento.
        super().__init__(pai)

        # Define o título da janela com o nome do fornecedor.
        self.title(f"Vendas do Fornecedor: {nome_forn}")

        # Armazena a referência ao banco de dados.
        self.db = db

        # Armazena o ID do fornecedor para consultas posteriores.
        self.id_forn = id_forn

        # Define as dimensões iniciais da janela.
        self.geometry("1150x400")

        # Configura a janela para ser modal (bloqueia interações com a
        #       janela pai enquanto está aberta).
        self.transient(pai)

        # Coloca o foco na nova janela, impedindo interações com
        #       outras janelas até que esta seja fechada.
        self.grab_set()

        # Centraliza a janela na tela.
        centralizar_janela(self)

        # Cria um frame para organizar os campos de filtro.
        # Este frame ajuda a alinhar os widgets de entrada e
        #       botões em uma única linha.
        frm_filtros = tk.Frame(self)

        # Posiciona o frame na janela, ocupando toda a largura disponível.
        # O padding horizontal (padx=5) e vertical (pady=5) criam um
        #       espaçamento visual ao redor do frame.
        frm_filtros.pack(fill="x", padx=5, pady=5)

        # Cria um rótulo para o campo de entrada da data inicial.
        # `text="Data Inicial (dd/mm/aaaa):"` define o texto exibido no rótulo.
        # `row=0, column=0` posiciona o rótulo na primeira linha, primeira coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        tk.Label(frm_filtros,
                 text="Data Inicial (dd/mm/aaaa):").grid(row=0, column=0, padx=5)

        # Cria um campo de entrada para a data inicial.
        # `width=10` define a largura do campo de entrada para 10 caracteres.
        # `row=0, column=1` posiciona o campo na primeira linha, segunda coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        self.ent_data_ini = tk.Entry(frm_filtros, width=10)
        self.ent_data_ini.grid(row=0, column=1, padx=5)

        # Cria um rótulo para o campo de entrada da data final.
        # `text="Data Final:"` define o texto exibido no rótulo.
        # `row=0, column=2` posiciona o rótulo na primeira
        #       linha, terceira coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        tk.Label(frm_filtros,
                 text="Data Final:").grid(row=0, column=2, padx=5)

        # Cria um campo de entrada para a data final.
        # `width=10` define a largura do campo de entrada para 10 caracteres.
        # `row=0, column=3` posiciona o campo na primeira linha, quarta coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        self.ent_data_fim = tk.Entry(frm_filtros, width=10)
        self.ent_data_fim.grid(row=0, column=3, padx=5)

        # Cria um rótulo para o campo de entrada do cliente.
        # `text="Cliente:"` define o texto exibido no rótulo.
        # `row=0, column=4` posiciona o rótulo na primeira linha, quinta coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        tk.Label(frm_filtros, text="Cliente:").grid(row=0, column=4, padx=5)

        # Cria um campo de entrada para o cliente.
        # `width=15` define a largura do campo de entrada para 15 caracteres.
        # `row=0, column=5` posiciona o campo na primeira linha, sexta coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        self.ent_cliente = tk.Entry(frm_filtros, width=15)
        self.ent_cliente.grid(row=0, column=5, padx=5)

        # Cria um rótulo para o campo de entrada do produto.
        # `text="Produto:"` define o texto exibido no rótulo.
        # `row=0, column=6` posiciona o rótulo na primeira
        #       linha, sétima coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal
        #       de 5 pixels ao redor do rótulo.
        tk.Label(frm_filtros,
                 text="Produto:").grid(row=0, column=6, padx=5)

        # Cria um campo de entrada para o produto.
        # `width=15` define a largura do campo de entrada para 15 caracteres.
        # `row=0, column=7` posiciona o campo na primeira linha, oitava coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        self.ent_produto = tk.Entry(frm_filtros, width=15)
        self.ent_produto.grid(row=0, column=7, padx=5)

        # Cria um rótulo para o campo de entrada do total do item.
        # `text="TotalItem:"` define o texto exibido no rótulo.
        # `row=0, column=8` posiciona o rótulo na primeira linha, nona coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do rótulo.
        tk.Label(frm_filtros, text="TotalItem:").grid(row=0, column=8, padx=5)

        # Cria um campo de entrada para o total do item.
        # `width=10` define a largura do campo de entrada para 10 caracteres.
        # `row=0, column=9` posiciona o campo na primeira linha, décima coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        self.ent_total = tk.Entry(frm_filtros, width=10)
        self.ent_total.grid(row=0, column=9, padx=5)

        # Cria um botão para aplicar o filtro.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a ação de filtrar os dados quando o botão é clicado.
        # `row=0, column=10` posiciona o botão na primeira linha, décima primeira coluna do grid.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do botão.
        tk.Button(frm_filtros,
                  text="Filtrar",
                  command=self.filtrar).grid(row=0, column=10, padx=5)

        # Define as colunas que serão exibidas na Treeview.
        # Cada item em `colunas` será usado como cabeçalho de uma coluna na Treeview.
        colunas = ("Data", "Cliente", "Produto", "TotalItem")

        # Cria uma Treeview para exibir os dados.
        # `columns=colunas` define as colunas que serão exibidas.
        # `show="headings"` remove a coluna de ícone padrão, deixando
        #       apenas os cabeçalhos das colunas definidas.
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")

        # Define o título de cada coluna e ajusta a largura.
        # `heading(c, text=c)` define o cabeçalho da coluna com o texto correspondente.
        # `column(c, width=120)` ajusta a largura de cada coluna para 120 pixels.
        for c in colunas:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)

        # Exibe a Treeview na interface.
        # `fill="both"` permite que a Treeview preencha horizontal e
        #       verticalmente o espaço disponível.
        # `expand=True` faz com que a Treeview expanda
        #       proporcionalmente ao redimensionar a janela.
        self.tree.pack(fill="both", expand=True)

        # Carrega os dados de vendas do fornecedor a partir do banco de dados.
        # `self.dados = self._carregar_dados()` chama o método que
        #       obtém as vendas associadas ao fornecedor atual.
        self.dados = self._carregar_dados()

        # Exibe os dados carregados na Treeview.
        # `_exibir(self.dados)` insere as informações de cada
        #       venda na interface, permitindo visualizá-las.
        self._exibir(self.dados)


    def _carregar_dados(self):

        # Inicializa uma lista vazia que armazenará os
        #       dados formatados de vendas.
        lista = []

        # Recupera todas as vendas armazenadas no banco de dados.
        # `todas_vendas` conterá um cursor para iterar sobre as vendas.
        todas_vendas = self.db.col_vendas.find()

        # Itera sobre cada venda para formatar os dados necessários.
        for vd in todas_vendas:

            # Converte a data da venda de ISO para um objeto de data Python.
            # Isso facilita a manipulação e a formatação da data posteriormente.
            data_obj = converter_iso_para_date(vd["data_hora"])

            # Converte o objeto de data para uma string no formato brasileiro.
            # Isso é útil para exibir as datas de maneira legível ao usuário.
            data_br = converter_date_para_str_br(data_obj)

            # Inicializa o nome do cliente como vazio.
            # Se o cliente estiver associado à venda, o nome será preenchido.
            nome_cliente = ""

            # Verifica se a venda tem um campo `cliente_id`.
            if vd.get("cliente_id"):

                # Busca os dados do cliente no banco de dados usando o `cliente_id`.
                # `doc_c` conterá as informações do cliente, caso ele exista.
                doc_c = self.db.col_clientes.find_one({"_id": vd["cliente_id"]})
                if doc_c:

                    # Se o cliente for encontrado, armazena seu nome.
                    nome_cliente = doc_c["nome"]

            # Armazena os itens da venda para posterior manipulação.
            itens = vd["itens"]

            # Itera sobre os itens da venda.
            # Cada item representa um produto comprado nesta venda.
            for it in itens:

                # Busca no banco de dados as informações do produto relacionado ao item.
                # `doc_p` conterá o documento do produto, caso ele exista.
                doc_p = self.db.col_produtos.find_one({"_id": it["produto_id"]})

                # Verifica se o produto existe e se pertence ao fornecedor especificado.
                # Isso é feito comparando o campo `fornecedor_id` do produto com o `id_forn` passado.
                if doc_p and str(doc_p["fornecedor_id"]) == self.id_forn:

                    # Calcula o subtotal para este item da venda.
                    # O subtotal é obtido multiplicando a quantidade
                    #       comprada pelo preço unitário.
                    subt = it["quantidade"] * it["preco_unitario"]

                    # Adiciona os dados formatados do item à lista.
                    # Cada entrada inclui a data da venda, o nome do cliente, o nome do produto,
                    #       e os valores do subtotal formatados como string e como número.
                    lista.append({
                        "data_obj": data_obj,  # Objeto de data para ordenações e filtros posteriores.
                        "data_br": data_br,  # Data formatada para exibição.
                        "cliente": nome_cliente,  # Nome do cliente associado à venda.
                        "produto": doc_p["nome"],  # Nome do produto relacionado ao item.
                        "total_str": f"{subt:.2f}",  # Subtotal formatado como string para exibição.
                        "total_val": subt  # Subtotal como número para cálculos futuros.
                    })

        # Retorna a lista final contendo todos os itens formatados para exibição.
        return lista


    # Método responsável por exibir os dados no Treeview.
    # `dados` é uma lista de dicionários contendo os dados
    #       formatados para exibição.
    def _exibir(self, dados):

        # Primeiro, limpa o Treeview removendo todas as linhas existentes.
        # Isso é feito para garantir que apenas os novos dados sejam exibidos.
        for i in self.tree.get_children():

            # Cada "child" no Treeview é deletado para que a tabela fique vazia.
            self.tree.delete(i)

        # Em seguida, itera sobre os dados formatados.
        # Cada entrada em `dados` é um dicionário que
        #       representa uma linha a ser exibida.
        for d in dados:

            # Insere uma nova linha no Treeview.
            # Os valores exibidos são:
            # - A data da venda (`data_br`), já formatada para o padrão brasileiro.
            # - O nome do cliente.
            # - O nome do produto comprado.
            # - O subtotal, formatado como uma string com duas casas decimais.
            self.tree.insert(
                "",  # Inserção na raiz do Treeview (sem pai).
                "end",  # Adiciona a nova linha no final da tabela.
                values=(d["data_br"], d["cliente"], d["produto"], d["total_str"])  # Valores das colunas.
            )


    # Método para aplicar filtros aos dados exibidos no Treeview.
    # Esse método é chamado quando o botão "Filtrar" é pressionado.
    # Ele coleta os valores dos campos de entrada (datas, cliente, produto, total)
    #       e utiliza esses valores para selecionar apenas os registros
    #       que atendem aos critérios fornecidos.
    def filtrar(self):

        # Coleta e converte a data inicial e final inseridas pelo usuário.
        # A função `analisar_data_br` transforma as strings
        #       fornecidas em objetos de data, se possível.
        di = analisar_data_br(self.ent_data_ini.get())  # Data inicial
        df = analisar_data_br(self.ent_data_fim.get())  # Data final

        # Coleta os filtros de texto fornecidos pelo usuário e os
        #       normaliza para letras minúsculas e sem espaços nas extremidades.
        cli_f = self.ent_cliente.get().lower().strip()  # Nome do cliente
        prod_f = self.ent_produto.get().lower().strip()  # Nome do produto
        tot_f = self.ent_total.get().lower().strip()  # Valor total

        # Cria uma lista para armazenar os dados que atendem aos filtros fornecidos.
        filtrados = []

        # Itera pelos dados originais para verificar quais registros
        #       atendem aos critérios de filtro.
        # Para cada registro, verifica-se a data, o nome do cliente, o
        #       produto e o total antes de decidir se o inclui na lista filtrada.
        for d in self.dados:

            # Verifica se a data do registro é anterior à data inicial fornecida.
            # Se for, pula este registro.
            if di and d["data_obj"] and d["data_obj"] < di:
                continue

            # Verifica se a data do registro é posterior à data final fornecida.
            # Se for, pula este registro.
            if df and d["data_obj"] and d["data_obj"] > df:
                continue

            # Verifica se o nome do cliente do registro contém a
            #       string fornecida no filtro.
            # Se não contém, pula este registro.
            if cli_f and cli_f not in d["cliente"].lower():
                continue

            # Verifica se o nome do produto do registro contém a
            #       string fornecida no filtro.
            # Se não contém, pula este registro.
            if prod_f and prod_f not in d["produto"].lower():
                continue

            # Verifica se o valor total do registro contém a string fornecida no filtro.
            # Se não contém, pula este registro.
            if tot_f and tot_f not in d["total_str"].lower():
                continue

            # Se o registro passou por todos os filtros, ele é
            #       adicionado à lista de registros filtrados.
            filtrados.append(d)

        # Atualiza a exibição na interface gráfica para mostrar
        #       apenas os registros filtrados.
        self._exibir(filtrados)



###############################################################################
# QUADRO DE PRODUTOS (VER QUEM COMPROU) COM DATAS dd/mm/aaaa
###############################################################################

# Define a classe QuadroProdutos que representa uma seção ou
#       janela de produtos na interface gráfica.
class QuadroProdutos(tk.Frame):

    # Inicializa a classe QuadroProdutos.
    # `pai` é o componente pai em que este quadro será colocado.
    # `db` é o objeto responsável por acessar o banco de dados.
    def __init__(self, pai, db: GerenciadorBanco):

        # Chama o método de inicialização da classe pai (tk.Frame).
        # Isso configura o quadro base dentro da hierarquia da interface gráfica.
        super().__init__(pai)

        # Armazena a referência ao banco de dados para
        #       uso em outros métodos da classe.
        self.db = db

        # Cria um frame na parte superior da interface.
        # `self` refere-se à janela ou frame principal.
        # `frm_top` será o contêiner para os elementos
        #       relacionados à busca de produtos.
        frm_top = tk.Frame(self)

        # Posiciona o frame na parte superior da janela.
        # `fill="x"` faz com que o frame preencha horizontalmente o espaço disponível.
        frm_top.pack(fill="x")

        # Adiciona uma etiqueta (label) ao frame superior.
        # `text="Buscar Produto:"` define o texto exibido na etiqueta.
        # `side="left"` posiciona a etiqueta no lado esquerdo do frame.
        # `padx=5` adiciona 5 pixels de espaço horizontal ao redor da etiqueta.
        tk.Label(frm_top, text="Buscar Produto:").pack(side="left", padx=5)

        # Cria um campo de entrada de texto para digitar o termo de busca.
        # `self.ent_busca` é o nome da variável que armazenará o widget de entrada de texto.
        # `tk.Entry(frm_top)` cria o campo de entrada associado ao frame `frm_top`.
        # Este campo permitirá que o usuário insira palavras ou
        #       frases que serão usadas como filtro.
        self.ent_busca = tk.Entry(frm_top)

        # Posiciona o campo de entrada no lado esquerdo do frame `frm_top`.
        # `pack(side="left")` alinha o campo no lado esquerdo do frame.
        # `padx=5` adiciona 5 pixels de espaço horizontal ao redor do campo.
        # O espaçamento melhora a apresentação visual e evita
        #       que os widgets fiquem muito próximos.
        self.ent_busca.pack(side="left", padx=5)

        # Cria um botão de busca ao lado do campo de entrada.
        # `text="Buscar"` define o texto que será exibido no botão.
        # `command=self.atualizar_lista` vincula o botão à função `self.atualizar_lista`.
        # Ao clicar no botão, a função será chamada para atualizar a
        #       lista de produtos com base no termo digitado.
        # `padx=5` adiciona 5 pixels de espaço horizontal ao redor do botão.
        tk.Button(frm_top,
                  text="Buscar",
                  command=self.atualizar_lista).pack(side="left", padx=5)

        # Cria uma barra de rolagem vertical para a lista de produtos.
        # `scroll_y` é a variável que armazena o widget de barra de rolagem.
        # `orient="vertical"` define que a barra será vertical.
        # A barra permitirá rolar pelos itens da lista caso o número
        #       de itens exceda o espaço visível.
        scroll_y = tk.Scrollbar(self, orient="vertical")

        # Cria uma `Treeview` para exibir os produtos em forma de tabela.
        # `self.lista_prod` é a variável que armazenará o widget da tabela.
        # `columns=("Código", "Nome", "Categoria", "PreçoVenda", "Estoque")`
        #       define as colunas da tabela.
        # `show="headings"` oculta a coluna raiz padrão e mostra
        #       apenas os títulos das colunas especificadas.
        # `yscrollcommand=scroll_y.set` associa a barra de rolagem `scroll_y` à `Treeview`.
        # Isso permite que a barra de rolagem funcione em conjunto com a tabela.
        self.lista_prod = ttk.Treeview(self,
                                        columns=("Código", "Nome", "Categoria", "PreçoVenda", "Estoque"),
                                        show="headings",
                                        yscrollcommand=scroll_y.set)

        # Configura a barra de rolagem vertical para que ela
        #       controle a visualização da `Treeview`.
        # `command=self.lista_prod.yview` faz com que a barra de
        #       rolagem ajuste a posição dos itens visíveis na `Treeview`.
        scroll_y.config(command=self.lista_prod.yview)

        # Posiciona a barra de rolagem no lado direito da interface e a
        #       ajusta para preencher verticalmente.
        # `side="right"` coloca a barra no lado direito.
        # `fill="y"` faz com que a barra ocupe todo o espaço vertical disponível.
        scroll_y.pack(side="right", fill="y")

        # Define os títulos e larguras das colunas na `Treeview`.
        # Cada coluna é identificada por um nome (por exemplo, "Código") e
        #       terá seu cabeçalho visível no topo.
        for c in ("Código", "Nome", "Categoria", "PreçoVenda", "Estoque"):

            # `heading` define o texto visível no cabeçalho da coluna.
            # `column` ajusta a largura inicial da coluna para 120 pixels.
            self.lista_prod.heading(c, text=c)
            self.lista_prod.column(c, width=120)

        # Exibe a `Treeview` na interface, expandindo-a para
        #       preencher o espaço disponível.
        # `fill="both"` faz com que ela se ajuste horizontal e verticalmente.
        # `expand=True` garante que a `Treeview` use o espaço total do contêiner.
        self.lista_prod.pack(fill="both", expand=True)

        # Cria um frame (`frm_b`) para organizar os botões na interface.
        # `fill="x"` faz com que o frame se estenda horizontalmente
        #       até as bordas do contêiner.
        frm_b = tk.Frame(self)
        frm_b.pack(fill="x")

        # Adiciona um botão "Cadastrar" dentro do `frm_b`.
        # `text="Cadastrar"` define o rótulo do botão.
        # `command=self.cadastrar` vincula a função `cadastrar` ao clique no botão.
        # `side="left"` posiciona o botão à esquerda dentro do frame.
        # `padx=5, pady=5` adiciona espaçamento ao redor do botão.
        tk.Button(frm_b,
                  text="Cadastrar",
                  command=self.cadastrar).pack(side="left", padx=5, pady=5)

        # Adiciona um botão "Editar" ao frame `frm_b`.
        # `text="Editar"` define o rótulo exibido no botão.
        # `command=self.editar` vincula a ação de clicar no botão à execução do método `editar`.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` e `pady=5` adicionam espaço horizontal e vertical ao redor do botão.
        tk.Button(frm_b,
                  text="Editar",
                  command=self.editar).pack(side="left", padx=5, pady=5)

        # Adiciona um botão "Excluir" ao frame `frm_b`.
        # `text="Excluir"` define o rótulo exibido no botão.
        # `command=self.excluir` vincula a ação de clicar no botão à execução do método `excluir`.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` e `pady=5` adicionam espaço horizontal e vertical ao redor do botão.
        tk.Button(frm_b,
                  text="Excluir",
                  command=self.excluir).pack(side="left", padx=5, pady=5)

        # Adiciona um botão "Atualizar" ao frame `frm_b`.
        # `text="Atualizar"` define o rótulo exibido no botão.
        # `command=self.atualizar_lista` vincula a ação de clicar no
        #       botão à execução do método `atualizar_lista`.
        # `side="left"` posiciona o botão ao lado esquerdo dentro do frame.
        # `padx=5` e `pady=5` adicionam espaço horizontal e vertical ao redor do botão.
        tk.Button(frm_b,
                  text="Atualizar",
                  command=self.atualizar_lista).pack(side="left", padx=5, pady=5)

        # Associa o evento de duplo clique em um item da lista ao método `ver_clientes`.
        # `<Double-1>` representa o evento de dois cliques
        #       consecutivos do botão esquerdo do mouse.
        # `self.ver_clientes` é o método que será executado
        #       quando o evento ocorrer.
        self.lista_prod.bind("<Double-1>", self.ver_clientes)

        # Chama o método `atualizar_lista` para preencher a lista de
        #       produtos com os dados atuais.
        # `atualizar_lista` recupera os dados da fonte e os exibe
        #       na Treeview `self.lista_prod`.
        self.atualizar_lista()


    # Define o método `atualizar_lista` da classe.
    def atualizar_lista(self):

        # Remove todos os itens existentes da Treeview.
        for i in self.lista_prod.get_children():
            self.lista_prod.delete(i)

        # Obtém o texto de busca do campo de entrada, removendo
        #       espaços em branco das extremidades.
        # Se não houver texto, busca todos os produtos.
        txt = self.ent_busca.get().strip()

        # Chama o método `listar_produtos` do gerenciador de banco de dados,
        #       passando o texto de busca, se houver. Retorna uma
        #       lista de produtos correspondentes.
        docs = self.db.listar_produtos(txt if txt else None)

        # Insere os produtos retornados na Treeview.
        for p in docs:
            self.lista_prod.insert(
                "",
                "end",
                values=(
                    p["codigo"],  # Código do produto.
                    p["nome"],  # Nome do produto.
                    p["categoria"],  # Categoria do produto.
                    p["preco_venda"],  # Preço de venda do produto.
                    p["quantidade_estoque"]  # Quantidade em estoque.
                ),
                iid=str(p["_id"])  # Identificador único baseado no ID do banco de dados.
            )


    # Define o método `cadastrar` da classe.
    def cadastrar(self):

        # Define uma função de callback (`cb`) que será chamada ao salvar o novo produto.
        # Essa função recebe os dados do produto (cd, nm, ds, cat, pc, pv, qt, idf)
        def cb(cd, nm, ds, cat, pc, pv, qt, idf):

            # e os usa para chamar o método `cadastrar_produto` no
            #       gerenciador de banco de dados.
            self.db.cadastrar_produto(cd, nm, ds, cat, pc, pv, qt, idf)

            # Após cadastrar o produto, chama o método `atualizar_lista`
            #       para recarregar a lista de produtos.
            self.atualizar_lista()

        # Cria uma nova instância da janela `FormProduto`,
        #       passando `self` como pai,
        # o callback `cb` definido acima e a instância do
        #       gerenciador de banco de dados `self.db`.
        FormProduto(self, cb, self.db)


    # Define o método `editar` da classe.
    def editar(self):

        # Obtém os itens selecionados na `Treeview` de produtos.
        sel = self.lista_prod.selection()

        # Se não houver itens selecionados, exibe uma mensagem de aviso e retorna.
        if not sel:
            messagebox.showwarning("Aviso",
                                   "Selecione um produto para editar.")
            return

        # Obtém o ID do primeiro item selecionado.
        id_p = sel[0]

        # Busca o documento do produto no banco de dados com base no ID.
        doc_p = self.db.col_produtos.find_one({"_id": ObjectId(id_p)})

        # Define uma função de callback (`cb`) que será chamada ao
        #       salvar as alterações no produto.
        # Essa função recebe os dados editados do produto (cd, nm, ds, cat, pc, pv, qt, idf)
        #       e os usa para chamar o método `atualizar_produto` no gerenciador de banco de dados.
        # Após atualizar o produto, chama o método `atualizar_lista`
        #       para recarregar a lista de produtos.
        def cb(cd, nm, ds, cat, pc, pv, qt, idf):
            self.db.atualizar_produto(id_p, cd, nm, ds, cat, pc, pv, qt, idf)
            self.atualizar_lista()

        # Cria uma nova instância da janela `FormProduto`, passando `self` como pai,
        # o callback `cb` definido acima, a instância do gerenciador de banco de dados `self.db`,
        #       e o documento do produto atual (`doc_p`) para preenchimento dos campos.
        FormProduto(self, cb, self.db, doc_p)


    # Define o método `excluir` da classe.
    def excluir(self):

        # Obtém os itens selecionados na `Treeview` de produtos.
        sel = self.lista_prod.selection()

        # Se não houver itens selecionados, exibe uma mensagem
        #       de aviso e retorna.
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return

        # Obtém o ID do primeiro item selecionado.
        id_p = sel[0]

        # Exibe uma mensagem de confirmação para o usuário antes de excluir o produto.
        # Se o usuário clicar em "Sim" (`askyesno` retorna True), o produto será excluído.
        if messagebox.askyesno("Confirmação",
                               "Deseja realmente excluir este produto?"):

            # Chama o método `excluir_produto` no gerenciador de
            #       banco de dados, passando o ID do produto.
            self.db.excluir_produto(id_p)

            # Após excluir o produto, chama o método `atualizar_lista`
            #       para recarregar a lista de produtos.
            self.atualizar_lista()


    # Define o método `ver_clientes` da classe, chamado ao
    #       clicar duas vezes em um produto na `Treeview`.
    def ver_clientes(self, event):

        # Obtém os itens selecionados na `Treeview` de produtos.
        sel = self.lista_prod.selection()

        # Se não houver itens selecionados, apenas retorna sem fazer nada.
        if not sel:
            return

        # Obtém o ID do primeiro item selecionado.
        id_p = sel[0]

        # Busca no banco de dados o produto correspondente ao ID selecionado.
        doc_p = self.db.col_produtos.find_one({"_id": ObjectId(id_p)})

        # Se o produto for encontrado (`doc_p` não é `None`):
        if doc_p:

            # Cria uma nova janela `JanelaClientesProduto` para exibir
            #       informações sobre os clientes
            #       associados ao produto, passando a janela pai, o gerenciador
            #       de banco de dados, o ID do produto,
            #       e o nome do produto como argumentos.
            JanelaClientesProduto(self, self.db, str(doc_p["_id"]), doc_p["nome"])


###############################################################################
# JANELA PARA VER CLIENTES QUE COMPRARAM UM PRODUTO (DATAS dd/mm/aaaa)
###############################################################################

# Define uma classe chamada `JanelaClientesProduto` que herda de `tk.Toplevel`.
# Essa classe cria uma janela específica para exibir os
#       clientes que compraram um determinado produto.
class JanelaClientesProduto(tk.Toplevel):

    # Inicializa a janela com o pai (janela ou quadro principal), o banco de dados,
    # o identificador do produto e o nome do produto como parâmetros.
    def __init__(self, pai, db: GerenciadorBanco, id_produto, nome_produto):

        # Chama o inicializador da classe pai (`tk.Toplevel`) para
        #       configurar a janela como um toplevel do tkinter.
        super().__init__(pai)

        # Define o título da janela, indicando que mostrará os
        #       clientes que compraram o produto especificado.
        # O título é configurado dinamicamente para incluir o nome do produto.
        self.title(f"Clientes que compraram: {nome_produto}")

        # Salva a instância do banco de dados fornecida para
        #       ser usada dentro da classe.
        self.db = db

        # Salva o identificador do produto (id_produto) fornecido
        #       como uma propriedade da instância.
        # Este identificador será usado para buscar os dados de
        #       clientes relacionados ao produto.
        self.id_prod = id_produto

        # Define as dimensões da janela. Aqui, a largura será
        #       800 pixels e a altura 400 pixels.
        # Essa configuração cria uma janela de tamanho fixo.
        self.geometry("1150x400")

        # Torna a janela modal, ou seja, impede que outras janelas da
        #       aplicação sejam acessadas enquanto esta estiver aberta.
        # `transient(pai)` associa a janela ao pai, para que sempre apareça acima dele.
        self.transient(pai)

        # `grab_set()` faz com que a janela capture todos os eventos de
        #       entrada, obrigando o usuário a interagir com ela antes de voltar ao pai.
        self.grab_set()

        # Centraliza a janela na tela. Essa função é chamada para
        #       calcular a posição da janela
        #       de forma que ela apareça no centro da tela ou do pai.
        centralizar_janela(self)

        # Cria um frame (quadro) para acomodar os filtros de pesquisa.
        # `frm_filtros` será usado como um contêiner para os
        #       widgets relacionados a filtros.
        frm_filtros = tk.Frame(self)

        # Posiciona o quadro na parte superior da janela.
        # `fill="x"` faz o quadro se expandir horizontalmente.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento ao redor do quadro.
        frm_filtros.pack(fill="x", padx=5, pady=5)

        # Adiciona um rótulo para a entrada de data inicial.
        # `text="Data Inicial (dd/mm/aaaa):"` define o texto do rótulo.
        # `grid(row=0, column=0)` posiciona o rótulo na primeira
        #       linha e na primeira coluna do quadro.
        # `padx=5` adiciona um espaçamento de 5 pixels à esquerda e à direita do rótulo.
        tk.Label(frm_filtros, text="Data Inicial (dd/mm/aaaa):").grid(row=0, column=0, padx=5)

        # Adiciona uma caixa de entrada para o usuário digitar a data inicial.
        # `width=10` define a largura da caixa de entrada.
        # `grid(row=0, column=1)` posiciona a entrada na primeira linha e
        #       na segunda coluna do quadro.
        # `padx=5` adiciona um espaçamento de 5 pixels à esquerda e à direita da entrada.
        self.ent_data_ini = tk.Entry(frm_filtros, width=10)
        self.ent_data_ini.grid(row=0, column=1, padx=5)

        # Cria um Label para exibir o texto "Data Final".
        # `text="Data Final:"` define o texto exibido no Label.
        # `frm_filtros` define o container onde o Label será inserido.
        # `.grid(row=0, column=2, padx=5)` posiciona o Label na linha 0, coluna 2,
        #       com um espaçamento horizontal de 5 pixels.
        tk.Label(frm_filtros, text="Data Final:").grid(row=0, column=2, padx=5)

        # Cria um campo de entrada de texto para a data final.
        # `width=10` define a largura do campo como 10 caracteres.
        # `frm_filtros` define o container onde o Entry será inserido.
        self.ent_data_fim = tk.Entry(frm_filtros, width=10)

        # Posiciona o campo de entrada de texto na interface.
        # `.grid(row=0, column=3, padx=5)` posiciona o Entry na linha 0, coluna 3,
        #       com um espaçamento horizontal de 5 pixels para melhorar a organização visual.
        self.ent_data_fim.grid(row=0, column=3, padx=5)

        # Cria um Label para exibir o texto "Cliente:".
        # `text="Cliente:"` define o texto exibido no Label.
        # `frm_filtros` define o container onde o Label será inserido.
        # `.grid(row=0, column=4, padx=5)` posiciona o Label na linha 0, coluna 4,
        #       com um espaçamento horizontal de 5 pixels para organização visual.
        tk.Label(frm_filtros, text="Cliente:").grid(row=0, column=4, padx=5)

        # Cria um campo de entrada de texto para que o usuário
        #       possa inserir o nome do cliente.
        # `width=15` define a largura do campo como 15 caracteres.
        # `frm_filtros` define o container onde o Entry será inserido.
        self.ent_cliente = tk.Entry(frm_filtros, width=15)

        # Posiciona o campo de entrada de texto na interface.
        # `.grid(row=0, column=5, padx=5)` posiciona o Entry na linha 0, coluna 5,
        #       com um espaçamento horizontal de 5 pixels para melhorar a organização visual.
        self.ent_cliente.grid(row=0, column=5, padx=5)

        # Cria um Label para exibir o texto "Forma:".
        # `text="Forma:"` define o texto exibido no Label.
        # `frm_filtros` define o container onde o Label será inserido.
        # `.grid(row=0, column=6, padx=5)` posiciona o Label na linha 0, coluna 6,
        #       com um espaçamento horizontal de 5 pixels para manter um layout organizado.
        tk.Label(frm_filtros, text="Forma:").grid(row=0, column=6, padx=5)

        # Cria um campo de entrada de texto para que o usuário possa
        #       inserir a forma de pagamento.
        # `width=10` define a largura do campo como 10 caracteres.
        # `frm_filtros` define o container onde o Entry será inserido.
        self.ent_forma = tk.Entry(frm_filtros, width=10)

        # Posiciona o campo de entrada de texto na interface.
        # `.grid(row=0, column=7, padx=5)` posiciona o Entry na linha 0, coluna 7,
        #       com um espaçamento horizontal de 5 pixels para melhorar a organização visual.
        self.ent_forma.grid(row=0, column=7, padx=5)

        # Cria um Label para exibir o texto "Subtotal:".
        # `text="Subtotal:"` define o texto exibido no Label.
        # `frm_filtros` define o container onde o Label será inserido.
        # `.grid(row=0, column=8, padx=5)` posiciona o Label na linha 0, coluna 8,
        #       com um espaçamento horizontal de 5 pixels para manter um layout organizado.
        tk.Label(frm_filtros, text="Subtotal:").grid(row=0, column=8, padx=5)

        # Cria um campo de entrada de texto para que o usuário
        #       possa inserir o valor do subtotal.
        # `width=10` define a largura do campo como 10 caracteres.
        # `frm_filtros` define o container onde o Entry será inserido.
        self.ent_subt = tk.Entry(frm_filtros, width=10)

        # Posiciona o campo de entrada de texto na interface.
        # `.grid(row=0, column=9, padx=5)` posiciona o Entry na linha 0, coluna 9,
        #       com um espaçamento horizontal de 5 pixels para melhorar a organização visual.
        self.ent_subt.grid(row=0, column=9, padx=5)

        # Cria um botão para aplicar o filtro.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a ação de chamar o
        #       método `filtrar` ao clicar no botão.
        # `.grid(row=0, column=10, padx=5)` posiciona o botão na linha 0, coluna 10,
        #       com um espaçamento horizontal de 5 pixels para manter o
        #       alinhamento organizado.
        tk.Button(frm_filtros,
                  text="Filtrar",
                  command=self.filtrar).grid(row=0, column=10, padx=5)

        # Define as colunas que serão exibidas na Treeview.
        # `colunas = ("Data", "Cliente", "Forma", "Subtotal")` cria
        #       uma tupla com os nomes das colunas.
        colunas = ("Data", "Cliente", "Forma", "Subtotal")

        # Cria um widget Treeview para exibir os dados em formato de tabela.
        # `self` define que o Treeview pertence à classe.
        # `columns=colunas` define quais colunas estarão presentes na tabela.
        # `show="headings"` oculta a primeira coluna oculta padrão e
        #       exibe apenas os cabeçalhos das colunas definidas.
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")

        # Percorre a tupla `colunas` e configura cada uma das colunas na Treeview.
        # `for c in colunas:` inicia um loop que percorre cada
        #       nome de coluna definido anteriormente.
        for c in colunas:

            # Define o cabeçalho da coluna na Treeview.
            # `self.tree.heading(c, text=c)` define o nome visível do cabeçalho da coluna.
            self.tree.heading(c, text=c)

            # Define a largura de cada coluna.
            # `self.tree.column(c, width=120)` define a largura da coluna em 120 pixels.
            self.tree.column(c, width=120)

        # Exibe a Treeview na interface.
        # `self.tree.pack(fill="both", expand=True)` garante que a
        #       tabela se ajuste ao tamanho do container.
        # `fill="both"` permite que a tabela se expanda tanto
        #       horizontal quanto verticalmente.
        # `expand=True` faz com que a tabela ocupe todo o
        #       espaço disponível no layout.
        self.tree.pack(fill="both", expand=True)

        # Carrega os dados iniciais chamando o método `_carregar_dados`.
        # `self.dados` armazena os dados retornados pelo método.
        # Este método busca os registros do
        #       banco de dados ou de um arquivo.
        self.dados = self._carregar_dados()

        # Exibe os dados carregados na Treeview.
        # `self._exibir(self.dados)` chama o método `_exibir`,
        #       que é responsável por inserir
        #       os dados na tabela para que fiquem visíveis ao usuário.
        self._exibir(self.dados)


    # Método privado para carregar os dados das vendas do banco de dados.
    # Retorna uma lista de vendas formatadas para exibição na Treeview.
    def _carregar_dados(self):

        # Inicializa uma lista vazia para armazenar os registros formatados.
        lista = []

        # Obtém todas as vendas da coleção `col_vendas` no banco de dados.
        # `self.db.col_vendas.find()` retorna um cursor
        #       contendo todos os documentos da coleção.
        todas_vendas = self.db.col_vendas.find()

        # Itera sobre todas as vendas recuperadas do banco de dados.
        for vd in todas_vendas:

            # Converte a data e hora do formato ISO (usado no
            #       banco de dados) para um objeto `datetime`.
            # `vd["data_hora"]` contém a data da venda armazenada em formato ISO 8601.
            data_obj = converter_iso_para_date(vd["data_hora"])

            # Converte o objeto `datetime` para uma string
            #       formatada no padrão brasileiro (DD/MM/AAAA).
            # Esse formato facilita a leitura e compreensão da data pelos usuários.
            data_br = converter_date_para_str_br(data_obj)

            # Obtém a forma de pagamento utilizada na venda.
            forma = vd["forma_pagamento"]

            # Inicializa a variável do nome do cliente como uma string vazia.
            # Caso o cliente esteja cadastrado, essa variável será
            #       preenchida com o nome do cliente.
            nome_cli = ""

            # Verifica se a venda possui um cliente associado (`cliente_id` não é nulo).
            if vd.get("cliente_id"):

                # Busca o documento do cliente na coleção `col_clientes`
                #       com base no `_id` armazenado na venda.
                cli_doc = self.db.col_clientes.find_one({"_id": vd["cliente_id"]})

                # Se um cliente for encontrado, extrai o nome do cliente e
                #       armazena na variável `nome_cli`.
                if cli_doc:
                    nome_cli = cli_doc["nome"]

            # Itera sobre a lista de itens da venda.
            # Cada venda pode conter vários itens, e precisamos verificar
            #       se o produto desejado está presente.
            for it in vd["itens"]:

                # Verifica se o ID do produto no item corresponde ao
                #       `self.id_prod` (produto filtrado).
                # `str(it["produto_id"]) == self.id_prod` garante que a
                #       comparação seja feita como string.
                if str(it["produto_id"]) == self.id_prod:

                    # Calcula o subtotal do item multiplicando a quantidade
                    #       comprada pelo preço unitário.
                    subt = it["quantidade"] * it["preco_unitario"]

                    # Adiciona os detalhes da venda formatados em um dicionário dentro da lista `lista`.
                    # `"data_obj"`: armazena a data como objeto `datetime`, útil para ordenação futura.
                    # `"data_br"`: armazena a data no formato brasileiro (DD/MM/AAAA) para exibição.
                    # `"cliente"`: nome do cliente, se disponível; caso contrário, permanece uma string vazia.
                    # `"forma"`: forma de pagamento utilizada na transação.
                    # `"subt_str"`: subtotal formatado como string com duas
                    #       casas decimais para exibição.
                    lista.append({
                        "data_obj": data_obj,
                        "data_br": data_br,
                        "cliente": nome_cli,
                        "forma": forma,
                        "subt_str": f"{subt:.2f}"
                    })

        # Retorna a lista contendo todas as vendas filtradas e
        #       formatadas para exibição na Treeview.
        return lista


    # Método privado para exibir os dados na Treeview.
    # `dados` é uma lista de dicionários contendo as informações
    #       das vendas filtradas.
    def _exibir(self, dados):

        # Remove todos os itens atualmente exibidos na Treeview
        #       antes de inserir os novos dados.
        # `self.tree.get_children()` retorna todos os itens da Treeview.
        # O loop percorre esses itens e os remove um por um usando `self.tree.delete(i)`.
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insere os novos dados na Treeview.
        # O loop percorre cada dicionário na lista `dados`, que
        #       contém as informações da venda formatadas.
        for d in dados:

            # Insere uma nova linha na Treeview.
            # `""` indica que o item não tem um elemento pai (é um item de nível raiz).
            # `"end"` significa que o item será adicionado no final da lista.
            # `values=(d["data_br"], d["cliente"], d["forma"], d["subt_str"])`
            #       define os valores que serão exibidos
            #        nas colunas da tabela, garantindo que a data, cliente,
            #        forma de pagamento e subtotal sejam exibidos corretamente.
            self.tree.insert("", "end",
                             values=(d["data_br"], d["cliente"], d["forma"], d["subt_str"]))

    # Método para filtrar os dados com base nos critérios
    #       inseridos pelo usuário.
    def filtrar(self):

        # Obtém e converte a data inicial informada pelo usuário.
        # `self.ent_data_ini.get()` captura o valor do campo de entrada.
        # `analisar_data_br()` converte a data do formato
        #       brasileiro (DD/MM/AAAA) para um objeto datetime.
        dt_ini = analisar_data_br(self.ent_data_ini.get())

        # Obtém e converte a data final informada pelo usuário.
        # `self.ent_data_fim.get()` captura o valor do campo de entrada.
        # `analisar_data_br()` converte a data para um objeto datetime.
        dt_fim = analisar_data_br(self.ent_data_fim.get())

        # Obtém o valor do filtro de cliente inserido pelo usuário.
        # `self.ent_cliente.get()` captura o texto digitado no campo de entrada.
        # `.lower()` converte para minúsculas para tornar a busca case-insensitive.
        # `.strip()` remove espaços em branco extras no início e no fim da string.
        cli_f = self.ent_cliente.get().lower().strip()

        # Obtém o valor do filtro da forma de pagamento.
        # `.lower().strip()` garante que a entrada seja comparada
        #       corretamente, ignorando maiúsculas/minúsculas e espaços.
        forma_f = self.ent_forma.get().lower().strip()

        # Obtém o valor do filtro de subtotal inserido pelo usuário.
        # `.lower().strip()` permite que o usuário insira valores
        #       sem se preocupar com espaços extras.
        subt_f = self.ent_subt.get().lower().strip()

        # Inicializa uma lista vazia para armazenar os registros
        #       que atendem aos critérios de filtro.
        filtrados = []

        # Percorre a lista de dados originais (`self.dados`) e aplica os filtros.
        for d in self.dados:

            # Verifica se a data da venda está antes da data inicial do filtro.
            # Se `dt_ini` for informado e `d["data_obj"]` existir, a venda
            #       será ignorada se estiver antes do intervalo.
            if dt_ini and d["data_obj"] and d["data_obj"] < dt_ini:
                continue  # Pula para a próxima iteração.

            # Verifica se a data da venda está depois da data final do filtro.
            # Se `dt_fim` for informado e `d["data_obj"]` existir, a
            #       venda será ignorada se estiver fora do intervalo.
            if dt_fim and d["data_obj"] and d["data_obj"] > dt_fim:
                continue  # Pula para a próxima iteração.

            # Verifica se o filtro de cliente foi informado e se o
            #       nome do cliente não contém o termo digitado.
            # `.lower()` garante que a comparação não seja sensível a maiúsculas e minúsculas.
            if cli_f and cli_f not in d["cliente"].lower():
                continue  # Pula para a próxima iteração.

            # Verifica se o filtro de forma de pagamento foi informado e
            #       se não há correspondência.
            # `.lower()` é usado para tornar a busca case-insensitive.
            if forma_f and forma_f not in d["forma"].lower():
                continue  # Pula para a próxima iteração.

            # Verifica se o filtro de subtotal foi informado e se não
            #           há correspondência na string formatada.
            # `.lower()` garante que a busca ignore maiúsculas e minúsculas.
            if subt_f and subt_f not in d["subt_str"].lower():
                continue  # Pula para a próxima iteração.

            # Se o registro passou por todos os filtros, ele é
            #       adicionado à lista `filtrados`.
            filtrados.append(d)

        # Exibe os dados filtrados na Treeview.
        # `_exibir(filtrados)` substitui os dados exibidos na
        #       interface pelos registros filtrados.
        self._exibir(filtrados)



# Define a classe `FormProduto`, que herda de `tk.Toplevel`.
class FormProduto(tk.Toplevel):

    # Define o método inicializador da classe.
    def __init__(self, pai, func_cb, db: GerenciadorBanco, dados=None):

        # Chama o construtor da classe base `tk.Toplevel`.
        super().__init__(pai)

        # Define o título da janela.
        self.title("Cadastro/Editar Produto")

        # Armazena o callback de função para ser chamado quando
        #       os dados forem salvos.
        self.func_cb = func_cb

        # Armazena uma referência ao gerenciador de banco de dados.
        self.db = db

        # Define que a janela não pode ser redimensionada.
        self.resizable(False, False)

        # Define a janela como modal (bloqueia a interação com a
        #       janela principal até ser fechada).
        self.transient(pai)

        # Coloca o foco na janela atual e bloqueia interações com outras janelas.
        self.grab_set()

        # Cria um rótulo para o campo "Código".
        # `text="Código:"` define o texto exibido no rótulo.
        # `row=0, column=0` posiciona o rótulo na primeira linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para o código.
        # O campo será usado para digitar ou editar o código do produto.
        # `row=0, column=1` posiciona o campo na primeira linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_codigo = tk.Entry(self)
        self.ent_codigo.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Nome".
        # `text="Nome:"` define o texto exibido no rótulo.
        # `row=1, column=0` posiciona o rótulo na segunda linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para o nome.
        # O campo será usado para digitar ou editar o nome do produto.
        # `row=1, column=1` posiciona o campo na segunda linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_nome = tk.Entry(self)
        self.ent_nome.grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Descrição".
        # `text="Descrição:"` define o texto exibido no rótulo.
        # `row=2, column=0` posiciona o rótulo na terceira linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para a descrição do produto.
        # O campo será usado para digitar ou editar a descrição do produto.
        # `row=2, column=1` posiciona o campo na terceira linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_desc = tk.Entry(self)
        self.ent_desc.grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Categoria".
        # `text="Categoria:"` define o texto exibido no rótulo.
        # `row=3, column=0` posiciona o rótulo na quarta linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Categoria:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para a categoria do produto.
        # Este campo será usado para digitar ou editar a categoria do produto.
        # `row=3, column=1` posiciona o campo na quarta linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_cat = tk.Entry(self)
        self.ent_cat.grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Preço Compra".
        # `text="Preço Compra:"` define o texto exibido no rótulo.
        # `row=4, column=0` posiciona o rótulo na quinta linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Preço Compra:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para o preço de compra.
        # Este campo será usado para digitar ou editar o valor de compra do produto.
        # `row=4, column=1` posiciona o campo na quinta linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_pc = tk.Entry(self)
        self.ent_pc.grid(row=4, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Preço Venda".
        # `text="Preço Venda:"` define o texto exibido no rótulo.
        # `row=5, column=0` posiciona o rótulo na sexta linha e
        #       primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Preço Venda:").grid(row=5, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para o preço de venda.
        # Este campo será usado para digitar ou editar o valor de venda do produto.
        # `row=5, column=1` posiciona o campo na sexta linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_pv = tk.Entry(self)
        self.ent_pv.grid(row=5, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Qtd. Estoque".
        # `text="Qtd. Estoque:"` define o texto exibido no rótulo.
        # `row=6, column=0` posiciona o rótulo na sétima linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Qtd. Estoque:").grid(row=6, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de texto para a quantidade em estoque.
        # Este campo será usado para digitar ou editar a quantidade de produtos em estoque.
        # `row=6, column=1` posiciona o campo na sétima linha e segunda coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do campo.
        self.ent_qt = tk.Entry(self)
        self.ent_qt.grid(row=6, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Fornecedor".
        # `text="Fornecedor:"` define o texto exibido no rótulo.
        # `row=7, column=0` posiciona o rótulo na oitava linha e primeira coluna da grade.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        tk.Label(self,
                 text="Fornecedor:").grid(row=7, column=0, padx=5, pady=5, sticky="e")

        # Obtém a lista de fornecedores do banco de dados.
        # A função `listar_fornecedores()` retorna uma lista de
        #       fornecedores cadastrados no banco.
        lista_forns = self.db.listar_fornecedores()

        # Cria uma variável Tkinter para armazenar o fornecedor selecionado.
        # `self.var_forn` será usada para vincular o valor escolhido no ComboBox ao código.
        self.var_forn = tk.StringVar()

        # Cria um ComboBox para selecionar o fornecedor.
        # `textvariable=self.var_forn` vincula o valor selecionado à variável `self.var_forn`.
        # `values=[f["nome"] for f in lista_forns]` preenche o ComboBox com os
        #       nomes dos fornecedores obtidos da lista `lista_forns`.
        # `state="readonly"` define que o ComboBox será somente leitura, ou seja,
        #       os valores só podem ser escolhidos da lista.
        self.combo_forn = ttk.Combobox( self,
                                        textvariable=self.var_forn,
                                        values=[f["nome"] for f in lista_forns],
                                        state="readonly")

        # Adiciona o ComboBox à grade da interface.
        # `row=7, column=1` posiciona o ComboBox na oitava linha e segunda coluna.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical ao redor do ComboBox.
        self.combo_forn.grid(row=7, column=1, padx=5, pady=5)

        # Cria um frame para os botões.
        # `frm_b = tk.Frame(self)` cria um frame dentro do formulário atual.
        frm_b = tk.Frame(self)

        # Posiciona o frame na grade da interface.
        # `row=8, column=0, columnspan=2` coloca o frame na nona
        #       linha, abrangendo duas colunas.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do frame.
        frm_b.grid(row=8, column=0, columnspan=2, pady=10)

        # Cria um botão para salvar os dados do formulário.
        # `text="Salvar"` define o texto exibido no botão.
        # `command=self.ao_salvar` associa a função `ao_salvar` ao clique no botão.
        tk.Button(frm_b, text="Salvar", command=self.ao_salvar).pack(side="left", padx=5)

        # Cria um botão para cancelar/fechar o formulário.
        # `text="Cancelar"` define o texto exibido no botão.
        # `command=self.destroy` associa a ação de fechar o formulário ao clique no botão.
        tk.Button(frm_b, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

        # Verifica se existem dados para preencher o formulário.
        if dados:

            # Insere o código do produto no campo de entrada correspondente.
            self.ent_codigo.insert(0, dados["codigo"])

            # Insere o nome do produto no campo de entrada correspondente.
            self.ent_nome.insert(0, dados["nome"])

            # Insere a descrição do produto no campo de entrada correspondente.
            self.ent_desc.insert(0, dados["descricao"])

            # Insere a categoria do produto no campo de entrada correspondente.
            self.ent_cat.insert(0, dados["categoria"])

            # Insere o preço de compra no campo de entrada correspondente.
            self.ent_pc.insert(0, dados["preco_compra"])

            # Insere o preço de venda no campo de entrada correspondente.
            self.ent_pv.insert(0, dados["preco_venda"])

            # Insere a quantidade em estoque no campo de entrada correspondente.
            self.ent_qt.insert(0, dados["quantidade_estoque"])

            # Busca o documento do fornecedor relacionado ao produto.
            doc_forn = self.db.col_fornecedores.find_one({"_id": dados["fornecedor_id"]})

            # Se o fornecedor for encontrado, seleciona-o no combobox.
            if doc_forn:
                self.combo_forn.set(doc_forn["nome"])

        # Centraliza a janela do formulário.
        self.after(0, lambda: centralizar_janela(self))

    # Define a função ao_salvar para ser chamada ao
    #       clicar no botão "Salvar".
    def ao_salvar(self):

        # Obtém o texto do campo de entrada do código, removendo espaços extras.
        cd = self.ent_codigo.get().strip()  # Código do produto.

        # Obtém o texto do campo de entrada do nome, removendo espaços extras.
        nm = self.ent_nome.get().strip()  # Nome do produto.

        # Obtém o texto do campo de entrada da descrição, removendo espaços extras.
        ds = self.ent_desc.get().strip()  # Descrição do produto.

        # Obtém o texto do campo de entrada da categoria, removendo espaços extras.
        cat = self.ent_cat.get().strip()  # Categoria do produto.

        # Obtém o texto do campo de entrada do preço de compra,
        #       removendo espaços extras.
        pc = self.ent_pc.get().strip()  # Preço de compra do produto.

        # Obtém o texto do campo de entrada do preço de venda,
        #       removendo espaços extras.
        pv = self.ent_pv.get().strip()  # Preço de venda do produto.

        # Obtém o texto do campo de entrada da quantidade em estoque,
        #       removendo espaços extras.
        qt = self.ent_qt.get().strip()  # Quantidade em estoque.

        # Obtém o texto do campo de entrada do fornecedor, removendo espaços extras.
        forn_nome = self.var_forn.get().strip()  # Nome do fornecedor.

        # Verifica se os campos de código e nome estão preenchidos.
        if not cd or not nm:

            # Exibe uma mensagem de erro caso um deles esteja vazio.
            messagebox.showerror("Erro",
                                 "Campos 'Código' e 'Nome' são obrigatórios!")
            return

        # Busca no banco de dados pelo fornecedor com o nome fornecido.
        doc_forn = self.db.col_fornecedores.find_one({"nome": forn_nome})

        # Se não encontrar o fornecedor, exibe uma mensagem de erro.
        if not doc_forn:
            messagebox.showerror("Erro",
                                 "Fornecedor inválido ou não selecionado.")
            return

        # Tenta converter os valores de preço de compra, preço de
        #       venda e quantidade para tipos numéricos.
        try:

            # Converte o preço de compra para um número decimal (float).
            pc_val = float(pc)

            # Converte o preço de venda para um número decimal (float).
            pv_val = float(pv)

            # Converte a quantidade para um número inteiro (int).
            qt_val = int(qt)

        except:

            # Caso a conversão falhe, exibe uma mensagem de erro
            #       indicando que os valores devem ser numéricos.
            messagebox.showerror("Erro",
                                 "Preço e quantidade devem ser numéricos.")
            return

        # Chama a função de callback (func_cb) com os valores já validados e convertidos,
        # incluindo o identificador (_id) do fornecedor selecionado.
        self.func_cb(cd, nm, ds, cat, pc_val, pv_val, qt_val, doc_forn["_id"])

        # Fecha a janela atual após salvar os dados.
        self.destroy()


###############################################################################
# QUADRO ADMINISTRATIVO
###############################################################################

# Classe `QuadroAdmin` que representa o painel administrativo da aplicação.
# Herda de `tk.Frame`, tornando-se um container para os
#       elementos da interface administrativa.
class QuadroAdmin(tk.Frame):

    # Método construtor da classe.
    # `pai` define o container onde o QuadroAdmin será inserido.
    # `db: GerenciadorBanco` é a instância do banco de dados
    #       para operações administrativas.
    # `usuario_logado` armazena as informações do usuário autenticado.
    def __init__(self, pai, db: GerenciadorBanco, usuario_logado):

        # Inicializa o `Frame` como um container dentro do `pai` (janela principal).
        super().__init__(pai)

        # Armazena a referência ao banco de dados na instância.
        self.db = db

        # Armazena os dados do usuário logado na instância.
        self.usuario = usuario_logado

        # Cria um rótulo (Label) para exibir o título do painel administrativo.
        # `text="Painel Administrativo"` define o texto exibido.
        # `font=("Arial", 16, "bold")` define a fonte como Arial, tamanho 16 e em negrito.
        # `.pack(pady=10)` adiciona um espaçamento vertical de 10 pixels para organização visual.
        tk.Label(self,
                 text="Painel Administrativo",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Cria um botão para abrir a janela de gerenciamento de usuários.
        # `text="Gerenciar Usuários"` define o texto do botão.
        # `command=self.abrir_janela_usuarios` associa a
        #       função `abrir_janela_usuarios` ao clique do botão.
        # `.pack(pady=5)` adiciona um espaçamento vertical de 5 pixels abaixo do botão.
        tk.Button(self,
                  text="Gerenciar Usuários",
                  command=self.abrir_janela_usuarios).pack(pady=5)

        # Cria um botão para abrir a janela de relatórios completos.
        # `text="Relatórios Completos"` define o texto do botão.
        # `command=self.abrir_relatorio_completo` associa a
        #       função `abrir_relatorio_completo` ao clique do botão.
        # `.pack(pady=5)` adiciona um espaçamento vertical
        #       de 5 pixels abaixo do botão.
        tk.Button(self,
                  text="Relatórios Completos",
                  command=self.abrir_relatorio_completo).pack(pady=5)



        # Cria um botão para abrir o Relatório Resumido.
        # - `text="Relatório Resumido"` define o rótulo do botão exibido na interface.
        # - `command=self.abrir_relatorio_resumido` associa o botão à função `abrir_relatorio_resumido`,
        #           garantindo que ao clicar, a tela do relatório resumido será aberta.
        btn_relatorio_resumido = tk.Button(self,
                                           text="Relatório Resumido",
                                           command=self.abrir_relatorio_resumido)

        # Posiciona o botão na interface.
        # - `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do botão,
        #           garantindo um layout mais organizado.
        btn_relatorio_resumido.pack(pady=5)



    def abrir_relatorio_resumido(self):

        """
        Método responsável por abrir a janela do Relatório Resumido.

        Este método cria uma nova instância da classe `JanelaRelatorioResumido`,
                que exibe os dados resumidos das vendas agrupados por cliente, produto e vendedor.

        Parâmetros:
        - Nenhum.

        Retorno:
        - Nenhum (a nova janela é aberta como um `Toplevel` dentro da aplicação).
        """

        # Cria uma nova instância da classe `JanelaRelatorioResumido`.
        # - `self.master`: Define a janela principal como a janela pai da nova instância.
        # - `self.db`: Passa a conexão com o banco de dados para que o
        #       relatório possa buscar os dados necessários.
        JanelaRelatorioResumido(self.master, self.db)


    # Método para abrir a janela de gerenciamento de usuários.
    def abrir_janela_usuarios(self):

        # Verifica se o usuário tem permissão de administrador antes de continuar.
        # `self.usuario["permissao"]` armazena o nível de permissão do usuário logado.
        # Se não for "admin", exibe uma mensagem de erro e interrompe a execução do método.
        if self.usuario["permissao"] != "admin":

            # Exibe um alerta informando que o acesso foi negado.
            # `messagebox.showerror("Erro", "Acesso negado!")` exibe uma janela de erro.
            return

        # Cria uma nova janela modal para gerenciamento de usuários.
        # `tk.Toplevel(self)` cria uma nova janela filha da interface principal.
        jan = tk.Toplevel(self)

        # Define o título da janela como "Usuários".
        # `jan.title("Usuários")` exibe o título na barra superior da nova janela.
        jan.title("Usuários")

        # Define o tamanho da janela para 600 pixels de largura e 400 pixels de altura.
        # `jan.geometry("600x400")` define a dimensão inicial da janela.
        jan.geometry("600x400")

        # Centraliza a nova janela na tela.
        # `centralizar_janela(jan)` chama uma função externa que
        #       ajusta a posição da janela no centro da tela.
        centralizar_janela(jan)

        # Cria uma barra de rolagem vertical para a lista de usuários.
        # `tk.Scrollbar(jan, orient="vertical")` cria um Scrollbar dentro da janela `jan`,
        #       com orientação vertical, permitindo a rolagem da lista de usuários.
        scroll_y = tk.Scrollbar(jan, orient="vertical")

        # Cria um widget Treeview para exibir a lista de usuários cadastrados.
        # `jan` define que o Treeview será inserido dentro da janela `jan`.
        # `columns=("Nome", "Usuário", "Permissão")` define as colunas da tabela.
        # `show="headings"` remove a primeira coluna padrão e exibe apenas os cabeçalhos definidos.
        # `yscrollcommand=scroll_y.set` conecta a barra de rolagem vertical ao Treeview,
        #       garantindo que a rolagem funcione corretamente quando a lista for longa.
        self.lista_usuarios = ttk.Treeview(jan,
                                           columns=("Nome", "Usuário", "Permissão"),
                                           show="headings",
                                           yscrollcommand=scroll_y.set)

        # Configura a barra de rolagem para controlar a visualização do Treeview.
        # `scroll_y.config(command=self.lista_usuarios.yview)` associa a barra de rolagem ao Treeview,
        #       garantindo que, ao mover a barra, a lista de usuários role corretamente na vertical.
        scroll_y.config(command=self.lista_usuarios.yview)

        # Posiciona a barra de rolagem na lateral direita da janela.
        # `side="right"` coloca a barra à direita do container (jan).
        # `fill="y"` faz com que a barra ocupe toda a altura disponível na janela.
        scroll_y.pack(side="right", fill="y")

        # Define o cabeçalho das colunas da Treeview.
        # `self.lista_usuarios.heading("Nome", text="Nome")` define o
        #       cabeçalho da coluna "Nome" como "Nome".
        self.lista_usuarios.heading("Nome", text="Nome")

        # Define o cabeçalho da coluna "Usuário".
        # O texto exibido no cabeçalho será "Usuário".
        self.lista_usuarios.heading("Usuário", text="Usuário")

        # Define o cabeçalho da coluna "Permissão".
        # O texto exibido será "Permissão", indicando o nível de acesso do
        #       usuário (ex: admin, gerente, vendedor).
        self.lista_usuarios.heading("Permissão", text="Permissão")

        # Configura a largura das colunas para melhorar a visualização.
        # `self.lista_usuarios.column("Nome", width=150)` define a
        #       largura da coluna "Nome" como 150 pixels,
        #       permitindo que nomes mais longos sejam exibidos corretamente.
        self.lista_usuarios.column("Nome", width=150)

        # Define a largura da coluna "Usuário" como 100 pixels.
        # Isso evita que nomes de usuário muito longos fiquem cortados ou desorganizados.
        self.lista_usuarios.column("Usuário", width=100)

        # Define a largura da coluna "Permissão" como 100 pixels.
        # Essa largura é suficiente para exibir permissões como "Admin", "Gerente" ou "Vendedor".
        self.lista_usuarios.column("Permissão", width=100)

        # Adiciona a Treeview à interface gráfica.
        # `fill="both"` permite que a Treeview se expanda para preencher o
        #       espaço disponível horizontal e verticalmente.
        # `expand=True` garante que a tabela ocupe todo o espaço
        #       possível dentro da janela `jan`.
        self.lista_usuarios.pack(fill="both", expand=True)

        # Cria um frame para organizar os botões de ação (Cadastrar,
        #       Editar e Excluir Usuário).
        # `frm_btn = tk.Frame(jan)` cria um frame dentro da
        #       janela `jan` para posicionar os botões.
        frm_btn = tk.Frame(jan)

        # Posiciona o frame na interface com um espaçamento vertical de 5 pixels.
        # `pady=5` adiciona um espaço entre o frame e os elementos acima dele.
        frm_btn.pack(pady=5)

        # Cria um botão para cadastrar um novo usuário.
        # `text="Cadastrar Usuário"` define o texto exibido no botão.
        # `command=self.cadastrar_usuario` associa o botão ao método `cadastrar_usuario`,
        #       que será chamado quando o usuário clicar no botão.
        # `side="left"` posiciona o botão no lado esquerdo do frame.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels entre os botões.
        tk.Button(frm_btn,
                  text="Cadastrar Usuário",
                  command=self.cadastrar_usuario).pack(side="left", padx=5)

        # Cria um botão para editar um usuário selecionado.
        # `text="Editar Usuário"` exibe o texto no botão.
        # `command=self.editar_usuario` chama o método `editar_usuario` ao clicar no botão.
        # `side="left"` posiciona o botão no lado esquerdo, ao lado do botão anterior.
        # `padx=5` mantém um espaçamento entre os botões para uma melhor organização visual.
        tk.Button(frm_btn,
                  text="Editar Usuário",
                  command=self.editar_usuario).pack(side="left", padx=5)

        # Cria um botão para excluir um usuário selecionado.
        # `text="Excluir Usuário"` define o texto exibido no botão.
        # `command=self.excluir_usuario` associa o botão ao método `excluir_usuario`,
        #       que será chamado quando o usuário clicar no botão.
        # `side="left"` alinha o botão ao lado dos anteriores.
        # `padx=5` mantém um espaçamento horizontal entre os botões.
        tk.Button(frm_btn,
                  text="Excluir Usuário",
                  command=self.excluir_usuario).pack(side="left", padx=5)

        # Chama o método para atualizar a lista de usuários na Treeview.
        # Esse método busca os usuários cadastrados no banco de
        #       dados e os exibe na interface.
        self.atualizar_lista_usuarios()


    # Método para atualizar a lista de usuários exibida na Treeview.
    def atualizar_lista_usuarios(self):

        # Remove todos os itens atualmente exibidos na Treeview para evitar duplicação.
        # `self.lista_usuarios.get_children()` retorna todos os itens da tabela.
        # O loop percorre esses itens e os remove um por um
        #       usando `self.lista_usuarios.delete(i)`.
        for i in self.lista_usuarios.get_children():
            self.lista_usuarios.delete(i)

        # Percorre a lista de usuários recuperados do banco de dados.
        # `self.db.listar_usuarios()` retorna uma lista contendo os usuários cadastrados.
        for u in self.db.listar_usuarios():

            # Insere um novo item na Treeview com as informações do usuário.
            # `""` indica que o item será inserido na raiz da Treeview.
            # `"end"` significa que o item será adicionado ao final da lista.
            # `values=(u["nome"], u["usuario"], u["permissao"])` define os
            #       valores a serem exibidos nas colunas.
            # `iid=str(u["_id"])` define um identificador único para
            #       cada linha, baseado no ID do usuário no banco de dados.
            self.lista_usuarios.insert("",
                                       "end",
                                       values=(u["nome"], u["usuario"], u["permissao"]), iid=str(u["_id"]))



    # Método para cadastrar um novo usuário no sistema.
    def cadastrar_usuario(self):

        # Verifica se o usuário logado tem permissão de administrador.
        # `self.usuario["permissao"]` armazena o nível de permissão do usuário atual.
        # Caso não seja "admin", exibe uma mensagem de erro e interrompe a execução do método.
        if self.usuario["permissao"] != "admin":

            # Exibe um alerta informando que apenas administradores
            #       podem cadastrar usuários.
            # `messagebox.showerror("Erro", "Apenas administrador pode
            #       cadastrar.")` cria uma caixa de diálogo de erro.
            return

        # Método para salvar um novo usuário no banco de dados.
        def salvar():

            # Obtém o valor do campo "Nome", removendo espaços
            #       extras antes e depois do texto.
            n = ent_nome.get().strip()

            # Obtém o valor do campo "Usuário", removendo espaços
            #       extras antes e depois do texto.
            usr = ent_user.get().strip()

            # Obtém o valor do campo "Senha", removendo espaços
            #       extras antes e depois do texto.
            snh = ent_senha.get().strip()

            # Obtém a permissão selecionada no combobox e remove espaços extras.
            perm = combo_perm.get().strip()

            # Verifica se algum dos campos obrigatórios está vazio.
            # Se "Nome", "Usuário" ou "Senha" não forem preenchidos, exibe
            #       uma mensagem de erro e interrompe o processo.
            if not n or not usr or not snh:

                # Exibe uma mensagem de erro caso algum campo esteja vazio.
                messagebox.showerror("Erro", "Preencha todos os campos!")

                return  # Sai da função sem prosseguir.

            # Chama o método `criar_usuario` no banco de dados para
            #       tentar cadastrar o novo usuário.
            # `status` indica se a operação foi bem-sucedida (True ou False).
            # `msg` contém uma mensagem informando o resultado da operação.
            status, msg = self.db.criar_usuario(n, usr, snh, perm)

            # Se o cadastro for bem-sucedido, exibe uma mensagem de sucesso.
            if status:

                # Exibe uma mensagem informando que o usuário foi
                #       cadastrado com sucesso.
                messagebox.showinfo("Sucesso", msg)

                # Atualiza a lista de usuários na interface para
                #       refletir o novo cadastro.
                self.atualizar_lista_usuarios()

                # Fecha a janela de cadastro após a operação ser concluída.
                form.destroy()

            else:

                # Caso ocorra um erro no cadastro (ex.: usuário já existente),
                #       exibe uma mensagem de erro com a descrição do problema.
                messagebox.showerror("Erro", msg)

        # Cria uma nova janela para o formulário de cadastro de usuário.
        # `tk.Toplevel()` cria uma nova janela modal que fica
        #       sobre a janela principal.
        form = tk.Toplevel()

        # Define o título da nova janela como "Cadastrar Usuário".
        # `form.title("Cadastrar Usuário")` exibe esse título na
        #       barra superior da janela.
        form.title("Cadastrar Usuário")

        # Define o tamanho da janela como 300 pixels de largura por 200 pixels de altura.
        # Isso garante um tamanho compacto e organizado para o
        #       formulário de cadastro.
        form.geometry("300x200")

        # Centraliza a janela na tela.
        # `centralizar_janela(form)` chama uma função externa para
        #       posicionar a janela no centro da tela,
        #       melhorando a experiência do usuário ao abrir a interface.
        centralizar_janela(form)

        # Cria um rótulo (Label) para o campo "Nome Completo".
        # `text="Nome Completo:"` define o texto exibido ao lado do campo de entrada.
        # `.grid(row=0, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 0 e coluna 0,
        #       adicionando espaçamento horizontal (`padx=5`) e vertical (`pady=5`).
        # `sticky="e"` alinha o texto à direita da célula para
        #       um melhor alinhamento com o campo de entrada.
        tk.Label(form,
                 text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o usuário digitar o nome completo.
        # `tk.Entry(form)` cria uma caixa de texto dentro da
        #       janela `form` onde o usuário pode digitar.
        ent_nome = tk.Entry(form)

        # Posiciona o campo de entrada ao lado do rótulo.
        # `.grid(row=0, column=1, padx=5, pady=5)` coloca o campo
        #       de entrada na linha 0, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do campo
        #       para melhorar a organização visual.
        ent_nome.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) para o campo "Usuário".
        # `text="Usuário:"` define o texto exibido ao lado do campo de entrada.
        # `.grid(row=1, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 1 e coluna 0,
        #       adicionando espaçamento horizontal (`padx=5`) e vertical (`pady=5`).
        # `sticky="e"` alinha o texto à direita da célula para um
        #       melhor alinhamento com o campo de entrada.
        tk.Label(form,
                 text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para o usuário digitar o nome de usuário (login).
        # `tk.Entry(form)` cria uma caixa de texto dentro da
        #       janela `form` onde o usuário pode digitar.
        ent_user = tk.Entry(form)

        # Posiciona o campo de entrada ao lado do rótulo.
        # `.grid(row=1, column=1, padx=5, pady=5)` coloca o campo de
        #       entrada na linha 1, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do
        #       campo para melhorar a organização visual.
        ent_user.grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) para o campo "Senha".
        # `text="Senha:"` define o texto exibido ao lado do campo de entrada.
        # `.grid(row=2, column=0, padx=5, pady=5, sticky="e")`
        #        posiciona o rótulo na linha 2 e coluna 0,
        #       adicionando espaçamento horizontal (`padx=5`) e vertical (`pady=5`).
        # `sticky="e"` alinha o texto à direita da célula para um
        #       melhor alinhamento com o campo de entrada.
        tk.Label(form,
                 text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada para a senha do usuário.
        # `tk.Entry(form, show="*")` cria uma caixa de texto
        #       onde o usuário pode digitar a senha.
        # O argumento `show="*"` oculta os caracteres digitados,
        #       exibindo asteriscos no lugar da senha.
        ent_senha = tk.Entry(form, show="*")

        # Posiciona o campo de entrada ao lado do rótulo.
        # `.grid(row=2, column=1, padx=5, pady=5)` coloca o
        #       campo de entrada na linha 2, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do
        #       campo para melhorar a organização visual.
        ent_senha.grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) para o campo "Permissão".
        # `text="Permissão:"` define o texto exibido ao lado do campo de seleção.
        # `.grid(row=3, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 3 e coluna 0,
        #       adicionando espaçamento horizontal (`padx=5`) e vertical (`pady=5`).
        # `sticky="e"` alinha o texto à direita da célula para um
        #       melhor alinhamento com o combobox.
        tk.Label(form,
                 text="Permissão:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de seleção (Combobox) para escolher a permissão do usuário.
        # `ttk.Combobox(form, values=["admin", "gerente", "vendedor"],
        #       state="readonly")` cria um combobox
        #       onde o usuário pode selecionar entre três opções: "admin", "gerente" e "vendedor".
        # `state="readonly"` impede que o usuário digite manualmente
        #       valores diferentes dos disponíveis na lista.
        combo_perm = ttk.Combobox(form,
                                  values=["admin", "gerente", "vendedor"],
                                  state="readonly")

        # Define a opção padrão do combobox como "vendedor".
        # Isso garante que, caso o usuário não altere a seleção, o
        #       valor padrão será "vendedor".
        combo_perm.set("vendedor")

        # Posiciona o combobox ao lado do rótulo.
        # `.grid(row=3, column=1, padx=5, pady=5)` coloca o
        #       combobox na linha 3, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do campo
        #       para melhorar a organização visual.
        combo_perm.grid(row=3, column=1, padx=5, pady=5)

        # Cria um botão para salvar os dados do novo usuário.
        # `text="Salvar"` define o texto exibido no botão.
        # `command=salvar` associa a ação de salvar os dados quando o botão for clicado.
        # `row=4` posiciona o botão na quarta linha do formulário.
        # `column=0` posiciona o botão na primeira coluna.
        # `columnspan=2` faz com que o botão ocupe duas colunas,
        #       garantindo que ele fique centralizado.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao
        #       redor do botão, melhorando a aparência visual.
        tk.Button(form,
                  text="Salvar",
                  command=salvar).grid(row=4, column=0, columnspan=2, pady=10)


    # Função para editar um usuário selecionado na lista.
    def editar_usuario(self):

        # Obtém a seleção atual na lista de usuários.
        # `self.lista_usuarios.selection()` retorna os itens selecionados.
        sel = self.lista_usuarios.selection()

        # Verifica se nenhum usuário foi selecionado.
        # Se a lista `sel` estiver vazia, exibe uma mensagem de erro.
        if not sel:

            # Exibe uma caixa de diálogo informando que um usuário deve
            #       ser selecionado antes de editar.
            # `messagebox.showerror("Erro", "Selecione um usuário
            #       para editar.")` mostra um alerta com o título "Erro"
            #       e a mensagem de erro correspondente.
            messagebox.showerror("Erro",
                                 "Selecione um usuário para editar.")

            # Sai da função para evitar erros.
            return

        # Obtém o ID do usuário selecionado.
        # `sel[0]` acessa o primeiro item da lista de seleção, que
        #       corresponde ao ID do usuário na lista.
        id_usr = sel[0]

        # Verifica se o usuário selecionado é o mesmo usuário logado.
        # `self.usuario["_id"]` contém o ID do usuário atualmente logado.
        # `str(self.usuario["_id"])` converte esse ID para
        #       string para comparação com `id_usr`.
        if id_usr == str(self.usuario["_id"]):

            # O usuário pode editar seus próprios dados, mas isso
            #       pode causar problemas se ele tentar se excluir.
            # Por enquanto, apenas ignoramos essa verificação, permitindo a edição.
            pass

        # Busca os dados do usuário selecionado no banco de dados.
        # `self.db.col_usuarios.find_one({"_id": ObjectId(id_usr)})`
        #       procura um usuário cujo ID seja igual ao `id_usr`.
        # `ObjectId(id_usr)` converte o ID do usuário para o formato correto do MongoDB.
        doc_u = self.db.col_usuarios.find_one({"_id": ObjectId(id_usr)})

        # Função para salvar as alterações feitas no usuário.
        def salvar_edicao():

            # Obtém o nome digitado pelo usuário e remove espaços extras.
            # `ent_nome.get().strip()` captura o valor do campo de
            #       entrada e remove espaços antes e depois do texto.
            n = ent_nome.get().strip()

            # Obtém o nome de usuário digitado e remove espaços extras.
            u = ent_user.get().strip()

            # Obtém a senha digitada e remove espaços extras.
            # Caso a senha seja deixada em branco, pode ser
            #       mantida a mesma senha existente.
            sn = ent_senha.get().strip()

            # Obtém a permissão selecionada no combobox e remove espaços extras.
            p = combo_perm.get().strip()

            # Verifica se os campos "Nome" e "Usuário" foram preenchidos.
            # Esses campos são obrigatórios para a atualização.
            if not n or not u:

                # Exibe uma mensagem de erro caso algum dos campos
                #       obrigatórios esteja vazio.
                messagebox.showerror("Erro",
                                     "Nome e Usuário são obrigatórios.")

                # Sai da função para evitar que a atualização
                #       prossiga com dados inválidos.
                return

            # Chama o método para atualizar os dados do usuário no banco de dados.
            # `self.db.atualizar_usuario(id_usr, n, u, sn, p)` atualiza o
            #       usuário identificado por `id_usr`
            #       com os novos valores de nome (`n`), usuário (`u`), senha (`sn`) e permissão (`p`).
            self.db.atualizar_usuario(id_usr, n, u, sn, p)

            # Exibe uma mensagem informando que a atualização foi realizada com sucesso.
            messagebox.showinfo("Sucesso", "Usuário atualizado!")

            # Atualiza a lista de usuários exibida na interface,
            #       refletindo as alterações feitas.
            self.atualizar_lista_usuarios()

            # Fecha a janela de edição do usuário após a atualização ser concluída.
            form_edicao.destroy()

        # Cria uma nova janela (Toplevel) para editar o usuário selecionado.
        # `tk.Toplevel()` cria uma nova janela independente, sobreposta à principal.
        form_edicao = tk.Toplevel()

        # Define o título da janela como "Editar Usuário".
        # Esse título aparece na barra superior da janela.
        form_edicao.title("Editar Usuário")

        # Define o tamanho da janela como 300 pixels de largura por 220 pixels de altura.
        form_edicao.geometry("300x220")

        # Chama a função para centralizar a janela na tela.
        # `centralizar_janela(form_edicao)` ajusta a posição da janela para
        #       que fique centralizada na tela do usuário.
        centralizar_janela(form_edicao)

        # Cria um rótulo (Label) para o campo "Nome Completo".
        # `text="Nome Completo:"` define o texto exibido ao lado do campo de entrada.
        # `.grid(row=0, column=0, padx=5, pady=5, sticky="e")` posiciona o
        #       rótulo na linha 0 e coluna 0.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical para
        #       melhorar a organização visual.
        # `sticky="e"` alinha o texto à direita da célula para garantir que
        #       fique bem alinhado com o campo de entrada.
        tk.Label(form_edicao,
                 text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa editar o nome completo.
        # `tk.Entry(form_edicao)` cria uma caixa de texto interativa
        #       dentro da janela `form_edicao`.
        ent_nome = tk.Entry(form_edicao)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=1, padx=5, pady=5)` define que ele
        #       será colocado na linha 0, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento entre os elementos
        #       para uma melhor disposição visual.
        ent_nome.grid(row=0, column=1, padx=5, pady=5)

        # Preenche automaticamente o campo de entrada com o nome atual
        #       do usuário obtido do banco de dados.
        # `doc_u["nome"]` contém o nome do usuário que está sendo editado.
        # `ent_nome.insert(0, doc_u["nome"])` insere esse nome no
        #       campo de entrada, permitindo que seja editado.
        ent_nome.insert(0, doc_u["nome"])

        # Cria um rótulo (Label) para o campo "Usuário".
        # `text="Usuário:"` define o texto exibido ao lado do campo de entrada.
        # `.grid(row=1, column=0, padx=5, pady=5, sticky="e")` posiciona o
        #       rótulo na linha 1 e coluna 0.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical
        #       para uma melhor organização visual.
        # `sticky="e"` alinha o texto à direita da célula para mantê-lo
        #       alinhado com o campo de entrada.
        tk.Label(form_edicao,
                 text="Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa editar o nome de usuário.
        # `tk.Entry(form_edicao)` cria uma caixa de texto onde o
        #       nome de usuário pode ser digitado ou modificado.
        ent_user = tk.Entry(form_edicao)

        # Posiciona o campo de entrada na interface ao lado do rótulo correspondente.
        # `.grid(row=1, column=1, padx=5, pady=5)` coloca o campo na linha 1, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do campo para
        #       melhorar a disposição dos elementos.
        ent_user.grid(row=1, column=1, padx=5, pady=5)

        # Preenche automaticamente o campo com o nome de usuário atual do banco de dados.
        # `doc_u["usuario"]` contém o nome de usuário que está sendo editado.
        # `ent_user.insert(0, doc_u["usuario"])` insere esse valor no
        #       campo de entrada, permitindo sua modificação.
        ent_user.insert(0, doc_u["usuario"])

        # Cria um rótulo (Label) para o campo "Nova Senha".
        # `text="Nova Senha:"` define o texto exibido ao lado do campo de entrada.
        # `.grid(row=2, column=0, padx=5, pady=5, sticky="e")` posiciona o
        #       rótulo na linha 2 e coluna 0.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical para
        #       uma melhor organização visual.
        # `sticky="e"` alinha o texto à direita da célula para garantir que
        #       fique bem alinhado com o campo de entrada.
        tk.Label(form_edicao,
                 text="Nova Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa inserir uma nova senha.
        # `tk.Entry(form_edicao, show="*")` cria uma caixa de texto
        #       onde a senha pode ser digitada.
        # `show="*"` mascara os caracteres digitados para ocultar a
        #       senha e garantir maior segurança.
        ent_senha = tk.Entry(form_edicao, show="*")

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=2, column=1, padx=5, pady=5)` coloca o campo na linha 2, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do
        #       campo para melhorar a organização visual.
        ent_senha.grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) para o campo "Permissão".
        # `text="Permissão:"` define o texto exibido ao lado do campo de seleção.
        # `.grid(row=3, column=0, padx=5, pady=5, sticky="e")`
        #       posiciona o rótulo na linha 3 e coluna 0.
        # `padx=5, pady=5` adiciona espaçamento horizontal e vertical
        #       para melhorar a organização visual.
        # `sticky="e"` alinha o texto à direita da célula para que
        #       fique alinhado com o campo de seleção.
        tk.Label(form_edicao,
                 text="Permissão:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Cria um menu suspenso (`Combobox`) para selecionar a permissão do usuário.
        # `values=["admin", "gerente", "vendedor"]` define as
        #       opções disponíveis no menu suspenso.
        # `state="readonly"` impede que o usuário digite valores personalizados,
        #       permitindo apenas a seleção das opções existentes.
        combo_perm = ttk.Combobox(form_edicao,
                                  values=["admin", "gerente", "vendedor"],
                                  state="readonly")

        # Posiciona o `Combobox` ao lado do rótulo correspondente.
        # `.grid(row=3, column=1, padx=5, pady=5)` coloca o menu
        #       suspenso na linha 3, coluna 1.
        # `padx=5, pady=5` adiciona espaçamento ao redor do campo
        #       para uma melhor organização visual.
        combo_perm.grid(row=3, column=1, padx=5, pady=5)

        # Define o valor inicial do `Combobox` com a permissão atual do usuário.
        # `doc_u["permissao"]` contém a permissão do usuário
        #       recuperada do banco de dados.
        # `combo_perm.set(doc_u["permissao"])` exibe essa permissão
        #       como valor selecionado no `Combobox`.
        combo_perm.set(doc_u["permissao"])

        # Cria um botão para salvar as alterações feitas nos dados do usuário.
        # `text="Salvar"` define o texto exibido no botão.
        # `command=salvar_edicao` associa a ação de salvar os dados
        #       editados ao clique do botão.
        # `.grid(row=4, column=0, columnspan=2, pady=10)` posiciona o
        #       botão na linha 4 e ocupa duas colunas.
        # `columnspan=2` faz com que o botão fique centralizado no formulário.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels
        #       para melhor organização visual.
        tk.Button(form_edicao,
                  text="Salvar",
                  command=salvar_edicao).grid(row=4, column=0, columnspan=2, pady=10)


    # Função para excluir um usuário selecionado na lista.
    def excluir_usuario(self):

        # Obtém a seleção atual na lista de usuários.
        # `self.lista_usuarios.selection()` retorna os itens selecionados.
        sel = self.lista_usuarios.selection()

        # Verifica se nenhum usuário foi selecionado.
        # Se a lista `sel` estiver vazia, exibe uma mensagem de erro.
        if not sel:

            # Exibe uma caixa de diálogo informando que um usuário deve ser
            #       selecionado antes da exclusão.
            # `messagebox.showerror("Erro", "Selecione um usuário para excluir.")`
            #       exibe um alerta com o título "Erro"
            #       e a mensagem correspondente.
            messagebox.showerror("Erro",
                                 "Selecione um usuário para excluir.")

            # Sai da função para evitar erros.
            return

        # Obtém o ID do usuário selecionado.
        # `sel[0]` acessa o primeiro item da lista de seleção,
        #       que corresponde ao ID do usuário na lista.
        id_usr = sel[0]

        # Verifica se o usuário está tentando excluir a si mesmo.
        # `str(self.usuario["_id"])` obtém o ID do usuário logado e converte para string.
        # Se `id_usr` for igual ao ID do usuário logado, impede a exclusão.
        if id_usr == str(self.usuario["_id"]):

            # Exibe uma mensagem de erro informando que o
            #       usuário não pode se excluir.
            messagebox.showerror("Erro",
                                 "Não é possível excluir a si mesmo!")

            # Sai da função para evitar a exclusão.
            return

        # Exibe uma caixa de diálogo para confirmar a exclusão do usuário.
        # `messagebox.askyesno("Confirmação", "Excluir este usuário?")`
        #       exibe uma pergunta ao usuário.
        # Se o usuário clicar em "Sim", retorna `True` e a exclusão prossegue.
        if messagebox.askyesno("Confirmação",
                               "Excluir este usuário?"):

            # Chama a função do banco de dados para remover o usuário.
            # `self.db.remover_usuario(id_usr)` deleta o usuário do
            #       banco de dados usando seu ID.
            self.db.remover_usuario(id_usr)

            # Atualiza a lista de usuários para refletir a exclusão na interface.
            # `self.atualizar_lista_usuarios()` recarrega a
            #       lista de usuários exibida na tela.
            self.atualizar_lista_usuarios()


    # Função para abrir a janela de relatório completo.
    def abrir_relatorio_completo(self):

        # Cria uma instância da classe `JanelaRelatorioCompleto`,
        #       que exibe os relatórios detalhados.
        # `self` representa a janela principal que está chamando o relatório.
        # `self.db` é a instância do banco de dados que será
        #       utilizada para buscar os dados do relatório.
        JanelaRelatorioCompleto(self, self.db)


# Definição da classe JanelaRelatorioResumido, que herda de tk.Toplevel
class JanelaRelatorioResumido(tk.Toplevel):

    """
    Construtor da classe que cria uma nova janela Toplevel para exibir o Relatório Resumido de Vendas.

    Parâmetros:
    - pai: Objeto da janela principal (master), onde esta janela está sendo aberta.
    - db: Instância do banco de dados (conexão com MongoDB ou outro banco utilizado).
    """

    def __init__(self, pai, db):

        # Chama o construtor da classe pai (tk.Toplevel), inicializando a nova janela
        super().__init__(pai)

        # Define o título da janela
        self.title("Relatório Resumido de Vendas")

        # Armazena a referência ao banco de dados para ser usada em consultas dentro da classe
        self.db = db

        # Define o tamanho da janela como 700 pixels de largura por 450 pixels de altura
        self.geometry("700x450")

        # Define esta janela como transitória em relação à janela principal (pai)
        # Isso significa que ela sempre ficará no topo da janela principal
        self.transient(pai)

        # Impede que o usuário interaja com a janela principal enquanto esta estiver aberta
        # O comando grab_set() captura os eventos de mouse e teclado apenas para esta janela
        self.grab_set()

        # Chama a função para centralizar a janela na tela do usuário
        centralizar_janela(self)

        # Criar abas para os relatórios
        # Cria um widget Notebook (Abas) dentro da janela para organizar os relatórios em abas separadas
        self.notebook = ttk.Notebook(self)

        # Posiciona o Notebook para ocupar toda a área disponível da janela
        # fill="both" → Expande tanto na horizontal quanto na vertical
        # expand=True → Permite que o notebook cresça conforme a janela for redimensionada
        self.notebook.pack(fill="both", expand=True)

        # Cria um Frame (contêiner) para cada aba dentro do Notebook
        # Cada frame conterá uma tabela específica do relatório
        self.frame_clientes = ttk.Frame(self.notebook)  # Aba para o relatório por Cliente
        self.frame_produtos = ttk.Frame(self.notebook)  # Aba para o relatório por Produto
        self.frame_vendedores = ttk.Frame(self.notebook)  # Aba para o relatório por Vendedor

        # Adiciona as abas ao Notebook, associando cada aba ao seu respectivo frame
        # O parâmetro text define o nome da aba que será exibido na interface
        self.notebook.add(self.frame_clientes, text="Por Cliente")  # Aba de clientes
        self.notebook.add(self.frame_produtos, text="Por Produto")  # Aba de produtos
        self.notebook.add(self.frame_vendedores, text="Por Vendedor")  # Aba de vendedores

        # Cria uma tabela (Treeview) dentro da aba "Por Cliente"
        # - self.frame_clientes: Define o frame onde a tabela será inserida.
        # - ["Cliente", "Total de Compras"]: Define as colunas da tabela, onde:
        #   * "Cliente" → Exibe o nome do cliente.
        #   * "Total de Compras" → Mostra o valor total que o cliente gastou.
        self.tree_clientes = self._criar_treeview(self.frame_clientes, ["Cliente", "Total de Compras"])

        # Cria uma tabela (Treeview) dentro da aba "Por Produto"
        # - self.frame_produtos: Define o frame onde a tabela será inserida.
        # - ["Produto", "Total Vendido"]: Define as colunas da tabela, onde:
        #   * "Produto" → Exibe o nome do produto vendido.
        #   * "Total Vendido" → Mostra a soma total de vendas desse produto em valor monetário.
        self.tree_produtos = self._criar_treeview(self.frame_produtos, ["Produto", "Total Vendido"])

        # Cria uma tabela (Treeview) dentro da aba "Por Vendedor"
        # - self.frame_vendedores: Define o frame onde a tabela será inserida.
        # - ["Vendedor", "Total de Vendas"]: Define as colunas da tabela, onde:
        #   * "Vendedor" → Exibe o nome do vendedor responsável pela venda.
        #   * "Total de Vendas" → Mostra o total em dinheiro vendido por esse vendedor.
        self.tree_vendedores = self._criar_treeview(self.frame_vendedores, ["Vendedor", "Total de Vendas"])

        # Cria um botão para exportar os dados das tabelas para um arquivo Excel.
        # - text="Exportar": Define o rótulo do botão que aparecerá na interface.
        # - command=self.exportar_para_excel: Associa a função `exportar_para_excel()`
        #           que será executada quando o botão for clicado, salvando os dados das tabelas no Excel.
        btn_exportar = tk.Button(self, text="Exportar", command=self.exportar_para_excel)

        # Exibe o botão na interface com um espaçamento vertical (pady=10) para melhor organização visual.
        btn_exportar.pack(pady=10)

        # Carregar os dados
        # Carrega os dados resumidos de vendas por cliente e armazena na variável `self.dados_clientes`
        # - self._carregar_resumo_vendas_por_cliente(): Função que acessa o banco de dados,
        #           agrupa as vendas por cliente e retorna uma lista com os nomes dos
        #           clientes e o total gasto por cada um.
        self.dados_clientes = self._carregar_resumo_vendas_por_cliente()

        # Carrega os dados resumidos de vendas por produto e armazena na variável `self.dados_produtos`
        # - self._carregar_resumo_vendas_por_produto(): Função que acessa o banco de dados,
        #           agrupa as vendas por produto e retorna uma lista com os nomes dos
        #           produtos e o total vendido de cada um.
        self.dados_produtos = self._carregar_resumo_vendas_por_produto()

        # Carrega os dados resumidos de vendas por vendedor e armazena na variável `self.dados_vendedores`
        # - self._carregar_resumo_vendas_por_vendedor(): Função que acessa o banco de dados,
        #           agrupa as vendas por vendedor e retorna uma lista com os nomes dos
        #           vendedores e o total de vendas realizadas por cada um.
        self.dados_vendedores = self._carregar_resumo_vendas_por_vendedor()

        # Exibe os dados carregados na Treeview correspondente a clientes
        # - self.tree_clientes: Tabela onde os dados dos clientes serão inseridos.
        # - self.dados_clientes: Lista contendo os dados de clientes que serão preenchidos na tabela.
        self._exibir(self.tree_clientes, self.dados_clientes)

        # Exibe os dados carregados na Treeview correspondente a produtos
        # - self.tree_produtos: Tabela onde os dados dos produtos serão inseridos.
        # - self.dados_produtos: Lista contendo os dados de produtos que serão preenchidos na tabela.
        self._exibir(self.tree_produtos, self.dados_produtos)

        # Exibe os dados carregados na Treeview correspondente a vendedores
        # - self.tree_vendedores: Tabela onde os dados dos vendedores serão inseridos.
        # - self.dados_vendedores: Lista contendo os dados de vendedores que serão preenchidos na tabela.
        self._exibir(self.tree_vendedores, self.dados_vendedores)

    def _criar_treeview(self, frame, colunas):

        """
        Método responsável por criar uma tabela (Treeview) dentro de um frame específico.

        Parâmetros:
        - frame: Frame onde a tabela será inserida (pode ser a aba de clientes, produtos ou vendedores).
        - colunas: Lista contendo os nomes das colunas que a tabela terá.

        Retorna:
        - Um objeto Treeview já configurado e posicionado dentro do frame.
        """

        # Cria a Treeview dentro do frame fornecido.
        # - columns=colunas: Define as colunas da tabela usando a lista de colunas recebida como parâmetro.
        # - show="headings": Exibe apenas os cabeçalhos das colunas, ocultando a coluna de índice padrão.
        tree = ttk.Treeview(frame, columns=colunas, show="headings")

        # Percorre cada nome de coluna fornecido e configura o cabeçalho e a formatação da coluna
        for c in colunas:

            # Define o texto do cabeçalho da coluna para o nome especificado
            tree.heading(c, text=c)

            # Configura a largura da coluna para 300 pixels e centraliza o conteúdo da célula
            tree.column(c, width=300, anchor="center")

        # Posiciona a tabela dentro do frame
        # - fill="both": Faz com que a tabela ocupe todo o espaço disponível no
        #           frame, tanto horizontalmente quanto verticalmente.
        # - expand=True: Permite que a tabela se expanda conforme o tamanho da janela for alterado.
        tree.pack(fill="both", expand=True)

        # Retorna a Treeview criada para ser utilizada nas abas do relatório
        return tree


    # Exporta os dados das abas (Clientes, Produtos e Vendedores) para um arquivo Excel.
    def exportar_para_excel(self):

        # Converte os dados da aba "Por Cliente" em uma lista de listas.
        # - `[list(d.values()) for d in self.dados_clientes]` percorre os dicionários de clientes,
        #   transformando os valores de cada dicionário em uma lista.
        # - Isso garante que os dados sejam organizados corretamente no formato de tabela do Excel.
        dados_clientes = [list(d.values()) for d in self.dados_clientes]

        # Converte os dados da aba "Por Produto" em uma lista de listas.
        # - Segue o mesmo processo da conversão dos clientes, aplicando a lógica aos produtos.
        dados_produtos = [list(d.values()) for d in self.dados_produtos]

        # Converte os dados da aba "Por Vendedor" em uma lista de listas.
        # - Cada entrada de vendedor será convertida em uma lista contendo seu nome e total de vendas.
        dados_vendedores = [list(d.values()) for d in self.dados_vendedores]

        # Verifica se todas as listas de dados estão vazias.
        # - `if not dados_clientes and not dados_produtos and not dados_vendedores` verifica se
        #       as três listas estão vazias.
        # - Se não houver dados para exportação, exibe um alerta para o usuário e interrompe a função.
        if not dados_clientes and not dados_produtos and not dados_vendedores:

            # Exibe um alerta informando que não há dados para exportação.
            # - `messagebox.showwarning("Aviso", "Não há dados para exportar!")` exibe um
            #       pop-up de aviso ao usuário.
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
            return

        # Cria um arquivo Excel chamado "relatorio_resumido.xlsx" e define o motor "openpyxl" para
        #       manipulação do arquivo.
        # - `with pd.ExcelWriter("relatorio_resumido.xlsx", engine="openpyxl") as writer:` abre
        #       um gerenciador de contexto
        #           que permite criar e salvar o arquivo automaticamente ao final da operação.
        with pd.ExcelWriter("relatorio_resumido.xlsx", engine="openpyxl") as writer:

            # Verifica se há dados na aba "Por Cliente" antes de escrever no Excel.
            # - `if dados_clientes:` garante que apenas abas com dados sejam criadas.
            if dados_clientes:

                # Converte a lista de clientes para um DataFrame do Pandas.
                # - `pd.DataFrame(dados_clientes, columns=["Cliente", "Total de Compras"])` cria um DataFrame
                #           com os dados e define as colunas correspondentes.
                df_clientes = pd.DataFrame(dados_clientes, columns=["Cliente", "Total de Compras"])

                # Escreve o DataFrame na aba "Por Cliente" do arquivo Excel.
                # - `df_clientes.to_excel(writer, sheet_name="Por Cliente", index=False)` salva
                #           os dados no Excel
                #           sem incluir a coluna de índices (index=False).
                df_clientes.to_excel(writer, sheet_name="Por Cliente", index=False)

            # Verifica se há dados na aba "Por Produto" antes de escrever no Excel.
            if dados_produtos:

                # Converte a lista de produtos para um DataFrame do Pandas.
                # - Cria uma tabela com os produtos vendidos e o valor total arrecadado.
                df_produtos = pd.DataFrame(dados_produtos, columns=["Produto", "Total Vendido"])

                # Escreve o DataFrame na aba "Por Produto" do arquivo Excel.
                df_produtos.to_excel(writer, sheet_name="Por Produto", index=False)

            # Verifica se há dados na aba "Por Vendedor" antes de escrever no Excel.
            if dados_vendedores:

                # Converte a lista de vendedores para um DataFrame do Pandas.
                # - Cria uma tabela com os vendedores e o total de vendas realizadas.
                df_vendedores = pd.DataFrame(dados_vendedores, columns=["Vendedor", "Total de Vendas"])

                # Escreve o DataFrame na aba "Por Vendedor" do arquivo Excel.
                df_vendedores.to_excel(writer, sheet_name="Por Vendedor", index=False)

        # Exibe uma mensagem informando que o relatório foi exportado com sucesso.
        # - `messagebox.showinfo("Sucesso", "Relatório exportado com sucesso para 'relatorio_resumido.xlsx'.")`
        #   exibe uma caixa de diálogo informando ao usuário que o arquivo foi gerado corretamente.
        messagebox.showinfo("Sucesso",
                            "Relatório exportado com sucesso para 'relatorio_resumido.xlsx'.")


    def _carregar_resumo_vendas_por_cliente(self):

        """
        Método responsável por carregar um resumo das vendas agrupadas por cliente.

        O método consulta o banco de dados para obter todas as vendas registradas,
        soma o total de compras de cada cliente e retorna uma lista formatada com os nomes
        dos clientes e o total gasto por cada um.

        Retorna:
        - Uma lista de dicionários contendo:
          * "Cliente": Nome do cliente.
          * "Total de Compras": Valor total gasto pelo cliente, formatado como moeda.
        """

        # Dicionário que armazenará os clientes e o total de compras de cada um
        resumo = {}

        # Obtém todas as vendas registradas no banco de dados
        vendas = self.db.col_vendas.find()

        # Percorre cada venda obtida do banco de dados
        for v in vendas:

            # Obtém o ID do cliente associado à venda
            cliente_id = v.get("cliente_id")

            # Define um valor padrão caso o cliente não seja encontrado
            nome_cliente = "Desconhecido"

            # Se houver um ID de cliente válido, busca o nome do cliente no banco de dados
            if cliente_id:
                cliente = self.db.col_clientes.find_one({"_id": cliente_id})

                # Se encontrar o cliente, obtém seu nome, senão mantém "Desconhecido"
                if cliente:
                    nome_cliente = cliente.get("nome", "Desconhecido")

            # Calcula o total de compras desta venda somando (quantidade * preço unitário) de cada item
            total_venda = sum(item["quantidade"] * item["preco_unitario"] for item in v["itens"])

            # Adiciona o total da venda ao cliente correspondente no dicionário `resumo`
            # - Se o cliente já existir no dicionário, soma o valor ao total existente.
            # - Se for a primeira vez que aparece, cria a entrada com o valor inicial.
            resumo[nome_cliente] = resumo.get(nome_cliente, 0) + total_venda

        # Retorna os dados formatados como uma lista de dicionários
        # - Cada entrada contém o nome do cliente e o total de compras formatado como moeda
        return [{"Cliente": k, "Total de Compras": f"R$ {v:.2f}"} for k, v in resumo.items()]


    def _carregar_resumo_vendas_por_produto(self):

        """
        Método responsável por carregar um resumo das vendas agrupadas por produto.

        O método consulta o banco de dados para obter todas as vendas registradas,
        soma o total vendido de cada produto e retorna uma lista formatada com os nomes
        dos produtos e o total arrecadado por cada um.

        Retorna:
        - Uma lista de dicionários contendo:
          * "Produto": Nome do produto vendido.
          * "Total Vendido": Valor total arrecadado com as vendas do produto, formatado como moeda.
        """

        # Dicionário que armazenará os produtos e o total vendido de cada um
        resumo = {}

        # Obtém todas as vendas registradas no banco de dados
        vendas = self.db.col_vendas.find()

        # Percorre cada venda recuperada do banco de dados
        for v in vendas:

            # Percorre todos os itens vendidos dentro da venda atual
            for item in v["itens"]:

                # Obtém o ID do produto vendido
                produto_id = item["produto_id"]

                # Define um valor padrão para o nome do produto caso ele não seja encontrado
                nome_produto = "Desconhecido"

                # Tenta buscar o nome do produto no banco de dados usando o ID do produto
                produto = self.db.col_produtos.find_one({"_id": produto_id})

                # Se encontrar o produto, obtém o nome, senão mantém "Desconhecido"
                if produto:
                    nome_produto = produto.get("nome", "Desconhecido")

                # Calcula o valor total vendido desse produto multiplicando a quantidade pelo preço unitário
                total_vendido = item["quantidade"] * item["preco_unitario"]

                # Adiciona o total vendido ao produto correspondente no dicionário `resumo`
                # - Se o produto já existir no dicionário, soma o valor ao total existente.
                # - Se for a primeira vez que aparece, cria a entrada com o valor inicial.
                resumo[nome_produto] = resumo.get(nome_produto, 0) + total_vendido

        # Retorna os dados formatados como uma lista de dicionários
        # - Cada entrada contém o nome do produto e o total vendido formatado como moeda
        return [{"Produto": k, "Total Vendido": f"R$ {v:.2f}"} for k, v in resumo.items()]


    def _carregar_resumo_vendas_por_vendedor(self):

        """
        Método responsável por carregar um resumo das vendas agrupadas por vendedor.

        O método consulta o banco de dados para obter todas as vendas registradas,
        soma o total de vendas realizadas por cada vendedor e retorna uma lista formatada
        com os nomes dos vendedores e o total vendido por cada um.

        Retorna:
        - Uma lista de dicionários contendo:
          * "Vendedor": Nome do vendedor.
          * "Total de Vendas": Valor total das vendas realizadas pelo vendedor, formatado como moeda.
        """

        # Dicionário que armazenará os vendedores e o total de vendas de cada um
        resumo = {}

        # Obtém todas as vendas registradas no banco de dados
        vendas = self.db.col_vendas.find()

        # Percorre cada venda obtida do banco de dados
        for v in vendas:

            # Obtém o ID do vendedor responsável pela venda
            vendedor_id = v.get("vendedor_id")

            # Define um valor padrão caso o vendedor não seja encontrado
            nome_vendedor = "Desconhecido"

            # Se houver um ID de vendedor válido, busca o nome do vendedor no banco de dados
            if vendedor_id:
                vendedor = self.db.col_usuarios.find_one({"_id": vendedor_id})

                # Se encontrar o vendedor, obtém seu nome, senão mantém "Desconhecido"
                if vendedor:
                    nome_vendedor = vendedor.get("nome", "Desconhecido")

            # Calcula o total de vendas dessa venda específica
            # Somando (quantidade * preço unitário) de cada item vendido
            total_venda = sum(item["quantidade"] * item["preco_unitario"] for item in v["itens"])

            # Adiciona o total de vendas ao vendedor correspondente no dicionário `resumo`
            # - Se o vendedor já existir no dicionário, soma o valor ao total existente.
            # - Se for a primeira vez que aparece, cria a entrada com o valor inicial.
            resumo[nome_vendedor] = resumo.get(nome_vendedor, 0) + total_venda

        # Retorna os dados formatados como uma lista de dicionários
        # - Cada entrada contém o nome do vendedor e o total de vendas formatado como moeda
        return [{"Vendedor": k, "Total de Vendas": f"R$ {v:.2f}"} for k, v in resumo.items()]


    def _exibir(self, tree, dados):

        """
        Método responsável por exibir os dados na Treeview.

        Este método primeiro limpa todos os itens atualmente exibidos na Treeview
        e, em seguida, insere os novos dados recebidos como parâmetro.

        Parâmetros:
        - tree: O widget Treeview onde os dados serão exibidos.
        - dados: Lista de dicionários contendo os dados que serão inseridos na Treeview.

        Retorno:
        - Nenhum (os dados são diretamente inseridos na Treeview).
        """

        # Remove todos os itens atualmente exibidos na Treeview.
        # - tree.get_children() retorna todos os itens presentes na Treeview.
        # - tree.delete(i) remove cada item individualmente.
        for i in tree.get_children():
            tree.delete(i)

        # Percorre a lista de dados e insere cada entrada na Treeview.
        for d in dados:

            # Insere um novo item no final da Treeview ("end").
            # - values=list(d.values()): Insere os valores do dicionário `d`
            #   convertidos em uma lista para preencher as colunas da Treeview.
            tree.insert("", "end", values=list(d.values()))



###############################################################################
# JANELA DE RELATÓRIO COMPLETO (MOSTRANDO TODOS OS ITENS DE VENDA)
###############################################################################
class JanelaRelatorioCompleto(tk.Toplevel):

    """
    Classe responsável por exibir um relatório detalhado de todas as vendas.

    O relatório exibe informações como Data, Cliente, Produto, Quantidade,
    Forma de Pagamento e Subtotal. Além disso, permite aplicar filtros e
    soma automaticamente quantidades e valores.

    As datas são exibidas no formato dd/mm/aaaa para melhor compreensão.
    """

    def __init__(self, pai, db: GerenciadorBanco):

        # Inicializa a classe `Toplevel`, criando uma nova
        #       janela modal sobre a janela principal.
        # `super().__init__(pai)` faz com que a janela dependa da
        #       janela `pai` (janela principal).
        super().__init__(pai)

        # Define o título da janela para "Relatório Completo de Vendas".
        # Esse título aparece na barra superior da janela.
        self.title("Relatório Completo de Vendas")

        # Armazena a referência ao banco de dados `db` para buscar as
        #       informações do relatório.
        self.db = db

        # Define o tamanho da janela como 900 pixels de largura
        #       por 500 pixels de altura.
        self.geometry("1150x500")

        # Define a janela como transitória em relação à janela principal.
        # Isso faz com que a nova janela sempre fique em primeiro
        #       plano e relacionada à janela `pai`.
        self.transient(pai)

        # Impede que o usuário interaja com a janela principal
        #       enquanto esta estiver aberta.
        # `grab_set()` captura os eventos do mouse e teclado para
        #       esta janela, desativando a interação com a principal.
        self.grab_set()

        # Centraliza a janela na tela do usuário.
        # `centralizar_janela(self)` ajusta a posição da janela
        #       para que fique centralizada.
        centralizar_janela(self)

        # Cria um quadro (`Frame`) para conter os filtros de busca no relatório.
        # `tk.Frame(self)` cria um contêiner dentro da janela do relatório.
        # Esse quadro ajudará a organizar os filtros visualmente.
        quadro_filtros = tk.Frame(self)

        # Exibe o quadro na interface.
        # `.pack(fill="x", pady=5)` faz com que o quadro ocupe toda a
        #       largura da janela (fill="x").
        # `pady=5` adiciona um espaçamento vertical de 5 pixels
        #       para separação dos elementos.
        quadro_filtros.pack(fill="x", pady=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada da Data Inicial.
        # `text="Data Inicial (dd/mm/aaaa):"` define o texto exibido no rótulo.
        # `.grid(row=0, column=0, padx=5)` posiciona o rótulo na
        #       primeira linha (row=0) e primeira coluna (column=0).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       para melhorar a organização visual.
        tk.Label(quadro_filtros,
                 text="Data Inicial (dd/mm/aaaa):").grid(row=0, column=0, padx=5)

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa digitar a data inicial do filtro.
        # `tk.Entry(quadro_filtros, width=10)` cria um campo de
        #       texto dentro do `quadro_filtros`.
        # `width=10` define a largura do campo, permitindo a
        #       digitação do formato "dd/mm/aaaa".
        self.ent_data_ini = tk.Entry(quadro_filtros, width=10)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=1, padx=5)` coloca o campo na mesma
        #       linha do rótulo, mas na segunda coluna (column=1).
        # `padx=5` adiciona espaçamento horizontal para
        #       separar o rótulo do campo de entrada.
        self.ent_data_ini.grid(row=0, column=1, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada da Data Final.
        # `text="Data Final:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=2, padx=5)` posiciona o rótulo na
        #       primeira linha (row=0) e terceira coluna (column=2).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       para melhorar a organização visual.
        tk.Label(quadro_filtros, text="Data Final:").grid(row=0, column=2, padx=5)

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa digitar a data final do filtro.
        # `tk.Entry(quadro_filtros, width=10)` cria um campo de
        #       texto dentro do `quadro_filtros`.
        # `width=10` define a largura do campo, permitindo a
        #       digitação do formato "dd/mm/aaaa".
        self.ent_data_fim = tk.Entry(quadro_filtros, width=10)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=3, padx=5)` coloca o campo na mesma
        #       linha do rótulo, mas na quarta coluna (column=3).
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       rótulo do campo de entrada.
        self.ent_data_fim.grid(row=0, column=3, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada do Cliente.
        # `text="Cliente:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=4, padx=5)` posiciona o rótulo na primeira
        #       linha (row=0) e quinta coluna (column=4).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       para melhorar a organização visual.
        tk.Label(quadro_filtros,
                 text="Cliente:").grid(row=0, column=4, padx=5)

        # Cria um campo de entrada (`Entry`) para que o usuário
        #       possa digitar o nome do cliente para filtrar os resultados.
        # `tk.Entry(quadro_filtros, width=15)` cria um campo de
        #       texto dentro do `quadro_filtros`.
        # `width=15` define a largura do campo, permitindo a
        #       entrada de um nome razoavelmente longo.
        self.ent_cliente = tk.Entry(quadro_filtros, width=15)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=5, padx=5)` coloca o campo na mesma
        #       linha do rótulo, mas na sexta coluna (column=5).
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       rótulo do campo de entrada.
        self.ent_cliente.grid(row=0, column=5, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada do Produto.
        # `text="Produto:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=6, padx=5)` posiciona o rótulo na
        #       primeira linha (row=0) e sétima coluna (column=6).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       para melhorar a organização visual.
        tk.Label(quadro_filtros,
                 text="Produto:").grid(row=0, column=6, padx=5)

        # Cria um campo de entrada (`Entry`) para que o usuário possa
        #       digitar o nome do produto para filtrar os resultados.
        # `tk.Entry(quadro_filtros, width=15)` cria um campo de
        #       texto dentro do `quadro_filtros`.
        # `width=15` define a largura do campo, permitindo a
        #       entrada de um nome de produto.
        self.ent_produto = tk.Entry(quadro_filtros, width=15)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=7, padx=5)` coloca o campo na mesma
        #       linha do rótulo, mas na oitava coluna (column=7).
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       rótulo do campo de entrada.
        self.ent_produto.grid(row=0, column=7, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada da Forma de Pagamento.
        # `text="Forma:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=8, padx=5)` posiciona o rótulo na primeira
        #       linha (row=0) e nona coluna (column=8).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para
        #       melhorar a organização visual.
        tk.Label(quadro_filtros, text="Forma:").grid(row=0, column=8, padx=5)

        # Cria um campo de entrada (`Entry`) para que o usuário possa digitar a
        #       forma de pagamento desejada para filtrar os resultados.
        # `tk.Entry(quadro_filtros, width=10)` cria um campo de texto dentro do `quadro_filtros`.
        # `width=10` define a largura do campo, permitindo a entrada de uma
        #       forma de pagamento como "PIX", "Crédito", "Débito" etc.
        self.ent_forma = tk.Entry(quadro_filtros, width=10)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=9, padx=5)` coloca o campo na mesma linha do
        #       rótulo, mas na décima coluna (column=9).
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       rótulo do campo de entrada.
        self.ent_forma.grid(row=0, column=9, padx=5)

        # Cria um rótulo (`Label`) para indicar o campo de entrada do Subtotal.
        # `text="Subtotal:"` define o texto exibido no rótulo.
        # `.grid(row=0, column=10, padx=5)` posiciona o rótulo na primeira
        #       linha (row=0) e décima primeira coluna (column=10).
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels para
        #       melhorar a organização visual.
        tk.Label(quadro_filtros,
                 text="Subtotal:").grid(row=0, column=10, padx=5)

        # Cria um campo de entrada (`Entry`) para que o usuário possa
        #       digitar um valor de subtotal para filtrar os resultados.
        # `tk.Entry(quadro_filtros, width=10)` cria um campo de texto
        #       dentro do `quadro_filtros`.
        # `width=10` define a largura do campo, permitindo a entrada de
        #       valores numéricos como "100.00" ou "500.75".
        self.ent_subt = tk.Entry(quadro_filtros, width=10)

        # Posiciona o campo de entrada ao lado do rótulo correspondente.
        # `.grid(row=0, column=11, padx=5)` coloca o campo na mesma linha do
        #       rótulo, mas na décima segunda coluna (column=11).
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       rótulo do campo de entrada.
        self.ent_subt.grid(row=0, column=11, padx=5)

        # Cria um botão (`Button`) para executar a filtragem dos dados com
        #       base nos critérios informados nos campos.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a ação de chamar a função `self.filtrar`
        #       quando o botão for clicado.
        # `.grid(row=0, column=12, padx=5)` posiciona o botão na primeira
        #       linha (row=0) e décima terceira coluna (column=12).
        # `padx=5` adiciona espaçamento horizontal para separar o
        #       botão dos demais campos.
        tk.Button(quadro_filtros,
                  text="Filtrar",
                  command=self.filtrar).grid(row=0, column=12, padx=5)

        # Define as colunas que serão exibidas na tabela de resultados.
        # A tupla contém os nomes das colunas.
        colunas = ("Data", "Cliente", "Produto", "Quantidade", "Forma", "Subtotal")

        # Cria uma `Treeview` para exibir os dados filtrados em formato de tabela.
        # `self` define que a tabela pertence à classe atual.
        # `columns=colunas` define as colunas que serão exibidas na tabela.
        # `show="headings"` faz com que apenas os cabeçalhos das colunas
        #       sejam exibidos, sem a primeira coluna oculta de índice.
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")

        # Percorre cada coluna definida na tupla `colunas`.
        for c in colunas:

            # Define o nome do cabeçalho de cada coluna da tabela (`Treeview`).
            # `self.tree.heading(c, text=c)` associa o nome da coluna `c` ao
            #       texto do cabeçalho exibido na interface.
            self.tree.heading(c, text=c)

            # Define a largura de cada coluna para melhorar a visualização dos dados.
            # `.column(c, width=130)` ajusta a largura de cada coluna para 130 pixels.
            self.tree.column(c, width=130)

        # Exibe a tabela (`Treeview`) na interface.
        # `.pack(fill="both", expand=True)` faz com que a tabela ocupe
        #       todo o espaço disponível na interface.
        # `fill="both"` permite que a tabela expanda tanto horizontalmente
        #       quanto verticalmente.
        # `expand=True` permite que a tabela ajuste seu tamanho
        #       automaticamente ao redimensionar a janela.
        self.tree.pack(fill="both", expand=True)

        # Cria um frame (`Frame`) para exibir o resumo dos dados filtrados.
        # `self` indica que este quadro pertence à classe atual.
        # `tk.Frame(self)` cria um contêiner dentro da interface
        #       principal para organizar os elementos do resumo.
        quadro_resumo = tk.Frame(self)

        # Posiciona o quadro do resumo na interface.
        # `.pack(fill="x", pady=5)` faz com que o quadro ocupe
        #       toda a largura da janela (`fill="x"`).
        # `pady=5` adiciona um espaçamento vertical de 5 pixels entre
        #       este quadro e os elementos acima dele.
        quadro_resumo.pack(fill="x", pady=5)

        # Cria um rótulo (`Label`) para indicar a quantidade total de itens no relatório.
        # `text="Qtd. Total de Itens:"` define o texto exibido no rótulo.
        # `.pack(side="left", padx=5)` alinha o rótulo à esquerda dentro do `quadro_resumo`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre este rótulo e os demais elementos.
        tk.Label(quadro_resumo,
                 text="Qtd. Total de Itens:").pack(side="left", padx=5)

        # Cria um rótulo (`Label`) que exibirá dinamicamente a
        #       quantidade total de itens calculada.
        # `text="0"` define o valor inicial do rótulo como 0.
        self.lbl_qtd_itens = tk.Label(quadro_resumo, text="0")

        # Posiciona o rótulo da quantidade total de itens ao lado do texto descritivo.
        # `.pack(side="left", padx=5)` alinha o rótulo à esquerda
        #       dentro do `quadro_resumo`, com um espaçamento horizontal de 5 pixels.
        self.lbl_qtd_itens.pack(side="left", padx=5)

        # Cria um rótulo (`Label`) para exibir o separador visual e
        #       indicar o campo de valor arrecadado.
        # `text=" | Valor Arrecadado:"` adiciona um separador (`|`) seguido do texto descritivo.
        # `.pack(side="left", padx=5)` alinha o rótulo à esquerda dentro do `quadro_resumo`.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels
        #       entre este rótulo e os demais elementos.
        tk.Label(quadro_resumo,
                 text=" | Valor Arrecadado:").pack(side="left", padx=5)

        # Cria um rótulo (`Label`) que exibirá dinamicamente o
        #       valor total arrecadado no relatório.
        # `text="R$ 0,00"` define o valor inicial do rótulo como "R$ 0,00".
        self.lbl_valor_arrec = tk.Label(quadro_resumo, text="R$ 0,00")

        # Posiciona o rótulo do valor arrecadado ao lado do texto descritivo.
        # `.pack(side="left", padx=5)` alinha o rótulo à esquerda
        #       dentro do `quadro_resumo`, com um espaçamento horizontal de 5 pixels.
        self.lbl_valor_arrec.pack(side="left", padx=5)

        # Carrega todos os itens de vendas do banco de dados ao
        #       abrir a janela do relatório.
        # `self._carregar_todos_itens()` é um método que busca todos os
        #       registros relevantes para exibição.
        # Os dados retornados são armazenados na variável `self.dados`
        #       para serem utilizados posteriormente.
        self.dados = self._carregar_todos_itens()

        # Exibe os dados carregados na interface da tabela (`Treeview`).
        # `self._exibir(self.dados)` chama o método `_exibir()`,
        #       que insere os dados na tabela.
        self._exibir(self.dados)



    def _carregar_todos_itens(self):

        # Define uma lista vazia `lista` para armazenar os itens
        #       das vendas que serão carregados.
        lista = []

        # Obtém todas as vendas armazenadas no banco de dados.
        # `self.db.col_vendas.find()` retorna todos os registros da coleção de vendas.
        vendas = self.db.col_vendas.find()

        # Percorre cada venda retornada na consulta.
        for v in vendas:

            # Converte a data/hora da venda do formato ISO para um
            #       objeto de data (`datetime`).
            # `converter_iso_para_date(v["data_hora"])` transforma a
            #       string de data ISO em um objeto `datetime`.
            data_obj = converter_iso_para_date(v["data_hora"])

            # Converte a data do formato `datetime` para uma string no
            #       formato brasileiro (dd/mm/aaaa).
            # `converter_date_para_str_br(data_obj)` retorna uma
            #       string formatada no padrão brasileiro.
            data_br = converter_date_para_str_br(data_obj)

            # Obtém a forma de pagamento utilizada na venda.
            forma = v["forma_pagamento"]

            # Inicializa a variável `nome_cliente` como uma string vazia,
            #       caso o cliente não esteja registrado.
            nome_cliente = ""

            # Verifica se há um cliente associado à venda.
            # `v.get("cliente_id")` verifica se a chave `cliente_id`
            #       existe no dicionário `v`.
            if v.get("cliente_id"):

                # Se houver um cliente associado, busca as informações do
                #       cliente no banco de dados.
                # `self.db.col_clientes.find_one({"_id": v["cliente_id"]})` retorna o
                #       documento do cliente correspondente.
                doc_c = self.db.col_clientes.find_one({"_id": v["cliente_id"]})

                # Se o cliente for encontrado, armazena o nome do
                #       cliente na variável `nome_cliente`.
                if doc_c:
                    nome_cliente = doc_c["nome"]

            # Percorre todos os itens vendidos dentro da venda `v`.
            for item in v["itens"]:

                # Busca o produto no banco de dados utilizando o
                #       ID armazenado em `item["produto_id"]`.
                # `find_one({"_id": item["produto_id"]})` retorna o
                #       documento do produto correspondente.
                doc_p = self.db.col_produtos.find_one({"_id": item["produto_id"]})

                # Se o produto for encontrado, obtém o nome do produto.
                # Caso contrário, define "Desconhecido" como nome do produto.
                nome_prod = doc_p["nome"] if doc_p else "Desconhecido"

                # Obtém a quantidade de unidades vendidas do produto.
                quant = item["quantidade"]

                # Calcula o subtotal multiplicando a quantidade
                #       pelo preço unitário do produto.
                subt = quant * item["preco_unitario"]

                # Adiciona os dados do item de venda na lista `lista` como um dicionário.
                lista.append({
                    "data_obj": data_obj,  # Data como objeto datetime, para filtragem posterior.
                    "data_br": data_br,  # Data formatada no padrão brasileiro (dd/mm/aaaa).
                    "cliente": nome_cliente,  # Nome do cliente que realizou a compra.
                    "produto": nome_prod,  # Nome do produto vendido.
                    "quantidade": quant,  # Quantidade de unidades vendidas.
                    "forma": forma,  # Forma de pagamento utilizada na venda.
                    "subt_str": f"{subt:.2f}",  # Subtotal formatado como string com duas casas decimais.
                    "subt_val": subt  # Subtotal em formato numérico para cálculos e somatórios.
                })

        # Retorna a lista contendo todos os itens das vendas processadas.
        return lista


    def _exibir(self, dados):

        # Remove todos os itens atualmente exibidos na tabela (`Treeview`).
        # `.get_children()` retorna todos os elementos da
        #       tabela, e `.delete(i)` remove cada um deles.
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Inicializa as variáveis para armazenar os totais de
        #       quantidade e valor arrecadado.
        # Contador para a quantidade total de itens vendidos.
        soma_qtd = 0

        # Contador para o valor total arrecadado.
        soma_valor = 0.0

        # Percorre todos os dados passados como argumento (`dados`).
        for d in dados:

            # Insere um novo item na tabela (`Treeview`).
            # `"end"` adiciona o item ao final da lista.
            # `values=(...)` define os valores que serão
            #       exibidos em cada coluna da tabela.
            self.tree.insert("",
                        "end",
                        values=(
                            d["data_br"],  # Data formatada no padrão brasileiro (dd/mm/aaaa).
                            d["cliente"],  # Nome do cliente que realizou a compra.
                            d["produto"],  # Nome do produto vendido.
                            d["quantidade"],  # Quantidade de unidades vendidas.
                            d["forma"],  # Forma de pagamento utilizada na venda.
                            d["subt_str"]))  # Subtotal da venda formatado como string (ex.: "12.50").


            # Atualiza o total de itens vendidos somando a quantidade do item atual.
            soma_qtd += d["quantidade"]

            # Atualiza o total de valor arrecadado somando o subtotal do item atual.
            soma_valor += d["subt_val"]

        # Atualiza a interface gráfica com a quantidade total de itens vendidos.
        # `self.lbl_qtd_itens.config(text=str(soma_qtd))` altera o texto
        #       do rótulo para exibir o valor atualizado.
        self.lbl_qtd_itens.config(text=str(soma_qtd))

        # Atualiza a interface gráfica com o valor total arrecadado.
        # `f"R$ {soma_valor:.2f}"` formata o valor como moeda
        #       brasileira, com duas casas decimais.
        self.lbl_valor_arrec.config(text=f"R$ {soma_valor:.2f}")


    def filtrar(self):

        """
        Filtra os dados exibidos na tabela com base nos valores
                inseridos nos campos de filtro.
        Os filtros incluem data inicial, data final, cliente,
                produto, forma de pagamento e subtotal.
        """

        # Converte a data inicial inserida no campo para um objeto de
        #       data no formato correto.
        # `analisar_data_br(self.ent_data_ini.get())` analisa a string
        #       de data e retorna um objeto `datetime`.
        # Caso o campo esteja vazio ou a conversão falhe, `dt_ini` será `None`.
        dt_ini = analisar_data_br(self.ent_data_ini.get())

        # Converte a data final inserida no campo para um objeto de data no formato correto.
        # `analisar_data_br(self.ent_data_fim.get())` funciona da mesma forma que `dt_ini`.
        dt_fim = analisar_data_br(self.ent_data_fim.get())

        # Obtém o valor do campo de cliente, convertendo para
        #       minúsculas e removendo espaços extras.
        # Isso garante que a filtragem seja insensível a
        #       maiúsculas/minúsculas e a espaços adicionais.
        cliente_f = self.ent_cliente.get().lower().strip()

        # Obtém o valor do campo de produto, aplicando as mesmas
        #       regras de limpeza e padronização.
        produto_f = self.ent_produto.get().lower().strip()

        # Obtém o valor do campo de forma de pagamento, garantindo a
        #       padronização para a filtragem.
        forma_f = self.ent_forma.get().lower().strip()

        # Obtém o valor do campo de subtotal e remove espaços
        #       adicionais para facilitar a busca.
        subt_f = self.ent_subt.get().lower().strip()

        # Inicializa uma lista vazia para armazenar os itens que
        #       correspondem aos critérios do filtro.
        filtrados = []

        # Percorre todos os itens da lista `self.dados`
        #       para aplicar os filtros.
        for d in self.dados:

            # ----------------------------- Comparação de Datas -----------------------------
            # Se `dt_ini` não for `None` e a data do item (`d["data_obj"]`) for
            #       menor que `dt_ini`, o item é ignorado.
            if dt_ini and d["data_obj"] and d["data_obj"] < dt_ini:
                continue  # Pula para o próximo item da lista.

            # Se `dt_fim` não for `None` e a data do item (`d["data_obj"]`) for
            #       maior que `dt_fim`, o item é ignorado.
            if dt_fim and d["data_obj"] and d["data_obj"] > dt_fim:
                continue  # Pula para o próximo item da lista.

            # ----------------------------- Comparação de Cliente -----------------------------
            # Se um filtro de cliente foi informado (`cliente_f` não
            #       está vazio) e o nome do cliente no item
            #       não contém a string filtrada, o item é ignorado.
            if cliente_f and cliente_f not in d["cliente"].lower():
                continue  # Pula para o próximo item da lista.

            # ----------------------------- Comparação de Produto -----------------------------
            # Se um filtro de produto foi informado (`produto_f` não
            #       está vazio) e o nome do produto no item
            #       não contém a string filtrada, o item é ignorado.
            if produto_f and produto_f not in d["produto"].lower():
                continue  # Pula para o próximo item da lista.

            # ----------------------------- Comparação de Forma de Pagamento -----------------------------
            # Se um filtro de forma de pagamento foi informado (`forma_f` não
            #       está vazio) e a forma de pagamento
            #       no item não contém a string filtrada, o item é ignorado.
            if forma_f and forma_f not in d["forma"].lower():
                continue  # Pula para o próximo item da lista.

            # ----------------------------- Comparação de Subtotal -----------------------------
            # Se um filtro de subtotal foi informado (`subt_f` não
            #       está vazio) e o subtotal do item
            #       não contém a string filtrada, o item é ignorado.
            if subt_f and subt_f not in d["subt_str"].lower():
                continue  # Pula para o próximo item da lista.

            # Se o item passou por todos os filtros, ele é
            #       adicionado à lista `filtrados`.
            filtrados.append(d)

        # Chama a função `_exibir()` para atualizar a tabela na
        #       interface com os itens filtrados.
        self._exibir(filtrados)


###############################################################################
# EXECUÇÃO
###############################################################################

# Cria uma instância da classe `Aplicacao`, que representa a
#       interface gráfica do programa.
# Essa instância inicializa todos os elementos e
#       funcionalidades da aplicação.
app = Aplicacao()

# Inicia o loop principal da interface gráfica (`mainloop()`).
# Esse método mantém a aplicação em execução, processando eventos do
#       usuário até que a janela seja fechada.
app.mainloop()