from gerar_set import generate_ordered_set



def binary_search(ordered_set, objetivo, left=0, right=None):
    if right is None:
        right = len(ordered_set) - 1

    if left > right:
        return -1  # nao achou

    mid = (left + right) // 2

    if ordered_set[mid] == objetivo:
        return mid  # achou, retorna o index
    elif ordered_set[mid] < objetivo:
        return binary_search(ordered_set, objetivo, mid + 1, right)  # buscar lado direito
    else:
        return binary_search(ordered_set, objetivo, left, mid - 1)  # buscar lado esquerdo



set_ordenado = generate_ordered_set()

objetivo = 7189

result = binary_search(set_ordenado, objetivo)

