# Importa o módulo tkinter com o apelido "tk" para criar interfaces gráficas
import tkinter as tk

# Importa widgets adicionais de tkinter, como caixas de texto,
#       mensagens e seletores de arquivos
from tkinter import ttk, messagebox, filedialog

# Importa especificamente a função `asksaveasfilename` do tkinter para salvar arquivos
from tkinter.filedialog import asksaveasfilename

from PIL.ImageOps import expand
from pandas import date_range
# Importa o módulo tkcalendar para criar seletores de data e calendários
from tkcalendar import Calendar, DateEntry

# Importa o módulo datetime para manipulação de datas e horas
from datetime import datetime, timedelta

# Importa a biblioteca pymongo para trabalhar com bancos de dados MongoDB
from pymongo import MongoClient

# Importa a classe ObjectId, que é usada no MongoDB para
#       identificar documentos de forma única
from bson import ObjectId

# Importa a biblioteca pandas para trabalhar com dados tabulares, como planilhas
import pandas as pd
from xlsxwriter.utility import quote_sheetname

###############################################################################
#                             LÓGICA DE NEGÓCIO                               #
###############################################################################

"""
    Classe principal que gerencia a lógica e operações do sistema.
    Esta classe centraliza a conexão com o banco de dados 
            MongoDB e fornece métodos para 
    interagir com diferentes coleções e funcionalidades, 
            como reservas de quadras e controle de estoque.
"""
class ReservaQuadra:

    """
        Método inicializador da classe, chamado automaticamente ao criar uma instância.
        Este método é usado para configurar a conexão com o banco de dados MongoDB e
        definir a coleção principal que será usada no sistema.
     """
    def __init__(self):

        # Estabelece a conexão com o servidor MongoDB local.
        # "MongoClient" é uma classe fornecida pelo pymongo que gerencia a
        #       comunicação com o servidor MongoDB.
        # O endereço "mongodb://localhost:27017/" indica que o MongoDB
        #       está rodando localmente (no mesmo computador)
        #       na porta padrão 27017.
        self.conexao = MongoClient("mongodb://localhost:27017/")

        # Define o banco de dados que será usado dentro do MongoDB.
        # Neste caso, "sistema_completo_db" é o nome do banco de dados
        #       onde todos os dados do sistema serão armazenados.
        # Se o banco não existir, ele será criado automaticamente ao inserir dados.
        self.banco = self.conexao["sistema_completo_db"]

        # Define as coleções que serão usadas no banco de dados.
        # No MongoDB, coleções são como "tabelas" em bancos de
        #       dados relacionais, mas são mais flexíveis.
        # Cada coleção pode armazenar documentos que representam dados específicos.

        # Coleção para armazenar informações de reservas.
        # Isso incluirá dados como horários, quadras reservadas,
        #       clientes associados, entre outros.
        self.colecao_reservas = self.banco["reservas"]

        # Coleção específica para armazenar informações sobre fornecedores.
        # Aqui podem ser armazenados dados como o nome do fornecedor,
        #       produtos fornecidos, contatos, etc.
        self.colecao_fornecedores = self.banco["fornecedores"]

        # Coleção dedicada para armazenar informações dos clientes.
        # Os dados podem incluir nome, contato, histórico de reservas ou
        #       qualquer outro dado relevante do cliente.
        self.colecao_clientes = self.banco["clientes"]

        # Coleção para armazenar os dados dos produtos.
        # Isso pode incluir itens relacionados ao uso das quadras, como
        #       bolas, redes, uniformes, etc.
        # Cada documento aqui pode conter informações sobre o nome do produto,
        #       quantidade em estoque, preço, etc.
        self.colecao_produtos = self.banco["produtos"]

        # Coleção para armazenar informações sobre os lugares ou quadras.
        # Cada documento pode representar um lugar/quadra específico e
        #       pode conter informações como: nome ou número da quadra,
        #                                      localização, tipo de quadra (grama, areia, etc.),
        #                                      disponibilidade, entre outros.
        self.colecao_lugares = self.banco["lugares"]


    """
            Retorna todas as reservas que correspondem ao filtro especificado.
            Se nenhum filtro for fornecido, retorna todas as reservas cadastradas.
        """

    """
            Define uma função que calcula o valor total de uma reserva.

            Parâmetros:
            - self: refere-se à instância da classe, permitindo acessar 
                    atributos e outros métodos.
            - lugar_id: o identificador único (ID) do lugar que está sendo reservado,
                    geralmente armazenado no banco de dados.
            - hora_inicial: string representando a hora de início da reserva no formato "HH:MM".
            - hora_final: string representando a hora de término da reserva no formato "HH:MM".

            Retorna:
            - O valor total da reserva, calculado com base na duração e 
                    no custo por hora do lugar.
        """

    def calcular_valor_reserva(self, lugar_id, hora_inicial, hora_final):

        # Busca no banco de dados os detalhes do lugar correspondente ao
        #       ID fornecido (como valor por hora).
        lugar = self.colecao_lugares.find_one({"_id": ObjectId(lugar_id)})

        # Verifica se o lugar foi encontrado no banco de dados. Caso
        #       contrário, retorna 0.0 como valor padrão.
        if not lugar:
            return 0.0

        # Obtém o valor por hora do lugar a partir do campo "valor_hora".
        # Caso não exista, utiliza 0.0 como padrão.
        valor_hora = lugar.get("valor_hora", 0.0)

        # Valida se as horas fornecidas (hora_inicial e hora_final)
        #       estão no formato correto (HH:MM).
        try:

            # Divide a string da hora inicial em horas e minutos,
            #       convertendo-os para inteiros.
            hi_h, hi_m = map(int, hora_inicial.split(":"))

            # Divide a string da hora final em horas e minutos,
            #       convertendo-os para inteiros.
            hf_h, hf_m = map(int, hora_final.split(":"))

        except ValueError:

            # Lança um erro se as horas não estiverem no formato correto.
            raise ValueError("Formato de hora inválido. Use HH:MM.")

        # Calcula o total de minutos da hora inicial.
        # Multiplica as horas por 60 para converter para minutos e
        #       soma com os minutos fornecidos (hi_m).
        minutos_inicial = hi_h * 60 + hi_m

        # Calcula o total de minutos da hora final.
        # Multiplica as horas por 60 para converter para minutos e
        #       soma com os minutos fornecidos (hf_m).
        minutos_final = hf_h * 60 + hf_m

        # Subtrai os minutos da hora inicial dos minutos da hora final
        #       para obter a duração total em minutos.
        minutos = minutos_final - minutos_inicial

        # Verifica se o resultado dos minutos é negativo.
        # Isso indica que a hora final é anterior à hora inicial, o
        #       que é uma situação inválida para reservas.
        if minutos < 0:

            # Gera um erro explicando que a hora final deve ser maior que a hora inicial.
            raise ValueError("Hora final deve ser maior que a hora inicial.")

        # Converte o total de minutos em horas para o cálculo do
        #       valor da reserva.
        # Divide os minutos totais por 60 para obter a quantidade
        #       exata de horas como um número decimal.
        horas = minutos / 60.0

        # Calcula o valor total da reserva.
        # Multiplica a quantidade de horas calculadas pelo valor
        #       por hora do lugar (valor_hora).
        return horas * valor_hora


    def buscar_reservas(self, filtro=None):

            # Verifica se o parâmetro 'filtro' é None (não foi fornecido).
            if filtro is None:

                # Caso não tenha filtro, cria um dicionário vazio
                #       para buscar todas as reservas.
                filtro = {}

            # Realiza a consulta no banco de dados MongoDB na coleção 'reservas'.
            # O método `find(filtro)` retorna um cursor com os
            #       documentos que correspondem ao filtro.
            # O uso de `list()` converte o cursor para uma lista Python
            #       com os resultados da consulta.
            return list(self.colecao_reservas.find(filtro))


    """
            Verifica se há conflito de horário de reserva para um determinado lugar e data.
            Retorna True se houver conflito, ou False caso contrário.
        """

    def verificar_conflito(self, lugar_id, data_reserva, hora_inicial, hora_final):

        # Busca no banco de dados todas as reservas existentes
        #       para o lugar e a data fornecidos.
        # `lugar_id` é convertido para ObjectId porque, no MongoDB, IDs
        #       são armazenados como ObjectId.
        # `data_reserva` filtra apenas as reservas feitas para
        #       aquela data específica.
        reservas_dia = self.colecao_reservas.find({

            # ID do lugar (quadra ou espaço) que será verificado.
            "lugar_id": ObjectId(lugar_id),

            # Data específica da reserva que estamos verificando.
            "data": data_reserva

        })

        # Itera sobre todas as reservas encontradas para o
        #       lugar e a data fornecidos.
        for reserva_existente in reservas_dia:

            # Recupera o horário inicial (hi) e o horário final (hf) da reserva já existente.
            hi = reserva_existente["hora_inicial"]  # Hora inicial da reserva já cadastrada.
            hf = reserva_existente["hora_final"]  # Hora final da reserva já cadastrada.

            # Verifica se há sobreposição de horários entre a reserva
            #       existente e a nova reserva.
            # Condição de conflito:
            # - Se a hora inicial da nova reserva (hora_inicial) for menor que a
            #       hora final da reserva existente (hf),
            #   E a hora final da nova reserva (hora_final) for maior que a hora
            #       inicial da reserva existente (hi).
            if hora_inicial < hf and hora_final > hi:

                # Conflito encontrado, retorna True imediatamente.
                return True

        # Se nenhuma sobreposição de horário for encontrada, retorna False.
        return False


    def abater_estoque_itens(self, itens_consumidos):

        # Itera sobre a lista de itens consumidos para processar cada produto.
        for item in itens_consumidos:

            # Obtém o ID do produto a partir do item consumido.
            prod_id = item.get("produto_id")

            # Obtém a quantidade consumida do item. Se não
            #       especificado, usa o valor padrão 0.
            qtd_consumida = item.get("qtd", 0)

            # Se o ID do produto não estiver presente no item,
            #       pula para o próximo item da lista.
            if not prod_id:
                continue

            # Busca o produto no banco de dados com base no ID do produto.
            produto_bd = self.colecao_produtos.find_one({"_id": ObjectId(prod_id)})

            # Verifica se o produto correspondente ao ID fornecido foi
            #       encontrado no banco de dados.
            # Isso garante que o sistema está tentando processar
            #       apenas produtos válidos.
            if not produto_bd:

                # Caso o produto não seja encontrado, o sistema lança uma
                #       exceção informando o ID do produto ausente.
                # Isso é importante para alertar o operador ou desenvolvedor
                #       sobre inconsistências no banco de dados.
                raise ValueError(f"Produto ID {prod_id} não encontrado.")

            # Verifica se o estoque atual do produto é menor do que a
            #       quantidade consumida especificada.
            # Essa validação é crucial para evitar que o sistema permita a
            #       reserva de itens além da capacidade disponível.
            if produto_bd["estoque"] < qtd_consumida:

                # Se o estoque for insuficiente, o sistema lança uma exceção do tipo ValueError.
                # A mensagem da exceção inclui o nome do produto e os valores relevantes:
                # - estoque atual (produto_bd["estoque"])
                # - quantidade que se tentou consumir (qtd_consumida)
                # Isso fornece informações detalhadas e claras para
                #       identificar rapidamente o problema.
                raise ValueError(
                    f"Estoque insuficiente para '{produto_bd['nome']}' "
                    f"(estoque={produto_bd['estoque']}, qtd={qtd_consumida})."
                )

        # Se todos os itens passarem nas validações anteriores (existência
        #       no banco e estoque suficiente),
        #       realiza o abate do estoque para cada produto consumido.
        for item in itens_consumidos:

            # Obtém o ID do produto consumido. O campo "produto_id" deve
            #       estar presente no item consumido.
            prod_id = item["produto_id"]

            # Obtém a quantidade consumida do item, indicada no dicionário do item.
            qtd_consumida = item["qtd"]

            # Atualiza o estoque do produto no banco de dados, utilizando a
            #       operação "$inc" do MongoDB.
            # A operação "$inc" decrementa o estoque do produto pelo valor
            #       especificado em "-qtd_consumida".
            # O filtro {"_id": ObjectId(prod_id)} garante que apenas o
            #       produto com o ID correspondente seja atualizado.
            self.colecao_produtos.update_one(

                # Filtra o produto pelo ID único no banco.
                {"_id": ObjectId(prod_id)},

                # Reduz o estoque pelo valor consumido.
                {"$inc": {"estoque": -qtd_consumida}}

            )



    def inserir_reserva(self, lugar_id, data, hora_inicial, hora_final,
                        cliente_id, valor_reserva, itens_consumidos=None):

        """
        Método para inserir uma nova reserva no banco de dados.

        Parâmetros:
        - lugar_id: Identificador único do lugar onde será feita a reserva.
        - data: Data da reserva no formato 'YYYY-MM-DD'.
        - hora_inicial: Horário de início da reserva (formato 'HH:MM').
        - hora_final: Horário de término da reserva (formato 'HH:MM').
        - cliente_id: Identificador único do cliente que realizou a reserva.
        - valor_reserva: Valor total da reserva calculado.
        - itens_consumidos: Lista de itens consumidos durante a reserva (opcional).
        """

        # Verifica se a lista de itens consumidos foi fornecida.
        # Caso não tenha sido passada, inicializa como uma lista vazia.
        if itens_consumidos is None:

            # Garante que mesmo sem itens consumidos, o código continue funcional.
            itens_consumidos = []

        # Busca no banco de dados o lugar correspondente ao ID fornecido.
        # O método `find_one` retorna o documento correspondente
        #       ao ID ou `None` se não encontrar.
        lugar = self.colecao_lugares.find_one({"_id": ObjectId(lugar_id)})

        # Verifica se o lugar foi encontrado no banco de dados.
        # Caso não encontre, levanta um erro para informar que o lugar não existe.
        if not lugar:
            raise ValueError("Lugar não encontrado no banco de dados.")

        # Calcula a soma total dos itens consumidos durante a reserva.
        # Para cada item na lista `itens_consumidos`, multiplica a
        #       quantidade (`qtd`) pelo preço unitário (`preco_unit`) e soma os resultados.
        soma_itens = sum(i["qtd"] * i["preco_unit"] for i in itens_consumidos)

        # Calcula o valor total da reserva.
        # O valor total é a soma do valor da reserva (horas no
        #       lugar) com o custo dos itens consumidos.
        valor_total = valor_reserva + soma_itens

        # Converte o ID do cliente (que foi recebido como uma
        #       string) para o tipo `ObjectId`.
        # Isso é necessário porque o MongoDB armazena IDs no
        #       formato `ObjectId`, e a consulta precisa usar o mesmo tipo.
        cliente_id_obj = ObjectId(cliente_id)

        # Cria um dicionário chamado `doc` para representar a reserva
        #       que será armazenada no banco de dados.
        doc = {

            # Armazena o ID do lugar como um `ObjectId`, necessário para
            #       identificar o lugar no banco de dados.
            "lugar_id": ObjectId(lugar_id),

            # Adiciona o nome do lugar. Se o campo "nome" não existir no
            #       documento do lugar, utiliza uma string vazia como padrão.
            "nome_lugar": lugar.get("nome", ""),

            # Adiciona o tipo do lugar (ex.: quadra esportiva, salão de festas).
            #       Se o campo "tipo" não existir, utiliza uma string vazia.
            "tipo_lugar": lugar.get("tipo", ""),

            # Registra a data da reserva, recebida como argumento.
            "data": data,

            # Registra a hora inicial da reserva, recebida como argumento.
            "hora_inicial": hora_inicial,

            # Registra a hora final da reserva, recebida como argumento.
            "hora_final": hora_final,

            # Armazena o ID do cliente como um `ObjectId`. Isso garante que o
            #       cliente seja identificado corretamente no banco de dados.
            "cliente_id": cliente_id_obj,  # <--- Armazenando como ObjectId

            # Registra o valor da reserva calculado anteriormente, que
            #       corresponde ao custo do lugar pelo período reservado.
            "valor_reserva": valor_reserva,

            # Armazena a lista de itens consumidos durante a reserva.
            # Cada item contém a quantidade consumida (`qtd`) e o
            #       preço unitário (`preco_unit`).
            "itens_consumidos": itens_consumidos,

            # Registra o valor total da reserva, que é a soma do valor da
            #       reserva e do custo dos itens consumidos.
            "valor_total": valor_total,

            # Adiciona a data e hora atuais como o momento de criação da reserva no sistema.
            # `datetime.now()` captura o momento exato em que o documento é criado.
            "data_criacao": datetime.now()

        }

        # Insere o dicionário `doc` como um novo documento na
        #       coleção `reservas` do MongoDB.
        # `insert_one` é usado para adicionar um único documento à coleção.
        self.colecao_reservas.insert_one(doc)


    """
        Cancela uma reserva específica com base no ID do lugar, 
                data, hora inicial e hora final.
    """

    def cancelar_reserva(self, lugar_id, data_reserva, hora_inicial, hora_final):

        # Busca no banco de dados MongoDB a reserva que corresponde
        #       exatamente aos parâmetros fornecidos.
        reserva = self.colecao_reservas.find_one({

            # Converte o ID do lugar para ObjectId, formato usado no MongoDB.
            "lugar_id": ObjectId(lugar_id),
            "data": data_reserva,  # Filtra pela data exata da reserva.
            "hora_inicial": hora_inicial,  # Filtra pela hora inicial da reserva.
            "hora_final": hora_final  # Filtra pela hora final da reserva.

        })

        # Verifica se a reserva foi encontrada no banco de dados.
        if not reserva:

            # Se a reserva não for encontrada, retorna False,
            #       indicando falha no cancelamento.
            return False

        # Obtém a lista de itens consumidos da reserva. Caso não existam
        #       itens consumidos, retorna uma lista vazia.
        itens_consumidos = reserva.get("itens_consumidos", [])

        # Itera sobre cada item da lista de itens consumidos.
        for item in itens_consumidos:

            # Obtém o ID do produto consumido. Se a chave "produto_id"
            #       não estiver presente, retorna None.
            prod_id = item.get("produto_id")

            # Obtém a quantidade consumida do produto. Se a chave "qtd"
            #       não existir, assume o valor padrão 0.
            qtd_consumida = item.get("qtd", 0)

            # Verifica se o ID do produto é válido e se a quantidade
            #       consumida é maior que 0 para continuar.
            if prod_id and qtd_consumida > 0:

                # Atualiza o registro do produto no banco de dados.
                # Localiza o produto pelo ID (convertido para ObjectId) e incrementa o estoque
                # adicionando a quantidade consumida de volta ao estoque.
                self.colecao_produtos.update_one(
                    {"_id": ObjectId(prod_id)},  # Critério de busca: produto com o ID especificado.
                    {"$inc": {"estoque": qtd_consumida}}  # Incremento do estoque com a quantidade devolvida.
                )

        # Exclui a reserva correspondente ao lugar, data e horários informados.
        resultado = self.colecao_reservas.delete_one({

            # Localiza a reserva pelo ID do lugar (convertido para ObjectId).
            "lugar_id": ObjectId(lugar_id),

            # Filtra pela data específica da reserva.
            "data": data_reserva,

            # Filtra pelo horário inicial da reserva.
            "hora_inicial": hora_inicial,

            # Filtra pelo horário final da reserva.
            "hora_final": hora_final

        })

        # Retorna True se pelo menos um documento foi excluído (deleted_count > 0).
        return resultado.deleted_count > 0


###############################################################################
#                        JANELA DE LUGARES (CRUD)                             #
###############################################################################
# Define a classe para gerenciar a interface de lugares.
class JanelaLugares:

    # Inicializa a janela de gerenciamento de lugares.
    # `parent` é a janela principal que contém esta janela.
    # `reserva` é o objeto que representa a conexão com o banco de
    #       dados e as operações relacionadas.
    def __init__(self, parent, reserva):

        # Salva a referência à janela pai para futuras interações.
        self.parent = parent

        # Salva a referência ao objeto `reserva` para realizar
        #       operações com o banco de dados.
        self.reserva = reserva

        # Cria uma nova janela do tipo `Toplevel`, filha da janela principal.
        self.janela = tk.Toplevel(parent)

        # Define o título da janela para "Gerenciamento de Lugares".
        self.janela.title("Gerenciamento de Lugares")

        # Define o estado da janela como "zoomed", expandindo
        #       para ocupar a tela inteira.
        self.janela.state("zoomed")

        # Cria um quadro com borda e título para o formulário de cadastro.
        # `self.janela` é a janela principal onde o quadro será inserido.
        # `text="Cadastro de Lugares"` define o título exibido na borda do quadro.
        # `padding=10` adiciona um espaço interno de 10 pixels dentro do quadro.
        quadro_form = ttk.LabelFrame(self.janela, text="Cadastro de Lugares", padding=10)

        # Posiciona o quadro na janela e define que ele ocupará toda a largura disponível.
        # `fill='x'` faz o quadro se expandir horizontalmente.
        # `padx=10` adiciona um espaço horizontal de 10 pixels em ambos os lados do quadro.
        # `pady=10` adiciona um espaço vertical de 10 pixels acima e abaixo do quadro.
        quadro_form.pack(fill='x', padx=10, pady=10)

        # Cria um rótulo de texto para o campo "Nome".
        # `text="Nome:"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte como Arial com tamanho 14.
        # `grid(row=0, column=0)` posiciona o rótulo na primeira
        #       linha (0) e primeira coluna (0) do quadro.
        # `padx=5, pady=5` adiciona um espaçamento interno de 5 pixels ao redor do rótulo.
        # `sticky='e'` alinha o rótulo à direita da célula da grade.
        ttk.Label(quadro_form,
                  text="Nome:",
                  font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de texto vinculada ao campo de entrada.
        # `self.var_nome` será usada para obter ou definir o valor digitado no campo.
        self.var_nome = tk.StringVar()

        # Cria um campo de entrada de texto para o nome do lugar.
        # `textvariable=self.var_nome` associa o campo à variável `self.var_nome`.
        # `font=("Arial", 14)` define a fonte como Arial com tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=0, column=1)` posiciona o campo de entrada na
        #       primeira linha (0) e segunda coluna (1) do quadro.
        # `padx=5, pady=5` adiciona um espaçamento interno de 5
        #       pixels ao redor do campo.
        ttk.Entry(quadro_form,
                  textvariable=self.var_nome,
                  font=("Arial", 14),
                  width=50).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo de texto para o campo "Tipo".
        # `text="Tipo:"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte como Arial com tamanho 14.
        # `grid(row=1, column=0)` posiciona o rótulo na segunda linha (1) e
        #       primeira coluna (0) do quadro.
        # `padx=5, pady=5` adiciona um espaçamento interno de 5 pixels ao redor do rótulo.
        # `sticky='e'` alinha o rótulo à direita da célula da grade.
        ttk.Label(quadro_form,
                  text="Tipo:",
                  font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de texto vinculada ao campo de entrada.
        # `self.var_tipo` será usada para obter ou definir o valor digitado no campo.
        self.var_tipo = tk.StringVar()

        # Cria um campo de entrada de texto para o tipo do lugar.
        # `textvariable=self.var_tipo` associa o campo à variável `self.var_tipo`.
        # `font=("Arial", 14)` define a fonte como Arial com tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=1, column=1)` posiciona o campo de entrada na
        #       segunda linha (1) e segunda coluna (1) do quadro.
        # `padx=5, pady=5` adiciona um espaçamento interno
        #       de 5 pixels ao redor do campo.
        ttk.Entry(quadro_form,
                  textvariable=self.var_tipo,
                  font=("Arial", 14),
                  width=50).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo de texto para o campo "Valor Hora (R$)".
        # `text="Valor Hora (R$):"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte como Arial com tamanho 14.
        # `grid(row=2, column=0)` posiciona o rótulo na terceira linha (2) e
        #       primeira coluna (0) do quadro.
        # `padx=5, pady=5` adiciona um espaçamento interno
        #       de 5 pixels ao redor do rótulo.
        # `sticky='e'` alinha o rótulo à direita da célula da grade.
        ttk.Label(quadro_form,
                  text="Valor Hora (R$):",
                  font=("Arial", 14)).grid(row=2, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de texto vinculada ao campo de entrada.
        # `self.var_valor` será usada para obter ou definir o valor digitado no campo.
        self.var_valor = tk.StringVar()

        # Cria um campo de entrada de texto para o valor da hora do lugar.
        # `textvariable=self.var_valor` associa o campo à variável `self.var_valor`.
        # `font=("Arial", 14)` define a fonte como Arial com tamanho 14.
        # `width=20` define a largura do campo como 20 caracteres.
        # `grid(row=2, column=1)` posiciona o campo de entrada na
        #       terceira linha (2) e segunda coluna (1) do quadro.
        # `padx=5, pady=5` adiciona um espaçamento interno de 5 pixels ao redor do campo.
        # `sticky='w'` alinha o campo à esquerda da célula da grade.
        ttk.Entry(quadro_form,
                  textvariable=self.var_valor,
                  font=("Arial", 14),
                  width=20).grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Botões do formulário (incluindo Alterar e Excluir na mesma linha)
        # Cria um quadro para organizar os botões abaixo do formulário.
        # `quadro_botoes_form` será o contêiner para os botões relacionados ao cadastro.
        # `ttk.Frame(quadro_form)` define o quadro como filho de `quadro_form`.
        # `grid(row=3, column=0, columnspan=2)` posiciona o quadro na quarta linha (3) do formulário,
        # ocupando duas colunas (columnspan=2) para centralizar os botões.
        # `pady=10` adiciona 10 pixels de espaçamento vertical acima e abaixo do quadro.
        quadro_botoes_form = ttk.Frame(quadro_form)
        quadro_botoes_form.grid(row=3, column=0, columnspan=2, pady=10)

        # Cria um botão de "Cadastrar" dentro do quadro de botões.
        # `text="Cadastrar"` define o texto exibido no botão.
        # `command=self.cadastrar` associa o método `self.cadastrar` ao
        #       botão para ser executado quando clicado.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=0)` posiciona o botão na primeira linha (0) e
        #       primeira coluna (0) do quadro.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Cadastrar",
                   command=self.cadastrar,
                   width=20).grid(row=0, column=0, padx=10)

        # Cria um botão de "Alterar" dentro do quadro de botões.
        # `text="Alterar"` define o texto exibido no botão.
        # `command=self.alterar` associa o método `self.alterar` ao botão,
        #       que será executado quando clicado.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=1)` posiciona o botão na primeira linha (0) e
        #       segunda coluna (1) do quadro.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Alterar",
                   command=self.alterar, width=20).grid(row=0, column=1, padx=10)

        # Cria um botão de "Excluir" dentro do quadro de botões.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir` associa o método `self.excluir` ao
        #       botão, que será executado quando clicado.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=2)` posiciona o botão na primeira linha (0) e
        #       terceira coluna (2) do quadro.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Excluir",
                   command=self.excluir,
                   width=20).grid(row=0, column=2, padx=10)

        # Cria um botão de "Limpar" dentro do quadro de botões.
        # `text="Limpar"` define o texto exibido no botão.
        # `command=self.limpar` associa o método `self.limpar` ao
        #       botão, que será executado quando clicado.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=3)` posiciona o botão na primeira linha (0) e
        #       quarta coluna (3) do quadro.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Limpar",
                   command=self.limpar,
                   width=20).grid(row=0, column=3, padx=10)

        # Cria um quadro para a tabela que exibe a lista de lugares.
        # `ttk.LabelFrame` é usado para criar um contêiner com uma borda e título.
        # `self.janela` define que o quadro será inserido na janela principal.
        # `text="Lista de Lugares"` define o título exibido no quadro.
        # `padding=10` adiciona 10 pixels de espaçamento interno ao redor do conteúdo do quadro.
        quadro_tabela = ttk.LabelFrame(self.janela, text="Lista de Lugares", padding=10)

        # Define o layout do quadro, ajustando-o para preencher o espaço disponível.
        # `fill='both'` indica que o quadro será redimensionado para
        #       preencher tanto na largura quanto na altura.
        # `expand=True` permite que o quadro expanda para ocupar o espaço disponível na janela.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal externo ao quadro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical externo ao quadro.
        quadro_tabela.pack(fill='both', expand=True, padx=10, pady=10)

        # Cria uma tabela (Treeview) para exibir os lugares cadastrados.
        # `quadro_tabela` é o contêiner onde a tabela será inserida.
        # `columns=("Nome", "Tipo", "ValorHora")` define as colunas da tabela.
        # `show='headings'` remove a coluna padrão que aparece na esquerda.
        # `height=15` define o número de linhas visíveis na tabela.
        self.tree = ttk.Treeview(
            quadro_tabela, columns=("Nome", "Tipo", "ValorHora"), show='headings', height=15
        )

        # Define o cabeçalho da coluna "Nome".
        # `text="Nome"` define o texto exibido no cabeçalho.
        self.tree.heading("Nome", text="Nome")

        # Define o cabeçalho da coluna "Tipo".
        # `text="Tipo"` define o texto exibido no cabeçalho.
        self.tree.heading("Tipo", text="Tipo")

        # Define o cabeçalho da coluna "ValorHora".
        # `text="Valor/Hora"` define o texto exibido no cabeçalho.
        self.tree.heading("ValorHora", text="Valor/Hora")

        # Configura a largura e alinhamento da coluna "Nome".
        # `width=300` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Nome", width=300, anchor="center")

        # Configura a largura e alinhamento da coluna "Tipo".
        # `width=250` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Tipo", width=250, anchor="center")

        # Configura a largura e alinhamento da coluna "ValorHora".
        # `width=150` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("ValorHora", width=150, anchor="center")

        # Posiciona a tabela dentro do quadro, ajustando para
        #       preencher o espaço disponível.
        # `fill='both'` faz com que a tabela seja redimensionada para
        #       preencher a largura e altura do quadro.
        # `expand=True` permite que a tabela expanda para ocupar todo o espaço disponível.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal externo.
        # `pady=10` adiciona 10 pixels de espaçamento vertical externo.
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Cria e configura o estilo para ajustar a fonte da Treeview.
        # `ttk.Style()` cria um objeto de estilo para personalizar componentes.
        style = ttk.Style()

        # Define a fonte padrão para as linhas da Treeview.
        # `font=("Arial", 14)` define a fonte como Arial, tamanho 14.
        style.configure("Treeview", font=("Arial", 14))

        # Define a fonte do cabeçalho da Treeview.
        # `font=("Arial", 14, "bold")` define a fonte como Arial, tamanho 14, em negrito.
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        # Vincula um evento de duplo clique (`<Double-1>`) a um método específico.
        # Quando o usuário der um duplo clique em uma linha da tabela, o
        #       método `selecionar_item` será chamado.
        self.tree.bind("<Double-1>", self.selecionar_item)

        # Chama o método `listar` para carregar e exibir os
        #       lugares cadastrados na tabela.
        self.listar()


    def listar(self):

        # Remove todos os itens da TreeView, garantindo que a
        #       lista seja atualizada do zero.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca todos os registros de lugares na coleção do banco de dados.
        lugares = self.reserva.colecao_lugares.find()

        # Itera sobre cada lugar retornado do banco de dados.
        for lug in lugares:

            # Insere o lugar atual na TreeView.
            self.tree.insert( "",  # Insere como item filho da raiz (sem hierarquia).
                        "end",  # Posiciona o item no final da lista.
                        iid=str(lug["_id"]),  # Define o identificador único do item como o ID do lugar.
                        values=( lug.get("nome", ""),  # Obtém o nome do lugar ou uma string vazia se não existir.
                                lug.get("tipo", ""),  # Obtém o tipo do lugar ou uma string vazia se não existir.
                                lug.get("valor_hora", 0.0)))  # Obtém o valor/hora do lugar ou 0.0 se não existir.



    def selecionar_item(self, event):

        # Obtém o item atualmente selecionado na TreeView.
        sel = self.tree.selection()

        # Verifica se há um item selecionado. Caso não haja, encerra a função.
        if not sel:
            return

        # Obtém o identificador único (iid) do item selecionado.
        iid = sel[0]

        # Recupera os valores associados ao item selecionado na TreeView.
        valores = self.tree.item(iid, "values")

        # Preenche os campos do formulário com os valores do item selecionado.
        # Define o valor do campo "Nome" com o primeiro valor da lista de valores.
        self.var_nome.set(valores[0])

        # Define o valor do campo "Tipo" com o segundo valor da lista de valores.
        self.var_tipo.set(valores[1])

        # Define o valor do campo "Valor Hora" com o terceiro valor da lista de valores.
        self.var_valor.set(valores[2])


    def cadastrar(self):

        # Obtém o valor do campo "Nome" e remove espaços em branco extras.
        nome = self.var_nome.get().strip()

        # Obtém o valor do campo "Tipo" e remove espaços em branco extras.
        tipo = self.var_tipo.get().strip()

        # Obtém o valor do campo "Valor Hora (R$)" e remove espaços em branco extras.
        val_str = self.var_valor.get().strip()

        # Verifica se algum dos campos está vazio.
        if not nome or not tipo or not val_str:

            # Exibe uma mensagem de aviso se algum campo obrigatório não foi preenchido.
            # `messagebox.showwarning` exibe um alerta com o título "Aviso" e uma mensagem informativa.
            # `parent=self.janela` garante que o alerta esteja associado à janela atual.
            messagebox.showwarning("Aviso",
                           "Preencha todos os campos.",
                                   parent=self.janela)
            return

        try:

            # Tenta converter o valor do campo "Valor Hora (R$)"
            #       para um número decimal (float).
            val_hora = float(val_str)

        except ValueError:

            # Caso ocorra um erro de conversão, exibe uma mensagem de
            #       erro informando que o valor é inválido.
            messagebox.showerror("Erro",
                                 "Valor hora inválido.",
                                 parent=self.janela)

            # Sai do método, pois o valor é inválido.
            return

        # Insere o novo lugar na coleção de lugares do banco de dados MongoDB.
        # O documento contém o nome, tipo e valor hora do lugar.
        self.reserva.colecao_lugares.insert_one({"nome": nome, "tipo": tipo, "valor_hora": val_hora})

        # Exibe uma mensagem de sucesso ao concluir o cadastro do lugar.
        messagebox.showinfo("Sucesso",
                            "Lugar cadastrado com sucesso!",
                            parent=self.janela)

        # Atualiza a lista de lugares exibida na interface.
        self.listar()

        # Limpa os campos de entrada do formulário após o cadastro.
        self.limpar()


    def alterar(self):

        # Obtém o item atualmente selecionado na TreeView.
        sel = self.tree.selection()

        # Verifica se há um item selecionado. Caso contrário, exibe um aviso ao usuário.
        if not sel:
            messagebox.showwarning("Aviso",
                                   "Selecione um registro para alterar.",
                                   parent=self.janela)
            return

        # Obtém o identificador único (iid) do item selecionado.
        iid = sel[0]

        # Obtém e sanitiza o valor do campo "Nome" do formulário.
        nome = self.var_nome.get().strip()

        # Obtém e sanitiza o valor do campo "Tipo" do formulário.
        tipo = self.var_tipo.get().strip()

        # Obtém e sanitiza o valor do campo "Valor Hora" do formulário.
        val_str = self.var_valor.get().strip()

        # Verifica se os campos "Nome", "Tipo" e "Valor Hora" foram preenchidos.
        if not nome or not tipo or not val_str:

            # Exibe uma mensagem de aviso caso algum campo esteja vazio.
            messagebox.showwarning("Aviso",
                                   "Preencha todos os campos antes de alterar.",
                                   parent=self.janela)
            return

        # Tenta converter o valor do campo "Valor Hora" para um número decimal.
        try:

            val_hora = float(val_str)

        except ValueError:

            # Exibe um aviso caso o valor fornecido não seja um número válido.
            messagebox.showwarning("Aviso",
                                   "Valor hora inválido.",
                                   parent=self.janela)
            return

        # Atualiza o registro do lugar no banco de dados.
        self.reserva.colecao_lugares.update_one(

            # Filtra pelo ID único do lugar selecionado.
            {"_id": ObjectId(iid)},

            # Define os novos valores para "nome", "tipo" e "valor_hora".
            {"$set": {"nome": nome, "tipo": tipo, "valor_hora": val_hora}}

        )

        # Exibe uma mensagem informando que a atualização foi bem-sucedida.
        messagebox.showinfo("Sucesso",
                            "Registro alterado com sucesso!",
                            parent=self.janela)

        # Atualiza a lista de lugares exibida na TreeView.
        self.listar()

        # Limpa os campos de entrada após a alteração.
        self.limpar()


    # Define o método para excluir o registro selecionado.
    def excluir(self):

        # Obtém o item selecionado na TreeView.
        sel = self.tree.selection()

        # Verifica se nenhum item foi selecionado.
        if not sel:

            # Exibe um aviso caso nenhum registro esteja selecionado.
            messagebox.showwarning("Aviso",
                                   "Selecione um registro para excluir.",
                                   parent=self.janela)
            return

        # Obtém o ID único do registro selecionado.
        iid = sel[0]

        # Exclui o registro do banco de dados com base no ID.
        self.reserva.colecao_lugares.delete_one({"_id": ObjectId(iid)})

        # Exibe uma mensagem informando que a exclusão foi concluída com sucesso.
        messagebox.showinfo("Sucesso",
                            "Registro excluído com sucesso!",
                            parent=self.janela)

        # Atualiza a lista de lugares exibida na TreeView.
        self.listar()

        # Limpa os campos de entrada após a exclusão.
        self.limpar()


    def limpar(self):

        # Limpa o campo "Nome" do formulário definindo seu valor como uma string vazia.
        self.var_nome.set("")

        # Limpa o campo "Tipo" do formulário definindo seu valor como uma string vazia.
        self.var_tipo.set("")

        # Limpa o campo "Valor Hora (R$)" do formulário definindo
        #       seu valor como uma string vazia.
        self.var_valor.set("")



