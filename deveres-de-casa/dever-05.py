from math import log as logaritmo


# =============================================================================
# 1. ORDENAÇÃO POR INTERCALAÇÃO
# =============================================================================

def ordenar_por_intercalacao(sequencia: list) -> list:
    """Realiza a ordenação de uma sequência por meio do Merge Sort.

    Análise de custo:
        - Recorrência associada: C(n) = 2C(n/2) + n
        - Aplicando o Teorema Mestre: a=2, b=2, f(n)=n
          log_b(a) = log_2(2) = 1  =>  n^1 = n = f(n)  =>  Caso 2
        - Conclusão: C(n) = Θ(n log n)

    Args:
        sequencia: Coleção de elementos comparáveis a ordenar.

    Returns:
        Nova sequência ordenada de forma crescente.
    """
    tamanho = len(sequencia)
    if tamanho <= 1:
        return sequencia

    ponto_medio = tamanho // 2
    metade_inferior = ordenar_por_intercalacao(sequencia[:ponto_medio])
    metade_superior = ordenar_por_intercalacao(sequencia[ponto_medio:])

    return _intercalar(metade_inferior, metade_superior)


def _intercalar(parte_a: list, parte_b: list) -> list:
    """Funde duas sequências previamente ordenadas em uma única ordenada.

    Args:
        parte_a: Sequência ordenada (lado esquerdo).
        parte_b: Sequência ordenada (lado direito).

    Returns:
        Sequência única contendo todos os elementos em ordem.
    """
    saida = []
    indice_a = indice_b = 0
    tam_a, tam_b = len(parte_a), len(parte_b)

    while indice_a < tam_a and indice_b < tam_b:
        if parte_a[indice_a] <= parte_b[indice_b]:
            saida.append(parte_a[indice_a])
            indice_a += 1
        else:
            saida.append(parte_b[indice_b])
            indice_b += 1

    saida.extend(parte_a[indice_a:])
    saida.extend(parte_b[indice_b:])
    return saida


# =============================================================================
# 2. PRODUTO DE MATRIZES
# =============================================================================

def produto_matricial(matriz_x: list[list[float]],
                      matriz_y: list[list[float]]) -> list[list[float]]:
    """Executa o produto entre duas matrizes pelo método tradicional.

    Análise de custo:
        - Três laços encadeados, cada um de tamanho n
        - C(n) = Θ(n³)

    Args:
        matriz_x: Matriz de ordem m x n.
        matriz_y: Matriz de ordem n x p.

    Returns:
        Matriz produto, de ordem m x p.

    Raises:
        ValueError: Quando o número de colunas de X difere do número
            de linhas de Y.
    """
    qtd_linhas_x = len(matriz_x)
    qtd_colunas_x = len(matriz_x[0])
    qtd_linhas_y = len(matriz_y)
    qtd_colunas_y = len(matriz_y[0])

    if qtd_colunas_x != qtd_linhas_y:
        raise ValueError(
            f"Ordens incompatíveis: X possui {qtd_colunas_x} colunas "
            f"enquanto Y possui {qtd_linhas_y} linhas."
        )

    produto = [[0.0] * qtd_colunas_y for _ in range(qtd_linhas_x)]

    for linha in range(qtd_linhas_x):           # O(n)
        for coluna in range(qtd_colunas_y):     # O(n)
            for indice in range(qtd_colunas_x): # O(n)
                produto[linha][coluna] += matriz_x[linha][indice] * matriz_y[indice][coluna]

    return produto


# =============================================================================
# 3. ESTUDO DE RECORRÊNCIAS VIA TEOREMA MESTRE
# =============================================================================

