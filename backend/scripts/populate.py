from datetime import date
from sqlmodel import Session
from backend.database import engine
from models.paciente import Paciente
from models.consulta import Consulta

# Cria um paciente de exemplo
paciente = Paciente(
    prontuario="123456",
    nome_completo="Maria da Silva",
    sexo="F",
    data_nascimento=date(2010, 5, 17),
    municipio="São Paulo",
    medico_assistente="Dr. João Andrade"
)

# Cria uma consulta associada
consulta = Consulta(
    data_consulta=date(2024, 4, 15),
    tipo_escoliose="idiopatica",
    angulo_cobb=55,
    progressao_6m=12.5,
    risser=2,
    menarca_status="pre",
    comorbidades="nenhuma",
    dor_funcional="moderada",
    espera_cirurgica_meses=9
)

# Abrindo sessão e salvando
with Session(engine) as session:
    session.add(paciente)
    session.commit()
    session.refresh(paciente)

    consulta.paciente_id = paciente.id
    session.add(consulta)
    session.commit()
    session.refresh(consulta)

    print(f"✅ Paciente ID {paciente.id} criado com consulta ID {consulta.id}")
