# Arquivo: backend/main.py

from dotenv import load_dotenv
load_dotenv() # Carrega as variáveis de ambiente do arquivo .env
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# LINHA CORRIGIDA ABAIXO:
# Trocamos "rotas_site" por "rotas", que é o nome do seu arquivo.
from endpoints.rotas import rota_site
from alexa.rota import rota_alexa
# 1. Cria a aplicação principal (o "Chefe de Cozinha")
app = FastAPI(title="SmartSolarGrid API")

# 2. Configura o CORS (a permissão para o seu frontend conversar com o backend)
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclui o seu "livro de receitas" (suas rotas) na aplicação principal
app.include_router(rota_site)
app.include_router(rota_alexa)
# 4. (Opcional) Uma rota de boas-vindas para testar a API facilmente
@app.get("/")
def health_check():
    return {"status": "OK", "message": "Bem-vindo à API SmartSolarGrid!"}
