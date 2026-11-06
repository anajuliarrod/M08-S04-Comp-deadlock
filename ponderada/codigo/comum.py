"""Utilitários compartilhados pelas três versões da questão A4.

Concentra os parâmetros individuais, a contagem de amostras consumidas,
perdidas e duplicadas e a execução repetida de cada versão, para que os
arquivos versao1.py, versao2.py e versao3.py contenham apenas a lógica
de produtor e consumidor.
"""

import argparse
import time
from collections import Counter
from dataclasses import dataclass

N = 7
AMOSTRAS = 20_000
EXECUCOES = 3
LIMITE_TRAVAMENTO_S = 1.0


@dataclass
class Resultado:
    """Medidas de uma execução.

    Atributos:
        consumidas: total de leituras feitas pelo consumidor.
        perdidas: amostras produzíveis que o consumidor nunca recebeu.
        duplicadas: leituras repetidas de uma amostra já recebida.
        invalidas: leituras de posições que ainda não tinham amostra.
        travou: True se o consumidor ficou 1 s sem receber nada.
        duracao_s: tempo total da execução, em segundos.
    """

    consumidas: int
    perdidas: int
    duplicadas: int
    invalidas: int
    travou: bool
    duracao_s: float


def apurar(lidas, total, travou, duracao_s):
    """Compara as leituras do consumidor com as amostras esperadas.

    Parâmetros:
        lidas: lista com cada valor lido, na ordem de leitura. O valor -1
            indica uma posição do buffer que nunca foi escrita.
        total: quantidade de amostras esperadas (numeradas de 0 a total-1).
        travou: indica se a execução terminou por travamento.
        duracao_s: duração da execução, em segundos.

    Retorno:
        Um Resultado com as contagens da execução.
    """
    contagem = Counter(valor for valor in lidas if valor >= 0)
    return Resultado(
        consumidas=len(lidas),
        perdidas=sum(1 for amostra in range(total) if amostra not in contagem),
        duplicadas=sum(vezes - 1 for vezes in contagem.values()),
        invalidas=sum(1 for valor in lidas if valor < 0),
        travou=travou,
        duracao_s=duracao_s,
    )


def ler_argumentos():
    """Lê as opções de linha de comando.

    Retorno:
        Um argparse.Namespace com os campos amostras e execucoes. Sem
        opções, valem os padrões do enunciado: 20.000 amostras, 3 execuções.
    """
    analisador = argparse.ArgumentParser(
        description="Produtor e consumidor com buffer circular."
    )
    analisador.add_argument("--amostras", type=int, default=AMOSTRAS)
    analisador.add_argument("--execucoes", type=int, default=EXECUCOES)
    return analisador.parse_args()


def rodar_versao(titulo, executar):
    """Roda uma versão várias vezes e imprime a tabela de resultados.

    Parâmetros:
        titulo: nome da versão, mostrado no cabeçalho da saída.
        executar: função que recebe o total de amostras e devolve a
            tupla (lidas, travou) de uma execução.

    Retorno:
        None. Os resultados são impressos na saída padrão.
    """
    argumentos = ler_argumentos()
    print(f"{titulo} | N = {N} | {argumentos.amostras} amostras")
    print(
        f"{'exec':>4} {'consumidas':>10} {'perdidas':>8} {'duplicadas':>10} "
        f"{'invalidas':>9} {'travou':>6} {'tempo(s)':>8}"
    )
    for numero in range(1, argumentos.execucoes + 1):
        inicio = time.monotonic()
        lidas, travou = executar(argumentos.amostras)
        duracao_s = time.monotonic() - inicio
        r = apurar(lidas, argumentos.amostras, travou, duracao_s)
        print(
            f"{numero:>4} {r.consumidas:>10} {r.perdidas:>8} {r.duplicadas:>10} "
            f"{r.invalidas:>9} {'sim' if r.travou else 'não':>6} "
            f"{r.duracao_s:>8.2f}"
        )
