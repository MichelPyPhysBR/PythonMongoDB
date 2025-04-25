# Importa o módulo tkinter e renomeia-o como tk para
# facilitar seu uso no código.
import tkinter as tk
from math import expm1

# Importa submódulos ttk e messagebox do tkinter, utilizados
# para criar widgets com estilos melhorados e exibir caixas de diálogo.
from tkinter import ttk, messagebox

# Importa o módulo Calendar do pacote tkcalendar, que permite
# criar um widget de calendário para seleção de datas.
from tkcalendar import Calendar

# Importa o módulo datetime da biblioteca datetime, usado
# para manipular datas e tempos.
from datetime import datetime

# Importa o módulo MongoClient do pacote pymongo, que
# permite conexão com um servidor MongoDB.
from pymongo import MongoClient


# Define a classe Onibus, responsável pela gestão das
# reservas de um ônibus.
class Onibus:

    # Método construtor da classe com parâmetro capacidade, que
    # define o número de lugares no ônibus.
    def __init__(self, capacidade):

        # Atributo que armazena a capacidade total de lugares no ônibus.
        self.capacidade = capacidade

        # Lista que representa os lugares no ônibus, inicializada
        # com 0 (desocupado) para cada lugar baseado na capacidade.
        self.lugares = [0] * capacidade

        # Cria um cliente MongoDB, conectando-se ao servidor MongoDB local padrão.
        self.cliente = MongoClient("mongodb://localhost:27017/")

        # Seleciona o banco de dados 'reserva_onibus_db' dentro do servidor MongoDB.
        self.bd = self.cliente["reserva_onibus_db"]

        # Seleciona a coleção 'reservas' dentro do banco de dados especificado.
        self.colecao_reservas = self.bd["reservas"]


    # Define o método 'carregar_reservas' que atualiza o status dos
    # lugares do ônibus com base nas reservas para uma data específica.
    def carregar_reservas(self, data):

        # Cria ou reinicializa a lista 'lugares' com zeros, indicando que
        # todos os lugares estão disponíveis inicialmente.
        # O uso de [0] * capacidade cria uma lista que contém o número zero
        # repetido tantas vezes quanto o valor de 'capacidade'.
        # Por exemplo, se capacidade é 20, isso resulta em [0, 0, 0, ..., 0] com 20 zeros.
        self.lugares = [0] * self.capacidade

        # Acessa a base de dados e utiliza o método 'find' para procurar todas as
        # entradas (reservas) onde a chave 'dia' corresponde
        # ao valor da variável 'data'. O resultado ('reservas') é um iterável que
        # permite percorrer cada documento que representa
        # uma reserva para esse dia.
        reservas = self.colecao_reservas.find({"dia": data})

        # Inicia um loop que irá percorrer cada documento encontrado na busca.
        for r in reservas:

            # Acessa o valor associado à chave 'lugar' dentro do
            # documento (representado por 'r') da reserva.
            # Este valor indica o número do lugar que foi reservado.
            num_lugar = r["lugar"]

            # Verifica se o número do lugar reservado está dentro do
            # intervalo permitido (de 1 até 'capacidade').
            # A verificação assegura que não tentaremos acessar
            # índices fora da lista 'lugares'.
            if 1 <= num_lugar <= self.capacidade:

                # Marca o lugar especificado como ocupado.
                # Ajusta o índice para base zero (listas em Python
                # começam em 0, não em 1), subtraindo 1 do número do lugar.
                # Por exemplo, lugar 1 na reserva corresponde ao
                # índice 0 na lista, lugar 2 ao índice 1, e assim por diante.
                self.lugares[num_lugar - 1] = 1


    # Define o método 'reservar_lugar' para reservar um lugar no ônibus,
    # recebendo como parâmetros o número do lugar, nome do cliente, CPF e a data da reserva.
    def reservar_lugar(self, num_lugar, nome, cpf, dia):

        # Verifica se o número do lugar é válido, ou seja, deve estar
        # dentro do intervalo de 1 até a capacidade máxima do ônibus.
        if num_lugar < 1 or num_lugar > self.capacidade:

            # Retorna uma mensagem indicando que o número do lugar é
            # inválido se estiver fora do intervalo.
            return "Lugar inválido"

        # Chama o método 'carregar_reservas' para atualizar o estado
        # atual dos lugares para a data especificada.
        self.carregar_reservas(dia)

        # Verifica se o lugar especificado está disponível (0 indica disponível).
        if self.lugares[num_lugar - 1] == 0:

            # Se disponível, marca o lugar como reservado (atribuindo 1).
            self.lugares[num_lugar - 1] = 1

            # Cria um dicionário contendo os detalhes da reserva.
            doc = {
                "lugar": num_lugar,  # Número do lugar.
                "nome": nome,  # Nome do cliente.
                "cpf": cpf,  # CPF do cliente.
                "dia": dia  # Data da reserva.
            }

            # Insere o documento da reserva na coleção de reservas
            # no banco de dados MongoDB.
            self.colecao_reservas.insert_one(doc)

            # Retorna uma mensagem de sucesso, indicando que o
            # lugar foi reservado com sucesso.
            return f"Lugar {num_lugar} reservado com sucesso."

        else:

            # Se o lugar já está ocupado, retorna uma mensagem
            # indicando que o lugar está indisponível.
            return f"Lugar {num_lugar} indisponível."


    # Define o método 'cancelar_reserva' para cancelar uma reserva de um
    # lugar específico em uma data específica.
    def cancelar_reserva(self, lugar, dia):

        # Primeiro, carrega todas as reservas para a data especificada para
        # atualizar o estado atual dos lugares.
        self.carregar_reservas(dia)

        # Verifica se o número do lugar está dentro da capacidade do ônibus e se o
        # lugar está atualmente reservado ('1' indica reservado).
        if 1 <= lugar <= self.capacidade and self.lugares[lugar - 1] == 1:

            # Se o lugar está reservado, executa a operação de remoção da
            # reserva no banco de dados.
            # O método 'delete_one' remove um documento específico da coleção,
            # neste caso, onde 'lugar' e 'dia' correspondem aos fornecidos.
            self.colecao_reservas.delete_one({"lugar": lugar, "dia": dia})

            # Retorna uma mensagem informando que a reserva foi cancelada com sucesso.
            return f"Lugar {lugar} reserva cancelada."

        else:

            # Se o lugar não está reservado, retorna uma mensagem
            # indicando que não há reserva para cancelar.
            return f"Lugar {lugar} não está reservado."