###############################################################################
#                JANELA DE FORNECEDORES (CRUD + HISTÓRICO)                    #
###############################################################################
class JanelaFornecedores:

    # Método construtor da classe JanelaFornecedores.
    def __init__(self, parent, reserva):

        # Armazena a referência da janela pai para possíveis interações.
        self.parent = parent

        # Armazena a instância do objeto reserva, que contém os
        #       métodos e coleções do banco de dados.
        self.reserva = reserva

        # Cria uma nova janela no topo da janela principal.
        self.janela = tk.Toplevel(parent)

        # Define o título da janela como "Gerenciamento de Fornecedores".
        self.janela.title("Gerenciamento de Fornecedores")

        # Define a janela no modo "zoomed" para ocupar toda a
        #       tela (compatível principalmente no Windows).
        self.janela.state("zoomed")

        # Cria um quadro com borda e título para organizar os widgets do formulário de cadastro.
        # `text="Cadastro de Fornecedores"` define o título exibido no quadro.
        # `padding=10` adiciona 10 pixels de espaçamento interno ao redor do conteúdo do quadro.
        quadro_form = ttk.LabelFrame(self.janela,
                                     text="Cadastro de Fornecedores",
                                     padding=10)

        # Posiciona o quadro no layout da janela.
        # `fill='x'` faz com que o quadro ocupe toda a largura horizontal disponível.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do quadro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do quadro.
        quadro_form.pack(fill='x', padx=10, pady=10)

        # Adiciona um rótulo "Nome:" dentro do quadro.
        # `text="Nome:"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        ttk.Label(quadro_form, text="Nome:", font=("Arial", 14)).grid(
            row=0,  # Especifica a posição do rótulo na linha 0 da grade.
            column=0,  # Especifica a posição do rótulo na coluna 0 da grade.
            padx=5,  # Adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
            pady=5,  # Adiciona 5 pixels de espaçamento vertical ao redor do rótulo.
            sticky='e'  # Alinha o rótulo à direita dentro da célula da grade.
        )

        # Cria uma variável do tipo StringVar para armazenar o
        #       valor do campo de entrada "Nome".
        # Essa variável será usada para vincular o texto
        #       digitado no campo ao programa.
        self.var_nome = tk.StringVar()

        # Cria um campo de entrada para o nome do fornecedor.
        # `textvariable=self.var_nome` vincula o valor digitado à variável self.var_nome.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=0, column=1)` posiciona o campo na linha 0, coluna 1 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        ttk.Entry(quadro_form,
                  textvariable=self.var_nome,
                  font=("Arial", 14),
                  width=50).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de documento (CNPJ/CPF).
        # `text="Documento (CNPJ/CPF):"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `grid(row=1, column=0)` posiciona o rótulo na linha 1, coluna 0 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        # `sticky='e'` alinha o rótulo à direita na célula da grade.
        ttk.Label(quadro_form,
                  text="Documento (CNPJ/CPF):",
                  font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de string para armazenar o documento do fornecedor.
        # `self.var_doc` será usada para capturar e manipular o
        #       valor digitado no campo de entrada.
        self.var_doc = tk.StringVar()


        # Cria um campo de entrada para o documento do fornecedor (CNPJ/CPF).
        # `textvariable=self.var_doc` vincula o valor digitado à variável self.var_doc.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=1, column=1)` posiciona o campo na linha 1, coluna 1 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        ttk.Entry(quadro_form,
                  textvariable=self.var_doc,
                  font=("Arial", 14),
                  width=50).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de telefone.
        # `text="Telefone:"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `grid(row=2, column=0)` posiciona o rótulo na linha 2, coluna 0 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        # `sticky='e'` alinha o rótulo à direita na célula da grade.
        ttk.Label(quadro_form,
                  text="Telefone:",
                  font=("Arial", 14)).grid(row=2, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de string para armazenar o telefone do fornecedor.
        # `self.var_tel` será usada para capturar e manipular o
        #       valor digitado no campo de entrada.
        self.var_tel = tk.StringVar()

        # Cria um campo de entrada para o telefone do fornecedor.
        # `textvariable=self.var_tel` vincula o valor digitado à variável self.var_tel.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=2, column=1)` posiciona o campo na linha 2, coluna 1 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        ttk.Entry(quadro_form,
                  textvariable=self.var_tel,
                  font=("Arial", 14),
                  width=50).grid(row=2, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de e-mail.
        # `text="E-mail:"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `grid(row=3, column=0)` posiciona o rótulo na linha 3, coluna 0 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        # `sticky='e'` alinha o rótulo à direita na célula da grade.
        ttk.Label(quadro_form,
                  text="E-mail:",
                  font=("Arial", 14)).grid(row=3, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de string para armazenar o e-mail do fornecedor.
        # `self.var_email` será usada para capturar e manipular o
        #       valor digitado no campo de entrada.
        self.var_email = tk.StringVar()

        # Cria um campo de entrada para o e-mail do fornecedor.
        # `textvariable=self.var_email` vincula o valor digitado à variável self.var_email.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=3, column=1)` posiciona o campo na linha 3, coluna 1 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        ttk.Entry(quadro_form,
                  textvariable=self.var_email,
                  font=("Arial", 14),
                  width=50).grid(row=3, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de endereço.
        # `text="Endereço:"` define o texto exibido no rótulo.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `grid(row=4, column=0)` posiciona o rótulo na linha 4, coluna 0 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        # `sticky='e'` alinha o rótulo à direita na célula da grade.
        ttk.Label(quadro_form,
                  text="Endereço:",
                  font=("Arial", 14)).grid(row=4, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de string para armazenar o endereço do fornecedor.
        # `self.var_end` será usada para capturar e manipular o
        #       valor digitado no campo de entrada.
        self.var_end = tk.StringVar()

        # Cria um campo de entrada para o endereço do fornecedor.
        # `textvariable=self.var_end` vincula o valor digitado à variável self.var_end.
        # `font=("Arial", 14)` define a fonte do texto como Arial, tamanho 14.
        # `width=50` define a largura do campo como 50 caracteres.
        # `grid(row=4, column=1)` posiciona o campo na linha 4, coluna 1 do quadro do formulário.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        ttk.Entry(quadro_form,
                  textvariable=self.var_end,
                  font=("Arial", 14),
                  width=50).grid(row=4, column=1, padx=5, pady=5)

        # Cria um quadro para organizar os botões do formulário (Cadastrar, Alterar e Excluir).
        # `quadro_form` é o contêiner onde esse quadro será posicionado.
        # `grid(row=5, column=0, columnspan=2)` posiciona o quadro na
        #       linha 5, ocupando as colunas 0 e 1.
        # `pady=10` adiciona 10 pixels de espaçamento vertical acima e abaixo do quadro.
        quadro_botoes_form = ttk.Frame(quadro_form)
        quadro_botoes_form.grid(row=5, column=0, columnspan=2, pady=10)

        # Cria um botão para cadastrar o fornecedor.
        # `text="Cadastrar"` define o texto exibido no botão.
        # `command=self.cadastrar` associa a ação de chamar o método
        #       self.cadastrar ao clicar no botão.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=0)` posiciona o botão na linha 0, coluna 0 do quadro de botões.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal à esquerda e à direita do botão.
        ttk.Button(quadro_botoes_form,
                   text="Cadastrar",
                   command=self.cadastrar,
                   width=20).grid(row=0, column=0, padx=10)

        # Cria um botão para alterar os dados do fornecedor.
        # `text="Alterar"` define o texto exibido no botão.
        # `command=self.alterar` associa a ação de chamar o
        #       método self.alterar ao clicar no botão.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=1)` posiciona o botão na linha 0, coluna 1 do quadro de botões.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal à esquerda e à direita do botão.
        ttk.Button(quadro_botoes_form,
                   text="Alterar",
                   command=self.alterar,
                   width=20).grid(row=0, column=1, padx=10)

        # Cria um botão para excluir um fornecedor.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir` associa a ação de chamar o
        #       método self.excluir ao clicar no botão.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=2)` posiciona o botão na linha 0, coluna 2 do quadro de botões.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal à esquerda e à direita do botão.
        ttk.Button(quadro_botoes_form,
                   text="Excluir",
                   command=self.excluir,
                   width=20).grid(row=0, column=2, padx=10)

        # Cria um botão para limpar os campos do formulário.
        # `text="Limpar"` define o texto exibido no botão.
        # `command=self.limpar` associa a ação de chamar o método self.limpar ao clicar no botão.
        # `width=10` define a largura do botão como 10 caracteres.
        # `grid(row=0, column=3)` posiciona o botão na linha 0, coluna 3 do quadro de botões.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal à esquerda e à direita do botão.
        ttk.Button(quadro_botoes_form,
                   text="Limpar",
                   command=self.limpar,
                   width=10).grid(row=0, column=3, padx=10)

        # Cria um botão para abrir o histórico do fornecedor.
        # `text="Histórico"` define o texto exibido no botão.
        # `command=self.abrir_historico_fornecedor` associa a ação de chamar o
        #       método self.abrir_historico_fornecedor ao clicar no botão.
        # `width=20` define a largura do botão como 20 caracteres.
        # `grid(row=0, column=4)` posiciona o botão na linha 0, coluna 4 do quadro de botões.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal à esquerda e à direita do botão.
        ttk.Button(quadro_botoes_form,
                   text="Histórico",
                   command=self.abrir_historico_fornecedor,
                   width=20).grid(row=0, column=4, padx=10)

        # Cria um quadro rotulado para exibir a tabela de fornecedores.
        # `text="Lista de Fornecedores"` define o título exibido no topo do quadro.
        # `padding=10` adiciona 10 pixels de espaçamento interno ao redor do conteúdo do quadro.
        quadro_tabela = ttk.LabelFrame(self.janela, text="Lista de Fornecedores", padding=10)

        # Posiciona o quadro na janela principal.
        # `fill='both'` faz com que o quadro expanda para preencher o
        #       espaço disponível na horizontal e na vertical.
        # `expand=True` permite que o quadro expanda automaticamente
        #       se o tamanho da janela for ajustado.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do quadro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do quadro.
        quadro_tabela.pack(fill='both', expand=True, padx=10, pady=10)

        # Cria um widget Treeview para exibir a lista de fornecedores.
        # `quadro_tabela` define o contêiner onde a Treeview será inserida.
        # `columns` define as colunas que serão exibidas: Nome,
        #       Documento, Telefone, Email e Endereço.
        # `show='headings'` indica que apenas os cabeçalhos das
        #       colunas serão exibidos, sem a coluna de ícones.
        # `height=15` define o número de linhas visíveis na tabela.
        self.tree = ttk.Treeview(quadro_tabela,
                                 columns=("Nome", "Documento", "Telefone", "Email", "Endereco"),
                                 show='headings',
                                 height=15)

        # Define o cabeçalho da coluna "Nome" com o texto "Nome".
        self.tree.heading("Nome", text="Nome")

        # Define o cabeçalho da coluna "Documento" com o texto "Documento".
        self.tree.heading("Documento", text="Documento")

        # Define o cabeçalho da coluna "Telefone" com o texto "Telefone".
        self.tree.heading("Telefone", text="Telefone")

        # Define o cabeçalho da coluna "Email" com o texto "E-mail".
        self.tree.heading("Email", text="E-mail")

        # Define o cabeçalho da coluna "Endereco" com o texto "Endereço".
        self.tree.heading("Endereco", text="Endereço")

        # Configura a largura e alinhamento da coluna "Nome".
        # `width=250` define a largura em pixels.
        # `anchor="center"` centraliza o texto dentro da coluna.
        self.tree.column("Nome", width=250, anchor="center")

        # Configura a largura e alinhamento da coluna "Documento".
        self.tree.column("Documento", width=200, anchor="center")

        # Configura a largura e alinhamento da coluna "Telefone".
        self.tree.column("Telefone", width=150, anchor="center")

        # Configura a largura e alinhamento da coluna "Email".
        self.tree.column("Email", width=200, anchor="center")

        # Configura a largura e alinhamento da coluna "Endereco".
        self.tree.column("Endereco", width=300, anchor="center")

        # Posiciona o widget Treeview no quadro da tabela.
        # `fill='both'` faz com que a tabela preencha o espaço
        #       horizontal e vertical disponível.
        # `expand=True` permite que a tabela se expanda automaticamente
        #       quando o tamanho da janela for ajustado.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor da tabela.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor da tabela.
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Cria um estilo para personalizar a aparência do widget Treeview.
        # `ttk.Style` é usado para alterar propriedades de estilo de widgets do ttk.
        style = ttk.Style()

        # Configura o estilo padrão da Treeview.
        # `font=("Arial", 14)` define que o texto na tabela usará a fonte Arial, tamanho 14.
        style.configure("Treeview", font=("Arial", 14))

        # Configura o estilo dos cabeçalhos da Treeview.
        # `font=("Arial", 14, "bold")` define que o texto nos
        #       cabeçalhos será Arial, tamanho 14, em negrito.
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        # Vincula o evento de liberar o botão do mouse (`<ButtonRelease-1>`) à
        #       função `selecionar_item`.
        # Esse evento será disparado quando o usuário clicar em um
        #       item da tabela e soltar o botão do mouse.
        self.tree.bind("<ButtonRelease-1>", self.selecionar_item)

        # Vincula o evento de duplo clique (`<Double-1>`) à
        #       função `abrir_historico_fornecedor`.
        # Esse evento será disparado quando o usuário der um
        #       duplo clique em um item da tabela.
        self.tree.bind("<Double-1>", self.abrir_historico_fornecedor)

        # Chama a função `listar` para preencher a Treeview
        #       com os dados iniciais dos fornecedores.
        self.listar()


    # Define o método `listar` para exibir todos os fornecedores na Treeview.
    def listar(self):

        # Remove todos os itens atualmente exibidos na Treeview.
        for item in self.tree.get_children():

            # `self.tree.delete(item)` remove o item especificado da Treeview.
            self.tree.delete(item)

        # Busca todos os fornecedores da coleção `colecao_fornecedores`.
        fornecs = self.reserva.colecao_fornecedores.find()

        # Itera sobre os fornecedores retornados do banco de dados.
        for f in fornecs:

            # Insere cada fornecedor na Treeview.
            self.tree.insert(
                "",  # Define que o item será inserido na raiz da Treeview.
                "end",  # Adiciona o item ao final da lista na Treeview.
                iid=str(f["_id"]),  # Define o ID único do item como o `_id` do fornecedor.
                values=(  # Define os valores exibidos nas colunas da Treeview.
                    f.get("nome", ""),  # Obtém o nome do fornecedor (vazio se não existir).
                    f.get("cpf", ""),  # Obtém o CPF do fornecedor (vazio se não existir).
                    f.get("telefone", ""),  # Obtém o telefone do fornecedor (vazio se não existir).
                    f.get("email", ""),  # Obtém o e-mail do fornecedor (vazio se não existir).
                    f.get("endereco", "")  # Obtém o endereço do fornecedor (vazio se não existir).
                )
            )


    # Define a função `selecionar_item` para ser chamada ao
    #       clicar em um item da Treeview.
    def selecionar_item(self, event):

        # Obtém o item selecionado na Treeview.
        # `self.tree.selection()` retorna uma lista de itens
        #       selecionados. Aqui pegamos o primeiro.
        selecionado = self.tree.selection()

        # Verifica se algum item foi selecionado.
        # Caso não haja seleção, a função retorna sem realizar nenhuma ação.
        if not selecionado:
            return

        # Obtém o ID do item selecionado na Treeview.
        # O ID corresponde ao identificador único associado ao item na tabela.
        item_id = selecionado[0]

        # Obtém os valores associados ao item selecionado.
        # `self.tree.item(item_id, "values")` retorna os valores
        #       de todas as colunas do item.
        valores = self.tree.item(item_id, "values")

        # Atualiza o campo de entrada para o nome com o valor do item selecionado.
        self.var_nome.set(valores[0])

        # Atualiza o campo de entrada para o documento com o valor do item selecionado.
        self.var_doc.set(valores[1])

        # Atualiza o campo de entrada para o telefone com o valor do item selecionado.
        self.var_tel.set(valores[2])

        # Atualiza o campo de entrada para o e-mail com o valor do item selecionado.
        self.var_email.set(valores[3])

        # Atualiza o campo de entrada para o endereço com o valor do item selecionado.
        self.var_end.set(valores[4])


    # Define a função `cadastrar` para inserir um novo
    #       fornecedor no banco de dados.
    def cadastrar(self):

        # Obtém o valor do campo "Nome" do formulário.
        # Remove espaços em branco no início e no final da string com `strip()`.
        nome = self.var_nome.get().strip()

        # Obtém o valor do campo "Documento (CNPJ/CPF)" do formulário.
        # Remove espaços em branco no início e no final da string com `strip()`.
        doc = self.var_doc.get().strip()

        # Obtém o valor do campo "Telefone" do formulário.
        # Remove espaços em branco no início e no final da string com `strip()`.
        tel = self.var_tel.get().strip()

        # Obtém o valor do campo "E-mail" do formulário.
        # Remove espaços em branco no início e no final da string com `strip()`.
        email = self.var_email.get().strip()

        # Obtém o valor do campo "Endereço" do formulário.
        # Remove espaços em branco no início e no final da string com `strip()`.
        end = self.var_end.get().strip()

        # Verifica se os campos obrigatórios "Nome" e "Documento" foram preenchidos.
        # Caso contrário, exibe uma mensagem de aviso e interrompe o cadastro.
        if not nome or not doc:

            # Exibe uma mensagem de aviso ao usuário.
            # Informa que os campos "Nome" e "Documento" são obrigatórios.
            messagebox.showwarning("Aviso",
                                   "Nome e Documento são obrigatórios.",
                                   parent=self.janela)
            return

        # Cria um dicionário para armazenar os dados do fornecedor
        #       que será inserido no banco de dados.
        doc_insert = {

            # Adiciona o valor do campo "Nome" ao dicionário com a chave "nome".
            "nome": nome,

            # Adiciona o valor do campo "Documento" ao dicionário.
            # A chave é definida como "cpf", mas pode ser alterada
            #       para "cnpj" conforme a necessidade.
            "cpf": doc,  # ou 'cnpj': doc, se preferir

            # Adiciona o valor do campo "Telefone" ao dicionário com a chave "telefone".
            "telefone": tel,

            # Adiciona o valor do campo "E-mail" ao dicionário com a chave "email".
            "email": email,

            # Adiciona o valor do campo "Endereço" ao dicionário com a chave "endereco".
            "endereco": end

        }

        # Insere o dicionário `doc_insert` na coleção de fornecedores do banco de dados.
        self.reserva.colecao_fornecedores.insert_one(doc_insert)

        # Exibe uma mensagem de sucesso para informar ao usuário que o fornecedor foi cadastrado.
        messagebox.showinfo("Sucesso",
                            "Fornecedor cadastrado!",
                            parent=self.janela)

        # Atualiza a lista de fornecedores exibida na interface
        #       para incluir o novo fornecedor.
        self.listar()

        # Limpa os campos do formulário para permitir o
        #       cadastro de um novo fornecedor.
        self.limpar()


    # Define o método `alterar` para atualizar os dados de
    #       um fornecedor selecionado.
    def alterar(self):

        # Verifica se há algum fornecedor selecionado na Treeview.
        sel = self.tree.selection()
        if not sel:

            # Exibe um aviso caso nenhum fornecedor tenha sido selecionado.
            messagebox.showwarning("Aviso",
                                   "Selecione um fornecedor para alterar.",
                                   parent=self.janela)
            return

        # Obtém o ID único do fornecedor selecionado.
        iid = sel[0]

        # Cria um dicionário com os novos valores dos campos a serem atualizados.
        doc_update = {
            "nome": self.var_nome.get().strip(),  # Obtém e remove espaços extras do nome.
            "cpf": self.var_doc.get().strip(),  # Obtém e remove espaços extras do documento (CPF/CNPJ).
            "telefone": self.var_tel.get().strip(),  # Obtém e remove espaços extras do telefone.
            "email": self.var_email.get().strip(),  # Obtém e remove espaços extras do e-mail.
            "endereco": self.var_end.get().strip()  # Obtém e remove espaços extras do endereço.
        }

        # Atualiza os dados do fornecedor no banco de dados usando o ID selecionado.
        # Utiliza `$set` para garantir que apenas os campos especificados sejam modificados.
        self.reserva.colecao_fornecedores.update_one({"_id": ObjectId(iid)}, {"$set": doc_update})

        # Exibe uma mensagem de confirmação após a alteração bem-sucedida.
        messagebox.showinfo("OK", "Fornecedor alterado!", parent=self.janela)

        # Atualiza a lista de fornecedores na Treeview para refletir as alterações.
        self.listar()

        # Limpa os campos do formulário após a alteração.
        self.limpar()


    def excluir(self):

        # Obtém a seleção atual na Treeview.
        sel = self.tree.selection()

        # Verifica se algum item foi selecionado.
        if not sel:

            # Exibe uma mensagem de aviso caso nenhum fornecedor esteja selecionado.
            messagebox.showwarning("Aviso",
                                   "Selecione um fornecedor para excluir.",
                                   parent=self.janela)
            return

        # Obtém o ID do fornecedor selecionado.
        iid = sel[0]

        # Remove o fornecedor do banco de dados usando o ID selecionado.
        self.reserva.colecao_fornecedores.delete_one({"_id": ObjectId(iid)})

        # Exibe uma mensagem de confirmação após a exclusão.
        messagebox.showinfo("OK", "Fornecedor excluído.", parent=self.janela)

        # Atualiza a Treeview para refletir a exclusão do fornecedor.
        self.listar()

        # Limpa os campos do formulário para evitar inconsistências.
        self.limpar()


    # Define o método `limpar` para limpar todos os campos do formulário.
    def limpar(self):

        # Limpa o campo "Nome" definindo o valor da variável `var_nome` como uma string vazia.
        self.var_nome.set("")

        # Limpa o campo "Documento" definindo o valor da variável `var_doc` como uma string vazia.
        self.var_doc.set("")

        # Limpa o campo "Telefone" definindo o valor da variável `var_tel` como uma string vazia.
        self.var_tel.set("")

        # Limpa o campo "E-mail" definindo o valor da variável `var_email` como uma string vazia.
        self.var_email.set("")

        # Limpa o campo "Endereço" definindo o valor da variável `var_end` como uma string vazia.
        self.var_end.set("")


    # Define a função `abrir_historico_fornecedor` para abrir o
    #       histórico detalhado de um fornecedor.
    def abrir_historico_fornecedor(self, event=None):

        # Obtém o item selecionado na Treeview.
        # `self.tree.selection()` retorna uma lista com os IDs dos itens selecionados.
        sel = self.tree.selection()

        # Verifica se algum item foi selecionado.
        # Caso não haja seleção, a função retorna sem realizar nenhuma ação.
        if not sel:
            return

        # Obtém o ID do item selecionado na Treeview.
        # O ID corresponde ao identificador único associado ao fornecedor na tabela.
        iid = sel[0]

        # Consulta o banco de dados para obter as informações detalhadas do fornecedor.
        # Utiliza o ID do item selecionado para buscar na coleção de fornecedores.
        fornecedor_bd = self.reserva.colecao_fornecedores.find_one({"_id": ObjectId(iid)})

        # Verifica se o fornecedor foi encontrado no banco de dados.
        if fornecedor_bd:

            # Se encontrado, abre a janela de histórico detalhado do fornecedor.
            # Passa como parâmetro o ID do fornecedor para a janela.
            JanelaHistoricoFornecedoresDetalhe(self.janela, self.reserva, fornecedor_bd["_id"])



class JanelaHistoricoFornecedoresDetalhe:

    # Inicializador da classe
    # `parent` é a janela pai.
    # `reserva` é o objeto responsável pela conexão com o banco de dados.
    # `fornecedor_id` é o ID do fornecedor cujo histórico será exibido.
    def __init__(self, parent, reserva: ReservaQuadra, fornecedor_id):

        # Armazena a janela pai.
        self.parent = parent

        # Armazena o objeto de reserva.
        self.reserva = reserva

        # Armazena o ID do fornecedor.
        self.fornecedor_id = fornecedor_id

        # Cria uma nova janela como um nível superior da janela principal.
        # `parent` é a janela pai que contém esta nova janela.
        self.janela = tk.Toplevel(parent)

        # Define o título da nova janela para "Histórico de
        #       Saída de Produtos - Fornecedor".
        self.janela.title("Histórico de Saída de Produtos - Fornecedor")

        # Define o estado da nova janela como maximizado na tela.
        self.janela.state("zoomed")

        # Cria um quadro com borda e título "Filtros" para organizar os filtros.
        # `padding=10` adiciona espaçamento interno de 10 pixels em
        #       todas as direções dentro do quadro.
        quadro_filtros = ttk.LabelFrame(self.janela, text="Filtros", padding=10)

        # Posiciona o quadro de filtros na parte superior da janela.
        # `fill="x"` faz com que o quadro preencha horizontalmente toda a largura disponível.
        # `padx=10` e `pady=10` adicionam 10 pixels de espaçamento
        #       externo nos eixos horizontal e vertical.
        quadro_filtros.pack(fill="x", padx=10, pady=10)

        # Cria um rótulo para o campo de filtro "Data Inicial".
        # `text="Data Inicial:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0)` posiciona o rótulo na primeira linha e
        #       primeira coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à borda direita da célula.
        ttk.Label(quadro_filtros,
                  text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de data para o filtro "Data Inicial".
        # `width=12` define a largura do campo de entrada.
        # `date_pattern="dd/MM/yyyy"` define o formato de exibição da data.
        self.data_inicial = DateEntry(quadro_filtros, width=12, date_pattern="dd/MM/yyyy")

        # Posiciona o campo de entrada de data na primeira linha e
        #       segunda coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento
        #       externo ao redor do campo.
        self.data_inicial.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de filtro "Data Final".
        # `text="Data Final:"` define o texto exibido no rótulo.
        # `grid(row=0, column=2)` posiciona o rótulo na primeira linha e
        #       terceira coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à borda direita da célula.
        ttk.Label(quadro_filtros,
                  text="Data Final:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de data para o filtro "Data Final".
        # `width=12` define a largura do campo de entrada.
        # `date_pattern="dd/MM/yyyy"` define o formato de exibição da data.
        self.data_final = DateEntry(quadro_filtros, width=12, date_pattern="dd/MM/yyyy")

        # Posiciona o campo de entrada de data na primeira linha e
        #       quarta coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento externo ao redor do campo.
        self.data_final.grid(row=0, column=3, padx=5, pady=5)

        # Cria um rótulo para o campo de filtro "Cliente".
        # `text="Cliente:"` define o texto exibido no rótulo.
        # `grid(row=1, column=0)` posiciona o rótulo na segunda linha e
        #       primeira coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à borda direita da célula.
        ttk.Label(quadro_filtros,
                  text="Cliente:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria uma variável de string para armazenar o filtro de cliente.
        # `tk.StringVar()` inicializa uma variável do tipo string
        #       que será vinculada ao campo de entrada.
        self.var_cliente = tk.StringVar()

        # Cria um campo de entrada para o filtro "Cliente".
        # `textvariable=self.var_cliente` vincula o valor do
        #       campo à variável `self.var_cliente`.
        # `width=20` define a largura do campo de entrada.
        # `grid(row=1, column=1)` posiciona o campo na segunda linha e
        #       segunda coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels ao redor do campo.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_cliente,
                  width=20).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de filtro "Produto".
        # `text="Produto:"` define o texto exibido no rótulo.
        # `grid(row=1, column=2)` posiciona o rótulo na segunda linha e
        #       terceira coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à borda direita da célula.
        ttk.Label(quadro_filtros,
                  text="Produto:").grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Cria uma variável de string para armazenar o filtro de produto.
        # `tk.StringVar()` inicializa uma variável do tipo string que
        #       será vinculada ao campo de entrada.
        self.var_produto = tk.StringVar()

        # Cria um campo de entrada para o filtro "Produto".
        # `textvariable=self.var_produto` vincula o valor do campo à
        #       variável `self.var_produto`.
        # `width=20` define a largura do campo de entrada.
        # `grid(row=1, column=3)` posiciona o campo na segunda linha e
        #       quarta coluna do quadro de filtros.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels ao redor do campo.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_produto,
                  width=20).grid(row=1, column=3, padx=5, pady=5)

        # Cria um botão para aplicar os filtros definidos nos campos.
        # `text="Aplicar Filtros"` define o texto exibido no botão.
        # `command=self.listar` vincula o clique do botão ao método `listar`, que
        #       executa a lógica para listar os resultados com base nos filtros.
        # `grid(row=0, column=4)` posiciona o botão na primeira linha e
        #       quinta coluna do quadro de filtros.
        # `padx=10` e `pady=5` adicionam 10 pixels de espaçamento horizontal e 5 pixels
        #       de espaçamento vertical ao redor do botão.
        # `rowspan=2` faz o botão ocupar o espaço de duas linhas, alinhando-se
        #       verticalmente com os campos de filtro.
        ttk.Button(quadro_filtros,
                   text="Aplicar Filtros",
                   command=self.listar).grid(row=0, column=4, padx=10, pady=5, rowspan=2)

        # Cria um quadro para organizar a Treeview com o título "Histórico de Saída de Produtos".
        # `text="Histórico de Saída de Produtos"` define o título do quadro.
        # `padding=10` adiciona 10 pixels de espaçamento interno em todos os lados do quadro.
        # `pack(fill="both", expand=True)` faz o quadro preencher todo o
        #       espaço disponível e se expandir com o layout da janela.
        # `padx=10` e `pady=10` adicionam 10 pixels de espaçamento externo
        #       horizontal e vertical ao redor do quadro.
        quadro_tree = ttk.LabelFrame(self.janela, text="Histórico de Saída de Produtos", padding=10)
        quadro_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria uma Treeview para exibir os dados do histórico de saída de produtos.
        # `columns=("Data", "Cliente", "Produto", "Qtd", "Vendas", "Fornecedor")`
        #       define as colunas que serão exibidas na Treeview.
        # `show='headings'` exibe apenas os cabeçalhos das colunas, sem a coluna de índice padrão.
        self.tree = ttk.Treeview( quadro_tree,
                                columns=("Data", "Cliente", "Produto", "Qtd", "Vendas", "Fornecedor"),
                                show='headings')

        # Define o cabeçalho da coluna "Data".
        # `text="Data"` define o título exibido no cabeçalho da coluna.
        self.tree.heading("Data", text="Data")

        # Define o cabeçalho da coluna "Cliente".
        # `text="Cliente"` define o título exibido no cabeçalho da coluna.
        self.tree.heading("Cliente", text="Cliente")

        # Define o cabeçalho da coluna "Produto".
        # `text="Produto"` define o título exibido no cabeçalho da coluna.
        self.tree.heading("Produto", text="Produto")

        # Define o cabeçalho da coluna "Qtd".
        # `text="Quantidade"` define o título exibido no cabeçalho da coluna.
        self.tree.heading("Qtd", text="Quantidade")

        # Define o cabeçalho da coluna "Vendas".
        # `text="Vendas (R$)"` define o título exibido no cabeçalho da coluna.
        self.tree.heading("Vendas", text="Vendas (R$)")

        # Define o cabeçalho da coluna "Fornecedor".
        # `text="Fornecedor"` define o título exibido no cabeçalho da coluna.
        self.tree.heading("Fornecedor", text="Fornecedor")

        # Configura a coluna "Data".
        # `width=100` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Data", width=100, anchor="center")

        # Configura a coluna "Cliente".
        # `width=150` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Cliente", width=150, anchor="center")

        # Configura a coluna "Produto".
        # `width=150` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Produto", width=150, anchor="center")

        # Configura a coluna "Qtd".
        # `width=100` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Qtd", width=100, anchor="center")

        # Configura a coluna "Vendas".
        # `width=120` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Vendas", width=120, anchor="center")

        # Configura a coluna "Fornecedor".
        # `width=150` define a largura da coluna em pixels.
        # `anchor="center"` alinha o texto no centro da coluna.
        self.tree.column("Fornecedor", width=150, anchor="center")

        # Exibe a Treeview na interface.
        # `fill="both"` faz com que a Treeview se expanda para preencher o espaço disponível.
        # `expand=True` permite que a Treeview expanda conforme o tamanho da janela.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal.
        # `pady=10` adiciona 10 pixels de espaçamento vertical.
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria um quadro para exibir contadores de totais.
        # `fill="x"` faz com que o quadro se expanda horizontalmente.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal.
        # `pady=5` adiciona 5 pixels de espaçamento vertical.
        quadro_totais = ttk.Frame(self.janela)
        quadro_totais.pack(fill="x", padx=10, pady=5)

        # Cria um rótulo para exibir o total de registros.
        # `text="Total de Registros: 0"` define o texto inicial do rótulo.
        # `font=("Arial", 12, "bold")` define a fonte Arial, tamanho 12, em negrito.
        self.label_total = ttk.Label(quadro_totais,
                                     text="Total de Registros: 0",
                                     font=("Arial", 12, "bold"))

        # Exibe o rótulo no lado esquerdo do quadro.
        # `side="left"` alinha o rótulo no lado esquerdo do quadro.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do rótulo.
        self.label_total.pack(side="left", padx=10)

        # Cria um rótulo para exibir o total de vendas.
        # `text="Total de Vendas: R$ 0.00"` define o texto inicial
        #       exibindo o valor total das vendas como 0.00.
        # `font=("Arial", 12, "bold")` define o texto em Arial, tamanho 12, em negrito.
        self.label_vendas = ttk.Label(quadro_totais,
                                      text="Total de Vendas: R$ 0.00",
                                      font=("Arial", 12, "bold"))

        # Posiciona o rótulo no lado esquerdo do quadro.
        # `side="left"` alinha o rótulo no lado esquerdo do quadro.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal ao redor do rótulo.
        self.label_vendas.pack(side="left", padx=10)

        # Cria um botão para exportar os dados para um arquivo Excel.
        # `text="Exportar para Excel"` define o texto exibido no botão.
        # `command=self.exportar_excel` associa a
        #       função `self.exportar_excel` ao clique do botão.
        ttk.Button(quadro_totais,
                   text="Exportar para Excel",
                   command=self.exportar_excel).pack(side="right", padx=10)

        # Carregar os dados
        self.listar()


    def listar(self):

        # Limpa os itens existentes na TreeView.
        # `self.tree.get_children()` retorna todos os itens da TreeView.
        # `self.tree.delete(i)` remove cada item da lista de itens da TreeView.
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Obtém os valores dos filtros aplicados.
        # `self.data_inicial.get_date()` retorna a data inicial selecionada no filtro.
        # `self.data_final.get_date()` retorna a data final selecionada no filtro.
        # `self.var_cliente.get().strip().lower()` obtém o valor do filtro de
        #       cliente, sem espaços e em letras minúsculas.
        # `self.var_produto.get().strip().lower()` obtém o valor do filtro de
        #       produto, sem espaços e em letras minúsculas.
        data_inicial = self.data_inicial.get_date()
        data_final = self.data_final.get_date()
        cliente_filtro = self.var_cliente.get().strip().lower()
        produto_filtro = self.var_produto.get().strip().lower()

        # Consulta todas as reservas no banco de dados.
        # `self.reserva.colecao_reservas.find()` retorna um
        #       cursor com todas as reservas da coleção.
        reservas = self.reserva.colecao_reservas.find()

        # Inicializa os contadores para vendas e registros.
        # `total_vendas` será usado para somar o total de vendas.
        # `total_registros` será usado para contar o número total de registros.
        total_vendas = 0
        total_registros = 0

        # Intera sobre a lista de reservas
        for r in reservas:

            # Tenta converter a data da reserva em um formato válido.
            # `r.get("data", "")` obtém a data da reserva em formato de string.
            # `datetime.strptime` converte a string para um objeto de data no formato "%d/%m/%Y".
            # `.date()` extrai apenas a parte da data.
            # Caso a data seja inválida, o bloco `except` ignora a reserva.
            try:
                data_reserva = datetime.strptime(r.get("data", ""), "%d/%m/%Y").date()
            except ValueError:
                continue

            # Verifica se a data da reserva está dentro do intervalo definido pelos filtros.
            # Se `data_reserva` não estiver entre `data_inicial` e `data_final`, ignora esta reserva.
            if not (data_inicial <= data_reserva <= data_final):
                continue

            # Inicializa a variável `nome_cliente` como uma string vazia.
            # Verifica se a reserva tem um ID de cliente associado.
            nome_cliente = ""
            if r.get("cliente_id"):

                # Consulta o banco de dados para obter os dados do cliente.
                # `self.reserva.colecao_clientes.find_one` retorna o
                #       cliente correspondente ao `cliente_id`.
                cli_doc = self.reserva.colecao_clientes.find_one({"_id": ObjectId(r["cliente_id"])})

                if cli_doc:

                    # Extrai o nome do cliente do documento encontrado.
                    nome_cliente = cli_doc.get("nome", "")

            # Verifica se o nome do cliente no filtro está contido no nome do cliente encontrado.
            # Se o filtro de cliente não for vazio e não corresponder ao nome do cliente, ignora esta reserva.
            if cliente_filtro and cliente_filtro not in nome_cliente.lower():
                continue

            # Itera sobre os itens consumidos na reserva atual.
            for item in r.get("itens_consumidos", []):

                # Obtém o ID do produto consumido.
                prod_id = item.get("produto_id")

                # Verifica se o produto possui um ID válido.
                if prod_id:

                    # Consulta o banco de dados para obter os detalhes do produto usando o `prod_id`.
                    produto_bd = self.reserva.colecao_produtos.find_one({"_id": ObjectId(prod_id)})

                    # Verifica se o produto foi encontrado no banco de dados.
                    if produto_bd:

                        # Obtém o ID do fornecedor associado ao produto.
                        forn_id = produto_bd.get("fornecedor_id")

                        # Verifica se o fornecedor do produto corresponde ao fornecedor atual.
                        if forn_id and str(forn_id) == str(self.fornecedor_id):

                            # Obtém o nome do produto consumido.
                            nome_produto = item.get("nome", "")

                            # Aplica o filtro de produto.
                            # Se o filtro de produto não for vazio e o nome do produto não
                            #       contiver o filtro, ignora este item.
                            if produto_filtro and produto_filtro not in nome_produto.lower():
                                continue

                            # Obtém a quantidade do item consumido.
                            qtd = item.get("qtd", 0)

                            # Obtém o preço de venda unitário do produto do banco de dados.
                            preco_venda = produto_bd.get("preco_venda", 0.0)

                            # Calcula o valor total das vendas para este item.
                            vendas = qtd * preco_venda

                            # Atualiza o total de vendas acumulado.
                            total_vendas += vendas

                            # Incrementa o contador total de registros.
                            total_registros += 1

                            # Insere os dados do item consumido na TreeView.
                            # `r.get("data", "")` insere a data da reserva.
                            # `nome_cliente` insere o nome do cliente associado à reserva.
                            # `nome_produto` insere o nome do produto consumido.
                            # `qtd` insere a quantidade consumida do produto.
                            # `f"{vendas:.2f}"` insere o valor formatado das vendas.
                            # `produto_bd.get("nome", "Fornecedor??")` insere o nome do fornecedor do produto.
                            self.tree.insert("",
                                        "end",
                                        values=(
                                            r.get("data", ""),
                                            nome_cliente,
                                            nome_produto,
                                            qtd,
                                            f"{vendas:.2f}",
                                            produto_bd.get("nome", "Fornecedor??")))

        # Atualiza o texto do rótulo que exibe o total de registros.
        # `text=f"Total de Registros: {total_registros}"` insere o número
        #       total de registros na interface.
        self.label_total.config(text=f"Total de Registros: {total_registros}")

        # Atualiza o texto do rótulo que exibe o valor total das vendas.
        # `text=f"Total de Vendas: R$ {total_vendas:.2f}"` insere o
        #       valor total das vendas formatado como moeda.
        self.label_vendas.config(text=f"Total de Vendas: R$ {total_vendas:.2f}")


    # Define o método para exportar os dados da TreeView para um arquivo Excel.
    def exportar_excel(self):

        # Abre uma janela para o usuário escolher onde salvar o arquivo Excel.
        # `defaultextension=".xlsx"` define a extensão padrão como `.xlsx`.
        # `filetypes` define os tipos de arquivo que o usuário pode salvar.
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
                                                 )

        # Verifica se o usuário selecionou um caminho de arquivo.
        # Se `file_path` for vazio, o usuário cancelou a operação.
        if not file_path:
            return

        # Inicializa uma lista para armazenar os dados da TreeView.
        data = []

        # Itera sobre todas as linhas da TreeView.
        # `self.tree.get_children()` retorna os IDs de todas as linhas na TreeView.
        for row_id in self.tree.get_children():

            # Pega os valores da linha correspondente usando o ID.
            row = self.tree.item(row_id)["values"]

            # Adiciona a linha à lista `data`.
            data.append(row)

        # Define os nomes das colunas que serão usadas no arquivo Excel.
        columns = ["Data", "Cliente", "Produto", "Quantidade", "Vendas", "Fornecedor"]

        # Cria um DataFrame do Pandas com os dados extraídos da TreeView.
        # `columns=columns` define os nomes das colunas no DataFrame.
        df = pd.DataFrame(data, columns=columns)

        # Exporta o DataFrame para um arquivo Excel no caminho especificado.
        # `index=False` evita que o índice seja salvo no arquivo.
        df.to_excel(file_path, index=False)

        # Exibe uma mensagem informando que a exportação foi concluída com sucesso.
        messagebox.showinfo("Exportação", "Dados exportados com sucesso!")


###############################################################################
#                PRODUTOS (CRUD + HISTÓRICO + DETALHE)                       #
###############################################################################
class JanelaProdutos:

    # Inicializa a classe `JanelaProdutos`.
    # `parent` é a janela pai onde esta janela será criada.
    # `reserva` é a instância da classe `ReservaQuadra` que gerencia os dados.
    def __init__(self, parent, reserva):

        # Define o atributo `parent` para armazenar a janela pai.
        self.parent = parent

        # Define o atributo `reserva` para acessar a lógica de manipulação de dados.
        self.reserva = reserva

        # Cria uma nova janela como filha da janela principal.
        # `tk.Toplevel(parent)` cria uma janela separada para
        #       gerenciamento de produtos.
        self.janela = tk.Toplevel(parent)

        # Define o título da janela.
        self.janela.title("Gerenciamento de Produtos")

        # Configura a janela para ser exibida no estado maximizado (zoomed).
        self.janela.state("zoomed")

        # Cria um quadro para o formulário de cadastro de produtos.
        # `ttk.LabelFrame` é um contêiner com uma borda e um título.
        # `text="Cadastro de Produtos"` define o título exibido no quadro.
        # `padding=10` adiciona espaçamento interno de 10 pixels ao redor do conteúdo.
        quadro_form = ttk.LabelFrame(self.janela, text="Cadastro de Produtos", padding=10)

        # Posiciona o quadro do formulário na janela.
        # `fill='x'` faz com que o quadro ocupe toda a largura disponível.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal externo.
        # `pady=10` adiciona 10 pixels de espaçamento vertical externo.
        quadro_form.pack(fill='x', padx=10, pady=10)

        # Cria um rótulo para o campo "Nome".
        # `text="Nome:"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `grid(row=0, column=0)` posiciona o rótulo na primeira
        #       linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='e'` alinha o rótulo à direita (leste) dentro da célula.
        ttk.Label(quadro_form,
                  text="Nome:",
                  font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de controle para armazenar o valor do campo "Nome".
        # `tk.StringVar()` cria uma variável de texto que será vinculada ao campo de entrada.
        self.var_nome = tk.StringVar()

        # Cria um campo de entrada para o nome do produto.
        # `textvariable=self.var_nome` vincula o valor do campo à variável `self.var_nome`.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `width=50` define a largura do campo de entrada.
        # `grid(row=0, column=1)` posiciona o campo de entrada na
        #       primeira linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e
        #       vertical de 5 pixels.
        ttk.Entry(quadro_form,
                  textvariable=self.var_nome,
                  font=("Arial", 12),
                  width=50).grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Categoria".
        # `text="Categoria:"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `grid(row=1, column=0)` posiciona o rótulo na segunda linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='e'` alinha o rótulo à direita (leste) dentro da célula.
        ttk.Label(quadro_form,
                  text="Categoria:",
                  font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de controle para armazenar o valor do campo "Categoria".
        # `tk.StringVar()` cria uma variável de texto que será vinculada ao campo de entrada.
        self.var_categoria = tk.StringVar()

        # Cria um campo de entrada para a categoria do produto.
        # `textvariable=self.var_categoria` vincula o valor do campo à variável `self.var_categoria`.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `width=50` define a largura do campo de entrada.
        # `grid(row=1, column=1)` posiciona o campo de entrada na
        #       segunda linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        ttk.Entry(quadro_form,
                  textvariable=self.var_categoria,
                  font=("Arial", 12), width=50).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Fornecedor".
        # `text="Fornecedor:"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `grid(row=2, column=0)` posiciona o rótulo na terceira linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='e'` alinha o rótulo à direita (leste) dentro da célula.
        ttk.Label(quadro_form,
                  text="Fornecedor:",
                  font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky='e')

        # Cria um campo combobox (menu suspenso) para selecionar o fornecedor.
        # `state="readonly"` impede a edição direta, permitindo apenas a seleção de opções da lista.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `width=48` define a largura do combobox.
        # `grid(row=2, column=1)` posiciona o combobox na terceira linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        self.combo_fornecedor = ttk.Combobox(quadro_form, state="readonly", font=("Arial", 12), width=48)
        self.combo_fornecedor.grid(row=2, column=1, padx=5, pady=5)

        # Cria um dicionário vazio para mapear os nomes dos fornecedores aos seus IDs.
        # `self.mapa_fornecedores` será preenchido posteriormente
        #       para facilitar a associação de valores.
        self.mapa_fornecedores = {}

        # Chama o método `carregar_fornecedores` para preencher o
        #       combobox com os fornecedores disponíveis.
        self.carregar_fornecedores()

        # Cria um rótulo para o campo "Preço Venda (R$)".
        # `text="Preço Venda (R$):"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `grid(row=3, column=0)` posiciona o rótulo na quarta linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='e'` alinha o rótulo à direita (leste) dentro da célula.
        ttk.Label(quadro_form,
                  text="Preço Venda (R$):",
                font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável para armazenar o valor do preço de venda.
        # `self.var_preco_venda` será vinculada ao campo de entrada e utilizada no código.
        self.var_preco_venda = tk.StringVar()

        # Cria um campo de entrada para o preço de venda.
        # `textvariable=self.var_preco_venda` vincula o valor do
        #       campo à variável `self.var_preco_venda`.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `width=15` define a largura do campo de entrada.
        # `grid(row=3, column=1)` posiciona o campo na quarta linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='w'` alinha o campo à esquerda (oeste) dentro da célula.
        ttk.Entry(quadro_form,
                  textvariable=self.var_preco_venda,
                  font=("Arial", 12),
                  width=15).grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Cria um rótulo para o campo "Preço Custo (R$)".
        # `text="Preço Custo (R$):"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `grid(row=4, column=0)` posiciona o rótulo na quinta linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='e'` alinha o rótulo à direita (leste) dentro da célula.
        ttk.Label(quadro_form,
                  text="Preço Custo (R$):",
                  font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável para armazenar o valor do preço de custo.
        # `self.var_preco_custo` será vinculada ao campo de entrada e utilizada no código.
        self.var_preco_custo = tk.StringVar()

        # Cria um campo de entrada para o preço de custo.
        # `textvariable=self.var_preco_custo` vincula o campo à
        #       variável `self.var_preco_custo`.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `width=15` define a largura do campo de entrada.
        # `grid(row=4, column=1)` posiciona o campo na quinta linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='w'` alinha o campo à esquerda (oeste) dentro da célula.
        ttk.Entry(quadro_form,
                  textvariable=self.var_preco_custo,
                  font=("Arial", 12), width=15).grid(row=4,
                                                     column=1,
                                                     padx=5,
                                                     pady=5,
                                                     sticky='w')

        # Cria um rótulo para o campo "Estoque".
        # `text="Estoque:"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `grid(row=5, column=0)` posiciona o rótulo na sexta linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='e'` alinha o rótulo à direita (leste) dentro da célula.
        ttk.Label(quadro_form,
                  text="Estoque:",
                  font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável para armazenar o valor do estoque.
        # `self.var_estoque` será vinculada ao campo de entrada e utilizada no código.
        self.var_estoque = tk.StringVar()

        # Cria um campo de entrada para o preço de custo.
        # `textvariable=self.var_estoque` vincula o campo à variável `self.var_estoque`.
        # `font=("Arial", 12)` define a fonte Arial com tamanho 12.
        # `width=15` define a largura do campo de entrada.
        # `grid(row=4, column=1)` posiciona o campo na quinta linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo horizontal e vertical de 5 pixels.
        # `sticky='w'` alinha o campo à esquerda (oeste) dentro da célula.
        ttk.Entry(quadro_form,
                  textvariable=self.var_estoque,
                  font=("Arial", 12),
                  width=15).grid(row=5, column=1, padx=5, pady=5, sticky='w')


        # Cria um rótulo para o campo "Estoque Mínimo", com a fonte
        #       configurada para "Arial", tamanho 12
        # O `text="Estoque Mínimo:"` define o texto exibido no rótulo.
        # `font=("Arial", 12)` define a fonte como Arial e o tamanho da fonte como 12.
        # `sticky='e'` alinha o rótulo à direita (East) da célula da grid.
        # `padx=5` e `pady=5` adicionam espaçamento de 5 pixels na
        #       horizontal e vertical, respectivamente.
        ttk.Label(quadro_form,
                  text="Estoque Mínimo:",
                  font=("Arial", 12)).grid(row=6,
                                           column=0,
                                           padx=5,
                                           pady=5,
                                           sticky='e')

        # Cria uma variável do tipo StringVar para armazenar o valor do "Estoque Mínimo".
        # O `StringVar()` é usado para associar uma variável a um
        #       widget (neste caso, ao campo de entrada do estoque mínimo).
        self.var_estoque_min = tk.StringVar()

        # Cria um campo de entrada para o valor mínimo do estoque.
        # `textvariable=self.var_estoque_min` vincula o campo de
        #       entrada à variável `self.var_estoque_min`.
        # `font=("Arial", 12)` define a fonte do texto dentro do campo como Arial com tamanho 12.
        # `width=15` define a largura do campo de entrada como 15 caracteres.
        # `grid(row=6, column=1)` posiciona o campo na sétima linha e na segunda coluna do quadro.
        # `padx=5` adiciona um espaçamento horizontal de 5 pixels ao redor do campo.
        # `pady=5` adiciona um espaçamento vertical de 5 pixels ao redor do campo.
        # `sticky='w'` alinha o campo à esquerda (w = west) dentro da célula da grade.
        ttk.Entry(quadro_form,
                  textvariable=self.var_estoque_min,
                  font=("Arial", 12),
                  width=15).grid(row=6,
                                 column=1,
                                 padx=5,
                                 pady=5,
                                 sticky='w')


        # Cria um quadro para agrupar os botões do formulário.
        # `ttk.Frame(quadro_form)` cria um container dentro do quadro do formulário.
        # `grid(row=7, column=0, columnspan=2)` posiciona o quadro na
        #       oitava linha e faz com que ele ocupe as duas colunas.
        # `pady=10` adiciona um espaçamento vertical de 10 pixels acima e abaixo do quadro.
        quadro_botoes_form = ttk.Frame(quadro_form)
        quadro_botoes_form.grid(row=7, column=0, columnspan=2, pady=10)

        # Cria um botão para cadastrar o produto.
        # `text="Cadastrar"` define o texto exibido no botão.
        # `command=self.cadastrar` associa o método `self.cadastrar` à ação de clique no botão.
        # `width=15` define a largura do botão como 15 caracteres.
        # `grid(row=0, column=0)` posiciona o botão na primeira linha e
        #       primeira coluna do quadro de botões.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Cadastrar",
                   command=self.cadastrar,
                   width=15).grid(row=0, column=0, padx=10)

        # Cria um botão para alterar os dados de um produto selecionado.
        # `text="Alterar"` define o texto exibido no botão.
        # `command=self.alterar` associa o método `self.alterar` à ação de clique no botão.
        # `width=15` define a largura do botão como 15 caracteres.
        # `grid(row=0, column=1)` posiciona o botão na primeira linha e
        #       segunda coluna do quadro de botões.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Alterar",
                   command=self.alterar, width=15).grid(row=0, column=1, padx=10)

        # Cria um botão para excluir um produto selecionado.
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir` associa o método `self.excluir` à ação de clique no botão.
        # `width=15` define a largura do botão como 15 caracteres.
        # `grid(row=0, column=2)` posiciona o botão na primeira linha e
        #       terceira coluna do quadro de botões.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Excluir",
                   command=self.excluir,
                   width=15).grid(row=0, column=2, padx=10)

        # Cria um botão para limpar os campos do formulário.
        # `text="Limpar"` define o texto exibido no botão.
        # `command=self.limpar` associa o método `self.limpar` à ação de clique no botão.
        # `width=10` define a largura do botão como 10 caracteres.
        # `grid(row=0, column=3)` posiciona o botão na primeira linha e
        #       quarta coluna do quadro de botões.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Limpar",
                   command=self.limpar, width=10).grid(row=0, column=3, padx=10)

        # Cria um botão para abrir o histórico de um produto.
        # `text="Histórico"` define o texto exibido no botão.
        # `command=self.abrir_historico_produto` associa o
        #       método `self.abrir_historico_produto` à ação de clique no botão.
        # `width=15` define a largura do botão como 15 caracteres.
        # `grid(row=0, column=4)` posiciona o botão na primeira linha e
        #       quinta coluna do quadro de botões.
        # `padx=10` adiciona um espaçamento horizontal de 10 pixels ao redor do botão.
        ttk.Button(quadro_botoes_form,
                   text="Histórico",
                   command=self.abrir_historico_produto,
                   width=15).grid(row=0, column=4, padx=10)

        # Quadro da Tabela
        # Cria um quadro para exibir a tabela de produtos.
        # `text="Lista de Produtos"` define o título do quadro.
        # `padding=10` adiciona um espaçamento interno de 10 pixels ao redor do conteúdo do quadro.
        quadro_tabela = ttk.LabelFrame(self.janela, text="Lista de Produtos", padding=10)

        # `pack(fill='both', expand=True, padx=10, pady=10)`:
        # - `fill='both'` expande o quadro para preencher tanto horizontal quanto verticalmente.
        # - `expand=True` permite que o quadro expanda dinamicamente dentro do layout.
        # - `padx=10, pady=10` adicionam espaçamento externo de 10 pixels em torno do quadro.
        quadro_tabela.pack(fill='both', expand=True, padx=10, pady=10)

        # Cria um Treeview para exibir os dados da tabela.
        # `columns` define os nomes das colunas que serão exibidas.
        # `show='headings'` exibe apenas os cabeçalhos das
        #       colunas, sem a coluna de índice padrão.
        # `height=15` define o número de linhas visíveis inicialmente.
        self.tree = ttk.Treeview( quadro_tabela,
                                columns=("Nome", "Cat", "Fornecedor", "PVenda", "PCusto", "Est", "EstMin"),
                                show='headings',
                                height=15)

        # Define o texto exibido nos cabeçalhos das colunas do Treeview.
        # `self.tree.heading("Nome", text="Nome")`:
        #   Define o cabeçalho da coluna "Nome" com o texto "Nome".
        self.tree.heading("Nome", text="Nome")

        # Define o cabeçalho da coluna "Cat" com o texto "Categoria".
        self.tree.heading("Cat", text="Categoria")

        # Define o cabeçalho da coluna "Fornecedor" com o texto "Fornecedor".
        self.tree.heading("Fornecedor", text="Fornecedor")

        # Define o cabeçalho da coluna "PVenda" com o texto "Preço Venda".
        self.tree.heading("PVenda", text="Preço Venda")

        # Define o cabeçalho da coluna "PCusto" com o texto "Preço Custo".
        self.tree.heading("PCusto", text="Preço Custo")

        # Define o cabeçalho da coluna "Est" com o texto "Estoque".
        self.tree.heading("Est", text="Estoque")

        # Define o cabeçalho da coluna "EstMin" com o texto "Estoque Min".
        self.tree.heading("EstMin", text="Estoque Min")

        # Adiciona o Treeview ao layout da janela.
        # `pack(fill='both', expand=True, padx=10, pady=10)`:
        # - `fill='both'` permite que o Treeview preencha o espaço
        #       disponível horizontal e verticalmente.
        # - `expand=True` permite que o Treeview se expanda conforme o layout disponível.
        # - `padx=10, pady=10` adicionam espaçamento externo de 10 pixels em torno do Treeview.
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Ajustando estilo da TreeView
        # Cria um objeto de estilo para personalizar os componentes visuais.
        # `style = ttk.Style()`: Cria uma instância de `ttk.Style`.
        style = ttk.Style()

        # Configura a fonte das linhas do Treeview.
        # `style.configure("Treeview", font=("Arial", 12))`:
        #   Define a fonte como "Arial", tamanho 12, para os itens do Treeview.
        style.configure("Treeview", font=("Arial", 12))

        # Configura a fonte do cabeçalho do Treeview.
        # `style.configure("Treeview.Heading", font=("Arial", 12, "bold"))`:
        #   Define a fonte como "Arial", tamanho 12, e em negrito para os cabeçalhos das colunas.
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Define ações ao interagir com o Treeview.
        # `self.tree.bind("<ButtonRelease-1>", self.selecionar_item)`:
        #   Associa o evento de "soltar o botão esquerdo do mouse" a um
        #           método chamado `self.selecionar_item`.
        #   Esse método é chamado sempre que o usuário clica em um item na tabela.
        self.tree.bind("<ButtonRelease-1>", self.selecionar_item)

        # `self.tree.bind("<Double-1>", self.abrir_historico_produto)`:
        #   Associa o evento de "clique duplo do botão esquerdo do mouse" ao
        #           método `self.abrir_historico_produto`.
        #   Esse método é chamado para abrir o histórico do produto
        #           selecionado na tabela.
        self.tree.bind("<Double-1>", self.abrir_historico_produto)

        # Chama o método `self.listar()` para preencher a tabela com os dados iniciais.
        # `self.listar()` carrega os produtos no Treeview.
        self.listar()


    # Define a função `listar`, que preenche a Treeview com os
    #       produtos cadastrados no banco de dados.
    def listar(self):

        # Remove todos os itens atuais da Treeview para evitar duplicação.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca todos os produtos cadastrados na coleção de produtos do banco de dados.
        prods = self.reserva.colecao_produtos.find()

        # Itera por cada produto encontrado no banco de dados.
        for p in prods:

            # Inicializa a variável `forn_nome` como uma string vazia.
            # Ela armazenará o nome do fornecedor.
            forn_nome = ""

            # Verifica se o produto possui um ID de fornecedor associado.
            if p.get("fornecedor_id"):

                # Busca o fornecedor correspondente no banco de dados
                #       usando o ID armazenado no produto.
                forn = self.reserva.colecao_fornecedores.find_one({"_id": p["fornecedor_id"]})

                # Se o fornecedor for encontrado, armazena o nome do fornecedor em `forn_nome`.
                if forn:
                    forn_nome = forn.get("nome", "")

            # Insere os dados do produto na Treeview para exibição.
            self.tree.insert(

                "",  # Insere no nível superior da Treeview (sem pai).
                "end",  # Adiciona no final da lista atual.
                iid=str(p["_id"]),  # Define um identificador único para cada linha, baseado no ID do produto.

                values=(

                    # Recupera o nome do produto, ou usa uma string vazia
                    #       se o valor estiver ausente.
                    p.get("nome", ""),

                    # Recupera a categoria do produto, ou usa uma string
                    #       vazia se o valor estiver ausente.
                    p.get("categoria", ""),

                    # Usa o nome do fornecedor recuperado anteriormente.
                    forn_nome,

                    # Recupera o preço de venda do produto, ou usa 0.0 como valor padrão.
                    p.get("preco_venda", 0.0),

                    # Recupera o preço de custo do produto, ou usa 0.0 como valor padrão.
                    p.get("preco_custo", 0.0),

                    # Recupera o estoque atual do produto, ou usa 0 como valor padrão.
                    p.get("estoque", 0),

                    # Recupera o estoque mínimo do produto, ou usa 0 como valor padrão.
                    p.get("estoque_minimo", 0)

                )
            )


    def selecionar_item(self, event):

        # Obtém os itens selecionados no Treeview.
        # `self.tree.selection()` retorna uma tupla com os IDs
        #       dos itens selecionados.
        selecionado = self.tree.selection()

        # Verifica se não há nenhum item selecionado.
        # Caso não haja, exibe uma mensagem de aviso e retorna.
        # `messagebox.showwarning` exibe uma caixa de diálogo de aviso com o título "Aviso".
        # O texto da mensagem é "Nenhum item selecionado.", com a janela principal como parent.
        if not selecionado:
            messagebox.showwarning("Aviso", "Nenhum item selecionado.", parent=self.janela)
            return

        # Obtém o ID do item selecionado.
        # `selecionado[0]` retorna o primeiro item da seleção (se houver mais de um).
        item_id = selecionado[0]

        # Obtém os valores associados ao item selecionado.
        # `self.tree.item(item_id, "values")` retorna os valores das
        #       colunas do item com o ID especificado.
        valores = self.tree.item(item_id, "values")

        # Preenche o campo de entrada do nome do produto.
        # `self.var_nome.set(valores[0])` define o primeiro valor do item
        #       selecionado (nome do produto) no campo correspondente.
        self.var_nome.set(valores[0])

        # Preenche o campo de entrada da categoria.
        # `self.var_categoria.set(valores[1])` define o segundo valor do item
        #       selecionado (categoria do produto) no campo correspondente.
        self.var_categoria.set(valores[1])

        # Preenche o combobox de fornecedor com o valor do fornecedor associado ao item selecionado.
        # `self.combo_fornecedor.set(valores[2])` define o terceiro valor do
        #       item selecionado (fornecedor) no combobox.
        self.combo_fornecedor.set(valores[2])

        # Preenche o campo de entrada do preço de venda.
        # `self.var_preco_venda.set(valores[3])` define o quarto valor do item
        #       selecionado (preço de venda) no campo correspondente.
        self.var_preco_venda.set(valores[3])

        # Preenche o campo de entrada do preço de custo.
        # `self.var_preco_custo.set(valores[4])` define o quinto valor do item
        #       selecionado (preço de custo) no campo correspondente.
        self.var_preco_custo.set(valores[4])

        # Preenche o campo de entrada do estoque atual.
        # `self.var_estoque.set(valores[5])` define o sexto valor do item
        #       selecionado (estoque atual) no campo correspondente.
        self.var_estoque.set(valores[5])

        # Preenche o campo de entrada do estoque mínimo.
        # `self.var_estoque_min.set(valores[6])` define o sétimo valor do
        #       item selecionado (estoque mínimo) no campo correspondente.
        self.var_estoque_min.set(valores[6])


    def cadastrar(self):

        # Obtém o valor do campo de nome do produto, removendo espaços extras.
        nome = self.var_nome.get().strip()

        # Obtém o valor do campo de categoria do produto, removendo espaços extras.
        cat = self.var_categoria.get().strip()

        # Obtém o nome do fornecedor selecionado no combobox, removendo espaços extras.
        forn_nome = self.combo_fornecedor.get().strip()

        # Verifica se o fornecedor selecionado está no mapa de fornecedores.
        # Caso contrário, exibe uma mensagem de aviso ao usuário.
        if forn_nome not in self.mapa_fornecedores:

            messagebox.showwarning("Aviso",
                                "Fornecedor inválido ou não encontrado.",
                                parent=self.janela)
            return

        # Obtém o ID do fornecedor a partir do mapa de fornecedores.
        forn_id = self.mapa_fornecedores[forn_nome]

        # Obtém o valor do campo de preço de venda, removendo espaços extras.
        pv_str = self.var_preco_venda.get().strip()

        # Obtém o valor do campo de preço de custo, removendo espaços extras.
        pc_str = self.var_preco_custo.get().strip()

        # Obtém o valor do campo de estoque, removendo espaços extras.
        est_str = self.var_estoque.get().strip()

        # Obtém o valor do campo de estoque mínimo, removendo espaços extras.
        estmin_str = self.var_estoque_min.get().strip()

        # Verifica se o nome do produto foi preenchido.
        # Caso contrário, exibe uma mensagem de aviso ao usuário.
        if not nome:

            messagebox.showwarning( "Aviso",
                            "Nome do produto é obrigatório.",
                            parent=self.janela)
            return

        try:

            # Converte o valor de preço de venda para float.
            pvenda = float(pv_str)

            # Converte o valor de preço de custo para float.
            pcusto = float(pc_str)

            # Converte o valor de estoque para inteiro.
            est_i = int(est_str)

            # Converte o valor de estoque mínimo para inteiro.
            estmin_i = int(estmin_str)

        except:

            # Exibe uma mensagem de aviso caso ocorra erro nas conversões numéricas.
            messagebox.showwarning("Aviso",
                            "Valores numéricos inválidos.",
                            parent=self.janela)
            return


        # Cria um dicionário contendo os dados do produto para cadastro.
        # O dicionário inclui nome, categoria, ID do fornecedor, preços, estoque e estoque mínimo.
        doc_prod = {
            "nome": nome,
            "categoria": cat,
            "fornecedor_id": ObjectId(forn_id),  # Converte o ID do fornecedor para ObjectId.
            "preco_venda": pvenda,  # Preço de venda do produto.
            "preco_custo": pcusto,  # Preço de custo do produto.
            "estoque": est_i,  # Quantidade em estoque do produto.
            "estoque_minimo": estmin_i  # Estoque mínimo do produto.

        }


        # Insere o dicionário do produto na coleção de produtos do banco de dados.
        self.reserva.colecao_produtos.insert_one(doc_prod)

        # Exibe uma mensagem de sucesso ao usuário indicando que o produto foi cadastrado.
        messagebox.showinfo( "Sucesso",
                    "Produto cadastrado!",
                    parent=self.janela)

        # Atualiza a lista de produtos exibida na interface.
        self.listar()

        # Limpa os campos do formulário de cadastro de produtos.
        self.limpar()



    def alterar(self):

        # Verifica se algum item foi selecionado na Treeview.
        # Se nenhum item foi selecionado, exibe uma mensagem de aviso.
        sel = self.tree.selection()
        if not sel:

            messagebox.showwarning("Aviso",
                                "Selecione um produto para alterar.",
                                parent=self.janela)  # Define a janela atual como pai da mensagem.

            # Interrompe o fluxo da função, já que nenhuma seleção foi feita.
            return

        # Obtém o ID do item selecionado na Treeview.
        iid = sel[0]

        # Obtém o nome do produto a partir do campo de entrada e remove espaços extras.
        nome = self.var_nome.get().strip()

        # Obtém a categoria do produto e remove espaços extras.
        cat = self.var_categoria.get().strip()

        # Obtém o nome do fornecedor selecionado no Combobox e remove espaços extras.
        forn_nome = self.combo_fornecedor.get().strip()

        # Verifica se o fornecedor selecionado é válido.
        # Caso contrário, exibe uma mensagem de aviso.
        if forn_nome not in self.mapa_fornecedores:

            messagebox.showwarning("Aviso",
                        "Fornecedor inválido.",
                        parent=self.janela)  # Define a janela atual como pai da mensagem.

            # Interrompe o fluxo da função, pois o fornecedor não é válido.
            return

        # Obtém o ID do fornecedor a partir do mapa de fornecedores.
        forn_id = self.mapa_fornecedores[forn_nome]

        # Obtém o preço de venda como string e remove espaços em branco extras.
        pv_str = self.var_preco_venda.get().strip()

        # Obtém o preço de custo como string e remove espaços em branco extras.
        pc_str = self.var_preco_custo.get().strip()

        # Obtém o estoque atual como string e remove espaços em branco extras.
        est_str = self.var_estoque.get().strip()

        # Obtém o estoque mínimo como string e remove espaços em branco extras.
        estmin_str = self.var_estoque_min.get().strip()

        try:

            # Converte o preço de venda para float. Se falhar, levanta um ValueError.
            pvenda = float(pv_str)

            # Converte o preço de custo para float. Se falhar, levanta um ValueError.
            pcusto = float(pc_str)

            # Converte o estoque atual para inteiro. Se falhar, levanta um ValueError.
            est_i = int(est_str)

            # Converte o estoque mínimo para inteiro. Se falhar, levanta um ValueError.
            estmin_i = int(estmin_str)

        except:

            # Exibe uma mensagem de aviso se qualquer uma das conversões falhar.
            messagebox.showwarning( "Aviso",
                            "Valores numéricos inválidos.",
                            parent=self.janela)  # Define a janela atual como pai da mensagem.

            # Interrompe o fluxo da função em caso de erro nas conversões.
            return

        # Cria um dicionário com os valores atualizados do produto.
        doc_update = {

            # Define o nome do produto.
            "nome": nome,

            # Define a categoria do produto.
            "categoria": cat,

            # Define o ID do fornecedor como um ObjectId.
            "fornecedor_id": ObjectId(forn_id),

            # Define o preço de venda atualizado.
            "preco_venda": pvenda,

            # Define o preço de custo atualizado.
            "preco_custo": pcusto,

            # Define a quantidade atualizada de estoque.
            "estoque": est_i,

            # Define o estoque mínimo atualizado.
            "estoque_minimo": estmin_i

        }

        # Atualiza o documento do produto no banco de dados.
        self.reserva.colecao_produtos.update_one(

            # Filtra pelo ID do produto selecionado.
            {"_id": ObjectId(iid)},

            # Define os novos valores a serem atualizados.
            {"$set": doc_update}

        )

        # Exibe uma mensagem informando que o produto foi alterado com sucesso.
        messagebox.showinfo( "OK",
                    "Produto alterado!",
                    parent=self.janela)  # Define a janela atual como pai da mensagem.

        # Atualiza a lista de produtos na interface após a alteração.
        self.listar()

        # Limpa os campos do formulário para novos cadastros ou alterações.
        self.limpar()



    def excluir(self):

        # Obtém o item selecionado na Treeview.
        sel = self.tree.selection()

        # Verifica se nenhum item foi selecionado.
        if not sel:

            # Exibe um aviso ao usuário caso nenhum item esteja selecionado.
            messagebox.showwarning("Aviso",
                        "Selecione um produto para excluir.",
                        parent=self.janela)  # Define a janela atual como pai da mensagem.

            return

        # Obtém o ID do item selecionado.
        iid = sel[0]

        # Remove o produto do banco de dados usando o ID selecionado.
        self.reserva.colecao_produtos.delete_one({"_id": ObjectId(iid)})

        # Exibe uma mensagem de sucesso ao usuário informando que o produto foi excluído.
        messagebox.showinfo("OK",
                    "Produto excluído!",
                            parent=self.janela)  # Define a janela atual como pai da mensagem.

        # Atualiza a lista de produtos exibidos na Treeview.
        self.listar()

        # Limpa os campos do formulário.
        self.limpar()


    # Define a função `limpar` que é responsável por redefinir os
    #       valores dos campos de entrada do formulário.
    def limpar(self):

        # Limpa o campo do nome do produto, definindo-o como uma string vazia.
        self.var_nome.set("")

        # Limpa o campo da categoria do produto, definindo-o como uma string vazia.
        self.var_categoria.set("")

        # Verifica se há valores disponíveis na combobox de fornecedores.
        # Se houver, define o fornecedor padrão como o primeiro da lista.
        if self.combo_fornecedor["values"]:
            self.combo_fornecedor.current(0)

        # Limpa o campo do preço de venda, definindo-o como uma string vazia.
        self.var_preco_venda.set("")

        # Limpa o campo do preço de custo, definindo-o como uma string vazia.
        self.var_preco_custo.set("")

        # Limpa o campo do estoque, definindo-o como uma string vazia.
        self.var_estoque.set("")

        # Limpa o campo do estoque mínimo, definindo-o como uma string vazia.
        self.var_estoque_min.set("")


    def carregar_fornecedores(self):

        # Busca todos os fornecedores na coleção do banco de dados.
        fornecs = self.reserva.colecao_fornecedores.find()

        # Cria uma lista para armazenar os nomes dos fornecedores.
        lista_nomes = []

        # Itera por todos os documentos (fornecedores) retornados pela consulta.
        for forn in fornecs:

            # Obtém o nome do fornecedor do campo "nome". Se não existir, usa "Sem Nome".
            nome = forn.get("nome", "Sem Nome")

            # Converte o ID do fornecedor para string e o armazena.
            _id = str(forn["_id"])

            # Adiciona o nome do fornecedor à lista de nomes.
            lista_nomes.append(nome)

            # Armazena o ID do fornecedor no dicionário `self.mapa_fornecedores` com o nome como chave.
            self.mapa_fornecedores[nome] = _id

        # Define os valores do combobox com os nomes dos fornecedores.
        self.combo_fornecedor["values"] = lista_nomes

        # Se houver nomes na lista, seleciona o primeiro fornecedor como padrão.
        if lista_nomes:
            self.combo_fornecedor.current(0)


    def abrir_historico_produto(self, event=None):

        # Verifica se há algum item selecionado na Treeview.
        sel = self.tree.selection()

        # Caso não tenha nenhum item selecionado, retorna e não executa nada.
        if not sel:
            return

        # Obtém o ID (identificador único) do item selecionado.
        iid = sel[0]

        # Cria uma nova janela para exibir o histórico detalhado do produto selecionado,
        # passando a janela atual (`self.janela`), o objeto de reserva (`self.reserva`),
        # e o ID do produto selecionado.
        JanelaHistoricoProdutosDetalhe(self.janela, self.reserva, iid)



###############################################################################
#                  HISTÓRICO DE PRODUTOS (DETALHE)                            #
###############################################################################
class JanelaHistoricoProdutosDetalhe:

    # Inicializa a janela de histórico de detalhes de produtos.
    # `parent` é a janela principal, `reserva` é a instância do
    #       sistema de reserva e `produto_id_str` é o ID do produto em formato de string.
    def __init__(self, parent, reserva, produto_id_str):

        # Armazena a referência da janela principal.
        self.parent = parent

        # Armazena a instância do sistema de reserva.
        self.reserva = reserva

        # Converte o ID do produto de string para um objeto ObjectId do MongoDB e armazena.
        self.produto_id = ObjectId(produto_id_str)

        # Configurando a janela principal
        # Cria uma nova janela como filha da janela principal (`parent`).
        self.janela = tk.Toplevel(parent)

        # Define o título da janela.
        self.janela.title("Histórico de Reservas para este Produto")

        # Configura o estado da janela para ocupar toda a tela (maximizada).
        self.janela.state("zoomed")

        # Quadro superior - Filtros
        # Cria um quadro de filtros dentro da janela para agrupar elementos de filtragem.
        # `text="Filtros"` define o título do quadro como "Filtros".
        # `padding=10` adiciona 10 pixels de preenchimento interno ao quadro.
        quadro_filtros = ttk.LabelFrame(self.janela, text="Filtros", padding=10)

        # Posiciona o quadro no layout da janela, preenchendo
        #       horizontalmente e com espaçamento externo.
        # `fill="x"` faz com que o quadro preencha todo o espaço horizontal disponível.
        # `padx=10` e `pady=10` adicionam espaçamento externo de 10 pixels
        #       nas direções horizontal e vertical.
        quadro_filtros.pack(fill="x", padx=10, pady=10)

        # Filtro de datas
        # Cria um rótulo para o campo "Data Inicial".
        # `text="Data Inicial:"` define o texto exibido no rótulo.
        # `grid` posiciona o rótulo na primeira linha (row=0) e primeira coluna (column=0).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de seleção de data para "Data Inicial".
        # `date_pattern="dd/MM/yyyy"` define o formato de exibição da data.
        # `width=12` define a largura do campo.
        self.dt_ini = DateEntry(quadro_filtros, date_pattern="dd/MM/yyyy", width=12)

        # Posiciona o campo de seleção de data na primeira
        #       linha (row=0) e segunda coluna (column=1).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do campo.
        self.dt_ini.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo "Data Final".
        # `text="Data Final:"` define o texto exibido no rótulo.
        # `grid` posiciona o rótulo na primeira linha (row=0) e terceira coluna (column=2).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Data Final:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Cria um campo de seleção de data para "Data Final".
        # `date_pattern="dd/MM/yyyy"` define o formato de exibição da data.
        # `width=12` define a largura do campo.
        self.dt_fim = DateEntry(quadro_filtros, date_pattern="dd/MM/yyyy", width=12)

        # Posiciona o campo de seleção de data na primeira
        #       linha (row=0) e quarta coluna (column=3).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do campo.
        self.dt_fim.grid(row=0, column=3, padx=5, pady=5)

        # Filtro de Lugar
        # Cria um rótulo para o campo "Lugar".
        # `text="Lugar:"` define o texto exibido no rótulo.
        # `grid` posiciona o rótulo na segunda linha (row=1) e primeira coluna (column=0).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Lugar:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria uma variável de texto para armazenar o valor do campo "Lugar".
        # `self.var_lugar` é a variável associada ao campo de entrada.
        self.var_lugar = tk.StringVar()

        # Cria um campo de entrada de texto para o filtro "Lugar".
        # `textvariable=self.var_lugar` vincula o valor do campo à
        #       variável `self.var_lugar`.
        # `width=20` define a largura do campo de entrada.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_lugar,
                  width=20).grid(row=1, column=1, padx=5, pady=5)

        # Filtro de Cliente
        # Cria um rótulo para o campo "Cliente".
        # `text="Cliente:"` define o texto exibido no rótulo.
        # `grid` posiciona o rótulo na segunda linha (row=1) e terceira coluna (column=2).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Cliente:").grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Cria uma variável de texto para armazenar o valor do campo "Cliente".
        # `self.var_cliente` é a variável associada ao campo de entrada.
        self.var_cliente = tk.StringVar()

        # Cria um campo de entrada de texto para o filtro "Cliente".
        # `textvariable=self.var_cliente` vincula o valor do
        #       campo à variável `self.var_cliente`.
        # `width=20` define a largura do campo de entrada.
        # `grid` posiciona o campo na segunda linha (row=1) e quarta coluna (column=3).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do campo.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_cliente,
                  width=20).grid(row=1, column=3, padx=5, pady=5)

        # Filtro de Produto
        # Cria um rótulo para o campo "Produto".
        # `text="Produto:"` define o texto exibido no rótulo.
        # `grid` posiciona o rótulo na segunda linha (row=1) e quinta coluna (column=4).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do rótulo.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Produto:").grid(row=1, column=4, padx=5, pady=5, sticky="e")

        # Cria uma variável de texto para armazenar o valor do campo "Produto".
        # `self.var_produto` é a variável associada ao campo de entrada.
        self.var_produto = tk.StringVar()

        # Cria um campo de entrada de texto para o filtro "Produto".
        # `textvariable=self.var_produto` vincula o valor do campo à variável `self.var_produto`.
        # `width=20` define a largura do campo de entrada.
        # `grid` posiciona o campo na segunda linha (row=1) e sexta coluna (column=5).
        # `padx=5` e `pady=5` adicionam espaçamento externo ao redor do campo.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_produto,
                  width=20).grid(row=1, column=5, padx=5, pady=5)

        # Botões de Ação
        # Cria um botão para aplicar filtros.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a ação de filtrar os dados ao clicar no botão.
        # `grid` posiciona o botão na terceira linha (row=2) e primeira coluna (column=0).
        # `padx=10` e `pady=5` adicionam espaçamento externo ao redor do botão.
        ttk.Button(quadro_filtros,
                   text="Filtrar",
                   command=self.filtrar).grid(row=2, column=0, padx=10, pady=5)

        # Cria um botão para exportar os dados para Excel.
        # `text="Exportar para Excel"` define o texto exibido no botão.
        # `command=self.exportar_excel` associa a ação de exportar os dados ao clicar no botão.
        # `grid` posiciona o botão na terceira linha (row=2) e segunda coluna (column=1).
        # `padx=10` e `pady=5` adicionam espaçamento externo ao redor do botão.
        ttk.Button(quadro_filtros,
                   text="Exportar para Excel",
                   command=self.exportar_excel).grid(row=2,
                                                     column=1,
                                                     padx=10,
                                                     pady=5)

        # Quadro da tabela
        # Cria um quadro para exibir a tabela com os detalhes das reservas do produto.
        # `text="Detalhes de Reservas para o Produto"` define o título do quadro.
        # `padding=10` adiciona espaçamento interno ao quadro.
        # `pack(fill="both", expand=True, padx=10, pady=10)` ajusta o
        #       quadro para preencher o espaço disponível,
        # permitindo expansão tanto horizontal quanto vertical, e adiciona espaçamento externo.
        quadro_tabela = ttk.LabelFrame(self.janela,
                                       text="Detalhes de Reservas para o Produto",
                                       padding=10)

        quadro_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria uma Treeview para exibir as colunas de detalhes das reservas.
        # `columns=("Data", "Lugar", "Cliente", "Produto", "Qtd", "PreçoUn", "Total")`
        #       define as colunas da tabela.
        # `show='headings'` exibe apenas os cabeçalhos, sem uma coluna inicial extra.
        self.tree = ttk.Treeview(quadro_tabela,
                                columns=("Data", "Lugar", "Cliente", "Produto", "Qtd", "PreçoUn", "Total"),
                                show='headings')

        # Define o cabeçalho para a coluna "Data" da Treeview.
        # `text="Data"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("Data", text="Data")

        # Define o cabeçalho para a coluna "Lugar" da Treeview.
        # `text="Lugar"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("Lugar", text="Lugar")

        # Define o cabeçalho para a coluna "Cliente" da Treeview.
        # `text="Cliente"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("Cliente", text="Cliente")

        # Define o cabeçalho para a coluna "Produto" da Treeview.
        # `text="Produto"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("Produto", text="Produto")

        # Define o cabeçalho para a coluna "Qtd" da Treeview.
        # `text="Qtd"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("Qtd", text="Qtd")

        # Define o cabeçalho para a coluna "PreçoUn" da Treeview.
        # `text="Preço Unitário"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("PreçoUn", text="Preço Unitário")

        # Define o cabeçalho para a coluna "Total" da Treeview.
        # `text="Total (R$)"` especifica o título exibido no cabeçalho da coluna.
        self.tree.heading("Total", text="Total (R$)")

        # Configura as colunas na Treeview, ajustando largura e alinhamento.
        # Define largura fixa de 140 pixels e centraliza os valores em cada coluna.
        for col in ("Data", "Lugar", "Cliente", "Produto", "Qtd", "PreçoUn", "Total"):
            self.tree.column(col, width=140, anchor="center")

        # Exibe a Treeview no layout, permitindo que ela preencha o espaço disponível.
        # `fill="both"` expande tanto horizontalmente quanto verticalmente.
        # `expand=True` permite que a tabela se ajuste dinamicamente ao redimensionar a janela.
        # `padx=5, pady=5` adiciona espaçamento externo.
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Cria um quadro para exibir os contadores totais.
        # `ttk.Frame(self.janela)` cria um container para os elementos de resumo.
        # `fill="x"` garante que o quadro se expanda horizontalmente.
        # `padx=10, pady=5` adiciona espaçamento externo ao quadro.
        quadro_totais = ttk.Frame(self.janela)
        quadro_totais.pack(fill="x", padx=10, pady=5)

        # Adiciona um rótulo para exibir o total calculado.
        # `text="Total: R$ 0.00"` define o texto inicial exibido no rótulo.
        # `font=("Arial", 12, "bold")` aplica uma fonte em negrito para destaque.
        self.lbl_total = ttk.Label(
            quadro_totais, text="Total: R$ 0.00", font=("Arial", 12, "bold")
        )

        # Posiciona o rótulo no lado esquerdo do quadro.
        # `side="left"` alinha o rótulo à esquerda do quadro.
        # `padx=10` adiciona espaçamento horizontal ao redor do rótulo.
        self.lbl_total.pack(side="left", padx=10)

        # Cria um rótulo para exibir o total de registros.
        # `text="Total de Registros: 0"` define o texto inicial exibido no rótulo.
        # `font=("Arial", 12, "bold")` aplica uma fonte em negrito para maior destaque visual.
        self.lbl_total_registros = ttk.Label(
            quadro_totais, text="Total de Registros: 0", font=("Arial", 12, "bold")
        )

        # Posiciona o rótulo no lado esquerdo do quadro.
        # `side="left"` alinha o rótulo à esquerda do quadro, ao lado do total.
        # `padx=10` adiciona espaçamento horizontal ao redor do rótulo.
        self.lbl_total_registros.pack(side="left", padx=10)

        # Chama o método `listar` para carregar os dados iniciais na TreeView.
        # Este método será responsável por preencher a tabela
        #       com os registros disponíveis.
        self.listar()


    # Define um método para converter uma string de data no
    #       formato "dd/MM/yyyy" em um objeto datetime.
    def converter_data_str(self, data_str):

        # Tenta converter a string fornecida para um objeto datetime.
        # `strptime(data_str, "%d/%m/%Y")` define o formato esperado para a string.
        try:

            return datetime.strptime(data_str, "%d/%m/%Y")

        # Caso a string não esteja no formato esperado, captura a exceção ValueError.
        # Retorna `None` para indicar uma conversão inválida.
        except ValueError:
            return None


    # Define um método para listar os dados com base nos filtros fornecidos.
    def listar(self, dt_ini=None, dt_fim=None, lugar="", cliente="", produto=""):

        # Limpa os dados existentes na tabela removendo
        #       todos os itens da TreeView.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Inicializa o total geral com 0.0, que será usado
        #       para somar os valores listados.
        total_geral = 0.0

        # Inicializa o contador de registros com 0 para rastrear a
        #       quantidade de registros listados.
        total_registros = 0

        try:

            # Realiza uma busca na coleção de reservas para obter os dados.
            reservas = self.reserva.colecao_reservas.find()

            # Itera sobre cada reserva retornada pela consulta.
            for r in reservas:

                # Obtém a data da reserva no formato string.
                data_str = r.get("data", "")

                # Converte a data da reserva de string para objeto datetime.
                # `data_str` é a data armazenada na reserva em formato de texto (ex.: "01/01/2030").
                # A função `converter_data_str` tenta transformar esse texto em um objeto `datetime`.
                # Isso é importante porque comparações de datas (como antes ou
                #       depois) só funcionam com objetos de data.
                data_obj = self.converter_data_str(data_str)

                # Aplica o filtro de data inicial.
                # Verifica se o filtro de data inicial (`dt_ini`) foi fornecido e
                #       se a data da reserva (`data_obj`)
                #       é válida (não é `None`). Em seguida, verifica se a data da
                #       reserva é menor que a data inicial.
                # Caso a data da reserva seja anterior à data inicial, essa
                #       reserva é ignorada (continua para a próxima).
                if dt_ini and data_obj and data_obj < dt_ini:
                    continue

                # Aplica o filtro de data final.
                # Verifica se o filtro de data final (`dt_fim`) foi fornecido e
                #       se a data da reserva (`data_obj`)
                # é válida. Em seguida, verifica se a data da reserva é maior que a data final.
                # Caso a data da reserva seja posterior à data final, essa
                #       reserva é ignorada (continua para a próxima).
                if dt_fim and data_obj and data_obj > dt_fim:
                    continue

                # Nome do lugar
                # Obtém o nome do lugar da reserva usando a chave "nome_lugar".
                # Caso o lugar não esteja presente na reserva,
                #       será atribuído "N/A" (não disponível) como valor padrão.
                lugar_nome = r.get("nome_lugar", "N/A")

                # Aplica o filtro de lugar.
                # Verifica se o filtro de lugar foi preenchido pelo usuário (`lugar`) e
                #       se o nome do lugar associado à reserva (`lugar_nome`)
                #       contém o valor informado no filtro (ignorando maiúsculas e minúsculas).
                # Caso o nome do lugar não corresponda ao filtro, a reserva
                #       será ignorada (continua para a próxima).
                if lugar and lugar.lower() not in lugar_nome.lower():
                    continue

                # Nome do cliente
                # Inicializa a variável `cli_nome` com uma string vazia.
                # O nome do cliente será buscado abaixo,
                #       caso a reserva possua um identificador de cliente associado.
                cli_nome = ""

                # Verifica se a reserva possui um cliente associado
                # Se a chave "cliente_id" estiver presente na reserva,
                #       indica que há um cliente vinculado.
                if r.get("cliente_id"):

                    # Busca o documento do cliente no banco de dados
                    #       usando o ID do cliente armazenado na reserva.
                    cliente_doc = self.reserva.colecao_clientes.find_one({"_id": ObjectId(r["cliente_id"])})

                    # Se o cliente for encontrado no banco de dados, obtém o nome do cliente.
                    # Caso o nome não esteja presente no documento,
                    #       atribui "N/A" (não disponível) como valor padrão.
                    if cliente_doc:
                        cli_nome = cliente_doc.get("nome", "N/A")

                # Aplica o filtro de cliente.
                # Verifica se o filtro de cliente foi preenchido pelo usuário (`cliente`) e
                #       se o nome do cliente associado à reserva (`cli_nome`)
                #       contém o valor informado no filtro (ignorando maiúsculas e minúsculas).
                # Caso o nome do cliente não corresponda ao filtro, a reserva será
                #       ignorada (continua para a próxima).
                if cliente and cliente.lower() not in cli_nome.lower():
                    continue

                # Itera sobre os itens consumidos associados à reserva.
                # Cada item é representado como um dicionário contendo
                #       informações sobre o produto consumido.
                for item_consumido in r.get("itens_consumidos", []):

                    # Obtém o nome do produto consumido.
                    # Se o nome não estiver disponível, atribui "N/A" (não disponível) como valor padrão.
                    nome_prod = item_consumido.get("nome", "N/A")

                    # Obtém o ID do produto consumido.
                    # Isso é usado para vincular o item a um produto específico
                    #       no banco de dados, se necessário.
                    produto_id = item_consumido.get("produto_id")

                    # Obtém a quantidade consumida do produto.
                    # Se a quantidade não estiver presente no item, assume o valor padrão de 0.
                    qtd = item_consumido.get("qtd", 0)

                    # Obtém o preço unitário do produto consumido.
                    # Caso o preço unitário não esteja especificado no item,
                    #       atribui o valor padrão de 0.0.
                    preco_un = item_consumido.get("preco_unit", 0.0)

                    # Verifica se o item consumido pertence ao produto selecionado.
                    # A comparação é feita utilizando o ID do produto armazenado no
                    #       item e o ID do produto atual (self.produto_id).
                    if produto_id and ObjectId(produto_id) == self.produto_id:

                        # Aplica o filtro de nome do produto, caso tenha sido fornecido.
                        # Ignora o item se o nome do produto não contém a string
                        #       fornecida no filtro (case-insensitive).
                        if produto and produto.lower() not in nome_prod.lower():
                            continue

                        # Calcula o valor total do item consumido multiplicando a
                        #       quantidade pelo preço unitário.
                        total_item = qtd * preco_un

                        # Adiciona o valor total do item ao total geral das reservas.
                        total_geral += total_item

                        # Incrementa o contador de registros processados.
                        total_registros += 1

                        # Insere os dados processados na TreeView (tabela da interface gráfica).
                        # Cada item consumido é exibido com as informações correspondentes.
                        self.tree.insert(
                            "",  # Indica que o item será inserido na raiz da TreeView (sem pai).
                            "end",  # Define que o item será adicionado no final da lista.
                            values=(
                                data_str,  # Data da reserva, no formato string.
                                lugar_nome,  # Nome do lugar onde ocorreu a reserva.
                                cli_nome,  # Nome do cliente que realizou a reserva.
                                nome_prod,  # Nome do produto consumido durante a reserva.
                                f"{qtd:.2f}",  # Quantidade consumida do produto, formatada com 2 casas decimais.
                                f"R$ {preco_un:.2f}",
                                # Preço unitário do produto, formatado em reais com 2 casas decimais.
                                f"R$ {total_item:.2f}"
                            # Valor total do item (quantidade x preço unitário), formatado.
                            )
                        )

            # Atualiza os valores exibidos nos rótulos (labels) da interface
            #       gráfica para refletir os totais calculados.

            # Atualiza o rótulo que exibe o total geral em reais.
            # `text=f"Total: R$ {total_geral:.2f}"` define o texto do rótulo com o
            #       total formatado em reais (2 casas decimais).
            self.lbl_total.config(text=f"Total: R$ {total_geral:.2f}")

            # Atualiza o rótulo que exibe o número total de registros encontrados.
            # `text=f"Total de Registros: {total_registros}"` exibe a contagem de registros processados.
            self.lbl_total_registros.config(text=f"Total de Registros: {total_registros}")

        # Captura qualquer exceção que ocorra durante o processo de listagem dos dados.
        except Exception as e:

            # Exibe uma mensagem de erro para o usuário utilizando uma caixa de diálogo.
            # `messagebox.showerror` cria uma janela pop-up com o título "Erro" e exibe a mensagem de erro.
            # `f"Erro ao listar os dados: {e}"` insere a descrição da exceção no texto da mensagem.
            messagebox.showerror("Erro", f"Erro ao listar os dados: {e}")


    # Define um método para filtrar os dados com base nos
    #       critérios fornecidos pelo usuário.
    def filtrar(self):

        # Converte a data inicial do filtro para um objeto
        #       datetime usando `converter_data_str`.
        dt_ini = self.converter_data_str(self.dt_ini.get())

        # Converte a data final do filtro para um objeto datetime
        #       usando `converter_data_str`.
        dt_fim = self.converter_data_str(self.dt_fim.get())

        # Obtém o texto do filtro de lugar, removendo espaços
        #       extras ao redor da string.
        lugar = self.var_lugar.get().strip()

        # Obtém o texto do filtro de cliente, removendo espaços
        #       extras ao redor da string.
        cliente = self.var_cliente.get().strip()

        # Obtém o texto do filtro de produto, removendo espaços
        #       extras ao redor da string.
        produto = self.var_produto.get().strip()

        # Chama o método `listar` para carregar os dados com base nos filtros aplicados.
        # Passa os parâmetros convertidos e os valores dos filtros ao método `listar`.
        self.listar(dt_ini, dt_fim, lugar, cliente, produto)

    # Define o método para exportar os dados exibidos na tabela para um arquivo Excel.
    def exportar_excel(self):


        # Abre uma janela para salvar o arquivo, permitindo ao usuário
        #       escolher o local e o nome do arquivo.
        # `defaultextension=".xlsx"` define a extensão padrão como .xlsx.
        # `filetypes` limita os tipos de arquivos que podem ser salvos, neste caso, arquivos Excel.
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )

        # Verifica se o usuário não selecionou um arquivo (cancelou a
        #       operação). Retorna para evitar erros.
        if not file_path:
            return

        # Lista para armazenar os dados extraídos da tabela.
        data = []

        # Itera sobre todas as linhas da tabela (TreeView).
        # `self.tree.get_children()` retorna os identificadores de todas as linhas.
        # Para cada linha, os valores são extraídos e adicionados à lista `data`.
        for row_id in self.tree.get_children():

            row = self.tree.item(row_id)["values"]  # Pega os valores da linha.
            data.append(row)  # Adiciona a linha à lista de dados.

        # Define os nomes das colunas que serão usadas no arquivo Excel.
        columns = ["Data", "Lugar", "Cliente", "Produto", "Quantidade", "Preço Unitário", "Total (R$)"]

        # Cria um DataFrame do Pandas com os dados da tabela e as colunas definidas.
        # O DataFrame é a estrutura que será usada para salvar os dados no Excel.
        df = pd.DataFrame(data, columns=columns)

        # Exporta os dados para um arquivo Excel.
        # `file_path` contém o caminho e o nome do arquivo escolhido pelo usuário.
        # `index=False` evita que o índice do DataFrame seja incluído no arquivo.
        df.to_excel(file_path, index=False)

        # Exibe uma mensagem informando que a exportação foi concluída com sucesso.
        messagebox.showinfo("Exportação", "Dados exportados com sucesso!")



###############################################################################
#                CLIENTES (CRUD + HISTÓRICO + DETALHE)                        #
###############################################################################
class JanelaClientes:

    # Método de inicialização da classe JanelaClientes.
    # `parent` é o widget pai onde esta janela será criada.
    # `reserva` é uma instância do objeto ReservaQuadra para interagir com os dados.
    def __init__(self, parent, reserva: ReservaQuadra):

        # Armazena o widget pai para referência futura.
        self.parent = parent

        # Armazena a instância de ReservaQuadra para uso em métodos da classe.
        self.reserva = reserva

        # Cria uma nova janela Toplevel para gerenciar os clientes.
        self.janela = tk.Toplevel(parent)

        # Define o título da janela como "Clientes".
        self.janela.title("Clientes")

        # Define o estado da janela para "zoomed" (máximo).
        self.janela.state("zoomed")

        # Cria um quadro para o formulário de cadastro de clientes,
        #       com um título e espaçamento interno.
        quadro_form = ttk.LabelFrame(self.janela, text="Cadastro de Clientes", padding=10)

        # Posiciona o quadro na janela, preenchendo horizontalmente e
        #       adicionando espaçamento externo.
        quadro_form.pack(fill="x", padx=10, pady=10)

        # Cria variáveis para armazenar os dados do formulário.
        # `self.var_nome` armazena o nome do cliente.
        self.var_nome = tk.StringVar()

        # `self.var_cpf` armazena o CPF do cliente.
        self.var_cpf = tk.StringVar()

        # `self.var_tel` armazena o telefone do cliente.
        self.var_tel = tk.StringVar()

        # `self.var_email` armazena o e-mail do cliente.
        self.var_email = tk.StringVar()

        # `self.var_end` armazena o endereço do cliente.
        self.var_end = tk.StringVar()

        # `self.var_tipo_cli` armazena o tipo do cliente (ex.: físico ou jurídico).
        self.var_tipo_cli = tk.StringVar()

        # Define uma lista de tuplas contendo o rótulo e a variável
        #       associada a cada campo do formulário.
        # Cada tupla contém:
        # - O rótulo do campo (ex.: "Nome:", "CPF:", etc.).
        # - A variável associada ao campo, que armazenará o valor correspondente.
        campos = [
            ("Nome:", self.var_nome),  # Campo para o nome do cliente.
            ("CPF:", self.var_cpf),  # Campo para o CPF do cliente.
            ("Telefone:", self.var_tel),  # Campo para o telefone do cliente.
            ("E-mail:", self.var_email),  # Campo para o e-mail do cliente.
            ("Endereço:", self.var_end),  # Campo para o endereço do cliente.
            ("Tipo Cliente (avulso/mensalista):", self.var_tipo_cli)  # Campo para o tipo de cliente.
        ]

        # Itera sobre a lista de campos para criar os rótulos e entradas dinamicamente.
        # Cada campo será colocado em uma linha diferente dentro do formulário.
        for i, (rotulo, var) in enumerate(campos):

            # Cria o rótulo do campo.
            # `text=rotulo` define o texto exibido no rótulo.
            # `font=("Arial", 12)` define a fonte e o tamanho do texto.
            # `sticky='e'` alinha o rótulo à direita da célula.
            # `padx=5, pady=5` adiciona espaçamento ao redor do rótulo.
            ttk.Label(quadro_form,
                      text=rotulo,
                      font=("Arial", 12)).grid(row=i, column=0, sticky='e', padx=5, pady=5)

            # Cria a entrada de texto correspondente ao rótulo.
            # `textvariable=var` vincula o valor da entrada à variável associada.
            # `font=("Arial", 12)` define a fonte e o tamanho do texto.
            # `width=40` define a largura da entrada de texto.
            # `padx=5, pady=5` adiciona espaçamento ao redor da entrada.
            ttk.Entry(quadro_form,
                      textvariable=var,
                      font=("Arial", 12), width=40).grid(row=i, column=1, padx=5, pady=5)

        # Cria um quadro para agrupar os botões de ação do formulário.
        # `row=len(campos)` posiciona o quadro logo abaixo dos campos criados dinamicamente.
        # `columnspan=2` faz o quadro ocupar duas colunas.
        # `pady=10` adiciona espaçamento vertical ao quadro.
        quadro_botoes = ttk.Frame(quadro_form)
        quadro_botoes.grid(row=len(campos), column=0, columnspan=2, pady=10)

        # Cria um botão para a ação "Cadastrar".
        # `text="Cadastrar"` define o texto exibido no botão.
        # `command=self.cadastrar` associa a ação de cadastro ao clique no botão.
        # `width=20` define a largura do botão.
        # `side="left"` posiciona o botão à esquerda dentro do quadro.
        # `padx=5` adiciona espaçamento horizontal entre os botões.
        ttk.Button(quadro_botoes,
                   text="Cadastrar",
                   command=self.cadastrar,
                   width=20).pack(side="left", padx=5)

        # Cria um botão para a ação "Alterar".
        # `text="Alterar"` define o texto exibido no botão.
        # `command=self.alterar` associa a ação de alteração ao clique no botão.
        # `width=20` define a largura do botão.
        # `side="left"` posiciona o botão à esquerda dentro do quadro.
        # `padx=5` adiciona espaçamento horizontal entre os botões.
        ttk.Button(quadro_botoes,
                   text="Alterar",
                   command=self.alterar,
                   width=20).pack(side="left", padx=5)

        # Cria um botão para a ação "Excluir".
        # `text="Excluir"` define o texto exibido no botão.
        # `command=self.excluir` associa a ação de exclusão ao clique no botão.
        # `width=20` define a largura do botão.
        # `side="left"` posiciona o botão à esquerda dentro do quadro.
        # `padx=5` adiciona espaçamento horizontal entre os botões.
        ttk.Button(quadro_botoes,
                   text="Excluir",
                   command=self.excluir,
                   width=20).pack(side="left", padx=5)

        # Cria um botão para a ação "Limpar".
        # `text="Limpar"` define o texto exibido no botão.
        # `command=self.limpar` associa a ação de limpar os campos ao clique no botão.
        # `width=20` define a largura do botão.
        # `side="left"` posiciona o botão à esquerda dentro do quadro.
        # `padx=5` adiciona espaçamento horizontal entre os botões.
        ttk.Button(quadro_botoes,
                   text="Limpar",
                   command=self.limpar,
                   width=20).pack(side="left", padx=5)

        # Cria um botão para abrir o histórico.
        # `text="Histórico"` define o texto exibido no botão.
        # `command=self.abrir_historico` associa a abertura do histórico ao clique no botão.
        # `width=20` define a largura do botão.
        # `side="left"` posiciona o botão à esquerda dentro do quadro.
        # `padx=5` adiciona espaçamento horizontal entre os botões.
        ttk.Button(quadro_botoes,
                   text="Histórico",
                   command=self.abrir_historico,
                   width=20).pack(side="left", padx=5)

        # Cria um quadro para exibir a tabela de clientes.
        # `text="Lista de Clientes"` define o título exibido no quadro.
        # `padding=10` adiciona espaçamento interno ao quadro.
        quadro_tabela = ttk.LabelFrame(self.janela, text="Lista de Clientes", padding=10)

        # `fill="both"` faz com que o quadro ocupe todo o espaço disponível na horizontal e vertical.
        # `expand=True` permite que o quadro seja expandido, caso a janela seja redimensionada.
        # `padx=10, pady=10` adicionam espaçamento externo ao redor do quadro.
        quadro_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria uma Treeview para exibir os dados dos clientes.
        # `columns` define as colunas que serão exibidas na tabela.
        # `show="headings"` exibe apenas os cabeçalhos, sem a coluna extra da hierarquia de itens.
        # `height=15` define a quantidade de linhas visíveis na tabela.
        self.tree = ttk.Treeview(quadro_tabela,
                                columns=("Nome", "CPF", "Telefone", "Email", "Endereco", "TipoCliente"),
                                show="headings",
                                height=15)

        # Configura as colunas da Treeview.
        # Para cada coluna em `self.tree["columns"]`, define o
        #       cabeçalho e as propriedades da coluna.
        for col in self.tree["columns"]:

            # `self.tree.heading(col, text=col, anchor="center")` define o
            #       texto do cabeçalho da coluna e centraliza o texto.
            # `self.tree.column(col, width=150, anchor="center")` define a
            #       largura da coluna e centraliza os dados da coluna.
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=150, anchor="center")

        # Posiciona a Treeview dentro do quadro.
        # `fill="both"` faz com que a Treeview ocupe todo o espaço disponível no quadro.
        # `expand=True` permite que a Treeview seja expandida, caso a janela seja redimensionada.
        # `padx=10, pady=10` adicionam espaçamento externo ao redor da Treeview.
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Configura o estilo da Treeview.
        style = ttk.Style()

        # Define a fonte dos dados exibidos na Treeview.
        # `font=("Arial", 12)` define a fonte como Arial, tamanho 12.
        style.configure("Treeview", font=("Arial", 12))

        # Define a fonte dos cabeçalhos das colunas na Treeview.
        # `font=("Arial", 12, "bold")` define a fonte como Arial, tamanho 12, em negrito.
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Associa um evento à Treeview para capturar a seleção de itens.
        # `"<<TreeviewSelect>>"` é o evento disparado quando o usuário seleciona um item na Treeview.
        # `self.selecionar_item` é o método que será chamado ao disparar o evento.
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item)

        # Chama o método `listar` para carregar os dados na Treeview.
        # Este método irá buscar os dados no banco de dados e
        #       preencher a Treeview com os registros existentes.
        self.listar()



    def listar(self):

        # Remove todas as linhas existentes na TreeView.
        # `get_children()` retorna todos os itens da TreeView.
        # `delete(item)` remove o item específico da TreeView.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca todos os clientes na coleção `colecao_clientes`.
        # O método `find()` retorna um cursor com todos os documentos.
        clientes = self.reserva.colecao_clientes.find()

        # Itera sobre cada cliente retornado pela consulta.
        for c in clientes:

            # Insere um novo registro na TreeView.
            # `iid=str(c["_id"])` define o ID do item como o ID do cliente no banco de dados.
            # `values` define os valores das colunas para o cliente.
            self.tree.insert( "",  # Adiciona o item na raiz (não é um item filho).
                    "end",  # Adiciona o item no final da lista.
                    iid=str(c["_id"]),  # Define o identificador único baseado no `_id` do cliente.
                    values=(
                        c.get("nome", ""),  # Nome do cliente ou vazio se não existir.
                        c.get("cpf", ""),  # CPF do cliente ou vazio.
                        c.get("telefone", ""),  # Telefone do cliente ou vazio.
                        c.get("email", ""),  # E-mail do cliente ou vazio.
                        c.get("endereco", ""),  # Endereço do cliente ou vazio.
                        c.get("tipo_cliente", "")  # Tipo do cliente (ex.: "avulso" ou "mensalista") ou vazio.
                    )
            )



    def selecionar_item(self, event):

        # Obtém o item selecionado na Treeview.
        # `self.tree.selection()` retorna uma tupla com os
        #       identificadores dos itens selecionados.
        selecionado = self.tree.selection()

        # Verifica se nenhum item foi selecionado.
        # Caso a tupla `selecionado` esteja vazia, o método retorna
        #       sem executar nenhuma ação.
        if not selecionado:
            return

        # Obtém o identificador do primeiro item selecionado.
        # Como a Treeview pode permitir múltiplas seleções, pegamos apenas o primeiro item.
        item_id = selecionado[0]

        # Recupera os valores do item selecionado.
        # `self.tree.item(item_id, "values")` retorna uma tupla com os
        #       valores das colunas do item selecionado.
        valores = self.tree.item(item_id, "values")

        # Preenche os campos do formulário com os valores da linha selecionada na Treeview.
        # `set` é usado para atualizar o valor da variável associada a cada campo.
        self.var_nome.set(valores[0])  # Atualiza o campo "Nome".
        self.var_cpf.set(valores[1])  # Atualiza o campo "CPF".
        self.var_tel.set(valores[2])  # Atualiza o campo "Telefone".
        self.var_email.set(valores[3])  # Atualiza o campo "E-mail".
        self.var_end.set(valores[4])  # Atualiza o campo "Endereço".
        self.var_tipo_cli.set(valores[5])  # Atualiza o campo "Tipo Cliente".




    def cadastrar(self):

        # Obtém o valor do campo "Nome" e remove espaços em branco no início e no final.
        # `self.var_nome.get()` retorna o valor atual vinculado à variável `self.var_nome`.
        nome = self.var_nome.get().strip()

        # Obtém o valor do campo "CPF" e remove espaços em branco no início e no final.
        cpf = self.var_cpf.get().strip()

        # Obtém o valor do campo "Telefone" e remove espaços em branco no início e no final.
        telefone = self.var_tel.get().strip()

        # Obtém o valor do campo "E-mail" e remove espaços em branco no início e no final.
        email = self.var_email.get().strip()

        # Obtém o valor do campo "Endereço" e remove espaços em branco no início e no final.
        endereco = self.var_end.get().strip()

        # Obtém o valor do campo "Tipo Cliente" (ex.: avulso ou
        #       mensalista) e remove espaços em branco.
        tipo_cliente = self.var_tipo_cli.get().strip()

        # Verifica se os campos obrigatórios "Nome" e "CPF" estão preenchidos.
        # Caso contrário, exibe uma mensagem de aviso e interrompe o fluxo.
        if not nome or not cpf:
            messagebox.showwarning( "Aviso",
                            "Nome e CPF são obrigatórios.",
                            parent=self.janela)
            return

        # Verifica se já existe um cliente com o mesmo CPF cadastrado na coleção de clientes.
        # `find_one({"cpf": cpf})` busca por um documento onde o
        #       campo `cpf` tenha o mesmo valor fornecido.
        if self.reserva.colecao_clientes.find_one({"cpf": cpf}):

            # Caso encontre duplicidade, exibe uma mensagem de
            #       aviso e interrompe o fluxo.
            messagebox.showwarning("Aviso",
                        "CPF já cadastrado para algum cliente.",
                                parent=self.janela)
            return

        # Monta o documento do cliente para inserção no banco de dados.
        # Os campos "nome", "cpf", "telefone", "email", "endereco" e
        #       "tipo_cliente" são incluídos no documento.
        doc_cli = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email,
            "endereco": endereco,
            "tipo_cliente": tipo_cliente,
        }

        # Insere o documento na coleção de clientes.
        # `insert_one(doc_cli)` adiciona o novo cliente ao banco de dados.
        self.reserva.colecao_clientes.insert_one(doc_cli)

        # Exibe uma mensagem de sucesso informando que o cliente foi cadastrado.
        messagebox.showinfo(
            "Sucesso",
            "Cliente cadastrado com sucesso!",
            parent=self.janela
        )

        # Atualiza a lista de clientes exibida na interface.
        self.listar()

        # Limpa os campos do formulário para permitir um novo cadastro.
        self.limpar()


    def alterar(self):

        # Verifica se algum cliente foi selecionado na TreeView.
        # `selection()` retorna os itens selecionados. Se estiver
        #       vazio, nenhum item foi selecionado.
        if not self.tree.selection():

            # Exibe uma mensagem de aviso ao usuário, indicando que é necessário selecionar um cliente.
            messagebox.showwarning("Aviso",
                                   "Selecione um cliente para alterar.",
                                   parent=self.janela)

            # Interrompe a execução da função.
            return

        # Obtém o identificador do item selecionado.
        # `selection()` retorna uma lista de itens selecionados. Aqui, pega o primeiro da lista.
        iid = self.tree.selection()[0]

        # Monta um dicionário com os novos dados do cliente para atualização no banco.
        # `strip()` é usado para remover espaços em branco desnecessários no
        #       início e no fim de cada valor.
        doc_update = {
            "nome": self.var_nome.get().strip(),  # Obtém o valor do campo "Nome".
            "cpf": self.var_cpf.get().strip(),  # Obtém o valor do campo "CPF".
            "telefone": self.var_tel.get().strip(),  # Obtém o valor do campo "Telefone".
            "email": self.var_email.get().strip(),  # Obtém o valor do campo "E-mail".
            "endereco": self.var_end.get().strip(),  # Obtém o valor do campo "Endereço".
            "tipo_cliente": self.var_tipo_cli.get().strip(),  # Obtém o valor do campo "Tipo Cliente".
        }

        # Atualiza o registro do cliente no banco de dados com os novos valores.
        # `update_one` busca o registro pelo ID e atualiza apenas os campos especificados em `$set`.
        self.reserva.colecao_clientes.update_one({"_id": ObjectId(iid)}, {"$set": doc_update})

        # Exibe uma mensagem informando que a alteração foi
        #       concluída com sucesso.
        messagebox.showinfo("Sucesso",
                            "Cliente alterado com sucesso!",
                            parent=self.janela)

        # Recarrega os dados atualizados na TreeView para refletir a alteração.
        self.listar()

        # Limpa os campos do formulário para evitar confusão com os dados antigos.
        self.limpar()


    def excluir(self):

        # Obtém o cliente selecionado na TreeView.
        sel = self.tree.selection()

        # Verifica se algum cliente foi selecionado. Caso contrário,
        #       exibe uma mensagem de aviso.
        if not sel:
            messagebox.showwarning("Aviso",
                                   "Selecione um cliente para excluir.",
                                   parent=self.janela)
            return

        # Recupera o ID do cliente selecionado.
        iid = sel[0]

        # Remove o cliente do banco de dados utilizando o ID.
        self.reserva.colecao_clientes.delete_one({"_id": ObjectId(iid)})

        # Exibe uma mensagem informando que o cliente foi excluído com sucesso.
        messagebox.showinfo("Sucesso",
                            "Cliente excluído com sucesso!",
                            parent=self.janela)

        # Atualiza a lista de clientes na TreeView para refletir a exclusão.
        self.listar()

        # Limpa os campos do formulário para evitar inconsistências.
        self.limpar()


    def limpar(self):

        # Limpa o campo de entrada do nome do cliente.
        # `set("")` atribui uma string vazia à variável associada ao campo de texto.
        self.var_nome.set("")

        # Limpa o campo de entrada do CPF.
        # Garante que o CPF do formulário seja redefinido para vazio.
        self.var_cpf.set("")

        # Limpa o campo de entrada do telefone.
        # Remove qualquer valor preenchido anteriormente no campo de telefone.
        self.var_tel.set("")

        # Limpa o campo de entrada do e-mail.
        # Reseta o campo de e-mail para permitir novas entradas.
        self.var_email.set("")

        # Limpa o campo de entrada do endereço.
        # Deixa o campo de endereço vazio.
        self.var_end.set("")

        # Limpa o campo de entrada do tipo de cliente.
        # Redefine o tipo de cliente (ex.: "avulso" ou "mensalista") para vazio.
        self.var_tipo_cli.set("")



    def abrir_historico(self):

        # Obtém o item selecionado na Treeview.
        # `self.tree.selection()` retorna uma tupla com os identificadores dos itens selecionados.
        sel = self.tree.selection()

        # Verifica se nenhum item foi selecionado.
        # Caso a tupla `sel` esteja vazia, exibe uma mensagem de aviso e encerra o método.
        if not sel:
            messagebox.showwarning( "Aviso",  # Título da mensagem.
                            "Selecione um cliente para visualizar o histórico.",  # Corpo da mensagem.
                            parent=self.janela)  # Define a janela atual como pai do messagebox.
            return

        # Obtém o identificador do primeiro item selecionado.
        # Como a Treeview pode permitir múltiplas seleções, pegamos apenas o primeiro item.
        iid = sel[0]

        # Abre a janela de histórico do cliente.
        # `JanelaHistoricoClientesDetalhe` é uma classe que exibe o histórico
        #       de ações relacionadas ao cliente.
        # Passa a janela atual (`self.janela`), o objeto de
        #       reserva (`self.reserva`), e o identificador do cliente (`iid`).
        JanelaHistoricoClientesDetalhe(self.janela, self.reserva, iid)



