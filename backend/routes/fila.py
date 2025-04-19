# backend/routes/fila.py

from fastapi import APIRouter, HTTPException
from backend.services.fila_service import gerar_fila
from backend.models.response import ResponseModel
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Fila"])


@router.get("/fila", response_model=ResponseModel)
def get_fila():
    try:
        fila = gerar_fila()
        return ResponseModel(success=True, data=fila, message="Fila gerada com sucesso")
    except Exception as e:
        # Logar o erro para diagnóstico
        logger.error(f"Erro ao gerar fila: {str(e)}", exc_info=True)
        return ResponseModel(success=False, data=None, message=f"Erro ao gerar fila: {str(e)}")
