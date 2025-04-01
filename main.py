import time
import concurrent.futures
import os
from opentelemetry import trace
from algoritmos_ordenacao import estrategias
from registrar_logs import registrar_logs

# Configura o tracer
tracer = trace.get_tracer(__name__)

def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo com tratamento de erros e tracing."""
    with tracer.start_as_current_span("carregar_dados") as span:
        try:
            # Verifica se o caminho existe
            caminho_completo = os.path.join(os.path.dirname(__file__), nome_arquivo)
            span.set_attribute("caminho_arquivo", caminho_completo)
            
            if not os.path.exists(caminho_completo):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_completo}")
                
            with open(caminho_completo, 'r') as f:
                dados = [int(linha.strip()) for linha in f if linha.strip()]
                
            span.set_attributes({
                "tamanho_dados": len(dados),
                "primeiro_valor": dados[0] if dados else None,
                "ultimo_valor": dados[-1] if dados else None
            })
            return dados
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise

def executar_algoritmo(estrategia, dados):
    """Executa um algoritmo de ordenação com tracing."""
    with tracer.start_as_current_span("executar_algoritmo") as span:
        try:
            inicio = time.time()
            dados_ordenados, comparacoes, trocas = estrategia.ordenar(dados.copy())
            fim = time.time()
            tempo_execucao = (fim - inicio) * 1000
            
            span.set_attributes({
                "algoritmo": type(estrategia).__name__,
                "tamanho_dados": len(dados),
                "tempo_execucao_ms": tempo_execucao,
                "comparacoes": comparacoes,
                "trocas": trocas
            })
            return tempo_execucao, comparacoes, trocas
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise

def executar_algoritmo_thread(nome, estrategia, dados, repeticoes):
    """Executa múltiplas iterações em thread separada com tracing."""
    with tracer.start_as_current_span(f"thread_{nome}") as span:
        tempos = []
        comparacoes_total = 0
        trocas_total = 0

        for i in range(repeticoes):
            with tracer.start_as_current_span(f"execucao_{i+1}") as exec_span:
                try:
                    tempo, comparacoes, trocas = executar_algoritmo(estrategia, dados)
                    tempos.append(tempo)
                    comparacoes_total += comparacoes
                    trocas_total += trocas
                    
                    exec_span.set_attributes({
                        "iteracao": i+1,
                        "tempo_execucao": tempo,
                        "comparacoes": comparacoes,
                        "trocas": trocas
                    })
                except Exception as e:
                    exec_span.record_exception(e)
                    exec_span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    raise

        return nome, {
            "tempo_medio": sum(tempos) / repeticoes,
            "comparacoes_media": comparacoes_total / repeticoes,
            "trocas_media": trocas_total / repeticoes,
        }

def comparar_algoritmos(nome_arquivo, repeticoes=5):
    """Função principal que compara todos os algoritmos."""
    with tracer.start_as_current_span("comparar_algoritmos") as root_span:
        try:
            dados = carregar_dados(nome_arquivo)
            root_span.set_attributes({
                "arquivo_entrada": nome_arquivo,
                "tamanho_dataset": len(dados),
                "repeticoes": repeticoes
            })

            resultados = {}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futuros = {
                    executor.submit(executar_algoritmo_thread, nome, estrategia, dados, repeticoes): nome
                    for nome, estrategia in estrategias.items()
                }

                for futuro in concurrent.futures.as_completed(futuros):
                    nome = futuros[futuro]
                    resultado = futuro.result()
                    resultados[nome] = resultado[1]
                    
                    registrar_logs(
                        nome_algoritmo=nome,
                        tamanho_dados=len(dados),
                        tempo_execucao=resultado[1]["tempo_medio"],
                        comparacoes=resultado[1]["comparacoes_media"],
                        trocas=resultado[1]["trocas_media"]
                    )

            return resultados
            
        except Exception as e:
            root_span.record_exception(e)
            root_span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise

if __name__ == "__main__":
    try:
        # Configura caminhos relativos
        diretorio_atual = os.path.dirname(__file__)
        pasta_dados = os.path.join(diretorio_atual, "dados")
        arquivo_dados = os.path.join(pasta_dados, "entrada.txt")
        
        # Verifica e cria estrutura de diretórios se necessário
        if not os.path.exists(pasta_dados):
            os.makedirs(pasta_dados)
            print(f"Diretório 'dados' criado em: {pasta_dados}")
            
        if not os.path.exists(arquivo_dados):
            # Cria um arquivo de exemplo se não existir
            with open(arquivo_dados, "w") as f:
                f.write("10\n5\n2\n8\n1\n15\n3\n7\n4\n9\n6\n")
            print(f"Arquivo de exemplo criado em: {arquivo_dados}")
        
        print(f"\nIniciando comparação de algoritmos com dados de: {arquivo_dados}")
        resultados = comparar_algoritmos(arquivo_dados, repeticoes=3)
        
        print("\nResultados finais:")
        for nome, metricas in sorted(resultados.items(), key=lambda x: x[1]["tempo_medio"]):
            print(f"{nome.ljust(20)}: {metricas['tempo_medio']:.2f} ms | "
                  f"Comparações: {metricas['comparacoes_media']:.0f} | "
                  f"Trocas: {metricas['trocas_media']:.0f}")
                  
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")
    finally:
        trace.get_tracer_provider().shutdown()