###############################################################################
#                            HISTÓRICO DE CLIENTES                            #
###############################################################################
class JanelaHistoricoClientesDetalhe:

    # Define o construtor da classe `JanelaHistoricoClientesDetalhe`.
    # `parent` é a janela principal ou pai que instanciou essa janela.
    # `reserva` é o objeto que contém as coleções do banco de dados (como clientes e reservas).
    # `cliente_id` é o identificador único do cliente cujas informações serão exibidas.
    def __init__(self, parent, reserva, cliente_id):

        self.parent = parent  # Armazena a janela pai.
        self.reserva = reserva  # Armazena o objeto `reserva` com acesso ao banco de dados.
        self.cliente_id = cliente_id  # Armazena o ID do cliente selecionado.

        # Obtém a coleção de reservas a partir do objeto `reserva` para buscar os dados no banco.
        self.col_reservas = self.reserva.colecao_reservas

        # Cria uma nova janela para exibir o histórico detalhado do cliente.
        # `parent` é a janela principal à qual esta está vinculada.
        self.janela = tk.Toplevel(parent)

        # `title="Histórico Completo do Cliente"` define o título exibido na barra da janela.
        self.janela.title("Histórico Completo do Cliente")

        # `state("zoomed")` ajusta a janela para ser maximizada automaticamente ao abrir.
        self.janela.state("zoomed")

        # Cria um rótulo que serve como título principal da janela.
        # `text="Histórico Detalhado do Cliente"` define o texto exibido no rótulo.
        # `font=("Arial", 16, "bold")` define a fonte usada, tamanho 16, em negrito.
        lbl_titulo = tk.Label(self.janela,
                              text="Histórico Detalhado do Cliente",
                              font=("Arial", 16, "bold"))

        # `pady=5` adiciona um espaçamento vertical de 5 pixels acima e abaixo do rótulo.
        lbl_titulo.pack(pady=5)

        # Cria um quadro para agrupar os filtros de pesquisa.
        # `ttk.LabelFrame` cria um frame com um rótulo associado.
        # `text="Filtros"` define o texto exibido no rótulo do quadro.
        # `padding=10` adiciona espaçamento interno de 10 pixels em todas as direções.
        quadro_filtros = ttk.LabelFrame(self.janela, text="Filtros", padding=10)

        # `fill="x"` faz com que o quadro preencha horizontalmente o espaço disponível.
        # `padx=10` e `pady=5` adicionam espaçamento externo de 10 pixels
        #       nas laterais e 5 pixels na parte superior e inferior.
        quadro_filtros.pack(fill="x", padx=10, pady=5)

        # Cria um rótulo para o campo de filtro de data inicial.
        # `text="Data Início:"` define o texto exibido no rótulo.
        # `grid(row=0, column=0)` posiciona o rótulo na primeira linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Data Início:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de data com o padrão de formato brasileiro (dd/MM/yyyy).
        # `DateEntry` é um widget de entrada de data.
        # `date_pattern='dd/MM/yyyy'` define o formato da data no campo.
        # `width=12` define a largura do campo de entrada.
        # `grid(row=0, column=1)` posiciona o campo na primeira linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        self.dt_ini = DateEntry(quadro_filtros, date_pattern='dd/MM/yyyy', width=12)
        self.dt_ini.grid(row=0, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de filtro de data final.
        # `text="Data Fim:"` define o texto exibido no rótulo.
        # `grid(row=0, column=2)` posiciona o rótulo na primeira linha e terceira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Data Fim:").grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Cria um campo de entrada de data com o padrão de formato brasileiro (dd/MM/yyyy).
        # `DateEntry` é um widget de entrada de data.
        # `date_pattern='dd/MM/yyyy'` define o formato da data no campo.
        # `width=12` define a largura do campo de entrada.
        # `grid(row=0, column=3)` posiciona o campo na primeira linha e quarta coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        self.dt_fim = DateEntry(quadro_filtros, date_pattern='dd/MM/yyyy', width=12)
        self.dt_fim.grid(row=0, column=3, padx=5, pady=5)

        # Cria um rótulo para o campo de filtro de lugar.
        # `text="Lugar:"` define o texto exibido no rótulo.
        # `grid(row=1, column=0)` posiciona o rótulo na segunda linha e primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Lugar:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cria uma variável de texto para vincular ao campo de entrada de lugar.
        # `tk.StringVar()` é uma variável que armazena strings e pode ser vinculada a widgets.
        self.var_lugar = tk.StringVar()

        # Cria um campo de entrada de texto para o filtro de lugar.
        # `textvariable=self.var_lugar` vincula o valor do campo à variável `self.var_lugar`.
        # `width=20` define a largura do campo de entrada.
        # `grid(row=1, column=1)` posiciona o campo na segunda linha e segunda coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_lugar,
                  width=20).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo para o campo de filtro de produto.
        # `text="Produto:"` define o texto exibido no rótulo.
        # `grid(row=1, column=2)` posiciona o rótulo na segunda linha e terceira coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        # `sticky="e"` alinha o rótulo à direita da célula.
        ttk.Label(quadro_filtros,
                  text="Produto:").grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Cria uma variável de texto para vincular ao campo de entrada de produto.
        # `tk.StringVar()` é uma variável que armazena strings e pode ser vinculada a widgets.
        self.var_produto = tk.StringVar()


        # Cria um campo de entrada de texto para o filtro de produto.
        # `textvariable=self.var_produto` vincula o valor do campo à variável `self.var_produto`.
        # `width=20` define a largura do campo de entrada.
        # `grid(row=1, column=3)` posiciona o campo na segunda linha e quarta coluna do quadro.
        # `padx=5` e `pady=5` adicionam espaçamento externo de 5 pixels em todas as direções.
        ttk.Entry(quadro_filtros,
                  textvariable=self.var_produto,
                  width=20).grid(row=1, column=3, padx=5, pady=5)

        # Cria um botão para aplicar os filtros.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a função `self.filtrar` à ação de clique no botão.
        # `grid(row=2, column=0)` posiciona o botão na terceira linha e primeira coluna do quadro.
        # `padx=10` e `pady=5` adicionam espaçamento externo
        #       de 10 pixels na horizontal e 5 pixels na vertical.
        # `sticky="w"` alinha o botão à esquerda da célula.
        ttk.Button(quadro_filtros,
                   text="Filtrar",
                   command=self.filtrar).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Cria um botão para exportar os dados para um arquivo Excel.
        # `text="Exportar para Excel"` define o texto exibido no botão.
        # `command=self.exportar_excel` associa a função `self.exportar_excel` à ação de clique no botão.
        # `grid(row=2, column=3)` posiciona o botão na terceira linha e quarta coluna do quadro.
        # `padx=10` e `pady=5` adicionam espaçamento externo de 10 pixels
        #       na horizontal e 5 pixels na vertical.
        # `sticky="e"` alinha o botão à direita da célula.
        ttk.Button(quadro_filtros,
                   text="Exportar para Excel",
                   command=self.exportar_excel).grid(row=2, column=3, padx=10, pady=5, sticky="e")

        # Cria o TreeView para exibir os dados do histórico detalhado do cliente.
        # `colunas` define os nomes das colunas exibidas: "Data", "Lugar", "Hora Inicial", "Hora Final",
        colunas = ("Data", "Lugar", "Hora Inicial", "Hora Final", "Item Consumido", "Qtd", "Valor Unit", "Total Item")

        # "Item Consumido", "Qtd", "Valor Unit" e "Total Item".
        # `self.tabela` é o widget TreeView que será utilizado para mostrar os dados.
        # `show="headings"` exibe apenas os cabeçalhos das colunas, sem uma coluna de índice.
        # `height=15` define a altura do TreeView, mostrando até 15 linhas de dados ao mesmo tempo.
        self.tabela = ttk.Treeview(self.janela, columns=colunas, show="headings", height=15)

        # Itera sobre cada coluna na lista `colunas`.
        for col in colunas:

            # Define o texto do cabeçalho para cada coluna no TreeView.
            self.tabela.heading(col, text=col)

            # Configura o alinhamento e largura padrão de cada coluna.
            self.tabela.column(col, anchor="center", width=120)

        # Posiciona o TreeView na janela.
        # `fill=tk.BOTH` permite que o TreeView ocupe todo o espaço
        #       horizontal e vertical disponível.
        # `expand=True` permite que o TreeView se ajuste ao redimensionamento da janela.
        # `padx=10` e `pady=10` adicionam um espaçamento
        #       externo de 10 pixels em torno do TreeView.
        self.tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cria um quadro para o rodapé que exibirá os totais.
        # `ttk.Frame(self.janela)` cria um frame associado à janela principal.
        # `fill="x"` garante que o quadro ocupe toda a largura disponível.
        # `padx=10` e `pady=5` adicionam espaçamento externo ao redor do quadro.
        quadro_rodape = ttk.Frame(self.janela)
        quadro_rodape.pack(fill="x", padx=10, pady=5)

        # Cria um rótulo para exibir o total de registros no rodapé.
        # `text="Total de Registros: 0"` define o texto inicial do rótulo.
        # `font=("Arial", 12, "bold")` define a fonte, tamanho e estilo (negrito) do texto.
        self.lbl_total_registros = ttk.Label(quadro_rodape,
                                            text="Total de Registros: 0",
                                            font=("Arial", 12, "bold"))

        # Posiciona o rótulo no lado esquerdo do quadro.
        # `side="left"` alinha o rótulo à esquerda.
        # `padx=10` adiciona espaçamento horizontal ao redor do rótulo.
        self.lbl_total_registros.pack(side="left", padx=10)

        # Cria um rótulo para exibir o total geral de valores no rodapé.
        # `text="Total Geral: R$ 0.00"` define o texto inicial do rótulo.
        # `font=("Arial", 12, "bold")` define a fonte, tamanho e estilo (negrito) do texto.
        self.lbl_total_valor = ttk.Label(quadro_rodape,
                                        text="Total Geral: R$ 0.00",
                                        font=("Arial", 12, "bold"))

        # Posiciona o rótulo no lado direito do quadro.
        # `side="right"` alinha o rótulo à direita.
        # `padx=10` adiciona espaçamento horizontal ao redor do rótulo.
        self.lbl_total_valor.pack(side="right", padx=10)

        # Chama o método `filtrar` para carregar e exibir a listagem inicial.
        # Isso garante que ao abrir a janela, os dados já estejam exibidos.
        self.filtrar()


    # Define um método para converter uma string de data no
    #       formato "dd/mm/yyyy" para um objeto `datetime`.
    def converter_data(self, data_str):

        # Tenta realizar a conversão da string para um objeto `datetime`
        #       usando o formato especificado.
        try:

            return datetime.strptime(data_str, "%d/%m/%Y")

        # Caso ocorra um erro durante a conversão (por exemplo, string mal formatada),
        # retorna `None` para indicar falha na conversão.
        except:
            return None


    # Define o método para filtrar os dados da tabela com
    #       base nos critérios do usuário.
    def filtrar(self):

        # Converte a data inicial fornecida pelo usuário para o formato `datetime`.
        dt_ini = self.converter_data(self.dt_ini.get())

        # Converte a data final fornecida pelo usuário para o formato `datetime`.
        dt_fim = self.converter_data(self.dt_fim.get())

        # Obtém o valor do filtro de lugar, remove espaços
        #       extras e converte para minúsculas.
        lugar = self.var_lugar.get().strip().lower()

        # Obtém o valor do filtro de produto, remove espaços
        #       extras e converte para minúsculas.
        produto = self.var_produto.get().strip().lower()

        # Limpa todos os itens da tabela para iniciar o
        #       preenchimento com dados filtrados.
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Inicializa a variável que armazenará o total geral dos valores exibidos.
        total_geral = 0.0

        # Inicializa a variável que contará o número de registros exibidos na tabela.
        total_registros = 0

        # Envolve o código em um bloco try para capturar possíveis erros durante a execução.
        try:

            # Converte o `cliente_id` em um objeto ObjectId para
            #       realizar a consulta no banco de dados.
            cliente_id = ObjectId(self.cliente_id)

            # Busca as reservas no banco de dados filtradas pelo `cliente_id`.
            reservas = self.col_reservas.find({"cliente_id": cliente_id})

            # Itera sobre cada reserva retornada pela consulta.
            for reserva in reservas:

                # Obtém a data da reserva no formato de string, caso esteja disponível.
                data = reserva.get("data", "")

                # Obtém o nome do lugar relacionado à reserva e converte
                #       para letras minúsculas para padronização.
                lugar_nome = reserva.get("nome_lugar", "").lower()

                # Obtém o horário inicial da reserva, se disponível.
                hora_ini = reserva.get("hora_inicial", "")

                # Obtém o horário final da reserva, se disponível.
                hora_fim = reserva.get("hora_final", "")

                # Obtém o valor da reserva e o converte para float.
                #       Se não houver valor, utiliza 0.0 como padrão.
                valor_reserva = float(reserva.get("valor_reserva", 0.0))

                # Converte a data da reserva em um objeto datetime para facilitar a comparação.
                data_obj = self.converter_data(data)

                # Verifica se há uma data inicial definida e se a data da reserva é
                #       anterior a ela. Se for, pula para a próxima iteração.
                if dt_ini and data_obj and data_obj < dt_ini:
                    continue

                # Verifica se há uma data final definida e se a data da reserva é
                #       posterior a ela. Se for, pula para a próxima iteração.
                if dt_fim and data_obj and data_obj > dt_fim:
                    continue

                # Verifica se há um filtro para o nome do lugar e se o nome do lugar da
                #       reserva não contém o filtro. Se não contiver, pula para a próxima iteração.
                if lugar and lugar not in lugar_nome:
                    continue

                # Insere uma nova linha na tabela com os detalhes do lugar reservado.
                # `values` define os valores que serão exibidos nas colunas da tabela.
                self.tabela.insert("",
                                   "end",  # Insere no final da tabela.
                                   values=(data,  # Data da reserva.
                                           lugar_nome,  # Nome do lugar reservado.
                                           hora_ini,  # Hora inicial da reserva.
                                           hora_fim,  # Hora final da reserva.
                                           "Lugar reservado",  # Descrição do item reservado.
                                           "",  # Quantidade (não aplicável para lugar reservado, então vazio).
                                           "",  # Valor unitário (não aplicável para lugar reservado, então vazio).
                                           f"R$ {valor_reserva:.2f}"))  # Valor total da reserva formatado em reais.

                # Incrementa o contador de registros totais.
                total_registros += 1

                # Obtém a lista de itens consumidos durante a reserva.
                itens = reserva.get("itens_consumidos", [])

                # Inicializa o subtotal da reserva para calcular o
                #       valor total dos itens consumidos.
                subtotal_reserva = 0.0

                # Itera sobre cada item consumido durante a reserva.
                for item in itens:

                    # Obtém a quantidade consumida do item, convertendo para float.
                    qtd = float(item.get("qtd", 0))

                    # Obtém o preço unitário do item, convertendo para float.
                    preco_unit = float(item.get("preco_unit", 0))

                    # Obtém o nome do produto consumido, convertendo para
                    #       minúsculas para facilitar comparações.
                    nome_prod = item.get("nome", "").lower()

                    # Calcula o valor total do item consumido multiplicando a
                    #       quantidade pelo preço unitário.
                    total_item = qtd * preco_unit

                    # Adiciona o valor total do item ao subtotal da reserva.
                    subtotal_reserva += total_item

                    # Filtra os itens consumidos com base no nome do produto.
                    # Se um filtro de produto foi definido, verifica se ele
                    #       está contido no nome do produto consumido.
                    if produto and produto not in nome_prod:
                        continue

                    # Insere uma nova linha na tabela para o item consumido.
                    # Inclui a data, nome do lugar, horários, nome do produto,
                    #       quantidade, preço unitário e total.
                    self.tabela.insert(
                        "",  # Indica que a nova linha será inserida no nível raiz (sem hierarquia).
                        "end",  # Insere a linha no final da tabela.
                        values=(
                            data,  # Data da reserva.
                            lugar_nome,  # Nome do lugar reservado.
                            hora_ini,  # Horário inicial da reserva.
                            hora_fim,  # Horário final da reserva.
                            item.get("nome", ""),  # Nome do item consumido.
                            f"{qtd:.2f}",  # Quantidade consumida formatada com duas casas decimais.
                            f"R$ {preco_unit:.2f}",  # Preço unitário do item formatado como moeda.
                            f"R$ {total_item:.2f}"  # Valor total do item consumido formatado como moeda.
                        )
                    )

                    # Incrementa o contador de registros totais.
                    total_registros += 1

                # Atualiza o total geral somando o valor da reserva e o
                #       subtotal dos itens consumidos.
                # `total_geral += valor_reserva + subtotal_reserva` incrementa o
                #       total geral com os valores calculados.
                total_geral += valor_reserva + subtotal_reserva

            # Atualiza o rótulo que exibe o total de registros.
            # `text=f"Total de Registros: {total_registros}"` define o texto do
            #       rótulo para exibir o total de registros processados.
            self.lbl_total_registros.config(text=f"Total de Registros: {total_registros}")

            # Atualiza o rótulo que exibe o total geral de valores.
            # `text=f"Total Geral: R$ {total_geral:.2f}"` formata e exibe o
            #       valor total em moeda com duas casas decimais.
            self.lbl_total_valor.config(text=f"Total Geral: R$ {total_geral:.2f}")



        # Trata exceções durante o processo de filtragem.
        # Caso ocorra algum erro, exibe uma mensagem de erro para o usuário.
        # `messagebox.showerror` exibe uma caixa de diálogo com o
        #       título "Erro" e uma mensagem detalhando o erro.
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")


    # Define o método `exportar_excel` para exportar os dados exibidos na
    #       tabela para um arquivo Excel.
    def exportar_excel(self):

        # Abre um diálogo para o usuário selecionar onde salvar o arquivo Excel.
        # `defaultextension=".xlsx"` define a extensão padrão como `.xlsx`.
        # `filetypes` permite ao usuário salvar o arquivo como Excel ou em outro formato.
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
                                                 )

        # Se o usuário cancelar a operação ou não fornecer um caminho, encerra a função.
        if not file_path:
            return

        # Cria uma lista para armazenar os dados da tabela.
        data = []

        # Itera por todas as linhas exibidas na tabela (`self.tabela`).
        for row_id in self.tabela.get_children():

            # Obtém os valores de cada linha usando o identificador (`row_id`).
            row = self.tabela.item(row_id)["values"]

            # Adiciona os valores da linha à lista `data`.
            data.append(row)

        # Define os nomes das colunas que serão utilizadas no arquivo Excel.
        columns = ["Data", "Lugar", "Hora Inicial", "Hora Final", "Item Consumido", "Qtd", "Valor Unit",
                   "Total Item"]

        # Cria um DataFrame do pandas usando os dados da tabela e as colunas definidas.
        df = pd.DataFrame(data, columns=columns)

        # Exporta o DataFrame para um arquivo Excel no caminho selecionado pelo usuário.
        # `index=False` evita que o índice do DataFrame seja incluído no arquivo.
        df.to_excel(file_path, index=False)

        # Exibe uma mensagem de sucesso ao concluir a exportação.
        messagebox.showinfo("Exportação", "Dados exportados com sucesso!")



