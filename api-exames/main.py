from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

app = FastAPI(title="API de Requisição de Exames", version="1.0.0")

class RequisicaoExame(BaseModel):
    requisicao: int
    item: int
    accession_number: str
    servico: str
    depara: str
    depara2: Optional[str]
    descricao: str
    grupo: str
    nome_grupo: str
    complemento: str
    quantidade: int
    posicao_exame: str
    id_material: str
    laboratorio: str
    prioridade: str
    atendimento: str
    tipo_atendimento: str
    leito: str
    acomodacao: str
    id_setor: str
    setor: str
    dt_requisicao: date
    rn: str
    prontuario: str
    paciente: str
    sexo: str
    dt_nascimento: date
    peso: float
    altura: int
    cpf: str
    rg: str
    email: str
    celular: str
    telefone: str
    id_med_solicitante: str
    medico_solicitante: str
    crm_solicitante: str
    sigla_solicitante: str
    uf_solicitante: str
    id_med_responsavel: str
    medico_responsavel: str
    crm_responsavel: str
    sigla_responsavel: str
    uf_responsavel: str
    id_plano: str
    plano: str
    id_convenio: str
    convenio: str
    id_filial: str
    status_exame: str
    modalidade: str
    nome_responsavel_at: Optional[str]
    rg_responsavel_at: Optional[str]
    cpf_responsavel_at: Optional[str]
    datarlz: datetime

@app.get("/exames", response_model=List[RequisicaoExame])
def listar_exames():
    return [
        {
            "requisicao": 10234567,
            "item": 2,
            "accession_number": "10234567002",
            "servico": "RAD123",
            "depara": "INT456",
            "depara2": "EXT789",
            "descricao": "Tomografia Computadorizada de Crânio",
            "grupo": "0701",
            "nome_grupo": "Tomografia",
            "complemento": "Com contraste intravenoso",
            "quantidade": 1,
            "posicao_exame": "SOLICITADO",
            "id_material": "MAT202",
            "laboratorio": "AC",
            "prioridade": "N",
            "atendimento": "ATD908172",
            "tipo_atendimento": "I",
            "leito": "403-A",
            "acomodacao": "Enfermaria",
            "id_setor": "SET034",
            "setor": "Pronto Socorro Adulto",
            "dt_requisicao": "2025-04-13",
            "rn": "N",
            "prontuario": "PCT903821",
            "paciente": "João Carlos Pereira",
            "sexo": "M",
            "dt_nascimento": "1978-02-15",
            "peso": 82.5,
            "altura": 175,
            "cpf": "12345678901",
            "rg": "SP9876543",
            "email": "joao.pereira@email.com",
            "celular": "11999998888",
            "telefone": "1133334455",
            "id_med_solicitante": "MED1456",
            "medico_solicitante": "Dra. Fernanda Ribeiro",
            "crm_solicitante": "472189",
            "sigla_solicitante": "CRM",
            "uf_solicitante": "SP",
            "id_med_responsavel": "MED2901",
            "medico_responsavel": "Dr. Marcelo Tavares",
            "crm_responsavel": "381026",
            "sigla_responsavel": "CRM",
            "uf_responsavel": "SP",
            "id_plano": "PLN5566",
            "plano": "Plano Saúde Mais",
            "id_convenio": "CNV1020",
            "convenio": "Convênio Vida Total",
            "id_filial": "FIL002",
            "status_exame": "NW",
            "modalidade": "CT",
            "nome_responsavel_at": "Luciana Gomes",
            "rg_responsavel_at": "RJ1122334",
            "cpf_responsavel_at": "32165498700",
            "datarlz": "2025-04-13T16:25:00"
        }
    ]
