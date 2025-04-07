
# A gente escolheu resolver o Problema da Mochila, que é bem conhecido na área da computação.
# A ideia é imaginar que temos uma mochila com um limite de peso e vários itens com pesos e valores diferentes.
# O desafio é decidir quais itens colocar na mochila para que o valor total seja o maior possível, sem ultrapassar o peso.
# Para isso, usamos uma solução recursiva com memoization, o que significa que a gente chama a função de forma repetida
# para testar diferentes combinações, mas guardando os resultados que já foram calculados antes.
# Assim, se a gente encontrar o mesmo problema de novo, não precisa recalcular — é só pegar o valor guardado.

# Esse "guarda os resultados" é feito com um dicionário do Python, que funciona como uma tabela de consulta bem rápida.
# A chave desse dicionário é uma combinação do índice do item atual com a capacidade restante da mochila,
# e o valor é o melhor resultado encontrado até ali.
# Com isso, a gente consegue evitar chamadas repetidas e economizar muito tempo de execução,
# deixando o algoritmo mais eficiente.
# A recursividade ajuda a explorar todas as possibilidades de escolha,
# enquanto a memoization garante que cada situação só é resolvida uma vez.
# Foi uma forma interessante de aplicar programação dinâmica na prática.

# O código abaixo implementa essa solução.

# Problema da Mochila (Knapsack Problem) com Recursão e Memoization

def knapsack(items, capacity, index=0, memo=None):
    if memo is None:
        memo = {}

    # cria uma chave única com base no índice do item e na capacidade restante
    key = (index, capacity)

    # verifica se esse subproblema já foi resolvido antes
    if key in memo:
        print(f"usando valor em cache para key={key}")
        return memo[key]

    # caso base: sem itens ou capacidade restante
    if index >= len(items) or capacity <= 0:
        return 0

    weight, value = items[index]

    print(f"analisando item {index} com peso={weight}, valor={value} e capacidade restante={capacity}")

    # opção 1: não incluir o item atual
    not_taken = knapsack(items, capacity, index + 1, memo)

    # opção 2: incluir o item atual (se couber na mochila)
    if weight <= capacity:
        taken = value + knapsack(items, capacity - weight, index + 1, memo)
        result = max(taken, not_taken)
        print(f"comparando: incluir={taken} vs não incluir={not_taken} => escolhido={result}")
    else:
        result = not_taken
        print(f"item {index} não cabe na mochila (peso={weight}), pulando")

    # armazena o resultado no cache
    memo[key] = result
    return result


if __name__ == "__main__":
    # lista de itens (peso, valor)
    itens = [(2, 3), (1, 2), (3, 4), (2, 2)]
    capacidade_mochila = 5

    print("iniciando resolução do problema da mochila com recursão e memoization...\n")
    valor_maximo = knapsack(itens, capacidade_mochila)
    print(f"\nvalor máximo que pode ser carregado: {valor_maximo}")