###############################################################################
#              JANELA PRINCIPAL DE RESERVAS (MAPA DE HORÁRIOS)                #
###############################################################################

# Define a classe `JanelaPrincipalReservas`, que gerencia a
#       interface gráfica de reservas.
class JanelaPrincipalReservas:

    # Método construtor chamado automaticamente ao criar uma instância da classe.
    # Ele configura os atributos iniciais necessários para a
    #       janela de reservas.
    # `self` é a referência à instância atual da classe. Usado
    #       para acessar atributos e métodos da classe.
    def __init__(self, parent, reserva: ReservaQuadra):


        # `parent` é a referência para a janela pai (geralmente a janela principal).
        # Isso é usado para associar a janela de reservas à janela
        #       principal, permitindo interação entre elas.
        self.parent = parent

        # `reserva` é o objeto do tipo `ReservaQuadra`, que contém as
        #       funcionalidades e métodos
        #       relacionados à manipulação de reservas, como acessar o
        #       banco de dados ou verificar conflitos.
        # Esse atributo será usado para executar as operações de
        #       reserva dentro desta janela.
        self.reserva = reserva

        # Cria uma nova janela como um subjacente (filho) da
        #       janela principal (`parent`).
        # `self.janela` armazena a referência para a janela, permitindo
        #       manipular seus atributos e métodos.
        self.janela = tk.Toplevel(parent)

        # Define o título da nova janela como "Reservas",
        #       exibido na barra superior da janela.
        self.janela.title("Reservas")

        # Ajusta o estado da janela para "zoomed", que a maximiza
        #       automaticamente na tela.
        # Em sistemas operacionais diferentes, isso pode se
        #       comportar como "tela cheia".
        self.janela.state("zoomed")

        # Cria um quadro principal dentro da janela para organizar os widgets.
        # `ttk.Frame` é um contêiner que permite organizar
        #       elementos de forma hierárquica.
        quadro_principal = ttk.Frame(self.janela)

        # Posiciona o quadro principal dentro da janela, ajustando-o
        #       para preencher todo o espaço disponível.
        # `fill='both'` faz o quadro preencher horizontal e verticalmente.
        # `expand=True` permite que o quadro cresça conforme o tamanho da janela muda.
        quadro_principal.pack(fill='both', expand=True)

        # Quadro esquerdo (menu e configurações)
        # Cria um quadro no lado esquerdo dentro do quadro principal.
        # `width=250` define a largura do quadro como 250 pixels.
        quadro_esquerdo = ttk.Frame(quadro_principal, width=250)

        # Posiciona o quadro no lado esquerdo da janela.
        # `side='left'` posiciona o quadro no lado esquerdo.
        # `fill='y'` faz o quadro preencher verticalmente todo o espaço disponível.
        # `padx=20` e `pady=20` adicionam 20 pixels de espaçamento
        #       horizontal e vertical ao redor do quadro.
        quadro_esquerdo.pack(side='left', fill='y', padx=20, pady=20)

        # Cria um botão dentro do quadro esquerdo que permite
        #       voltar para a janela principal.
        # `text="Voltar"` define o texto exibido no botão.
        # `command=self.janela.destroy` fecha a janela atual ao clicar no botão.
        botao_voltar = ttk.Button(quadro_esquerdo, text="Voltar", command=self.janela.destroy)

        # Posiciona o botão dentro do quadro esquerdo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do botão.
        # `fill='x'` faz o botão preencher horizontalmente todo o
        #       espaço disponível no quadro.
        botao_voltar.pack(pady=5, fill='x')

        # Cria um rótulo no quadro esquerdo com o texto "Reservas".
        # `text="Reservas"` define o texto do rótulo.
        # `font=("Arial", 20, "bold")` define a fonte como Arial, tamanho 20, em negrito.
        ttk.Label(quadro_esquerdo, text="Reservas", font=("Arial", 20, "bold")).pack(pady=10)

        # Cria um rótulo no quadro esquerdo para o campo "Lugar".
        # `text="Lugar:"` define o texto do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do rótulo.
        ttk.Label(quadro_esquerdo, text="Lugar:").pack(pady=5)

        # Cria um combobox (caixa de seleção) no quadro esquerdo para selecionar o lugar.
        # `state="readonly"` torna o combobox somente leitura,
        #       permitindo apenas selecionar opções.
        # `width=25` define a largura do combobox como 25 caracteres.
        self.combo_lugar = ttk.Combobox(quadro_esquerdo, state="readonly", width=25)

        # Posiciona o combobox no quadro esquerdo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do combobox.
        self.combo_lugar.pack(pady=5)

        # Cria um dicionário vazio para mapear os lugares do banco de dados.
        # `self.mapa_lugares` será usado para associar os IDs dos
        #       lugares aos seus nomes no combobox.
        self.mapa_lugares = {}

        # Chama o método `carregar_lugares` para carregar os
        #       lugares do banco de dados
        #       e preencher o combobox com as opções disponíveis.
        self.carregar_lugares()

        # Calendário
        # Cria um rótulo no quadro esquerdo com o texto "Data".
        # `text="Data:"` define o texto do rótulo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do rótulo.
        ttk.Label(quadro_esquerdo, text="Data:").pack(pady=5)

        # Cria um calendário no quadro esquerdo para selecionar a data.
        # `selectmode='day'` define que o calendário permite selecionar apenas um dia por vez.
        # `date_pattern='dd/MM/yyyy'` define o formato de exibição da data como dia/mês/ano.
        self.cal_data = Calendar(quadro_esquerdo, selectmode='day', date_pattern='dd/MM/yyyy')

        # Posiciona o calendário no quadro esquerdo.
        # `pady=5` adiciona 5 pixels de espaçamento vertical
        #       acima e abaixo do calendário.
        self.cal_data.pack(pady=5)

        # Obtém a data atual no formato "dd/MM/yyyy".
        # `datetime.now()` retorna a data e hora atuais.
        # `strftime("%d/%m/%Y")` formata a data no padrão desejado.
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        # Define a data atual como a data selecionada no calendário.
        # `selection_set(data_hoje)` seleciona a data de hoje no calendário.
        self.cal_data.selection_set(data_hoje)

        # Cria um botão no quadro esquerdo com o texto "Atualizar Mapa".
        # `text="Atualizar Mapa"` define o texto exibido no botão.
        # `command=self.atualizar_mapa` associa a função `atualizar_mapa` ao
        #       botão para ser chamada ao clicar.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do botão.
        ttk.Button(quadro_esquerdo, text="Atualizar Mapa", command=self.atualizar_mapa).pack(pady=5)

        # Cria um botão no quadro esquerdo com o texto "Cadastrar Reserva".
        # `text="Cadastrar Reserva"` define o texto exibido no botão.
        # `command=self.abrir_cadastro_reserva` associa a função `abrir_cadastro_reserva` ao
        #       botão para ser chamada ao clicar.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do botão.
        ttk.Button(quadro_esquerdo, text="Cadastrar Reserva", command=self.abrir_cadastro_reserva).pack(pady=5)

        # Cria um botão no quadro esquerdo com o texto "Pesquisar Histórico".
        # `text="Pesquisar Histórico"` define o texto exibido no botão.
        # `command=self.abrir_pesquisa_reservas` associa a função `abrir_pesquisa_reservas` ao
        #       botão para ser chamada ao clicar.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do botão.
        ttk.Button(quadro_esquerdo, text="Pesquisar Histórico", command=self.abrir_pesquisa_reservas).pack(pady=5)

        # Quadro direito - mapa de horários
        # Cria um quadro no lado direito do quadro principal.
        # `ttk.Frame(quadro_principal)` cria um novo contêiner associado ao quadro principal.
        # `side='right'` posiciona o quadro à direita do contêiner principal.
        # `fill='both'` faz com que o quadro preencha tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o quadro ocupe espaço adicional quando o tamanho da janela muda.
        # `padx=10` e `pady=10` adicionam 10 pixels de espaçamento ao redor do quadro.
        quadro_direito = ttk.Frame(quadro_principal)
        quadro_direito.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Adiciona um rótulo ao quadro direito com o texto "Mapa de Horários".
        # `ttk.Label(quadro_direito)` cria um rótulo associado ao quadro direito.
        # `text="Mapa de Horários"` define o texto exibido no rótulo.
        # `font=("Arial", 16, "bold")` especifica a fonte, o tamanho do
        #       texto e aplica o estilo em negrito.
        # `pack(pady=5)` posiciona o rótulo no quadro, adicionando 5 pixels de
        #       espaçamento vertical acima e abaixo.
        ttk.Label(quadro_direito, text="Mapa de Horários", font=("Arial", 16, "bold")).pack(pady=5)

        # Cria um canvas dentro do quadro direito, que servirá como área de exibição para o mapa.
        # `tk.Canvas(quadro_direito)` cria o canvas e associa ao quadro direito.
        # `bg="#ffffff"` define o fundo do canvas como branco.
        # `pack(side='left')` posiciona o canvas no lado esquerdo do quadro direito.
        # `fill='both'` faz com que o canvas preencha tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o canvas ocupe espaço adicional ao redimensionar a janela.
        self.canvas_mapa = tk.Canvas(quadro_direito, bg="#ffffff")
        self.canvas_mapa.pack(side='left', fill='both', expand=True)

        # Cria uma barra de rolagem vertical associada ao canvas.
        # `ttk.Scrollbar(quadro_direito)` cria a barra de rolagem no quadro direito.
        # `orient="vertical"` especifica a orientação da barra como vertical.
        # `command=self.canvas_mapa.yview` associa a barra de rolagem ao movimento vertical do canvas.
        # `pack(side='right')` posiciona a barra no lado direito do quadro direito.
        # `fill='y'` faz com que a barra de rolagem preencha toda a altura do quadro.
        barra_scroll = ttk.Scrollbar(quadro_direito, orient="vertical", command=self.canvas_mapa.yview)
        barra_scroll.pack(side='right', fill='y')

        # Configura o canvas para usar a barra de rolagem vertical.
        # `yscrollcommand=barra_scroll.set` sincroniza o movimento da
        #       barra de rolagem com o canvas.
        self.canvas_mapa.configure(yscrollcommand=barra_scroll.set)

        # Cria um frame dentro do canvas para organizar os horários.
        # `ttk.Frame(self.canvas_mapa)` cria o frame como um elemento dentro do canvas.
        self.frame_horarios = ttk.Frame(self.canvas_mapa)

        # Insere o frame no canvas como uma janela.
        # `(0, 0)` define as coordenadas da posição inicial do frame no canvas.
        # `window=self.frame_horarios` associa o frame à janela criada no canvas.
        # `anchor="nw"` fixa o frame no canto superior esquerdo do canvas.
        self.canvas_mapa.create_window((0, 0), window=self.frame_horarios, anchor="nw")

        # Vincula o evento de reconfiguração do frame ao método `ajustar_scroll`.
        # `<Configure>` é acionado sempre que o tamanho do frame é alterado.
        # Isso permite ajustar dinamicamente o tamanho do canvas para
        #       incluir todos os horários.
        self.frame_horarios.bind("<Configure>", self.ajustar_scroll)

        # Chama o método para atualizar o mapa de horários.
        # Essa ação inicializa a exibição dos dados no canvas.
        self.atualizar_mapa()


    # Define o método para ajustar a área de rolagem do canvas.
    def ajustar_scroll(self, event):

        # Atualiza a região de rolagem do canvas para incluir
        #       todos os elementos visíveis.
        # `self.canvas_mapa.bbox("all")` calcula as coordenadas da área total
        #       ocupada pelos elementos no canvas.
        # `scrollregion` é a propriedade que define a área rolável do canvas.
        self.canvas_mapa.configure(scrollregion=self.canvas_mapa.bbox("all"))


    # Define o método para atualizar o mapa de horários exibido.
    def atualizar_mapa(self):

        # Remove todos os widgets existentes no frame de horários.
        for widget in self.frame_horarios.winfo_children():

            # Destrói cada widget presente no frame.
            widget.destroy()

        # Obtém o nome do lugar selecionado na combobox.
        lugar_nome = self.combo_lugar.get()

        # Verifica se nenhum lugar foi selecionado.
        if not lugar_nome:

            # Sai do método caso não haja lugar selecionado.
            return

        # Verifica se o lugar selecionado está mapeado no
        #       dicionário `mapa_lugares`.
        if lugar_nome not in self.mapa_lugares:

            # Sai do método caso o lugar não esteja no mapeamento.
            return

        # Obtém o ID do lugar selecionado como string a partir do
        #       dicionário `mapa_lugares`.
        lugar_id_str = self.mapa_lugares[lugar_nome]

        # Obtém a data selecionada no calendário.
        data_sel = self.cal_data.get_date()

        # Busca as reservas no banco de dados para o lugar e a data selecionados.
        reservas_dia = self.reserva.buscar_reservas({

            # Converte o ID do lugar para um formato válido de ObjectId.
            "lugar_id": ObjectId(lugar_id_str),

            # Filtra pela data selecionada no calendário.
            "data": data_sel

        })

        # Define o horário inicial para o mapa de horários (08:00).
        horario_atual = datetime.strptime("08:00", "%H:%M")

        # Define o horário final para o mapa de horários (23:59).
        horario_fim = datetime.strptime("23:59", "%H:%M")

        # Variável para controlar a posição na grade onde os horários serão exibidos.
        # `linha_coluna_A` é usada para controlar a linha da grade.
        linha_coluna_A = 0

        # `linha_coluna_B` é usada para controlar a coluna da grade.
        linha_coluna_B = 0

        # Enquanto o horário atual não ultrapassar o horário final, itera pelos horários.
        while horario_atual <= horario_fim:

            # Formata o horário atual como string no formato "HH:MM".
            hora_str = horario_atual.strftime("%H:%M")

            # Calcula o próximo intervalo de 30 minutos e o formata como string.
            prox_str = (horario_atual + timedelta(minutes=30)).strftime("%H:%M")

            # Inicializa uma variável para verificar se o intervalo está reservado.
            reservado = False

            # Itera pelas reservas do dia para verificar conflitos.
            for reserva_dia in reservas_dia:

                # Verifica se o horário atual está dentro do intervalo da reserva.
                if (reserva_dia["hora_inicial"] <= hora_str < reserva_dia["hora_final"]):

                    # Marca o intervalo como reservado se houver conflito.
                    reservado = True

                    # Interrompe a busca nas reservas, pois já encontrou um conflito.
                    break

            # Define a cor de fundo do rótulo com base na disponibilidade do horário.
            # Se o horário está reservado (`reservado=True`), a cor será amarelo claro (#ffeb3b).
            # Caso contrário, a cor será verde claro (#a5d6a7), indicando disponibilidade.
            cor_fundo = "#ffeb3b" if reservado else "#a5d6a7"

            # Cria um rótulo (label) que representará o intervalo de
            #       horário no mapa de horários.
            label_hora = tk.Label(

                # O rótulo será colocado dentro do `self.frame_horarios`,
                #       que contém todos os horários.
                self.frame_horarios,

                # Define o texto do rótulo como o intervalo de horários
                #       atual, no formato "HH:MM - HH:MM".
                text=f"{hora_str} - {prox_str}",

                # Define a cor de fundo do rótulo, usando a variável `cor_fundo`
                #       calculada anteriormente.
                bg=cor_fundo,

                # Define a largura do rótulo como 30 caracteres (ajuda a
                #       padronizar os tamanhos dos rótulos).
                width=30,

                # Centraliza o texto no rótulo horizontalmente.
                anchor='center',

                # Define a fonte do texto do rótulo como Arial, tamanho 14,
                #       para melhorar a legibilidade.
                font=("Arial", 14)

            )

            # Verifica se o horário não está reservado.
            if not reservado:

                # Se o horário está disponível (não reservado), adiciona um evento de clique no rótulo.
                # O evento vincula o clique esquerdo do mouse ("<Button-1>") à função `clicar_horario`.
                # A função será chamada com o horário inicial (`hora_str`) como argumento.
                label_hora.bind("<Button-1>", lambda e, h=hora_str: self.clicar_horario(h))

            # Divide visualmente os horários em duas colunas para melhor organização.
            # Os horários até "15:30" serão posicionados na coluna 0.
            if hora_str <= "15:30":

                # Posiciona o rótulo na linha atual (`linha_coluna_A`) da coluna 0.
                # `padx=5` e `pady=3` adicionam espaçamento horizontal e
                #       vertical entre os rótulos.
                # `sticky='ew'` faz com que o rótulo se expanda horizontalmente
                #       para ocupar o espaço disponível.
                label_hora.grid(row=linha_coluna_A, column=0, padx=5, pady=3, sticky='ew')

                # Incrementa o contador de linhas da coluna 0.
                linha_coluna_A += 1

            else:

                # Os horários após "15:30" serão posicionados na coluna 1.
                # Posiciona o rótulo na linha atual (`linha_coluna_B`) da coluna 1.
                label_hora.grid(row=linha_coluna_B, column=1, padx=5, pady=3, sticky='ew')

                # Incrementa o contador de linhas da coluna 1.
                linha_coluna_B += 1

            # Avança o horário atual em 30 minutos para criar o próximo intervalo.
            # Usa `timedelta` para manipular o tempo com precisão.
            horario_atual += timedelta(minutes=30)

        # Configura a coluna 0 do `frame_horarios` para se expandir proporcionalmente.
        # `weight=1` indica que a coluna receberá uma parte igual do espaço disponível.
        self.frame_horarios.grid_columnconfigure(0, weight=1)

        # Configura a coluna 1 do `frame_horarios` para se expandir proporcionalmente.
        # `weight=1` assegura que ambas as colunas (0 e 1) compartilhem o
        #       espaço horizontal de forma igual.
        self.frame_horarios.grid_columnconfigure(1, weight=1)


    def clicar_horario(self, hora_inicial):

        # Obtém a data selecionada no calendário.
        # `self.cal_data.get_date()` retorna a data selecionada no formato configurado.
        data_sel = self.cal_data.get_date()

        # Abre a janela de cadastro de reserva.
        # `JanelaCadastroReserva` é a classe que gerencia o cadastro de reservas.
        # `self.janela` é a janela pai atual (JanelaPrincipalReservas), passada como referência.
        # `self.reserva` é a instância do sistema de reservas, necessária para gerenciar os dados.
        # `self` é a instância atual, passada para que a janela de cadastro possa interagir com ela.
        # `data_inicial=data_sel` e `hora_inicial=hora_inicial` fornecem a
        #       data e hora selecionadas para pré-preencher o formulário de cadastro.
        JanelaCadastroReserva(self.janela,
                              self.reserva,
                              self,
                              data_inicial=data_sel,
                              hora_inicial=hora_inicial)


    # Define o método para carregar os lugares disponíveis no banco de dados.
    def carregar_lugares(self):

        # Busca todos os registros na coleção de lugares do banco de dados.
        lugares = self.reserva.colecao_lugares.find()

        # Inicializa uma lista para armazenar os nomes dos lugares.
        lista_nomes = []

        # Itera sobre cada lugar retornado na consulta.
        for lugar in lugares:

            # Obtém o nome do lugar.
            nome_lug = lugar["nome"]

            # Converte o ID do lugar para string.
            _id = str(lugar["_id"])

            # Adiciona o nome do lugar à lista de nomes.
            lista_nomes.append(nome_lug)

            # Mapeia o nome do lugar ao seu ID para referência futura.
            self.mapa_lugares[nome_lug] = _id

        # Define os valores da combobox com a lista de nomes dos lugares.
        self.combo_lugar["values"] = lista_nomes

        # Se houver lugares disponíveis, define o primeiro item
        #       como o selecionado por padrão.
        if lista_nomes:
            self.combo_lugar.current(0)


    def abrir_cadastro_reserva(self):

        # Obtém a data atualmente selecionada no calendário.
        # `self.cal_data.get_date()` retorna a data no formato
        #       configurado ('dd/MM/yyyy').
        data_sel = self.cal_data.get_date()

        # Abre a janela de cadastro de reserva.
        # `JanelaCadastroReserva` é a classe responsável por criar a interface de cadastro.
        # `self.janela` é a janela pai (JanelaPrincipalReservas) que será passada como referência.
        # `self.reserva` é a instância do sistema de reservas, utilizada para manipular os dados no MongoDB.
        # `self` (JanelaPrincipalReservas) é passado para permitir a interação com a janela principal.
        # `data_inicial=data_sel` define a data selecionada no calendário como valor inicial no formulário.
        JanelaCadastroReserva(self.janela, self.reserva, self, data_inicial=data_sel)

    # Abre a janela de pesquisa de reservas.
    # `JanelaPesquisaReservas` é a classe que gerencia a interface
    #       para busca de reservas no sistema.
    def abrir_pesquisa_reservas(self):

        # `self.janela` é a referência para a janela principal (JanelaPrincipalReservas),
        #       que será utilizada como janela pai para a nova janela de pesquisa.
        # `self.reserva` é a instância do sistema de reservas, fornecendo
        #       acesso às coleções e métodos necessários para a pesquisa.
        # `self` é passado como referência para permitir interação com a
        #       janela principal, se necessário.
        JanelaPesquisaReservas(self.janela, self.reserva, self)


