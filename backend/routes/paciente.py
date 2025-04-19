# backend/routes/paciente.py
from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from backend.database import engine
from backend.models.paciente import Paciente
from backend.models.response import ResponseModel
from backend.services.paciente_service import (
    criar_paciente,
    buscar_paciente_por_id,
    listar_pacientes,
    atualizar_paciente,
    deletar_paciente
)
from typing import List, Dict, Any
from datetime import date
from pydantic import BaseModel

# Esquema simplificado para receber dados do formulário
class PacienteInput(BaseModel):
    prontuario: str
    nome_completo: str
    sexo: str
    data_nascimento: str  # Recebendo como string do formulário
    municipio: str
    medico_assistente: str

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])


@router.get("/", response_model=ResponseModel)
def get_pacientes():
    pacientes = listar_pacientes()
    return ResponseModel(success=True, data=pacientes, message="Pacientes listados com sucesso")


@router.get("/{id}", response_model=ResponseModel)
def get_paciente(id: int):
    paciente = buscar_paciente_por_id(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return ResponseModel(success=True, data=paciente, message="Paciente encontrado")


@router.post("/", response_model=ResponseModel, status_code=201)
def post_paciente(paciente_input: PacienteInput):
    try:
        # Converter a string de data para objeto date
        data_nascimento = date.fromisoformat(paciente_input.data_nascimento)
        
        # Criar o objeto Paciente com os dados convertidos
        paciente = Paciente(
            prontuario=paciente_input.prontuario,
            nome_completo=paciente_input.nome_completo,
            sexo=paciente_input.sexo,
            data_nascimento=data_nascimento,
            municipio=paciente_input.municipio,
            medico_assistente=paciente_input.medico_assistente
        )
        
        novo = criar_paciente(paciente)
        return ResponseModel(success=True, data=novo, message="Paciente criado com sucesso")
    except ValueError as e:
        # Tratar erros de formato de data
        raise HTTPException(status_code=400, detail=f"Erro no formato dos dados: {str(e)}")
    except Exception as e:
        # Tratar outros erros
        raise HTTPException(status_code=500, detail=f"Erro ao criar paciente: {str(e)}")


@router.put("/{id}", response_model=ResponseModel)
def put_paciente(id: int, dados: dict):
    paciente = atualizar_paciente(id, dados)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return ResponseModel(success=True, data=paciente, message="Paciente atualizado com sucesso")


@router.delete("/{id}", response_model=ResponseModel)
def delete_paciente(id: int):
    sucesso = deletar_paciente(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return ResponseModel(success=True, data=None, message="Paciente removido com sucesso")


# Corrigindo o endpoint duplicado /pacientes e usando diretamente o modelo Paciente
@router.post("/criar", response_model=ResponseModel)
def criar_paciente_endpoint(paciente_dados: Paciente):
    try:
        novo = criar_paciente(paciente_dados)
        return ResponseModel(success=True, data=novo, message="Paciente criado com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
