"""
Dever de Casa 07 - O Desafio do Pronto-Socorro
==============================================
Implementação computacional de um mecanismo de classificação de risco
em ambiente hospitalar valendo-se de uma Heap Máxima para ordenar o
atendimento conforme a intensidade da dor manifestada (escala 1-10).

Capacidades desta solução:
    1. Cadastramento de N enfermos acompanhados da intensidade da dor.
    2. Encaminhamento conforme ordem de prioridade via Heap Máxima.
    3. Atualização da prioridade de enfermo previamente cadastrado
       (equivalente funcional das operações Decrease-Key e Increase-Key).
    4. Reflexão acerca do custo computacional das rotinas oferecidas.

Custos computacionais resumidos:
    - inscrever (push)                    : O(log n)
    - encaminhar (extract-max)            : O(log n)
    - atualizar_prioridade (com mapa)     : O(log n)
    - achar enfermo pelo identificador    : O(1) via dicionário de apoio
                                            ou O(n) via percorrimento linear
    - montagem do heap a partir de lista  : O(n)  (heapify bottom-up)

Comentário relevante:
    Numa heap implementada apenas como vetor, a busca por elemento
    arbitrário consome O(n). Para que a alteração de prioridade seja
    de fato O(log n), torna-se obrigatório preservar uma estrutura
    auxiliar (identificador_enfermo -> índice corrente no heap) que
    se mantenha íntegra após cada permutação durante sift-up / sift-down.
    Foi este o caminho seguido aqui.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# =============================================================================
# VALORES-LIMITE DA APLICAÇÃO
# =============================================================================

LIMITE_INFERIOR_DOR = 1
LIMITE_SUPERIOR_DOR = 10


# =============================================================================
# ABSTRAÇÃO DO ENFERMO
# =============================================================================

@dataclass
class FichaEnfermo:
    """Encapsula os dados de um enfermo aguardando atendimento.

    Attributes:
        identificador: Número único atribuído ao enfermo (sequencial).
        nome_paciente: Nome do enfermo no sistema.
        grau_dor: Grau de dor declarado pelo enfermo (1 a 10).
        sequencia_entrada: Marca temporal de chegada — serve para resolver
            empates quando dois enfermos possuem grau de dor coincidente,
            preservando a regra FIFO entre prioridades iguais.
    """

    identificador: int
    nome_paciente: str
    grau_dor: int
    sequencia_entrada: int = field(default=0)

    def __post_init__(self) -> None:
        """Avalia se o grau de dor informado respeita os limites aceitos."""
        if not (LIMITE_INFERIOR_DOR <= self.grau_dor <= LIMITE_SUPERIOR_DOR):
            raise ValueError(
                f"Grau de dor recusado ({self.grau_dor}). "
                f"O valor admitido vai de {LIMITE_INFERIOR_DOR} a {LIMITE_SUPERIOR_DOR}."
            )

    def __repr__(self) -> str:
        return (f"FichaEnfermo(id={self.identificador}, nome={self.nome_paciente!r}, "
                f"dor={self.grau_dor})")


# =============================================================================
# ESTRUTURA DE PRIORIDADE (HEAP MÁXIMA) PARA ENFERMOS
# =============================================================================

class CentralAtendimento:
    """Central de prioridade modelada como Heap Máxima de fichas de enfermos.

    A ordem de atendimento decorre de uma chave dupla:
        (grau_dor desc, sequencia_entrada asc)
    Quem possui dor mais elevada é atendido antes; em situações de empate,
    a precedência é de quem entrou primeiro na central.

    Sustenta também uma estrutura ``_tabela_indice`` que vincula cada
    ``identificador`` à posição atual ocupada pelo enfermo no heap.
    Graças a ela, a rotina ``atualizar_prioridade`` se encerra em O(log n).
    """

    def __init__(self) -> None:
        """Constrói a central sem qualquer enfermo aguardando."""
        self._estrutura_heap: list[FichaEnfermo] = []
        self._tabela_indice: dict[int, int] = {}

    # -------------------------------------------------------------------------
    # Operações que apenas leem dados
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._estrutura_heap)

    def central_sem_enfermos(self) -> bool:
        """Informa se nenhum enfermo está aguardando atendimento."""
        return len(self._estrutura_heap) == 0

    def observar_proximo(self) -> Optional[FichaEnfermo]:
        """Mostra (porém não retira) o enfermo de maior prioridade no momento.

        Custo computacional: O(1).

        Returns:
            A ficha do próximo a ser atendido, ou None se nada houver na central.
        """
        return self._estrutura_heap[0] if self._estrutura_heap else None

    # -------------------------------------------------------------------------
    # Operações que mudam o conteúdo da central
    # -------------------------------------------------------------------------

    def inscrever(self, ficha: FichaEnfermo) -> None:
        """Acrescenta uma ficha de enfermo à central.

        Custo computacional: O(log n).

        Args:
            ficha: Dados do enfermo que está sendo inscrito.
        """
        self._estrutura_heap.append(ficha)
        local_inicial = len(self._estrutura_heap) - 1
        self._tabela_indice[ficha.identificador] = local_inicial
        self._promover(local_inicial)

    def encaminhar(self) -> FichaEnfermo:
        """Extrai e devolve a ficha de maior prioridade (situada na raiz).

        Custo computacional: O(log n).

        Returns:
            Ficha do enfermo encaminhado para atendimento.

        Raises:
            IndexError: Caso não exista nenhum enfermo na central.
        """
        if not self._estrutura_heap:
            raise IndexError("Não há enfermos aguardando na central.")

        ficha_da_raiz = self._estrutura_heap[0]
        ficha_da_cauda = self._estrutura_heap.pop()
        del self._tabela_indice[ficha_da_raiz.identificador]

        if self._estrutura_heap:
            # Reposiciona a ficha da cauda na raiz e restaura a propriedade.
            self._estrutura_heap[0] = ficha_da_cauda
            self._tabela_indice[ficha_da_cauda.identificador] = 0
            self._rebaixar(0)

        return ficha_da_raiz

    def atualizar_prioridade(self, identificador: int, grau_dor_revisto: int) -> None:
        """Atualiza o grau de dor de um enfermo já inscrito na central.

        Esta única rotina concentra o comportamento de:
            - Increase-Key: grau_dor_revisto > grau_dor anterior  =>  promove
            - Decrease-Key: grau_dor_revisto < grau_dor anterior  =>  rebaixa

        Custo computacional:
            - Localização do enfermo : O(1)  (graças à tabela de índice)
            - Restauração do heap    : O(log n)
            - Custo total            : O(log n)

        Caso a tabela auxiliar não existisse, a localização passaria a
        custar O(n) por inspeção sequencial, dominando o custo total —
        a restauração permaneceria O(log n), porém perderia destaque.

        Args:
            identificador: Identificador único do enfermo a ser atualizado.
            grau_dor_revisto: Novo grau de dor (1 a 10).

        Raises:
            KeyError: Caso o enfermo não esteja registrado na central.
            ValueError: Caso ``grau_dor_revisto`` esteja fora do permitido.
        """
        if not (LIMITE_INFERIOR_DOR <= grau_dor_revisto <= LIMITE_SUPERIOR_DOR):
            raise ValueError(
                f"Grau de dor recusado ({grau_dor_revisto}). "
                f"O valor admitido vai de {LIMITE_INFERIOR_DOR} a {LIMITE_SUPERIOR_DOR}."
            )

        if identificador not in self._tabela_indice:
            raise KeyError(
                f"Enfermo id={identificador} não está cadastrado na central."
            )

        local_corrente = self._tabela_indice[identificador]
        grau_dor_prévio = self._estrutura_heap[local_corrente].grau_dor
        self._estrutura_heap[local_corrente].grau_dor = grau_dor_revisto

        # Direciona o reequilíbrio para o lado adequado conforme a mudança.
        if grau_dor_revisto > grau_dor_prévio:
            self._promover(local_corrente)
        elif grau_dor_revisto < grau_dor_prévio:
            self._rebaixar(local_corrente)

    # -------------------------------------------------------------------------
    # Mecanismos internos que sustentam a heap
    # -------------------------------------------------------------------------

    @staticmethod
    def _calcular_chave(ficha: FichaEnfermo) -> tuple[int, int]:
        """Monta a chave que ordena as prioridades (valor maior vence).

        Numa Heap Máxima desejamos que a MAIOR dor fique no topo e que,
        em caso de empate, vença a MENOR sequencia_entrada. Como Python
        confronta tuplas posição a posição, basta retornar
        ``-sequencia_entrada`` para que o critério "maior vence" funcione
        também no desempate.
        """
        return (ficha.grau_dor, -ficha.sequencia_entrada)

    def _eleger_mais_prioritario(self, local_a: int, local_b: int) -> int:
        """Indica qual entre dois locais abriga o enfermo de maior prioridade."""
        if self._calcular_chave(self._estrutura_heap[local_a]) >= \
                self._calcular_chave(self._estrutura_heap[local_b]):
            return local_a
        return local_b

    def _alternar_posicoes(self, local_a: int, local_b: int) -> None:
        """Inverte duas fichas no heap e sincroniza a tabela de índice."""
        self._estrutura_heap[local_a], self._estrutura_heap[local_b] = \
            self._estrutura_heap[local_b], self._estrutura_heap[local_a]
        self._tabela_indice[self._estrutura_heap[local_a].identificador] = local_a
        self._tabela_indice[self._estrutura_heap[local_b].identificador] = local_b

    def _promover(self, local: int) -> None:
        """Faz um nó subir até que a propriedade da Heap Máxima volte a valer.

        Custo computacional: O(log n).
        """
        while local > 0:
            local_progenitor = (local - 1) // 2
            # Sobe enquanto for mais prioritário do que seu progenitor.
            if self._calcular_chave(self._estrutura_heap[local]) > \
                    self._calcular_chave(self._estrutura_heap[local_progenitor]):
                self._alternar_posicoes(local, local_progenitor)
                local = local_progenitor
            else:
                break

    def _rebaixar(self, local: int) -> None:
        """Faz um nó descer até que a propriedade da Heap Máxima volte a valer.

        Custo computacional: O(log n).
        """
        quantidade = len(self._estrutura_heap)
        while True:
            descendente_esq = 2 * local + 1
            descendente_dir = 2 * local + 2
            escolhido = local

            # Confronta o nó atual com cada um dos descendentes disponíveis.
            if descendente_esq < quantidade:
                escolhido = self._eleger_mais_prioritario(escolhido, descendente_esq)
            if descendente_dir < quantidade:
                escolhido = self._eleger_mais_prioritario(escolhido, descendente_dir)

            # Quando nenhum descendente supera o pai, a propriedade já vale.
            if escolhido == local:
                break

            self._alternar_posicoes(local, escolhido)
            local = escolhido


# =============================================================================
# EXIBIÇÃO PRÁTICA
# =============================================================================

def exibir_cenario_central() -> None:
    """Reproduz um caso de uso completo da central de atendimento."""
    print("=" * 60)
    print("PRONTO-SOCORRO — CENTRAL DE ATENDIMENTO (Heap Máxima)")
    print("=" * 60)

    listagem_inicial = [
        ("Ana",     4),
        ("Bruno",   9),
        ("Carla",   2),
        ("Daniel",  7),
        ("Eduarda", 9),
        ("Felipe",  5),
    ]

    central = CentralAtendimento()

    print("\n[1] Entrada dos enfermos na central:")
    for marca_temporal, (nome, dor) in enumerate(listagem_inicial, start=1):
        ficha_nova = FichaEnfermo(
            identificador=marca_temporal,
            nome_paciente=nome,
            grau_dor=dor,
            sequencia_entrada=marca_temporal,
        )
        central.inscrever(ficha_nova)
        print(f"  -> entrou {ficha_nova}")

    print(f"\n[2] Próximo a ser chamado: {central.observar_proximo()}")

    print("\n[3] Atualização de prioridade:")
    print("    Carla (id=3) teve piora no quadro — dor saltou para 10.")
    central.atualizar_prioridade(identificador=3, grau_dor_revisto=10)
    print(f"    Próximo agora: {central.observar_proximo()}")

    print("\n    Bruno (id=2) recebeu analgésico e a dor caiu para 3.")
    central.atualizar_prioridade(identificador=2, grau_dor_revisto=3)
    print(f"    Próximo agora: {central.observar_proximo()}")

    print("\n[4] Ordem definitiva de chamada:")
    numero_chamada = 1
    while not central.central_sem_enfermos():
        ficha_chamada = central.encaminhar()
        print(f"  {numero_chamada:>2}º -> {ficha_chamada}")
        numero_chamada += 1


def exibir_resumo_custos() -> None:
    """Apresenta um quadro consolidado com os custos de cada rotina."""
    print("\n" + "=" * 60)
    print("QUADRO DE CUSTOS COMPUTACIONAIS")
    print("=" * 60)
    quadro_resumo = [
        ("inscrever(ficha)",                      "O(log n)"),
        ("encaminhar()  [extract-max]",           "O(log n)"),
        ("observar_proximo()  [peek]",            "O(1)"),
        ("atualizar_prioridade()  com tabela",    "O(log n)"),
        ("atualizar_prioridade()  sem tabela",    "O(n)  — busca domina"),
        ("construção em lote (heapify)",          "O(n)"),
    ]
    for nome_rotina, custo_calculado in quadro_resumo:
        print(f"  {nome_rotina:<40} -> {custo_calculado}")

    print(
        "\nPapel da tabela de índice:\n"
        "  Sem essa tabela, achar uma ficha qualquer dentro do vetor que\n"
        "  sustenta a heap exige percorrimento linear O(n). Quando o mapa\n"
        "  identificador -> índice é atualizado em toda alternância\n"
        "  (sift-up/sift-down), a atualização passa a ser regida pela\n"
        "  restauração do heap, fechando em O(log n) — desempenho idêntico\n"
        "  ao de Decrease/Increase-Key nas heaps binárias tradicionais."
    )


def executar() -> None:
    """Função inicial — dispara as duas apresentações."""
    exibir_cenario_central()
    exibir_resumo_custos()


if __name__ == "__main__":
    executar()