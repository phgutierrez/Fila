# backend/services/consulta_service.py

from datetime import date
from backend.models.consulta import Consulta
from backend.models.paciente import Paciente
from sqlmodel import Session
from backend.database import engine

# Cálculo da idade na data da consulta


def calcular_idade(data_nascimento: date, data_consulta: date) -> int:
    idade = data_consulta.year - data_nascimento.year
    if (data_consulta.month, data_consulta.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

# Cálculo do escore clínico


def calcular_escore(consulta: Consulta, idade: int) -> int:
    escore = 0

    # Tipo de escoliose
    if consulta.tipo_escoliose == "idiopatica":
        escore += 1
    elif consulta.tipo_escoliose in ("sindromica", "congenita", "displasica"):
        escore += 2
    elif consulta.tipo_escoliose == "neuromuscular":
        escore += 3

    # Ângulo de Cobb
    if 40 <= consulta.angulo_cobb <= 59:
        escore += 1
    elif 60 <= consulta.angulo_cobb <= 79:
        escore += 2
    elif consulta.angulo_cobb >= 80:
        escore += 3

    # Progressão documentada
    if consulta.progressao_6m <= 0:
        escore += 0
    elif consulta.progressao_6m <= 10:
        escore += 1
    else:
        escore += 2

    # Idade
    if idade <= 10:
        escore += 2
    elif 11 <= idade <= 14:
        escore += 1

    # Risser
    if consulta.risser in (0, 1, 2):
        escore += 2

    # Menarca
    if consulta.menarca_status in ("pre", "masculino"):
        escore += 2

    # Comorbidades
    if consulta.comorbidades in ("gastro", "epilepsia"):
        escore += 1
    elif consulta.comorbidades in ("traqueo", "vni", "restricao_pulmonar"):
        escore += 2

    # Dor / Impacto funcional
    if consulta.dor_funcional == "moderada":
        escore += 1
    elif consulta.dor_funcional == "intensa":
        escore += 2

    # Tempo de espera
    if 6 <= consulta.espera_cirurgica_meses <= 12:
        escore += 1
    elif consulta.espera_cirurgica_meses > 12:
        escore += 2

    return escore

# Classificação por escore


def classificar_prioridade(escore: int) -> str:
    if escore <= 9:
        return "eletiva"
    elif escore <= 15:
        return "intermediaria"
    return "alta"

# Salvar consulta com cálculo automático


def salvar_consulta(paciente: Paciente, consulta: Consulta) -> Consulta:
    idade = calcular_idade(paciente.data_nascimento, consulta.data_consulta)
    escore = calcular_escore(consulta, idade)
    prioridade = classificar_prioridade(escore)

    consulta.escore = escore
    consulta.classificacao_prioridade = prioridade

    with Session(engine) as session:
        consulta.paciente_id = paciente.id
        session.add(consulta)
        session.commit()
        session.refresh(consulta)
        return consulta
