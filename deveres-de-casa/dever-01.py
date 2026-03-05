import time
import random

def insertion_sort(array):
    """Ordena uma lista usando o algoritmo Insertion Sort

    Algoritmo de ordenação de complexidade O(n²) na qual verifica todas
    as casas com a casa atual até encontrar o local em que se deve inserir
    o número.

    Args:
        array: Lista de elementos que serão comparados e ordenados
    
    Returns:
        array: A mesma lista que foi recebida, porém ordenada em ordem crescente.
    """
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j>=0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array

sizes = [1000, 5000, 10000, 20000, 50000]

for n in sizes:
    original_array = random.sample(range(n * 10), n)

    # Insertion Sort
    copy_array_is = original_array.copy()
    begin_is = time.time()
    insertion_sort(copy_array_is)
    end_is = time.time()
    is_time = end_is - begin_is

    # Sorted
    copy_array_sorted = original_array.copy()
    begin_sorted = time.time()
    sorted(copy_array_is)
    end_sorted = time.time()
    sorted_time = end_sorted - begin_sorted

    print(f"{n:>8} | {is_time:>14.6f}s | {sorted_time:>14.6f}s")

print("End! Vinícius von Glehn Severo | 2312130010")