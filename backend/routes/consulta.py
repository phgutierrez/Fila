# backend/routes/consulta.py

from fastapi import APIRouter, HTTPException
from backend.models.consulta import Consulta
from backend.services.consulta_service import salvar_consulta
from backend.services.paciente_service import buscar_paciente_com_consultas
from sqlmodel import Session
from backend.database import engine
from typing import List

router = APIRouter(prefix="/api/v1", tags=["Consultas"])


@router.get("/pacientes/{id}/consultas", response_model=List[Consulta])
def get_consultas_do_paciente(id: int):
    paciente = buscar_paciente_com_consultas(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente.consultas


@router.post("/pacientes/{id}/consultas", response_model=Consulta, status_code=201)
def post_consulta(id: int, consulta: Consulta):
    paciente = buscar_paciente_com_consultas(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return salvar_consulta(paciente, consulta)


@router.get("/consultas/{id}", response_model=Consulta)
def get_consulta_por_id(id: int):
    with Session(engine) as session:
        consulta = session.get(Consulta, id)
        if not consulta:
            raise HTTPException(
                status_code=404, detail="Consulta não encontrada")
        return consulta
