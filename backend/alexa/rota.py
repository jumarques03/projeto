from fastapi import APIRouter, Request
from funcoes_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao, ler_cargas, acesso_cargas, dicas, obter_clima
from funcoes_auxiliares.status_aparelhos import infos
from funcoes_auxiliares.cargas_prioritarias import ligar_cargas_prioritarias, desligar_cargas_prioritarias, info_consumo
rota_alexa = APIRouter(prefix="/alexa")

@rota_alexa.post("/")
async def alexa_webhook(request: Request):
    try:
        corpo_intent = await request.json()
        tipo_request = corpo_intent["request"]["type"]

        if tipo_request == "LaunchRequest":
            texto_resposta = (
                "Bem-vindo ao SmartSolarGrid!   "
                "Você pode pedir o status de seus aparelhos de energia,  "
                " saber o clima de sua cidade,   "
                " a dica do dia sobre energia,  ligar,    desligar e saber suas cargas prioritárias."
            )

        elif tipo_request == "IntentRequest":
            intent_nome = corpo_intent["request"]["intent"]["name"]

            if intent_nome == "StatusAparelhosDeEnergiaIntent":
                infos_aparelhos = infos()
                texto_resposta = (
                    f"Seu painel solar está gerando {infos_aparelhos['producao_solar_watts']} Watts, "
                    f" o nível de sua bateria é {infos_aparelhos['bateria_carga']}"
                    f" e sua rede está consumindo no total {infos_aparelhos['consumo_casa_watts']} Watts."
                )

            elif intent_nome == "DicaIntent":
                dica = dicas()
                texto_resposta = f"Sua dica é: {dica}" 

            elif intent_nome == "LigarCargasIntent":
                ligar_cargas_prioritarias()
                informacoes_consumo = info_consumo()
                texto_resposta = f"Ok, as cargas prioritárias foram ligadas." + f"{informacoes_consumo['duracao']}"

            elif intent_nome == "DesligarCargasIntent":
                desligar_cargas_prioritarias()
                texto_resposta = "Ok, as cargas prioritárias foram desligadas."

            elif intent_nome == "SaberCargasPrioritariasIntent":
                cargas = ler_cargas()
                texto_resposta = f"Suas cargas prioritárias são: {acesso_cargas(cargas)}"
            
            elif intent_nome == "ClimaIntent":
                try:
                    cidade = corpo_intent["request"]["intent"]["slots"]["cidade"]["value"]
                    clima = obter_clima(cidade)
                    
                    texto_resposta = (
                        f"Em {clima['localizacao']},"
                        f"A descrição do clima é de {clima['descricao']}. "
                        f"A temperatura máxima será de {clima['temperatura_maxima']} "
                        f"e a mínima de {clima['temperatura_minima']}. "
                        f"A chance de chuva é de {clima.get('chance_de_chuva(%)', 'não disponível')}"
                        f" e as nuvens cobrirão {clima['cobertura_de_nuvens(%)']} do céu."
                    )

                except KeyError:
                    texto_resposta = "Por favor, me diga o nome da cidade que deseja consultar."

            else:
                texto_resposta = "Desculpe, não entendi sua solicitação! Poderia repetir, por favor?"


        elif tipo_request == "SessionEndedRequest":
            texto_resposta = "Até logo! Obrigado por usar o SmartSolarGrid."

        else:
            texto_resposta = "Desculpe, ocorreu um problema ao processar sua solicitação."

        resposta = corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta

    except Exception as e:
        return resposta_erro_padrao(e)