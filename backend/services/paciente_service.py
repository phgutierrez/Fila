# backend/services/paciente_service.py

from sqlmodel import Session, select
from backend.database import engine
from backend.models.paciente import Paciente
from backend.models.consulta import Consulta
from typing import List, Optional

# CRIAR paciente


def criar_paciente(paciente: Paciente) -> Paciente:
    with Session(engine) as session:
        session.add(paciente)
        session.commit()
        session.refresh(paciente)
        return paciente

# LER paciente por ID


def buscar_paciente_por_id(paciente_id: int) -> Optional[Paciente]:
    with Session(engine) as session:
        paciente = session.get(Paciente, paciente_id)
        return paciente

# LISTAR todos os pacientes


def listar_pacientes() -> List[Paciente]:
    with Session(engine) as session:
        pacientes = session.exec(select(Paciente)).all()
        return pacientes

# ATUALIZAR paciente


def atualizar_paciente(paciente_id: int, novos_dados: dict) -> Optional[Paciente]:
    with Session(engine) as session:
        paciente = session.get(Paciente, paciente_id)
        if not paciente:
            return None
        for chave, valor in novos_dados.items():
            setattr(paciente, chave, valor)
        session.add(paciente)
        session.commit()
        session.refresh(paciente)
        return paciente

# DELETAR paciente


def deletar_paciente(paciente_id: int) -> bool:
    with Session(engine) as session:
        paciente = session.get(Paciente, paciente_id)
        if not paciente:
            return False
        session.delete(paciente)
        session.commit()
        return True

# Buscar paciente + histórico de consultas


def buscar_paciente_com_consultas(paciente_id: int) -> Optional[Paciente]:
    with Session(engine) as session:
        statement = select(Paciente).where(Paciente.id == paciente_id)
        paciente = session.exec(statement).first()
        if paciente:
            _ = paciente.consultas  # força carregar relacionamento
        return paciente
