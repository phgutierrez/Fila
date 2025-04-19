# backend/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from backend.config import settings
from backend.database import create_db_and_tables
from backend.routes.paciente import router as paciente_router
from backend.routes.consulta import router as consulta_router
from backend.routes.fila import router as fila_router

app = FastAPI(title="Fila de Escoliose API", version="1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"⬅️ {response.status_code} {request.url}")
    return response

# Global Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "data": None, "message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "data": None, "message": "Erro de validação", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"🔥 Erro inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "data": None, "message": "Erro interno do servidor"},
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include Routers
app.include_router(paciente_router)
app.include_router(consulta_router)
app.include_router(fila_router)