# Define a classe 'JanelaCadastro', responsável por criar e gerenciar a
# interface de cadastro de novas reservas de passagens.
class JanelaCadastro:

    # Método construtor que é chamado ao criar uma nova instância de JanelaCadastro.
    # Parâmetros:
    # janela_pai: referência à janela principal ou à janela que
    # chama a janela de cadastro.
    # onibus: objeto que representa o ônibus e suas reservas, permitindo
    # interagir com os dados de reserva.
    # janela_principal: referência à instância da JanelaPrincipal para
    # permitir chamadas de volta a métodos da janela principal.
    # data_inicial: data predefinida para facilitar o processo de cadastro,
    # geralmente a data atual selecionada na janela principal.
    def __init__(self,
                 janela_pai,
                 onibus,
                 janela_principal,
                 data_inicial,
                 lugar=None):

        # Armazena a referência à instância da janela principal para
        # que métodos desta possam ser acessados.
        self.janela_principal = janela_principal

        # Armazena a referência ao objeto onibus para acessar e
        # modificar os dados das reservas.
        self.onibus = onibus

        # Cria uma nova janela de nível superior, que aparecerá
        # sobre a janela principal.
        self.janela = tk.Toplevel(janela_pai)

        # Define o título da nova janela, que aparece na
        # barra de título da janela.
        self.janela.title("Cadastrar Reserva")

        # Configura a cor de fundo da janela para cinza claro (#f0f0f0),
        # mantendo a consistência estética com outras partes da aplicação.
        self.janela.configure(bg="#f0f0f0")

        # Após a criação da janela, este comando garante que quaisquer tarefas
        # pendentes que afetem o layout sejam processadas,
        # preparando a janela para operações de dimensionamento e posicionamento.
        self.janela.update_idletasks()

        # Obtém a largura total da tela onde a janela está sendo exibida.
        largura_tela = self.janela.winfo_screenwidth()

        # Obtém a altura total da tela onde a janela está sendo exibida.
        altura_tela = self.janela.winfo_screenheight()

        # Define a largura e altura da janela de cadastro.
        largura = 400
        altura = 550

        # Calcula a posição x da janela para que ela fique
        # centralizada horizontalmente na tela.
        pos_x = int(largura_tela / 2 - largura / 2)

        # Calcula a posição y da janela para que ela fique
        # centralizada verticalmente na tela.
        pos_y = int(altura_tela / 2 - altura / 2)

        # Configura a geometria da janela para usar as dimensões e posições
        # calculadas, fazendo com que a janela apareça centralizada na tela.
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Cria um label na janela de cadastro que serve como título da mesma.
        # 'text="Cadastrar Reserva"' define o texto exibido no label.
        # 'font=("Arial", 20, "bold")' configura a fonte do texto como Arial,
        # tamanho 20 e em negrito, o que destaca o título na interface.
        # 'bg="#f0f0f0"' define a cor de fundo do label como cinza claro,
        # consistente com o esquema de cores da janela.
        tk.Label(self.janela,
                 text="Cadastrar Reserva",
                 font=("Arial", 20, "bold"),
                 bg="#f0f0f0").pack(pady=20)

        # Cria um frame dentro da janela que contém os campos de
        # formulário para entrada de dados de reserva.
        # 'bg="#f0f0f0"' define a cor de fundo do frame como cinza claro.
        frame_form = tk.Frame(self.janela,
                              bg="#f0f0f0")

        # Empacota o frame dentro da janela com espaçamento interno
        # de 10 pixels em todas as direções para separar os elementos visuais.
        frame_form.pack(pady=10, padx=10)

        # Cria um rótulo 'Label' para o campo 'Nome' no formulário.
        tk.Label(frame_form,

                 # Define o texto do label.
                 text="Nome:",

                 # Configura a fonte do texto como Arial, tamanho 14,
                 # para manter a consistência visual.
                 font=("Arial", 14),

                 # Posiciona o label na primeira linha e primeira coluna,
                 # alinhado à direita ('sticky='e''), com padding de 5 pixels.
                 bg="#f0f0f0").grid(row=0,
                                    column=0,
                                    sticky='e',
                                    padx=5,
                                    pady=5)

        # Cria uma variável de controle do tipo StringVar, que é usada para armazenar e
        # gerenciar o conteúdo do campo de entrada associado.
        self.nome_var = tk.StringVar()

        # Cria um campo de entrada 'Entry' para o usuário inserir o nome.
        tk.Entry(frame_form,

                 # Associa o campo de entrada à variável de controle 'nome_var'.
                 textvariable=self.nome_var,

                 # Define a fonte para manter a consistência visual.
                 font=("Arial", 14),

                 # Posiciona o campo de entrada ao lado do rótulo 'Nome',
                 # na mesma linha, com padding de 5 pixels para espaçamento adequado.
                 width=20).grid(row=0,
                                column=1,
                                padx=5,
                                pady=5)

        # Cria um rótulo 'Label' para o campo 'CPF' no formulário.
        tk.Label(frame_form,

                 # Define o texto do label.
                 text="CPF:",

                 # Usa a mesma fonte e tamanho do label anterior para consistência.
                 font=("Arial", 14),

                 # Posiciona o label na segunda linha e primeira coluna,
                 # alinhado à direita, com padding de 5 pixels.
                 bg="#f0f0f0").grid(row=1,
                                    column=0,
                                    sticky='e',
                                    padx=5,
                                    pady=5)

        # Cria uma variável de controle do tipo StringVar para o campo de CPF.
        self.cpf_var = tk.StringVar()

        # Cria um campo de entrada 'Entry' para o usuário inserir o CPF.
        tk.Entry(frame_form,

                 # Associa o campo de entrada à variável de controle 'cpf_var'.
                 textvariable=self.cpf_var,

                 # Mantém a fonte consistente com os outros campos.
                 font=("Arial", 14),

                 # Posiciona o campo de entrada ao lado do rótulo 'CPF',
                 # na mesma linha, garantindo espaçamento adequado com padding de 5 pixels.
                 width=20).grid(row=1, column=1, padx=5, pady=5)

        # Cria um rótulo (Label) no formulário, especificando onde o número
        # do lugar será exibido ou inserido.
        # 'text="Lugar:"' define o texto exibido no rótulo, indicando que o
        # campo próximo a ele se refere ao número do lugar.
        # 'font=("Arial", 14)' configura a fonte do texto para Arial, tamanho 14,
        # garantindo que o texto seja claro e legível.
        # 'bg="#f0f0f0"' define a cor de fundo do rótulo como um cinza muito claro,
        # onde "#f0f0f0" é o código hexadecimal para essa cor.
        # '.grid(...)' posiciona o rótulo dentro de um layout de grade no formulário.
        # 'row=2' posiciona o rótulo na terceira linha da grade.
        # 'column=0' posiciona o rótulo na primeira coluna da grade.
        # 'sticky='e'' alinha o rótulo ao lado direito da célula da grade para
        # manter a consistência visual com outros campos.
        # 'padx=5' e 'pady=5' adicionam uma margem interna de 5 pixels em torno do
        # rótulo, separando-o visualmente dos outros elementos do formulário.
        tk.Label(frame_form,
                 text="Lugar:",
                 font=("Arial", 14),
                 bg="#f0f0f0").grid(row=2,
                                    column=0,
                                    sticky='e',
                                    padx=5,
                                    pady=5)

        # Cria uma variável do tipo StringVar para gerenciar o valor do campo
        # associado ao número do lugar.
        # 'value=str(lugar) if lugar else ""' inicializa a variável com o
        # número do lugar convertido para string, se existir,
        # ou com uma string vazia se nenhum valor inicial for fornecido.
        self.lugar_var = tk.StringVar(value=str(lugar) if lugar else "")

        # Cria um campo de entrada (Entry) onde o número do lugar pode ser visto.
        # 'textvariable=self.lugar_var' associa este campo de entrada à variável 'self.lugar_var',
        # permitindo que o valor do campo seja gerenciado dinamicamente.
        # 'font=("Arial", 14)' configura a fonte do texto dentro do campo para Arial, tamanho 14,
        # assegurando clareza e uniformidade com o restante do formulário.
        # 'width=5' define a largura do campo de entrada suficiente para acomodar um
        # número de lugar típico, garantindo que o campo não ocupe muito espaço.
        # 'state='disabled'' desativa a edição deste campo, impedindo que o usuário modifique
        # seu conteúdo diretamente, utilizado para casos onde o lugar já está
        # definido e não deve ser alterado.
        # '.grid(...)' posiciona o campo de entrada na grade do formulário.
        # 'row=2' coloca o campo de entrada na mesma linha do rótulo "Lugar".
        # 'column=1' coloca o campo de entrada na segunda coluna, ao lado do rótulo.
        # 'sticky='w'' alinha o campo de entrada ao lado esquerdo da célula da
        # grade para manter a consistência visual.
        # 'padx=5' e 'pady=5' adicionam uma margem externa de 5 pixels ao redor do
        # campo, garantindo que não fique muito próximo de outros elementos.
        tk.Entry(frame_form,
                 textvariable=self.lugar_var,
                 font=("Arial", 14),
                 width=5).grid(row=2,
                                        column=1,
                                        padx=5,
                                        pady=5,
                                        sticky='w')

        # Cria um rótulo (Label) para indicar o campo onde a data da reserva será escolhida.
        # 'text="Data da Reserva:"' especifica o texto que aparece no rótulo, orientando o
        # usuário sobre a funcionalidade do campo adjacente.
        # 'font=("Arial", 14)' define a fonte e tamanho do texto no rótulo, garantindo que
        # seja fácil de ler e esteticamente consistente com outros rótulos no formulário.
        # 'bg="#f0f0f0"' configura a cor de fundo do rótulo como cinza claro, especificamente o
        # código hexadecimal "#f0f0f0", o que mantém a cor de fundo uniforme em todo o formulário.
        # 'grid(row=3, column=0, sticky='e', padx=5, pady=5)' posiciona o rótulo na
        # terceira linha e primeira coluna do layout de grade,
        # alinhando-o à direita da célula ('sticky='e''), e adicionando um
        # espaçamento interno de 5 pixels em todas as direções para separação visual.
        tk.Label(frame_form,
                 text="Data da Reserva:",
                 font=("Arial", 14),
                 bg="#f0f0f0").grid(row=3,
                                    column=0,
                                    sticky='e',
                                    padx=5,
                                    pady=5)

        # Cria um widget Calendar, que permite ao usuário selecionar uma data de um calendário interativo.
        # 'frame_form' indica que o calendário será colocado dentro do frame do formulário.
        # 'selectmode='day'' configura o calendário para permitir a seleção de dias individuais.
        # 'date_pattern='dd/mm/yyyy'' define o formato da data exibida como dia, mês e ano em números.
        # Este widget facilita a entrada de datas, garantindo que o usuário selecione uma data válida.
        self.cal_cadastro = Calendar(frame_form,
                                     selectmode='day',
                                     date_pattern='dd/mm/yyyy')

        # Posiciona o widget de calendário na grade.
        # 'grid(row=3, column=1, padx=5, pady=5)' coloca o calendário na terceira
        # linha e segunda coluna do layout de grade, diretamente ao lado do
        # rótulo correspondente, e adiciona um espaçamento de 5 pixels em todas as
        # direções para consistência visual e espaço adequado.
        self.cal_cadastro.grid(row=3,
                               column=1,
                               padx=5,
                               pady=5)

        # Define a data inicial no widget de calendário.
        # 'selection_set(data_inicial)' configura o calendário para mostrar e
        # selecionar uma data inicial especificada, o que é útil quando a
        # data já é conhecida ou deve ser pré-definida, como em um
        # formulário de edição de reserva.
        self.cal_cadastro.selection_set(data_inicial)

        # Cria um botão na interface gráfica que permite ao usuário confirmar a ação de reserva.
        # 'self.janela' especifica que o botão será colocado na janela principal ou em
        # uma janela específica definida anteriormente na classe.
        # 'text="Reservar"' define o texto exibido no botão, que é "Reservar", indicando a
        # ação que o botão realizará quando pressionado.
        # 'font=("Arial", 14)' configura a fonte do texto no botão, utilizando Arial tamanho 14,
        # para manter a legibilidade e consistência com outros textos da interface.
        # 'bg="#dcedc8"' define a cor de fundo do botão como um verde claro, onde "#dcedc8" é o
        # código hexadecimal dessa cor, escolhida para dar uma aparência amigável e destacada.
        # 'command=self.reservar' associa o botão à função 'reservar', que é um método definido
        # dentro da mesma classe. Esta função será executada quando o botão for clicado,
        # tratando de toda a lógica de reserva com base nos dados inseridos no formulário.
        # 'pack(pady=20)' posiciona o botão na interface, usando o gerenciador de geometria 'pack',
        # que coloca o botão e o centraliza por padrão.
        # 'pady=20' adiciona uma margem vertical de 20 pixels acima e abaixo do botão,
        # separando-o de outros elementos da interface para evitar um layout
        # visualmente congestionado.
        tk.Button(self.janela,
                  text="Reservar",
                  font=("Arial", 14),
                  bg="#dcedc8",
                  command=self.reservar).pack(pady=20)

    # Define o método 'reservar' que é chamado ao clicar no
    # botão "Reservar" na janela de cadastro.
    def reservar(self):

        # Obtém e limpa os espaços em branco em torno do nome inserido pelo usuário.
        nome = self.nome_var.get().strip()

        # Obtém e limpa os espaços em branco em torno do CPF inserido pelo usuário.
        cpf = self.cpf_var.get().strip()

        # Obtém a data selecionada no widget de calendário.
        dia = self.cal_cadastro.get_date()

        # Tenta converter o valor inserido no campo 'Lugar' para um inteiro.
        try:
            lugar = int(self.lugar_var.get())

        except:

            # Se a conversão falhar, mostra uma mensagem de aviso e encerra a função.
            messagebox.showwarning("Aviso", "Lugar inválido.")
            return

        # Verifica se todos os campos necessários foram preenchidos.
        if not nome or not cpf or not dia:

            # Se algum campo estiver vazio, mostra uma mensagem de aviso e encerra a função.
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        # Chama o método 'reservar_lugar' da instância do ônibus para tentar reservar o lugar.
        res = self.onibus.reservar_lugar(lugar, nome, cpf, dia)

        # Mostra uma mensagem informativa com o resultado da tentativa de
        # reserva (sucesso ou falha).
        messagebox.showinfo("Info", res)

        # Destroi a janela de cadastro, fechando-a após a
        # reserva ser completada ou falhada.
        self.janela.destroy()

        # Chama o método 'atualizar_mapa' da janela principal para atualizar a
        # visualização dos lugares com base na nova reserva.
        self.janela_principal.atualizar_mapa()



