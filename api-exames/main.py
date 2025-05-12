from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncpg

app = FastAPI()

#================================Classes=======================================
class Exame(BaseModel):
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
    id_material: Optional[str]
    laboratorio: Optional[str]
    atendimento: Optional[int]
    prioridade: Optional[str]
    tipo_atendimento: Optional[str]
    leito: Optional[str]
    acomodacao: Optional[str]
    id_setor: Optional[str]
    setor: Optional[str]
    rn: Optional[str]
    prontuario: Optional[int]
    sexo: Optional[str]
    dt_nascimento: Optional[datetime]
    peso: Optional[float]
    altura: Optional[float]
    email: Optional[str]
    id_med_solicitante: Optional[str]
    medico_solicitante: Optional[str]
    crm_solicitante: Optional[str]
    sigla_solicitante: Optional[str]
    uf_solicitante: Optional[str]
    id_med_responsavel: Optional[str]
    medico_responsavel: Optional[str]
    crm_responsavel: Optional[str]
    sigla_responsavel: Optional[str]
    uf_responsavel: Optional[str]
    id_plano: Optional[str]
    plano: Optional[str]
    id_convenio: Optional[str]
    convenio: Optional[str]
    id_filial: Optional[str]


class NovaRequisicao(BaseModel):
    exames: List[Exame]

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
    id_material: Optional[str]
    laboratorio: Optional[str]
    atendimento: Optional[int]
    prioridade: Optional[str]
    tipo_atendimento: Optional[str]
    leito: Optional[str]
    acomodacao: Optional[str]
    id_setor: Optional[str]
    setor: Optional[str]
    rn: Optional[str]
    prontuario: Optional[int]
    sexo: Optional[str]
    dt_nascimento: Optional[datetime]
    peso: Optional[float]
    altura: Optional[float]
    email: Optional[str]
    id_med_solicitante: Optional[str]
    medico_solicitante: Optional[str]
    crm_solicitante: Optional[str]
    sigla_solicitante: Optional[str]
    uf_solicitante: Optional[str]
    id_med_responsavel: Optional[str]
    medico_responsavel: Optional[str]
    crm_responsavel: Optional[str]
    sigla_responsavel: Optional[str]
    uf_responsavel: Optional[str]
    id_plano: Optional[str]
    plano: Optional[str]
    id_convenio: Optional[str]
    convenio: Optional[str]
    id_filial: Optional[str]

# Conexão com o banco (waresearch)
async def get_db_pool():
    return await asyncpg.create_pool(
        user="wareline_integracoes",
        password="War&lin$2025@",
        database="waresearch",
        host="44.207.38.121",
        port=5432
    )

@app.on_event("startup")
async def on_startup():
    app.state.pool = await get_db_pool()

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.pool.close()

#========================================Endpoint POST====================================
from fastapi import HTTPException
from datetime import datetime

@app.post("/requisicao")
async def cadastrar_requisicao(nova_requisicao: NovaRequisicao):
    async with app.state.pool.acquire() as conn:
        async with conn.transaction():
            # Obter a última requisição existente
            row = await conn.fetchrow("SELECT MAX(requisicao) AS ultima FROM integracoes.requisicoes")
            ultima_requisicao = row['ultima'] or 0
            nova_requisicao_num = ultima_requisicao + 1

            for i, exame in enumerate(nova_requisicao.exames, start=1):
                item = i
                accession_number = f"{nova_requisicao_num}{str(item).zfill(3)}"

                dt_convertida = None
                if exame.dt_requisicao:
                    try:
                        dt_convertida = datetime.fromisoformat(exame.dt_requisicao)
                    except ValueError:
                        raise HTTPException(status_code=400, detail="Formato inválido para dt_requisicao. Use ISO 8601.")

                await conn.execute("""
                    INSERT INTO integracoes.requisicoes (
                        requisicao, item, accession_number, servico, descricao, grupo, nome_grupo,
                        complemento, quantidade, posicao_exame, paciente, cpf, rg, telefone, dt_requisicao,
                        id_material, laboratorio, atendimento, prioridade, tipo_atendimento, leito,
                        acomodacao, id_setor, setor, rn, prontuario, sexo, dt_nascimento, peso, altura,
                        email, id_med_solicitante, medico_solicitante, crm_solicitante, sigla_solicitante,
                        uf_solicitante, id_med_responsavel, medico_responsavel, crm_responsavel,
                        sigla_responsavel, uf_responsavel, id_plano, plano, id_convenio, convenio, id_filial
                    )
                    VALUES (
                        $1, $2, $3, $4, $5, $6, $7,
                        $8, $9, $10, $11, $12, $13, $14, $15,
                        $16, $17, $18, $19, $20, $21,
                        $22, $23, $24, $25, $26, $27, $28, $29, $30,
                        $31, $32, $33, $34, $35,
                        $36, $37, $38, $39,
                        $40, $41, $42, $43, $44, $45, $46
                    )
                """,
                nova_requisicao_num,
                item,
                accession_number,
                exame.servico,
                exame.descricao,
                exame.grupo,
                exame.nome_grupo,
                exame.complemento,
                exame.quantidade,
                exame.posicao_exame,
                exame.paciente,
                exame.cpf,
                exame.rg,
                exame.telefone,
                dt_convertida,
                exame.id_material,
                exame.laboratorio,
                exame.atendimento,
                exame.prioridade,
                exame.tipo_atendimento,
                exame.leito,
                exame.acomodacao,
                exame.id_setor,
                exame.setor,
                exame.rn,
                exame.prontuario,
                exame.sexo,
                exame.dt_nascimento,
                exame.peso,
                exame.altura,
                exame.email,
                exame.id_med_solicitante,
                exame.medico_solicitante,
                exame.crm_solicitante,
                exame.sigla_solicitante,
                exame.uf_solicitante,
                exame.id_med_responsavel,
                exame.medico_responsavel,
                exame.crm_responsavel,
                exame.sigla_responsavel,
                exame.uf_responsavel,
                exame.id_plano,
                exame.plano,
                exame.id_convenio,
                exame.convenio,
                exame.id_filial
                )

    return {
        "mensagem": "Requisição cadastrada com sucesso",
        "requisicao": nova_requisicao_num,
        "itens": len(nova_requisicao.exames)
    }

#==============================Endpoint GET=========================================
@app.get("/requisicoes", response_model=List[Requisicao])
async def listar_requisicoes(
    requisicao: Optional[int] = Query(None),
    item: Optional[int] = Query(None)
):
    query = """
    SELECT requisicao, item, accession_number, servico, descricao, grupo, nome_grupo,
        complemento, quantidade, posicao_exame, paciente, cpf, rg, telefone, dt_requisicao,
        id_material, laboratorio, atendimento, prioridade, tipo_atendimento, leito, acomodacao,
        id_setor, setor, rn, prontuario, sexo, dt_nascimento, peso, altura, email,
        id_med_solicitante, medico_solicitante, crm_solicitante, sigla_solicitante, uf_solicitante,
        id_med_responsavel, medico_responsavel, crm_responsavel, sigla_responsavel, uf_responsavel,
        id_plano, plano, id_convenio, convenio, id_filial
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
            row_dict = dict(row)
            if row_dict.get("dt_requisicao"):
                row_dict["dt_requisicao"] = row_dict["dt_requisicao"].strftime('%Y-%m-%dT%H:%M:%S')
            if row_dict.get("dt_nascimento"):
                row_dict["dt_nascimento"] = row_dict["dt_nascimento"].strftime('%Y-%m-%dT%H:%M:%S')
            result.append(row_dict)

        return result
