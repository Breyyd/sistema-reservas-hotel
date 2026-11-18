"""
models.py - POO do sistema
Aqui ficam as classes do hotel (cliente, quarto (e os tipos), reserva e hotel)
Ficam também as excessões do sistema.
"""

from datetime import date

class ReservaError(Exception):
    """Erro genérico do sistema de reservas."""

class DataInvalidaError(ReservaError):
    """Lança quando não tem sentido no momento da reserva."""

class QuartoIndisponivelError(ReservaError):
    """Lança quando o quarto já está reservado no período citado."""

class CadastroError(ReservaError):
    """Lança quando o cadastrado é repetido/não encontrado."""

# --- Cliente --- #
class Cliente:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def para_dict(self):
        """Converte em dicionário para salvar em JSON"""
        return{"nome": self.nome, "cpf": self.cpf, "telefone": self.telefone}

    def __str__(self):
        return f"{self.nome} (CPF:{self.cpf}, Tel: {self.telefone})"

# --- Quarto e seus tipos (Herança e Polimorfismo, visto em aula) --- # 
class Quarto:
    """Classe principal(base). Os tipos de quarto herdam dela."""

    tipo = "Padrão"
    capacidade = 1

    def __init__(self, numero, diaria):
        self.numero = numero
        self.diaria = diaria

    def calcular_preco(self, noites):
        """Preço padrão: diária x número de noites."""
        return self.diaria * noites

    def para_dict(self):
        return {"numero": self.numero, "tipo": self.tipo, "diaria": self.diaria}

    def __str__(self):
        # self.tipo e self.capacidade mudam de acordo com a sublasse (baseado no polimorfismo)
        return (f"Quarto {self.numero} - {self.tipo} "
                f"({self.capacidade} pessoa(s)) - R$ {self.diaria:.2f}/noite")


class QuartoSolteiro(Quarto):
    tipo = "Solteiro"
    capacidade = 1


class QuartoCasal(Quarto):
    tipo = "Casal"
    capacidade = 2

class Suite(Quarto):
    tipo = "Suíte"
    capacidade = 4
    TAXA_SERVICO = 0.10 # adiciona 10% a mais sobre diárias

    def calcular_preco(self, noites):
        """Sobrescreve a classe base: somando a taxa de serviço."""
        preco_base = super().calcular_preco(noites)
        return preco_base * (1 + self.TAXA_SERVICO)

# Dicionário para recriar tipo de quarto a partir do texto
TIPOS_DE_QUARTO = {
    "Solteiro": QuartoSolteiro,
    "Casal": QuartoCasal,
    "Suíte": Suite,
}


# --- Reserva --- #
class Reserva:
    def __init__(self, codigo, cliente, quarto, entrada, saida, ativa=True):
        if saida <= entrada:
            raise DataInvalidaError("A data de saída deve ser depois da data de entrada!")
        self.codigo = codigo
        self.cliente = cliente
        self.quarto = quarto
        self.entrada = entrada
        self.saida = saida
        self.ativa = ativa

    def noites(self):
        return (self.saida - self.entrada).days

    def total(self):
        # Nao importa o tipo de quarto (polimorfismo)
        return self.quarto.calcular_preco(self.noites())

    def conflito_com(self, entrada, saida):
        """Verdadeiro se o periodo informado sobrepoe o dessa reserva"""
        return self.ativa and entrada < self.saida and self.entrada < saida

    def cancelar(self):
        self.ativa = False

    def para_dict(self):
        return {
            "codigo": self.codigo,
            "cpf_cliente": self.cliente.cpf,
            "numero_quarto": self.quarto.numero,
            "entrada": self.entrada.isoformat(),
            "saida": self.saida.isoformat(),
            "ativa": self.ativa,
        }

    def __str__(self):
        situacao = "ATIVA" if self.ativa else "CANCELADA"
        return (f"#{self.codigo} [{situacao}] {self.cliente.nome} - "
                f"Quarto {self.quarto.numero} ({self.quarto.tipo}) - "
                f"{self.entrada.strftime('%d/%m/%Y')} a {self.saida.strftime('%d/%m/%Y')} - "
                f"{self.noites()} noites(s) - Total: R$ {self.total():.2f}")



# --- Hotel: guardar listas e aplicar as regras --- #
class Hotel:
    def __init__(self, nome):
        self.nome = nome
        self.clientes = []
        self.quartos = []
        self.reservas = []

# --- clientes --- #
def buscar_cliente(self, cpf):
    for cliente in self.clientes:
        if cliente.cpf == cpf:
            return cliente
    raise CadastroError(f"Nenhum cliente com CPF {cpf}.")

def cadastrar_cliente(self, cliente):
    if any(c.cpf == cliente.cpf for c in self.clientes):
        raise CadastroError(f"Já existe um cliente com CPF {cliente.cpf}.")
    self.clientes.append(cliente)


# --- quartos --- #
def buscar_quarto(self, numero):
    for quarto in self.quartos:
        if quarto.numero == numero:
            return quarto
    raise CadastroError(f"Quarto {numero} não existe.")

def cadastrar_quarto(self, quarto):
    if any(q.numero == quarto.numero for q in self.quartos):
        raise CadastroError(f"O quarto {quarto.numero} já está cadastrado.")
    self.quartos.append(quarto)

def quarto_disponivel(self, quarto, entrada, saida):
    for reserva in self.reservas:
        if reserva.quarto is quarto and reserva.conflita_com(entrada, saida):
            return False
    return True

def quartos_disponiveis(self, entrada, saida):
    return [q for q in self.quartos if self.quarto_disponivel(q, entrada, saida)]

# --- reservas ---
def proximo_codigo(self):
    if not self.reservas:
        return 1
    return max(r.codigo for r in self.reservas) + 1

def validar_periodo(self, entrada, saida):
    if entrada < date.today():
        raise DataInvalidaError("Não é possível reservar para uma data que já passou!")
    if saida <= entrada:
        raise DataInvalidaError("A data de saída deve ser depois da data de entrada")

def fazer_reserva(self, cpf, numero_quarto, entrada, saida):
    self.validar_periodo(entrada, saida)
    cliente = self.buscar_cliente(cpf)
    quarto = self.buscar_quarto(numero_quarto)
    if not self.quarto_disponivel(quarto, entrada, saida):
        raise QuartoIndisponivelError(
            f"O quarto {numero_quarto} já está reservado nesse período.")
    reserva = Reserva(self.proximo_codigo(), cliente, quarto, entrada, saida)
    self.reservas.append(reserva)
    return reserva

def buscar_reserva(self, codigo):
    for reserva in self.reservas:
        if reserva.codigo == codigo:
            return reserva
    raise CadastroError (f"Reserva #{codigo} não encontrada.")

def cancelar_reserva(self, codigo):
    reserva = self.buscar_reserva(codigo)
    if not reserva.ativa:
        raise ReservaError(f"A reserva #{codigo} já estava cancelada.")
    reserva.cancelar()
    return reserva