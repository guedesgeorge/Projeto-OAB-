from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from scraper.scraper import fetch_lawyer_data # Importa a função do scraper

app = FastAPI(
    title="API de Consulta OAB",
    description="Uma API para extrair dados de advogados do Cadastro Nacional da OAB.",
    version="1.0.0"
)

class OABRequest(BaseModel):
    name: str = Field(..., description="Nome completo do advogado a ser pesquisado.")
    uf: str = Field(..., min_length=2, max_length=2, description="UF da seccional (ex: SP).")

class OABResponse(BaseModel):
    oab: str
    nome: str
    uf: str
    categoria: str
    data_inscricao: str
    situacao: str

@app.post("/fetch_oab", response_model=OABResponse, tags=["OAB"])
async def fetch_oab_endpoint(request: OABRequest):
    """
    Recebe um nome e uma UF, busca no site da OAB e retorna os dados do advogado.
    """
    print(f"Recebida requisição para: Nome='{request.name}', UF='{request.uf}'")
    
    data = fetch_lawyer_data(request.name, request.uf)

    if data and "error" in data:
        if "não encontrado" in data["error"]:
            raise HTTPException(status_code=404, detail=data["error"])
        raise HTTPException(status_code=500, detail=f"Erro durante o scraping: {data['error']}")
    
    if not data:
         raise HTTPException(status_code=500, detail="Erro interno: o scraping não retornou dados.")

    return data