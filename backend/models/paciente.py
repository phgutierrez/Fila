# backend/models/paciente.py

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

    # Usar ClassVar para indicar que este campo não é um campo de dados Pydantic
    consultas: ClassVar[RelationshipProperty] = relationship(
        "Consulta", back_populates="paciente")

    @field_validator("sexo")
    @classmethod
    def validar_sexo(cls, v: str) -> str:
        if v not in ("M", "F"):
            raise ValueError(
                "Sexo deve ser 'M' (masculino) ou 'F' (feminino), conforme registro clínico.")
        return v

    @field_validator("prontuario")
    @classmethod
    def validar_prontuario(cls, v: str) -> str:
        if not v.strip():
            raise ValueError(
                "O campo 'prontuario' não pode estar vazio. Utilize um identificador clínico válido.")
        return v

    @field_validator("nome_completo")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if len(v.strip().split()) < 2:
            raise ValueError(
                "Informe o nome completo do paciente (nome e sobrenome).")
        return v

    @field_validator("municipio")
    @classmethod
    def validar_municipio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O município de residência deve ser informado.")
        return v
