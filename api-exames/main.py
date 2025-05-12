from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import HTTPException

class Requisicao(BaseModel):
    requisicao: int
    item: int
    accession_number: str
    servico: str
    descricao: Optional[str]
    grupo: Optional[str]
    nome_grupo: Optional[str]
    complemento: Optional[str]
    quantidade: Optional[int]
    posicao_exame: Optional[str]
    paciente: Optional[str]
    cpf: Optional[str]
    rg: Optional[str]
    telefone: Optional[str]
    dt_requisicao: Optional[str]

import asyncpg
from fastapi import FastAPI

async def get_db_pool():
    return await asyncpg.create_pool(
        user="wareline_integracoes",
        password="War&lin$2025@",
        database="waresearch",
        host="44.207.38.121",
        port=5432
    )

async def startup(app: FastAPI):
    app.state.pool = await get_db_pool()

async def shutdown(app: FastAPI):
    await app.state.pool.close()

from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await startup(app)

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown(app)

@app.get("/requisicoes", response_model=List[Requisicao])
async def listar_requisicoes(
    requisicao: Optional[int] = Query(None),
    item: Optional[int] = Query(None)
):
    query = """
    SELECT requisicao, item, accession_number, servico, descricao, grupo, nome_grupo,
        complemento, quantidade, posicao_exame, paciente, cpf, rg, telefone, dt_requisicao
    FROM integracoes.requisicoes
    WHERE 1=1
    """
    params = []
    if requisicao is not None:
        query += f" AND requisicao = ${len(params) + 1}"
        params.append(requisicao)
    if item is not None:
        query += f" AND item = ${len(params) + 1}"
        params.append(item)

    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch(query, *params)
        
        result = []
        for row in rows:
            row_dict = {key: value for key, value in row.items()}  # Convertendo para dicionário
            if row_dict['dt_requisicao']:
                row_dict['dt_requisicao'] = row_dict['dt_requisicao'].strftime('%Y-%m-%dT%H:%M:%S')
            result.append(row_dict)
        
        return result

@app.post("/requisicao")
async def cadastrar_requisicao(requisicao: Requisicao):
    conn = await asyncpg.connect(
        user="wareline_integracoes",
        password="War&lin$2025@",
        database="waresearch",
        host="44.207.38.121",
        port=5432)
    try:
        dt_convertida = None
        if requisicao.dt_requisicao:
            dt_convertida = datetime.fromisoformat(requisicao.dt_requisicao)

        await conn.execute("""
            INSERT INTO integracoes.requisicoes (
                requisicao, item, accession_number, servico, descricao,
                grupo, nome_grupo, complemento, quantidade, posicao_exame,
                paciente, cpf, rg, telefone, dt_requisicao
            )
            VALUES (
                $1, $2, $3, $4, $5,
                $6, $7, $8, $9, $10,
                $11, $12, $13, $14, $15
            )
        """,
        requisicao.requisicao,
        requisicao.item,
        requisicao.accession_number,
        requisicao.servico,
        requisicao.descricao,
        requisicao.grupo,
        requisicao.nome_grupo,
        requisicao.complemento,
        requisicao.quantidade,
        requisicao.posicao_exame,
        requisicao.paciente,
        requisicao.cpf,
        requisicao.rg,
        requisicao.telefone,
        dt_convertida
        )

        return {"mensagem": "Requisição cadastrada com sucesso"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Formato inválido para dt_requisicao. Use o formato ISO 8601.")
