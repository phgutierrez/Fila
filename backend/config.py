from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Variáveis de configuração
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fila.db")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

class Settings:
    db_url = DATABASE_URL
    debug = DEBUG

settings = Settings()
