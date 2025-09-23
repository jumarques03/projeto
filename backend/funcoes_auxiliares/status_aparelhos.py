import random
import pandas as pd
import os
from dotenv import load_dotenv

def infos():
    load_dotenv()
    caminho = os.getenv("CAMINHO")
    dados= pd.read_excel(caminho)
    dicionario_dados = dados.to_dict(orient="records")

    valido = False
    while not valido:
        n = random.randint(0, len(dicionario_dados) - 1)
        if dicionario_dados[n]['FV(W)'] != 0 and dicionario_dados[n]['Carga(W)'] != 0.0:
            valido = True

    dia = dicionario_dados[n]
    print(dia)

    dados_de_exemplo = {
        "inversor_status": "Operando Normalmente",
        "bateria_carga": f"{dia['SOC(%)']}%",
        "producao_solar_watts": dia['FV(W)'],
        "consumo_casa_watts": dia['Carga(W)']
    }

    return dados_de_exemplo

