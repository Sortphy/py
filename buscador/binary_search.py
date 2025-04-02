import sys
import os
from pathlib import Path

# Adiciona o diretório pai ao Python path
sys.path.append(str(Path(__file__).parent.parent))

from algoritmos_ordenacao.tim_sort import TimSort

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def load_unordered_list(filename):
    """Reads a text file with one number per line and returns a list of integers."""
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file if line.strip()]

def get_user_input():
    """Gets target value from command line input with validation."""
    while True:
        user_input = input("Digite o número que deseja buscar (ou 'sair' para terminar): ")
        if user_input.lower() == 'sair':
            return None
        try:
            return int(user_input)
        except ValueError:
            print("Por favor, digite um número inteiro válido.")

if __name__ == '__main__':
    # Caminho corrigido para os dados
    project_root = Path(__file__).parent.parent
    filename = project_root / 'dados' / 'dados_100000.txt'
    
    # Carrega os dados
    try:
        unordered_data = load_unordered_list(filename)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {filename}")
        print("Verifique se o arquivo existe e o caminho está correto")
        exit(1)
    
    # Ordena com TimSort
    tim_sorter = TimSort()
    sorted_data, comparacoes, trocas = tim_sorter.ordenar(unordered_data.copy())
    
    print(f"\nDados ordenados (amostra): {sorted_data[:5]}...{sorted_data[-5:]}")
    print(f"Comparações: {comparacoes}, Trocas: {trocas}\n")
    
    # Loop para permitir múltiplas buscas
    while True:
        target = get_user_input()
        if target is None:
            print("Encerrando o programa...")
            break
        
        index = binary_search(sorted_data, target)
        
        if index != -1:
            print(f"✅ Valor {target} encontrado no índice {index}\n")
        else:
            print(f"❌ Valor {target} não encontrado\n")