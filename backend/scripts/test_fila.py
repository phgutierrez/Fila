# backend/scripts/test_fila.py
"""
Script para testar a ordenação da fila com diferentes critérios.
"""

from backend.services.fila_service import gerar_fila
import json
from datetime import date


def formatar_data(data_obj):
    if isinstance(data_obj, date):
        return data_obj.strftime("%d/%m/%Y")
    return data_obj


def mostrar_fila_formatada(fila):
    """Mostra a fila formatada com detalhes de cada paciente"""
    print("\n=== FILA ORDENADA ===")
    print(f"{'ID':<5} {'Nome':<20} {'Escore':<8} {'Prioridade':<15} {'Idade':<6} {'Primeira Consulta'}")
    print("-" * 80)

    for i, paciente in enumerate(fila, 1):
        print(f"{paciente['paciente_id']:<5} {paciente['nome'][:20]:<20} {paciente['escore']:<8} "
              f"{paciente['prioridade']:<15} {paciente['idade']:<6} {formatar_data(paciente['data_primeira_consulta'])}")


def teste_ordenacao_fila():
    print("Gerando fila com critérios combinados...")
    fila = gerar_fila()

    # Teste de ordenação: mostrar os pacientes ordenados
    mostrar_fila_formatada(fila)

    # Verificar se a ordenação está correta
    for i in range(len(fila) - 1):
        # Maior escore deve vir primeiro
        if fila[i]["escore"] < fila[i+1]["escore"]:
            print(
                f"\nAVISO: Escore fora de ordem! {fila[i]['escore']} vem antes de {fila[i+1]['escore']}")

        # Se escores são iguais, proximidade com 18 anos deve ser o critério
        elif fila[i]["escore"] == fila[i+1]["escore"]:
            if abs(fila[i]["idade"] - 18) > abs(fila[i+1]["idade"] - 18):
                print(f"\nAVISO: Idade fora de ordem! Idade {fila[i]['idade']} (distância de 18: {abs(fila[i]['idade'] - 18)}) "
                      f"vem antes de idade {fila[i+1]['idade']} (distância de 18: {abs(fila[i+1]['idade'] - 18)})")

    print("\n✅ Teste de ordenação da fila concluído.")

    return fila


# Executar o teste se o script for executado diretamente
if __name__ == "__main__":
    teste_ordenacao_fila()
