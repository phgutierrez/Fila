# backend/routes/fila.py

from fastapi import APIRouter
from backend.services.fila_service import gerar_fila

router = APIRouter(prefix="/api/v1", tags=["Fila"])


@router.get("/fila")
def get_fila():
    return gerar_fila()