def avaliar_recorrencia_mestre(subproblemas: int, divisor: int,
                               rotulo_f: str, expoente_f: float) -> dict:
    """Avalia uma recorrência C(n) = a·C(n/b) + f(n) pelo Teorema Mestre.

    O Teorema Mestre compara f(n) = n^expoente_f contra n^(log_b(a)):
        - Caso 1: f(n) = O(n^(log_b(a) - ε))  =>  C(n) = Θ(n^log_b(a))
        - Caso 2: f(n) = Θ(n^log_b(a))         =>  C(n) = Θ(n^log_b(a) · log n)
        - Caso 3: f(n) = Ω(n^(log_b(a) + ε))  =>  C(n) = Θ(f(n))

    Args:
        subproblemas: Quantidade de subproblemas gerados (a >= 1).
        divisor: Fator pelo qual o tamanho é reduzido (b > 1).
        rotulo_f: Descrição textual de f(n), ex: "sqrt(n)", "n", "n^2".
        expoente_f: Expoente de n em f(n), ex: 0.5 para sqrt(n), 1 para n.

    Returns:
        Dicionário com as chaves:
            - 'log_b_a': resultado de log_b(a)
            - 'caso': caso identificado do Teorema Mestre (1, 2 ou 3)
            - 'complexidade': string descrevendo a complexidade obtida

    """
    valor_log = logaritmo(subproblemas, divisor)
    diferenca = expoente_f - valor_log  # positivo => caso 3, zero => caso 2, neg => caso 1

    if abs(diferenca) < 1e-9:
        caso_identificado = 2
        descricao_complexidade = f"Θ(n^{valor_log:.4g} · log n)"
    elif diferenca < 0:
        caso_identificado = 1
        descricao_complexidade = f"Θ(n^{valor_log:.4g})"
    else:
        caso_identificado = 3
        descricao_complexidade = f"Θ({rotulo_f})"

    return {
        "log_b_a": valor_log,
        "caso": caso_identificado,
        "complexidade": descricao_complexidade,
    }


# =============================================================================
# APRESENTAÇÃO DOS RESULTADOS
# =============================================================================

def apresentar_merge_sort() -> None:
    """Exibe o funcionamento e o custo do Merge Sort."""
    print("=" * 60)
    print("1. MERGE SORT")
    print("=" * 60)
    print("Recorrência : C(n) = 2C(n/2) + n")
    print("Teorema Mestre: a=2, b=2, f(n)=n")
    print(f"  log_b(a)  = log_2(2) = {logaritmo(2, 2):.1f}")
    print("  f(n) = n^1 = n^log_b(a)  =>  Caso 2")
    print("Complexidade: Θ(n log n)\n")

    amostra = [38, 27, 43, 3, 9, 82, 10]
    sequencia_ordenada = ordenar_por_intercalacao(amostra)
    print(f"  Entrada : {amostra}")
    print(f"  Saída   : {sequencia_ordenada}\n")


def apresentar_produto_matrizes() -> None:
    """Exibe o funcionamento e o custo do produto matricial."""
    print("=" * 60)
    print("2. MULTIPLICAÇÃO DE MATRIZES")
    print("=" * 60)
    print("Três laços encadeados de tamanho n")
    print("Complexidade: Θ(n³)\n")

    primeira = [[1, 2, 3],
                [4, 5, 6]]
    segunda = [[7,  8],
               [9,  10],
               [11, 12]]

    matriz_produto = produto_matricial(primeira, segunda)
    print("  Matriz X (2x3):")
    for linha_atual in primeira:
        print(f"    {linha_atual}")
    print("  Matriz Y (3x2):")
    for linha_atual in segunda:
        print(f"    {linha_atual}")
    print("  Resultado X×Y (2x2):")
    for linha_atual in matriz_produto:
        print(f"    {linha_atual}\n")


def apresentar_recorrencias() -> None:
    """Avalia as três recorrências aplicando o Teorema Mestre."""
    print("=" * 60)
    print("3. RECORRÊNCIAS (Teorema Mestre)")
    print("=" * 60)

    lista_recorrencias = [
        (2,  4, "sqrt(n)", 0.5, "C(n) = 2C(n/4) + √n"),
        (2,  4, "n",       1.0, "C(n) = 2C(n/4) + n"),
        (16, 4, "n^2",     2.0, "C(n) = 16C(n/4) + n²"),
    ]

    for subprobs, div, rotulo, expo, enunciado in lista_recorrencias:
        resultado_analise = avaliar_recorrencia_mestre(subprobs, div, rotulo, expo)
        print(f"  Recorrência : {enunciado}")
        print(f"  Parâmetros  : a={subprobs}, b={div}, f(n)={rotulo}")
        print(f"  log_{div}({subprobs})    = {resultado_analise['log_b_a']:.4g}")
        print(f"  Caso        : {resultado_analise['caso']}")
        print(f"  Complexidade: {resultado_analise['complexidade']}\n")


def executar() -> None:
    """Função inicial — dispara todas as apresentações."""
    apresentar_merge_sort()
    apresentar_produto_matrizes()
    apresentar_recorrencias()


if __name__ == "__main__":
    executar()