# Define a classe 'JanelaPesquisa' para gerenciar a interface de
# pesquisa de reservas históricas.
class JanelaPesquisa:

    # Método construtor que é chamado ao criar uma nova instância de JanelaPesquisa.
    def __init__(self, janela_pai, onibus, janela_principal):

        # Armazena a referência à instância da janela principal para que
        # métodos desta possam ser acessados.
        self.janela_principal = janela_principal

        # Armazena a referência ao objeto onibus para acessar e
        # modificar os dados das reservas.
        self.onibus = onibus

        # Cria uma nova janela de nível superior que aparecerá
        # acima da janela principal.
        self.janela = tk.Toplevel(janela_pai)

        # Define o título da nova janela, que aparece na barra de título da janela.
        self.janela.title("Pesquisar Reservas")

        # Configura a cor de fundo da janela para cinza claro (#f0f0f0),
        # mantendo a consistência visual com outras partes da aplicação.
        self.janela.configure(bg="#f0f0f0")

        # Após a criação da janela, processa tarefas pendentes para garantir
        # que as dimensões da janela sejam atualizadas.
        self.janela.update_idletasks()

        # Obtém a largura total da tela onde a janela está sendo exibida.
        largura_tela = self.janela.winfo_screenwidth()

        # Obtém a altura total da tela onde a janela está sendo exibida.
        altura_tela = self.janela.winfo_screenheight()

        # Define a largura e altura desejadas para a janela de pesquisa.
        largura = 1250
        altura = 500

        # Calcula a posição x e y para centralizar a janela na tela.
        pos_x = int(largura_tela / 2 - largura / 2)
        pos_y = int(altura_tela / 2 - altura / 2)

        # Aplica a geometria calculada à janela, usando as dimensões e
        # as posições x e y definidas,
        # garantindo que a janela seja centralizada na tela do usuário.
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        # Cria um frame 'frame_filtros' na janela de pesquisa para
        # conter os campos de filtro.
        # 'bg="#f0f0f0"' configura a cor de fundo do frame como cinza claro.
        frame_filtros = tk.Frame(self.janela,
                                 bg="#f0f0f0")

        # 'pack(pady=10)' empacota o frame dentro da janela com um
        # espaçamento vertical de 10 pixels.
        frame_filtros.pack(pady=10)

        # Define uma lista com os rótulos dos campos de filtro que serão criados.
        self.rotulos_filtro = ["Lugar", "Nome", "CPF", "Data"]

        # Cria uma lista vazia para armazenar as referências aos
        # campos de entrada que serão criados.
        self.campos_filtro = []

        # Itera sobre cada rótulo na lista de rótulos de filtro.
        for rot in self.rotulos_filtro:

            # Cria um rótulo para cada filtro e o adiciona ao 'frame_filtros'.
            # 'text=rot' define o texto do label baseado no rótulo.
            # 'font=("Arial", 14)' configura a fonte do texto como Arial tamanho 14.
            # 'pack(side=tk.LEFT, padx=10)' empacota o rótulo alinhado à
            # esquerda com um espaçamento horizontal de 10 pixels.
            tk.Label(frame_filtros,
                     text=rot,
                     font=("Arial", 14),
                     bg="#f0f0f0").pack(side=tk.LEFT,
                                        padx=10)

            # Cria um campo de entrada ('Entry') para inserção dos dados de filtro.
            # 'font=("Arial", 14)' especifica a fonte do texto no campo de entrada.
            campo = tk.Entry(frame_filtros, font=("Arial", 14))

            # Empacota o campo de entrada alinhado à esquerda diretamente
            # ao lado do seu rótulo correspondente.
            campo.pack(side=tk.LEFT)

            # Adiciona o campo de entrada à lista 'campos_filtro' para fácil
            # acesso e manipulação posterior.
            self.campos_filtro.append(campo)

        # Cria um widget Treeview na janela de pesquisa. Treeview é usado
        # para exibir os dados em formato de tabela.
        self.treeview = ttk.Treeview(self.janela)

        # Define as colunas que o Treeview terá. Cada coluna
        # precisa de um identificador.
        self.treeview["columns"] = ("Lugar", "Nome", "CPF", "Data")

        # Configura os cabeçalhos das colunas, especificando o texto e o alinhamento de cada um.
        self.treeview.heading("Lugar", text="Lugar", anchor=tk.CENTER)  # Cabeçalho para a coluna "Lugar", centrado.
        self.treeview.heading("Nome", text="Nome", anchor=tk.CENTER)  # Cabeçalho para a coluna "Nome", centrado.
        self.treeview.heading("CPF", text="CPF", anchor=tk.CENTER)  # Cabeçalho para a coluna "CPF", centrado.
        self.treeview.heading("Data", text="Data", anchor=tk.CENTER)  # Cabeçalho para a coluna "Data", centrado.

        # Configura a coluna #0, que é a coluna padrão usada para hierarquia
        # quando o Treeview é usado para exibir dados hierárquicos.
        # Configura a largura para 0 para não exibi-la, pois não será usada.
        self.treeview.column("#0", width=0, stretch=tk.NO)

        # Configura o estilo do Treeview usando o módulo ttk.Style.
        style = ttk.Style()

        # Define a fonte para os itens no Treeview.
        style.configure("Treeview", font=("Arial", 14))

        # Define a fonte para os cabeçalhos das colunas.
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Configura o tamanho e o alinhamento das colunas definidas anteriormente.
        self.treeview.column("Lugar", width=100,
                             anchor=tk.CENTER)  # Configura a coluna "Lugar" com largura 100 e alinhamento central.
        self.treeview.column("Nome", width=200,
                             anchor=tk.W)  # Configura a coluna "Nome" com largura 200 e alinhamento à esquerda (West).
        self.treeview.column("CPF", width=150,
                             anchor=tk.CENTER)  # Configura a coluna "CPF" com largura 150 e alinhamento central.
        self.treeview.column("Data", width=100,
                             anchor=tk.CENTER)  # Configura a coluna "Data" com largura 100 e alinhamento central.

        # Carrega todas as reservas disponíveis na coleção de reservas do
        # MongoDB e as armazena em uma lista.
        self.reservas = list(self.onibus.colecao_reservas.find({}))

        # Itera sobre cada reserva obtida da base de dados.
        for r in self.reservas:

            # Insere cada reserva como uma nova linha no Treeview. Cada elemento da
            # tupla corresponde a uma coluna no Treeview.
            # "" e tk.END especificam que o item deve ser inserido no final da
            # lista de itens, sem hierarquia de pai-filho.
            self.treeview.insert("",
                                 tk.END,
                                 values=(r["lugar"], r["nome"], r["cpf"], r["dia"]))

        # Cria uma barra de rolagem vertical e associa-a ao Treeview.
        scrollbar = ttk.Scrollbar(self.janela,
                                  orient=tk.VERTICAL,
                                  command=self.treeview.yview)

        # Empacota a barra de rolagem na janela, alinhada à direita e expandindo-se
        # verticalmente para preencher o espaço disponível ao lado do Treeview.
        scrollbar.pack(side=tk.RIGHT,
                       fill=tk.Y)

        # Configura o Treeview para usar a barra de rolagem vertical criada.
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Empacota o Treeview na janela, permitindo que ele expanda tanto
        # verticalmente quanto horizontalmente para ocupar o espaço disponível.
        self.treeview.pack(pady=10,
                           padx=10,
                           fill=tk.BOTH,
                           expand=True)

        # Define a função 'filtrar_reservas' que não aceita nenhum argumento externo.
        def filtrar_reservas():

            # Inicia removendo todos os itens existentes no Treeview para
            # preparar a exibição dos itens filtrados.
            # Itera sobre todos os itens (filhos) presentes no Treeview.
            for i in self.treeview.get_children():

                # Deleta cada item iterativamente, limpando o Treeview.
                self.treeview.delete(i)

            # Cria um dicionário 'filtros' para armazenar os critérios de
            # pesquisa baseados nos valores dos campos de entrada.
            filtros = {}

            # Itera simultaneamente sobre os rótulos dos filtros e os
            # respectivos campos de entrada.
            for rot, campo in zip(self.rotulos_filtro, self.campos_filtro):

                # Obtém o valor inserido no campo de entrada e remove espaços
                # desnecessários das extremidades.
                valor = campo.get().strip()

                # Verifica se algum valor foi inserido no campo.
                if valor:

                    # Se um valor foi inserido, adiciona-o ao dicionário de filtros,
                    # convertendo o valor para letras minúsculas.
                    # A chave do dicionário é o rótulo do filtro (por exemplo, "Nome", "CPF") e
                    # o valor é o texto inserido pelo usuário.
                    filtros[rot] = valor.lower()

            # Itera sobre cada reserva previamente carregada na lista 'self.reservas'.
            for rr in self.reservas:

                # Converte os valores de cada campo da reserva para strings e,
                # se necessário, para letras minúsculas.
                # Isso garante que a busca seja insensível a maiúsculas e minúsculas.
                lugar_str = str(rr["lugar"])  # Converte o número do lugar para uma string.
                nome_str = rr["nome"].lower()  # Converte o nome para letras minúsculas.
                cpf_str = rr["cpf"].lower()  # Converte o CPF para letras minúsculas.
                dia_str = rr["dia"].lower()  # Converte a data para letras minúsculas.

                # Inicializa uma variável booleana 'corresponde' como True, assumindo que a
                # reserva corresponde aos filtros até que se prove o contrário.
                corresponde = True

                # Verifica se há um filtro para o lugar e, se sim, verifica se o
                # valor não corresponde ao lugar da reserva.
                # Se não corresponder, marca 'corresponde' como False.
                if "Lugar" in filtros and filtros["Lugar"] != lugar_str.lower():
                    corresponde = False

                # Verifica se há um filtro para o nome e, se sim, verifica se o
                # valor inserido não está contido no nome da reserva.
                # Se o nome não contiver o filtro, marca 'corresponde' como False.
                if "Nome" in filtros and filtros["Nome"] not in nome_str:
                    corresponde = False

                # Verifica se há um filtro para o CPF e, se sim, verifica se o
                # valor não corresponde ao CPF da reserva.
                # Se não corresponder, marca 'corresponde' como False.
                if "CPF" in filtros and filtros["CPF"] != cpf_str:
                    corresponde = False

                # Verifica se há um filtro para a data e, se sim, verifica se o
                # valor não corresponde à data da reserva.
                # Se não corresponder, marca 'corresponde' como False.
                if "Data" in filtros and filtros["Data"] != dia_str:
                    corresponde = False

                # Se a reserva passou em todos os critérios de filtro (corresponde
                # ainda é True), insere-a no Treeview.
                if corresponde:

                    # Insere a reserva no Treeview como uma nova linha.
                    # Os valores correspondem às colunas definidas anteriormente no
                    # Treeview (Lugar, Nome, CPF, Data).
                    self.treeview.insert("",
                                         tk.END,
                                         values=(rr["lugar"], rr["nome"], rr["cpf"], rr["dia"]))


        # Define a função 'cancelar_reserva' que lida com a exclusão de
        # uma reserva selecionada no Treeview.
        def cancelar_reserva():

            # Obtém a seleção atual no Treeview. Selec é uma tupla contendo os
            # identificadores dos itens selecionados.
            selec = self.treeview.selection()

            # Verifica se nenhuma linha foi selecionada no Treeview.
            if not selec:

                # Mostra uma mensagem de aviso caso o usuário não tenha selecionado uma reserva.
                messagebox.showwarning("Aviso", "Selecione uma reserva para cancelar.")
                return  # Encerra a função, pois não há nenhuma reserva para cancelar.

            # Obtém os detalhes do item selecionado no Treeview.
            item = self.treeview.item(selec[0])

            # Obtém o valor do número do lugar a partir da primeira
            # coluna do item selecionado.
            lugar = item["values"][0]

            # Obtém a data da reserva a partir da quarta coluna do item selecionado.
            dia = item["values"][3]

            # Chama o método 'cancelar_reserva' da instância do ônibus,
            # passando o lugar e a data.
            # Isso executa a exclusão da reserva no banco de dados e
            # retorna uma mensagem de confirmação.
            res = self.onibus.cancelar_reserva(lugar, dia)

            # Mostra uma mensagem informativa com o resultado da
            # tentativa de cancelamento.
            messagebox.showinfo("Info", res)

            # Recarrega os dados do Treeview após o cancelamento.
            # Primeiro, limpa todos os itens existentes no Treeview.
            for i in self.treeview.get_children():
                self.treeview.delete(i)

            # Carrega novamente todas as reservas do banco de dados e as
            # armazena na lista 'self.reservas'.
            self.reservas = list(self.onibus.colecao_reservas.find({}))

            # Insere as reservas recarregadas no Treeview, atualizando a exibição.
            for rr in self.reservas:
                self.treeview.insert("",
                                     tk.END,
                                     values=(rr["lugar"], rr["nome"], rr["cpf"], rr["dia"]))

            # Atualiza o mapa de assentos na janela principal para refletir as mudanças.
            self.janela_principal.atualizar_mapa()


        botao_filtrar = tk.Button(
            frame_filtros,  # Adiciona o botão dentro do frame de filtros.
            text="Filtrar",  # Define o texto exibido no botão como "Filtrar".
            font=("Arial", 14),  # Configura a fonte do texto como Arial, tamanho 14.
            bg="#dcedc8",  # Define a cor de fundo do botão para um verde claro (#dcedc8).
            command=filtrar_reservas
            # Associa a função `filtrar_reservas` ao botão. Esta função será executada ao clicar no botão.
        )
        botao_filtrar.pack(

            # Posiciona o botão alinhado à esquerda dentro do frame.
            side=tk.LEFT,

            # Adiciona um espaçamento horizontal de 10 pixels para
            # separar o botão de outros elementos.
            padx=10

        )

        botao_cancelar = tk.Button(

            # Adiciona o botão diretamente na janela principal de pesquisa.
            self.janela,

            # Define o texto exibido no botão.
            text="Cancelar Reserva Selecionada",

            # Configura a fonte do texto como Arial, tamanho 14.
            font=("Arial", 14),

            # Define a cor de fundo do botão para um amarelo claro (#ffe082).
            bg="#ffe082",

            # Associa a função `cancelar_reserva` ao botão. Esta função
            # será executada ao clicar no botão.
            command=cancelar_reserva

        )

        botao_cancelar.pack(

            # Adiciona um espaçamento vertical de 10 pixels para separar o
            # botão de outros elementos na janela.
            pady=10

        )