###############################################################################
#             JANELA DE CADASTRO DE RESERVA (FECHA AO FINALIZAR)             #
###############################################################################
class JanelaCadastroReserva:

    """
    Classe que cria uma janela para o cadastro de novas reservas.
    Permite selecionar o lugar, data, hora e itens consumidos, além
            de salvar a reserva no banco de dados.
    """

    # Inicializa a janela de cadastro de reservas.
    def __init__(self, parent, reserva: ReservaQuadra, janela_reservas,
                 data_inicial=None, hora_inicial=None):


        # `parent`: objeto da janela pai que invocou esta janela.
        # Usado como referência para criar uma janela modal ou complementar.
        self.parent = parent

        # `reserva`: instância de `ReservaQuadra`, gerencia
        #       conexão e operações do MongoDB.
        # É usado para salvar as informações da reserva no banco de dados.
        self.reserva = reserva

        # `janela_reservas`: referência da janela principal de
        #       reservas (JanelaPrincipalReservas).
        # Isso permite atualizar a visualização ou interagir com a
        #       janela principal após o cadastro.
        self.janela_reservas = janela_reservas

        # Cria uma nova janela vinculada ao `parent`.
        # `tk.Toplevel` cria uma janela secundária sobre a janela principal.
        self.janela = tk.Toplevel(parent)

        # Define o título da janela como "Cadastrar Reserva".
        # Esse título aparece na barra superior da janela.
        self.janela.title("Cadastrar Reserva")

        # Define o estado da janela como "zoomed", o que significa
        #       que a janela será exibida em tela cheia.
        self.janela.state("zoomed")

        # Cria um quadro principal para organizar os widgets dentro da janela.
        # `ttk.Frame` é usado como um contêiner para outros widgets.
        quadro_principal = ttk.Frame(self.janela)

        # Posiciona o quadro principal para ocupar todo o espaço disponível na janela.
        # `fill='both'` faz com que o quadro se expanda tanto na
        #       largura quanto na altura.
        # `expand=True` permite que o quadro cresça junto com a
        #       janela caso ela seja redimensionada.
        quadro_principal.pack(fill='both', expand=True)

        # Cria um quadro superior dentro do quadro principal.
        # Este quadro será usado para posicionar o botão "Voltar" e outros elementos no topo.
        quadro_topo = ttk.Frame(quadro_principal)

        # Posiciona o quadro superior no topo da janela.
        # `side='top'` define que o quadro será posicionado na parte superior da janela.
        # `fill='x'` permite que o quadro se expanda horizontalmente para
        #       ocupar toda a largura disponível.
        quadro_topo.pack(side='top', fill='x')

        # Cria um botão no quadro superior para retornar à janela anterior.
        # `text="Voltar"` define o texto exibido no botão como "Voltar".
        # `command=self.janela.destroy` associa a ação de fechar a janela ao clicar no botão.
        # `side='left'` posiciona o botão no lado esquerdo do quadro.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(quadro_topo, text="Voltar", command=self.janela.destroy).pack(side='left', padx=5)

        # Cria um rótulo no quadro superior como título da janela de cadastro.
        # `text="Cadastro de Reserva"` define o texto exibido no rótulo
        #       como "Cadastro de Reserva".
        # `font=("Arial", 16, "bold")` define a fonte do texto como Arial,
        #       tamanho 16, e com estilo em negrito.
        # `side='left'` posiciona o rótulo ao lado do botão "Voltar".
        # `padx=20` adiciona 20 pixels de espaçamento horizontal entre o botão e o rótulo.
        ttk.Label(quadro_topo,
                  text="Cadastro de Reserva",
                  font=("Arial", 16, "bold")).pack(side='left', padx=20)

        # Quadro principal: 2 colunas (esquerda / direita)
        # Cria um quadro para o lado esquerdo dentro do quadro principal.
        # `quadro_principal` é o contêiner pai deste quadro.
        quadro_esquerda = ttk.Frame(quadro_principal)

        # Posiciona o quadro esquerdo no lado esquerdo do contêiner principal.
        # `side='left'` define que o quadro será posicionado à esquerda.
        # `fill='both'` permite que o quadro se expanda para preencher
        #       tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o quadro expanda para ocupar o espaço restante se disponível.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal externo em ambos os lados do quadro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical externo em ambos os lados do quadro.
        quadro_esquerda.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        # Cria um quadro para o lado direito dentro do quadro principal.
        # `quadro_principal` é o contêiner pai deste quadro.
        quadro_direita = ttk.Frame(quadro_principal)

        # Posiciona o quadro direito no lado direito do contêiner principal.
        # `side='right'` define que o quadro será posicionado à direita.
        # `fill='both'` permite que o quadro se expanda para preencher
        #       tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o quadro expanda para ocupar o espaço restante se disponível.
        # `padx=10` adiciona 10 pixels de espaçamento horizontal externo em ambos os lados do quadro.
        # `pady=10` adiciona 10 pixels de espaçamento vertical externo em ambos os lados do quadro.
        quadro_direita.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Esquerda: Cliente, Lugar, Data, Horas
        # Define o contador `linha` para rastrear a posição na grade do quadro esquerdo.
        linha = 0

        # Cria um rótulo para o campo "Cliente".
        # `text="Cliente:"` define o texto exibido no rótulo.
        # `grid(row=linha, column=0)` posiciona o rótulo na linha 0 e na coluna 0.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento externo horizontal e vertical.
        # `sticky='e'` alinha o rótulo à direita (east) dentro da célula da grade.
        ttk.Label(quadro_esquerda,
                  text="Cliente:").grid(row=linha, column=0, padx=5, pady=5, sticky='e')

        # Cria uma combobox (caixa de seleção) para selecionar um cliente.
        # `state="readonly"` define a combobox como somente leitura, ou
        #       seja, o usuário pode apenas selecionar itens.
        # `width=30` define a largura da combobox.
        self.combo_cliente = ttk.Combobox(quadro_esquerda, state="readonly", width=30)

        # Posiciona a combobox na grade.
        # `grid(row=linha, column=1)` coloca a combobox na linha 0 e
        #       coluna 1 (ao lado do rótulo "Cliente").
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento
        #       externo horizontal e vertical.
        # `sticky='w'` alinha a combobox à esquerda (west) dentro da célula da grade.
        self.combo_cliente.grid(row=linha, column=1, padx=5, pady=5, sticky='w')

        # Inicializa um dicionário vazio para mapear os nomes dos clientes para seus IDs.
        # Será usado para associar os nomes exibidos na
        #       combobox aos IDs no banco de dados.
        self.mapa_clientes = {}

        # Carrega a lista de clientes do banco de dados e preenche a combobox.
        self.carregar_clientes()

        # Incrementa o contador `linha` para posicionar o próximo
        #       conjunto de widgets na linha seguinte.
        linha += 1

        # Cria um rótulo para o campo "Lugar".
        # `text="Lugar:"` define o texto exibido no rótulo.
        # `grid(row=linha, column=0)` posiciona o rótulo na linha atual e na coluna 0.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='e'` alinha o rótulo à direita (east) dentro da célula da grade.
        ttk.Label(quadro_esquerda,
                  text="Lugar:").grid(row=linha,
                                      column=0,
                                      padx=5,
                                      pady=5,
                                      sticky='e')

        # Cria uma combobox (caixa de seleção) para selecionar um lugar.
        # `state="readonly"` define a combobox como somente leitura, ou
        #       seja, o usuário pode apenas selecionar itens.
        # `width=30` define a largura da combobox.
        self.combo_lugar = ttk.Combobox(quadro_esquerda, state="readonly", width=30)

        # Posiciona a combobox na grade.
        # `grid(row=linha, column=1)` coloca a combobox na linha atual e
        #       coluna 1 (ao lado do rótulo "Lugar").
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='w'` alinha a combobox à esquerda (west) dentro da célula da grade.
        self.combo_lugar.grid(row=linha,
                              column=1,
                              padx=5,
                              pady=5,
                              sticky='w')

        # Inicializa um dicionário vazio para mapear os nomes dos
        #       lugares para seus IDs.
        # Este dicionário será usado para associar os nomes exibidos na
        #       combobox aos IDs no banco de dados.
        self.mapa_lugares = {}

        # Carrega a lista de lugares do banco de dados e preenche a combobox.
        self.carregar_lugares()

        # Incrementa o contador `linha` para posicionar o próximo
        #       conjunto de widgets na linha seguinte.
        linha += 1

        # Cria um rótulo para o campo "Hora Inicial".
        # `text="Hora Inicial (HH:MM):"` define o texto exibido no rótulo.
        # `grid(row=linha, column=0)` posiciona o rótulo na linha atual e na coluna 0.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='e'` alinha o rótulo à direita (east) dentro da célula da grade.
        ttk.Label(quadro_esquerda,
                  text="Hora Inicial (HH:MM):").grid(row=linha,
                                                     column=0,
                                                     padx=5,
                                                     pady=5,
                                                     sticky='e')

        # Cria uma variável de controle do tipo `StringVar` para
        #       armazenar o valor da hora inicial.
        # O valor inicial da variável é definido com `hora_inicial` se
        #       fornecido, caso contrário, é uma string vazia.
        self.var_hora_inicial = tk.StringVar(value=hora_inicial if hora_inicial else "")

        # Cria uma entrada de texto para o usuário digitar a hora inicial.
        # `textvariable=self.var_hora_inicial` vincula a entrada à
        #       variável `self.var_hora_inicial`, permitindo acessar e atualizar o valor.
        # `width=10` define a largura da entrada de texto.
        ttk.Entry(quadro_esquerda, textvariable=self.var_hora_inicial, width=10).grid(
            row=linha, column=1, padx=5, pady=5, sticky='w'
        )
        # A entrada é posicionada na linha atual (linha), coluna 1, ao lado do rótulo.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='w'` alinha a entrada à esquerda (west) dentro da célula da grade.

        # Incrementa o contador `linha` para posicionar o próximo
        #       conjunto de widgets na linha seguinte.
        linha += 1

        # Cria um rótulo para o campo "Hora Final".
        # `text="Hora Final (HH:MM):"` define o texto exibido no rótulo.
        # `grid(row=linha, column=0)` posiciona o rótulo na linha atual e na coluna 0.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='e'` alinha o rótulo à direita (east) dentro da célula da grade.
        ttk.Label(quadro_esquerda,
                  text="Hora Final (HH:MM):").grid(row=linha,
                                                   column=0,
                                                   padx=5,
                                                   pady=5,
                                                   sticky='e')

        # Cria uma variável de controle do tipo `StringVar` para
        #       armazenar o valor da hora final.
        # O valor inicial da variável é uma string vazia por padrão.
        self.var_hora_final = tk.StringVar()

        # Cria uma entrada de texto para o usuário digitar a hora final.
        # `textvariable=self.var_hora_final` vincula a entrada à
        #       variável `self.var_hora_final`, permitindo acessar e atualizar o valor.
        # `width=10` define a largura da entrada de texto.
        ttk.Entry(quadro_esquerda, textvariable=self.var_hora_final, width=10).grid(
            row=linha, column=1, padx=5, pady=5, sticky='w'
        )
        # A entrada é posicionada na linha atual (linha), coluna 1, ao lado do rótulo.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='w'` alinha a entrada à esquerda (west) dentro da célula da grade.

        # Incrementa o contador `linha` para posicionar o próximo
        #       conjunto de widgets na linha seguinte.
        linha += 1

        # Cria um rótulo para o campo "Data da Reserva".
        # `text="Data da Reserva:"` define o texto exibido no rótulo.
        # `grid(row=linha, column=0)` posiciona o rótulo na linha atual e na coluna 0.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='e'` alinha o rótulo à direita (east) dentro da célula da grade.
        ttk.Label(quadro_esquerda,
                  text="Data da Reserva:").grid(row=linha,
                                                column=0,
                                                padx=5,
                                                pady=5,
                                                sticky='e')

        # Cria um calendário para selecionar a data da reserva.
        # `quadro_esquerda` é o contêiner onde o calendário será inserido.
        # `selectmode='day'` configura o calendário para permitir a seleção de um único dia.
        # `date_pattern='dd/MM/yyyy'` define o formato da data exibida como dia/mês/ano.
        self.cal_reserva = Calendar( quadro_esquerda,
                                    selectmode='day',
                                    date_pattern='dd/MM/yyyy') # O calendário será posicionado na próxima etapa.

        # Posiciona o calendário na grade do quadro esquerdo.
        # `row=linha` especifica a linha atual onde o calendário será colocado.
        # `column=1` posiciona o calendário na coluna 1, ao lado do rótulo "Data da Reserva".
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='w'` alinha o calendário à esquerda (west) dentro da célula da grade.
        self.cal_reserva.grid(row=linha, column=1, padx=5, pady=5, sticky='w')

        # Verifica se um valor inicial para a data foi fornecido no argumento `data_inicial`.
        # Se `data_inicial` estiver definido, define a data selecionada do calendário.
        # `self.cal_reserva.selection_set(data_inicial)` seleciona a data fornecida no calendário.
        if data_inicial:
            self.cal_reserva.selection_set(data_inicial)

        # Incrementa a variável `linha` para posicionar o próximo widget na linha seguinte.
        linha += 1

        # Cria um rótulo para exibir o texto "Valor/Hora (R$):".
        # `text="Valor/Hora (R$):"` define o texto do rótulo.
        # `row=linha` especifica a linha atual onde o rótulo será colocado.
        # `column=0` posiciona o rótulo na primeira coluna (à esquerda).
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical externo.
        # `sticky='e'` alinha o rótulo à direita (east) dentro da célula da grade.
        ttk.Label(quadro_esquerda,
                  text="Valor/Hora (R$):").grid(row=linha,
                                                column=0,
                                                padx=5,
                                                pady=5,
                                                sticky='e')

        # Cria uma variável de texto para armazenar o valor/hora inserido pelo usuário.
        # `self.var_valor_hora` será vinculada ao campo de entrada.
        self.var_valor_hora = tk.StringVar()

        # Cria um campo de entrada para permitir que o usuário insira o valor/hora.
        # `textvariable=self.var_valor_hora` vincula o valor
        #       inserido à variável `self.var_valor_hora`.
        # `width=10` define a largura do campo de entrada em 10 caracteres.
        ttk.Entry(quadro_esquerda,  # O campo de entrada será colocado no quadro esquerdo.
                    textvariable=self.var_valor_hora,  # Variável associada ao campo.
                    width=10  # Define a largura do campo de entrada.
                ).grid(row=linha,  # Coloca o campo na linha atual.
                        column=1,  # Posiciona o campo na segunda coluna (à direita do rótulo).
                        padx=5,  # Adiciona 5 pixels de espaçamento horizontal externo.
                        pady=5,  # Adiciona 5 pixels de espaçamento vertical externo.
                        sticky='w')  # Alinha o campo de entrada à esquerda (west) dentro da célula da grade.


        # Define uma função interna chamada `calcular_valor_hora`.
        def calcular_valor_hora():

            # Obtém o nome do lugar selecionado no combobox e remove espaços extras ao redor.
            # `self.combo_lugar.get()` retorna o texto selecionado no combobox.
            # `strip()` remove quaisquer espaços no início e no final do texto.
            lugar_nome_escolhido = self.combo_lugar.get().strip()

            # Verifica se o nome do lugar selecionado está no dicionário `self.mapa_lugares`.
            # `not in self.mapa_lugares` retorna True se o lugar não for encontrado no dicionário.
            if lugar_nome_escolhido not in self.mapa_lugares:

                # Exibe uma mensagem de aviso ao usuário se o lugar não for válido.
                # `messagebox.showwarning` exibe uma caixa de diálogo
                #       com um título, uma mensagem
                #       e um ícone de aviso.
                # `"Aviso"` é o título da caixa de diálogo.
                # `"Lugar inválido. Selecione da lista."` é a mensagem exibida.
                messagebox.showwarning("Aviso",
                                       "Lugar inválido. Selecione da lista.")

                # Interrompe a execução da função, já que não há
                #       um lugar válido selecionado.
                return

            # Obtém o ID do lugar a partir do dicionário `self.mapa_lugares`.
            # Usa o nome do lugar selecionado (`lugar_nome_escolhido`)
            #       como chave para buscar o ID.
            lugar_id = self.mapa_lugares[lugar_nome_escolhido]

            # Obtém a hora inicial inserida pelo usuário no campo correspondente.
            # `self.var_hora_inicial.get()` retorna o valor da variável associada ao campo.
            # `strip()` remove espaços em branco no início e no final do texto.
            hi = self.var_hora_inicial.get().strip()

            # Obtém a hora final inserida pelo usuário no campo correspondente.
            # `self.var_hora_final.get()` retorna o valor da variável associada ao campo.
            # `strip()` remove espaços em branco no início e no final do texto.
            hf = self.var_hora_final.get().strip()

            # Verifica se as horas inicial e final estão preenchidas.
            # `not hi` é True se o campo `hi` estiver vazio.
            # `not hf` é True se o campo `hf` estiver vazio.
            if not hi or not hf:

                # Exibe uma mensagem de aviso ao usuário se os campos
                #       de horas estiverem vazios.
                # `messagebox.showwarning` cria uma caixa de diálogo de aviso.
                # `"Aviso"` é o título da mensagem.
                # `"Preencha Hora Inicial e Final."` é o texto exibido ao usuário.
                messagebox.showwarning("Aviso", "Preencha Hora Inicial e Final.")

                # Interrompe a execução da função, já que os campos
                #       necessários não estão preenchidos.
                return

            try:

                # Tenta calcular o valor da reserva usando os dados fornecidos.
                # `self.reserva.calcular_valor_reserva` calcula o valor com
                #       base no ID do lugar e nas horas inicial e final.
                # `valor_calc` recebe o resultado do cálculo.
                valor_calc = self.reserva.calcular_valor_reserva(lugar_id, hi, hf)

                # Atualiza o campo `self.var_valor_hora` com o valor calculado,
                #       formatado com duas casas decimais.
                # `f"{valor_calc:.2f}"` formata o valor em um formato monetário (ex.: "100.00").
                self.var_valor_hora.set(f"{valor_calc:.2f}")

                # Chama o método `self.atualizar_total` para recalcular o total da
                #       reserva (incluindo outros itens, se aplicável).
                self.atualizar_total()


            except ValueError as erro:

                # Captura qualquer erro de validação gerado no cálculo do valor da reserva.
                # Exibe uma mensagem de erro ao usuário.
                # `"Erro"` é o título da mensagem.
                # `str(erro)` converte o erro gerado em texto para exibição.
                messagebox.showerror("Erro", str(erro))


        # Cria um botão para calcular o valor da reserva por hora.
        # `text="Calcular Valor/Hora"` define o texto exibido no botão.
        # `command=calcular_valor_hora` associa a função `calcular_valor_hora` à ação de clique no botão.
        ttk.Button(quadro_esquerda,  # Define o quadro onde o botão será colocado.
                   text="Calcular Valor/Hora",  # Texto do botão.
                   command=calcular_valor_hora  # Função chamada ao clicar no botão.
                   ).grid(row=linha,  # Define a linha onde o botão será posicionado.
                          column=1,  # Define a coluna onde o botão será posicionado.
                          sticky='w',  # Alinha o botão à esquerda da célula.
                          padx=5,  # Adiciona 5 pixels de espaçamento horizontal ao redor do botão.
                          pady=5)  # Adiciona 5 pixels de espaçamento vertical ao redor do botão.

        # Cria um quadro para organizar a exibição dos itens consumidos.
        # `quadro_direita` é o contêiner principal onde este quadro será inserido.
        # Define o contêiner pai onde o quadro será colocado.
        quadro_tree = ttk.Frame(quadro_direita)

        # Posiciona o quadro no topo da área direita.
        # `side='top'` posiciona o quadro na parte superior.
        # `fill='both'` permite que o quadro preencha tanto a largura quanto a altura disponíveis.
        # `expand=True` permite que o quadro se expanda para ocupar espaço adicional, se houver.
        quadro_tree.pack(side='top',  # Posiciona o quadro no topo da área.
                         fill='both',  # Preenche completamente o espaço disponível em largura e altura.
                         expand=True)  # Permite expansão para ocupar espaço extra.

        # Adiciona um rótulo para indicar a seção de itens consumidos.
        # `quadro_tree` é o contêiner onde este rótulo será inserido.
        ttk.Label(quadro_tree,  # Define o contêiner onde o rótulo será colocado.
                  text="Itens Consumidos:"  # Texto exibido no rótulo.
                  ).pack(pady=5)  # Adiciona 5 pixels de espaçamento vertical ao redor do rótulo.

        # Cria uma tabela (Treeview) para exibir os itens consumidos.
        # `quadro_tree` é o contêiner onde a tabela será inserida.
        self.tree_itens = ttk.Treeview(quadro_tree,  # Define o quadro pai onde a tabela será posicionada.
                                       columns=("Produto", "Qtd", "Preço", "Custo", "ID"),
                                       # Define as colunas da tabela.
                                       show='headings',
                                       # Exibe apenas os cabeçalhos das colunas, sem a coluna inicial padrão.
                                       height=8)  # Define a altura da tabela como 8 linhas visíveis.

        # Configura o cabeçalho da coluna "Produto".
        # Define o texto exibido como "Produto".
        self.tree_itens.heading("Produto", text="Produto")

        # Configura o cabeçalho da coluna "Qtd" (quantidade).
        # Define o texto exibido como "Qtd".
        self.tree_itens.heading("Qtd", text="Qtd")

        # Configura o cabeçalho da coluna "Preço".
        # Define o texto exibido como "R$/Un" (Preço por unidade em reais).
        self.tree_itens.heading("Preço", text="R$/Un")

        # Configura o cabeçalho da coluna "Custo".
        # Define o texto exibido como "Custo/Un" (Custo por unidade).
        self.tree_itens.heading("Custo", text="Custo/Un")

        # Configura o cabeçalho da coluna "ID".
        # Define o texto exibido como "prod_id" (identificador do produto).
        self.tree_itens.heading("ID", text="prod_id")

        # Define a largura da coluna "ID" como 0 e impede que ela seja redimensionada.
        # Isso oculta visualmente a coluna, mas mantém os dados acessíveis.
        self.tree_itens.column("ID", width=0, stretch=False)

        # Posiciona a tabela no contêiner `quadro_tree`.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento ao redor da tabela.
        # `fill='both'` permite que a tabela preencha toda a largura e altura disponíveis.
        # `expand=True` permite que a tabela se expanda para ocupar espaço extra, se houver.
        self.tree_itens.pack(padx=5,  # Espaçamento horizontal de 5 pixels.
                             pady=5,  # Espaçamento vertical de 5 pixels.
                             fill='both',  # Preenche completamente o espaço disponível em largura e altura.
                             expand=True)  # Permite expansão para ocupar espaço extra.

        # Cria um quadro para organizar os botões relacionados à tabela de itens.
        # `quadro_tree` é o contêiner onde este quadro será inserido.
        quadro_tree_botoes = ttk.Frame(quadro_tree)

        # Posiciona o quadro dos botões logo abaixo da tabela.
        # `pady=5` adiciona 5 pixels de espaçamento vertical acima e abaixo do quadro.
        quadro_tree_botoes.pack(
            pady=5  # Espaçamento vertical ao redor do quadro.
        )

        # Cria um botão para adicionar itens à tabela.
        # `text="Adicionar Item"` define o texto exibido no botão.
        # `command=self.adicionar_item` associa a ação de adicionar um item ao botão.
        ttk.Button(quadro_tree_botoes,  # Define o quadro onde o botão será inserido.
                   text="Adicionar Item",  # Texto exibido no botão.
                   command=self.adicionar_item  # Método chamado ao clicar no botão.
                   ).pack(side='left',  # Posiciona o botão à esquerda dentro do quadro.
                          padx=5)  # Adiciona 5 pixels de espaçamento horizontal entre os botões.

        # Cria um botão para remover itens selecionados na tabela.
        # `text="Remover Item"` define o texto exibido no botão.
        # `command=self.remover_item` associa a ação de remover um item ao botão.
        ttk.Button(quadro_tree_botoes,  # Define o quadro onde o botão será inserido.
                   text="Remover Item",  # Texto exibido no botão.
                   command=self.remover_item  # Método chamado ao clicar no botão.
                   ).pack(side='left',  # Posiciona o botão à esquerda ao lado do botão anterior.
                          padx=5)  # Adiciona 5 pixels de espaçamento horizontal entre os botões.

        # Totais
        # Cria um quadro para exibir os totais financeiros relacionados à reserva.
        # Este quadro será posicionado no topo da seção direita.
        quadro_totais = ttk.Frame(quadro_direita)  # Define o contêiner onde o quadro será inserido.

        # Posiciona o quadro dos totais no topo da seção direita.
        # `side='top'` posiciona o quadro na parte superior.
        # `fill='x'` faz com que o quadro preencha horizontalmente a seção direita.
        # `pady=10` adiciona 10 pixels de espaçamento vertical ao redor do quadro.
        quadro_totais.pack(side='top',  # Posiciona o quadro no topo.
                           fill='x',  # Preenche horizontalmente o espaço disponível.
                           pady=10)  # Adiciona espaçamento vertical ao redor do quadro.

        # Cria um rótulo para exibir o texto "Valor Produtos (R$):".
        # Este rótulo será usado para indicar o campo relacionado ao valor dos produtos.
        ttk.Label(quadro_totais,  # Define o quadro onde o rótulo será inserido.
                  text="Valor Produtos (R$):"  # Define o texto exibido no rótulo.
                  ).grid(row=0,  # Define a linha onde o rótulo será inserido no quadro.
                         column=0,  # Define a coluna onde o rótulo será inserido no quadro.
                         sticky='e',  # Alinha o texto do rótulo à direita.
                         padx=5,  # Adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
                         pady=5)  # Adiciona 5 pixels de espaçamento vertical ao redor do rótulo.

        # Cria uma variável para armazenar o valor total dos produtos.
        # A variável inicializa com o valor "0.00".
        self.var_valor_produtos = tk.StringVar(value="0.00")  # Valor inicial da variável.

        # Cria um rótulo para exibir o valor total dos produtos, vinculado à variável.
        # O texto exibido no rótulo será atualizado automaticamente quando o valor da variável mudar.
        ttk.Label(quadro_totais,  # Define o quadro onde o rótulo será inserido.
                  textvariable=self.var_valor_produtos  # Vincula o texto do rótulo à variável.
                  ).grid(row=0,  # Define a linha onde o rótulo será inserido no quadro.
                         column=1,  # Define a coluna onde o rótulo será inserido no quadro.
                         sticky='w',  # Alinha o texto do rótulo à esquerda.
                         padx=5,  # Adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
                         pady=5)  # Adiciona 5 pixels de espaçamento vertical ao redor do rótulo.

        # Cria um rótulo para indicar o total geral (valor final da reserva incluindo produtos e serviços).
        ttk.Label(quadro_totais,  # Define o quadro onde o rótulo será inserido.
                  text="Total (R$):"  # Texto fixo exibido no rótulo.
                  ).grid(row=1,  # Define a linha onde o rótulo será posicionado no quadro.
                         column=0,  # Define a coluna onde o rótulo será posicionado no quadro.
                         sticky='e',  # Alinha o texto à direita da célula.
                         padx=5,  # Adiciona 5 pixels de espaçamento horizontal entre o rótulo e outros elementos.
                         pady=5)  # Adiciona 5 pixels de espaçamento vertical entre o rótulo e outros elementos.

        # Cria uma variável para armazenar o valor total da reserva (inicialmente "0.00").
        # Define o valor inicial como zero formatado com duas casas decimais.
        self.var_total = tk.StringVar(value="0.00")

        # Cria um rótulo para exibir o valor total da reserva.
        ttk.Label(quadro_totais,  # Define o quadro onde o rótulo será inserido.
                  textvariable=self.var_total,  # Vincula o texto exibido à variável `self.var_total`.
                  font=("Arial", 12, "bold")  # Define a fonte como Arial, tamanho 12, em negrito.
                  ).grid(row=1,  # Define a linha onde o rótulo será posicionado no quadro.
                         column=1,  # Define a coluna onde o rótulo será posicionado no quadro.
                         sticky='w',  # Alinha o texto à esquerda da célula.
                         padx=5,  # Adiciona 5 pixels de espaçamento horizontal entre o rótulo e outros elementos.
                         pady=5)  # Adiciona 5 pixels de espaçamento vertical entre o rótulo e outros elementos.

        # Cria um botão para finalizar a reserva.
        ttk.Button(quadro_direita,  # Define o quadro onde o botão será inserido.
                   text="Finalizar Reserva",  # Texto exibido no botão.
                   command=self.finalizar_reserva  # Associa o clique no botão ao método `self.finalizar_reserva`.
                   ).pack(side='bottom',  # Posiciona o botão na parte inferior do quadro.
                          pady=20)  # Adiciona 20 pixels de espaçamento vertical acima e abaixo do botão.


    def atualizar_total(self):

        # Tenta converter o valor da variável `var_valor_hora`
        #       para um número decimal (float).
        try:

            # Obtém o valor por hora informado pelo usuário.
            valor_hora = float(self.var_valor_hora.get())

        except:

            # Caso ocorra um erro na conversão (ex.: campo vazio ou
            #       valor inválido), define como 0.0.
            valor_hora = 0.0

        # Inicializa a soma dos custos dos itens consumidos em 0.0.
        soma_itens = 0.0

        # Itera por todas as linhas (itens) da árvore `tree_itens`.
        for iid in self.tree_itens.get_children():

            # Obtém os valores associados ao item atual da árvore.
            valores = self.tree_itens.item(iid, "values")

            # Os valores são armazenados na seguinte ordem:
            # (nome_produto, quantidade, preço_unitário, custo_unitário, id_produto).

            # Converte a quantidade (coluna 1) para float.
            qtd = float(valores[1])

            # Converte o preço unitário (coluna 2) para float.
            preco = float(valores[2])

            # Adiciona o custo total do item (quantidade * preço
            #       unitário) à soma total de itens.
            soma_itens += qtd * preco


        # Atualiza o valor total dos produtos consumidos.
        # Converte a soma total dos itens consumidos para string
        #       formatada com duas casas decimais.
        self.var_valor_produtos.set(f"{soma_itens:.2f}")

        # Calcula o total geral da reserva.
        # Soma o valor da reserva por hora (`valor_hora`) com o custo
        #       total dos produtos consumidos (`soma_itens`).
        total_geral = valor_hora + soma_itens

        # Atualiza o valor total geral na interface.
        # Converte o total geral para string formatada com duas casas decimais.
        self.var_total.set(f"{total_geral:.2f}")


    def carregar_clientes(self):

        # Obtém todos os clientes da coleção `colecao_clientes` no banco de dados.
        clientes = self.reserva.colecao_clientes.find()

        # Itera sobre cada cliente encontrado na coleção.
        for cliente in clientes:

            # Obtém o nome do cliente. Se o campo "nome" não existir,
            #       usa "SemNome" como valor padrão.
            nome_cli = cliente.get("nome", "SemNome")

            # Armazena o ID do cliente no mapa de clientes, convertendo o ID para string.
            self.mapa_clientes[nome_cli] = str(cliente["_id"])

        # Define os valores do combobox de clientes como as chaves do
        #       mapa de clientes (nomes).
        self.combo_cliente["values"] = list(self.mapa_clientes.keys())

        # Se o combobox tiver valores disponíveis, seleciona o
        #       primeiro cliente por padrão.
        if self.combo_cliente["values"]:

            # Seleciona a primeira opção do combobox.
            self.combo_cliente.current(0)


    def adicionar_item(self):

        # Abre a janela de adição de item.
        # Passa a instância atual da janela principal, a instância do sistema de reservas,
        #       o widget Treeview que contém os itens consumidos e a própria janela principal.
        JanelaAdicionarItemReserva(self.janela,  # Referência para a janela principal.
                                   self.reserva,  # Referência para o sistema de reservas.
                                   self.tree_itens,  # Referência ao Treeview onde os itens serão exibidos.
                                   self)  # Referência à própria instância da janela.


    def remover_item(self):

        # Obtém a seleção atual no Treeview.
        selecao = self.tree_itens.selection()

        # Verifica se algum item foi selecionado.
        if not selecao:

            # Exibe uma mensagem de aviso caso nenhum item tenha sido selecionado.
            messagebox.showwarning(

                "Aviso",  # Título da janela de aviso.
                "Selecione um item para remover."  # Mensagem exibida no aviso.

            )

            # Encerra o método, pois não há item para remover.
            return

        # Remove o item selecionado do Treeview.
        self.tree_itens.delete(selecao[0])

        # Atualiza o valor total exibido após a remoção do item.
        self.atualizar_total()


    # ---------------------------------------------

    def finalizar_reserva(self):

        # Obtém o nome do cliente selecionado no combobox e
        #       remove espaços desnecessários.
        nome_cliente = self.combo_cliente.get().strip()

        # Verifica se o cliente selecionado está no mapa de clientes.
        # Se o cliente não estiver no mapa, exibe uma mensagem de aviso.
        if nome_cliente not in self.mapa_clientes:
            messagebox.showwarning("Aviso", "Selecione um cliente da lista.")
            return

        # Obtém o ID do cliente correspondente ao nome selecionado no mapa de clientes.
        cliente_id = self.mapa_clientes[nome_cliente]

        # Obtém o nome do lugar selecionado no combobox de lugares.
        # O método `.get()` recupera o valor selecionado, enquanto `.strip()`
        #       remove espaços em branco extras.
        nome_lugar = self.combo_lugar.get().strip()

        # Verifica se o nome do lugar selecionado está presente no mapa de lugares.
        # Caso o lugar não esteja no mapa, exibe uma mensagem de
        #       aviso ao usuário e interrompe a execução.
        if nome_lugar not in self.mapa_lugares:
            messagebox.showwarning("Aviso", "Selecione um lugar da lista.")
            return

        # Obtém o ID do lugar correspondente ao nome selecionado
        #       usando o dicionário `mapa_lugares`.
        lugar_id = self.mapa_lugares[nome_lugar]

        # Recupera o valor inserido no campo de hora inicial e remove
        #       quaisquer espaços em branco extras.
        hi = self.var_hora_inicial.get().strip()

        # Recupera o valor inserido no campo de hora final e remove
        #       quaisquer espaços em branco extras.
        hf = self.var_hora_final.get().strip()

        # Obtém a data selecionada no calendário `cal_reserva`.
        # O método `.get_date()` retorna a data no formato especificado pelo calendário.
        data_res = self.cal_reserva.get_date()

        # Tenta converter o valor do campo `var_valor_hora` para um
        #       número decimal (float).
        # Caso o campo esteja vazio ou contenha um valor
        #       inválido, o `except` captura a exceção
        #       e atribui o valor padrão de 0.0 a `valor_hora`.
        try:

            valor_hora = float(self.var_valor_hora.get())

        except:

            # Define `valor_hora` como 0.0 em caso de erro na conversão.
            valor_hora = 0.0

        # Verifica se os campos obrigatórios (hora inicial, hora final e
        #       data da reserva) estão preenchidos.
        # Caso qualquer um deles esteja vazio, exibe uma mensagem de
        #       aviso e interrompe a execução.
        if not hi or not hf or not data_res:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        # Verifica se já existe uma reserva no mesmo lugar, data e horário fornecidos.
        # Chama o método `verificar_conflito` da classe de reserva, passando o `lugar_id`,
        # a data da reserva (`data_res`), a hora inicial (`hi`) e a hora final (`hf`).
        if self.reserva.verificar_conflito(lugar_id, data_res, hi, hf):

            # Se o método retornar `True`, significa que já existe uma
            #       reserva que entra em conflito.
            # Exibe uma mensagem de erro informando o conflito e
            #       interrompe a execução da função.
            messagebox.showerror("Conflito",
                                 "Já existe reserva neste horário/lugar.")
            return

        # Inicializa uma lista vazia para armazenar os itens consumidos durante a reserva.
        # Esses itens serão posteriormente adicionados ao registro da reserva.
        itens_consumidos = []

        # Itera sobre cada item presente na `tree_itens`, que
        #       representa os itens consumidos na reserva.
        for iid in self.tree_itens.get_children():

            # Obtém os valores associados ao item atual da `Treeview`.
            valores = self.tree_itens.item(iid, "values")

            # Extrai o nome do produto a partir do primeiro campo dos valores.
            nome_prod = valores[0]

            # Converte a quantidade consumida do produto (segundo campo)
            #       para um número decimal (float).
            qtd = float(valores[1])

            # Converte o preço unitário do produto (terceiro campo) para float.
            preco_unit = float(valores[2])

            # Converte o custo unitário do produto (quarto campo) para float.
            custo_unit = float(valores[3])

            # Obtém o ID do produto (quinto campo) como string.
            produto_id = valores[4]

            # Adiciona as informações do item como um dicionário na lista `itens_consumidos`.
            # Cada dicionário contém os dados relevantes sobre o item consumido:
            # - `nome`: Nome do produto consumido.
            # - `qtd`: Quantidade consumida.
            # - `preco_unit`: Preço unitário do produto.
            # - `custo_unit`: Custo unitário do produto.
            # - `produto_id`: Identificador único do produto.
            itens_consumidos.append({
                "nome": nome_prod,
                "qtd": qtd,
                "preco_unit": preco_unit,
                "custo_unit": custo_unit,
                "produto_id": produto_id
            })

        # Tenta abater o estoque para os itens consumidos na reserva.
        try:

            # Chama o método `abater_estoque_itens` da classe `reserva`,
            # passando a lista `itens_consumidos` que contém os produtos e suas quantidades.
            self.reserva.abater_estoque_itens(itens_consumidos)

        except ValueError as e:

            # Caso ocorra um erro de estoque insuficiente (levantado como `ValueError`),
            # exibe uma mensagem de erro em uma caixa de diálogo.
            # A mensagem detalha o motivo do erro, incluindo o nome do
            #       produto afetado e o estoque disponível.
            messagebox.showerror("Estoque insuficiente", str(e))

            # Encerra a execução do método para que o processo de reserva não continue.
            return

        # Insere a reserva no banco de dados.
        # O método `inserir_reserva` da classe `reserva` é chamado com
        #       os parâmetros necessários:
        # - `lugar_id`: O ID do lugar selecionado.
        # - `data_res`: A data da reserva, obtida do calendário.
        # - `hi` e `hf`: Hora inicial e final da reserva.
        # - `cliente_id`: O ID do cliente selecionado.
        # - `valor_hora`: O valor calculado para a reserva.
        # - `itens_consumidos`: Lista contendo os itens consumidos na reserva.
        self.reserva.inserir_reserva(lugar_id, data_res, hi, hf, cliente_id, valor_hora, itens_consumidos)

        # Exibe uma mensagem de sucesso em uma caixa de diálogo, informando
        #       que a reserva foi cadastrada com sucesso.
        # A propriedade `parent=self.janela` garante que a mensagem
        #       seja exibida sobre a janela atual.
        messagebox.showinfo("Sucesso",
                            "Reserva cadastrada com sucesso!",
                            parent=self.janela)

        # Atualiza o mapa de horários na janela principal de
        #       reservas, refletindo a nova reserva.
        self.janela_reservas.atualizar_mapa()

        # Fecha a janela de cadastro de reserva após concluir a operação.
        self.janela.destroy()

    # ---------------------------------------


    def carregar_lugares(self):

        # Obtém todos os registros da coleção `colecao_lugares` no banco de dados.
        lugares = self.reserva.colecao_lugares.find()

        # Itera sobre cada registro de lugar encontrado.
        for lugar in lugares:

            # Obtém o nome do lugar armazenado no campo "nome".
            nome_lugar = lugar["nome"]

            # Armazena o ID do lugar no mapa de lugares, convertendo o ID para string.
            self.mapa_lugares[nome_lugar] = str(lugar["_id"])

        # Define os valores do combobox de lugares como as chaves do
        #       mapa de lugares (nomes).
        self.combo_lugar["values"] = list(self.mapa_lugares.keys())

        # Se o combobox tiver valores disponíveis, seleciona o
        #       primeiro lugar por padrão.
        if self.combo_lugar["values"]:

            # Seleciona a primeira opção do combobox.
            self.combo_lugar.current(0)



###############################################################################
#        JANELA PARA ADICIONAR ITEM DE RESERVA (COMBO DE PRODUTOS)           #
###############################################################################
class JanelaAdicionarItemReserva:

    # Inicializa a janela para adicionar itens à reserva.
    # Recebe os seguintes parâmetros:
    # - `parent`: Janela principal (pai) que chama esta janela.
    # - `reserva`: Objeto da classe `ReservaQuadra` com conexão e métodos de banco de dados.
    # - `tree_itens`: Referência ao TreeView onde os itens consumidos são exibidos.
    # - `tela_reserva`: Referência à tela de cadastro de reservas para interagir ou atualizar dados.
    def __init__(self, parent, reserva: ReservaQuadra, tree_itens, tela_reserva):

        # Salva a referência à janela pai para manipulação e
        #       exibição de mensagens ou widgets.
        self.parent = parent

        # Recebe o objeto `reserva` da classe `ReservaQuadra`, que
        #       contém os métodos e a conexão com o banco de dados.
        self.reserva = reserva

        # `tree_itens` é o TreeView da tela principal de reservas,
        #       onde os itens consumidos são exibidos.
        # A referência permite adicionar ou modificar itens diretamente.
        self.tree_itens = tree_itens

        # `tela_reserva` é uma referência à tela principal de cadastro de reservas.
        # Permite interagir com métodos ou atualizações de layout desta tela.
        self.tela_reserva = tela_reserva

        # Cria uma nova janela de nível superior para adicionar itens consumidos.
        # A janela é filha da janela principal (`parent`).
        self.janela = tk.Toplevel(parent)

        # Define o título da janela como "Adicionar Item Consumido".
        self.janela.title("Adicionar Item Consumido")

        # Define o tamanho fixo da janela em 400x200 pixels.
        largura = 400
        altura = 200

        # Calcula a largura da tela para centralizar horizontalmente.
        largura_tela = self.janela.winfo_screenwidth()

        # Calcula a altura da tela para centralizar verticalmente.
        altura_tela = self.janela.winfo_screenheight()

        # Calcula a posição horizontal para centralizar a janela.
        pos_x = (largura_tela // 2) - (largura // 2)

        # Calcula a posição vertical para centralizar a janela.
        pos_y = (altura_tela // 2) - (altura // 2)

        # Aplica as dimensões e a posição calculadas para centralizar a janela na tela.
        # `geometry` define o tamanho (largura x altura) e a posição (+x+y).
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Cria um quadro (`Frame`) dentro da nova janela para organizar os widgets.
        # Adiciona um espaçamento de 10 pixels ao redor do quadro.
        quadro = ttk.Frame(self.janela)
        quadro.pack(padx=10, pady=10)

        # Cria um rótulo para identificar o campo de seleção do produto.
        # O texto "Produto:" será exibido na posição especificada.
        # `row=0` e `column=0` colocam o rótulo na primeira linha e na primeira coluna do quadro.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical.
        # `sticky='e'` alinha o rótulo à direita dentro da célula da grade.
        ttk.Label(quadro, text="Produto:").grid(row=0, column=0, padx=5, pady=5, sticky='e')

        # Cria uma combobox (caixa de seleção) para listar os produtos disponíveis.
        # A combobox será configurada como somente leitura (`state="readonly"`),
        #       o que impede o usuário de digitar manualmente um produto.
        # `width=30` define a largura da combobox em caracteres.
        self.combo_produto = ttk.Combobox(quadro, state="readonly", width=30)

        # Posiciona a combobox de produtos na grade do quadro.
        # `row=0` e `column=1` colocam a combobox na primeira linha e na segunda coluna,
        #       ao lado do rótulo "Produto:".
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e vertical
        #       ao redor da combobox para melhor espaçamento visual.
        self.combo_produto.grid(row=0, column=1, padx=5, pady=5)

        # Cria um dicionário vazio para mapear os nomes dos produtos ao seus IDs.
        # Esse mapeamento será utilizado posteriormente para associar o produto selecionado
        #       ao seu identificador no banco de dados.
        self.mapa_produtos = {}

        # Chama o método `carregar_produtos`, que será responsável por preencher a combobox
        #       com os produtos disponíveis e atualizar o dicionário `mapa_produtos`.
        self.carregar_produtos()

        # Cria um rótulo com o texto "Quantidade:" para identificar o
        #       campo de entrada de quantidade.
        # O rótulo é posicionado na segunda linha (`row=1`) e na
        #       primeira coluna (`column=0`)
        #       dentro do `quadro`.
        # `padx=5` e `pady=5` adicionam espaçamento ao redor do rótulo,
        #       e `sticky='e'` alinha o rótulo à direita dentro de sua célula.
        ttk.Label(quadro,
                  text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky='e')

        # Cria uma variável de controle do tipo `StringVar` para armazenar a quantidade
        #       inserida pelo usuário no campo de entrada.
        # Essa variável será vinculada ao campo de entrada para capturar e manipular
        #       o valor digitado de forma dinâmica.
        self.var_qtd = tk.StringVar()

        # Cria um campo de entrada (`Entry`) para que o usuário insira a quantidade do produto.
        # O campo de entrada é vinculado à variável `self.var_qtd` para capturar o valor digitado.
        # Define a largura do campo como 10 caracteres (`width=10`).
        ttk.Entry(quadro,  # Define o contêiner onde o campo será inserido.
                textvariable=self.var_qtd,  # Vincula o valor do campo à variável `self.var_qtd`.
                width=10  # Define a largura do campo de entrada.
                ).grid(row=1,  # Posiciona o campo de entrada na segunda linha do quadro.
                        column=1,  # Posiciona o campo na segunda coluna da linha especificada.
                        padx=5,  # Adiciona 5 pixels de espaçamento horizontal ao redor do campo.
                        pady=5,  # Adiciona 5 pixels de espaçamento vertical ao redor do campo.
                        sticky='w')  # Alinha o campo de entrada à esquerda dentro de sua célula.


        # Cria um botão para adicionar o item à lista de itens consumidos.
        botao_adicionar = ttk.Button(quadro,  # Define o contêiner onde o botão será inserido.
                                    text="Adicionar",  # Define o texto exibido no botão como "Adicionar".
                                    command=self.confirmar)  # Define a ação a ser executada ao clicar no botão.

        # Posiciona o botão na grade do quadro.
        botao_adicionar.grid(row=2,  # Posiciona o botão na terceira linha do quadro.
                            column=1,  # Posiciona o botão na segunda coluna da linha especificada.
                            sticky='e',  # Alinha o botão à direita dentro de sua célula.
                            pady=10)  # Adiciona 10 pixels de espaçamento vertical abaixo do botão.



    def carregar_produtos(self):

        # Obtém todos os produtos cadastrados na coleção de
        #       produtos do banco de dados.
        produtos = self.reserva.colecao_produtos.find()

        # Inicializa uma lista para armazenar os nomes dos produtos.
        lista_nomes = []

        # Itera sobre cada produto retornado pelo banco de dados.
        for prod in produtos:
            nome_p = prod["nome"]  # Obtém o nome do produto.
            _id = str(prod["_id"])  # Converte o ID do produto para string.

            # Adiciona o nome do produto à lista de nomes.
            lista_nomes.append(nome_p)

            # Adiciona o mapeamento do nome do produto para
            #       seu ID na variável `mapa_produtos`.
            self.mapa_produtos[nome_p] = _id

        # Configura os valores da combobox com a lista de nomes dos produtos.
        self.combo_produto["values"] = lista_nomes

        # Se houver produtos disponíveis, seleciona o primeiro como padrão.
        if lista_nomes:

            # Define o índice atual da combobox para o primeiro item.
            self.combo_produto.current(0)


    def confirmar(self):

        # Obtém o nome do produto selecionado na combobox e
        #       remove espaços em branco das extremidades.
        nome_prod = self.combo_produto.get().strip()

        # Verifica se o nome do produto existe no mapa de produtos carregados.
        if nome_prod not in self.mapa_produtos:

            # Se o produto não estiver no mapa, exibe um alerta para o usuário.
            messagebox.showwarning("Aviso",
                                   "Selecione corretamente o produto.")

            # Encerra o método sem continuar o processamento.
            return

        # Obtém o ID do produto correspondente ao nome selecionado.
        prod_id = self.mapa_produtos[nome_prod]

        # Obtém o valor digitado no campo de quantidade e remove
        #       espaços em branco das extremidades.
        qtd_str = self.var_qtd.get().strip()

        try:

            # Tenta converter o valor da quantidade para um número de ponto flutuante.
            qtd_i = float(qtd_str)

        except ValueError:

            # Se ocorrer um erro de conversão, exibe uma mensagem de
            #       aviso informando que a quantidade é inválida.
            messagebox.showwarning("Aviso", "Quantidade inválida.")

            # Encerra o método sem continuar o processamento.
            return

        # Verifica se a quantidade é menor ou igual a zero.
        if qtd_i <= 0:

            # Se a quantidade for inválida, exibe um aviso indicando
            #       que ela deve ser maior que zero.
            messagebox.showwarning("Aviso", "Quantidade deve ser > 0.")

            # Encerra o método sem continuar o processamento.
            return

        # Busca o produto no banco de dados pelo seu ID (prod_id).
        produto_bd = self.reserva.colecao_produtos.find_one({"_id": ObjectId(prod_id)})

        # Verifica se o produto foi encontrado no banco de dados.
        if not produto_bd:

            # Se não foi encontrado, exibe uma mensagem de erro
            #       informando que o produto não está no banco.
            messagebox.showerror("Erro",
                                 "Produto não encontrado no banco.")

            # Encerra o método sem continuar o processamento.
            return

        # Obtém o preço de venda do produto a partir do banco de dados.
        # Se o preço de venda não estiver definido, assume 0.0 como valor padrão.
        preco_unit = produto_bd.get("preco_venda", 0.0)

        # Obtém o preço de custo do produto a partir do banco de dados.
        # Se o preço de custo não estiver definido, assume 0.0 como valor padrão.
        custo_unit = produto_bd.get("preco_custo", 0.0)

        # Insere um novo item na Treeview (tabela de itens consumidos).
        # O item é inserido no final ("end") sem um identificador pai ("").
        # Os valores exibidos na tabela são:
        # - `nome_prod`: Nome do produto selecionado no combobox.
        # - `qtd_i`: Quantidade do produto especificada pelo usuário.
        # - `f"{preco_unit:.2f}"`: Preço unitário do produto formatado com duas casas decimais.
        # - `f"{custo_unit:.2f}"`: Custo unitário do produto formatado com duas casas decimais.
        # - `prod_id`: Identificador único do produto no banco de dados.
        self.tree_itens.insert("",
                                "end",
                                values=(nome_prod,
                                        qtd_i,
                                        f"{preco_unit:.2f}",
                                        f"{custo_unit:.2f}",
                                        prod_id))

        # Fecha a janela de adicionar item consumido após concluir a operação.
        self.janela.destroy()

        # Chama o método `atualizar_total` da tela de reserva para recalcular
        # os valores totais com base no novo item adicionado.
        self.tela_reserva.atualizar_total()



###############################################################################
#                    JANELA DE PESQUISA/HISTÓRICO DE RESERVAS                 #
###############################################################################
class JanelaPesquisaReservas:

    """
    Classe que cria e gerencia a interface gráfica para
            pesquisar e visualizar reservas.
    """

    def __init__(self, parent, reserva: ReservaQuadra, janela_reservas):

        """
        Método construtor que inicializa a janela de pesquisa de reservas.

        Args:
            parent: A janela pai (geralmente a janela principal) que serve como base
                    para esta nova janela.
            reserva (ReservaQuadra): Instância da classe `ReservaQuadra`, usada para
                                     acessar métodos de manipulação de dados no banco
                                     de reservas.
            janela_reservas: Referência para a janela principal de reservas, permitindo
                             sincronizar ações e atualizações entre as janelas.
        """

        # Define a janela pai da interface atual.
        # Isso é importante para posicionar e hierarquizar esta
        #       janela em relação à janela principal.
        self.parent = parent

        # Recebe a instância de `ReservaQuadra`, que contém métodos e atributos necessários
        #       para acessar e manipular os dados de reservas no banco de dados MongoDB.
        self.reserva = reserva

        # Define uma referência à janela principal de reservas.
        # Isso permite que as ações realizadas nesta janela de pesquisa (como excluir ou
        #       atualizar reservas) sejam refletidas diretamente na janela principal.
        self.janela_reservas = janela_reservas

        # Cria uma nova janela (Toplevel) que será exibida acima
        #       da janela principal (parent).
        self.janela = tk.Toplevel(parent)

        # Define o título da nova janela para "Histórico de Reservas".
        self.janela.title("Histórico de Reservas")

        # Configura a nova janela para abrir em tela cheia ou maximizada.
        # "zoomed" funciona no Windows; em outros sistemas operacionais,
        #       pode ser necessário ajustar.
        self.janela.state("zoomed")

        # Cria um quadro (Frame) na parte superior da janela, para
        #       agrupar elementos como rótulos e botões.
        quadro_topo = ttk.Frame(self.janela)

        # Posiciona o quadro no topo da janela, preenchendo
        #       horizontalmente (`fill='x'`) e adicionando
        #       5 pixels de espaçamento vertical (`pady=5`).
        quadro_topo.pack(side='top', fill='x', pady=5)

        # Cria um botão dentro do quadro superior (`quadro_topo`)
        #       que permite voltar para a janela anterior.
        # `text="Voltar"` define o texto exibido no botão como "Voltar".
        # `command=self.janela.destroy` associa a ação de fechar a janela atual ao clicar no botão.
        # `side='left'` posiciona o botão no lado esquerdo do quadro.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do botão.
        ttk.Button(quadro_topo,
                   text="Voltar",
                   command=self.janela.destroy).pack(side='left', padx=5)

        # Cria um rótulo dentro do quadro superior (`quadro_topo`)
        #       para exibir o texto "Nome Cliente:".
        # `text="Nome Cliente:"` define o texto exibido no rótulo.
        # `side='left'` posiciona o rótulo no lado esquerdo do quadro.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(quadro_topo, text="Nome Cliente:").pack(side='left', padx=5)

        # Cria uma variável de controle (`StringVar`) para
        #       armazenar o nome do cliente digitado.
        # A variável será usada para vincular o texto digitado no campo de entrada.
        self.var_nome_cliente = tk.StringVar()

        # Cria um campo de entrada de texto (Entry) dentro do quadro superior (`quadro_topo`).
        # `textvariable=self.var_nome_cliente` vincula o texto digitado à variável `self.var_nome_cliente`.
        # `width=15` define a largura do campo de entrada para 15 caracteres.
        # `side='left'` posiciona o campo de entrada no lado esquerdo do quadro, ao lado do rótulo.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        ttk.Entry(quadro_topo,
                  textvariable=self.var_nome_cliente,
                  width=15).pack(side='left', padx=5)

        # Cria um rótulo dentro do quadro superior (`quadro_topo`)
        #       para exibir o texto "Data (dd/mm/aaaa):".
        # `text="Data (dd/mm/aaaa):"` define o texto exibido no rótulo.
        # `side='left'` posiciona o rótulo no lado esquerdo do quadro.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do rótulo.
        ttk.Label(quadro_topo,
                  text="Data (dd/mm/aaaa):").pack(side='left', padx=5)

        # Cria uma variável de controle (`StringVar`) para armazenar a
        #       data digitada no formato dd/mm/aaaa.
        # A variável será usada para vincular o texto digitado no campo de entrada.
        self.var_data = tk.StringVar()

        # Cria um campo de entrada de texto (Entry) dentro do quadro
        #       superior (`quadro_topo`) para inserir a data.
        # `textvariable=self.var_data` vincula o texto digitado à variável `self.var_data`.
        # `width=10` define a largura do campo de entrada para 10 caracteres,
        #       suficiente para o formato dd/mm/aaaa.
        # `side='left'` posiciona o campo de entrada no lado esquerdo do quadro, ao lado do rótulo.
        # `padx=5` adiciona 5 pixels de espaçamento horizontal ao redor do campo de entrada.
        ttk.Entry(quadro_topo, textvariable=self.var_data, width=10).pack(side='left', padx=5)

        # Cria um botão para aplicar o filtro nas reservas.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a função `self.filtrar`
        #       para ser executada ao clicar no botão.
        # `pack(side='left', padx=5)` posiciona o botão no lado esquerdo do `quadro_topo`
        #       com um espaçamento horizontal de 5 pixels em ambos os lados.
        ttk.Button(quadro_topo, text="Filtrar", command=self.filtrar).pack(side='left', padx=5)

        # Cria um botão dentro do quadro superior (`quadro_topo`) com a
        #       funcionalidade de cancelar a reserva selecionada.
        # `text="Cancelar Reserva Selecionada"` define o texto exibido no botão.
        # `command=self.cancelar_reserva` associa a ação de chamar o
        #       método `self.cancelar_reserva` ao clicar no botão.
        # `pack(side='left', padx=5)` posiciona o botão no lado esquerdo do
        #       quadro e adiciona 5 pixels de espaçamento horizontal.
        ttk.Button(quadro_topo,
                    text="Cancelar Reserva Selecionada",
                    command=self.cancelar_reserva).pack(side='left', padx=5)


        # Cria uma Treeview para exibir os dados das reservas em formato de tabela.
        # `self.janela` é o contêiner onde a Treeview será inserida.
        # `columns` define as colunas que a Treeview terá, especificando
        #       seus identificadores.
        # `show='headings'` indica que somente os cabeçalhos das colunas
        #       serão exibidos (sem a coluna inicial padrão da Treeview).
        self.tree = ttk.Treeview(self.janela,
                                columns=("Lugar", "Data", "HoraIni", "HoraFim", "Cliente", "Total", "Itens"),
                                show='headings')

        # Define o cabeçalho da coluna "Lugar".
        # `text="Lugar"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("Lugar", text="Lugar")

        # Define o cabeçalho da coluna "Data".
        # `text="Data"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("Data", text="Data")

        # Define o cabeçalho da coluna "Hora Início".
        # `text="Hora Início"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("HoraIni", text="Hora Início")

        # Define o cabeçalho da coluna "Hora Final".
        # `text="Hora Final"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("HoraFim", text="Hora Final")

        # Define o cabeçalho da coluna "Cliente".
        # `text="Cliente"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("Cliente", text="Cliente")

        # Define o cabeçalho da coluna "Total R$".
        # `text="Total R$"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("Total", text="Total R$")

        # Define o cabeçalho da coluna "Produtos Consumidos".
        # `text="Produtos Consumidos"` especifica o texto exibido no cabeçalho da coluna.
        self.tree.heading("Itens", text="Produtos Consumidos")

        # Define a largura da coluna "Lugar" como 150 pixels para acomodar o nome do lugar.
        self.tree.column("Lugar", width=150)

        # Define a largura da coluna "Data" como 100 pixels, suficiente
        #       para o formato "dd/mm/aaaa".
        self.tree.column("Data", width=100)

        # Define a largura da coluna "HoraIni" como 100 pixels para
        #       exibir o horário de início.
        self.tree.column("HoraIni", width=100)

        # Define a largura da coluna "HoraFim" como 100 pixels para exibir o horário final.
        self.tree.column("HoraFim", width=100)

        # Define a largura da coluna "Cliente" como 150 pixels para
        #       acomodar o nome do cliente.
        self.tree.column("Cliente", width=150)

        # Define a largura da coluna "Total" como 80 pixels, suficiente
        #       para exibir valores monetários.
        self.tree.column("Total", width=80)

        # Define a largura da coluna "Itens" como 300 pixels para
        #       listar os produtos consumidos.
        self.tree.column("Itens", width=300)

        # Exibe a árvore (`Treeview`) na janela.
        # `fill='both'` faz com que a árvore preencha tanto a largura
        #       quanto a altura disponíveis.
        # `expand=True` permite que a árvore se expanda conforme o tamanho da janela.
        # `padx=10` e `pady=10` adicionam 10 pixels de espaçamento ao redor da árvore.
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Carrega todas as reservas inicialmente ao criar a janela.
        # Chama o método `buscar_reservas` da classe `ReservaQuadra`
        #       para buscar todas as reservas no banco.
        self.reservas = self.reserva.buscar_reservas()

        # Popula a árvore (`Treeview`) com os dados das reservas obtidas.
        self.preencher_tree(self.reservas)


    def preencher_tree(self, reservas):

        # Limpa todos os itens existentes na árvore antes de adicionar novos.
        # Itera sobre os identificadores (`item`) de todos os elementos da árvore.
        for item in self.tree.get_children():

            # Remove cada item encontrado na árvore.
            self.tree.delete(item)

        # Itera sobre a lista de reservas fornecida como argumento.
        for reserva in reservas:

            # Busca no banco de dados a informação do lugar associado à reserva.
            lugar_bd = self.reserva.colecao_lugares.find_one({"_id": reserva["lugar_id"]})

            # Obtém o nome do lugar a partir dos dados encontrados no banco.
            # Se `lugar_bd` for None (não encontrado), usa uma string vazia como padrão.
            lugar_nome = lugar_bd.get("nome", "") if lugar_bd else ""

            # Inicializa a variável `nome_cliente` como uma string vazia.
            nome_cliente = ""

            # Verifica se a reserva possui um campo `cliente_id`.
            if reserva.get("cliente_id"):

                # Realiza uma busca no banco de dados, na coleção de clientes,
                #       utilizando o `cliente_id` da reserva.
                cliente_bd = self.reserva.colecao_clientes.find_one({"_id": ObjectId(reserva["cliente_id"])})

                # Se um cliente correspondente for encontrado no banco de dados,
                # obtém o valor do campo `nome`. Caso contrário, mantém `nome_cliente`
                #       como uma string vazia.
                if cliente_bd:
                    nome_cliente = cliente_bd.get("nome", "")

            # Obtém a lista de itens consumidos da reserva. Se não houver itens,
            #       usa uma lista vazia como padrão.
            itens_consumidos = reserva.get("itens_consumidos", [])

            # Inicializa uma lista vazia para armazenar as descrições
            #       dos produtos consumidos.
            lista_produtos_str = []

            # Itera sobre cada item consumido presente na reserva.
            for item_consumido in itens_consumidos:

                # Obtém o nome do produto do item consumido. Caso não exista,
                #       define como uma string vazia.
                nome_prod = item_consumido.get("nome", "")

                # Obtém a quantidade consumida do item. Caso não exista, define como 0.
                qtd = item_consumido.get("qtd", 0)

                # Adiciona à lista uma string formatada com o nome do produto e a
                #       quantidade consumida no formato `Produto (xQtd)`.
                lista_produtos_str.append(f"{nome_prod} (x{qtd})")

            # Junta todas as descrições de produtos em uma única string, separadas por vírgulas.
            itens_str = ", ".join(lista_produtos_str)

            # Insere uma nova linha na Treeview para exibir as
            #       informações da reserva.
            self.tree.insert(

                "",  # Insere no nível superior (sem hierarquia de pai/filho).
                "end",  # Adiciona a nova linha no final da lista de itens.
                values=(lugar_nome,  # Nome do lugar relacionado à reserva.
                    reserva["data"],  # Data da reserva (formato dd/mm/aaaa).
                    reserva["hora_inicial"],  # Hora de início da reserva.
                    reserva["hora_final"],  # Hora de término da reserva.
                    nome_cliente,  # Nome do cliente que realizou a reserva.
                    f"{reserva['valor_total']:.2f}",  # Valor total da reserva, formatado com 2 casas decimais.
                    itens_str))  # Lista de itens consumidos, concatenados em uma única string.


    def filtrar(self):

        # Obtém o valor digitado no campo de filtro do cliente e o converte para minúsculas.
        nome_cli_filtro = self.var_nome_cliente.get().strip().lower()

        # Obtém o valor digitado no campo de filtro da data.
        data_filtro = self.var_data.get().strip()

        # Inicializa a lista que armazenará as reservas filtradas.
        filtradas = []

        # Percorre todas as reservas disponíveis para aplicar os filtros.
        for reserva in self.reservas:

            # Inicializa o nome do cliente como vazio.
            nome_cli = ""

            # Verifica se há um cliente associado à reserva (com `cliente_id`).
            if reserva.get("cliente_id"):

                # Busca o cliente na coleção de clientes pelo `cliente_id`.
                cliente_bd = self.reserva.colecao_clientes.find_one({"_id": ObjectId(reserva["cliente_id"])})

                # Se o cliente for encontrado, obtém o nome e o converte para minúsculas.
                if cliente_bd:
                    nome_cli = cliente_bd.get("nome", "").lower()

            # Verifica se o nome do cliente passa no filtro.
            # Se nenhum filtro de cliente foi fornecido (`not nome_cli_filtro`), considera válido.
            # Caso contrário, verifica se o nome do cliente na reserva contém o filtro fornecido.
            passa_nome = (not nome_cli_filtro) or (nome_cli_filtro in nome_cli)

            # Verifica se a data da reserva passa no filtro.
            # Se nenhum filtro de data foi fornecido (`not data_filtro`), considera válido.
            # Caso contrário, compara a data da reserva com o filtro fornecido.
            passa_data = (not data_filtro) or (reserva["data"] == data_filtro)

            # Se a reserva passa em ambos os filtros (nome e data),
            #       adiciona à lista de filtradas.
            if passa_nome and passa_data:
                filtradas.append(reserva)

        # Preenche a Treeview com as reservas que passaram no filtro.
        self.preencher_tree(filtradas)



    def cancelar_reserva(self):

        # Obtém as reservas selecionadas na Treeview.
        selecionados = self.tree.selection()

        # Verifica se nenhuma reserva foi selecionada.
        if not selecionados:

            # Exibe um aviso para o usuário indicando que é necessário selecionar uma reserva.
            messagebox.showwarning("Aviso",
                                   "Selecione uma reserva para cancelar.")

            # Interrompe a execução do método, pois não há reservas para cancelar.
            return

        # Obtém os dados da reserva selecionada na Treeview.
        item_tree = self.tree.item(selecionados[0])

        # Extrai os valores associados à reserva selecionada. Esses valores incluem:
        # (Lugar, Data, HoraIni, HoraFim, Cliente, Total, Itens)
        valores = item_tree["values"]

        # Extrai o nome do lugar da reserva a partir dos valores obtidos.
        lugar_nome = valores[0]

        # Extrai a data da reserva selecionada.
        data_res = valores[1]

        # Extrai a hora inicial da reserva selecionada.
        hora_inicial = valores[2]

        # Extrai a hora final da reserva selecionada.
        hora_final = valores[3]

        # Busca no banco de dados a informação completa do lugar associado ao nome.
        # Aqui, `self.reserva.colecao_lugares` representa a coleção de lugares no MongoDB.
        lugar_bd = self.reserva.colecao_lugares.find_one({"nome": lugar_nome})

        # Verifica se o lugar foi encontrado no banco de dados.
        # Caso contrário, exibe uma mensagem de erro e interrompe o
        #       processo de cancelamento.
        if not lugar_bd:
            messagebox.showerror("Erro",
                                 "Lugar não encontrado no banco.")
            return

        # Chama o método `cancelar_reserva` da classe `ReservaQuadra` para cancelar a reserva.
        # Passa os parâmetros necessários: ID do lugar, data da reserva, hora inicial e hora final.
        ok = self.reserva.cancelar_reserva(lugar_bd["_id"], data_res, hora_inicial, hora_final)

        # Verifica se a reserva foi cancelada com sucesso.
        if ok:

            # Exibe uma mensagem informando o sucesso do cancelamento.
            messagebox.showinfo("Sucesso", "Reserva cancelada.")

            # Atualiza a lista de reservas chamando o método `buscar_reservas`.
            self.reservas = self.reserva.buscar_reservas()

            # Aplica os filtros atuais na lista atualizada
            #       para refletir as mudanças.
            self.filtrar()

            # Atualiza o mapa de horários na janela principal de reservas.
            self.janela_reservas.atualizar_mapa()

        else:

            # Exibe um aviso caso o cancelamento da reserva não tenha sido realizado.
            messagebox.showwarning("Aviso",
                                   "Não foi possível cancelar a reserva.")


