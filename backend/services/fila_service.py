# backend/services/fila_service.py

from sqlmodel import select, Session
from backend.database import engine
from backend.models.paciente import Paciente
from backend.models.consulta import Consulta
from backend.services.consulta_service import calcular_idade
from typing import List, Dict, Any
from datetime import date
import logging

# Configuração do logger
logger = logging.getLogger(__name__)


def buscar_pacientes_com_consultas():
    """
    Busca todos os pacientes e suas consultas de forma segura.
    """
    with Session(engine) as session:
        # Primeiro buscamos todos os pacientes
        pacientes = session.exec(select(Paciente)).all()

        # Para cada paciente, buscamos suas consultas explicitamente
        resultado = []
        for paciente in pacientes:
            # Buscar as consultas associadas a este paciente
            consultas = session.exec(
                select(Consulta).where(Consulta.paciente_id == paciente.id)
            ).all()

            # Se o paciente tem consultas, adicionamos à lista de resultados
            if consultas:
                resultado.append((paciente, consultas))

        return resultado

# Gera fila com critérios combinados


def gerar_fila() -> List[Dict[str, Any]]:
    try:
        fila = []

        # Buscar pacientes e suas consultas
        pacientes_consultas = buscar_pacientes_com_consultas()

        for paciente, consultas in pacientes_consultas:
            # Verificar se há consultas (já verificado na função auxiliar, mas por precaução)
            if not consultas:
                continue

            # Ordenar consultas por data
            consultas_ordenadas = sorted(
                consultas, key=lambda c: c.data_consulta)
            ultima_consulta = consultas_ordenadas[-1]
            primeira_consulta = consultas_ordenadas[0]

            idade = calcular_idade(
                paciente.data_nascimento, ultima_consulta.data_consulta)

            fila.append({
                "paciente_id": paciente.id,
                "nome": paciente.nome_completo,
                "escore": ultima_consulta.escore or 0,
                "prioridade": ultima_consulta.classificacao_prioridade,
                "idade": idade,
                "data_primeira_consulta": primeira_consulta.data_consulta,
            })

        # Ordena por:
        # 1. Maior escore
        # 2. Menor diferença para 18 anos (idade mais próxima de 18)
        # 3. Primeira consulta mais antiga
        fila_ordenada = sorted(
            fila,
            key=lambda x: (
                -x["escore"],
                abs(x["idade"] - 18),
                x["data_primeira_consulta"]
            )
        )

        return fila_ordenada
    except Exception as e:
        logger.error(f"Erro ao gerar fila: {str(e)}", exc_info=True)
        raise
