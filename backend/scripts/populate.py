# backend/scripts/populate.py

from sqlmodel import Session
from datetime import date
from backend.database import engine
from backend.models.paciente import Paciente
from backend.models.consulta import Consulta
from backend.services.consulta_service import salvar_consulta

pacientes_dados = [
    {
        "prontuario": "0001",
        "nome_completo": "Maria da Silva",
        "sexo": "F",
        "data_nascimento": date(2012, 5, 10),
        "municipio": "São Paulo",
        "medico_assistente": "Dr. João Andrade",
        "consultas": [
            {
                "data_consulta": date(2024, 4, 10),
                "tipo_escoliose": "idiopatica",
                "angulo_cobb": 62,
                "progressao_6m": 8.0,
                "risser": 2,
                "menarca_status": "pre",
                "comorbidades": "nenhuma",
                "dor_funcional": "moderada",
                "espera_cirurgica_meses": 9,
            }
        ]
    },
    {
        "prontuario": "0002",
        "nome_completo": "João Pereira",
        "sexo": "M",
        "data_nascimento": date(2008, 3, 14),
        "municipio": "Campinas",
        "medico_assistente": "Dra. Lúcia Moreira",
        "consultas": [
            {
                "data_consulta": date(2024, 2, 25),
                "tipo_escoliose": "neuromuscular",
                "angulo_cobb": 85,
                "progressao_6m": 15.0,
                "risser": 1,
                "menarca_status": "masculino",
                "comorbidades": "traqueo",
                "dor_funcional": "intensa",
                "espera_cirurgica_meses": 13,
            }
        ]
    },
    {
        "prontuario": "0003",
        "nome_completo": "Ana Souza",
        "sexo": "F",
        "data_nascimento": date(2010, 8, 22),
        "municipio": "Ribeirão Preto",
        "medico_assistente": "Dr. Felipe Lima",
        "consultas": [
            {
                "data_consulta": date(2024, 3, 15),
                "tipo_escoliose": "displasica",
                "angulo_cobb": 45,
                "progressao_6m": 2.0,
                "risser": 3,
                "menarca_status": "pos",
                "comorbidades": "epilepsia",
                "dor_funcional": "moderada",
                "espera_cirurgica_meses": 7,
            }
        ]
    },
]

with Session(engine) as session:
    for dados in pacientes_dados:
        paciente = Paciente(
            prontuario=dados["prontuario"],
            nome_completo=dados["nome_completo"],
            sexo=dados["sexo"],
            data_nascimento=dados["data_nascimento"],
            municipio=dados["municipio"],
            medico_assistente=dados["medico_assistente"]
        )
        session.add(paciente)
        session.commit()
        session.refresh(paciente)

        for c in dados["consultas"]:
            consulta = Consulta(**c)
            salvar_consulta(paciente, consulta)

print("✅ Pacientes e consultas populados com sucesso!")
