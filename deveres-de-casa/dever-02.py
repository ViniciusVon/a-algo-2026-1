import time
import random

# Tive que adicionar isso porque recebi erros de limite de recusão atingidos
import sys
sys.setrecursionlimit(10000)

def factorial_recursive (n):
    """Realiza o cálculo de um número fatorial recursivamente

    Algoritmo recursivo que utiliza a própria função para realizar os cálculos.

    Problem:
        O problema que encontrei está relacionado com a utilização simultânea da pilha por 
        utilizar a recursão. A complexidade é O(n), pois a recursão acontecerá n vezes até
        chegar ao valor final (n == 0).
    
    Args:
        n: Número que precisa ser calculado o fatorial

    Returns:
        number: Resultado encontrado a partir da multiplicação de todos os termos anteriores
    """
    if n == 0: 
        return 1
    else: 
        return n * factorial_recursive(n-1)
    
numbers = [10, 100, 500, 1000]

for n in numbers:
    # Begin Measure
    begin_factorial = time.time()
    
    result = factorial_recursive(n)
    # Finish Measure
    end_factorial = time.time()
    
    # Factorial Duration
    duration_factorial = end_factorial - begin_factorial
    print(f"{n:>8} | {duration_factorial:>14.6f}s")

print("End! Vinícius von Glehn Severo | 2312130010")
