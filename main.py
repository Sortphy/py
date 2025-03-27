import time
import concurrent.futures
from algoritmos_ordenacao import estrategias

def carregar_dados(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return [int(linha) for linha in f]

def executar_algoritmo(estrategia, dados):
    inicio = time.time()
    dados_ordenados, comparacoes, trocas = estrategia.ordenar(dados.copy())
    fim = time.time()
    tempo_execucao = (fim - inicio) * 1000
    return tempo_execucao, comparacoes, trocas

def executar_algoritmo_thread(nome, estrategia, dados, repeticoes):
    tempos = []
    comparacoes_total = 0
    trocas_total = 0

    for _ in range(repeticoes):
        tempo, comparacoes, trocas = executar_algoritmo(estrategia, dados)
        tempos.append(tempo)
        comparacoes_total += comparacoes
        trocas_total += trocas

    return nome, {
        "tempo_medio": sum(tempos) / repeticoes,
        "comparacoes_media": comparacoes_total / repeticoes,
        "trocas_media": trocas_total / repeticoes,
    }

def comparar_algoritmos(nome_arquivo, repeticoes=5):
    dados = carregar_dados(nome_arquivo)
    resultados = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = {
            executor.submit(executar_algoritmo_thread, nome, estrategia, dados, repeticoes): nome
            for nome, estrategia in estrategias.items()
        }

        for futuro in concurrent.futures.as_completed(futuros):
            nome = futuros[futuro]
            resultados[nome] = futuro.result()[1]

    return resultados
