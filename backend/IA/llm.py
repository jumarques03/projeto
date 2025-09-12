# Arquivo: backend/IA/llm.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json 
from IA.analise_dados import extrair_metricas


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=GOOGLE_API_KEY)


def assistente_llm_site(info: dict, pergunta: str):
    metricas = extrair_metricas()

    # Formata os dicionários como uma string JSON legível. A IA entende isso muito melhor.
    info_formatado = json.dumps(info, indent=2, ensure_ascii=False)
    metricas_formatado = json.dumps(metricas, indent=2, ensure_ascii=False)


    # --- ETAPA 2: Definir as Instruções (Prompt) ---

    # System prompt focado apenas na identidade e regras gerais da IA
    system_prompt = """
    Você é o SmartSolarGrid, um assistente virtual especialista em sistemas de energia solar.
    Sua personalidade é prestativa, técnica e objetiva.
    Responda sempre em português brasileiro, de forma coesa, coerente e em poucas palavras, sem usar markdown ou formatação especial.
    Baseie sua resposta estritamente nos dados de contexto fornecidos.
    Se a pergunta não puder ser respondida com o contexto, responda: "Desculpe, não possuo essa informação disponível! Posso te ajudar em outro assunto?"
    """

    # User prompt que combina os dados e a pergunta do usuário
    user_prompt = f"""
    ### CONTEXTO DO SISTEMA ###
    Aqui estão os dados e métricas atuais do sistema do usuário. Use-os para formular sua resposta.
    O consumo e geração solar estão em kWh, o soc médio é medido em %, os horários de pico são em horas.

    Métricas Analíticas:
    {metricas_formatado}

    Informações em Tempo Real dos Aparelhos:
    {info_formatado}

    ### PERGUNTA DO USUÁRIO ###
    "{pergunta}"
    """


    # --- ETAPA 3: Configurar e Chamar o Modelo ---
    
    generation_config = {
        "temperature": 0.5, # Reduzido um pouco para respostas mais focadas nos fatos
        "max_output_tokens": 300, 
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=system_prompt,
        generation_config=generation_config
    )

    resposta = model.generate_content(user_prompt)

    return {
        "pergunta": pergunta,
        "resposta": resposta.text.strip()
    }