from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.config import settings
from backend.database import create_db_and_tables
from backend.routes.paciente import router as paciente_router
from backend.routes.consulta import router as consulta_router
from backend.routes.fila import router as fila_router
# Adicionando import para api_router
from backend.routes.base_router import api_router

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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Include Routers
app.include_router(paciente_router)
app.include_router(consulta_router)
app.include_router(fila_router)
app.include_router(api_router, prefix="/api/v1")
