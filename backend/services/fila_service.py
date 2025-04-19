# backend/services/fila_service.py

from sqlmodel import select, Session
from backend.database import engine
from backend.models.paciente import Paciente
from backend.services.consulta_service import calcular_idade
from typing import List, Dict, Any
from datetime import date

# Gera fila com critérios combinados


def gerar_fila() -> List[Dict[str, Any]]:
    with Session(engine) as session:
        pacientes = session.exec(select(Paciente)).all()
        fila = []

        for paciente in pacientes:
            consultas = paciente.consultas
            if not consultas:
                continue

            ultima_consulta = sorted(
                consultas, key=lambda c: c.data_consulta)[-1]
            primeira_consulta = sorted(
                consultas, key=lambda c: c.data_consulta)[0]
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
