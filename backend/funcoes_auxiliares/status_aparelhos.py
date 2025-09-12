# Arquivo: backend/funcoes_auxiliares/status_aparelhos.py

def infos():
    """
    Esta função busca os dados dos aparelhos.
    Por enquanto, ela retorna dados de exemplo.
    No futuro, você pode colocar aqui a lógica real para ler os dados do seu inversor/bateria.
    """
    dados_de_exemplo = {
        "inversor_status": "Operando Normalmente",
        "bateria_carga": "85%",
        "producao_solar_watts": 1500,
        "consumo_casa_watts": 450
    }
    return dados_de_exemplo