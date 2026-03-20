import time

import sys
sys.setrecursionlimit(100000)

def recursive_function(n):
    """ Retornar o valor de n seguindo a formula 2F(n-1) + n^2

    Args:
        n: Número que será iterado recursivamente para retornar o valor

    Returns:
        n: Retorna o valor da soma da função utilizando o casoo base como F(1) == 2
    """
    if n == 1: return 2

    return 2 * recursive_function(n - 1) + n*n

n = input("Entre com um número para a função recursiva: ")
begin_function_recursive = time.time()
n_number = int(n)
result = recursive_function(n_number)
end_function_recursive = time.time()

duration_function_recursive = end_function_recursive - begin_function_recursive

print(f"{result} | {duration_function_recursive:>14.6f}s")
print("End! Vinícius von Glehn Severo | 2312130010")
