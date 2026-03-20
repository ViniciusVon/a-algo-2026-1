import time

def recursion_function_1(n):
    """ Função recursiva que utiliza a função F(n) = F(n-1) + n + 1 com caso base F(0) = 1

    Args:
        n: Número a ser calculado a partir da função recursiva

    Returns:
        result: Valor calculado recursivamente pela função acima
    """
    if n == 0: return 1

    return recursion_function_1(n-1) + n + 1

def recursion_function_2(n):
    """ Função recursiva que utiliza a função F(n) = F(n-1) + 3*n + 2 com caso base F(1) = 1

    Args:
        n: Número a ser calculado a partir da função recursiva

    Returns:
        result: Valor calculado recursivamente pela função acima
    """
    if n == 1: return 1

    return recursion_function_2(n-1) + 3*n + 2

begin_recursion_time_1 = time.time()
result_1 = recursion_function_1(10)
end_recursion_time_1 = time.time()


begin_recursion_time_2 = time.time()
result_2 = recursion_function_2(6)
end_recursion_time_2 = time.time()

duration_recursion_function_1 = end_recursion_time_1 - begin_recursion_time_1
duration_recursion_function_2 = end_recursion_time_2 - begin_recursion_time_2

print("Recursion 1 \n")
print(f"{result_1} | {duration_recursion_function_1:>14.6f}s")
print("Recursion 2 \n")
print(f"{result_2} | {duration_recursion_function_2:>14.6f}s")
