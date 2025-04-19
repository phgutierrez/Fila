from fastapi import APIRouter, HTTPException
from backend.models.consulta import Consulta
from backend.models.response import ResponseModel
from backend.services.consulta_service import salvar_consulta
from backend.services.paciente_service import buscar_paciente_com_consultas
from sqlmodel import Session
from backend.database import engine

router = APIRouter(prefix="/api/v1", tags=["Consultas"])

@router.get("/pacientes/{id}/consultas", response_model=ResponseModel)
def get_consultas_do_paciente(id: int):
    paciente = buscar_paciente_com_consultas(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return ResponseModel(success=True, data=paciente.consultas, message="Consultas retornadas com sucesso")

@router.post("/pacientes/{id}/consultas", response_model=ResponseModel, status_code=201)
def post_consulta(id: int, consulta: Consulta):
    paciente = buscar_paciente_com_consultas(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    nova = salvar_consulta(paciente, consulta)
    return ResponseModel(success=True, data=nova, message="Consulta salva com sucesso")

@router.get("/consultas/{id}", response_model=ResponseModel)
def get_consulta_por_id(id: int):
    with Session(engine) as session:
        consulta = session.get(Consulta, id)
        if not consulta:
            raise HTTPException(status_code=404, detail="Consulta não encontrada")
        return ResponseModel(success=True, data=consulta, message="Consulta encontrada")
