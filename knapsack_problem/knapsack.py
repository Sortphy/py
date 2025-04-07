
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

import matplotlib.pyplot as plt

class Node:
    def __init__(self, label, value, x=0, y=0):
        self.label = label
        self.value = value
        self.x = x
        self.y = y
        self.children = []

def knapsack_visual(items, capacity):
    memo = {}
    counter = {'count': 0}

    def helper(index, capacity, depth, x_offset):
        key = (index, capacity)
        counter['count'] += 1
        node_label = f'i:{index} c:{capacity}'
        
        if key in memo:
            value = memo[key]
            node = Node(node_label + f'\ncache:{value}', value, x_offset, -depth)
            return value, node

        if index >= len(items) or capacity <= 0:
            node = Node(node_label + '\nret: 0', 0, x_offset, -depth)
            return 0, node

        weight, value = items[index]
        left_value, left_node = helper(index + 1, capacity, depth + 1, x_offset - 1.5 ** (4 - depth))

        if weight <= capacity:
            right_value, right_node = helper(index + 1, capacity - weight, depth + 1, x_offset + 1.5 ** (4 - depth))
            result = max(left_value, value + right_value)
        else:
            right_node = None
            result = left_value

        memo[key] = result
        node = Node(node_label + f'\nret: {result}', result, x_offset, -depth)
        node.children.append(left_node)
        if right_node:
            node.children.append(right_node)

        return result, node

    result, root_node = helper(0, capacity, 0, 0)
    return result, root_node

def draw_tree(node, ax):
    ax.text(node.x, node.y, node.label, ha='center', bbox=dict(boxstyle="round", fc="lightblue"))
    for child in node.children:
        ax.plot([node.x, child.x], [node.y, child.y], 'k-')
        draw_tree(child, ax)

if __name__ == "__main__":
    items = [(2, 3), (1, 2), (3, 4), (2, 2)]
    capacity = 5

    print("gerando visualização com matplotlib...")
    result, root = knapsack_visual(items, capacity)
    print(f"valor máximo: {result}")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    draw_tree(root, ax)
    plt.title("Árvore de chamadas do Problema da Mochila")
    plt.tight_layout()
    plt.show()
