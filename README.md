# Projeto de Comparação de Algoritmos de Ordenação

Este projeto implementa, compara e analisa a performance de diferentes algoritmos de ordenação, utilizando o padrão de projeto **Strategy** para modularidade e **OpenTelemetry** para coleta de métricas e logs.

---

## Algoritmos Implementados

### Básicos
- Bubble Sort
- Bubble Sort Melhorado
- Insertion Sort
- Selection Sort

### Avançados (Dividir para Conquistar)
- Quick Sort
- Merge Sort
- Tim Sort

---

## Requisitos

Certifique-se de ter instalado:

- Python 3.8 ou superior
- Gerenciador de pacotes `pip`

---

## Instalação

1. Clone o repositório:

  ```bash
  git clone <URL_DO_REPOSITORIO>
  cd <NOME_DO_REPOSITORIO>
  ```

2. Instale as dependências:

  ```bash
  pip install -r requirements.txt
  ```

---

## Como Executar o Projeto

### 1. Gerar Dados Aleatórios

Execute o script `gerador_dados.py` para criar conjuntos de números aleatórios:

```bash
python gerador_dados.py
```

### 2. Executar os Algoritmos de Ordenação

Execute o script `main.py` para rodar os algoritmos e coletar métricas de desempenho:

```bash
python main.py
```

O que acontece durante a execução:
- Os algoritmos são aplicados a cada conjunto de dados.
- Métricas como tempo de execução, número de comparações e trocas são coletadas.
- Logs são gerados utilizando o OpenTelemetry.

### 3. Visualizar Logs e Métricas

Os logs são exibidos no console e podem ser enviados para o Jaeger para análise.

#### Configuração do Jaeger

Inicie o Jaeger com Docker:

```bash
docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 -p 5775:5775/udp -p 6831:6831/udp -p 6832:6832/udp -p 5778:5778 -p 16686:16686 -p 14268:14268 -p 9411:9411 jaegertracing/all-in-one:1.21
```

Acesse o Jaeger no navegador:

[http://localhost:16686](http://localhost:16686)

Procure pelos traces gerados pelo projeto.

---

## Resultados

Após a execução, os resultados incluem:
- Tempo de execução (em milissegundos)
- Número de comparações realizadas
- Número de trocas/movimentações realizadas

Os resultados são exibidos no console e registrados no Jaeger para análise detalhada.
