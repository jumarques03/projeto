from funcoes_auxiliares.funcs_auxiliares import ler_cargas
from funcoes_auxiliares.status_aparelhos import infos
import json
import os
from dotenv import load_dotenv

load_dotenv()
caminho = os.getenv("CARGAS")

def ligar_cargas_prioritarias():
    try:
        with open(caminho, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):

        status = {"cargas_prioritarias_ativas": False}

    status['cargas_prioritarias_ativas'] = True

    with open(caminho, 'w') as f:
        json.dump(status, f, indent=2)

def desligar_cargas_prioritarias():
    with open(caminho, 'r+') as f:
        status = json.load(f)
        status['cargas_prioritarias_ativas'] = False
        f.seek(0)
        json.dump(status, f, indent=2)

def verificar_status_cargas():
    try:
        with open(caminho, 'r') as f:
            status = json.load(f)
            return status['cargas_prioritarias_ativas']
    except FileNotFoundError:
        return False

def consumo_aparelhos():
    if not verificar_status_cargas():
        return {'Cargas prioritárias desligadas.'}
    else:
        cargas = ler_cargas()
        
        # Tentar pegar esses valores de algum lugar 
        computador_consumo  = 150
        # geladeira_consumo  = 300
        televisao_consumo  = 175

        consumo =  {
            f'Consumo {cargas["1"]}' : f'{computador_consumo}',
            # f'Consumo {cargas["2"]}' : f'{geladeira_consumo}',
            f'Consumo {cargas["3"]}' : f'{televisao_consumo}'
        }

        consumo_total_cargas = computador_consumo  + televisao_consumo

        return {'consumo_de_cada_aparelho' : consumo, 'consumo_total_das_cargas' : consumo_total_cargas}

def info_consumo():
    if not verificar_status_cargas():
        return {'Cargas prioritárias desligadas.'} 
    else:
        consumo = consumo_aparelhos()
        consumo_residencia = infos()
        consumo_cargas = consumo['consumo_total_das_cargas'] 
        porcentagem_equivalente_consumo_total = (consumo_cargas / consumo_residencia['consumo_casa_watts'] ) * 100

        # Capacidade de Armazenamento nominal da bateria Lynx U G3: 5.4 kWh = 5400 Wh
        duracao_bateria  = (5400)/consumo_cargas

        return {f'O consumo de suas cargas prioritárias equivale a {porcentagem_equivalente_consumo_total:.2f}% do consumo total da residência.',
                f'Caso acabe a luz, sua bateria conseguirá abastecer suas cargas por {int(duracao_bateria)}h.'}