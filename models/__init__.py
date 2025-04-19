# backend/models/__init__.py
# importa todos os modelos
from .paciente import Paciente
from .consulta import Consulta

# Define quais símbolos são exportados pelo módulo
__all__ = ["Paciente", "Consulta"]
