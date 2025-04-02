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

if __name__ == '__main__':
    # Load unordered numbers from the text file
    filename = 'unordered.txt'
    unordered_data = load_unordered_list(filename)
    
    # Sort the list using TimSort
    tim_sorter = TimSort()
    sorted_data, comparacoes, trocas = tim_sorter.ordenar(unordered_data)
    print("Sorted list:", sorted_data)
    print("Comparisons:", comparacoes, "Swaps:", trocas)
    
    # Search for the target using binary search
    target = 7189
    index = binary_search(sorted_data, target)
    if index != -1:
        print(f"Target {target} found at index {index}")
    else:
        print(f"Target {target} not found")
