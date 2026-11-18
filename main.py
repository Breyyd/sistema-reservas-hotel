"""
main.py - menu e interação com o usuário.
 
"""
 
from datetime import datetime
 
from models import Cliente, TIPOS_DE_QUARTO, ReservaError
from dados import salvar_dados, carregar_dados
  
# ---- Funções de leitura com validação ---- #

def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Este campo não pode ficar vazio.")
 
 
def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro.")
 
 
def ler_decimal(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor > 0:
                return valor
            print("O valor deve ser maior que zero.")
        except ValueError:
            print("Digite um número válido (ex.: 150.00).")
 
 
def ler_data(mensagem):
    while True:
        try:
            return datetime.strptime(input(mensagem), "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA.")
 
 
# ---- Funções de cada opção do menu ---- # 

def cadastrar_cliente(hotel):
    print("\n--- Cadastro de cliente ---")
    nome = ler_texto("Nome: ")
    cpf = ler_texto("CPF (só números): ")
    telefone = ler_texto("Telefone: ")
    hotel.cadastrar_cliente(Cliente(nome, cpf, telefone))
    print("Cliente cadastrado com sucesso!")
 
 
def cadastrar_quarto(hotel):
    print("\n--- Cadastro de quarto ---")
    tipos = list(TIPOS_DE_QUARTO)
    for i, tipo in enumerate(tipos, start=1):
        print(f"{i} - {tipo}")
    escolha = ler_inteiro("Tipo do quarto: ")
    if escolha < 1 or escolha > len(tipos):
        print("Tipo inválido.")
        return
    classe = TIPOS_DE_QUARTO[tipos[escolha - 1]]
    numero = ler_inteiro("Número do quarto: ")
    diaria = ler_decimal("Valor da diária (R$): ")
    hotel.cadastrar_quarto(classe(numero, diaria))
    print("Quarto cadastrado com sucesso!")
 
 
def listar(titulo, itens):
    print(f"\n--- {titulo} ---")
    if not itens:
        print("Nenhum registro.")
    for item in itens:
        print(item)
 
 
def fazer_reserva(hotel):
    print("\n--- Nova reserva ---")
    cpf = ler_texto("CPF do cliente: ")
    cliente = hotel.buscar_cliente(cpf)  # lança CadastroError se não existir
    print(f"Cliente: {cliente.nome}")
    entrada = ler_data("Data de entrada (DD/MM/AAAA): ")
    saida = ler_data("Data de saída (DD/MM/AAAA): ")
    hotel.validar_periodo(entrada, saida)  # lança DataInvalidaError se for inválido
 
    disponiveis = hotel.quartos_disponiveis(entrada, saida)
    if not disponiveis:
        print("Nenhum quarto disponível nesse período.")
        return
    listar("Quartos disponíveis no período", disponiveis)
    numero = ler_inteiro("Número do quarto escolhido: ")
    reserva = hotel.fazer_reserva(cpf, numero, entrada, saida)
    print("Reserva realizada!")
    print(reserva)
 
 
def cancelar_reserva(hotel):
    print("\n--- Cancelar reserva ---")
    codigo = ler_inteiro("Código da reserva: ")
    reserva = hotel.cancelar_reserva(codigo)
    print(f"Reserva #{reserva.codigo} cancelada.")
 
 
def exibir_menu():
    print("\n========== HOTEL BOA ESTADIA ==========")
    print("1 - Cadastrar cliente")
    print("2 - Cadastrar quarto")
    print("3 - Listar clientes")
    print("4 - Listar quartos")
    print("5 - Fazer reserva")
    print("6 - Listar reservas")
    print("7 - Cancelar reserva")
    print("0 - Sair")
 
 

# ---- Parte principall do programa ---- #

def main():
    hotel = carregar_dados("Hotel Boa Estadia")
 
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
 
        try:
            if opcao == "1":
                cadastrar_cliente(hotel)
            elif opcao == "2":
                cadastrar_quarto(hotel)
            elif opcao == "3":
                listar("Clientes", hotel.clientes)
            elif opcao == "4":
                listar("Quartos", hotel.quartos)
            elif opcao == "5":
                fazer_reserva(hotel)
            elif opcao == "6":
                listar("Reservas", hotel.reservas)
            elif opcao == "7":
                cancelar_reserva(hotel)
            elif opcao == "0":
                salvar_dados(hotel)
                print("Dados salvos. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
                continue
            salvar_dados(hotel)  # salva depois de cada operação
        except ReservaError as erro:  # captura todas as exceções
            print(f"Erro: {erro}")
 
 
if __name__ == "__main__":
    main()
 