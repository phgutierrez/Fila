# backend/routes/paciente.py

from fastapi import APIRouter, HTTPException
from backend.models.paciente import Paciente
from backend.services.paciente_service import (
    criar_paciente,
    buscar_paciente_por_id,
    listar_pacientes,
    atualizar_paciente,
    deletar_paciente
)
from typing import List

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])


@router.get("/", response_model=List[Paciente])
def get_pacientes():
    return listar_pacientes()


@router.get("/{id}", response_model=Paciente)
def get_paciente(id: int):
    paciente = buscar_paciente_por_id(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.post("/", response_model=Paciente, status_code=201)
def post_paciente(paciente: Paciente):
    return criar_paciente(paciente)


@router.put("/{id}", response_model=Paciente)
def put_paciente(id: int, dados: dict):
    paciente = atualizar_paciente(id, dados)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.delete("/{id}", status_code=204)
def delete_paciente(id: int):
    sucesso = deletar_paciente(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
