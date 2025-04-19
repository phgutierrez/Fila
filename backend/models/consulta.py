# backend/models/consulta.py

from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING, ClassVar
from datetime import date
from pydantic import field_validator
from sqlalchemy.orm import relationship, RelationshipProperty

if TYPE_CHECKING:
    from .paciente import Paciente


class Consulta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paciente_id: int = Field(foreign_key="paciente.id")

    data_consulta: date
    tipo_escoliose: str
    angulo_cobb: int
    progressao_6m: float
    risser: int
    menarca_status: str
    comorbidades: str
    dor_funcional: str
    espera_cirurgica_meses: int

    escore: Optional[int] = None
    classificacao_prioridade: Optional[str] = None

    # Usar ClassVar para indicar que este campo não é um campo de dados Pydantic
    paciente: ClassVar[RelationshipProperty] = relationship(
        "Paciente", back_populates="consultas")

    @field_validator("risser")
    @classmethod
    def validar_risser(cls, v: int) -> int:
        if not 0 <= v <= 5:
            raise ValueError(
                "O valor de Risser deve estar entre 0 e 5, conforme a classificação radiográfica.")
        return v

    @field_validator("menarca_status")
    @classmethod
    def validar_menarca(cls, v: str) -> str:
        if v not in ("pre", "pos", "masculino"):
            raise ValueError(
                "Status da menarca deve ser 'pre', 'pos' ou 'masculino'.")
        return v

    @field_validator("tipo_escoliose")
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        if v not in ("idiopatica", "sindromica", "congenita", "displasica", "neuromuscular"):
            raise ValueError(
                "Tipo de escoliose inválido. Use: idiopatica, sindromica, congenita, displasica ou neuromuscular.")
        return v

    @field_validator("dor_funcional")
    @classmethod
    def validar_dor(cls, v: str) -> str:
        if v not in ("sem", "moderada", "intensa"):
            raise ValueError(
                "Nível de dor inválido. Use: sem, moderada ou intensa.")
        return v
