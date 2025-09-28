from funcoes_auxiliares.funcs_auxiliares import ler_cargas
from funcoes_auxiliares.status_aparelhos import infos
import json
import os
from dotenv import load_dotenv

load_dotenv()
caminho_status = os.getenv("CARGAS")

CONSUMO_PADRAO = {
    "Computador": 150,
    "Geladeira": 300,
    "Televisão": 175,
    "Ar Condicionado": 1200,
    "Air Fryer": 1500,
    "Ventilador": 70,
    "Lâmpada LED": 10,
    "Cafeteira": 800
}

def ligar_cargas_prioritarias():
    try:
        with open(caminho_status, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        status = {"cargas_prioritarias_ativas": False}
    status['cargas_prioritarias_ativas'] = True
    with open(caminho_status, 'w') as f:
        json.dump(status, f, indent=2)
    return status

def desligar_cargas_prioritarias():
    with open(caminho_status, 'r+') as f:
        status = json.load(f)
        status['cargas_prioritarias_ativas'] = False
        f.seek(0)
        json.dump(status, f, indent=2)

def verificar_status_cargas():
    try:
        with open(caminho_status, 'r') as f:
            status = json.load(f)
            return status.get('cargas_prioritarias_ativas', False)
    except FileNotFoundError:
        return False

def consumo_aparelhos():
    if not verificar_status_cargas():
        return {'Cargas prioritárias desligadas.'}
    else:
        cargas_prioritarias = ler_cargas()
        consumo_individual = {}
        consumo_total_cargas = 0

        for nome_aparelho in cargas_prioritarias.values():
            consumo_w = CONSUMO_PADRAO.get(nome_aparelho, 0)
            consumo_individual[f'Consumo {nome_aparelho}'] = f'{consumo_w}'
            consumo_total_cargas += consumo_w

        return {
            'consumo_de_cada_aparelho': consumo_individual,
            'consumo_total_das_cargas': consumo_total_cargas
        }

def info_consumo():
    if not verificar_status_cargas():
        return {'duracao': 'Cargas prioritárias desligadas.'}
    else:
        dados_consumo = consumo_aparelhos()
        consumo_cargas = dados_consumo.get('consumo_total_das_cargas', 0)

        if consumo_cargas == 0:
            return {'duracao': 'Sem consumo, a bateria dura indefinidamente.'}

        # Capacidade de Armazenamento nominal da bateria: 5400 Wh
        duracao_bateria = 5400 / consumo_cargas
        
        return {'duracao': f'Caso acabe a luz, sua bateria conseguirá abastecer suas cargas por {int(duracao_bateria)}h.'}