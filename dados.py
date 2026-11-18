"""
dados.py - salva e carrega os dados em arquivo .JSON,
pra nao perder nada quando o programa é fechado
"""

import json
import os
from datetime import date

from models import Hotel, Cliente, Reserva, TIPOS_DE_QUARTO

PASTA_DADOS = "dados"
ARQ_CLIENTES = os.path.join(PASTA_DADOS, "clientes.json")
ARQ_QUARTOS = os.path.join(PASTA_DADOS, "quartos.json")
ARQ_RESERVAS = os.path.join(PASTA_DADOS, "reservas.json")


def _salvar_json(caminho, lista):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, ensure_ascii=False, indent=2)


def _ler_json(caminho):
    """Lê um arquivo JSON. Se não existir ou estiver corrompido, ele devolve a lista vazia."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return [] # é uma primeira execuçao - entao o arquivo ainda nao existe.
    except json.JSONDecodeError:
        print(f"Aviso: o arquivo {caminho} está corrompido e foi ignorado.")
        return []


def salvar_dados(hotel):
    os.makedirs(PASTA_DADOS, exist_ok=True) # cria a pasta se nao existir
    _salvar_json(ARQ_CLIENTES, [c.para_dict() for c in hotel.clientes])
    _salvar_json(ARQ_QUARTOS, [q.para_dict() for q in hotel.quartos])
    _salvar_json(ARQ_RESERVAS, [r.para_dict() for r in hotel.reservas])


def carregar_dados(nome_hotel):
    hotel = Hotel(nome_hotel)

    for d in _ler_json(ARQ_CLIENTES):
        hotel.clientes.append(Cliente(d["nome"], d["cpf"], d["telefone"]))

    for d in _ler_json(ARQ_QUARTOS):
        classe = TIPOS_DE_QUARTO[d["tipo"]] # escolhe a subclasse certinha
        hotel.quartos.append(classe(d["numero"], d["diaria"]))

    for d in _ler_json(ARQ_RESERVAS):
        reserva = Reserva(
            d["codigo"],
            hotel.buscar_cliente(d["cpf_cliente"]),
            hotel.buscar_quarto(d["numero_quarto"]),
            date.fromisoformat(d["entrada"]),
            date.fromisoformat(d["saida"]),
            d["ativa"],
        )
        hotel.reservas.append(reserva)

    return hotel