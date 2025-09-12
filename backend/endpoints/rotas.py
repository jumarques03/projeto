from graficos.graficos import serie_temporal, histograma, obter_producao_hoje # <-- Adicione obter_producao_hoje
from fastapi import APIRouter
from funcoes_auxiliares.status_aparelhos import infos
from funcoes_auxiliares.funcs_auxiliares import ler_cargas, salvar_cargas_prioritarias, reorganizar_indices, obter_clima
from graficos.graficos import serie_temporal, histograma
from ia.llm import assistente_llm_site
from pydantic import BaseModel

class CargaPayload(BaseModel):
    dispositivo: str

class PerguntaPayload(BaseModel): 
    pergunta: str

rota_site= APIRouter(prefix="/site")

@rota_site.get("/producao_hoje")
async def producao_hoje():
    return obter_producao_hoje()

@rota_site.get("/status_aparelhos")
async def status_aparelhos():
    try:
        return infos()
    except:
        return {"mensagem":"Não foi possível obter as informações sobre seu inversor e bateria."}

@rota_site.post("/escolher_cargas_prioritarias")
async def escolher_carga_prioritaria(payload: CargaPayload):
    try:
        cargas = ler_cargas()
        novo_id = str(len(cargas) + 1)
        cargas[novo_id] = payload.dispositivo 
        salvar_cargas_prioritarias(cargas)
        return {"mensagem": "Carga prioritária registrada com sucesso!"}
    except Exception as e:
        print(f"Erro ao salvar carga: {e}")
        return {"mensagem":"Não foi possível registrar sua carga prioritária."}
        
@rota_site.get("/lista_cargas_prioritarias")
async def listar_cargas_prioritarias():
    try:
        cargas = ler_cargas()
        return {"cargas_prioritarias": cargas}
    except: 
        return {"mensagem":"Não foi possível acessar sua lista de cargas prioritárias."}

@rota_site.delete("/remover_carga_prioritaria")
async def remover_carga_prioritaria(carga_id: str):
    try:
        cargas = ler_cargas()
        if carga_id in cargas:
            carga_removida = cargas.pop(carga_id)
            cargas = reorganizar_indices(cargas)
            salvar_cargas_prioritarias(cargas)
            return {"mensagem": f"Carga '{carga_removida}' removida com sucesso!"}
        else:
            return {"erro": "ID da carga não encontrado."}
    except:
        return {"mensagem":"Não foi possível deletar sua carga prioritária."}


@rota_site.get("/geracao_solar")
async def obter_geracao_solar():
    try: 
        cor = '#8fc34d' 
        return serie_temporal('FV(W)', cor, 'Geração Solar(W)', 'Dia', 'Watts')
    except:
        return {"mensagem":"Não foi possível carregar o gráfico!"}

@rota_site.get("/energia_consumida_concessionaria")
async def obter_energia_concessionaria():
    try:
        cor = '#e74c3c' 
        return serie_temporal('Rede elétrica (W)', cor, 'Energia Comprada(W)', 'Dia', 'Watts')
    except:
        return {"mensagem":"Não foi possível carregar o gráfico!"}

@rota_site.get("/carga_consumida")
async def obter_carga_consumida(): 
    try:
        cor = '#12b4cf' 
        return serie_temporal('Carga(W)', cor, 'Consumo da Residência(W)', 'Dia', 'Watts')
    except:
        return {"mensagem":"Não foi possível carregar o gráfico!"}

@rota_site.get("/dados_bateria")
async def obter_dados_bateria():
    try:
        cor = '#f1c40f' 
        return serie_temporal('Dados da Bateria(W)', cor, 'Uso da Bateria(W)', 'Dia', 'Watts')
    except:
        return {"mensagem":"Não foi possível carregar o gráfico!"}

@rota_site.get("/nivel_bateria")
async def obter_nivel_bateria():
    try:
        return histograma('SOC(%)', 10, 'Nível de Bateria(%)', 'Porcentagem', 'Frequência')
    except:
        return {"mensagem":"Não foi possível carregar o gráfico!"}

@rota_site.post("/assistente")
async def chatbot(payload: PerguntaPayload):
    try:
        info_aparelhos = infos()
        pergunta_do_usuario = payload.pergunta
        dialogo = assistente_llm_site(info_aparelhos, pergunta_do_usuario)
        return dialogo
    except Exception as e:
        print(f"Erro no chatbot: {e}")
        return {"mensagem":"Desculpe não consegui processar sua pergunta. Tente novamente mais tarde!"}

@rota_site.get("/clima")
async def clima(local: str):
    try:
        clima = obter_clima(local)
        return clima
    except:
        return {"mensagem":"Não foi possível acessar as informações do clima de sua cidade."}