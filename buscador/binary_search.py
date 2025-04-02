import sys
import os
from pathlib import Path
from time import time

sys.path.append(str(Path(__file__).parent.parent))

from algoritmos_ordenacao.tim_sort import TimSort

def create_hash_table(arr):
    """Cria uma tabela hash (dicionário) com os valores e seus índices"""
    return {value: index for index, value in enumerate(arr)}

def load_unordered_list(filename):
    """Lê um arquivo de texto com um número por linha e retorna uma lista de inteiros."""
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file if line.strip()]

def get_user_input():
    """Obtém o valor alvo da entrada do usuário com validação."""
    while True:
        user_input = input("Digite o número que deseja buscar (ou 'sair' para terminar): ")
        if user_input.lower() == 'sair':
            return None
        try:
            return int(user_input)
        except ValueError:
            print("Por favor, digite um número inteiro válido.")

if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    filename = project_root / 'dados' / 'dados_100000.txt'
    
    try:
        unordered_data = load_unordered_list(filename)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {filename}")
        print("Verifique se o arquivo existe e o caminho está correto")
        exit(1)
    
    print("\nOrdenando dados com TimSort...")
    start_time = time()
    tim_sorter = TimSort()
    sorted_data, comparacoes, trocas = tim_sorter.ordenar(unordered_data.copy())
    sort_time = (time() - start_time) * 1000
    
    print(f"Dados ordenados (amostra): {sorted_data[:5]}...{sorted_data[-5:]}")
    print(f"Tempo de ordenação: {sort_time:.2f}ms")
    print(f"Comparações: {comparacoes}, Trocas: {trocas}")
    
    print("\nCriando tabela hash...")
    start_time = time()
    hash_table = create_hash_table(sorted_data)
    hash_time = (time() - start_time) * 1000
    print(f"Tabela hash criada em {hash_time:.2f}ms")
    print(f"Tamanho da tabela: {len(hash_table)} elementos\n")
    
    while True:
        target = get_user_input()
        if target is None:
            print("Encerrando o programa...")
            break
        
        start_time = time()
        index = hash_table.get(target, -1)
        search_time = (time() - start_time) * 1000
        
        if index != -1:
            print(f"✅ Valor {target} encontrado no índice {index}")
            print(f"Tempo de busca: {search_time:.6f}ms\n")
        else:
            print(f"❌ Valor {target} não encontrado")
            print(f"Tempo de busca: {search_time:.6f}ms\n")