import random
import pandas as pd
import os
from dotenv import load_dotenv

def infos():
    load_dotenv()
    caminho = os.getenv("CAMINHO")
    dados= pd.read_excel(caminho)

    dicionario_dados = dados.to_dict(orient="records")
    n = random.randint(0, len(dicionario_dados) - 1)
    dia= dicionario_dados[n]
    print(dia)

    dados_de_exemplo = {
        "inversor_status": "Operando Normalmente",
        "bateria_carga": f"{dia['SOC(%)']}%" ,
        "producao_solar_watts": dia['FV(W)'],
        "consumo_casa_watts": dia['Carga(W)']
    }

    # dados_de_exemplo = {
    #     "inversor_status": "Operando Normalmente",
    #     "bateria_carga": "85%",
    #     "producao_solar_watts": 1500,
    #     "consumo_casa_watts": 450
    # }

    return dados_de_exemplo