# backend/graficos/graficos.py
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
caminho = os.getenv("CAMINHO")

try:
    dados = pd.read_excel(caminho)
    df = pd.DataFrame(dados)
    df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")
    df = df.set_index('Horário')
    df2 = df.copy()
    df_diario = df.resample('D').sum()
except FileNotFoundError:
    print(f"!!!!!!!!!!!! ERRO CRÍTICO: O arquivo de dados em '{caminho}' não foi encontrado. !!!!!!!!!!!!")
    df_diario = pd.DataFrame()
    df2 = pd.DataFrame()


def serie_temporal(valor: str, cor: str, titulo: str, x: str, y: str):
    labels = df_diario.index.strftime('%d/%m').tolist()
    data_points = df_diario[valor].tolist()

    chart_config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": titulo,
                "data": data_points,
                "borderColor": cor,
                "backgroundColor": f"{cor}33",
                "fill": True,
                "tension": 0.4, 
                "pointBackgroundColor": cor 
            }]
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False, 
            "layout": {         
                "padding": 10     
            },
            "plugins": { "legend": { "display": False } }, 
            "scales": {
                "x": { "title": { "display": True, "text": x } },
                "y": { "title": { "display": True, "text": y } }
            }
        }
    }
    return chart_config


def histograma(valor: str, intervalo: int, titulo: str, x: str, y: str):
    print("\n--- INICIANDO DEBUG DO HISTOGRAMA ---")

    if valor not in df2.columns:
        print(f"AVISO: A coluna '{valor}' não foi encontrada.")
        return {"type": "bar", "data": {"labels": [], "datasets": []}, "options": {"plugins": {"title": {"display": True, "text": "Dados não encontrados"}}}}

    print(f"1. Dados Originais da Coluna '{valor}' (primeiros 10 valores):")
    print(df2[valor].head(10))

    dados_coluna = df2[valor].astype(str)
    dados_numericos_str = dados_coluna.str.extract(r'(\d+\.?\d*)', expand=False)
    dados_numericos = pd.to_numeric(dados_numericos_str, errors='coerce')
    dados_validos = dados_numericos.dropna()

    print(f"\n2. Dados da Coluna '{valor}' APÓS a limpeza (primeiros 10 valores):")
    print(dados_validos.head(10))
    print(f"Tipo de dados após limpeza: {dados_validos.dtype}")

    if dados_validos.empty:
        print("AVISO FINAL: A coluna está vazia após a limpeza. Não é possível gerar o histograma.")
        return {"type": "bar", "data": {"labels": [], "datasets": []}, "options": {"plugins": {"title": {"display": True, "text": "Sem dados válidos para exibir"}}}}

    try:
        print("\n3. TENTANDO calcular o histograma...")
        counts, bin_edges = np.histogram(dados_validos, bins=intervalo)
        print("Cálculo do histograma realizado com SUCESSO.")

    except Exception as e:
        print("\n!!!!!!!!!!!!!!!!! ERRO ENCONTRADO !!!!!!!!!!!!!!!!!")
        print("A função np.histogram falhou. O erro exato foi:")
        import traceback
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return {"type": "bar", "data": {"labels": [], "datasets": []}, "options": {"plugins": {"title": {"display": True, "text": "Erro ao processar dados"}}}}

    print("\n4. Montando o JSON de resposta.")
    labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)]
    
    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": f'Frequência de {valor}',
                "data": counts.tolist(),
                "backgroundColor": 'rgba(70, 193, 171, 0.5)', 
                "borderColor": 'rgba(70, 193, 171, 1)',
                "borderWidth": 1
            }]
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "layout": {          
                "padding": 10     
            },
            "plugins": { "legend": { "display": False }, "title": { "display": False, "text": titulo } },
            "scales": {
                "x": { "title": { "display": True, "text": x } },
                "y": { "title": { "display": True, "text": y }, "beginAtZero": True }
            }
        }
    }
    print("--- FIM DO DEBUG DO HISTOGRAMA ---\n")
    return chart_config


def obter_producao_hoje():
    try:
        producao_do_dia = df_diario['FV(W)'].iloc[-1]
        return {"producao_hoje": f"{producao_do_dia:.2f}"}
    except (IndexError, KeyError):
        return {"producao_hoje": "0.00"}