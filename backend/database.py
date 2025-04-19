from sqlmodel import SQLModel, create_engine
from backend.config import settings

engine = create_engine(settings.db_url, echo=True)


def create_db_and_tables():
    # Alterado o caminho de importação de 'models' para 'backend.models'
    from backend.models import paciente, consulta
    # importa os modelos
    SQLModel.metadata.create_all(engine)
    print("✅ Banco de dados criado com sucesso!")
