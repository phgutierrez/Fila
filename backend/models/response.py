# backend/models/response.py

from typing import Any, Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": 1, "nome": "Maria da Silva"},
                "message": "Paciente retornado com sucesso."
            }
        }
