from sqlmodel import SQLModel, create_engine
from backend.config import settings

engine = create_engine(settings.db_url, echo=True)


def create_db_and_tables():
    from models import paciente, consulta
  # importa os modelos
    SQLModel.metadata.create_all(engine)
