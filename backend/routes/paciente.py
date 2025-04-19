# backend/routes/paciente.py

from fastapi import APIRouter, HTTPException
from backend.models.paciente import Paciente
from backend.models.response import ResponseModel
from backend.services.paciente_service import (
    criar_paciente,
    buscar_paciente_por_id,
    listar_pacientes,
    atualizar_paciente,
    deletar_paciente
)
from typing import List

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
def post_paciente(paciente: Paciente):
    novo = criar_paciente(paciente)
    return ResponseModel(success=True, data=novo, message="Paciente criado com sucesso")

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