###############################################################################
#                     JANELA DE RELATÓRIO (FILTRAR E MOSTRAR)                 #
###############################################################################

class JanelaRelatorio:

    """
    Classe que representa a janela de relatórios, utilizada para exibir informações
    detalhadas sobre reservas e estatísticas relacionadas ao sistema.
    """

    def __init__(self, parent, reserva: ReservaQuadra):

        """
        Inicializa a janela de relatórios com os parâmetros necessários.

        Args:
            parent: Referência para a janela pai, necessária para exibir
                    esta janela no contexto correto.
            reserva (ReservaQuadra): Instância de ReservaQuadra que gerencia o
                    acesso ao banco de dados e fornece os métodos necessários.
        """

        # Atributo `self.parent` armazena a referência à janela pai.
        self.parent = parent

        # Atributo `self.reserva` guarda a instância de ReservaQuadra,
        #       permitindo consultas e operações no banco.
        self.reserva = reserva

        # Cria uma nova janela secundária (Toplevel) com a referência à janela pai.
        self.janela = tk.Toplevel(parent)

        # Define o título da janela como "Relatório de Reservas e Itens".
        self.janela.title("Relatório de Reservas e Itens")

        # Define o estado da janela como "zoomed" para que ela ocupe a tela inteira.
        self.janela.state("zoomed")

        # Cria um quadro (Frame) na parte superior da janela para
        #       acomodar os elementos do topo.
        quadro_topo = ttk.Frame(self.janela)

        # Posiciona o quadro na parte superior da janela,
        #       preenchendo horizontalmente (fill='x')
        #       e adicionando um espaçamento vertical (pady=5).
        quadro_topo.pack(side='top', fill='x', pady=5)

        # Primeira linha de filtros
        # Cria um novo frame (linha1) dentro do quadro superior (`quadro_topo`).
        # O frame será usado para organizar os elementos de entrada e rótulos na parte superior.
        # `side='top'` posiciona o frame no topo do `quadro_topo`.
        # `fill='x'` faz com que o frame preencha horizontalmente o espaço disponível.
        # `pady=2` adiciona 2 pixels de espaçamento vertical acima e abaixo do frame.
        linha1 = ttk.Frame(quadro_topo)
        linha1.pack(side='top', fill='x', pady=2)

        # Cria um rótulo (label) com o texto "Data Início:" para
        #       identificar o campo de data inicial.
        # `text="Data Início:"` define o texto exibido no rótulo.
        # `pack(side='left', padx=5)` posiciona o rótulo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Label(linha1, text="Data Início:").pack(side='left', padx=5)

        # Cria um campo de entrada de data (DateEntry) para o usuário selecionar a data inicial.
        # `date_pattern='dd/MM/yyyy'` define o formato da data como dia/mês/ano.
        # `width=12` define a largura do campo como 12 caracteres.
        # `pack(side='left', padx=5)` posiciona o campo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        self.dt_ini = DateEntry(linha1, date_pattern='dd/MM/yyyy', width=12)
        self.dt_ini.pack(side='left', padx=5)

        # Cria um rótulo (label) com o texto "Data Fim:" para identificar o campo de data final.
        # `text="Data Fim:"` define o texto exibido no rótulo.
        # `pack(side='left', padx=5)` posiciona o rótulo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Label(linha1, text="Data Fim:").pack(side='left', padx=5)

        # Cria um campo de entrada de data (DateEntry) para o usuário selecionar a data final.
        # `date_pattern='dd/MM/yyyy'` define o formato da data como dia/mês/ano.
        # `width=12` define a largura do campo como 12 caracteres.
        # `pack(side='left', padx=5)` posiciona o campo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        self.dt_fim = DateEntry(linha1, date_pattern='dd/MM/yyyy', width=12)
        self.dt_fim.pack(side='left', padx=5)

        # Cria um rótulo (label) com o texto "Cliente:" para identificar o
        #       campo de entrada de cliente.
        # `text="Cliente:"` define o texto exibido no rótulo.
        # `pack(side='left', padx=5)` posiciona o rótulo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Label(linha1, text="Cliente:").pack(side='left', padx=5)

        # Cria uma variável Tkinter (StringVar) para armazenar o
        #       texto digitado no campo de entrada.
        # `self.var_cliente` será vinculada ao campo de entrada para
        #       capturar o nome do cliente.
        self.var_cliente = tk.StringVar()

        # Cria um campo de entrada de texto (Entry) para o usuário digitar o nome do cliente.
        # `textvariable=self.var_cliente` vincula o campo de entrada à variável `self.var_cliente`.
        # `width=15` define a largura do campo como 15 caracteres.
        # `pack(side='left', padx=5)` posiciona o campo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Entry(linha1,
                  textvariable=self.var_cliente, width=15).pack(side='left', padx=5)

        # Cria um rótulo (label) com o texto "Fornecedor:" para
        #       identificar o campo de entrada de fornecedor.
        # `text="Fornecedor:"` define o texto exibido no rótulo.
        # `pack(side='left', padx=5)` posiciona o rótulo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Label(linha1, text="Fornecedor:").pack(side='left', padx=5)

        # Cria uma variável Tkinter (StringVar) para armazenar o texto
        #       digitado no campo de entrada de fornecedor.
        # `self.var_fornecedor` será vinculada ao campo de entrada
        #       para capturar o nome do fornecedor.
        self.var_fornecedor = tk.StringVar()

        # Cria um campo de entrada de texto (Entry) para o usuário digitar o nome do fornecedor.
        # `textvariable=self.var_fornecedor` vincula o campo de entrada à variável `self.var_fornecedor`.
        # `width=15` define a largura do campo como 15 caracteres.
        # `pack(side='left', padx=5)` posiciona o campo à esquerda no frame `linha1`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Entry(linha1,
                  textvariable=self.var_fornecedor,
                  width=15).pack(side='left', padx=5)

        # Segunda linha de filtros
        # Cria um frame chamado `linha2` dentro de `quadro_topo`.
        # Este frame será usado para organizar os widgets da segunda linha do topo.
        # `pack(side='top', fill='x', pady=2)` posiciona o frame no topo,
        #       faz com que ele ocupe toda a largura disponível (`fill='x'`) e
        #       adiciona 2 pixels de espaçamento vertical.
        linha2 = ttk.Frame(quadro_topo)
        linha2.pack(side='top', fill='x', pady=2)

        # Cria um rótulo (label) com o texto "Produto:" para
        #       identificar o campo de entrada do produto.
        # `text="Produto:"` define o texto exibido no rótulo.
        # `pack(side='left', padx=5)` posiciona o rótulo à esquerda no frame `linha2`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Label(linha2, text="Produto:").pack(side='left', padx=5)

        # Cria uma variável Tkinter (StringVar) para armazenar o texto
        #       digitado no campo de entrada do produto.
        # `self.var_produto` será vinculada ao campo de entrada
        #       para capturar o nome do produto.
        self.var_produto = tk.StringVar()

        # Cria um campo de entrada de texto (Entry) para o usuário digitar o nome do produto.
        # `textvariable=self.var_produto` vincula o campo de entrada à variável `self.var_produto`.
        # `width=15` define a largura do campo como 15 caracteres.
        # `pack(side='left', padx=5)` posiciona o campo à esquerda no frame `linha2`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Entry(linha2,
                  textvariable=self.var_produto,
                  width=15).pack(side='left', padx=5)

        # Cria um rótulo (label) com o texto "Lugar:" para
        #       identificar o campo de entrada do lugar.
        # `text="Lugar:"` define o texto exibido no rótulo.
        # `pack(side='left', padx=5)` posiciona o rótulo à esquerda no frame `linha2`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Label(linha2, text="Lugar:").pack(side='left', padx=5)

        # Cria uma variável Tkinter (StringVar) para armazenar o
        #       texto digitado no campo de entrada do lugar.
        # `self.var_lugar` será vinculada ao campo de entrada
        #       para capturar o nome do lugar.
        self.var_lugar = tk.StringVar()

        # Cria um campo de entrada de texto (Entry) para o usuário digitar o nome do lugar.
        # `textvariable=self.var_lugar` vincula o campo de entrada à variável `self.var_lugar`.
        # `width=15` define a largura do campo como 15 caracteres.
        # `pack(side='left', padx=5)` posiciona o campo à esquerda no frame `linha2`
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Entry(linha2,
                  textvariable=self.var_lugar,
                  width=15).pack(side='left', padx=5)

        # Cria um botão com o texto "Filtrar" para aplicar filtros nos dados exibidos.
        # `text="Filtrar"` define o texto exibido no botão.
        # `command=self.filtrar` associa a ação de filtrar os dados ao clicar no botão,
        #       chamando o método `self.filtrar`.
        # `pack(side='left', padx=5)` posiciona o botão à esquerda no frame `linha2`,
        #       com 5 pixels de espaçamento horizontal (padding) à direita.
        ttk.Button(linha2,
                   text="Filtrar",
                   command=self.filtrar).pack(side='left', padx=5)

        # Cria um botão com o texto "Exportar para Excel" para
        #       exportar os dados filtrados.
        # `text="Exportar para Excel"` define o texto exibido no botão.
        # `command=self.exportar_para_excel` associa a ação de
        #       exportar para Excel ao clicar no botão,
        #       chamando o método `self.exportar_para_excel`.
        # `pack(side='left', padx=10)` posiciona o botão à esquerda no frame `linha2`,
        #       com 10 pixels de espaçamento horizontal (padding) à direita para maior separação.
        ttk.Button(linha2,
                   text="Exportar para Excel",
                   command=self.exportar_para_excel).pack(side='left', padx=10)

        # Cria um widget Treeview para exibir os dados na forma de tabela.
        # `self.janela` é a janela onde o Treeview será inserido.
        # `columns=(...)` define as colunas exibidas na tabela.
        # `show='headings'` indica que somente os cabeçalhos das colunas serão exibidos,
        #       sem a coluna raiz (a coluna inicial oculta por padrão no Treeview).
        self.tree = ttk.Treeview(self.janela,
                                columns=("Data", "Lugar", "Cliente", "Fornecedor", "Produto", "Qtd",
                                    "CustoUn", "PrecoUn", "CustoTot", "PrecoTot", "Lucro"),
                                 show='headings')

        # Define os cabeçalhos que serão exibidos na tabela.
        # `cabecalhos` é uma lista de strings com os nomes das colunas.
        # Os nomes devem corresponder às colunas definidas no parâmetro `columns` acima.
        cabecalhos = [
            "Data", "Lugar", "Cliente", "Fornecedor", "Produto", "Qtd",
            "CustoUn", "PrecoUn", "CustoTot", "PrecoTot", "Lucro"
        ]

        # Configura cada coluna do Treeview com base na lista `cabecalhos`.
        # `for cab in cabecalhos:` inicia um loop que percorre cada item na lista `cabecalhos`.
        for cab in cabecalhos:

            # Define o texto do cabeçalho da coluna.
            # `self.tree.heading(cab, text=cab)` usa o nome da coluna (`cab`) para
            #       definir tanto o identificador da coluna quanto o texto visível no cabeçalho.
            self.tree.heading(cab, text=cab)

            # Configura a largura padrão de cada coluna.
            # `self.tree.column(cab, width=120)` define a largura de 120 pixels para cada coluna.
            # Isso é útil para garantir que os dados sejam exibidos corretamente e
            #       que a coluna não fique muito estreita.
            self.tree.column(cab, width=120)

        # Adiciona o widget Treeview à janela e configura como ele será exibido.
        # `fill='both'` faz com que o Treeview ocupe todo o espaço disponível
        #       tanto horizontalmente quanto verticalmente.
        # `expand=True` permite que o Treeview expanda quando a janela for redimensionada.
        # `padx=10` e `pady=10` adicionam 10 pixels de espaçamento ao redor do
        #       Treeview, deixando a interface mais espaçada e organizada.
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Rodapé com totais
        # Cria um quadro no rodapé para exibir informações resumidas.
        # `ttk.Frame(self.janela)` cria um contêiner dentro da janela principal.
        # `side='bottom'` posiciona o quadro na parte inferior da janela.
        # `fill='x'` faz com que o quadro preencha toda a largura disponível.
        # `padx=5` e `pady=5` adicionam 5 pixels de espaçamento horizontal e
        #       vertical ao redor do quadro.
        quadro_rodape = ttk.Frame(self.janela)
        quadro_rodape.pack(side='bottom', fill='x', padx=5, pady=5)

        # Cria um rótulo no quadro do rodapé para exibir a quantidade total de registros.
        # `text="Registros: 0"` define o texto inicial do rótulo como "Registros: 0".
        # Esse texto será atualizado conforme os dados forem filtrados.
        self.lbl_registros = ttk.Label(quadro_rodape, text="Registros: 0")

        # Posiciona o rótulo no lado esquerdo do quadro com 10
        #       pixels de espaçamento horizontal.
        self.lbl_registros.pack(side='left', padx=10)

        # Cria um rótulo para exibir o custo total das reservas.
        # `text="Custo Total: 0.00"` define o texto inicial do rótulo.
        self.lbl_custo = ttk.Label(quadro_rodape, text="Custo Total: 0.00")

        # Posiciona o rótulo no lado esquerdo do quadro com 10
        #       pixels de espaçamento horizontal.
        self.lbl_custo.pack(side='left', padx=10)

        # Cria um rótulo para exibir o valor total faturado.
        # `text="Faturado: 0.00"` define o texto inicial do rótulo.
        self.lbl_faturado = ttk.Label(quadro_rodape, text="Faturado: 0.00")

        # Posiciona o rótulo no lado esquerdo do quadro
        #       com 10 pixels de espaçamento horizontal.
        self.lbl_faturado.pack(side='left', padx=10)

        # Cria um rótulo para exibir o lucro total.
        # `text="Lucro: 0.00"` define o texto inicial do rótulo.
        self.lbl_lucro = ttk.Label(quadro_rodape, text="Lucro: 0.00")

        # Posiciona o rótulo no lado esquerdo do quadro
        #       com 10 pixels de espaçamento horizontal.
        self.lbl_lucro.pack(side='left', padx=10)

        # Chama o método `filtrar()` para carregar e exibir os
        #       dados iniciais no Treeview.
        # Isso garante que os valores iniciais dos rótulos no rodapé
        #       sejam preenchidos com base nos dados do banco.
        self.filtrar()


    # Define o método `filtrar` para aplicar filtros nos
    #       dados exibidos na tabela.
    # Ele utiliza os valores inseridos pelo usuário nos campos de
    #       data, cliente, fornecedor, produto e lugar.
    def filtrar(self):

        try:

            # Obtém a data inicial do widget `DateEntry` configurado para o filtro.
            # `self.dt_ini.get_date()` retorna a data selecionada no formato apropriado.
            data_ini = self.dt_ini.get_date()

            # Obtém a data final do widget `DateEntry` configurado para o filtro.
            # `self.dt_fim.get_date()` retorna a data selecionada no formato apropriado.
            data_fim = self.dt_fim.get_date()

            # Obtém o texto do campo de filtro de cliente.
            # `self.var_cliente.get()` retorna o valor atual da variável
            #       associada ao campo de texto.
            # `strip().lower()` remove espaços extras e converte o texto para
            #       letras minúsculas, facilitando a comparação.
            cliente_filtro = self.var_cliente.get().strip().lower()

            # Obtém o texto do campo de filtro de fornecedor.
            # Mesmo processo de limpeza e conversão é aplicado como no filtro de cliente.
            fornec_filtro = self.var_fornecedor.get().strip().lower()

            # Obtém o texto do campo de filtro de produto.
            # O processo é similar aos campos anteriores, para garantir uma comparação consistente.
            prod_filtro = self.var_produto.get().strip().lower()

            # Obtém o texto do campo de filtro de lugar.
            # Realiza a mesma limpeza de espaços e conversão para minúsculas.
            lugar_filtro = self.var_lugar.get().strip().lower()

            # Chama o método `buscar_reservas` para obter todas as
            #       reservas do banco de dados.
            # Esse método retorna uma lista de dicionários, onde cada
            #       dicionário representa uma reserva.
            reservas = self.reserva.buscar_reservas()

            # Cria uma lista vazia `linhas` para armazenar as reservas que
            #       atenderem aos filtros aplicados.
            linhas = []

            # Itera sobre cada reserva retornada pelo método `buscar_reservas`.
            for r in reservas:

                # Obtém a data da reserva no formato de string a partir do dicionário da reserva.
                # Utiliza `.get()` para evitar erros caso a chave "data" não esteja presente.
                data_res = r.get("data", "")

                # Converte a data obtida em um objeto `datetime.date`,
                #       usando o método `converter_data`.
                # Essa conversão facilita as comparações posteriores com
                #       as datas de início e fim.
                dt_res = self.converter_data(data_res)

                # Verifica se `dt_res` é um objeto `datetime` (que inclui data e hora).
                # Se for, converte para apenas a parte da data (`date`), descartando a hora.
                if isinstance(dt_res, datetime):
                    dt_res = dt_res.date()

                # Verifica se a data da reserva está fora do intervalo definido pelos filtros de data.
                # `dt_res < data_ini` significa que a reserva ocorre antes da data de início.
                # `dt_res > data_fim` significa que a reserva ocorre após a data de término.
                # Se qualquer uma dessas condições for verdadeira, a reserva é ignorada (`continue`).
                if dt_res and (dt_res < data_ini or dt_res > data_fim):
                    continue

                # Inicializa a variável `lugar_nome` como uma string vazia
                #       para armazenar o nome do lugar.
                lugar_nome = ""

                # Busca no banco de dados pelo lugar associado à reserva,
                #       usando o campo `lugar_id` da reserva.
                # `find_one` retorna o primeiro registro correspondente ao filtro especificado.
                lug = self.reserva.colecao_lugares.find_one({"_id": r["lugar_id"]})

                # Verifica se o lugar foi encontrado no banco de dados.
                if lug:

                    # Obtém o nome do lugar utilizando o método `get` para evitar
                    #       erros caso a chave "nome" esteja ausente.
                    lugar_nome = lug.get("nome", "")

                # Verifica se o filtro de lugar está ativo (`lugar_filtro`) e se o
                #       texto filtrado não está presente no nome do lugar.
                # O nome do lugar é convertido para letras minúsculas (`lower()`)
                #       para comparação case-insensitive.
                if lugar_filtro and lugar_filtro not in lugar_nome.lower():

                    # Se o lugar não corresponder ao filtro, ignora a reserva e
                    #       passa para a próxima iteração.
                    continue

                # Inicializa a variável `nome_cli` como uma string vazia para
                #       armazenar o nome do cliente associado à reserva.
                nome_cli = ""

                # Verifica se a reserva possui o campo `cliente_id`.
                if r.get("cliente_id"):

                    # Busca no banco de dados pelo cliente associado à reserva usando o `cliente_id`.
                    doc_cli = self.reserva.colecao_clientes.find_one({"_id": ObjectId(r["cliente_id"])})

                    # Verifica se o cliente foi encontrado no banco de dados.
                    if doc_cli:

                        # Obtém o nome do cliente usando o método `get`.
                        nome_cli = doc_cli.get("nome", "")

                # Verifica se o filtro de cliente está ativo (`cliente_filtro`) e
                #       se o texto filtrado não está presente no nome do cliente.
                # O nome do cliente é convertido para letras minúsculas (`lower()`)
                #       para comparação case-insensitive.
                if cliente_filtro and cliente_filtro not in nome_cli.lower():

                    # Se o cliente não corresponder ao filtro, ignora a
                    #       reserva e passa para a próxima iteração.
                    continue

                # Adiciona o valor da reserva como um produto fictício chamado "ReservaLugar".
                # Obtém o valor da reserva a partir do dicionário `r` com o
                #       método `get`, retornando 0.0 se a chave não existir.
                val_reserva = r.get("valor_reserva", 0.0)

                # Verifica se o valor da reserva é maior que 0.0 para
                #       considerar como produto.
                if val_reserva > 0.0:

                    # Verifica se não há filtro de produto (`prod_filtro`) ou se o
                    #       filtro de produto corresponde ao texto "ReservaLugar".
                    # Converte o texto "reservalugar" para minúsculas para comparação case-insensitive.
                    if not prod_filtro or "reservalugar".startswith(prod_filtro.lower()):

                        # Verifica se não há filtro de fornecedor (`fornec_filtro`),
                        #       pois a reserva de lugar não possui fornecedor associado.
                        if not fornec_filtro:

                            # Adiciona uma linha à lista `linhas` com os detalhes da reserva de lugar.
                            linhas.append({
                                "data": data_res,  # Data da reserva
                                "lugar": lugar_nome,  # Nome do lugar associado
                                "cliente": nome_cli,  # Nome do cliente associado
                                "produto": "ReservaLugar",  # Nome fictício do produto para a reserva
                                "fornecedor": "",  # Fornecedor é vazio para reservas de lugar
                                "qtd": 1.0,  # Quantidade é 1, pois a reserva é uma unidade
                                "custo_unit": 0.0,  # Custo unitário é 0 para reservas de lugar
                                "preco_unit": val_reserva  # Preço unitário é igual ao valor da reserva
                            })

                # Itera sobre a lista de itens consumidos na reserva, acessada
                #       pela chave "itens_consumidos".
                # Se a chave não existir ou estiver vazia, será retornada
                #       uma lista vazia como padrão.
                for item in r.get("itens_consumidos", []):

                    # Obtém o nome do produto consumido a partir do item,
                    #       retornando uma string vazia se não existir.
                    nome_produto = item.get("nome", "")

                    # Obtém a quantidade consumida do item. Se não especificado, retorna 0 como padrão.
                    qtd = item.get("qtd", 0)

                    # Obtém o custo unitário do item, retornando 0.0 como padrão se não especificado.
                    custo_u = item.get("custo_unit", 0.0)

                    # Obtém o preço unitário do item, retornando 0.0 como padrão se não especificado.
                    preco_u = item.get("preco_unit", 0.0)

                    # Obtém o identificador do produto consumido, retornando `None` se não especificado.
                    prod_id = item.get("produto_id")

                    # Inicializa o nome do fornecedor como uma string vazia,
                    #       caso não seja encontrado.
                    fornecedor_nome = ""

                    # Verifica se o ID do produto consumido está presente no item.
                    if prod_id:

                        # Busca o produto no banco de dados pelo seu identificador único (prod_id).
                        produto_bd = self.reserva.colecao_produtos.find_one({"_id": ObjectId(prod_id)})

                        # Se o produto foi encontrado e contém um fornecedor associado (fornecedor_id):
                        if produto_bd and produto_bd.get("fornecedor_id"):

                            # Busca o fornecedor associado ao produto no banco de dados.
                            fornec_bd = self.reserva.colecao_fornecedores.find_one(
                                {"_id": produto_bd["fornecedor_id"]})

                            # Se o fornecedor foi encontrado, armazena o nome do fornecedor.
                            if fornec_bd:
                                fornecedor_nome = fornec_bd.get("nome", "")

                    # Filtra os resultados com base no filtro de fornecedor.
                    # Verifica se o nome do fornecedor (em letras minúsculas)
                    #       contém o texto do filtro fornecido.
                    if fornec_filtro and fornec_filtro not in fornecedor_nome.lower():

                        # Se não corresponder, pula para o próximo item.
                        continue

                    # Filtra os resultados com base no filtro de produto.
                    # Verifica se o nome do produto (em letras minúsculas)
                    #       contém o texto do filtro fornecido.
                    if prod_filtro and prod_filtro not in nome_produto.lower():

                        # Se não corresponder, pula para o próximo item.
                        continue

                    # Adiciona uma linha à lista `linhas` para representar o item consumido.
                    linhas.append({

                        # A data da reserva é adicionada à linha como "data".
                        "data": data_res,

                        # O nome do lugar associado à reserva é adicionado como "lugar".
                        "lugar": lugar_nome,

                        # O nome do cliente associado à reserva é adicionado como "cliente".
                        "cliente": nome_cli,

                        # O nome do produto consumido é adicionado como "produto".
                        "produto": nome_produto,

                        # O nome do fornecedor do produto consumido é adicionado como "fornecedor".
                        "fornecedor": fornecedor_nome,

                        # A quantidade consumida do produto é adicionada como "qtd".
                        "qtd": qtd,

                        # O custo unitário do produto consumido é adicionado como "custo_unit".
                        "custo_unit": custo_u,

                        # O preço unitário do produto consumido é adicionado como "preco_unit".
                        "preco_unit": preco_u

                    })

            # Remove todos os itens existentes na TreeView antes de preenchê-la novamente.
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inicializa o contador de registros para mostrar o
            #       total de linhas adicionadas.
            total_registros = 0

            # Inicializa o acumulador de custo total, que somará os
            #       custos de todos os produtos/reservas.
            total_custo = 0.0

            # Inicializa o acumulador de preço total, que somará os
            #       preços de todos os produtos/reservas.
            total_preco = 0.0

            # Itera sobre cada linha filtrada para adicionar na TreeView.
            for ln in linhas:

                # Extrai os valores da linha atual, como data, lugar, cliente, etc.
                data_ = ln["data"]  # Data da reserva/consumo.
                lug_ = ln["lugar"]  # Nome do lugar relacionado à reserva.
                cli_ = ln["cliente"]  # Nome do cliente associado à reserva.
                forn_ = ln["fornecedor"]  # Nome do fornecedor do produto (se aplicável).
                prod_ = ln["produto"]  # Nome do produto consumido ou "ReservaLugar" se for uma reserva.
                qtd_ = ln["qtd"]  # Quantidade consumida do produto.
                cu_ = ln["custo_unit"]  # Custo unitário do produto consumido.
                pu_ = ln["preco_unit"]  # Preço unitário do produto consumido.

                # Calcula o custo total, multiplicando o custo unitário
                #       pela quantidade consumida.
                custo_tot = cu_ * qtd_

                # Calcula o preço total, multiplicando o preço unitário
                #       pela quantidade consumida.
                preco_tot = pu_ * qtd_

                # Calcula o lucro, subtraindo o custo total do preço total.
                lucro_ = preco_tot - custo_tot

                # Insere uma nova linha na TreeView para exibição.
                self.tree.insert(

                    "",  # Indica que será inserido na raiz, sem um pai específico.
                    "end",  # Adiciona ao final da lista de itens na TreeView.
                    values=(
                        data_,  # Data associada à reserva ou consumo.
                        lug_,  # Nome do lugar relacionado à reserva.
                        cli_,  # Nome do cliente associado à reserva.
                        forn_,  # Nome do fornecedor do produto (se aplicável).
                        prod_,  # Nome do produto consumido ou "ReservaLugar" para reservas.
                        f"{qtd_:.2f}",  # Quantidade consumida formatada com 2 casas decimais.
                        f"{cu_:.2f}",  # Custo unitário formatado com 2 casas decimais.
                        f"{pu_:.2f}",  # Preço unitário formatado com 2 casas decimais.
                        f"{custo_tot:.2f}",  # Custo total formatado com 2 casas decimais.
                        f"{preco_tot:.2f}",  # Preço total formatado com 2 casas decimais.
                        f"{lucro_:.2f}"  # Lucro formatado com 2 casas decimais.
                    )
                )

                # Incrementa o contador total de registros exibidos na TreeView.
                total_registros += 1

                # Soma o custo total calculado para obter o custo geral.
                total_custo += custo_tot

                # Soma o preço total calculado para obter o faturamento geral.
                total_preco += preco_tot

            # Atualiza o rótulo que exibe o número total de registros na TreeView.
            # `text=f"Registros: {total_registros}"` define o texto a ser
            #       exibido, incluindo a contagem de registros.
            self.lbl_registros.config(text=f"Registros: {total_registros}")

            # Atualiza o rótulo que exibe o custo total das reservas e itens consumidos.
            # `text=f"Custo Total: R$ {total_custo:.2f}"` define o texto com o
            #       custo total formatado com duas casas decimais.
            self.lbl_custo.config(text=f"Custo Total: R$ {total_custo:.2f}")

            # Atualiza o rótulo que exibe o valor faturado total das reservas e itens consumidos.
            # `text=f"Faturado: R$ {total_preco:.2f}"` define o texto com o
            #       faturamento total formatado com duas casas decimais.
            self.lbl_faturado.config(text=f"Faturado: R$ {total_preco:.2f}")

            # Atualiza o rótulo que exibe o lucro total calculado como
            #       diferença entre faturamento e custo.
            # `text=f"Lucro: R$ {(total_preco - total_custo):.2f}"` define o
            #       texto com o lucro formatado com duas casas decimais.
            self.lbl_lucro.config(text=f"Lucro: R$ {(total_preco - total_custo):.2f}")


        except Exception as e:

            # Captura e trata exceções que podem ocorrer durante a aplicação dos filtros.
            # `Exception as e` armazena detalhes do erro na variável `e` para exibição ao usuário.
            # Exibe uma mensagem de erro em um diálogo modal para informar o problema.
            # `messagebox.showerror` é usado para criar uma janela de erro com título "Erro".
            # `f"Erro ao aplicar filtros: {e}"` inclui detalhes da exceção na mensagem exibida.
            # `parent=self.janela` define a janela atual como pai para centralizar a mensagem.
            messagebox.showerror("Erro",
                                 f"Erro ao aplicar filtros: {e}",
                                 parent=self.janela)

    # Define o método para converter uma string de data em um objeto `datetime`.
    # `data_str` é a string no formato "dd/mm/yyyy" a ser convertida.
    def converter_data(self, data_str):

        # Tenta realizar a conversão utilizando o formato especificado.
        try:

            # `datetime.strptime` interpreta a string no
            #       formato "dd/mm/yyyy" e retorna um objeto `datetime`.
            return datetime.strptime(data_str, "%d/%m/%Y")

        # Captura qualquer exceção que ocorra durante a conversão (ex.: formato inválido).
        except:

            # Retorna `None` se a conversão falhar, indicando
            #       que a string de data é inválida.
            return None


    # Define o método `exportar_para_excel` para exportar os dados
    #       da TreeView para um arquivo Excel.
    def exportar_para_excel(self):

        # Obtém as colunas da TreeView.
        # `[self.tree.heading(col, 'text') for col in self.tree["columns"]]`
        #       percorre todas as colunas configuradas na TreeView
        #       e extrai o texto de cada cabeçalho, armazenando-o na lista `colunas`.
        colunas = [self.tree.heading(col, 'text') for col in self.tree["columns"]]

        # Cria uma lista vazia chamada `dados` para armazenar as
        #       linhas exibidas na TreeView.
        dados = []

        # Itera sobre todos os itens da TreeView.
        # `self.tree.get_children()` retorna os identificadores de
        #       todos os itens visíveis na TreeView.
        for item in self.tree.get_children():

            # Obtém os valores associados a cada linha usando `self.tree.item(item, "values")`.
            # Os valores de cada linha são adicionados à lista `dados`.
            dados.append(self.tree.item(item, "values"))

        # Converte os dados coletados da TreeView em um DataFrame do pandas.
        # `pd.DataFrame(dados, columns=colunas)` cria o DataFrame, onde `dados`
        #       são as linhas e `colunas` são os cabeçalhos.
        df = pd.DataFrame(dados, columns=colunas)

        # Abre uma caixa de diálogo para salvar o arquivo.
        # `asksaveasfilename` retorna o caminho escolhido pelo
        #       usuário para salvar o arquivo.
        # O parâmetro `defaultextension=".xlsx"` garante que o arquivo seja
        #       salvo com extensão `.xlsx` por padrão.
        # O parâmetro `filetypes` define que apenas arquivos do tipo Excel
        #       aparecerão na lista de tipos permitidos.
        caminho = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivo Excel", "*.xlsx")])

        # Verifica se o usuário selecionou um caminho (não cancelou a operação).
        if caminho:

            # Exporta o DataFrame para um arquivo Excel no caminho selecionado.
            # `index=False` garante que o índice do DataFrame não será salvo no arquivo.
            df.to_excel(caminho, index=False)

            # Exibe uma mensagem informando que a exportação foi concluída com sucesso.
            messagebox.showinfo("Exportação", "Dados exportados com sucesso!")



