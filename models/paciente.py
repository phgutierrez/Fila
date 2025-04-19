from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional, List, TYPE_CHECKING, ClassVar
from datetime import date
from pydantic import field_validator
from sqlalchemy.orm import relationship, RelationshipProperty

if TYPE_CHECKING:
    from .consulta import Consulta


class Paciente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prontuario: str
    nome_completo: str
    sexo: str
    data_nascimento: date
    municipio: str
    medico_assistente: str

    # Usar ClassVar para indicar que este campo não é um campo Pydantic normal
    consultas: ClassVar[RelationshipProperty] = relationship(
        "Consulta", back_populates="paciente")

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, v: str) -> str:
        if v not in ("M", "F"):
            raise ValueError("Sexo deve ser 'M' ou 'F'")
        return v
