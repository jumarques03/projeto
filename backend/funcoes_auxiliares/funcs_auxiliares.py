from fastapi.responses import JSONResponse
import json
import random
import os
from dotenv import load_dotenv
import requests

caminho_arquivo = "dados/cargas_prioritarias.json"

def corpo_resposta_para_Alexa(texto, acabar_sessao):
    resposta = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": texto
                },
                "shouldEndSession": acabar_sessao
            }
        }
    
    return JSONResponse(content=resposta)

def resposta_erro_padrao(e):
    print(e)
    return corpo_resposta_para_Alexa("Desculpe, houve um problema ao processar sua solicitação.", True)

def ler_cargas():
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)
    
def salvar_cargas_prioritarias(lista):
    with open(caminho_arquivo, 'w', encoding="utf-8") as f:
        json.dump(lista, f, indent=4)

def reorganizar_indices(cargas):
    novas_cargas = {}
    for i, dispositivo in enumerate(cargas.values(), start=1):
        novas_cargas[i] = dispositivo
    return novas_cargas

def acesso_cargas(cargas):
    separador = ", "
    string_final_cargas = separador.join(cargas.values())
    return string_final_cargas

def dicas():
    dicas= [
        "Concentre o uso de aparelhos de alto consumo entre 10h e 15h para otimizar o uso da energia solar. Isso ajuda a reduzir o consumo da rede e aproveita melhor a energia gerada durante o dia.",
        "Programe eletrodomésticos inteligentes para funcionarem no pico solar e evitar o consumo da rede. Assim você economiza energia e mantém a bateria carregada.",
        "Use ar-condicionado e forno elétrico durante o dia para maximizar o uso da energia solar gerada, reduzindo a necessidade de energia da rede à noite.",
        "Mantenha uma reserva mínima de 20% de energia na bateria para garantir energia para emergências ou uso noturno, evitando ficar sem energia quando mais precisar.",
        "Reduza o consumo noturno quando houver previsão de chuva, pois a geração solar será menor no dia seguinte, evitando descarregar a bateria rapidamente.",
        "Desligue completamente os aparelhos em stand-by para evitar o consumo fantasma que se acumula ao longo do tempo, economizando energia sem esforço.",
        "Use réguas com interruptor para desligar múltiplos eletrônicos facilmente e controlar o consumo de stand-by, facilitando a economia diária.",
        "Prefira iluminação LED à noite, pois LEDs são mais eficientes e reduzem o consumo noturno sem comprometer o conforto.",
        "Evite usar aparelhos de alto consumo à noite para diminuir a necessidade de consumir energia da rede nos horários mais caros, economizando na conta.",
        "Mantenha os painéis solares limpos, pois a sujeira pode diminuir significativamente a produção de energia, garantindo eficiência máxima.",
        "Monitore a produção de energia pelo aplicativo do inversor para identificar problemas no sistema ou otimizar seu consumo de forma contínua.",
        "Fique atento a quedas inesperadas na geração solar, pois pode ser um sinal de falha no painel ou no inversor, evitando desperdício de energia.",
        "Use a energia da bateria nos horários de tarifa mais cara para reduzir custos, evitando o consumo da rede quando o preço é mais alto.",
        "Use aparelhos durante o dia para liberar energia para a bateria, mantendo-a carregada para uso noturno e garantindo autonomia.",
        "Configure o sistema conforme sua rotina e tarifas para adaptar a energia ao seu estilo de vida e ao valor da energia na sua região, otimizando economia.",
        "Concentre tarefas de alto consumo entre 11h e 14h, o período de maior geração solar, ideal para usar a energia produzida sem gastar da rede.",
        "Evite air fryer e grill à noite, preferindo micro-ondas, pois aparelhos de aquecimento impactam a bateria e a rede noturna.",
        "Diminua o brilho de TVs e monitores à noite, pois isso reduz o consumo de forma sutil, mas consistente, ajudando na economia diária.",
        "Revise as configurações do sistema a cada estação, pois o clima e o ângulo do sol mudam, exigindo ajustes para otimizar a eficiência energética.",
        "Instale baterias em locais ventilados e protegidos do sol para manter o desempenho e a vida útil delas por mais tempo.",
        "Compare sua geração com a de vizinhos para detectar problemas, o que pode ajudar a identificar falhas no seu sistema rapidamente.",
        "Evite deixar carregadores conectados sem uso, pois eles também consomem energia em stand-by sem necessidade.",
        "Use sensores de presença para iluminação automática e garantir que as luzes só fiquem ligadas quando há alguém no ambiente.",
        "Instale tomadas inteligentes para monitorar o consumo, permitindo o controle de aparelhos específicos e maior economia.",
        "Configure alertas de consumo excessivo para receber avisos quando o consumo atingir níveis indesejados, evitando desperdícios.",
        "Controle dispositivos por voz com assistente virtual para aumentar a conveniência e o controle sobre o consumo de energia.",
        "Escolha eletrodomésticos com selo de eficiência energética, pois aparelhos mais eficientes consomem menos energia a longo prazo.",
        "Crie rotinas de desligamento por horário para automatizar o desligamento de aparelhos, garantindo economia sem precisar lembrar.",
        "Use cortinas térmicas para reduzir a necessidade de ar-condicionado e aquecedores, diminuindo o consumo sem perder conforto.",
        "Aproveite a ventilação cruzada para manter a casa fresca e economizar energia, evitando o uso do ar-condicionado.",
        "Realize auditorias energéticas periódicas para identificar áreas de desperdício e encontrar novas formas de economizar energia."
        ]
 
    n = random.randint(0, len(dicas) - 1)
    return dicas[n]

def obter_clima(cidade: str):
    load_dotenv()
    chave_api = os.getenv("API_KEY")

    url = f"https://api.hgbrasil.com/weather?key={chave_api}&city_name={cidade}"
    resposta = requests.get(url).json()

    forecast_list = resposta['results']['forecast']

    previsao_proximos_dias = []
    for dia_previsao in forecast_list[1:4]:
        previsao_proximos_dias.append({
            "dia_semana": dia_previsao['weekday'],
            "data": dia_previsao['date'],
            "max": f"{dia_previsao['max']}°",
            "min": f"{dia_previsao['min']}°",
            "descricao": dia_previsao['description']
        })
    
    clima = {
        "localizacao": resposta['results']['city'],
        "periodo_do_dia": resposta['results']['currently'],
        "descricao": forecast_list[0]['description'],
        "dia": forecast_list[0]['date'],
        "temperatura_maxima": f"{forecast_list[0]['max']}°C",
        "temperatura_minima": f"{forecast_list[0]['min']}°C",
        "preciptacao_total_(mm)": f"{forecast_list[0]['rain']}mm",
        "cobertura_de_nuvens(%)": f"{forecast_list[0]['cloudiness']}%",
        "chance_de_chuva(%)": f"{forecast_list[0]['rain_probability']}%",
        "previsao_proximos_dias": previsao_proximos_dias 
    }

    return clima