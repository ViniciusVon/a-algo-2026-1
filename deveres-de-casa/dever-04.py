"""
Módulo para resolução da recorrência T(k) = 2·T(k-1) + k², com T(1) = 2.

A forma fechada equivalente é:
    T(k) = 13 · 2^(k-1) - k² - 4k - 6

Dedução:
    - Componente homogênea de T(k) = 2·T(k-1): α · 2^k
    - Componente particular para k² (palpite Ak² + Bk + C):
        A = -1, B = -4, C = -6
    - Forma geral: T(k) = α · 2^k - k² - 4k - 6
    - Condição inicial T(1) = 2: 2α - 1 - 4 - 6 = 2 → α = 13/2
    - Reescrevendo: T(k) = 13 · 2^(k-1) - k² - 4k - 6

Custo recursivo: O(2^k) — não recomendado para k elevado.
Custo da forma fechada: O(1).
"""
from math import pow as potencia

VALOR_INICIAL = 2
INDICE_INICIAL = 1


def resolver_por_recorrencia(k):
    """
    Obtém T(k) aplicando recursão direta da definição:
        T(k) = 2 · T(k-1) + k²
        T(1) = 2

    Args:
        k (int): Índice inteiro positivo desejado.

    Returns:
        int: O valor de T(k).

    Raises:
        ValueError: Quando k é inferior a 1.

    """
    if k < INDICE_INICIAL:
        raise ValueError(f"k precisa ser pelo menos {INDICE_INICIAL}.")
    if k == INDICE_INICIAL:
        return VALOR_INICIAL
    return 2 * resolver_por_recorrencia(k - 1) + k ** 2


def resolver_por_formula(k):
    """
    Obtém T(k) através da expressão fechada deduzida da recorrência:
        T(k) = 13 · 2^(k-1) - k² - 4k - 6

    Resultado da resolução de T(k) = 2·T(k-1) + k² com T(1) = 2.
    Emprega math.pow para a exponenciação.
    Custo: O(1).

    Args:
        k (int): Índice inteiro positivo desejado.

    Returns:
        int: O valor de T(k).

    Raises:
        ValueError: Quando k é inferior a 1.
    """
    if k < INDICE_INICIAL:
        raise ValueError(f"k precisa ser pelo menos {INDICE_INICIAL}.")
    saida = 13 * potencia(2, k - 1) - k ** 2 - 4 * k - 6
    return int(saida)


def obter_entrada_usuario():
    """
    Obtém do usuário um inteiro positivo correspondente a k.

    Insiste na leitura até receber uma resposta válida (inteiro >= 1).

    Returns:
        int: O valor de k informado pelo usuário.
    """
    while True:
        texto_digitado = input("\nInforme o valor de k (inteiro positivo): ")
        try:
            valor_convertido = int(texto_digitado)
            if valor_convertido < INDICE_INICIAL:
                print(f"Aviso: k precisa ser pelo menos {INDICE_INICIAL}. Repita a operação.")
            else:
                return valor_convertido
        except ValueError:
            print("Aviso: valor inválido. Forneça um número inteiro.")


def executar():
    """
    Rotina principal: coleta k do usuário e mostra T(k) pelos dois caminhos.

    Determina T(k) tanto via recorrência quanto via forma fechada,
    permitindo o confronto dos resultados para validação.
    """
    print("=== Resolução da Recorrência T(k) = 2·T(k-1) + k² ===")
    indice_k = obter_entrada_usuario()
    saida_recorrencia = resolver_por_recorrencia(indice_k)
    saida_formula = resolver_por_formula(indice_k)
    print(f"\nT({indice_k}) via recorrência:   {saida_recorrencia}")
    print(f"T({indice_k}) via forma fechada: {saida_formula}")


if __name__ == "__main__":
    executar()