# backend/scripts/test_escore.py
"""
Script para testar o cálculo de escore com todos os tipos possíveis.
"""

from backend.services.consulta_service import calcular_escore, classificar_prioridade
from backend.models.consulta import Consulta
from datetime import date


def criar_consulta_base():
    """Cria uma consulta com valores padrão para teste"""
    return Consulta(
        paciente_id=1,
        data_consulta=date(2025, 4, 19),
        tipo_escoliose="idiopatica",
        angulo_cobb=45,
        progressao_6m=5.0,
        risser=3,
        menarca_status="pos",
        comorbidades="nenhuma",
        dor_funcional="sem",
        espera_cirurgica_meses=3
    )


def testar_escore_tipo_escoliose():
    """Testa o cálculo de escore para diferentes tipos de escoliose"""
    print("\n=== TESTE: TIPO DE ESCOLIOSE ===")
    tipos = ["idiopatica", "sindromica",
             "congenita", "displasica", "neuromuscular"]

    for tipo in tipos:
        consulta = criar_consulta_base()
        consulta.tipo_escoliose = tipo
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Tipo: {tipo:<15} | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_angulo_cobb():
    """Testa o cálculo de escore para diferentes ângulos de Cobb"""
    print("\n=== TESTE: ÂNGULO DE COBB ===")
    angulos = [35, 45, 65, 85]

    for angulo in angulos:
        consulta = criar_consulta_base()
        consulta.angulo_cobb = angulo
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Ângulo: {angulo:<3}° | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_progressao():
    """Testa o cálculo de escore para diferentes progressões em 6 meses"""
    print("\n=== TESTE: PROGRESSÃO EM 6 MESES ===")
    progressoes = [0.0, 5.0, 12.0]

    for prog in progressoes:
        consulta = criar_consulta_base()
        consulta.progressao_6m = prog
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Progressão: {prog:<4}° | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_idade():
    """Testa o cálculo de escore para diferentes idades"""
    print("\n=== TESTE: IDADE ===")
    idades = [9, 12, 16]

    for idade in idades:
        consulta = criar_consulta_base()
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Idade: {idade:<2} anos | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_risser():
    """Testa o cálculo de escore para diferentes valores de Risser"""
    print("\n=== TESTE: RISSER ===")
    risser_valores = [0, 2, 4]

    for risser in risser_valores:
        consulta = criar_consulta_base()
        consulta.risser = risser
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Risser: {risser} | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_menarca():
    """Testa o cálculo de escore para diferentes status de menarca"""
    print("\n=== TESTE: MENARCA STATUS ===")
    status = ["pre", "pos", "masculino"]

    for menarca in status:
        consulta = criar_consulta_base()
        consulta.menarca_status = menarca
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Menarca: {menarca:<10} | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_comorbidades():
    """Testa o cálculo de escore para diferentes comorbidades"""
    print("\n=== TESTE: COMORBIDADES ===")
    comorbidades = ["nenhuma", "gastro", "epilepsia",
                    "traqueo", "vni", "restricao_pulmonar"]

    for comorb in comorbidades:
        consulta = criar_consulta_base()
        consulta.comorbidades = comorb
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Comorbidade: {comorb:<18} | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_dor():
    """Testa o cálculo de escore para diferentes níveis de dor"""
    print("\n=== TESTE: DOR FUNCIONAL ===")
    dores = ["sem", "moderada", "intensa"]

    for dor in dores:
        consulta = criar_consulta_base()
        consulta.dor_funcional = dor
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(f"Dor: {dor:<9} | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_escore_espera():
    """Testa o cálculo de escore para diferentes tempos de espera"""
    print("\n=== TESTE: TEMPO DE ESPERA ===")
    esperas = [3, 9, 15]

    for espera in esperas:
        consulta = criar_consulta_base()
        consulta.espera_cirurgica_meses = espera
        idade = 14
        escore = calcular_escore(consulta, idade)
        prioridade = classificar_prioridade(escore)
        print(
            f"Espera: {espera:<2} meses | Escore: {escore:<2} | Prioridade: {prioridade}")


def testar_casos_extremos():
    """Testa casos extremos para verificar o escore mínimo e máximo possível"""
    print("\n=== TESTE: CASOS EXTREMOS ===")

    # Caso com escore mínimo
    consulta_min = Consulta(
        paciente_id=1,
        data_consulta=date(2025, 4, 19),
        tipo_escoliose="idiopatica",
        angulo_cobb=35,  # < 40
        progressao_6m=0.0,  # <= 0
        risser=4,  # > 2
        menarca_status="pos",  # não é "pre" nem "masculino"
        comorbidades="nenhuma",  # sem comorbidades
        dor_funcional="sem",  # sem dor
        espera_cirurgica_meses=3  # < 6
    )
    idade_min = 15  # > 14
    escore_min = calcular_escore(consulta_min, idade_min)
    prioridade_min = classificar_prioridade(escore_min)

    # Caso com escore máximo
    consulta_max = Consulta(
        paciente_id=1,
        data_consulta=date(2025, 4, 19),
        tipo_escoliose="neuromuscular",  # +3
        angulo_cobb=85,  # >= 80, +3
        progressao_6m=15.0,  # > 10, +2
        risser=0,  # < 3, +2
        menarca_status="pre",  # "pre" ou "masculino", +2
        comorbidades="traqueo",  # comorbidade grave, +2
        dor_funcional="intensa",  # +2
        espera_cirurgica_meses=15  # > 12, +2
    )
    idade_max = 9  # <= 10, +2
    escore_max = calcular_escore(consulta_max, idade_max)
    prioridade_max = classificar_prioridade(escore_max)

    print(
        f"Caso Mínimo | Escore: {escore_min:<2} | Prioridade: {prioridade_min}")
    print(
        f"Caso Máximo | Escore: {escore_max:<2} | Prioridade: {prioridade_max}")

    # Verificar distribuição das prioridades
    print("\n=== DISTRIBUIÇÃO DE ESCORES/PRIORIDADES ===")
    print(f"Prioridade Eletiva: escore <= 9")
    print(f"Prioridade Intermediária: 9 < escore <= 15")
    print(f"Prioridade Alta: escore > 15")


def executar_todos_testes():
    """Executa todos os testes de escore"""
    testar_escore_tipo_escoliose()
    testar_escore_angulo_cobb()
    testar_escore_progressao()
    testar_escore_idade()
    testar_escore_risser()
    testar_escore_menarca()
    testar_escore_comorbidades()
    testar_escore_dor()
    testar_escore_espera()
    testar_casos_extremos()

    print("\n✅ Testes de cálculo de escore concluídos.")


# Executar o teste se o script for executado diretamente
if __name__ == "__main__":
    executar_todos_testes()