# Define a classe 'JanelaPrincipal' que gerencia a janela principal do
# sistema de reserva de passagens.
class JanelaPrincipal:

    # Método construtor que inicializa uma nova instância da JanelaPrincipal com a
    # janela do sistema e uma instância do ônibus.
    def __init__(self, janela_sistema, onibus):

        # Armazena a referência da janela principal do sistema (tk.Tk())
        # passada como argumento.
        self.janela_sistema = janela_sistema

        # Armazena a referência para a instância da classe
        # Onibus passada como argumento.
        self.onibus = onibus

        # Define o título da janela do sistema, que aparecerá na
        # barra de título da janela.
        self.janela_sistema.title("Sistema de Reserva de Passagens")

        # Configura o estado da janela para 'zoomed', fazendo com que
        # ela maximize automaticamente quando for aberta.
        self.janela_sistema.state('zoomed')

        # Define a cor de fundo da janela principal para um
        # cinza claro (#f0f0f0).
        self.janela_sistema.configure(bg="#f0f0f0")

        # Cria um frame principal que atuará como o contêiner principal
        # para outros widgets dentro da janela do sistema.
        frame_principal = tk.Frame(self.janela_sistema, bg="#f0f0f0")

        # Empacota o frame principal para preencher toda a janela, expandindo-se
        # conforme necessário para ocupar o espaço disponível.
        frame_principal.pack(fill='both', expand=True)

        # Cria um frame secundário 'frame_esquerda' dentro do 'frame_principal'.
        # 'bg="#f0f0f0"' define a cor de fundo do frame como um cinza claro.
        frame_esquerda = tk.Frame(frame_principal, bg="#f0f0f0")

        # Empacota 'frame_esquerda' na janela.
        # 'side='left'' posiciona o frame no lado esquerdo da janela principal.
        # 'fill='y'' faz com que o frame expanda verticalmente para ocupar todo o
        # espaço vertical disponível na janela.
        # 'padx=20' e 'pady=20' adicionam uma margem interna de 20 pixels em
        # todas as direções para separar os elementos visuais dentro do frame.
        frame_esquerda.pack(side='left',
                            fill='y',
                            padx=20,
                            pady=20)

        # Cria um widget 'Label' chamado 'titulo', que serve como
        # título da seção dentro do 'frame_esquerda'.
        # 'text="Reserva de Passagens"' define o texto exibido no label.
        # 'font=("Arial", 24, "bold")' define a fonte do texto como Arial, tamanho 24, em negrito.
        # 'bg="#f0f0f0"' configura a cor de fundo do label para combinar
        # com o fundo do frame.
        titulo = tk.Label(frame_esquerda,
                          text="Reserva de Passagens",
                          font=("Arial", 24, "bold"),
                          bg="#f0f0f0")

        # Empacota o widget 'titulo' dentro do 'frame_esquerda'.
        # 'pady=20' adiciona espaço vertical de 20 pixels acima e abaixo do
        # título para evitar que os elementos fiquem muito juntos.
        titulo.pack(pady=20)


        # Cria outro widget 'Label' para instruir os usuários a
        # selecionarem uma data.
        # 'text="Selecione a data:"' fornece as instruções visuais para os usuários.
        # 'font=("Arial", 16)' define a fonte do texto como
        # Arial, tamanho 16, que é menor que a do título para uma hierarquia visual.
        # 'bg="#f0f0f0"' mantém a cor de fundo consistente com o
        # restante da interface.
        tk.Label(frame_esquerda,
                 text="Selecione a data:",
                 font=("Arial", 16),
                 bg="#f0f0f0").pack(pady=10)

        # Instancia o widget 'Calendar' que permite aos usuários escolher uma data.
        # 'selectmode='day'' configura o calendário para permitir a
        # seleção de dias individuais.
        # 'date_pattern='dd/mm/yyyy'' estabelece o formato de data
        # mostrado no calendário para dia, mês e ano.
        self.cal = Calendar(frame_esquerda,
                            selectmode='day',
                            date_pattern='dd/mm/yyyy')

        # Empacota o calendário dentro do 'frame_esquerda'.
        # 'pady=10' adiciona espaço vertical de 10 pixels acima e abaixo do
        # calendário para uma distribuição uniforme dos elementos.
        self.cal.pack(pady=10)

        # Cria um frame que será usado para conter o mapa de assentos
        # na parte direita da janela principal.
        # 'frame_principal' é o contêiner pai onde este novo frame será inserido.
        # 'bg="#f0f0f0"' define a cor de fundo do frame como cinza claro,
        # onde "#f0f0f0" é o código hexadecimal dessa cor,
        # proporcionando um fundo neutro que não distrai.
        frame_direita = tk.Frame(frame_principal,
                                 bg="#f0f0f0")

        # Posiciona o 'frame_direita' dentro do 'frame_principal'.
        # 'side='right'' faz com que o frame seja ancorado ao lado direito da janela principal.
        # 'fill='both'' faz com que o frame expanda tanto horizontal quanto
        # verticalmente para preencher o espaço disponível.
        # 'expand=True' permite que o frame expanda para ocupar qualquer espaço
        # extra na janela, garantindo que utilize todo o espaço disponível.
        # 'padx=5' e 'pady=20' adicionam um espaçamento externo de 5 pixels
        # horizontalmente e 20 pixels verticalmente em torno do frame,
        # criando uma margem que separa o frame dos outros elementos ou bordas da janela.
        frame_direita.pack(side='right',
                           fill='both',
                           expand=True,
                           padx=5,
                           pady=20)

        # Cria um rótulo dentro do 'frame_direita' para servir como título da
        # seção do mapa de assentos.
        # 'text="Mapa de Assentos"' define o texto que será exibido no rótulo,
        # indicando claramente a função daquela área da interface.
        # 'font=("Arial", 20, "bold")' define a fonte do texto como Arial,
        # tamanho 20, em negrito, destacando o título e tornando-o facilmente legível.
        # 'bg="#f0f0f0"' mantém a cor de fundo do rótulo consistente com a do
        # frame, mantendo um design uniforme.
        self.mapa_label = tk.Label(
            frame_direita,
            text="Mapa de Assentos",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )

        # Posiciona o rótulo 'self.mapa_label' dentro do 'frame_direita'.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels acima e abaixo do rótulo,
        # ajudando a separar visualmente o título do resto do conteúdo do
        # frame e melhorando a estética.
        self.mapa_label.pack(pady=10)

        # Cria um frame secundário dentro do 'frame_direita' que foi definido
        # anteriormente. Este frame será específico para o mapa de assentos,
        # substituindo um widget de texto por botões, que representarão os assentos.
        # Isso oferece uma interatividade maior para o usuário.
        # 'bg="#f0f0f0"' define a cor de fundo do frame como cinza claro,
        # usando o código hexadecimal "#f0f0f0".
        # Manter a cor consistente com o restante da interface ajuda a manter um
        # design coeso e minimiza distrações visuais.
        self.frame_mapa = tk.Frame(frame_direita,
                                   bg="#f0f0f0")

        # Posiciona o 'self.frame_mapa' dentro do 'frame_direita'.
        # 'fill='both'' especifica que o frame deve expandir tanto vertical quanto
        # horizontalmente para preencher todo o espaço disponível dentro do 'frame_direita'.
        # Isso garante que o mapa de assentos utilize todo o espaço designado para ele,
        # otimizando o uso da área disponível.
        # 'expand=True' permite que o frame cresça para ocupar qualquer espaço
        # adicional na janela, garantindo que o mapa de assentos seja
        # exibido de forma adequada.
        # 'pady=10' adiciona uma margem vertical de 10 pixels acima e abaixo do frame,
        # proporcionando um espaçamento que separa visualmente o mapa de assentos de
        # outros conteúdos ou bordas do 'frame_direita'.
        self.frame_mapa.pack(fill='both',
                             expand=True,
                             pady=10)

        # Cria um Canvas dentro do 'self.frame_mapa', que é o frame
        # dedicado ao mapa de assentos.
        # 'bg="#f0f0f0"' define a cor de fundo do Canvas como cinza claro, o
        # código hexadecimal "#f0f0f0" é usado para manter a consistência
        # visual com o restante da interface.
        # O Canvas é utilizado aqui como uma área de desenho flexível onde os
        # botões representando os assentos serão adicionados.
        # Isso permite uma organização gráfica mais complexa e
        # personalizada dos componentes da interface.
        self.canvas = tk.Canvas(self.frame_mapa,
                                bg="#f0f0f0")

        # Cria uma barra de rolagem vertical associada ao Canvas criado anteriormente.
        # 'orient=tk.VERTICAL' configura a orientação da barra de rolagem para
        # vertical, o que é apropriado para a visualização de uma lista extensa de
        # assentos que pode não caber totalmente na altura disponível da janela.
        # 'command=self.canvas.yview' associa a movimentação da barra de rolagem ao
        # deslocamento vertical do conteúdo dentro do Canvas.
        # Isso permite que o usuário desloque a visualização dos assentos verticalmente
        # usando a barra de rolagem, melhorando a acessibilidade e usabilidade da interface.
        self.scrollbar = tk.Scrollbar(self.frame_mapa,
                                      orient=tk.VERTICAL,
                                      command=self.canvas.yview)

        # Configura o Canvas para responder ao deslocamento da barra de rolagem.
        # 'yscrollcommand=self.scrollbar.set' faz com que a posição da barra de
        # rolagem reflita e controle a posição da visualização vertical dentro do Canvas.
        # Essa configuração é necessária para sincronizar o movimento da barra de
        # rolagem com o conteúdo do Canvas, garantindo que o usuário possa
        # navegar efetivamente pelo mapa de assentos.
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Adiciona a barra de rolagem ('scrollbar') ao lado direito do frame que contém o canvas.
        # 'side=tk.RIGHT' posiciona a barra de rolagem na parte direita do frame 'self.frame_mapa'.
        # 'fill=tk.Y' faz com que a barra de rolagem se estenda verticalmente ao
        # longo de todo o lado direito do frame, ocupando todo o espaço vertical disponível.
        # Essa configuração é ideal para interfaces onde é necessário rolar
        # através de uma lista longa de itens, como um mapa de assentos.
        self.scrollbar.pack(side=tk.RIGHT,
                            fill=tk.Y)

        # Adiciona o canvas ao lado esquerdo do frame, garantindo que ele ocupe o
        # espaço restante não utilizado pela barra de rolagem.
        # 'side=tk.LEFT' posiciona o canvas à esquerda dentro do frame,
        # oposto à barra de rolagem.
        # 'fill=tk.BOTH' permite que o canvas expanda tanto vertical quanto
        # horizontalmente para preencher todo o espaço disponível no frame.
        # 'expand=True' faz com que o canvas cresça para ocupar qualquer espaço
        # extra na interface, garantindo que o conteúdo dentro do
        # canvas seja acessível e bem apresentado.
        self.canvas.pack(side=tk.LEFT,
                         fill=tk.BOTH,
                         expand=True)

        # Cria um frame dentro do canvas para servir como container para os
        # widgets (como botões que representam os assentos).
        # Este frame será usado para organizar visualmente os assentos dentro do canvas.
        # 'bg="#f0f0f0"' define a cor de fundo do frame interno como cinza claro,
        # mantendo a consistência com o design geral da interface.
        self.canvas_frame = tk.Frame(self.canvas,
                                     bg="#f0f0f0")

        # Cria uma 'janela' dentro do canvas, onde o 'self.canvas_frame' é ancorado.
        # '(0, 0)' define a posição inicial da janela no canvas, no canto superior esquerdo.
        # 'window=self.canvas_frame' especifica que o frame interno criado
        # anteriormente será o conteúdo dessa 'janela'.
        # 'anchor="nw"' garante que o frame seja ancorado a partir do canto
        # superior esquerdo (noroeste), ajudando a manter a orientação
        # correta dos conteúdos dentro do canvas.
        self.canvas.create_window((0, 0),
                                  window=self.canvas_frame,
                                  anchor="nw")

        # Cria um botão no frame à esquerda que, quando clicado, chamará a
        # função 'atualizar_mapa' para atualizar a visualização dos assentos.
        # 'text="Atualizar Mapa"' define o texto do botão.
        # 'font=("Arial", 16)' define a fonte do texto como Arial tamanho 16.
        # 'bg="#dcedc8"' define a cor de fundo do botão para um verde claro.
        # 'command=self.atualizar_mapa' associa o botão à função 'atualizar_mapa'
        # que será executada ao clicar no botão.
        # 'pack(pady=10)' posiciona o botão no frame, adicionando um espaçamento
        # vertical de 10 pixels para separação dos elementos.
        tk.Button(frame_esquerda,
                  text="Atualizar Mapa",
                  font=("Arial", 16),
                  bg="#dcedc8",
                  command=self.atualizar_mapa).pack(pady=10)

        # Cria um botão para abrir a janela de cadastro de novas reservas.
        # 'text="Cadastrar (Reservar)"' define o texto do botão.
        # 'bg="#a5d6a7"' define a cor de fundo do botão para um verde médio.
        tk.Button(frame_esquerda,
                  text="Cadastrar (Reservar)",
                  font=("Arial", 16),
                  bg="#a5d6a7",
                  command=self.abrir_cadastro).pack(pady=10)

        # Cria um botão para abrir a janela de pesquisa de reservas históricas,
        # que permite ao usuário consultar reservas passadas.
        tk.Button(frame_esquerda,

                  # Define o texto do botão.
                  text="Pesquisar (Histórico)",

                  # Define a fonte como Arial tamanho 16, garantindo que o texto seja legível.
                  font=("Arial", 16),

                  # Define a cor de fundo do botão para um azul claro, criando um visual atraente.
                  bg="#b3e5fc",

                  # Associa o botão à função 'abrir_pesquisa' e posiciona com um
                  # padding vertical de 10 pixels para separação.
                  command=self.abrir_pesquisa).pack(pady=10)

        # Seleciona a data atual no calendário e atualiza o mapa de assentos.
        # 'hoje = datetime.now().strftime("%d/%m/%Y")' obtém a data
        # atual formatada como dia/mês/ano.
        hoje = datetime.now().strftime("%d/%m/%Y")

        # 'self.cal.selection_set(hoje)' define a data selecionada no
        # calendário como a data atual.
        self.cal.selection_set(hoje)

        # 'self.atualizar_mapa()' chama a função para atualizar o
        # mapa de assentos com a data atual.
        self.atualizar_mapa()


    """
        Atualiza o mapa de assentos em formato de duas colunas com 
                barra de rolagem e largura expandida.
        Este método é responsável por mostrar visualmente o estado atual dos 
                assentos (livres ou reservados) com base na data selecionada no calendário.
        """

    def atualizar_mapa(self):

        # A linha abaixo recupera a data selecionada pelo usuário no
        # widget de calendário.
        # O método 'get_date()' é um método do tkcalendar.Calendar que
        # retorna a data selecionada no formato de string.
        data = self.cal.get_date()

        # Após obter a data, o método 'carregar_reservas' do objeto 'onibus' é
        # chamado com essa data como argumento.
        # Este método é responsável por carregar o estado atual dos assentos (se
        # estão reservados ou não) para a data especificada,
        # atualizando o atributo 'lugares' do objeto 'onibus' que é uma lista onde
        # cada posição representa um assento e o valor
        # indica se o assento está reservado (1) ou não (0).
        self.onibus.carregar_reservas(data)

        # A seguir, todos os widgets existentes no 'canvas_frame' são removidos.
        # 'canvas_frame' é um contêiner (frame) dentro de um objeto 'Canvas' que
        # contém botões representando os assentos do ônibus.
        # O método 'winfo_children()' retorna uma lista de todos os widgets filhos (neste
        # caso, botões de assento) contidos dentro de 'canvas_frame'.
        for widget in self.canvas_frame.winfo_children():

            # Cada widget (botão de assento) é destruído iterativamente.
            # O método 'destroy()' é usado para remover completamente um widget da
            # interface gráfica e liberar todos os recursos de sistema relacionados.
            widget.destroy()

        # Adiciona os botões no layout de duas colunas
        for i in range(self.onibus.capacidade):

            # Verifica se o assento atual (índice i) está reservado. A lista 'lugares'
            # contém 1 para reservado e 0 para livre.
            reservado = self.onibus.lugares[i] == 1

            # Define a cor do botão baseado no status do assento: amarelo (#ffd700) se
            # reservado, verde (#98fb98) se livre.
            cor = "#ffd700" if reservado else "#98fb98"

            # A função 'manipular_click' captura o valor atual de 'i' na variável 'indice'.
            def manipular_click(indice=i):

                # Verifica se o assento no índice especificado está reservado.
                if self.onibus.lugares[indice] == 1:

                    # Consulta no banco de dados MongoDB para encontrar uma reserva específica.
                    # Usa 'find_one' para buscar um único documento que corresponde aos
                    # critérios: número do lugar ('lugar') e data ('dia').
                    # 'indice + 1' ajusta o índice base-0 para base-1, já que os
                    # lugares no banco de dados começam em 1, não em 0.
                    reserva = self.onibus.colecao_reservas.find_one({"lugar": indice + 1, "dia": data})

                    # Verifica se algum documento foi encontrado com os critérios especificados.
                    # Se 'reserva' não é None, significa que uma reserva foi encontrada
                    # para o assento e a data especificados.
                    if reserva:

                        # Constrói uma string que contém as informações da reserva encontrada.
                        # Esta string inclui o número do lugar, o nome da pessoa que fez a
                        # reserva, o CPF e a data da reserva.
                        # Os dados são acessados diretamente do documento retornado do banco de dados.
                        info_reserva = (
                            f"Lugar: {reserva['lugar']}\n"
                            f"Nome: {reserva['nome']}\n"
                            f"CPF: {reserva['cpf']}\n"
                            f"Data: {reserva['dia']}"
                        )

                        # Abre uma caixa de diálogo perguntando ao usuário se deseja
                        # cancelar a reserva encontrada.
                        # 'askyesno' cria uma janela de mensagem com botões 'Sim' e 'Não'.
                        # O texto exibido inclui as informações da reserva e pergunta se o
                        # usuário deseja cancelar essa reserva.
                        confirmar = messagebox.askyesno("Reserva Encontrada",
                                                        f"{info_reserva}\n\nDeseja cancelar esta reserva?")

                        # Verifica se o usuário clicou no botão 'Sim' na caixa de diálogo.
                        if confirmar:

                            # Chama o método 'cancelar_reserva' do objeto 'onibus' para
                            # cancelar a reserva no banco de dados.
                            # Passa o índice do lugar (ajustado para base-1) e a data como
                            # argumentos para identificar a reserva a ser cancelada.
                            resultado = self.onibus.cancelar_reserva(indice + 1, data)

                            # Exibe uma mensagem informando o resultado do processo de cancelamento.
                            # 'showinfo' cria uma janela de mensagem que mostra o texto do
                            # resultado, que geralmente confirma o cancelamento.
                            messagebox.showinfo("Reserva Cancelada", resultado)

                            # Atualiza o mapa de assentos para refletir a mudança no estado
                            # dos assentos após o cancelamento.
                            # Isso garante que o mapa gráfico dos assentos mostre o assento
                            # como disponível se o cancelamento foi bem-sucedido.
                            self.atualizar_mapa()


                else:

                    # Se o lugar está disponível, abre a janela de cadastro para fazer uma nova reserva.
                    JanelaCadastro(self.janela_sistema, self.onibus, self, data, lugar=indice + 1)

            # Cria um botão para cada assento. O botão é configurado
            # com o texto do número do lugar,
            # a cor determinada pelo status do assento (reservado ou livre), e uma
            # ação associada ao clique que executa a função 'manipular_click'.
            # Esta função manipula o comportamento do botão dependendo do
            # estado do assento (reservado ou não).
            botao = tk.Button(

                # Especifica o frame dentro do canvas onde o botão será adicionado.
                self.canvas_frame,

                # Configura o texto do botão para indicar o número do lugar,
                # incrementando i por 1 para corresponder à contagem humana.
                text=f"Lugar {i + 1}",

                # Define a cor de fundo do botão baseado na variável 'cor', que é
                # amarela para assentos reservados e verde para livres.
                bg=cor,

                # Associa o botão à função 'manipular_click', que será chamada
                # quando o botão for clicado.
                command=manipular_click,

                # Define a fonte do texto do botão como Arial, tamanho 14, em negrito.
                font=("Arial", 14, "bold"),

                # Define a altura do botão como 1, adequado para a visualização do texto.
                height=1,

                # Define a largura do botão como 30, suficiente para exibir o
                # texto do lugar confortavelmente.
                width=30

            )

            # Organiza os botões em um grid de duas colunas dentro do frame especificado.
            # Isso permite uma apresentação organizada dos lugares em pares.
            # A organização em grid é escolhida para simular a disposição física dos
            # assentos em um ônibus, facilitando a visualização pelo usuário.
            # Calcula a linha para o botão baseado no índice do assento.
            # A divisão inteira por 2 agrupa os lugares em pares.
            row = i // 2

            # Calcula a coluna (0 ou 1) para alternar os botões entre esquerda e
            # direita, mantendo a simetria do layout de assentos.
            column = i % 2

            # Posiciona o botão criado anteriormente dentro do grid layout do 'canvas_frame'.
            # 'row=row' define em qual linha do grid o botão será colocado. O valor de 'row' é
            # calculado com base no índice do assento,
            # permitindo uma distribuição equilibrada dos botões em várias linhas,
            # dependendo do número total de assentos.
            # 'column=column' define em qual coluna do grid o botão será colocado.
            # O valor de 'column' alterna entre 0 e 1,
            # permitindo que os botões sejam organizados em duas colunas, o que ajuda a
            # simular a disposição física dos assentos em um ônibus.
            # 'padx=10' e 'pady=5' adicionam um espaçamento externo de 10 pixels na
            # horizontal e 5 pixels na vertical entre o botão e outros elementos do grid.
            # Isso ajuda a evitar que os botões fiquem visualmente amontoados e
            # melhora a estética geral da interface.
            # 'sticky="nsew"' é uma opção de configuração que faz o botão expandir
            # para preencher todo o espaço disponível na célula do grid.
            # As letras 'n', 's', 'e', 'w' representam norte, sul, leste e oeste,
            # respectivamente, indicando que o botão deve se expandir
            # em todas as direções para ocupar completamente sua célula no
            # grid, assegurando que o layout seja responsivo e visualmente coerente.
            botao.grid(row=row,
                       column=column,
                       padx=10,
                       pady=5,
                       sticky="nsew")  # Expande na horizontal

            # Configura as propriedades de expansão das colunas dentro do frame 'canvas_frame'.
            # Isso é necessário para garantir que ambos os lados do grid (esquerda e
            # direita) expandam uniformemente ao redimensionar a janela.
            self.canvas_frame.grid_columnconfigure(0, weight=1)  # Atribui um 'peso' de 1 à coluna da esquerda.
            self.canvas_frame.grid_columnconfigure(1, weight=1)  # Atribui um 'peso' de 1 à coluna da direita.

            # Estas configurações asseguram que ambas as colunas tenham a mesma capacidade de
            # expansão e que o layout responda bem a mudanças no tamanho da janela.

            # Atualiza as tarefas pendentes de layout do Canvas.
            # Isso é importante para garantir que todos os elementos gráficos sejam
            # corretamente dimensionados e posicionados antes de realizar mais configurações.
            self.canvas.update_idletasks()

            # Configura a região de rolagem do Canvas para englobar toda a
            # área onde os botões são desenhados.
            # 'self.canvas.bbox("all")' calcula a caixa de delimitação que
            # contém todos os elementos no Canvas,
            # garantindo que a barra de rolagem permita visualizar todos os
            # elementos ao mover-se verticalmente.
            self.canvas.config(scrollregion=self.canvas.bbox("all"))


    # Define o método 'abrir_cadastro' usado para abrir uma janela de
    # cadastro de novas reservas.
    def abrir_cadastro(self):

        # Obtém a data atualmente selecionada no calendário pelo usuário. Este valor
        # será usado para predefinir a data na janela de cadastro.
        data_selecionada = self.cal.get_date()

        # Cria uma nova instância da classe 'JanelaCadastro'. Esta classe é uma janela
        # que permite ao usuário cadastrar uma nova reserva.
        # 'self.janela_sistema' passa a janela principal como parâmetro para que a
        # janela de cadastro possa ser aberta dentro do contexto da aplicação principal.
        # 'self.onibus' passa a instância do ônibus para permitir que a janela de
        # cadastro interaja com os dados das reservas.
        # 'self' passa a instância atual da classe JanelaPrincipal para permitir
        # chamadas de volta para métodos desta classe.
        # 'data_selecionada' é usada para configurar automaticamente a data da
        # reserva na nova janela de cadastro.
        JanelaCadastro(self.janela_sistema,
                       self.onibus,
                       self,
                       data_selecionada)

    # Define o método 'abrir_pesquisa' usado para abrir uma janela de
    # pesquisa de reservas históricas.
    def abrir_pesquisa(self):

        # Cria uma nova instância da classe 'JanelaPesquisa'. Esta classe é uma
        # janela que permite ao usuário pesquisar reservas passadas.
        # 'self.janela_sistema' passa a janela principal como parâmetro para
        # que a janela de pesquisa possa ser aberta dentro do contexto da
        # aplicação principal.
        # 'self.onibus' passa a instância do ônibus para permitir que a
        # janela de pesquisa interaja com os dados das reservas.
        # 'self' passa a instância atual da classe JanelaPrincipal para permitir
        # chamadas de volta para métodos desta classe.
        JanelaPesquisa(self.janela_sistema,
                       self.onibus,
                       self)


# 'tk.Tk()' inicializa a janela principal da interface gráfica.
# Cria a janela principal da aplicação usando Tkinter.
janela_sistema = tk.Tk()

# Cria uma instância da classe 'Onibus', que gerencia os dados
        # relacionados ao ônibus e suas reservas.
# 'Onibus(20)' inicializa o objeto do ônibus com uma
        # capacidade de 20 lugares.
onibus = Onibus(20)

# Cria a interface principal da aplicação, associando a janela do
        # sistema e o objeto do ônibus.
# 'JanelaPrincipal(janela_sistema, onibus)' cria a interface
        # gráfica principal da aplicação.
# Passa a janela Tk ('janela_sistema') para exibir a interface e o
        # objeto 'onibus' para gerenciar as operações relacionadas às reservas.
app = JanelaPrincipal(janela_sistema, onibus)

# Inicia o loop principal da interface gráfica.
# 'mainloop()' é um método Tkinter que entra em um loop
        # contínuo para processar eventos.
janela_sistema.mainloop()