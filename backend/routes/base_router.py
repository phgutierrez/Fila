# backend/routes/base_router.py
from fastapi import APIRouter

api_router = APIRouter()

# Importar e incluir rotas reais depois
# from .paciente import router as paciente_router
# api_router.include_router(paciente_router, prefix="/pacientes", tags=["Pacientes"])
