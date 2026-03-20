import time
import random

# Tive que adicionar isso porque recebi erros de limite de recusão atingidos
import sys
sys.setrecursionlimit(1000000)

def is_palindrome(array, inicio, fim):
    """Verifica se a o array é um palindromo

    Algoritmo recursivo que utiliza a própria função para realizar as verificações.

    Problem:
        O problema que encontrei está relacionado com a utilização simultânea da pilha por 
        utilizar a recursão. A complexidade é O(n), pois a recursão acontecerá n vezes até
        chegar ao valor final (n == 0).
    
    Args:
        array: Array que irei percorrer para realizar as verificações

    Returns:
        boolean: Resultado lógico contendo a veracidade se um array é palíndromo ou não 
    """
    if inicio >= fim:
        return True
    
    if array[inicio] != array[fim]:
        return False
    
    return is_palindrome(array, inicio + 1, fim - 1)

def generate_palindrome(length):
    if length <= 0:
        return []
    
    half = length // 2
    half_elements = [random.randint(1, 100) for _ in range(half)]
    
    if length % 2 == 0:
        array = half_elements + half_elements[::-1]
    else:
        middle = random.randint(1, 100)
        array = half_elements + [middle] + half_elements[::-1]
    
    return array

  
array_false = ["b", "b", "a", "b"]    

arrays = [generate_palindrome(50), generate_palindrome(10000), generate_palindrome(100000), array_false]

for n in arrays:
    # Begin Measure
    begin_is_palindrome = time.time()
    
    result = is_palindrome(n, 0, len(n) - 1)
    # Finish Measure
    end_is_palindrome = time.time()
    
    # is_palindrome Duration
    duration_is_palindrome = end_is_palindrome - begin_is_palindrome
    print(f"{result} | {duration_is_palindrome:>14.6f}s")

print("End! Vinícius von Glehn Severo | 2312130010")