###############################################################################
#                     JANELA PRINCIPAL (MENU LATERAL)                         #
###############################################################################

"""
    Classe que define a janela principal da interface gráfica do usuário.
    Herda de `tk.Tk` para criar a janela principal da aplicação.
"""
class JanelaPrincipal(tk.Tk):

    """
        Inicializa a janela principal da aplicação e configura a interação
        com o objeto de gerenciamento de reservas.

        :param reserva: Instância da classe `ReservaQuadra`, que contém toda a
                        lógica para gerenciar reservas e acesso ao banco de dados.
    """
    def __init__(self, reserva):

        # Chama o método __init__ da classe pai (tk.Tk) para inicializar a janela Tkinter.
        # Isso é necessário porque estamos sobrescrevendo o método __init__ e precisamos
        # garantir que as configurações básicas da janela Tkinter sejam feitas corretamente.
        super().__init__()

        self.reserva = reserva

        # Configurações gerais da janela principal

        # Define o título da janela principal.
        # O título será exibido na barra superior da interface gráfica.
        self.title("Sistema Completo - Reservas e Estoque")

        # Configura a janela para ser exibida em tela cheia.
        # "zoomed" é utilizado principalmente no Windows para tela cheia.
        # Em sistemas operacionais diferentes, pode-se usar "fullscreen".
        self.state("zoomed")

        # Cria um objeto de estilo do `ttk` associado à janela.
        # Este objeto será usado para configurar o design dos
        #       componentes visuais (botões, rótulos, etc.).
        style = ttk.Style(self)

        # Configura o estilo padrão para os botões do tipo `TButton`.
        # Define a fonte dos botões como Arial, tamanho 14.
        # Adiciona 10 pixels de preenchimento interno ao redor do texto dos botões.
        style.configure("TButton", font=("Arial", 14), padding=10)

        # Configura o estilo padrão para os rótulos do tipo `TLabel`.
        # Define a fonte dos rótulos como Arial, tamanho 18, com estilo em negrito.
        style.configure("TLabel", font=("Arial", 18, "bold"))

        # Configura um estilo especial para rótulos do tipo `Title.TLabel`.
        # Define o estilo de fonte do rótulo.
        # `font=("Arial", 24, "bold")` define a fonte como Arial, tamanho 24, em negrito.
        # `foreground="#004d99"` define a cor do texto como azul escuro (#004d99).
        style.configure("Title.TLabel", font=("Arial", 24, "bold"), foreground="#004d99")

        # Configura o layout principal da janela.
        # `self.grid_columnconfigure(0, weight=1)` configura a coluna 0 da grade.
        # Define que ela será redimensionada proporcionalmente ao espaço disponível.
        self.grid_columnconfigure(0, weight=1)

        # `self.grid_rowconfigure(0, weight=1)` configura a linha 0 da grade.
        # Define que ela também será redimensionada proporcionalmente.
        self.grid_rowconfigure(0, weight=1)

        # Cria um quadro central para organizar os widgets.
        # `ttk.Frame(self)` cria um quadro dentro da janela principal.
        quadro_central = ttk.Frame(self)

        # Posiciona o quadro central na grade da janela principal.
        # `row=0` e `column=0` especificam a posição do quadro na grade.
        # `sticky="nsew"` faz com que o quadro preencha todo o espaço
        #       disponível (norte, sul, leste, oeste).
        # `padx=50` e `pady=50` adicionam 50 pixels de espaçamento
        #       horizontal e vertical ao redor do quadro.
        quadro_central.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        # Configura a coluna 0 do quadro central para se ajustar
        #       dinamicamente ao redimensionar.
        # `weight=1` significa que a coluna receberá uma proporção
        #       igual do espaço disponível.
        quadro_central.grid_columnconfigure(0, weight=1)

        # Configura a linha 0 do quadro central para se ajustar
        #       dinamicamente ao redimensionar.
        # `weight=1` significa que a linha também receberá uma
        #       proporção igual do espaço disponível.
        quadro_central.grid_rowconfigure(0, weight=1)


        # Cria um rótulo (label) para exibir o título do sistema.
        # `quadro_central` é o contêiner onde o rótulo será posicionado.
        # `text="Sistema Completo - Reservas e Estoque"` define o
        #       texto exibido no rótulo.
        # `style="Title.TLabel"` aplica o estilo configurado anteriormente
        #       para rótulos do tipo `Title.TLabel`.
        lbl_titulo = ttk.Label(
            quadro_central, text="Sistema Completo - Reservas e Estoque", style="Title.TLabel"
        )

        # Posiciona o rótulo na grade do quadro central.
        # `row=0` indica que o rótulo será colocado na primeira
        #       linha (índice 0) da grade.
        # `column=0` indica que o rótulo será colocado na primeira
        #       coluna (índice 0) da grade.
        # `pady=20` adiciona 20 pixels de espaçamento vertical acima e
        #       abaixo do rótulo, criando espaço.
        lbl_titulo.grid(row=0, column=0, pady=20)

        # Cria um quadro dentro do quadro central para organizar os
        #       botões de forma centralizada.
        # Esse quadro servirá como um contêiner para os botões.
        # `quadro_central` é o contêiner pai onde o quadro de
        #       botões será posicionado.
        quadro_botoes = ttk.Frame(quadro_central)

        # Posiciona o quadro de botões na grade do quadro central.
        # `row=1` indica que o quadro de botões será colocado na
        #       segunda linha (índice 1) da grade.
        # `column=0` indica que o quadro de botões será colocado na
        #       primeira coluna (índice 0) da grade.
        # `pady=20` adiciona 20 pixels de espaçamento vertical acima e
        #       abaixo do quadro de botões, criando espaço.
        quadro_botoes.grid(row=1, column=0, pady=20)

        # Define uma lista de botões para o menu principal.
        # Cada item na lista é uma tupla contendo:
        # - `texto`: o texto exibido no botão.
        # - `comando`: a função que será chamada ao clicar no botão.
        botoes_menu = [
            ("Lugares", self.abrir_janela_lugares),  # Botão para "Lugares".
            ("Fornecedores", self.abrir_janela_fornecedores),  # Botão para "Fornecedores".
            ("Produtos", self.abrir_janela_produtos),  # Botão para "Produtos".
            ("Clientes", self.abrir_janela_clientes),  # Botão para "Clientes".
            ("Reservas", self.abrir_janela_reservas),  # Botão para "Reservas".
            ("Relatório", self.abrir_janela_relatorio),  # Botão para "Relatório".
        ]

        # Organiza os botões do menu principal em uma única coluna.
        # Cada botão é adicionado em uma linha consecutiva, começando da linha 0.
        for i, (texto, comando) in enumerate(botoes_menu):

            # Cria um botão do tipo `ttk.Button`.
            # `text=texto` define o texto do botão.
            # `command=comando` associa o botão à função correspondente.
            # `width=30` define a largura fixa do botão em 30 caracteres.
            btn = ttk.Button(quadro_botoes, text=texto, command=comando, width=30)

            # Posiciona o botão na grade do quadro de botões.
            # `row=i` coloca o botão na linha `i` da grade, começando de 0.
            # `column=0` posiciona o botão na primeira coluna (índice 0) da grade.
            # `pady=10` adiciona 10 pixels de espaçamento vertical entre os botões.
            # `sticky="ew"` faz com que o botão se expanda horizontalmente
            #       para preencher a largura disponível.
            btn.grid(row=i, column=0, pady=10, sticky="ew")

        # Configura a coluna 0 do quadro de botões para expandir proporcionalmente.
        # `weight=1` permite que os botões se ajustem ao tamanho do
        #       quadro quando redimensionado.
        quadro_botoes.grid_columnconfigure(0, weight=1)

    # Define o método para abrir a janela de gerenciamento de lugares.
    def abrir_janela_lugares(self):

        # Instancia a classe `JanelaLugares` para gerenciar lugares.
        # `self` é passado como referência à janela principal.
        # `self.reserva` é o objeto de conexão com o banco de dados.
        JanelaLugares(self, self.reserva)

    # Define o método para abrir a janela de gerenciamento de fornecedores.
    def abrir_janela_fornecedores(self):

        # Instancia a classe `JanelaFornecedores` para gerenciar fornecedores.
        # `self` é a referência à janela principal.
        # `self.reserva` é o objeto de conexão com o banco de dados.
        JanelaFornecedores(self, self.reserva)

    # Define o método para abrir a janela de gerenciamento de produtos.
    def abrir_janela_produtos(self):

        # Instancia a classe `JanelaProdutos` para gerenciar produtos.
        # `self` é a referência à janela principal.
        # `self.reserva` é o objeto de conexão com o banco de dados.
        JanelaProdutos(self, self.reserva)

    # Define o método para abrir a janela de gerenciamento de clientes.
    def abrir_janela_clientes(self):

        # Instancia a classe `JanelaClientes` para gerenciar clientes.
        # `self` é a referência à janela principal.
        # `self.reserva` é o objeto de conexão com o banco de dados.
        JanelaClientes(self, self.reserva)

    # Define o método para abrir a janela de gerenciamento de reservas.
    def abrir_janela_reservas(self):

        # Instancia a classe `JanelaPrincipalReservas` para gerenciar reservas.
        # `self` é a referência à janela principal.
        # `self.reserva` é o objeto de conexão com o banco de dados.
        JanelaPrincipalReservas(self, self.reserva)

    # Define o método para abrir a janela de relatórios.
    def abrir_janela_relatorio(self):

        # Instancia a classe `JanelaRelatorio` para exibir relatórios do sistema.
        # `self` é a referência à janela principal.
        # `self.reserva` é o objeto de conexão com o banco de dados.
        JanelaRelatorio(self, self.reserva)


###############################################################################
#                            RODAR O SISTEMA                                  #
###############################################################################


# Cria uma instância da classe ReservaQuadra, que é responsável
#      por gerenciar as reservas.
reserva = ReservaQuadra()

# Cria a instância da classe JanelaPrincipal, passando a instância
#       de reserva como parâmetro.
# Isso inicializa a interface gráfica da aplicação, com a lógica
#       da reserva associada a ela.
app = JanelaPrincipal(reserva)

# Chama o método mainloop() da Tkinter para manter a janela aberta,
#       aguardando interações do usuário.
# Esse método entra no loop de eventos, onde ele escuta ações do usuário,
#       como cliques e teclas pressionadas.
app.mainloop()