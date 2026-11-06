"""Questão A4, versão 3: igual à versão 2, com a ordem do produtor trocada.

O produtor faz wait(mutex) antes de wait(vazio). Quando o buffer enche, ele
dorme segurando o mutex e o consumidor não consegue mais liberar posições.

Uso: python3 versao3.py [--amostras 20000] [--execucoes 3]
"""

import threading
import time

from comum import N, rodar_versao
from versao2 import Estado, consumidor, esperar_ou_parar


def produtor(estado, total):
    """Gera as amostras 0 a total-1: wait(mutex), depois wait(vazio).

    Parâmetros:
        estado: dados compartilhados.
        total: quantidade de amostras a produzir.

    Retorno:
        None. Encerra antes do fim se estado.parar for ligado.
    """
    entrada = 0
    for amostra in range(total):
        if not esperar_ou_parar(estado, estado.mutex):
            return
        if not esperar_ou_parar(estado, estado.vazio):
            return
        estado.buffer[entrada] = amostra
        entrada = (entrada + 1) % N
        lido = estado.ocupadas
        time.sleep(0)
        estado.ocupadas = lido + 1
        estado.mutex.release()
        estado.cheio.release()


def executar(total):
    """Roda uma execução completa da versão 3.

    Parâmetros:
        total: quantidade de amostras da execução.

    Retorno:
        Tupla (lidas, travou) com os valores lidos e o estado de travamento.
    """
    estado = Estado()
    lidas = []
    thread = threading.Thread(target=produtor, args=(estado, total))
    thread.start()
    travou = consumidor(estado, total, lidas)
    estado.parar = True
    thread.join()
    return lidas, travou


if __name__ == "__main__":
    rodar_versao("Versão 3: ordem trocada no produtor", executar)
